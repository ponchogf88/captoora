#!/usr/bin/env python3
"""
Genera voz ElevenLabs v3 + cama ambiental + capa de SFX Toy-Prop sincronizada
para BF01 Black Friday (WATERS_013 · PRESUPUESTO) y exporta los timings exactos
en proyectos/waters-3d-studio/src/data/bf01Timings.json.
"""
import json
import math
import shutil
import struct
import subprocess
import sys
import urllib.request
import wave
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
SCRIPTS_DIR = ROOT / "proyectos/waters-serie/scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import waters_audio_engine as engine  # noqa: E402
import add_toyprop_sfx as sfx  # noqa: E402

WORK_DIR = ROOT / "proyectos/waters-serie/black_friday_bf01"
AUDIO_DIR = WORK_DIR / "audio"
CACHE_DIR = AUDIO_DIR / "cache"
TIMINGS_ARCHIVE = AUDIO_DIR / "bf01_timings.json"
TIMINGS_STUDIO = ROOT / "proyectos/waters-3d-studio/src/data/bf01Timings.json"
MASTER_WAV = AUDIO_DIR / "bf01_master_sfx.wav"

FFMPEG = engine.FFMPEG if Path(engine.FFMPEG).exists() else (shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg")
FFPROBE = engine.FFPROBE if Path(engine.FFPROBE).exists() else (shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe")
SR = 44100
FPS = 30

BF01_SCRIPT: List[Dict[str, Any]] = [
    {
        "id": "A1_hook",
        "pause_after": 0.25,
        "text": (
            "Hoy es Black Friday y media ciudad está metiendo su tarjeta en pruebas gratis "
            "y APIs de inteligencia artificial... pero un solo botón apagado te puede despertar "
            "mañana con cuarenta mil pesos cobrados en el banco."
        ),
    },
    {
        "id": "A2_bucle",
        "pause_after": 0.25,
        "text": (
            "Dejas corriendo tu primer agente automático en la noche usando la tarjeta de tu negocio. "
            "Un pequeño error de programación mete al bot en bucle infinito: se reintenta diez mil veces "
            "en cuatro horas mientras duermes."
        ),
    },
    {
        "id": "A3a_grafica",
        "pause_after": 0.20,
        "text": (
            "Mira cómo sube la consola: a las dos de la mañana van cuatrocientos veinte dólares, "
            "a las cuatro ya cruzaste mil doscientos cincuenta, y a las seis amaneces con dos mil dólares quemados."
        ),
    },
    {
        "id": "A3b_gauge",
        "pause_after": 0.25,
        "text": (
            "Todo porque el Auto-Recharge siguió cobrando sin pedirte permiso "
            "y sin un límite duro encendido."
        ),
    },
    {
        "id": "A4_puertas",
        "pause_after": 0.25,
        "text": (
            "Hoy en Black Friday tienes dos puertas: meter tu tarjeta principal directo "
            "y rezar que nada falle, o blindarte en tres minutos antes de dar clic."
        ),
    },
    {
        "id": "A5a_candados",
        "pause_after": 0.25,
        "text": (
            "Tres candados obligatorios: uno, activa Hard Monthly Limit de veinte dólares "
            "en Gemini, Anthropic u OpenAI. Dos, usa tarjeta virtual topada. "
            "Tres, exige aprobación humana arriba de diez ejecuciones."
        ),
    },
    {
        "id": "A5b_cta",
        "pause_after": 0.45,
        "text": (
            "Que tu automatización no se vuelva tu bancarrota. "
            "Comenta PRESUPUESTO y te paso la guía exacta paso a paso."
        ),
    },
]


def check_elevenlabs_quota(api_key: str) -> Dict[str, Any]:
    try:
        req = urllib.request.Request(
            "https://api.elevenlabs.io/v1/user/subscription",
            headers={"xi-api-key": api_key},
        )
        data = json.loads(urllib.request.urlopen(req, timeout=15).read())
        used = int(data.get("character_count", 0))
        limit = int(data.get("character_limit", 0))
        return {"character_count": used, "character_limit": limit, "remaining": limit - used}
    except Exception as exc:
        return {"error": str(exc)}


def build_ambient_bed(total_sec: float, out_wav: Path) -> None:
    n_total = int((total_sec + 0.3) * SR)
    freqs = (110.0, 164.81, 261.63, 392.0)
    buf = bytearray()
    for i in range(n_total):
        t = i / SR
        env_fade = min(1.0, t / 0.6) * min(1.0, max(0.0, (total_sec - t) / 0.8))
        pulse = 0.72 + 0.28 * math.sin(2.0 * math.pi * 0.25 * t)
        val = sum(math.sin(2.0 * math.pi * f * t + idx * 0.6) * (0.28 / (idx + 1)) for idx, f in enumerate(freqs))
        sub = t % 1.0
        tick = math.sin(2.0 * math.pi * 880.0 * sub) * math.exp(-sub * 85.0) * 0.04
        sample = (val * 0.14 * pulse + tick) * env_fade
        s_i = max(-32767, min(32767, int(sample * 32767.0)))
        buf.extend(struct.pack("<hh", s_i, s_i))
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(bytes(buf))


def main() -> int:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    api_key = engine.load_api_key()
    if not api_key:
        raise RuntimeError("No se encontró ELEVENLABS_API_KEY en .env ni entorno")

    before = check_elevenlabs_quota(api_key)
    print("ElevenLabs quota BEFORE:", before)

    clips: List[Dict[str, Any]] = []
    t_cursor = 0.15
    total_chars = 0

    for item in BF01_SCRIPT:
        mp3_path = CACHE_DIR / f"{item['id']}.mp3"
        chars = len(item["text"])
        total_chars += chars
        if not mp3_path.exists():
            print(f"[BF01] TTS {item['id']} ({chars} chars)...")
            engine.tts_to_mp3(
                item["text"],
                engine.TONY_ID,
                mp3_path,
                api_key,
                stability=0.34,
                language_code="es",
            )
        else:
            print(f"[BF01] Cache HIT {item['id']} ({chars} chars)")

        dur = engine.probe_duration(mp3_path)
        pause = float(item.get("pause_after", 0.25))
        start_s = round(t_cursor, 3)
        end_s = round(t_cursor + dur + pause, 3)
        start_f = int(round(start_s * FPS))
        end_f = int(round(end_s * FPS))
        clips.append(
            {
                "id": item["id"],
                "start": start_s,
                "voice_end": round(t_cursor + dur, 3),
                "end": end_s,
                "duration": round(end_s - start_s, 3),
                "voice_dur": round(dur, 3),
                "startFrame": start_f,
                "durationInFrames": max(1, end_f - start_f),
                "chars": chars,
                "mp3": str(mp3_path.relative_to(ROOT)),
            }
        )
        t_cursor = end_s

    # Anchor first clip from frame 0 visually (audio starts at 0.15s)
    clips[0]["startFrame"] = 0
    clips[0]["durationInFrames"] = int(round(clips[0]["end"] * FPS))
    for i in range(1, len(clips)):
        prev_end = clips[i - 1]["startFrame"] + clips[i - 1]["durationInFrames"]
        clips[i]["startFrame"] = prev_end
        clips[i]["durationInFrames"] = max(1, int(round(clips[i]["end"] * FPS)) - prev_end)

    total_dur = round(t_cursor + 0.25, 2)
    total_frames = clips[-1]["startFrame"] + clips[-1]["durationInFrames"]

    # Map clip timings for synced Toy-Prop SFX
    by_id = {c["id"]: c for c in clips}
    a5a = by_id["A5a_candados"]
    d1_f = max(4, round(a5a["durationInFrames"] * 0.18))
    d2_f = max(d1_f + 12, round(a5a["durationInFrames"] * 0.50))
    d3_f = max(d2_f + 12, round(a5a["durationInFrames"] * 0.78))
    check_delays = [d1_f, d2_f, d3_f]

    # Build synced SFX WAV
    n_total = int((total_dur + 0.5) * SR)
    buf_l = [0.0] * n_total
    buf_r = [0.0] * n_total

    sfx.add_crack_impact(buf_l, buf_r, by_id["A1_hook"]["start"] + 1.10)
    sfx.add_siren_pulse(buf_l, buf_r, by_id["A1_hook"]["start"] + 2.00)
    sfx.add_pop_whoosh(buf_l, buf_r, by_id["A2_bucle"]["start"], pitch_scale=1.0)
    sfx.add_pop_whoosh(buf_l, buf_r, by_id["A3a_grafica"]["start"], pitch_scale=1.05)
    sfx.add_gauge_sweep(buf_l, buf_r, by_id["A3b_gauge"]["start"] + 0.15)
    sfx.add_siren_pulse(buf_l, buf_r, by_id["A3b_gauge"]["start"] + 0.75)
    sfx.add_doors_chime(buf_l, buf_r, by_id["A4_puertas"]["start"])
    sfx.add_pop_whoosh(buf_l, buf_r, a5a["start"], pitch_scale=1.15)
    sfx.add_check_ding(buf_l, buf_r, (a5a["startFrame"] + d1_f) / FPS, 1046.5)  # C6
    sfx.add_check_ding(buf_l, buf_r, (a5a["startFrame"] + d2_f) / FPS, 1318.5)  # E6
    sfx.add_check_ding(buf_l, buf_r, (a5a["startFrame"] + d3_f) / FPS, 1568.0)  # G6
    sfx.add_pop_whoosh(buf_l, buf_r, by_id["A5b_cta"]["start"], pitch_scale=1.2)

    sfx_wav = AUDIO_DIR / "bf01_sfx.wav"
    peak = max(0.001, max(max(abs(x) for x in buf_l), max(abs(x) for x in buf_r)))
    gain = min(1.0, 0.75 / peak)
    raw = bytearray()
    for lv, rv in zip(buf_l, buf_r):
        il = max(-32767, min(32767, int(lv * gain * 32767.0)))
        ir = max(-32767, min(32767, int(rv * gain * 32767.0)))
        raw.extend(struct.pack("<hh", il, ir))
    with wave.open(str(sfx_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(bytes(raw))

    bed_wav = AUDIO_DIR / "bf01_bed.wav"
    build_ambient_bed(total_dur, bed_wav)

    inputs = [
        "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo:d={total_dur:.3f}",
        "-i", str(sfx_wav),
        "-i", str(bed_wav),
    ]
    filters = ["[1:a]volume=0.42[sfx]", "[2:a]volume=0.20[bed]"]
    mix_labels = ["[0:a]", "[sfx]", "[bed]"]
    for idx, cl in enumerate(clips, start=3):
        inputs.extend(["-i", str(ROOT / cl["mp3"])])
        ms = int(cl["start"] * 1000)
        lbl = f"[v{idx}]"
        filters.append(f"[{idx}:a]adelay={ms}|{ms},volume=1.32{lbl}")
        mix_labels.append(lbl)

    fc = ";".join(filters) + ";" + "".join(mix_labels) + f"amix=inputs={len(mix_labels)}:duration=longest:normalize=0,alimiter=limit=0.95[aout]"
    subprocess.run(
        [FFMPEG, "-y", *inputs, "-filter_complex", fc, "-map", "[aout]", "-t", f"{total_dur:.3f}", "-ar", str(SR), "-ac", "2", str(MASTER_WAV)],
        check=True,
        capture_output=True,
    )

    after = check_elevenlabs_quota(api_key)
    print("ElevenLabs quota AFTER:", after)

    payload = {
        "total_duration": total_dur,
        "total_frames": total_frames,
        "total_chars": total_chars,
        "check_delays": check_delays,
        "master_wav": str(MASTER_WAV.relative_to(ROOT)),
        "clips": clips,
        "elevenlabs_quota_before": before,
        "elevenlabs_quota_after": after,
    }
    TIMINGS_ARCHIVE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    TIMINGS_STUDIO.parent.mkdir(parents=True, exist_ok=True)
    TIMINGS_STUDIO.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Master WAV: {MASTER_WAV} ({total_dur:.2f}s / {total_frames} frames)")
    print(f"✅ Timings: {TIMINGS_STUDIO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
