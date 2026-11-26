#!/usr/bin/env python3
"""
Construye el proyecto HyperFrames 9:16 (1080x1920, 30 fps) para HRM-01:
"¿Qué es un modelo ABLITERATED?" en formato Black Canvas Coloreado.
Lee los tiempos reales de audio/hrm01_timings.json y genera 03_piloto_hrm01_hf/index.html.
"""
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
BASE = ROOT / "proyectos/waters-serie/biblioteca_hermes_abliterated"
TIMINGS = BASE / "audio/hrm01_timings.json"
STICKERS_DIR = BASE / "01_stickers_black_canvas"
OUT_DIR = BASE / "03_piloto_hrm01_hf"

REQUIRED_STICKERS = [
    "stk_01_abliteration_vector.png",
    "stk_04_docker_sandbox_escudo.png",
    "stk_06_alerta_prompt_injection.png",
]


def build_hrm01_html(meta: Dict[str, Any]) -> str:
    dur = round(float(meta["total_duration"]), 2)
    clips: List[Dict[str, Any]] = meta["clips"]
    by_id = {c["id"]: c for c in clips}

    b1 = by_id["B1_hook"]
    b2 = by_id["B2_vector"]
    b3 = by_id["B3_realidad"]
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

    s2_diag_in = round(s2_start + 0.45, 2)
    s2_vec_bad = round(s2_start + 1.4, 2)
    s2_vec_good = round(s2_start + 2.6, 2)

    s3_box1_in = round(s3_start + 0.45, 2)
    s3_box2_in = round(s3_start + 1.8, 2)

    s4_alert_in = round(s4_start + 0.35, 2)
    s4_lock1_in = round(s4_start + 1.8, 2)
    s4_lock2_in = round(s4_start + 3.1, 2)
    s4_lock3_in = round(s4_start + 4.4, 2)

    s5_cta_in = round(s5_start + 0.45, 2)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>HRM-01 · ¿Qué es un modelo ABLITERATED? (Black Canvas Coloreado)</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #0d0e12;
      color: #f8fafc;
      font-family: "Outfit", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    #root {{
      position: relative;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #0d0e12;
    }}
    .bg-stage {{
      position: absolute;
      inset: 0;
      z-index: 1;
      overflow: hidden;
    }}
    .grid-bg {{
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(to right, rgba(255, 255, 255, 0.038) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.038) 1px, transparent 1px);
      background-size: 54px 54px;
    }}
    .orb-cyan {{
      position: absolute;
      width: 760px;
      height: 760px;
      left: -140px;
      top: 120px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.22) 0%, rgba(56, 189, 248, 0) 70%);
    }}
    .orb-amber {{
      position: absolute;
      width: 720px;
      height: 720px;
      right: -160px;
      top: 560px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(245, 158, 11, 0.16) 0%, rgba(245, 158, 11, 0) 70%);
    }}
    /* Banda segura estricta: y=168..1328px, x=64..936px (rail derecho libre + >590px abajo libres para CapCut Pro) */
    .safe-stage {{
      position: absolute;
      top: 168px;
      left: 64px;
      width: 872px;
      height: 1160px;
      z-index: 10;
    }}
    .top-bar-clip {{
      position: absolute;
      top: 0;
      left: 0;
      width: 872px;
      height: 62px;
    }}
    .top-bar {{
      display: flex;
      align-items: center;
      gap: 18px;
      height: 62px;
      padding: 0 22px;
      border-radius: 999px;
      background: #141720;
      border: 2px solid #2b3244;
    }}
    .series-badge {{
      color: #38bdf8;
      font-size: 28px;
      font-weight: 800;
      letter-spacing: 0.04em;
      white-space: nowrap;
    }}
    .prog-track {{
      flex: 1;
      height: 10px;
      border-radius: 999px;
      background: #1f2535;
      overflow: hidden;
    }}
    .prog-fill {{
      width: 100%;
      height: 100%;
      background: #38bdf8;
      transform-origin: left center;
    }}
    .scene-slot {{
      position: absolute;
      top: 90px;
      left: 0;
      width: 872px;
      height: 1060px;
    }}
    .board-card {{
      background: #13151d;
      border: 3px solid #2b3142;
      border-radius: 34px;
      padding: 40px 42px;
    }}
    .pill {{
      display: inline-block;
      padding: 10px 22px;
      border-radius: 999px;
      font-size: 28px;
      font-weight: 800;
      margin-bottom: 20px;
      letter-spacing: 0.03em;
    }}
    .pill-amber {{
      background: rgba(245, 158, 11, 0.18);
      color: #fbbf24;
      border: 2px solid #f59e0b;
    }}
    .pill-cyan {{
      background: rgba(56, 189, 248, 0.16);
      color: #38bdf8;
      border: 2px solid #38bdf8;
    }}
    .pill-rose {{
      background: rgba(251, 113, 133, 0.16);
      color: #fb7185;
      border: 2px solid #fb7185;
    }}
    .pill-emerald {{
      background: rgba(52, 211, 153, 0.16);
      color: #34d399;
      border: 2px solid #34d399;
    }}
    .h1 {{
      font-size: 56px;
      font-weight: 900;
      line-height: 1.08;
      color: #ffffff;
      margin-bottom: 16px;
      letter-spacing: -0.02em;
    }}
    .lead {{
      font-size: 32px;
      line-height: 1.35;
      color: #cbd5e1;
      font-weight: 600;
      margin-bottom: 26px;
    }}
    .sticker-stage {{
      background: #0d0e12;
      border: 2px solid #283044;
      border-radius: 26px;
      padding: 16px;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
    }}
    .sticker-main {{
      width: 100%;
      max-height: 500px;
      object-fit: contain;
      display: block;
    }}
    .diagram-panel {{
      background: #0d0e12;
      border: 2px solid #38bdf8;
      border-radius: 26px;
      padding: 22px;
    }}
    .diagram-panel svg {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .stack-col {{
      display: flex;
      flex-direction: column;
      gap: 22px;
    }}
    .node-box {{
      background: #0d0e12;
      border: 3px solid #2e3445;
      border-radius: 26px;
      padding: 28px 30px;
    }}
    .node-red {{ border-color: #fb7185; }}
    .node-green {{ border-color: #34d399; }}
    .node-label {{
      font-size: 30px;
      font-weight: 900;
      margin-bottom: 10px;
      letter-spacing: 0.03em;
    }}
    .c-red {{ color: #fb7185; }}
    .c-green {{ color: #34d399; }}
    .node-text {{
      font-size: 30px;
      line-height: 1.35;
      color: #e2e8f0;
      font-weight: 600;
    }}
    .alert-row {{
      display: flex;
      align-items: center;
      gap: 22px;
      background: rgba(251, 113, 133, 0.12);
      border: 2px solid #fb7185;
      border-radius: 24px;
      padding: 20px 24px;
      margin-bottom: 24px;
    }}
    .thumb-180 {{
      width: 200px;
      height: 200px;
      object-fit: contain;
      flex-shrink: 0;
    }}
    .alert-copy {{
      font-size: 29px;
      line-height: 1.32;
      color: #ffe4e6;
      font-weight: 700;
    }}
    .locks-wrap {{
      display: flex;
      align-items: center;
      gap: 22px;
    }}
    .locks-list {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .lock-row {{
      background: #0d0e12;
      border: 2px solid #34d399;
      border-radius: 20px;
      padding: 18px 22px;
      font-size: 29px;
      font-weight: 800;
      color: #ecfdf5;
    }}
    .cta-panel {{
      margin-top: 26px;
      background: #fbbf24;
      color: #0d0e12;
      border-radius: 28px;
      padding: 34px 36px;
      border: 4px solid #ffffff;
    }}
    .cta-title {{
      font-size: 46px;
      font-weight: 900;
      line-height: 1.1;
      margin-bottom: 10px;
    }}
    .cta-sub {{
      font-size: 31px;
      font-weight: 800;
      color: #111827;
      line-height: 1.3;
    }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="hrm01_abliterated" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920" data-fps="30">
    <audio id="master-audio" class="clip" src="assets/hrm01_master.wav" data-start="0" data-duration="{dur}" data-volume="1" data-track-index="10"></audio>

    <div class="bg-stage" data-layout-ignore>
      <div id="bg-grid" class="grid-bg"></div>
      <div id="orb-cyan" class="orb-cyan"></div>
      <div id="orb-amber" class="orb-amber"></div>
    </div>

    <div class="safe-stage">
      <div id="top-bar" class="clip top-bar-clip" data-start="0" data-duration="{dur}">
        <div id="top-bar-inner" class="top-bar">
          <span class="series-badge">¡WATERS! · BLACK CANVAS</span>
          <div class="prog-track"><div id="prog-fill" class="prog-fill"></div></div>
        </div>
      </div>

      <!-- S1: HOOK -->
      <div id="sc-1" class="clip scene-slot" data-start="{s1_start}" data-duration="{d1}">
        <div id="sc-1-inner" class="board-card">
          <span class="pill pill-amber">MODELO ABLITERATED · HRM-01</span>
          <h1 class="h1">¿Qué es un modelo ABLITERATED?</h1>
          <p class="lead">Así borran el botón de rechazo (y el peligro real).</p>
          <div class="sticker-stage">
            <img id="s1-sticker" class="sticker-main" src="assets/stk_01_abliteration_vector.png" alt="Vector de abliteración" />
          </div>
        </div>
      </div>

      <!-- S2: VECTOR DE RECHAZO -->
      <div id="sc-2" class="clip scene-slot" data-start="{s2_start}" data-duration="{d2}">
        <div id="sc-2-inner" class="board-card">
          <span class="pill pill-cyan">CÓMO FUNCIONA POR DENTRO</span>
          <h1 class="h1">Anulan el vector de rechazo</h1>
          <p class="lead">Ubican la flecha matemática de negativa en los pesos abiertos y la borran sin reentrenar.</p>
          <div id="s2-diag" class="diagram-panel">
            <svg viewBox="0 0 780 340" width="780" height="340">
              <rect x="10" y="14" width="365" height="312" rx="20" fill="#13151d" stroke="#fb7185" stroke-width="3"/>
              <text x="34" y="62" fill="#fb7185" font-size="30" font-weight="800">ESTÁNDAR (FRENO)</text>
              <line x1="36" y1="168" x2="236" y2="168" stroke="#38bdf8" stroke-width="8" stroke-linecap="round"/>
              <line id="vec-refusal" x1="236" y1="168" x2="328" y2="96" stroke="#fb7185" stroke-width="8" stroke-linecap="round"/>
              <text x="34" y="246" fill="#e2e8f0" font-size="30" font-weight="700">"Lo siento, no puedo"</text>
              <text x="34" y="290" fill="#fb7185" font-size="30" font-weight="700">Dispara rechazo</text>

              <rect x="405" y="14" width="365" height="312" rx="20" fill="#13151d" stroke="#34d399" stroke-width="3"/>
              <text x="429" y="62" fill="#34d399" font-size="30" font-weight="800">ABLITERATED</text>
              <line id="vec-ablit" x1="431" y1="168" x2="736" y2="168" stroke="#34d399" stroke-width="8" stroke-linecap="round"/>
              <text x="429" y="246" fill="#e2e8f0" font-size="30" font-weight="700">Sin flecha de freno</text>
              <text x="429" y="290" fill="#34d399" font-size="30" font-weight="700">Sin reentrenamiento</text>
            </svg>
          </div>
        </div>
      </div>

      <!-- S3: REALIDAD SIN HUMO -->
      <div id="sc-3" class="clip scene-slot" data-start="{s3_start}" data-duration="{d3}">
        <div id="sc-3-inner" class="board-card">
          <span class="pill pill-rose">LA REALIDAD SIN HUMO</span>
          <h1 class="h1">No es más inteligente</h1>
          <p class="lead">Conserva su conocimiento, pero pierde el freno de emergencia.</p>
          <div class="stack-col">
            <div id="s3-box1" class="node-box node-red">
              <div class="node-label c-red">PIERDE EL FRENO</div>
              <div class="node-text">Baja la barrera frente a código dañino o inyecciones de texto si lo sueltas sin control.</div>
            </div>
            <div id="s3-box2" class="node-box node-green">
              <div class="node-label c-green">USO CONTROLADO</div>
              <div class="node-text">Útil para investigar filtros y evaluar respuestas en laboratorios aislados.</div>
            </div>
          </div>
        </div>
      </div>

      <!-- S4: 3 CANDADOS CAPTOORA -->
      <div id="sc-4" class="clip scene-slot" data-start="{s4_start}" data-duration="{d4}">
        <div id="sc-4-inner" class="board-card">
          <span class="pill pill-emerald">REGLA CAPTOORA · DEFENSA</span>
          <h1 class="h1">Sin aislamiento, 1 correo te tumba</h1>
          <div id="s4-alert" class="alert-row">
            <img class="thumb-180" src="assets/stk_06_alerta_prompt_injection.png" alt="Alerta Prompt Injection" />
            <div class="alert-copy">Prompt Injection + Terminal abierta = órdenes que ya nadie detiene.</div>
          </div>
          <div class="locks-wrap">
            <div class="locks-list">
              <div id="s4-lock1" class="lock-row">1. Docker Sandbox</div>
              <div id="s4-lock2" class="lock-row">2. Firewall UFW cerrado</div>
              <div id="s4-lock3" class="lock-row">3. Aprobación humana obligatoria</div>
            </div>
            <img class="thumb-180" src="assets/stk_04_docker_sandbox_escudo.png" alt="Escudo Docker Sandbox" />
          </div>
        </div>
      </div>

      <!-- S5: CTA HERMES -->
      <div id="sc-5" class="clip scene-slot" data-start="{s5_start}" data-duration="{d5}">
        <div id="sc-5-inner" class="board-card">
          <span class="pill pill-amber">CHECKLIST DEFENSIVO</span>
          <h1 class="h1">Aísla antes de probar</h1>
          <p class="lead">Primero blinda tu entorno.</p>
          <div id="s5-cta" class="cta-panel">
            <div class="cta-title">COMENTA: HERMES</div>
            <div class="cta-sub">Guía de 3 candados.</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});

      tl.fromTo("#prog-fill", {{ scaleX: 0.03 }}, {{ scaleX: 1.0, duration: {dur}, ease: "none" }}, 0);
      tl.fromTo("#bg-grid", {{ backgroundPosition: "0px 0px" }}, {{ backgroundPosition: "54px 54px", duration: {dur}, ease: "none" }}, 0);
      tl.fromTo("#orb-cyan", {{ x: 0, y: 0 }}, {{ x: 140, y: 90, duration: {dur}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#orb-amber", {{ x: 0, y: 0 }}, {{ x: -120, y: -90, duration: {dur}, ease: "sine.inOut" }}, 0);

      // S1 Hook
      tl.fromTo("#sc-1-inner", {{ y: 12, scale: 0.98, opacity: 1 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.35, ease: "power3.out" }}, 0);
      tl.fromTo("#s1-sticker", {{ scale: 0.94 }}, {{ scale: 1, duration: 0.45, ease: "back.out(1.4)" }}, 0.15);
      tl.to("#sc-1-inner", {{ x: -80, opacity: 0, duration: 0.22, ease: "power2.in" }}, {s1_exit});

      // S2 Diagrama Vector
      tl.fromTo("#sc-2-inner", {{ x: 80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {s2_start});
      tl.fromTo("#s2-diag", {{ y: 16, opacity: 0.3 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power2.out" }}, {s2_diag_in});
      tl.fromTo("#vec-refusal", {{ opacity: 0.15 }}, {{ opacity: 1, duration: 0.55, ease: "power2.out" }}, {s2_vec_bad});
      tl.fromTo("#vec-ablit", {{ opacity: 0.15 }}, {{ opacity: 1, duration: 0.55, ease: "power2.out" }}, {s2_vec_good});
      tl.to("#sc-2-inner", {{ x: -80, opacity: 0, duration: 0.22, ease: "power2.in" }}, {s2_exit});

      // S3 Realidad
      tl.fromTo("#sc-3-inner", {{ x: 80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {s3_start});
      tl.fromTo("#s3-box1", {{ y: 20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.38, ease: "power3.out" }}, {s3_box1_in});
      tl.fromTo("#s3-box2", {{ y: 20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.38, ease: "power3.out" }}, {s3_box2_in});
      tl.to("#sc-3-inner", {{ x: -80, opacity: 0, duration: 0.22, ease: "power2.in" }}, {s3_exit});

      // S4 Candados
      tl.fromTo("#sc-4-inner", {{ x: 80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {s4_start});
      tl.fromTo("#s4-alert", {{ scale: 0.96, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "power2.out" }}, {s4_alert_in});
      tl.fromTo("#s4-lock1", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.32, ease: "power3.out" }}, {s4_lock1_in});
      tl.fromTo("#s4-lock2", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.32, ease: "power3.out" }}, {s4_lock2_in});
      tl.fromTo("#s4-lock3", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.32, ease: "power3.out" }}, {s4_lock3_in});
      tl.to("#sc-4-inner", {{ x: -80, opacity: 0, duration: 0.22, ease: "power2.in" }}, {s4_exit});

      // S5 CTA
      tl.fromTo("#sc-5-inner", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.32, ease: "power3.out" }}, {s5_start});
      tl.fromTo("#s5-cta", {{ scale: 0.9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }}, {s5_cta_in});

      window.__timelines = window.__timelines || {{}};
      window.__timelines["hrm01_abliterated"] = tl;
    }})();
  </script>
</body>
</html>
"""


def main() -> int:
    data = json.loads(TIMINGS.read_text(encoding="utf-8"))
    meta = data["hrm01"]

    assets_dir = OUT_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / ".gitignore").write_text(".hyperframes/\nrenders/\nassets/*.wav\n", encoding="utf-8")

    shutil.copy2(BASE / "audio/hrm01_master.wav", assets_dir / "hrm01_master.wav")
    for name in REQUIRED_STICKERS:
        shutil.copy2(STICKERS_DIR / name, assets_dir / name)

    html = build_hrm01_html(meta)
    out_html = OUT_DIR / "index.html"
    out_html.write_text(html, encoding="utf-8")
    print(f"BUILT {out_html} (dur={meta['total_duration']}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
