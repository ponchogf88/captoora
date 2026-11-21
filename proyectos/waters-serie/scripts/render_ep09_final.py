#!/usr/bin/env python3
"""
Pipeline de Renderizado Final para EP09 DIA-APPLE:
1. Renderiza secuencia de imágenes con Remotion CLI (--sequence)
2. Ensambla y codifica con FFmpeg según las reglas maestras de Mac:
   - yuv420p, bt709, color_range tv, -crf 18, -preset slow, -movflags +faststart
   - Audio master WAV (voces Tony + Agy + SFX rescate + chimes + beats @ 44.1kHz stereo)
3. Valida el resultado con ffprobe (resolución 1080x1920, duración 60.0s, codecs)
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/Users/user/captoora")
STUDIO_DIR = ROOT / "proyectos/waters-3d-studio"
AUDIO_MASTER = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP09_DIA_APPLE/EP09_master.wav"
OUTPUT_MP4 = ROOT / "proyectos/waters-serie/renders/WATERS_CHISPA_EP09_APPLE_60S.mp4"
FRAMES_DIR = Path("/tmp/ep09_frames_seq")

FFMPEG = "/Users/user/.local/bin/ffmpeg"
if not Path(FFMPEG).exists():
    FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"

FFPROBE = "/Users/user/.local/bin/ffprobe"
if not Path(FFPROBE).exists():
    FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"

def main():
    print("🚀 [FASE DE RENDER] Iniciando Renderizado de WATERS EP09 DIA-APPLE...")
    print(f"🎬 Composición: WatersChispaEp09 (1,800 frames @ 30fps = 60.0s)")
    print(f"📁 Directorio de frames temporales: {FRAMES_DIR}")
    print(f"🎵 Audio Master: {AUDIO_MASTER}")
    print(f"🎥 Destino: {OUTPUT_MP4}")

    if not AUDIO_MASTER.exists():
        print(f"❌ Error: No existe el audio master en {AUDIO_MASTER}")
        return 1

    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    t0 = time.time()

    # Paso 1: Remotion render image sequence
    remotion_cmd = [
        "npx", "remotion", "render",
        "WatersChispaEp09",
        str(FRAMES_DIR),
        "--sequence",
        "--image-format", "jpeg",
        "--jpeg-quality", "95",
        "--concurrency", "6",
        "--log", "warn",
    ]

    print("⏳ Ejecutando Remotion sequence render...")
    res = subprocess.run(remotion_cmd, cwd=str(STUDIO_DIR))
    if res.returncode != 0:
        print(f"❌ Error en renderizado Remotion (código {res.returncode})")
        return res.returncode

    t1 = time.time()
    print(f"✅ Secuencia renderizada en {t1 - t0:.1f}s")

    # Contar frames
    frames = list(FRAMES_DIR.glob("element-*.jpeg"))
    print(f"🖼️ Total de frames generados: {len(frames)}")
    if len(frames) == 0:
        print("❌ Error: No se encontraron frames en el directorio temporal.")
        return 1

    # Paso 2: FFmpeg ensamblado y codificación con estándares de calidad Mac/Broadcast
    print("⏳ Codificando MP4 final con FFmpeg...")
    ffmpeg_cmd = [
        FFMPEG, "-y",
        "-framerate", "30",
        "-i", str(FRAMES_DIR / "element-%04d.jpeg"),
        "-i", str(AUDIO_MASTER),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-colorspace", "bt709",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-color_range", "tv",
        "-crf", "18",
        "-preset", "slow",
        "-movflags", "+faststart",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(OUTPUT_MP4),
    ]

    res_ff = subprocess.run(ffmpeg_cmd)
    if res_ff.returncode != 0:
        print(f"❌ Error en FFmpeg (código {res_ff.returncode})")
        return res_ff.returncode

    t2 = time.time()
    print(f"✅ MP4 generado exitosamente en {t2 - t1:.1f}s: {OUTPUT_MP4}")

    # Paso 3: Validación con ffprobe
    print("\n🔍 --- REPORTE DE VALIDACIÓN FFPROBE (VIDEO) ---")
    probe_v = [
        FFPROBE, "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,duration,r_frame_rate,codec_name,pix_fmt",
        "-of", "default=noprint_wrappers=1",
        str(OUTPUT_MP4)
    ]
    subprocess.run(probe_v)

    print("\n🔍 --- REPORTE DE VALIDACIÓN FFPROBE (AUDIO) ---")
    probe_a = [
        FFPROBE, "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,sample_rate,channels,duration",
        "-of", "default=noprint_wrappers=1",
        str(OUTPUT_MP4)
    ]
    subprocess.run(probe_a)

    file_size_mb = OUTPUT_MP4.stat().st_size / (1024 * 1024)
    print(f"\n📦 Tamaño del archivo final: {file_size_mb:.2f} MB")

    # Limpieza
    print(f"🧹 Limpiando frames temporales en {FRAMES_DIR}...")
    shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    print("✨ Limpieza completada.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
