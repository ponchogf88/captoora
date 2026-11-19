#!/usr/bin/env python3
"""
CAPTOORA STUDIO // GENERADOR DE REPORTES Y HUBS HTML SEPARADOS PARA PUERTO VALLARTA (FASE 2)

Lee las salidas JSON aisladas de Puerto Vallarta:
  - dashboard/data/puerto_vallarta/eventos_zona_romantica.json
  - dashboard/data/puerto_vallarta/eventos_zona_hotelera.json
  - dashboard/data/puerto_vallarta/eventos_centro_y_bahia.json
  - dashboard/data/puerto_vallarta/influencers_y_cobertura_pv.json
  - dashboard/data/puerto_vallarta/proveedores_taller_pv.json

Genera Markdown + HTML dark-luxury (sin mezclar zonas ni Nuevo León, 0% mención IA,
sin palabra 'presumir' y sin menciones geográficas de origen):
  1) docs/EVENTOS_PV_ZONA_ROMANTICA.md & docs/puerto_vallarta_eventos_zona_romantica.html
  2) docs/EVENTOS_PV_ZONA_HOTELERA.md & docs/puerto_vallarta_eventos_zona_hotelera.html
  3) docs/EVENTOS_PV_CENTRO_Y_BAHIA.md & docs/puerto_vallarta_eventos_centro_bahia.html
  4) docs/INFLUENCERS_Y_COBERTURA_PV.md & docs/puerto_vallarta_influencers_y_cobertura.html
  5) docs/PROVEEDORES_TALLER_PUERTO_VALLARTA.md & docs/puerto_vallarta_proveedores_taller.html
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

from captoora_agents.config import now_iso, read_json, validate_client_copy

PV_DATA_ROOT = ROOT_DIR / "dashboard" / "data" / "puerto_vallarta"
DOCS_DIR = ROOT_DIR / "docs"

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

NAV_LINKS = [
    ("puerto_vallarta_eventos_zona_romantica.html", "Eventos · Zona Romántica"),
    ("puerto_vallarta_eventos_zona_hotelera.html", "Eventos · Zona Hotelera"),
    ("puerto_vallarta_eventos_centro_bahia.html", "Eventos · Centro / Bahía"),
    ("puerto_vallarta_influencers_y_cobertura.html", "Influencers, Invitados & Cobertura"),
    ("puerto_vallarta_proveedores_taller.html", "Proveedores Taller PV"),
]


def _assert_clean_texts(texts: list[str], context: str) -> None:
    for idx, txt in enumerate(texts):
        if not txt:
            continue
        violations = validate_client_copy(txt)
        if violations:
            raise ValueError(f"Guardrail Captoora bloqueó {context}[{idx}]: {violations}")
        low = txt.lower()
        for term in FORBIDDEN_ORIGIN_TERMS:
            if term in low:
                raise ValueError(f"Término de origen bloqueado ('{term}') en {context}[{idx}]")


def _clean_wa_digits(phone: str) -> str:
    digits = "".join(ch for ch in (phone or "") if ch.isdigit())
    if len(digits) == 10:
        return f"52{digits}"
    return digits


def _shared_css() -> str:
    return """
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
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
    }
    body {
      background: radial-gradient(circle at 85% 0%, rgba(198,255,0,0.06), transparent 36%),
                  radial-gradient(circle at 10% 10%, rgba(212,175,55,0.08), transparent 40%),
                  var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      line-height: 1.5;
      padding: 28px 20px 64px;
    }
    .wrap { max-width: 1320px; margin: 0 auto; }
    .topbar {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding-bottom: 18px;
      border-bottom: 1px solid rgba(212, 175, 55, 0.35);
      margin-bottom: 18px;
    }
    .brand-eyebrow {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      letter-spacing: 0.18em;
      color: var(--volt);
      text-transform: uppercase;
    }
    h1 {
      font-family: 'Cinzel', serif;
      font-size: clamp(1.45rem, 2.8vw, 2.2rem);
      color: #fff;
      margin-top: 4px;
    }
    .subtitle { color: var(--muted); font-size: 0.9rem; margin-top: 4px; }
    .nav-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 22px;
    }
    .nav-pill {
      padding: 8px 14px;
      border-radius: 999px;
      border: 1px solid rgba(212, 175, 55, 0.35);
      background: rgba(255,255,255,0.03);
      color: var(--champagne);
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 600;
    }
    .nav-pill.active, .nav-pill:hover {
      border-color: var(--volt);
      color: #07060b;
      background: var(--volt);
    }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }
    .kpi {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px 16px;
    }
    .kpi-val { font-size: 1.65rem; font-weight: 800; color: #fff; font-family: 'JetBrains Mono', monospace; }
    .kpi-val.volt { color: var(--volt); }
    .kpi-val.gold { color: var(--gold); }
    .kpi-label { font-size: 0.74rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px; }
    .callout {
      background: rgba(212,175,55,0.08);
      border: 1px solid rgba(212,175,55,0.35);
      border-radius: 14px;
      padding: 14px 18px;
      margin-bottom: 20px;
      font-size: 0.88rem;
      color: var(--champagne);
    }
    .controls {
      display: grid;
      grid-template-columns: 1.6fr 1fr 1fr;
      gap: 10px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px;
      margin-bottom: 18px;
    }
    @media (max-width: 900px) { .controls { grid-template-columns: 1fr; } }
    input, select {
      width: 100%;
      background: var(--surface);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
      font-size: 0.86rem;
      font-family: inherit;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 16px;
    }
    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
    }
    .card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; }
    .card-title { font-size: 1.02rem; font-weight: 700; color: #fff; }
    .tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      padding: 4px 8px;
      border-radius: 999px;
      white-space: nowrap;
      border: 1px solid rgba(212,175,55,0.45);
      background: rgba(212,175,55,0.12);
      color: var(--champagne);
    }
    .tag.volt {
      border-color: rgba(198,255,0,0.55);
      background: rgba(198,255,0,0.1);
      color: var(--volt);
    }
    .meta { font-size: 0.81rem; color: var(--muted); }
    .meta strong { color: #e2e0ec; }
    .obs {
      font-size: 0.8rem;
      color: #ebe6d7;
      background: rgba(255,255,255,0.03);
      border-left: 3px solid var(--gold);
      padding: 8px 10px;
      border-radius: 6px;
    }
    .actions {
      padding-top: 10px;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      gap: 8px;
      flex-wrap: wrap;
    }
    .btn {
      font-size: 0.76rem;
      font-weight: 700;
      padding: 7px 11px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      text-decoration: none;
      cursor: pointer;
    }
    .btn.primary { background: var(--volt); color: #07060b; border-color: var(--volt); }
    .btn.gold { border-color: rgba(212,175,55,0.5); color: var(--champagne); }
    .shot-thumb {
      width: 100%;
      height: 175px;
      border-radius: 10px;
      object-fit: cover;
      object-position: left top;
      border: 1px solid var(--border);
      cursor: pointer;
      background: #090910;
    }
    dialog {
      margin: auto;
      background: var(--card);
      color: var(--text);
      border: 1px solid rgba(212,175,55,0.45);
      border-radius: 16px;
      max-width: 820px;
      width: 92vw;
      padding: 20px;
    }
    dialog::backdrop { background: rgba(0,0,0,0.82); }
    textarea {
      width: 100%;
      min-height: 200px;
      background: var(--surface);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px;
      font-family: inherit;
      font-size: 0.85rem;
      margin: 10px 0;
    }
    h2.section-h {
      font-family: 'Cinzel', serif;
      font-size: 1.25rem;
      color: var(--champagne);
      margin: 26px 0 12px;
    }
    """


def _nav_html(active_filename: str) -> str:
    links = []
    for fname, label in NAV_LINKS:
        cls = "nav-pill active" if fname == active_filename else "nav-pill"
        links.append(f'<a class="{cls}" href="{html.escape(fname)}">{html.escape(label)}</a>')
    return '<nav class="nav-pills">' + "".join(links) + "</nav>"


def _render_zone_events_markdown(zone_title: str, subtitle: str, data: dict[str, Any]) -> str:
    events = data.get("events", [])
    _assert_clean_texts([e.get("guion_acercamiento_captoora", "") for e in events], f"events md {zone_title}")
    by_sub = Counter(e.get("subzona") or zone_title for e in events)
    by_cat = Counter(e.get("categoria") or "Evento" for e in events)

    lines = [
        f"# Cartelera de Eventos, Conciertos, Posadas & Brechas de Cobertura · Puerto Vallarta — {zone_title}",
        "",
        f"> **Territorio exclusivo:** `{zone_title}` (`{subtitle}`) · **Actualizado:** `{data.get('updated_at', now_iso())}`  ",
        "> **Posicionamiento Captoora Studio:** Enfoque en portafolio editorial, técnica de baja luz / 1/2000s, entrega digital el mismo día o 48–72h y piezas LED QR artesanales en 3–5 días hábiles.",
        "",
        "## 1. Resumen de Oportunidades en la Zona",
        "",
        f"- **Eventos y residencias verificadas en vivo:** `{data.get('total_events', 0)}`",
        f"- **Cobertura abierta (sin fotógrafo editorial dedicado):** `{data.get('open_coverage_count', 0)}`",
        f"- **Cobertura parcial (solo prensa general; oportunidad VIP / artistas / patrocinadores):** `{data.get('partial_coverage_count', 0)}`",
        f"- **Registros filtrados por estar fuera de Puerto Vallarta (Nayarit/Vidanta/Tepic/Online):** `{data.get('excluded_outside_pv_count', 0)}`",
        "",
        "| Subzona / Circuito | Eventos |",
        "| :--- | ---: |",
    ]
    for sz, cnt in by_sub.most_common():
        lines.append(f"| {sz} | {cnt} |")
    lines.extend(["", "| Categoría | Cantidad |", "| :--- | ---: |"])
    for cat, cnt in by_cat.most_common():
        lines.append(f"| {cat} | {cnt} |")

    lines.extend(
        [
            "",
            "---",
            "",
            f"## 2. Agenda Detallada, Invitados y Cobertura ({zone_title})",
            "",
            "| # | Fecha | Evento | Recinto / Subzona | Invitados / Artistas / Lineup | Cobertura Detectada | Estado Captoora | Fuente |",
            "|---:|---|---|---|---|---|---|---|",
        ]
    )
    for idx, ev in enumerate(events, start=1):
        inv = "; ".join(ev.get("invitados_artistas_lineup") or [])[:120]
        lines.append(
            f"| {idx} | {ev.get('fecha','')} | **{str(ev.get('titulo','')).replace('|','/')}** | "
            f"{str(ev.get('recinto','')).replace('|','/')} ({ev.get('subzona','')}) | {inv.replace('|','/')} | "
            f"{str(ev.get('cobertura_fotografica_detectada','')).replace('|','/')} | **{ev.get('estado_oportunidad_captoora','')}** | [Fuente]({ev.get('fuente_url','#')}) |"
        )

    lines.extend(["", "## 3. Guiones Personalizados Listos para Enviar (0% IA · Enfoque Editorial)", ""])
    for ev in events[:12]:
        lines.append(f"### {ev.get('titulo')} ({ev.get('fecha')})")
        lines.append(f"> {ev.get('guion_acercamiento_captoora')}")
        lines.append("")

    return "\n".join(lines) + "\n"


def _render_zone_events_html(filename: str, zone_title: str, subtitle: str, data: dict[str, Any]) -> str:
    events = data.get("events", [])
    _assert_clean_texts([e.get("guion_acercamiento_captoora", "") for e in events], f"events html {zone_title}")
    safe_json = json.dumps(events, ensure_ascii=False).replace("</", "<\\/")
    subzones = sorted({e.get("subzona") or zone_title for e in events})
    cats = sorted({e.get("categoria") or "Evento" for e in events})
    sub_opts = "".join(f'<option value="{html.escape(s)}">{html.escape(s)}</option>' for s in subzones)
    cat_opts = "".join(f'<option value="{html.escape(c)}">{html.escape(c)}</option>' for c in cats)

    return f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Captoora Studio · Eventos PV — {html.escape(zone_title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>{_shared_css()}</style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <div>
        <div class="brand-eyebrow">CAPTOORA STUDIO · CARTELERA EN VIVO, INVITADOS &amp; COBERTURA PUERTO VALLARTA</div>
        <h1>Eventos &amp; Oportunidades — {html.escape(zone_title)}</h1>
        <p class="subtitle">{html.escape(subtitle)} · Filtrado estricto fuera de Nayarit / Vidanta / Tepic.</p>
      </div>
    </header>
    {_nav_html(filename)}
    <section class="kpi-grid">
      <div class="kpi"><div class="kpi-val">{data.get('total_events', 0)}</div><div class="kpi-label">Eventos en {html.escape(zone_title)}</div></div>
      <div class="kpi"><div class="kpi-val volt">{data.get('open_coverage_count', 0)}</div><div class="kpi-label">Sin Fotógrafo Dedicado</div></div>
      <div class="kpi"><div class="kpi-val gold">{data.get('partial_coverage_count', 0)}</div><div class="kpi-label">Oportunidad VIP / Marcas</div></div>
      <div class="kpi"><div class="kpi-val">{data.get('excluded_outside_pv_count', 0)}</div><div class="kpi-label">Excluidos (Fuera de PV)</div></div>
    </section>
    <section class="controls">
      <input id="qInput" type="search" placeholder="Buscar por evento, artista, chef, DJ, recinto o fecha..." />
      <select id="subSelect"><option value="all">Todas las subzonas ({len(subzones)})</option>{sub_opts}</select>
      <select id="catSelect"><option value="all">Todas las categorías ({len(cats)})</option>{cat_opts}</select>
    </section>
    <div style="margin-bottom:12px; color:var(--muted); font-size:0.84rem;" id="countLabel"></div>
    <main id="cardsGrid" class="grid"></main>
  </div>
  <dialog id="scriptModal">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <strong id="modalTitle"></strong>
      <button class="btn" onclick="document.getElementById('scriptModal').close()">Cerrar</button>
    </div>
    <textarea id="modalText"></textarea>
    <div style="display:flex; justify-content:flex-end; gap:10px;">
      <button class="btn primary" onclick="copyModal()">Copiar Guion</button>
    </div>
  </dialog>
  <script>
    const EVENTS = {safe_json};
    function esc(s) {{ return String(s||'').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c])); }}
    function render() {{
      const q = document.getElementById('qInput').value.trim().toLowerCase();
      const sub = document.getElementById('subSelect').value;
      const cat = document.getElementById('catSelect').value;
      const rows = EVENTS.filter(e => {{
        if (sub !== 'all' && e.subzona !== sub) return false;
        if (cat !== 'all' && e.categoria !== cat) return false;
        if (q) {{
          const hay = `${{e.titulo}} ${{e.recinto}} ${{e.fecha}} ${{(e.invitados_artistas_lineup||[]).join(' ')}} ${{(e.influencers_relacionados||[]).join(' ')}}`.toLowerCase();
          if (!hay.includes(q)) return false;
        }}
        return true;
      }});
      document.getElementById('countLabel').textContent = `Mostrando ${{rows.length}} de ${{EVENTS.length}} eventos verificados`;
      document.getElementById('cardsGrid').innerHTML = rows.map(e => {{
        const openCls = String(e.estado_oportunidad_captoora||'').includes('Abierta') ? 'tag volt' : 'tag';
        const guests = (e.invitados_artistas_lineup||[]).join(' · ') || 'Talento anunciado en ficha';
        const leadTag = e.lead_gmaps_vinculado ? `<div class="meta"><strong>Ficha Maps vinculada:</strong> ${{esc(e.lead_gmaps_vinculado.nombre_gmaps)}} (${{esc(e.lead_gmaps_vinculado.telefono||'Sin tel')}})</div>` : '';
        return `
          <article class="card">
            <div>
              <div class="card-top">
                <div class="card-title">${{esc(e.titulo)}}</div>
                <span class="${{openCls}}">${{esc(e.estado_oportunidad_captoora)}}</span>
              </div>
              <div class="meta" style="margin-top:6px;"><strong>Fecha:</strong> ${{esc(e.fecha)}} · ${{esc(e.horario)}}</div>
              <div class="meta"><strong>Recinto:</strong> ${{esc(e.recinto)}}</div>
              <div class="meta"><strong>Subzona:</strong> ${{esc(e.subzona)}} · <strong>Categoría:</strong> ${{esc(e.categoria)}}</div>
              <div class="meta"><strong>Invitados / Lineup:</strong> ${{esc(guests)}}</div>
              ${{leadTag}}
              <div class="obs" style="margin-top:8px;"><strong>Cobertura detectada:</strong> ${{esc(e.cobertura_fotografica_detectada)}}</div>
            </div>
            <div class="actions">
              <a class="btn" href="${{esc(e.fuente_url)}}" target="_blank">Fuente en vivo &rarr;</a>
              <button class="btn primary" onclick="openScript('${{esc(e.id)}}')">Ver Guion Captoora</button>
            </div>
          </article>
        `;
      }}).join('');
    }}
    function openScript(id) {{
      const ev = EVENTS.find(x => x.id === id);
      if (!ev) return;
      document.getElementById('modalTitle').textContent = `${{ev.titulo}} — Guion Neutral`;
      document.getElementById('modalText').value = ev.guion_acercamiento_captoora || '';
      document.getElementById('scriptModal').showModal();
    }}
    function copyModal() {{
      const t = document.getElementById('modalText');
      t.select();
      navigator.clipboard.writeText(t.value);
    }}
    ['qInput','subSelect','catSelect'].forEach(id => {{
      document.getElementById(id).addEventListener('input', render);
      document.getElementById(id).addEventListener('change', render);
    }});
    render();
  </script>
</body>
</html>"""


def _render_influencers_markdown(inf: dict[str, Any]) -> str:
    infs = inf.get("influencers_y_creadores_pv", [])
    vips = inf.get("invitados_especiales_y_artistas", [])
    chefs = inf.get("chefs_invitados_festival_gourmet_pv", [])
    photos = (inf.get("resumen_cobertura_actual") or {}).get("fotografos_y_medios_detectados", [])
    _assert_clean_texts([x.get("guion_dm_captoora", "") for x in infs], "influencers md")

    lines = [
        "# Radar de Influencers, Invitados VIP & Brechas de Cobertura Fotográfica · Puerto Vallarta",
        "",
        f"> **Actualizado:** `{inf.get('updated_at', now_iso())}` · **Alcance:** Zona Romántica, Zona Hotelera y Centro / Bahía",
        "",
        "## 1. Diagnóstico Real de Cobertura Fotográfica en Puerto Vallarta",
        "",
        f"> {(inf.get('resumen_cobertura_actual') or {}).get('hallazgo_clave','')}",
        "",
        "| Fotógrafo / Medio Detectado en Prensa Local | Eventos de Muestra | Brecha Libre para Captoora |",
        "|---|---|---|",
    ]
    for p in photos:
        lines.append(
            f"| **{p.get('nombre_medio','')}** | {'; '.join(p.get('eventos_cubiertos_muestra') or [])[:110]} | {p.get('brecha_que_deja_para_captoora','')} |"
        )

    lines.extend(["", "## 2. Influencers & Creadores Activos en Puerto Vallarta + Guion DM", "", "| Creador | Handle | Nicho / Zona | Cobertura Actual | Oportunidad Captoora |", "|---|---|---|---|---|"])
    for c in infs:
        lines.append(
            f"| **{c.get('nombre','')}** | `{c.get('handle','')}` | {c.get('segmento','')} | {c.get('cobertura_actual','')} | {c.get('oportunidad_captoora','')} |"
        )
    lines.append("")
    for c in infs:
        lines.append(f"### DM Sugerido · {c.get('nombre')} ({c.get('handle')})")
        lines.append(f"> {c.get('guion_dm_captoora')}")
        lines.append("")

    lines.extend(["## 3. Artistas, DJs & Celebridades Invitadas (Nov 2026 – Ene 2027)", "", "| Invitado / Talento | Evento / Sede | Zona PV | Estatus de Cobertura |", "|---|---|---|---|"])
    for v in vips:
        lines.append(f"| **{v.get('nombre','')}** | {v.get('evento','')} | `{v.get('zona','')}` | {v.get('cobertura_propia','')} |")

    lines.extend(["", "## 4. Chefs Invitados & Restaurantes Anfitriones PV (31º Festival Gourmet)", "", "| Chef Invitado | Restaurante Anfitrión (Solo PV) | Subzona | Dirección |", "|---|---|---|---|"])
    for ch in chefs:
        lines.append(f"| **{ch.get('nombre_invitado','')}** | {ch.get('sede_pv','')} | {ch.get('subzona','')} | {ch.get('direccion','')} |")

    return "\n".join(lines) + "\n"


def _render_influencers_html(inf: dict[str, Any]) -> str:
    infs = inf.get("influencers_y_creadores_pv", [])
    vips = inf.get("invitados_especiales_y_artistas", [])
    chefs = inf.get("chefs_invitados_festival_gourmet_pv", [])
    photos = (inf.get("resumen_cobertura_actual") or {}).get("fotografos_y_medios_detectados", [])
    _assert_clean_texts([x.get("guion_dm_captoora", "") for x in infs], "influencers html")

    inf_cards = []
    for idx, c in enumerate(infs):
        dm_esc = html.escape(c.get("guion_dm_captoora", ""))
        inf_cards.append(
            f"""<article class="card">
              <div>
                <div class="card-top">
                  <div class="card-title">{html.escape(c.get('nombre',''))}</div>
                  <span class="tag volt">{html.escape(c.get('handle',''))}</span>
                </div>
                <div class="meta" style="margin-top:6px;"><strong>Segmento:</strong> {html.escape(c.get('segmento',''))}</div>
                <div class="meta"><strong>Cobertura actual:</strong> {html.escape(c.get('cobertura_actual',''))}</div>
                <div class="obs" style="margin-top:8px;"><strong>Ángulo Captoora:</strong> {html.escape(c.get('oportunidad_captoora',''))}</div>
              </div>
              <div class="actions">
                <a class="btn" href="{html.escape(c.get('fuente','#'))}" target="_blank">Referencia &rarr;</a>
                <button class="btn primary" onclick="copyTextIdx({idx})">Copiar Guion DM</button>
              </div>
            </article>"""
        )

    vip_cards = "".join(
        f"""<article class="card">
          <div>
            <div class="card-top">
              <div class="card-title">{html.escape(v.get('nombre',''))}</div>
              <span class="tag">{html.escape(v.get('zona',''))}</span>
            </div>
            <div class="meta" style="margin-top:6px;"><strong>Evento:</strong> {html.escape(v.get('evento',''))}</div>
            <div class="obs" style="margin-top:8px;">{html.escape(v.get('cobertura_propia',''))}</div>
          </div>
        </article>"""
        for v in vips
    )

    chef_cards = "".join(
        f"""<article class="card">
          <div>
            <div class="card-top">
              <div class="card-title">{html.escape(ch.get('nombre_invitado',''))}</div>
              <span class="tag gold">{html.escape(ch.get('sede_pv',''))}</span>
            </div>
            <div class="meta" style="margin-top:6px;"><strong>Subzona:</strong> {html.escape(ch.get('subzona',''))}</div>
            <div class="meta"><strong>Dirección:</strong> {html.escape(ch.get('direccion',''))}</div>
          </div>
          <div class="actions">
            <a class="btn" href="{html.escape(ch.get('fuente_url','#'))}" target="_blank">Ficha FGI &rarr;</a>
          </div>
        </article>"""
        for ch in chefs
    )

    phot_cards = "".join(
        f"""<article class="card">
          <div>
            <div class="card-top">
              <div class="card-title">{html.escape(p.get('nombre_medio',''))}</div>
              <span class="tag">Crédito Detectado</span>
            </div>
            <div class="meta" style="margin-top:6px;"><strong>Cobertura muestra:</strong> {html.escape('; '.join(p.get('eventos_cubiertos_muestra') or []))}</div>
            <div class="obs" style="margin-top:8px;"><strong>Brecha libre:</strong> {html.escape(p.get('brecha_que_deja_para_captoora',''))}</div>
          </div>
        </article>"""
        for p in photos
    )

    dms_json = json.dumps([c.get("guion_dm_captoora", "") for c in infs], ensure_ascii=False).replace("</", "<\\/")

    return f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Captoora Studio · Influencers, Invitados &amp; Cobertura PV</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>{_shared_css()}</style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <div>
        <div class="brand-eyebrow">CAPTOORA STUDIO · INTELIGENCIA DE CREADORES, ARTISTAS INVITADOS &amp; PRENSA PV</div>
        <h1>Influencers, Invitados VIP &amp; Brechas de Cobertura</h1>
        <p class="subtitle">Mapeo de quién está viniendo a Puerto Vallarta, quién ya tiene fotógrafo y dónde hay puerta abierta para Captoora.</p>
      </div>
    </header>
    {_nav_html("puerto_vallarta_influencers_y_cobertura.html")}
    <section class="kpi-grid">
      <div class="kpi"><div class="kpi-val">{len(infs)}</div><div class="kpi-label">Grupos de Creadores / Influencers</div></div>
      <div class="kpi"><div class="kpi-val volt">{len(vips)}</div><div class="kpi-label">Artistas / DJs / Celebridades VIP</div></div>
      <div class="kpi"><div class="kpi-val gold">{len(chefs)}</div><div class="kpi-label">Chefs Invitados (Solo PV)</div></div>
      <div class="kpi"><div class="kpi-val">{len(photos)}</div><div class="kpi-label">Fotógrafos Prensa Detectados</div></div>
    </section>
    <div class="callout">{html.escape((inf.get('resumen_cobertura_actual') or {}).get('hallazgo_clave',''))}</div>
    <h2 class="section-h">1. Influencers &amp; Creadores Locales / Temporada</h2>
    <div class="grid">{''.join(inf_cards)}</div>
    <h2 class="section-h">2. Talento Internacional, DJs &amp; Invitados Especiales</h2>
    <div class="grid">{vip_cards}</div>
    <h2 class="section-h">3. Chefs Invitados en Puerto Vallarta (31º Festival Gourmet)</h2>
    <div class="grid">{chef_cards}</div>
    <h2 class="section-h">4. Fotógrafos &amp; Medios Detectados (Mapa de Brechas)</h2>
    <div class="grid">{phot_cards}</div>
  </div>
  <script>
    const DMS = {dms_json};
    function copyTextIdx(i) {{
      navigator.clipboard.writeText(DMS[i] || '');
      alert('Guion DM copiado al portapapeles.');
    }}
  </script>
</body>
</html>"""


def _render_suppliers_markdown(sup_data: dict[str, Any]) -> str:
    suppliers = sup_data.get("suppliers", [])
    checklist = sup_data.get("field_audit_checklist_off_internet", [])
    strat = sup_data.get("anti_cheap_souvenir_strategy") or {}
    by_spec = Counter(s.get("especialidad") or "Taller" for s in suppliers)

    lines = [
        "# Directorio Auditado de Proveedores Locales de Taller · Puerto Vallarta (Solo PV)",
        "",
        f"> **Actualizado:** `{sup_data.get('updated_at', now_iso())}` · **Total de talleres mapeados:** `{sup_data.get('total_suppliers', 0)}`",
        "",
        "## 1. Estrategia Anti-Souvenir Barato y Blindaje de Margen",
        "",
        f"> **{strat.get('regla_central', '')}**",
        "",
    ]
    for r in strat.get("reglas_de_empaquetado", []):
        lines.append(f"- {r}")

    lines.extend(["", "## 2. Protocolo de Auditoría Presencial (Para Talleres Sin Presencia en Internet)", ""])
    for step in checklist:
        lines.append(f"- {step}")

    lines.extend(["", "## 3. Distribución por Especialidad", "", "| Especialidad | Talleres |", "| :--- | ---: |"])
    for k, cnt in by_spec.most_common():
        lines.append(f"| {k} | {cnt} |")

    lines.extend(
        [
            "",
            "## 4. Ranking de Proveedores Auditados en Google Maps + Chrome CDP",
            "",
            "| # | Proveedor | Especialidad | Corredor PV | Score Confiabilidad | Tier | Rating / Reseñas | Fotos | Teléfono | Maps / Captura |",
            "|---:|---|---|---|---:|---|---|---|---|---|",
        ]
    )
    for idx, s in enumerate(suppliers, start=1):
        shot = s.get("screenshot_path") or ""
        shot_md = f"[Captura](../{shot})" if shot else "Pendiente"
        lines.append(
            f"| {idx} | **{str(s.get('nombre','')).replace('|','/')}** | {s.get('especialidad','')} | {s.get('corredor','')} | "
            f"{s.get('reliability_score',0)}/100 | {s.get('reliability_tier','')} | {s.get('rating','N/D')} ★ ({s.get('resenas',0)}) | "
            f"{s.get('images_count','N/D')} | {s.get('telefono') or 'Sin tel'} | [Maps]({s.get('gmaps_url','#')}) · {shot_md} |"
        )
    return "\n".join(lines) + "\n"


def _render_suppliers_html(sup_data: dict[str, Any]) -> str:
    suppliers = sup_data.get("suppliers", [])
    checklist = sup_data.get("field_audit_checklist_off_internet", [])
    strat = sup_data.get("anti_cheap_souvenir_strategy") or {}
    specs = sorted({s.get("especialidad") or "Taller" for s in suppliers})
    tiers = sorted({s.get("reliability_tier") or "Tier" for s in suppliers})

    export_rows = [
        {
            **s,
            "wa_digits": _clean_wa_digits(s.get("telefono", "")),
            "screenshot_rel": f"../{s['screenshot_path']}" if s.get("screenshot_path") else "",
        }
        for s in suppliers
    ]
    safe_json = json.dumps(export_rows, ensure_ascii=False).replace("</", "<\\/")
    spec_opts = "".join(f'<option value="{html.escape(x)}">{html.escape(x)}</option>' for x in specs)
    tier_opts = "".join(f'<option value="{html.escape(x)}">{html.escape(x)}</option>' for x in tiers)

    strat_bullets = "".join(f"<li>{html.escape(x)}</li>" for x in strat.get("reglas_de_empaquetado", []))
    check_bullets = "".join(f"<li>{html.escape(x)}</li>" for x in checklist)

    return f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Captoora Studio · Proveedores de Taller Confiables PV</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>{_shared_css()} ul.bullets {{ padding-left: 18px; display:flex; flex-direction:column; gap:6px; margin-top:8px; }}</style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <div>
        <div class="brand-eyebrow">CAPTOORA STUDIO · AUDITORÍA DE PROVEEDORES LOCALES &amp; PROTOCOLO OFF-INTERNET</div>
        <h1>Proveedores Locales de Taller — Puerto Vallarta</h1>
        <p class="subtitle">Corte láser/acrílico, carpintería parota/nogal, enmarcados Fine Art e imprentas auditados en Google Maps + checklist de campo.</p>
      </div>
    </header>
    {_nav_html("puerto_vallarta_proveedores_taller.html")}
    <section class="kpi-grid">
      <div class="kpi"><div class="kpi-val">{sup_data.get('total_suppliers', 0)}</div><div class="kpi-label">Proveedores PV Auditados</div></div>
      <div class="kpi"><div class="kpi-val volt">{sup_data.get('tier_a_count', 0)}</div><div class="kpi-label">Tier A · Confiabilidad Alta</div></div>
      <div class="kpi"><div class="kpi-val gold">{sup_data.get('tier_b_count', 0)}</div><div class="kpi-label">Tier B · Validar Muestra</div></div>
      <div class="kpi"><div class="kpi-val">{sup_data.get('tier_c_count', 0)}</div><div class="kpi-label">Tier C · Inspección Presencial</div></div>
    </section>
    <div class="callout">
      <strong>Posicionamiento Anti-Souvenir Barato:</strong> {html.escape(strat.get('regla_central', ''))}
      <ul class="bullets">{strat_bullets}</ul>
    </div>
    <div class="callout" style="background:rgba(198,255,0,0.05); border-color:rgba(198,255,0,0.35); color:#e5f3ba;">
      <strong>Protocolo Presencial para Talleres que No Están en Internet:</strong>
      <ul class="bullets">{check_bullets}</ul>
    </div>
    <section class="controls">
      <input id="qInput" type="search" placeholder="Buscar por nombre, dirección, teléfono o corredor..." />
      <select id="specSelect"><option value="all">Todas las especialidades ({len(specs)})</option>{spec_opts}</select>
      <select id="tierSelect"><option value="all">Todos los Tiers ({len(tiers)})</option>{tier_opts}</select>
    </section>
    <div style="margin-bottom:12px; color:var(--muted); font-size:0.84rem;" id="countLabel"></div>
    <main id="cardsGrid" class="grid"></main>
  </div>
  <dialog id="shotModal">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
      <strong id="shotTitle"></strong>
      <button class="btn" onclick="document.getElementById('shotModal').close()">Cerrar</button>
    </div>
    <img id="shotImg" src="" alt="Captura Google Maps" style="width:100%; border-radius:10px; border:1px solid var(--border);" />
  </dialog>
  <script>
    const SUPPLIERS = {safe_json};
    function esc(s) {{ return String(s||'').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c])); }}
    function render() {{
      const q = document.getElementById('qInput').value.trim().toLowerCase();
      const spec = document.getElementById('specSelect').value;
      const tier = document.getElementById('tierSelect').value;
      const rows = SUPPLIERS.filter(s => {{
        if (spec !== 'all' && s.especialidad !== spec) return false;
        if (tier !== 'all' && s.reliability_tier !== tier) return false;
        if (q) {{
          const hay = `${{s.nombre}} ${{s.direccion}} ${{s.corredor}} ${{s.telefono}} ${{s.especialidad}}`.toLowerCase();
          if (!hay.includes(q)) return false;
        }}
        return true;
      }});
      document.getElementById('countLabel').textContent = `Mostrando ${{rows.length}} de ${{SUPPLIERS.length}} talleres en Puerto Vallarta`;
      document.getElementById('cardsGrid').innerHTML = rows.map(s => {{
        const thumb = s.screenshot_rel ? `<img class="shot-thumb" src="${{esc(s.screenshot_rel)}}" alt="${{esc(s.nombre)}}" loading="lazy" onclick="openShot('${{esc(s.slug)}}')" />` : '';
        const tierCls = s.reliability_score >= 75 ? 'tag volt' : 'tag';
        const notes = (s.reliability_notes || []).join(' · ') || 'Validar presencialmente';
        const quoteMsg = encodeURIComponent(`Hola equipo de ${{s.nombre}}, soy Jesús Gutiérrez de Captoora Studio. Buscamos cotizar muestra calibrada de piezas corporativas en ${{s.especialidad}} (acrílico óptico cast 8mm / base sólida / corte de precisión) en Puerto Vallarta. ¿Manejan atención en taller esta semana?`);
        return `
          <article class="card">
            <div>
              ${{thumb}}
              <div class="card-top" style="margin-top:8px;">
                <div class="card-title">${{esc(s.nombre)}}</div>
                <span class="${{tierCls}}">${{s.reliability_score}}/100</span>
              </div>
              <div class="meta" style="margin-top:4px;"><strong>${{esc(s.especialidad)}}</strong> · ${{esc(s.reliability_tier)}}</div>
              <div class="meta"><strong>Corredor:</strong> ${{esc(s.corredor)}}</div>
              <div class="meta">${{esc(s.direccion)}}</div>
              <div class="meta"><strong>Tel:</strong> ${{esc(s.telefono || 'Sin teléfono')}} · <strong>Maps:</strong> ${{s.rating ?? 'N/D'}} ★ (${{s.resenas}}) · ${{s.images_count ?? 'N/D'}} fotos</div>
              <div class="obs" style="margin-top:8px;">${{esc(notes)}}</div>
            </div>
            <div class="actions">
              <a class="btn" href="${{esc(s.gmaps_url)}}" target="_blank">Google Maps &rarr;</a>
              ${{s.sitio_web ? `<a class="btn" href="${{esc(s.sitio_web)}}" target="_blank">Web / Red</a>` : ''}}
              ${{s.wa_digits ? `<a class="btn primary" href="https://wa.me/${{s.wa_digits}}?text=${{quoteMsg}}" target="_blank">Cotizar Muestra WA</a>` : ''}}
            </div>
          </article>
        `;
      }}).join('');
    }}
    function openShot(slug) {{
      const s = SUPPLIERS.find(x => x.slug === slug);
      if (!s || !s.screenshot_rel) return;
      document.getElementById('shotTitle').textContent = s.nombre;
      document.getElementById('shotImg').src = s.screenshot_rel;
      document.getElementById('shotModal').showModal();
    }}
    ['qInput','specSelect','tierSelect'].forEach(id => {{
      document.getElementById(id).addEventListener('input', render);
      document.getElementById(id).addEventListener('change', render);
    }});
    render();
  </script>
</body>
</html>"""


def build_phase2_pv_hub() -> dict[str, Path]:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, Path] = {}

    zone_configs = [
        ("zona_romantica", "Zona Romántica", "Emiliano Zapata · Olas Altas · Basilio Badillo · Los Muertos · Amapas", "EVENTOS_PV_ZONA_ROMANTICA.md", "puerto_vallarta_eventos_zona_romantica.html"),
        ("zona_hotelera", "Zona Hotelera", "Zona Hotelera Norte (Las Glorias / Versalles / Fluvial / CICPV) · Marina Vallarta · Zona Hotelera Sur / Costa Sur", "EVENTOS_PV_ZONA_HOTELERA.md", "puerto_vallarta_eventos_zona_hotelera.html"),
        ("centro_y_bahia", "Centro / Bahía", "Centro Histórico · Malecón · Isla Río Cuale · Col. 5 de Diciembre (Teatro Vallarta / MUYGUUD) · Salidas en Bahía PV", "EVENTOS_PV_CENTRO_Y_BAHIA.md", "puerto_vallarta_eventos_centro_bahia.html"),
    ]
    for zkey, title, subtitle, md_name, html_name in zone_configs:
        zdata = read_json(PV_DATA_ROOT / f"eventos_{zkey}.json", default={"events": []})
        md_path = DOCS_DIR / md_name
        html_path = DOCS_DIR / html_name
        md_path.write_text(_render_zone_events_markdown(title, subtitle, zdata), encoding="utf-8")
        html_path.write_text(_render_zone_events_html(html_name, title, subtitle, zdata), encoding="utf-8")
        outputs[f"{zkey}_md"] = md_path
        outputs[f"{zkey}_html"] = html_path

    inf_data = read_json(PV_DATA_ROOT / "influencers_y_cobertura_pv.json", default={})
    inf_md = DOCS_DIR / "INFLUENCERS_Y_COBERTURA_PV.md"
    inf_html = DOCS_DIR / "puerto_vallarta_influencers_y_cobertura.html"
    inf_md.write_text(_render_influencers_markdown(inf_data), encoding="utf-8")
    inf_html.write_text(_render_influencers_html(inf_data), encoding="utf-8")
    outputs["influencers_md"] = inf_md
    outputs["influencers_html"] = inf_html

    sup_data = read_json(PV_DATA_ROOT / "proveedores_taller_pv.json", default={})
    sup_md = DOCS_DIR / "PROVEEDORES_TALLER_PUERTO_VALLARTA.md"
    sup_html = DOCS_DIR / "puerto_vallarta_proveedores_taller.html"
    sup_md.write_text(_render_suppliers_markdown(sup_data), encoding="utf-8")
    sup_html.write_text(_render_suppliers_html(sup_data), encoding="utf-8")
    outputs["suppliers_md"] = sup_md
    outputs["suppliers_html"] = sup_html

    return outputs


if __name__ == "__main__":
    paths = build_phase2_pv_hub()
    for k, p in paths.items():
        print(f"[✓] {k}: {p}")
