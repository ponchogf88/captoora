#!/usr/bin/env python3
"""
Motor de audio + SFX sincronizados para ¿Caíste o no caíste?
- Usa ElevenLabs v3 (TONY_ID = Antigravity Guardrails, AGY_ID = ChatGPT Fácil)
  con caché en audio/cache/ para proteger la cuota.
- Por defecto (--shorts) genera únicamente los 3 Shorts prioritarios (P4, P2, P8).
- Con --all prepara además el caché/master del piloto completo de 10 preguntas.
"""
import argparse
import json
import math
import struct
import subprocess
import sys
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
PROJECT = ROOT / "proyectos/caiste-o-no-caiste"
WATERS_SCRIPTS = ROOT / "proyectos/waters-serie/scripts"
sys.path.insert(0, str(WATERS_SCRIPTS))

from waters_audio_engine import (  # noqa: E402
    AGY_ID,
    FFMPEG,
    SR,
    TONY_ID,
    _add_sample,
    add_ui_pop,
    load_api_key,
    probe_duration,
    tts_to_mp3,
)

CACHE_DIR = PROJECT / "audio/cache"
AUDIO_OUT = PROJECT / "audio"
PILOTO_JSON = PROJECT / "piloto_01_nivel_facil.json"
SHORTS_TIMINGS_JSON = AUDIO_OUT / "shorts_timings.json"

SHORTS_SPECS = [
    {
        "short_id": "short_P4",
        "pregunta_num": 4,
        "slug": "P4_CFE",
        "master_name": "short_P4_cfe_master.wav",
        "render_name": "CAISTE_SHORT_01_P4_CFE_SEGUNDO_ROBADO.mp4",
        "seg1": (
            "Te llega este WhatsApp ahorita: tu recibo de CFE venció, paga mil "
            "doscientos cuarenta pesos en dos horas o te cortan la luz hoy. "
            "¿Real o trampa? Cinco segundos."
        ),
        "seg2": (
            "¡Trampa! Uno: CFE nunca cobra recibos ni amenaza cortes desde un "
            "WhatsApp particular. Dos: no trae tu nombre ni número de servicio real. "
            "Tres: usan pánico extremo de dos horas para que pagues sin pensar."
        ),
        "seg3": (
            "Guardrail: revisa y paga siempre directo en la app CFE Contigo. "
            "Y dime la neta… ¿sentiste que te robaron un segundo? Comenta CAÍ o NO CAÍ."
        ),
    },
    {
        "short_id": "short_P2",
        "pregunta_num": 2,
        "slug": "P2_BANCO",
        "master_name": "short_P2_banco_master.wav",
        "render_name": "CAISTE_SHORT_02_P2_BANCO_REAL.mp4",
        "seg1": (
            "Abres la app oficial de tu banco y adentro te sale: compra registrada "
            "por cuatrocientos ochenta pesos en farmacia, ¿fuiste tú?, botón sí o no. "
            "¿Real o trampa? Cinco segundos."
        ),
        "seg2": (
            "¡Real! ¡Sí era verdadero! Uno: ya estás autenticado adentro de tu app "
            "oficial del banco. Dos: no te pide NIP, contraseña ni códigos por chat. "
            "Tres: solo confirmas o bloqueas el cargo dentro del mismo sistema."
        ),
        "seg3": (
            "Guardrail: desconfiar no es bloquear todo a ciegas, verifica dentro de tu "
            "app oficial antes de entrar en pánico. ¿Caíste pensando que era estafa? "
            "Comenta CAÍ o NO CAÍ."
        ),
    },
    {
        "short_id": "short_P8",
        "pregunta_num": 8,
        "slug": "P8_DHL",
        "master_name": "short_P8_dhl_master.wav",
        "render_name": "CAISTE_SHORT_03_P8_DHL_SEGUNDO_ROBADO.mp4",
        "seg1": (
            "Te llega este SMS rápido: DHL Express, tu envío internacional está "
            "retenido en aduana, paga trescientos cincuenta pesos en este enlace "
            "para liberarlo. ¿Real o trampa? Cinco segundos."
        ),
        "seg2": (
            "¡Trampa! Uno: DHL nunca cobra impuestos aduanales con enlaces genéricos "
            "por SMS. Dos: apuestan a que estés esperando un pedido reciente. "
            "Tres: meten prisa para que sueltes tu tarjeta sin validar."
        ),
        "seg3": (
            "Guardrail: copia tu guía real y consúltala directo en el portal oficial "
            "de DHL. Y dime la neta… ¿sentiste que te robaron un segundo? Comenta CAÍ o NO CAÍ."
        ),
    },
]


def add_tone_ping(buf_l: List[float], buf_r: List[float], start: float, freq: float, dur: float, amp: float, pan: float = 0.0) -> None:
    n_len = int(dur * SR)
    base = int(start * SR)
    for k in range(n_len):
        dt = k / SR
        env = min(1.0, dt / 0.004) * math.exp(-dt * (5.5 / max(dur, 0.05)))
        val = amp * env * (math.sin(2.0 * math.pi * freq * dt) + 0.25 * math.sin(4.0 * math.pi * freq * dt))
        _add_sample(buf_l, buf_r, base + k, val, pan)


def add_clock_tick(buf_l: List[float], buf_r: List[float], start: float, accent: bool = False) -> None:
    dur = 0.085
    n_len = int(dur * SR)
    base = int(start * SR)
    f0 = 1320.0 if accent else 980.0
    amp = 0.42 if accent else 0.34
    for k in range(n_len):
        dt = k / SR
        env = min(1.0, dt / 0.0015) * math.exp(-dt * 48.0)
        click = math.sin(2.0 * math.pi * f0 * dt) + 0.45 * math.sin(2.0 * math.pi * (f0 * 2.1) * dt)
        _add_sample(buf_l, buf_r, base + k, amp * env * click, 0.0)


def add_steal_slide(buf_l: List[float], buf_r: List[float], start: float) -> None:
    """SFX travieso cuando Grok se roba un segundo: zip ascendente + pop juguetón."""
    dur = 0.22
    n_len = int(dur * SR)
    base = int(start * SR)
    phase = 0.0
    for k in range(n_len):
        dt = k / SR
        f_inst = 460.0 + 920.0 * (dt / dur) ** 1.4
        phase += 2.0 * math.pi * f_inst / SR
        env = min(1.0, dt / 0.008) * math.exp(-dt * 12.0)
        _add_sample(buf_l, buf_r, base + k, 0.38 * env * math.sin(phase), -0.25)
    add_ui_pop(buf_l, buf_r, start + 0.14, f_start=340.0, f_end=1120.0, amp=0.45, with_sparkle=True)


def add_time_up_alarm(buf_l: List[float], buf_r: List[float], start: float) -> None:
    add_tone_ping(buf_l, buf_r, start, 784.0, 0.16, 0.36)
    add_tone_ping(buf_l, buf_r, start + 0.09, 523.25, 0.22, 0.38)


def add_reveal_sting(buf_l: List[float], buf_r: List[float], start: float, is_real: bool) -> None:
    if is_real:
        # Acorde mayor cálido C5-E5-G5
        for idx, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
            add_tone_ping(buf_l, buf_r, start + idx * 0.045, f, 0.45, 0.26, pan=(idx - 1.5) * 0.2)
    else:
        # Golpe game-show para TRAMPA
        add_tone_ping(buf_l, buf_r, start, 311.13, 0.22, 0.34, pan=-0.15)
        add_tone_ping(buf_l, buf_r, start + 0.06, 220.0, 0.35, 0.38, pan=0.15)
        add_ui_pop(buf_l, buf_r, start + 0.02, f_start=180.0, f_end=640.0, amp=0.35, with_sparkle=False)


def add_warm_bed(buf_l: List[float], buf_r: List[float], total_sec: float) -> None:
    """Cama musical marimba/pad suave sin derechos (-24 dB aprox bajo voz)."""
    chords = [
        (261.63, 329.63, 392.00),  # C
        (220.00, 261.63, 329.63),  # Am
        (174.61, 220.00, 261.63),  # F
        (196.00, 246.94, 293.66),  # G
    ]
    n_total = len(buf_l)
    fade_len = int(0.8 * SR)
    step = 0.5
    t = 0.0
    beat_idx = 0
    while t < total_sec - 0.3:
        chord = chords[(beat_idx // 4) % len(chords)]
        note = chord[beat_idx % 3]
        add_tone_ping(buf_l, buf_r, t, note * 2.0, 0.42, 0.045, pan=((beat_idx % 2) - 0.5) * 0.35)
        t += step
        beat_idx += 1

    # Soft pad undertone
    for k in range(min(n_total, int(total_sec * SR))):
        sec = k / SR
        c_idx = int(sec / 2.0) % len(chords)
        c = chords[c_idx]
        env = min(1.0, sec / 0.4) * min(1.0, max(0.0, (total_sec - sec) / 0.8))
        val = 0.022 * env * (
            math.sin(2.0 * math.pi * c[0] * sec)
            + 0.7 * math.sin(2.0 * math.pi * c[1] * sec)
        )
        buf_l[k] += val
        buf_r[k] += val
    _ = fade_len


def write_wav(path: Path, buf_l: List[float], buf_r: List[float]) -> None:
    peak = max(0.001, max(max(abs(x) for x in buf_l), max(abs(x) for x in buf_r)))
    gain = min(1.0, 0.85 / peak)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        frames = bytearray()
        for l_val, r_val in zip(buf_l, buf_r):
            il = max(-32767, min(32767, int(l_val * gain * 32767.0)))
            ir = max(-32767, min(32767, int(r_val * gain * 32767.0)))
            frames.extend(struct.pack("<hh", il, ir))
        wf.writeframes(bytes(frames))


def get_tts_cached(key: str, text: str, voice_id: str, api_key: str) -> tuple[Path, int]:
    mp3_path = CACHE_DIR / f"{key}.mp3"
    if mp3_path.exists() and mp3_path.stat().st_size > 1000:
        return mp3_path, 0
    if not api_key:
        raise RuntimeError(f"Falta ELEVENLABS_API_KEY para sintetizar {mp3_path}")
    tts_to_mp3(text, voice_id, mp3_path, api_key, stability=0.35, language_code="es")
    return mp3_path, len(text)


def build_short(spec: Dict[str, Any], q_data: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    short_id = spec["short_id"]
    p1, c1 = get_tts_cached(f"{short_id}_seg1_chatgpt", spec["seg1"], AGY_ID, api_key)
    p2, c2 = get_tts_cached(f"{short_id}_seg2_guardrails", spec["seg2"], TONY_ID, api_key)
    p3, c3 = get_tts_cached(f"{short_id}_seg3_cta", spec["seg3"], TONY_ID, api_key)
    chars_used = c1 + c2 + c3

    d1 = probe_duration(p1)
    d2 = probe_duration(p2)
    d3 = probe_duration(p3)

    is_stolen = bool(q_data["segundo_robado"])
    is_real = q_data["respuesta"] == "REAL"

    hook_start = 0.0
    seg1_at = 0.08
    hook_end = round(seg1_at + d1 + 0.14, 2)

    countdown_start = hook_end
    countdown_dur = 4.0 if is_stolen else 5.0
    countdown_end = round(countdown_start + countdown_dur, 2)
    steal_time: Optional[float] = round(countdown_start + 2.65, 2) if is_stolen else None

    reveal_start = countdown_end
    seg2_at = round(reveal_start + 0.28, 2)
    reveal_end = round(seg2_at + d2 + 0.22, 2)

    guardrail_start = reveal_end
    seg3_at = round(guardrail_start + 0.16, 2)
    total_duration = round(math.ceil((seg3_at + d3 + 0.65) * 30.0) / 30.0, 2)

    n_total = int((total_duration + 0.25) * SR)
    buf_l = [0.0] * n_total
    buf_r = [0.0] * n_total

    # 1. Cama musical + notificación inicial
    add_warm_bed(buf_l, buf_r, total_duration)
    add_ui_pop(buf_l, buf_r, 0.15, f_start=320.0, f_end=980.0, amp=0.38, with_sparkle=True)

    # 2. Ticks del contador + robo de segundo o chime final
    if is_stolen:
        for offset in (0.0, 1.0, 2.0, 3.0):
            add_clock_tick(buf_l, buf_r, countdown_start + offset, accent=(offset == 0.0))
        assert steal_time is not None
        add_steal_slide(buf_l, buf_r, steal_time)
        add_time_up_alarm(buf_l, buf_r, countdown_start + 3.92)
    else:
        for offset in (0.0, 1.0, 2.0, 3.0, 4.0):
            add_clock_tick(buf_l, buf_r, countdown_start + offset, accent=(offset == 0.0))
        add_tone_ping(buf_l, buf_r, countdown_start + 4.92, 880.0, 0.25, 0.36)

    # 3. Sting revelación + transición guardrail
    add_reveal_sting(buf_l, buf_r, reveal_start + 0.06, is_real=is_real)
    add_ui_pop(buf_l, buf_r, guardrail_start + 0.05, f_start=290.0, f_end=940.0, amp=0.36, with_sparkle=True)

    sfx_wav = CACHE_DIR / f"{short_id}_sfx.wav"
    write_wav(sfx_wav, buf_l, buf_r)

    master_wav = AUDIO_OUT / spec["master_name"]
    fc = (
        f"[1:a]adelay={int(seg1_at * 1000)}|{int(seg1_at * 1000)},volume=1.30[v1];"
        f"[2:a]adelay={int(seg2_at * 1000)}|{int(seg2_at * 1000)},volume=1.32[v2];"
        f"[3:a]adelay={int(seg3_at * 1000)}|{int(seg3_at * 1000)},volume=1.32[v3];"
        f"[4:a]volume=0.85[sfx];"
        f"[0:a][sfx][v1][v2][v3]amix=inputs=5:duration=longest:normalize=0,"
        f"alimiter=limit=0.84[aout]"
    )
    subprocess.run(
        [
            FFMPEG, "-y",
            "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={total_duration:.2f}",
            "-i", str(p1),
            "-i", str(p2),
            "-i", str(p3),
            "-i", str(sfx_wav),
            "-filter_complex", fc,
            "-map", "[aout]",
            "-t", f"{total_duration:.2f}",
            "-ar", "44100",
            "-ac", "2",
            str(master_wav),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    real_dur = round(probe_duration(master_wav), 2)
    return {
        "short_id": short_id,
        "pregunta_num": spec["pregunta_num"],
        "slug": spec["slug"],
        "titulo": q_data["titulo"],
        "respuesta": q_data["respuesta"],
        "segundo_robado": is_stolen,
        "render_name": spec["render_name"],
        "audio_file": spec["master_name"],
        "audio_path": f"audio/{spec['master_name']}",
        "hook_start": hook_start,
        "hook_end": hook_end,
        "countdown_start": countdown_start,
        "countdown_end": countdown_end,
        "steal_time": steal_time,
        "reveal_start": reveal_start,
        "reveal_end": reveal_end,
        "guardrail_start": guardrail_start,
        "total_duration": real_dur,
        "seg_durations": {"seg1": round(d1, 2), "seg2": round(d2, 2), "seg3": round(d3, 2)},
        "char_count_used": chars_used,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera audios + SFX sincronizados de Piloto 01")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--shorts", action="store_true", help="Genera solo los 3 Shorts prioritarios (default)")
    group.add_argument("--all", action="store_true", help="Cachea locuciones completas del piloto de 10 preguntas")
    args = parser.parse_args()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_OUT.mkdir(parents=True, exist_ok=True)

    piloto = json.loads(PILOTO_JSON.read_text(encoding="utf-8"))
    q_by_num = {q["numero"]: q for q in piloto["preguntas"]}
    api_key = load_api_key()

    results = []
    total_chars = 0
    for spec in SHORTS_SPECS:
        q_data = q_by_num[spec["pregunta_num"]]
        meta = build_short(spec, q_data, api_key)
        results.append(meta)
        total_chars += meta["char_count_used"]
        print(
            f"OK {meta['short_id']} -> {meta['audio_file']} "
            f"(dur={meta['total_duration']}s, steal={meta['steal_time']}, chars_tts={meta['char_count_used']})"
        )

    if args.all:
        # Sintetiza también intro/outro y preguntas restantes en caché (bajo pedido explícito)
        _, c_intro = get_tts_cached("full_intro", piloto["intro"]["texto"], TONY_ID, api_key)
        _, c_outro = get_tts_cached("full_outro", piloto["outro"]["texto"], TONY_ID, api_key)
        total_chars += c_intro + c_outro
        for q in piloto["preguntas"]:
            n = q["numero"]
            _, ca = get_tts_cached(f"full_P{n}_caso", f"Pregunta {n}. {q['caso_pantalla']} Cinco segundos.", AGY_ID, api_key)
            pistas = " ".join(q["pistas"])
            _, cb = get_tts_cached(f"full_P{n}_rev", f"¡{q['respuesta']}! {pistas} Guardrail: {q['guardrail']}", TONY_ID, api_key)
            total_chars += ca + cb
        print(f"OK --all caché completo generado (total_chars_sintetizados={total_chars})")

    payload = {
        "total_chars_newly_synthesized": total_chars,
        "shorts": results,
    }
    SHORTS_TIMINGS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"TIMINGS_WRITTEN -> {SHORTS_TIMINGS_JSON.relative_to(ROOT)} | NEW_CHARS={total_chars}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
