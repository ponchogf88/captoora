#!/usr/bin/env python3
"""
Genera la versión extendida (>60s para OpusClip + Captions) de EP01 (GTA 6 Récord $3B + Gemini 4 Neon)
con eleven_v3 (Antonio + Liza) y CERO traslapes garantizados.
"""
import argparse
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
OUT_AUDIO = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP01_EXT"
BEATS_JSON = ROOT / "proyectos/waters-3d-studio/src/episodeBeats.json"
FFMPEG = "/Users/imac/.local/bin/ffmpeg"
FFPROBE = "/Users/imac/.local/bin/ffprobe"
FPS = 30

CHUY_ID = "htFfPSZGJwjBv1CL0aMD"  # Antonio
AGY_ID = "kl7d390GatBPfqhRTyAl"   # Liza


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
            "stability": 0.32,
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
                    "stability": 0.32,
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
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True,
    ).strip()
    return float(out)


EP01_EXT_LINES = [
    {
        "speaker": "chuy",
        "text": "[excited] Waters gamers!",
        "language_code": "en",
        "kind": "clip",
        "videoFile": "chuy_01_susto_alerta.mp4",
        "topTag": "🚨 ¡WATERS GAMERS!",
        "accentColor": "#FF4D4D",
        "zoomStart": 1.0,
        "zoomEnd": 1.12,
        "shakeIntro": True,
    },
    {
        "speaker": "agy",
        "text": "[serious] ¡Aguas con el lanzamiento de GTA seis hoy! Nueve punto ocho millones de vistas en horas.",
        "kind": "clip_plus_broll",
        "videoFile": "agy_01_solo_explicando.mp4",
        "topTag": "🤖 AGY · ALERTA GTA 6",
        "brollTopTag": "🎮 LANZAMIENTO VIRAL",
        "monitorTitle": "TRENDING · X / TIKTOK",
        "headline": "GTA 6: 9.8M VISTAS",
        "lines": ["> 9.8 millones de vistas en horas", "> tráfico masivo buscando el juego", "! EL BLANCO #1 DE HACKERS HOY"],
        "accentColor": "#38BDF8",
    },
    {
        "speaker": "chuy",
        "text": "[surprised] ¿Nueve punto ocho millones?! ¡Escuché que rompió todos los récords!",
        "kind": "clip",
        "videoFile": "chuy_04_escucha_atento.mp4",
        "topTag": "💬 CHUY × AGY",
        "accentColor": "#38BDF8",
        "zoomStart": 1.0,
        "zoomEnd": 1.08,
    },
    {
        "speaker": "agy",
        "text": "[excited] ¡Total! Más de mil millones de dólares en pura preventa... y estiman tres mil millones antes de fin de año. ¡Ni una película ni una serie había logrado eso!",
        "kind": "clip_plus_broll",
        "videoFile": "agy_01_solo_explicando.mp4",
        "topTag": "💰 RÉCORD HISTÓRICO",
        "brollTopTag": "📈 CIFRA RÉCORD MUNDIAL",
        "monitorTitle": "MARKET DATA · GTA 6",
        "headline": "$3,000M USD ESTIMADOS",
        "lines": ["> +$1,000M USD en pura preventa", "> $3,000M USD antes de fin de año", "★ SUPERÓ A CINE, SERIES Y JUEGOS"],
        "accentColor": "#DFB15B",
    },
    {
        "speaker": "agy",
        "text": "[whispering] Y justo donde hay tres mil millones de dólares... hoy hackers usan Claude para hacer Vibe Hacking e ingeniería inversa.",
        "kind": "broll",
        "topTag": "⚠️ VIBE HACKING + IA",
        "monitorTitle": "ANTHROPIC · CLAUDE TERMINAL",
        "headline": "INGENIERÍA INVERSA IA",
        "lines": ["$ vibe-hacking --target=gta6-hype", "> generando phishing + cracks falsos", "! VELOCIDAD 10X CON IA"],
        "accentColor": "#FF4D4D",
    },
    {
        "speaker": "chuy",
        "text": "[nervous] ¿O sea que si bajo un link o un crack falso... pierdo mi cuenta?!",
        "kind": "clip",
        "videoFile": "chuy_02_angustia_sudor.mp4",
        "topTag": "😰 ¿PIERDO MI CUENTA?",
        "accentColor": "#FF4D4D",
        "zoomStart": 1.0,
        "zoomEnd": 1.1,
    },
    {
        "speaker": "agy",
        "text": "[serious] ¡Exacto! Traen Infostealers que roban tus tarjetas y tu cuenta de PlayStation, Xbox o Steam en segundos.",
        "kind": "broll",
        "topTag": "☠️ TRAMPA INFOSTEALER",
        "monitorTitle": "SECURITY ALERT · MALWARE",
        "headline": "ROBO EN SEGUNDOS",
        "lines": ["[!] Crack falso ➔ Infostealer activo", "[!] Extrayendo tarjetas y tokens...", "[X] CUENTA PSN / XBOX / STEAM ROBADA"],
        "accentColor": "#FF4D4D",
    },
    {
        "speaker": "chuy",
        "text": "[gasps] ¡No manches! ¿Y cómo blindo mis cuentas antes de regarla?",
        "kind": "clip",
        "videoFile": "chuy_03_sorpresa_silla.mp4",
        "topTag": "😱 ¡NO MANCHES!",
        "accentColor": "#DFB15B",
        "zoomStart": 1.0,
        "zoomEnd": 1.18,
    },
    {
        "speaker": "agy",
        "text": "[excited] ¡Con Gemini cuatro Neon en Antigravity! Analiza links sospechosos, blinda contraseñas y activa dos FA al instante.",
        "kind": "broll",
        "topTag": "🛡️ GEMINI 4 NEON",
        "monitorTitle": "ANTIGRAVITY · SHIELD ON",
        "headline": "BLINDAJE CON NEON",
        "lines": ["✓ Analizando links sospechosos", "✓ Verificando 2FA + contraseñas", "✓ CUENTAS GAMER PROTEGIDAS"],
        "accentColor": "#DFB15B",
    },
    {
        "speaker": "chuy",
        "text": "[sighs] [laughs] ¡Uf, qué alivio! ¡Ya quedó blindada al cien!",
        "kind": "clip",
        "videoFile": "chuy_06_feliz_celebrando.mp4",
        "topTag": "🎉 ¡CUENTA BLINDADA!",
        "accentColor": "#22C55E",
        "zoomStart": 1.0,
        "zoomEnd": 1.08,
    },
    {
        "speaker": "agy",
        "text": "[excited] ¡Comenta Neon y te mando la guía gratis para proteger tus cuentas hoy!",
        "kind": "clip_plus_broll",
        "videoFile": "agy_03_solo_feliz_guino.mp4",
        "topTag": "🚀 AGY · ANTIGRAVITY",
        "brollTopTag": "📩 GUÍA GRATIS",
        "monitorTitle": "CAPTOORA × ANTIGRAVITY",
        "headline": "PROTEGE TU CUENTA HOY",
        "lines": ["> Checklist anti-infostealers", "> Prompts de verificación en Neon"],
        "ctaText": "COMENTA: NEON 🚀",
        "accentColor": "#DFB15B",
    },
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-beats", action="store_true", help="Conserva timings exactos de episodeBeats.json[EP01_EXT]")
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        print("ERROR: Falta ELEVENLABS_API_KEY", file=sys.stderr)
        return 1

    OUT_AUDIO.mkdir(parents=True, exist_ok=True)
    fixed_starts = [0.00, 2.3333, 9.3333, 14.0667, 26.80, 36.7333, 41.80, 51.10, 55.60, 64.50, 69.9667]
    beats_out = []
    audio_events = []
    current_frame = 0

    for idx, item in enumerate(EP01_EXT_LINES, start=1):
        mp3_path = OUT_AUDIO / f"{idx:02d}_{item['speaker']}.mp3"
        if not mp3_path.exists():
            vid = CHUY_ID if item["speaker"] == "chuy" else AGY_ID
            lang = item.get("language_code")
            print(f"[EP01_EXT] TTS {idx:02d} ({item['speaker']}, lang={lang}): {item['text']}")
            tts_to_mp3(item["text"], vid, mp3_path, api_key, language_code=lang)

        dur = probe_duration(mp3_path)
        start_sec = fixed_starts[idx - 1] if args.keep_beats else (current_frame / FPS)
        audio_events.append((start_sec + 0.08, mp3_path))

        # CERO traslapes: el beat siempre dura al menos dur + 0.25s
        needed_frames = max(48, math.ceil((dur + 0.25) * FPS))

        if item["kind"] == "clip":
            if needed_frames <= 116:
                beats_out.append({
                    "kind": "clip",
                    "durationInFrames": needed_frames,
                    "videoFile": item["videoFile"],
                    "topTag": item["topTag"],
                    "accentColor": item["accentColor"],
                    "zoomStart": item.get("zoomStart", 1.0),
                    "zoomEnd": item.get("zoomEnd", 1.09),
                    "shakeIntro": item.get("shakeIntro", False),
                })
                current_frame += needed_frames
            else:
                # Si excede 116f (~3.86s), dividir entre 2 cortes limpios del mismo clip para cero traslape
                f1 = 105
                f2 = needed_frames - f1
                beats_out.append({
                    "kind": "clip",
                    "durationInFrames": f1,
                    "videoFile": item["videoFile"],
                    "topTag": item["topTag"],
                    "accentColor": item["accentColor"],
                    "zoomStart": item.get("zoomStart", 1.0),
                    "zoomEnd": 1.08,
                    "shakeIntro": item.get("shakeIntro", False),
                })
                beats_out.append({
                    "kind": "clip",
                    "durationInFrames": f2,
                    "videoFile": item["videoFile"],
                    "topTag": item["topTag"],
                    "accentColor": item["accentColor"],
                    "zoomStart": 1.12,
                    "zoomEnd": 1.20,
                    "shakeIntro": False,
                })
                current_frame += needed_frames

        elif item["kind"] == "broll":
            beats_out.append({
                "kind": "broll",
                "durationInFrames": needed_frames,
                "topTag": item["topTag"],
                "monitorTitle": item["monitorTitle"],
                "headline": item["headline"],
                "lines": item["lines"],
                "ctaText": item.get("ctaText"),
                "accentColor": item["accentColor"],
            })
            current_frame += needed_frames

        elif item["kind"] == "clip_plus_broll":
            clip_frames = min(105, max(54, needed_frames // 2))
            broll_frames = max(60, needed_frames - clip_frames)
            beats_out.append({
                "kind": "clip",
                "durationInFrames": clip_frames,
                "videoFile": item["videoFile"],
                "topTag": item["topTag"],
                "accentColor": item["accentColor"],
                "zoomStart": 1.0,
                "zoomEnd": 1.08,
            })
            beats_out.append({
                "kind": "broll",
                "durationInFrames": broll_frames,
                "topTag": item["brollTopTag"],
                "monitorTitle": item["monitorTitle"],
                "headline": item["headline"],
                "lines": item["lines"],
                "ctaText": item.get("ctaText"),
                "accentColor": item["accentColor"],
            })
            current_frame += clip_frames + broll_frames

    # Asegurar >= 62s para que OpusClip acepte sin problema (> 1 minuto)
    if args.keep_beats:
        existing = json.loads(BEATS_JSON.read_text(encoding="utf-8"))
        total_sec = sum(b["durationInFrames"] for b in existing["EP01_EXT"]) / FPS
        current_frame = int(round(total_sec * FPS))
    elif current_frame < 62 * FPS:
        extra = 62 * FPS - current_frame
        beats_out[-1]["durationInFrames"] += extra
        current_frame += extra
        total_sec = current_frame / FPS
    else:
        total_sec = current_frame / FPS
    master_wav = OUT_AUDIO / "EP01_EXT_master.wav"
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

    if not args.keep_beats:
        existing = json.loads(BEATS_JSON.read_text(encoding="utf-8")) if BEATS_JSON.exists() else {}
        existing["EP01_EXT"] = beats_out
        BEATS_JSON.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ [EP01_EXT] Total frames={current_frame} ({total_sec:.2f}s) | WAV={master_wav}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
