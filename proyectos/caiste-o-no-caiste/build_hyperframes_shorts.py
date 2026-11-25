#!/usr/bin/env python3
"""
Construye el proyecto HyperFrames standalone en hyperframes_shorts/ para los 3 Shorts
prioritarios (P4 CFE Segundo Robado, P2 Banco Real, P8 DHL Segundo Robado) usando
timings exactos de audio/shorts_timings.json y los activos PNG 3D voxel pastel.
"""
import html
import json
import shutil
from pathlib import Path
from typing import Any, Dict

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
PROJECT = ROOT / "proyectos/caiste-o-no-caiste"
TIMINGS_PATH = PROJECT / "audio/shorts_timings.json"
PILOTO_PATH = PROJECT / "piloto_01_nivel_facil.json"
HF_DIR = PROJECT / "hyperframes_shorts"
HF_ASSETS = HF_DIR / "assets"


def copy_assets() -> None:
    HF_ASSETS.mkdir(parents=True, exist_ok=True)
    files_to_copy = [
        PROJECT / "assets/escenarios/escenario_01_facil_casa.png",
        PROJECT / "assets/personajes/chatgpt_facil.png",
        PROJECT / "assets/personajes/guardrails_antigravity.png",
        PROJECT / "assets/personajes/grok_dificil.png",
        PROJECT / "audio/short_P4_cfe_master.wav",
        PROJECT / "audio/short_P2_banco_master.wav",
        PROJECT / "audio/short_P8_dhl_master.wav",
    ]
    for src in files_to_copy:
        if not src.exists():
            raise FileNotFoundError(f"Falta activo requerido: {src}")
        shutil.copy2(src, HF_ASSETS / src.name)


def esc(txt: str) -> str:
    return html.escape(txt, quote=True)


def build_short_html(short_meta: Dict[str, Any], q_data: Dict[str, Any]) -> str:
    sid = short_meta["short_id"]
    dur = float(short_meta["total_duration"])
    h_start = float(short_meta["hook_start"])
    h_end = float(short_meta["hook_end"])
    h_dur = round(h_end - h_start, 2)

    c_start = float(short_meta["countdown_start"])
    c_end = float(short_meta["countdown_end"])
    c_dur = round(c_end - c_start, 2)
    is_stolen = bool(short_meta["segundo_robado"])
    steal_t = short_meta["steal_time"]

    r_start = float(short_meta["reveal_start"])
    r_end = float(short_meta["reveal_end"])
    r_dur = round(r_end - r_start, 2)

    g_start = float(short_meta["guardrail_start"])
    g_dur = round(dur - g_start, 2)

    is_real = q_data["respuesta"] == "REAL"
    audio_file = short_meta["audio_file"]
    pistas = q_data["pistas"]

    hook_eyebrow = "NIVEL FÁCIL · 5 SEGUNDOS"
    hook_title = "ATENTO AL MENSAJE" if is_real else "¿CAERÍAS EN ESTE MENSAJE?"
    if short_meta["pregunta_num"] == 4:
        case_sender = "WhatsApp · Número desconocido"
        hook_title = "¿TE CORTAN LA LUZ HOY?"
    elif short_meta["pregunta_num"] == 2:
        case_sender = "App Oficial del Banco"
        hook_title = "¿FRAUDE O AVISO REAL?"
    else:
        case_sender = "SMS · Aviso de paquetería"
        hook_title = "¿PAQUETE RETENIDO EN ADUANA?"

    stamp_text = "✅ ¡ES REAL!" if is_real else "❌ ¡ES TRAMPA!"
    stamp_class = "stamp-real" if is_real else "stamp-trampa"
    cta_sub = (
        "¿Sentiste que te robaron 1 segundo? Comenta CAÍ o NO CAÍ"
        if is_stolen
        else "¿Pensaste que era estafa? Comenta CAÍ o NO CAÍ"
    )

    # Countdown clips + tweens
    digit_clips = []
    digit_tweens = []
    if is_stolen:
        assert steal_t is not None
        steal_t = float(steal_t)
        d3_dur = round(steal_t - (c_start + 2.0), 2)
        d2_dur = round((c_start + 3.0) - steal_t, 2)
        d1_start = round(c_start + 3.0, 2)
        d1_dur = round(c_end - d1_start, 2)
        steps = [
            ("digit-5", "5", c_start, 1.0, False),
            ("digit-4", "4", round(c_start + 1.0, 2), 1.0, False),
            ("digit-3", "3", round(c_start + 2.0, 2), max(0.3, d3_dur), False),
            ("digit-2", "2", steal_t, max(0.25, d2_dur), True),
            ("digit-1", "1", d1_start, max(0.5, d1_dur), False),
        ]
    else:
        steps = [
            ("digit-5", "5", c_start, 1.0, False),
            ("digit-4", "4", round(c_start + 1.0, 2), 1.0, False),
            ("digit-3", "3", round(c_start + 2.0, 2), 1.0, False),
            ("digit-2", "2", round(c_start + 3.0, 2), 1.0, False),
            ("digit-1", "1", round(c_start + 4.0, 2), 1.0, False),
        ]

    for el_id, label, st, dd, stolen_step in steps:
        extra_cls = " stolen-digit" if stolen_step else ""
        digit_clips.append(
            f'        <div id="{el_id}" class="clip digit-slot" data-start="{st}" data-duration="{dd}">\n'
            f'          <div id="{el_id}-inner" class="digit-card{extra_cls}">\n'
            f'            <span class="digit-num">{label}</span>\n'
            f'            <span class="digit-sub">{"¡UPS! −1s" if stolen_step else "SEG"}</span>\n'
            f'          </div>\n'
            f'        </div>'
        )
        if stolen_step:
            digit_tweens.append(
                f'      tl.fromTo("#{el_id}-inner", {{ scale: 1.0, x: 0, rotation: 0, opacity: 1 }}, '
                f'{{ scale: 0.72, x: 240, rotation: 18, opacity: 0.2, duration: {dd:.2f}, ease: "power3.in" }}, {st});'
            )
        else:
            digit_tweens.append(
                f'      tl.fromTo("#{el_id}-inner", {{ scale: 0.84, opacity: 0.9 }}, '
                f'{{ scale: 1.04, opacity: 1.0, duration: 0.22, ease: "back.out(2)" }}, {st});'
            )

    grok_block = ""
    grok_tween = ""
    if is_stolen:
        assert steal_t is not None
        g_steal_dur = round(c_end - steal_t, 2)
        grok_block = f"""
      <div id="grok-robbery" class="clip host-row" data-start="{steal_t}" data-duration="{max(0.8, g_steal_dur)}">
        <div id="grok-robbery-inner" class="host-card grok-card">
          <img class="avatar-img" src="assets/grok_dificil.png" alt="Grok" />
          <div class="host-copy">
            <div class="host-badge grok-badge">GROK · −1 SEG</div>
            <div class="host-line">¡Te robé 1 seg!</div>
          </div>
        </div>
      </div>"""
        grok_tween = (
            f'      tl.fromTo("#grok-robbery-inner", {{ x: 110, opacity: 0, rotation: 6 }}, '
            f'{{ x: 0, opacity: 1, rotation: 0, duration: 0.24, ease: "back.out(1.9)" }}, {steal_t});'
        )

    # Reveal clues staggered cleanly inside [r_start, r_end)
    clue_step = round(max(2.8, (r_dur - 2.0) / 3.0), 2)
    c1_t = round(r_start + 0.5, 2)
    c2_t = round(r_start + 0.5 + clue_step, 2)
    c3_t = round(r_start + 0.5 + clue_step * 2.0, 2)

    # Micro-movimientos vivos cada ~2.2s para evitar tramos estáticos ("dead_stretch")
    chatgpt_end = float(steal_t) if is_stolen else c_end
    life_tweens = []
    t_bob = round(h_start + 2.2, 2)
    up = True
    while t_bob < chatgpt_end - 1.0:
        life_tweens.append(
            f'      tl.to("#host-chatgpt-inner .avatar-img", {{ y: {-7 if up else 0}, duration: 0.9, ease: "sine.inOut" }}, {t_bob});'
        )
        up = not up
        t_bob = round(t_bob + 2.2, 2)

    t_gbob = round(r_start + 2.0, 2)
    g_up = True
    while t_gbob < dur - 1.0:
        life_tweens.append(
            f'      tl.to("#host-guardrails-inner .avatar-img", {{ y: {-7 if g_up else 0}, duration: 0.9, ease: "sine.inOut" }}, {t_gbob});'
        )
        g_up = not g_up
        t_gbob = round(t_gbob + 2.2, 2)

    if g_dur > 4.5:
        cta_pulse_t = round(g_start + 3.5, 2)
        life_tweens.append(
            f'      tl.to("#cta-box-inner", {{ scale: 1.03, duration: 0.45, ease: "power1.inOut" }}, {cta_pulse_t});'
        )
        life_tweens.append(
            f'      tl.to("#cta-box-inner", {{ scale: 1.0, duration: 0.45, ease: "power1.inOut" }}, {round(cta_pulse_t + 0.5, 2)});'
        )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>{esc(sid)} — ¿Caíste o no caíste?</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #fdf6ea;
      font-family: "Outfit", "Nunito", sans-serif;
      color: #2b2420;
    }}
    #root {{
      position: relative;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #fdf6ea;
    }}
    /* Fondo diorama pastel cálido (CERO filtros CSS ni neón) */
    .bg-stage {{
      position: absolute;
      inset: 0;
      z-index: 1;
    }}
    .bg-photo {{
      position: absolute;
      inset: 0;
      width: 1080px;
      height: 1920px;
      object-fit: cover;
      object-position: center 65%;
    }}
    .bg-veil {{
      position: absolute;
      inset: 0;
      background: linear-gradient(
        180deg,
        rgba(253, 246, 234, 0.88) 0%,
        rgba(253, 246, 234, 0.78) 54%,
        rgba(247, 236, 214, 0.58) 76%,
        rgba(245, 232, 206, 0.90) 100%
      );
    }}
    .rail-strip {{
      position: absolute;
      left: 68px;
      right: 136px;
      bottom: 430px;
      height: 18px;
      border-top: 5px solid #9c6e4b;
      border-bottom: 5px solid #8a96a6;
      opacity: 0.45;
      z-index: 2;
    }}
    /* Zona segura vertical: 168 px -> 1330 px; derecha libre de x=944..1080 para rail de botones */
    .stage-safe {{
      position: absolute;
      top: 176px;
      left: 64px;
      width: 872px;
      height: 1146px;
      z-index: 10;
    }}
    .pill-top {{
      display: inline-block;
      padding: 12px 26px;
      border-radius: 999px;
      background: #f9d14b;
      color: #2b2420;
      font-weight: 800;
      font-size: 28px;
      letter-spacing: 0.04em;
      border: 3px solid #2b2420;
      box-shadow: 0 6px 0 #d5a928;
    }}
    .pill-countdown {{
      background: #2b2420;
      color: #fdf6ea;
      border-color: #2b2420;
      box-shadow: 0 6px 0 #7a6657;
    }}
    .pill-guardrail {{
      background: #7be0b4;
      color: #1f3329;
      border-color: #2b2420;
      box-shadow: 0 6px 0 #4fae84;
    }}
    .hero-title {{
      margin-top: 22px;
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 62px;
      line-height: 1.04;
      color: #2b2420;
      letter-spacing: -0.02em;
    }}
    /* Fase 1: Hook + tarjeta de caso */
    .hook-head {{
      position: absolute;
      top: 0;
      left: 0;
      width: 872px;
    }}
    .phone-card-clip {{
      position: absolute;
      top: 252px;
      left: 0;
      width: 872px;
    }}
    .phone-card {{
      background: #fffcf5;
      border: 4px solid #2b2420;
      border-radius: 34px;
      padding: 34px 36px;
      box-shadow: 0 14px 0 #dfd1ba;
    }}
    .sender-bar {{
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 28px;
      font-weight: 800;
      color: #6b5b4f;
      margin-bottom: 18px;
    }}
    .sender-dot {{
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: {"#3ea672" if is_real else "#e06458"};
      border: 2px solid #2b2420;
    }}
    .case-body {{
      font-family: "Nunito", "Outfit", sans-serif;
      font-size: 40px;
      font-weight: 800;
      line-height: 1.24;
      color: #2b2420;
    }}
    /* Tarjeta inferior de personaje (y=800..1130 dentro de stage-safe) */
    .host-row {{
      position: absolute;
      left: 0;
      top: 785px;
      width: 872px;
    }}
    .host-card {{
      display: flex;
      align-items: center;
      gap: 28px;
      background: #fff9ee;
      border: 4px solid #2b2420;
      border-radius: 34px;
      padding: 22px 30px;
      box-shadow: 0 12px 0 #dfd1ba;
    }}
    .grok-card {{
      background: #ede9f6;
      box-shadow: 0 12px 0 #b8afc9;
    }}
    .avatar-img {{
      width: 240px;
      height: 240px;
      border-radius: 26px;
      border: 3px solid #2b2420;
      object-fit: cover;
      flex: none;
    }}
    .host-copy {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .host-badge {{
      display: inline-block;
      align-self: flex-start;
      padding: 8px 18px;
      border-radius: 999px;
      background: #7be0b4;
      color: #1d3228;
      font-size: 28px;
      font-weight: 800;
      border: 2px solid #2b2420;
    }}
    .grok-badge {{
      background: #6d568c;
      color: #fdf6ea;
    }}
    .guard-badge {{
      background: #f9d14b;
      color: #2b2420;
    }}
    .host-line {{
      font-size: 36px;
      font-weight: 800;
      line-height: 1.18;
      color: #2b2420;
    }}
    /* Fase 2: Reloj 5 segundos / 4s Segundo Robado */
    .cd-head {{
      position: absolute;
      top: 0;
      left: 0;
      width: 872px;
    }}
    .cd-question {{
      margin-top: 20px;
      font-size: 40px;
      font-weight: 800;
      line-height: 1.2;
      background: #fffcf5;
      border: 4px solid #2b2420;
      border-radius: 26px;
      padding: 22px 28px;
      box-shadow: 0 10px 0 #dfd1ba;
    }}
    .digit-slot {{
      position: absolute;
      top: 290px;
      left: 0;
      width: 872px;
      height: 450px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .digit-card {{
      width: 420px;
      height: 420px;
      border-radius: 68px;
      background: #fff8ea;
      border: 6px solid #2b2420;
      box-shadow: 0 18px 0 #d5a928;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }}
    .stolen-digit {{
      background: #f6d7d4;
      box-shadow: 0 18px 0 #c9645b;
    }}
    .digit-num {{
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 220px;
      line-height: 0.95;
      color: #2b2420;
    }}
    .digit-sub {{
      font-size: 32px;
      font-weight: 800;
      letter-spacing: 0.08em;
      color: #6b5b4f;
      margin-top: 8px;
    }}
    /* Fase 3: Revelación + 3 pistas */
    .reveal-stamp-wrap {{
      position: absolute;
      top: 0;
      left: 0;
      width: 872px;
    }}
    .stamp-banner {{
      padding: 26px 34px;
      border-radius: 30px;
      border: 5px solid #2b2420;
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 68px;
      text-align: center;
      letter-spacing: -0.01em;
    }}
    .stamp-trampa {{
      background: #e66b60;
      color: #fffcf5;
      box-shadow: 0 12px 0 #a9443b;
    }}
    .stamp-real {{
      background: #3aa772;
      color: #fffcf5;
      box-shadow: 0 12px 0 #26734e;
    }}
    .clues-wrap {{
      position: absolute;
      top: 175px;
      left: 0;
      width: 872px;
      height: 580px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .clue-row {{
      position: relative;
      width: 872px;
      min-height: 168px;
    }}
    .clue-card {{
      display: flex;
      align-items: center;
      gap: 22px;
      background: #fffcf5;
      border: 4px solid #2b2420;
      border-radius: 26px;
      padding: 22px 26px;
      box-shadow: 0 9px 0 #dfd1ba;
    }}
    .clue-num {{
      width: 64px;
      height: 64px;
      border-radius: 20px;
      background: #f9d14b;
      border: 3px solid #2b2420;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 36px;
      flex: none;
    }}
    .clue-text {{
      font-family: "Nunito", "Outfit", sans-serif;
      font-size: 34px;
      font-weight: 800;
      line-height: 1.2;
      color: #2b2420;
    }}
    /* Fase 4: Guardrail + CTA */
    .guard-head {{
      position: absolute;
      top: 0;
      left: 0;
      width: 872px;
    }}
    .guard-card-clip {{
      position: absolute;
      top: 100px;
      left: 0;
      width: 872px;
    }}
    .guard-card {{
      background: #fff9e6;
      border: 5px solid #2b2420;
      border-radius: 34px;
      padding: 36px;
      box-shadow: 0 14px 0 #d5a928;
    }}
    .guard-title {{
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 46px;
      color: #2b2420;
      margin-bottom: 16px;
    }}
    .guard-rule {{
      font-family: "Nunito", "Outfit", sans-serif;
      font-size: 40px;
      font-weight: 800;
      line-height: 1.24;
      color: #2b2420;
    }}
    .cta-box-clip {{
      position: absolute;
      top: 525px;
      left: 0;
      width: 872px;
    }}
    .cta-box {{
      background: #2b2420;
      color: #fdf6ea;
      border-radius: 30px;
      padding: 28px 34px;
      border: 4px solid #2b2420;
      box-shadow: 0 12px 0 #7a6657;
    }}
    .cta-main {{
      font-family: "Archivo Black", "Outfit", sans-serif;
      font-size: 42px;
      color: #f9d14b;
      margin-bottom: 10px;
    }}
    .cta-sub {{
      font-size: 32px;
      font-weight: 700;
      line-height: 1.2;
      color: #fdf6ea;
    }}
  </style>
</head>
<body>
  <div
    id="root"
    data-composition-id="{esc(sid)}"
    data-start="0"
    data-duration="{dur}"
    data-width="1080"
    data-height="1920"
    data-fps="30"
  >
    <audio
      id="master-audio"
      class="clip"
      src="assets/{esc(audio_file)}"
      data-start="0"
      data-duration="{dur}"
      data-volume="1"
      data-track-index="10"
    ></audio>

    <div class="bg-stage" data-layout-ignore>
      <img class="bg-photo" src="assets/escenario_01_facil_casa.png" alt="Escenario voxel pastel" />
      <div class="bg-veil"></div>
      <div class="rail-strip"></div>
    </div>

    <div class="stage-safe">
      <!-- FASE 1: HOOK & CASO -->
      <div id="hook-head" class="clip hook-head" data-start="{h_start}" data-duration="{h_dur}">
        <div id="hook-head-inner">
          <div class="pill-top">{esc(hook_eyebrow)}</div>
          <h1 class="hero-title">{esc(hook_title)}</h1>
        </div>
      </div>

      <div id="phone-card" class="clip phone-card-clip" data-start="{h_start}" data-duration="{h_dur}">
        <div id="phone-card-inner" class="phone-card">
          <div class="sender-bar"><span class="sender-dot"></span>{esc(case_sender)}</div>
          <p class="case-body">{esc(q_data["caso_pantalla"])}</p>
        </div>
      </div>

      <div id="host-chatgpt" class="clip host-row" data-start="{h_start}" data-duration="{round(chatgpt_end - h_start, 2)}">
        <div id="host-chatgpt-inner" class="host-card">
          <img class="avatar-img" src="assets/chatgpt_facil.png" alt="ChatGPT Nivel Fácil" />
          <div class="host-copy">
            <div class="host-badge">CHATGPT · NIVEL FÁCIL</div>
            <div class="host-line">¿Real o trampa? Tienes 5 segundos.</div>
          </div>
        </div>
      </div>

      <!-- FASE 2: CONTADOR -->
      <div id="cd-head" class="clip cd-head" data-start="{c_start}" data-duration="{c_dur}">
        <div id="cd-head-inner">
          <div class="pill-top pill-countdown">DECIDE ANTES DE CERO</div>
          <div class="cd-question">{esc(q_data["titulo"])} — ¿REAL O TRAMPA?</div>
        </div>
      </div>

{chr(10).join(digit_clips)}
{grok_block}

      <!-- FASE 3: REVELACIÓN + 3 PISTAS -->
      <div id="reveal-stamp" class="clip reveal-stamp-wrap" data-start="{r_start}" data-duration="{r_dur}">
        <div id="reveal-stamp-inner" class="stamp-banner {stamp_class}">{esc(stamp_text)}</div>
      </div>

      <div class="clues-wrap">
        <div id="clue-1" class="clip clue-row" data-start="{c1_t}" data-duration="{round(r_end - c1_t, 2)}">
          <div id="clue-1-inner" class="clue-card">
            <div class="clue-num">1</div>
            <div class="clue-text">{esc(pistas[0])}</div>
          </div>
        </div>
        <div id="clue-2" class="clip clue-row" data-start="{c2_t}" data-duration="{round(r_end - c2_t, 2)}">
          <div id="clue-2-inner" class="clue-card">
            <div class="clue-num">2</div>
            <div class="clue-text">{esc(pistas[1])}</div>
          </div>
        </div>
        <div id="clue-3" class="clip clue-row" data-start="{c3_t}" data-duration="{round(r_end - c3_t, 2)}">
          <div id="clue-3-inner" class="clue-card">
            <div class="clue-num">3</div>
            <div class="clue-text">{esc(pistas[2])}</div>
          </div>
        </div>
      </div>

      <div id="host-guardrails" class="clip host-row" data-start="{r_start}" data-duration="{round(dur - r_start, 2)}">
        <div id="host-guardrails-inner" class="host-card">
          <img class="avatar-img" src="assets/guardrails_antigravity.png" alt="Antigravity Guardrails" />
          <div class="host-copy">
            <div class="host-badge guard-badge">ANTIGRAVITY · GUARDRAILS</div>
            <div class="host-line">Pon los rieles antes de dar clic.</div>
          </div>
        </div>
      </div>

      <!-- FASE 4: GUARDRAIL + CTA -->
      <div id="guard-head" class="clip guard-head" data-start="{g_start}" data-duration="{g_dur}">
        <div id="guard-head-inner">
          <div class="pill-top pill-guardrail">TU REGLA DE BOLSILLO</div>
        </div>
      </div>

      <div id="guard-card" class="clip guard-card-clip" data-start="{g_start}" data-duration="{g_dur}">
        <div id="guard-card-inner" class="guard-card">
          <div class="guard-title">GUARDRAIL 🛡️</div>
          <p class="guard-rule">{esc(q_data["guardrail"])}</p>
        </div>
      </div>

      <div id="cta-box" class="clip cta-box-clip" data-start="{round(g_start + 1.2, 2)}" data-duration="{round(max(1.0, g_dur - 1.2), 2)}">
        <div id="cta-box-inner" class="cta-box">
          <div class="cta-main">¿CAÍSTE O NO CAÍSTE?</div>
          <div class="cta-sub">{esc(cta_sub)}</div>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});

      // Frame 0 visible inmediatamente (nunca negro ni opacidad 0 al arranque)
      tl.fromTo("#hook-head-inner", {{ y: 12, opacity: 1 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power2.out" }}, {h_start});
      tl.fromTo("#phone-card-inner", {{ y: 16, scale: 0.97, opacity: 1 }}, {{ y: 0, scale: 1.0, opacity: 1, duration: 0.45, ease: "back.out(1.4)" }}, {h_start});
      tl.fromTo("#host-chatgpt-inner", {{ y: 14, opacity: 1 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power2.out" }}, {h_start});

      tl.fromTo("#cd-head-inner", {{ y: 18, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, ease: "power2.out" }}, {c_start});
{chr(10).join(digit_tweens)}
{grok_tween}

      tl.fromTo("#reveal-stamp-inner", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1.0, opacity: 1, duration: 0.28, ease: "back.out(2)" }}, {r_start});
      tl.fromTo("#host-guardrails-inner", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, ease: "power2.out" }}, {r_start});
      tl.fromTo("#clue-1-inner", {{ x: -30, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.28, ease: "power2.out" }}, {c1_t});
      tl.fromTo("#clue-2-inner", {{ x: -30, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.28, ease: "power2.out" }}, {c2_t});
      tl.fromTo("#clue-3-inner", {{ x: -30, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.28, ease: "power2.out" }}, {c3_t});

      tl.fromTo("#guard-head-inner", {{ y: 16, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, ease: "power2.out" }}, {g_start});
      tl.fromTo("#guard-card-inner", {{ scale: 0.94, opacity: 0 }}, {{ scale: 1.0, opacity: 1, duration: 0.32, ease: "back.out(1.5)" }}, {g_start});
      tl.fromTo("#cta-box-inner", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.32, ease: "power2.out" }}, {round(g_start + 1.2, 2)});
{chr(10).join(life_tweens)}

      window.__timelines = window.__timelines || {{}};
      window.__timelines["{esc(sid)}"] = tl;
    }})();
  </script>
</body>
</html>
"""


def main() -> int:
    copy_assets()
    timings = json.loads(TIMINGS_PATH.read_text(encoding="utf-8"))
    piloto = json.loads(PILOTO_PATH.read_text(encoding="utf-8"))
    q_by_num = {q["numero"]: q for q in piloto["preguntas"]}

    for sm in timings["shorts"]:
        q_data = q_by_num[sm["pregunta_num"]]
        html_src = build_short_html(sm, q_data)
        out_html = HF_DIR / f"{sm['short_id']}.html"
        out_html.write_text(html_src, encoding="utf-8")
        print(f"BUILT {out_html.relative_to(ROOT)} (dur={sm['total_duration']}s, steal={sm['steal_time']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
