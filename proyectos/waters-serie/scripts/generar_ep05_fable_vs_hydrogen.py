#!/usr/bin/env python3
"""
Genera EP05 ("Fable 5.2 ($19 / 45 min) vs Gemini 4 Hydrogen ($1.50 o Gratis / 12 min)
+ Clon GTA 6 en 10 min + Modo IA Ilimitado") con ElevenLabs eleven_v3,
separando "¡Waters!" con language_code="en" al inicio y cierre (sin acento pocho).
"""
import json
import math
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
ENV_FILE = ROOT / ".env"
OUT_AUDIO = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP05_FABLE_HYDROGEN"
BEATS_JSON = ROOT / "proyectos/waters-3d-studio/src/episodeBeats.json"
FFMPEG = "/Users/imac/.local/bin/ffmpeg"
FFPROBE = "/Users/imac/.local/bin/ffprobe"
FPS = 30

TONY_ID = "htFfPSZGJwjBv1CL0aMD"  # Antonio - Confident, Gentle and Clear
AGY_ID = "kl7d390GatBPfqhRTyAl"   # Liza - Natural Mexican Creator


def load_api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key and ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ELEVENLABS_API_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val.startswith("sk_"):
                    return val
    return key


def tts_to_mp3(
    text: str,
    voice_id: str,
    out_path: Path,
    api_key: str,
    stability: float = 0.32,
    language_code: Optional[str] = None,
) -> None:
    def _post(body_dict: dict) -> bytes:
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            data=json.dumps(body_dict).encode("utf-8"),
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()

    body = {
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": 0.78,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }
    if language_code:
        body["language_code"] = language_code

    try:
        out_path.write_bytes(_post(body))
    except urllib.error.HTTPError as err:
        if language_code and err.code in (400, 422):
            clean_text = re.sub(r"\[[^\]]+\]\s*", "", text).strip()
            fallback_body = {
                "text": clean_text,
                "model_id": "eleven_turbo_v2_5",
                "language_code": language_code,
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": 0.78,
                    "style": 0.0,
                    "use_speaker_boost": True,
                },
            }
            out_path.write_bytes(_post(fallback_body))
        else:
            raise


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            FFPROBE,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


EP05_LINES = [
    {
        "speaker": "tony",
        "text": "[serious] Waters!",
        "language_code": "en",
        "stability": 0.35,
        "topTag": "🚨 ¡WATERS · FABLE 5 vs GEMINI 4!",
        "accentColor": "#FF3B3B",
        "expression": "shock",
        "cardType": "alert_intro",
        "heroTitle": "FABLE 5.2 vs GEMINI 4",
        "heroSubtitle": "¿$19 USD ó $1.50 USD / GRATIS?",
    },
    {
        "speaker": "tony",
        "text": "[serious] ¿Qué, vas a seguir quemando diecinueve dólares y cuarenta y cinco minutos en Fable cinco punto dos para hacer una sola animación?!",
        "topTag": "💸 $19 USD · 45 MINUTOS",
        "accentColor": "#FF4D4D",
        "expression": "skeptic",
        "cardType": "vs_duel",
    },
    {
        "speaker": "agy",
        "text": "[excited] ¡Para nada! Google acaba de soltar Gemini cuatro Hydrogen: hizo esa misma animación en doce minutos y por un dólar cincuenta... ¡o totalmente gratis!",
        "topTag": "⚡ GEMINI 4 HYDROGEN · 12 MIN",
        "accentColor": "#00F5D4",
        "expression": "star_eyes",
        "cardType": "vs_duel",
    },
    {
        "speaker": "tony",
        "text": "[surprised] ¿Cómo que diez veces más barato?! ¡Enséñame los números reales de la API!",
        "topTag": "📊 PRECIO REAL POR 1M TOKENS",
        "accentColor": "#00F5D4",
        "expression": "shock",
        "cardType": "vs_duel",
    },
    {
        "speaker": "agy",
        "text": "[serious] Mira: Fable cinco cobra diez dólares de entrada y cincuenta de salida. Hydrogen cobra uno cincuenta y siete cincuenta... ¡y en Terminal Bench saltó de dieciocho punto dos a cincuenta y siete por ciento, superando a Fable y a GPT Astra seis!",
        "topTag": "🏆 TERMINAL BENCH 4.1 · TOP #5",
        "accentColor": "#38BDF8",
        "expression": "star_eyes",
        "cardType": "bench_race",
    },
    {
        "speaker": "tony",
        "text": "[excited] ¡Aguas! ¿Y sí es cierto que le armó un clon jugable de GTA seis en tres D en solo diez minutos?!",
        "topTag": "🎮 CLON 3D GTA 6 · 10 MIN",
        "accentColor": "#DFB15B",
        "expression": "shock",
        "cardType": "gta6_build",
    },
    {
        "speaker": "agy",
        "text": "[excited] ¡En diez minutos con motos, aviones, barcos y cámara en primera persona! Pero ojo: no uses el Gemini normal. Métete a Google AI Studio y activa razonamiento Extra Alto en modo MAX.",
        "topTag": "⚙️ TRUCO: AI STUDIO · MODO MAX",
        "accentColor": "#DFB15B",
        "expression": "laser_focus",
        "cardType": "gta6_build",
    },
    {
        "speaker": "agy",
        "text": "[whispering] Y el secreto para no quedarte en cero por ciento de cuota: usa la pestaña Modo IA directo en google punto com. ¡Ya corre Gemini cuatro Hydrogen ilimitado, sin límite de cinco horas ni semanal!",
        "topTag": "♾️ MODO IA GOOGLE · SIN LÍMITES",
        "accentColor": "#22C55E",
        "expression": "star_eyes",
        "cardType": "three_secrets",
    },
    {
        "speaker": "agy",
        "text": "[excited] Comenta HYDROGEN y te mando los tres links y el ID oculto para conectarlo gratis a tus agentes. ¡Toma tus precauciones!",
        "topTag": "🚀 COMENTA: HYDROGEN",
        "accentColor": "#00F5D4",
        "expression": "happy_wink",
        "cardType": "cta_wink",
        "heroTitle": "COMENTA: HYDROGEN 🚀",
        "heroSubtitle": "3 Links + ID Oculto gemini-4-hydrogen",
    },
    {
        "speaker": "tony",
        "text": "[excited] Waters!... Waters!",
        "language_code": "en",
        "stability": 0.35,
        "topTag": "🌊 ¡WATERS!",
        "accentColor": "#00F5D4",
        "expression": "happy_wink",
        "cardType": "cta_wink",
        "heroTitle": "¡WATERS! 🌊🔥",
        "heroSubtitle": "10X Más Barato · 3.75X Más Rápido",
    },
]


def main() -> int:
    api_key = load_api_key()
    if not api_key:
        print("ERROR: Falta ELEVENLABS_API_KEY", file=sys.stderr)
        return 1

    OUT_AUDIO.mkdir(parents=True, exist_ok=True)
    beats_out = []
    audio_events = []
    current_frame = 0

    for idx, item in enumerate(EP05_LINES, start=1):
        mp3_path = OUT_AUDIO / f"{idx:02d}_{item['speaker']}.mp3"
        if not mp3_path.exists():
            vid = TONY_ID if item["speaker"] == "tony" else AGY_ID
            lang = item.get("language_code")
            stab = item.get("stability", 0.32)
            print(f"[EP05] TTS {idx:02d} ({item['speaker']}, lang={lang}): {item['text']}")
            tts_to_mp3(item["text"], vid, mp3_path, api_key, stability=stab, language_code=lang)

        dur = probe_duration(mp3_path)
        start_sec = current_frame / FPS
        audio_events.append((start_sec + 0.08, mp3_path))

        needed_frames = max(54, math.ceil((dur + 0.28) * FPS))
        beat_entry = {
            "durationInFrames": needed_frames,
            "topTag": item["topTag"],
            "accentColor": item["accentColor"],
            "expression": item["expression"],
            "cardType": item["cardType"],
            "speaking": True,
        }
        if "heroTitle" in item:
            beat_entry["heroTitle"] = item["heroTitle"]
        if "heroSubtitle" in item:
            beat_entry["heroSubtitle"] = item["heroSubtitle"]

        beats_out.append(beat_entry)
        current_frame += needed_frames

    if current_frame < 62 * FPS:
        extra = 62 * FPS - current_frame
        beats_out[-2]["durationInFrames"] += extra
        current_frame += extra

    total_sec = current_frame / FPS
    master_wav = OUT_AUDIO / "EP05_master.wav"
    inputs = [
        "-f", "lavfi", "-i", "sine=frequency=110:duration=0.40",
        "-f", "lavfi", "-i", "sine=frequency=880:duration=0.30",
        "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={total_sec:.3f}",
    ]
    filters = [
        "[0:a]afade=t=out:st=0.05:d=0.35,volume=0.45[sfx0]",
        "[1:a]adelay=60|60,afade=t=out:st=0.08:d=0.22,volume=0.20[sfx1]",
    ]
    mix = ["[sfx0]", "[sfx1]", "[2:a]"]
    for i, (st, p) in enumerate(audio_events, start=3):
        inputs.extend(["-i", str(p)])
        ms = int(st * 1000)
        lbl = f"[v{i}]"
        filters.append(f"[{i}:a]adelay={ms}|{ms},volume=1.20{lbl}")
        mix.append(lbl)

    fc = ";".join(filters) + ";" + "".join(mix) + f"amix=inputs={len(mix)}:duration=longest:normalize=0[aout]"
    subprocess.run(
        [FFMPEG, "-y", *inputs, "-filter_complex", fc, "-map", "[aout]", "-ar", "44100", "-ac", "2", str(master_wav)],
        check=True,
    )

    existing = json.loads(BEATS_JSON.read_text(encoding="utf-8")) if BEATS_JSON.exists() else {}
    existing["EP05_FABLE_HYDROGEN"] = beats_out
    BEATS_JSON.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ [EP05_FABLE_HYDROGEN] Total frames={current_frame} ({total_sec:.2f}s) | WAV={master_wav}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
