#!/usr/bin/env python3
"""
CAPTOORA STUDIO // GENERADOR DE MAPEADOS SEPARADOS POR ZONA (PUERTO VALLARTA)

Lee únicamente los archivos separados de:
  - dashboard/data/puerto_vallarta/zona_romantica/gmaps_audits.json
  - dashboard/data/puerto_vallarta/zona_hotelera/gmaps_audits.json
  - dashboard/data/puerto_vallarta/centro_y_bahia/gmaps_audits.json

Genera por separado (sin mezclar zonas ni Nuevo León):
  - docs/MAPEADO_PV_ZONA_ROMANTICA.md
  - docs/MAPEADO_PV_ZONA_HOTELERA.md
  - docs/MAPEADO_PV_CENTRO_Y_BAHIA.md
  - docs/puerto_vallarta_zona_romantica.html
  - docs/puerto_vallarta_zona_hotelera.html
  - docs/puerto_vallarta_centro_bahia.html
  - docs/demos_pv/{zona}/{slug}.html (Prototipo Web Express + Checklist GBP -35% por negocio)
"""

from __future__ import annotations

import html
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from captoora_agents.config import now_iso, read_json, slugify, validate_client_copy, write_json
from captoora_agents.mockups import (
    build_gbp_optimization_checklist,
    build_smb_landing_prototype_html,
)

PV_DATA_ROOT = ROOT_DIR / "dashboard" / "data" / "puerto_vallarta"
DOCS_DIR = ROOT_DIR / "docs"
DEMOS_DIR = DOCS_DIR / "demos_pv"

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

ZONE_SPECS: list[dict[str, str]] = [
    {
        "key": "zona_romantica",
        "title": "Zona Romántica",
        "subtitle": "Emiliano Zapata · Olas Altas · Basilio Badillo · Playa Los Muertos",
        "html_filename": "puerto_vallarta_zona_romantica.html",
        "md_filename": "MAPEADO_PV_ZONA_ROMANTICA.md",
        "events_html": "puerto_vallarta_eventos_zona_romantica.html",
    },
    {
        "key": "zona_hotelera",
        "title": "Zona Hotelera",
        "subtitle": "Zona Hotelera Norte · Las Glorias · Marina Vallarta · Zona Hotelera Sur",
        "html_filename": "puerto_vallarta_zona_hotelera.html",
        "md_filename": "MAPEADO_PV_ZONA_HOTELERA.md",
        "events_html": "puerto_vallarta_eventos_zona_hotelera.html",
    },
    {
        "key": "centro_y_bahia",
        "title": "Centro / Bahía",
        "subtitle": "Centro Histórico 48300 · Malecón · Isla Río Cuale · Gringo Gulch · 5 de Diciembre",
        "html_filename": "puerto_vallarta_centro_bahia.html",
        "md_filename": "MAPEADO_PV_CENTRO_Y_BAHIA.md",
        "events_html": "puerto_vallarta_eventos_centro_bahia.html",
    },
]


def _assert_clean_pv_outreach(audits: list[dict[str, Any]], context: str) -> None:
    for item in audits:
        for mode_name, text in (item.get("outreach_modes") or {}).items():
            violations = validate_client_copy(text)
            if violations:
                raise ValueError(f"Guardrail Captoora bloqueó {context} ({item.get('nombre')} · {mode_name}): {violations}")
            low = text.lower()
            for term in FORBIDDEN_ORIGIN_TERMS:
                if term in low:
                    raise ValueError(
                        f"Referencia geográfica de origen no permitida ('{term}') detectada en {context} ({item.get('nombre')})"
                    )


def _clean_wa_digits(phone: str) -> str:
    digits = "".join(ch for ch in (phone or "") if ch.isdigit())
    if len(digits) == 10:
        return f"52{digits}"
    return digits


def _generate_zone_prototypes(
    zone_key: str,
    audits: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    """Build personalized Web Express HTML prototypes & GBP checklists for every prospect in a zone."""
    zone_demo_dir = DEMOS_DIR / zone_key
    zone_demo_dir.mkdir(parents=True, exist_ok=True)
    checklists_by_slug: dict[str, dict[str, Any]] = {}
    demo_rel_by_slug: dict[str, str] = {}

    for rec in audits:
        slug = str(rec.get("slug") or slugify(rec.get("nombre") or "negocio"))
        checklist = build_gbp_optimization_checklist(rec)
        proto_html = build_smb_landing_prototype_html(
            rec,
            assets_prefix="../../../assets",
            gbp_checklist=checklist,
        )
        out_path = zone_demo_dir / f"{slug}.html"
        out_path.write_text(proto_html, encoding="utf-8")
        checklists_by_slug[slug] = checklist
        demo_rel_by_slug[slug] = f"demos_pv/{zone_key}/{slug}.html"

    return checklists_by_slug, demo_rel_by_slug


def _render_zone_markdown(
    zone_key: str,
    zone_title: str,
    subtitle: str,
    index: dict[str, Any],
    checklists: dict[str, dict[str, Any]],
    demo_rels: dict[str, str],
) -> str:
    audits: list[dict[str, Any]] = index.get("audits", [])
    _assert_clean_pv_outreach(audits, f"markdown {zone_key}")
    by_niche = Counter(a.get("nicho") or "Sin Clasificar" for a in audits)
    by_subzona = Counter(a.get("subzona") or zone_title for a in audits)
    by_flag = Counter(f for a in audits for f in (a.get("audit_flags") or []))
    no_web_count = sum(
        1 for a in audits if (checklists.get(a.get("slug", ""), {}).get("website_status") in {"sin_web", "solo_red_social"})
    )

    lines: list[str] = [
        f"# Mapeado Comercial, Auditoría Google Business Profile y Prototipos Web · Puerto Vallarta — {zone_title}",
        "",
        f"> **Territorio aislado:** `{zone_title}` (`{subtitle}`) · **Actualizado:** `{index.get('updated_at', now_iso())}`  ",
        "> **Posicionamiento Captoora Studio:** Enfoque en portafolio, resultados visuales, estilo editorial, actualización Google Business Profile + Página Web Express (Entrega digital 48–72h / mismo día en eventos · Piezas físicas LED QR en taller artesanal: 3–5 días hábiles).",
        "",
        "## 1. Resumen Ejecutivo de la Zona",
        "",
        f"- **Total de prospectos mapeados en {zone_title}:** `{len(audits)}`",
        f"- **Sin Sitio Web Propio o Solo Red Social (Prioridad Web Express + GBP):** `{no_web_count}`",
        f"- **Con oportunidad visual priorizada (`audit_score >= 15`):** `{index.get('deficient_count', 0)}`",
        f"- **Capturas reales verificadas en Chrome CDP:** `{index.get('captured_count', 0)}`",
        f"- **Portada automática Street View (`CARRITO STREET VIEW`):** `{index.get('streetview_count', 0)}`",
        f"- **Fichas sin reclamar (`SIN RECLAMAR`):** `{index.get('unclaimed_count', 0)}`",
        f"- **Prototipos Web Express generados listos para abrir:** `{len(demo_rels)}`",
        "",
        "### Distribución por Subzona",
        "",
        "| Subzona / Corredor | Prospectos |",
        "| :--- | ---: |",
    ]
    for sz, cnt in by_subzona.most_common():
        lines.append(f"| {sz} | {cnt} |")

    lines.extend(
        [
            "",
            "### Distribución por Giro / Nicho",
            "",
            "| Nicho Captoora | Cantidad |",
            "| :--- | ---: |",
        ]
    )
    for nicho, cnt in by_niche.most_common():
        lines.append(f"| {nicho} | {cnt} |")

    lines.extend(
        [
            "",
            "### Banderas de Dolor Visual & Perfil de Negocio Detectadas",
            "",
            "| Bandera de Auditoría | Negocios Afectados |",
            "| :--- | ---: |",
        ]
    )
    for flag, cnt in by_flag.most_common():
        lines.append(f"| `{flag}` | {cnt} |")

    lines.extend(
        [
            "",
            "---",
            "",
            f"## 2. Inventario Mapeado por Nicho ({zone_title})",
            "",
        ]
    )

    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in audits:
        grouped.setdefault(item.get("nicho") or "Small Business & Comercios", []).append(item)

    for nicho, items in sorted(grouped.items(), key=lambda kv: len(kv[1]), reverse=True):
        lines.append(f"### {nicho} ({len(items)})")
        lines.append("")
        lines.append(
            "| # | Negocio | Subzona | Score | Web Actual | Banderas Google Maps | Rating | Teléfono | Demo Web & Maps |"
        )
        lines.append("|---:|---|---|---:|---|---|---|---|---|")
        for idx, item in enumerate(items, start=1):
            slug = str(item.get("slug") or slugify(item.get("nombre") or "negocio"))
            nombre = str(item.get("nombre") or "").replace("|", "/")
            subzona = str(item.get("subzona") or zone_title).replace("|", "/")
            score = item.get("audit_score", 0)
            chk = checklists.get(slug, {})
            wstatus = chk.get("website_status", "mejorable")
            wlabel = (
                "Sin Web"
                if wstatus == "sin_web"
                else ("Solo Red Social" if wstatus == "solo_red_social" else "Web Propia")
            )
            flags_str = ", ".join(item.get("audit_flags") or []) or "Ficha sólida (upsell editorial)"
            rating = item.get("rating")
            resenas = item.get("resenas", 0)
            rating_str = f"{rating} ★ ({resenas})" if rating is not None else f"N/A ({resenas})"
            phone = str(item.get("telefono") or "Sin teléfono")
            gmaps_url = item.get("gmaps_url") or "#"
            shot = item.get("screenshot_path") or ""
            demo_rel = demo_rels.get(slug, "")
            demo_md = f"[Web Demo]({demo_rel})" if demo_rel else "—"
            shot_md = f"[Captura](../{shot})" if shot else "Sin captura"
            lines.append(
                f"| {idx} | **{nombre}** | {subzona} | {score}/100 | {wlabel} | {flags_str} | {rating_str} | {phone} | {demo_md} · [Maps]({gmaps_url}) · {shot_md} |"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def _render_zone_html(
    zone_spec: dict[str, str],
    index: dict[str, Any],
    checklists: dict[str, dict[str, Any]],
    demo_rels: dict[str, str],
) -> str:
    zone_key = zone_spec["key"]
    zone_title = zone_spec["title"]
    subtitle = zone_spec["subtitle"]
    audits: list[dict[str, Any]] = index.get("audits", [])
    _assert_clean_pv_outreach(audits, f"html {zone_key}")

    records_payload: list[dict[str, Any]] = []
    no_web_total = 0
    for a in audits:
        slug = str(a.get("slug") or slugify(a.get("nombre") or "negocio"))
        chk = checklists.get(slug) or build_gbp_optimization_checklist(a)
        wstatus = chk.get("website_status", "mejorable")
        if wstatus in {"sin_web", "solo_red_social"}:
            no_web_total += 1
        nombre = a.get("nombre", "")
        subzona = a.get("subzona", "") or zone_title
        urgent_n = chk.get("urgent_count", 0)
        web_msg_mode = (
            f"Hola equipo de {nombre} 👋, soy Jesús Gutiérrez de Captoora Studio (Portafolio: https://captoora.studio/sports).\n\n"
            f"Detectamos su ficha en Google Maps en {subzona} ({chk.get('headline_diagnosis', '')}) y preparamos sin costo una vista previa de cómo quedaría su nueva Página Web Express conectada directo a su ficha Google Business Profile ({urgent_n} mejoras clave listas para aplicar en 48–72h con -35% de temporada).\n\n"
            f"¿Te comparto el enlace de su prototipo web y checklist de Google Maps ahorita?"
        )
        if validate_client_copy(web_msg_mode):
            raise ValueError(f"Guardrail bloqueó guion Web+GBP para {nombre}")

        modes = dict(a.get("outreach_modes") or {})
        modes["mode_d_web_gbp"] = web_msg_mode
        records_payload.append(
            {
                "slug": slug,
                "nombre": nombre,
                "categoria": a.get("categoria", ""),
                "nicho": a.get("nicho", ""),
                "subzona": subzona,
                "direccion": a.get("direccion", ""),
                "telefono": a.get("telefono", ""),
                "wa_digits": _clean_wa_digits(a.get("telefono", "")),
                "sitio_web": a.get("sitio_web", ""),
                "gmaps_url": a.get("gmaps_url", ""),
                "rating": a.get("rating"),
                "resenas": a.get("resenas", 0),
                "images_count": a.get("images_count"),
                "claim_this_business": bool(a.get("claim_this_business")),
                "has_streetview_cover": bool(a.get("has_streetview_cover")),
                "audit_flags": a.get("audit_flags", []),
                "audit_score": a.get("audit_score", 0),
                "client_observations": a.get("client_observations", []),
                "screenshot_rel": f"../{a['screenshot_path']}" if a.get("screenshot_path") else "",
                "demo_web_rel": demo_rels.get(slug, ""),
                "website_status": wstatus,
                "gbp_checklist": chk,
                "outreach_modes": modes,
                "lat": a.get("lat"),
                "lng": a.get("lng"),
            }
        )

    safe_audits_json = json.dumps(records_payload, ensure_ascii=False).replace("</", "<\\/")
    niches = sorted({a.get("nicho") or "Small Business & Comercios" for a in audits})
    subzones = sorted({a.get("subzona") or zone_title for a in audits})

    niche_options = "".join(f'<option value="{html.escape(n)}">{html.escape(n)}</option>' for n in niches)
    subzone_options = "".join(f'<option value="{html.escape(s)}">{html.escape(s)}</option>' for s in subzones)

    zone_nav_pills = "".join(
        f'<a class="zone-pill {"active" if zs["key"] == zone_key else ""}" href="{html.escape(zs["html_filename"])}">{html.escape(zs["title"])}</a>'
        for zs in ZONE_SPECS
    )

    page_html = f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Captoora Studio · Mapeado Google Maps, Web Express &amp; GBP PV — {html.escape(zone_title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: #07060b;
      --card: #101018;
      --surface: #171724;
      --gold: #d4af37;
      --champagne: #e8d5a8;
      --volt: #c6ff00;
      --danger: #ff6b6b;
      --text: #f5f4f8;
      --muted: #9c9aa8;
      --border: rgba(255, 255, 255, 0.1);
    }}
    body {{
      background: radial-gradient(circle at 85% 0%, rgba(198,255,0,0.06), transparent 36%),
                  radial-gradient(circle at 10% 10%, rgba(212,175,55,0.08), transparent 40%),
                  var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      line-height: 1.5;
      padding: 28px 20px 64px;
    }}
    .wrap {{ max-width: 1340px; margin: 0 auto; }}
    .topbar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-end;
      gap: 16px;
      padding-bottom: 18px;
      border-bottom: 1px solid rgba(212, 175, 55, 0.35);
      margin-bottom: 22px;
    }}
    .brand-eyebrow {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      letter-spacing: 0.16em;
      color: var(--volt);
      text-transform: uppercase;
    }}
    h1 {{
      font-family: 'Cinzel', serif;
      font-size: clamp(1.45rem, 3vw, 2.25rem);
      color: #fff;
      margin-top: 4px;
    }}
    .subtitle {{ color: var(--muted); font-size: 0.9rem; margin-top: 4px; }}
    .nav-cluster {{ display: flex; flex-direction: column; gap: 8px; align-items: flex-end; }}
    @media (max-width: 900px) {{ .nav-cluster {{ align-items: flex-start; }} }}
    .zone-pills {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .zone-pill {{
      padding: 8px 14px;
      border-radius: 999px;
      border: 1px solid rgba(212, 175, 55, 0.38);
      background: rgba(212, 175, 55, 0.06);
      color: var(--champagne);
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 700;
    }}
    .zone-pill.active {{
      background: var(--volt);
      color: #090b10;
      border-color: var(--volt);
    }}
    .hub-links {{ display: flex; flex-wrap: wrap; gap: 10px; font-size: 0.78rem; }}
    .hub-links a {{ color: var(--champagne); text-decoration: none; border-bottom: 1px dashed rgba(212,175,55,0.45); }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}
    .kpi {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px 16px;
    }}
    .kpi-val {{ font-size: 1.65rem; font-weight: 800; color: #fff; font-family: 'JetBrains Mono', monospace; }}
    .kpi-val.volt {{ color: var(--volt); }}
    .kpi-val.gold {{ color: var(--gold); }}
    .kpi-label {{ font-size: 0.74rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px; }}
    .controls {{
      display: grid;
      grid-template-columns: 1.45fr 1fr 1fr 1.15fr;
      gap: 10px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px;
      margin-bottom: 18px;
    }}
    @media (max-width: 900px) {{ .controls {{ grid-template-columns: 1fr; }} }}
    input, select {{
      width: 100%;
      background: var(--surface);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
      font-size: 0.86rem;
      font-family: inherit;
    }}
    .results-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 14px;
      color: var(--muted);
      font-size: 0.84rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 16px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .shot-wrap {{
      position: relative;
      height: 195px;
      background: #090910;
      border-bottom: 1px solid var(--border);
      cursor: pointer;
      overflow: hidden;
    }}
    .shot-wrap img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: left top;
      display: block;
    }}
    .shot-empty {{
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--muted);
      font-size: 0.8rem;
      padding: 16px;
      text-align: center;
    }}
    .score-pill {{
      position: absolute;
      top: 10px;
      right: 10px;
      background: rgba(7, 6, 11, 0.9);
      border: 1px solid var(--volt);
      color: var(--volt);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.71rem;
      font-weight: 700;
      padding: 4px 9px;
      border-radius: 999px;
    }}
    .web-pill {{
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(7, 6, 11, 0.9);
      border: 1px solid rgba(255,107,107,0.65);
      color: #ffb3b3;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      font-weight: 700;
      padding: 4px 9px;
      border-radius: 999px;
    }}
    .web-pill.ok {{ border-color: rgba(212,175,55,0.55); color: var(--champagne); }}
    .card-body {{ padding: 16px; display: flex; flex-direction: column; gap: 8px; flex: 1; }}
    .card-top {{ display: flex; justify-content: space-between; gap: 10px; align-items: flex-start; }}
    .card-title {{ font-size: 1.02rem; font-weight: 700; color: #fff; }}
    .subzona-tag {{
      font-size: 0.69rem;
      background: rgba(212,175,55,0.12);
      border: 1px solid rgba(212,175,55,0.35);
      color: var(--champagne);
      padding: 3px 8px;
      border-radius: 999px;
      white-space: nowrap;
    }}
    .meta-line {{ font-size: 0.8rem; color: var(--muted); }}
    .meta-line strong {{ color: #d8d6e2; }}
    .flags {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 2px; }}
    .flag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      padding: 3px 8px;
      border-radius: 6px;
      background: rgba(255, 107, 107, 0.12);
      border: 1px solid rgba(255, 107, 107, 0.35);
      color: #ffb3b3;
    }}
    .flag.ok {{
      background: rgba(198,255,0,0.08);
      border-color: rgba(198,255,0,0.35);
      color: var(--volt);
    }}
    .obs {{
      font-size: 0.79rem;
      color: #d7d4c9;
      background: rgba(255,255,255,0.03);
      border-left: 3px solid var(--gold);
      padding: 8px 10px;
      border-radius: 6px;
    }}
    .card-actions {{
      padding: 12px 16px;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .btn {{
      font-size: 0.75rem;
      font-weight: 700;
      padding: 7px 11px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      text-decoration: none;
      cursor: pointer;
    }}
    .btn.primary {{
      background: var(--volt);
      color: #090b10;
      border-color: var(--volt);
    }}
    .btn.gold {{
      border-color: rgba(212,175,55,0.5);
      color: var(--champagne);
    }}
    dialog {{
      margin: auto;
      background: var(--card);
      color: var(--text);
      border: 1px solid rgba(212,175,55,0.45);
      border-radius: 16px;
      max-width: 860px;
      width: 92vw;
      padding: 20px;
    }}
    dialog::backdrop {{ background: rgba(0, 0, 0, 0.8); }}
    textarea {{
      width: 100%;
      min-height: 220px;
      background: var(--surface);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px;
      font-family: inherit;
      font-size: 0.85rem;
      margin: 10px 0;
    }}
    .gbp-list {{ list-style: none; display: flex; flex-direction: column; gap: 8px; margin: 12px 0; max-height: 55vh; overflow-y: auto; }}
    .gbp-item {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 3px solid var(--gold);
      border-radius: 10px;
      padding: 10px 12px;
      font-size: 0.84rem;
    }}
    .gbp-item.crit {{ border-left-color: var(--volt); }}
    .gbp-badge {{ font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; padding: 2px 6px; border-radius: 999px; background: rgba(198,255,0,0.14); color: var(--volt); margin-right: 6px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <div>
        <div class="brand-eyebrow">CAPTOORA STUDIO · GOOGLE MAPS + PROTOTIPOS WEB EXPRESS + ACTUALIZACIÓN GBP</div>
        <h1>Puerto Vallarta — {html.escape(zone_title)}</h1>
        <p class="subtitle">{html.escape(subtitle)} · Zona 100% separada de otras áreas PV.</p>
      </div>
      <div class="nav-cluster">
        <div class="zone-pills">{zone_nav_pills}</div>
        <div class="hub-links">
          <a href="{html.escape(zone_spec['events_html'])}">Eventos &amp; Posadas de {html.escape(zone_title)} &rarr;</a>
          <a href="puerto_vallarta_influencers_y_cobertura.html">Influencers PV &rarr;</a>
          <a href="puerto_vallarta_proveedores_taller.html">Proveedores Taller PV &rarr;</a>
        </div>
      </div>
    </header>

    <section class="kpi-grid">
      <div class="kpi"><div class="kpi-val">{len(audits)}</div><div class="kpi-label">Prospectos en {html.escape(zone_title)}</div></div>
      <div class="kpi"><div class="kpi-val volt">{no_web_total}</div><div class="kpi-label">Sin Web / Solo Red Social</div></div>
      <div class="kpi"><div class="kpi-val gold">{index.get('deficient_count', 0)}</div><div class="kpi-label">Oportunidad Visual (&ge;15 pts)</div></div>
      <div class="kpi"><div class="kpi-val">{index.get('captured_count', 0)}/{len(audits)}</div><div class="kpi-label">Capturas Maps Verificadas</div></div>
      <div class="kpi"><div class="kpi-val">{index.get('streetview_count', 0)}</div><div class="kpi-label">Portada Street View</div></div>
      <div class="kpi"><div class="kpi-val">{index.get('unclaimed_count', 0)}</div><div class="kpi-label">Sin Reclamar</div></div>
    </section>

    <section class="controls">
      <input id="qInput" type="search" placeholder="Buscar por nombre, dirección, categoría o teléfono..." />
      <select id="nicheSelect"><option value="all">Todos los nichos ({len(niches)})</option>{niche_options}</select>
      <select id="subzoneSelect"><option value="all">Todas las subzonas ({len(subzones)})</option>{subzone_options}</select>
      <select id="flagSelect">
        <option value="all">Todas las oportunidades</option>
        <option value="NO_WEB">Sin Sitio Web / Solo Red Social ({no_web_total})</option>
        <option value="SOCIAL_ONLY">Solo Red Social (IG / FB / Linktree)</option>
        <option value="CARRITO STREET VIEW">Carrito Street View</option>
        <option value="LOW_PHOTOS">0 a 5 Fotos</option>
        <option value="SIN RECLAMAR">Sin Reclamar</option>
        <option value="HIGH_SCORE">Prioridad Alta (&ge;40 pts)</option>
      </select>
    </section>

    <div class="results-meta">
      <span id="visibleCount"></span>
      <span>Entrega digital (Web Express + GBP + Foto) 48–72h · Display acrílico LED QR artesanal: 3–5 días hábiles</span>
    </div>

    <main id="cardsGrid" class="grid"></main>
  </div>

  <dialog id="shotModal">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
      <strong id="shotTitle"></strong>
      <button class="btn" onclick="document.getElementById('shotModal').close()">Cerrar</button>
    </div>
    <img id="shotImg" src="" alt="Captura Google Maps" style="width:100%; border-radius:10px; border:1px solid var(--border);" />
  </dialog>

  <dialog id="gbpModal">
    <div style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
      <strong id="gbpTitle"></strong>
      <button class="btn" onclick="document.getElementById('gbpModal').close()">Cerrar</button>
    </div>
    <p id="gbpDiag" style="font-size:0.86rem; color:var(--champagne); margin-top:8px;"></p>
    <ul id="gbpList" class="gbp-list"></ul>
    <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap; margin-top:10px;">
      <a id="gbpDemoLink" href="#" target="_blank" class="btn gold">Abrir Prototipo Web Completo &rarr;</a>
      <div style="display:flex; gap:8px;">
        <button class="btn" onclick="copyChecklistText()">Copiar Checklist GBP</button>
        <a id="gbpWaBtn" href="#" target="_blank" class="btn primary">Enviar por WhatsApp &rarr;</a>
      </div>
    </div>
  </dialog>

  <dialog id="copyModal">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <strong id="copyTitle"></strong>
      <button class="btn" onclick="document.getElementById('copyModal').close()">Cerrar</button>
    </div>
    <div style="display:flex; gap:8px; margin-top:10px; flex-wrap:wrap;">
      <button class="btn gold" onclick="setVariant('mode_d_web_gbp')">Web Demo + GBP (-35%)</button>
      <button class="btn gold" onclick="setVariant('mode_b_diagnostico')">Corto Diagnóstico</button>
      <button class="btn gold" onclick="setVariant('mode_a_directo')">Completo -35%</button>
      <button class="btn gold" onclick="setVariant('mode_c_hibrido')">Portafolio &amp; Estilo</button>
    </div>
    <textarea id="copyTextarea"></textarea>
    <div style="display:flex; justify-content:flex-end; gap:10px;">
      <button class="btn" onclick="copyText()">Copiar Texto</button>
      <a id="waSendLink" href="#" target="_blank" class="btn primary">Abrir WhatsApp &rarr;</a>
    </div>
  </dialog>

  <script>
    const RECORDS = {safe_audits_json};
    let activeRecord = null;

    function esc(s) {{
      return String(s || '').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
    }}

    function webBadgeLabel(status) {{
      if (status === 'sin_web') return 'SIN SITIO WEB PROPIO';
      if (status === 'solo_red_social') return 'SOLO RED SOCIAL';
      return 'WEB PROPIA';
    }}

    function render() {{
      const q = document.getElementById('qInput').value.trim().toLowerCase();
      const niche = document.getElementById('nicheSelect').value;
      const subzona = document.getElementById('subzoneSelect').value;
      const flag = document.getElementById('flagSelect').value;

      const filtered = RECORDS.filter(r => {{
        if (niche !== 'all' && r.nicho !== niche) return false;
        if (subzona !== 'all' && r.subzona !== subzona) return false;
        if (flag === 'CARRITO STREET VIEW' && !r.audit_flags.includes('CARRITO STREET VIEW')) return false;
        if (flag === 'LOW_PHOTOS' && !r.audit_flags.includes('0 FOTOS') && !r.audit_flags.includes('<=5 FOTOS')) return false;
        if (flag === 'SIN RECLAMAR' && !r.audit_flags.includes('SIN RECLAMAR')) return false;
        if (flag === 'NO_WEB' && r.website_status !== 'sin_web' && r.website_status !== 'solo_red_social') return false;
        if (flag === 'SOCIAL_ONLY' && r.website_status !== 'solo_red_social') return false;
        if (flag === 'HIGH_SCORE' && r.audit_score < 40) return false;
        if (q) {{
          const hay = `${{r.nombre}} ${{r.categoria}} ${{r.direccion}} ${{r.telefono}} ${{r.nicho}}`.toLowerCase();
          if (!hay.includes(q)) return false;
        }}
        return true;
      }});

      document.getElementById('visibleCount').textContent = `Mostrando ${{filtered.length}} de ${{RECORDS.length}} prospectos en {html.escape(zone_title)}`;
      const grid = document.getElementById('cardsGrid');
      grid.innerHTML = filtered.map(r => {{
        const shotHtml = r.screenshot_rel
          ? `<img src="${{esc(r.screenshot_rel)}}" alt="${{esc(r.nombre)}}" loading="lazy" />`
          : `<div class="shot-empty">Sin captura pendiente · Abrir ficha directa en Google Maps</div>`;
        const flagsHtml = r.audit_flags.length
          ? r.audit_flags.map(f => `<span class="flag">${{esc(f)}}</span>`).join('')
          : `<span class="flag ok">FICHA COMPLETA · UPSELL EDITORIAL</span>`;
        const obs = (r.client_observations && r.client_observations[0]) || 'Oportunidad para elevar vitrina editorial y reserva directa en Google Maps.';
        const ratingStr = r.rating !== null && r.rating !== undefined ? `${{r.rating}} ★ (${{r.resenas}})` : `N/D (${{r.resenas}})`;
        const imgsStr = r.images_count !== null && r.images_count !== undefined ? `${{r.images_count}} fotos` : 'Fotos N/D';
        const waDirect = r.wa_digits && r.outreach_modes && r.outreach_modes.mode_d_web_gbp
          ? `https://wa.me/${{r.wa_digits}}?text=${{encodeURIComponent(r.outreach_modes.mode_d_web_gbp)}}`
          : '';
        const webPillCls = r.website_status === 'mejorable' ? 'web-pill ok' : 'web-pill';
        const urgentN = (r.gbp_checklist && r.gbp_checklist.urgent_count) || 0;
        return `
          <article class="card">
            <div>
              <div class="shot-wrap" onclick="openShot('${{esc(r.slug)}}')">
                ${{shotHtml}}
                <span class="${{webPillCls}}">${{webBadgeLabel(r.website_status)}}</span>
                <span class="score-pill">Dolor: ${{r.audit_score}}/100</span>
              </div>
              <div class="card-body">
                <div class="card-top">
                  <div class="card-title">${{esc(r.nombre)}}</div>
                  <span class="subzona-tag">${{esc(r.subzona)}}</span>
                </div>
                <div class="meta-line"><strong>${{esc(r.nicho)}}</strong> · ${{esc(r.categoria)}}</div>
                <div class="meta-line">${{esc(r.direccion)}}</div>
                <div class="meta-line"><strong>Tel:</strong> ${{esc(r.telefono || 'Sin teléfono')}} · <strong>Maps:</strong> ${{ratingStr}} · ${{imgsStr}}</div>
                <div class="flags">${{flagsHtml}}</div>
                <div class="obs">${{esc(obs)}}</div>
              </div>
            </div>
            <div class="card-actions">
              <div style="display:flex; gap:6px; flex-wrap:wrap;">
                ${{r.demo_web_rel ? `<a class="btn primary" href="${{esc(r.demo_web_rel)}}" target="_blank">Web Demo &rarr;</a>` : ''}}
                <button class="btn gold" onclick="openGbp('${{esc(r.slug)}}')">Checklist GBP (${{urgentN}})</button>
                <a class="btn" href="${{esc(r.gmaps_url)}}" target="_blank">Maps</a>
              </div>
              <div style="display:flex; gap:6px; flex-wrap:wrap;">
                <button class="btn" onclick="openCopy('${{esc(r.slug)}}')">Guiones</button>
                ${{waDirect ? `<a class="btn gold" href="${{esc(waDirect)}}" target="_blank">WhatsApp</a>` : ''}}
              </div>
            </div>
          </article>
        `;
      }}).join('');
    }}

    function openShot(slug) {{
      const rec = RECORDS.find(x => x.slug === slug);
      if (!rec || !rec.screenshot_rel) return;
      document.getElementById('shotTitle').textContent = rec.nombre;
      document.getElementById('shotImg').src = rec.screenshot_rel;
      document.getElementById('shotModal').showModal();
    }}

    function openGbp(slug) {{
      activeRecord = RECORDS.find(x => x.slug === slug);
      if (!activeRecord || !activeRecord.gbp_checklist) return;
      const chk = activeRecord.gbp_checklist;
      document.getElementById('gbpTitle').textContent = `${{activeRecord.nombre}} — Actualización Google Business Profile`;
      document.getElementById('gbpDiag').textContent = `${{chk.headline_diagnosis}} (${{chk.priority_level}})`;
      document.getElementById('gbpList').innerHTML = (chk.tasks || []).map(t => `
        <li class="gbp-item ${{t.status === 'critico' ? 'crit' : ''}}">
          <div><span class="gbp-badge">${{t.status === 'critico' ? 'PRIORIDAD' : 'OPTIMIZAR'}}</span><strong>${{esc(t.area)}}</strong></div>
          <div style="margin-top:4px; color:#d8d8e4;">${{esc(t.action)}}</div>
        </li>
      `).join('');
      const demoLink = document.getElementById('gbpDemoLink');
      if (activeRecord.demo_web_rel) {{
        demoLink.style.display = 'inline-block';
        demoLink.href = activeRecord.demo_web_rel;
      }} else {{
        demoLink.style.display = 'none';
      }}
      const waBtn = document.getElementById('gbpWaBtn');
      const waText = (activeRecord.outreach_modes && activeRecord.outreach_modes.mode_d_web_gbp) || '';
      if (activeRecord.wa_digits) {{
        waBtn.style.display = 'inline-block';
        waBtn.href = `https://wa.me/${{activeRecord.wa_digits}}?text=${{encodeURIComponent(waText)}}`;
      }} else {{
        waBtn.style.display = 'none';
      }}
      document.getElementById('gbpModal').showModal();
    }}

    function copyChecklistText() {{
      if (!activeRecord || !activeRecord.gbp_checklist) return;
      const chk = activeRecord.gbp_checklist;
      const txt = `Checklist Google Business Profile · ${{activeRecord.nombre}}\\n` +
        `${{chk.headline_diagnosis}}\\n\\n` +
        (chk.tasks || []).map((t, i) => `${{i + 1}}. [${{t.status.toUpperCase()}}] ${{t.area}}: ${{t.action}}`).join('\\n');
      navigator.clipboard.writeText(txt);
    }}

    function openCopy(slug) {{
      activeRecord = RECORDS.find(x => x.slug === slug);
      if (!activeRecord) return;
      document.getElementById('copyTitle').textContent = `${{activeRecord.nombre}} — Propuesta Web & Maps`;
      setVariant('mode_d_web_gbp');
      document.getElementById('copyModal').showModal();
    }}

    function setVariant(key) {{
      if (!activeRecord || !activeRecord.outreach_modes) return;
      const txt = activeRecord.outreach_modes[key] || '';
      document.getElementById('copyTextarea').value = txt;
      const waBtn = document.getElementById('waSendLink');
      if (activeRecord.wa_digits) {{
        waBtn.style.display = 'inline-block';
        waBtn.href = `https://wa.me/${{activeRecord.wa_digits}}?text=${{encodeURIComponent(txt)}}`;
      }} else {{
        waBtn.style.display = 'none';
      }}
    }}

    function copyText() {{
      const ta = document.getElementById('copyTextarea');
      ta.select();
      navigator.clipboard.writeText(ta.value);
    }}

    ['qInput', 'nicheSelect', 'subzoneSelect', 'flagSelect'].forEach(id => {{
      document.getElementById(id).addEventListener('input', render);
      document.getElementById(id).addEventListener('change', render);
    }});
    render();
  </script>
</body>
</html>"""
    return page_html


def build_all_pv_zone_maps() -> dict[str, Path]:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    DEMOS_DIR.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, Path] = {}
    zone_summaries: dict[str, Any] = {}

    for zone_spec in ZONE_SPECS:
        zkey = zone_spec["key"]
        idx = read_json(PV_DATA_ROOT / zkey / "gmaps_audits.json", default={"audits": []})
        audits = idx.get("audits", [])
        checklists, demo_rels = _generate_zone_prototypes(zkey, audits)
        zone_summaries[zkey] = {k: v for k, v in idx.items() if k != "audits"}
        zone_summaries[zkey]["prototypes_count"] = len(demo_rels)
        zone_summaries[zkey]["no_own_website_count"] = sum(
            1 for c in checklists.values() if c.get("website_status") in {"sin_web", "solo_red_social"}
        )

        md_text = _render_zone_markdown(
            zkey,
            zone_spec["title"],
            zone_spec["subtitle"],
            idx,
            checklists,
            demo_rels,
        )
        html_text = _render_zone_html(zone_spec, idx, checklists, demo_rels)

        md_path = DOCS_DIR / zone_spec["md_filename"]
        html_path = DOCS_DIR / zone_spec["html_filename"]
        md_path.write_text(md_text, encoding="utf-8")
        html_path.write_text(html_text, encoding="utf-8")
        outputs[f"{zkey}_md"] = md_path
        outputs[f"{zkey}_html"] = html_path

    resumen_path = PV_DATA_ROOT / "territorio_resumen.json"
    resumen = read_json(resumen_path, default={"territory": "Puerto Vallarta, Jalisco (Solo PV)"})
    resumen["updated_at"] = now_iso()
    resumen["zones"] = zone_summaries
    write_json(resumen_path, resumen)
    return outputs


if __name__ == "__main__":
    paths = build_all_pv_zone_maps()
    for key, p in paths.items():
        print(f"[✓] {key}: {p}")
