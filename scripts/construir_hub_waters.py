#!/usr/bin/env python3
"""
Genera proyectos/waters-serie/index.html embebiendo calendario_30_dias.json
y 100_SITUACIONES_WATERS.csv para operación 100% autocontenida (file:// y HTTP).
"""

import csv
import json
from pathlib import Path

BASE_DIR = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie")
CAL_JSON = BASE_DIR / "calendario_30_dias.json"
CSV_FILE = BASE_DIR / "100_SITUACIONES_WATERS.csv"
OUT_HTML = BASE_DIR / "index.html"

episodes = json.loads(CAL_JSON.read_text(encoding="utf-8"))
with CSV_FILE.open("r", encoding="utf-8") as f:
    situations = list(csv.DictReader(f))

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Soy Chuy · ¡WATERS! OS, Fábrica 3D &amp; Legal Engineer Hub</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #07090f;
    --surface: rgba(16, 21, 34, 0.78);
    --surface-solid: #101522;
    --border: rgba(255, 255, 255, 0.09);
    --text: #f3f5f9;
    --muted: #98a2b8;
    --gold: #dfb15b;
    --red: #ff4d4d;
    --lime: #a3e635;
    --cyan: #38bdf8;
    --glow: rgba(223, 177, 91, 0.22);
    --scene-accent: #dfb15b;
  }

  /* Escenarios dinámicos estilo soyvibecoder.com */
  body[data-scene="monterrey"] { --bg: #07090f; --glow: rgba(223, 177, 91, 0.25); --scene-accent: #dfb15b; }
  body[data-scene="tribunal"] { --bg: #080b14; --glow: rgba(56, 189, 248, 0.24); --scene-accent: #38bdf8; }
  body[data-scene="redteam"]  { --bg: #0d070a; --glow: rgba(255, 77, 77, 0.24); --scene-accent: #ff4d4d; }
  body[data-scene="gryffindor"] { --bg: #0a0c09; --glow: rgba(163, 230, 53, 0.22); --scene-accent: #a3e635; }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body {
    font-family: 'Space Grotesk', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.55;
    min-height: 100vh;
    overflow-x: hidden;
    transition: background 0.55s ease;
  }

  /* Atmósfera ambiental cambiante */
  .ambient-backdrop {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background:
      radial-gradient(circle at 15% 18%, var(--glow) 0%, transparent 45%),
      radial-gradient(circle at 85% 75%, rgba(56, 189, 248, 0.12) 0%, transparent 42%),
      radial-gradient(circle at 50% 0%, rgba(255, 255, 255, 0.03) 0%, transparent 60%);
    transition: background 0.6s ease;
  }

  .container {
    position: relative;
    z-index: 1;
    max-width: 1260px;
    margin: 0 auto;
    padding: 28px 20px 80px;
  }

  /* Top Navigation & Escenario Switcher */
  .topbar {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: rgba(12, 16, 26, 0.85);
    backdrop-filter: blur(14px);
    margin-bottom: 30px;
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .brand-avatar {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    object-fit: cover;
    border: 2px solid var(--gold);
  }
  .brand-title { font-weight: 700; font-size: 1.05rem; }
  .brand-sub { font-size: 0.8rem; color: var(--muted); }

  .scene-switcher {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }
  .scene-label { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-right: 4px; }
  .scene-btn {
    background: rgba(255,255,255,0.04);
    color: var(--muted);
    border: 1px solid var(--border);
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.25s ease;
  }
  .scene-btn:hover, .scene-btn[aria-pressed="true"] {
    color: #07090f;
    background: var(--scene-accent);
    border-color: var(--scene-accent);
    font-weight: 600;
  }

  /* Hero estilo soyvibecoder.com + Accesos Directos */
  .hero-grid {
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: 28px;
    align-items: center;
    margin-bottom: 48px;
  }
  @media (max-width: 900px) {
    .hero-grid { grid-template-columns: 1fr; }
  }
  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 77, 77, 0.14);
    border: 1px solid rgba(255, 77, 77, 0.4);
    color: #ff8a8a;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 16px;
  }
  .hero h1 {
    font-size: clamp(2rem, 4.2vw, 3.3rem);
    line-height: 1.08;
    margin-bottom: 16px;
    letter-spacing: -0.02em;
  }
  .hero h1 span { color: var(--gold); }
  .hero p.lead {
    color: var(--muted);
    font-size: 1.05rem;
    margin-bottom: 24px;
    max-width: 60ch;
  }

  /* Linktree Cards estilo soyvibecoder.com */
  .vibecoder-links {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .vibe-link {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 16px 20px;
    border-radius: 16px;
    border: 1px solid var(--border);
    background: var(--surface);
    backdrop-filter: blur(12px);
    color: var(--text);
    text-decoration: none;
    transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.25s ease, background 0.25s ease;
  }
  .vibe-link:hover {
    transform: translateX(6px);
    border-color: var(--scene-accent);
    background: rgba(22, 29, 46, 0.95);
  }
  .vibe-link strong { display: block; font-size: 1rem; margin-bottom: 2px; }
  .vibe-link small { display: block; color: var(--muted); font-size: 0.84rem; }
  .vibe-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    padding: 4px 9px;
    border-radius: 999px;
    background: rgba(223, 177, 91, 0.16);
    color: var(--gold);
    border: 1px solid rgba(223, 177, 91, 0.35);
    white-space: nowrap;
  }

  /* Section Headings */
  .sec-head {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-end;
    gap: 12px;
    margin: 54px 0 22px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
  }
  .sec-head h2 { font-size: 1.65rem; letter-spacing: -0.015em; }
  .sec-head p { color: var(--muted); font-size: 0.92rem; }

  /* 2. CARRUSEL EXPANDIBLE HORIZONTAL (Transición exacta video OpusClip) */
  .accordion-strip {
    display: flex;
    gap: 14px;
    height: 440px;
    width: 100%;
  }
  @media (max-width: 900px) {
    .accordion-strip { flex-direction: column; height: auto; }
  }
  .strip-card {
    position: relative;
    flex: 1;
    min-width: 0;
    border-radius: 22px;
    overflow: hidden;
    border: 1px solid var(--border);
    background: #101522;
    cursor: pointer;
    transition: flex 0.45s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.3s ease, box-shadow 0.4s ease;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  }
  .strip-card:hover, .strip-card:focus-within, .strip-card.is-active {
    flex: 2.8;
    border-color: var(--gold);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 28px var(--glow);
  }
  .strip-card img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 20%;
    transition: transform 0.55s cubic-bezier(0.22, 1, 0.36, 1), filter 0.4s ease;
    filter: brightness(0.65) saturate(0.95);
  }
  .strip-card:hover img, .strip-card.is-active img {
    transform: scale(1.04);
    filter: brightness(0.92) saturate(1.08);
  }
  .strip-overlay {
    position: relative;
    z-index: 2;
    padding: 20px;
    background: linear-gradient(180deg, transparent 0%, rgba(7, 9, 15, 0.88) 42%, rgba(7, 9, 15, 0.98) 100%);
  }
  .strip-tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 999px;
    background: rgba(223, 177, 91, 0.22);
    color: var(--gold);
    margin-bottom: 8px;
  }
  .strip-card h3 { font-size: 1.05rem; margin-bottom: 6px; }
  .strip-extra {
    max-height: 0;
    opacity: 0;
    overflow: hidden;
    transition: max-height 0.4s ease, opacity 0.35s ease;
    font-size: 0.86rem;
    color: #d6dce8;
  }
  .strip-card:hover .strip-extra,
  .strip-card:focus-within .strip-extra,
  .strip-card.is-active .strip-extra {
    max-height: 180px;
    opacity: 1;
    margin-top: 6px;
  }

  /* 3. FÁBRICA DE VIDEO & REPRODUCTOR */
  .factory-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }
  .card {
    border-radius: 20px;
    border: 1px solid var(--border);
    background: var(--surface);
    backdrop-filter: blur(12px);
    padding: 20px;
    container-type: inline-size;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .video-frame {
    width: 100%;
    max-height: 500px;
    aspect-ratio: 9 / 16;
    border-radius: 14px;
    background: #000;
    object-fit: contain;
    border: 1px solid rgba(255,255,255,0.12);
  }
  .cli-box {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    background: #05070c;
    border: 1px solid var(--border);
    padding: 12px 14px;
    border-radius: 12px;
    color: var(--lime);
    overflow-x: auto;
  }

  /* Filtros y Calendario 30 Días */
  .filter-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 14px;
  }
  .chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    color: var(--muted);
    padding: 7px 14px;
    border-radius: 999px;
    font-family: inherit;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .chip:hover { border-color: var(--gold); color: var(--text); }
  .chip.active { background: var(--gold); color: #07090f; border-color: var(--gold); font-weight: 700; }

  .search-input {
    width: 100%;
    max-width: 440px;
    padding: 10px 16px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: rgba(16, 21, 34, 0.9);
    color: var(--text);
    font-family: inherit;
    font-size: 0.92rem;
  }
  .search-input:focus { outline: 2px solid var(--gold); border-color: transparent; }

  .calendar-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 18px;
    margin-top: 18px;
  }
  .ep-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .ep-day {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.78rem;
    padding: 4px 10px;
    border-radius: 8px;
    background: rgba(223, 177, 91, 0.16);
    color: var(--gold);
  }
  .ep-cta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    padding: 4px 9px;
    border-radius: 8px;
    background: rgba(163, 230, 53, 0.14);
    color: var(--lime);
    border: 1px solid rgba(163, 230, 53, 0.3);
  }
  .ep-impacts {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    font-size: 0.76rem;
    color: var(--muted);
  }
  .impact-pill {
    background: rgba(255,255,255,0.05);
    padding: 3px 8px;
    border-radius: 6px;
  }

  /* Acordeón accesible moderno (<details>) siguiendo modern-web-guidance */
  details.script-box {
    border: 1px solid var(--border);
    border-radius: 12px;
    background: rgba(7, 9, 15, 0.55);
    padding: 10px 12px;
  }
  details.script-box summary {
    list-style: none;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.86rem;
    color: var(--cyan);
  }
  details.script-box summary::before {
    content: "▶";
    font-size: 0.72rem;
    transition: rotate 0.2s ease;
  }
  details.script-box[open] > summary::before { rotate: 90deg; }
  details.script-box::details-content {
    interpolate-size: allow-keywords;
    overflow: clip;
    contain: layout;
  }
  @media (prefers-reduced-motion: no-preference) {
    details.script-box::details-content {
      transition: block-size 0.3s ease-in-out, content-visibility 0.3s ease-in-out allow-discrete;
    }
  }
  .beat-list {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 0.84rem;
    color: #dbe2f0;
  }
  .beat-item { padding: 8px; border-left: 3px solid var(--gold); background: rgba(255,255,255,0.03); border-radius: 0 8px 8px 0; }
  .beat-item strong { display: block; color: var(--gold); font-size: 0.75rem; margin-bottom: 2px; }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 9px 14px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.06);
    color: var(--text);
    font-family: inherit;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s ease;
  }
  .btn:hover { background: var(--gold); color: #07090f; border-color: var(--gold); }
  .btn-primary { background: var(--gold); color: #07090f; border-color: var(--gold); }
  .btn-primary:hover { filter: brightness(1.08); }

  /* Radiografía Tribunal Virtual + Parches Red Team */
  .grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 18px;
  }
  .norm-item {
    padding: 12px 14px;
    border-radius: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    margin-bottom: 10px;
  }
  .norm-item strong { color: var(--cyan); font-size: 0.92rem; display: block; margin-bottom: 4px; }
  .norm-item p { font-size: 0.84rem; color: #cbd5e1; }

  /* CV Modular & Productos */
  .cv-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    margin-top: 16px;
  }
  .cv-card {
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px;
    background: rgba(14, 19, 32, 0.86);
    transition: all 0.25s ease;
  }
  .cv-card.is-highlighted {
    border-color: var(--lime);
    box-shadow: 0 0 24px rgba(163, 230, 53, 0.14);
  }
  .cv-card.is-dimmed { opacity: 0.35; }

  /* Tabla 100 Situaciones */
  .table-wrap {
    max-height: 460px;
    overflow: auto;
    border: 1px solid var(--border);
    border-radius: 16px;
    background: rgba(10, 14, 24, 0.85);
    margin-top: 14px;
  }
  table { width: 100%; border-collapse: collapse; font-size: 0.84rem; }
  th, td { padding: 11px 14px; text-align: left; border-bottom: 1px solid var(--border); vertical-align: top; }
  th { position: sticky; top: 0; background: #101626; color: var(--gold); font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em; }
  tr:hover td { background: rgba(255,255,255,0.03); }

  /* Casting 8 Versiones + Aviso 0 Créditos ElevenLabs + Spotlight PJENL */
  .casting-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 18px;
  }
  .casting-card {
    border-radius: 20px;
    border: 1px solid var(--border);
    background: var(--surface);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
  }
  .casting-card:hover {
    transform: translateY(-4px);
    border-color: var(--gold);
  }
  .casting-card.is-chosen {
    border: 2px solid var(--lime);
    box-shadow: 0 0 28px rgba(163, 230, 53, 0.22);
  }
  .casting-card img {
    width: 100%;
    aspect-ratio: 9 / 14;
    object-fit: cover;
    object-position: center 15%;
    display: block;
    background: #0a0d16;
  }
  .casting-body {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
  }
  .audio-shield-banner {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    border-radius: 16px;
    border: 1px solid rgba(163, 230, 53, 0.45);
    background: rgba(163, 230, 53, 0.09);
    color: #e9fcd0;
    margin-bottom: 18px;
    font-size: 0.9rem;
  }
  .tv-spotlight {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 18px;
  }
  @media (max-width: 900px) {
    .tv-spotlight { grid-template-columns: 1fr; }
  }
  .novato-pro-box {
    white-space: pre-wrap;
    font-family: 'Space Grotesk', system-ui, sans-serif;
    font-size: 0.85rem;
    line-height: 1.5;
    padding: 14px;
    border-radius: 14px;
    background: rgba(7, 9, 15, 0.72);
    border: 1px solid var(--border);
    color: #e2e8f0;
  }

  footer {
    margin-top: 64px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 14px;
    color: var(--muted);
    font-size: 0.84rem;
  }
</style>
</head>
<body data-scene="monterrey">
<div class="ambient-backdrop" aria-hidden="true"></div>

<div class="container">
  <!-- TOPBAR -->
  <header class="topbar">
    <div class="brand">
      <img class="brand-avatar" src="./assets/pose_01_susto_waters.jpg" alt="Abogado de Plastilina ¡WATERS!">
      <div>
        <div class="brand-title">Soy Chuy · El Abogado de Plastilina (¡WATERS!)</div>
        <div class="brand-sub">Personal Operating System · Legal Engineer · Ciberseguridad &amp; IA</div>
      </div>
    </div>
    <div class="scene-switcher" role="group" aria-label="Selector de escenario ambiental">
      <span class="scene-label">Escenario:</span>
      <button class="scene-btn" data-scene-target="monterrey" aria-pressed="true">Oficina Monterrey</button>
      <button class="scene-btn" data-scene-target="tribunal" aria-pressed="false">Tribunal Virtual 404</button>
      <button class="scene-btn" data-scene-target="redteam" aria-pressed="false">Sala Red Team</button>
      <button class="scene-btn" data-scene-target="gryffindor" aria-pressed="false">Lab Gryffindor</button>
    </div>
  </header>

  <!-- HERO + HUB ESTILO SOYVIBECODER.COM -->
  <section class="hero-grid">
    <div class="hero">
      <div class="hero-badge">😱 [SUSPIRO DRAMÁTICO] ➔ ¡¡¡WATERS!!! · TEMPORADA 1 PILOTO</div>
      <h1>Ciberseguridad, IA y Derecho sin <span>demandas ni sustos</span>.</h1>
      <p class="lead">
        Soy Abogado aprendiendo Ciberseguridad e Inteligencia Artificial porque es la forma de hacer justicia y proteger a las personas. Un solo Enter en un agente hoy afecta tu dinero, tu tiempo, tu trabajo, tus clientes y tus juicios.
      </p>
      <div style="display:flex; flex-wrap:wrap; gap:10px;">
        <a class="btn btn-primary" href="#calendario">📅 Abrir Calendario 30 Días</a>
        <a class="btn" href="#fabrica">🎬 Ver Pilotos Renderizados MP4</a>
        <a class="btn" href="#tribunal">⚖️ Secretos Tribunal Virtual 404</a>
      </div>
    </div>

    <nav class="vibecoder-links" aria-label="Accesos principales estilo soyvibecoder">
      <a class="vibe-link" href="#fabrica">
        <span>
          <strong>🎬 La Fábrica ¡WATERS!</strong>
          <small>Tu serie animada 3D de plastilina. Eliges el capítulo y tu Mac arma el reel MP4.</small>
        </span>
        <span class="vibe-pill">PYTHON + FFMPEG</span>
      </a>
      <a class="vibe-link" href="#tribunal">
        <span>
          <strong>⚖️ Manual Secreto Tribunal Virtual + Kit IA</strong>
          <small>Arts. 44–87 CPCNL, Acuerdos 2011–2025, prompts blindados y parches Red Team.</small>
        </span>
        <span class="vibe-pill">$200 MXN / DM</span>
      </a>
      <a class="vibe-link" href="#productos">
        <span>
          <strong>🎓 El Curso: IA y Ciberseguridad sin Demandas</strong>
          <small>3 niveles: Protección Familiar, Negocios con Bots Seguros y Legal Engineering.</small>
        </span>
        <span class="vibe-pill">$400 MXN · 3 NIVELES</span>
      </a>
      <a class="vibe-link" href="#cv-modular">
        <span>
          <strong>🚀 CV Modular Legal Engineer + Proof of Work</strong>
          <small>Portafolio filtrado para Harvey.ai, Clara, Google y Microsoft.</small>
        </span>
        <span class="vibe-pill">HARVEY · GOOGLE</span>
      </a>
      <a class="vibe-link" href="https://ponchogf88.github.io/legaltech-innovation-lab/" target="_blank" rel="noopener noreferrer">
        <span>
          <strong>🧪 LegalTech Innovation Lab (En Vivo en GitHub Pages)</strong>
          <small>81 pruebas pytest en verde, Red Team endurecido y flujo real de PJENL.</small>
        </span>
        <span class="vibe-pill">LIVE LAB ↗</span>
      </a>
    </nav>
  </section>

  <!-- 1B. CASTING OFICIAL DEL PERSONAJE ¡WATERS! (8 VERSIONES) -->
  <div class="sec-head" id="casting">
    <div>
      <h2>🎭 Casting Oficial del Personaje ¡WATERS! — Compara las 8 Versiones</h2>
      <p>La versión original + 7 estilos nuevos esculpidos en 9:16 para que elijas cuál aprobamos como rostro definitivo de la serie.</p>
    </div>
    <span class="ep-cta" id="chosen-character-status">Personaje activo: Original (Plastilina Clásico)</span>
  </div>
  <section class="casting-grid" id="casting-grid">
    <article class="casting-card is-chosen" data-char-id="v00" data-char-name="Original · Plastilina Saco Azul" data-char-src="./assets/pose_01_susto_waters.jpg">
      <img src="./assets/pose_01_susto_waters.jpg" alt="Opción Original Plastilina Saco Azul">
      <div class="casting-body">
        <span class="strip-tag">Opción 00 · Base</span>
        <h3>Plastilina Clásico (Saco Azul)</h3>
        <p style="font-size:0.84rem; color:var(--muted);">El primero que aprobaste con tus 4 poses ya listas. Estilo Aardman cálido en despacho tradicional.</p>
        <button type="button" class="btn btn-primary choose-char-btn" style="margin-top:auto;">✅ Elegir este como Personaje Oficial</button>
      </div>
    </article>
    <article class="casting-card" data-char-id="v01" data-char-name="V01 · Legal Engineer Hoodie + Lentes" data-char-src="./assets/casting/v01_legal_engineer_hoodie.jpg">
      <img src="./assets/casting/v01_legal_engineer_hoodie.jpg" alt="Versión 01 Legal Engineer Hoodie">
      <div class="casting-body">
        <span class="strip-tag">Versión 01 · Claymation Tech</span>
        <h3>Legal Engineer (Hoodie + Lentes)</h3>
        <p style="font-size:0.84rem; color:var(--muted);">Plastilina más joven con barba regia, lentes de pasta, hoodie bajo el blazer y alerta de Tribunal Virtual detrás.</p>
        <button type="button" class="btn choose-char-btn" style="margin-top:auto;">✅ Elegir este como Personaje Oficial</button>
      </div>
    </article>
    <article class="casting-card" data-char-id="v02" data-char-name="V02 · Pixar 3D Cinematográfico" data-char-src="./assets/casting/v02_pixar_3d_cinematic.jpg">
      <img src="./assets/casting/v02_pixar_3d_cinematic.jpg" alt="Versión 02 Pixar 3D Cinematográfico">
      <div class="casting-body">
        <span class="strip-tag">Versión 02 · Cine 3D Deluxe</span>
        <h3>Abogado-Hacker 3D (Estilo Pixar)</h3>
        <p style="font-size:0.84rem; color:var(--muted);">Render 3D de estudio con piel suave, pin dorado de balanza, holograma rojo y el Cerro de la Silla al fondo.</p>
        <button type="button" class="btn choose-char-btn" style="margin-top:auto;">✅ Elegir este como Personaje Oficial</button>
      </div>
    </article>
    <article class="casting-card" data-char-id="v03" data-char-name="V03 · Designer Toy Vinilo 404" data-char-src="./assets/casting/v03_vinyl_designer_toy.jpg">
      <img src="./assets/casting/v03_vinyl_designer_toy.jpg" alt="Versión 03 Designer Toy Vinilo">
      <div class="casting-body">
        <span class="strip-tag">Versión 03 · Art Toy Vinilo</span>
        <h3>Coleccionable Vinilo 3D (404)</h3>
        <p style="font-size:0.84rem; color:var(--muted);">Acabado satinado tipo Designer Toy con mazo judicial en mano y laptop en Error 404. Ultra reconocible en feed.</p>
        <button type="button" class="btn choose-char-btn" style="margin-top:auto;">✅ Elegir este como Personaje Oficial</button>
      </div>
    </article>
    <article class="casting-card" data-char-id="v04" data-char-name="V04 · Puppet Artesanal de Fieltro" data-char-src="./assets/casting/v04_felt_puppet_artisan.jpg">
      <img src="./assets/casting/v04_felt_puppet_artisan.jpg" alt="Versión 04 Puppet de Fieltro">
      <div class="casting-body">
        <span class="strip-tag">Versión 04 · Stop-Motion Textil</span>
        <h3>Puppet de Fieltro y Lana</h3>
        <p style="font-size:0.84rem; color:var(--muted);">Estilo artesanal Wes Anderson con costuras y tela real. Da calidez humana inmediata para hablarle a familias y papás.</p>
        <button type="button" class="btn choose-char-btn" style="margin-top:auto;">✅ Elegir este como Personaje Oficial</button>
      </div>
    </article>
    <article class="casting-card" data-char-id="v05" data-char-name="V05 · Cartoon 2D Tinta en Mundo 3D" data-char-src="./assets/casting/v05_2d_ink_in_3d_world.jpg">
      <img src="./assets/casting/v05_2d_ink_in_3d_world.jpg" alt="Versión 05 Cartoon 2D en Mundo 3D">
      <div class="casting-body">
        <span class="strip-tag">Versión 05 · Híbrido 2D/3D</span>
        <h3>Caricatura 2D en Oficina 3D</h3>
        <p style="font-size:0.84rem; color:var(--muted);">Expresión facial de comedia explosiva con contornos de tinta negra sobre despacho 3D desenfocado.</p>
        <button type="button" class="btn choose-char-btn" style="margin-top:auto;">✅ Elegir este como Personaje Oficial</button>
      </div>
    </article>
    <article class="casting-card" data-char-id="v06" data-char-name="V06 · Cyber-Regio Monterrey" data-char-src="./assets/casting/v06_clay_regio_norteno_tech.jpg">
      <img src="./assets/casting/v06_clay_regio_norteno_tech.jpg" alt="Versión 06 Cyber-Regio Monterrey">
      <div class="casting-body">
        <span class="strip-tag">Versión 06 · Identidad Regia</span>
        <h3>Cyber-Regio (Cerro de la Silla)</h3>
        <p style="font-size:0.84rem; color:var(--muted);">Plastilina con el Cerro de la Silla gigante en la ventana, MacBook, termo y sombrero regio en el escritorio.</p>
        <button type="button" class="btn choose-char-btn" style="margin-top:auto;">✅ Elegir este como Personaje Oficial</button>
      </div>
    </article>
    <article class="casting-card" data-char-id="v07" data-char-name="V07 · Minifigura LEGO Legal Engineer" data-char-src="./assets/casting/v07_lego_minifig_cinematic.jpg">
      <img src="./assets/casting/v07_lego_minifig_cinematic.jpg" alt="Versión 07 LEGO Legal Engineer">
      <div class="casting-body">
        <span class="strip-tag">Versión 07 · LEGO Cinematográfico</span>
        <h3>Minifigura LEGO 404</h3>
        <p style="font-size:0.84rem; color:var(--muted);">Plástico ABS cinematográfico con gafete LEGAL ENGINEER y pantallas Error 404. Hipnótico para retención.</p>
        <button type="button" class="btn choose-char-btn" style="margin-top:auto;">✅ Elegir este como Personaje Oficial</button>
      </div>
    </article>
  </section>

  <!-- 1C. BLOQUE DESTACADO: ESPECIAL TRIBUNAL VIRTUAL PJENL (10 HALLAZGOS + NOVATO VS PRO) -->
  <div class="sec-head" id="especial-pjenl">
    <div>
      <h2>⚖️ Especial Tribunal Virtual PJENL — Tus 10 Videos Bomba</h2>
      <p>Los hallazgos exactos sobre enlaces 404, CPCNL Arts. 44–87 y Acuerdos 2011–2025 listos con su guion hablado y su descripción estilo <strong>Novato vs. Pro</strong> para disparar comentarios.</p>
    </div>
  </div>
  <section class="card">
    <div class="filter-bar" id="tv-spotlight-tabs" aria-label="Selector rápido de los 10 videos de Tribunal Virtual"></div>
    <div class="tv-spotlight" id="tv-spotlight-body"></div>
  </section>

  <!-- CARRUSEL CON TRANSICIÓN EXPANDIBLE HORIZONTAL (OPUSCLIP STYLE) -->
  <div class="sec-head">
    <div>
      <h2>🎭 Cast de Plastilina 3D &amp; Flujo de Escena</h2>
      <p>Pasa el cursor o toca cualquier tarjeta para activar la expansión acordeón horizontal.</p>
    </div>
  </div>
  <section class="accordion-strip" aria-label="Galería interactiva de poses">
    <article class="strip-card is-active" tabindex="0">
      <img src="./assets/v01/pose_01_susto.jpg" alt="V01 Pose 1 Susto ¡WATERS!">
      <div class="strip-overlay">
        <span class="strip-tag">0:00 – 0:03 · V01 Susto</span>
        <h3>El Gancho: ¡¡¡WATERS!!!</h3>
        <div class="strip-extra">
          Entra tu audio real de <strong>[Suspiro dramático]</strong> seguido del grito <strong>¡WATERS!</strong> con tu Legal Engineer de Hoodie y Lentes.
        </div>
      </div>
    </article>

    <article class="strip-card" tabindex="0">
      <img src="./assets/v01/cameo_victima_v04.jpg" alt="Don Peluche La Víctima V04">
      <div class="strip-overlay">
        <span class="strip-tag">0:04 – 0:14 · Don Peluche (La Víctima)</span>
        <h3>La Víctima en Apuros</h3>
        <div class="strip-extra">
          Don Peluche a punto de picarle a un botón peligroso o caer en <strong>Error 404</strong> / estafa, afectando <strong>Dinero, Tiempo o Juicio</strong>.
        </div>
      </div>
    </article>

    <article class="strip-card" tabindex="0">
      <img src="./assets/v01/v01_pose_02_experto_mascotita.jpg" alt="V01 Pose 2 Experto con Mascotita 4K">
      <div class="strip-overlay">
        <span class="strip-tag">0:15 – 0:42 · V01 + Mascotita 4K</span>
        <h3>El Blindaje + Mascotita</h3>
        <div class="strip-extra">
          Chuy Legal Engineer con candado dorado y su <strong>Mascotita Camarita 4K</strong> en el hombro explicando <strong>Art. 75</strong>, <strong>Art. 64</strong> y <strong>HITL</strong>.
        </div>
      </div>
    </article>

    <article class="strip-card" tabindex="0">
      <img src="./assets/v01/v01_pose_03_cta_mascotita.jpg" alt="V01 Pose 3 Cierre CTA con Mascotita 4K">
      <div class="strip-overlay">
        <span class="strip-tag">0:43 – 0:52 · V01 + Mascotita CTA</span>
        <h3>Guiño + CTA Comentarios</h3>
        <div class="strip-extra">
          Ambos guiñando y señalando abajo: <em>"Comenta <strong>WATERS</strong>, <strong>TRIBUNAL</strong> o <strong>TERMINO</strong> y te lo mando por DM."</em>
        </div>
      </div>
    </article>

    <article class="strip-card" tabindex="0">
      <img src="./assets/casting/v02_pixar_3d_cinematic.jpg" alt="Modo Rotativo Pixar 3D">
      <div class="strip-overlay">
        <span class="strip-tag">Universo Rotativo · 0 Aburrimiento</span>
        <h3>Estilos Alternos por Episodio</h3>
        <div class="strip-extra">
          Podemos alternar <code>V01 Clay Tech</code> con <code>V02 Pixar</code>, <code>V04 Don Peluche</code> o <code>V07 LEGO</code> para que el feed nunca sea repetitivo.
        </div>
      </div>
    </article>
  </section>

  <!-- FÁBRICA ¡WATERS! & REPRODUCTOR DE LOS 3 VIDEOS DE PRUEBA V01 -->
  <div class="sec-head" id="fabrica">
    <div>
      <h2>🎬 La Fábrica ¡WATERS! — Primeros 3 Videos de Prueba (Elenco V01 + Mascotita 4K)</h2>
      <p>Generados en vertical 1080×1920 con cortes dinámicos de zoom, cameo de Don Peluche y subtítulos Hormozi listos para montar tu voz.</p>
    </div>
  </div>
  <div class="audio-shield-banner" role="status">
    <span style="font-size:1.5rem;">🛡️</span>
    <div>
      <strong>0 Créditos de ElevenLabs y 0 Voz Robótica de macOS:</strong> Estos 3 videos nuevos se renderizaron en modo <code>--solo-video --cast v01</code> con un sutil golpe de alerta al <code>0:00</code> y pista limpia (sin el robot de macOS) para que revises ritmo, poses y subtítulos sobre la marcha antes de conectar tu voz real.
    </div>
  </div>
  <section class="factory-grid">
    <article class="card">
      <div class="ep-header">
        <span class="ep-day">PRUEBA V01 #1 · WHATSAPP</span>
        <span class="ep-cta">CTA: WATERS</span>
      </div>
      <h3>¡WATERS con el botón de Agente de IA en WhatsApp Business!</h3>
      <video class="video-frame" controls muted preload="metadata" poster="./assets/v01/pose_01_susto.jpg">
        <source src="./renders/V01_PRUEBA_01_WHATSAPP_WATERS.mp4" type="video/mp4">
      </video>
      <div class="cli-box">python3 proyectos/waters-serie/fabrica_waters.py --dia 1 --cast v01 --solo-video --output renders/V01_PRUEBA_01_WHATSAPP_WATERS.mp4</div>
    </article>

    <article class="card">
      <div class="ep-header">
        <span class="ep-day">PRUEBA V01 #2 · PJENL 404</span>
        <span class="ep-cta">CTA: TRIBUNAL</span>
      </div>
      <h3>¡WATERS! Enlaces 404 y 5 Superpoderes Ocultos del Tribunal Virtual</h3>
      <video class="video-frame" controls muted preload="metadata" poster="./assets/v01/v01_pose_02_experto_mascotita.jpg">
        <source src="./renders/V01_PRUEBA_02_TRIBUNAL_VIRTUAL_404.mp4" type="video/mp4">
      </video>
      <div class="cli-box">python3 proyectos/waters-serie/fabrica_waters.py --dia 2 --cast v01 --solo-video --output renders/V01_PRUEBA_02_TRIBUNAL_VIRTUAL_404.mp4</div>
    </article>

    <article class="card">
      <div class="ep-header">
        <span class="ep-day">PRUEBA V01 #3 · ART. 75 CPCNL</span>
        <span class="ep-cta">CTA: TERMINO</span>
      </div>
      <h3>¡WATERS! ¿Se cayó el Tribunal Virtual a las 11:58 PM? Así salvas tu término</h3>
      <video class="video-frame" controls muted preload="metadata" poster="./assets/v01/v01_pose_03_cta_mascotita.jpg">
        <source src="./renders/V01_PRUEBA_03_SALVAMENTO_ART75.mp4" type="video/mp4">
      </video>
      <div class="cli-box" id="custom-cli-cmd">python3 proyectos/waters-serie/fabrica_waters.py --dia 3 --cast v01 --audio ~/Downloads/tu_voz_real.mp3</div>
    </article>
  </section>

  <!-- CALENDARIO MAESTRO 30 DÍAS -->
  <div class="sec-head" id="calendario">
    <div>
      <h2>📅 Calendario Maestro de Contenido — 30 Días</h2>
      <p>Filtra por pilar temático o por impacto en la vida del usuario y expande cada día para leer y copiar su guion completo.</p>
    </div>
    <input type="search" id="cal-search" class="search-input" placeholder="Buscar en calendario (ej. Tribunal, 404, Claude, WhatsApp, FEJUD)...">
  </div>

  <div class="filter-bar" id="pillar-filters" aria-label="Filtros por pilar">
    <button class="chip active" data-pillar="ALL">Todos (30)</button>
    <button class="chip" data-pillar="Tribunal Virtual PJENL">⚖️ Tribunal Virtual PJENL</button>
    <button class="chip" data-pillar="Agentes IA &amp; WhatsApp/Claude">🤖 Agentes IA &amp; WhatsApp/Claude</button>
    <button class="chip" data-pillar="Ciberseguridad &amp; Red Team">🛡️ Ciberseguridad &amp; Red Team</button>
    <button class="chip" data-pillar="LegalTech">📜 LegalTech &amp; EU AI Act</button>
    <button class="chip" data-pillar="Finanzas &amp; Negocios">💰 Finanzas &amp; Negocios</button>
  </div>
  <div class="filter-bar" id="impact-filters" aria-label="Filtros por impacto">
    <button class="chip active" data-impact="ALL">Impacto: Todos</button>
    <button class="chip" data-impact="Dinero">💰 Dinero</button>
    <button class="chip" data-impact="Tiempo">⏱️ Tiempo</button>
    <button class="chip" data-impact="Trabajo">💼 Trabajo</button>
    <button class="chip" data-impact="Clientes">🤝 Clientes</button>
    <button class="chip" data-impact="Juicio">⚖️ Juicio</button>
  </div>

  <section class="calendar-grid" id="calendar-container"></section>

  <!-- RADIOGRAFÍA TRIBUNAL VIRTUAL PJENL + PARCHES RED TEAM -->
  <div class="sec-head" id="tribunal">
    <div>
      <h2>⚖️ Radiografía del Tribunal Virtual PJENL + Parches Red Team</h2>
      <p>Hallazgos reales verificados en <code>pjenl.gob.mx</code>, CPCNL Arts. 44–87, Acuerdos 2011–2025 y pruebas de ciberseguridad.</p>
    </div>
  </div>
  <section class="grid-2">
    <article class="card">
      <h3>🔍 Dónde está el "Manual" real (y por qué sale 404)</h3>
      <div class="norm-item">
        <strong>El manual interno (Acuerdo 4-II/2014) vs. Guía Pública</strong>
        <p>No existe un PDF único público porque el manual operativo es de administración judicial interna (<code>4-II/2014</code>). Para litigantes rige: <strong>Segundo Título Especial del CPCNL (Arts. 44–87)</strong>, <code>TVConvenio.pdf</code>, <code>TVPrivacidad.pdf</code> y Dirección de Informática (<code>cst@pjenl.gob.mx</code> · Tel. 81-2020-7751).</p>
      </div>
      <div class="norm-item">
        <strong>Enlaces caídos 404 vs. Rutas Vivas Reales</strong>
        <p>El link viejo <code>/Instituto/micrositio-tutoriales.html</code> da 404. Los tutoriales en MP4 vigentes viven en <code>pjenl.gob.mx/Instituto/Tutoriales/</code>, <code>SiC@Vi</code> y YouTube <code>@PJENL</code>.</p>
      </div>
      <div class="norm-item">
        <strong>Sobre "Dialoga" y Mediación</strong>
        <p>No figura un módulo llamado Dialoga en reglamentos publicados; la mediación electrónica oficial opera bajo el <strong>IMASC</strong> (Acuerdos <code>8/2017</code>, <code>16/2017</code>, <code>2/2019</code>, <code>10/2022</code>, <code>13/2022</code> y enlace UMC <code>14/2017</code>).</p>
      </div>
      <h3 style="margin-top:8px;">🛡️ 4 Parches Red Team Reales (LegalTech Lab)</h3>
      <div class="norm-item">
        <strong>1. Scrubbing RFC / CURP / CLABE (security.py)</strong>
        <p>Regex con <code>re.IGNORECASE</code> normalizado contra genéricos (<code>XAXX010101000</code> / <code>XEXX010101000</code>) y detección de CLABE de 18 dígitos con espacios o guiones sin falsos positivos en teléfonos o decimales.</p>
      </div>
      <div class="norm-item">
        <strong>2. Protección DoS Content-Length (api.py)</strong>
        <p>Tope máximo estricto de <code>1 MiB</code> (código <code>413</code>) y validación de enteros (<code>400</code>) en peticiones POST.</p>
      </div>
      <div class="norm-item">
        <strong>3. CORS Allowlist + Token HITL (api.py)</strong>
        <p>Eliminado comodín <code>*</code>; restringido a <code>localhost</code>, <code>127.0.0.1</code> y GitHub Pages oficial (<code>403</code> a terceros) + token <code>LEGAL_LAB_API_TOKEN</code>.</p>
      </div>
      <div class="norm-item">
        <strong>4. Integridad Forense SHA-256 + Lock OS (audit.py)</strong>
        <p>Bloqueo exclusivo concurrente <code>fcntl.flock</code> (POSIX) / <code>msvcrt.locking</code> (Windows) sobre archivo <code>.lock</code> para blindar la cadena de hashes.</p>
      </div>
    </article>

    <article class="card">
      <h3>⚡ Los 10 Superpoderes Ocultos del Tribunal Virtual (CPCNL 44–87)</h3>
      <div class="norm-item">
        <strong>1. Sobre Electrónico de Posiciones (Acuerdo 2-II/2025 · 02/07/2025)</strong>
        <p>Exhibir y resguardar pliego de posiciones de prueba confesional en formato electrónico cifrado hasta audiencia.</p>
      </div>
      <div class="norm-item">
        <strong>2. FEJUD + e.firma (Acuerdos 1-II/2025 y 7/2017)</strong>
        <p>Firma electrónica judicial avanzada propia del PJENL además de la FIEL del SAT.</p>
      </div>
      <div class="norm-item">
        <strong>3. Oficios Electrónicos a Empleadores y Bancos NO Partes (7/2022 y 8/2022)</strong>
        <p>Clave en pensión alimenticia para girar retenciones salariales electrónicas directo a empresas o bancos sin ser parte.</p>
      </div>
      <div class="norm-item">
        <strong>4. Escudo de Salvamento de Términos (Art. 75 + Bitácora Art. 53)</strong>
        <p>Si cae el portal en día de vencimiento, manifiéstalo en la promoción; el juez debe recabar reporte de Informática antes de desechar.</p>
      </div>
      <div class="norm-item">
        <strong>5. Desbloqueo Directo con el Administrador (Art. 64 CPCNL)</strong>
        <p>Con auto favorable de autorización, solicita habilitación directa al Administrador si el juzgado olvidó encender el permiso.</p>
      </div>
      <div class="norm-item">
        <strong>6. Autorización vs. Doble Clave para Promover (Arts. 61, 70 y 74)</strong>
        <p>Autorización por expediente, doble clave de envío y obligación del Secretario de certificar promociones al inicio y fin de jornada.</p>
      </div>
      <div class="norm-item">
        <strong>7. Exhortos Electrónicos e Incompetencias Mercantiles (Arts. 79–80, 5-II/2013, 2-II/2017, 7-II/2021)</strong>
        <p>Expediente electrónico independiente para exhortos, despachos e incompetencias sin correo físico.</p>
      </div>
      <div class="norm-item">
        <strong>8. Copias Certificadas Electrónicas (Acuerdo 3-II/2015)</strong>
        <p>Expedición digital con validez oficial evitando filas y fotocopiado físico.</p>
      </div>
      <div class="norm-item">
        <strong>9. Penal Acusatorio, Adolescentes y Laboral (15/2011, 5/2018, 16/2022)</strong>
        <p>Acceso digital a carpetas en materias especializadas del PJENL.</p>
      </div>
      <div class="norm-item">
        <strong>10. UMC en Línea, Cabinas y Citas UAPA (1-II/2024 · WhatsApp 81-8366-6781)</strong>
        <p>Agenda de actuarios en línea y citas de comparecencia para entrega de billetes de depósito.</p>
      </div>
    </article>
  </section>

  <!-- CURSOS, KIT DE SKILLS & CV MODULAR -->
  <div class="sec-head" id="productos">
    <div>
      <h2>💼 Ecosistema Monetizable &amp; CV Modular para Empresas</h2>
      <p>Modelo circular de <code>soyvibecoder.com</code> adaptado a tu carrera: ingresos digitales inmediatos + evidencia viva para Harvey.ai, Clara, Google y Microsoft.</p>
    </div>
  </div>
  <section class="grid-2" style="margin-bottom:28px;">
    <article class="card">
      <span class="ep-day">KIT DE BLINDAJE IA &amp; TRIBUNAL ($200 MXN)</span>
      <h3>Archivo de Skills Legales, Prompts &amp; Checklists</h3>
      <p style="font-size:0.88rem; color:var(--muted);">Inspirado en el paquete descargable de <code>/skills</code>:</p>
      <ul style="padding-left:18px; font-size:0.86rem; color:#d8e0ef; display:flex; flex-direction:column; gap:6px;">
        <li>5 System Prompts blindados para WhatsApp Business y Claude (Anti-alucinación y cero descuentos indebidos).</li>
        <li>Guía Maestra del Tribunal Virtual PJENL sin errores 404 (Arts. 44–87 + machote Art. 75 y Art. 64).</li>
        <li>Checklist de 4 Capas Red Team (Scrubbing RFC/CURP/CLABE, CORS, DoS 1 MiB y SHA-256).</li>
        <li>Matriz de 4 Niveles de Riesgo del EU AI Act traducida a español operativo.</li>
      </ul>
    </article>
    <article class="card">
      <span class="ep-day">CURSO EN 3 NIVELES ($400 MXN)</span>
      <h3>IA, Ciberseguridad y LegalTech sin Demandas</h3>
      <ul style="padding-left:18px; font-size:0.86rem; color:#d8e0ef; display:flex; flex-direction:column; gap:8px;">
        <li><strong>Nivel 1 · Ciudadano &amp; Familia:</strong> Blindar WhatsApp, detectar voces clonadas con IA y proteger tarjetas/cuentas de tu mamá y familia.</li>
        <li><strong>Nivel 2 · Negocios &amp; Emprendedores:</strong> Conectar bots de atención y CRM sin multas INAI/PROFECO ni promesas contractuales ilegales.</li>
        <li><strong>Nivel 3 · Abogados &amp; Empresas:</strong> Tribunal Virtual avanzado, gobernanza EU AI Act y auditoría de flujos Legal Engineering.</li>
      </ul>
    </article>
  </section>

  <!-- CV MODULAR -->
  <section class="card" id="cv-modular">
    <div class="ep-header">
      <div>
        <h3>🎯 CV Modular Interactivo por Vacante (Cero CVs de 6 Hojas)</h3>
        <p style="font-size:0.86rem; color:var(--muted);">Haz clic en la empresa objetivo para resaltar automáticamente tus tarjetas más fuertes y copiar tu pitch directo para el Hiring Manager.</p>
      </div>
      <button class="btn btn-primary" id="copy-pitch-btn">📋 Copiar Pitch para LinkedIn / DM</button>
    </div>
    <div class="filter-bar" id="cv-filters" style="margin-top:8px;">
      <button class="chip active" data-role="all">Vista General</button>
      <button class="chip" data-role="harvey">⚖️ Harvey.ai / Clara (Legal Engineer)</button>
      <button class="chip" data-role="bigtech">🌐 Google / Microsoft (AI Governance &amp; Policy)</button>
      <button class="chip" data-role="security">🛡️ Cybersecurity &amp; Red Team</button>
      <button class="chip" data-role="trainer">🎓 Instructor &amp; LegalTech Creator</button>
    </div>
    <p id="role-pitch-preview" style="padding:12px 14px; border-radius:12px; background:rgba(163,230,53,0.08); border:1px solid rgba(163,230,53,0.25); font-size:0.86rem; color:#e5f9c6;"></p>
    <div class="cv-grid" id="cv-cards-grid">
      <article class="cv-card" data-tags="harvey bigtech trainer">
        <span class="strip-tag">Base Jurídica + Tech</span>
        <h4>Licenciatura en Derecho + Enfoque LegalTech</h4>
        <p style="font-size:0.84rem; color:var(--muted);">Dominio procesal mexicano (CPCNL, LFPDPPP, Código Penal/Civil) combinado con diseño de prompts jurídicos, flujos electrónicos y responsabilidad de agentes autónomos.</p>
      </article>
      <article class="cv-card" data-tags="harvey security bigtech">
        <span class="strip-tag">Proof of Work Vivo</span>
        <h4>LegalTech Innovation Lab (81 Pytest Passing)</h4>
        <p style="font-size:0.84rem; color:var(--muted);">Laboratorio funcional en GitHub Pages integrando flujos reales de pensión alimenticia PJENL, librería normativa estructurada y endurecimiento Red Team verificado.</p>
      </article>
      <article class="cv-card" data-tags="security bigtech">
        <span class="strip-tag">Ciberseguridad Aplicada</span>
        <h4>Red Team Hardening &amp; PII Scrubbing</h4>
        <p style="font-size:0.84rem; color:var(--muted);">Implementación de scrubbing case-insensitive (RFC, CURP, CLABE), tope anti-DoS 1 MiB, CORS estricto con token HITL y auditoría SHA-256 con locks a nivel OS.</p>
      </article>
      <article class="cv-card" data-tags="bigtech harvey">
        <span class="strip-tag">Regulación Global</span>
        <h4>EU AI Act Compliance &amp; HITL Architecture</h4>
        <p style="font-size:0.84rem; color:var(--muted);">Clasificación de sistemas por nivel de riesgo (Inaceptable, Alto Riesgo RRHH/Finanzas), diseño de controles Human-in-the-Loop y trazabilidad ética.</p>
      </article>
      <article class="cv-card" data-tags="harvey trainer">
        <span class="strip-tag">Producto &amp; Contenido</span>
        <h4>Fábrica Automatizada de Video 3D (¡WATERS!)</h4>
        <p style="font-size:0.84rem; color:var(--muted);">Orquestación multi-agente (Imagen 3D, TTS, FFmpeg) para traducir riesgos complejos de ciberseguridad y ley en cápsulas educativas de alto alcance.</p>
      </article>
      <article class="cv-card" data-tags="trainer harvey">
        <span class="strip-tag">Comunicación</span>
        <h4>Vocación Docente y Visión Estratégica</h4>
        <p style="font-size:0.84rem; color:var(--muted);">Experiencia guiando estrategia digital legal de alto crecimiento (de &lt;100 a +40,000 seguidores orgánicos) y facilidad natural para explicar conceptos complejos con claridad.</p>
      </article>
    </div>
  </section>

  <!-- EXPLORADOR COMPLETO 100 SITUACIONES -->
  <div class="sec-head" id="catalogo-100">
    <div>
      <h2>🗂️ Explorador Completo de las 100 Situaciones ¡WATERS!</h2>
      <p>Catálogo vivo desde <code>100_SITUACIONES_WATERS.csv</code>. Busca cualquier palabra para improvisar o grabar nuevos episodios al instante.</p>
    </div>
    <input type="search" id="csv-search" class="search-input" placeholder="Buscar en los 100 capítulos (ej. cajero, pagare, pension, pickle, cors, ine)...">
  </div>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Categoría</th>
          <th>Escenario &amp; Susto</th>
          <th>Gancho ¡WATERS!</th>
          <th>Riesgo &amp; Blindaje</th>
          <th>CTA</th>
        </tr>
      </thead>
      <tbody id="csv-table-body"></tbody>
    </table>
  </div>

  <footer>
    <span>Captoora Studio · Personal OS de Jesús Gutiérrez (Chuy)</span>
    <span>Serie ¡WATERS! · Abogado + Ciberseguridad + IA</span>
  </footer>
</div>

<script id="waters-episodes-data" type="application/json">__EPISODES_JSON__</script>
<script id="waters-csv-data" type="application/json">__CSV_JSON__</script>
<script>
  const EPISODES = JSON.parse(document.getElementById('waters-episodes-data').textContent);
  const SITUATIONS = JSON.parse(document.getElementById('waters-csv-data').textContent);

  // 1. Escenarios ambientales estilo soyvibecoder.com
  document.querySelectorAll('.scene-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.body.dataset.scene = btn.dataset.sceneTarget;
      document.querySelectorAll('.scene-btn').forEach(b => b.setAttribute('aria-pressed', b === btn));
    });
  });

  // 2. Tarjetas acordeón horizontal táctiles / clic además de hover
  const stripCards = document.querySelectorAll('.strip-card');
  stripCards.forEach(card => {
    card.addEventListener('click', () => {
      stripCards.forEach(c => c.classList.remove('is-active'));
      card.classList.add('is-active');
    });
  });

  // 3. Calendario 30 Días + Filtros
  let currentPillar = 'ALL';
  let currentImpact = 'ALL';
  let calQuery = '';

  const calContainer = document.getElementById('calendar-container');

  function formatScriptText(ep) {
    const lines = [`EPISODIO DÍA ${ep.dia}: ${ep.titulo_viral}`, `CTA Palabra Clave: ${ep.cta_palabra}`, '---'];
    for (const [k, v] of Object.entries(ep.guion)) {
      lines.push(`${k}:\n${v}`);
    }
    return lines.join('\n\n');
  }

  function renderCalendar() {
    const filtered = EPISODES.filter(ep => {
      const matchPillar = currentPillar === 'ALL' || ep.pilar.includes(currentPillar);
      const matchImpact = currentImpact === 'ALL' || ep.impactos.some(im => im.toLowerCase().includes(currentImpact.toLowerCase()));
      const blob = (ep.titulo_viral + ' ' + ep.pilar + ' ' + ep.cta_palabra + ' ' + Object.values(ep.guion).join(' ')).toLowerCase();
      const matchSearch = !calQuery || blob.includes(calQuery);
      return matchPillar && matchImpact && matchSearch;
    });

    calContainer.innerHTML = '';
    if (!filtered.length) {
      calContainer.innerHTML = '<p style="color:var(--muted);">No hay episodios con esos filtros.</p>';
      return;
    }

    filtered.forEach(ep => {
      const card = document.createElement('article');
      card.className = 'card';

      const beatsHtml = Object.entries(ep.guion).map(([label, text]) => `
        <div class="beat-item">
          <strong>${label}</strong>
          <span>${text}</span>
        </div>
      `).join('');

      const impactsHtml = ep.impactos.map(i => `<span class="impact-pill">${i}</span>`).join('');

      card.innerHTML = `
        <div class="ep-header">
          <span class="ep-day">DÍA ${String(ep.dia).padStart(2, '0')} · ${ep.pilar}</span>
          <span class="ep-cta">DM: ${ep.cta_palabra}</span>
        </div>
        <h3 style="font-size:1.05rem;">${ep.titulo_viral}</h3>
        <div class="ep-impacts">${impactsHtml}</div>
        <p style="font-size:0.82rem; color:var(--muted);">🎁 <strong>Entrega DM:</strong> ${ep.recurso_entrega}</p>
        <details class="script-box">
          <summary>Ver guion completo (45–52s · 4 poses)</summary>
          <div class="beat-list">${beatsHtml}</div>
        </details>
        <div style="display:flex; gap:8px; margin-top:auto;">
          <button type="button" class="btn copy-script-btn" style="flex:1;">📋 Copiar Guion</button>
          <button type="button" class="btn select-cli-btn">⚙️ Comando MP4</button>
        </div>
      `;

      const copyBtn = card.querySelector('.copy-script-btn');
      copyBtn.addEventListener('click', () => {
        navigator.clipboard?.writeText(formatScriptText(ep));
        copyBtn.textContent = '✅ ¡Copiado!';
        setTimeout(() => copyBtn.textContent = '📋 Copiar Guion', 1600);
      });

      const cliBtn = card.querySelector('.select-cli-btn');
      cliBtn.addEventListener('click', () => {
        const cliBox = document.getElementById('custom-cli-cmd');
        cliBox.textContent = `python3 proyectos/waters-serie/fabrica_waters.py --dia ${ep.dia} --audio ~/Downloads/mi_voz_waters.mp3`;
        document.getElementById('fabrica').scrollIntoView({ behavior: 'smooth' });
      });

      calContainer.appendChild(card);
    });
  }

  document.querySelectorAll('#pillar-filters .chip').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#pillar-filters .chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentPillar = btn.dataset.pillar;
      renderCalendar();
    });
  });

  document.querySelectorAll('#impact-filters .chip').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#impact-filters .chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentImpact = btn.dataset.impact;
      renderCalendar();
    });
  });

  document.getElementById('cal-search').addEventListener('input', e => {
    calQuery = e.target.value.trim().toLowerCase();
    renderCalendar();
  });

  renderCalendar();

  // 4. CV Modular por Vacante
  const ROLE_PITCHES = {
    all: "Vista completa de perfil híbrido: Abogado Litigante + Legal Engineer + Especialista en Ciberseguridad e IA con laboratorio funcional en producción.",
    harvey: "Hola, soy Jesús Gutiérrez — abogado mexicano enfocado en Legal Engineering. Construí flujos auditables de IA jurídica sobre litigio real del Poder Judicial de NL (CPCNL Arts. 44–87, 81 tests Pytest en verde) y controles HITL listos para entornos legales exigentes como Harvey.ai y Clara.",
    bigtech: "Abogado especializado en AI Governance (EU AI Act), responsabilidad de agentes autónomos y cumplimiento ético-técnico. Traduzco regulación compleja en arquitectura segura Human-in-the-Loop y educación escalable para equipos y usuarios.",
    security: "Enfoque práctico de Red Team aplicado a apps de IA: regex PII scrubbing (RFC/CURP/CLABE), limitación DoS en payload (413/400), endurecimiento CORS/HITL Token (403) y cadenas de auditoría criptográficas SHA-256 con locks a nivel OS.",
    trainer: "Creador de la serie educativa '¡WATERS!' con fábrica de producción 3D automatizada en Python/FFmpeg, enseñando prevención digital y uso seguro de IA de forma cercana, entretenida y libre de tecnicismos intimidatorios."
  };

  let activeRole = 'all';
  const pitchPreview = document.getElementById('role-pitch-preview');
  const cvCards = document.querySelectorAll('#cv-cards-grid .cv-card');

  function updateCvRole(role) {
    activeRole = role;
    pitchPreview.textContent = ROLE_PITCHES[role];
    cvCards.forEach(c => {
      const tags = c.dataset.tags.split(' ');
      if (role === 'all') {
        c.classList.remove('is-highlighted', 'is-dimmed');
      } else if (tags.includes(role)) {
        c.classList.add('is-highlighted');
        c.classList.remove('is-dimmed');
      } else {
        c.classList.remove('is-highlighted');
        c.classList.add('is-dimmed');
      }
    });
  }

  document.querySelectorAll('#cv-filters .chip').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#cv-filters .chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      updateCvRole(btn.dataset.role);
    });
  });

  document.getElementById('copy-pitch-btn').addEventListener('click', (e) => {
    navigator.clipboard?.writeText(ROLE_PITCHES[activeRole]);
    const old = e.target.textContent;
    e.target.textContent = '✅ Pitch copiado';
    setTimeout(() => e.target.textContent = old, 1600);
  });

  updateCvRole('all');

  // 5. Tabla Buscador de 100 Situaciones
  const csvBody = document.getElementById('csv-table-body');
  function renderCsvTable(query = '') {
    const q = query.trim().toLowerCase();
    const rows = SITUATIONS.filter(r => !q || Object.values(r).join(' ').toLowerCase().includes(q));
    csvBody.innerHTML = rows.map(r => `
      <tr>
        <td><code>${r.ID}</code></td>
        <td><strong>${r.Categoria}</strong></td>
        <td><strong>${r.Escenario_Visual}</strong><br><small style="color:var(--muted);">${r.Situacion_El_Susto}</small></td>
        <td style="color:var(--gold); font-weight:600;">${r.Gancho_Waters}</td>
        <td><span style="color:#fda4af;">Riesgo:</span> ${r.Riesgo_Real}<br><span style="color:var(--lime);">Blindaje:</span> ${r.Blindaje_Solucion}</td>
        <td><span class="ep-cta">${r.CTA_Palabra_Clave}</span></td>
      </tr>
    `).join('');
  }

  document.getElementById('csv-search').addEventListener('input', e => renderCsvTable(e.target.value));
  renderCsvTable();

  // 6. Selector Oficial del Casting de 8 Versiones
  const castingCards = document.querySelectorAll('#casting-grid .casting-card');
  const chosenStatus = document.getElementById('chosen-character-status');
  const brandAvatar = document.querySelector('.brand-avatar');

  function applyChosenCharacter(charId) {
    castingCards.forEach(card => {
      const isMatch = card.dataset.charId === charId;
      card.classList.toggle('is-chosen', isMatch);
      const btn = card.querySelector('.choose-char-btn');
      if (isMatch) {
        chosenStatus.textContent = `Personaje activo: ${card.dataset.charName}`;
        if (brandAvatar) brandAvatar.src = card.dataset.charSrc;
        btn.classList.add('btn-primary');
        btn.textContent = '🌟 Personaje Seleccionado';
      } else {
        btn.classList.remove('btn-primary');
        btn.textContent = '✅ Elegir este como Personaje Oficial';
      }
    });
    try { localStorage.setItem('waters_chosen_char_v2', charId); } catch (e) {}
  }

  castingCards.forEach(card => {
    card.querySelector('.choose-char-btn').addEventListener('click', () => {
      applyChosenCharacter(card.dataset.charId);
    });
  });

  try {
    const savedChar = localStorage.getItem('waters_chosen_char_v2');
    if (savedChar && document.querySelector(`[data-char-id="${savedChar}"]`)) {
      applyChosenCharacter(savedChar);
    } else {
      applyChosenCharacter('v01');
    }
  } catch (e) {
    applyChosenCharacter('v01');
  }

  // 7. Bloque Destacado: Especial Tribunal Virtual PJENL (10 Videos + Copy Novato vs Pro)
  const tvEpisodes = EPISODES.filter(ep => ep.pilar.includes('Tribunal Virtual PJENL'));
  const tvTabs = document.getElementById('tv-spotlight-tabs');
  const tvBody = document.getElementById('tv-spotlight-body');

  function buildNovatoProCopy(ep) {
    const keys = Object.keys(ep.guion);
    const desmadre = ep.guion[keys[2]] || '';
    const blindaje = ep.guion[keys[3]] || '';
    return [
      `Comenta "${ep.cta_palabra}" y te mando la guía paso a paso 👇`,
      ``,
      `${ep.titulo_viral}`,
      ``,
      `𝗘𝗟 𝗡𝗢𝗩𝗔𝗧𝗢 🔒`,
      `${desmadre}`,
      ``,
      `𝗘𝗟 𝗣𝗥𝗢 🌙`,
      `${blindaje}`,
      ``,
      `1️⃣ 𝗧𝗜𝗘𝗠𝗣𝗢 ⏱️ — Menos filas físicas y cero enlaces rotos 404.`,
      `2️⃣ 𝗦𝗘𝗚𝗨𝗥𝗜𝗗𝗔𝗗 🛡️ — ${ep.recurso_entrega}.`,
      `3️⃣ 𝗔𝗖𝗖𝗜𝗢́𝗡 💬 — Comenta ${ep.cta_palabra} y te llega por DM.`,
      ``,
      `⚖️ Nota informativa: Contenido educativo sobre normativa procesal vigente en Nuevo León (CPCNL Arts. 44–87 y Acuerdos PJENL). No sustituye asesoría legal particular en un juicio en curso.`
    ].join('\n');
  }

  function renderTvSpotlight(dia) {
    const ep = tvEpisodes.find(e => e.dia === dia) || tvEpisodes[0];
    if (!ep) return;
    document.querySelectorAll('#tv-spotlight-tabs .chip').forEach(b => {
      b.classList.toggle('active', Number(b.dataset.tvDia) === ep.dia);
    });
    const beatsHtml = Object.entries(ep.guion).map(([k, v]) => `
      <div class="beat-item">
        <strong>${k}</strong>
        <span>${v}</span>
      </div>
    `).join('');
    const novatoProText = buildNovatoProCopy(ep);
    tvBody.innerHTML = `
      <div>
        <div class="ep-header" style="margin-bottom:10px;">
          <span class="ep-day">DÍA ${String(ep.dia).padStart(2, '0')} · ${ep.id_ref}</span>
          <span class="ep-cta">DM: ${ep.cta_palabra}</span>
        </div>
        <h3 style="margin-bottom:10px;">${ep.titulo_viral}</h3>
        <div class="beat-list">${beatsHtml}</div>
        <div style="margin-top:12px; display:flex; gap:8px; flex-wrap:wrap;">
          <button type="button" class="btn btn-primary" id="tv-copy-script">📋 Copiar Guion Hablado</button>
          <button type="button" class="btn" id="tv-solo-cmd">⚙️ Comando --solo-video</button>
        </div>
      </div>
      <div>
        <div class="ep-header" style="margin-bottom:8px;">
          <span class="strip-tag" style="margin:0;">Copy Viral Instagram · Novato 🔒 vs. Pro 🌙</span>
          <button type="button" class="btn" id="tv-copy-ig">📋 Copiar Copy Instagram</button>
        </div>
        <div class="novato-pro-box" id="tv-novato-pro-preview"></div>
      </div>
    `;
    document.getElementById('tv-novato-pro-preview').textContent = novatoProText;
    document.getElementById('tv-copy-script').addEventListener('click', (ev) => {
      navigator.clipboard?.writeText(formatScriptText(ep));
      ev.target.textContent = '✅ ¡Guion Copiado!';
      setTimeout(() => ev.target.textContent = '📋 Copiar Guion Hablado', 1500);
    });
    document.getElementById('tv-copy-ig').addEventListener('click', (ev) => {
      navigator.clipboard?.writeText(novatoProText);
      ev.target.textContent = '✅ ¡Copy IG Copiado!';
      setTimeout(() => ev.target.textContent = '📋 Copiar Copy Instagram', 1500);
    });
    document.getElementById('tv-solo-cmd').addEventListener('click', () => {
      const cliBox = document.getElementById('custom-cli-cmd');
      cliBox.textContent = `python3 proyectos/waters-serie/fabrica_waters.py --dia ${ep.dia} --solo-video`;
      document.getElementById('fabrica').scrollIntoView({ behavior: 'smooth' });
    });
  }

  tvEpisodes.forEach((ep, idx) => {
    const btn = document.createElement('button');
    btn.className = 'chip' + (idx === 0 ? ' active' : '');
    btn.dataset.tvDia = ep.dia;
    btn.textContent = `Día ${ep.dia} · ${ep.cta_palabra}`;
    btn.addEventListener('click', () => renderTvSpotlight(ep.dia));
    tvTabs.appendChild(btn);
  });
  if (tvEpisodes.length) renderTvSpotlight(tvEpisodes[0].dia);
</script>
</body>
</html>
"""

html_out = HTML_TEMPLATE.replace(
    "__EPISODES_JSON__", json.dumps(episodes, ensure_ascii=False).replace("</", "<\\/")
).replace(
    "__CSV_JSON__", json.dumps(situations, ensure_ascii=False).replace("</", "<\\/")
)

OUT_HTML.write_text(html_out, encoding="utf-8")
print(f"Built {OUT_HTML} ({len(html_out)} bytes) with {len(episodes)} episodes and {len(situations)} CSV rows.")
