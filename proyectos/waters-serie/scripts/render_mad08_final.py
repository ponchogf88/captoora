#!/usr/bin/env python3
"""
Pipeline de Renderizado Final para MAD-08:
1. Renderiza secuencia de imágenes con Remotion CLI (--sequence)
2. Ensambla y codifica con FFmpeg según las reglas maestras de Mac:
   - yuv420p, bt709, color_range tv, -crf 18, -movflags +faststart
   - Audio master WAV (voces + SFX + música + silencio dramático)
3. Valida el resultado con ffprobe (resolución 1080x1920, duración ~46.0s, codecs)
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/Users/user/captoora")
STUDIO_DIR = ROOT / "proyectos/waters-3d-studio"
AUDIO_MASTER = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/MAD08_CUOTA/MAD08_master.wav"
OUTPUT_MP4 = ROOT / "proyectos/waters-serie/renders/WATERS_CHISPA_MAD08_CUOTA_45S.mp4"
FRAMES_DIR = Path("/tmp/mad08_frames_seq")

FFMPEG = "/Users/user/.local/bin/ffmpeg"
if not Path(FFMPEG).exists():
    FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"

FFPROBE = "/Users/user/.local/bin/ffprobe"
if not Path(FFPROBE).exists():
    FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"

def main():
    print("🚀 [FASE 3] Iniciando Renderizado de WATERS MAD-08...")
    print(f"🎬 Composición: WatersMad08 (1,380 frames @ 30fps = 46.0s)")
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
        "src/index.ts",
        "WatersMad08",
        str(FRAMES_DIR),
        "--sequence",
        "--image-format=jpeg",
        "--jpeg-quality=95",
        "--concurrency=6",
        "--quiet"
    ]
    print(f"⏳ Ejecutando Remotion sequence render...")
    res = subprocess.run(remotion_cmd, cwd=str(STUDIO_DIR))
    if res.returncode != 0:
        print("❌ Error en remotion render --sequence")
        return res.returncode

    t_render = time.time() - t0
    print(f"✅ Secuencia renderizada en {t_render:.1f}s")

    # Contar frames
    frames = list(FRAMES_DIR.glob("element-*.jpeg"))
    print(f"🖼️ Total de frames generados: {len(frames)}")

    # Paso 2: Ensamblar con FFmpeg bajo especificación estricta
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
        str(OUTPUT_MP4)
    ]
    print("⏳ Codificando MP4 final con FFmpeg...")
    res_ffmpeg = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res_ffmpeg.returncode != 0:
        print("❌ Error en FFmpeg:")
        print(res_ffmpeg.stderr.decode()[-1000:])
        return res_ffmpeg.returncode

    t_total = time.time() - t0
    print(f"✅ MP4 generado exitosamente en {t_total:.1f}s: {OUTPUT_MP4}")

    # Paso 3: Validación con ffprobe
    probe_cmd = [
        FFPROBE,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,duration,codec_name,pix_fmt",
        "-of", "default=noprint_wrappers=1",
        str(OUTPUT_MP4)
    ]
    probe_res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, text=True)
    print("\n🔍 --- REPORTE DE VALIDACIÓN FFPROBE (VIDEO) ---")
    print(probe_res.stdout.strip())

    probe_audio_cmd = [
        FFPROBE,
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,sample_rate,channels,duration",
        "-of", "default=noprint_wrappers=1",
        str(OUTPUT_MP4)
    ]
    probe_audio_res = subprocess.run(probe_audio_cmd, stdout=subprocess.PIPE, text=True)
    print("\n🔍 --- REPORTE DE VALIDACIÓN FFPROBE (AUDIO) ---")
    print(probe_audio_res.stdout.strip())

    file_size_mb = OUTPUT_MP4.stat().st_size / (1024 * 1024)
    print(f"\n📦 Tamaño del archivo final: {file_size_mb:.2f} MB")

    # Limpieza de frames temporales
    print(f"🧹 Limpiando frames temporales en {FRAMES_DIR}...")
    shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    print("✨ Limpieza completada.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
