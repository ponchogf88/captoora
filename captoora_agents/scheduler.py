"""24/7 Background Scheduler & Inbound Webhook Awakening Engine (Monterrey CST)."""

from __future__ import annotations

import asyncio
import contextlib
import hmac
import os
from datetime import datetime
from typing import Any

from .config import FILES, MONTERREY_TZ, append_agent_event, now_iso, write_json
from .growth_suite import (
    compute_accountant_snapshot,
    compute_weekly_report,
    get_or_init_growth_state,
    refresh_ceo_weekly_plan,
    trigger_tomorrow_reminder,
)


def _current_monterrey_dt() -> datetime:
    return datetime.now(MONTERREY_TZ)


def execute_scheduler_slot(
    slot_id: str,
    *,
    manual: bool = False,
    now_dt: datetime | None = None,
) -> dict[str, Any]:
    """Run one scheduled awakening slot safely without performing unsupervised external sends."""
    dt = now_dt or _current_monterrey_dt()
    state = get_or_init_growth_state()
    sched = state.setdefault("scheduler", {})
    today = dt.strftime("%Y-%m-%d")

    result_detail = ""
    if slot_id == "08_30_ceo":
        plan = refresh_ceo_weekly_plan()
        result_detail = f"CEO Briefing despertado: {plan.get('week_focus', '')[:120]}"
    elif slot_id == "10_00_followups":
        rep = compute_weekly_report()
        due = rep["funnel_metrics"]["followups_24_48h_due"]
        pending = rep["funnel_metrics"]["pending_trigger"]
        result_detail = f"Detector 24–48h: {due} seguimientos CRM y {pending} triggers en cola."
        append_agent_event("ventas_outreach", "Despertó Seguimientos 24–48h", result_detail, zone="desk_ventas", source="scheduler")
    elif slot_id == "13_00_pull":
        rep = compute_weekly_report()
        result_detail = f"Corte Pull & SEO: {rep['seo_status']['note'][:120]}"
        append_agent_event("marky_marketing", "Corte Pull & SEO 13:00", result_detail, zone="estudio_marky", source="scheduler")
    elif slot_id == "18_00_tomorrow":
        rem = trigger_tomorrow_reminder(send_email_to="", dry_run=True)
        result_detail = f"Recordatorio Agenda Mañana listo ({rem['blocks_count']} bloques)."
    elif slot_id == "fri_16_report":
        snap = compute_accountant_snapshot()
        result_detail = f"Reporte Contador & Ventas: {snap['summary']['ads_gate_status']}"
        append_agent_event("contabilidad_finanzas", "Reporte Viernes 16:00", result_detail, zone="boveda_finanzas", source="scheduler")
    else:
        raise ValueError(f"Slot programado desconocido: {slot_id}")

    # Refresh state before marking slot completed to avoid clobbering inner writes
    state = get_or_init_growth_state()
    sched = state.setdefault("scheduler", {})
    ran = sched.setdefault("ran_slots_today", {})
    ran[slot_id] = today
    sched["last_tick"] = now_iso()
    sched["last_executed_slot"] = {"slot_id": slot_id, "at": now_iso(), "manual": manual, "detail": result_detail}
    write_json(FILES["growth_suite"], state)
    return sched["last_executed_slot"]


def tick_scheduler(now_dt: datetime | None = None) -> dict[str, Any]:
    """Evaluate all CST slots for current time and execute due slots at most once per day."""
    dt = now_dt or _current_monterrey_dt()
    state = get_or_init_growth_state()
    sched = state.get("scheduler", {})
    if not sched.get("enabled", True):
        return {"enabled": False, "executed": [], "tick_at": now_iso()}

    today = dt.strftime("%Y-%m-%d")
    weekday = dt.weekday()
    ran_today = sched.get("ran_slots_today", {})
    executed: list[dict[str, Any]] = []

    for slot in sched.get("slots", []):
        sid = slot.get("id")
        if not sid or ran_today.get(sid) == today:
            continue
        if weekday not in slot.get("weekdays", []):
            continue
        sh, sm = int(slot.get("hour", 0)), int(slot.get("minute", 0))
        # Fire within 20-minute window after scheduled minute so brief restarts don't miss the slot
        now_mins = dt.hour * 60 + dt.minute
        slot_mins = sh * 60 + sm
        if 0 <= (now_mins - slot_mins) <= 20:
            executed.append(execute_scheduler_slot(sid, manual=False, now_dt=dt))

    state = get_or_init_growth_state()
    state.setdefault("scheduler", {})["last_tick"] = now_iso()
    write_json(FILES["growth_suite"], state)
    return {"enabled": True, "executed": executed, "tick_at": now_iso()}


def toggle_scheduler(enabled: bool) -> dict[str, Any]:
    state = get_or_init_growth_state()
    sched = state.setdefault("scheduler", {})
    sched["enabled"] = bool(enabled)
    sched["last_tick"] = now_iso()
    write_json(FILES["growth_suite"], state)
    append_agent_event(
        "chief_of_staff",
        f"Despertador 24/7 {'ACTIVADO' if enabled else 'PAUSADO'}",
        "Control de ciclos automáticos horarios CST.",
        zone="mesa_directiva",
        source="human_ui",
    )
    return get_scheduler_status()


def get_scheduler_status() -> dict[str, Any]:
    state = get_or_init_growth_state()
    sched = state.get("scheduler", {})
    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.captoora.server247.plist")
    return {
        "enabled": bool(sched.get("enabled", True)),
        "last_tick": sched.get("last_tick"),
        "last_executed_slot": sched.get("last_executed_slot"),
        "ran_slots_today": sched.get("ran_slots_today", {}),
        "slots": sched.get("slots", []),
        "launchd_installed": os.path.exists(plist_path),
        "launchd_plist_path": plist_path,
    }


def process_inbound_webhook(
    *,
    source_name: str,
    event_type: str,
    payload: dict[str, Any],
    provided_secret: str | None = None,
) -> dict[str, Any]:
    """Authenticate external webhook (Calendly/GoHighLevel/WhatsApp) and wake Chief of Staff."""
    expected = os.getenv("CAPTOORA_WEBHOOK_SECRET", "").strip()
    if expected:
        if not provided_secret or not hmac.compare_digest(provided_secret.strip(), expected):
            raise PermissionError("CAPTOORA_WEBHOOK_SECRET inválido o faltante.")

    lead_name = str(payload.get("name") or payload.get("prospect") or payload.get("contact_name") or source_name).strip()
    append_agent_event(
        "chief_of_staff",
        f"Webhook {source_name}: {event_type}",
        f"Despertó seguimiento por evento entrante de {lead_name}.",
        target_agent="ventas_outreach",
        zone="mesa_directiva",
        source="webhook_inbound",
    )
    return {
        "accepted": True,
        "source": source_name,
        "event_type": event_type,
        "lead_name": lead_name,
        "woke_at": now_iso(),
    }


async def scheduler_background_loop(stop_event: asyncio.Event) -> None:
    """Async background loop running inside FastAPI lifespan to tick every 60s."""
    while not stop_event.is_set():
        with contextlib.suppress(Exception):
            await asyncio.to_thread(tick_scheduler)
        with contextlib.suppress(asyncio.TimeoutError):
            await asyncio.wait_for(stop_event.wait(), timeout=60.0)
