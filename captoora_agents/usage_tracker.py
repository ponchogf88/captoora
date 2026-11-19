"""API token, transcript telemetry, WhatsApp Cloud quota, and traffic-light cost tracker."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from . import ROOT_DIR
from .config import FILES, MONTERREY_TZ, now_iso, read_json, write_json

DEFAULT_LIMITS = {
    "daily_token_budget": 500_000,
    "monthly_whatsapp_limit": 1000,
    "daily_usd_limit": 5.0,
    "dry_run_preferred": False,
}

# Approximate Gemini 2.5 Pro / Flash blended estimation per 1M tokens (for budget guidance only)
_INPUT_USD_PER_M = 0.30
_CACHE_USD_PER_M = 0.03
_OUTPUT_USD_PER_M = 2.50
_USD_TO_MXN = 20.2


def _default_usage_state() -> dict[str, Any]:
    return {
        "limits": dict(DEFAULT_LIMITS),
        "runtime_calls": [],
        "whatsapp_dispatches": [],
        "apify_runs": [],
        "updated_at": now_iso(),
    }


def _scan_antigravity_transcripts() -> dict[str, Any]:
    """Read real SDK PLANNER_RESPONSE token usage logged in .antigravity_state/."""
    state_root = ROOT_DIR / ".antigravity_state" / "brain"
    input_tokens = 0
    cache_read_tokens = 0
    output_tokens = 0
    model_steps = 0
    tool_calls = 0
    sessions: set[str] = set()
    today_str = datetime.now(MONTERREY_TZ).date().isoformat()
    today_tokens = 0

    if not state_root.exists():
        return {
            "sessions": 0,
            "model_steps": 0,
            "tool_calls": 0,
            "input_tokens": 0,
            "cache_read_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "today_tokens": 0,
        }

    for transcript_file in state_root.glob("*/.system_generated/logs/transcript.jsonl"):
        sessions.add(transcript_file.parents[2].name)
        try:
            with transcript_file.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if entry.get("type") != "PLANNER_RESPONSE":
                        continue
                    model_steps += 1
                    inp = int(entry.get("input_tokens") or 0)
                    cache = int(entry.get("cache_read_tokens") or 0)
                    out = int(entry.get("output_tokens") or 0)
                    tcalls = len(entry.get("tool_calls") or [])
                    input_tokens += inp
                    cache_read_tokens += cache
                    output_tokens += out
                    tool_calls += tcalls
                    created = str(entry.get("created_at") or "")
                    if created.startswith(today_str):
                        today_tokens += inp + cache + out
        except OSError:
            continue

    total_tokens = input_tokens + cache_read_tokens + output_tokens
    return {
        "sessions": len(sessions),
        "model_steps": model_steps,
        "tool_calls": tool_calls,
        "input_tokens": input_tokens,
        "cache_read_tokens": cache_read_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "today_tokens": today_tokens,
    }


def _estimate_cost_usd(input_tokens: int, cache_tokens: int, output_tokens: int) -> float:
    usd = (
        (max(0, input_tokens) / 1_000_000.0) * _INPUT_USD_PER_M
        + (max(0, cache_tokens) / 1_000_000.0) * _CACHE_USD_PER_M
        + (max(0, output_tokens) / 1_000_000.0) * _OUTPUT_USD_PER_M
    )
    return round(usd, 4)


def record_sdk_usage(agent_id: str, usage_metadata: Any) -> dict[str, Any]:
    """Persist live UsageMetadata emitted by Google Antigravity ChatResponse."""
    if usage_metadata is None:
        return {}

    def _pick(field: str) -> int:
        if isinstance(usage_metadata, dict):
            return int(usage_metadata.get(field) or 0)
        return int(getattr(usage_metadata, field, 0) or 0)

    inp = _pick("prompt_token_count")
    cache = _pick("cached_content_token_count")
    cand = _pick("candidates_token_count")
    thoughts = _pick("thoughts_token_count")
    out = cand + thoughts
    total = _pick("total_token_count") or (inp + cache + out)

    state = read_json(FILES["usage"], default=_default_usage_state())
    calls = state.get("runtime_calls", [])
    calls.insert(
        0,
        {
            "timestamp": now_iso(),
            "agent_id": agent_id,
            "input_tokens": inp,
            "cache_read_tokens": cache,
            "output_tokens": out,
            "total_tokens": total,
        },
    )
    state["runtime_calls"] = calls[:120]
    state["updated_at"] = now_iso()
    write_json(FILES["usage"], state)
    return calls[0]


def record_whatsapp_dispatch(count: int = 1, *, mode: str = "meta_cloud_api") -> None:
    """Record dispatched WhatsApp messages against free monthly Cloud tier."""
    state = read_json(FILES["usage"], default=_default_usage_state())
    dispatches = state.get("whatsapp_dispatches", [])
    dispatches.insert(
        0,
        {
            "timestamp": now_iso(),
            "count": max(1, int(count)),
            "mode": mode,
        },
    )
    state["whatsapp_dispatches"] = dispatches[:200]
    state["updated_at"] = now_iso()
    write_json(FILES["usage"], state)


def update_usage_limits(
    *,
    daily_token_budget: int | None = None,
    monthly_whatsapp_limit: int | None = None,
    daily_usd_limit: float | None = None,
    dry_run_preferred: bool | None = None,
) -> dict[str, Any]:
    """Update operator-configured API budget thresholds and return refreshed summary."""
    state = read_json(FILES["usage"], default=_default_usage_state())
    limits = state.get("limits", dict(DEFAULT_LIMITS))
    if daily_token_budget is not None:
        limits["daily_token_budget"] = max(5000, int(daily_token_budget))
    if monthly_whatsapp_limit is not None:
        limits["monthly_whatsapp_limit"] = max(50, int(monthly_whatsapp_limit))
    if daily_usd_limit is not None:
        limits["daily_usd_limit"] = round(max(0.25, float(daily_usd_limit)), 2)
    if dry_run_preferred is not None:
        limits["dry_run_preferred"] = bool(dry_run_preferred)
    state["limits"] = limits
    state["updated_at"] = now_iso()
    write_json(FILES["usage"], state)
    return get_usage_summary()


def get_usage_summary() -> dict[str, Any]:
    """Combine .antigravity_state transcripts + runtime SDK calls + WhatsApp dispatches into traffic-light status."""
    state = read_json(FILES["usage"], default=_default_usage_state())
    limits = {**DEFAULT_LIMITS, **state.get("limits", {})}
    transcript = _scan_antigravity_transcripts()

    today_str = datetime.now(MONTERREY_TZ).date().isoformat()
    month_prefix = today_str[:7]
    runtime_calls = state.get("runtime_calls", [])
    runtime_in = sum(int(c.get("input_tokens") or 0) for c in runtime_calls)
    runtime_cache = sum(int(c.get("cache_read_tokens") or 0) for c in runtime_calls)
    runtime_out = sum(int(c.get("output_tokens") or 0) for c in runtime_calls)
    runtime_total = sum(int(c.get("total_tokens") or 0) for c in runtime_calls)

    # Transcript logs already cover Antigravity SDK steps; take max or combined cleanly without double-counting identical sessions
    total_in = max(transcript["input_tokens"], runtime_in) if runtime_calls and transcript["input_tokens"] else transcript["input_tokens"] + runtime_in
    total_cache = max(transcript["cache_read_tokens"], runtime_cache) if runtime_calls and transcript["cache_read_tokens"] else transcript["cache_read_tokens"] + runtime_cache
    total_out = max(transcript["output_tokens"], runtime_out) if runtime_calls and transcript["output_tokens"] else transcript["output_tokens"] + runtime_out
    total_tokens = total_in + total_cache + total_out

    est_usd = _estimate_cost_usd(total_in, total_cache, total_out)
    est_mxn = round(est_usd * _USD_TO_MXN, 2)

    budget_tokens = max(5000, int(limits["daily_token_budget"]))
    token_pct = round(min(100.0, (total_tokens / budget_tokens) * 100.0), 1)
    usd_limit = max(0.25, float(limits["daily_usd_limit"]))
    usd_pct = round(min(100.0, (est_usd / usd_limit) * 100.0), 1)
    peak_pct = max(token_pct, usd_pct)

    wa_dispatches = state.get("whatsapp_dispatches", [])
    wa_month_count = sum(
        int(d.get("count") or 0)
        for d in wa_dispatches
        if str(d.get("timestamp") or "").startswith(month_prefix)
    )
    wa_limit = max(50, int(limits["monthly_whatsapp_limit"]))
    wa_pct = round(min(100.0, (wa_month_count / wa_limit) * 100.0), 1)

    if peak_pct >= 85.0 or limits.get("dry_run_preferred"):
        semaphore = "rojo" if peak_pct >= 85.0 else "ambar"
        action_hint = (
            "DETENER llamadas automáticas SDK y operar solo modo manual / wa.me / Mail."
            if peak_pct >= 85.0
            else "Modo Dry-Run Cero Tokens activo: usa plantillas y envíos directos."
        )
    elif peak_pct >= 60.0 or wa_pct >= 75.0:
        semaphore = "ambar"
        action_hint = "Bajar ritmo automático: usar caché local, filtros y pruebas --dry-run."
    else:
        semaphore = "verde"
        action_hint = "Consumo saludable: margen amplio para orquesta SDK y prospección."

    return {
        "semaphore": semaphore,
        "action_hint": action_hint,
        "estimated_accuracy_note": "Telemetría real de transcripts SDK + runtime local; USD estimado aprox. tarifa Gemini.",
        "tokens": {
            "input": total_in,
            "cache_read": total_cache,
            "output": total_out,
            "total": total_tokens,
            "budget": budget_tokens,
            "pct": token_pct,
        },
        "cost_approx": {
            "usd": est_usd,
            "mxn": est_mxn,
            "usd_limit": usd_limit,
            "usd_pct": usd_pct,
        },
        "activity": {
            "sdk_sessions": transcript["sessions"],
            "model_steps": transcript["model_steps"] + len(runtime_calls),
            "tool_calls": transcript["tool_calls"],
        },
        "whatsapp_quota": {
            "month_used": wa_month_count,
            "monthly_free_limit": wa_limit,
            "pct": wa_pct,
        },
        "limits": limits,
        "updated_at": now_iso(),
    }
