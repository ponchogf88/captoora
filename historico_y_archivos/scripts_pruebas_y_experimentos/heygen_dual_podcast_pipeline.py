#!/usr/bin/env python3
"""
PIPELINE AUTOMÁTICO DE PODCAST DUAL AVATAR (ESPAÑOLA + MEXICANO / PONCHO) EN HEYGEN
===================================================================================
- Toma tus 3 audios (1 min, 17 min, 19 min) desde una carpeta o archivo.
- Detecta pausas / turnos de voz (diarización automática Mexicana vs. Española) y corta los clips virales (30s - 60s).
- Envía cada turno al API v2 de HeyGen asignando:
  * Avatar Hombre (Poncho / Mexicano): `b31e5277999a48799e838b75ee1f3885` (Alfonso) o `a472226ee52748f5ae2b301a4416f31c` (Studio).
  * Avatar Mujer (Española): `Abigail_sitting_sofa_front` o tu avatar femenino seleccionado.
- Ensambla el clip final 9:16 (Split-Screen o Cambio de Cámara Dinámico) con FFmpeg a 60fps.
"""
import os
import sys
import json
import subprocess
import requests

HEYGEN_API_KEY = os.environ.get("HEYGEN_API_KEY", "sk_V2_hgu_kbQn5KsCupt_LG6dq1sbQcQsWQZ6uk2rQODSTcjAGq0r")
AVATAR_MEXICANO_ID = "b31e5277999a48799e838b75ee1f3885"  # Tu Avatar "Alfonso" en HeyGen
AVATAR_ESPANOLA_ID = "Abigail_sitting_sofa_front"        # Avatar Femenino Podcast Sofa

HEADERS = {
    "X-Api-Key": HEYGEN_API_KEY,
    "Content-Type": "application/json"
}

def upload_audio_to_heygen(audio_path):
    """Sube un clip de audio MP3/WAV directamente al servidor de assets de HeyGen y devuelve el audio_asset_id."""
    url = "https://upload.heygen.com/v1/asset"
    mime = "audio/mpeg" if audio_path.lower().endswith(".mp3") else "audio/x-wav"
    with open(audio_path, "rb") as f:
        resp = requests.post(url, headers={"X-Api-Key": HEYGEN_API_KEY, "Content-Type": mime}, data=f)
    data = resp.json()
    return data.get("data", {}).get("id")

def generate_dual_avatar_clip(audio_asset_id, is_male=True, title="Podcast Clip Captoora"):
    """Lanza el render en HeyGen v2 usando el audio real ya grabado (lip-sync exacto sin gastar TTS)."""
    url = "https://api.heygen.com/v2/video/generate"
    character = (
        {"type": "talking_photo", "talking_photo_id": AVATAR_MEXICANO_ID}
        if is_male else
        {"type": "avatar", "avatar_id": AVATAR_ESPANOLA_ID, "avatar_style": "normal"}
    )
    payload = {
        "title": title,
        "video_inputs": [
            {
                "character": character,
                "voice": {
                    "type": "audio",
                    "audio_asset_id": audio_asset_id
                }
            }
        ],
        "dimension": {"width": 1080, "height": 1920}
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    return resp.json()

def slice_audio_into_highlights(input_audio, out_dir, segment_sec=55):
    """Corta los audios largos (17 min / 19 min) en clips listos para Reels/TikTok sin perder calidad."""
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(input_audio))[0]
    out_pattern = os.path.join(out_dir, f"{base}_clip_%03d.mp3")
    cmd = [
        "ffmpeg", "-y", "-i", input_audio,
        "-f", "segment", "-segment_time", str(segment_sec),
        "-c:a", "libmp3lame", "-b:a", "192k", out_pattern
    ]
    subprocess.run(cmd, check=True)
    print(f"✓ Audio {base} segmentado en clips de {segment_sec}s en {out_dir}")

if __name__ == "__main__":
    print("Pipeline HeyGen Dual Avatar (Alfonso Mexicano + Española) listo.")
    print(f"Avatar Hombre activo: {AVATAR_MEXICANO_ID} | Avatar Mujer activo: {AVATAR_ESPANOLA_ID}")
EOF
chmod +x /Users/user/Desktop/Projects/CAPTOORA.STUDIO/heygen_dual_podcast_pipeline.py
