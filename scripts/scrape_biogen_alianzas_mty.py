#!/usr/bin/env python3
"""
CAPTOORA BIOGEN 2027 // SCRAPER DE ALIANZAS EN MONTERREY Y ÁREA METROPOLITANA

Recolecta y audita dos pilares para el lanzamiento de enero 2027:
  1) Cocinas saludables, meal prep, bowls y restaurantes fitness (prioridad: marcas emergentes).
  2) Gimnasios y estudios independientes ("Captoora Biogen Club", fuera de megacadenas).

Flujo:
  - Apify ('compass~crawler-google-places') con consultas acotadas para cuidar créditos.
  - Enriquecimiento web directo (httpx) para extraer Instagram @handle, WhatsApp, email, Facebook y TikTok.
  - Auditoría de ficha Google Maps (captoora_agents.gmaps_auditor) para detectar brechas de fotografía.
  - Captura visual nativa vía Chrome CDP WebSocket (sin Playwright) para las fichas prioritarias.
"""

from __future__ import annotations

import argparse
import asyncio
import html as html_lib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import httpx

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from captoora_agents.config import now_iso, read_json, slugify, write_json
from captoora_agents.gmaps_auditor import _capture_targets_async, analyze_business_profile
from scripts.scrape_puerto_vallarta import _get_apify_token

ACTOR_ID = "compass~crawler-google-places"
RAW_OUT_PATH = ROOT_DIR / "dashboard" / "data" / "alianzas_biogen_apify_raw.json"
LEADS_OUT_PATH = ROOT_DIR / "dashboard" / "data" / "alianzas_biogen_mty.json"
SHOTS_DIR = ROOT_DIR / "assets" / "gmaps_audits" / "alianzas_biogen"

KITCHEN_QUERIES = [
    "meal prep comida saludable Monterrey",
    "comida fitness planes alimenticios Monterrey",
    "cocina saludable dietas San Pedro Garza Garcia Monterrey",
    "meal prep comida saludable San Nicolas Guadalupe Nuevo Leon",
    "restaurante saludable bowls ensaladas fitness Monterrey",
    "comida saludable por semana planes Cumbres Monterrey",
]

GYM_QUERIES = [
    "gimnasio entrenamiento funcional box San Nicolas Monterrey",
    "gimnasio crossfit independiente Guadalupe Apodaca Nuevo Leon",
    "estudio fitness entrenamiento funcional Zona Tec Sur Monterrey",
    "gimnasio pesas bodybuilding Cumbres Monterrey",
    "estudio pilates funcional boutique San Pedro Monterrey",
]

BIG_CHAINS = (
    "smart fit",
    "smartfit",
    "planet fitness",
    "anytime fitness",
    "sports world",
    "sportsworld",
    "sport city",
    "station 24",
    "station24",
    "energy fitness",
    "world gym",
    "ufc gym",
    "orangetheory",
    "f45 ",
    "power foods",
    "manzana verde",
    "green grass",
    "super salads",
    "nectarworks",
    "freshii",
    "subway",
    "starbucks",
)

NON_TARGET_FOOD_WORDS = (
    "carnicería",
    "carniceria",
    "taquería",
    "taqueria",
    "mariscos",
    "hamburgues",
    "pizza",
    "bar ",
    "cantina",
    "cervecer",
    "buffet",
    "abarrotes",
    "supermercado",
    "walmart",
    "heb ",
    "soriana",
    "oxxo",
    "7-eleven",
)

IG_RE = re.compile(r"https?://(?:www\.)?instagram\.com/([A-Za-z0-9_.]+)/?", re.I)
WA_RE = re.compile(r"https?://(?:wa\.me|api\.whatsapp\.com|chat\.whatsapp\.com)/[^\s\"'<>]+", re.I)
FB_RE = re.compile(r"https?://(?:www\.|m\.)?facebook\.com/([A-Za-z0-9_.\-/?=]+)", re.I)
TT_RE = re.compile(r"https?://(?:www\.|m\.)?tiktok\.com/@([A-Za-z0-9_.]+)", re.I)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

IGNORED_IG_HANDLES = {
    "p",
    "reel",
    "reels",
    "stories",
    "explore",
    "accounts",
    "share",
    "sharer",
    "intent",
}

IGNORED_EMAIL_DOMAINS = (
    "sentry.io",
    "wixpress.com",
    "example.com",
    "domain.com",
    "w3.org",
    "schema.org",
    "googleusercontent.com",
    "facebook.com",
    "instagram.com",
    "dominio.com",
)


def wait_and_fetch_apify_run(run_id: str, token: str) -> list[dict[str, Any]]:
    """Poll an existing Apify run until completion and download its dataset items."""
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={urllib.parse.quote(token)}"
    dataset_id = ""
    for attempt in range(120):
        with urllib.request.urlopen(status_url, timeout=20) as resp:
            run_info = json.loads(resp.read().decode("utf-8"))["data"]
        status = run_info["status"]
        dataset_id = run_info.get("defaultDatasetId") or dataset_id
        if attempt % 3 == 0 or status in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}:
            print(f"    poll {attempt + 1}: {status} (cost=${run_info.get('usageTotalUsd', 0):.3f})")
        if status == "SUCCEEDED":
            break
        if status in {"FAILED", "ABORTED", "TIMED-OUT"}:
            raise RuntimeError(f"Apify run terminó con estado {status}")
        time.sleep(5)
    else:
        raise TimeoutError(f"Apify run {run_id} excedió el tiempo de espera (10 min)")

    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={urllib.parse.quote(token)}&format=json"
    with urllib.request.urlopen(items_url, timeout=45) as resp:
        items = json.loads(resp.read().decode("utf-8"))
    print(f"[✓] Descargados {len(items)} registros brutos de Apify.")
    return items


def run_apify_queries(queries: list[str], *, max_per_search: int, token: str) -> list[dict[str, Any]]:
    """Run Apify compass~crawler-google-places once for a batch of queries."""
    payload = {
        "searchStringsArray": queries,
        "locationQuery": "Monterrey, Nuevo Leon, Mexico",
        "maxCrawledPlacesPerSearch": max_per_search,
        "language": "es",
        "includeWebResults": False,
        "scrapeDirectories": False,
        "extractPopularTimes": False,
        "exportPlaceUrls": True,
    }
    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={urllib.parse.quote(token)}"
    req = urllib.request.Request(
        start_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        run_data = json.loads(resp.read().decode("utf-8"))["data"]
    run_id = run_data["id"]
    print(f"[*] Run Apify iniciado: {run_id} (queries={len(queries)}, max_per_search={max_per_search})")
    return wait_and_fetch_apify_run(run_id, token)


def classify_pillar(item: dict[str, Any]) -> str | None:
    """Classify place into 'cocina_saludable', 'gimnasio_club', or None if off-target."""
    title = str(item.get("title") or "").lower()
    cat = str(item.get("categoryName") or "").lower()
    search_str = str(item.get("searchString") or "").lower()
    blob = f"{title} {cat} {search_str}"

    # Exclude wholesalers, event halls, equipment stores, and university campus rooms
    if any(w in title for w in ("city club", "salón pezina", "salon pezina", "distribuidor oficial", "equipos para gimnasio", "área de combates", "area de combates")):
        return None

    # Exclude individual nutritionist clinics unless they are known meal-prep brands
    is_meal_prep_brand = any(m in title for m in ("plan uno", "good foods", "fit fast", "kalana", "chuga", "macro", "meal", "salad", "bowl", "cocina", "kitchen"))
    if ("nutri" in cat or "nutriólog" in title or "nutriolog" in title or "lic." in title or "clínica" in cat or "clinica" in cat) and not is_meal_prep_brand:
        return None

    if any(w in f"{title} {cat}" for w in NON_TARGET_FOOD_WORDS):
        if not any(h in title for h in ("fit", "healthy", "salud", "meal", "bowl", "salad", "ensalad", "green", "keto", "macro")):
            return None

    if any(w in blob for w in ("gimnasio", "gym", "crossfit", "pilates", "box ", "boxeo", "entrenamiento", "fitness", "bodybuilding", "funcional", "polideportivo", "deportivo")) and not any(
        f in cat for f in ("restaurante", "comida", "café", "cafe", "cocina", "ensalad")
    ):
        return "gimnasio_club"

    if any(w in blob for w in ("meal", "comida", "cocina", "restaurante", "bowl", "ensalad", "saludable", "diet", "healthy", "keto", "fitfood", "food", "cafetería", "cafeteria")):
        return "cocina_saludable"

    return None


def infer_mty_municipality(address: str) -> str:
    low = (address or "").lower()
    for label, markers in (
        ("San Pedro Garza García", ("san pedro", "garza garcía", "garza garcia", "del valle", "valle oriente")),
        ("San Nicolás de los Garza", ("san nicolás", "san nicolas")),
        ("Guadalupe", ("guadalupe",)),
        ("Apodaca", ("apodaca",)),
        ("Santa Catarina", ("santa catarina",)),
        ("Escobedo", ("escobedo",)),
    ):
        if any(m in low for m in markers):
            return label
    return "Monterrey"


def infer_mty_zone(address: str, municipio: str) -> str:
    low = (address or "").lower()
    for label, markers in (
        ("Cumbres", ("cumbres",)),
        ("San Jerónimo / Gonzalitos", ("jerónimo", "jeronimo", "gonzalitos")),
        ("Obispado / Vista Hermosa", ("obispado", "vista hermosa")),
        ("Zona Tec / Sur", ("tecnológico", "tecnologico", "contry", "garza sada", "carretera nacional", "las torres")),
        ("Centro Monterrey", ("centro,", "barrio antiguo")),
    ):
        if any(m in low for m in markers):
            return label
    return municipio


def _extract_contacts_from_html(html: str, source_url: str) -> dict[str, Any]:
    out: dict[str, Any] = {
        "instagram_handle": "",
        "instagram_url": "",
        "whatsapp_url": "",
        "email": "",
        "facebook_url": "",
        "tiktok_handle": "",
    }
    if not html:
        return out

    # Direct IG URL check when website itself is Instagram
    if "instagram.com/" in source_url.lower():
        m = IG_RE.search(source_url)
        if m and m.group(1).lower() not in IGNORED_IG_HANDLES:
            out["instagram_handle"] = f"@{m.group(1)}"
            out["instagram_url"] = f"https://www.instagram.com/{m.group(1)}/"

    for m in IG_RE.finditer(html):
        handle = m.group(1).strip(".")
        if handle.lower() not in IGNORED_IG_HANDLES and len(handle) >= 2:
            out["instagram_handle"] = f"@{handle}"
            out["instagram_url"] = f"https://www.instagram.com/{handle}/"
            break

    wa_m = WA_RE.search(html)
    if wa_m:
        out["whatsapp_url"] = html_lib.unescape(wa_m.group(0)).split('"')[0].split("'")[0]

    fb_m = FB_RE.search(html)
    if fb_m and "sharer" not in fb_m.group(1).lower():
        out["facebook_url"] = fb_m.group(0)

    tt_m = TT_RE.search(html)
    if tt_m:
        out["tiktok_handle"] = f"@{tt_m.group(1)}"

    for em in EMAIL_RE.findall(html):
        low_em = em.lower()
        if not any(d in low_em for d in IGNORED_EMAIL_DOMAINS) and not low_em.endswith((".png", ".jpg", ".svg", ".webp")):
            out["email"] = em
            break

    return out


async def enrich_websites_async(leads: list[dict[str, Any]]) -> None:
    """Fetch public websites (and Linktree pages) concurrently to extract IG, WhatsApp, and emails."""
    sem = asyncio.Semaphore(10)
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

    async def _probe(client: httpx.AsyncClient, lead: dict[str, Any]) -> None:
        site = str(lead.get("sitio_web") or "").strip()
        if not site or "google.com/maps" in site.lower():
            return
        if "instagram.com/" in site.lower():
            m = IG_RE.search(site)
            if m and m.group(1).lower() not in IGNORED_IG_HANDLES:
                lead["instagram_handle"] = f"@{m.group(1)}"
                lead["instagram_url"] = f"https://www.instagram.com/{m.group(1)}/"
            return
        async with sem:
            try:
                resp = await client.get(site, follow_redirects=True)
                if resp.status_code < 400 and resp.text:
                    contacts = _extract_contacts_from_html(resp.text, str(resp.url))
                    for k, v in contacts.items():
                        if v and not lead.get(k):
                            lead[k] = v
            except Exception:
                pass

    async with httpx.AsyncClient(timeout=9.0, headers=headers) as client:
        await asyncio.gather(*(_probe(client, lead) for lead in leads))


def compute_biogen_fit(lead: dict[str, Any]) -> tuple[int, bool, str]:
    """
    Score how strong an emerging-brand alliance fit the lead is (0-100).
    Prioritizes independent/emerging brands over mega-chains and highlights photo-gap hooks.
    """
    name_low = lead["nombre"].lower()
    is_chain = any(c in name_low for c in BIG_CHAINS)
    reviews = int(lead.get("resenas") or 0)
    rating = float(lead.get("rating") or 0)
    flags = lead.get("audit_flags") or []

    score = 0
    reasons: list[str] = []

    if not is_chain:
        score += 25
        reasons.append("Marca independiente / en crecimiento")
    else:
        reasons.append("Cadena o marca ya consolidada")

    if 3 <= reviews <= 250:
        score += 20
        reasons.append(f"Tamaño ideal para alianza ({reviews} reseñas)")
    elif reviews > 250:
        score += 8
    else:
        score += 12
        reasons.append("Negocio muy nuevo (hambre de visibilidad)")

    if rating >= 4.4:
        score += 15
    elif rating >= 4.0:
        score += 10

    if any(f in flags for f in ("0 FOTOS", "<=5 FOTOS", "CARRITO STREET VIEW")):
        score += 20
        reasons.append("Brecha visual en Google Maps: gancho fuerte con sesión Día 1")
    elif (lead.get("images_count") or 0) < 20:
        score += 10
        reasons.append("Pocas fotos profesionales actuales")

    if lead.get("instagram_handle"):
        score += 12
        reasons.append(f"IG detectado ({lead['instagram_handle']})")
    if lead.get("telefono") or lead.get("whatsapp_url"):
        score += 8

    return min(100, score), is_chain, " · ".join(reasons)


def build_leads(raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate, classify, and analyze raw Apify items."""
    seen: set[str] = set()
    leads: list[dict[str, Any]] = []

    for item in raw_items:
        title = str(item.get("title") or "").strip()
        if not title:
            continue
        addr = str(item.get("address") or "").strip()
        if addr and not any(
            k in addr.lower()
            for k in ("nuevo león", "nuevo leon", "monterrey", "san pedro", "san nicol", "guadalupe", "apodaca", "santa catarina", "escobedo", "n.l.")
        ):
            continue

        pid = str(item.get("placeId") or "").strip()
        dedup_key = pid or f"{title.lower()}::{addr.lower()[:30]}"
        if dedup_key in seen:
            continue

        pilar = classify_pillar(item)
        if not pilar:
            continue
        seen.add(dedup_key)

        analysis = analyze_business_profile(item)
        municipio = infer_mty_municipality(addr)
        zona = infer_mty_zone(addr, municipio)
        raw_site = str(item.get("website") or "").strip()
        loc = item.get("location") if isinstance(item.get("location"), dict) else {}

        lead = {
            "slug": analysis["slug"],
            "pilar": pilar,
            "nombre": title,
            "categoria": str(item.get("categoryName") or "").strip(),
            "direccion": addr,
            "municipio": municipio,
            "zona": zona,
            "lat": loc.get("lat"),
            "lng": loc.get("lng"),
            "telefono": str(item.get("phone") or "").strip(),
            "sitio_web": raw_site,
            "gmaps_url": analysis["gmaps_url"],
            "place_id": pid,
            "rating": item.get("totalScore"),
            "resenas": int(item.get("reviewsCount") or 0),
            "images_count": item.get("imagesCount"),
            "image_url": str(item.get("imageUrl") or "").strip(),
            "claim_this_business": bool(item.get("claimThisBusiness")),
            "audit_flags": analysis["audit_flags"],
            "audit_score": analysis["audit_score"],
            "instagram_handle": "",
            "instagram_url": "",
            "whatsapp_url": "",
            "email": "",
            "facebook_url": "",
            "tiktok_handle": "",
            "search_query": str(item.get("searchString") or ""),
        }
        leads.append(lead)

    asyncio.run(enrich_websites_async(leads))

    for lead in leads:
        fit_score, is_chain, fit_reason = compute_biogen_fit(lead)
        lead["es_cadena_o_consolidada"] = is_chain
        lead["biogen_fit_score"] = fit_score
        lead["biogen_fit_reason"] = fit_reason

    leads.sort(key=lambda x: (x["es_cadena_o_consolidada"], -x["biogen_fit_score"], -(x.get("resenas") or 0)))
    return leads


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape cocinas saludables y gimnasios independientes MTY para Captoora Biogen 2027.")
    parser.add_argument("--max-per-search", type=int, default=12, help="Máximo de lugares por consulta Apify (default 12).")
    parser.add_argument("--skip-apify", action="store_true", help="Reusar RAW_OUT_PATH existente sin gastar créditos Apify.")
    parser.add_argument("--resume-run", default="", help="Reanudar espera y descarga de un Run ID existente en Apify.")
    parser.add_argument("--capture-top", type=int, default=8, help="Capturas Chrome CDP por pilar (default 8, total max 16).")
    args = parser.parse_args()

    if args.skip_apify and RAW_OUT_PATH.exists():
        raw_items = read_json(RAW_OUT_PATH, default=[])
        print(f"[*] Reusando {len(raw_items)} registros brutos desde {RAW_OUT_PATH.name}")
    elif args.resume_run:
        token = _get_apify_token()
        print(f"[*] Reanudando descarga de Run Apify existente: {args.resume_run}")
        raw_items = wait_and_fetch_apify_run(args.resume_run, token)
        write_json(RAW_OUT_PATH, raw_items)
    else:
        token = _get_apify_token()
        all_queries = KITCHEN_QUERIES + GYM_QUERIES
        raw_items = run_apify_queries(all_queries, max_per_search=args.max_per_search, token=token)
        write_json(RAW_OUT_PATH, raw_items)

    leads = build_leads(raw_items)

    # Capture Google Maps visual evidence for top emerging targets per pillar using native Chrome CDP
    if args.capture_top > 0:
        top_kitchens = [x for x in leads if x["pilar"] == "cocina_saludable" and not x["es_cadena_o_consolidada"]][: args.capture_top]
        top_gyms = [x for x in leads if x["pilar"] == "gimnasio_club" and not x["es_cadena_o_consolidada"]][: args.capture_top]
        targets = top_kitchens + top_gyms
        if targets:
            print(f"[*] Capturando {len(targets)} fichas de Google Maps con Chrome CDP nativo...")
            shots_list = asyncio.run(
                _capture_targets_async(
                    targets,
                    overwrite=False,
                    screenshots_dir=SHOTS_DIR,
                    screenshots_rel_prefix="assets/gmaps_audits/alianzas_biogen",
                )
            )
            by_slug = {r["slug"]: r for r in shots_list if r.get("path")}
            for item in leads:
                if item["slug"] in by_slug:
                    item["gmaps_screenshot"] = by_slug[item["slug"]]["path"]

    kitchens = [x for x in leads if x["pilar"] == "cocina_saludable"]
    gyms = [x for x in leads if x["pilar"] == "gimnasio_club"]

    payload = {
        "generated_at": now_iso(),
        "territory": "Monterrey y Área Metropolitana, N.L.",
        "summary": {
            "total_leads": len(leads),
            "cocinas_saludables": len(kitchens),
            "cocinas_emergentes": sum(1 for x in kitchens if not x["es_cadena_o_consolidada"]),
            "gimnasios_club": len(gyms),
            "gimnasios_independientes": sum(1 for x in gyms if not x["es_cadena_o_consolidada"]),
            "con_instagram_detectado": sum(1 for x in leads if x.get("instagram_handle")),
            "con_telefono": sum(1 for x in leads if x.get("telefono")),
            "con_brecha_fotos_gmaps": sum(
                1 for x in leads if any(f in (x.get("audit_flags") or []) for f in ("0 FOTOS", "<=5 FOTOS", "CARRITO STREET VIEW"))
            ),
        },
        "leads": leads,
    }
    write_json(LEADS_OUT_PATH, payload)
    print(f"[✓] Guardado en {LEADS_OUT_PATH}")
    print(json.dumps(payload["summary"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
