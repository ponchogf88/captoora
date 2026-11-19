"""Local zero-quota Marketing HQ (Marky, Lupe, Conan) replacing Grokbot and syncing all user subscriptions."""

from __future__ import annotations

import urllib.parse
from typing import Any

from .config import (
    FILES,
    append_agent_event,
    now_iso,
    read_json,
    set_agent_runtime_status,
    validate_client_copy,
    write_json,
)

SUBSCRIPTION_STACK: list[dict[str, Any]] = [
    {
        "id": "opusclip_pro",
        "name": "OpusClip Pro (Mes Gratis · URGENTE)",
        "cost_label": "$0 hoy (Trial Pro por vencer)",
        "urgency": "CRÍTICA",
        "owner_agent": "conan_content",
        "account": "Cuenta Principal",
        "role": "Convertir 3 videos largos (OBS / estudio) en 25–30 clips verticales 9:16 con subtítulos y reencuadre antes de que termine el mes gratis.",
        "daily_workflow": "Grabar 3 pilares de 8–12 min -> Subir hoy a OpusClip Pro -> Exportar Top 25 clips sin esperar.",
    },
    {
        "id": "google_pro_poncho",
        "name": "Google AI Pro #1 (Cuenta Poncho)",
        "cost_label": "$395 MXN/mes",
        "urgency": "ACTIVA",
        "owner_agent": "chief_of_staff",
        "account": "Poncho Principal",
        "role": "Orquesta Antigravity principal, código, FastAPI/tests, NotebookLM Comercial B2B y Drive maestro.",
        "daily_workflow": "Usar en Chrome Perfil 1 para estrategia, cierre B2B, correo Mail.app y dashboard :8765.",
    },
    {
        "id": "google_pro_yari",
        "name": "Google AI Pro #2 (Cuenta Yari · Promo)",
        "cost_label": "$99 MXN/mes promo (después $395)",
        "urgency": "ACTIVA · DOBLE CUOTA",
        "owner_agent": "marky_marketing",
        "account": "Yari Secundaria",
        "role": "Segunda cuota completa: Antigravity Creativo (Conan), Gemini Deep Research, Flow/Veo, Whisk y NotebookLM de Guiones.",
        "daily_workflow": "Abrir en Chrome Perfil 2 apuntando al mismo repo `/epic-bohr` y Drive compartido cuando el Perfil 1 descanse cuota.",
    },
    {
        "id": "captions_app",
        "name": "Captions App",
        "cost_label": "Suscripción Activa",
        "urgency": "ACTIVA",
        "owner_agent": "conan_content",
        "account": "Móvil / Studio",
        "role": "Talking-head frente a cámara con teleprompter, contacto visual natural y subtítulos editoriales de lujo para TikTok / Reels / LinkedIn.",
        "daily_workflow": "Grabar intros de 15s (Navidad -35%, Google Maps Antes/Después y Biogen Beta) directo para Lupe.",
    },
    {
        "id": "canva_app",
        "name": "Canva (Mac + Web)",
        "cost_label": "Suscripción Activa",
        "urgency": "ACTIVA",
        "owner_agent": "conan_content",
        "account": "Canva Studio",
        "role": "Carruseles 4:5 (LinkedIn + IG), portadas Google Maps personalizadas, historias -35% y flyers Biogen Beta.",
        "daily_workflow": "Usar 3 plantillas maestras Captoora (Negro #090b10 + Champagne + Volt #c6ff00) para duplicar piezas en 5 minutos.",
    },
    {
        "id": "meta_muse_suite",
        "name": "Meta Business Suite + Meta Muse Móvil",
        "cost_label": "Incluido (Cuenta Meta / WA Business)",
        "urgency": "ACTIVA · MÓVIL",
        "owner_agent": "lupe_social",
        "account": "Celular + Desktop",
        "role": "Lupe organiza programación en FB + IG + WhatsApp Business y Marky genera el Brief de Bolsillo para Muse en tu celular cuando sales.",
        "daily_workflow": "Copiar Context Pack para Muse antes de salir; regresar notas del celular al importador de Marketing HQ.",
    },
    {
        "id": "aftershoot_evoto",
        "name": "Aftershoot + Evoto",
        "cost_label": "Licencias / Apps Mac Instaladas",
        "urgency": "ACTIVA",
        "owner_agent": "conan_content",
        "account": "Mac Desktop",
        "role": "Aftershoot: selección rápida Halftime Blitz en cancha el mismo día. Evoto: retoque escultural consistente para Biogen Beta y retratos Small Business.",
        "daily_workflow": "Aftershoot -> exportación rápida -> Evoto preset Biogen/Editorial -> Pixieset + Canva.",
    },
    {
        "id": "capcut_obs_pixieset",
        "name": "CapCut + OBS + Pixieset + Apify + Motor Local",
        "cost_label": "Stack Producción Local ($0 cuota bot)",
        "urgency": "ACTIVA · 0 GROKBOT",
        "owner_agent": "lupe_social",
        "account": "Mac Local",
        "role": "OBS graba auditorías Maps; CapCut cierra clips de OpusClip; Pixieset aloja galerías y Trackeo; Chromium/WeasyPrint genera PNGs/PDFs sin cuotas.",
        "daily_workflow": "Todo respaldado localmente sin depender jamás de Grokbot (baja definitiva = $0 riesgo de corte).",
    },
]

GOOGLE_PRO_SYNC_PROTOCOL: dict[str, Any] = {
    "title": "Protocolo de Sincronía 2x Google AI Pro (Principal $395 + Yari $99 promo)",
    "summary": "Opera ambas cuotas Pro en paralelo sin choques ni pérdida de contexto usando 2 perfiles de Chrome sobre este mismo repositorio local.",
    "lanes": [
        {
            "lane": "Carril A · Cuenta Principal ($395 MXN/mes)",
            "focus": "Dirección, Código, Ventas & Servidor :8765",
            "assigned_apps": ["Antigravity HQ (Orquesta & Código)", "FastAPI + Chrome CDP :8765", "NotebookLM Comercial B2B", "Mail.app + WhatsApp Web"],
            "handoff_rule": "Guarda cambios en `dashboard/data/*.json` y ejecuta cierres/triggers.",
        },
        {
            "lane": "Carril B · Cuenta Yari ($99/mes promo -> $395)",
            "focus": "Conan Producción Creativa, Guiones & Multimedia",
            "assigned_apps": ["Antigravity Backup Creativo", "Flow / Veo 3 clips cinematográficos", "Whisk (conceptos iluminación/set)", "NotebookLM Guiones & Investigación"],
            "handoff_rule": "Exporta media a `assets/` y scripts/ideas directo a esta carpeta compartida `epic-bohr`.",
        },
        {
            "lane": "Carril C · Motor Local Captoora ($0 Tokens · Ilimitado)",
            "focus": "Marky, Lupe y Conan sin gastar cuotas de ninguna cuenta",
            "assigned_apps": ["marketing_hub.py", "mockups.py (PNG + PDF)", "gmaps_auditor.py (CDP)", "Dashboard :8765"],
            "handoff_rule": "Calendario, captions, respuestas DM y láminas Antes/Después se generan 100% gratis en Python.",
        },
    ],
}

OPUSCLIP_RESCUE_SPRINT: dict[str, Any] = {
    "status": "URGENTE · MES GRATIS PRO POR VENCER (0 -> 30 CLIPS)",
    "goal": "Producir al menos 25–30 clips verticales editados esta semana antes de perder acceso a OpusClip Pro.",
    "settings_checklist": [
        "Aspect Ratio: 9:16 Auto-Reframe con seguimiento facial activo.",
        "Clip Length: Mix 'Auto (<60s)' + rango corto '15s–35s' para Reels/TikTok rápidos.",
        "Brand Template en OpusClip: Tipografía sans limpia, texto blanco/champagne `#f5f4ef` + resaltado `#c6ff00` (cero ruido barato).",
        "Después de exportar: pasa solo los Top 5 clips con Score >85 por CapCut/Captions para poner CTA 'captoora.studio/sports · -35%'.",
    ],
    "pillars_to_record": [
        {
            "id": "OPUS-REC-1",
            "title": "Grabación 1 (12 min · OBS Pantalla + Cámara): Auditoría en Vivo de Google Maps SPGG/MTY",
            "tool": "OBS Studio + Chrome :8765 + OpusClip Pro",
            "estimated_clips": "10–12 clips B2B para Clínicas, Kinders y Gimnasios TotalPass",
            "script_bullets": [
                "Abre 5 fichas reales del tab Small Biz (Street View, 0 fotos, Sin Reclamar) sin exponer datos privados sensibles si prefieres usar nuestros PNGs.",
                "Explica cada 90 seg un error distinto: carrito de Street View, falta de teléfono, enlace a perfil personal bloqueable en Meta.",
                "Cierra cada bloque con CTA limpio: 'Te armamos tu comparativa Antes vs Después y subimos portada verificada (-35% arranca 2027)'.",
            ],
        },
        {
            "id": "OPUS-REC-2",
            "title": "Grabación 2 (10 min · Estudio / Captions Teleprompter): Navidad 2026 en Cancha y Acrílicos LED",
            "tool": "Captions App + Trofeo Acrílico LED físico + OpusClip Pro",
            "estimated_clips": "8–10 clips para Pádel, Danza, Colegios y Posadas",
            "script_bullets": [
                "Muestra en cámara un acrílico LED cálido y explica la diferencia entre diplomas de papel vs reconocimiento de colección.",
                "Desglosa las 3 Opciones (-35%: Digital $3,185 · Impresión/Marcos $5,135 · Suite LED $7,475 con pago físico en 2do momento).",
                "Aclara en 1 frase: fotografía digital el mismo día; taller artesanal MTY/SPGG en 3 a 5 días hábiles.",
            ],
        },
        {
            "id": "OPUS-REC-3",
            "title": "Grabación 3 (8 min · Estudio Lighting Biogen): Registro Físico Escultural para Atletas y Gyms",
            "tool": "Cámara / Captions + Set iluminación estudio + OpusClip Pro",
            "estimated_clips": "6–8 clips para TotalPass, CrossFit, Nutriólogos y Biogen Beta",
            "script_bullets": [
                "Explica por qué las selfies en espejo de vestidor distorsionan el progreso real.",
                "Muestra el protocolo de iluminación escultural y ángulo repetible (semanal/quincenal/mensual de 3 a 60 meses).",
                "Presenta la tarifa piloto fundador Biogen Beta (-35%: desde $1,268/mes en 3m hasta $748/mes en 60m).",
            ],
        },
    ],
}

DEFAULT_CONTENT_CALENDAR: list[dict[str, Any]] = [
    {
        "id": "POST-01",
        "day": "Lunes AM",
        "platform": "Instagram + Facebook (Meta Business Suite)",
        "track": "Camino 1 · Navidad 2026 (-35%)",
        "title": "Reel: Tu Torneo del Pavo merece trofeos LED y fotos antes de la premiación",
        "conan_tool": "OpusClip Pro + CapCut (9:16)",
        "conan_deliverable": "Reel 22s 9:16 con encendido de acrílico LED + acción 1/2000s",
        "caption": (
            "Un diploma de papel o una carpeta olvidada meses después no proyectan la categoría de tu torneo. 🏆\n\n"
            "En Captoora Sports entregamos selección fotográfica el mismo día para proyectar en redes sociales una imagen profesional "
            "al nivel de excelencia de tu club, con opción de trofeos escultóricos en acrílico óptico iluminado con LED cálida* "
            "financiables por patrocinadores.\n\n"
            "🎄 Temporada Navidad -35%: Digital desde $3,185 MXN · Suite Full + LED $7,475 MXN (piezas físicas diferibles a 2do momento).\n"
            "👉 Agenda en captoora.studio/sports o WA +52 81 4005 0088.\n"
            "*Digital mismo día; acrílicos LED en taller local MTY/SPGG: 3–5 días hábiles."
        ),
        "hashtags": "#PadelMonterrey #SanPedroGarzaGarcia #CaptooraSports #TorneoDelPavo #Posada2026",
        "cta_url": "https://business.facebook.com/latest/composer",
        "status": "ready_for_trigger",
    },
    {
        "id": "POST-02",
        "day": "Martes PM",
        "platform": "TikTok",
        "track": "Camino 4 · Small Business 2027 (-35%)",
        "title": "Video Corto: ¿Tu negocio sale con el carrito de Google Street View?",
        "conan_tool": "OBS + OpusClip Pro + Captions (9:16)",
        "conan_deliverable": "Clip vertical 28s comparando Street View vs Vitrina 2027",
        "caption": (
            "Cuando alguien busca tu clínica, gimnasio o jardín de niños en Monterrey, tu primera impresión pasa en 3 segundos en Google Maps. 📍\n\n"
            "Si tu ficha abre con el carrito de Street View o sin teléfono verificado, estás dejando pasar clientes listos para agendar.\n\n"
            "Captoora Small Business 2027 (-35%): sesión editorial en tu negocio + carga directa en Google Maps + Meta Business Portfolio "
            "(FB, IG y WA sin bloqueos) desde $3,900 MXN.\n"
            "Pide tu lámina comparativa Antes vs. Después en captoora.studio/sports 📲"
        ),
        "hashtags": "#Monterrey #GoogleMapsPro #GoogleMapsMexico #PymesMonterrey #CaptooraStudio",
        "cta_url": "https://www.tiktok.com/tiktokstudio/upload",
        "status": "ready_for_trigger",
    },
    {
        "id": "POST-03",
        "day": "Miércoles AM",
        "platform": "LinkedIn B2B",
        "track": "Camino 1 + Camino 4 · Corporativos & Clubes",
        "title": "Carrusel 4:5: Cómo justificar renovación a patrocinadores 2027 con evidencia visual el mismo día",
        "conan_tool": "Canva (Carrusel 5 láminas 4:5) + Aftershoot",
        "conan_deliverable": "PDF/Carrusel 4:5 (Coca-Cola FEMSA / Tecate / Poder Judicial NL proof)",
        "caption": (
            "Las marcas patrocinadoras no renuevan por gratitud: renuevan con evidencia fotográfica limpia el mismo día del evento.\n\n"
            "En Captoora Studio (con experiencia en producciones para Coca-Cola FEMSA, Heineken/Tecate y Poder Judicial de Nuevo León) "
            "separamos la entrega digital en vivo de la manufactura artesanal de reconocimientos LED en taller local (3–5 días hábiles), "
            "para que el comité directivo proyecte en redes sociales una imagen profesional al nivel de excelencia de su institución.\n\n"
            "Conoce el formato modular (-35% Temporada) o solicita tu Dossier B2B en https://captoora.studio/sports"
        ),
        "hashtags": "#MonterreyBusiness #SanPedroGarzaGarcia #Patrocinios #MarketingDeportivo #B2B",
        "cta_url": "https://www.linkedin.com/feed/",
        "status": "ready_for_trigger",
    },
    {
        "id": "POST-04",
        "day": "Jueves PM",
        "platform": "Instagram + TikTok",
        "track": "Camino 3 · Captoora Biogen (Beta -35%)",
        "title": "Reel Escultural: Por qué las selfies de espejo mienten sobre tu físico",
        "conan_tool": "Evoto + Captions + CapCut (9:16)",
        "conan_deliverable": "Comparativa estudio iluminación cenital lateral 18s",
        "caption": (
            "Si cambias de espejo, luz y ángulo cada semana, nunca ves con claridad tu verdadera recomposición física. 💡\n\n"
            "Presentamos Captoora Biogen (Beta): tu bitácora fotográfica en estudio con esquema de luz escultural controlada, cámara de alta velocidad "
            "y encuadre idéntico semana a semana (planes semanales, quincenales o mensuales de 3 a 60 meses).\n\n"
            "Cupo fundador -35%: desde $1,268 MXN/mes (plan 3m) hasta $748 MXN/mes (60m). Escríbenos por DM o en captoora.studio/sports."
        ),
        "hashtags": "#FitnessMonterrey #TotalPass #CulturismoMexico #CaptooraBiogen #FotografiaDeportiva",
        "cta_url": "https://business.facebook.com/latest/composer",
        "status": "ready_for_trigger",
    },
    {
        "id": "POST-05",
        "day": "Viernes AM",
        "platform": "Facebook + WhatsApp Business Status (Meta Suite)",
        "track": "Camino 2 + Camino 4 · TotalPass & Small Business 2027",
        "title": "Comparativa Antes vs. Después Google Maps + Bono QR Reseñas LED",
        "conan_tool": "Motor Local mockups.py (PNG Antes/Después)",
        "conan_deliverable": "Imagen 1600x1200 Antes vs Después (Street View -> Portada Editorial)",
        "caption": (
            "¿Buscan tu gimnasio, consultorio o colegio en Google Maps y lo primero que ven es el techo de una calle? 👀\n\n"
            "Llevamos equipo de iluminación editorial directo a tu sede: armamos diagnóstico Antes vs. Después gratuito, reclamamos "
            "y subimos fotos calibre estudio directo a Google Maps / TotalPass y blindamos tu Meta Business Portfolio (FB + IG + WhatsApp).\n\n"
            "Entrega ágil en 48–72h · Tarifa Temporada -35% desde $3,900 MXN. Mándanos tu nombre de negocio por WhatsApp (+52 81 4005 0088) y te enviamos tu vista previa."
        ),
        "hashtags": "#MonterreyBusiness #SmallBusinessNL #GoogleMaps #CaptooraStudio #FotografiaEditorial",
        "cta_url": "https://business.facebook.com/latest/composer",
        "status": "ready_for_trigger",
    },
    {
        "id": "POST-06",
        "day": "Sábado AM",
        "platform": "Instagram Carrusel + LinkedIn",
        "track": "Camino 1 · Galas Danza & Colegios White-Glove",
        "title": "Gala sin costo para tu academia: El Marco San Pedro + entrega al brindis",
        "conan_tool": "Canva + Pixieset + Aftershoot",
        "conan_deliverable": "Carrusel 4:5 (Estudio Backstage + Marco Madera Maciza)",
        "caption": (
            "Directora de academia o colegio: cubre tu festival navideño sin descapitalizar la escuela. 🩰✨\n\n"
            "Con nuestro esquema White-Glove montamos un mini-estudio editorial en backstage el día de tu gala; las familias pre-ordenan en línea "
            "su Set Conmemorativo en marco de madera fina (El Marco San Pedro) o placa LED cálida*, y la institución recibe su galería oficial el mismo día "
            "para proyectar en redes sociales una imagen profesional al nivel de excelencia de su escuela.\n\n"
            "Agenda Nov–Dic (-35%): captoora.studio/sports\n"
            "*Galería digital mismo día; marcos y placas LED en taller MTY/SPGG: 3–5 días hábiles."
        ),
        "hashtags": "#DanzaMonterrey #SanPedroGarzaGarcia #FestivalNavideno #ElMarcoSanPedro #CaptooraStudio",
        "cta_url": "https://business.facebook.com/latest/composer",
        "status": "ready_for_trigger",
    },
]

LUPE_DM_PLAYBOOK: list[dict[str, str]] = [
    {
        "id": "DM-PRECIO",
        "trigger_label": "¿Cuánto cuesta? / Info precios (-35%)",
        "channel": "IG / FB / TikTok / WA",
        "reply_text": (
            "¡Hola! Qué gusto saludarte 👋 Con -35% de temporada tenemos 3 opciones claras para que elijas la ideal:\n"
            "1) Solo Digital (mismo día): $3,185 MXN (eventos) o $3,900 MXN (Google Maps Small Business).\n"
            "2) Cobertura + Reels + Meta Business Portfolio / Marcos: $5,135 MXN (eventos) o $6,890 MXN (Small Business).\n"
            "3) Suite Completa con Acrílicos LED cálida (3–5 días en taller, pago físico diferible en 2do momento): $7,475 o $10,400 MXN.\n"
            "¿Para qué negocio o evento sería y te paso tu vista previa?"
        ),
    },
    {
        "id": "DM-MAPS",
        "trigger_label": "Vi lo de Google Maps Antes vs. Después",
        "channel": "IG / FB / WA",
        "reply_text": (
            "¡Excelente! En menos de 24h revisamos tu ficha actual de Google Maps y te preparamos gratis tu lámina 'Antes vs. Después' "
            "junto con el checklist de Meta Business Portfolio para evitar bloqueos entre Facebook, Instagram y WhatsApp. "
            "Pásame el nombre exacto de tu negocio y zona en MTY/SPGG para armártela hoy mismo 📸"
        ),
    },
    {
        "id": "DM-BIOGEN",
        "trigger_label": "Info Captoora Biogen (Beta) / Bitácora Física",
        "channel": "IG / TikTok / Gym",
        "reply_text": (
            "Captoora Biogen (Beta) es nuestra bitácora fotográfica en estudio con luz escultural calibrada (1/2000s) "
            "y ángulo exactamente repetible (semanal, quincenal o mensual, de 3 a 60 meses). "
            "Con -35% de piloto fundador va desde $1,268 MXN/mes (3 meses) hasta $748 MXN/mes (60 meses). "
            "¿Buscas plan personal o convenio para atletas y miembros de tu gimnasio/clínica?"
        ),
    },
    {
        "id": "DM-TIEMPOS",
        "trigger_label": "¿Entregan el mismo día? ¿Y los acrílicos/marcos?",
        "channel": "LinkedIn / IG / WA",
        "reply_text": (
            "Sí: toda la parte digital (selección Halftime Blitz en eventos o galería curada en galeria.captoora.studio) "
            "se entrega el mismo día (48–72h en sesiones Small Business de tienda completa). Las piezas físicas artesanales "
            "(acrílicos ópticos con luz LED cálida y marcos de El Marco San Pedro) se fabrican en taller local en 3 a 5 días hábiles "
            "y puedes liquidarlas en un 2do momento al aprobar tu galería 🙌"
        ),
    },
]


def _validate_marketing_state(state: dict[str, Any]) -> None:
    """Guarantee zero prohibited AI/'presumir' phrases in any client-facing calendar/DM string."""
    for post in state.get("content_calendar", []):
        text = f"{post.get('caption', '')}\n{post.get('hashtags', '')}"
        bad = validate_client_copy(text)
        if bad:
            raise ValueError(f"Post {post.get('id')} violó guardrail Captoora: {bad}")
    for dm in state.get("lupe_dm_playbook", []):
        bad = validate_client_copy(dm.get("reply_text", ""))
        if bad:
            raise ValueError(f"DM {dm.get('id')} violó guardrail Captoora: {bad}")


def build_muse_mobile_brief(state: dict[str, Any] | None = None) -> str:
    """Build a compact copy-paste context brief for Meta Muse Mobile while user is away from Mac."""
    asana = read_json(FILES["asana"], default={"sprint": {}, "tasks": []})
    gmaps = read_json(FILES["gmaps_audits"], default={"total_leads": 141, "captured_count": 75, "streetview_count": 19})
    sprint = asana.get("sprint", {})
    pending_tasks = [t for t in asana.get("tasks", []) if t.get("status") in ("waiting_trigger", "in_progress")][:5]
    task_lines = "\n".join(f"- [{t.get('id')}] {t.get('title')}" for t in pending_tasks) or "- Sin bloqueos urgentes."

    return (
        "CONTEXTO DE BOLSILLO CAPTOORA (SINCRO MUSE MÓVIL -> ANTIGRAVITY MAC):\n"
        f"• Sprint Activo: {sprint.get('tuesday_noon_label', 'Martes 17 Nov 12:00 PM')} (Meta 1–3 cierres)\n"
        f"• Base Google Maps en vivo: {gmaps.get('total_leads', 141)} leads, {gmaps.get('captured_count', 75)} capturas PNG, {gmaps.get('streetview_count', 19)} Street View detectados.\n"
        "• REGLAS INQUEBRANTABLES HACIA CLIENTES: 0% mención de IA/Inteligencia Artificial, NUNCA usar 'presumir', separar entrega digital mismo día (o 48–72h Small Biz) de taller LED/marcos (3–5 días hábiles).\n"
        "• TARIFAS -35% ACTIVAS HOY:\n"
        "  1) Navidad 2026: Solo Digital $3,185 | Foto+Impresión $5,135 | Suite Full+LED $7,475 MXN (físico diferible en 2do momento).\n"
        "  2) Captoora Biogen Beta: $1,268/mes (3m) a $748/mes (60m), bitácora visual física semanal–bimestral.\n"
        "  3) Captoora Small Business 2027: Impulso Maps $3,900 | Suite Total $6,890 | Posicionamiento+QR LED $10,400 MXN.\n"
        f"• PRIORIDADES HOY EN RADAR:\n{task_lines}\n"
        "• CUANDO TE DICTE IDEAS O LEADS EN LA CALLE: resúmelos en viñetas cortas [LEAD / CLIP OPUS / TAREA LUPE / TAREA CONAN] para pegarlos de regreso en Antigravity (:8765)."
    )


def build_initial_marketing_state() -> dict[str, Any]:
    """Construct complete Marky + Lupe + Conan workspace seed (zero external quota required)."""
    state = {
        "updated_at": now_iso(),
        "grokbot_status": "ELIMINADO (0% dependencia · 100% equipo nativo en localhost)",
        "team_hierarchy": {
            "director": {"agent_id": "marky_marketing", "name": "Marky", "title": "Director de Marketing & Estrategia"},
            "reports": [
                {"agent_id": "lupe_social", "name": "Lupe", "title": "Social Media, Meta Business Suite, TikTok, LinkedIn & DMs"},
                {"agent_id": "conan_content", "name": "Conan", "title": "Creación de Contenido & Suite de Suscripciones"},
            ],
        },
        "subscriptions_stack": SUBSCRIPTION_STACK,
        "google_pro_sync": GOOGLE_PRO_SYNC_PROTOCOL,
        "opusclip_rescue_sprint": OPUSCLIP_RESCUE_SPRINT,
        "content_calendar": DEFAULT_CONTENT_CALENDAR,
        "lupe_dm_playbook": LUPE_DM_PLAYBOOK,
        "conan_briefs": [
            {
                "id": "BRIEF-001",
                "title": "Maratón OpusClip Pro · 3 Grabaciones Base -> 25–30 Clips 9:16",
                "tool_stack": "OBS + Captions + OpusClip Pro + CapCut",
                "output_format": "MP4 9:16 + Subtítulos Champagne/Volt",
                "for_agent": "lupe_social",
                "status": "in_progress",
                "created_at": now_iso(),
            },
            {
                "id": "BRIEF-002",
                "title": "Carrusel B2B LinkedIn/IG: Evidencia Mismo Día para Patrocinadores 2027",
                "tool_stack": "Canva (4:5) + Aftershoot + mockups.py",
                "output_format": "5 Slides PNG 1080x1350 + PDF Carrusel",
                "for_agent": "lupe_social",
                "status": "ready",
                "created_at": now_iso(),
            },
        ],
        "muse_mobile_sync": {
            "notes_log": [],
            "context_pack": "",
        },
    }
    _validate_marketing_state(state)
    state["muse_mobile_sync"]["context_pack"] = build_muse_mobile_brief(state)
    return state


def get_or_init_marketing_state() -> dict[str, Any]:
    """Load marketing_studio.json or initialize cleanly if missing."""
    existing = read_json(FILES["marketing"], default=None)
    if existing and isinstance(existing, dict) and existing.get("content_calendar"):
        if not existing.get("muse_mobile_sync", {}).get("context_pack"):
            existing.setdefault("muse_mobile_sync", {})["context_pack"] = build_muse_mobile_brief(existing)
            write_json(FILES["marketing"], existing)
        return existing
    fresh = build_initial_marketing_state()
    write_json(FILES["marketing"], fresh)
    return fresh


def regenerate_marketing_plan(focus: str = "all", week_label: str = "Semana Sprint Nov 2026 (-35%)") -> dict[str, Any]:
    """Deterministically refresh Marky's weekly multi-network plan and Muse mobile brief with 0 tokens."""
    state = get_or_init_marketing_state()
    state["updated_at"] = now_iso()
    state["active_week_label"] = week_label
    state["active_focus"] = focus
    state["muse_mobile_sync"]["context_pack"] = build_muse_mobile_brief(state)
    _validate_marketing_state(state)
    write_json(FILES["marketing"], state)

    set_agent_runtime_status("marky_marketing", "ready")
    append_agent_event(
        "marky_marketing",
        "Actualizó Plan de Contenido",
        f"Sincronizó parrilla multired ({week_label}) para Lupe y briefs OpusClip/Canva/Captions de Conan (0 tokens).",
        target_agent="lupe_social",
        zone="estudio_marky",
        source="local_zero_token",
    )
    return state


def enqueue_lupe_calendar_post(post_id: str, custom_caption: str | None = None, platform_override: str | None = None) -> dict[str, Any]:
    """Queue a Lupe social post from marketing_studio.json into Human Trigger Queue with copy validation."""
    state = get_or_init_marketing_state()
    post = next((p for p in state.get("content_calendar", []) if p.get("id") == post_id), None)
    if not post:
        raise ValueError(f"Post '{post_id}' no encontrado en el calendario de Lupe.")

    caption = (custom_caption if custom_caption is not None else post.get("caption", "")).strip()
    tags = post.get("hashtags", "").strip()
    full_copy = f"{caption}\n\n{tags}".strip() if tags and tags not in caption else caption
    violations = validate_client_copy(full_copy)
    if violations:
        raise ValueError("Guardrail bloqueó el copy de Lupe: " + " | ".join(violations))

    platform = (platform_override or post.get("platform") or "Meta Business Suite (FB + IG)").strip()
    queue = read_json(FILES["approvals"], default={"policy": "HUMAN_APPROVAL_REQUIRED", "items": []})
    items = queue.get("items", [])

    apr_id = f"LUPE-{post_id.replace('POST-', '')}"
    items = [i for i in items if i.get("id") != apr_id]
    new_item = {
        "id": apr_id,
        "agent_id": "lupe_social",
        "task_id": "TASK-702",
        "target_name": f"{platform} · {post.get('title')}",
        "niche": post.get("track") or "Marca & Multired",
        "channel": f"{platform} (Programación Lupe)",
        "phone": "",
        "package_ref": f"Conan Brief: {post.get('conan_tool')} -> {post.get('conan_deliverable')}",
        "financial_impact_mxn": 0,
        "estimated_margin_pct": 100.0,
        "compliance_flags": ["0% mención IA", "Sin 'presumir'", "Validado por Marky", "Aprobación Lupe"],
        "draft_text": full_copy,
        "status": "pending_trigger",
        "created_at": now_iso(),
        "decided_at": None,
    }
    items.insert(0, new_item)
    queue["items"] = items
    write_json(FILES["approvals"], queue)

    post["status"] = "queued_for_trigger"
    state["updated_at"] = now_iso()
    write_json(FILES["marketing"], state)

    set_agent_runtime_status("lupe_social", "waiting_trigger")
    append_agent_event(
        "lupe_social",
        f"Encoló {apr_id} ({platform})",
        f"Lupe preparó caption y ficha para {post.get('title')[:80]} (esperando Tu Último Trigger).",
        target_agent="trigger_gate",
        zone="trigger_gate",
        source="local_zero_token",
    )
    return {"enqueued_item": new_item, "marketing_studio": state}


def register_conan_creative_brief(
    title: str,
    tool_stack: str = "OpusClip Pro + CapCut",
    output_format: str = "Reel 9:16",
    target_channel: str = "TikTok + IG Reels",
    notes: str = "",
) -> dict[str, Any]:
    """Create a production brief for Conan (syncing Asana TASK + marketing_studio)."""
    state = get_or_init_marketing_state()
    briefs = state.get("conan_briefs", [])
    next_num = len(briefs) + 1
    brief = {
        "id": f"BRIEF-{next_num:03d}",
        "title": title.strip(),
        "tool_stack": tool_stack.strip(),
        "output_format": output_format.strip(),
        "target_channel": target_channel.strip(),
        "notes": notes.strip(),
        "for_agent": "lupe_social",
        "status": "in_progress",
        "created_at": now_iso(),
    }
    briefs.insert(0, brief)
    state["conan_briefs"] = briefs[:25]
    state["updated_at"] = now_iso()
    write_json(FILES["marketing"], state)

    asana = read_json(FILES["asana"], default={"sprint": {}, "projects": [], "tasks": []})
    tasks = asana.get("tasks", [])
    existing_nums = [int(t["id"].split("-")[1]) for t in tasks if t.get("id", "").startswith("TASK-") and t["id"].split("-")[1].isdigit()]
    new_task = {
        "id": f"TASK-{max(existing_nums, default=700) + 1}",
        "project_id": "proj_social_embudo",
        "title": f"[Conan · {tool_stack}] {title.strip()} -> entrega para Lupe ({target_channel})",
        "assigned_agent": "conan_content",
        "status": "in_progress",
        "priority": "Alta",
        "due_label": "Sprint Suscripciones",
        "depends_on": [],
        "deliverable_ref": f"{brief['id']} ({output_format})",
    }
    tasks.append(new_task)
    asana["tasks"] = tasks
    write_json(FILES["asana"], asana)

    set_agent_runtime_status("conan_content", "ready")
    append_agent_event(
        "conan_content",
        f"Nuevo Brief {brief['id']}",
        f"Conan tomó producción '{title.strip()}' en {tool_stack} para entregar a Lupe.",
        target_agent="lupe_social",
        zone="estudio_conan",
        source="local_zero_token",
    )
    return {"brief": brief, "task": new_task, "marketing_studio": state}


def ingest_muse_mobile_notes(notes_text: str, target_agent: str = "marky_marketing") -> dict[str, Any]:
    """Import mobile notes captured with Meta Muse on the go into Asana tasks and Marketing HQ."""
    clean = (notes_text or "").strip()
    if len(clean) < 4:
        raise ValueError("Pega al menos una idea o nota de Muse para convertirla en acción.")

    state = get_or_init_marketing_state()
    lines = [ln.strip("•-* \t") for ln in clean.splitlines() if ln.strip("•-* \t")]
    summary_line = lines[0][:140]

    asana = read_json(FILES["asana"], default={"sprint": {}, "projects": [], "tasks": []})
    tasks = asana.get("tasks", [])
    existing_nums = [int(t["id"].split("-")[1]) for t in tasks if t.get("id", "").startswith("TASK-") and t["id"].split("-")[1].isdigit()]
    new_task = {
        "id": f"TASK-{max(existing_nums, default=700) + 1}",
        "project_id": "proj_social_embudo",
        "title": f"[Muse Móvil] {summary_line}",
        "assigned_agent": target_agent,
        "status": "in_progress",
        "priority": "Alta",
        "due_label": "Sincronizado de Móvil",
        "depends_on": [],
        "deliverable_ref": "Meta Muse Sync",
    }
    tasks.append(new_task)
    asana["tasks"] = tasks
    write_json(FILES["asana"], asana)

    log = state.setdefault("muse_mobile_sync", {}).setdefault("notes_log", [])
    log.insert(
        0,
        {
            "timestamp": now_iso(),
            "target_agent": target_agent,
            "task_id": new_task["id"],
            "notes": clean[:600],
        },
    )
    state["muse_mobile_sync"]["notes_log"] = log[:20]
    state["muse_mobile_sync"]["context_pack"] = build_muse_mobile_brief(state)
    state["updated_at"] = now_iso()
    write_json(FILES["marketing"], state)

    append_agent_event(
        target_agent,
        f"Sincronizó Nota Muse -> {new_task['id']}",
        summary_line,
        target_agent="lupe_social",
        zone="estudio_marky",
        source="local_zero_token",
    )
    return {"task": new_task, "marketing_studio": state}


def run_local_marketing_mission(agent_id: str, instruction: str | None = None) -> dict[str, Any]:
    """Deterministic zero-quota execution for Marky, Lupe, Conan (never hits third-party bot quotas)."""
    state = get_or_init_marketing_state()
    clean_instr = (instruction or "").strip()

    if agent_id == "marky_marketing":
        updated = regenerate_marketing_plan(focus="all", week_label="Plan Activo (-35% · OpusClip + 2x Google Pro)")
        if clean_instr:
            ingest_muse_mobile_notes(clean_instr, target_agent="marky_marketing")
        return {
            "mode": "local_zero_token",
            "agent_id": agent_id,
            "summary": (
                "Marky actualizó el Plan Maestro de Suscripciones (0 tokens): prioridad crítica salvar 25–30 clips en OpusClip Pro, "
                "reparto Dual Google Pro (Poncho $395 vs Yari $99 promo) y sincronía Muse Móvil."
            ),
            "marketing_studio": updated,
        }

    if agent_id == "lupe_social":
        next_post = next((p for p in state.get("content_calendar", []) if p.get("status") != "queued_for_trigger"), state["content_calendar"][0])
        res = enqueue_lupe_calendar_post(next_post["id"], custom_caption=clean_instr or None)
        return {
            "mode": "local_zero_token",
            "agent_id": agent_id,
            "summary": f"Lupe dejó lista la publicación {res['enqueued_item']['id']} para {next_post['platform']} en Tu Último Trigger (0 tokens).",
            "enqueued_id": res["enqueued_item"]["id"],
        }

    if agent_id == "conan_content":
        brief_title = clean_instr or "Grabación + Batch OpusClip Pro 3 pilares (Maps + Navidad LED + Biogen)"
        res = register_conan_creative_brief(
            title=brief_title,
            tool_stack="OpusClip Pro + Captions + Canva + CapCut",
            output_format="9:16 Reels + 4:5 Carrusel",
            target_channel="IG + TikTok + LinkedIn (Lupe)",
        )
        return {
            "mode": "local_zero_token",
            "agent_id": agent_id,
            "summary": f"Conan registró {res['brief']['id']} y su tarea {res['task']['id']} lista para entregar a Lupe (0 tokens).",
            "brief": res["brief"],
            "task": res["task"],
        }

    # Generic zero-token validation fallback for bots 1..7 when Dry-Run / Sin Cuotas is active
    asana = read_json(FILES["asana"], default={"tasks": []})
    queue = read_json(FILES["approvals"], default={"items": []})
    pending = [i for i in queue.get("items", []) if i.get("status") == "pending_trigger"]
    set_agent_runtime_status(agent_id, "ready")
    event = append_agent_event(
        agent_id,
        "Misión Local (0 Tokens)",
        f"Validó {len(asana.get('tasks', []))} tareas Asana y {len(pending)} triggers pendientes sin consumir cuota externa.",
        source="local_zero_token",
    )
    return {
        "mode": "local_zero_token",
        "agent_id": agent_id,
        "tasks_count": len(asana.get("tasks", [])),
        "pending_triggers": len(pending),
        "event": event,
    }
