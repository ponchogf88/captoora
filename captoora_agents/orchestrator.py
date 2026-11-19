"""10-Agent Orchestrator built with Google Antigravity SDK ('One Job Per Bot' + Zero-Quota Local Engine)."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from typing import Any

from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.triggers import TriggerContext, every

from . import ROOT_DIR
from .config import FILES, append_agent_event, read_json, set_agent_runtime_status
from .marketing_hub import run_local_marketing_mission
from .safety_and_hooks import CURRENT_ACTOR, build_agent_hooks, build_security_policies
from .schemas import AgentMissionOutput
from .tools import (
    assign_conan_creative_brief,
    audit_contract_clauses,
    calculate_package_financials,
    create_asana_task,
    enqueue_human_trigger,
    generate_subscription_content_plan,
    get_portfolio_highlights,
    list_asana_tasks,
    prepare_lupe_social_post,
    read_verified_leads,
    update_asana_task_status,
)
from .usage_tracker import get_usage_summary, record_sdk_usage

SPECIALIST_DEFS: dict[str, dict[str, Any]] = {
    "scouting_radar": {
        "description": "Extrae y prioriza prospectos de temporada Nov-Dic (Pádel, Danza, CrossFit) en San Pedro y Monterrey.",
        "system_instructions": (
            "Eres Bot 2 (Scouting & Radar NL) de Captoora Sports en San Jerónimo, Monterrey. "
            "Tu ÚNICA responsabilidad es inspeccionar leads en apify_scraped_leads.json, priorizar los clubes de Pádel "
            "con mayor probabilidad de Torneo del Pavo / Posada y las academias de Danza con Gala Navideña, y actualizar "
            "su estado en el tablero Asana. Nunca redactas ventas ni prometes contacto directo."
        ),
        "tools": [read_verified_leads, list_asana_tasks, update_asana_task_status],
        "default_prompt": "Revisa los leads de Pádel & Raqueta y Baile & Danza Señoras y reporta el Top 5 prioritario para hoy.",
    },
    "embudo_marketing": {
        "description": "Diseña estrategias del Embudo Invisible (autofinanciables por sponsor o preventa White-Glove) sin imposición.",
        "system_instructions": (
            "Eres Bot 3 (Marketing & Embudo Invisible) de Captoora Sports. Tu ÚNICA misión es estructurar ofertas donde "
            "el cliente perciba inversión de estatus y riesgo cero (ej. Torneo del Pavo pagado por patrocinador con acrílicos "
            "ópticos iluminados con luz LED cálida, o Galas pagadas por preventa de marcos de El Marco San Pedro). "
            "REGLAS INQUEBRANTABLES en cualquier texto hacia clientes: JAMÁS mencionar IA/Inteligencia Artificial, "
            "JAMÁS usar la palabra 'presumir', usar 'proyectar en redes sociales una imagen profesional al nivel de excelencia "
            "de su club', e incluir nota sutil de taller local (3 a 5 días hábiles para piezas físicas). Encola propuestas vía enqueue_human_trigger."
        ),
        "tools": [read_verified_leads, calculate_package_financials, enqueue_human_trigger, list_asana_tasks],
        "default_prompt": "Prepara una propuesta del Embudo Invisible enfocada en academias de danza o clubes de pádel lista en la cola de aprobación.",
    },
    "social_content": {
        "description": "Redacta guiones 9:16 y captions para @captoora mostrando entrega el mismo día y acrílicos LED.",
        "system_instructions": (
            "Eres Bot 4 (Redes Sociales & Marca @captoora). Tu ÚNICA tarea es redactar guiones breves de Reels/Stories 9:16 "
            "y captions elegantes enfocados en estatus deportivo de San Pedro y Monterrey, apoyados en el portafolio real. "
            "JAMÁS menciones IA ni uses el verbo 'presumir'. Destaca la entrega el mismo día y las piezas en acrílico "
            "óptico iluminadas con luz LED cálida (con nota fina de 3 a 5 días hábiles en taller). Encola borradores vía enqueue_human_trigger."
        ),
        "tools": [get_portfolio_highlights, enqueue_human_trigger, list_asana_tasks],
        "default_prompt": "Crea 1 guión corto de Reel o post de LinkedIn B2B sobre trofeos iluminados LED y entrega el mismo día, y encólalo para Trigger.",
    },
    "ventas_outreach": {
        "description": "Redacta borradores hiper-personalizados de WhatsApp/Pixieset para cerrar el primer 'Sí' en 72 horas.",
        "system_instructions": (
            "Eres Bot 5 (Ventas B2B & Cierre 3 Días) de Captoora Sports. Tu ÚNICA función es redactar mensajes diagnósticos "
            "personalizados por WhatsApp o email para los leads verificados, sin vender agresivamente ('Caballo de Troya'). "
            "REGLAS ESTRICTAS: Nunca envíes mensajes por tu cuenta; usa SIEMPRE enqueue_human_trigger para dejar cada "
            "borrador en 'pending_trigger'. Prohibido mencionar 'IA' o 'presumir'. Siempre separa entrega digital mismo día "
            "de manufactura en taller (3 a 5 días hábiles) cuando menciones acrílicos LED o marcos."
        ),
        "tools": [read_verified_leads, calculate_package_financials, enqueue_human_trigger, list_asana_tasks, update_asana_task_status],
        "default_prompt": "Selecciona 1 lead de Pádel o Danza que aún no tenga borrador pendiente y genera su mensaje diagnóstico personalizado en la cola de Último Trigger.",
    },
    "contabilidad_finanzas": {
        "description": "Audita márgenes netos (>=70%), anticipos 50/50, costos de proveedores y suscripciones/CFDI.",
        "system_instructions": (
            "Eres Bot 6 (Contabilidad, Cotizaciones & Margen) de Captoora Sports. Tu ÚNICA responsabilidad es verificar que "
            "toda cotización conserve margen sano (>=70%), cobre 50% de anticipo obligatorio al reservar fecha y 50% contra "
            "entrega digital, monitorear costos de El Marco San Pedro / Foco Lab / Promocionales MTY y suscripciones (Pixieset, Apify)."
        ),
        "tools": [calculate_package_financials, list_asana_tasks, update_asana_task_status],
        "default_prompt": "Verifica la rentabilidad de los paquetes de temporada PKG-4 y PKG-5 y reporta el margen neto y anticipo 50% requerido.",
    },
    "ops_talleres_legal": {
        "description": "Coordina SLAs (Halftime Blitz mismo día vs taller LED 3-5 días) y audita cláusulas contractuales.",
        "system_instructions": (
            "Eres Bot 7 (Operaciones, Talleres LED & Legal) de Captoora Sports. Tu ÚNICA responsabilidad es proteger los SLAs "
            "(entrega digital 15 min / mismo día bajo control Captoora vs 3 a 5 días hábiles en talleres locales) y revisar "
            "cláusulas de contratos contra focos rojos (derechos morales, pago 50/50, riesgo deportivo)."
        ),
        "tools": [audit_contract_clauses, list_asana_tasks, update_asana_task_status, enqueue_human_trigger],
        "default_prompt": "Audita las condiciones operativas estándar para eventos de Nov-Dic y confirma que las notas de taller LED 3-5 días estén protegidas.",
    },
    "marky_marketing": {
        "description": "Director de Marketing: dirige a Lupe y Conan, plan de contenido multired y sincronía de suscripciones sin Grokbot.",
        "system_instructions": (
            "Eres Bot 8 (Marky · Director de Marketing & Estrategia) de Captoora Studio, revivido nativamente en localhost sin cuotas Grokbot. "
            "Lideras a Lupe (redes/captions/mensajes) y Conan (creación de contenido con suscripciones: OpusClip Pro urgente por vencer, "
            "Captions, Canva, Aftershoot, Evoto, CapCut, 2x Google AI Pro Principal+Yari y Meta Muse móvil). "
            "Coordina campañas en los 4 Caminos (-35% Navidad, Gimnasios TotalPass, Biogen Beta, Small Business 2027), "
            "asigna briefs a Conan y actualiza el plan semanal sin jamás mencionar IA ni usar 'presumir'."
        ),
        "tools": [
            generate_subscription_content_plan,
            assign_conan_creative_brief,
            read_verified_leads,
            list_asana_tasks,
            create_asana_task,
        ],
        "default_prompt": "Actualiza el plan semanal de contenido para exprimir OpusClip Pro antes de vencer, reparte tareas entre Conan y Lupe y sincroniza el Brief de Bolsillo para Muse.",
    },
    "lupe_social": {
        "description": "Community & Social Media: programa IG/FB Meta Business Suite, TikTok, LinkedIn, captions y respuestas DM.",
        "system_instructions": (
            "Eres Bot 9 (Lupe · Redes Sociales, Meta Business Suite & Community Manager) bajo dirección de Marky. "
            "Tu misión es preparar y programar publicaciones para Meta Business Suite (Facebook + Instagram + WhatsApp Business), TikTok y LinkedIn, "
            "redactar captions magnéticos, hashtags locales NL y respuestas humanas a mensajes/DMs. "
            "REGLAS INQUEBRANTABLES: JAMÁS mencionar IA/Inteligencia Artificial ni 'presumir'; separar entrega digital mismo día/48h de taller LED 3–5 días hábiles; "
            "siempre encolar borradores en Último Trigger vía prepare_lupe_social_post."
        ),
        "tools": [prepare_lupe_social_post, get_portfolio_highlights, list_asana_tasks],
        "default_prompt": "Prepara y encola la siguiente publicación multired (Meta Business Suite, TikTok o LinkedIn) con caption validado para Último Trigger.",
    },
    "conan_content": {
        "description": "Creador de Contenido: ejecuta piezas para Lupe usando OpusClip Pro, Captions, Canva, Aftershoot, Evoto, CapCut y motor local.",
        "system_instructions": (
            "Eres Bot 10 (Conan · Creación de Contenido & Suite Creativa) bajo dirección de Marky, produciendo piezas para Lupe. "
            "Exprime al máximo las suscripciones del usuario sin depender de Grokbot: OpusClip Pro (urgente rescatar 25–30 clips), "
            "Captions (talking-head), Canva (carruseles 4:5), Aftershoot (culling rápido), Evoto (Biogen Beta), CapCut (9:16), "
            "2da cuota Google AI Pro Yari y motor local Chromium/WeasyPrint. Documenta briefs listos en Asana vía assign_conan_creative_brief."
        ),
        "tools": [assign_conan_creative_brief, get_portfolio_highlights, generate_subscription_content_plan, list_asana_tasks],
        "default_prompt": "Genera el brief operativo de producción en OpusClip Pro + Captions/Canva para entregar reels 9:16 y carruseles listos a Lupe.",
    },
}

CHIEF_INSTRUCTIONS = (
    "Eres Bot 1 (Director de Orquesta / Chief of Staff) de Captoora Sports en San Jerónimo, Monterrey. "
    "Tu misión crítica es que el negocio logre su PRIMER 'SÍ' antes del vencimiento del Sprint de cierre. "
    "Coordina a tus 9 subagentes especializados (scouting_radar, embudo_marketing, social_content, ventas_outreach, "
    "contabilidad_finanzas, ops_talleres_legal, y la célula de Marketing revivida sin Grokbot: marky_marketing -> lupe_social + conan_content). "
    "Mantén cada subagente enfocado en su única tarea, delega cuando corresponda, actualiza el tablero Asana y garantiza "
    "que toda comunicación externa o cotización quede estacionada en la cola de Último Trigger para aprobación humana."
)


_SPECIALIST_DISABLED_TOOLS = [
    "run_command",
    "create_file",
    "edit_file",
    "ask_question",
    "run_workflow",
    "generate_image",
    "schedule",
    "list_directory",
    "search_directory",
    "find_file",
    "view_file",
    "invoke_subagent",
]


def _build_subagent_configs() -> list[types.SubagentConfig]:
    """Construct all 6 single-responsibility SubagentConfig objects."""
    configs: list[types.SubagentConfig] = []
    for name, spec in SPECIALIST_DEFS.items():
        configs.append(
            types.SubagentConfig(
                name=name,
                description=spec["description"],
                system_instructions=spec["system_instructions"],
                tools=spec["tools"],
                capabilities=types.SubagentCapabilities(
                    agent_behavior=types.AgentBehavior.AUTONOMOUS,
                    disabled_tools=_SPECIALIST_DISABLED_TOOLS,
                ),
            )
        )
    return configs


def build_agent_config(agent_id: str, triggers: list | None = None) -> LocalAgentConfig:
    """Create a LocalAgentConfig tailored either to the Chief of Staff or a specific single-job specialist."""
    policies = build_security_policies()
    hooks = build_agent_hooks()
    app_data_dir = str(ROOT_DIR / ".antigravity_state")

    if agent_id == "chief_of_staff":
        subagents = _build_subagent_configs()
        return LocalAgentConfig(
            system_instructions=CHIEF_INSTRUCTIONS,
            tools=[
                list_asana_tasks,
                create_asana_task,
                update_asana_task_status,
                read_verified_leads,
                calculate_package_financials,
                enqueue_human_trigger,
            ],
            subagents=subagents,
            capabilities=types.CapabilitiesConfig(
                enable_subagents=True,
                max_subagent_depth=1,
                allowed_subagents=list(SPECIALIST_DEFS.keys()),
                agent_behavior=types.AgentBehavior.AUTONOMOUS,
                disabled_tools=["run_command", "create_file", "edit_file", "ask_question", "run_workflow"],
            ),
            workspaces=[str(ROOT_DIR)],
            policies=policies,
            hooks=hooks,
            triggers=triggers or [],
            budget_config=types.BudgetConfig(max_model_calls=8, max_tool_calls=12),
            response_schema=AgentMissionOutput,
            app_data_dir=app_data_dir,
        )

    if agent_id not in SPECIALIST_DEFS:
        raise ValueError(f"Agente desconocido: '{agent_id}'.")

    spec = SPECIALIST_DEFS[agent_id]
    return LocalAgentConfig(
        system_instructions=(
            spec["system_instructions"]
            + " Usa directamente tus herramientas de dominio asignadas sin explorar directorios ni invocar otros agentes."
        ),
        tools=spec["tools"],
        capabilities=types.CapabilitiesConfig(
            enable_subagents=False,
            agent_behavior=types.AgentBehavior.AUTONOMOUS,
            disabled_tools=_SPECIALIST_DISABLED_TOOLS,
        ),
        workspaces=[str(ROOT_DIR)],
        policies=policies,
        hooks=hooks,
        triggers=triggers or [],
        budget_config=types.BudgetConfig(max_model_calls=5, max_tool_calls=8),
        response_schema=AgentMissionOutput,
        app_data_dir=app_data_dir,
    )


async def run_agent_mission(
    agent_id: str,
    instruction: str | None = None,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Execute one agent mission either via live Google Antigravity SDK or deterministic dry-run."""
    valid_ids = {"chief_of_staff", *SPECIALIST_DEFS.keys()}
    if agent_id not in valid_ids:
        raise ValueError(f"Agente '{agent_id}' no existe. Opciones: {sorted(valid_ids)}")

    usage_limits = (get_usage_summary() or {}).get("limits", {})
    prefer_zero_token = bool(usage_limits.get("dry_run_preferred"))
    is_marketing_trio = agent_id in ("marky_marketing", "lupe_social", "conan_content")

    if dry_run or prefer_zero_token or (is_marketing_trio and not os.environ.get("GEMINI_API_KEY")):
        if is_marketing_trio:
            return run_local_marketing_mission(agent_id, instruction)
        set_agent_runtime_status(agent_id, "ready")
        asana = read_json(FILES["asana"], default={"tasks": []})
        queue = read_json(FILES["approvals"], default={"items": []})
        pending = [i for i in queue.get("items", []) if i.get("status") == "pending_trigger"]
        event = append_agent_event(
            agent_id,
            "Verificación Dry-Run",
            f"Validó {len(asana.get('tasks', []))} tareas Asana y {len(pending)} triggers pendientes (sin consumo Gemini).",
            source="dry_run",
        )
        return {
            "mode": "dry_run",
            "agent_id": agent_id,
            "tasks_count": len(asana.get("tasks", [])),
            "pending_triggers": len(pending),
            "event": event,
        }

    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError(
            "GEMINI_API_KEY no está configurada en el entorno. "
            "Puedes usar a Marky/Lupe/Conan o activar 'Modo Cero Tokens' sin consumir cuota externa."
        )

    prompt = instruction or (
        "Revisa el estado actual del tablero Asana y la cola de aprobación. Coordina prioridades para lograr el primer 'Sí' dentro del Sprint de 72 horas y reporta el siguiente paso concreto."
        if agent_id == "chief_of_staff"
        else SPECIALIST_DEFS[agent_id]["default_prompt"]
    )

    set_agent_runtime_status(agent_id, "running")
    append_agent_event(
        agent_id,
        "Inició Misión SDK",
        prompt[:180],
        source="sdk_real",
    )

    token = CURRENT_ACTOR.set(agent_id)
    try:
        config = build_agent_config(agent_id)
        async with Agent(config) as agent:
            response = await agent.chat(prompt)
            structured = await response.structured_output()
            raw_text = await response.text() if structured is None else json.dumps(structured, ensure_ascii=False)
            try:
                usage_meta = await response.usage_metadata()
                record_sdk_usage(agent_id, usage_meta)
            except Exception:
                pass
            queue = read_json(FILES["approvals"], default={"items": []})
            has_waiting = any(
                i.get("agent_id") == agent_id and i.get("status") == "pending_trigger"
                for i in queue.get("items", [])
            )
            set_agent_runtime_status(agent_id, "waiting_trigger" if has_waiting else "ready")
            summary_line = (structured or {}).get("summary") or raw_text[:180]
            append_agent_event(
                agent_id,
                "Finalizó Misión SDK",
                summary_line,
                source="sdk_real",
            )
            return {
                "mode": "sdk_real",
                "agent_id": agent_id,
                "output": structured or {"summary": raw_text},
            }
    except Exception as exc:
        set_agent_runtime_status(agent_id, "ready")
        append_agent_event(
            agent_id,
            "Error en Misión",
            str(exc)[:180],
            source="sdk_error",
        )
        raise
    finally:
        CURRENT_ACTOR.reset(token)


def build_scheduled_chief(interval_seconds: int = 14400) -> LocalAgentConfig:
    """Optional scheduled daemon configuration using Google Antigravity's every() trigger."""

    async def scheduled_sprint_check(ctx: TriggerContext) -> None:
        await ctx.send(
            "Revisa la cola de aprobación pendiente y tareas del Sprint 72h sin enviar ningún mensaje por tu cuenta."
        )

    return build_agent_config("chief_of_staff", triggers=[every(interval_seconds, scheduled_sprint_check)])


def main() -> None:
    parser = argparse.ArgumentParser(description="Orquestador de los 10 Agentes Captoora Sports & Marketing.")
    parser.add_argument(
        "--agent",
        default="chief_of_staff",
        help=(
            "ID del agente a ejecutar (chief_of_staff, scouting_radar, embudo_marketing, social_content, "
            "ventas_outreach, contabilidad_finanzas, ops_talleres_legal, marky_marketing, lupe_social, conan_content)."
        ),
    )
    parser.add_argument("--instruction", default=None, help="Instrucción específica para el agente.")
    parser.add_argument("--dry-run", action="store_true", help="Valida estado local / ejecuta sin llamar API externa.")
    args = parser.parse_args()

    result = asyncio.run(run_agent_mission(args.agent, args.instruction, dry_run=args.dry_run))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
