#!/usr/bin/env python3
"""
CAPTOORA STUDIO // PUERTO VALLARTA ZONE-SEPARATED APIFY SCRAPER & AUDITOR

Ejecuta extracciones independientes en Apify ('compass~crawler-google-places'):
  1) Zona Romántica (Emiliano Zapata, Olas Altas, Playa Los Muertos, Basilio Badillo)
  2) Zona Hotelera (Zona Hotelera Norte / Las Glorias, Marina y Zona Hotelera Sur)
  3) Centro / Bahía (Centro Histórico, Malecón, Col. 5 de Diciembre, Isla Río Cuale)

Aplica filtrado estricto geográfico (dirección + coordenadas + place_id único)
para evitar contaminación entre zonas y guarda cada territorio por separado sin modificar Nuevo León.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from captoora_agents.config import now_iso, read_json, write_json
from captoora_agents.gmaps_auditor import (
    analyze_business_profile,
    capture_flagged_places,
    sync_audit_index_from_sources,
)

load_dotenv(ROOT_DIR / ".env")

ACTOR_ID = "compass~crawler-google-places"
PV_DATA_ROOT = ROOT_DIR / "dashboard" / "data" / "puerto_vallarta"
PV_SHOTS_ROOT = ROOT_DIR / "assets" / "gmaps_audits" / "puerto_vallarta"

ZONA_ROMANTICA_QUERIES = [
    "restaurantes brunch cafe Zona Romantica Puerto Vallarta",
    "bar cocteleria cafe especialidad Olas Altas Emiliano Zapata Puerto Vallarta",
    "hotel boutique beach club Zona Romantica Puerto Vallarta",
    "clinica dental spa medicina estetica Zona Romantica Emiliano Zapata Puerto Vallarta",
    "gimnasio pilates yoga danza Zona Romantica Emiliano Zapata Puerto Vallarta",
    "tienda de ropa boutique recuerdos Zona Romantica Puerto Vallarta",
    "tienda conveniencia abarrotes licoreria Zona Romantica Emiliano Zapata Puerto Vallarta",
]

ZONA_HOTELERA_QUERIES = [
    "hotel resort beach club Zona Hotelera Norte Las Glorias Puerto Vallarta",
    "hotel resort beach club Conchas Chinas Puerto Vallarta",
    "hotel resort spa restaurante Garza Blanca Carretera Barra de Navidad Puerto Vallarta",
    "restaurante cafe brunch Zona Hotelera Las Glorias Puerto Vallarta",
    "bar lounge cafeteria Zona Hotelera Puerto Vallarta",
    "clinica dental spa medicina estetica Zona Hotelera Las Glorias Puerto Vallarta",
    "gimnasio pilates club de padel Zona Hotelera Puerto Vallarta",
    "tienda de ropa boutique souvenirs Zona Hotelera Las Glorias Puerto Vallarta",
    "tienda conveniencia minimarket plaza Zona Hotelera Puerto Vallarta",
]

CENTRO_BAHIA_QUERIES = [
    "restaurantes cafe especialidad Centro Malecon Puerto Vallarta",
    "restaurante cafe brunch 5 de Diciembre Puerto Vallarta",
    "hotel boutique hostal Centro 5 de Diciembre Puerto Vallarta",
    "bar terraza lounge Centro Malecon Puerto Vallarta",
    "galerias de arte boutique ropa Centro Puerto Vallarta",
    "clinica dental spa estetica Centro 5 de Diciembre Puerto Vallarta",
    "estudio yoga gimnasio pilates Centro 5 de Diciembre Puerto Vallarta",
    "tienda artesanias souvenirs cafe Isla Rio Cuale Puerto Vallarta",
]

# Keywords for deterministic zone validation (never cross-contaminate ZR <-> ZH <-> Centro/Bahía)
ROMANTICA_KEYWORDS = (
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
    "rodolfo gómez",
    "rodolfo gomez",
    "aquiles serdán",
    "aquiles serdan",
    "constitución",
    "constitucion",
    "francisca rodríguez",
    "francisca rodriguez",
    "naranjo",
    "aguacate",
    "48380",
)

HOTELERA_NORTE_KEYWORDS = (
    "zona hotelera norte",
    "zona hotelera",
    "las glorias",
    "medina ascencio",
    "francisco medina ascencio",
    "olímpica",
    "olimpica",
    "versalles",
    "fluvial",
    "aralias",
    "48333",
    "48330",
    "48310",
    "48313",
)

HOTELERA_MARINA_KEYWORDS = (
    "marina vallarta",
    "paseo de la marina",
    "48335",
    "48354",
)

HOTELERA_SUR_KEYWORDS = (
    "zona hotelera sur",
    "conchas chinas",
    "garza blanca",
    "barra de navidad",
    "punta negra",
    "mismaloya",
    "48390",
    "48399",
)

CENTRO_BAHIA_KEYWORDS = (
    "48300",
    "48350",
    "5 de diciembre",
    "paseo díaz ordaz",
    "paseo diaz ordaz",
    "malecón",
    "malecon",
    "proyecto escola",
    "gringo gulch",
    "isla río cuale",
    "isla rio cuale",
    "el cerro",
    "centro, ",
    "downtown",
    "parroquia",
    "playa camarones",
)

OUTSIDE_PV_KEYWORDS = (
    "nuevo vallarta",
    "nuevo nayarit",
    "bahía de banderas",
    "bahia de banderas",
    "nayarit",
    "bucerías",
    "bucerias",
    "mezcales",
    "jarretaderas",
    "san vicente",
    "ixtapa",
    "las juntas",
    "centro pitillal",
    "pitillal",
    "48290",
    "bobadilla",
    "coapinole",
    "mojoneras",
)


def _get_apify_token() -> str:
    token = (os.environ.get("APIFY_TOKEN") or os.environ.get("APIFY_API_TOKEN") or "").strip()
    if token:
        return token
    fallback_file = ROOT_DIR / "scripts" / "run_apify_production.py"
    if fallback_file.exists():
        for line in fallback_file.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("API_TOKEN") and "=" in line:
                candidate = line.split("=", 1)[1].strip().strip("\"'")
                if candidate.startswith("apify_api_"):
                    return candidate
    raise RuntimeError("No se encontró APIFY_TOKEN ni APIFY_API_TOKEN en .env o entorno.")


def classify_pv_zone(item: dict[str, Any]) -> tuple[str | None, str]:
    """
    Classify an Apify place strictly into 'zona_romantica', 'zona_hotelera', 'centro_y_bahia', or None (out-of-scope).
    Returns (zone_key, subzona_label).
    """
    address = str(item.get("address") or item.get("direccion") or "").strip()
    addr_low = address.lower()

    if any(k in addr_low for k in OUTSIDE_PV_KEYWORDS):
        return None, "Fuera de Puerto Vallarta (Nayarit/Periferia)"

    if "puerto vallarta" not in addr_low and "jal." not in addr_low and "jalisco" not in addr_low and "483" not in addr_low:
        return None, "Fuera de Puerto Vallarta"

    loc = item.get("location") if isinstance(item.get("location"), dict) else {}
    raw_lat = loc.get("lat") if loc else item.get("lat")
    raw_lng = loc.get("lng") if loc else item.get("lng")
    lat = float(raw_lat) if raw_lat is not None else None
    lng = float(raw_lng) if raw_lng is not None else None

    # 1. Primary coordinate + address verification for Zona Romántica (south of Río Cuale, north of Conchas Chinas)
    in_romantica_box = (
        lat is not None
        and lng is not None
        and 20.5940 <= lat <= 20.60595
        and -105.2430 <= lng <= -105.2265
    )
    has_north_hotel_marker = any(k in addr_low for k in (HOTELERA_NORTE_KEYWORDS + HOTELERA_MARINA_KEYWORDS))
    has_romantica_colonia = any(
        k in addr_low for k in ("zona romántica", "zona romantica", "emiliano zapata", "olas altas", "basilio badillo", "48380")
    )

    if (in_romantica_box or (lat is None and has_romantica_colonia)) and not has_north_hotel_marker:
        if "olas altas" in addr_low or "los muertos" in addr_low or "púlpito" in addr_low or "pulpito" in addr_low:
            return "zona_romantica", "Olas Altas / Playa Los Muertos"
        if "basilio badillo" in addr_low:
            return "zona_romantica", "Corredor Basilio Badillo"
        return "zona_romantica", "Emiliano Zapata / Zona Romántica"

    # 2. Centro / Bahía north of Río Cuale up to southern edge of Las Glorias (Centro 48300 + 5 de Diciembre 48350 + Malecón + Río Cuale)
    in_centro_bahia_box = (
        lat is not None
        and lng is not None
        and 20.60595 < lat < 20.6190
        and -105.2410 <= lng <= -105.2200
    )
    has_centro_marker = any(k in addr_low for k in CENTRO_BAHIA_KEYWORDS)
    if (in_centro_bahia_box or (lat is None and has_centro_marker)) and not has_north_hotel_marker and not has_romantica_colonia:
        if "5 de diciembre" in addr_low or "48350" in addr_low or "camarones" in addr_low:
            return "centro_y_bahia", "Col. 5 de Diciembre / Playa Camarones"
        if "díaz ordaz" in addr_low or "diaz ordaz" in addr_low or "malecón" in addr_low or "malecon" in addr_low:
            return "centro_y_bahia", "Malecón & Paseo Díaz Ordaz"
        if "río cuale" in addr_low or "rio cuale" in addr_low or "gringo gulch" in addr_low:
            return "centro_y_bahia", "Isla Río Cuale & Gringo Gulch"
        return "centro_y_bahia", "Centro Histórico · 48300"

    # 3. Coordinate + keyword verification for Zona Hotelera (Norte, Marina & Sur)
    in_hotelera_sur_box = (
        lat is not None
        and lng is not None
        and 20.5350 <= lat < 20.5940
        and -105.2650 <= lng <= -105.2290
    )
    if (any(k in addr_low for k in HOTELERA_SUR_KEYWORDS) and (lat is None or lat < 20.5945)) or in_hotelera_sur_box:
        return "zona_hotelera", "Zona Hotelera Sur / Conchas Chinas"

    in_hotelera_marina_box = (
        lat is not None
        and lng is not None
        and 20.6580 <= lat <= 20.6840
        and -105.2660 <= lng <= -105.2360
    )
    if any(k in addr_low for k in HOTELERA_MARINA_KEYWORDS) or in_hotelera_marina_box:
        return "zona_hotelera", "Zona Hotelera · Marina Vallarta"

    in_hotelera_norte_box = (
        lat is not None
        and lng is not None
        and 20.6190 <= lat <= 20.6625
        and -105.2540 <= lng <= -105.2200
    )
    if any(k in addr_low for k in HOTELERA_NORTE_KEYWORDS) or in_hotelera_norte_box:
        if "las glorias" in addr_low:
            return "zona_hotelera", "Zona Hotelera Norte · Las Glorias"
        if "medina ascencio" in addr_low or "zona hotelera" in addr_low:
            return "zona_hotelera", "Zona Hotelera Norte / Medina Ascencio"
        if "5 de diciembre" in addr_low:
            return "zona_hotelera", "Gateway 5 de Diciembre · Corredor Hotelero"
        return "zona_hotelera", "Corredor Versalles / Fluvial (Zona Hotelera Norte)"

    return None, "Otra Colonia Fuera de las 3 Zonas PV"


def _niche_opportunity_pv(niche: str) -> str:
    opportunities = {
        "Hoteles, Resorts & Beach Clubs": (
            "Fotografía editorial de hospitalidad (habitaciones, alberca, beach club) + Google Maps optimizado para reserva directa y Meta Business sin bloqueos."
        ),
        "Restaurantes & Cafés Boutique": (
            "Fotografía gastronómica editorial (platillos, mixología, barra de café) + renovación de portada Google Maps y placa LED QR de reseñas 5★."
        ),
        "Clínicas & Consultorios": (
            "Retrato médico/estético de confianza + instalaciones limpias en Google Maps + Meta Business Portfolio sin bloqueos publicitarios."
        ),
        "Fitness & CrossFit": (
            "Editorial de estudio, clases y coaches + portada Google Maps / reserva de clase prueba + piloto Captoora Biogen Beta."
        ),
        "Baile & Danza Señoras": (
            "Fotografía editorial de clases y presentaciones + renovación de perfil Google Maps y Meta Business."
        ),
        "Pádel & Raqueta": (
            "Cobertura deportiva 1/2000s en pista + Google Maps verificado para reservas y trofeos/placas acrílicas LED."
        ),
        "Tiendas, Boutiques & Comercios": (
            "Vitrina boutique en Google Maps (escaparate, interior y productos estrella) + catálogo WhatsApp / Meta Business y display QR de reseñas."
        ),
    }
    return opportunities.get(
        niche,
        "Renovación editorial en Google Maps + Meta Business Portfolio en regla + display acrílico LED QR.",
    )


def run_apify_scrape(queries: list[str], *, zone_label: str, max_per_search: int, token: str) -> list[dict[str, Any]]:
    print(f"[*] Iniciando extracción Apify para {zone_label} ({len(queries)} búsquedas, max {max_per_search}/búsqueda)...")
    payload = {
        "searchStringsArray": queries,
        "locationQuery": "Puerto Vallarta, Jalisco, Mexico",
        "maxCrawledPlacesPerSearch": max_per_search,
        "language": "es",
        "includeWebResults": False,
        "scrapeDirectories": False,
        "extractPopularTimes": False,
        "exportPlaceUrls": True,
    }
    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={token}"
    req = urllib.request.Request(
        start_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        run_data = json.loads(resp.read().decode("utf-8"))["data"]
    run_id = run_data["id"]
    dataset_id = run_data["defaultDatasetId"]
    print(f"    Run ID: {run_id} | Dataset ID: {dataset_id}")

    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={token}"
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={token}&format=json"

    for attempt in range(45):
        time.sleep(4)
        with urllib.request.urlopen(urllib.request.Request(status_url), timeout=20) as resp:
            status = json.loads(resp.read().decode("utf-8"))["data"]["status"]
        print(f"    [{zone_label}] Intento {attempt + 1}: {status}")
        if status in {"SUCCEEDED", "READY"}:
            break
        if status in {"FAILED", "ABORTED", "TIMED-OUT"}:
            raise RuntimeError(f"Apify run {run_id} ({zone_label}) terminó con estado {status}")

    with urllib.request.urlopen(urllib.request.Request(dataset_url), timeout=40) as resp:
        items = json.loads(resp.read().decode("utf-8"))
    print(f"[✓] {zone_label}: {len(items)} registros brutos descargados de Apify.")
    return items


def filter_and_build_zone_datasets(
    raw_romantica_candidates: list[dict[str, Any]],
    raw_hotelera_candidates: list[dict[str, Any]],
    raw_centro_candidates: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Strictly separate and deduplicate places into Zona Romántica, Zona Hotelera,
    and Centro / Bahía, discarding out-of-perimeter listings with zero cross-zone place_id overlap.
    """
    zone_buckets: dict[str, dict[str, dict[str, Any]]] = {
        "zona_romantica": {},
        "zona_hotelera": {},
        "centro_y_bahia": {},
    }
    global_placed: set[str] = set()
    excluded: list[dict[str, Any]] = []

    def ingest(candidates: list[dict[str, Any]], expected_zone: str) -> None:
        for item in candidates:
            title = str(item.get("title") or "").strip()
            if not title:
                continue
            pid = str(item.get("placeId") or "").strip()
            dedup_id = pid or title.lower()
            if dedup_id in global_placed:
                continue
            classified_zone, subzona = classify_pv_zone(item)

            if classified_zone is None:
                excluded.append(
                    {
                        "nombre": title,
                        "direccion": item.get("address") or "",
                        "razon": subzona,
                        "corrida_origen": expected_zone,
                        "place_id": pid,
                    }
                )
                continue

            # When ingesting Phase 3 Centro / Bahía, do not move or duplicate places belonging to ZR/ZH if ZR/ZH were already loaded
            if expected_zone == "centro_y_bahia" and classified_zone != "centro_y_bahia":
                if dedup_id in zone_buckets[classified_zone]:
                    continue

            global_placed.add(dedup_id)
            enriched = dict(item)
            enriched["_pv_zone_key"] = classified_zone
            enriched["_pv_subzona"] = subzona
            zone_buckets[classified_zone][dedup_id] = enriched

    ingest(raw_romantica_candidates, "zona_romantica")
    ingest(raw_hotelera_candidates, "zona_hotelera")
    if raw_centro_candidates:
        ingest(raw_centro_candidates, "centro_y_bahia")

    zone_configs = {
        "zona_romantica": {
            "label": "Zona Romántica",
            "dir": PV_DATA_ROOT / "zona_romantica",
            "shots_dir": PV_SHOTS_ROOT / "zona_romantica",
            "shots_rel": "assets/gmaps_audits/puerto_vallarta/zona_romantica",
        },
        "zona_hotelera": {
            "label": "Zona Hotelera",
            "dir": PV_DATA_ROOT / "zona_hotelera",
            "shots_dir": PV_SHOTS_ROOT / "zona_hotelera",
            "shots_rel": "assets/gmaps_audits/puerto_vallarta/zona_hotelera",
        },
        "centro_y_bahia": {
            "label": "Centro / Bahía",
            "dir": PV_DATA_ROOT / "centro_y_bahia",
            "shots_dir": PV_SHOTS_ROOT / "centro_y_bahia",
            "shots_rel": "assets/gmaps_audits/puerto_vallarta/centro_y_bahia",
        },
    }

    summaries: dict[str, Any] = {}
    for zone_key, cfg in zone_configs.items():
        raw_items = list(zone_buckets[zone_key].values())
        raw_path = cfg["dir"] / "apify_raw.json"
        leads_path = cfg["dir"] / "leads.json"
        audits_path = cfg["dir"] / "gmaps_audits.json"
        write_json(raw_path, raw_items)

        leads_list: list[dict[str, Any]] = []
        for raw in raw_items:
            raw_copy = dict(raw)
            raw_copy["municipio"] = "Puerto Vallarta"
            raw_copy["zona"] = cfg["label"]
            raw_copy["subzona"] = raw.get("_pv_subzona") or cfg["label"]
            analysis = analyze_business_profile(raw_copy)
            leads_list.append(
                {
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
                    "municipio": "Puerto Vallarta",
                    "zona": cfg["label"],
                    "subzona": raw_copy["subzona"],
                    "lat": analysis.get("lat"),
                    "lng": analysis.get("lng"),
                    "nicho": analysis["nicho"],
                    "oportunidad_captoora": _niche_opportunity_pv(analysis["nicho"]),
                }
            )
        write_json(leads_path, leads_list)

        summary = sync_audit_index_from_sources(
            raw_path=raw_path,
            leads_path=leads_path,
            audits_path=audits_path,
            screenshots_dir=cfg["shots_dir"],
            screenshots_rel_prefix=cfg["shots_rel"],
            mockups_rel_prefix=f"assets/mockups/puerto_vallarta/{zone_key}",
        )
        summaries[zone_key] = {k: v for k, v in summary.items() if k != "audits"}

    # Deduplicate excluded log by place_id/nombre
    seen_exc: set[str] = set()
    clean_excluded: list[dict[str, Any]] = []
    for exc in excluded:
        k = exc.get("place_id") or exc["nombre"].lower()
        if k not in seen_exc:
            seen_exc.add(k)
            clean_excluded.append(exc)

    territory_meta = {
        "updated_at": now_iso(),
        "territory": "Puerto Vallarta, Jalisco (Solo PV)",
        "zones": summaries,
        "excluded_out_of_perimeter_count": len(clean_excluded),
        "excluded_sample": clean_excluded[:30],
    }
    write_json(PV_DATA_ROOT / "territorio_resumen.json", territory_meta)
    return territory_meta


async def capture_zones_async(
    *,
    zones: tuple[str, ...] = ("zona_romantica", "zona_hotelera", "centro_y_bahia"),
    only_deficient: bool = True,
    limit_per_zone: int | None = None,
    overwrite: bool = False,
) -> dict[str, Any]:
    labels = {
        "zona_romantica": "PV Zona Romántica",
        "zona_hotelera": "PV Zona Hotelera",
        "centro_y_bahia": "PV Centro / Bahía",
    }
    results: dict[str, Any] = {}
    for zone_key in zones:
        label = labels[zone_key]
        zdir = PV_DATA_ROOT / zone_key
        sdir = PV_SHOTS_ROOT / zone_key
        print(f"[*] Capturando fichas Google Maps en Chrome CDP para {label}...")
        res = await capture_flagged_places(
            limit=limit_per_zone,
            only_deficient=only_deficient,
            overwrite=overwrite,
            raw_path=zdir / "apify_raw.json",
            leads_path=zdir / "leads.json",
            audits_path=zdir / "gmaps_audits.json",
            screenshots_dir=sdir,
            screenshots_rel_prefix=f"assets/gmaps_audits/puerto_vallarta/{zone_key}",
            mockups_rel_prefix=f"assets/mockups/puerto_vallarta/{zone_key}",
            territory_label=label,
            log_event=False,
        )
        results[zone_key] = res["summary"]
    return results


def _download_apify_dataset(dataset_id: str, token: str) -> list[dict[str, Any]]:
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={token}&format=json"
    with urllib.request.urlopen(urllib.request.Request(dataset_url), timeout=40) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Scraper Apify y Auditor Visual por Zonas Separadas para Puerto Vallarta.")
    parser.add_argument("--max-per-search", type=int, default=10, help="Máximo de lugares por búsqueda en Apify.")
    parser.add_argument("--skip-scrape", action="store_true", help="Reprocesa caché/apify_raw.json existente sin llamar a Apify.")
    parser.add_argument("--zones", choices=("all", "centro_y_bahia"), default="all", help="Permite ejecutar Apify+CDP solo para Centro/Bahía preservando ZR y ZH.")
    parser.add_argument("--from-datasets", nargs="+", help="Descarga dataset IDs de Apify existentes sin ejecutar nuevas corridas.")
    parser.add_argument("--skip-capture", action="store_true", help="Omite capturas Chrome CDP.")
    parser.add_argument("--all-leads", action="store_true", help="Captura todos los lugares de cada zona, no solo audit_score >= 15.")
    parser.add_argument("--limit-capture", type=int, default=None, help="Tope de capturas CDP por zona.")
    args = parser.parse_args()

    cache_path = PV_DATA_ROOT / "apify_all_raw_cache.json"
    cached = read_json(cache_path, default={}) if cache_path.exists() else {}

    if args.from_datasets:
        token = _get_apify_token()
        raw_romantica = _download_apify_dataset(args.from_datasets[0], token)
        raw_hotelera = _download_apify_dataset(args.from_datasets[1], token) if len(args.from_datasets) > 1 else []
        raw_centro = _download_apify_dataset(args.from_datasets[2], token) if len(args.from_datasets) > 2 else []
        write_json(cache_path, {"romantica": raw_romantica, "hotelera": raw_hotelera, "centro": raw_centro})
    elif not args.skip_scrape:
        token = _get_apify_token()
        if args.zones == "centro_y_bahia":
            # Keep exact pinned Phase 1 Zona Romántica (48) and Zona Hotelera (57) raw lists intact
            raw_romantica = read_json(PV_DATA_ROOT / "zona_romantica" / "apify_raw.json", default=cached.get("romantica", []))
            raw_hotelera = read_json(PV_DATA_ROOT / "zona_hotelera" / "apify_raw.json", default=cached.get("hotelera", []))
            # Include any previously excluded Centro candidates from Phase 1 cache + fresh dedicated Centro/Bahía Apify scrape
            fresh_centro = run_apify_scrape(
                CENTRO_BAHIA_QUERIES,
                zone_label="Puerto Vallarta · Centro / Bahía",
                max_per_search=args.max_per_search,
                token=token,
            )
            raw_centro = fresh_centro + list(cached.get("romantica", [])) + list(cached.get("hotelera", []))
        else:
            raw_romantica = run_apify_scrape(
                ZONA_ROMANTICA_QUERIES,
                zone_label="Puerto Vallarta · Zona Romántica",
                max_per_search=args.max_per_search,
                token=token,
            )
            raw_hotelera = run_apify_scrape(
                ZONA_HOTELERA_QUERIES,
                zone_label="Puerto Vallarta · Zona Hotelera",
                max_per_search=args.max_per_search,
                token=token,
            )
            raw_centro = run_apify_scrape(
                CENTRO_BAHIA_QUERIES,
                zone_label="Puerto Vallarta · Centro / Bahía",
                max_per_search=args.max_per_search,
                token=token,
            )
        write_json(cache_path, {"romantica": raw_romantica, "hotelera": raw_hotelera, "centro": raw_centro})
    else:
        raw_romantica = cached.get("romantica") or read_json(PV_DATA_ROOT / "zona_romantica" / "apify_raw.json", default=[])
        raw_hotelera = cached.get("hotelera") or read_json(PV_DATA_ROOT / "zona_hotelera" / "apify_raw.json", default=[])
        raw_centro = cached.get("centro") or read_json(PV_DATA_ROOT / "centro_y_bahia" / "apify_raw.json", default=[])

    territory_meta = filter_and_build_zone_datasets(raw_romantica, raw_hotelera, raw_centro)
    print("[✓] Datasets separados por zona generados:")
    print(json.dumps(territory_meta["zones"], indent=2, ensure_ascii=False))

    if not args.skip_capture:
        target_zones: tuple[str, ...] = ("centro_y_bahia",) if args.zones == "centro_y_bahia" else ("zona_romantica", "zona_hotelera", "centro_y_bahia")
        cap_res = asyncio.run(
            capture_zones_async(
                zones=target_zones,
                only_deficient=not args.all_leads,
                limit_per_zone=args.limit_capture,
            )
        )
        print("[✓] Capturas visuales Chrome CDP completadas:")
        print(json.dumps(cap_res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
