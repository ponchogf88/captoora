"""Growth Command Suite: Accountant ($0 upfront Ads gate + PFAE 612 SAT), CEO, SEO/20-Clips, Zoho Mail, Agenda, Calendly, Apify/GHL CRM & WA Web Supervisor."""

from __future__ import annotations

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
            "base_url": os.getenv("CALENDLY_BASE_URL", "").strip(),
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
                {"time": "09:30", "title": "Ventana Push Clínica / Colegios / Kínders (Zoho 20–30)", "owner": "ventas_outreach", "channel": "Zoho chuy@"},
                {"time": "11:00", "title": "Ventana Push Clubes Pádel / Gyms (15–20 WA Web 1-Clic)", "owner": "ventas_outreach", "channel": "WhatsApp Web"},
                {"time": "13:00", "title": "Seguimiento respuestas + Links Calendly 15 min", "owner": "ventas_outreach", "channel": "Calendly"},
                {"time": "16:30", "title": "Batch Creativo Pull (OpusClip 9:16 + Meta Suite + TikTok)", "owner": "conan_content", "channel": "Meta/TT/LI"},
                {"time": "18:00", "title": "Cierre diario Contador + Recordatorio de Mañana", "owner": "contabilidad_finanzas", "channel": "Contabilidad"},
            ],
            "tomorrow_blocks": [
                {"time": "08:30", "title": "Despertador 24/7: Resumen CEO & Cola Follow-up 48h", "owner": "chief_of_staff", "channel": "Scheduler"},
                {"time": "09:30", "title": "Rutas presenciales confirmadas (Mapa MTY Optimizado)", "owner": "ops_talleres_legal", "channel": "Mapa Rutas"},
                {"time": "12:00", "title": "Corte Seguimientos 72h (-35% / 2do Momento)", "owner": "ventas_outreach", "channel": "WA / Zoho"},
                {"time": "17:00", "title": "Publicación Reel / Collab hora pico según Insights", "owner": "lupe_social", "channel": "IG / TikTok"},
            ],
            "tomorrow_reminders_log": [],
        },
        "crm_records": {},
        "mail_campaigns_log": [],
        "whatsapp_web_log": [],
        "apify_sweeps_log": [],
        "scheduler": {
            "enabled": True,
            "last_tick": None,
            "ran_slots_today": {},
            "slots": [
                {"id": "08_30_ceo", "hour": 8, "minute": 30, "weekdays": [0, 1, 2, 3, 4, 5], "label": "08:30 CST · Briefing CEO & Agenda"},
                {"id": "10_00_followups", "hour": 10, "minute": 0, "weekdays": [0, 1, 2, 3, 4, 5], "label": "10:00 CST · Detector Follow-up 24–48h"},
                {"id": "13_00_pull", "hour": 13, "minute": 0, "weekdays": [0, 1, 2, 3, 4, 5], "label": "13:00 CST · Corte Mediodía & Pull SEO"},
                {"id": "18_00_tomorrow", "hour": 18, "minute": 0, "weekdays": [0, 1, 2, 3, 4, 5], "label": "18:00 CST · Recordatorio Agenda Mañana"},
                {"id": "fri_16_report", "hour": 16, "minute": 0, "weekdays": [4], "label": "Viernes 16:00 CST · Reporte Contador & Ventas"},
            ],
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
def enrich_emails_from_websites(limit: int = 12) -> dict[str, Any]:
    """Scan verified prospect websites (sitio_web) politely to discover public contact emails."""
    leads = read_json(FILES["leads"], default=[]) or []
    state = get_or_init_growth_state()
    crm = state.setdefault("crm_records", {})

    candidates = [
        l
        for l in leads
        if str(l.get("sitio_web") or "").startswith("http")
        and not any(s in str(l.get("sitio_web")).lower() for s in ("instagram.com", "facebook.com", "google.com/maps", "tiktok.com", "wa.me"))
    ]
    checked = 0
    found_rows: list[dict[str, Any]] = []
    for lead in candidates[: max(1, min(limit, 25))]:
        url = str(lead["sitio_web"]).strip()
        slug = slugify(lead.get("nombre", "negocio"))
        checked += 1
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 CaptooraB2BContactFinder/1.0"})
        emails_found: list[str] = []
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                html = resp.read(160_000).decode("utf-8", errors="ignore")
            raw_matches = EMAIL_REGEX.findall(html)
            for em in raw_matches:
                low = em.lower()
                if not any(bad in low for bad in (".png", ".jpg", ".svg", "wixpress.com", "sentry.io", "example.com")):
                    if low not in emails_found:
                        emails_found.append(low)
        except Exception:
            emails_found = []

        if emails_found:
            row = crm.setdefault(slug, {"slug": slug, "nombre": lead.get("nombre"), "stage": "Nuevo"})
            row["email"] = emails_found[0]
            row["email_source"] = f"website_public ({url})"
            found_rows.append({"slug": slug, "nombre": lead.get("nombre"), "email": emails_found[0]})

    state["updated_at"] = now_iso()
    write_json(FILES["growth_suite"], state)
    append_agent_event(
        "scouting_radar",
        "Enriqueció Correos Web",
        f"Revisó {checked} sitios públicos y detectó {len(found_rows)} correos de contacto.",
        zone="radar_maps",
        source="human_ui",
    )
    return {"checked_websites": checked, "emails_found": found_rows}


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
    entry = {
        "sent_at": now_iso(),
        "slug": clean_slug,
        "nombre": nombre,
        "phone": phone,
        "notes": notes,
    }
    log.insert(0, entry)
    state["whatsapp_web_log"] = log[:200]
    crm = state.setdefault("crm_records", {})
    crm_row = crm.setdefault(clean_slug, {"slug": clean_slug, "nombre": nombre})
    if crm_row.get("stage", "Nuevo") in ("Nuevo", ""):
        crm_row["stage"] = "Contactado"
    crm_row["phone"] = phone
    crm_row["last_contacted_at"] = now_iso()
    write_json(FILES["growth_suite"], state)
    append_agent_event(
        "ventas_outreach",
        "Despachó WhatsApp Web (1-Clic)",
        f"{nombre} ({phone}) registrado en CRM -> Contactado.",
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
