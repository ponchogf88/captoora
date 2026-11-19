"""Configuration, atomic JSON state helpers, event stream logging, and copy guardrails."""

from __future__ import annotations

import json
import os
import re
import threading
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from . import DATA_DIR, ROOT_DIR

load_dotenv(ROOT_DIR / ".env")

MONTERREY_TZ = timezone(timedelta(hours=-6), name="CST")

FILES = {
    "roster": DATA_DIR / "agents_roster.json",
    "asana": DATA_DIR / "projects_asana.json",
    "approvals": DATA_DIR / "approval_queue.json",
    "accounting": DATA_DIR / "accounting_ledger.json",
    "events": DATA_DIR / "agent_events.json",
    "leads": DATA_DIR / "apify_scraped_leads.json",
    "outreach": DATA_DIR / "outreach.json",
    "usage": DATA_DIR / "usage_telemetry.json",
    "gmaps_audits": DATA_DIR / "gmaps_audits.json",
    "marketing": DATA_DIR / "marketing_studio.json",
    "portfolio": ROOT_DIR / "assets" / "portfolio" / "manifest.json",
    "growth_suite": DATA_DIR / "growth_suite.json",
    "leads_geo": DATA_DIR / "leads_geo.json",
    "routes_log": DATA_DIR / "routes_log.json",
}

AGENT_ZONES = {
    "chief_of_staff": "mesa_directiva",
    "scouting_radar": "radar_maps",
    "embudo_marketing": "atelier_embudo",
    "social_content": "estudio_social",
    "ventas_outreach": "desk_ventas",
    "contabilidad_finanzas": "boveda_finanzas",
    "ops_talleres_legal": "taller_led",
    "marky_marketing": "estudio_marky",
    "lupe_social": "cabina_lupe",
    "conan_content": "estudio_conan",
}

_IO_LOCK = threading.RLock()

# Regex carefully bounded with \b so Spanish words like "día", "fotografía", "experiencia" pass cleanly.
_FORBIDDEN_COPY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\b(inteligencia\s+artificial|i\.?\s*a\.?)\b", re.IGNORECASE),
        "Mención prohibida de IA/Inteligencia Artificial en texto orientado al cliente.",
    ),
    (
        re.compile(r"\bpresum[a-z]*\b", re.IGNORECASE),
        "Uso prohibido del verbo 'presumir'; sustituir por 'proyectar imagen profesional / nivel de excelencia'.",
    ),
]

_NEIGHBORHOOD_SELF_BRAG_RE = re.compile(
    r"(aqu[ií]\s+en\s+(?:colinas\s+de\s+)?san\s+jer[oó]nimo|estudio\s+en\s+(?:colinas\s+de\s+)?san\s+jer[oó]nimo|captoora\s+(?:sports|studio)\s*\([^)]*san\s+jer[oó]nimo|#SanJeronimo)",
    re.IGNORECASE,
)


def now_iso() -> str:
    """Return current Monterrey local timestamp in ISO-8601 format."""
    return datetime.now(MONTERREY_TZ).isoformat(timespec="seconds")


def read_json(path: Path, default: Any = None) -> Any:
    """Thread-safe JSON loader."""
    with _IO_LOCK:
        if not path.exists():
            return default
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    """Thread-safe atomic JSON writer."""
    with _IO_LOCK:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(f"{path.suffix}.tmp")
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp_path, path)


def validate_client_copy(text: str) -> list[str]:
    """Check client-facing copy against Captoora's zero-AI, anti-'presumir', and zero neighborhood-brag rules."""
    violations: list[str] = []
    for pattern, reason in _FORBIDDEN_COPY_PATTERNS:
        if pattern.search(text or ""):
            violations.append(reason)
    if _NEIGHBORHOOD_SELF_BRAG_RE.search(text or ""):
        violations.append(
            "Evita destacar colonia propia ('Colinas de San Jerónimo'); lidera con técnica 1/2000s, iluminación y movilidad a la sede del cliente."
        )
    return violations


def append_agent_event(
    agent_id: str,
    action: str,
    detail: str,
    *,
    target_agent: str | None = None,
    zone: str | None = None,
    source: str = "sdk_real",
) -> dict[str, Any]:
    """Append an execution/activity event to agent_events.json (keeps latest 80 entries)."""
    with _IO_LOCK:
        state = read_json(
            FILES["events"],
            default={"studio_mode": "active", "active_agent": agent_id, "events": []},
        )
        events = state.get("events", [])
        next_num = len(events) + 1
        event = {
            "id": f"EVT-{next_num:03d}-{int(datetime.now().timestamp()) % 10000}",
            "timestamp": now_iso(),
            "agent_id": agent_id,
            "target_agent": target_agent,
            "zone": zone or AGENT_ZONES.get(agent_id, "mesa_directiva"),
            "action": action,
            "detail": detail[:280],
            "source": source,
        }
        events.insert(0, event)
        state["events"] = events[:80]
        state["active_agent"] = agent_id
        state["studio_mode"] = "active" if source == "sdk_real" else state.get("studio_mode", "idle_ready")
        write_json(FILES["events"], state)
        return event


def set_agent_runtime_status(agent_id: str, status: str) -> None:
    """Update agent status ('ready', 'running', 'waiting_trigger') and last_run timestamp in roster."""
    with _IO_LOCK:
        roster = read_json(FILES["roster"], default={"agents": []})
        now = now_iso()
        for agent in roster.get("agents", []):
            if agent.get("id") == agent_id:
                agent["status"] = status
                agent["last_run"] = now
        roster["updated_at"] = now
        write_json(FILES["roster"], roster)


def slugify(text: str) -> str:
    """Convert business name into a deterministic ASCII filename slug."""
    normalized = unicodedata.normalize("NFKD", str(text or "negocio")).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", normalized).strip("_").lower()
    return slug[:64] or "negocio"
