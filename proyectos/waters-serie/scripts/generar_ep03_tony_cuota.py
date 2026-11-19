#!/usr/bin/env python3
"""
Genera EP03 ("Tony regaña por quemar el 100% de la cuota semanal de IA -> 4 Guardrails FinOps")
con ElevenLabs eleven_v3 (Tony=Antonio, Ingeniero=clon Chuy, Agy=Liza),
separando la firma "¡Guárersss!" en clips de audio independientes para mantener
la pronunciación en inglés ("guarersss") sin traslapes de audio.
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
OUT_AUDIO = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP03_TONY_CUOTA"
BEATS_JSON = ROOT / "proyectos/waters-3d-studio/src/episodeBeats.json"
FFMPEG = "/Users/imac/.local/bin/ffmpeg"
FFPROBE = "/Users/imac/.local/bin/ffprobe"
FPS = 30

TONY_ID = "htFfPSZGJwjBv1CL0aMD"       # Antonio - Confident, Gentle and Clear
INGENIERO_ID = "2GvH1uOsZcLg7MmLn5b2"  # Voz Ingeniero (clon Chuy)
AGY_ID = "kl7d390GatBPfqhRTyAl"        # Liza - Natural Mexican Creator

VOICE_MAP = {
    "tony": TONY_ID,
    "ingeniero": INGENIERO_ID,
    "agy": AGY_ID,
}


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
    model_id: str = "eleven_v3",
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
        "model_id": model_id,
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
            # Fallback para modelos que requieran language_code explícito sin tags [emotion]
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


EP03_LINES = [
    {
        "speaker": "tony",
        "text": "[serious] Waters!",
        "language_code": "en",
        "stability": 0.35,
        "kind": "clip",
        "videoFile": "chuy_01_susto_alerta.mp4",
        "topTag": "🚨 ¡WATERS · CUOTA EN 0%!",
        "accentColor": "#FF4D4D",
        "zoomStart": 1.0,
        "zoomEnd": 1.14,
        "shakeIntro": True,
    },
    {
        "speaker": "tony",
        "text": "[serious] ¿Qué, te vas a acabar la cuota semanal de inteligencia artificial de la empresa sin poner controles ni guardrails?! ¡El tablero está en cero por ciento!",
        "kind": "clip_plus_broll",
        "videoFile": "chuy_04_escucha_atento.mp4",
        "topTag": "😠 TONY · REGAÑO EN VIVO",
        "brollTopTag": "📉 SETTINGS · MODEL CREDITS",
        "monitorTitle": "ANTIGRAVITY · QUOTA 0%",
        "headline": "CUOTA SEMANAL: 0%",
        "screenshotFile": "screenshots/cuota_0_porciento_antigravity.jpg",
        "lines": [
            "> Gemini Models .......... 0% (5d 9h)",
            "> Claude & GPT ........... 0% (6d 3h)",
            "> Gemini 4 Argon ......... 0% (5d 15h)",
            "! PARO TOTAL DE AGENTES",
        ],
        "accentColor": "#FF4D4D",
    },
    {
        "speaker": "ingeniero",
        "text": "[surprised] ¿Por qué en cero, Tony?! ¡Si apenas es miércoles y ya tengo mi cuenta conectada!",
        "kind": "clip",
        "videoFile": "chuy_03_sorpresa_silla.mp4",
        "topTag": "😱 ¿POR QUÉ EN CERO?!",
        "accentColor": "#38BDF8",
        "zoomStart": 1.0,
        "zoomEnd": 1.10,
    },
    {
        "speaker": "tony",
        "text": "[serious] ¡Ay, no puede ser! Mira, te explico: dejaste un solo chat abierto con mil seiscientos catorce pasos... ¡quemaste ciento treinta y cinco millones de tokens haciendo quince videos!",
        "kind": "clip_plus_broll",
        "videoFile": "chuy_01_susto_alerta.mp4",
        "topTag": "📊 AUTOPSIA DEL CHAT",
        "brollTopTag": "🔥 TELEMETRÍA REAL",
        "monitorTitle": "TRANSCRIPT · 82fb8bb2 LOGS",
        "headline": "135.1M TOKENS QUEMADOS",
        "lines": [
            "$ steps: 1,614 | subagentes: 15",
            "> input: 12.8M | output: 710K",
            "> cache_read: 121.6M TOKENS",
            "★ SPRINT: 15 MP4 + 20 FOTOS + 3D",
        ],
        "accentColor": "#DFB15B",
    },
    {
        "speaker": "ingeniero",
        "text": "[nervous] [laughs] ¡Te juro que hasta me dio vergüenza, Tony! Siento que los de Google me están viendo en una pantalla diciendo: ¡mira a este cómo se acabó la cuota! Menos mal que tenía apagado el botón de Enable Overages y la segunda cuenta lista...",
        "kind": "clip",
        "videoFile": "chuy_02_angustia_sudor.mp4",
        "topTag": "😅 PENA CON GOOGLE",
        "accentColor": "#FF4D4D",
        "zoomStart": 1.0,
        "zoomEnd": 1.12,
    },
    {
        "speaker": "tony",
        "text": "[serious] ¡¿Y si estás en una empresa donde no hay segunda cuenta?! ¡Cómo es posible que al propio Legal Engineer se le vote la cuota por descuidado!",
        "kind": "broll",
        "topTag": "⚠️ AUDITORÍA CTO",
        "monitorTitle": "AI FINOPS · RISK ALERT",
        "headline": "¿Y SI NO HAY 2DA CUENTA?",
        "lines": [
            "[!] 1 chat largo re-envía >100K/turno",
            "[!] Sin límites = cuota congelada 6 días",
            "[X] RIESGO OPERATIVO DE EMPRESA",
        ],
        "accentColor": "#FF4D4D",
    },
    {
        "speaker": "agy",
        "text": "[excited] ¡Tranquilo, Tony! Ya activamos los cuatro Guardrails de FinOps: compactar el chat cada doscientos cincuenta pasos te ahorra ciento veintiún millones de tokens de caché.",
        "kind": "clip_plus_broll",
        "videoFile": "agy_01_solo_explicando.mp4",
        "topTag": "🤖 AGY · AI FINOPS",
        "brollTopTag": "🛡️ GUARDRAILS ACTIVOS",
        "monitorTitle": "FINOPS · TOKEN GOVERNANCE",
        "headline": "4 GUARDRAILS ANTI-QUEMA",
        "lines": [
            "1. /compact o Handoff cada 250 pasos",
            "2. Evita re-leer 121.6M de caché",
            "✓ AHORRO ~90% EN CADA MENSAJE",
        ],
        "accentColor": "#22C55E",
    },
    {
        "speaker": "ingeniero",
        "text": "[excited] ¡Y Model Tiering! Usamos el modelo Orchestrator solo para decisiones legales, y Gemini Flash o scripts de Python locales con cero tokens para renders y git push.",
        "kind": "clip_plus_broll",
        "videoFile": "chuy_06_feliz_celebrando.mp4",
        "topTag": "⚡ MODEL TIERING",
        "brollTopTag": "⚙️ OFFLOAD A PYTHON",
        "monitorTitle": "ROUTING · COST CONTROL",
        "headline": "TIERING + PYTHON LOCAL",
        "lines": [
            "3. Orchestrator = diseño y estrategia",
            "   Flash = terminal, git y copias",
            "4. Python / FFmpeg = 0 TOKENS LLM",
        ],
        "accentColor": "#38BDF8",
    },
    {
        "speaker": "tony",
        "text": "[sighs] Más te vale poner ese freno automático al ochenta por ciento... porque el próximo millón de tokens sale de tu quincena.",
        "kind": "clip",
        "videoFile": "chuy_05_cierre_sonrisa.mp4",
        "topTag": "💸 CIRCUIT BREAKER 80%",
        "accentColor": "#DFB15B",
        "zoomStart": 1.0,
        "zoomEnd": 1.09,
    },
    {
        "speaker": "agy",
        "text": "[excited] ¡Comenta FinOps para mandarte el protocolo de control de cuotas! ¡Toma tus precauciones!",
        "kind": "broll",
        "topTag": "📩 PROTOCOLO FINOPS",
        "monitorTitle": "CAPTOORA × AI FINOPS",
        "headline": "CONTROLA TUS CUOTAS HOY",
        "lines": [
            "> Script auditor de transcript JSONL",
            "> Alertas 70% / 85% / Freno al 95%",
        ],
        "ctaText": "COMENTA: FINOPS 🚀",
        "accentColor": "#22C55E",
    },
    {
        "speaker": "tony",
        "text": "[excited] Waters!... Waters!",
        "language_code": "en",
        "stability": 0.35,
        "kind": "clip",
        "videoFile": "agy_03_solo_feliz_guino.mp4",
        "topTag": "🌊 ¡WATERS!",
        "accentColor": "#DFB15B",
        "zoomStart": 1.0,
        "zoomEnd": 1.12,
        "shakeIntro": True,
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
    last_broll_idx = None

    for idx, item in enumerate(EP03_LINES, start=1):
        mp3_path = OUT_AUDIO / f"{idx:02d}_{item['speaker']}.mp3"
        if not mp3_path.exists():
            vid = VOICE_MAP[item["speaker"]]
            stab = item.get("stability", 0.32)
            lang = item.get("language_code")
            print(f"[EP03] TTS {idx:02d} ({item['speaker']}, lang={lang}): {item['text']}")
            tts_to_mp3(item["text"], vid, mp3_path, api_key, stability=stab, language_code=lang)

        dur = probe_duration(mp3_path)
        start_sec = current_frame / FPS
        audio_events.append((start_sec + 0.08, mp3_path))

        # CERO traslapes: cada beat dura al menos audio + 0.25s
        needed_frames = max(48, math.ceil((dur + 0.25) * FPS))

        if item["kind"] == "clip":
            rem = needed_frames
            chunk_idx = 0
            while rem > 0:
                chunk = min(108, rem) if rem > 114 else rem
                # Evitar último fragmento demasiado corto
                if rem - chunk > 0 and rem - chunk < 30:
                    chunk = rem // 2
                z0 = item.get("zoomStart", 1.0) + chunk_idx * 0.06
                z1 = item.get("zoomEnd", 1.10) + chunk_idx * 0.06
                beats_out.append(
                    {
                        "kind": "clip",
                        "durationInFrames": chunk,
                        "videoFile": item["videoFile"],
                        "topTag": item["topTag"],
                        "accentColor": item["accentColor"],
                        "zoomStart": round(z0, 2),
                        "zoomEnd": round(z1, 2),
                        "shakeIntro": item.get("shakeIntro", False) if chunk_idx == 0 else False,
                    }
                )
                rem -= chunk
                chunk_idx += 1
            current_frame += needed_frames

        elif item["kind"] == "broll":
            beats_out.append(
                {
                    "kind": "broll",
                    "durationInFrames": needed_frames,
                    "topTag": item["topTag"],
                    "monitorTitle": item["monitorTitle"],
                    "headline": item["headline"],
                    "lines": item["lines"],
                    "screenshotFile": item.get("screenshotFile"),
                    "ctaText": item.get("ctaText"),
                    "accentColor": item["accentColor"],
                }
            )
            last_broll_idx = len(beats_out) - 1
            current_frame += needed_frames

        elif item["kind"] == "clip_plus_broll":
            clip_frames = min(105, max(54, needed_frames // 2))
            broll_frames = max(60, needed_frames - clip_frames)
            beats_out.append(
                {
                    "kind": "clip",
                    "durationInFrames": clip_frames,
                    "videoFile": item["videoFile"],
                    "topTag": item["topTag"],
                    "accentColor": item["accentColor"],
                    "zoomStart": 1.0,
                    "zoomEnd": 1.08,
                }
            )
            beats_out.append(
                {
                    "kind": "broll",
                    "durationInFrames": broll_frames,
                    "topTag": item["brollTopTag"],
                    "monitorTitle": item["monitorTitle"],
                    "headline": item["headline"],
                    "lines": item["lines"],
                    "screenshotFile": item.get("screenshotFile"),
                    "ctaText": item.get("ctaText"),
                    "accentColor": item["accentColor"],
                }
            )
            last_broll_idx = len(beats_out) - 1
            current_frame += clip_frames + broll_frames

    # Asegurar >= 62s para compatibilidad total con OpusClip (> 1 minuto)
    if current_frame < 62 * FPS:
        extra = 62 * FPS - current_frame
        pad_idx = last_broll_idx if last_broll_idx is not None else len(beats_out) - 1
        beats_out[pad_idx]["durationInFrames"] += extra
        current_frame += extra

    total_sec = current_frame / FPS
    master_wav = OUT_AUDIO / "EP03_master.wav"
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
    existing["EP03_TONY_CUOTA"] = beats_out
    BEATS_JSON.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ [EP03_TONY_CUOTA] Total frames={current_frame} ({total_sec:.2f}s) | WAV={master_wav}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
