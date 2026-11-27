#!/usr/bin/env python3
"""
Genera y mezcla el audio maestro (~25s) para Captoora Studio CPT-REEL-01:
"¿Por qué tu foto se ve plana? (Antes -> Después de luz en estudio)"
Aplica gancho auditivo desde t=0.02s (REF-15) con waters_audio_engine.py.
"""
import json
import math
import random
import struct
import subprocess
import sys
import time
import urllib.request
import wave
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
SCRIPTS_DIR = ROOT / "proyectos/waters-serie/scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import waters_audio_engine as engine  # noqa: E402

WORK_DIR = ROOT / "proyectos/captoora-reels/reel_01_antes_despues_luz"
AUDIO_DIR = WORK_DIR / "audio"
CACHE_DIR = AUDIO_DIR / "cache/cpt01"
MASTER_WAV = AUDIO_DIR / "cpt01_master.wav"
TIMINGS_JSON = AUDIO_DIR / "cpt01_timings.json"

FFMPEG = engine.FFMPEG
FFPROBE = engine.FFPROBE
SR = engine.SR

CPT01_SCRIPT: List[Dict[str, Any]] = [
    {
        "id": "C1_hook",
        "chapter": "01 · Hook Visual + Auditivo",
        "pause_after": 0.18,
        "text": (
            "¿Ves por qué una foto de celular se ve plana? "
            "No es tu cámara ni el modelo: es controlar la luz antes de disparar."
        ),
    },
    {
        "id": "C2_revelado",
        "chapter": "02 · Cortina Antes -> Después",
        "pause_after": 0.18,
        "text": (
            "Mira cómo cambia el mismo retrato cuando diriges sombras, contraste y dirección de luz en el set. "
            "Pasa de foto común a retrato de portada."
        ),
    },
    {
        "id": "C3_estudio",
        "chapter": "03 · Estudio Colinas",
        "pause_after": 0.18,
        "text": (
            "En Captoora Studio, en Colinas de San Jerónimo, Monterrey, "
            "tienes el estudio listo con softbox, ciclorama y guía."
        ),
    },
    {
        "id": "C4_cta",
        "chapter": "04 · Popup Seguir + SESIÓN",
        "pause_after": 0.45,
        "text": (
            "¿Quieres tu sesión o rentar el set? Comenta SESIÓN y síguenos en Captoora Studio."
        ),
    },
]


def build_warm_bed(total_sec: float, out_wav: Path, seed: int = 314) -> None:
    """Cama cálida de estudio determinista a bajo nivel."""
    n_total = int((total_sec + 0.3) * SR)
    freqs = (130.81, 196.00, 261.63, 329.63)  # C3, G3, C4, E4 suave
    buf = bytearray()
    for i in range(n_total):
        t = i / SR
        env_fade = min(1.0, t / 0.5) * min(1.0, max(0.0, (total_sec - t) / 0.7))
        pulse = 0.78 + 0.22 * math.sin(2.0 * math.pi * 0.4 * t)
        val = 0.0
        for idx, f in enumerate(freqs):
            val += math.sin(2.0 * math.pi * f * t + idx * 0.5) * (0.26 / (idx + 1))
        sample = (val * 0.14 * pulse) * env_fade
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


def mix_cpt01(api_key: str, seed: int = 314) -> Dict[str, Any]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    clips: List[Dict[str, Any]] = []
    t_cursor = 0.18
    total_chars = 0

    for item in CPT01_SCRIPT:
        mp3_path = CACHE_DIR / f"{item['id']}.mp3"
        chars = len(item["text"])
        total_chars += chars
        if not mp3_path.exists():
            if not api_key:
                raise RuntimeError(f"Falta ELEVENLABS_API_KEY para sintetizar {item['id']}")
            print(f"[cpt01] TTS {item['id']} ({chars} chars)...")
            engine.tts_to_mp3(
                item["text"],
                engine.TONY_ID,
                mp3_path,
                api_key,
                stability=0.34,
                language_code="es",
            )
        else:
            print(f"[cpt01] Cache HIT {item['id']} ({chars} chars)")

        dur = engine.probe_duration(mp3_path)
        pause = float(item.get("pause_after", 0.18))
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

    # Gancho auditivo inmediato en t=0.02s (REF-15)
    engine.add_ui_pop(buf_l, buf_r, 0.02, f_start=230.0, f_end=960.0, amp=0.45, with_sparkle=True)
    for ki in range(4):
        engine.add_mech_keystroke(buf_l, buf_r, 0.06 + ki * 0.045, rng, is_enter=(ki == 3), amp=0.22)

    for ci, cl in enumerate(clips[1:], start=1):
        st = cl["start"]
        engine.add_ui_pop(
            buf_l,
            buf_r,
            max(0.05, st - 0.04),
            f_start=280.0 + ci * 40.0,
            f_end=840.0 + ci * 50.0,
            amp=0.32,
            with_sparkle=(ci == len(clips) - 1),
        )

    sfx_wav = AUDIO_DIR / "cpt01_sfx.wav"
    peak = max(0.001, max(max(abs(x) for x in buf_l), max(abs(x) for x in buf_r)))
    gain = min(1.0, 0.74 / peak)
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

    bed_wav = AUDIO_DIR / "cpt01_bed.wav"
    build_warm_bed(total_dur, bed_wav, seed=seed + 7)

    inputs = [
        "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo:d={total_dur:.3f}",
        "-i", str(sfx_wav),
        "-i", str(bed_wav),
    ]
    filters = ["[1:a]volume=0.62[sfx]", "[2:a]volume=0.18[bed]"]
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

    meta = mix_cpt01(api_key=api_key, seed=314)
    time.sleep(2.5)
    after = check_elevenlabs_quota(api_key)
    print("ElevenLabs quota AFTER:", after)

    payload = {
        "cpt01": meta,
        "elevenlabs_quota_before": before,
        "elevenlabs_quota_after": after,
    }
    TIMINGS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote timings -> {TIMINGS_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
