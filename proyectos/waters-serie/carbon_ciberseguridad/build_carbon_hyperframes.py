#!/usr/bin/env python3
"""
Construye ambos proyectos HyperFrames independientes a partir de audio/carbon_timings.json:
  1) hf_short_60s/       (1080x1920, 30 fps) -> Short vertical ¿Oro Puro o Puro Humo?
  2) hf_explainer_3min/  (1920x1080, 30 fps) -> Deep Dive explicativo horizontal
"""
import json
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
BASE = ROOT / "proyectos/waters-serie/carbon_ciberseguridad"
TIMINGS = BASE / "audio/carbon_timings.json"


def build_short_html(meta: Dict[str, Any]) -> str:
    dur = float(meta["total_duration"])
    c = {x["id"]: x for x in meta["clips"]}
    s1, s2, s3, s4, s5 = c["S1_hook"], c["S2_secbench"], c["S3_exploitgym"], c["S4_cwebench"], c["S5_letrachiquita"]
    s6 = c["S6_cta"]

    def w_end(item: Dict[str, Any], next_item: Optional[Dict[str, Any]]) -> float:
        return round(next_item["start"], 2) if next_item else dur

    scenes = [
        ("s1", s1["start"], w_end(s1, s2)),
        ("s2", s2["start"], w_end(s2, s3)),
        ("s3", s3["start"], w_end(s3, s4)),
        ("s4", s4["start"], w_end(s4, s5)),
        ("s5", s5["start"], w_end(s5, s6)),
        ("s6", s6["start"], dur),
    ]
    durs = {k: round(e - st, 2) for k, st, e in scenes}
    starts = {k: round(st, 2) for k, st, _ in scenes}

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Gemini 4 Carbon en Ciberseguridad · ¿Oro Puro o Puro Humo? (Short)</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #0e131b;
      font-family: "Outfit", "Nunito", sans-serif;
      color: #f8fafc;
    }}
    #root {{
      position: relative;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #0e131b;
    }}
    .bg-stage {{
      position: absolute;
      inset: 0;
      z-index: 1;
      overflow: hidden;
    }}
    .halo-orb-a {{
      position: absolute;
      width: 780px;
      height: 780px;
      left: -120px;
      top: 140px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(56,189,248,0.28) 0%, rgba(56,189,248,0) 70%);
    }}
    .halo-orb-b {{
      position: absolute;
      width: 820px;
      height: 820px;
      right: -180px;
      top: 520px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(168,85,247,0.26) 0%, rgba(168,85,247,0) 70%);
    }}
    .halo-orb-c {{
      position: absolute;
      width: 680px;
      height: 680px;
      left: 160px;
      top: 900px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(245,158,11,0.18) 0%, rgba(245,158,11,0) 70%);
    }}
    /* Banda segura vertical estricta: y=172..1310px, x=64..936px (rail derecho 944..1080 y abajo 1330..1920 libres) */
    .safe-stage {{
      position: absolute;
      top: 172px;
      left: 64px;
      width: 872px;
      height: 1138px;
      z-index: 10;
    }}
    .top-bar-clip {{
      position: absolute;
      top: 0;
      left: 0;
      width: 872px;
      height: 58px;
    }}
    .top-bar {{
      display: flex;
      align-items: center;
      gap: 16px;
      height: 58px;
      padding: 0 22px;
      border-radius: 999px;
      background: #161f2d;
      border: 2px solid #2c3b52;
    }}
    .top-tag {{
      font-family: "Space Mono", monospace;
      font-size: 28px;
      font-weight: 700;
      color: #f9d14b;
      white-space: nowrap;
    }}
    .prog-track {{
      flex: 1;
      height: 12px;
      border-radius: 999px;
      background: #233044;
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
      top: 86px;
      left: 0;
      width: 872px;
      height: 1020px;
    }}
    .card {{
      background: #151e2b;
      border: 3px solid #2e3f57;
      border-radius: 34px;
      padding: 36px 38px;
      box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
    }}
    .pill {{
      display: inline-block;
      padding: 10px 24px;
      border-radius: 999px;
      font-family: "Space Mono", monospace;
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 22px;
    }}
    .pill-amber {{ background: #f9d14b; color: #111827; }}
    .pill-cyan {{ background: #38bdf8; color: #081220; }}
    .pill-emerald {{ background: #34d399; color: #062116; }}
    .pill-rose {{ background: #fb7185; color: #2b0910; }}
    .h1 {{
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 56px;
      line-height: 1.06;
      color: #ffffff;
      letter-spacing: -0.02em;
      margin-bottom: 20px;
    }}
    .sub {{
      font-family: "Nunito", "Outfit", sans-serif;
      font-size: 36px;
      font-weight: 700;
      line-height: 1.26;
      color: #cbd5e1;
    }}
    .source-chip {{
      margin-top: 26px;
      padding: 18px 24px;
      border-radius: 22px;
      background: #101722;
      border: 2px solid #28364a;
      font-family: "Space Mono", monospace;
      font-size: 28px;
      color: #93c5fd;
    }}
    /* Gráficas de barras animadas */
    .bars-stack {{
      margin-top: 26px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .bar-row {{
      background: #101722;
      border: 2px solid #273549;
      border-radius: 22px;
      padding: 20px 24px;
    }}
    .bar-head {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 12px;
    }}
    .bar-name {{
      font-size: 32px;
      font-weight: 800;
      color: #f1f5f9;
    }}
    .bar-val {{
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 40px;
      color: #38bdf8;
    }}
    .bar-val-gold {{ color: #f9d14b; }}
    .bar-val-muted {{ color: #94a3b8; }}
    .bar-rail {{
      width: 100%;
      height: 24px;
      border-radius: 999px;
      background: #1e293b;
      overflow: hidden;
    }}
    .bar-fill {{
      height: 100%;
      border-radius: 999px;
      transform-origin: left center;
    }}
    .fill-gold {{ background: #f9d14b; }}
    .fill-cyan {{ background: #38bdf8; }}
    .fill-slate {{ background: #64748b; }}
    .fine-list {{
      margin-top: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .fine-item {{
      padding: 22px 26px;
      border-radius: 24px;
      background: #101722;
      border-left: 8px solid #fb7185;
      font-size: 32px;
      font-weight: 700;
      line-height: 1.24;
      color: #f1f5f9;
    }}
    .verdict-box {{
      margin-top: 26px;
      padding: 28px 30px;
      border-radius: 26px;
      background: #f9d14b;
      color: #111827;
      border: 4px solid #ffffff;
    }}
    .verdict-title {{
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 44px;
      line-height: 1.08;
      margin-bottom: 10px;
    }}
    .verdict-sub {{
      font-size: 32px;
      font-weight: 800;
      color: #1e293b;
    }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="carbon_short_60s" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920" data-fps="30">
    <audio id="master-audio" class="clip" src="assets/carbon_short_60s_master.wav" data-start="0" data-duration="{dur}" data-volume="1" data-track-index="10"></audio>

    <div class="bg-stage" data-layout-ignore>
      <div id="orb-a" class="halo-orb-a"></div>
      <div id="orb-b" class="halo-orb-b"></div>
      <div id="orb-c" class="halo-orb-c"></div>
    </div>

    <div class="safe-stage">
      <div id="top-bar" class="clip top-bar-clip" data-start="0" data-duration="{dur}">
        <div id="top-bar-inner" class="top-bar">
          <span class="top-tag">AUDITORÍA IA</span>
          <div class="prog-track"><div id="prog-fill-bar" class="prog-fill"></div></div>
        </div>
      </div>

      <!-- S1: HOOK -->
      <div id="sc-1" class="clip scene-slot" data-start="{starts['s1']}" data-duration="{durs['s1']}">
        <div id="sc-1-inner" class="card">
          <div class="pill pill-amber">¿ORO PURO O PURO HUMO?</div>
          <h1 class="h1">¿Gemini 4 Carbon es el rey en ciberseguridad?</h1>
          <p class="sub">Google lo presume en Grande y lo abrió en Google Pro. Revisamos los datos reales.</p>
          <div class="source-chip">3 benchmarks públicos + letra chiquita</div>
        </div>
      </div>

      <!-- S2: SEC-BENCH PRO -->
      <div id="sc-2" class="clip scene-slot" data-start="{starts['s2']}" data-duration="{durs['s2']}">
        <div id="sc-2-inner" class="card">
          <div class="pill pill-cyan">PRUEBA 1 · DETECCIÓN</div>
          <h1 class="h1">SEC-bench Pro (Docker real)</h1>
          <p class="sub">Cacería de fallos y PoC en V8, SpiderMonkey y kernel Linux.</p>
          <div class="bars-stack">
            <div class="bar-row">
              <div class="bar-head"><span class="bar-name">Gemini 4 Carbon</span><span class="bar-val bar-val-gold">88.2%</span></div>
              <div class="bar-rail"><div id="s2-b1" class="bar-fill fill-gold" style="width:88.2%;"></div></div>
            </div>
            <div class="bar-row">
              <div class="bar-head"><span class="bar-name">GPT-6.2 Astra</span><span class="bar-val">~86.7%</span></div>
              <div class="bar-rail"><div id="s2-b2" class="bar-fill fill-cyan" style="width:86.7%;"></div></div>
            </div>
          </div>
          <div class="source-chip">Fuente: Model Card DeepMind / SEC-bench Pro</div>
        </div>
      </div>

      <!-- S3: EXPLOITGYM -->
      <div id="sc-3" class="clip scene-slot" data-start="{starts['s3']}" data-duration="{durs['s3']}">
        <div id="sc-3-inner" class="card">
          <div class="pill pill-cyan">PRUEBA 2 · EXPLOTACIÓN</div>
          <h1 class="h1">ExploitGym (898 fallos reales)</h1>
          <p class="sub">UC Berkeley + Max Planck + labs: encadenar un exploit funcional.</p>
          <div class="bars-stack">
            <div class="bar-row">
              <div class="bar-head"><span class="bar-name">Gemini 4 Carbon</span><span class="bar-val bar-val-gold">54.8%</span></div>
              <div class="bar-rail"><div id="s3-b1" class="bar-fill fill-gold" style="width:75%;"></div></div>
            </div>
            <div class="bar-row">
              <div class="bar-head"><span class="bar-name">GPT-6 Astra</span><span class="bar-val">42.4%</span></div>
              <div class="bar-rail"><div id="s3-b2" class="bar-fill fill-cyan" style="width:58%;"></div></div>
            </div>
            <div class="bar-row">
              <div class="bar-head"><span class="bar-name">Claude Opus 5.5</span><span class="bar-val bar-val-muted">34.5%</span></div>
              <div class="bar-rail"><div id="s3-b3" class="bar-fill fill-slate" style="width:47%;"></div></div>
            </div>
          </div>
        </div>
      </div>

      <!-- S4: CWE-BENCH -->
      <div id="sc-4" class="clip scene-slot" data-start="{starts['s4']}" data-duration="{durs['s4']}">
        <div id="sc-4-inner" class="card">
          <div class="pill pill-emerald">PRUEBA 3 · PARCHES</div>
          <h1 class="h1">CWE-bench (Collinear AI)</h1>
          <p class="sub">Auditar repo sin pista de ubicación y parchar sin romper la app.</p>
          <div class="bars-stack">
            <div class="bar-row">
              <div class="bar-head"><span class="bar-name">Gemini 4 Carbon</span><span class="bar-val bar-val-gold">71.0%</span></div>
              <div class="bar-rail"><div id="s4-b1" class="bar-fill fill-gold" style="width:71%;"></div></div>
            </div>
            <div class="bar-row">
              <div class="bar-head"><span class="bar-name">OpenAI (Astra)</span><span class="bar-val">~68.0%</span></div>
              <div class="bar-rail"><div id="s4-b2" class="bar-fill fill-cyan" style="width:68%;"></div></div>
            </div>
            <div class="bar-row">
              <div class="bar-head"><span class="bar-name">Anthropic (Opus)</span><span class="bar-val bar-val-muted">~67.0%</span></div>
              <div class="bar-rail"><div id="s4-b3" class="bar-fill fill-slate" style="width:67%;"></div></div>
            </div>
          </div>
        </div>
      </div>

      <!-- S5: LETRA CHIQUITA -->
      <div id="sc-5" class="clip scene-slot" data-start="{starts['s5']}" data-duration="{durs['s5']}">
        <div id="sc-5-inner" class="card">
          <div class="pill pill-rose">⚠️ LA LETRA CHIQUITA</div>
          <h1 class="h1">Lo que casi nadie cuenta</h1>
          <div class="fine-list">
            <div id="s5-i1" class="fine-item">1. Las 3 pruebas usan reglas distintas: NO se suman ni dan 100% seguro.</div>
            <div id="s5-i2" class="fine-item">2. Astra sacó 100% en ExploitBench y Claude Fable compite duro en código diario.</div>
            <div id="s5-i3" class="fine-item">3. Carbon razona más largo: quema mucho más cuota de thinking tokens.</div>
          </div>
        </div>
      </div>

      <!-- S6: VEREDICTO + CTA -->
      <div id="sc-6" class="clip scene-slot" data-start="{starts['s6']}" data-duration="{durs['s6']}">
        <div id="sc-6-inner" class="card">
          <div class="pill pill-amber">REGLA PRÁCTICA · GOOGLE PRO</div>
          <h1 class="h1">Úsalo como cirujano, no para todo</h1>
          <p class="sub">Audita repos o bugs críticos con Carbon; deja lo diario en modelos ligeros.</p>
          <div id="s6-verdict" class="verdict-box">
            <div class="verdict-title">COMENTA: CARBON</div>
            <div class="verdict-sub">Te paso los links a los 3 estudios reales.</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});

      // Fondo Halo continuo (evita tramos estáticos)
      tl.fromTo("#orb-a", {{ x: 0, y: 0 }}, {{ x: 160, y: 120, duration: {dur}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#orb-b", {{ x: 0, y: 0 }}, {{ x: -140, y: -110, duration: {dur}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#orb-c", {{ scale: 0.9 }}, {{ scale: 1.15, duration: {dur}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#prog-fill-bar", {{ scaleX: 0.03 }}, {{ scaleX: 1.0, duration: {dur}, ease: "none" }}, 0);

      // Frame 0 inmediato
      tl.fromTo("#sc-1-inner", {{ y: 12, scale: 0.97, opacity: 1 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.35, ease: "power4.out" }}, {starts['s1']});
      tl.to("#sc-1-inner", {{ x: -90, opacity: 0, duration: 0.22, ease: "power3.in" }}, {round(starts['s2'] - 0.22, 2)});

      // S2
      tl.fromTo("#sc-2-inner", {{ x: 90, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power4.out" }}, {starts['s2']});
      tl.fromTo("#s2-b1", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.75, ease: "power4.out" }}, {round(starts['s2'] + 0.35, 2)});
      tl.fromTo("#s2-b2", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.75, ease: "power4.out" }}, {round(starts['s2'] + 0.55, 2)});
      tl.to("#sc-2-inner", {{ x: -90, opacity: 0, duration: 0.22, ease: "power3.in" }}, {round(starts['s3'] - 0.22, 2)});

      // S3
      tl.fromTo("#sc-3-inner", {{ x: 90, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power4.out" }}, {starts['s3']});
      tl.fromTo("#s3-b1", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.7, ease: "power4.out" }}, {round(starts['s3'] + 0.4, 2)});
      tl.fromTo("#s3-b2", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.7, ease: "power4.out" }}, {round(starts['s3'] + 0.65, 2)});
      tl.fromTo("#s3-b3", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.7, ease: "power4.out" }}, {round(starts['s3'] + 0.9, 2)});
      tl.to("#sc-3-inner", {{ x: -90, opacity: 0, duration: 0.22, ease: "power3.in" }}, {round(starts['s4'] - 0.22, 2)});

      // S4
      tl.fromTo("#sc-4-inner", {{ x: 90, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power4.out" }}, {starts['s4']});
      tl.fromTo("#s4-b1", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.7, ease: "power4.out" }}, {round(starts['s4'] + 0.4, 2)});
      tl.fromTo("#s4-b2", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.7, ease: "power4.out" }}, {round(starts['s4'] + 0.65, 2)});
      tl.fromTo("#s4-b3", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.7, ease: "power4.out" }}, {round(starts['s4'] + 0.9, 2)});
      tl.to("#sc-4-inner", {{ x: -90, opacity: 0, duration: 0.22, ease: "power3.in" }}, {round(starts['s5'] - 0.22, 2)});

      // S5
      tl.fromTo("#sc-5-inner", {{ scale: 0.94, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(1.4)" }}, {starts['s5']});
      tl.fromTo("#s5-i1", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.32, ease: "power3.out" }}, {round(starts['s5'] + 0.3, 2)});
      tl.fromTo("#s5-i2", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.32, ease: "power3.out" }}, {round(starts['s5'] + 1.8, 2)});
      tl.fromTo("#s5-i3", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.32, ease: "power3.out" }}, {round(starts['s5'] + 3.4, 2)});
      tl.to("#sc-5-inner", {{ x: -90, opacity: 0, duration: 0.22, ease: "power3.in" }}, {round(starts['s6'] - 0.22, 2)});

      // S6
      tl.fromTo("#sc-6-inner", {{ y: 36, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power4.out" }}, {starts['s6']});
      tl.fromTo("#s6-verdict", {{ scale: 0.88, opacity: 0 }}, {{ scale: 1.0, opacity: 1, duration: 0.38, ease: "back.out(1.7)" }}, {round(starts['s6'] + 0.6, 2)});

      window.__timelines = window.__timelines || {{}};
      window.__timelines["carbon_short_60s"] = tl;
    }})();
  </script>
</body>
</html>
"""


def build_long_html(meta: Dict[str, Any]) -> str:
    dur = float(meta["total_duration"])
    clips = meta["clips"]

    chapters_ui = [
        ("01 Reclamo", clips[0]["start"], clips[1]["start"]),
        ("02 Origen", clips[1]["start"], clips[2]["start"]),
        ("03 SEC-bench", clips[2]["start"], clips[3]["start"]),
        ("04 ExploitGym", clips[3]["start"], clips[4]["start"]),
        ("05 CWE-bench", clips[4]["start"], clips[5]["start"]),
        ("06 Rivales", clips[5]["start"], clips[7]["start"]),
        ("07 Letra Chiquita", clips[7]["start"], clips[9]["start"]),
        ("08 Google Pro", clips[9]["start"], dur),
    ]

    # Precompute clip start/durations seamlessly back-to-back
    slots = []
    for i, item in enumerate(clips):
        st = round(item["start"], 2)
        en = round(clips[i + 1]["start"], 2) if i + 1 < len(clips) else dur
        slots.append((item["id"], st, round(en - st, 2)))
    smap = {k: (st, dd) for k, st, dd in slots}

    nav_pills_html = []
    nav_tweens = []
    for idx, (label, cs, ce) in enumerate(chapters_ui):
        pid = f"nav-{idx}"
        nav_pills_html.append(f'<div id="{pid}" class="nav-pill">{label}</div>')
        nav_tweens.append(f'      tl.to("#{pid}", {{ backgroundColor: "#F9D14B", color: "#111827", duration: 0.2 }}, {round(cs, 2)});')
        if idx < len(chapters_ui) - 1:
            nav_tweens.append(f'      tl.to("#{pid}", {{ backgroundColor: "#182232", color: "#94A3B8", duration: 0.2 }}, {round(ce, 2)});')

    def scene_wrap(cid: str, badge: str, pill_cls: str, left_h: str, left_p: str, footer: str, right_html: str) -> str:
        st, dd = smap[cid]
        return f"""
      <div id="{cid}" class="clip scene-grid-clip" data-start="{st}" data-duration="{dd}">
        <div id="{cid}-inner" class="scene-grid">
          <div class="col-left">
            <div class="pill {pill_cls}">{badge}</div>
            <h1 class="h1-wide">{left_h}</h1>
            <p class="p-wide">{left_p}</p>
            <div class="cite-box">{footer}</div>
          </div>
          <div class="col-right">{right_html}</div>
        </div>
      </div>"""

    # Right panels for the 11 chapters
    r_l01 = """
      <div class="panel">
        <div class="stat-label">DISPONIBLE EN GOOGLE AI PRO</div>
        <div class="big-stat" style="color:#F9D14B;">GEMINI 4 CARBON</div>
        <div class="sub-stat">Promocionado como modelo frontera en defensa y análisis de vulnerabilidades.</div>
        <div class="vs-row"><span class="vs-pill">Vs GPT-6.2 Astra</span><span class="vs-pill">Vs Opus 5.5 / Fable 5.2</span><span class="vs-pill">Vs Grok 4.6/4.7</span></div>
      </div>"""
    r_l02 = """
      <div class="panel">
        <div class="stat-label">CRONOLOGÍA VERIFICADA 2026</div>
        <div class="step-card"><b>28 OCT 2026:</b> Anuncio oficial DeepMind</div>
        <div class="step-card"><b>FAIRWIND PROGRAM:</b> Acceso inicial solo defensores</div>
        <div class="step-card"><b>PRE-RELEASE EE. UU.:</b> Pruebas gubernamentales</div>
        <div class="step-card" style="border-color:#F9D14B;"><b>10 NOV 2026 → PRO:</b> Apertura API + Google Pro</div>
      </div>"""
    r_l03 = """
      <div class="panel">
        <div class="stat-label">SEC-BENCH PRO · CAZA EN DOCKER</div>
        <div class="hbar-row"><div class="hbar-top"><span>Gemini 4 Carbon</span><span style="color:#F9D14B;">88.2%</span></div><div class="hbar-track"><div id="l03-b1" class="hbar-fill fill-gold" style="width:88.2%;"></div></div></div>
        <div class="hbar-row"><div class="hbar-top"><span>GPT-6.2 Astra</span><span style="color:#38BDF8;">~86.75%</span></div><div class="hbar-track"><div id="l03-b2" class="hbar-fill fill-cyan" style="width:86.7%;"></div></div></div>
        <div class="note-line">Mide generación de PoC reales en V8, SpiderMonkey y Linux kernel.</div>
      </div>"""
    r_l04 = """
      <div class="panel">
        <div class="stat-label">EXPLOITGYM · 898 FALLOS REALES</div>
        <div class="hbar-row"><div class="hbar-top"><span>Gemini 4 Carbon</span><span style="color:#F9D14B;">54.8%</span></div><div class="hbar-track"><div id="l04-b1" class="hbar-fill fill-gold" style="width:74%;"></div></div></div>
        <div class="hbar-row"><div class="hbar-top"><span>GPT-6 Astra</span><span style="color:#38BDF8;">42.4%</span></div><div class="hbar-track"><div id="l04-b2" class="hbar-fill fill-cyan" style="width:57%;"></div></div></div>
        <div class="hbar-row"><div class="hbar-top"><span>Claude Opus 5.5</span><span style="color:#94A3B8;">34.5%</span></div><div class="hbar-track"><div id="l04-b3" class="hbar-fill fill-slate" style="width:46%;"></div></div></div>
        <div class="note-line">UC Berkeley · Max Planck · UCSB · ASU (mayo 2026).</div>
      </div>"""
    r_l05 = """
      <div class="panel">
        <div class="stat-label">CWE-BENCH · AUDITORÍA Y PARCHE</div>
        <div class="hbar-row"><div class="hbar-top"><span>Gemini 4 Carbon</span><span style="color:#34D399;">71.0%</span></div><div class="hbar-track"><div id="l05-b1" class="hbar-fill fill-emerald" style="width:71%;"></div></div></div>
        <div class="hbar-row"><div class="hbar-top"><span>OpenAI (Astra)</span><span style="color:#38BDF8;">~68.0%</span></div><div class="hbar-track"><div id="l05-b2" class="hbar-fill fill-cyan" style="width:68%;"></div></div></div>
        <div class="hbar-row"><div class="hbar-top"><span>Anthropic (Opus)</span><span style="color:#94A3B8;">~67.0%</span></div><div class="hbar-track"><div id="l05-b3" class="hbar-fill fill-slate" style="width:67%;"></div></div></div>
        <div class="note-line">Sin pista de ubicación · Tercero independiente: Collinear AI.</div>
      </div>"""
    r_l06 = """
      <div class="panel">
        <div class="stat-label">CARA A CARA CON RIVALES DIRECTOS</div>
        <div class="step-card"><b>GPT-6 / 6.2 Astra:</b> 100% en ExploitBench · Nivel "Crítico" OpenAI</div>
        <div class="step-card"><b>Claude Fable 5.2 / Opus 5.5:</b> Fuertes en agentes de código diario</div>
        <div class="step-card"><b>Política Anthropic:</b> Candados estrictos abiertos · Mythos cerrado</div>
      </div>"""
    r_l07 = """
      <div class="panel">
        <div class="stat-label">GROK + ARTIFICIAL ANALYSIS v5.0</div>
        <div class="hbar-row"><div class="hbar-top"><span>Gemini 4 Carbon (AA v5.0)</span><span style="color:#F9D14B;">59 pts (#1)</span></div><div class="hbar-track"><div id="l07-b1" class="hbar-fill fill-gold" style="width:88%;"></div></div></div>
        <div class="hbar-row"><div class="hbar-top"><span>Claude Opus 5.5</span><span style="color:#38BDF8;">58 pts</span></div><div class="hbar-track"><div id="l07-b2" class="hbar-fill fill-cyan" style="width:85%;"></div></div></div>
        <div class="hbar-row"><div class="hbar-top"><span>GPT-6.2 Astra</span><span style="color:#34D399;">57 pts</span></div><div class="hbar-track"><div id="l07-b3" class="hbar-fill fill-emerald" style="width:83%;"></div></div></div>
        <div class="note-line">Grok 4.6/4.7 evaluado en CyberGym/Cursor, sin liderar la triple tabla.</div>
      </div>"""
    r_l08 = """
      <div class="panel">
        <div class="stat-label" style="color:#FB7185;">⚠️ AUDITORÍA METODOLÓGICA (1/2)</div>
        <div class="step-card" style="border-color:#FB7185;"><b>1. NO SE SUMAN:</b> SEC-bench, ExploitGym y CWE-bench miden cosas distintas.</div>
        <div class="step-card" style="border-color:#FB7185;"><b>2. PASS@1 ≠ ESTABILIDAD:</b> Cambia mucho al medir pass@4 y reintentos.</div>
        <div class="step-card" style="border-color:#F9D14B;"><b>3. COSTO OCULTO:</b> Carbon usa muchos más thinking tokens por respuesta.</div>
      </div>"""
    r_l09 = """
      <div class="panel">
        <div class="stat-label" style="color:#FB7185;">⚠️ AUDITORÍA METODOLÓGICA (2/2)</div>
        <div class="big-stat" style="color:#FB7185;">71% ≠ 100% SEGURO</div>
        <div class="step-card"><b>LABORATORIO DOCKER:</b> Basado en CVEs conocidos y contenedores aislados.</div>
        <div class="step-card"><b>EL 29% RESTANTE:</b> En producción, un solo hueco rompe el sistema.</div>
        <div class="step-card"><b>REGLA:</b> Herramienta de apoyo, jamás sustituto del ingeniero.</div>
      </div>"""
    r_l10 = """
      <div class="panel">
        <div class="stat-label" style="color:#34D399;">ESTRATEGIA FINOPS EN GOOGLE AI PRO</div>
        <div class="step-card" style="border-color:#F9D14B;"><b>GEMINI 4 CARBON (CIRUJANO):</b> Auditar repos, seguridad, bugs duros.</div>
        <div class="step-card" style="border-color:#38BDF8;"><b>NEON / HYDROGEN (DIARIO):</b> Resúmenes, scripts rápidos, iteraciones.</div>
        <div class="note-line">Proteges tu cuota semanal y sacas máximo provecho al plan Pro.</div>
      </div>"""
    r_l11 = """
      <div class="panel" style="border-color:#F9D14B;">
        <div class="stat-label">DÓNDE VERIFICAR TÚ MISMO</div>
        <div class="step-card"><b>1.</b> blog.google / deepmind.google (Model Card Carbon)</div>
        <div class="step-card"><b>2.</b> arXiv · ExploitGym &amp; SEC-bench Pro · cwe-bench.com</div>
        <div class="step-card" style="background:#F9D14B;color:#111827;font-size:32px;font-weight:900;">COMENTA: AUDITA · Checklist + Links</div>
      </div>"""

    all_scenes = "\n".join([
        scene_wrap("L01_hook", "01 · ¿ORO PURO O PURO HUMO?", "pill-amber", "¿Por qué dicen que Carbon brilla en ciberseguridad?", "No basta el titular de lanzamiento: revisamos qué pruebas realizó Google DeepMind y contra quién se midió.", "Fuente: Anuncio y Model Card · oct–nov 2026", r_l01),
        scene_wrap("L02_origen", "02 · DESPLIEGUE CONTROLADO", "pill-cyan", "Del Programa Fairwind a tu plan Google AI Pro", "Por su capacidad dual en análisis de vulnerabilidades, empezó restringido antes de abrirse a desarrolladores.", "Fuente: Google Blog / Fairwind Program", r_l02),
        scene_wrap("L03_secbench", "03 · PRUEBA 1 — DETECCIÓN", "pill-cyan", "SEC-bench Pro: 88.2% cazando bugs reales", "Reproducir fallos con pruebas de concepto válidas dentro de contenedores Docker sobre software real.", "Fuente: SEC-bench Pro / DeepMind Model Card", r_l03),
        scene_wrap("L04_exploitgym", "04 · PRUEBA 2 — EXPLOTACIÓN", "pill-amber", "ExploitGym: su mayor ventaja (54.8%)", "Evaluación de UC Berkeley y Max Planck sobre 898 fallos reales para probar explotabilidad real.", "Fuente: arXiv ExploitGym (mayo 2026)", r_l04),
        scene_wrap("L05_cwebench", "05 · PRUEBA 3 — PARCHES", "pill-emerald", "CWE-bench: 71.0% reparando sin pistas", "Entregar un repositorio entero sin señalar dónde está el fallo y verificar si el parche lo resuelve.", "Fuente: Collinear AI · cwe-bench.com (oct 2026)", r_l05),
        scene_wrap("L06_vs_astra_fable", "06 · VS ASTRA, OPUS Y FABLE", "pill-cyan", "Nadie domina todas las pruebas a la vez", "Astra brilló con 100% en ExploitBench; Opus 5.5 y Fable 5.2 compiten fuerte en ingeniería diaria.", "Fuente: OpenAI System Card / Anthropic", r_l06),
        scene_wrap("L07_vs_grok", "06 · VS GROK E ÍNDICE GENERAL", "pill-cyan", "¿Y Grok? Más el ranking Artificial Analysis", "Grok 4.6/4.7 participa en CyberGym y harnesses como Cursor, pero no lidera estas 3 métricas públicas.", "Fuente: Artificial Analysis Intelligence Index v5.0", r_l07),
        scene_wrap("L08_letrachiquita_1", "07 · LETRA CHIQUITA I", "pill-rose", "Por qué NO debes sumar porcentajes", "Mezclar datasets distintos distorsiona el riesgo real; además Carbon consume más tokens de razonamiento.", "Fuente: Crítica metodológica arXiv / AppSec", r_l08),
        scene_wrap("L09_letrachiquita_2", "07 · LETRA CHIQUITA II", "pill-rose", "Laboratorio Docker ≠ producción real", "Un 71% en benchmark no reemplaza revisión humana, sandbox ni arquitectura de mínimo privilegio.", "Fuente: Criterio de Ingeniería Legal y AppSec", r_l09),
        scene_wrap("L10_finops_pro", "08 · FINOPS GOOGLE PRO", "pill-emerald", "Cómo usar Carbon sin quemar tu cuota", "Regla del cirujano: Carbon audita lo crítico; Neon o Hydrogen ejecutan las tareas rápidas del día.", "Captoora FinOps · Uso óptimo de cuotas", r_l10),
        scene_wrap("L11_cta", "09 · VEREDICTO VERIFICADO", "pill-amber", "Músculo real con letra chiquita clara", "Comprueba tú mismo los tres benchmarks y usa estos criterios antes de confiar un repo en producción.", "Captoora Studio · ¿Oro Puro o Puro Humo?", r_l11),
    ])

    # Tweens per chapter
    scene_tweens = []
    for i, (cid, st, dd) in enumerate(slots):
        en = round(st + dd, 2)
        if i == 0:
            scene_tweens.append(f'      tl.fromTo("#{cid}-inner", {{ y: 12, opacity: 1 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power4.out" }}, {st});')
        else:
            scene_tweens.append(f'      tl.fromTo("#{cid}-inner", {{ x: 70, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.32, ease: "power4.out" }}, {st});')
        if i < len(slots) - 1:
            scene_tweens.append(f'      tl.to("#{cid}-inner", {{ x: -70, opacity: 0, duration: 0.22, ease: "power3.in" }}, {round(en - 0.22, 2)});')

    # Bar grow animations synced cleanly with L03, L04, L05, L07
    bar_tweens = [
        f'      tl.fromTo("#l03-b1", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L03_secbench"][0] + 0.4, 2)});',
        f'      tl.fromTo("#l03-b2", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L03_secbench"][0] + 0.7, 2)});',
        f'      tl.fromTo("#l04-b1", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L04_exploitgym"][0] + 0.4, 2)});',
        f'      tl.fromTo("#l04-b2", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L04_exploitgym"][0] + 0.7, 2)});',
        f'      tl.fromTo("#l04-b3", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L04_exploitgym"][0] + 1.0, 2)});',
        f'      tl.fromTo("#l05-b1", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L05_cwebench"][0] + 0.4, 2)});',
        f'      tl.fromTo("#l05-b2", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L05_cwebench"][0] + 0.7, 2)});',
        f'      tl.fromTo("#l05-b3", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L05_cwebench"][0] + 1.0, 2)});',
        f'      tl.fromTo("#l07-b1", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L07_vs_grok"][0] + 0.4, 2)});',
        f'      tl.fromTo("#l07-b2", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L07_vs_grok"][0] + 0.7, 2)});',
        f'      tl.fromTo("#l07-b3", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 0.8, ease: "power4.out" }}, {round(smap["L07_vs_grok"][0] + 1.0, 2)});',
    ]

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Gemini 4 Carbon vs Rivales en Ciberseguridad · Explicativo 3 min</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      background: #0d121a;
      font-family: "Outfit", "Nunito", sans-serif;
      color: #f8fafc;
    }}
    #root {{
      position: relative;
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      background: #0d121a;
    }}
    .bg-stage {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; }}
    .glow-1 {{
      position: absolute; width: 1000px; height: 1000px; left: -160px; top: -220px; border-radius: 50%;
      background: radial-gradient(circle, rgba(56,189,248,0.22) 0%, rgba(56,189,248,0) 70%);
    }}
    .glow-2 {{
      position: absolute; width: 1100px; height: 1100px; right: -180px; bottom: -260px; border-radius: 50%;
      background: radial-gradient(circle, rgba(249,209,75,0.16) 0%, rgba(249,209,75,0) 70%);
    }}
    .safe-16-9 {{
      position: absolute;
      inset: 56px 76px;
      z-index: 10;
    }}
    .nav-clip {{
      position: absolute;
      top: 0;
      left: 0;
      width: 1768px;
      height: 62px;
    }}
    .nav-bar {{
      display: flex;
      align-items: center;
      gap: 10px;
      height: 62px;
      padding: 8px 12px;
      border-radius: 18px;
      background: #141d2a;
      border: 2px solid #29384e;
    }}
    .nav-pill {{
      flex: 1;
      text-align: center;
      padding: 8px 10px;
      border-radius: 12px;
      background: #182232;
      color: #94a3b8;
      font-family: "Space Mono", monospace;
      font-size: 20px;
      font-weight: 700;
      white-space: nowrap;
    }}
    .scene-grid-clip {{
      position: absolute;
      top: 90px;
      left: 0;
      width: 1768px;
      height: 850px;
    }}
    .scene-grid {{
      display: flex;
      gap: 44px;
      width: 1768px;
      height: 850px;
      align-items: stretch;
    }}
    .col-left {{
      flex: 1.05;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 28px 12px 28px 8px;
    }}
    .col-right {{
      flex: 1;
      display: flex;
      align-items: center;
    }}
    .pill {{
      align-self: flex-start;
      padding: 10px 24px;
      border-radius: 999px;
      font-family: "Space Mono", monospace;
      font-size: 24px;
      font-weight: 700;
      margin-bottom: 24px;
    }}
    .pill-amber {{ background: #f9d14b; color: #111827; }}
    .pill-cyan {{ background: #38bdf8; color: #081220; }}
    .pill-emerald {{ background: #34d399; color: #062116; }}
    .pill-rose {{ background: #fb7185; color: #2b0910; }}
    .h1-wide {{
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 62px;
      line-height: 1.06;
      color: #ffffff;
      letter-spacing: -0.02em;
      margin-bottom: 24px;
    }}
    .p-wide {{
      font-family: "Nunito", "Outfit", sans-serif;
      font-size: 36px;
      font-weight: 700;
      line-height: 1.3;
      color: #cbd5e1;
      margin-bottom: 32px;
    }}
    .cite-box {{
      align-self: flex-start;
      padding: 14px 22px;
      border-radius: 16px;
      background: #141d2a;
      border: 2px solid #2c3c54;
      font-family: "Space Mono", monospace;
      font-size: 22px;
      color: #93c5fd;
    }}
    .panel {{
      width: 100%;
      background: #151e2b;
      border: 3px solid #2f4059;
      border-radius: 34px;
      padding: 40px 42px;
      box-shadow: 0 22px 48px rgba(0, 0, 0, 0.35);
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .stat-label {{
      font-family: "Space Mono", monospace;
      font-size: 24px;
      font-weight: 700;
      color: #93c5fd;
      letter-spacing: 0.04em;
    }}
    .big-stat {{
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 60px;
      line-height: 1.04;
    }}
    .sub-stat {{
      font-size: 32px;
      font-weight: 700;
      line-height: 1.28;
      color: #e2e8f0;
    }}
    .vs-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      margin-top: 8px;
    }}
    .vs-pill {{
      padding: 12px 20px;
      border-radius: 16px;
      background: #101722;
      border: 2px solid #334155;
      font-size: 24px;
      font-weight: 800;
      color: #f8fafc;
    }}
    .step-card {{
      padding: 20px 24px;
      border-radius: 20px;
      background: #101722;
      border: 2px solid #2b3a4f;
      font-size: 28px;
      line-height: 1.26;
      color: #f1f5f9;
    }}
    .hbar-row {{
      background: #101722;
      border: 2px solid #273549;
      border-radius: 20px;
      padding: 18px 22px;
    }}
    .hbar-top {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      font-size: 30px;
      font-weight: 800;
      margin-bottom: 10px;
    }}
    .hbar-track {{
      width: 100%;
      height: 22px;
      border-radius: 999px;
      background: #1e293b;
      overflow: hidden;
    }}
    .hbar-fill {{
      height: 100%;
      border-radius: 999px;
      transform-origin: left center;
    }}
    .fill-gold {{ background: #f9d14b; }}
    .fill-cyan {{ background: #38bdf8; }}
    .fill-emerald {{ background: #34d399; }}
    .fill-slate {{ background: #64748b; }}
    .note-line {{
      font-size: 24px;
      font-weight: 700;
      color: #94a3b8;
      margin-top: 4px;
    }}
    .prog-bottom-clip {{
      position: absolute;
      bottom: 0;
      left: 0;
      width: 1768px;
      height: 10px;
    }}
    .prog-bottom-rail {{
      width: 100%;
      height: 10px;
      border-radius: 999px;
      background: #1c2636;
      overflow: hidden;
    }}
    .prog-bottom-fill {{
      width: 100%;
      height: 100%;
      background: #f9d14b;
      transform-origin: left center;
    }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="carbon_explainer_3min" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080" data-fps="30">
    <audio id="master-audio" class="clip" src="assets/carbon_explainer_3min_master.wav" data-start="0" data-duration="{dur}" data-volume="1" data-track-index="10"></audio>

    <div class="bg-stage" data-layout-ignore>
      <div id="glow-1" class="glow-1"></div>
      <div id="glow-2" class="glow-2"></div>
    </div>

    <div class="safe-16-9">
      <div id="nav-wrap" class="clip nav-clip" data-start="0" data-duration="{dur}">
        <div id="nav-inner" class="nav-bar">
          {"".join(nav_pills_html)}
        </div>
      </div>

      {all_scenes}

      <div id="prog-bottom" class="clip prog-bottom-clip" data-start="0" data-duration="{dur}">
        <div class="prog-bottom-rail"><div id="prog-bottom-bar" class="prog-bottom-fill"></div></div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});

      tl.fromTo("#glow-1", {{ x: 0, y: 0 }}, {{ x: 320, y: 180, duration: {dur}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#glow-2", {{ x: 0, y: 0 }}, {{ x: -280, y: -150, duration: {dur}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#prog-bottom-bar", {{ scaleX: 0.02 }}, {{ scaleX: 1.0, duration: {dur}, ease: "none" }}, 0);

{chr(10).join(nav_tweens)}
{chr(10).join(scene_tweens)}
{chr(10).join(bar_tweens)}

      window.__timelines = window.__timelines || {{}};
      window.__timelines["carbon_explainer_3min"] = tl;
    }})();
  </script>
</body>
</html>
"""


def main() -> int:
    timings = json.loads(TIMINGS.read_text(encoding="utf-8"))

    # 1) Short 60s project
    short_dir = BASE / "hf_short_60s"
    (short_dir / "assets").mkdir(parents=True, exist_ok=True)
    (short_dir / ".gitignore").write_text(".hyperframes/\nrenders/\n", encoding="utf-8")
    shutil.copy2(BASE / "audio/carbon_short_60s_master.wav", short_dir / "assets/carbon_short_60s_master.wav")
    (short_dir / "index.html").write_text(build_short_html(timings["short_60s"]), encoding="utf-8")
    print(f"BUILT {short_dir / 'index.html'} (dur={timings['short_60s']['total_duration']}s)")

    # 2) Long 3min explainer project
    long_dir = BASE / "hf_explainer_3min"
    (long_dir / "assets").mkdir(parents=True, exist_ok=True)
    (long_dir / ".gitignore").write_text(".hyperframes/\nrenders/\n", encoding="utf-8")
    shutil.copy2(BASE / "audio/carbon_explainer_3min_master.wav", long_dir / "assets/carbon_explainer_3min_master.wav")
    (long_dir / "index.html").write_text(build_long_html(timings["explainer_3min"]), encoding="utf-8")
    print(f"BUILT {long_dir / 'index.html'} (dur={timings['explainer_3min']['total_duration']}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
