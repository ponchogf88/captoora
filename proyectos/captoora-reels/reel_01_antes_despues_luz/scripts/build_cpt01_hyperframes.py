#!/usr/bin/env python3
"""
Construye el proyecto HyperFrames 9:16 (1080x1920, 30 fps) para Captoora Studio CPT-REEL-01:
Aplica las 4 palancas de REF-15 (Zoom 0s + SFX 0s + Titular fijo + Cortina Antes->Después)
cumpliendo 100% docs/LEY_VISUAL_CAPTOORA.md (fotografía protagonista Zero-Crop y cero texto encima).
"""
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
BASE = ROOT / "proyectos/captoora-reels/reel_01_antes_despues_luz"
TIMINGS = BASE / "audio/cpt01_timings.json"
OUT_DIR = BASE / "hf_reel_25s"
FFMPEG = "/Users/imac/.local/bin/ffmpeg"


def build_cpt01_html(meta: Dict[str, Any]) -> str:
    dur = round(float(meta["total_duration"]), 2)
    clips: List[Dict[str, Any]] = meta["clips"]
    by_id = {c["id"]: c for c in clips}

    c1 = by_id["C1_hook"]
    c2 = by_id["C2_revelado"]
    c3 = by_id["C3_estudio"]
    c4 = by_id["C4_cta"]

    sa_start, sa_end = 0.0, round(float(c3["start"]), 2)
    sb_start, sb_end = sa_end, round(float(c4["start"]), 2)
    sc_start, sc_end = sb_end, dur

    da = round(sa_end - sa_start, 2)
    db = round(sb_end - sb_start, 2)
    dc = round(sc_end - sc_start, 2)

    hook_dur = round(max(1.0, sb_end - 0.12), 2)
    hook_exit = round(max(0.5, sb_end - 0.34), 2)

    wipe_start = 0.65
    wipe_dur = round(max(2.0, sa_end - 0.55 - wipe_start), 2)
    sa_exit = round(max(1.0, sa_end - 0.22), 2)

    sb_exit = round(max(sb_start + 0.5, sb_end - 0.22), 2)
    sb_zoom_dur = round(max(1.0, db - 0.25), 2)

    sc_pop_in = round(sc_start + 0.3, 2)
    sc_pulse_dur = round(max(0.6, dc - 0.35), 2)

    _ = c1, c2

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Captoora Studio · Antes / Después de Luz (CPT-REEL-01)</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #0b0c10;
      color: #ffffff;
      font-family: "Outfit", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    #root {{
      position: relative;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #0b0c10;
    }}
    .bg-stage {{
      position: absolute;
      inset: 0;
      z-index: 1;
      overflow: hidden;
    }}
    .studio-grid {{
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(to right, rgba(200, 245, 59, 0.04) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(200, 245, 59, 0.04) 1px, transparent 1px);
      background-size: 56px 56px;
    }}
    .lime-halo {{
      position: absolute;
      width: 780px;
      height: 780px;
      left: 110px;
      top: 160px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(200, 245, 59, 0.14) 0%, rgba(200, 245, 59, 0) 68%);
    }}
    /* Banda segura estricta: y=152..1352px, x=56..944px (rail derecho + 568px abajo libres para subtítulos) */
    .safe-stage {{
      position: absolute;
      top: 152px;
      left: 56px;
      width: 888px;
      height: 1200px;
      z-index: 10;
    }}
    /* Gancho textual fijo arriba (REF-15): nunca toca ni cubre al sujeto fotografiado */
    .top-hook-clip {{
      position: absolute;
      top: 0;
      left: 0;
      width: 888px;
      height: 184px;
    }}
    .top-hook-card {{
      width: 100%;
      background: #13161f;
      border: 2px solid #2b3142;
      border-radius: 26px;
      padding: 20px 28px;
      text-align: center;
    }}
    .hook-kicker {{
      font-size: 40px;
      font-weight: 900;
      line-height: 1.08;
      color: #ffffff;
      letter-spacing: -0.015em;
    }}
    .hook-accent {{
      font-size: 46px;
      font-weight: 900;
      line-height: 1.08;
      color: #c8f53b;
      letter-spacing: -0.015em;
      margin-top: 4px;
    }}
    .stage-body {{
      position: absolute;
      top: 206px;
      left: 0;
      width: 888px;
      height: 980px;
    }}
    .cta-body {{
      position: absolute;
      top: 40px;
      left: 0;
      width: 888px;
      height: 1140px;
    }}
    /* Contenedor fotográfico Zero-Crop: object-fit contain preserva 100% cabeza, casco y calzado */
    .photo-showcase {{
      width: 100%;
      background: #060709;
      border: 3px solid #2a3040;
      border-radius: 28px;
      padding: 16px;
    }}
    .photo-frame {{
      position: relative;
      width: 100%;
      height: 600px;
      border-radius: 18px;
      overflow: hidden;
      background: #050507;
    }}
    .photo-full {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
    }}
    .before-layer {{
      position: absolute;
      inset: 0;
      clip-path: inset(0 0 0 10%);
    }}
    .before-grade {{
      filter: brightness(0.62) contrast(0.74) saturate(0.45);
    }}
    .wipe-divider {{
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0;
      width: 6px;
      background: #c8f53b;
    }}
    .wipe-legend {{
      margin-top: 18px;
      background: #13161f;
      border: 2px solid #2b3142;
      border-radius: 22px;
      padding: 20px 26px;
    }}
    .legend-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }}
    .pill-muted {{
      padding: 6px 16px;
      border-radius: 999px;
      background: #232736;
      color: #e2e8f0;
      font-size: 28px;
      font-weight: 800;
    }}
    .pill-lime {{
      padding: 6px 18px;
      border-radius: 999px;
      background: #c8f53b;
      color: #0b0c10;
      font-size: 28px;
      font-weight: 900;
    }}
    .wipe-rail {{
      width: 100%;
      height: 12px;
      border-radius: 999px;
      background: #232736;
      overflow: hidden;
    }}
    .wipe-fill {{
      width: 100%;
      height: 100%;
      background: #c8f53b;
      transform-origin: left center;
    }}
    .studio-frame {{
      position: relative;
      width: 100%;
      height: 540px;
      border-radius: 18px;
      overflow: hidden;
      background: #050507;
    }}
    .chips-3 {{
      margin-top: 18px;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
    }}
    .chip-box {{
      background: #13161f;
      border: 2px solid #2b3142;
      border-radius: 20px;
      padding: 18px 12px;
      text-align: center;
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
    }}
    .chip-accent {{
      color: #c8f53b;
      display: block;
      margin-bottom: 4px;
      font-size: 28px;
      font-weight: 900;
    }}
    /* Cierre: foto protagonista intacta arriba + popup oficial @captoora.studio (REF-15) */
    .cta-photo-card {{
      width: 100%;
      background: #060709;
      border: 3px solid #2a3040;
      border-radius: 28px;
      padding: 16px;
      margin-bottom: 24px;
    }}
    .cta-photo-frame {{
      position: relative;
      width: 100%;
      height: 500px;
      border-radius: 18px;
      overflow: hidden;
      background: #050507;
    }}
    .follow-popup {{
      width: 100%;
      background: #13161f;
      border: 3px solid #c8f53b;
      border-radius: 30px;
      padding: 28px 32px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .profile-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }}
    .profile-left {{
      display: flex;
      align-items: center;
      gap: 18px;
    }}
    .logo-badge {{
      width: 92px;
      height: 92px;
      border-radius: 50%;
      background: #0b0c10;
      border: 2px solid #c8f53b;
      padding: 10px;
      object-fit: contain;
    }}
    .handle-txt {{
      font-size: 36px;
      font-weight: 900;
      color: #ffffff;
    }}
    .loc-txt {{
      font-size: 28px;
      font-weight: 600;
      color: #cbd5e1;
      margin-top: 2px;
    }}
    .btn-seguir {{
      padding: 14px 28px;
      border-radius: 999px;
      background: #c8f53b;
      color: #0b0c10;
      font-size: 30px;
      font-weight: 900;
      white-space: nowrap;
    }}
    .cta-strip {{
      background: #c8f53b;
      color: #0b0c10;
      border-radius: 20px;
      padding: 18px 26px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 32px;
      font-weight: 900;
    }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="cpt01_antes_despues" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920" data-fps="30">
    <audio id="master-audio" class="clip" src="assets/cpt01_master.wav" data-start="0" data-duration="{dur}" data-volume="1" data-track-index="10"></audio>

    <div class="bg-stage" data-layout-ignore>
      <div id="studio-grid" class="studio-grid"></div>
      <div id="lime-halo" class="lime-halo"></div>
    </div>

    <div class="safe-stage">
      <!-- GANCHO TEXTUAL PERSISTENTE ARRIBA (REF-15) -->
      <div id="top-hook" class="clip top-hook-clip" data-start="0" data-duration="{hook_dur}">
        <div id="top-hook-card" class="top-hook-card">
          <div class="hook-kicker">¿TU FOTO SE VE PLANA?</div>
          <div class="hook-accent">LA LUZ LO CAMBIA TODO</div>
        </div>
      </div>

      <!-- ESCENA A: ZOOM 0s + CORTINA CONTINUA ANTES -> DESPUÉS -->
      <div id="sc-a" class="clip stage-body" data-start="{sa_start}" data-duration="{da}">
        <div id="sc-a-inner">
          <div id="sa-showcase" class="photo-showcase">
            <div class="photo-frame">
              <img class="photo-full" src="assets/hero-portrait-after.jpg" alt="Retrato oficial Captoora con luz dirigida" />
              <div id="before-overlay" class="before-layer">
                <img class="photo-full" src="assets/hero-portrait-before.jpg" alt="Simulación luz plana antes" />
              </div>
              <div id="wipe-divider" class="wipe-divider"></div>
            </div>
          </div>
          <div class="wipe-legend">
            <div class="legend-row">
              <span class="pill-muted">ANTES · LUZ PLANA</span>
              <span class="pill-lime">DESPUÉS · LUZ CAPTOORA</span>
            </div>
            <div class="wipe-rail"><div id="wipe-prog" class="wipe-fill"></div></div>
          </div>
        </div>
      </div>

      <!-- ESCENA B: ESTUDIO REAL COLINAS DE SAN JERÓNIMO -->
      <div id="sc-b" class="clip stage-body" data-start="{sb_start}" data-duration="{db}">
        <div id="sc-b-inner">
          <div class="photo-showcase">
            <div class="studio-frame">
              <img id="sb-photo" class="photo-full" src="assets/escenario-1.jpg" alt="Escenario 1 Captoora Studio" />
            </div>
          </div>
          <div class="chips-3">
            <div class="chip-box"><span class="chip-accent">SET PRO</span>Softbox + Luz</div>
            <div class="chip-box"><span class="chip-accent">MONTERREY</span>Colinas</div>
            <div class="chip-box"><span class="chip-accent">GUÍA REAL</span>Pose y cámara</div>
          </div>
        </div>
      </div>

      <!-- ESCENA C: POPUP @captoora.studio + COMENTA SESIÓN -->
      <div id="sc-c" class="clip cta-body" data-start="{sc_start}" data-duration="{dc}">
        <div id="sc-c-inner">
          <div class="cta-photo-card">
            <div class="cta-photo-frame">
              <img id="sc-photo" class="photo-full" src="assets/hero-portrait-cta.jpg" alt="Retrato oficial Captoora Studio" />
            </div>
          </div>
          <div id="follow-popup" class="follow-popup">
            <div class="profile-row">
              <div class="profile-left">
                <img class="logo-badge" src="assets/captoora_logo_lente_centrado_blanco.png" alt="Logo Captoora" />
                <div>
                  <div class="handle-txt">@captoora.studio</div>
                  <div class="loc-txt">Colinas, MTY</div>
                </div>
              </div>
              <div class="btn-seguir">Seguir</div>
            </div>
            <div class="cta-strip">
              <span>COMENTA: SESIÓN</span>
              <span>WA 81 4005 0088</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});

      tl.fromTo("#studio-grid", {{ backgroundPosition: "0px 0px" }}, {{ backgroundPosition: "56px 56px", duration: {dur}, ease: "none" }}, 0);
      tl.fromTo("#lime-halo", {{ x: -40, y: 0 }}, {{ x: 90, y: 80, duration: {dur}, ease: "sine.inOut" }}, 0);

      // Titular fijo sale al entrar el popup de cierre
      tl.fromTo("#top-hook-card", {{ y: -12, opacity: 1 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 0);
      tl.to("#top-hook-card", {{ y: -24, opacity: 0, duration: 0.22, ease: "power2.in" }}, {hook_exit});

      // Escena A: Punch-in zoom en t=0 (REF-15) + cortina continua Antes -> Después
      tl.fromTo("#sa-showcase", {{ scale: 0.90 }}, {{ scale: 1.0, duration: 0.50, ease: "power3.out" }}, 0);
      tl.fromTo("#before-overlay", {{ clipPath: "inset(0 0 0 10%)" }}, {{ clipPath: "inset(0 0 0 98%)", duration: {wipe_dur}, ease: "power1.inOut" }}, {wipe_start});
      tl.fromTo("#wipe-divider", {{ x: 85 }}, {{ x: 838, duration: {wipe_dur}, ease: "power1.inOut" }}, {wipe_start});
      tl.fromTo("#wipe-prog", {{ scaleX: 0.10 }}, {{ scaleX: 0.98, duration: {wipe_dur}, ease: "power1.inOut" }}, {wipe_start});
      tl.to("#sc-a-inner", {{ x: -60, opacity: 0, duration: 0.22, ease: "power2.in" }}, {sa_exit});

      // Escena B: Estudio real con zoom continuo suave
      tl.fromTo("#sc-b-inner", {{ x: 60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.28, ease: "power3.out" }}, {sb_start});
      tl.fromTo("#sb-photo", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {sb_zoom_dur}, ease: "sine.inOut" }}, {sb_start});
      tl.to("#sc-b-inner", {{ x: -60, opacity: 0, duration: 0.22, ease: "power2.in" }}, {sb_exit});

      // Escena C: Popup @captoora.studio + pulso suave en retrato
      tl.fromTo("#sc-c-inner", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {sc_start});
      tl.fromTo("#follow-popup", {{ scale: 0.92 }}, {{ scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, {sc_pop_in});
      tl.fromTo("#sc-photo", {{ scale: 1.0 }}, {{ scale: 1.04, duration: {sc_pulse_dur}, ease: "sine.inOut" }}, {sc_start});

      window.__timelines = window.__timelines || {{}};
      window.__timelines["cpt01_antes_despues"] = tl;
    }})();
  </script>
</body>
</html>
"""


def main() -> int:
    data = json.loads(TIMINGS.read_text(encoding="utf-8"))
    meta = data["cpt01"]

    assets_dir = OUT_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / ".gitignore").write_text(".hyperframes/\nrenders/\nassets/*.wav\n", encoding="utf-8")

    shutil.copy2(BASE / "audio/cpt01_master.wav", assets_dir / "cpt01_master.wav")
    src_hero = ROOT / "assets/hero-portrait.png"
    after_jpg = assets_dir / "hero-portrait-after.jpg"
    before_jpg = assets_dir / "hero-portrait-before.jpg"
    cta_jpg = assets_dir / "hero-portrait-cta.jpg"
    subprocess.run([FFMPEG, "-y", "-i", str(src_hero), "-vf", "scale='min(1400,iw):-1'", "-q:v", "2", str(after_jpg)], check=True, capture_output=True)
    subprocess.run([FFMPEG, "-y", "-i", str(src_hero), "-vf", "scale='min(1400,iw):-1',eq=brightness=-0.20:contrast=0.65:saturation=0.25", "-q:v", "2", str(before_jpg)], check=True, capture_output=True)
    shutil.copy2(after_jpg, cta_jpg)
    shutil.copy2(ROOT / "assets/media_jpg/escenario-1.jpg", assets_dir / "escenario-1.jpg")
    shutil.copy2(ROOT / "assets/captoora_logo_lente_centrado_blanco.png", assets_dir / "captoora_logo_lente_centrado_blanco.png")

    html = build_cpt01_html(meta)
    out_html = OUT_DIR / "index.html"
    out_html.write_text(html, encoding="utf-8")
    print(f"BUILT {out_html} (dur={meta['total_duration']}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
