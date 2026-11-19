"""Visual Google Maps Business Profile Auditor (Apify metadata + Chrome CDP captures)."""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import re
import shutil
import socket
import subprocess
import tempfile
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import httpx
import websockets

from . import ROOT_DIR
from .config import FILES, append_agent_event, now_iso, read_json, slugify, validate_client_copy, write_json
from .mockups import CHROME_BIN, resolve_niche_profile

GMAPS_AUDITS_DIR = ROOT_DIR / "assets" / "gmaps_audits"
RAW_APIFY_PATH = ROOT_DIR / "dashboard" / "data" / "apify_dataset_raw.json"

DESKTOP_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

SOCIAL_OR_FREE_DOMAINS = (
    "m.facebook.com",
    "facebook.com",
    "instagram.com",
    "wixsite.com",
    "linktr.ee",
    "wa.me",
)

FLAG_CLIENT_OBSERVATIONS = {
    "CARRITO STREET VIEW": (
        "Tu portada actual en Google Maps muestra la vista automática de calle (Street View) en lugar "
        "de una toma cuidada de tu fachada, instalaciones y equipo."
    ),
    "0 FOTOS": (
        "Tu perfil de Google Maps aún aparece sin galería fotográfica curada que proyecte la calidad "
        "real de tus servicios."
    ),
    "<=5 FOTOS": (
        "Tu galería actual muestra pocas fotografías (5 o menos); sumar 15–30 imágenes editoriales eleva "
        "la confianza de clientes nuevos desde la primera búsqueda."
    ),
    "SIN RECLAMAR": (
        "La ficha aún muestra el aviso 'Reclamar este negocio': completamos contigo la verificación oficial "
        "para proteger tu marca, horarios y portada."
    ),
    "SIN SITIO WEB": (
        "La ficha no enlaza todavía a un sitio web o catálogo comercial propio para convertir búsquedas en citas o ventas."
    ),
    "RED PERSONAL EN RIESGO": (
        "Tu enlace apunta a una red social o página personal; migrar a un Meta Business Portfolio oficial "
        "y catálogo unificado evita interrupciones o bloqueos de cuenta al crecer tus ventas."
    ),
    "SIN TELÉFONO": (
        "Tu perfil aún muestra la invitación de 'Agregar número de teléfono': dejamos verificados tu teléfono "
        "y botón directo a WhatsApp Business."
    ),
    "POCAS RESEÑAS": (
        "Incluimos placa acrílica con QR de mostrador para acelerar reseñas verificadas en Google Maps 2027."
    ),
}


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def analyze_business_profile(item: dict[str, Any]) -> dict[str, Any]:
    """Compute internal triage flags, severity score, and respectful client observations."""
    name = str(item.get("nombre") or item.get("title") or "").strip()
    category = str(item.get("categoria") or item.get("categoryName") or "Negocio Local").strip()
    address = str(item.get("direccion") or item.get("address") or "San Pedro Garza García / Monterrey, N.L.").strip()
    phone = str(item.get("telefono") or item.get("phone") or "").strip()
    website = str(item.get("sitio_web") or item.get("website") or "").strip()
    gmaps_url = str(item.get("gmaps_url") or item.get("url") or "").strip()
    place_id = str(item.get("place_id") or item.get("placeId") or "").strip()
    image_url = str(item.get("image_url") or item.get("imageUrl") or "").strip()

    raw_imgs_count = item.get("images_count") if "images_count" in item else item.get("imagesCount")
    images_count = int(raw_imgs_count) if raw_imgs_count is not None else None
    claim_flag = bool(item.get("claim_this_business") if "claim_this_business" in item else item.get("claimThisBusiness"))
    reviews = int(item.get("resenas") if "resenas" in item else (item.get("reviewsCount") or 0))
    rating = item.get("rating") if "rating" in item else item.get("totalScore")

    flags: list[str] = []
    score = 0

    if "streetviewpixels" in image_url.lower() or "streetview" in image_url.lower():
        flags.append("CARRITO STREET VIEW")
        score += 32

    if images_count is not None:
        if images_count == 0:
            flags.append("0 FOTOS")
            score += 35
        elif images_count <= 5:
            flags.append("<=5 FOTOS")
            score += 22

    if claim_flag:
        flags.append("SIN RECLAMAR")
        score += 26

    if not website or "google.com/maps" in website.lower():
        flags.append("SIN SITIO WEB")
        score += 18
    elif any(dom in website.lower() for dom in SOCIAL_OR_FREE_DOMAINS):
        flags.append("RED PERSONAL EN RIESGO")
        score += 15

    if not phone:
        flags.append("SIN TELÉFONO")
        score += 12

    if reviews < 10:
        flags.append("POCAS RESEÑAS")
        score += 6

    score = min(100, score)
    target_url = build_maps_target_url(
        {"nombre": name, "direccion": address, "gmaps_url": gmaps_url, "place_id": place_id}
    )
    observations = [FLAG_CLIENT_OBSERVATIONS[f] for f in flags if f in FLAG_CLIENT_OBSERVATIONS]

    lat_val = item.get("lat")
    lng_val = item.get("lng")
    if (lat_val is None or lng_val is None) and isinstance(item.get("location"), dict):
        lat_val = item["location"].get("lat")
        lng_val = item["location"].get("lng")

    municipio = str(item.get("municipio") or _infer_municipality(address, lat=lat_val, lng=lng_val)).strip()
    zona = str(item.get("zona") or _infer_zone(address, lat=lat_val, lng=lng_val, municipio=municipio)).strip()

    return {
        "slug": slugify(name),
        "nombre": name,
        "categoria": category,
        "direccion": address,
        "municipio": municipio,
        "zona": zona,
        "subzona": str(item.get("subzona") or "").strip(),
        "lat": lat_val,
        "lng": lng_val,
        "nicho": str(item.get("nicho") or _infer_niche(name, category)),
        "telefono": phone,
        "sitio_web": website or target_url,
        "gmaps_url": target_url,
        "place_id": place_id,
        "image_url": image_url,
        "images_count": images_count,
        "claim_this_business": claim_flag,
        "has_streetview_cover": "CARRITO STREET VIEW" in flags,
        "rating": rating,
        "resenas": reviews,
        "audit_flags": flags,
        "audit_score": score,
        "client_observations": observations,
    }


def _infer_municipality(address: str, *, lat: float | None = None, lng: float | None = None) -> str:
    low = (address or "").lower()
    if any(
        k in low
        for k in (
            "puerto vallarta",
            "zona romántica",
            "zona romantica",
            "emiliano zapata",
            "olas altas",
            "las glorias",
            "zona hotelera",
            "conchas chinas",
            "marina vallarta",
            "48380",
            "48333",
            "48330",
            "48310",
            "48390",
        )
    ):
        return "Puerto Vallarta"
    if lat is not None and lng is not None and 20.50 <= float(lat) <= 20.72 and -105.32 <= float(lng) <= -105.18:
        return "Puerto Vallarta"
    if "Santa Catarina" in address:
        return "Santa Catarina"
    if "San Pedro" in address or "Garza García" in address:
        return "San Pedro Garza García"
    return "Monterrey"


def _infer_zone(
    address: str,
    *,
    lat: float | None = None,
    lng: float | None = None,
    municipio: str | None = None,
) -> str:
    low = (address or "").lower()
    muni = municipio or _infer_municipality(address, lat=lat, lng=lng)
    if muni == "Puerto Vallarta":
        if any(
            k in low
            for k in (
                "zona romántica",
                "zona romantica",
                "emiliano zapata",
                "olas altas",
                "basilio badillo",
                "los muertos",
                "lazaro cardenas",
                "lázaro cárdenas",
                "pino suárez",
                "pino suarez",
                "ignacio l. vallarta",
                "48380",
            )
        ):
            return "Zona Romántica"
        if any(
            k in low
            for k in (
                "zona hotelera",
                "las glorias",
                "medina ascencio",
                "olímpica",
                "olimpica",
                "conchas chinas",
                "garza blanca",
                "marina vallarta",
                "48333",
                "48330",
                "48310",
                "48390",
            )
        ):
            return "Zona Hotelera"
        if lat is not None and lng is not None:
            f_lat, f_lng = float(lat), float(lng)
            if 20.594 <= f_lat <= 20.6068 and -105.243 <= f_lng <= -105.227:
                return "Zona Romántica"
            if (20.620 <= f_lat <= 20.675 and -105.255 <= f_lng <= -105.220) or (
                20.535 <= f_lat < 20.594 and -105.265 <= f_lng <= -105.230
            ):
                return "Zona Hotelera"
        return "Puerto Vallarta"

    if "jerónimo" in low or "jeronimo" in low:
        return "San Jerónimo"
    if "obispado" in low or "vista hermosa" in low:
        return "Obispado / Vista Hermosa"
    if "cumbres" in low:
        return "Cumbres"
    if "san pedro" in low or "del valle" in low:
        return "San Pedro"
    return muni


def _infer_niche(name: str, category: str) -> str:
    nl = (name or "").lower()
    cl = (category or "").lower()
    joined = f"{nl} {cl}"
    if "padel" in joined or "pádel" in joined or "tenis" in cl:
        return "Pádel & Raqueta"
    if any(w in joined for w in ("hotel", "resort", "beach club", "hostal", "hospedaje", "alojamiento", "suites", "villa", "complejo hotelero")):
        return "Hoteles, Resorts & Beach Clubs"
    if any(w in joined for w in ("crossfit", "hyrox", "fitness", "gimnasio", "gym", "pilates", "totalpass", "yoga", "centro deportivo")):
        return "Fitness & CrossFit"
    if any(w in joined for w in ("danza", "dance", "baile", "ballet", "salsa", "bachata")) and "yoga" not in nl:
        return "Baile & Danza Señoras"
    if any(
        w in joined
        for w in (
            "dental",
            "dentist",
            "clínica",
            "clinica",
            "médico",
            "medico",
            "consultorio",
            "nutri",
            "fisioter",
            "dermat",
            "salud",
            "spa",
            "estétic",
            "estetic",
            "masaj",
            "wellness",
        )
    ):
        return "Clínicas & Consultorios"
    if any(
        w in joined
        for w in (
            "café",
            "cafe",
            "coffee",
            "restauran",
            "brunch",
            "bistro",
            "panader",
            "bakery",
            "bar ",
            "bar/",
            "coctel",
            "cocktail",
            "cervecer",
            "cantina",
            "mariscos",
            "taquer",
            "cocina",
        )
    ) or cl.strip() in {"bar", "pub", "lounge"}:
        return "Restaurantes & Cafés Boutique"
    if any(w in joined for w in ("kinder", "jardín", "jardin", "guarder", "preescolar", "colegio", "instituto", "school", "liceo", "academia deportiva")):
        return "Colegios & Jardines de Niños"
    if any(
        w in joined
        for w in (
            "tienda",
            "boutique",
            "ropa",
            "recuerdo",
            "souvenir",
            "artesan",
            "conveniencia",
            "abarrotes",
            "minimarket",
            "minisuper",
            "licor",
            "joyer",
            "regalo",
            "zapater",
            "galer",
            "supermercado",
            "mercado",
        )
    ):
        return "Tiendas, Boutiques & Comercios"
    return "Small Business & Comercios"


def build_maps_target_url(record: dict[str, Any]) -> str:
    """Build direct Google Maps place URL avoiding ambiguous search lists whenever place_id exists."""
    raw_url = str(record.get("gmaps_url") or record.get("url") or "").strip()
    if raw_url.startswith("https://www.google.com/maps/") and ("place_id=" in raw_url or "/maps/place/" in raw_url):
        if "hl=" not in raw_url:
            sep = "&" if "?" in raw_url else "?"
            return f"{raw_url}{sep}hl=es-MX"
        return raw_url
    name = str(record.get("nombre") or record.get("title") or "").strip()
    place_id = str(record.get("place_id") or record.get("placeId") or "").strip()
    address = str(record.get("direccion") or record.get("address") or "").strip()
    params = {"api": "1", "query": f"{name} {address}".strip() or name, "hl": "es-MX"}
    if place_id:
        params["query_place_id"] = place_id
    return "https://www.google.com/maps/search/?" + urllib.parse.urlencode(params)


def sync_audit_index_from_sources(
    *,
    raw_path: Path | None = None,
    leads_path: Path | None = None,
    audits_path: Path | None = None,
    screenshots_dir: Path | None = None,
    screenshots_rel_prefix: str = "assets/gmaps_audits",
    mockups_rel_prefix: str = "assets/mockups/small_biz",
) -> dict[str, Any]:
    """Merge raw Apify metadata with enriched leads and build/update gmaps_audits.json."""
    target_raw_path = raw_path or RAW_APIFY_PATH
    target_leads_path = leads_path or FILES["leads"]
    target_audits_path = audits_path or FILES["gmaps_audits"]
    target_shots_dir = screenshots_dir or GMAPS_AUDITS_DIR
    rel_prefix = screenshots_rel_prefix.rstrip("/")
    mockups_prefix = mockups_rel_prefix.rstrip("/")

    raw_items = read_json(target_raw_path, default=[])
    leads = read_json(target_leads_path, default=[])
    existing_index = read_json(target_audits_path, default={"audits": []})
    existing_by_slug = {a.get("slug"): a for a in existing_index.get("audits", []) if a.get("slug")}

    raw_by_name = {
        str(x.get("title") or "").strip().lower(): x
        for x in raw_items
        if x.get("title")
    }
    raw_by_pid = {
        str(x.get("placeId") or "").strip(): x
        for x in raw_items
        if x.get("placeId")
    }

    enriched_leads: list[dict[str, Any]] = []
    seen_keys: set[str] = set()

    for lead in leads:
        name_key = str(lead.get("nombre") or "").strip().lower()
        pid = str(lead.get("place_id") or "").strip()
        dedup_key = pid or name_key
        raw_match = raw_by_pid.get(pid) or raw_by_name.get(name_key)
        merged = dict(lead)
        if raw_match:
            merged.setdefault("place_id", raw_match.get("placeId") or "")
            if not merged.get("place_id"):
                merged["place_id"] = raw_match.get("placeId") or ""
            merged["gmaps_url"] = raw_match.get("url") or merged.get("gmaps_url") or ""
            merged["image_url"] = raw_match.get("imageUrl") or merged.get("image_url") or ""
            if raw_match.get("imagesCount") is not None:
                merged["images_count"] = raw_match.get("imagesCount")
            merged["claim_this_business"] = bool(raw_match.get("claimThisBusiness"))
            if raw_match.get("website") and (not merged.get("sitio_web") or "google.com/maps" in str(merged.get("sitio_web"))):
                merged["sitio_web"] = raw_match.get("website")
            if raw_match.get("phone") and not merged.get("telefono"):
                merged["telefono"] = raw_match.get("phone")
            loc = raw_match.get("location") or {}
            if isinstance(loc, dict):
                merged.setdefault("lat", loc.get("lat"))
                merged.setdefault("lng", loc.get("lng"))

        analysis = analyze_business_profile(merged)
        merged["place_id"] = analysis["place_id"]
        merged["gmaps_url"] = analysis["gmaps_url"]
        merged["audit_flags"] = analysis["audit_flags"]
        merged["audit_score"] = analysis["audit_score"]
        merged["has_streetview_cover"] = analysis["has_streetview_cover"]
        merged["client_observations"] = analysis["client_observations"]
        if analysis.get("lat") is not None:
            merged["lat"] = analysis["lat"]
        if analysis.get("lng") is not None:
            merged["lng"] = analysis["lng"]
        if analysis.get("images_count") is not None:
            merged["images_count"] = analysis["images_count"]
        if analysis.get("image_url"):
            merged["image_url"] = analysis["image_url"]

        slug = analysis["slug"]
        shot_rel = f"{rel_prefix}/{slug}.png"
        shot_abs = target_shots_dir / f"{slug}.png"
        if shot_abs.exists() and shot_abs.stat().st_size > 10_000:
            merged["gmaps_screenshot"] = shot_rel
        enriched_leads.append(merged)
        if dedup_key:
            seen_keys.add(dedup_key)
        if name_key:
            seen_keys.add(name_key)

    # Include any raw Apify entries not yet in leads JSON
    for raw in raw_items:
        title = str(raw.get("title") or "").strip()
        pid = str(raw.get("placeId") or "").strip()
        if not title or (pid and pid in seen_keys) or title.lower() in seen_keys:
            continue
        analysis = analyze_business_profile(raw)
        slug = analysis["slug"]
        shot_rel = f"{rel_prefix}/{slug}.png"
        shot_abs = target_shots_dir / f"{slug}.png"
        new_lead = {
            "nombre": analysis["nombre"],
            "categoria": analysis["categoria"],
            "direccion": analysis["direccion"],
            "telefono": analysis["telefono"],
            "sitio_web": analysis["sitio_web"],
            "gmaps_url": analysis["gmaps_url"],
            "place_id": analysis["place_id"],
            "image_url": analysis["image_url"],
            "images_count": analysis["images_count"],
            "claim_this_business": analysis["claim_this_business"],
            "has_streetview_cover": analysis["has_streetview_cover"],
            "audit_flags": analysis["audit_flags"],
            "audit_score": analysis["audit_score"],
            "client_observations": analysis["client_observations"],
            "rating": analysis["rating"],
            "resenas": analysis["resenas"],
            "municipio": analysis["municipio"],
            "zona": analysis["zona"],
            "subzona": analysis.get("subzona", ""),
            "lat": analysis.get("lat"),
            "lng": analysis.get("lng"),
            "nicho": analysis["nicho"],
            "oportunidad_captoora": analysis["client_observations"][0] if analysis["client_observations"] else "Renovación visual 2027 + Setup Meta Business.",
        }
        if shot_abs.exists() and shot_abs.stat().st_size > 10_000:
            new_lead["gmaps_screenshot"] = shot_rel
        enriched_leads.append(new_lead)
        if pid:
            seen_keys.add(pid)
        seen_keys.add(title.lower())

    write_json(target_leads_path, enriched_leads)

    audits: list[dict[str, Any]] = []
    seen_audit_slugs: set[str] = set()
    for lead in enriched_leads:
        nombre = str(lead.get("nombre") or "").strip()
        if not nombre:
            continue
        base_slug = slugify(nombre)
        slug = base_slug
        if slug in seen_audit_slugs:
            suffix = slugify(str(lead.get("zona") or lead.get("municipio") or "sucursal"))[:18]
            slug = f"{base_slug[:45]}_{suffix}" if suffix else f"{base_slug}_2"
            idx = 2
            while slug in seen_audit_slugs:
                slug = f"{base_slug[:45]}_{idx}"
                idx += 1
        seen_audit_slugs.add(slug)
        flags = list(lead.get("audit_flags") or [])
        score = int(lead.get("audit_score") or 0)
        shot_rel = f"{rel_prefix}/{slug}.png"
        shot_abs = target_shots_dir / f"{slug}.png"
        prev = existing_by_slug.get(slug, {})
        has_shot = shot_abs.exists() and shot_abs.stat().st_size > 10_000
        before_after_rel = f"{mockups_prefix}/{slug}_AntesDespues_2027.png"
        dossier_rel = f"{mockups_prefix}/{slug}_Dossier_SMB_2027.pdf"

        client_obs = list(lead.get("client_observations") or [])
        if not client_obs and lead.get("oportunidad_captoora"):
            client_obs = [str(lead["oportunidad_captoora"]).strip()]

        municipio = str(lead.get("municipio") or "Monterrey").strip()
        zona = str(lead.get("zona") or municipio).strip()

        audits.append(
            {
                "slug": slug,
                "nombre": nombre,
                "categoria": lead.get("categoria") or "Negocio Local",
                "nicho": lead.get("nicho") or "Small Business & Comercios",
                "municipio": municipio,
                "zona": zona,
                "subzona": lead.get("subzona") or "",
                "lat": lead.get("lat"),
                "lng": lead.get("lng"),
                "direccion": lead.get("direccion") or "",
                "telefono": lead.get("telefono") or "",
                "sitio_web": lead.get("sitio_web") or "",
                "gmaps_url": lead.get("gmaps_url") or build_maps_target_url(lead),
                "place_id": lead.get("place_id") or "",
                "logo": lead.get("logo") or prev.get("logo") or "",
                "rating": lead.get("rating"),
                "resenas": int(lead.get("resenas") or 0),
                "images_count": lead.get("images_count"),
                "claim_this_business": bool(lead.get("claim_this_business")),
                "has_streetview_cover": bool(lead.get("has_streetview_cover")),
                "audit_flags": flags,
                "audit_score": score,
                "client_observations": client_obs,
                "screenshot_path": shot_rel if has_shot else "",
                "capture_status": "captured" if has_shot else prev.get("capture_status", "queued"),
                "captured_at": prev.get("captured_at") or (now_iso() if has_shot else None),
                "before_after_path": before_after_rel if (ROOT_DIR / before_after_rel).exists() else "",
                "dossier_pdf_path": dossier_rel if (ROOT_DIR / dossier_rel).exists() else "",
                "outreach_modes": build_smb_outreach_variants(
                    {
                        "nombre": nombre,
                        "categoria": lead.get("categoria") or "",
                        "nicho": lead.get("nicho") or "",
                        "municipio": municipio,
                        "zona": zona,
                        "audit_flags": flags,
                        "client_observations": client_obs,
                    }
                ),
            }
        )

    audits.sort(key=lambda a: (len(a["audit_flags"]) > 0, a["audit_score"], 1 if a["has_streetview_cover"] else 0), reverse=True)
    summary = {
        "updated_at": now_iso(),
        "total_leads": len(enriched_leads),
        "total_audited": len(audits),
        "deficient_count": sum(1 for a in audits if a["audit_score"] >= 15),
        "captured_count": sum(1 for a in audits if a["capture_status"] == "captured"),
        "streetview_count": sum(1 for a in audits if "CARRITO STREET VIEW" in a["audit_flags"]),
        "zero_photos_count": sum(1 for a in audits if "0 FOTOS" in a["audit_flags"]),
        "unclaimed_count": sum(1 for a in audits if "SIN RECLAMAR" in a["audit_flags"]),
        "audits": audits,
    }
    write_json(target_audits_path, summary)
    return summary


def _neutralize_origin(text: str) -> str:
    return (
        text.replace("en taller MTY/SPGG", "en taller artesanal")
        .replace("taller MTY/SPGG", "taller artesanal")
        .replace("en taller MTY", "en taller artesanal")
        .replace("taller MTY", "taller artesanal")
    )


def build_smb_outreach_variants(audit: dict[str, Any]) -> dict[str, str]:
    """Generate niche-personalized Mode A (Direct Visual), Mode B (2-Step Short), and Mode C (Hybrid) drafts."""
    name = str(audit.get("nombre") or "su negocio").strip()
    flags = set(audit.get("audit_flags") or [])
    obs_list = list(audit.get("client_observations") or [])
    municipio = str(audit.get("municipio") or "Monterrey").strip()
    zona = str(audit.get("zona") or "").strip()
    external_territory = municipio.lower() not in {"monterrey", "san pedro garza garcía", "san pedro garza garcia", "santa catarina", "san pedro"}

    profile = resolve_niche_profile(
        str(audit.get("nicho") or ""),
        name=name,
        category=str(audit.get("categoria") or ""),
    )

    if "CARRITO STREET VIEW" in flags:
        finding = "su ficha en Google Maps todavía abre con la vista automática de calle (Street View)"
    elif "0 FOTOS" in flags:
        finding = "su perfil de Google Maps aparece todavía sin galería fotográfica curada"
    elif "SIN RECLAMAR" in flags:
        finding = "su perfil en Google Maps sigue marcado para verificación oficial ('Reclamar este negocio') y con espacio visual por aprovechar"
    elif obs_list:
        finding = obs_list[0].rstrip(".")
    else:
        finding = f"su ficha de Google Maps y presencia de {profile.niche_key} pueden proyectar una vitrina editorial mucho más sólida"

    if external_territory:
        wa_t1 = _neutralize_origin(profile.wa_tier1)
        wa_t2 = _neutralize_origin(profile.wa_tier2)
        wa_t3 = _neutralize_origin(profile.wa_tier3)
        wa_extra = _neutralize_origin(profile.wa_extra_bullet)
        zone_hint = f" en {zona}" if zona and zona.lower() != municipio.lower() else ""

        mode_a = (
            f"Hola equipo de {name} 👋, te saluda Jesús Gutiérrez de Captoora Studio (Dirección Editorial & Estrategia Google Maps).\n\n"
            f"Revisando fichas comerciales{zone_hint} en Google Maps notamos que {finding}, cuando su espacio y experiencia merecen proyectar una imagen profesional de alto nivel.\n\n"
            f"Con enfoque técnico de iluminación editorial y portafolio enfocado en resultados (https://captoora.studio/sports), estructuramos 3 opciones con -35% de lanzamiento para su Dossier {profile.niche_key}:\n"
            f"{wa_t1}\n"
            f"{wa_t2}\n"
            f"{wa_t3}\n"
            f"{wa_extra}\n\n"
            f"¿Cuál de las 3 opciones revisamos esta semana? Portafolio y técnica: https://captoora.studio/sports\n\n"
            f"*Entrega digital en 48–72h (mismo día en eventos); piezas físicas LED QR en taller artesanal: 3–5 días hábiles con entrega coordinada."
        )

        mode_b = (
            f"Hola equipo de {name} 👋, soy Jesús Gutiérrez de Captoora Studio (Portafolio: https://captoora.studio/sports). "
            f"Preparamos una auditoría visual de cortesía para {name}{zone_hint} sobre cómo aparece hoy su ficha en Google Maps ({finding}) "
            f"y cómo elevarla con fotografía editorial y dirección visual. ¿Te la comparto en imagen Antes/Después con -35% de lanzamiento?"
        )

        mode_c = (
            f"Hola {name} 👋, te escribe Jesús Gutiérrez de Captoora Studio (Producción Editorial & Google Maps).\n\n"
            f"Trabajamos con técnica de luz calibrada y portafolio enfocado en conversión visual para {profile.niche_key} (-35% vigente):\n"
            f"• Portafolio, resultados y estilo: https://captoora.studio/sports\n"
            f"• {wa_t1}\n"
            f"• {wa_t2}\n"
            f"{wa_extra}\n\n"
            f"¿Te envío su dossier visual personalizado de Google Maps?\n\n"
            f"*Digital el mismo día/48–72h; piezas físicas acrílico LED y marcos en taller artesanal: 3–5 días hábiles con entrega coordinada."
        )
    else:
        mode_a = (
            f"Hola equipo de {name} 👋, te saluda Jesús Gutiérrez de Captoora Studio (Producción Editorial 1/2000s · https://captoora.studio/sports).\n\n"
            f"Revisando cómo compiten hoy los negocios en Google Maps notamos que {finding}, cuando su espacio y servicio merecen proyectar una imagen profesional de primer nivel para 2027.\n\n"
            f"Vamos directo a su sede en Monterrey y SPGG con iluminación editorial calibrada y entrega ágil. Preparamos su comparativa personalizada 'Antes y Después' (-35% Temporada activo):\n"
            f"{profile.wa_tier1}\n"
            f"{profile.wa_tier2}\n"
            f"{profile.wa_tier3}\n"
            f"{profile.wa_extra_bullet}\n\n"
            f"¿Cuál de las 3 opciones revisamos esta semana?\n\n"
            f"*Entrega digital en 48–72h (mismo día en eventos); placa acrílica QR LED artesanal: 3–5 días hábiles."
        )

        mode_b = (
            f"Hola equipo de {name} 👋, soy Jesús Gutiérrez de Captoora Studio (Portafolio: https://captoora.studio/sports). "
            f"Preparamos una auditoría visual personalizada de cortesía para {name} sobre cómo aparece hoy su ficha en Google Maps ({finding}) "
            f"y cómo elevarla en 48–72h con fotografía editorial en su sede (-35% de lanzamiento). ¿Te la comparto por aquí?"
        )

        mode_c = (
            f"Hola {name} 👋, te escribe Jesús Gutiérrez de Captoora Studio (Producción Editorial de Alta Velocidad & Google Maps).\n\n"
            f"Con iluminación controlada en sitio y entrega en 48–72h estamos renovando vitrinas 2027 en {profile.niche_key} (-35% Temporada vigente):\n"
            f"• Portafolio interactivo y casos reales: https://captoora.studio/sports\n"
            f"• {profile.wa_tier1}\n"
            f"• {profile.wa_tier2}\n"
            f"{profile.wa_extra_bullet}\n\n"
            f"¿Te envío su dossier visual personalizado de Google Maps para 2027?\n\n"
            f"*Digital mismo día/48–72h; acrílicos LED y marcos artesanales en taller: 3–5 días hábiles."
        )

    for label, text in (("mode_a_directo", mode_a), ("mode_b_diagnostico", mode_b), ("mode_c_hibrido", mode_c)):
        violations = validate_client_copy(text)
        if violations:
            raise ValueError(f"Guardrail blocked SMB copy ({label}): {violations}")

    return {
        "mode_a_directo": mode_a,
        "mode_b_diagnostico": mode_b,
        "mode_c_hibrido": mode_c,
    }


async def _cdp_call(ws: Any, req_id: int, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"id": req_id, "method": method}
    if params:
        payload["params"] = params
    await ws.send(json.dumps(payload))
    while True:
        raw_msg = await asyncio.wait_for(ws.recv(), timeout=25.0)
        msg = json.loads(raw_msg)
        if msg.get("id") == req_id:
            if "error" in msg:
                raise RuntimeError(f"CDP {method} error: {msg['error']}")
            return msg.get("result", {})


async def _capture_targets_async(
    targets: list[dict[str, Any]],
    *,
    overwrite: bool = False,
    screenshots_dir: Path | None = None,
    screenshots_rel_prefix: str = "assets/gmaps_audits",
) -> list[dict[str, Any]]:
    if not CHROME_BIN.exists():
        raise FileNotFoundError(f"Google Chrome not found at {CHROME_BIN}")

    target_shots_dir = screenshots_dir or GMAPS_AUDITS_DIR
    rel_prefix = screenshots_rel_prefix.rstrip("/")
    target_shots_dir.mkdir(parents=True, exist_ok=True)
    port = _free_port()
    tmp_dir = tempfile.mkdtemp(prefix="captoora_gmaps_cdp_")
    cmd = [
        str(CHROME_BIN),
        "--headless=new",
        "--use-gl=angle",
        "--use-angle=swiftshader",
        "--enable-webgl",
        "--hide-scrollbars",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={tmp_dir}",
        "--window-size=1280,820",
        "--lang=es-MX",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-agent={DESKTOP_UA}",
        "about:blank",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    results: list[dict[str, Any]] = []

    try:
        ws_url = ""
        async with httpx.AsyncClient(timeout=5.0) as client:
            for _ in range(30):
                try:
                    resp = await client.get(f"http://127.0.0.1:{port}/json/list")
                    pages = resp.json()
                    page = next((p for p in pages if p.get("type") == "page" and p.get("webSocketDebuggerUrl")), None)
                    if page:
                        ws_url = page["webSocketDebuggerUrl"]
                        break
                except Exception:
                    await asyncio.sleep(0.25)

        if not ws_url:
            raise RuntimeError("No se pudo conectar a Chrome DevTools Protocol para Google Maps.")

        async with websockets.connect(ws_url, max_size=25 * 1024 * 1024) as ws:
            req_id = 1

            async def call(method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
                nonlocal req_id
                cur = req_id
                req_id += 1
                return await _cdp_call(ws, cur, method, params)

            await call("Page.enable")
            await call("Network.enable")
            await call(
                "Network.setUserAgentOverride",
                {
                    "userAgent": DESKTOP_UA,
                    "platform": "MacIntel",
                    "acceptLanguage": "es-MX,es;q=0.9,en;q=0.8",
                },
            )
            await call(
                "Emulation.setDeviceMetricsOverride",
                {
                    "width": 1280,
                    "height": 820,
                    "deviceScaleFactor": 1,
                    "mobile": False,
                },
            )

            for item in targets:
                slug = item["slug"]
                out_path = target_shots_dir / f"{slug}.png"
                rel_path = f"{rel_prefix}/{slug}.png"
                if out_path.exists() and out_path.stat().st_size > 10_000 and not overwrite:
                    results.append({"slug": slug, "status": "cached", "path": rel_path})
                    continue

                url = item.get("gmaps_url") or build_maps_target_url(item)
                try:
                    await call("Page.navigate", {"url": url})
                    await asyncio.sleep(4.8)

                    # Dismiss cookie banners if any & click first result if search feed opened
                    eval_res = await call(
                        "Runtime.evaluate",
                        {
                            "expression": """
                            (() => {
                              const rejectBtn = Array.from(document.querySelectorAll('button')).find(b => /rechazar/i.test(b.innerText || ''));
                              if (rejectBtn) rejectBtn.click();
                              const hasH1 = Boolean(document.querySelector('h1.DUwDvf'));
                              const firstCard = document.querySelector('a.hfpxzc');
                              if (!hasH1 && firstCard) {
                                firstCard.click();
                                return 'clicked_first';
                              }
                              return hasH1 ? 'place_loaded' : 'other';
                            })()
                            """,
                            "returnByValue": True,
                        },
                    )
                    nav_state = (eval_res.get("result") or {}).get("value")
                    if nav_state == "clicked_first":
                        await asyncio.sleep(4.2)

                    # Wait briefly for hero photo or street view image to settle, and remove hover focus
                    for _ in range(6):
                        img_eval = await call(
                            "Runtime.evaluate",
                            {
                                "expression": """
                                (() => {
                                  if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
                                  const hero = document.querySelector('[role="main"] button img, [role="main"] img');
                                  return Boolean(hero && hero.complete && hero.naturalWidth > 20);
                                })()
                                """,
                                "returnByValue": True,
                            },
                        )
                        if (img_eval.get("result") or {}).get("value"):
                            break
                        await asyncio.sleep(0.7)

                    await asyncio.sleep(0.5)
                    shot = await call("Page.captureScreenshot", {"format": "png", "fromSurface": True})
                    png_bytes = base64.b64decode(shot["data"])
                    out_path.write_bytes(png_bytes)
                    results.append(
                        {
                            "slug": slug,
                            "nombre": item.get("nombre"),
                            "status": "captured",
                            "bytes": len(png_bytes),
                            "path": rel_path,
                        }
                    )
                except Exception as exc:
                    results.append({"slug": slug, "nombre": item.get("nombre"), "status": "error", "error": str(exc)})
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return results


async def capture_flagged_places(
    *,
    limit: int | None = None,
    slugs: list[str] | None = None,
    only_deficient: bool = True,
    overwrite: bool = False,
    raw_path: Path | None = None,
    leads_path: Path | None = None,
    audits_path: Path | None = None,
    screenshots_dir: Path | None = None,
    screenshots_rel_prefix: str = "assets/gmaps_audits",
    mockups_rel_prefix: str = "assets/mockups/small_biz",
    territory_label: str = "Small Business",
    log_event: bool = True,
) -> dict[str, Any]:
    """Audit raw/leads sources, capture Chrome CDP Google Maps screenshots, and update workspace JSONs."""
    summary = sync_audit_index_from_sources(
        raw_path=raw_path,
        leads_path=leads_path,
        audits_path=audits_path,
        screenshots_dir=screenshots_dir,
        screenshots_rel_prefix=screenshots_rel_prefix,
        mockups_rel_prefix=mockups_rel_prefix,
    )
    audits = summary["audits"]
    if slugs:
        slug_set = set(slugs)
        candidates = [a for a in audits if a["slug"] in slug_set]
    elif only_deficient:
        candidates = [a for a in audits if a["audit_score"] >= 15]
    else:
        candidates = list(audits)

    if not overwrite:
        pending = [a for a in candidates if a["capture_status"] != "captured"]
    else:
        pending = list(candidates)

    if limit is not None:
        pending = pending[: max(0, int(limit))]

    capture_results: list[dict[str, Any]] = []
    if pending:
        # Process in batches of 15 to keep Chrome heap fresh
        batch_size = 15
        for start in range(0, len(pending), batch_size):
            batch = pending[start : start + batch_size]
            batch_res = await _capture_targets_async(
                batch,
                overwrite=overwrite,
                screenshots_dir=screenshots_dir,
                screenshots_rel_prefix=screenshots_rel_prefix,
            )
            capture_results.extend(batch_res)

    updated = sync_audit_index_from_sources(
        raw_path=raw_path,
        leads_path=leads_path,
        audits_path=audits_path,
        screenshots_dir=screenshots_dir,
        screenshots_rel_prefix=screenshots_rel_prefix,
        mockups_rel_prefix=mockups_rel_prefix,
    )
    captured_now = sum(1 for r in capture_results if r.get("status") == "captured")
    if captured_now and log_event:
        append_agent_event(
            "scouting_radar",
            "Auditoría Visual Maps",
            f"Capturó {captured_now} fichas de Google Maps ({updated['captured_count']} totales en {territory_label}).",
            target_agent="ventas_outreach",
            zone="radar_maps",
            source="gmaps_auditor",
        )
    return {
        "batch_results": capture_results,
        "summary": {k: v for k, v in updated.items() if k != "audits"},
        "audits": updated["audits"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Auditor visual Google Maps + captura CDP Captoora.")
    parser.add_argument("--sync-only", action="store_true", help="Solo sincroniza banderas de auditoría sin abrir Chrome.")
    parser.add_argument("--all-leads", action="store_true", help="Captura capturas pendientes para los 141 prospectos, no solo puntaje >=15.")
    parser.add_argument("--limit", type=int, default=None, help="Máximo número de capturas nuevas a realizar.")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescribe capturas ya guardadas.")
    parser.add_argument("--slug", action="append", default=None, help="Slug específico a capturar.")
    args = parser.parse_args()

    if args.sync_only:
        res = sync_audit_index_from_sources()
        print(json.dumps({k: v for k, v in res.items() if k != "audits"}, indent=2, ensure_ascii=False))
        return

    res = asyncio.run(
        capture_flagged_places(
            limit=args.limit,
            slugs=args.slug,
            only_deficient=not args.all_leads,
            overwrite=args.overwrite,
        )
    )
    print(json.dumps(res["summary"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
