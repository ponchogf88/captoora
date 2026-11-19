#!/usr/bin/env python3
"""
CAPTOORA SPORTS // PRODUCTION APIFY GOOGLE MAPS LEAD SCRAPER
Ejecuta el actor 'compass/crawler-google-places' de Apify para extraer negocios de
Pádel, Danza/Baile, Porrismo y CrossFit en San Pedro Garza García y Monterrey.
"""

import os
from pathlib import Path
import urllib.request
import urllib.parse
import json
import time
import sys

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
API_TOKEN = os.environ.get("APIFY_TOKEN") or os.environ.get("APIFY_API_TOKEN") or ""
ACTOR_ID = "compass~crawler-google-places"

QUERIES = [
    # Tier 1: Pádel, Tenis & Clubes Deportivos
    "club de padel San Pedro Garza Garcia",
    "padel club Monterrey",
    "club deportivo Colinas de San Jeronimo Monterrey",
    # Tier 1: Baile, Danza & Señoras
    "academia de baile San Pedro Garza Garcia",
    "estudio de danza San Pedro Garza Garcia",
    "dance studio Monterrey",
    # Tier 2: Porrismo & Cheerleading
    "porristas cheerleading Monterrey",
    # Tier 2: Gimnasios, TotalPass & Rendimiento (SPGG + San Jerónimo + Obispado + Cumbres)
    "crossfit San Pedro Garza Garcia",
    "gimnasio totalpass San Jeronimo Monterrey",
    "gimnasio pilates Obispado Vista Hermosa Monterrey",
    "gimnasio Del Valle San Pedro Garza Garcia",
    # Tier 2: Colegios Privados & Jardines de Niños
    "colegio privado deportes San Pedro Garza Garcia",
    "jardin de ninos kinder San Jeronimo San Pedro Monterrey",
    "academia deportiva infantil futbol natacion San Pedro Monterrey",
    # Camino 4 · Small Business 2027 (Clínicas, Consultorios, Restaurantes/Cafés Boutique)
    "clinica dental consultorio medico San Jeronimo Obispado Monterrey",
    "clinica nutricion fisioterapia San Pedro Garza Garcia",
    "cafe restaurante boutique San Jeronimo Del Valle Monterrey",
]

SMALL_BIZ_QUERIES = [
    "clinica dental consultorio medico San Jeronimo Obispado Monterrey",
    "clinica nutricion fisioterapia San Pedro Garza Garcia",
    "jardin de ninos kinder boutique San Jeronimo San Pedro Monterrey",
    "cafe restaurante brunch San Jeronimo Del Valle Monterrey",
    "gimnasio pilates entrenamiento funcional TotalPass San Jeronimo Monterrey",
    "Deportivo San Jeronimo gym alberca Monterrey",
    "coworking estudio creadores consultoria San Pedro San Jeronimo Monterrey",
]


def start_apify_run(queries: list[str] | None = None, max_per_search: int = 8):
    selected = queries or SMALL_BIZ_QUERIES
    print(f"[*] Iniciando extracción con Apify para {len(selected)} búsquedas (max {max_per_search} c/u)...")

    payload = {
        "searchStringsArray": selected,
        "locationQuery": "Monterrey, Nuevo Leon, Mexico",
        "maxCrawledPlacesPerSearch": max_per_search,
        "language": "es",
        "includeWebResults": False,
        "scrapeDirectories": False,
        "extractPopularTimes": False,
        "exportPlaceUrls": True,
    }

    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={API_TOKEN}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        run_data = json.loads(resp.read().decode("utf-8"))
        run_id = run_data["data"]["id"]
        dataset_id = run_data["data"]["defaultDatasetId"]
        print("[✓] Run iniciado exitosamente en Apify!")
        print(f"    Run ID: {run_id}")
        print(f"    Dataset ID: {dataset_id}")
        return run_id, dataset_id


def wait_for_completion(run_id, dataset_id):
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={API_TOKEN}"
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={API_TOKEN}&format=json"

    print("[*] Esperando a que Apify recolecte los datos de Google Maps...")
    for attempt in range(30):
        time.sleep(5)
        req = urllib.request.Request(status_url)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            status = data["data"]["status"]
            print(f"    Intento {attempt + 1}: Estado actual = {status}")

            if status in ["SUCCEEDED", "READY"]:
                print("[✓] Extracción completada en Apify. Descargando dataset...")
                break
            elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                print(f"[!] El run terminó con estado: {status}")
                return None

    req_dataset = urllib.request.Request(dataset_url)
    with urllib.request.urlopen(req_dataset, timeout=30) as resp:
        items = json.loads(resp.read().decode("utf-8"))
        print(f"[✓] Se descargaron {len(items)} registros brutos de Google Maps.")
        return items


def classify_niche(name: str, category: str) -> tuple[str, str]:
    name_lower = (name or "").lower()
    cat_lower = (category or "").lower()
    if "padel" in name_lower or "pádel" in name_lower or "padel" in cat_lower or "tenis" in cat_lower:
        return (
            "Pádel & Raqueta",
            "Cobertura fotográfica de torneos de fin de semana con entrega al medio tiempo y venta de bloques acrílicos LED.",
        )
    if any(w in name_lower or w in cat_lower for w in ["dental", "dentist", "clínica", "clinica", "médico", "medico", "consultorio", "nutri", "fisioter", "dermat", "salud", "hospital"]):
        return (
            "Clínicas & Consultorios",
            "Captoora Small Business 2027: renovación de ficha Google Maps, retratos médicos de confianza y Setup Meta Business Portfolio + Biogen Beta.",
        )
    if any(w in name_lower or w in cat_lower for w in ["café", "cafe", "coffee", "restauran", "brunch", "bistro", "panader", "bakery", "cocina"]):
        return (
            "Restaurantes & Cafés Boutique",
            "Captoora Small Business 2027 (-35%): fotografía editorial de platillos y fachada en Google Maps + catálogo Meta Business sin bloqueos.",
        )
    if any(w in name_lower or w in cat_lower for w in ["kinder", "jardín", "jardin", "guarder", "preescolar", "maternal", "colegio", "instituto", "preparatoria", "prepa", "school", "liceo", "udem", "academia deportiva"]):
        return (
            "Colegios & Jardines de Niños",
            "Festivales navideños y portada institucional en Google Maps para generar confianza inmediata en familias (desde Opción 1 Digital -35%).",
        )
    if any(w in name_lower or w in cat_lower for w in ["danza", "dance", "baile", "ballet", "barre", "salsa", "ritmo"]):
        return (
            "Baile & Danza Señoras",
            "Festivales de invierno y galas: cobertura White-Glove + renovación visual Google Maps y Meta Business Portfolio.",
        )
    if any(w in name_lower or w in cat_lower for w in ["cheer", "porristas", "gimnasia", "acro"]):
        return (
            "Porrismo & Gimnasia",
            "Fotografía a 1/2000s congelando pirámides y lances en el aire. Trading cards foil y renovación de perfil Google Maps.",
        )
    if any(w in name_lower or w in cat_lower for w in ["crossfit", "hyrox", "box", "fitness", "gimnasio", "gym", "pilates", "totalpass", "entrenamiento"]):
        return (
            "Fitness & CrossFit",
            "Portada Google Maps + TotalPass profesional, sesiones HSS 1/8000s y piloto Captoora Biogen (Beta) para miembros.",
        )
    return (
        "Small Business & Comercios",
        "Captoora Small Business 2027 (-35%): fotografía pro de fachada e interiores + carga directa en Google Maps + Setup Meta Business.",
    )


def compute_audit_flags(item: dict) -> tuple[list[str], int]:
    flags: list[str] = []
    score = 0
    img_url = str(item.get("imageUrl") or "")
    imgs_count = item.get("imagesCount")
    claim_flag = bool(item.get("claimThisBusiness"))
    website = str(item.get("website") or "")
    phone = str(item.get("phone") or "")
    reviews = int(item.get("reviewsCount") or 0)

    if "streetviewpixels" in img_url.lower() or "streetview" in img_url.lower():
        flags.append("CARRITO STREET VIEW")
        score += 32
    if imgs_count is not None and int(imgs_count) == 0:
        flags.append("0 FOTOS")
        score += 35
    elif imgs_count is not None and int(imgs_count) <= 5:
        flags.append("<=5 FOTOS")
        score += 22
    if claim_flag:
        flags.append("SIN RECLAMAR")
        score += 26
    if not website or "google.com/maps" in website.lower():
        flags.append("SIN SITIO WEB")
        score += 18
    elif any(s in website.lower() for s in ("m.facebook.com", "facebook.com", "instagram.com", "wixsite.com")):
        flags.append("RED PERSONAL EN RIESGO")
        score += 15
    if not phone.strip():
        flags.append("SIN TELÉFONO")
        score += 12
    if reviews < 10:
        flags.append("POCAS RESEÑAS")
        score += 6
    return flags, min(100, score)


def process_and_save(
    items: list[dict],
    *,
    raw_cache_path: str | None = None,
):
    repo_root = Path(__file__).resolve().parent.parent
    resolved_cache = raw_cache_path or str(repo_root / "dashboard" / "data" / "apify_dataset_raw.json")
    if resolved_cache:
        try:
            with open(resolved_cache, "r", encoding="utf-8") as rf:
                existing_raw = json.load(rf)
        except Exception:
            existing_raw = []
        seen_pid = {x.get("placeId") or x.get("title") for x in existing_raw}
        merged_raw = list(existing_raw) + [x for x in items if (x.get("placeId") or x.get("title")) not in seen_pid]
        with open(resolved_cache, "w", encoding="utf-8") as wf:
            json.dump(merged_raw, wf, indent=2, ensure_ascii=False)

    leads = []
    for item in items:
        name = item.get("title")
        if not name:
            continue
        category = item.get("categoryName") or "Negocio Local"
        address = item.get("address") or "San Pedro Garza García / Monterrey, N.L."
        phone = item.get("phone") or ""
        gmaps_url = item.get("url") or "#"
        website = item.get("website") or gmaps_url or "#"
        rating = item.get("totalScore")
        reviews = int(item.get("reviewsCount") or 0)
        nicho, oportunidad = classify_niche(name, category)

        if "Santa Catarina" in address:
            municipio = "Santa Catarina"
        elif "San Pedro" in address or "Garza García" in address:
            municipio = "San Pedro Garza García"
        else:
            municipio = "Monterrey"

        addr_low = address.lower()
        if "jerónimo" in addr_low or "jeronimo" in addr_low:
            zona = "San Jerónimo"
        elif "obispado" in addr_low or "vista hermosa" in addr_low:
            zona = "Obispado / Vista Hermosa"
        elif "cumbres" in addr_low:
            zona = "Cumbres"
        elif "san pedro" in addr_low or "valle" in addr_low:
            zona = "San Pedro"
        else:
            zona = municipio

        flags, score = compute_audit_flags(item)
        leads.append({
            "nombre": name,
            "categoria": category,
            "direccion": address,
            "telefono": phone,
            "sitio_web": website,
            "gmaps_url": gmaps_url,
            "place_id": item.get("placeId") or "",
            "image_url": item.get("imageUrl") or "",
            "images_count": item.get("imagesCount"),
            "claim_this_business": bool(item.get("claimThisBusiness")),
            "has_streetview_cover": "CARRITO STREET VIEW" in flags,
            "audit_flags": flags,
            "audit_score": score,
            "rating": rating,
            "resenas": reviews,
            "municipio": municipio,
            "zona": zona,
            "nicho": nicho,
            "oportunidad_captoora": oportunidad,
        })

    output_path = str(repo_root / "dashboard" / "data" / "apify_scraped_leads.json")
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    except Exception:
        existing = []

    by_name = {str(x.get("nombre", "")).strip().lower(): idx for idx, x in enumerate(existing)}
    merged = list(existing)
    added = 0
    for l in leads:
        key = l["nombre"].strip().lower()
        if key in by_name:
            idx = by_name[key]
            # Preserve existing logo/custom notes while enriching live Google Maps audit fields
            for k in ("gmaps_url", "place_id", "image_url", "images_count", "claim_this_business", "has_streetview_cover", "audit_flags", "audit_score"):
                if l.get(k) not in (None, "", []):
                    merged[idx][k] = l[k]
        else:
            merged.append(l)
            by_name[key] = len(merged) - 1
            added += 1

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"[✓] {len(merged)} leads totales (nuevos agregados: {added}) guardados en:\n    {output_path}")
    return merged


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "small_biz"
    queries = QUERIES if mode == "all" else SMALL_BIZ_QUERIES
    run_id, dataset_id = start_apify_run(queries=queries, max_per_search=8)
    items = wait_for_completion(run_id, dataset_id)
    if items:
        process_and_save(items)
