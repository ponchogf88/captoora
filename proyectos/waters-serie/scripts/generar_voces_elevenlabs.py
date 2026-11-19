#!/usr/bin/env python3
"""
Pipeline Audio-First (cero traslapes, cero silencios muertos):
1. Genera las líneas con ElevenLabs (Chuy = Cristian Medina, Agy = Liam/Orion).
2. Mide la duración exacta de cada .mp3 con ffprobe.
3. Calcula los frames exactos de cada beat y exporta src/episodeBeats.json para Remotion.
4. Genera la pista maestra WAV perfectamente sincronizada con el SFX de 0:00.
"""
import json
import math
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
ENV_FILE = ROOT / ".env"
OUT_AUDIO = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3"
BEATS_JSON = ROOT / "proyectos/waters-3d-studio/src/episodeBeats.json"
FFMPEG = "/Users/imac/.local/bin/ffmpeg"
FFPROBE = "/Users/imac/.local/bin/ffprobe"
FPS = 30

CHUY_ID = "htFfPSZGJwjBv1CL0aMD"  # Antonio (cercano, respiraciones/risa)
AGY_ID = "kl7d390GatBPfqhRTyAl"   # Liza (Natural Mexican Creator)


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


def tts_to_mp3(text: str, voice_id: str, out_path: Path, api_key: str) -> None:
    payload = json.dumps(
        {
            "text": text,
            "model_id": "eleven_v3",
            "voice_settings": {
                "stability": 0.32,
                "similarity_boost": 0.78,
                "style": 0.0,
                "use_speaker_boost": True,
            },
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=payload,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        out_path.write_bytes(resp.read())


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True,
    ).strip()
    return float(out)


EPISODE_DEFS = {
    "EP01": [
        {
            "speaker": "chuy",
            "text": "[gasps] ¡Waters gamers!",
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
            "text": "[serious] ¡Chuy, aguas con el lanzamiento de GTA seis hoy! Casi diez millones de vistas en horas.",
            "kind": "clip_plus_broll",
            "videoFile": "agy_01_solo_explicando.mp4",
            "topTag": "🤖 AGY · ALERTA GTA 6",
            "brollTopTag": "🎮 LANZAMIENTO VIRAL",
            "monitorTitle": "TRENDING · X / TIKTOK",
            "headline": "GTA 6: 9.8M VISTAS",
            "lines": ["> tráfico masivo buscando descargas", "> hackers aprovechando el hype HOY", "! AGUAS CON LINKS FALSOS"],
            "accentColor": "#38BDF8",
        },
        {
            "speaker": "chuy",
            "text": "[surprised] ¿Qué pasó? ¡Si todo mundo lo está buscando!",
            "kind": "clip",
            "videoFile": "chuy_04_escucha_atento.mp4",
            "topTag": "💬 CHUY × AGY",
            "accentColor": "#38BDF8",
            "zoomStart": 1.0,
            "zoomEnd": 1.08,
        },
        {
            "speaker": "agy",
            "text": "[whispering] Por eso mismo... hoy hackers usan inteligencia artificial como Claude para hacer Vibe Hacking e ingeniería inversa.",
            "kind": "clip_plus_broll",
            "videoFile": "agy_01_solo_explicando.mp4",
            "topTag": "⚠️ VIBE HACKING + IA",
            "brollTopTag": "🤖 CLAUDE · TERMINAL",
            "monitorTitle": "ANTHROPIC · CLAUDE TERMINAL",
            "headline": "INGENIERÍA INVERSA IA",
            "lines": ["$ vibe-hacking --target=gta6-hype", "> generando phishing + cracks falsos", "! VELOCIDAD 10X CON IA"],
            "accentColor": "#FF4D4D",
        },
        {
            "speaker": "chuy",
            "text": "[nervous] ¿O sea que si bajo uno falso... pierdo mi cuenta?!",
            "kind": "clip",
            "videoFile": "chuy_02_angustia_sudor.mp4",
            "topTag": "😰 ¿PIERDO MI CUENTA?",
            "accentColor": "#FF4D4D",
            "zoomStart": 1.0,
            "zoomEnd": 1.1,
        },
        {
            "speaker": "agy",
            "text": "[serious] ¡Exacto! Traen Infostealers que roban tus tarjetas y tu cuenta de PlayStation, Xbox o Steam.",
            "kind": "broll",
            "topTag": "☠️ TRAMPA INFOSTEALER",
            "monitorTitle": "SECURITY ALERT · MALWARE",
            "headline": "ROBO EN SEGUNDOS",
            "lines": ["[!] Crack falso ➔ Infostealer activo", "[!] Extrayendo tarjetas y tokens...", "[X] CUENTA PSN / XBOX / STEAM ROBADA"],
            "accentColor": "#FF4D4D",
        },
        {
            "speaker": "chuy",
            "text": "[gasps] ¡No manches! ¿Y cómo la protejo?",
            "kind": "clip",
            "videoFile": "chuy_03_sorpresa_silla.mp4",
            "topTag": "😱 ¡NO MANCHES!",
            "accentColor": "#DFB15B",
            "zoomStart": 1.0,
            "zoomEnd": 1.18,
        },
        {
            "speaker": "agy",
            "text": "[excited] ¡Con Gemini cuatro Neon en Antigravity! Detecta links falsos, blinda contraseñas y activa dos FA.",
            "kind": "broll",
            "topTag": "🛡️ GEMINI 4 NEON",
            "monitorTitle": "ANTIGRAVITY · SHIELD ON",
            "headline": "BLINDAJE CON NEON",
            "lines": ["✓ Analizando links sospechosos", "✓ Verificando 2FA + contraseñas", "✓ CUENTAS GAMER PROTEGIDAS"],
            "accentColor": "#DFB15B",
        },
        {
            "speaker": "chuy",
            "text": "[sighs] [laughs] ¡Uf, qué alivio! ¡Ya quedó blindada!",
            "kind": "clip",
            "videoFile": "chuy_06_feliz_celebrando.mp4",
            "topTag": "🎉 ¡CUENTA BLINDADA!",
            "accentColor": "#22C55E",
            "zoomStart": 1.0,
            "zoomEnd": 1.08,
        },
        {
            "speaker": "agy",
            "text": "[excited] ¡Comenta Neon y te mando la guía gratis!",
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
    ],
    "EP02": [
        {
            "speaker": "chuy",
            "text": "[gasps] ¡Waters si te bloquearon tu cuenta!",
            "kind": "clip",
            "videoFile": "chuy_01_susto_alerta.mp4",
            "topTag": "🚨 ¡WATERS CREADORES!",
            "accentColor": "#FF4D4D",
            "zoomStart": 1.0,
            "zoomEnd": 1.12,
            "shakeIntro": True,
        },
        {
            "speaker": "chuy",
            "text": "[sighs] Tenía una cuenta comercial de hace años que ni recordaba... y no podía enlazar Facebook con Instagram.",
            "kind": "clip_plus_broll",
            "videoFile": "chuy_02_angustia_sudor.mp4",
            "topTag": "😫 INFIERNO EN META",
            "brollTopTag": "⚠️ CUENTA COMERCIAL TRABADA",
            "monitorTitle": "META BUSINESS SUITE",
            "headline": "ERROR AL ENLAZAR IG + FB",
            "lines": ["[!] Business Manager viejo detectado", "[!] Permisos bloqueados / sin acceso", "[X] FORMULARIOS SIN RESPUESTA"],
            "accentColor": "#FF4D4D",
        },
        {
            "speaker": "agy",
            "text": "[excited] ¡Tranquilo, Chuy! Con la IA agéntica de Google ya no peleas solo contra soporte.",
            "kind": "clip",
            "videoFile": "agy_01_solo_explicando.mp4",
            "topTag": "🤖 AGY · IA AGÉNTICA",
            "accentColor": "#38BDF8",
            "zoomStart": 1.0,
            "zoomEnd": 1.08,
        },
        {
            "speaker": "chuy",
            "text": "[nervous] Un amigo influencer perdió su cuenta por reportes y ya iba a abrir otra por pura flojera.",
            "kind": "clip_plus_broll",
            "videoFile": "chuy_04_escucha_atento.mp4",
            "topTag": "📱 CASO REAL INFLUENCER",
            "brollTopTag": "🔁 SEGUIMIENTO AUTOMÁTICO",
            "monitorTitle": "GOOGLE AGENTIC WORKFLOW",
            "headline": "EL AGENTE NO SUELTA EL CASO",
            "lines": ["> Redactando apelación formal...", "> Seguimiento automático al ticket", "✓ RESPUESTA REAL DE SOPORTE"],
            "accentColor": "#38BDF8",
        },
        {
            "speaker": "agy",
            "text": "[serious] El Agente redacta la apelación y da seguimiento automático hasta recuperarla.",
            "kind": "broll",
            "topTag": "✅ CUENTAS ENLAZADAS",
            "monitorTitle": "META STATUS · VERIFICADO",
            "headline": "FB + IG RECUPERADOS",
            "lines": ["✓ Cuenta comercial antigua resuelta", "✓ Cuenta de influencer restaurada", "✓ AÑOS DE TRABAJO A SALVO"],
            "accentColor": "#22C55E",
        },
        {
            "speaker": "chuy",
            "text": "[surprised] ¿En serio, sin mandar cien correos?!",
            "kind": "clip",
            "videoFile": "chuy_03_sorpresa_silla.mp4",
            "topTag": "😲 ¿SIN CIEN CORREOS?",
            "accentColor": "#DFB15B",
            "zoomStart": 1.0,
            "zoomEnd": 1.16,
        },
        {
            "speaker": "chuy",
            "text": "[laughs] ¡Y sí se pudo! ¡Recuperada al cien!",
            "kind": "clip",
            "videoFile": "chuy_06_feliz_celebrando.mp4",
            "topTag": "🎉 ¡VICTORIA TOTAL!",
            "accentColor": "#22C55E",
            "zoomStart": 1.0,
            "zoomEnd": 1.08,
        },
        {
            "speaker": "agy",
            "text": "[excited] ¡Comenta Agente y te enseño cómo recuperarla!",
            "kind": "clip_plus_broll",
            "videoFile": "agy_03_solo_feliz_guino.mp4",
            "topTag": "🤖 AGY · MODO HÉROE",
            "brollTopTag": "🚀 RECUPERA TU CUENTA",
            "monitorTitle": "CAPTOORA × ANTIGRAVITY",
            "headline": "¿CUENTA BLOQUEADA?",
            "lines": ["> Flujo agéntico de apelación", "> Blindaje para creadores"],
            "ctaText": "COMENTA: AGENTE 🚀",
            "accentColor": "#DFB15B",
        },
    ],
}


def build_episode(ep_key: str, api_key: str) -> list[dict]:
    ep_dir = OUT_AUDIO / ep_key
    ep_dir.mkdir(parents=True, exist_ok=True)
    beats_out = []
    audio_events = []
    current_frame = 0

    for idx, item in enumerate(EPISODE_DEFS[ep_key], start=1):
        mp3_path = ep_dir / f"{idx:02d}_{item['speaker']}.mp3"
        if not mp3_path.exists():
            vid = CHUY_ID if item["speaker"] == "chuy" else AGY_ID
            print(f"[{ep_key}] TTS {idx:02d} ({item['speaker']}): {item['text']}")
            tts_to_mp3(item["text"], vid, mp3_path, api_key)

        dur = probe_duration(mp3_path)
        start_sec = current_frame / FPS
        audio_events.append((start_sec + 0.08, mp3_path))

        # Exact frames for this line (plus 0.18s breathing gap)
        needed_frames = max(45, math.ceil((dur + 0.22) * FPS))

        if item["kind"] == "clip":
            # Flow clip max is 120 frames (4.0s)
            clip_frames = min(116, needed_frames)
            beats_out.append({
                "kind": "clip",
                "durationInFrames": clip_frames,
                "videoFile": item["videoFile"],
                "topTag": item["topTag"],
                "accentColor": item["accentColor"],
                "zoomStart": item.get("zoomStart", 1.0),
                "zoomEnd": item.get("zoomEnd", 1.09),
                "shakeIntro": item.get("shakeIntro", False),
            })
            current_frame += clip_frames

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
            # Split cleanly: up to 96 frames (3.2s) of character clip, rest (min 60f) on B-roll monitor!
            clip_frames = min(96, max(54, needed_frames // 2))
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

    # Build synced master WAV (0:00 impact SFX + exact sequential voice lines)
    total_sec = current_frame / FPS
    master_wav = ep_dir / f"{ep_key}_master.wav"
    inputs = [
        "-f", "lavfi", "-i", f"sine=frequency=110:duration=0.40",
        "-f", "lavfi", "-i", f"sine=frequency=880:duration=0.30",
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
    print(f"✅ [{ep_key}] Total frames={current_frame} ({total_sec:.2f}s) | Master WAV={master_wav}")
    return beats_out


def main() -> int:
    api_key = load_api_key()
    if not api_key:
        print("ERROR: Falta ELEVENLABS_API_KEY válida (sk_...) en .env", file=sys.stderr)
        return 1
    ep1_beats = build_episode("EP01", api_key)
    ep2_beats = build_episode("EP02", api_key)
    BEATS_JSON.write_text(json.dumps({"EP01": ep1_beats, "EP02": ep2_beats}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Exportado {BEATS_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
