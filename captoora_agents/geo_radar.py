"""Monterrey & SPGG Geo-Radar: 141-lead GPS index, attack status overlay, and TSP route optimizer."""

from __future__ import annotations

import argparse
import json
import math
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from . import ROOT_DIR
from .config import FILES, append_agent_event, now_iso, read_json, slugify, write_json

STUDIO_BASE = {
    "name": "Captoora Base Operativa",
    "address": "Av. Paseo de los Álamos 165, Colinas de San Jerónimo, Monterrey, N.L.",
    "lat": 25.6788,
    "lng": -100.3694,
}

# Bounding box for Greater Monterrey Metro Area (Monterrey, SPGG, Santa Catarina, Guadalupe, Apodaca, San Nicolás)
_MTY_LAT_RANGE = (25.40, 26.02)
_MTY_LNG_RANGE = (-100.65, -100.02)

ZONE_ANCHORS: list[tuple[tuple[str, ...], tuple[float, float]]] = [
    (("san jerónimo", "san jeronimo", "colinas", "álamos", "puerta del sol", "rogelio cantú"), (25.6795, -100.3715)),
    (("obispado", "vista hermosa", "chepevera", "hidalgo"), (25.6745, -100.3465)),
    (("del valle", "centrito", "valle oriente", "san agustín", "gómez morín", "ricardo margáin", "alberto santos"), (25.6538, -100.3665)),
    (("chipinque", "tampiquito", "valle de chipinque", "san pedro", "garza garcía", "santa bárbara"), (25.6505, -100.3820)),
    (("cumbres", "leones", "puerta de hierro", "paseo de los leones", "vista hermosa"), (25.7165, -100.3885)),
    (("carretera nacional", "valle alto", "estanzuela", "esfera", "pueblo sereno"), (25.5680, -100.2565)),
    (("tec", "tecnológico", "contry", "garza sada", "roma", "primavera"), (25.6495, -100.2895)),
    (("santa catarina", "huasteca", "vía cordillera"), (25.6730, -100.4560)),
    (("guadalupe", "linda vista", "apoda", "san nicolás", "san nicolas", "anahuac"), (25.7145, -100.2785)),
    (("centro", "barrio antiguo", "fundidora", "marco"), (25.6692, -100.3099)),
]

DEFAULT_MTY_COORDS = (25.6732, -100.3450)


def _in_mty_bbox(lat: float, lng: float) -> bool:
    return (_MTY_LAT_RANGE[0] <= lat <= _MTY_LAT_RANGE[1]) and (_MTY_LNG_RANGE[0] <= lng <= _MTY_LNG_RANGE[1])


def _anchor_for_text(text: str, index_idx: int) -> tuple[float, float]:
    low = (text or "").lower()
    base_lat, base_lng = DEFAULT_MTY_COORDS
    for keywords, coords in ZONE_ANCHORS:
        if any(k in low for k in keywords):
            base_lat, base_lng = coords
            break
    # Tiny deterministic spiral (~110m radius) so nearby plaza entries remain clickable independently
    angle = index_idx * 2.39996
    radius = 0.0009 * (1 + (index_idx % 4) * 0.4)
    return round(base_lat + math.sin(angle) * radius, 6), round(base_lng + math.cos(angle) * radius, 6)


def _nominatim_geocode(query: str) -> tuple[float, float] | None:
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": query, "format": "json", "limit": 1, "countrycodes": "mx"}
    )
    req = urllib.request.Request(url, headers={"User-Agent": "CaptooraGeoRadar/1.0 (chuy@captoora.studio)"})
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            rows = json.loads(resp.read().decode("utf-8"))
        if isinstance(rows, list) and rows:
            lat = float(rows[0]["lat"])
            lng = float(rows[0]["lon"])
            if _in_mty_bbox(lat, lng):
                return round(lat, 6), round(lng, 6)
    except Exception:
        return None
    return None


def classify_map_category(nicho: str, categoria: str = "") -> str:
    text = f"{nicho} {categoria}".lower()
    if any(k in text for k in ("colegio", "kinder", "kínder", "jardín de niños", "jardin de ninos", "escuela", "guarder", "institute")):
        return "Escuelas & Colegios"
    if any(k in text for k in ("pádel", "padel", "tenis", "raqueta")):
        return "Pádel & Raqueta"
    if any(k in text for k in ("baile", "danza", "dance", "ballet", "pole")):
        return "Baile & Danza"
    if any(k in text for k in ("clínica", "clinica", "dental", "médic", "medic", "nutri", "fisio", "consultorio")):
        return "Clínicas & Salud"
    if any(k in text for k in ("café", "cafe", "restaurante", "brunch", "comercio", "small business", "cowork")):
        return "Cafés & Comercios"
    return "Gimnasios & Fitness"


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


def sync_geo_leads(*, geocode_missing: bool = False) -> dict[str, Any]:
    """Build or refresh verified leads_geo.json (141 leads) combining Apify exact GPS, OSM Nominatim, and zone anchors."""
    leads = read_json(FILES["leads"], default=[]) or []
    raw_path = ROOT_DIR / "dashboard" / "data" / "apify_dataset_raw.json"
    raw = read_json(raw_path, default=[]) or []
    existing_geo = read_json(FILES["leads_geo"], default={"pins": []}) or {"pins": []}
    existing_by_slug = {p.get("slug"): p for p in existing_geo.get("pins", []) if p.get("slug")}

    raw_by_pid = {
        x["placeId"]: x["location"]
        for x in raw
        if x.get("placeId") and isinstance(x.get("location"), dict) and x["location"].get("lat")
    }
    raw_by_title = {
        str(x.get("title") or "").strip().lower(): x["location"]
        for x in raw
        if x.get("title") and isinstance(x.get("location"), dict) and x["location"].get("lat")
    }

    pins: list[dict[str, Any]] = []
    seen_slugs: set[str] = set()
    for idx, lead in enumerate(leads):
        name = str(lead.get("nombre") or f"Negocio {idx + 1}").strip()
        slug = slugify(name)
        if slug in seen_slugs:
            slug = f"{slug}_{idx + 1}"
        seen_slugs.add(slug)

        lat = None
        lng = None
        precision = "zone_centroid"

        pid = lead.get("place_id")
        loc = raw_by_pid.get(pid) or raw_by_title.get(name.lower())
        if isinstance(loc, dict) and loc.get("lat") and loc.get("lng"):
            lat = round(float(loc["lat"]), 6)
            lng = round(float(loc["lng"]), 6)
            precision = "apify_exact"
        elif slug in existing_by_slug and existing_by_slug[slug].get("lat"):
            prev = existing_by_slug[slug]
            lat = float(prev["lat"])
            lng = float(prev["lng"])
            precision = str(prev.get("geo_precision") or "osm_geocoded")
        elif geocode_missing:
            addr = str(lead.get("direccion") or "").strip()
            muni = str(lead.get("municipio") or "Monterrey").strip()
            query = f"{addr}, {muni}, Nuevo León, México" if addr else f"{name}, {muni}, Nuevo León, México"
            found = _nominatim_geocode(query)
            if not found and addr:
                # Retry dropping street suite/local clutter
                short_addr = addr.split(",")[0].strip()
                found = _nominatim_geocode(f"{short_addr}, {muni}, Nuevo León, México")
            if found:
                lat, lng = found
                precision = "osm_geocoded"
            time.sleep(1.05)  # Respect Nominatim 1 req/s usage policy

        if lat is None or lng is None:
            lat, lng = _anchor_for_text(f"{lead.get('zona','')} {lead.get('direccion','')} {lead.get('municipio','')}", idx)
            precision = "zone_centroid"

        pins.append(
            {
                "slug": slug,
                "nombre": name,
                "nicho": str(lead.get("nicho") or "Small Business & Comercios"),
                "map_category": classify_map_category(str(lead.get("nicho") or ""), str(lead.get("categoria") or "")),
                "categoria": str(lead.get("categoria") or ""),
                "municipio": str(lead.get("municipio") or "Monterrey"),
                "zona": str(lead.get("zona") or ""),
                "direccion": str(lead.get("direccion") or ""),
                "telefono": str(lead.get("telefono") or ""),
                "sitio_web": str(lead.get("sitio_web") or ""),
                "rating": lead.get("rating"),
                "resenas": lead.get("resenas") or 0,
                "gmaps_url": str(lead.get("gmaps_url") or ""),
                "lat": lat,
                "lng": lng,
                "geo_precision": precision,
            }
        )

    payload = {
        "updated_at": now_iso(),
        "base": STUDIO_BASE,
        "total_pins": len(pins),
        "precision_counts": {
            "apify_exact": sum(1 for p in pins if p["geo_precision"] == "apify_exact"),
            "osm_geocoded": sum(1 for p in pins if p["geo_precision"] == "osm_geocoded"),
            "zone_centroid": sum(1 for p in pins if p["geo_precision"] == "zone_centroid"),
        },
        "pins": pins,
    }
    write_json(FILES["leads_geo"], payload)
    return payload


def get_enriched_geo_map() -> dict[str, Any]:
    """Return 141 pins enriched dynamically with live attack status, distance from Base, and CRM tags."""
    geo = read_json(FILES["leads_geo"], default=None)
    if not geo or not geo.get("pins"):
        geo = sync_geo_leads(geocode_missing=False)

    audits_idx = read_json(FILES["gmaps_audits"], default={"audits": []}) or {"audits": []}
    audit_by_slug = {a.get("slug"): a for a in audits_idx.get("audits", []) if a.get("slug")}

    queue = read_json(FILES["approvals"], default={"items": []}) or {"items": []}
    approved_names = set()
    pending_names = set()
    for item in queue.get("items", []):
        target_low = str(item.get("target_name") or "").lower()
        if item.get("status") == "approved":
            approved_names.add(target_low)
        elif item.get("status") == "pending_trigger":
            pending_names.add(target_low)

    growth = read_json(FILES["growth_suite"], default={}) or {}
    crm = growth.get("crm_records", {}) if isinstance(growth, dict) else {}
    wa_sent_slugs = {
        row.get("slug")
        for row in (growth.get("whatsapp_web_log", []) if isinstance(growth, dict) else [])
        if row.get("slug")
    }
    mail_sent_slugs = {
        row.get("slug")
        for row in (growth.get("mail_campaigns_log", []) if isinstance(growth, dict) else [])
        if row.get("slug")
    }

    base = geo.get("base") or STUDIO_BASE
    base_lat, base_lng = float(base["lat"]), float(base["lng"])

    enriched_pins: list[dict[str, Any]] = []
    status_counts = {
        "atacado_aprobado": 0,
        "en_cola_pendiente": 0,
        "dolor_critico_sin_atacar": 0,
        "sin_atacar": 0,
    }

    for pin in geo.get("pins", []):
        slug = pin["slug"]
        name_low = pin["nombre"].lower()
        audit = audit_by_slug.get(slug, {})
        crm_row = crm.get(slug, {}) if isinstance(crm, dict) else {}
        crm_stage = str(crm_row.get("stage") or "").lower()

        is_approved = (
            slug in wa_sent_slugs
            or slug in mail_sent_slugs
            or crm_stage in ("contactado", "respondio", "calendly", "cotizado", "anticipo_50", "cerrado")
            or any(name_low[:14] in t for t in approved_names if len(name_low) >= 6)
        )
        is_pending = (not is_approved) and any(name_low[:14] in t for t in pending_names if len(name_low) >= 6)
        flags = audit.get("audit_flags") or []
        has_critical_pain = bool(
            audit.get("is_deficient")
            or any(f in flags for f in ("CARRITO STREET VIEW", "0 FOTOS", "SIN RECLAMAR"))
        )

        if is_approved:
            campaign_status = "atacado_aprobado"
            status_label = "Atacado / Activo"
        elif is_pending:
            campaign_status = "en_cola_pendiente"
            status_label = "En Cola Trigger"
        elif has_critical_pain:
            campaign_status = "dolor_critico_sin_atacar"
            status_label = "Dolor Crítico · Sin Atacar"
        else:
            campaign_status = "sin_atacar"
            status_label = "Sin Atacar"

        status_counts[campaign_status] += 1
        dist_km = haversine_km(base_lat, base_lng, float(pin["lat"]), float(pin["lng"]))

        enriched_pins.append(
            {
                **pin,
                "campaign_status": campaign_status,
                "status_label": status_label,
                "crm_stage": crm_row.get("stage") or "Nuevo",
                "confirmed_yes_today": bool(crm_row.get("confirmed_yes_today", False)),
                "distance_from_base_km": dist_km,
                "audit_flags": flags,
                "before_after_path": audit.get("before_after_path") or f"assets/mockups/small_biz/{slug}_AntesDespues_2027.png",
                "dossier_pdf_path": audit.get("dossier_pdf_path") or f"assets/mockups/small_biz/{slug}_Dossier_SMB_2027.pdf",
                "screenshot_path": audit.get("screenshot_path") or f"assets/gmaps_audits/{slug}.png",
            }
        )

    routes_log = read_json(FILES["routes_log"], default={"routes": []}) or {"routes": []}
    return {
        "updated_at": now_iso(),
        "base": base,
        "total_pins": len(enriched_pins),
        "precision_counts": geo.get("precision_counts", {}),
        "status_counts": status_counts,
        "pins": enriched_pins,
        "saved_routes": routes_log.get("routes", [])[:15],
    }


def _route_total_distance(order: list[dict[str, Any]], start_lat: float, start_lng: float) -> float:
    total = 0.0
    clat, clng = start_lat, start_lng
    for node in order:
        total += haversine_km(clat, clng, float(node["lat"]), float(node["lng"]))
        clat, clng = float(node["lat"]), float(node["lng"])
    return total


def optimize_visit_route(
    slugs: list[str],
    *,
    origin_lat: float | None = None,
    origin_lng: float | None = None,
    origin_name: str | None = None,
) -> dict[str, Any]:
    """Compute an efficient visit route (Nearest-Neighbor + 2-opt) across selected Monterrey/SPGG leads."""
    clean_slugs = [str(s).strip() for s in slugs if str(s).strip()]
    if not clean_slugs:
        raise ValueError("Selecciona al menos 1 negocio o escuela para trazar la ruta.")

    geo_map = get_enriched_geo_map()
    by_slug = {p["slug"]: p for p in geo_map["pins"]}
    selected = [by_slug[s] for s in clean_slugs if s in by_slug]
    if not selected:
        raise ValueError("No se encontraron coordenadas válidas para los slugs seleccionados.")

    base = geo_map["base"]
    start_lat = float(origin_lat if origin_lat is not None else base["lat"])
    start_lng = float(origin_lng if origin_lng is not None else base["lng"])
    start_label = origin_name or base["name"]

    # Nearest-Neighbor construction
    remaining = list(selected)
    ordered: list[dict[str, Any]] = []
    cur_lat, cur_lng = start_lat, start_lng
    while remaining:
        best_idx = min(
            range(len(remaining)),
            key=lambda i: haversine_km(cur_lat, cur_lng, float(remaining[i]["lat"]), float(remaining[i]["lng"])),
        )
        nxt = remaining.pop(best_idx)
        ordered.append(nxt)
        cur_lat, cur_lng = float(nxt["lat"]), float(nxt["lng"])

    # 2-opt local optimization keeping fixed origin
    if len(ordered) >= 3:
        improved = True
        while improved:
            improved = False
            best_dist = _route_total_distance(ordered, start_lat, start_lng)
            for i in range(len(ordered) - 1):
                for j in range(i + 1, len(ordered)):
                    candidate = ordered[:i] + list(reversed(ordered[i : j + 1])) + ordered[j + 1 :]
                    cand_dist = _route_total_distance(candidate, start_lat, start_lng)
                    if cand_dist + 0.02 < best_dist:
                        ordered = candidate
                        best_dist = cand_dist
                        improved = True

    stops: list[dict[str, Any]] = []
    clat, clng = start_lat, start_lng
    total_km = 0.0
    total_drive_min = 0
    for idx, node in enumerate(ordered, start=1):
        leg_km = haversine_km(clat, clng, float(node["lat"]), float(node["lng"]))
        leg_min = max(5, round(leg_km * 2.5 + 4))
        total_km = round(total_km + leg_km, 2)
        total_drive_min += leg_min
        stops.append(
            {
                "stop_number": idx,
                "slug": node["slug"],
                "nombre": node["nombre"],
                "map_category": node["map_category"],
                "municipio": node["municipio"],
                "direccion": node["direccion"],
                "telefono": node["telefono"],
                "lat": node["lat"],
                "lng": node["lng"],
                "leg_distance_km": leg_km,
                "estimated_drive_min": leg_min,
                "cumulative_km": total_km,
                "campaign_status": node["campaign_status"],
            }
        )
        clat, clng = float(node["lat"]), float(node["lng"])

    last = stops[-1]
    waypoints = "|".join(f"{s['lat']},{s['lng']}" for s in stops[:-1])
    gmaps_params: dict[str, str] = {
        "api": "1",
        "origin": f"{start_lat},{start_lng}",
        "destination": f"{last['lat']},{last['lng']}",
        "travelmode": "driving",
    }
    if waypoints:
        gmaps_params["waypoints"] = waypoints
    google_maps_route_url = "https://www.google.com/maps/dir/?" + urllib.parse.urlencode(gmaps_params)

    return {
        "origin": {"name": start_label, "lat": start_lat, "lng": start_lng},
        "stops_count": len(stops),
        "total_distance_km": total_km,
        "estimated_total_drive_min": total_drive_min,
        "google_maps_route_url": google_maps_route_url,
        "stops": stops,
    }


def save_confirmed_route(
    *,
    title: str,
    slugs: list[str],
    scheduled_date: str = "",
    notes: str = "",
    origin_lat: float | None = None,
    origin_lng: float | None = None,
) -> dict[str, Any]:
    """Compute, register, and persist a confirmed visit route in routes_log.json."""
    plan = optimize_visit_route(slugs, origin_lat=origin_lat, origin_lng=origin_lng)
    log = read_json(FILES["routes_log"], default={"routes": []}) or {"routes": []}
    routes = log.get("routes", [])
    route_id = f"RUTA-{len(routes) + 1:03d}"
    entry = {
        "id": route_id,
        "title": title.strip() or f"Ruta Monterrey ({len(plan['stops'])} paradas)",
        "scheduled_date": scheduled_date.strip() or now_iso()[:10],
        "created_at": now_iso(),
        "status": "programada",
        "notes": notes.strip(),
        **plan,
    }
    routes.insert(0, entry)
    log["routes"] = routes[:50]
    write_json(FILES["routes_log"], log)
    append_agent_event(
        "ops_talleres_legal",
        f"Trazó y registró {route_id}",
        f"{entry['title']} · {plan['stops_count']} paradas · {plan['total_distance_km']} km.",
        zone="taller_led",
        source="human_ui",
    )
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description="Construye índice GPS de Monterrey/SPGG para los 141 leads.")
    parser.add_argument("--geocode-missing", action="store_true", help="Geocodifica con OSM Nominatim los leads sin lat/lng en Apify.")
    args = parser.parse_args()
    res = sync_geo_leads(geocode_missing=args.geocode_missing)
    print(json.dumps({k: res[k] for k in ("updated_at", "total_pins", "precision_counts")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
