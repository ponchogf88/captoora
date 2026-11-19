"""Domain-specific Python tools invoked by the 7 Captoora Sports agents."""

from __future__ import annotations

import json
import urllib.parse
from typing import Any

from .config import (
    FILES,
    append_agent_event,
    now_iso,
    read_json,
    validate_client_copy,
    write_json,
)


def read_verified_leads(niche: str = "all", limit: int = 12) -> str:
    """Read verified Apify/Google Maps leads in San Pedro Garza García and Monterrey.

    Args:
        niche: Optional filter such as 'Pádel & Raqueta', 'Baile & Danza Señoras',
            'Fitness & CrossFit', or 'all'.
        limit: Maximum number of lead records to return (default 12).
    """
    leads = read_json(FILES["leads"], default=[])
    if niche and niche.lower() != "all":
        leads = [l for l in leads if niche.lower() in (l.get("nicho") or "").lower()]
    leads = leads[: max(1, min(limit, 30))]
    append_agent_event(
        "scouting_radar",
        f"Consultó leads ({niche})",
        f"Extrajo {len(leads)} prospectos verificados de Apify para prospección.",
        target_agent="ventas_outreach",
    )
    return json.dumps(leads, ensure_ascii=False, indent=2)


def list_asana_tasks(project_id: str = "all", assigned_agent: str = "all") -> str:
    """List projects and tasks from Captoora's Asana tracker.

    Args:
        project_id: Filter by project ID or pass 'all'.
        assigned_agent: Filter by agent ID (e.g. 'ventas_outreach') or 'all'.
    """
    asana = read_json(FILES["asana"], default={"projects": [], "tasks": []})
    tasks = asana.get("tasks", [])
    if project_id and project_id != "all":
        tasks = [t for t in tasks if t.get("project_id") == project_id]
    if assigned_agent and assigned_agent != "all":
        tasks = [t for t in tasks if t.get("assigned_agent") == assigned_agent]
    return json.dumps(
        {"sprint": asana.get("sprint", {}), "projects": asana.get("projects", []), "tasks": tasks},
        ensure_ascii=False,
        indent=2,
    )


def update_asana_task_status(task_id: str, new_status: str, deliverable_ref: str = "") -> str:
    """Update an Asana task status and optional deliverable reference.

    Args:
        task_id: Task ID such as 'TASK-101'.
        new_status: One of 'backlog', 'in_progress', 'waiting_trigger', or 'done'.
        deliverable_ref: Optional reference to draft/deliverable (e.g. 'APR-007').
    """
    valid = {"backlog", "in_progress", "waiting_trigger", "done"}
    if new_status not in valid:
        return f"Error: status inválido '{new_status}'. Debe ser uno de {sorted(valid)}."

    asana = read_json(FILES["asana"], default={"projects": [], "tasks": []})
    for task in asana.get("tasks", []):
        if task.get("id") == task_id:
            task["status"] = new_status
            if deliverable_ref:
                task["deliverable_ref"] = deliverable_ref
            write_json(FILES["asana"], asana)
            append_agent_event(
                task.get("assigned_agent", "chief_of_staff"),
                f"Actualizó {task_id} -> {new_status}",
                task.get("title", ""),
                target_agent="chief_of_staff",
            )
            return f"OK: {task_id} actualizado a '{new_status}'."
    return f"Error: No se encontró la tarea '{task_id}'."


def create_asana_task(
    project_id: str,
    title: str,
    assigned_agent: str,
    priority: str = "Alta",
    due_label: str = "Sprint 72h",
) -> str:
    """Create a new task in the Asana project board.

    Args:
        project_id: Target project ID from projects_asana.json.
        title: Concise actionable task title in Spanish.
        assigned_agent: One of the 7 Captoora agent IDs.
        priority: Priority label ('Crítica', 'Alta', 'Media-Alta').
        due_label: Deadline tag ('Hoy', 'Día 2', 'Día 3', 'Semanal').
    """
    asana = read_json(FILES["asana"], default={"projects": [], "tasks": []})
    tasks = asana.get("tasks", [])
    existing_nums = [int(t["id"].split("-")[1]) for t in tasks if t.get("id", "").startswith("TASK-") and t["id"].split("-")[1].isdigit()]
    next_id = f"TASK-{max(existing_nums, default=600) + 1}"
    new_task = {
        "id": next_id,
        "project_id": project_id,
        "title": title,
        "assigned_agent": assigned_agent,
        "status": "in_progress",
        "priority": priority,
        "due_label": due_label,
        "depends_on": [],
        "deliverable_ref": "En preparación",
    }
    tasks.append(new_task)
    asana["tasks"] = tasks
    write_json(FILES["asana"], asana)
    append_agent_event(
        "chief_of_staff",
        f"Asignó {next_id}",
        f"Delegó a {assigned_agent}: {title}",
        target_agent=assigned_agent,
    )
    return json.dumps(new_task, ensure_ascii=False)


def calculate_package_financials(
    package_id: str = "PKG-4",
    discount_pct: float = 0.0,
    split_physical_later: bool = False,
    niche: str = "padel_gym",
) -> str:
    """Compute revenue, direct supplier cost, 50% advance, deferred split, net profit, and margin.

    Args:
        package_id: 'PKG-1'..'PKG-5', 'OPT-DIGITAL', 'OPT-PRINT', 'OPT-FULL-LED', 'BIOGEN-3M'..'BIOGEN-60M', or 'SMB-MAPS', 'SMB-TOTAL', 'SMB-SUITE-2027'.
        discount_pct: Optional seasonal discount percentage between 0 and 35.
        split_physical_later: If True, splits digital booking advance vs phase-2 physical/Ads payment.
        niche: Pricing column for modular tiers ('padel_gym', 'danza_colegios', 'corp_btl').
    """
    ledger = read_json(FILES["accounting"], default={"packages_catalog": []})
    bounded_discount = max(0.0, min(float(discount_pct), 35.0))
    for pkg in ledger.get("packages_catalog", []):
        if pkg.get("id") == package_id:
            final_price = round(pkg["price_mxn"] * (1.0 - bounded_discount / 100.0), 2)
            cost = float(pkg["direct_cost_mxn"])
            net = round(final_price - cost, 2)
            margin = round((net / final_price) * 100.0, 1) if final_price > 0 else 0.0
            advance_50 = round(final_price * 0.5, 2)
            result = {
                "package_id": package_id,
                "name": pkg["name"],
                "list_price_mxn": float(pkg["price_mxn"]),
                "discount_pct": bounded_discount,
                "final_price_mxn": final_price,
                "seasonal_35_price_mxn": round(float(pkg["price_mxn"]) * 0.65, 2),
                "advance_50_pct_mxn": advance_50,
                "balance_delivery_50_pct_mxn": advance_50,
                "direct_supplier_cost_mxn": cost,
                "net_profit_mxn": net,
                "margin_pct": margin,
                "healthy_margin_ok": margin >= 67.0,
                "digital_sla": pkg["digital_sla"],
                "physical_sla": pkg["physical_sla"],
            }
            if split_physical_later and cost > 0:
                digital_slice = round(final_price - cost * 2.2, 2)
                result["split_physical_later"] = True
                result["phase_1_digital_total_mxn"] = digital_slice
                result["phase_1_advance_50_mxn"] = round(digital_slice * 0.5, 2)
                result["phase_2_physical_balance_mxn"] = round(final_price - digital_slice, 2)
            append_agent_event(
                "contabilidad_finanzas",
                f"Calculó cotización {package_id}",
                f"Precio ${final_price:,.0f} MXN · Anticipo ${advance_50:,.0f} MXN · Margen {margin}%.",
                target_agent="ventas_outreach",
            )
            return json.dumps(result, ensure_ascii=False, indent=2)

    modular_tiers = ledger.get("modular_options_matrix", {}).get("tiers", [])
    niche_key = niche if niche in {"padel_gym", "danza_colegios", "corp_btl"} else "padel_gym"
    for tier in modular_tiers:
        if tier.get("id") == package_id:
            base_price = float(tier.get("prices_by_niche", {}).get(niche_key, 4900))
            final_price = round(base_price * (1.0 - bounded_discount / 100.0), 2)
            split_cfg = tier.get("deferred_split", {})
            if split_physical_later and split_cfg.get("enabled"):
                phase_1_total = round(float(split_cfg.get("phase_1_digital_mxn", 4900)) * (1.0 - bounded_discount / 100.0), 2)
                phase_2_total = round(max(0.0, final_price - phase_1_total), 2)
                cost_today = 350.0
                net = round(final_price - float(tier.get("direct_cost_mxn", 350)), 2)
            else:
                phase_1_total = final_price
                phase_2_total = 0.0
                cost_today = float(tier.get("direct_cost_mxn", 350))
                net = round(final_price - cost_today, 2)
            margin = round((net / final_price) * 100.0, 1) if final_price > 0 else 0.0
            result = {
                "package_id": package_id,
                "name": tier["title"],
                "niche": niche_key,
                "list_price_mxn": base_price,
                "discount_pct": bounded_discount,
                "final_price_mxn": final_price,
                "seasonal_35_price_mxn": round(base_price * 0.65, 2),
                "advance_50_pct_mxn": round(phase_1_total * 0.5, 2),
                "balance_delivery_50_pct_mxn": round(phase_1_total * 0.5, 2),
                "split_physical_later": bool(split_physical_later and split_cfg.get("enabled")),
                "phase_1_digital_mxn": phase_1_total,
                "phase_2_physical_mxn": phase_2_total,
                "direct_supplier_cost_mxn": cost_today if split_physical_later else float(tier.get("direct_cost_mxn", 350)),
                "net_profit_mxn": net,
                "margin_pct": margin,
                "healthy_margin_ok": margin >= 67.0,
                "digital_sla": tier["digital_sla"],
                "physical_sla": tier["physical_sla"],
            }
            append_agent_event(
                "contabilidad_finanzas",
                f"Cotizó {package_id} ({niche_key})",
                f"Entrada ${result['phase_1_digital_mxn']:,.0f} MXN · Margen {margin}%.",
                target_agent="ventas_outreach",
            )
            return json.dumps(result, ensure_ascii=False, indent=2)

    smb_tiers = ledger.get("small_business_catalog", {}).get("tiers", [])
    for smb in smb_tiers:
        if smb.get("id") == package_id:
            list_price = float(smb.get("list_price_mxn", 6000))
            final_price = round(list_price * (1.0 - bounded_discount / 100.0), 2)
            cost = float(smb.get("direct_cost_mxn", 300))
            split_cfg = smb.get("deferred_split", {})
            if split_physical_later and split_cfg.get("enabled"):
                phase_1_total = round(float(split_cfg.get("phase_1_digital_mxn", final_price)), 2)
                if bounded_discount != 35.0:
                    phase_1_total = round(final_price * 0.66, 2)
                phase_2_total = round(max(0.0, final_price - phase_1_total), 2)
            else:
                phase_1_total = final_price
                phase_2_total = 0.0
            net = round(final_price - cost, 2)
            margin = round((net / final_price) * 100.0, 1) if final_price > 0 else 0.0
            result = {
                "package_id": package_id,
                "name": f"Captoora Small Business · {smb['title']}",
                "list_price_mxn": list_price,
                "discount_pct": bounded_discount,
                "final_price_mxn": final_price,
                "seasonal_35_price_mxn": float(smb.get("promo_price_mxn", round(list_price * 0.65, 2))),
                "advance_50_pct_mxn": round(phase_1_total * 0.5, 2),
                "balance_delivery_50_pct_mxn": round(phase_1_total * 0.5, 2),
                "split_physical_later": bool(split_physical_later and split_cfg.get("enabled")),
                "phase_1_digital_mxn": phase_1_total,
                "phase_2_physical_mxn": phase_2_total,
                "direct_supplier_cost_mxn": cost,
                "net_profit_mxn": net,
                "margin_pct": margin,
                "healthy_margin_ok": margin >= 70.0,
                "digital_sla": smb["digital_sla"],
                "physical_sla": smb["physical_sla"],
            }
            append_agent_event(
                "contabilidad_finanzas",
                f"Cotizó {package_id} (Small Business)",
                f"Lista ${list_price:,.0f} · Final ${final_price:,.0f} MXN (-{bounded_discount:.0f}%) · Margen {margin}%.",
                target_agent="ventas_outreach",
            )
            return json.dumps(result, ensure_ascii=False, indent=2)

    for plan in ledger.get("biogen_pilot_catalog", {}).get("durations", []):
        if plan.get("id") == package_id:
            monthly = round(float(plan["beta_monthly_mxn"]) * (1.0 - bounded_discount / 100.0), 2)
            months = int(plan["months"])
            total_contract = round(monthly * months, 2)
            cost_total = round(180.0 * months, 2)
            net = round(total_contract - cost_total, 2)
            margin = round((net / total_contract) * 100.0, 1) if total_contract > 0 else 0.0
            result = {
                "package_id": package_id,
                "name": f"Captoora Biogen Beta · {plan['label']}",
                "monthly_mxn": monthly,
                "months": months,
                "discount_pct": bounded_discount,
                "final_price_mxn": total_contract,
                "advance_50_pct_mxn": monthly,
                "balance_delivery_50_pct_mxn": round(total_contract - monthly, 2),
                "direct_supplier_cost_mxn": cost_total,
                "net_profit_mxn": net,
                "margin_pct": margin,
                "healthy_margin_ok": margin >= 70.0,
                "digital_sla": "Entrega digital comparativa el mismo día de sesión (cuerpo/ángulo idéntico)",
                "physical_sla": "Cuadros o placas acrílicas de evolución trimestral opcionales en 3-5 días hábiles",
            }
            return json.dumps(result, ensure_ascii=False, indent=2)

    return f"Error: paquete '{package_id}' no encontrado en accounting_ledger.json."


def audit_contract_clauses(clause_summary: str) -> str:
    """Audit proposed client contract terms against Captoora's legal protection rules.

    Args:
        clause_summary: Summary of client payment terms, IP cession, or liability obligations.
    """
    text_lower = clause_summary.lower()
    red_flags: list[str] = []
    if any(k in text_lower for k in ("60 dias", "60 días", "90 dias", "90 días", "120")):
        red_flags.append("FOCO ROJO: Plazo de pago >15 días; exigir 50% anticipo y 50% contra entrega digital.")
    if any(k in text_lower for k in ("cesion total", "cesión total", "patrimoniales y morales", "exclusiv")):
        red_flags.append("FOCO ROJO: Cesión absoluta o exclusividad; cambiar a licencia no exclusiva y retener derechos morales/portafolio.")
    if any(k in text_lower for k in ("15 min", "en vivo")) and ("acrilic" in text_lower or "acrílic" in text_lower or "marco" in text_lower):
        red_flags.append("ALERTA SLA: Separar entrega digital mismo día vs manufactura artesanal de taller (3 a 5 días hábiles).")

    append_agent_event(
        "ops_talleres_legal",
        "Auditó términos contractuales",
        f"Detectó {len(red_flags)} alerta(s) críticas antes de firma.",
        target_agent="chief_of_staff",
    )
    return json.dumps(
        {
            "red_flags": red_flags,
            "mandatory_clauses": [
                "50% anticipo obligatorio al reservar fecha + 50% contra entrega digital",
                "Conservación de derechos morales y licencia de portafolio Captoora",
                "Distinción explícita: entrega digital el mismo día vs piezas físicas taller NL (3-5 días hábiles)",
            ],
        },
        ensure_ascii=False,
        indent=2,
    )


def get_portfolio_highlights(category: str = "all") -> str:
    """Inspect real portfolio items from assets/portfolio/manifest.json for visual campaigns.

    Args:
        category: Category key ('toros', 'football', 'cheer', 'nidos', or 'all').
    """
    items = read_json(FILES["portfolio"], default=[])
    if category and category != "all":
        items = [i for i in items if i.get("category") == category]
    return json.dumps(items[:8], ensure_ascii=False, indent=2)


def enqueue_human_trigger(
    agent_id: str,
    target_name: str,
    niche: str,
    channel: str,
    draft_text: str,
    package_ref: str = "4. Torneo del Pavo & Posada Pádel ($12,500 MXN)",
    phone: str = "",
    financial_impact_mxn: float = 12500.0,
    estimated_margin_pct: float = 80.8,
    task_id: str = "",
    is_client_facing: bool = True,
) -> str:
    """Queue a prepared outreach draft, social post, or operational checklist for the human owner's final approval trigger.

    Args:
        agent_id: ID of the requesting Captoora agent (e.g. 'ventas_outreach').
        target_name: Target club, academy, company, or channel.
        niche: Business niche ('Pádel & Raqueta', 'Baile & Danza Señoras', etc.).
        channel: Proposed dispatch channel ('WhatsApp Directo', 'Pixieset Email', 'Instagram Reels', etc.).
        draft_text: Exact copy ready for human review before sending.
        package_ref: Commercial package or deliverable label.
        phone: Digits-only phone number with country code if WhatsApp (e.g. '528123545695').
        financial_impact_mxn: Estimated revenue or quote impact in MXN.
        estimated_margin_pct: Estimated net margin percentage.
        task_id: Optional Asana task ID to move into 'waiting_trigger'.
        is_client_facing: Whether the text will be read by external clients (enforces zero-AI copy check).
    """
    if is_client_facing:
        violations = validate_client_copy(draft_text)
        if violations:
            return "RECHAZADO POR GUARDRAIL DE ESTILO: " + " | ".join(violations)

    queue = read_json(FILES["approvals"], default={"policy": "HUMAN_APPROVAL_REQUIRED", "items": []})
    items = queue.get("items", [])
    existing_nums = [int(i["id"].split("-")[1]) for i in items if i.get("id", "").startswith("APR-") and i["id"].split("-")[1].isdigit()]
    next_id = f"APR-{max(existing_nums, default=6) + 1:03d}"

    clean_phone = "".join(ch for ch in (phone or "") if ch.isdigit())
    wa_url = (
        f"https://wa.me/{clean_phone}?text={urllib.parse.quote(draft_text)}"
        if clean_phone
        else ""
    )

    new_item = {
        "id": next_id,
        "agent_id": agent_id,
        "task_id": task_id or "TASK-101",
        "target_name": target_name,
        "niche": niche,
        "channel": f"{channel}" + (f" (+{clean_phone})" if clean_phone else ""),
        "phone": clean_phone,
        "package_ref": package_ref,
        "financial_impact_mxn": financial_impact_mxn,
        "estimated_margin_pct": estimated_margin_pct,
        "compliance_flags": ["0% mención IA", "Sin palabra 'presumir'", "Cola de Último Trigger"],
        "draft_text": draft_text,
        "whatsapp_url": wa_url,
        "status": "pending_trigger",
        "created_at": now_iso(),
        "decided_at": None,
    }
    items.insert(0, new_item)
    queue["items"] = items
    write_json(FILES["approvals"], queue)

    if task_id:
        asana = read_json(FILES["asana"], default={"tasks": []})
        for t in asana.get("tasks", []):
            if t.get("id") == task_id:
                t["status"] = "waiting_trigger"
                t["deliverable_ref"] = next_id
        write_json(FILES["asana"], asana)

    append_agent_event(
        agent_id,
        f"Encoló {next_id} (Trigger)",
        f"Propuesta lista para {target_name} vía {channel}. Esperando tu aprobación.",
        target_agent="trigger_gate",
        zone="trigger_gate",
    )
    return json.dumps({"enqueued_id": next_id, "status": "pending_trigger"}, ensure_ascii=False)


def generate_subscription_content_plan(
    focus: str = "all",
    week_label: str = "Semana Sprint Nov 2026 (-35%)",
) -> str:
    """Refresh Marky's weekly multi-network content plan maximizing user subscriptions without external quotas.

    Args:
        focus: Track focus ('all', 'opusclip', 'navidad', 'small_business', or 'biogen').
        week_label: Descriptive week tag for the refreshed schedule.
    """
    from .marketing_hub import regenerate_marketing_plan

    state = regenerate_marketing_plan(focus=focus, week_label=week_label)
    return json.dumps(
        {
            "status": "updated",
            "week_label": state.get("active_week_label"),
            "posts_count": len(state.get("content_calendar", [])),
            "opusclip_targets": len((state.get("opusclip_rescue_sprint") or {}).get("pillars_to_record", [])),
            "subscriptions_active": len(state.get("subscriptions_stack", [])),
        },
        ensure_ascii=False,
    )


def prepare_lupe_social_post(
    platform: str,
    target_title: str,
    draft_text: str,
    conan_tool: str = "OpusClip Pro + CapCut",
    niche: str = "Marca & Multired",
) -> str:
    """Queue a validated social post, Meta Business Suite card, TikTok, or LinkedIn draft from Lupe for Human Trigger.

    Args:
        platform: Target social network ('Meta Business Suite (FB + IG)', 'TikTok', 'LinkedIn B2B', etc.).
        target_title: Brief post topic/hook title.
        draft_text: Full client-facing caption text (must pass zero-AI and no-'presumir' guardrails).
        conan_tool: Creative subscription used by Conan to prepare visuals.
        niche: Campaign track tag.
    """
    violations = validate_client_copy(draft_text)
    if violations:
        return "RECHAZADO POR GUARDRAIL DE ESTILO: " + " | ".join(violations)
    return enqueue_human_trigger(
        agent_id="lupe_social",
        target_name=f"{platform} · {target_title}",
        niche=niche,
        channel=f"{platform} (Programación Lupe)",
        draft_text=draft_text,
        package_ref=f"Conan Pieza: {conan_tool}",
        financial_impact_mxn=0.0,
        estimated_margin_pct=100.0,
        task_id="TASK-702",
        is_client_facing=True,
    )


def assign_conan_creative_brief(
    title: str,
    tool_stack: str = "OpusClip Pro + CapCut + Captions",
    output_format: str = "Reel 9:16",
    target_channel: str = "IG Reels + TikTok + LinkedIn",
    notes: str = "",
) -> str:
    """Create a creative production brief for Conan using user's active tools and sync an Asana task for Lupe.

    Args:
        title: Concise production piece title.
        tool_stack: Subscriptions used ('OpusClip Pro', 'Captions', 'Canva', 'Aftershoot', 'Evoto', 'CapCut').
        output_format: Deliverable spec ('Reel 9:16', 'Carrusel 4:5', 'PNG Antes/Después').
        target_channel: Where Lupe will schedule it.
        notes: Specific hook, CTA, or shot guidance.
    """
    from .marketing_hub import register_conan_creative_brief

    res = register_conan_creative_brief(
        title=title,
        tool_stack=tool_stack,
        output_format=output_format,
        target_channel=target_channel,
        notes=notes,
    )
    return json.dumps({"brief": res["brief"], "task_id": res["task"]["id"]}, ensure_ascii=False)

