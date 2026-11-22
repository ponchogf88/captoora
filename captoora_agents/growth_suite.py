"""Growth Command Suite: Accountant ($0 upfront Ads gate + PFAE 612 SAT), CEO, SEO/20-Clips, Zoho Mail, Agenda, Calendly, Apify/GHL CRM & WA Web Supervisor."""

from __future__ import annotations

from datetime import datetime, timedelta
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from . import ROOT_DIR
from .config import (
    FILES,
    MONTERREY_TZ,
    append_agent_event,
    now_iso,
    read_json,
    slugify,
    validate_client_copy,
    write_json,
)
from .email_sender import get_smtp_status, send_email_via_zoho
from .whatsapp_cloud import clean_phone_digits, get_cloud_status

load_dotenv(ROOT_DIR / ".env", override=False)

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

ZONE_PRESETS: dict[str, dict[str, Any]] = {
    "san_jeronimo": {"label": "San Jerónimo / Obispado", "query_suffix": "San Jeronimo Obispado Monterrey"},
    "spgg_del_valle": {"label": "San Pedro / Del Valle", "query_suffix": "Del Valle San Pedro Garza Garcia"},
    "valle_oriente": {"label": "Valle Oriente / Lázaro Cárdenas", "query_suffix": "Valle Oriente San Pedro Monterrey"},
    "cumbres": {"label": "Cumbres / Paseo de los Leones", "query_suffix": "Cumbres Paseo de los Leones Monterrey"},
    "carretera_nacional": {"label": "Carretera Nacional / Esfera", "query_suffix": "Carretera Nacional Monterrey"},
    "tec_contry": {"label": "Zona Tec / Contry", "query_suffix": "Zona Tec Contry Monterrey"},
    "santa_catarina": {"label": "Santa Catarina / Vía Cordillera", "query_suffix": "Via Cordillera Santa Catarina Nuevo Leon"},
    "guadalupe_apodaca": {"label": "Guadalupe / San Nicolás / Apodaca", "query_suffix": "San Nicolas Guadalupe Nuevo Leon"},
}

NICHE_PRESETS: dict[str, str] = {
    "colegios": "colegio privado jardin de ninos",
    "gimnasios": "gimnasio fitness crossfit pilates",
    "padel": "club de padel tenis",
    "clinicas": "clinica dental medicina estetica fisioterapia",
    "danza": "academia de baile estudio de danza",
    "restaurantes": "restaurante cafe boutique brunch",
}


_DEFAULT_SCHEDULER_SLOTS: list[dict[str, Any]] = [
    {"id": "08_30_ceo", "hour": 8, "minute": 30, "weekdays": [0, 1, 2, 3, 4, 5], "label": "08:30 CST · Briefing CEO & Agenda"},
    {"id": "09_15_daily_email_batch", "hour": 9, "minute": 15, "weekdays": [0, 1, 2, 3, 4, 5], "label": "09:15 CST · Extractor Web + Lote Diario Zoho (25/día)"},
    {"id": "10_00_followups", "hour": 10, "minute": 0, "weekdays": [0, 1, 2, 3, 4, 5], "label": "10:00 CST · Cadencia Seguimiento 48h / 72h / Día 7"},
    {"id": "13_00_pull", "hour": 13, "minute": 0, "weekdays": [0, 1, 2, 3, 4, 5], "label": "13:00 CST · Corte Mediodía & Pull SEO"},
    {"id": "18_00_tomorrow", "hour": 18, "minute": 0, "weekdays": [0, 1, 2, 3, 4, 5], "label": "18:00 CST · Recordatorio Agenda Mañana"},
    {"id": "18_15_iterate_ab", "hour": 18, "minute": 15, "weekdays": [0, 1, 2, 3, 4, 5], "label": "18:15 CST · Iteración A/B & Aprendizaje Diario"},
    {"id": "fri_16_report", "hour": 16, "minute": 0, "weekdays": [4], "label": "Viernes 16:00 CST · Reporte Contador & Ventas"},
]


def _default_daily_automation() -> dict[str, Any]:
    return {
        "settings": {
            "auto_send_enabled": True,
            "daily_email_cap": 25,
            "territory_mix": {"mty": 10, "pv": 10, "biogen": 5},
        },
        "scanned_urls": [],
        "ab_variants": {
            "A_diagnostico_tecnica": {
                "label": "Variante A · Hallazgo Google Maps + Técnica 1/2000s",
                "sent": 0,
                "replies": 0,
                "meetings": 0,
                "closes": 0,
                "active": True,
            },
            "B_roi_patrocinio_vitrina": {
                "label": "Variante B · Vitrina 2027 / Retorno Rápido -35%",
                "sent": 0,
                "replies": 0,
                "meetings": 0,
                "closes": 0,
                "active": True,
            },
            "C_biogen_aliados_flujo": {
                "label": "Variante C · Alianzas Captoora Biogen Flow",
                "sent": 0,
                "replies": 0,
                "meetings": 0,
                "closes": 0,
                "active": True,
            },
        },
        "daily_email_batch": {"batch_date": None, "prepared_at": None, "items": []},
        "followups_due_cache": [],
        "negotiation_logs": [],
        "last_iteration_report": None,
    }


def _default_growth_state() -> dict[str, Any]:
    return {
        "updated_at": now_iso(),
        "tracking_ids": {
            "ga4_id": os.getenv("GA4_MEASUREMENT_ID", "").strip(),
            "meta_pixel_id": os.getenv("META_PIXEL_ID", "").strip(),
            "tiktok_pixel_id": os.getenv("TIKTOK_PIXEL_ID", "").strip(),
            "google_ads_tag": os.getenv("GOOGLE_ADS_TAG", "").strip(),
        },
        "calendly": {
            "base_url": os.getenv("CALENDLY_BASE_URL", "").strip() or "https://calendly.com/captoora",
            "event_types": [
                {"id": "maps_audit_15", "label": "Auditoría Google Maps & Vitrina 2027 (15 min)", "slug": "auditoria-maps-15m"},
                {"id": "navidad_led_20", "label": "Demo Eventos + Trofeos Acrílico LED (20 min)", "slug": "demo-led-20m"},
                {"id": "biogen_piloto_20", "label": "Sesión Piloto Captoora Biogen (20 min)", "slug": "biogen-piloto-20m"},
            ],
            "generated_links": [],
        },
        "ceo_plan": {
            "updated_at": now_iso(),
            "week_focus": "Lograr los primeros 1–3 cierres con anticipo 50% antes de invertir $1 en Ads (pauta $0 hoy -> desbloqueo por utilidad cobrada).",
            "primary_kpis": ["Primer 'Sí' cobrado (50%)", "15–20 WA Web diarios sin bloqueo", "20–30 clips semanales Pull"],
            "trending_hooks_mty": [
                "¿Tu negocio abre en Google Maps con el carrito gris de Street View?",
                "Congelamiento Global Shutter 1/2000s + entrega Halftime Blitz en 15 minutos",
                "Premiación con acrílico óptico iluminado LED cálida financiada por tus patrocinadores",
                "Captoora Biogen Flow: registro semanal escultural + dieta y evolución comprobable",
            ],
            "daily_priorities": [
                {"day": "Hoy / Arranque", "focus": "Despachar las 4 aprobaciones + lote de 15 fichas con Street View vía WhatsApp Web y Zoho."},
                {"day": "Día 2", "focus": "Publicar primeros Reels teardown de Google Maps + seguimiento 48h."},
                {"day": "Día 3–4", "focus": "Agendar 3–5 demos de 15 min en Calendly y cobrar 1er anticipo 50% para desbloquear pauta."},
                {"day": "Viernes 16:00", "focus": "Auditoría de caja del Contador (SAT IVA/ISR + margen) y recalibración semanal."},
            ],
        },
        "seo_and_clips": {
            "updated_at": now_iso(),
            "last_topic": "Auditoría Visual Google Maps + Producción Editorial 1/2000s",
            "target_keywords": [
                "fotografía deportiva profesional 1/2000s monterrey",
                "cobertura torneos pádel entrega mismo día san pedro",
                "optimizar google maps negocios clínicas colegios monterrey",
                "trofeos y placas acrílico led personalizadas monterrey",
                "sesión fotográfica evolutiva atletas captoora biogen",
            ],
            "clips_20": _build_20_clips_matrix("Auditoría Google Maps + Alta Velocidad 1/2000s"),
        },
        "agenda": {
            "updated_at": now_iso(),
            "today_blocks": [
                {"time": "08:30", "title": "Briefing CEO + Revisión Cola Último Trigger", "owner": "chief_of_staff", "channel": "Dashboard :8765"},
                {"time": "09:15", "title": "Extractor Web + Lote Diario Zoho (25 correos MTY/PV/Biogen)", "owner": "ventas_outreach", "channel": "Zoho chuy@"},
                {"time": "10:00", "title": "Cadencia Automática de Seguimiento 48h / 72h / Día 7", "owner": "ventas_outreach", "channel": "Zoho + WA Web"},
                {"time": "13:00", "title": "Negociación de Respuestas + Links Calendly 15 min", "owner": "ventas_outreach", "channel": "Calendly"},
                {"time": "16:30", "title": "Batch Creativo Pull (OpusClip 9:16 + Meta Suite + TikTok)", "owner": "conan_content", "channel": "Meta/TT/LI"},
                {"time": "18:15", "title": "Iteración A/B Diaria + Cierre Contador", "owner": "marky_marketing", "channel": "Iterador A/B"},
            ],
            "tomorrow_blocks": [
                {"time": "08:30", "title": "Despertador 24/7: Resumen CEO & Cola Follow-up 48h", "owner": "chief_of_staff", "channel": "Scheduler"},
                {"time": "09:15", "title": "Lote Diario Zoho A/B optimizado con ganador del día previo", "owner": "ventas_outreach", "channel": "Zoho chuy@"},
                {"time": "10:00", "title": "Disparo Seguimientos 48h/72h (-35% / 2do Momento)", "owner": "ventas_outreach", "channel": "WA / Zoho"},
                {"time": "18:15", "title": "Iteración nocturna de tasas de respuesta y promoción de gancho", "owner": "marky_marketing", "channel": "Iterador A/B"},
            ],
            "tomorrow_reminders_log": [],
        },
        "crm_records": {},
        "mail_campaigns_log": [],
        "whatsapp_web_log": [],
        "apify_sweeps_log": [],
        "daily_automation": _default_daily_automation(),
        "scheduler": {
            "enabled": True,
            "last_tick": None,
            "ran_slots_today": {},
            "slots": list(_DEFAULT_SCHEDULER_SLOTS),
        },
    }


def _build_20_clips_matrix(topic: str) -> list[dict[str, Any]]:
    hooks = [
        ("¿Tu negocio abre en Google Maps con el carrito gris de Street View?", "Dolor Maps", "OpusClip + OBS"),
        ("Así se ve congelar acción real a 1/2000s Global Shutter vs foto normal.", "Técnica 1/2000s", "Aftershoot + CapCut"),
        ("Por qué un trofeo acrílico LED genera menciones que un diploma nunca logra.", "Acrílico LED", "Captions App"),
        ("3 segundos en Google Maps deciden si un padre agenda visita en tu colegio.", "Colegios & Kínders", "OBS + OpusClip"),
        ("Cómo se autofinancia la cobertura fotográfica de un torneo con patrocinadores.", "Pádel / Sponsor", "Captions App"),
        ("Por qué las selfies de espejo distorsionan tu progreso físico (luz escultural).", "Captoora Biogen", "Evoto + CapCut"),
        ("Lo que pasa cuando un paciente compara dos consultorios dentales en Maps.", "Clínicas Salud", "OBS + Canva"),
        ("Halftime Blitz: cómo entregamos fotos editoriales en 15 minutos en cancha.", "Velocidad", "Aftershoot + Reels"),
        ("El error #1 en enlaces de Meta que provoca bloqueos entre FB, IG y WhatsApp.", "Meta Portfolio", "Captions App"),
        ("De ficha 'Sin Reclamar' a vitrina verificada lista para recibir citas.", "Conversión Maps", "OBS + CapCut"),
        ("Por qué dividimos pago digital mismo día y piezas físicas LED en taller (3–5d).", "Transparencia SLA", "Captions App"),
        ("Antes vs. Después real: gimnasio TotalPass renovado para cerrar inscripciones.", "Gyms & TotalPass", "Canva + CapCut"),
        ("El ángulo exacto que piden las marcas patrocinadoras para renovar en 2027.", "B2B Patrocinios", "LinkedIn Clip"),
        ("Cómo una academia financia su festival navideño sin descapitalizar la escuela.", "Danza White-Glove", "Captions App"),
        ("El bucle de 5 años: una placa QR LED en recepción generando reseñas diarias.", "QR LED Reseñas", "OpusClip Pro"),
        ("Behind the scenes: calibración de luz escultural en menos de 12 minutos en sitio.", "Iluminación", "CapCut 9:16"),
        ("Cómo documentamos dieta + meal prep + físico como un Flow continuo.", "Biogen Flow", "Captions + Evoto"),
        ("Los 3 errores que hacen ver amateur a una marca deportiva en Instagram.", "Autoridad", "OpusClip Pro"),
        ("Qué revisamos gratis en menos de 24h en tu ficha actual de Google Maps.", "Lead Magnet", "OBS + Captions"),
        ("Resumen semanal: cómo elevar tu vitrina 2027 con -35% vigente antes de cierre.", "Oferta Directa", "Meta Suite + TT"),
    ]
    platforms = ["IG Reels + TikTok", "TikTok + Shorts", "IG Reels + FB", "LinkedIn B2B"]
    clips: list[dict[str, Any]] = []
    for idx, (hook, pillar, tool) in enumerate(hooks, start=1):
        clips.append(
            {
                "clip_num": idx,
                "id": f"CLIP-{idx:02d}",
                "topic": topic,
                "pillar": pillar,
                "hook_0_3s": hook,
                "duration": "18–32s",
                "tool": tool,
                "platform": platforms[(idx - 1) % len(platforms)],
                "cta": "Pide tu lámina Antes/Después en captoora.studio/sports o WA +52 81 4005 0088",
            }
        )
    return clips


def get_or_init_growth_state() -> dict[str, Any]:
    state = read_json(FILES["growth_suite"], default=None)
    if not isinstance(state, dict) or "ceo_plan" not in state:
        state = _default_growth_state()
        write_json(FILES["growth_suite"], state)
        return state

    changed = False
    defaults_da = _default_daily_automation()
    da = state.get("daily_automation")
    if not isinstance(da, dict):
        state["daily_automation"] = defaults_da
        changed = True
    else:
        for k, v in defaults_da.items():
            if k not in da:
                da[k] = v
                changed = True
            elif isinstance(v, dict) and isinstance(da[k], dict):
                for sub_k, sub_v in v.items():
                    if sub_k not in da[k]:
                        da[k][sub_k] = sub_v
                        changed = True

    cal = state.setdefault("calendly", {})
    if not str(cal.get("base_url") or "").strip():
        cal["base_url"] = os.getenv("CALENDLY_BASE_URL", "").strip() or "https://calendly.com/captoora"
        changed = True

    sched = state.setdefault("scheduler", {"enabled": True, "slots": []})
    existing_ids = {s.get("id") for s in sched.get("slots", []) if isinstance(s, dict)}
    if any(slot["id"] not in existing_ids for slot in _DEFAULT_SCHEDULER_SLOTS):
        by_id = {s.get("id"): s for s in sched.get("slots", []) if isinstance(s, dict) and s.get("id")}
        for slot in _DEFAULT_SCHEDULER_SLOTS:
            by_id.setdefault(slot["id"], slot)
        ordered = [by_id[slot["id"]] for slot in _DEFAULT_SCHEDULER_SLOTS]
        sched["slots"] = ordered
        changed = True

    if changed:
        write_json(FILES["growth_suite"], state)
    return state


# ------------------------------------------------------------------------------
# 1. AGENTE CONTADOR (PFAE 612 SAT + CANDADO $0 PAUTA HASTA VENTAS COBRADAS)
# ------------------------------------------------------------------------------
def compute_accountant_snapshot() -> dict[str, Any]:
    """Compute real cashflow, SAT 612 taxes (IVA 16% + ISR provision), ads budget gate, and first-sale forecast."""
    ledger = read_json(FILES["accounting"], default={}) or {}
    fiscal = ledger.get("fiscal_profile") or {
        "regime_code": "612",
        "regime_name": "Persona Física con Actividades Empresariales y Profesionales",
        "rfc": "GUFJ870801NA6",
        "iva_rate_pct": 16.0,
        "isr_reserve_pct": 20.0,
        "pm_isr_retention_pct": 10.0,
        "pm_iva_retention_pct": 10.67,
        "ads_reinvestment_pct": 20.0,
    }
    cash = ledger.get("cashflow_ledger") or {"paid_sales": [], "expenses": [], "ads_spend_log": []}
    paid_sales = cash.get("paid_sales", [])
    expenses = cash.get("expenses", [])
    ads_spend_log = cash.get("ads_spend_log", [])

    iva_rate = float(fiscal.get("iva_rate_pct", 16.0)) / 100.0
    isr_rate = float(fiscal.get("isr_reserve_pct", 20.0)) / 100.0
    reinvest_rate = float(fiscal.get("ads_reinvestment_pct", 20.0)) / 100.0

    gross_collected = 0.0
    direct_production_costs = 0.0
    iva_collected_total = 0.0
    pm_retentions_total = 0.0
    subtotal_sales_ex_iva = 0.0

    for sale in paid_sales:
        amt = float(sale.get("amount_collected_mxn") or 0.0)
        direct_cost = float(sale.get("direct_cost_mxn") or 0.0)
        includes_iva = bool(sale.get("includes_iva", True))
        is_pm = bool(sale.get("client_is_persona_moral", False))

        if includes_iva:
            base_subtotal = amt / (1.0 + iva_rate)
            iva_part = amt - base_subtotal
        else:
            base_subtotal = amt
            iva_part = 0.0

        pm_isr_ret = base_subtotal * (float(fiscal.get("pm_isr_retention_pct", 10.0)) / 100.0) if is_pm else 0.0
        gross_collected += amt
        subtotal_sales_ex_iva += base_subtotal
        iva_collected_total += iva_part
        direct_production_costs += direct_cost
        pm_retentions_total += pm_isr_ret

    deductible_expenses = sum(float(e.get("amount_mxn") or 0.0) for e in expenses)
    # IVA acreditable aproximado sobre gastos facturados con IVA
    iva_creditable = sum(
        (float(e.get("amount_mxn") or 0.0) - float(e.get("amount_mxn") or 0.0) / (1.0 + iva_rate))
        for e in expenses
        if e.get("has_cfdi_iva", True)
    )
    iva_payable_sat = max(0.0, iva_collected_total - iva_creditable)

    taxable_profit = max(0.0, subtotal_sales_ex_iva - direct_production_costs - deductible_expenses)
    isr_estimated_reserve = max(0.0, taxable_profit * isr_rate - pm_retentions_total)
    total_tax_reserve = round(iva_payable_sat + isr_estimated_reserve, 2)

    ads_already_spent = sum(float(a.get("amount_mxn") or 0.0) for a in ads_spend_log)
    free_net_profit = round(
        gross_collected - direct_production_costs - deductible_expenses - total_tax_reserve,
        2,
    )

    ads_unlocked = len(paid_sales) > 0 and free_net_profit > 0.0
    authorized_ads_budget = round(max(0.0, free_net_profit * reinvest_rate - ads_already_spent), 2) if ads_unlocked else 0.0

    # Platform allocation strictly gated by unlocked budget ($0 when no sales yet)
    platform_allocations = [
        {"platform": "Google Search Ads", "share_pct": 40, "authorized_mxn": round(authorized_ads_budget * 0.40, 2), "role": "Alta intención (quien ya busca servicios)"},
        {"platform": "Meta Ads (IG/FB Remarketing)", "share_pct": 30, "authorized_mxn": round(authorized_ads_budget * 0.30, 2), "role": "Retargeting a visitas + Clips Antes/Después"},
        {"platform": "TikTok Spark Ads", "share_pct": 15, "authorized_mxn": round(authorized_ads_budget * 0.15, 2), "role": "Solo empujar Top 2 clips orgánicos ganadores"},
        {"platform": "MercadoLibre Ads (SKU Acrílico LED)", "share_pct": 15, "authorized_pct_note": "Solo producto físico QR/Trofeo LED", "authorized_mxn": round(authorized_ads_budget * 0.15, 2), "role": "Embudo físico de negocios compradores"},
        {"platform": "ChatGPT / Bing Search AEO", "share_pct": 0, "authorized_mxn": 0.0, "role": "Visibilidad orgánica vía llms.txt + Schema ($0 pauta)"},
    ]

    # Pipeline forecast from real data
    queue = read_json(FILES["approvals"], default={"items": []}) or {"items": []}
    q_items = queue.get("items", [])
    approved_cnt = sum(1 for i in q_items if i.get("status") == "approved")
    pending_cnt = sum(1 for i in q_items if i.get("status") == "pending_trigger")
    audits = read_json(FILES["gmaps_audits"], default={"deficient_count": 68}) or {"deficient_count": 68}
    deficient_cnt = int(audits.get("deficient_count") or 68)

    # First-sale forecast grounded transparently in ticket catalog and safe daily cadence
    entry_ticket_avg = 5135.0
    expected_advance_50 = round(entry_ticket_avg * 0.5, 2)
    sample_first_sale_unlocked_ads = round((expected_advance_50 - 450.0) * 0.68 * reinvest_rate, 2)

    return {
        "updated_at": now_iso(),
        "fiscal_profile": fiscal,
        "summary": {
            "paid_sales_count": len(paid_sales),
            "gross_collected_mxn": round(gross_collected, 2),
            "direct_production_costs_mxn": round(direct_production_costs, 2),
            "deductible_expenses_mxn": round(deductible_expenses, 2),
            "iva_payable_sat_mxn": round(iva_payable_sat, 2),
            "isr_estimated_reserve_mxn": round(isr_estimated_reserve, 2),
            "total_tax_reserve_mxn": total_tax_reserve,
            "free_net_profit_mxn": free_net_profit,
            "ads_already_spent_mxn": round(ads_already_spent, 2),
            "ads_unlocked": ads_unlocked,
            "authorized_ads_budget_mxn": authorized_ads_budget,
            "ads_gate_status": (
                f"DESBLOQUEADO: ${authorized_ads_budget:,.0f} MXN autorizados ({int(reinvest_rate * 100)}% utilidad libre neta)"
                if ads_unlocked
                else "BLOQUEADO EN $0 MXN · Regla Cero Deuda activa hasta cobrar la 1ª venta real"
            ),
        },
        "platform_allocations": platform_allocations,
        "first_sale_forecast": {
            "active_pipeline": {
                "approved_ready": approved_cnt,
                "pending_trigger": pending_cnt,
                "deficient_gmaps_targets": deficient_cnt,
            },
            "estimated_window": "Días 5 a 10 manteniendo 15–20 WA Web + 20–30 correos Zoho diarios",
            "expected_first_advance_50_mxn": expected_advance_50,
            "estimated_ads_unlock_on_first_sale_mxn": sample_first_sale_unlocked_ads,
            "note": "Proyección operativa referencial; el desbloqueo real ocurre al registrar el cobro en caja.",
        },
        "recent_sales": paid_sales[:12],
        "recent_expenses": expenses[:12],
    }


def record_accountant_sale(
    *,
    client_name: str,
    package_ref: str,
    amount_collected_mxn: float,
    direct_cost_mxn: float = 0.0,
    includes_iva: bool = True,
    client_is_persona_moral: bool = False,
    payment_phase: str = "Anticipo 50%",
) -> dict[str, Any]:
    ledger = read_json(FILES["accounting"], default={}) or {}
    cash = ledger.setdefault("cashflow_ledger", {"paid_sales": [], "expenses": [], "ads_spend_log": []})
    entry = {
        "id": f"VTA-{len(cash.get('paid_sales', [])) + 1:03d}",
        "recorded_at": now_iso(),
        "client_name": client_name.strip(),
        "package_ref": package_ref.strip(),
        "payment_phase": payment_phase,
        "amount_collected_mxn": round(float(amount_collected_mxn), 2),
        "direct_cost_mxn": round(float(direct_cost_mxn), 2),
        "includes_iva": bool(includes_iva),
        "client_is_persona_moral": bool(client_is_persona_moral),
    }
    cash.setdefault("paid_sales", []).insert(0, entry)
    ledger["cashflow_ledger"] = cash
    write_json(FILES["accounting"], ledger)
    snap = compute_accountant_snapshot()
    append_agent_event(
        "contabilidad_finanzas",
        f"Registró cobro {entry['id']}",
        f"{entry['client_name']} · +${entry['amount_collected_mxn']:,.0f} MXN · Bolsa Ads: ${snap['summary']['authorized_ads_budget_mxn']:,.0f} MXN.",
        zone="boveda_finanzas",
        source="human_ui",
    )
    return {"sale": entry, "accountant": snap}


def record_accountant_expense(
    *,
    concept: str,
    amount_mxn: float,
    category: str = "Taller / Producción",
    has_cfdi_iva: bool = True,
) -> dict[str, Any]:
    ledger = read_json(FILES["accounting"], default={}) or {}
    cash = ledger.setdefault("cashflow_ledger", {"paid_sales": [], "expenses": [], "ads_spend_log": []})
    entry = {
        "id": f"GAS-{len(cash.get('expenses', [])) + 1:03d}",
        "recorded_at": now_iso(),
        "concept": concept.strip(),
        "category": category.strip(),
        "amount_mxn": round(float(amount_mxn), 2),
        "has_cfdi_iva": bool(has_cfdi_iva),
    }
    cash.setdefault("expenses", []).insert(0, entry)
    write_json(FILES["accounting"], ledger)
    snap = compute_accountant_snapshot()
    append_agent_event(
        "contabilidad_finanzas",
        f"Registró gasto {entry['id']}",
        f"{entry['concept']} · -${entry['amount_mxn']:,.0f} MXN.",
        zone="boveda_finanzas",
        source="human_ui",
    )
    return {"expense": entry, "accountant": snap}


def update_fiscal_config(
    *,
    isr_reserve_pct: float | None = None,
    ads_reinvestment_pct: float | None = None,
) -> dict[str, Any]:
    ledger = read_json(FILES["accounting"], default={}) or {}
    fiscal = ledger.setdefault("fiscal_profile", {})
    if isr_reserve_pct is not None:
        fiscal["isr_reserve_pct"] = round(max(0.0, min(float(isr_reserve_pct), 45.0)), 2)
    if ads_reinvestment_pct is not None:
        fiscal["ads_reinvestment_pct"] = round(max(0.0, min(float(ads_reinvestment_pct), 50.0)), 2)
    write_json(FILES["accounting"], ledger)
    return compute_accountant_snapshot()


def audit_contract_financial_and_tax(contract_text: str) -> dict[str, Any]:
    """Audit contract clauses from a Mexican Persona Física Actividad Empresarial (612) fiscal + cashflow view."""
    txt = (contract_text or "").lower()
    alerts: list[str] = []
    if any(k in txt for k in ("60 días", "90 días", "120 días", "net 60", "net 90")):
        alerts.append("FOCO ROJO FLUJO: Plazo de pago >=60 días descapitaliza producción e impuestos IVA del mes de facturación.")
    if any(k in txt for k in ("persona moral", "s.a. de c.v.", "s.a.p.i.", "s. de r.l.", "retención", "retencion")):
        alerts.append("AVISO FISCAL 612: Si el cliente es Persona Moral y facturas servicios profesionales, verifica retenciones 10% ISR + 2/3 IVA en el CFDI.")
    if any(k in txt for k in ("patrimoniales y morales", "cesión total", "cesion total")):
        alerts.append("FOCO ROJO LFDA: Pretenden ceder derechos morales/patrimoniales totales; limitar a licencia de uso editorial sin perder portafolio.")
    if "50%" not in txt and "anticipo" not in txt:
        alerts.append("ALERTA CAJA: No menciona 50% de anticipo obligatorio; agregar antes de bloquear fecha.")
    if not alerts:
        alerts.append("OK FINANCIERO: Sin cláusulas críticas detectadas; validar RFC/Régimen 612 (GUFJ870801NA6) y uso CFDI G03.")

    append_agent_event(
        "contabilidad_finanzas",
        "Auditoría Fiscal de Contrato",
        f"Detectó {len(alerts)} punto(s) fiscales/financieros PFAE 612.",
        zone="boveda_finanzas",
        source="human_ui",
    )
    return {"regime": "612 PFAE · GUFJ870801NA6", "alerts": alerts}


# ------------------------------------------------------------------------------
# 2. SEO/AEO READINESS + 20 CLIPS + CEO PERSONAL + REPORTES + AGENDA + CALENDLY
# ------------------------------------------------------------------------------
def get_seo_aeo_status() -> dict[str, Any]:
    portal_html = (ROOT_DIR / "captoora_sports.html").read_text(encoding="utf-8") if (ROOT_DIR / "captoora_sports.html").exists() else ""
    state = get_or_init_growth_state()
    tr = state.get("tracking_ids", {})
    return {
        "sitemap_xml_ready": (ROOT_DIR / "sitemap.xml").exists(),
        "robots_txt_ready": (ROOT_DIR / "robots.txt").exists(),
        "llms_txt_ready": (ROOT_DIR / "llms.txt").exists(),
        "json_ld_ready": "application/ld+json" in portal_html and "ProfessionalService" in portal_html,
        "no_neighborhood_brag": "San Jerónimo, Monterrey" not in portal_html[:1200],
        "ga4_configured": bool(tr.get("ga4_id")),
        "meta_pixel_configured": bool(tr.get("meta_pixel_id")),
        "note": "Cimientos SEO + AEO listos localmente. Sube sitemap.xml/robots.txt/llms.txt a captoora.studio y verifica Search Console + Bing Webmaster Tools para captar ChatGPT Search.",
    }


def refresh_ceo_weekly_plan(custom_focus: str | None = None) -> dict[str, Any]:
    state = get_or_init_growth_state()
    acct = compute_accountant_snapshot()
    focus = (
        custom_focus.strip()
        if custom_focus and custom_focus.strip()
        else (
            "Fase Despegue Cero Deuda: convertir las 4 aprobaciones listas + 68 fichas Street View con mensajes por técnica/velocidad hasta cobrar el 1er anticipo 50% y liberar Ads."
            if not acct["summary"]["ads_unlocked"]
            else f"Escala Controlada: reinvertir ${acct['summary']['authorized_ads_budget_mxn']:,.0f} MXN de utilidad neta en Google/Meta/Spark + 20 clips semanales."
        )
    )
    state["ceo_plan"] = {
        **state.get("ceo_plan", {}),
        "updated_at": now_iso(),
        "week_focus": focus,
    }
    state["updated_at"] = now_iso()
    write_json(FILES["growth_suite"], state)
    append_agent_event("chief_of_staff", "Actualizó Plan CEO", focus[:160], zone="mesa_directiva", source="human_ui")
    return state["ceo_plan"]


def generate_20_clips_plan(topic: str) -> dict[str, Any]:
    clean_topic = topic.strip() or "Auditoría Google Maps + Alta Velocidad 1/2000s"
    state = get_or_init_growth_state()
    clips = _build_20_clips_matrix(clean_topic)
    for c in clips:
        bad = validate_client_copy(f"{c['hook_0_3s']} {c['cta']}")
        if bad:
            raise ValueError(f"Guardrail bloqueó clip {c['id']}: {bad}")
    state["seo_and_clips"] = {
        **state.get("seo_and_clips", {}),
        "updated_at": now_iso(),
        "last_topic": clean_topic,
        "clips_20": clips,
    }
    state["updated_at"] = now_iso()
    write_json(FILES["growth_suite"], state)
    append_agent_event(
        "conan_content",
        "Transformó Tema en 20 Clips",
        f"20 guiones listos para OpusClip/Captions/Lupe sobre: {clean_topic[:80]}",
        target_agent="lupe_social",
        zone="estudio_conan",
        source="human_ui",
    )
    return state["seo_and_clips"]


def compute_weekly_report() -> dict[str, Any]:
    queue = read_json(FILES["approvals"], default={"items": []}) or {"items": []}
    q_items = queue.get("items", [])
    state = get_or_init_growth_state()
    crm = state.get("crm_records", {})
    acct = compute_accountant_snapshot()
    geo_routes = read_json(FILES["routes_log"], default={"routes": []}) or {"routes": []}

    pending = sum(1 for i in q_items if i.get("status") == "pending_trigger")
    approved = sum(1 for i in q_items if i.get("status") == "approved")
    wa_sent = len(state.get("whatsapp_web_log", []))
    mail_sent = sum(1 for m in state.get("mail_campaigns_log", []) if not m.get("dry_run"))
    calendly_links = len((state.get("calendly") or {}).get("generated_links", []))
    replied = sum(1 for r in crm.values() if isinstance(r, dict) and r.get("stage") in ("Respondio", "Calendly", "Cotizado", "Anticipo_50", "Cerrado"))
    followup_due = sum(1 for r in crm.values() if isinstance(r, dict) and r.get("stage") == "Contactado")

    return {
        "generated_at": now_iso(),
        "funnel_metrics": {
            "pending_trigger": pending,
            "approved_in_queue": approved,
            "whatsapp_web_sent": wa_sent,
            "zoho_emails_sent": mail_sent,
            "crm_replied_or_advanced": replied,
            "calendly_links_generated": calendly_links,
            "followups_24_48h_due": followup_due,
            "routes_logged": len(geo_routes.get("routes", [])),
        },
        "accountant_summary": acct["summary"],
        "seo_status": get_seo_aeo_status(),
    }


# ------------------------------------------------------------------------------
# 3. MAIL MARKETING ZOHO + EXTRACTOR DE CORREOS DE SITIOS WEB + MAILERFIND
# ------------------------------------------------------------------------------
def _extract_valid_emails(html_text: str) -> list[str]:
    found: list[str] = []
    for em in EMAIL_REGEX.findall(html_text or ""):
        low = em.lower()
        if not any(bad in low for bad in (".png", ".jpg", ".jpeg", ".svg", ".webp", "wixpress.com", "sentry.io", "example.com", "domain.com", "email.com", "tuempresa.com")):
            if low not in found:
                found.append(low)
    return found


def _collect_multi_territory_prospects() -> list[dict[str, Any]]:
    """Aggregate normalized prospect rows across Monterrey/SPGG, Puerto Vallarta (3 zones), and Biogen Alliances."""
    data_root = FILES["leads"].parent
    seen: set[str] = set()
    rows: list[dict[str, Any]] = []

    def _is_scannable_site(url: str) -> bool:
        u = str(url or "").strip()
        if not u.startswith("http"):
            return False
        low = u.lower()
        return not any(s in low for s in ("instagram.com", "facebook.com", "google.com/maps", "tiktok.com", "wa.me", "youtube.com"))

    # 1. Biogen Alliances (often include pre-extracted emails & specific PDFs)
    bio_path = data_root / "alianzas_biogen_mty.json"
    if bio_path.exists():
        bio = read_json(bio_path, default={}) or {}
        for item in bio.get("leads", []):
            if not isinstance(item, dict):
                continue
            name = str(item.get("nombre") or "").strip()
            slug = str(item.get("slug") or slugify(name))
            if not name or slug in seen:
                continue
            seen.add(slug)
            pilar = str(item.get("pilar") or "")
            pdf_rel = (
                "docs/Propuesta_Captoora_Biogen_Cocina_Aliada.pdf"
                if "cocina" in pilar
                else "docs/Propuesta_Captoora_Biogen_Gimnasio_Club.pdf"
            )
            site = str(item.get("sitio_web") or "")
            rows.append(
                {
                    "slug": slug,
                    "nombre": name,
                    "territory": "biogen",
                    "nicho": str(item.get("categoria") or pilar or "Alianza Biogen"),
                    "zona": str(item.get("zona") or item.get("municipio") or "MTY"),
                    "telefono": str(item.get("telefono") or ""),
                    "sitio_web": site if _is_scannable_site(site) else "",
                    "email": str(item.get("email") or "").strip().lower(),
                    "offer_track": "biogen",
                    "pdf_rel_path": pdf_rel,
                    "demo_rel_path": "",
                    "audit_flags": item.get("audit_flags") or [],
                }
            )

    # 2. Puerto Vallarta (3 strict separated zones)
    for zone in ("zona_romantica", "zona_hotelera", "centro_y_bahia"):
        pv_path = data_root / "puerto_vallarta" / zone / "gmaps_audits.json"
        if not pv_path.exists():
            continue
        pv_data = read_json(pv_path, default={"audits": []}) or {"audits": []}
        for item in pv_data.get("audits", []):
            name = str(item.get("nombre") or "").strip()
            slug = str(item.get("slug") or slugify(name))
            if not name or slug in seen:
                continue
            seen.add(slug)
            site = str(item.get("sitio_web") or "")
            rows.append(
                {
                    "slug": slug,
                    "nombre": name,
                    "territory": "pv",
                    "nicho": str(item.get("nicho") or item.get("categoria") or "Hospitalidad & Comercios"),
                    "zona": str(item.get("subzona") or item.get("zona") or zone),
                    "telefono": str(item.get("telefono") or ""),
                    "sitio_web": site if _is_scannable_site(site) else "",
                    "email": "",
                    "offer_track": "small_business",
                    "pdf_rel_path": str(item.get("dossier_pdf_path") or ""),
                    "demo_rel_path": f"docs/demos_pv/{zone}/{slug}.html",
                    "audit_flags": item.get("audit_flags") or [],
                }
            )

    # 3. Monterrey / SPGG core leads + audits
    audits_idx = read_json(FILES["gmaps_audits"], default={"audits": []}) or {"audits": []}
    audit_by_slug = {a.get("slug"): a for a in audits_idx.get("audits", []) if a.get("slug")}
    mty_leads = read_json(FILES["leads"], default=[]) or []
    for item in mty_leads:
        name = str(item.get("nombre") or "").strip()
        slug = slugify(name)
        if not name or slug in seen:
            continue
        seen.add(slug)
        audit = audit_by_slug.get(slug, {})
        site = str(item.get("sitio_web") or "")
        nicho = str(item.get("nicho") or "Small Business")
        track = "navidad_led" if any(k in nicho.lower() for k in ("pádel", "padel", "danza", "baile")) else "small_business"
        rows.append(
            {
                "slug": slug,
                "nombre": name,
                "territory": "mty",
                "nicho": nicho,
                "zona": str(item.get("zona") or item.get("municipio") or "MTY / SPGG"),
                "telefono": str(item.get("telefono") or ""),
                "sitio_web": site if _is_scannable_site(site) else "",
                "email": "",
                "offer_track": track,
                "pdf_rel_path": str(audit.get("dossier_pdf_path") or f"assets/mockups/small_biz/{slug}_Dossier_SMB_2027.pdf"),
                "demo_rel_path": "",
                "audit_flags": audit.get("audit_flags") or [],
            }
        )
    return rows


def _sync_preseeded_emails_into_crm(state: dict[str, Any], candidates: list[dict[str, Any]]) -> int:
    crm = state.setdefault("crm_records", {})
    imported = 0
    for c in candidates:
        em = c.get("email")
        if not em:
            continue
        row = crm.setdefault(c["slug"], {"slug": c["slug"], "nombre": c["nombre"], "stage": "Nuevo"})
        if not row.get("email"):
            row["email"] = em
            row["email_source"] = "apify_preseeded"
            imported += 1
        row.setdefault("territory", c["territory"])
        row.setdefault("nicho", c["nicho"])
        if c.get("telefono") and not row.get("phone"):
            row["phone"] = c["telefono"]
    return imported


def _fetch_emails_from_url(url: str) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0 CaptooraB2BContactFinder/1.0"}
    found: list[str] = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as resp:
            html = resp.read(140_000).decode("utf-8", errors="ignore")
        found.extend(_extract_valid_emails(html))
        if not found:
            parsed = urllib.parse.urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            for suffix in ("/contacto", "/contact"):
                try:
                    c_req = urllib.request.Request(base_url + suffix, headers=headers)
                    with urllib.request.urlopen(c_req, timeout=4) as c_resp:
                        c_html = c_resp.read(120_000).decode("utf-8", errors="ignore")
                    found.extend(_extract_valid_emails(c_html))
                    if found:
                        break
                except Exception:
                    continue
    except Exception:
        return []
    return list(dict.fromkeys(found))


def enrich_emails_from_websites(limit: int = 18) -> dict[str, Any]:
    """Import preseeded Biogen emails and scan public MTY/PV/Biogen websites without repeating scanned URLs."""
    state = get_or_init_growth_state()
    da = state.setdefault("daily_automation", _default_daily_automation())
    scanned_urls: list[str] = da.setdefault("scanned_urls", [])
    scanned_set = set(scanned_urls)

    all_candidates = _collect_multi_territory_prospects()
    preseeded_imported = _sync_preseeded_emails_into_crm(state, all_candidates)
    crm = state.setdefault("crm_records", {})

    by_terr: dict[str, list[dict[str, Any]]] = {"mty": [], "pv": [], "biogen": []}
    for c in all_candidates:
        site = c.get("sitio_web") or ""
        if site and site not in scanned_set and not (crm.get(c["slug"], {}) or {}).get("email"):
            by_terr.setdefault(c["territory"], []).append(c)

    ordered_scan: list[dict[str, Any]] = []
    max_len = max((len(v) for v in by_terr.values()), default=0)
    for idx in range(max_len):
        for tk in ("mty", "pv", "biogen"):
            if idx < len(by_terr[tk]):
                ordered_scan.append(by_terr[tk][idx])

    checked = 0
    found_rows: list[dict[str, Any]] = []
    for lead in ordered_scan[: max(1, min(limit, 30))]:
        url = lead["sitio_web"]
        checked += 1
        if url not in scanned_set:
            scanned_urls.append(url)
            scanned_set.add(url)
        emails_found = _fetch_emails_from_url(url)
        if emails_found:
            row = crm.setdefault(lead["slug"], {"slug": lead["slug"], "nombre": lead["nombre"], "stage": "Nuevo"})
            row["email"] = emails_found[0]
            row["email_source"] = f"website_public ({url})"
            row["territory"] = lead["territory"]
            row["nicho"] = lead["nicho"]
            if lead.get("telefono") and not row.get("phone"):
                row["phone"] = lead["telefono"]
            found_rows.append({"slug": lead["slug"], "nombre": lead["nombre"], "territory": lead["territory"], "email": emails_found[0]})

    da["scanned_urls"] = scanned_urls[-600:]
    state["updated_at"] = now_iso()
    write_json(FILES["growth_suite"], state)
    append_agent_event(
        "scouting_radar",
        "Enriqueció Correos Web (Multi-Territorio)",
        f"Importó {preseeded_imported} pre-extraídos, escaneó {checked} webs y halló {len(found_rows)} correos nuevos.",
        zone="radar_maps",
        source="human_ui",
    )
    return {"checked_websites": checked, "preseeded_imported": preseeded_imported, "emails_found": found_rows}


def send_growth_mail_campaign(
    *,
    to_email: str,
    prospect_name: str,
    offer_track: str = "small_business",
    attach_slug: str = "",
    dry_run: bool = True,
) -> dict[str, Any]:
    """Send or dry-run a client-safe campaign email via Zoho SMTP (chuy@captoora.studio) with optional personalized PDF."""
    offer_map = {
        "small_business": (
            f"{prospect_name}: Comparativa visual en Google Maps & Producción 2027 (-35%)",
            "Renovación visual completa en su sede (iluminación calibrada + entrega en 48–72h + carga directa a Google Maps y Meta Business Portfolio sin bloqueos), desde $3,900 MXN (-35%).",
        ),
        "navidad_led": (
            f"{prospect_name}: Cobertura mismo día 1/2000s + Trofeos LED financiables (-35%)",
            "Fotografía deportiva Halftime Blitz (entrega en 15 minutos el mismo día) con opción de trofeos en acrílico óptico iluminados con luz LED cálida (taller artesanal 3–5 días hábiles).",
        ),
        "biogen": (
            f"{prospect_name}: Programa Piloto Captoora Biogen · Registro Semanal de Élite",
            "Documentación semanal en estudio con esquema de luz escultural controlado y clips verticales 9:16 listos para potenciar historias y Reels.",
        ),
    }
    subject, pitch = offer_map.get(offer_track, offer_map["small_business"])
    calendly = get_or_init_growth_state().get("calendly", {}).get("base_url") or "https://captoora.studio/sports"

    html_body = f"""
    <div style="background:#050608;color:#f5f4ef;font-family:Arial,sans-serif;padding:28px;border:1px solid #c9a23f;border-radius:12px;">
      <p style="color:#c9a23f;font-size:11px;letter-spacing:2px;margin:0 0 8px;">CAPTOORA STUDIO · PRODUCCIÓN EDITORIAL 1/2000s</p>
      <h2 style="margin:0 0 12px;color:#f5f4ef;">Hola equipo de {prospect_name},</h2>
      <p style="line-height:1.55;color:#d2d5de;">{pitch}</p>
      <p style="line-height:1.55;color:#d2d5de;">Vamos directo a su sede en Monterrey y San Pedro o cubrimos su evento con entrega digital ágil.</p>
      <p style="margin:18px 0;">
        <a href="https://captoora.studio/sports" style="background:#c5a880;color:#050608;padding:10px 18px;border-radius:8px;text-decoration:none;font-weight:bold;">Ver Portafolio 3D</a>
        &nbsp;&nbsp;
        <a href="{calendly}" style="border:1px solid #c5a880;color:#c5a880;padding:10px 18px;border-radius:8px;text-decoration:none;">Agendar Diagnóstico 15 min</a>
      </p>
      <p style="font-size:12px;color:#98a2b3;">Jesús Gutiérrez · Captoora Studio · WhatsApp +52 81 4005 0088 · chuy@captoora.studio</p>
    </div>
    """

    attachments: list[Path] = []
    if attach_slug:
        pdf_candidate = ROOT_DIR / "assets" / "mockups" / "small_biz" / f"{slugify(attach_slug)}_Dossier_SMB_2027.pdf"
        if pdf_candidate.exists():
            attachments.append(pdf_candidate)

    result = send_email_via_zoho(
        to_email=to_email,
        subject=subject,
        html_body=html_body,
        attachments=attachments,
        dry_run=dry_run,
    )
    state = get_or_init_growth_state()
    state.setdefault("mail_campaigns_log", []).insert(
        0,
        {
            "timestamp": now_iso(),
            "to_email": to_email,
            "prospect_name": prospect_name,
            "offer_track": offer_track,
            "dry_run": dry_run,
            "status": result.get("mode") or ("sent" if result.get("sent") else "dry_run"),
            "attachments": [p.name for p in attachments],
        },
    )
    state["mail_campaigns_log"] = state["mail_campaigns_log"][:60]
    write_json(FILES["growth_suite"], state)
    return {**result, "smtp_status": get_smtp_status()}


# ------------------------------------------------------------------------------
# 4. CALENDLY CONTROL + AGENDA TOMORROW REMINDER + APIFY SWEEP + CRM KYC
# ------------------------------------------------------------------------------
def generate_calendly_client_link(*, prospect_name: str, slug: str = "", event_type_id: str = "maps_audit_15") -> dict[str, Any]:
    state = get_or_init_growth_state()
    cal = state.setdefault("calendly", {})
    base = (cal.get("base_url") or os.getenv("CALENDLY_BASE_URL") or "https://calendly.com/captoora").strip().rstrip("/")
    ev = next((e for e in cal.get("event_types", []) if e["id"] == event_type_id), None) or {
        "id": event_type_id,
        "label": "Diagnóstico 15 min",
        "slug": "auditoria-maps-15m",
    }
    query = urllib.parse.urlencode(
        {
            "name": prospect_name.strip(),
            "utm_source": "captoora",
            "utm_campaign": ev["id"],
        }
    )
    url = f"{base}/{ev['slug']}?{query}"
    wa_msg = (
        f"Hola {prospect_name}, te comparto el enlace directo para apartar 15 minutos en agenda "
        f"y revisar sin costo tu propuesta visual: {url}"
    )
    violations = validate_client_copy(wa_msg)
    if violations:
        raise ValueError(f"Guardrail bloqueó mensaje Calendly: {violations}")

    rec = {
        "created_at": now_iso(),
        "prospect_name": prospect_name,
        "slug": slug or slugify(prospect_name),
        "event_type": ev["label"],
        "url": url,
        "whatsapp_message": wa_msg,
    }
    cal.setdefault("generated_links", []).insert(0, rec)
    cal["generated_links"] = cal["generated_links"][:50]
    write_json(FILES["growth_suite"], state)
    append_agent_event("ventas_outreach", "Generó Link Calendly", f"{prospect_name} -> {ev['slug']}", zone="desk_ventas", source="human_ui")
    return rec


def update_calendly_base_url(base_url: str) -> dict[str, Any]:
    state = get_or_init_growth_state()
    state.setdefault("calendly", {})["base_url"] = base_url.strip().rstrip("/")
    write_json(FILES["growth_suite"], state)
    return state["calendly"]


def trigger_tomorrow_reminder(*, send_email_to: str = "", dry_run: bool = True) -> dict[str, Any]:
    state = get_or_init_growth_state()
    blocks = state.get("agenda", {}).get("tomorrow_blocks", [])
    summary_lines = [f"- {b['time']} | {b['title']} ({b['channel']})" for b in blocks]
    body_text = "Agenda de Mañana Captoora Studio:\n" + "\n".join(summary_lines)
    email_res = None
    if send_email_to.strip():
        email_res = send_email_via_zoho(
            to_email=send_email_to.strip(),
            subject="Recordatorio Agenda de Mañana · Captoora Command",
            html_body="<pre style='font-family:monospace;background:#050608;color:#f5f4ef;padding:18px;'>" + body_text + "</pre>",
            plain_text=body_text,
            dry_run=dry_run,
        )
    rec = {"triggered_at": now_iso(), "blocks_count": len(blocks), "email_result": email_res, "text": body_text}
    state["agenda"].setdefault("tomorrow_reminders_log", []).insert(0, rec)
    write_json(FILES["growth_suite"], state)
    append_agent_event("chief_of_staff", "Recordatorio Agenda Mañana", f"{len(blocks)} bloques ordenados.", zone="mesa_directiva", source="human_ui")
    return rec


def upsert_crm_kyc(payload: dict[str, Any]) -> dict[str, Any]:
    state = get_or_init_growth_state()
    crm = state.setdefault("crm_records", {})
    slug = slugify(payload.get("slug") or payload.get("nombre") or "prospecto")
    existing = crm.get(slug, {"slug": slug})
    updated = {
        **existing,
        **{k: v for k, v in payload.items() if v is not None},
        "slug": slug,
        "updated_at": now_iso(),
    }
    crm[slug] = updated
    write_json(FILES["growth_suite"], state)

    ghl_webhook = os.getenv("GHL_WEBHOOK_URL", "").strip()
    ghl_dispatched = False
    if ghl_webhook and payload.get("sync_ghl"):
        try:
            req = urllib.request.Request(
                ghl_webhook,
                data=json.dumps(updated).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=6):
                ghl_dispatched = True
        except Exception:
            ghl_dispatched = False

    append_agent_event("ventas_outreach", f"Actualizó CRM/KYC ({updated.get('stage','Nuevo')})", str(updated.get("nombre") or slug), zone="desk_ventas", source="human_ui")
    return {"record": updated, "ghl_webhook_dispatched": ghl_dispatched}


# ------------------------------------------------------------------------------
# 5. WHATSAPP WEB 1-CLICK SUPERVISOR QUEUE (ZERO-BAN SAFE)
# ------------------------------------------------------------------------------
def get_whatsapp_web_supervisor_queue() -> dict[str, Any]:
    """Build safe 1-click WhatsApp Web dispatch list tracking daily cap (max 15-20/day)."""
    state = get_or_init_growth_state()
    queue = read_json(FILES["approvals"], default={"items": []}) or {"items": []}
    leads = read_json(FILES["leads"], default=[]) or []
    today_prefix = now_iso()[:10]
    wa_log = state.get("whatsapp_web_log", [])
    sent_today = sum(1 for row in wa_log if str(row.get("sent_at") or "").startswith(today_prefix))
    sent_slugs = {row.get("slug") for row in wa_log}

    cards: list[dict[str, Any]] = []
    # First priority: approved triggers waiting WhatsApp send
    for item in queue.get("items", []):
        phone = str(item.get("phone") or "").strip()
        if not phone:
            continue
        slug = slugify(str(item.get("target_name") or item.get("id")))
        text = str(item.get("draft_text") or "").strip()
        if validate_client_copy(text):
            continue
        try:
            digits = clean_phone_digits(phone)
        except ValueError:
            continue
        cards.append(
            {
                "id": item.get("id"),
                "slug": slug,
                "nombre": item.get("target_name"),
                "nicho": item.get("niche"),
                "phone": digits,
                "queue_status": item.get("status"),
                "already_sent_logged": slug in sent_slugs,
                "message": text,
                "web_whatsapp_url": f"https://web.whatsapp.com/send?phone={digits}&text={urllib.parse.quote(text)}",
                "attachments": item.get("attachments", []),
            }
        )

    # Second priority: top deficient/school/gym leads not yet in queue
    audits = read_json(FILES["gmaps_audits"], default={"audits": []}) or {"audits": []}
    for audit in audits.get("audits", [])[:35]:
        phone = str(audit.get("telefono") or "").strip()
        slug = str(audit.get("slug") or "")
        if not phone or not slug or slug in sent_slugs or any(c["slug"] == slug for c in cards):
            continue
        try:
            digits = clean_phone_digits(phone)
        except ValueError:
            continue
        pitch = (audit.get("outreach_modes") or {}).get("mode_b_diagnostico") or (
            f"Hola equipo de {audit.get('nombre')} 👋, soy Jesús Gutiérrez de Captoora Studio (https://captoora.studio/sports). "
            f"Preparamos su comparativa visual personalizada Antes vs. Después en Google Maps para proyectar su marca en 2027. ¿Te la comparto?"
        )
        if validate_client_copy(pitch):
            continue
        cards.append(
            {
                "id": f"AUD-{slug[:10].upper()}",
                "slug": slug,
                "nombre": audit.get("nombre"),
                "nicho": audit.get("nicho"),
                "phone": digits,
                "queue_status": "audit_ready",
                "already_sent_logged": False,
                "message": pitch,
                "web_whatsapp_url": f"https://web.whatsapp.com/send?phone={digits}&text={urllib.parse.quote(pitch)}",
                "attachments": [
                    {"type": "image", "path": audit.get("before_after_path")},
                    {"type": "pdf", "path": audit.get("dossier_pdf_path")},
                ],
            }
        )

    return {
        "mode": get_cloud_status()["mode"],
        "daily_safe_limit": 20,
        "sent_today": sent_today,
        "remaining_today_safe": max(0, 20 - sent_today),
        "total_sent_logged": len(wa_log),
        "items": cards[:25],
    }


def mark_whatsapp_web_sent(*, slug: str, nombre: str, phone: str, notes: str = "") -> dict[str, Any]:
    state = get_or_init_growth_state()
    log = state.setdefault("whatsapp_web_log", [])
    clean_slug = slugify(slug or nombre)
    now_dt = datetime.now(MONTERREY_TZ)
    entry = {
        "sent_at": now_dt.isoformat(timespec="seconds"),
        "slug": clean_slug,
        "nombre": nombre,
        "phone": phone,
        "notes": notes,
    }
    log.insert(0, entry)
    state["whatsapp_web_log"] = log[:200]
    crm = state.setdefault("crm_records", {})
    crm_row = crm.setdefault(clean_slug, {"slug": clean_slug, "nombre": nombre})
    curr_stage = str(crm_row.get("stage") or "Nuevo")
    if curr_stage in ("Nuevo", ""):
        crm_row["stage"] = "Contactado"
        next_gap: timedelta | None = timedelta(hours=48)
    elif curr_stage == "Contactado":
        crm_row["stage"] = "Toque_48h"
        next_gap = timedelta(hours=24)
    elif curr_stage == "Toque_48h":
        crm_row["stage"] = "Toque_72h"
        next_gap = timedelta(days=4)
    elif curr_stage == "Toque_72h":
        crm_row["stage"] = "Breakup_Dia7"
        next_gap = None
    else:
        next_gap = timedelta(hours=48)

    crm_row["phone"] = phone
    crm_row["channel_last"] = "whatsapp_web"
    crm_row["touch_count"] = int(crm_row.get("touch_count") or 0) + 1
    crm_row["last_contacted_at"] = entry["sent_at"]
    crm_row["next_followup_at"] = (now_dt + next_gap).isoformat(timespec="seconds") if next_gap else ""
    write_json(FILES["growth_suite"], state)
    append_agent_event(
        "ventas_outreach",
        f"Despachó WhatsApp Web ({crm_row['stage']})",
        f"{nombre} ({phone}) registrado en CRM -> {crm_row['stage']}.",
        zone="desk_ventas",
        source="human_trigger",
    )
    return {"logged": entry, "supervisor": get_whatsapp_web_supervisor_queue()}


def run_apify_zone_sweep(zones: list[str], niche_keys: list[str], dry_run: bool = True) -> dict[str, Any]:
    """Prepare or launch an Apify multi-zone search sweep cleanly."""
    queries: list[str] = []
    for z in zones:
        z_info = ZONE_PRESETS.get(z)
        if not z_info:
            continue
        for n in niche_keys:
            n_kw = NICHE_PRESETS.get(n)
            if n_kw:
                queries.append(f"{n_kw} {z_info['query_suffix']}")
    if not queries:
        raise ValueError("Selecciona al menos una zona y un giro válido para peinar.")

    state = get_or_init_growth_state()
    rec = {
        "timestamp": now_iso(),
        "zones": zones,
        "niches": niche_keys,
        "queries": queries,
        "dry_run": dry_run,
        "status": "planned_dry_run" if dry_run else "script_triggered",
    }
    if not dry_run:
        script = ROOT_DIR / "scripts" / "run_apify_production.py"
        if script.exists():
            subprocess.Popen([str(ROOT_DIR / ".venv" / "bin" / "python"), str(script)], cwd=str(ROOT_DIR))
    state.setdefault("apify_sweeps_log", []).insert(0, rec)
    state["apify_sweeps_log"] = state["apify_sweeps_log"][:25]
    write_json(FILES["growth_suite"], state)
    append_agent_event(
        "scouting_radar",
        "Barrido Apify Multi-Zona",
        f"{len(queries)} búsquedas en {len(zones)} zona(s) ({'Dry-Run' if dry_run else 'En Vivo'}).",
        zone="radar_maps",
        source="human_ui",
    )
    return rec


# ------------------------------------------------------------------------------
# 6. AUTOMATIZACIONES DIARIAS: CORREOS 25/DIA, CADENCIA 48H/72H, CIERRE E ITERACION
# ------------------------------------------------------------------------------
_PV_FORBIDDEN_ORIGIN = ("monterrey", "san jerónimo", "san jeronimo", "san pedro garza", "spgg", "nuevo león", "nuevo leon")


def _parse_iso_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).strip())
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=MONTERREY_TZ)
    return dt


def _daily_queue_dir() -> Path:
    if FILES["growth_suite"].parent == ROOT_DIR / "dashboard" / "data":
        return ROOT_DIR / "assets" / "mockups" / "daily_queue"
    return FILES["growth_suite"].parent / "daily_queue"


def _pick_active_ab_variant(da: dict[str, Any], territory: str, idx: int) -> str:
    variants = da.get("ab_variants", {})
    if territory == "biogen" and (variants.get("C_biogen_aliados_flujo", {}).get("active", True)):
        return "C_biogen_aliados_flujo"
    active_ids = [
        vid
        for vid in ("A_diagnostico_tecnica", "B_roi_patrocinio_vitrina", "C_biogen_aliados_flujo")
        if variants.get(vid, {}).get("active", True)
    ] or ["A_diagnostico_tecnica"]
    rep = da.get("last_iteration_report") or {}
    winner = rep.get("winner_variant_id")
    if winner in active_ids and any(r.get("score", 0) > 0 for r in rep.get("metrics_by_variant", [])):
        weighted = [winner, winner] + active_ids
        return weighted[idx % len(weighted)]
    return active_ids[idx % len(active_ids)]


def _compose_daily_email_payload(prospect: dict[str, Any], variant_id: str, calendly_base: str) -> dict[str, str]:
    name = prospect["nombre"]
    territory = prospect.get("territory", "mty")
    demo_hint = f" Preparamos su vista web demostrativa ({prospect['demo_rel_path']}) lista para revisar." if territory == "pv" and prospect.get("demo_rel_path") else ""

    if territory == "biogen" or variant_id == "C_biogen_aliados_flujo":
        subject = f"{name}: Alianza Captoora Biogen Flow · Contenido Editorial Semanal"
        plain = (
            f"Hola equipo de {name}, soy Jesús Gutiérrez de Captoora Studio (https://captoora.studio/sports). "
            f"Abrimos el programa piloto Captoora Biogen Flow con cobertura fotográfica de iluminación escultural y clips verticales 9:16 listos en 48–72h para proyectar el nivel real de su marca sin adelantos rígidos. "
            f"Adjunto la propuesta en PDF; si les hace sentido revisarlo 15 minutos, pueden apartar hora en {calendly_base} o responder este correo."
        )
    elif variant_id == "B_roi_patrocinio_vitrina":
        subject = f"{name}: Vitrina Digital 2027 con -35% (Entrega 48–72h + Opción QR LED)"
        plain = (
            f"Hola equipo de {name}, les escribe Jesús Gutiérrez de Captoora Studio (https://captoora.studio/sports).{demo_hint} "
            f"Tenemos esquema modular con -35% de temporada desde $3,900 MXN para renovar su presencia en Google Maps y redes en 48–72h (con opción en 2do momento de placa QR en acrílico LED cálida en 3–5 días hábiles para impulsar reseñas reales). "
            f"¿Revisamos las opciones 15 minutos en {calendly_base}?"
        )
    else:
        subject = f"{name}: Comparativa Visual y Producción Editorial 1/2000s (-35%)"
        plain = (
            f"Hola equipo de {name}, soy Jesús Gutiérrez de Captoora Studio (https://captoora.studio/sports).{demo_hint} "
            f"Preparamos un diagnóstico visual de su ficha actual para proyectar su servicio al más alto nivel con captura Global Shutter 1/2000s, carga optimizada en Google Maps y Meta sin bloqueos desde $3,900 MXN (-35%, entrega digital en 48–72h). "
            f"¿Te comparto la muestra o agendamos 15 minutos en {calendly_base}?"
        )

    violations = validate_client_copy(f"{subject} {plain}")
    if violations:
        raise ValueError(f"Guardrail bloqueó correo para {name}: {violations}")
    if territory == "pv":
        low = f"{subject} {plain}".lower()
        for bad_term in _PV_FORBIDDEN_ORIGIN:
            if bad_term in low:
                raise ValueError(f"Territorio PV violado por término prohibido '{bad_term}' en {name}")

    html_body = f"""
    <div style="background:#08090c;color:#f5f4ef;font-family:Arial,sans-serif;padding:28px;border:1px solid #c5a880;border-radius:12px;">
      <p style="color:#c5a880;font-size:11px;letter-spacing:2px;margin:0 0 8px;">CAPTOORA STUDIO · PRODUCCIÓN EDITORIAL 1/2000s</p>
      <h2 style="margin:0 0 12px;color:#f5f4ef;">Hola equipo de {name},</h2>
      <p style="line-height:1.6;color:#d2d5de;">{plain}</p>
      <p style="margin:18px 0;">
        <a href="https://captoora.studio/sports" style="background:#c5a880;color:#08090c;padding:10px 18px;border-radius:8px;text-decoration:none;font-weight:bold;">Ver Portafolio</a>
        &nbsp;&nbsp;
        <a href="{calendly_base}" style="border:1px solid #c5a880;color:#c5a880;padding:10px 18px;border-radius:8px;text-decoration:none;">Agendar 15 min</a>
      </p>
      <p style="font-size:12px;color:#888d9e;">Jesús Gutiérrez · Captoora Studio · WhatsApp +52 81 4005 0088 · chuy@captoora.studio</p>
    </div>
    """
    return {"subject": subject, "plain_text": plain, "html_body": html_body}


def update_automation_settings(
    *,
    auto_send_enabled: bool | None = None,
    daily_email_cap: int | None = None,
    territory_mix: dict[str, int] | None = None,
) -> dict[str, Any]:
    state = get_or_init_growth_state()
    da = state.setdefault("daily_automation", _default_daily_automation())
    settings = da.setdefault("settings", {})
    if auto_send_enabled is not None:
        settings["auto_send_enabled"] = bool(auto_send_enabled)
    if daily_email_cap is not None:
        settings["daily_email_cap"] = max(1, min(int(daily_email_cap), 50))
    if isinstance(territory_mix, dict):
        clean_mix = {
            k: max(0, int(territory_mix.get(k, settings.get("territory_mix", {}).get(k, 0))))
            for k in ("mty", "pv", "biogen")
        }
        settings["territory_mix"] = clean_mix
    write_json(FILES["growth_suite"], state)
    return settings


def prepare_daily_email_batch(
    *,
    max_emails: int | None = None,
    territory_mix: dict[str, int] | None = None,
    scan_websites_first: bool = False,
) -> dict[str, Any]:
    """Assemble today's curated daily Zoho email batch balancing MTY, PV, and Biogen leads without duplicates."""
    if scan_websites_first:
        enrich_emails_from_websites(limit=15)

    state = get_or_init_growth_state()
    da = state.setdefault("daily_automation", _default_daily_automation())
    settings = da.setdefault("settings", {})
    cap = max(1, min(int(max_emails or settings.get("daily_email_cap") or 25), 50))
    mix = territory_mix or settings.get("territory_mix") or {"mty": 10, "pv": 10, "biogen": 5}
    calendly_base = (state.get("calendly") or {}).get("base_url") or "https://calendly.com/captoora"

    all_candidates = _collect_multi_territory_prospects()
    _sync_preseeded_emails_into_crm(state, all_candidates)
    by_slug = {c["slug"]: c for c in all_candidates}
    crm = state.setdefault("crm_records", {})

    # Gather eligible prospects with verified email who haven't been emailed yet
    pools: dict[str, list[dict[str, Any]]] = {"mty": [], "pv": [], "biogen": []}
    for slug, row in crm.items():
        if not isinstance(row, dict):
            continue
        em = str(row.get("email") or "").strip()
        if not em or "@" not in em:
            continue
        if row.get("email_sent_at") or str(row.get("stage") or "Nuevo") not in ("Nuevo", ""):
            continue
        base = by_slug.get(slug, {})
        terr = row.get("territory") or base.get("territory") or "mty"
        if terr not in pools:
            terr = "mty"
        pools[terr].append(
            {
                "slug": slug,
                "nombre": row.get("nombre") or base.get("nombre") or slug,
                "email": em,
                "phone": row.get("phone") or base.get("telefono") or "",
                "territory": terr,
                "nicho": row.get("nicho") or base.get("nicho") or "Small Business",
                "offer_track": base.get("offer_track") or ("biogen" if terr == "biogen" else "small_business"),
                "pdf_rel_path": base.get("pdf_rel_path") or "",
                "demo_rel_path": base.get("demo_rel_path") or "",
            }
        )

    chosen: list[dict[str, Any]] = []
    chosen_slugs: set[str] = set()
    for tk in ("mty", "pv", "biogen"):
        quota = max(0, int(mix.get(tk, 0)))
        for cand in pools[tk][:quota]:
            if len(chosen) >= cap:
                break
            if cand["slug"] not in chosen_slugs:
                chosen.append(cand)
                chosen_slugs.add(cand["slug"])

    # Fill any remaining capacity from whichever territory has verified emails ready
    if len(chosen) < cap:
        for tk in ("biogen", "mty", "pv"):
            for cand in pools[tk]:
                if len(chosen) >= cap:
                    break
                if cand["slug"] not in chosen_slugs:
                    chosen.append(cand)
                    chosen_slugs.add(cand["slug"])

    batch_items: list[dict[str, Any]] = []
    for idx, cand in enumerate(chosen):
        vid = _pick_active_ab_variant(da, cand["territory"], idx)
        composed = _compose_daily_email_payload(cand, vid, calendly_base)
        batch_items.append(
            {
                **cand,
                "ab_variant": vid,
                "subject": composed["subject"],
                "plain_text": composed["plain_text"],
                "html_body": composed["html_body"],
                "status": "queued",
                "eml_path": None,
                "dispatched_at": None,
            }
        )

    today_str = now_iso()[:10]
    da["daily_email_batch"] = {
        "batch_date": today_str,
        "prepared_at": now_iso(),
        "items": batch_items,
    }
    state["updated_at"] = now_iso()
    write_json(FILES["growth_suite"], state)
    append_agent_event(
        "ventas_outreach",
        "Preparó Lote Diario de Correos",
        f"{len(batch_items)} prospectos listos (MTY/PV/Biogen) · SMTP {'Activo' if get_smtp_status()['configured'] else 'Modo .eml / Dry-Run'}.",
        zone="desk_ventas",
        source="daily_automation",
    )
    return da["daily_email_batch"]


def dispatch_daily_email_batch(*, dry_run: bool = False, limit: int = 25) -> dict[str, Any]:
    """Send today's curated email batch safely via Zoho SMTP (up to daily cap), exporting .eml when dry-run or unconfigured."""
    state = get_or_init_growth_state()
    da = state.setdefault("daily_automation", _default_daily_automation())
    batch = da.get("daily_email_batch") or {}
    today_dt = datetime.now(MONTERREY_TZ)
    today_str = today_dt.strftime("%Y-%m-%d")
    if not batch.get("items") or batch.get("batch_date") != today_str:
        batch = prepare_daily_email_batch()
        state = get_or_init_growth_state()
        da = state["daily_automation"]
        batch = da["daily_email_batch"]

    daily_cap = int((da.get("settings") or {}).get("daily_email_cap") or 25)
    sent_today = sum(
        1
        for m in state.get("mail_campaigns_log", [])
        if (not m.get("dry_run")) and str(m.get("timestamp") or "").startswith(today_str)
    )
    remaining_cap = max(0, daily_cap - sent_today)
    smtp_ready = get_smtp_status()["configured"]
    effective_dry = bool(dry_run or not smtp_ready)
    budget = min(max(1, limit), remaining_cap) if not effective_dry else min(max(1, limit), len(batch.get("items", [])))

    queue_dir = _daily_queue_dir()
    crm = state.setdefault("crm_records", {})
    variants = da.setdefault("ab_variants", {})
    processed = 0
    sent_count = 0
    eml_count = 0

    for item in batch.get("items", []):
        if item.get("status") == "sent_zoho" or processed >= budget:
            continue
        attachments: list[Path] = []
        rel_pdf = str(item.get("pdf_rel_path") or "").strip()
        if rel_pdf:
            p = ROOT_DIR / rel_pdf
            if p.exists():
                attachments.append(p)

        eml_target = queue_dir / f"{today_str}_{item['slug']}.eml" if effective_dry else None
        res = send_email_via_zoho(
            to_email=item["email"],
            subject=item["subject"],
            html_body=item["html_body"],
            plain_text=item.get("plain_text"),
            attachments=attachments,
            dry_run=effective_dry,
            save_eml_path=eml_target,
        )
        processed += 1
        item["dispatched_at"] = now_iso()
        if res.get("eml_path"):
            item["eml_path"] = res["eml_path"]

        if res.get("sent"):
            sent_count += 1
            item["status"] = "sent_zoho"
            row = crm.setdefault(item["slug"], {"slug": item["slug"], "nombre": item["nombre"], "email": item["email"]})
            row["stage"] = "Contactado"
            row["territory"] = item.get("territory", "mty")
            row["ab_variant"] = item.get("ab_variant", "A_diagnostico_tecnica")
            row["touch_count"] = max(1, int(row.get("touch_count") or 0))
            row["channel_last"] = "zoho_smtp"
            row["email_sent_at"] = item["dispatched_at"]
            row["last_contacted_at"] = item["dispatched_at"]
            row["next_followup_at"] = (today_dt + timedelta(hours=48)).isoformat(timespec="seconds")
            v_stats = variants.get(row["ab_variant"])
            if isinstance(v_stats, dict):
                v_stats["sent"] = int(v_stats.get("sent") or 0) + 1
        else:
            eml_count += 1
            item["status"] = "eml_ready"

        state.setdefault("mail_campaigns_log", []).insert(
            0,
            {
                "timestamp": item["dispatched_at"],
                "to_email": item["email"],
                "prospect_name": item["nombre"],
                "slug": item["slug"],
                "territory": item.get("territory", "mty"),
                "ab_variant": item.get("ab_variant", "A_diagnostico_tecnica"),
                "offer_track": item.get("offer_track", "small_business"),
                "dry_run": effective_dry,
                "status": res.get("mode") or ("sent" if res.get("sent") else "eml_ready"),
                "attachments": [p.name for p in attachments],
                "eml_path": res.get("eml_path"),
            },
        )

    state["mail_campaigns_log"] = state.get("mail_campaigns_log", [])[:120]
    state["updated_at"] = now_iso()
    write_json(FILES["growth_suite"], state)
    append_agent_event(
        "ventas_outreach",
        "Despachó Lote Diario Zoho",
        f"Enviados SMTP: {sent_count} · Borradores .eml generados: {eml_count} (tope restante: {max(0, remaining_cap - sent_count)}/{daily_cap}).",
        zone="desk_ventas",
        source="daily_automation",
    )
    return {
        "batch_date": today_str,
        "smtp_configured": smtp_ready,
        "effective_dry_run": effective_dry,
        "sent_count": sent_count,
        "eml_exported_count": eml_count,
        "daily_cap": daily_cap,
        "remaining_cap_today": max(0, remaining_cap - sent_count),
        "batch": da["daily_email_batch"],
    }


def evaluate_due_followups(now_dt: datetime | None = None) -> dict[str, Any]:
    """Compute overdue 48h / 72h / Day-7 follow-ups with ready client-safe messages & WhatsApp links."""
    dt = now_dt or datetime.now(MONTERREY_TZ)
    state = get_or_init_growth_state()
    crm = state.get("crm_records", {})
    calendly_base = (state.get("calendly") or {}).get("base_url") or "https://calendly.com/captoora"
    due_items: list[dict[str, Any]] = []

    next_step_map = {
        "Contactado": ("Toque_48h", timedelta(hours=24)),
        "Toque_48h": ("Toque_72h", timedelta(days=4)),
        "Toque_72h": ("Breakup_Dia7", None),
    }

    for slug, row in crm.items():
        if not isinstance(row, dict):
            continue
        stage = str(row.get("stage") or "Nuevo")
        if stage not in next_step_map:
            continue
        due_at = _parse_iso_dt(row.get("next_followup_at"))
        if due_at is None:
            last_ct = _parse_iso_dt(row.get("last_contacted_at"))
            if last_ct is not None:
                due_at = last_ct + timedelta(hours=48)
        if due_at is None or due_at > dt:
            continue

        next_stage, _ = next_step_map[stage]
        nombre = str(row.get("nombre") or slug)
        terr = str(row.get("territory") or "mty")

        if next_stage == "Toque_48h":
            subject = f"Re: Muestra visual lista · {nombre}"
            msg = (
                f"Hola equipo de {nombre}, retomo breve nuestro mensaje de hace 48h. "
                f"Ya tenemos preparada la comparativa visual Antes vs. Después para mostrar cómo proyectar su marca en línea con entrega digital en 48–72h. ¿Se las comparto por aquí?"
            )
        elif next_stage == "Toque_72h":
            subject = f"Re: 15 min esta semana + -35% · {nombre}"
            msg = (
                f"Hola equipo de {nombre}, cerramos semana con agenda limitada y sigue activo el -35% de temporada (pudiendo arrancar solo con producción digital desde $3,900 MXN y dejar piezas acrílicas LED para un 2do momento). "
                f"Si gustas apartar 15 minutos directos, aquí está mi agenda: {calendly_base}"
            )
        else:
            subject = f"Cierre de seguimiento · {nombre}"
            msg = (
                f"Hola equipo de {nombre}, no quiero saturar su bandeja. Dejo abierta la puerta para cuando quieran renovar su vitrina visual con fotografía editorial 1/2000s en https://captoora.studio/sports. ¡Mucho éxito esta semana!"
            )

        if validate_client_copy(f"{subject} {msg}"):
            continue

        phone_raw = str(row.get("phone") or "").strip()
        wa_url = ""
        if phone_raw:
            try:
                digits = clean_phone_digits(phone_raw)
                wa_url = f"https://web.whatsapp.com/send?phone={digits}&text={urllib.parse.quote(msg)}"
            except ValueError:
                wa_url = ""

        due_items.append(
            {
                "slug": slug,
                "nombre": nombre,
                "territory": terr,
                "current_stage": stage,
                "next_stage": next_stage,
                "due_since": due_at.isoformat(timespec="seconds"),
                "email": str(row.get("email") or ""),
                "phone": phone_raw,
                "subject": subject,
                "message": msg,
                "web_whatsapp_url": wa_url,
            }
        )

    da = state.setdefault("daily_automation", _default_daily_automation())
    da["followups_due_cache"] = due_items[:50]
    write_json(FILES["growth_suite"], state)
    return {"evaluated_at": dt.isoformat(timespec="seconds"), "due_count": len(due_items), "items": due_items}


def dispatch_due_followups(
    *,
    channel: str = "all",
    dry_run: bool = False,
    limit: int = 20,
    now_dt: datetime | None = None,
) -> dict[str, Any]:
    """Dispatch overdue follow-ups across Zoho email / prepare WA Web 1-click queue and advance CRM cadence."""
    dt = now_dt or datetime.now(MONTERREY_TZ)
    eval_res = evaluate_due_followups(now_dt=dt)
    due_items = eval_res["items"][: max(1, min(limit, 50))]

    state = get_or_init_growth_state()
    crm = state.setdefault("crm_records", {})
    smtp_ready = get_smtp_status()["configured"]
    effective_dry = bool(dry_run or not smtp_ready)
    queue_dir = _daily_queue_dir()
    today_str = dt.strftime("%Y-%m-%d")

    email_sent = 0
    eml_saved = 0
    wa_ready = 0
    next_gap = {"Toque_48h": timedelta(hours=24), "Toque_72h": timedelta(days=4), "Breakup_Dia7": None}

    for item in due_items:
        has_email = bool(item["email"])
        has_wa = bool(item["web_whatsapp_url"])
        row = crm.get(item["slug"])
        if not isinstance(row, dict):
            continue

        if channel in ("all", "email") and has_email:
            html_body = (
                "<div style='background:#08090c;color:#f5f4ef;font-family:Arial,sans-serif;padding:24px;border:1px solid #c5a880;border-radius:10px;'>"
                f"<p style='line-height:1.6;color:#d2d5de;'>{item['message']}</p>"
                "<p style='font-size:12px;color:#888d9e;'>Jesús Gutiérrez · Captoora Studio · +52 81 4005 0088</p></div>"
            )
            eml_path = queue_dir / f"followup_{today_str}_{item['slug']}.eml" if effective_dry else None
            res = send_email_via_zoho(
                to_email=item["email"],
                subject=item["subject"],
                html_body=html_body,
                plain_text=item["message"],
                dry_run=effective_dry,
                save_eml_path=eml_path,
            )
            if res.get("sent"):
                email_sent += 1
                row["stage"] = item["next_stage"]
                row["touch_count"] = int(row.get("touch_count") or 1) + 1
                row["last_contacted_at"] = dt.isoformat(timespec="seconds")
                gap = next_gap.get(item["next_stage"])
                row["next_followup_at"] = (dt + gap).isoformat(timespec="seconds") if gap else ""
            else:
                eml_saved += 1
        elif channel in ("all", "whatsapp_web") and has_wa:
            wa_ready += 1
            if dry_run:
                continue

    write_json(FILES["growth_suite"], state)
    updated_due = evaluate_due_followups(now_dt=dt)
    append_agent_event(
        "ventas_outreach",
        "Ejecutó Cadencia Seguimientos",
        f"Vencidos: {len(due_items)} · Correos enviados: {email_sent} · .eml: {eml_saved} · WA listos: {wa_ready}.",
        zone="desk_ventas",
        source="daily_automation",
    )
    return {
        "processed_due": len(due_items),
        "email_sent": email_sent,
        "eml_saved": eml_saved,
        "whatsapp_ready": wa_ready,
        "remaining_due": updated_due["due_count"],
        "due_items": updated_due["items"],
    }


OBJECTION_PLAYBOOKS: dict[str, dict[str, str]] = {
    "precio": {
        "label": "Está elevado / fuera de presupuesto ahorita",
        "reply": (
            "Totalmente comprensible. Justo por eso estructuramos la entrada modular con -35% desde $3,900 MXN solo fase digital "
            "(entrega en 48–72h para que empiecen a capitalizar reservas de inmediato) y las placas o reconocimientos LED en un segundo momento. "
            "Se aparta únicamente con el 50% ($1,950 MXN) y el resto contra entrega."
        ),
    },
    "despues_navidad": {
        "label": "Lo vemos después de vacaciones / próximo año",
        "reply": (
            "Perfecto, podemos dejar apartada fecha con el precio congelado -35% usando un anticipo simbólico del 50%, o bien hacer ahorita solo el levantamiento digital "
            "para arrancar enero con su vitrina Google Maps y redes ya listas mientras la competencia apenas comienza a cotizar."
        ),
    },
    "ya_tengo_fotografo": {
        "label": "Ya trabajamos con alguien / agencia",
        "reply": (
            "Excelente que ya valoren la imagen profesional. Nuestro enfoque complementa perfecto en cobertura de acción 1/2000s (entrega en 15 minutos en vivo) y auditoría técnica de Google Maps / placa QR de reseñas en recepción. "
            "Si gustan hacemos una prueba comparativa puntual de 15 min sin compromiso."
        ),
    },
    "persona_moral_cfdi": {
        "label": "Somos empresa / requerimos factura y retenciones",
        "reply": (
            "Emitimos factura CFDI 4.0 de inmediato bajo Régimen 612 (RFC GUFJ870801NA6, uso CFDI G03) con desglose fiscal transparente para Persona Moral cuando aplique. "
            "Trabajamos con orden de servicio clara: 50% al confirmar fecha y 50% al entregar la galería digital."
        ),
    },
    "solo_digital_primero": {
        "label": "Nos interesa primero solo digital / sin LED físico",
        "reply": (
            "Excelente decisión: la fase digital se produce y entrega en 48–72h (o el mismo día en torneos y eventos) sin depender de tiempos de taller. "
            "Apartamos con el 50% de anticipo y el 50% restante contra entrega del enlace curado."
        ),
    },
    "demo_y_cierre": {
        "label": "Pidió detalles finales para agendar y cerrar",
        "reply": (
            "Excelente, con gusto cerramos hoy tu fecha en 15 minutos para revisar la muestra visual y elegir entre Solo Digital (-35%) o Suite Completa con 50% de anticipo."
        ),
    },
}


def log_prospect_reply_and_close(
    *,
    slug: str,
    nombre: str = "",
    outcome: str = "objecion",
    objection_key: str = "demo_y_cierre",
    offer_track: str = "small_business",
    package_ref: str = "Suite Total / Impulso Maps -35%",
    collected_mxn: float = 0.0,
    direct_cost_mxn: float = 0.0,
    client_is_persona_moral: bool = False,
    notes: str = "",
) -> dict[str, Any]:
    """Record a real prospect response, generate closing objection reply + 50/50 split, and update A/B + Accounting."""
    state = get_or_init_growth_state()
    da = state.setdefault("daily_automation", _default_daily_automation())
    crm = state.setdefault("crm_records", {})
    clean_slug = slugify(slug or nombre)
    row = crm.setdefault(clean_slug, {"slug": clean_slug, "nombre": nombre or clean_slug, "stage": "Nuevo"})
    display_name = nombre.strip() or str(row.get("nombre") or clean_slug)
    calendly_base = (state.get("calendly") or {}).get("base_url") or "https://calendly.com/captoora"

    stage_map = {
        "positivo": "Respondio",
        "objecion": "Respondio",
        "pidio_cotizacion": "Cotizado",
        "agendo_calendly": "Calendly",
        "cerrado_anticipo": "Anticipo_50",
        "no_interesado": "Descartado",
    }
    new_stage = stage_map.get(outcome, "Respondio")
    now_dt = datetime.now(MONTERREY_TZ)
    row["stage"] = new_stage
    row["last_reply_outcome"] = outcome
    row["last_reply_at"] = now_dt.isoformat(timespec="seconds")
    if notes.strip():
        row["notes"] = notes.strip()
    if new_stage in ("Anticipo_50", "Descartado"):
        row["next_followup_at"] = ""
    elif new_stage in ("Respondio", "Cotizado"):
        row["next_followup_at"] = (now_dt + timedelta(hours=24)).isoformat(timespec="seconds")

    vid = str(row.get("ab_variant") or "A_diagnostico_tecnica")
    v_stats = (da.get("ab_variants") or {}).get(vid)
    if isinstance(v_stats, dict):
        if outcome != "no_interesado":
            v_stats["replies"] = int(v_stats.get("replies") or 0) + 1
        if outcome == "agendo_calendly":
            v_stats["meetings"] = int(v_stats.get("meetings") or 0) + 1
        if outcome == "cerrado_anticipo":
            v_stats["closes"] = int(v_stats.get("closes") or 0) + 1

    pb = OBJECTION_PLAYBOOKS.get(objection_key, OBJECTION_PLAYBOOKS["demo_y_cierre"])
    suggested_reply = f"Hola equipo de {display_name}, {pb['reply']} Agenda directa 15 min: {calendly_base}"
    if validate_client_copy(suggested_reply):
        raise ValueError("Guardrail bloqueó respuesta de negociación.")

    log_entry = {
        "timestamp": now_iso(),
        "slug": clean_slug,
        "nombre": display_name,
        "outcome": outcome,
        "objection_key": objection_key,
        "new_stage": new_stage,
        "ab_variant": vid,
        "suggested_reply": suggested_reply,
        "collected_mxn": float(collected_mxn or 0.0),
    }
    da.setdefault("negotiation_logs", []).insert(0, log_entry)
    da["negotiation_logs"] = da["negotiation_logs"][:60]
    write_json(FILES["growth_suite"], state)

    sale_result = None
    if outcome == "cerrado_anticipo" and collected_mxn > 0:
        sale_result = record_accountant_sale(
            client_name=display_name,
            package_ref=package_ref,
            amount_collected_mxn=collected_mxn,
            direct_cost_mxn=direct_cost_mxn,
            includes_iva=True,
            client_is_persona_moral=client_is_persona_moral,
            payment_phase="Anticipo 50% (Cierre Negociación)",
        )

    phone_raw = str(row.get("phone") or "").strip()
    wa_url = ""
    if phone_raw:
        try:
            wa_url = f"https://web.whatsapp.com/send?phone={clean_phone_digits(phone_raw)}&text={urllib.parse.quote(suggested_reply)}"
        except ValueError:
            wa_url = ""

    append_agent_event(
        "ventas_outreach",
        f"Negociación {new_stage}: {display_name}",
        f"Resultado: {outcome} · Objeción: {objection_key}" + (f" · Cobro +${collected_mxn:,.0f} MXN" if collected_mxn > 0 else ""),
        zone="desk_ventas",
        source="human_ui",
    )
    return {
        "crm_record": row,
        "suggested_reply": suggested_reply,
        "web_whatsapp_url": wa_url,
        "calendly_url": calendly_base,
        "accountant_sale": sale_result,
        "ab_variants": da.get("ab_variants", {}),
    }


def run_daily_iteration_cycle() -> dict[str, Any]:
    """Analyze real A/B variant & territory conversion metrics, pause zero-reply variants, and tune next day's CEO focus."""
    state = get_or_init_growth_state()
    da = state.setdefault("daily_automation", _default_daily_automation())
    variants = da.setdefault("ab_variants", {})
    crm = state.get("crm_records", {})

    variant_rows: list[dict[str, Any]] = []
    paused_ids: list[str] = []
    for vid, v in variants.items():
        sent = int(v.get("sent") or 0)
        replies = int(v.get("replies") or 0)
        meetings = int(v.get("meetings") or 0)
        closes = int(v.get("closes") or 0)
        reply_rate = round((replies / sent) * 100.0, 1) if sent else 0.0
        close_rate = round((closes / sent) * 100.0, 1) if sent else 0.0
        score = closes * 5 + meetings * 3 + replies
        if sent >= 15 and replies == 0:
            v["active"] = False
            paused_ids.append(vid)
        variant_rows.append(
            {
                "id": vid,
                "label": v.get("label", vid),
                "sent": sent,
                "replies": replies,
                "meetings": meetings,
                "closes": closes,
                "reply_rate_pct": reply_rate,
                "close_rate_pct": close_rate,
                "active": bool(v.get("active", True)),
                "score": score,
            }
        )

    variant_rows.sort(key=lambda r: (r["score"], r["reply_rate_pct"], r["sent"]), reverse=True)
    winner = variant_rows[0] if variant_rows else None

    terr_metrics: dict[str, dict[str, int]] = {
        "mty": {"total_crm": 0, "contacted": 0, "replied_or_better": 0, "closed": 0},
        "pv": {"total_crm": 0, "contacted": 0, "replied_or_better": 0, "closed": 0},
        "biogen": {"total_crm": 0, "contacted": 0, "replied_or_better": 0, "closed": 0},
    }
    for row in crm.values():
        if not isinstance(row, dict):
            continue
        t = str(row.get("territory") or "mty")
        if t not in terr_metrics:
            t = "mty"
        st = str(row.get("stage") or "Nuevo")
        terr_metrics[t]["total_crm"] += 1
        if st != "Nuevo":
            terr_metrics[t]["contacted"] += 1
        if st in ("Respondio", "Cotizado", "Calendly", "Anticipo_50", "Cerrado"):
            terr_metrics[t]["replied_or_better"] += 1
        if st in ("Anticipo_50", "Cerrado"):
            terr_metrics[t]["closed"] += 1

    recs: list[str] = []
    if winner and winner["score"] > 0:
        recs.append(f"Promover '{winner['label']}' ({winner['reply_rate_pct']}% respuesta) como variante principal en el lote de mañana 09:15 CST.")
    else:
        recs.append("Aún sin respuestas registradas en A/B: mantener rotación equitativa A/B/C y ejecutar escáner web para completar 25 envíos diarios.")
    if paused_ids:
        recs.append(f"Pausadas automáticamente por 0% respuesta (>=15 envíos): {', '.join(paused_ids)}.")
    if get_smtp_status()["configured"]:
        recs.append("Zoho SMTP activo: el lote 09:15 CST y cadencia 10:00 CST operan en envío real controlado.")
    else:
        recs.append("Pendiente pegar SMTP_PASS en .env para cambiar exportación .eml a disparo Zoho automático.")

    report = {
        "ran_at": now_iso(),
        "winner_variant_id": winner["id"] if winner else "A_diagnostico_tecnica",
        "paused_variants": paused_ids,
        "metrics_by_variant": variant_rows,
        "metrics_by_territory": terr_metrics,
        "recommendations": recs,
    }
    da["last_iteration_report"] = report
    state.setdefault("ceo_plan", {})["updated_at"] = now_iso()
    if recs:
        state["ceo_plan"]["week_focus"] = recs[0]
    write_json(FILES["growth_suite"], state)
    append_agent_event(
        "marky_marketing",
        "Iteración Nocturna A/B",
        f"Ganadora: {report['winner_variant_id']} · Pausadas: {len(paused_ids)} · {recs[0][:120]}",
        target_agent="chief_of_staff",
        zone="estudio_marky",
        source="daily_automation",
    )
    return report


def get_daily_automation_overview() -> dict[str, Any]:
    state = get_or_init_growth_state()
    da = state.get("daily_automation", _default_daily_automation())
    due = evaluate_due_followups()
    crm = state.get("crm_records", {})
    with_email = sum(1 for r in crm.values() if isinstance(r, dict) and r.get("email"))
    uncontacted_email = sum(1 for r in crm.values() if isinstance(r, dict) and r.get("email") and str(r.get("stage") or "Nuevo") in ("Nuevo", ""))
    return {
        "settings": da.get("settings", {}),
        "smtp_configured": get_smtp_status()["configured"],
        "crm_with_email": with_email,
        "uncontacted_with_email": uncontacted_email,
        "scanned_websites_count": len(da.get("scanned_urls", [])),
        "daily_email_batch": da.get("daily_email_batch", {}),
        "due_followups": due,
        "ab_variants": da.get("ab_variants", {}),
        "objection_playbooks": {k: v["label"] for k, v in OBJECTION_PLAYBOOKS.items()},
        "negotiation_logs": da.get("negotiation_logs", [])[:12],
        "last_iteration_report": da.get("last_iteration_report"),
    }

