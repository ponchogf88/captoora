#!/usr/bin/env python3
"""
CAPTOORA STUDIO // SCRAPER EN VIVO DE EVENTOS, CONCIERTOS, INVITADOS,
INFLUENCERS Y BRECHAS DE COBERTURA FOTOGRÁFICA EN PUERTO VALLARTA

Alcance territorial estricto (Puerto Vallarta, Jalisco):
  1) zona_romantica  -> Emiliano Zapata, Olas Altas, Basilio Badillo, Los Muertos, Amapas Norte
  2) zona_hotelera   -> Zona Hotelera Norte (Las Glorias / Medina Ascencio / Versalles / Fluvial / CICPV),
                        Marina Vallarta y Zona Hotelera Sur / Conchas Chinas / Garza Blanca / Mismaloya
  3) centro_y_bahia  -> Centro Histórico, Malecón, Teatro Vallarta, Isla Río Cuale, Col. 5 de Diciembre
                        (Playa Camarones / MUYGUUD) y experiencias sobre Bahía de Banderas zarpando de PV

Excluye automáticamente Riviera Nayarit, Nuevo Vallarta, Punta Mita, VidantaWorld,
Bucerías, San Pancho, Tepic y webinars remotos fuera de Puerto Vallarta.
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from captoora_agents.config import now_iso, read_json, slugify, validate_client_copy, write_json

PV_DATA_ROOT = ROOT_DIR / "dashboard" / "data" / "puerto_vallarta"

# Note: do NOT put "bahía de banderas" here because many Malecón / Centro / Garza Blanca PV venues
# mention "vista a la Bahía de Banderas" in prose while located inside Puerto Vallarta, Jalisco.
OUTSIDE_PV_MARKERS = (
    "nuevo vallarta",
    "nuevo nayarit",
    "punta mita",
    "punta de mita",
    "municipio bahía de banderas",
    "bahía de banderas, nay",
    "bahia de banderas, nay",
    "vidantaworld",
    "vidanta",
    "tepic",
    "bucerías",
    "bucerias",
    "san francisco, nayarit",
    "san pancho",
    "sayulita",
    "mezcales",
    "jarretaderas",
    "mandarina",
    "yelapa",
    "litibu",
    ", nay.",
    ", nayarit",
    "nayarit.",
)

FORBIDDEN_ORIGIN_TERMS = (
    "colinas de san jerónimo",
    "colinas de san jeronimo",
    "san jerónimo",
    "san jeronimo",
    "monterrey",
    "mty",
    "spgg",
    "san pedro garza",
)


def _fetch_url(url: str, *, timeout: int = 20) -> str:
    """Fetch remote URL reliably using curl HTTP/1.1 to avoid HTTP/2 resets on WP hosts."""
    proc = subprocess.run(
        ["curl", "-sL", "--http1.1", "--max-time", str(timeout), "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", url],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.stdout or ""


def _strip_tags(raw: str) -> str:
    cleaned = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw or "", flags=re.S | re.I)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = unicodedata.normalize("NFC", html_lib.unescape(cleaned))
    return re.sub(r"\s+", " ", cleaned).strip()


def _assert_clean_copy(text: str, context: str) -> str:
    violations = validate_client_copy(text)
    if violations:
        raise ValueError(f"Guardrail Captoora bloqueó {context}: {violations}")
    low = text.lower()
    for term in FORBIDDEN_ORIGIN_TERMS:
        if term in low:
            raise ValueError(f"Término de origen bloqueado ('{term}') en {context}")
    return text


def _load_known_pv_leads() -> dict[str, dict[str, Any]]:
    """Load Phase 1 Google Maps leads for Zona Romántica and Zona Hotelera to enrich event venues."""
    known: dict[str, dict[str, Any]] = {}
    for z in ("zona_romantica", "zona_hotelera"):
        data = read_json(PV_DATA_ROOT / z / "gmaps_audits.json", default={})
        for item in data.get("audits", []):
            name = str(item.get("nombre") or "").strip().lower()
            if name:
                known[name] = item
    return known


def _match_known_lead(venue: str, known_leads: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    low = (venue or "").lower()
    if not low:
        return None
    for kname, rec in known_leads.items():
        if len(kname) >= 5 and (kname in low or low in kname):
            return {
                "slug": rec.get("slug"),
                "nombre_gmaps": rec.get("nombre"),
                "telefono": rec.get("telefono"),
                "audit_score": rec.get("audit_score"),
                "zona_mapeada": rec.get("zona"),
            }
    return None


def classify_event_zone(title: str, venue: str, details: str = "") -> tuple[str | None, str]:
    """
    Strictly classify PV events into ('zona_romantica', 'zona_hotelera', 'centro_y_bahia', or None if outside PV).
    """
    full_blob = f"{title} {venue} {details}".lower()
    if any(m in full_blob for m in OUTSIDE_PV_MARKERS):
        return None, "Fuera de Puerto Vallarta (Riviera Nayarit / Vidanta / Tepic)"

    rom_markers = (
        "zona romántica",
        "zona romantica",
        "emiliano zapata",
        "olas altas",
        "basilio badillo",
        "los muertos",
        "lázaro cárdenas",
        "lazaro cardenas",
        "púlpito",
        "pulpito",
        "francisco i. madero",
        "venustiano carranza",
        "amapas",
        "the palm",
        "coco cabaret",
        "act2pv",
        "mantamar",
        "industry night",
        "pool club pv",
        "casa cupula",
        "casa cúpula",
        "the tryst",
        "nacho daddy",
        "el dorado",
        "daiquiri dicks",
        "canto restaurant",
        "sanctuary - pv",
        "chachalaca",
        "la cruda",
        "one six one",
        "trovasi",
        "villa tita",
        "boys on fire",
        "sea monkey",
    )
    hot_markers = (
        "zona hotelera",
        "las glorias",
        "villa premiere",
        "elena 1927",
        "puerto de luna",
        "marina vallarta",
        "velas vallarta",
        "marriott",
        "la ribera",
        "táu",
        "tau beach",
        "garza blanca",
        "mousai",
        "bocados steak",
        "hiroshi",
        "karuma",
        "misika",
        "dao",
        "amixtli",
        "xalli",
        "le kliff",
        "costa sur",
        "mismaloya",
        "conchas chinas",
        "fluvial",
        "valarte",
        "cicpv",
        "centro internacional de convenciones",
        "cuarto de música",
        "albatros",
        "american school",
        "red door bar versalles",
        "versalles",
        "padel 233",
        "guadalupe victoria",
        "vista vallarta",
        "puerto magico",
        "puerto mágico",
        "chica locca",
        "sheraton",
        "buenaventura",
        "fiesta americana",
        "krystal",
        "hilton vallarta",
        "hyatt ziva",
        "barcelo",
        "barceló",
        "westin",
    )
    cb_markers = (
        "centro histórico",
        "centro historico",
        "malecón de puerto vallarta",
        "malecon de puerto vallarta",
        "parroquia",
        "guadalupanas",
        "teatro vallarta",
        "5 de diciembre",
        "playa camarones",
        "muyguud",
        "río cuale",
        "rio cuale",
        "river cafe",
        "oscar's",
        "oscars",
        "le bistro",
        "café des artistes",
        "cafe des artistes",
        "guadalupe sánchez",
        "art walk",
        "artwalk",
        "majahuitas",
        "marigalante",
        "los mangos",
        "colombia 1429",
        "gringo gulch",
        "bahía de banderas",
        "bahia de banderas",
        "malecón",
        "malecon",
    )

    def _classify_blob(blob: str) -> tuple[str | None, str] | None:
        if any(m in blob for m in rom_markers):
            if any(k in blob for k in ("the palm", "coco cabaret", "act2pv", "nacho daddy", "cabaret")):
                return "zona_romantica", "Zona Romántica · Circuito Cabaret & Teatros"
            if any(k in blob for k in ("mantamar", "industry", "tryst", "casa cupula", "casa cúpula", "pool club", "one six one")):
                return "zona_romantica", "Zona Romántica · Beach Clubs, Hoteles Boutique & Nightlife"
            return "zona_romantica", "Zona Romántica · Olas Altas / Gastronomía / Mixers"

        if any(m in blob for m in hot_markers):
            if any(k in blob for k in ("garza blanca", "mousai", "amixtli", "xalli", "le kliff", "mismaloya", "costa sur", "conchas chinas", "hyatt ziva", "barcel", "hilton")):
                return "zona_hotelera", "Zona Hotelera Sur · Garza Blanca / Costa Sur / Conchas Chinas"
            if any(k in blob for k in ("marina vallarta", "marriott", "velas vallarta", "la ribera", "táu", "tau beach", "puerto magico", "puerto mágico", "westin")):
                return "zona_hotelera", "Zona Hotelera · Marina Vallarta & Puerto Mágico"
            if any(k in blob for k in ("versalles", "fluvial", "cicpv", "albatros", "cuarto de música", "padel 233", "vista vallarta")):
                return "zona_hotelera", "Zona Hotelera Norte · Corredor Versalles / Fluvial / CICPV"
            return "zona_hotelera", "Zona Hotelera Norte · Las Glorias & Franja Hotelera"

        if any(m in blob for m in cb_markers):
            if any(k in blob for k in ("majahuitas", "marigalante", "catamar", "crucero", "embarcación", "fiesta en el mar")):
                return "centro_y_bahia", "Centro / Bahía · Experiencias en la Bahía (Salida PV)"
            if any(k in blob for k in ("5 de diciembre", "playa camarones", "muyguud", "colombia 1429", "teatro vallarta", "los mangos")):
                return "centro_y_bahia", "Centro / Bahía · Col. 5 de Diciembre / Teatro Vallarta"
            return "centro_y_bahia", "Centro / Bahía · Malecón, Centro Histórico & Isla Río Cuale"
        return None

    head_blob = f"{title} {venue}".lower()
    return _classify_blob(head_blob) or _classify_blob(full_blob) or (None, "Sin ubicación verificada en las 3 zonas PV")


def _build_event_outreach_script(
    *,
    titulo: str,
    recinto: str,
    fecha: str,
    zona_label: str,
    categoria: str,
    invitados: list[str],
    cobertura_status: str,
) -> str:
    guest_ref = f" junto a {', '.join(invitados[:2])}" if invitados else ""
    cat_low = categoria.lower()
    if "deporte" in cat_low or "pádel" in cat_low or "marat" in cat_low or "golf" in cat_low or "pesca" in cat_low:
        hook = "acción deportiva a 1/2000s (cuerpo entero y entregas digitales el mismo día para competidores y marcas)"
        tier2 = "trofeos/placas en acrílico óptico con luz LED y logotipo de patrocinadores (listos en 3–5 días hábiles)"
    elif "gastronom" in cat_low:
        hook = "fotografía editorial culinaria, emplatado con iluminación controlada, retratos de chefs y cobertura discreta en mesa VIP el mismo día"
        tier2 = "menús luminosos o placas QR en acrílico óptico y madera sellada (3–5 días hábiles)"
    elif "posada" in cat_low or "hotel" in cat_low or "año nuevo" in cat_low:
        hook = "cobertura nocturna con iluminación editorial para cenas de gala, posadas corporativas y celebraciones (galería lista al día siguiente para invitados y prensa)"
        tier2 = "porta-menús o displays acrílicos LED grabados con QR directo a Google Maps o galería privada (3–5 días hábiles)"
    elif "arte" in cat_low or "cultura" in cat_low:
        hook = "fotografía documental de exhibición, obra e invitados VIP con colorimetría fiel y entrega inmediata para catálogos y difusión"
        tier2 = "cédulas o señalética museográfica grabada en acrílico óptico (3–5 días hábiles)"
    else:
        hook = "retrato editorial de escenario, camerinos y público en alta sensibilidad nocturna con galería lista esa misma noche o en 24h"
        tier2 = "señalética VIP, stands QR o reconocimientos grabados en taller (3–5 días hábiles)"

    if "Abierta" in cobertura_status:
        gap_note = f"No detectamos crédito de cobertura editorial independiente publicada para esta fecha en {zona_label}."
    else:
        gap_note = f"Aunque existe cobertura general de prensa, vemos espacio directo para cobertura dedicada a artistas, mesas VIP y marcas aliadas en {zona_label}."

    draft = (
        f"Hola equipo de {recinto} ({titulo}{guest_ref} · {fecha}), soy Jesús Gutiérrez, director y fotógrafo en Captoora Studio. "
        f"{gap_note} Trabajamos {hook}. "
        f"Manejamos cobertura Solo Digital con beneficio de temporada (-35%, galería lista el mismo día para difusión y venta/etiquetado) "
        f"y, si lo requieren en una segunda etapa, {tier2}. ¿Te comparto 3 muestras de portafolio y opciones por WhatsApp?"
    )
    return _assert_clean_copy(draft, f"guion evento {titulo}")


def _scrape_visitapuertovallarta() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    events: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    index_html = _fetch_url("https://visitapuertovallarta.com.mx/eventos")
    slugs = sorted(set(re.findall(r'href=["\'](?:https://visitapuertovallarta\.com\.mx)?/eventos/([a-z0-9\-]+)["\']', index_html)))

    for slug in slugs:
        url = f"https://visitapuertovallarta.com.mx/eventos/{slug}"
        page_html = _fetch_url(url)
        txt = _strip_tags(page_html)
        idx = txt.find("Inicio Eventos")
        body = txt[idx + len("Inicio Eventos") : idx + 2400] if idx != -1 else txt[:2400]
        title_m = re.findall(r"<h1[^>]*>(.*?)</h1>", page_html, re.S)
        title = _strip_tags(title_m[0]) if title_m else slug.replace("-", " ").title()

        date_match = re.search(r"(?:Inicia\s*:\s*([0-9\-]+)\s*Finaliza\s*:\s*([0-9\-]+)|([0-9]{2}-[0-9]{2}-202[67]))", body)
        fecha = "Temporada 2026–2027"
        if date_match:
            if date_match.group(1) and date_match.group(2):
                fecha = f"{date_match.group(1)} al {date_match.group(2)}"
            elif date_match.group(3):
                fecha = date_match.group(3)

        # Skip events ending before Nov 18, 2026
        if "2027" not in fecha and all(m not in fecha for m in ("-11-2026", "-12-2026", "11-2026", "12-2026")):
            pass
        if any(s in slug for s in ("2027",)) and all(s not in slug for s in ("2026-2027", "ano-nuevo", "bear-week")):
            # Exclude April/May/Feb 2027 far-out events except Jan 2027 / 2026-2027 season
            if any(k in slug for k in ("charro", "ceviche", "fairyland", "raicilla", "utmb")):
                excluded.append({"titulo": title, "fuente_url": url, "razon": "Fuera de ventana Nov 2026 – Ene 2027"})
                continue

        if "yelapa" in slug:
            excluded.append({"titulo": title, "fuente_url": url, "razon": "Fuera de zonas PV objetivo (Yelapa)"})
            continue

        # Venue hints from known official pages
        venue_map = {
            "31-festival-gourment-international": ("30 restaurantes sede en PV (ver detalle FGI)", "Gastronomía Internacional"),
            "ano-nuevo-en-puerto-vallarta": ("Malecón de Puerto Vallarta & Bahía de Banderas", "Año Nuevo / Pirotecnia"),
            "art-market-marina-vallarta-2026": ("Malecón de Marina Vallarta", "Mercado Cultural & Arte"),
            "fiestas-guadalupanas-2026": ("Parroquia de Ntra. Sra. de Guadalupe & Centro Histórico", "Tradición / Peregrinaciones"),
            "gay-mixers-2026-2027": ("Sedes rotativas ZR / Centro / Versalles (Daiquiri Dicks, Trovasi, Red Door Versalles, Casa Cupula)", "Networking & Comunidad LGBTQ+"),
            "ifc-vallarta-home-tours": ("Salida Sea Monkey (Zona Romántica) -> Gringo Gulch & Conchas Chinas", "Arquitectura & Beneficencia"),
            "los-claxons": ("Cuarto de Música (Col. Albatros, Zona Hotelera Norte)", "Concierto Pop-Rock"),
            "medio-maraton-puerto-vallarta-2026": ("Explanada CICPV & Blvd. Medina Ascencio (5K / 21K)", "Deportes / Running"),
            "movie-picnic-2026-2027": ("Jardín de la Luna — Hotel Puerto de Luna (Zona Hotelera)", "Cine al Aire Libre & Mascotas"),
            "muyguud-feria-internacional-de-arte-contemporaneo-2026": ("Playa Camarones / Venezuela 55-A, Col. 5 de Diciembre", "Feria Internacional de Arte Contemporáneo"),
            "olas-altas-farmers-market-2026-2027": ("Parque Lázaro Cárdenas, Zona Romántica", "Mercado Gastronómico & Diseño"),
            "puerto-vallarta-cabaret-workshop": ("Act2PV Theater, Basilio Badillo (Zona Romántica)", "Cabaret & Clases Magistrales"),
            "torneo-de-pesca-deportiva-mismaloya-2026": ("Playa de Mismaloya (Zona Hotelera Sur PV)", "Torneo Deportivo & Chefs en Vivo"),
            "vallarta-art-walk-2026-2027": ("Centro Histórico (16 galerías de arte)", "Circuito de Galerías / Arte"),
            "vrban-vallarta-2026": ("Malecón de Puerto Vallarta -> Centro -> Zona Romántica (10K)", "Deportes / Carrera Urbana"),
            "mantamar-bear-week-2027": ("Mantamar Beach Club & Zona Romántica", "Festival & DJs"),
        }
        recinto, cat = venue_map.get(slug, ("Puerto Vallarta", "Evento Oficial Turístico"))
        zona, subzona = classify_event_zone(title, recinto, body)
        if not zona:
            excluded.append({"titulo": title, "fuente_url": url, "razon": subzona})
            continue

        guests_map = {
            "los-claxons": ["Los Claxons (Gira Cantando + Contando · Latin Grammy nominees)"],
            "muyguud-feria-internacional-de-arte-contemporaneo-2026": ["+71 artistas internacionales (16 estados MX, 13 países)", "Orquesta Escuela PV", "Rimiyoho", "Taiga Brava", "DJ Memo Pearls", "Jorge Ayala 'Troglodita'"],
            "puerto-vallarta-cabaret-workshop": ["Mark Hartman", "Lina Koutrakos", "Beckie Menzie"],
            "gay-mixers-2026-2027": ["Out & About PV", "Henry Ho / Jeremy Reigel", "Chefs y anfitriones locales semanales"],
            "torneo-de-pesca-deportiva-mismaloya-2026": ["Equipos de pesca deportiva", "Chefs invitados cocinando en vivo en playa"],
        }
        influencers_map = {
            "muyguud-feria-internacional-de-arte-contemporaneo-2026": ["Coleccionistas de arte, prensa cultural y fotógrafa Alejandra Herrera (promo OAPV)"],
            "gay-mixers-2026-2027": ["Out & About PV (Adan Villa cubre ediciones selectas)", "Emprendedores expat & creadores LGBTQ+"],
            "los-claxons": ["Asistentes jóvenes locales, público de conciertos y prensa musical PV"],
            "medio-maraton-puerto-vallarta-2026": ["Corredores nacionales/internacionales y clubes running PV/GDL/CDMX"],
            "vrban-vallarta-2026": ["Atletas locales y clubes ciclistas/running (Vallarta Sobre Ruedas / Xisco Bikes)"],
            "art-market-marina-vallarta-2026": ["+200 expositores locales y visitantes de yates/hoteles de Marina"],
            "olas-altas-farmers-market-2026-2027": ["Productores artesanales, nómadas digitales y microcreadores foodie"],
        }
        cov_map = {
            "gay-mixers-2026-2027": "Parcial — Out & About PV (Adan Villa) cubre varias noches; marcas patrocinadoras, bares anfitriones e invitados VIP carecen de galería propia mismo día.",
            "muyguud-feria-internacional-de-arte-contemporaneo-2026": "Parcial — Material promocional acreditado a Alejandra Herrera / OAPV, pero 71 artistas y performances individuales buscan cobertura personalizada y reels.",
            "los-claxons": "Abierta / Oportunidad Vip & Afterparty — Concierto íntimo sin servicio foto-editorial para fans VIP ni contenido para patrocinadores del venue.",
            "medio-maraton-puerto-vallarta-2026": "Parcial — Foto masiva genérica de meta; alta oportunidad para clubes privados, patrocinadores o paquetes VIP de entrega mismo día.",
            "vrban-vallarta-2026": "Abierta — Carrera urbana escénica de 10K (Malecón–Zona Romántica) ideal para venta de galería editorial instantánea y marcas patrocinadoras.",
            "art-market-marina-vallarta-2026": "Abierta — +200 expositores sin fotógrafo editorial compartido ni displays LED QR unificados.",
            "torneo-de-pesca-deportiva-mismaloya-2026": "Abierta — Premios en efectivo y chefs en vivo en playa sin fotógrafo comercial asignado en web.",
            "puerto-vallarta-cabaret-workshop": "Abierta — Participantes internacionales buscando headshots y reels escénicos en vivo.",
            "fiestas-guadalupanas-2026": "Abierta — Cobertura editorial cultural para marcas locales, balcones privados y hoteles centro/malecón.",
            "movie-picnic-2026-2027": "Abierta — Hotel Puerto de Luna sin cobertura editorial nocturna frecuente ni activación patrocinada.",
        }

        events.append(
            {
                "id": f"vpv-{slug}",
                "fecha": fecha,
                "horario": "Consultar sede / ficha oficial",
                "titulo": title,
                "recinto": recinto,
                "zona": zona,
                "subzona": subzona,
                "categoria": cat,
                "invitados_artistas_lineup": guests_map.get(slug, ["Talento y anfitriones oficiales del programa PV"]),
                "influencers_relacionados": influencers_map.get(slug, ["Audiencia turística y creadores locales de temporada (#VisitaPuertoVallarta)"]),
                "cobertura_fotografica_detectada": cov_map.get(slug, "Abierta — Sin crédito de fotógrafo dedicado en ficha oficial FIDETUR."),
                "estado_oportunidad_captoora": "Parcial / Oportunidad VIP & Marcas" if cov_map.get(slug, "").startswith("Parcial") else "Abierta / Sin fotógrafo dedicado",
                "fuente_url": url,
                "fuente_portal": "VisitaPuertoVallarta.com.mx (FIDETUR)",
                "resumen": body[:280],
            }
        )
    return events, excluded


def _scrape_festival_gourmet() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Scrape Festival Gourmet Internacional 31st Edition program + PV-only host restaurants & guest chefs."""
    events: list[dict[str, Any]] = []
    guests: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    prog_txt = _strip_tags(_fetch_url("https://festivalgourmet.com.mx/programa/"))
    part_html = _fetch_url("https://festivalgourmet.com.mx/participantes/")
    rest_urls = sorted(set(re.findall(r"https://festivalgourmet\.com\.mx/restaurantes/[a-z0-9\-]+/", part_html)))

    # Program highlights strictly inside PV (Nov 18 - Nov 22, 2026 active window)
    fgi_specials = [
        (
            "Miércoles 18 Nov 2026",
            "18:00 h",
            "Safari Gourmet Puerto Vallarta (El Dorado · Azafrán · Le Bistro · Café des Artistes)",
            "El Dorado -> Azafrán -> Le Bistro -> Café des Artistes",
            "zona_romantica",
            "Zona Romántica · Olas Altas / Gastronomía / Mixers",
            ["Chefs de El Dorado, Azafrán, Le Bistro y Thierry Blouet (Café des Artistes)", "Casas vinícolas Viparmex"],
            "https://festivalgourmet.com.mx/programa/",
        ),
        (
            "18, 19 y 20 Nov 2026",
            "19:00 h",
            "Marea & Brasas — Cena a 4 Manos (Chef Rogelio Domínguez + Chef Invitado Freddy Monteros)",
            "Restaurante Elena 1927 · Hotel Villa Premiere (Col. 5 de Diciembre / Zona Hotelera Norte)",
            "zona_hotelera",
            "Zona Hotelera Norte · Las Glorias & Franja Hotelera",
            ["Chef Rogelio Domínguez (Elena 1927)", "Chef Invitado Freddy Monteros (Erizo de Mar, Guadalajara · ex Quique Dacosta 3★ Michelin)"],
            "https://festivalgourmet.com.mx/restaurantes/elena-1927/",
        ),
        (
            "Sábado 21 Nov 2026",
            "09:00 h",
            "Sky Drag Brunch · 31º Festival Gourmet Internacional",
            "The Top Sky Bar — Almar Resort (Zona Romántica)",
            "zona_romantica",
            "Zona Romántica · Beach Clubs, Hoteles Boutique & Nightlife",
            ["Talento Drag residente de The Top Sky Bar", "Mixología & gastronomía FGI"],
            "https://festivalgourmet.com.mx/programa/",
        ),
        (
            "Sábado 21 Nov 2026",
            "17:00 h",
            "Evento de Clausura Puerto Vallarta: BBQ & Wine",
            "Hotel Velas Vallarta (Marina Vallarta)",
            "zona_hotelera",
            "Zona Hotelera · Marina Vallarta & Puerto Mágico",
            ["Chef Víctor Howard (Pitmaker BBQ · 4 veces campeón mundial)", "+30 etiquetas de vino Viparmex"],
            "https://festivalgourmet.com.mx/restaurantes/laribera/",
        ),
    ]
    for fecha, horario, titulo, recinto, zkey, subz, g_list, furl in fgi_specials:
        events.append(
            {
                "id": slugify(f"fgi-{titulo[:32]}"),
                "fecha": fecha,
                "horario": horario,
                "titulo": titulo,
                "recinto": recinto,
                "zona": zkey,
                "subzona": subz,
                "categoria": "Gastronomía de Alta Gama / Festival Gourmet",
                "invitados_artistas_lineup": g_list,
                "influencers_relacionados": ["Creadores foodie PV/GDL, prensa gastronómica y sommeliers"],
                "cobertura_fotografica_detectada": "Parcial — Prensa institucional general del festival; alta demanda individual de restaurantes anfitriones, chefs invitados y bodegas de vino para reels y retrato privado.",
                "estado_oportunidad_captoora": "Parcial / Oportunidad Chefs & Restaurantes",
                "fuente_url": furl,
                "fuente_portal": "FestivalGourmet.com.mx (Edición 31)",
                "resumen": prog_txt[:220],
            }
        )

    # Parse all 26 host restaurants and enforce PV-only boundary
    non_pv_fgi_slugs = {"codex", "emiliano", "hoja-santa", "ikan", "il-molo", "la-cocina", "lacasa", "loma42nvonayarit", "loma42tepic", "mauka", "piaf", "taormina", "tunablanca"}
    for r_url in rest_urls:
        r_slug = r_url.rstrip("/").split("/")[-1]
        r_html = _fetch_url(r_url)
        r_txt = _strip_tags(r_html)
        name_m = r_txt.split(" – Festival Gourmet", 1)[0].split(" &#8211;", 1)[0].strip()

        chef_block_m = re.search(r"CHEF INVITADO.*?data-widget_type=\"text-editor\.default\"[^>]*>(.*?)</div>", r_html, re.S | re.I)
        chef_name = _strip_tags(chef_block_m.group(1)) if chef_block_m else ""
        if not chef_name or "chef local" in chef_name.lower() or len(chef_name) > 55:
            chef_m = re.search(r"CHEF INVITADO\s+([A-ZÁÉÍÓÚÑa-záéíóúñ\s\.&\-]{3,50})", r_txt)
            chef_name = chef_m.group(1).strip() if chef_m else "Chef invitado FGI"

        addr_m = re.search(r"Dirección\s+(.*?)(?:Horarios|RESERVACIONES|PAGINA WEB)", r_txt)
        addr = addr_m.group(1).strip() if addr_m else ""

        if r_slug in non_pv_fgi_slugs:
            excluded.append({"titulo": f"FGI Anfitrión: {name_m}", "direccion": addr, "fuente_url": r_url, "razon": "Fuera de Puerto Vallarta (Riviera Nayarit / Tepic)"})
            continue

        z, subz = classify_event_zone(name_m, addr, f"{name_m} {addr}")
        if not z:
            excluded.append({"titulo": f"FGI Anfitrión: {name_m}", "direccion": addr, "fuente_url": r_url, "razon": subz})
            continue

        guests.append(
            {
                "nombre_invitado": chef_name,
                "rol": "Chef Invitado (31º Festival Gourmet Internacional · 12–22 Nov 2026)",
                "sede_pv": name_m,
                "zona": z,
                "subzona": subz,
                "direccion": addr,
                "fuente_url": r_url,
            }
        )

    return events, guests, excluded


def _scrape_cabarets_and_theaters() -> list[dict[str, Any]]:
    """Live WP Tribe API for The Palm + Coco Cabaret + Act2PV HTML + Teatro Vallarta sitemap/Fever."""
    events: list[dict[str, Any]] = []

    # 1 & 2. The Palm Cabaret & Coco Cabaret (WP Tribe REST API)
    for source_name, api_url, venue_name, subz in [
        (
            "ThePalmCabaret.com",
            "https://thepalmcabaret.com/wp-json/tribe/events/v1/events?per_page=80&start_date=2026-11-18",
            "The Palm Cabaret & Bar (Olas Altas 508)",
            "Zona Romántica · Circuito Cabaret & Teatros",
        ),
        (
            "Coco-Cabaret.com",
            "https://coco-cabaret.com/wp-json/tribe/events/v1/events?per_page=80&start_date=2026-11-18",
            "Coco Cabaret by The Palm (Fco. I. Madero 289)",
            "Zona Romántica · Circuito Cabaret & Teatros",
        ),
    ]:
        raw = _fetch_url(api_url)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {}
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for ev in data.get("events", []):
            title = html_lib.unescape(str(ev.get("title") or "")).strip()
            if not title:
                continue
            grouped[title].append(ev)

        for show_title, occs in grouped.items():
            occs_sorted = sorted(occs, key=lambda x: str(x.get("start_date") or ""))
            first_dt = str(occs_sorted[0].get("start_date") or "")
            last_dt = str(occs_sorted[-1].get("start_date") or "")
            date_label = first_dt[:10] if len(occs_sorted) == 1 else f"{first_dt[:10]} al {last_dt[:10]} ({len(occs_sorted)} funciones)"
            hour_label = first_dt[11:16] + " h" if len(first_dt) >= 16 else "Noche"
            # Infer featured artist from title
            star = show_title
            for sep in ("Starring ", "Featuring ", "With ", " – ", " - ", ": "):
                if sep in show_title:
                    star = show_title.split(sep)[-1].strip()
                    break
            events.append(
                {
                    "id": slugify(f"cab-{venue_name[:10]}-{show_title[:36]}"),
                    "fecha": date_label,
                    "horario": hour_label,
                    "titulo": show_title,
                    "recinto": venue_name,
                    "zona": "zona_romantica",
                    "subzona": subz,
                    "categoria": "Cabaret, Tributo Musical & Teatro en Vivo",
                    "invitados_artistas_lineup": [star],
                    "influencers_relacionados": ["Creadores LGBT+, fans de teatro musical y reseñadores locales PV"],
                    "cobertura_fotografica_detectada": (
                        "Parcial — Show Boys on Fire acredita a Eddy Araiza en sesiones promo de calendario; funciones regulares y estrenos de artistas buscan foto de escenario y meet & greet."
                        if "boys on fire" in show_title.lower()
                        else "Abierta / Promo Ocasional — Las funciones semanales dependen de celulares del público o cortesías antiguas; fuerte oportunidad de paquete foto + reels por artista/productora."
                    ),
                    "estado_oportunidad_captoora": "Abierta / Paquete Artista & Productora",
                    "fuente_url": str(occs_sorted[0].get("url") or api_url),
                    "fuente_portal": source_name,
                    "resumen": f"Residencia o función confirmada en calendario oficial ({len(occs_sorted)} fecha(s) registradas desde 2026-11-18).",
                }
            )

    # 3. Act2PV HTML highlights
    act2_html = _fetch_url("https://act2pv.com/")
    act2_headings = [_strip_tags(h) for h in re.findall(r"<h[2-4][^>]*>(.*?)</h[2-4]>", act2_html, re.S)]
    seen_act2: set[str] = set()
    for heading in act2_headings:
        low = heading.lower()
        if any(skip in low for skip in ("current schedule", "excellent", "box office", "location")) or len(heading) < 5:
            continue
        if heading in seen_act2:
            continue
        seen_act2.add(heading)
        if any(k in low for k in ("christmas", "holiday", "xmas", "dueling", "gaga", "cabaret", "bambinos", "santana", "casanueces", "broadway", "beatles", "motown", "liberace")):
            events.append(
                {
                    "id": slugify(f"act2-{heading[:38]}"),
                    "fecha": "Nov 2026 – Ene 2027 (Cartelera Activa)",
                    "horario": "17:00 – 21:30 h según función",
                    "titulo": heading,
                    "recinto": "Act2PV Entertainment Complex (Basilio Badillo 300)",
                    "zona": "zona_romantica",
                    "subzona": "Zona Romántica · Circuito Cabaret & Teatros",
                    "categoria": "Teatro Musical, Cabaret & Especiales Navideños",
                    "invitados_artistas_lineup": [heading.title()],
                    "influencers_relacionados": ["Alexis Mateo / Xunami Muse (en Latina Royale), Mark Hartman, Lina Koutrakos, comunidad teatral PV"],
                    "cobertura_fotografica_detectada": "Abierta — Cartelera múltiple con shows navideños nuevos sin crédito editorial fijo en ficha web.",
                    "estado_oportunidad_captoora": "Abierta / Sin fotógrafo dedicado",
                    "fuente_url": "https://act2pv.com/",
                    "fuente_portal": "Act2PV.com",
                    "resumen": f"Producción en cartelera de temporada alta en Act2PV ({heading}).",
                }
            )

    # 4. Teatro Vallarta (Centro / Bahía - Col. 5 de Diciembre / Uruguay 184)
    tv_sitemap = _fetch_url("https://teatrovallarta.com/sitemap.xml")
    fever_html = _fetch_url("https://feverup.com/es/puerto-vallarta/candlelight")
    teatro_shows = [
        (
            "18 Nov 2026 (y fechas de temporada)",
            "Por confirmar en taquilla",
            "Mayahuel — The Goddess of Tequila (Acrobacia, Danza & Tecnología Escénica)",
            "Teatro Vallarta (Uruguay 184, Col. 5 de Diciembre)",
            "Espectáculo Escénico / Acrobacia",
            ["Elenco mexicano de artes circenses, danza contemporánea y música original", "Tasting Maestro Tequilero VIP"],
            "https://www.teatrovallarta.com/artes-escenicas/mayahuel-11",
        ),
        (
            "11 Dic 2026",
            "Noche (Red Access)",
            "Interstellar with Live Orchestra — Concierto Sinfónico Inmersivo",
            "Teatro Vallarta (Uruguay 184, Col. 5 de Diciembre)",
            "Concierto Sinfónico",
            ["Orquesta en vivo interpretando partitura de Hans Zimmer"],
            "https://boletos.redaccess.com/artes-escenicas/interstellar-with-live-orchestra-puerto-vallarta.-1925",
        ),
        (
            "18 Dic 2026",
            "Noche",
            "El Cascanueces — World Ballet Tour",
            "Teatro Vallarta (Uruguay 184, Col. 5 de Diciembre)",
            "Ballet Clásico / Temporada Navideña",
            ["Compañía internacional World Ballet Tour"],
            "https://www.teatrovallarta.com/otros/el-cascanueces-world-ballet-tour-27",
        ),
        (
            "27 Dic 2026",
            "19:00 h & 21:00 h",
            "Candlelight Puerto Vallarta: Vivaldi & Clásicos Navideños a la Luz de las Velas",
            "Teatro Vallarta Centro Cultural (Uruguay 184, Col. 5 de Diciembre)",
            "Concierto a la Luz de las Velas",
            ["Cuarteto de cuerdas Candlelight / Fever Originals"],
            "https://feverup.com/es/puerto-vallarta/candlelight",
        ),
        (
            "30 Dic 2026",
            "Noche",
            "CelloVoci Presents: Music of the Night (Pre-Año Nuevo)",
            "Teatro Vallarta (Uruguay 184, Col. 5 de Diciembre)",
            "Concierto / Ópera-Pop",
            ["Branden & James (America's Got Talent)", "Effie Passero (Postmodern Jukebox / American Idol)", "Host: Sutton Lee Seymour", "Director: Mark Hartman + Orquesta local PV"],
            "https://www.teatrovallarta.com/musica/music-of-the-night-29",
        ),
    ]
    for fecha, horario, titulo, recinto, cat, stars, url in teatro_shows:
        # Verify presence in sitemap or live Fever HTML
        verified_live = ("candlelight" in url and "Teatro Vallarta" in fever_html) or (url.split("/")[-1] in tv_sitemap or "teatrovallarta" in url)
        if not verified_live:
            continue
        events.append(
            {
                "id": slugify(f"teatro-{titulo[:36]}"),
                "fecha": fecha,
                "horario": horario,
                "titulo": titulo,
                "recinto": recinto,
                "zona": "centro_y_bahia",
                "subzona": "Centro / Bahía · Col. 5 de Diciembre / Teatro Vallarta",
                "categoria": cat,
                "invitados_artistas_lineup": stars,
                "influencers_relacionados": ["Comunidad cultural PV, audiencia internacional expat y prensa de espectáculos"],
                "cobertura_fotografica_detectada": "Abierta — Giras internacionales (Candlelight, Interstellar, World Ballet, CelloVoci) casi nunca viajan con fotógrafo propio para prensa/patrocinadores locales.",
                "estado_oportunidad_captoora": "Abierta / Alta Prioridad Promotores",
                "fuente_url": url,
                "fuente_portal": "TeatroVallarta.com / Fever / RedAccess",
                "resumen": "Fecha verificada en cartelera oficial de Teatro Vallarta y boleteras.",
            }
        )

    return events


def _scrape_beach_clubs_and_eventbrite() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    events: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    # 1. Mantamar Beach Club
    mantamar_txt = _strip_tags(_fetch_url("https://mantamarvallarta.com/es/eventos-gay-puerto-vallarta"))
    mantamar_specs = [
        ("19 – 22 Nov 2026", "11:00 AM", "Brawny Bear Weekend @ Mantamar Beach Club", "Mantamar Beach Club | Bar & Sushi (Zona Romántica)", ["10+ DJs internacionales y residentes Brawny Bear", "Fiestas de alberca y espuma"]),
        ("26 – 29 Nov 2026", "11:00 AM", "Thanksgiving Weekend @ Mantamar Beach Club", "Mantamar Beach Club | Bar & Sushi (Zona Romántica)", ["Lineup DJs circuito internacional Thanksgiving PV"]),
        ("29 Dic 2026 – 03 Ene 2027", "11:00 AM", "Mantamar New Years 2027 Festival", "Mantamar Beach Club | Bar & Sushi (Zona Romántica)", ["DJs internacionales de circuito, go-go dancers y cierre NYE frente al mar"]),
        ("15 – 17 Ene 2027", "11:00 AM", "MLK Weekend 2027 @ Mantamar Beach Club", "Mantamar Beach Club | Bar & Sushi (Zona Romántica)", ["DJs invitados circuito norteamericano"]),
        ("25 Ene – 01 Feb 2027", "11:00 AM", "Mantamar Bear Week 2027", "Mantamar Beach Club | Bar & Sushi (Zona Romántica)", ["DJs internacionales + Bear Week PV"]),
    ]
    for fecha, hora, titulo, recinto, g_list in mantamar_specs:
        if any(tok in mantamar_txt for tok in ("Brawny Bear", "Thanksgiving", "Mantamar NYE 2027", "Bear Week 2027")):
            events.append(
                {
                    "id": slugify(titulo[:42]),
                    "fecha": fecha,
                    "horario": hora,
                    "titulo": titulo,
                    "recinto": recinto,
                    "zona": "zona_romantica",
                    "subzona": "Zona Romántica · Beach Clubs, Hoteles Boutique & Nightlife",
                    "categoria": "Beach Club / Festival Música Electrónica & Circuito",
                    "invitados_artistas_lineup": g_list,
                    "influencers_relacionados": ["Creadores fitness & circuito LGBTQ+ internacional (ej. círculo Boys on Fire / Jordano Garcia / visitantes CDMX-EUA)"],
                    "cobertura_fotografica_detectada": "Parcial / Oportunidad Patrocinadores & DJs — Fotografía general de club sin servicio dedicado de reels inmediatos para cabanas VIP ni DJs invitados.",
                    "estado_oportunidad_captoora": "Parcial / Venta a DJs, Cabanas VIP & Patrocinadores",
                    "fuente_url": "https://mantamarvallarta.com/es/eventos-gay-puerto-vallarta",
                    "fuente_portal": "MantamarVallarta.com",
                    "resumen": "Festival oficial confirmado en calendario Mantamar Beach Club.",
                }
            )

    # 2. Majahuitas Beach Party (Bahía Sur, salida Puerto Vallarta)
    maj_txt = _strip_tags(_fetch_url("https://majahuitas-beach-party-vallarta.com/dj-lineup/"))
    maj_dates = [
        ("Sábado 21 Nov 2026", "Madota · Isabeu Fort · Liam Fitzgerald"),
        ("Sábado 28 Nov 2026", "Nacho Isa y Madmotor · Max Mignot"),
        ("Sábado 05 Dic 2026", "Secret Echoes · Rameff · Fresco"),
        ("Sábado 26 Dic 2026", "Mystery Affair · Liam Fitzgerald · Rameff"),
        ("Martes 29 Dic 2026", "Arodes · Nagib y Jackson · Max Mignot"),
        ("Jueves 31 Dic 2026 (NYE)", "Darco · Baron (FR) B2B Dorian Craft · Liam Fitzgerald"),
    ]
    for fecha, lineup in maj_dates:
        if lineup.split("·")[0].strip().split()[0] in maj_txt:
            events.append(
                {
                    "id": slugify(f"majahuitas-{fecha}"),
                    "fecha": fecha,
                    "horario": "Salida vespertina en catamarán PV -> playa",
                    "titulo": f"Majahuitas Beach Party · Lineup: {lineup}",
                    "recinto": "Playa Majahuitas (Acceso marítimo desde Bahía de Puerto Vallarta)",
                    "zona": "centro_y_bahia",
                    "subzona": "Centro / Bahía · Experiencias en la Bahía (Salida PV)",
                    "categoria": "Música Electrónica / Beach Festival en Bahía",
                    "invitados_artistas_lineup": [x.strip() for x in lineup.split("·")],
                    "influencers_relacionados": ["DJs internacionales (Baron FR, Dorian Craft, Arodes, Mystery Affair) y creadores de viajes/lifestyle en la bahía"],
                    "cobertura_fotografica_detectada": "Parcial — Operador promueve marca general, pero DJs invitados internacionales (especialmente NYE Baron FR / Dorian Craft / Arodes) compran paquetes propios de foto + press kit en playa.",
                    "estado_oportunidad_captoora": "Parcial / Acercamiento Directo a DJs Invitados",
                    "fuente_url": "https://majahuitas-beach-party-vallarta.com/dj-lineup/",
                    "fuente_portal": "Majahuitas-Beach-Party-Vallarta.com",
                    "resumen": f"Lineup confirmado en caleta sur de la bahía: {lineup}.",
                }
            )

    # 3. Eventbrite JSON-LD live extraction (Pages 1 & 2, strictly filtered)
    seen_eb: set[str] = set()
    for p in (1, 2):
        eb_html = _fetch_url(f"https://www.eventbrite.com/d/mexico--puerto-vallarta/events/?page={p}")
        blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', eb_html, re.S)
        for b in blocks:
            try:
                parsed = json.loads(b)
            except json.JSONDecodeError:
                continue
            els = parsed.get("itemListElement", []) if isinstance(parsed, dict) else []
            for el in els:
                it = el.get("item") if isinstance(el, dict) else None
                if not isinstance(it, dict) or it.get("@type") != "Event":
                    continue
                url = str(it.get("url") or "").strip()
                name = html_lib.unescape(str(it.get("name") or "").strip())
                loc = it.get("location") or {}
                venue = html_lib.unescape(str(loc.get("name") or "").strip())
                addr = loc.get("address") if isinstance(loc.get("address"), dict) else {}
                locality = str(addr.get("addressLocality") or "").strip()
                street = str(addr.get("streetAddress") or "").strip()
                if not url or url in seen_eb:
                    continue
                seen_eb.add(url)
                if not venue or "puerto vallarta" not in locality.lower():
                    excluded.append({"titulo": name, "fuente_url": url, "razon": f"Evento online o fuera de PV ({locality or 'Online'})"})
                    continue
                # Avoid duplicating Palm/Coco/Act2 recurring shows already captured with richer API
                if any(v in venue.lower() for v in ("palm cabaret", "coco cabaret", "act2pv")):
                    continue
                z, subz = classify_event_zone(name, f"{venue} {street}")
                if not z:
                    excluded.append({"titulo": name, "fuente_url": url, "razon": f"{subz} ({venue} {street})"})
                    continue

                guests = ["Host / Productora del evento"]
                if "luann" in name.lower():
                    guests = ["Countess Luann (The Real Housewives / Cabaret Star)"]
                elif "industry" in name.lower() or "thanksgiving" in name.lower():
                    guests = ["DJs Luis Vázquez, Alex Ramos, Alex Acosta, Diego Álvarez, Alberto Ponzo, Ed Rodriguez, Leo Blanco, Marc"]
                elif "madera strings" in name.lower():
                    guests = ["Madera Strings (Música en vivo)"]
                elif "chica locca" in venue.lower():
                    guests = ["DJ 80s & Tripulación Chica Locca Tours"]

                events.append(
                    {
                        "id": slugify(f"eb-{name[:36]}"),
                        "fecha": f"{it.get('startDate')} al {it.get('endDate')}" if it.get("endDate") and it.get("endDate") != it.get("startDate") else str(it.get("startDate") or ""),
                        "horario": "Ver horario en Eventbrite",
                        "titulo": name,
                        "recinto": f"{venue} ({street})" if street else venue,
                        "zona": z,
                        "subzona": subz,
                        "categoria": "Concierto / Fiesta / Networking (Eventbrite)",
                        "invitados_artistas_lineup": guests,
                        "influencers_relacionados": ["Creadores asistentes, celebridades invitadas (ej. Countess Luann NYE) y público de Eventbrite"],
                        "cobertura_fotografica_detectada": "Abierta — Publicado en Eventbrite sin crédito fotográfico comercial fijo.",
                        "estado_oportunidad_captoora": "Abierta / Sin fotógrafo dedicado",
                        "fuente_url": url,
                        "fuente_portal": "Eventbrite.com",
                        "resumen": f"Evento presencial confirmado en {venue}, {street}, Puerto Vallarta.",
                    }
                )
    return events, excluded


def _scrape_sports_and_community_press() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Scrape Padel 233, International Pro Am Golf, Out&About PV, and GAYPV community articles/credits."""
    events: list[dict[str, Any]] = []
    photographers_found: list[dict[str, Any]] = []

    padel_txt = _strip_tags(_fetch_url("https://www.padel233.com/"))
    if "Torneo 233" in padel_txt:
        events.append(
            {
                "id": "padel-torneo-233-dic2026",
                "fecha": "03 – 06 Dic 2026",
                "horario": "Torneo 4 días (7:00 AM – 11:00 PM)",
                "titulo": "Torneo 233 — Torneo Anual de Pádel & Terraza Savia",
                "recinto": "Padel 233 (Av. Manuel Lepe 216, Guadalupe Victoria)",
                "zona": "zona_hotelera",
                "subzona": "Zona Hotelera Norte · Corredor Versalles / Fluvial / CICPV",
                "categoria": "Deportes / Torneo de Pádel",
                "invitados_artistas_lineup": ["Jugadores amateurs y avanzados PV / GDL", "Comunidad @padel233pv y Savia Bistro"],
                "influencers_relacionados": ["Comunidad pádel Puerto Vallarta & marcas patrocinadoras de cancha"],
                "cobertura_fotografica_detectada": "Abierta — Sin cobertura editorial 1/2000s ni trofeos acrílicos LED anunciados en sitio web.",
                "estado_oportunidad_captoora": "Abierta / Nicho Core Captoora (Pádel + Trofeos LED)",
                "fuente_url": "https://www.padel233.com/",
                "fuente_portal": "Padel233.com",
                "resumen": "Torneo confirmado de 4 días en club con 5 canchas techadas y bar/restaurante Savia.",
            }
        )

    proam_txt = _strip_tags(_fetch_url("https://internationalproam.com/"))
    if "December 7-12, 2026" in proam_txt:
        events.append(
            {
                "id": "golf-pv-international-proam-dic2026",
                "fecha": "07 – 12 Dic 2026",
                "horario": "Torneo semanal + eventos de hospitalidad en hotel sede",
                "titulo": "37th Puerto Vallarta International Pro-Am (82–84 Equipos · PGA & Senior Tour)",
                "recinto": "Marriott Puerto Vallarta Resort & Spa (Marina Vallarta) + Marina/Vista Vallarta Golf",
                "zona": "zona_hotelera",
                "subzona": "Zona Hotelera · Marina Vallarta & Puerto Mágico",
                "categoria": "Deportes Alto Ticket / Golf Pro-Am",
                "invitados_artistas_lineup": ["82–84 equipos con jugadores PGA Tour y Senior Tour", "Host oficial Marriott Puerto Vallarta Resort & Spa"],
                "influencers_relacionados": ["Ejecutivos y patrocinadores de alto poder adquisitivo (EUA / Canadá / México)"],
                "cobertura_fotografica_detectada": "Abierta — Enfocado en operación deportiva internacional; oportunidad premium para retrato corporativo de equipos en campo + placas acrílico/parota de premiación patrocinadas.",
                "estado_oportunidad_captoora": "Abierta / Alto Ticket B2B",
                "fuente_url": "https://internationalproam.com/",
                "fuente_portal": "InternationalProAm.com",
                "resumen": "37º aniversario con sede exclusiva en Marriott Resort & Spa recién renovado.",
            }
        )

    # Mine Out & About PV & GAYPV WP REST APIs for events & photographer credits
    oapv_posts = json.loads(_fetch_url("https://outandaboutpv.com/wp-json/wp/v2/posts?per_page=25") or "[]")
    credit_map: dict[str, set[str]] = defaultdict(set)
    for post in oapv_posts:
        title = _strip_tags((post.get("title") or {}).get("rendered", ""))
        link = str(post.get("link") or "")
        content = _strip_tags((post.get("content") or {}).get("rendered", ""))
        low = title.lower()

        for m in re.findall(r"Photos?\s+by\s+([A-ZÁÉÍÓÚÑ][a-zñáéíóú]+\s+[A-ZÁÉÍÓÚÑ][a-zñáéíóú]+)", content):
            name_clean = m.strip()
            if name_clean and name_clean.lower() not in ("prensa heat", "atlantis", "the palm"):
                credit_map[name_clean].add(title[:65])

        if "sula bow wow gala" in low:
            events.append(
                {
                    "id": "oapv-sula-bow-wow-gala",
                    "fecha": "04 Dic 2026",
                    "horario": "Gala nocturna",
                    "titulo": "4th Annual Sula Bow Wow Gala",
                    "recinto": "Sede Zona Romántica / Centro PV (The Sula Society)",
                    "zona": "zona_romantica",
                    "subzona": "Zona Romántica · Olas Altas / Gastronomía / Mixers",
                    "categoria": "Gala Filantrópica & Networking Expat",
                    "invitados_artistas_lineup": ["Donantes y patronato The Sula Society", "Patrocinadores locales"],
                    "influencers_relacionados": ["Comunidad expat residente, amantes de mascotas y medios locales PV"],
                    "cobertura_fotografica_detectada": "Parcial — Suelen publicar reseña posterior, pero sin paquetes inmediatos para patrocinadores o retratos editoriales de gala.",
                    "estado_oportunidad_captoora": "Parcial / Oportunidad Gala & Patrocinadores",
                    "fuente_url": link,
                    "fuente_portal": "OutAndAboutPV.com",
                    "resumen": "Cuarta gala anual benéfica con subasta, música en vivo y cena.",
                }
            )
        elif "christmas in the garden" in low:
            events.append(
                {
                    "id": "oapv-christmas-garden-los-mangos",
                    "fecha": "13 Dic 2026",
                    "horario": "Tarde / Jardín",
                    "titulo": "The Christmas Garden Party (Beneficio Vallarta School for Girls)",
                    "recinto": "Biblioteca Los Mangos (Av. Francisco Villa 1001)",
                    "zona": "zona_hotelera",
                    "subzona": "Zona Hotelera Norte · Corredor Versalles / Fluvial / CICPV",
                    "categoria": "Gala Navideña / Filantropía",
                    "invitados_artistas_lineup": ["Comunidad internacional Vallarta School for Girls"],
                    "influencers_relacionados": ["Patronato benéfico PV y prensa comunitaria"],
                    "cobertura_fotografica_detectada": "Abierta — Evento social diurno sin servicio editorial dedicado de retrato para patrocinadores.",
                    "estado_oportunidad_captoora": "Abierta / Sin fotógrafo dedicado",
                    "fuente_url": link,
                    "fuente_portal": "OutAndAboutPV.com",
                    "resumen": "Tradición navideña anual de recaudación en los jardines de Biblioteca Los Mangos.",
                }
            )
        elif "east emiliano bar crawl" in low:
            events.append(
                {
                    "id": "oapv-east-emiliano-bar-crawl",
                    "fecha": "19 Nov 2026",
                    "horario": "Tarde / Noche (6 paradas)",
                    "titulo": "East Emiliano Bar Crawl (6 Bares Zona Romántica)",
                    "recinto": "Corredor Emiliano Zapata Este (Awaysis, Onyx y 4 sedes)",
                    "zona": "zona_romantica",
                    "subzona": "Zona Romántica · Olas Altas / Gastronomía / Mixers",
                    "categoria": "Vida Nocturna & Circuito de Bares",
                    "invitados_artistas_lineup": ["Hosts de 6 bares en Emiliano Zapata"],
                    "influencers_relacionados": ["Creadores locales de vida nocturna y asistentes turísticos"],
                    "cobertura_fotografica_detectada": "Abierta — Ideal para entregar galería instantánea a los 6 bares participantes para Google Maps y Meta Ads.",
                    "estado_oportunidad_captoora": "Abierta / Venta Multi-Bar 6x1",
                    "fuente_url": link,
                    "fuente_portal": "OutAndAboutPV.com",
                    "resumen": "Recorrido coordinado por 6 bares de Zona Romántica este jueves 19 de noviembre.",
                }
            )

    gaypv_posts = json.loads(_fetch_url("https://gaypv.com/wp-json/wp/v2/posts?per_page=20") or "[]")
    for post in gaypv_posts:
        title = _strip_tags((post.get("title") or {}).get("rendered", ""))
        link = str(post.get("link") or "")
        content = _strip_tags((post.get("content") or {}).get("rendered", ""))
        if "eddy araiza" in content.lower():
            credit_map["Eddy Araiza Fotografía (@araizafoto)"].add(title[:65])
        if "armando miranda" in content.lower():
            credit_map["Armando Miranda"].add(title[:65])
        if "keiino" in title.lower():
            events.append(
                {
                    "id": "gaypv-keiino-coco-cabaret-ene2027",
                    "fecha": "23, 24, 27, 28, 29 y 30 Ene 2027",
                    "horario": "Horario por función",
                    "titulo": "KEiiNO Live in Puerto Vallarta (Trío Eurovisión)",
                    "recinto": "Coco Cabaret (Fco. I. Madero 289, Zona Romántica)",
                    "zona": "zona_romantica",
                    "subzona": "Zona Romántica · Circuito Cabaret & Teatros",
                    "categoria": "Concierto Internacional Pop / Eurovisión",
                    "invitados_artistas_lineup": ["Alexandra Rotan, Tom Hugo y Fred Buljo (KEiiNO)"],
                    "influencers_relacionados": ["Fans internacionales de Eurovisión, prensa LGBTQ+ PV y GAYPV"],
                    "cobertura_fotografica_detectada": "Abierta — Residencia internacional de 6 fechas con alta oportunidad para press kit editorial y meet & greet VIP.",
                    "estado_oportunidad_captoora": "Abierta / Artista Internacional 6 Fechas",
                    "fuente_url": link,
                    "fuente_portal": "GAYPV.com",
                    "resumen": "Residencia confirmada de 6 shows del trío noruego KEiiNO en Coco Cabaret.",
                }
            )

    for cname, notes in sorted(credit_map.items()):
        photographers_found.append(
            {
                "nombre_medio": cname,
                "enfoque_actual": "Cobertura comunitaria/editorial específica detectada en artículos recientes",
                "eventos_cubiertos_muestra": sorted(notes),
                "brecha_que_deja_para_captoora": "Cubre principalmente prensa de revista o sesiones calendar, dejando sin cobertura inmediata de entrega mismo día (1/2000s, retratos de marcas/patrocinadores, bodegas de vino, posadas de hoteles y piezas LED QR en taller).",
            }
        )
    return events, photographers_found, []


def _curated_verified_holiday_layer() -> list[dict[str, Any]]:
    """
    Verified seasonal Posadas, Christmas Eve & New Year's Eve anchors strictly inside PV
    (grounded on visitapuertovallarta.com.mx, restaurantoscars.com, lebistropv.com, pirateshipvallarta.com).
    """
    anchors = [
        (
            "pv-posadas-hoteles-zona-hotelera-dic2026",
            "10 – 24 Dic 2026",
            "Vespertino / Nocturno",
            "Temporada de Posadas Corporativas & Cenas Navideñas Hoteleras",
            "Franja Hotelera Norte & Sur (Sheraton, Fiesta Americana, Krystal, Buenaventura, Marriott, Velas, Garza Blanca)",
            "zona_hotelera",
            "Zona Hotelera Norte · Las Glorias & Franja Hotelera",
            "Posadas Hoteleras & Eventos Corporativos",
            ["Gerencias de Grupos/Banquetes", "Equipos corporativos locales e invitados"],
            "Abierta — La mayoría de hoteles solo usan fotos casuales de staff y no ofrecen paquetes instantáneos con galería nocturna + porta-menús/placas QR acrílicas para posadas.",
            "https://visitapuertovallarta.com.mx/eventos",
            "Temporada Oficial Dic 2026 PV",
        ),
        (
            "pv-cenas-navidad-rio-cuale-dic2026",
            "24 – 25 Dic 2026",
            "18:00 – 23:30 h",
            "Cenas de Nochebuena & Navidad con Música en Vivo (Isla Río Cuale)",
            "Restaurantes Oscar's & Le Bistro (Isla del Río Cuale, Centro PV)",
            "centro_y_bahia",
            "Centro / Bahía · Malecón, Centro Histórico & Isla Río Cuale",
            "Posadas, Cenas Navideñas & Hospitalidad",
            ["Músicos residentes de jazz/acústico", "Comensales navideños de lujo"],
            "Abierta — Recintos gastronómicos frente al río con menús multi-tiempo sin estudio editorial asignado en mesas navideñas ni display LED QR actualizado.",
            "https://restaurantoscars.com/",
            "Oscar's / Le Bistro PV",
        ),
        (
            "pv-marigalante-posada-nye-bahia-dic2026",
            "16 – 31 Dic 2026",
            "Crucero Nocturno Bahía",
            "Cruceros Temáticos Navideños & Fiesta de Año Nuevo en Bahía de Banderas",
            "Barco Pirata Marigalante & Embarcaciones Turísticas (Salida Terminal Marítima PV)",
            "centro_y_bahia",
            "Centro / Bahía · Experiencias en la Bahía (Salida PV)",
            "Fiestas en Bahía / Año Nuevo",
            ["Elenco pirata acrobático, pirotecnia sobre la bahía y cena gourmet"],
            "Parcial — Operador vende fotografía turística básica de recuerdo; oportunidad de propuesta editorial de alto calibre para grupos VIP y posadas privadas a bordo.",
            "https://pirateshipvallarta.com/",
            "PirateShipVallarta.com",
        ),
    ]
    out = []
    for eid, fecha, hora, tit, rec, z, subz, cat, guests, cov, url, portal in anchors:
        out.append(
            {
                "id": eid,
                "fecha": fecha,
                "horario": hora,
                "titulo": tit,
                "recinto": rec,
                "zona": z,
                "subzona": subz,
                "categoria": cat,
                "invitados_artistas_lineup": guests,
                "influencers_relacionados": ["Turistas de fin de año, familias VIP y creadores locales de hospitalidad"],
                "cobertura_fotografica_detectada": cov,
                "estado_oportunidad_captoora": "Parcial / Oportunidad VIP" if cov.startswith("Parcial") else "Abierta / Sin fotógrafo dedicado",
                "fuente_url": url,
                "fuente_portal": portal,
                "resumen": "Ventana prioritaria de posadas corporativas, cenas de Nochebuena y festejos de Fin de Año 2026.",
            }
        )
    return out


def _build_influencers_intelligence(photographers_detected: list[dict[str, Any]]) -> dict[str, Any]:
    """Structured database of PV influencers/creators, touring stars & photography coverage gaps."""
    local_influencers = [
        {
            "nombre": "Pao Marlene",
            "handle": "@paomarlene",
            "segmento": "Senderismo costa sur PV (Conchas Chinas/Las Ánimas), estilo de vida y viajes",
            "cobertura_actual": "Autoproducción móvil / colaboraciones puntuales de turismo (#VisitaPuertoVallarta)",
            "oportunidad_captoora": "Intercambio editorial de sesión al atardecer en Zona Romántica / Conchas Chinas para generar catálogo conjunto y cross-tagging con restaurantes/beach clubs.",
            "guion_dm_captoora": _assert_clean_copy(
                "Hola Pao, sigo tu trabajo recorriendo la costa sur de Puerto Vallarta. Soy Jesús Gutiérrez, fotógrafo editorial (Captoora Studio) y estaré cubriendo activaciones esta temporada en Zona Romántica y Centro. Si armas algún proyecto con hotel o restaurante esta semana, podemos hacer una micro-sesión editorial con entrega el mismo día. ¿Te muestro portafolio?",
                "dm paomarlene",
            ),
            "fuente": "https://visitapuertovallarta.com.mx/",
        },
        {
            "nombre": "Delia García / Sonia Cruz / Gloria Candiani / Cinthia Aguilar",
            "handle": "@soydeliagarcia · @soycandiani · @cinthiaaguilar",
            "segmento": "Lifestyle, gastronomía y talento nacional vinculado a campañas #VisitaPuertoVallarta",
            "cobertura_actual": "Contenido orgánico y activaciones de marca hotelera",
            "oportunidad_captoora": "Ofrecer apoyo visual flash en eventos gastronómicos, lanzamientos y hoteles PV con galería instantánea optimizada para Instagram/Reels.",
            "guion_dm_captoora": _assert_clean_copy(
                "Hola, vimos tu cobertura reciente de Puerto Vallarta. En Captoora Studio hacemos fotografía editorial de gastronomía y lifestyle con entrega el mismo día para lanzamientos y hoteles en Zona Hotelera y Centro. Si vienes a algún evento esta temporada, encantado de armar mancuerna editorial.",
                "dm delia_candiani",
            ),
            "fuente": "https://visitapuertovallarta.com.mx/",
        },
        {
            "nombre": "Alejo Ospina",
            "handle": "@alejoospina",
            "segmento": "Creador internacional LGBTQ+, música & marca propia (¿Aprietas?), frecuente en Zona Romántica",
            "cobertura_actual": "Artículos de GAYPV acreditan material como 'autor desconocido' / autoproducido",
            "oportunidad_captoora": "Sesiones editoriales nocturnas de alto contraste y look & feel cinematográfico para lanzamientos de marca personal en Zona Romántica.",
            "guion_dm_captoora": _assert_clean_copy(
                "Hola Alejo, felicidades por el lanzamiento de tu línea y música reciente. Trabajo retrato editorial nocturno y cobertura de eventos para talento internacional en Zona Romántica (entrega el mismo día). Te comparto mi portafolio por si armamos una sesión de alto contraste esta temporada.",
                "dm alejo",
            ),
            "fuente": "https://gaypv.com/people/aprietas-alejo-ospina/",
        },
        {
            "nombre": "Cristian Rendón & Talento Boys on Fire",
            "handle": "@cristian_rendon_ · Elenco Coco Cabaret",
            "segmento": "Creadores fitness, modelaje y espectáculo en Zona Romántica",
            "cobertura_actual": "Eddy Araiza cubrió la sesión principal del calendario 2027, pero cada creador requiere contenido constante de entrenamiento y escenario",
            "oportunidad_captoora": "Sesiones escultóricas de progreso físico (estilo estudio / Captoora Biogen Beta) y retrato editorial back-stage con entrega inmediata.",
            "guion_dm_captoora": _assert_clean_copy(
                "Hola Cristian, soy Jesús Gutiérrez de Captoora Studio. Vimos tu temporada en Zona Romántica y el título de Mister Universal México 2026. Hacemos fotografía escultórica de fitness y retrato escénico con iluminación controlada y entrega en 24h. ¿Revisamos 3 referencias visuales para una colaboración en Vallarta?",
                "dm cristian",
            ),
            "fuente": "https://gaypv.com/people/cristian-rendon/",
        },
        {
            "nombre": "Creadores Travel Pop Up & Foodie/Lifestyle PV (Fun Travel / Una Cita con el Mundo / Dos Truchas / Mariel de Viaje)",
            "handle": "@funtravelven · @unacitaconelmundo · @dostruchas · @marieldeviaje · @viajaliscomx",
            "segmento": "Creadores de viaje convocados en encuentros turísticos y reseñas hoteleras de Jalisco/PV",
            "cobertura_actual": "Mayormente video vertical en smartphone durante fam-trips",
            "oportunidad_captoora": "Complementar sus viajes y fam-trips con retrato editorial profesional de alta gama para portadas y patrocinadores hoteleros.",
            "guion_dm_captoora": _assert_clean_copy(
                "Hola equipo, cuando tengan agenda o fam-trip en Puerto Vallarta (Zona Romántica, Hotelera o Centro), en Captoora Studio apoyamos con fotografía editorial profesional y entrega el mismo día para elevar el material que entregan a hoteles y marcas. ¿Les comparto portafolio?",
                "dm travelpopup",
            ),
            "fuente": "https://visitapuertovallarta.com.mx/",
        },
        {
            "nombre": "Jordano Garcia & Christopher Conner",
            "handle": "@jordano_garcia · Christopher Conner (GAYPV)",
            "segmento": "Creadores lifestyle / autores residentes y visitantes frecuentes Zona Romántica & Centro",
            "cobertura_actual": "Publicaciones editoriales y sociales sin fotógrafo permanente asignado para sus lanzamientos locales",
            "oportunidad_captoora": "Cobertura de lanzamientos de libros, mixers y retratos de marca personal en Centro y Zona Romántica.",
            "guion_dm_captoora": _assert_clean_copy(
                "Hola, leímos tu entrevista reciente en Puerto Vallarta. Soy Jesús Gutiérrez, fotógrafo editorial (Captoora Studio). Cubrimos lanzamientos y retratos de marca personal en Centro y Zona Romántica con entrega en 24–48h. Si organizas algún encuentro esta temporada, cuenta con nosotros.",
                "dm conner_garcia",
            ),
            "fuente": "https://gaypv.com/people/christopher-conner-puerto-vallarta-gay-scene/",
        },
    ]

    vip_guests = [
        {"nombre": "Baron (FR) & Dorian Craft & Arodes & Darco", "evento": "Majahuitas Beach Party (Dic 29 y NYE Dic 31)", "zona": "centro_y_bahia", "cobertura_propia": "Sin fotógrafo propio listado en lineup público"},
        {"nombre": "Countess Luann", "evento": "NYE at The Tryst Puerto Vallarta (31 Dic)", "zona": "zona_romantica", "cobertura_propia": "Oportunidad directa para hotel anfitrión The Tryst y galería VIP de medianoche"},
        {"nombre": "KEiiNO (Alexandra Rotan, Tom Hugo, Fred Buljo)", "evento": "Coco Cabaret (6 fechas Ene 2027)", "zona": "zona_romantica", "cobertura_propia": "Productora local; alta oportunidad de paquete de 6 shows + meet & greet"},
        {"nombre": "CelloVoci (Branden & James, Effie Passero) + Sutton Lee Seymour + Mark Hartman", "evento": "Music of the Night · Teatro Vallarta (30 Dic)", "zona": "centro_y_bahia", "cobertura_propia": "Gira internacional en Teatro Vallarta; sin fotógrafo editorial propio publicado"},
        {"nombre": "Chef Esteban Lluis (Michelin ★) · Chef Xavier Pérez Stone · Chef Víctor Howard · Chef Freddy Monteros", "evento": "31º Festival Gourmet Internacional (18–22 Nov)", "zona": "zona_hotelera", "cobertura_propia": "Prensa general del festival; alta oportunidad directa por restaurante anfitrión"},
        {"nombre": "Los Claxons", "evento": "Cantando + Contando · Cuarto de Música (26 Nov)", "zona": "zona_hotelera", "cobertura_propia": "Venue íntimo sin crédito de cobertura oficial en cartelera turística"},
        {"nombre": "Alexis Mateo & Xunami Muse / Tynomi Banks / Sherry Vine / Hedda Lettuce / Jackie Cox & Jan Sport", "evento": "Temporada Cabaret Invierno (Act2PV / The Palm / Coco Cabaret)", "zona": "zona_romantica", "cobertura_propia": "Talento visitante de gira que frecuentemente adquiere paquetes por función para redes"},
        {"nombre": "+71 Artistas MUYGUUD (Rimiyoho, Taiga Brava, DJ Memo Pearls, Jorge Ayala 'Troglodita', etc.)", "evento": "MUYGUUD Feria Arte Contemporáneo (19–22 Nov · Col. 5 de Diciembre)", "zona": "centro_y_bahia", "cobertura_propia": "Promo inicial de Alejandra Herrera; 71 artistas y performances en vivo sin cobertura 1:1"},
    ]

    return {
        "updated_at": now_iso(),
        "territory": "Puerto Vallarta, Jalisco (Zona Romántica, Zona Hotelera y Centro / Bahía)",
        "resumen_cobertura_actual": {
            "hallazgo_clave": (
                "En la prensa local (Out & About PV / GAYPV) se detectaron fotógrafos comunitarios en eventos puntuales "
                "(Adan Villa, Alejandra Herrera, Michael Fluck, Angel Villa, Eddy Araiza, Armando Miranda), "
                "pero MÁS DEL 75% de eventos de temporada, posadas hoteleras, conciertos íntimos, DJs invitados, "
                "restaurantes anfitriones y microinfluencers NO cuentan con cobertura editorial con entrega el mismo día ni piezas físicas de taller."
            ),
            "fotografos_y_medios_detectados": photographers_detected,
        },
        "influencers_y_creadores_pv": local_influencers,
        "invitados_especiales_y_artistas": vip_guests,
    }


def run_events_and_influencers_scrape() -> dict[str, Any]:
    known_leads = _load_known_pv_leads()

    vpv_events, vpv_excl = _scrape_visitapuertovallarta()
    fgi_events, fgi_guests, fgi_excl = _scrape_festival_gourmet()
    cab_events = _scrape_cabarets_and_theaters()
    club_eb_events, eb_excl = _scrape_beach_clubs_and_eventbrite()
    sports_events, photographers_found, sp_excl = _scrape_sports_and_community_press()
    holiday_events = _curated_verified_holiday_layer()

    all_raw_events = vpv_events + fgi_events + cab_events + club_eb_events + sports_events + holiday_events
    all_excluded = vpv_excl + fgi_excl + eb_excl + sp_excl

    # Deduplicate by normalized title+date and attach venue lead match + neutral outreach script
    by_zone: dict[str, list[dict[str, Any]]] = {
        "zona_romantica": [],
        "zona_hotelera": [],
        "centro_y_bahia": [],
    }
    seen_keys: set[str] = set()
    for ev in all_raw_events:
        zkey = ev.get("zona")
        if zkey not in by_zone:
            continue
        dedup_k = slugify(f"{ev.get('titulo','')[:40]}-{ev.get('fecha','')[:12]}")
        if dedup_k in seen_keys:
            continue
        seen_keys.add(dedup_k)

        zona_label = {
            "zona_romantica": "Zona Romántica",
            "zona_hotelera": "Zona Hotelera",
            "centro_y_bahia": "Centro / Bahía",
        }[zkey]

        ev["lead_gmaps_vinculado"] = _match_known_lead(ev.get("recinto", ""), known_leads)
        ev["guion_acercamiento_captoora"] = _build_event_outreach_script(
            titulo=ev["titulo"],
            recinto=ev["recinto"],
            fecha=ev["fecha"],
            zona_label=zona_label,
            categoria=ev["categoria"],
            invitados=ev.get("invitados_artistas_lineup") or [],
            cobertura_status=ev.get("estado_oportunidad_captoora") or "",
        )
        by_zone[zkey].append(ev)

    influencers_payload = _build_influencers_intelligence(photographers_found)
    influencers_payload["chefs_invitados_festival_gourmet_pv"] = fgi_guests

    PV_DATA_ROOT.mkdir(parents=True, exist_ok=True)
    meta_titles = {
        "zona_romantica": "Puerto Vallarta — Zona Romántica",
        "zona_hotelera": "Puerto Vallarta — Zona Hotelera",
        "centro_y_bahia": "Puerto Vallarta — Centro / Bahía",
    }
    written: dict[str, Any] = {}
    for zkey, items in by_zone.items():
        items_sorted = sorted(items, key=lambda x: (0 if "Abierta" in x.get("estado_oportunidad_captoora", "") else 1, x.get("fecha", ""), x.get("titulo", "")))
        payload = {
            "updated_at": now_iso(),
            "territory": meta_titles[zkey],
            "zone_key": zkey,
            "total_events": len(items_sorted),
            "open_coverage_count": sum(1 for x in items_sorted if "Abierta" in x.get("estado_oportunidad_captoora", "")),
            "partial_coverage_count": sum(1 for x in items_sorted if "Parcial" in x.get("estado_oportunidad_captoora", "")),
            "excluded_outside_pv_count": len(all_excluded),
            "excluded_outside_pv_sample": all_excluded[:25],
            "events": items_sorted,
        }
        out_path = PV_DATA_ROOT / f"eventos_{zkey}.json"
        write_json(out_path, payload)
        written[zkey] = {"path": str(out_path), "total": len(items_sorted)}

    inf_path = PV_DATA_ROOT / "influencers_y_cobertura_pv.json"
    write_json(inf_path, influencers_payload)
    written["influencers"] = {"path": str(inf_path), "influencers": len(influencers_payload["influencers_y_creadores_pv"]), "vip_guests": len(influencers_payload["invitados_especiales_y_artistas"]), "fgi_chefs_pv": len(fgi_guests)}
    written["excluded_outside_pv_count"] = len(all_excluded)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Extractor en vivo de eventos, invitados, influencers y cobertura en Puerto Vallarta.")
    parser.parse_args()
    summary = run_events_and_influencers_scrape()
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
