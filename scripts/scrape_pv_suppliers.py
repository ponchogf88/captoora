#!/usr/bin/env python3
"""
CAPTOORA STUDIO // AUDITOR DE PROVEEDORES LOCALES DE TALLER EN PUERTO VALLARTA

Ejecuta Apify ('compass~crawler-google-places') para localizar talleres reales en
Puerto Vallarta (corte láser/acrílico, enmarcados/molduras, carpintería fina,
imprentas gran formato, rótulos LED/3D y trofeos/grabados), verifica señales de
confiabilidad en Google Maps y captura fichas reales con Chrome CDP.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from captoora_agents.config import now_iso, read_json, slugify, write_json
from captoora_agents.gmaps_auditor import _capture_targets_async, analyze_business_profile
from scripts.scrape_puerto_vallarta import OUTSIDE_PV_KEYWORDS, _get_apify_token, run_apify_scrape

PV_DATA_ROOT = ROOT_DIR / "dashboard" / "data" / "puerto_vallarta"
SUPPLIERS_JSON = PV_DATA_ROOT / "proveedores_taller_pv.json"
SUPPLIERS_RAW_JSON = PV_DATA_ROOT / "proveedores_taller_apify_raw.json"
SUPPLIERS_SHOTS_DIR = ROOT_DIR / "assets" / "gmaps_audits" / "puerto_vallarta" / "proveedores_taller"

SUPPLIER_QUERIES = [
    "corte laser acrilico grabado Puerto Vallarta",
    "anuncios luminosos letras 3D LED Puerto Vallarta",
    "enmarcado marcos cuadros molduras Puerto Vallarta",
    "imprenta gran formato impresion digital Puerto Vallarta",
    "carpinteria ebanisteria madera fina parota Puerto Vallarta",
    "trofeos reconocimientos placas grabadas Puerto Vallarta",
    "router CNC rotulacion taller publicidad Puerto Vallarta",
]


def classify_supplier_specialty(name: str, category: str) -> str:
    joined = f"{name} {category}".lower()
    if any(k in joined for k in ("enmarcad", "marco", "moldura", "cuadro", "galer")):
        return "Enmarcados & Molduras Fine Art"
    if any(k in joined for k in ("láser", "laser", "cnc", "acrílic", "acrilic", "plasma", "grabado", "trofeo", "placa")):
        return "Corte Láser, CNC & Acrílico"
    if any(k in joined for k in ("luminos", "led", "neón", "neon", "rótulo", "rotul", "anuncio", "letrero", "3d")):
        return "Letreros LED, Rótulos & 3D"
    if any(k in joined for k in ("carpinter", "ebanist", "parota", "madera", "mueble")):
        return "Carpintería & Madera Fina (Nogal/Parota)"
    return "Imprenta Editorial & Gran Formato"


def classify_pv_corridor(address: str, lat: float | None = None) -> str:
    low = (address or "").lower()
    if any(k in low for k in ("48380", "zona romántica", "zona romantica", "olas altas")) or (
        lat is not None and 20.594 <= lat <= 20.606
    ):
        return "Zona Romántica"
    if any(k in low for k in ("valentín gómez", "valentin gomez", "48320", "pitillal", "48290", "coapinole", "bobadilla", "48298")):
        return "Corredor Industrial / Comercial El Pitillal"
    if any(k in low for k in ("zona hotelera", "las glorias", "versalles", "fluvial", "aramara", "gaviotas", "francisco villa", "guadalupe victoria", "48310", "48312", "48314", "48317", "48328", "48330", "48333")):
        return "Zona Hotelera / Corredor Versalles–Francisco Villa"
    if any(k in low for k in ("las juntas", "48291", "mojoneras", "ixtapa")):
        return "Corredor Norte (Las Juntas / Bodegas)"
    if any(k in low for k in ("5 de diciembre", "centro,", "48300", "48350")):
        return "Centro / Col. 5 de Diciembre"
    return "Centro / Área Urbana Puerto Vallarta"


def score_supplier_reliability(item: dict[str, Any]) -> tuple[int, str, list[str]]:
    """
    Evaluate workshop reliability signals: reviews volume, rating, active website, phone, and photo evidence.
    Higher score = stronger online verification; low score != bad workshop, means physical audit needed.
    """
    rating = float(item.get("totalScore") or item.get("rating") or 0)
    reviews = int(item.get("reviewsCount") or item.get("resenas") or 0)
    website = str(item.get("website") or item.get("sitio_web") or "").strip()
    phone = str(item.get("phone") or item.get("telefono") or "").strip()
    imgs = int(item.get("imagesCount") or item.get("images_count") or 0)
    claimed = not bool(item.get("claimThisBusiness") if "claimThisBusiness" in item else item.get("claim_this_business"))

    score = 0
    notes: list[str] = []
    if reviews >= 50:
        score += 30
        notes.append(f"{reviews} reseñas verificadas")
    elif reviews >= 15:
        score += 20
        notes.append(f"{reviews} reseñas locales")
    elif reviews >= 3:
        score += 10
        notes.append(f"Pocas reseñas ({reviews}): validar muestras en persona")
    else:
        notes.append("Sin historial digital suficiente: auditoría presencial obligatoria")

    if rating >= 4.5:
        score += 25
    elif rating >= 4.0:
        score += 15
    elif rating > 0:
        score += 5

    if website and "google.com/maps" not in website.lower():
        score += 15
        notes.append("Sitio/portafolio web activo")
    if phone:
        score += 15
    if imgs >= 10:
        score += 10
        notes.append(f"{imgs} fotos de trabajos")
    if claimed:
        score += 5
    else:
        notes.append("Ficha sin reclamar (verificar horario/existencia antes de ir)")

    if score >= 75:
        tier = "Tier A · Confiable Verificado (Prioridad Cotización)"
    elif score >= 50:
        tier = "Tier B · Confiable Condicional (Validar Muestras y SLA)"
    else:
        tier = "Tier C · Presencial / Bajo Radar (Inspección Física Requerida)"
    return min(100, score), tier, notes


def process_suppliers(raw_items: list[dict[str, Any]]) -> dict[str, Any]:
    dedup: dict[str, dict[str, Any]] = {}
    excluded: list[dict[str, Any]] = []

    for item in raw_items:
        title = str(item.get("title") or "").strip()
        address = str(item.get("address") or "").strip()
        if not title:
            continue
        addr_low = address.lower()
        # Exclude Riviera Nayarit / Bucerías / Nuevo Vallarta per strict PV-only boundary
        if any(k in addr_low for k in OUTSIDE_PV_KEYWORDS if k not in ("ixtapa", "las juntas")):
            excluded.append({"nombre": title, "direccion": address, "razon": "Fuera de Puerto Vallarta (Nayarit)"})
            continue
        if "puerto vallarta" not in addr_low and "jal." not in addr_low and "jalisco" not in addr_low and "483" not in addr_low and "482" not in addr_low:
            excluded.append({"nombre": title, "direccion": address, "razon": "Fuera de Puerto Vallarta"})
            continue

        pid = str(item.get("placeId") or "").strip() or title.lower()
        if pid in dedup:
            continue

        loc = item.get("location") if isinstance(item.get("location"), dict) else {}
        lat = float(loc["lat"]) if loc.get("lat") is not None else None
        lng = float(loc["lng"]) if loc.get("lng") is not None else None

        analysis = analyze_business_profile({**item, "municipio": "Puerto Vallarta"})
        specialty = classify_supplier_specialty(title, str(item.get("categoryName") or ""))
        corridor = classify_pv_corridor(address, lat=lat)
        rel_score, tier, rel_notes = score_supplier_reliability(item)
        slug = slugify(title)
        shot_abs = SUPPLIERS_SHOTS_DIR / f"{slug}.png"
        shot_rel = f"assets/gmaps_audits/puerto_vallarta/proveedores_taller/{slug}.png"

        dedup[pid] = {
            "slug": slug,
            "nombre": title,
            "categoria": item.get("categoryName") or "Taller / Proveedor",
            "especialidad": specialty,
            "corredor": corridor,
            "direccion": address,
            "telefono": item.get("phone") or "",
            "sitio_web": item.get("website") or "",
            "gmaps_url": analysis["gmaps_url"],
            "place_id": item.get("placeId") or "",
            "rating": item.get("totalScore"),
            "resenas": int(item.get("reviewsCount") or 0),
            "images_count": item.get("imagesCount"),
            "claim_this_business": bool(item.get("claimThisBusiness")),
            "reliability_score": rel_score,
            "reliability_tier": tier,
            "reliability_notes": rel_notes,
            "lat": lat,
            "lng": lng,
            "screenshot_path": shot_rel if (shot_abs.exists() and shot_abs.stat().st_size > 10_000) else "",
        }

    suppliers = sorted(
        dedup.values(),
        key=lambda x: (x["reliability_score"], x["resenas"], float(x["rating"] or 0)),
        reverse=True,
    )

    payload = {
        "updated_at": now_iso(),
        "territory": "Puerto Vallarta, Jalisco (Solo PV)",
        "total_suppliers": len(suppliers),
        "tier_a_count": sum(1 for s in suppliers if s["reliability_score"] >= 75),
        "tier_b_count": sum(1 for s in suppliers if 50 <= s["reliability_score"] < 75),
        "tier_c_count": sum(1 for s in suppliers if s["reliability_score"] < 50),
        "excluded_out_of_pv": excluded,
        "field_audit_checklist_off_internet": [
            "1. Maquinaria propia vs revendedor: pedir ver el láser CO2 / router CNC / sierra de inglete operando en el local (muchos locales en Zona Centro solo revenden y subcontratan con sobreprecio o retraso).",
            "2. Espesor y pureza de acrílico: exigir acrílico cast (vaciado) óptico de 6mm a 10mm transparente cristal sin tintes verdosos ni bordes quemados; rechazar acrílico extruido delgado de souvenir (2–3mm).",
            "3. Madera resistente a humedad costera de Vallarta: validar parota, nogal o rosa morada estufada y sellada con poliuretano mate (el MDF sin sellado se hincha con la brisa marina).",
            "4. Electrónica LED cálida (2700K–3000K): probar encendido continuo, soldadura limpia en base de madera, conector USB-C / eliminador 12V seguro y luz uniforme sin puntos calientes.",
            "5. Prueba de muestra pagada antes de lote: jamás pagar 100% por adelantado en un taller sin historial; producir 1 pieza muestra calibrada (pago contra muestra) y pactar SLA por escrito (máx. 3–5 días hábiles).",
            "6. Zonas clave para caminar talleres fuera de Google Maps: Av. Francisco Villa (tramo Versalles a Libramiento), calle Ecuador / Colombia en Col. 5 de Diciembre, Av. Grandes Lagos / Fluvial-Pitillal y carretera a Las Juntas.",
        ],
        "anti_cheap_souvenir_strategy": {
            "regla_central": "Captoora jamás compite contra souvenirs turísticos baratos de Malecón o tianguis ($80–$250 MXN). Vendemos dirección visual editorial + piezas B2B de alto estatus con margen >= 70%.",
            "reglas_de_empaquetado": [
                "Nunca cotices un trofeo o placa acrílica suelta sin la producción fotográfica o el paquete editorial; el artículo físico es un multiplicador de estatus y reseñas (QR LED en recepción/barra o premiación de torneo).",
                "Diferencia el material al instante: acrílico óptico grueso 8–10mm grabado a precisión + base sólida de parota/nogal + luz LED cálida vs llaveros o acrílico delgado de 3mm de recuerdo turístico.",
                "Siempre cobra la fase digital primero (48–72h o mismo día en evento) y ofrece las piezas de taller como Fase 2 opcional (3–5 días hábiles), protegiendo flujo de caja y evitando depender de urgencias de maquila.",
                "Para eventos de alto ticket (Torneo Pádel 233, Golf Pro-Am, cenas VIP Festival Gourmet, posadas de hoteles), vende las placas LED con espacio para logo de patrocinador para que el patrocinador cubra el costo.",
            ],
        },
        "suppliers": suppliers,
    }
    write_json(SUPPLIERS_JSON, payload)
    return payload


async def capture_suppliers_screenshots(suppliers: list[dict[str, Any]], *, limit: int | None = None, overwrite: bool = False) -> list[dict[str, Any]]:
    targets = suppliers[:limit] if limit else suppliers
    return await _capture_targets_async(
        targets,
        overwrite=overwrite,
        screenshots_dir=SUPPLIERS_SHOTS_DIR,
        screenshots_rel_prefix="assets/gmaps_audits/puerto_vallarta/proveedores_taller",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extractor Apify y Auditor Chrome CDP de Proveedores de Taller en Puerto Vallarta.")
    parser.add_argument("--max-per-search", type=int, default=8)
    parser.add_argument("--skip-scrape", action="store_true")
    parser.add_argument("--skip-capture", action="store_true")
    parser.add_argument("--limit-capture", type=int, default=30)
    args = parser.parse_args()

    if not args.skip_scrape:
        token = _get_apify_token()
        raw_items = run_apify_scrape(
            SUPPLIER_QUERIES,
            zone_label="Puerto Vallarta · Proveedores Taller",
            max_per_search=args.max_per_search,
            token=token,
        )
        write_json(SUPPLIERS_RAW_JSON, raw_items)
    else:
        raw_items = read_json(SUPPLIERS_RAW_JSON, default=[])

    payload = process_suppliers(raw_items)
    print(f"[✓] Proveedores PV procesados: {payload['total_suppliers']} (Tier A: {payload['tier_a_count']}, Tier B: {payload['tier_b_count']}, Tier C: {payload['tier_c_count']})")

    if not args.skip_capture and payload["suppliers"]:
        asyncio.run(capture_suppliers_screenshots(payload["suppliers"], limit=args.limit_capture))
        payload = process_suppliers(raw_items)
        captured_total = sum(1 for s in payload["suppliers"] if s.get("screenshot_path"))
        print(f"[✓] Capturas Chrome CDP de proveedores completadas: {captured_total}/{payload['total_suppliers']}")


if __name__ == "__main__":
    main()
