#!/usr/bin/env python3
"""
Genera y mezcla el audio maestro para el Short HRM-01 ("¿Qué es un modelo ABLITERATED?")
en formato Black Canvas Coloreado, reutilizando waters_audio_engine.py y caché MP3 por bloque.
"""
import json
import math
import random
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

WORK_DIR = ROOT / "proyectos/waters-serie/biblioteca_hermes_abliterated"
AUDIO_DIR = WORK_DIR / "audio"
CACHE_DIR = AUDIO_DIR / "cache/hrm01"
MASTER_WAV = AUDIO_DIR / "hrm01_master.wav"
TIMINGS_JSON = AUDIO_DIR / "hrm01_timings.json"

FFMPEG = engine.FFMPEG
FFPROBE = engine.FFPROBE
SR = engine.SR

HRM01_SCRIPT: List[Dict[str, Any]] = [
    {
        "id": "B1_hook",
        "chapter": "01 · Hook",
        "pause_after": 0.25,
        "text": (
            "¿Has visto videos presumiendo modelos abliterated cien por ciento sin censura? "
            "Te explico en cuarenta segundos qué les hacen por dentro y dónde está el peligro real."
        ),
    },
    {
        "id": "B2_vector",
        "chapter": "02 · Vector de Rechazo",
        "pause_after": 0.25,
        "text": (
            "Cuando entrenan una inteligencia artificial normal, queda grabada una ruta matemática "
            "llamada vector de rechazo. Cuando detecta algo riesgoso, dispara el clásico: lo siento, no puedo ayudarte. "
            "La técnica abliteration mide esa flecha exacta y la borra de los pesos sin reentrenar toda la red."
        ),
    },
    {
        "id": "B3_realidad",
        "chapter": "03 · Realidad",
        "pause_after": 0.25,
        "text": (
            "Pero ojo con la realidad: el modelo no se vuelve más inteligente ni mágico. "
            "Conserva su conocimiento, pero pierde el freno de emergencia. "
            "Sirve para investigar filtros en laboratorios controlados, pero también baja la barrera frente a código dañino."
        ),
    },
    {
        "id": "B4_candados",
        "chapter": "04 · Tres Candados",
        "pause_after": 0.25,
        "text": (
            "Regla de oro Captoora: si conectas un agente autónomo con acceso a terminal a un modelo sin frenos "
            "y sin aislamiento, un solo correo con prompt injection puede darle órdenes que ya nadie detiene. "
            "Por eso exige tres candados: Docker Sandbox, firewall cerrado y aprobación humana."
        ),
    },
    {
        "id": "B5_cta",
        "chapter": "05 · CTA HERMES",
        "pause_after": 0.35,
        "text": (
            "¿Quieres la guía defensiva de tres candados antes de correr agentes locales? "
            "Comenta HERMES."
        ),
    },
]


def build_ambient_bed(total_sec: float, out_wav: Path, seed: int = 88) -> None:
    """Cama oscura investigativa determinista a bajo nivel (-24 dB) para no competir con la voz."""
    n_total = int((total_sec + 0.3) * SR)
    freqs = (110.0, 164.81, 261.63, 392.0)
    buf = bytearray()
    for i in range(n_total):
        t = i / SR
        env_fade = min(1.0, t / 0.8) * min(1.0, max(0.0, (total_sec - t) / 0.9))
        pulse = 0.72 + 0.28 * math.sin(2.0 * math.pi * 0.25 * t)
        val = 0.0
        for idx, f in enumerate(freqs):
            val += math.sin(2.0 * math.pi * f * t + idx * 0.6) * (0.28 / (idx + 1))
        sub = t % 1.0
        tick = math.sin(2.0 * math.pi * 880.0 * sub) * math.exp(-sub * 85.0) * 0.045
        sample = (val * 0.14 * pulse + tick) * env_fade
        s_i = max(-32767, min(32767, int(sample * 32767.0)))
        buf.extend(struct.pack("<hh", s_i, s_i))
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(bytes(buf))


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


def mix_hrm01(api_key: str, seed: int = 612) -> Dict[str, Any]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    clips: List[Dict[str, Any]] = []
    t_cursor = 0.15
    total_chars = 0

    for item in HRM01_SCRIPT:
        mp3_path = CACHE_DIR / f"{item['id']}.mp3"
        chars = len(item["text"])
        total_chars += chars
        if not mp3_path.exists():
            if not api_key:
                raise RuntimeError(f"Falta ELEVENLABS_API_KEY para sintetizar {item['id']}")
            print(f"[hrm01] TTS {item['id']} ({chars} chars)...")
            engine.tts_to_mp3(
                item["text"],
                engine.TONY_ID,
                mp3_path,
                api_key,
                stability=0.34,
                language_code="es",
            )
        else:
            print(f"[hrm01] Cache HIT {item['id']} ({chars} chars)")

        dur = engine.probe_duration(mp3_path)
        pause = float(item.get("pause_after", 0.25))
        start_s = round(t_cursor, 3)
        end_s = round(t_cursor + dur + pause, 3)
        clips.append(
            {
                "id": item["id"],
                "chapter": item.get("chapter", item["id"]),
                "start": start_s,
                "voice_end": round(t_cursor + dur, 3),
                "end": end_s,
                "duration": round(end_s - start_s, 3),
                "voice_dur": round(dur, 3),
                "chars": chars,
                "mp3": str(mp3_path.relative_to(ROOT)),
            }
        )
        t_cursor = end_s

    total_dur = round(t_cursor + 0.35, 2)

    n_total = int((total_dur + 0.5) * SR)
    buf_l = [0.0] * n_total
    buf_r = [0.0] * n_total
    rng = random.Random(seed)

    for ci, cl in enumerate(clips):
        st = cl["start"]
        engine.add_ui_pop(
            buf_l,
            buf_r,
            max(0.02, st - 0.04),
            f_start=260.0 + (ci % 4) * 35.0,
            f_end=780.0 + (ci % 4) * 50.0,
            amp=0.30,
            with_sparkle=(ci == 0 or ci == len(clips) - 1),
        )
        for ki in range(6):
            tk = st + 0.06 + ki * 0.055 + rng.uniform(-0.005, 0.005)
            engine.add_mech_keystroke(
                buf_l,
                buf_r,
                tk,
                rng,
                is_enter=(ki == 5),
                pan=((ki % 5) - 2) * 0.14,
                amp=0.18,
            )

    sfx_wav = AUDIO_DIR / "hrm01_sfx.wav"
    peak = max(0.001, max(max(abs(x) for x in buf_l), max(abs(x) for x in buf_r)))
    gain = min(1.0, 0.72 / peak)
    with wave.open(str(sfx_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        raw = bytearray()
        for lv, rv in zip(buf_l, buf_r):
            raw.extend(
                struct.pack(
                    "<hh",
                    max(-32767, min(32767, int(lv * gain * 32767))),
                    max(-32767, min(32767, int(rv * gain * 32767))),
                )
            )
        wf.writeframes(bytes(raw))

    bed_wav = AUDIO_DIR / "hrm01_bed.wav"
    build_ambient_bed(total_dur, bed_wav, seed=seed + 11)

    inputs = [
        "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo:d={total_dur:.3f}",
        "-i", str(sfx_wav),
        "-i", str(bed_wav),
    ]
    filters = ["[1:a]volume=0.58[sfx]", "[2:a]volume=0.22[bed]"]
    mix_labels = ["[0:a]", "[sfx]", "[bed]"]
    for idx, cl in enumerate(clips, start=3):
        inputs.extend(["-i", str(ROOT / cl["mp3"])])
        ms = int(cl["start"] * 1000)
        lbl = f"[v{idx}]"
        filters.append(f"[{idx}:a]adelay={ms}|{ms},volume=1.28{lbl}")
        mix_labels.append(lbl)

    fc = (
        ";".join(filters)
        + ";"
        + "".join(mix_labels)
        + f"amix=inputs={len(mix_labels)}:duration=longest:normalize=0,alimiter=limit=0.92[aout]"
    )
    subprocess.run(
        [
            FFMPEG,
            "-y",
            *inputs,
            "-filter_complex",
            fc,
            "-map",
            "[aout]",
            "-t",
            f"{total_dur:.3f}",
            "-ar",
            str(SR),
            "-ac",
            "2",
            str(MASTER_WAV),
        ],
        check=True,
        capture_output=True,
    )

    probe_out = subprocess.check_output(
        [
            FFPROBE,
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_name,sample_rate",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(MASTER_WAV),
        ],
        text=True,
    ).strip().replace("\n", " | ")
    print(f"OK {MASTER_WAV.name} ({MASTER_WAV.stat().st_size} B) -> {probe_out}")

    return {
        "total_duration": total_dur,
        "total_chars": total_chars,
        "master_wav": str(MASTER_WAV.relative_to(ROOT)),
        "clips": clips,
    }


def main() -> int:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    api_key = engine.load_api_key()
    before = check_elevenlabs_quota(api_key) if api_key else {"error": "missing_key"}
    print("ElevenLabs quota BEFORE:", before)
    if not api_key:
        print("ERROR: missing ELEVENLABS_API_KEY", file=sys.stderr)
        return 1

    meta = mix_hrm01(api_key=api_key, seed=612)
    after = check_elevenlabs_quota(api_key)
    print("ElevenLabs quota AFTER:", after)

    payload = {
        "hrm01": meta,
        "elevenlabs_quota_before": before,
        "elevenlabs_quota_after": after,
    }
    TIMINGS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote timings -> {TIMINGS_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
