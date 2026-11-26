#!/usr/bin/env python3
"""
Construye el proyecto HyperFrames 9:16 (1080x1920, 30 fps) para HRM-03:
"¿Por qué tu IA bloquea pruebas de seguridad en TU negocio?"
Combina fórmula Triple Hook (REF-14) + Attention Trap (REF-13) sobre estética
Editorial Crema (#F3EFEA) con Polarity Flip Dark (#111318) en el giro peligroso.
"""
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
BASE = ROOT / "proyectos/waters-serie/biblioteca_hermes_abliterated"
TIMINGS = BASE / "audio/hrm03_timings.json"
STICKERS_DIR = BASE / "01_stickers_black_canvas"
OUT_DIR = BASE / "04_piloto_hrm03_editorial_hf"


def chispa_svg(pose: str, dark: bool = False) -> str:
    """Personaje 2D original Captoora ('Chispa Editorial 2D') en 4 poses vectoriales."""
    ink = "#f8fafc" if dark else "#18181b"
    body_fill = "#1f2430" if dark else "#ebe6df"
    face_fill = "#111318" if dark else "#ffffff"
    coral = "#ff7a59" if dark else "#c93b1c"

    if pose == "shrug":
        arms = f"""
          <path d="M98 164 Q64 150 52 126" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
          <path d="M182 164 Q216 150 228 126" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
          <circle cx="50" cy="122" r="9" fill="{face_fill}" stroke="{ink}" stroke-width="4"/>
          <circle cx="230" cy="122" r="9" fill="{face_fill}" stroke="{ink}" stroke-width="4"/>
        """
    elif pose == "point":
        arms = f"""
          <path d="M98 164 Q76 184 96 196" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
          <path d="M182 162 Q212 132 218 82" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
          <circle cx="218" cy="76" r="9" fill="{coral}" stroke="{ink}" stroke-width="4"/>
        """
    elif pose == "shield":
        arms = f"""
          <path d="M98 164 Q78 140 72 110" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
          <path d="M182 164 Q202 140 208 110" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
          <circle cx="72" cy="105" r="9" fill="{coral}" stroke="{ink}" stroke-width="4"/>
          <circle cx="208" cy="105" r="9" fill="{coral}" stroke="{ink}" stroke-width="4"/>
        """
    else:  # cta
        arms = f"""
          <path d="M98 164 Q70 142 64 102" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
          <path d="M182 164 Q210 142 216 102" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
          <circle cx="64" cy="96" r="9" fill="{coral}" stroke="{ink}" stroke-width="4"/>
          <circle cx="216" cy="96" r="9" fill="{coral}" stroke="{ink}" stroke-width="4"/>
        """

    return f"""
      <svg viewBox="0 0 280 220" width="280" height="220" aria-hidden="true">
        {arms}
        <!-- Torso sudadera Captoora -->
        <rect x="96" y="148" width="88" height="64" rx="22" fill="{body_fill}" stroke="{ink}" stroke-width="4.5"/>
        <circle cx="154" cy="176" r="6" fill="{coral}"/>
        <!-- Cabeza monitor redondeado -->
        <rect x="86" y="54" width="108" height="90" rx="26" fill="{face_fill}" stroke="{ink}" stroke-width="4.5"/>
        <!-- Gorra coral Captoora -->
        <path d="M88 64 Q140 20 192 64 Z" fill="{coral}" stroke="{ink}" stroke-width="4.5" stroke-linejoin="round"/>
        <rect x="82" y="58" width="116" height="14" rx="7" fill="{coral}" stroke="{ink}" stroke-width="4"/>
        <!-- Ojos doble lente OO -->
        <circle cx="118" cy="98" r="14" fill="none" stroke="{ink}" stroke-width="4.5"/>
        <circle cx="118" cy="98" r="5" fill="{coral}"/>
        <circle cx="162" cy="98" r="14" fill="none" stroke="{ink}" stroke-width="4.5"/>
        <circle cx="162" cy="98" r="5" fill="{coral}"/>
        <!-- Sonrisa / expresión -->
        <path d="M126 124 Q140 134 154 124" fill="none" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>
      </svg>
    """


def build_hrm03_html(meta: Dict[str, Any]) -> str:
    dur = round(float(meta["total_duration"]), 2)
    clips: List[Dict[str, Any]] = meta["clips"]
    by_id = {c["id"]: c for c in clips}

    b1 = by_id["B1_triple_hook"]
    b2 = by_id["B2_stakes"]
    b3 = by_id["B3_head_fake"]
    b4 = by_id["B4_candados"]
    b5 = by_id["B5_cta"]

    s1_start, s1_end = 0.0, round(float(b2["start"]), 2)
    s2_start, s2_end = s1_end, round(float(b3["start"]), 2)
    s3_start, s3_end = s2_end, round(float(b4["start"]), 2)
    s4_start, s4_end = s3_end, round(float(b5["start"]), 2)
    s5_start, s5_end = s4_end, dur

    d1 = round(s1_end - s1_start, 2)
    d2 = round(s2_end - s2_start, 2)
    d3 = round(s3_end - s3_start, 2)
    d4 = round(s4_end - s4_start, 2)
    d5 = round(s5_end - s5_start, 2)

    s1_exit = round(max(0.4, s1_end - 0.22), 2)
    s2_exit = round(max(s2_start + 0.5, s2_end - 0.22), 2)
    s3_exit = round(max(s3_start + 0.5, s3_end - 0.22), 2)
    s4_exit = round(max(s4_start + 0.5, s4_end - 0.22), 2)

    s1_card_in = 0.35
    s1_snap_in = round(min(s1_end - 1.2, 4.2), 2)

    s2_chips_in = round(s2_start + 0.55, 2)
    s2_bar_in = round(s2_start + 1.4, 2)

    s3_flip_in = round(max(0.1, s3_start - 0.12), 2)
    s3_card_in = round(s3_start + 0.55, 2)
    s3_flip_out = round(max(s3_start + 0.6, s4_start - 0.14), 2)

    s4_l1 = round(s4_start + 0.85, 2)
    s4_l2 = round(s4_start + 2.25, 2)
    s4_l3 = round(s4_start + 3.65, 2)

    s5_pill_in = round(s5_start + 0.4, 2)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>HRM-03 · ¿Por qué tu IA bloquea pruebas de seguridad en TU negocio?</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #f3efea;
      color: #141416;
      font-family: "Outfit", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    #root {{
      position: relative;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #f3efea;
    }}
    .bg-stage {{
      position: absolute;
      inset: 0;
      z-index: 1;
      overflow: hidden;
    }}
    .paper-dots {{
      position: absolute;
      inset: 0;
      background-image: radial-gradient(rgba(20, 20, 22, 0.08) 1.5px, transparent 1.5px);
      background-size: 40px 40px;
    }}
    .glow-coral {{
      position: absolute;
      width: 780px;
      height: 780px;
      left: 150px;
      top: 140px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(224, 72, 38, 0.14) 0%, rgba(224, 72, 38, 0) 68%);
    }}
    .dark-backdrop {{
      position: absolute;
      inset: 0;
      background: #111318;
      opacity: 0;
      z-index: 2;
    }}
    .dark-glow {{
      position: absolute;
      width: 760px;
      height: 760px;
      left: 160px;
      top: 200px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(255, 122, 89, 0.22) 0%, rgba(255, 122, 89, 0) 70%);
    }}
    /* Zona segura estricta: y=156..1376px, x=64..936px (rail derecho + 544px abajo libres para CapCut Pro) */
    .safe-stage {{
      position: absolute;
      top: 156px;
      left: 64px;
      width: 872px;
      height: 1220px;
      z-index: 10;
    }}
    .top-dots-clip {{
      position: absolute;
      top: 0;
      left: 0;
      width: 872px;
      height: 44px;
      display: flex;
      justify-content: center;
      align-items: center;
    }}
    .dots-row {{
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 10px 22px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.9);
      border: 2px solid #dfd7cd;
    }}
    .dot-seg {{
      width: 24px;
      height: 10px;
      border-radius: 999px;
      background: #d5cdc2;
    }}
    .dot-seg.is-active {{
      width: 56px;
      background: #c93b1c;
    }}
    .scene-slot {{
      position: absolute;
      top: 66px;
      left: 0;
      width: 872px;
      height: 1140px;
    }}
    .scene-inner {{
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
    }}
    .editorial-head {{
      width: 100%;
    }}
    .kicker {{
      display: inline-block;
      padding: 8px 20px;
      border-radius: 999px;
      background: #ffffff;
      border: 2px solid #dfd7cd;
      color: #c93b1c;
      font-size: 28px;
      font-weight: 800;
      letter-spacing: 0.03em;
      margin-bottom: 18px;
    }}
    .kicker-dark {{
      background: #1b202b;
      border-color: #343d52;
      color: #ff7a59;
    }}
    .h1-edit {{
      font-size: 68px;
      font-weight: 900;
      line-height: 1.05;
      color: #141416;
      letter-spacing: -0.025em;
      margin-bottom: 18px;
    }}
    .h1-edit-dark {{
      color: #ffffff;
    }}
    .serif-it {{
      font-family: "Playfair Display", Georgia, serif;
      font-style: italic;
      font-weight: 700;
      color: #c93b1c;
    }}
    .serif-it-dark {{
      color: #ff7a59;
    }}
    .sub-edit {{
      font-size: 32px;
      line-height: 1.32;
      color: #3d3f45;
      font-weight: 600;
      margin-bottom: 24px;
    }}
    .sub-edit-dark {{
      color: #cbd5e1;
    }}
    .ui-card {{
      width: 100%;
      background: #ffffff;
      border: 2px solid #e2dad0;
      border-radius: 28px;
      padding: 28px 32px;
      text-align: left;
    }}
    .ui-card-dark {{
      background: #191d26;
      border: 3px solid #fb7185;
      border-radius: 28px;
      padding: 26px 30px;
      text-align: left;
      width: 100%;
    }}
    .prompt-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 18px;
      border-bottom: 2px solid #f0ebe4;
      margin-bottom: 18px;
    }}
    .prompt-txt {{
      font-size: 30px;
      font-weight: 700;
      color: #141416;
    }}
    .badge-coral {{
      padding: 8px 18px;
      border-radius: 999px;
      background: #c93b1c;
      color: #ffffff;
      font-size: 30px;
      font-weight: 800;
      white-space: nowrap;
    }}
    .snap-note {{
      font-size: 30px;
      font-weight: 700;
      color: #c93b1c;
    }}
    .chips-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-bottom: 20px;
    }}
    .stake-chip {{
      background: #ffffff;
      border: 2px solid #e2dad0;
      border-radius: 22px;
      padding: 18px 14px;
      text-align: center;
    }}
    .chip-top {{
      font-size: 28px;
      font-weight: 900;
      color: #c93b1c;
      margin-bottom: 6px;
    }}
    .chip-bot {{
      font-size: 28px;
      font-weight: 700;
      color: #141416;
    }}
    .meter-track {{
      width: 100%;
      height: 22px;
      border-radius: 999px;
      background: #ebe4dc;
      overflow: hidden;
      margin-top: 14px;
    }}
    .meter-fill {{
      width: 84%;
      height: 100%;
      border-radius: 999px;
      background: #c93b1c;
      transform-origin: left center;
    }}
    .dark-flex {{
      display: flex;
      align-items: center;
      gap: 24px;
    }}
    .dark-stk {{
      width: 220px;
      height: 220px;
      object-fit: contain;
      flex-shrink: 0;
    }}
    .dark-warn-title {{
      font-size: 32px;
      font-weight: 900;
      color: #ff7a59;
      margin-bottom: 10px;
    }}
    .dark-warn-body {{
      font-size: 29px;
      line-height: 1.32;
      color: #f8fafc;
      font-weight: 600;
    }}
    .locks-stack {{
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .lock-card {{
      background: #ffffff;
      border: 2px solid #d5e6dc;
      border-left: 10px solid #1e7b4f;
      border-radius: 22px;
      padding: 20px 26px;
      display: flex;
      align-items: center;
      gap: 18px;
      text-align: left;
    }}
    .lock-num {{
      font-size: 30px;
      font-weight: 900;
      color: #1e7b4f;
      min-width: 48px;
    }}
    .lock-txt {{
      font-size: 30px;
      font-weight: 800;
      color: #141416;
    }}
    .comment-bar {{
      width: 100%;
      background: #ffffff;
      border: 3px solid #c93b1c;
      border-radius: 999px;
      padding: 22px 26px 22px 36px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 18px;
    }}
    .comment-txt {{
      font-size: 40px;
      font-weight: 900;
      color: #141416;
      letter-spacing: 0.03em;
    }}
    .comment-btn {{
      padding: 12px 28px;
      border-radius: 999px;
      background: #c93b1c;
      color: #ffffff;
      font-size: 30px;
      font-weight: 900;
    }}
    .char-wrap {{
      width: 280px;
      height: 220px;
      display: flex;
      justify-content: center;
      align-items: flex-end;
    }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="hrm03_editorial_sandbox" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920" data-fps="30">
    <audio id="master-audio" class="clip" src="assets/hrm03_master.wav" data-start="0" data-duration="{dur}" data-volume="1" data-track-index="10"></audio>

    <div class="bg-stage" data-layout-ignore>
      <div id="paper-dots" class="paper-dots"></div>
      <div id="glow-coral" class="glow-coral"></div>
      <div id="dark-backdrop" class="dark-backdrop">
        <div class="dark-glow"></div>
      </div>
    </div>

    <div class="safe-stage">
      <div id="top-dots" class="clip top-dots-clip" data-start="0" data-duration="{dur}">
        <div class="dots-row">
          <span id="dot-1" class="dot-seg is-active"></span>
          <span id="dot-2" class="dot-seg"></span>
          <span id="dot-3" class="dot-seg"></span>
          <span id="dot-4" class="dot-seg"></span>
        </div>
      </div>

      <!-- S1: TRIPLE HOOK -->
      <div id="sc-1" class="clip scene-slot" data-start="{s1_start}" data-duration="{d1}">
        <div id="sc-1-inner" class="scene-inner">
          <div class="editorial-head">
            <span class="kicker">TRIPLE HOOK · HRM-03</span>
            <h1 class="h1-edit">tu IA te <span class="serif-it">bloquea</span></h1>
            <p class="sub-edit">Al auditar TU propio negocio, el 90% cae en una trampa peor.</p>
            <div id="s1-card" class="ui-card">
              <div class="prompt-row">
                <span class="prompt-txt">"Audita fugas en mi web..."</span>
                <span class="badge-coral">BLOQUEADO</span>
              </div>
              <div id="s1-snap" class="snap-note">Giro real: sin censura ≠ seguro</div>
            </div>
          </div>
          <div id="s1-char" class="char-wrap">{chispa_svg("shrug", dark=False)}</div>
        </div>
      </div>

      <!-- S2: STAKES + BIG QUESTION -->
      <div id="sc-2" class="clip scene-slot" data-start="{s2_start}" data-duration="{d2}">
        <div id="sc-2-inner" class="scene-inner">
          <div class="editorial-head">
            <span class="kicker">LO QUE ESTÁ EN JUEGO</span>
            <h1 class="h1-edit">48 horas <span class="serif-it">o fugas</span></h1>
            <p class="sub-edit">¿Cómo revisas permisos antes de entregar sin que la nube te frene?</p>
            <div id="s2-chips" class="chips-grid">
              <div class="stake-chip"><div class="chip-top">48h</div><div class="chip-bot">Límite</div></div>
              <div class="stake-chip"><div class="chip-top">Web</div><div class="chip-bot">Cliente</div></div>
              <div class="stake-chip"><div class="chip-top">Fuga</div><div class="chip-bot">Permisos</div></div>
            </div>
            <div class="ui-card">
              <div class="prompt-txt">Riesgo si lanzas a ciegas</div>
              <div class="meter-track"><div id="s2-bar" class="meter-fill"></div></div>
            </div>
          </div>
          <div class="char-wrap">{chispa_svg("point", dark=False)}</div>
        </div>
      </div>

      <!-- S3: HEAD FAKE (DARK POLARITY FLIP) -->
      <div id="sc-3" class="clip scene-slot" data-start="{s3_start}" data-duration="{d3}">
        <div id="sc-3-inner" class="scene-inner">
          <div class="editorial-head">
            <span class="kicker kicker-dark">EL GIRO PELIGROSO</span>
            <h1 class="h1-edit h1-edit-dark">el giro <span class="serif-it serif-it-dark">peligroso</span></h1>
            <p class="sub-edit sub-edit-dark">Un agente local sin frenos y sin aislamiento lee tus llaves con 1 correo.</p>
            <div id="s3-card" class="ui-card-dark">
              <div class="dark-flex">
                <img class="dark-stk" src="assets/stk_03_filtros_vs_auditoria.png" alt="Filtros vs Auditoría local" />
                <div>
                  <div class="dark-warn-title">TERMINAL ABIERTA + PROMPT INJECTION</div>
                  <div class="dark-warn-body">Autorización propia NO sirve si ejecutas comandos directo en tu máquina.</div>
                </div>
              </div>
            </div>
          </div>
          <div class="char-wrap">{chispa_svg("shield", dark=True)}</div>
        </div>
      </div>

      <!-- S4: 3 CANDADOS -->
      <div id="sc-4" class="clip scene-slot" data-start="{s4_start}" data-duration="{d4}">
        <div id="sc-4-inner" class="scene-inner">
          <div class="editorial-head">
            <span class="kicker">ARQUITECTURA DEFENSIVA</span>
            <h1 class="h1-edit">los 3 <span class="serif-it">candados</span></h1>
            <p class="sub-edit">Audita TU propio entorno con caja cerrada y control humano.</p>
            <div class="locks-stack">
              <div id="s4-l1" class="lock-card"><span class="lock-num">01</span><span class="lock-txt">Docker Sandbox aislado</span></div>
              <div id="s4-l2" class="lock-card"><span class="lock-num">02</span><span class="lock-txt">Firewall UFW cerrado</span></div>
              <div id="s4-l3" class="lock-card"><span class="lock-num">03</span><span class="lock-txt">Aprobación humana obligatoria</span></div>
            </div>
          </div>
          <div class="char-wrap">{chispa_svg("point", dark=False)}</div>
        </div>
      </div>

      <!-- S5: CTA COMPACT -->
      <div id="sc-5" class="clip scene-slot" data-start="{s5_start}" data-duration="{d5}">
        <div id="sc-5-inner" class="scene-inner">
          <div class="editorial-head">
            <h1 class="h1-edit">Comenta <span class="serif-it">SANDBOX</span></h1>
            <div id="s5-pill" class="comment-bar">
              <span class="comment-txt">SANDBOX |</span>
              <span class="comment-btn">ENVIAR</span>
            </div>
            <p class="sub-edit">Checklist de 3 candados.</p>
          </div>
          <div class="char-wrap">{chispa_svg("cta", dark=False)}</div>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});

      // Movimiento continuo del papel + halo coral + respiración 2D de Chispa (evita dead_stretch sin extender duración)
      tl.fromTo("#paper-dots", {{ backgroundPosition: "0px 0px" }}, {{ backgroundPosition: "40px 40px", duration: {dur}, ease: "none" }}, 0);
      tl.fromTo("#glow-coral", {{ x: -40, y: 0 }}, {{ x: 80, y: 120, duration: {dur}, ease: "sine.inOut" }}, 0);
      tl.fromTo(".char-wrap", {{ y: 0 }}, {{ y: -12, duration: 1.8, repeat: Math.max(1, Math.floor({dur} / 1.8) - 1), yoyo: true, ease: "sine.inOut" }}, 0);

      // S1 Hook
      tl.fromTo("#sc-1-inner", {{ y: 14, opacity: 1 }}, {{ y: 0, opacity: 1, duration: 0.32, ease: "power3.out" }}, 0);
      tl.fromTo("#s1-card", {{ scale: 0.94 }}, {{ scale: 1, duration: 0.38, ease: "back.out(1.4)" }}, {s1_card_in});
      tl.fromTo("#s1-snap", {{ opacity: 0.2, x: -16 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power2.out" }}, {s1_snap_in});
      tl.to("#sc-1-inner", {{ x: -70, opacity: 0, duration: 0.22, ease: "power2.in" }}, {s1_exit});

      // S2 Stakes
      tl.to("#dot-1", {{ width: 24, backgroundColor: "#d5cdc2", duration: 0.2 }}, {s2_start});
      tl.to("#dot-2", {{ width: 56, backgroundColor: "#c93b1c", duration: 0.2 }}, {s2_start});
      tl.fromTo("#sc-2-inner", {{ x: 70, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {s2_start});
      tl.fromTo("#s2-chips", {{ y: 18, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power2.out" }}, {s2_chips_in});
      tl.fromTo("#s2-bar", {{ scaleX: 0.08 }}, {{ scaleX: 1, duration: 0.9, ease: "power3.out" }}, {s2_bar_in});
      tl.to("#sc-2-inner", {{ x: -70, opacity: 0, duration: 0.22, ease: "power2.in" }}, {s2_exit});

      // S3 Polarity Flip -> Dark (#111318)
      tl.to("#dot-2", {{ width: 24, backgroundColor: "#d5cdc2", duration: 0.2 }}, {s3_start});
      tl.to("#dot-3", {{ width: 56, backgroundColor: "#ff7a59", duration: 0.2 }}, {s3_start});
      tl.to("#dark-backdrop", {{ opacity: 1, duration: 0.22, ease: "power2.out" }}, {s3_flip_in});
      tl.fromTo("#sc-3-inner", {{ scale: 0.95, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.32, ease: "power3.out" }}, {s3_start});
      tl.fromTo("#s3-card", {{ y: 20, opacity: 0.3 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power2.out" }}, {s3_card_in});
      tl.to("#sc-3-inner", {{ x: -70, opacity: 0, duration: 0.22, ease: "power2.in" }}, {s3_exit});
      tl.to("#dark-backdrop", {{ opacity: 0, duration: 0.22, ease: "power2.in" }}, {s3_flip_out});

      // S4 Candados -> Vuelta a Editorial Crema
      tl.to("#dot-3", {{ width: 24, backgroundColor: "#d5cdc2", duration: 0.2 }}, {s4_start});
      tl.to("#dot-4", {{ width: 56, backgroundColor: "#1e7b4f", duration: 0.2 }}, {s4_start});
      tl.fromTo("#sc-4-inner", {{ x: 70, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {s4_start});
      tl.fromTo("#s4-l1", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {s4_l1});
      tl.fromTo("#s4-l2", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {s4_l2});
      tl.fromTo("#s4-l3", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {s4_l3});
      tl.to("#sc-4-inner", {{ x: -70, opacity: 0, duration: 0.22, ease: "power2.in" }}, {s4_exit});

      // S5 CTA
      tl.fromTo("#sc-5-inner", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {s5_start});
      tl.fromTo("#s5-pill", {{ scale: 0.9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.38, ease: "back.out(1.6)" }}, {s5_pill_in});

      window.__timelines = window.__timelines || {{}};
      window.__timelines["hrm03_editorial_sandbox"] = tl;
    }})();
  </script>
</body>
</html>
"""


def main() -> int:
    data = json.loads(TIMINGS.read_text(encoding="utf-8"))
    meta = data["hrm03"]

    assets_dir = OUT_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / ".gitignore").write_text(".hyperframes/\nrenders/\nassets/*.wav\n", encoding="utf-8")

    shutil.copy2(BASE / "audio/hrm03_master.wav", assets_dir / "hrm03_master.wav")
    shutil.copy2(STICKERS_DIR / "stk_03_filtros_vs_auditoria.png", assets_dir / "stk_03_filtros_vs_auditoria.png")

    html = build_hrm03_html(meta)
    out_html = OUT_DIR / "index.html"
    out_html.write_text(html, encoding="utf-8")
    print(f"BUILT {out_html} (dur={meta['total_duration']}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
