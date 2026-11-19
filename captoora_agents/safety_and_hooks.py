"""Safety policies and Google Antigravity SDK hooks enforcing Human Approval Trigger and brand copy rules."""

from __future__ import annotations

from contextvars import ContextVar

from google.antigravity import types
from google.antigravity.hooks import hooks, policy

from .config import ROOT_DIR, append_agent_event, validate_client_copy

CURRENT_ACTOR: ContextVar[str | None] = ContextVar("captoora_current_actor", default=None)

_TOOL_TO_AGENT = {
    "read_verified_leads": "scouting_radar",
    "list_asana_tasks": "chief_of_staff",
    "update_asana_task_status": "chief_of_staff",
    "create_asana_task": "chief_of_staff",
    "calculate_package_financials": "contabilidad_finanzas",
    "audit_contract_clauses": "ops_talleres_legal",
    "get_portfolio_highlights": "social_content",
    "enqueue_human_trigger": "ventas_outreach",
    "generate_subscription_content_plan": "marky_marketing",
    "prepare_lupe_social_post": "lupe_social",
    "assign_conan_creative_brief": "conan_content",
    "invoke_subagent": "chief_of_staff",
}


def build_security_policies() -> list:
    """Deny by default (blocking run_command and direct file writes) and allow Captoora domain tools."""
    return [
        policy.deny_all(),
        policy.deny("run_command"),
        policy.deny("create_file"),
        policy.deny("edit_file"),
        policy.allow("read_verified_leads"),
        policy.allow("list_asana_tasks"),
        policy.allow("update_asana_task_status"),
        policy.allow("create_asana_task"),
        policy.allow("calculate_package_financials"),
        policy.allow("audit_contract_clauses"),
        policy.allow("get_portfolio_highlights"),
        policy.allow("enqueue_human_trigger"),
        policy.allow("generate_subscription_content_plan"),
        policy.allow("prepare_lupe_social_post"),
        policy.allow("assign_conan_creative_brief"),
        policy.allow("invoke_subagent"),
        policy.allow("search_web"),
        policy.allow("finish"),
    ]


@hooks.pre_tool_call_decide
async def pre_tool_guardrail(data: types.ToolCall) -> types.HookResult:
    """Log live tool call intent for the Studio HQ view and block prohibited client copy."""
    args = data.args or {}
    actor = str(
        args.get("agent_id")
        or CURRENT_ACTOR.get()
        or _TOOL_TO_AGENT.get(data.name, "chief_of_staff")
    )

    if data.name in ("enqueue_human_trigger", "prepare_lupe_social_post"):
        is_client_facing = True if data.name == "prepare_lupe_social_post" else bool(args.get("is_client_facing", True))
        draft_text = str(args.get("draft_text", ""))
        if is_client_facing:
            violations = validate_client_copy(draft_text)
            if violations:
                reason = "Guardrail Captoora bloqueó borrador: " + " | ".join(violations)
                append_agent_event(actor, "Bloqueo de Estilo", reason, source="sdk_hook")
                return types.HookResult(allow=False, message=reason)

    if data.name in ("start_subagent", "invoke_subagent"):
        sub_name = str(args.get("TypeName") or args.get("subagent_name") or args.get("name") or "especialista")
        if "Subagents" in args and isinstance(args["Subagents"], list) and args["Subagents"]:
            sub_name = ", ".join(str(s.get("TypeName", "bot")) for s in args["Subagents"])
        append_agent_event(
            "chief_of_staff",
            f"Delega a {sub_name}",
            "El Director de Orquesta asignó una subtarea en vivo.",
            target_agent=sub_name.split(",")[0].strip(),
            source="sdk_real",
        )
    else:
        append_agent_event(
            actor,
            f"Ejecuta {data.name}",
            str(args)[:180],
            source="sdk_real",
        )

    return types.HookResult(allow=True)


@hooks.post_tool_call
async def post_tool_logger(data) -> None:
    """Record tool completion signal in live studio log."""
    tool_name = getattr(data, "name", None) or "herramienta"
    actor = CURRENT_ACTOR.get() or _TOOL_TO_AGENT.get(tool_name, "chief_of_staff")
    append_agent_event(
        actor,
        f"Completó {tool_name}",
        "Resultado registrado en estado compartido.",
        source="sdk_real",
    )


def build_agent_hooks() -> list:
    """Return active SDK lifecycle hooks."""
    return [pre_tool_guardrail, post_tool_logger]
