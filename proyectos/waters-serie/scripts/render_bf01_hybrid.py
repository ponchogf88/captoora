#!/usr/bin/env python3
"""
Renderizado final limpio 16:9 de BF01 (HybridBlackFridayBF01):
SIN subtítulos quemados abajo para pasar directo por OpusClip + Captions.
"""
import json
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
STUDIO_DIR = ROOT / "proyectos/waters-3d-studio"
TIMINGS_JSON = ROOT / "proyectos/waters-3d-studio/src/data/bf01Timings.json"
AUDIO_MASTER = ROOT / "proyectos/waters-serie/black_friday_bf01/audio/bf01_master_sfx.wav"
OUTPUT_MP4 = ROOT / "proyectos/waters-serie/renders/BF01_BLACK_FRIDAY_PRESUPUESTO_16X9_CLEAN.mp4"
COLA_MP4 = ROOT / "proyectos/waters-serie/cola_programacion_semana/listos_para_arrastrar/00_BLACK_FRIDAY_PRESUPUESTO_OPUS_CLEAN.mp4"
FRAMES_DIR = Path("/tmp/bf01_frames")

FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"


def main() -> int:
    meta = json.loads(TIMINGS_JSON.read_text(encoding="utf-8"))
    print(f"🚀 Renderizando BF01 Híbrido 16:9 ({meta['total_frames']} frames = {meta['total_duration']:.2f}s)...")
    if not AUDIO_MASTER.exists():
        print(f"❌ Falta audio maestro: {AUDIO_MASTER}")
        return 1

    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    remotion_cmd = [
        "npx",
        "remotion",
        "render",
        "src/index.ts",
        "HybridBlackFridayBF01",
        str(FRAMES_DIR),
        "--sequence",
        "--image-format=jpeg",
        "--jpeg-quality=90",
        "--concurrency=2",
        "--quiet",
    ]
    res = subprocess.run(remotion_cmd, cwd=str(STUDIO_DIR))
    if res.returncode != 0:
        print("❌ Error en remotion render --sequence (HybridBlackFridayBF01)")
        return res.returncode

    frames = sorted(FRAMES_DIR.glob("element-*.jpeg"))
    print(f"✅ {len(frames)} frames renderizados en {time.time() - t0:.1f}s")
    if not frames:
        return 1

    ffmpeg_cmd = [
        FFMPEG,
        "-y",
        "-framerate",
        "30",
        "-i",
        str(FRAMES_DIR / "element-%04d.jpeg"),
        "-i",
        str(AUDIO_MASTER),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-colorspace",
        "bt709",
        "-color_primaries",
        "bt709",
        "-color_trc",
        "bt709",
        "-color_range",
        "tv",
        "-crf",
        "18",
        "-preset",
        "medium",
        "-movflags",
        "+faststart",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(OUTPUT_MP4),
    ]
    print("⏳ Codificando MP4 16:9 limpio...")
    res_ff = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res_ff.returncode != 0:
        print("❌ Error FFmpeg:", res_ff.stderr.decode(errors="ignore")[-1000:])
        return res_ff.returncode

    COLA_MP4.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUT_MP4, COLA_MP4)
    print(f"📦 Master limpio para OpusClip: {COLA_MP4} ({COLA_MP4.stat().st_size / (1024*1024):.2f} MB)")

    v_probe = subprocess.run(
        [
            FFPROBE, "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,duration,codec_name,pix_fmt",
            "-of", "default=noprint_wrappers=1", str(COLA_MP4),
        ],
        stdout=subprocess.PIPE, text=True,
    )
    a_probe = subprocess.run(
        [
            FFPROBE, "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=codec_name,sample_rate,channels,duration",
            "-of", "default=noprint_wrappers=1", str(COLA_MP4),
        ],
        stdout=subprocess.PIPE, text=True,
    )
    print("\n🔍 FFPROBE VIDEO:\n" + v_probe.stdout.strip())
    print("\n🔍 FFPROBE AUDIO:\n" + a_probe.stdout.strip())

    shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    print(f"✨ Completado en {time.time() - t0:.1f}s totales")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
