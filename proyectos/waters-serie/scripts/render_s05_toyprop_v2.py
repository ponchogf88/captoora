#!/usr/bin/env python3
"""
Pipeline de Renderizado S05 v2 (Toy-Prop 3D 16:9 Deep Dive - Gemini 4 Carbon):
1. Respalda S05 v1 en /tmp/ORO_CARBON_S05_V1_backup.mp4 si no existe respaldo.
2. Renderiza secuencia JPEG 1920x1080 con Remotion CLI (--sequence, --concurrency=2).
3. Ensambla MP4 H.264 + audio maestro con SFX (carbon_explainer_3min_master_sfx.wav) vía FFmpeg.
4. Valida symlink de cola y reporte ffprobe.
"""
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
STUDIO_DIR = ROOT / "proyectos/waters-3d-studio"
AUDIO_MASTER = ROOT / "proyectos/waters-serie/carbon_ciberseguridad/audio/carbon_explainer_3min_master_sfx.wav"
OUTPUT_MP4 = ROOT / "proyectos/waters-serie/renders/ORO_CARBON_CIBERSEGURIDAD_EXPLICATIVO_3MIN.mp4"
COLA_MP4 = ROOT / "proyectos/waters-serie/cola_programacion_semana/listos_para_arrastrar/05_VIE_2000_ORO_CARBON_EXPLICATIVO_3MIN.mp4"
BACKUP_V1 = Path("/tmp/ORO_CARBON_S05_V1_backup.mp4")
FRAMES_DIR = Path("/tmp/s05_toyprop_frames")

FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"


def main() -> int:
    print("🚀 Iniciando render S05 Toy-Prop 3D 16:9 v2 (ToyPropCarbonS05, 8195 frames @ 30fps)...")
    if not AUDIO_MASTER.exists():
        print(f"❌ No existe audio maestro SFX: {AUDIO_MASTER}")
        return 1

    if OUTPUT_MP4.exists() and not BACKUP_V1.exists():
        shutil.copy2(OUTPUT_MP4, BACKUP_V1)
        print(f"💾 Respaldo v1 guardado en {BACKUP_V1}")

    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    remotion_cmd = [
        "npx",
        "remotion",
        "render",
        "src/index.ts",
        "ToyPropCarbonS05",
        str(FRAMES_DIR),
        "--sequence",
        "--image-format=jpeg",
        "--jpeg-quality=90",
        "--concurrency=2",
        "--quiet",
    ]
    res = subprocess.run(remotion_cmd, cwd=str(STUDIO_DIR))
    if res.returncode != 0:
        print("❌ Error en remotion render --sequence (ToyPropCarbonS05)")
        return res.returncode

    frames = sorted(FRAMES_DIR.glob("element-*.jpeg"))
    print(f"✅ {len(frames)} frames renderizados en {time.time() - t0:.1f}s")
    if not frames:
        print("❌ No se generaron frames JPEG")
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
        "19",
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
    print("⏳ Codificando MP4 16:9 final con FFmpeg...")
    res_ff = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res_ff.returncode != 0:
        print("❌ Error en FFmpeg:")
        print(res_ff.stderr.decode(errors="ignore")[-1000:])
        return res_ff.returncode

    COLA_MP4.parent.mkdir(parents=True, exist_ok=True)
    if not (COLA_MP4.exists() and COLA_MP4.resolve() == OUTPUT_MP4.resolve()):
        shutil.copy2(OUTPUT_MP4, COLA_MP4)
    print(f"📦 Cola lista: {COLA_MP4} ({COLA_MP4.stat().st_size / (1024*1024):.2f} MB)")

    v_probe = subprocess.run(
        [
            FFPROBE,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate,duration,codec_name,pix_fmt",
            "-of",
            "default=noprint_wrappers=1",
            str(COLA_MP4),
        ],
        stdout=subprocess.PIPE,
        text=True,
    )
    a_probe = subprocess.run(
        [
            FFPROBE,
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_name,sample_rate,channels,duration",
            "-of",
            "default=noprint_wrappers=1",
            str(COLA_MP4),
        ],
        stdout=subprocess.PIPE,
        text=True,
    )
    print("\n🔍 FFPROBE VIDEO:\n" + v_probe.stdout.strip())
    print("\n🔍 FFPROBE AUDIO:\n" + a_probe.stdout.strip())

    shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    print(f"✨ Completado en {time.time() - t0:.1f}s totales")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
