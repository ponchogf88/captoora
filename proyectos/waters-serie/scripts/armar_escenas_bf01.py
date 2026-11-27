#!/usr/bin/env python3
"""
Pipeline modular escena-por-escena + unión final vía FFmpeg para BF01 (Multi-Ángulo Real):
  1. Toma los 6 clips reales con lip-sync de clips_raw/01.mp4 .. 06.mp4
     (o los 6 más recientes de ~/Downloads con --from-downloads).
  2. Auto-recorta franjas negras (cropdetect) -> public/avatar/bf01_s0X.mp4
     y extrae el audio ORIGINAL de ese clip (bf01_s0X_orig.wav) + duración exacta.
  3. Renderiza cada escena independiente con HybridBF01Scene a su duración EXACTA (1:1 frames, cero loop).
  4. Mezcla ese audio real (con su lip-sync) + micro-SFX sutil -> escenas/0X_<nombre>.mp4.
  5. Une las 6 escenas aprobadas con FFmpeg concat -> BF01_COMPLETO_UNIDO.mp4 + copia a cola OpusClip.

Uso:
  python3 proyectos/waters-serie/scripts/armar_escenas_bf01.py --from-downloads
  python3 proyectos/waters-serie/scripts/armar_escenas_bf01.py --scene 3   # solo rehace escena 3 y re-une
"""
import argparse
import json
import math
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
STUDIO_DIR = ROOT / "proyectos/waters-3d-studio"
PUBLIC_AVATAR = STUDIO_DIR / "public/avatar"
WORK_DIR = ROOT / "proyectos/waters-serie/black_friday_bf01"
CLIPS_RAW = WORK_DIR / "clips_raw"
AUDIO_WORK = WORK_DIR / "audio_escenas"
ESCENAS_DIR = WORK_DIR / "escenas"
FINAL_UNIDO = WORK_DIR / "BF01_COMPLETO_UNIDO.mp4"
COLA_MP4 = ROOT / "proyectos/waters-serie/cola_programacion_semana/listos_para_arrastrar/00_BLACK_FRIDAY_PRESUPUESTO_OPUS_CLEAN.mp4"

SCRIPTS_DIR = ROOT / "proyectos/waters-serie/scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
import add_toyprop_sfx as sfx  # noqa: E402

FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
SR = 44100
FPS = 30

SCENE_META: Dict[int, str] = {
    1: "01_hook_alerta",
    2: "02_bucle_cajita_ia",
    3: "03_grafica_gasto",
    4: "04_dilema_puertas_3d",
    5: "05_candados_checklist_3d",
    6: "06_cierre_cta",
}


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


def has_audio_stream(path: Path) -> bool:
    out = subprocess.check_output(
        [
            FFPROBE,
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_type",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return out == "audio"


def detect_crop(path: Path) -> str:
    p = subprocess.run(
        [FFMPEG, "-i", str(path), "-t", "3", "-vf", "cropdetect=24:16:0", "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    crops = [ln.split("crop=")[-1].split()[0] for ln in p.stderr.splitlines() if "crop=" in ln]
    return f"crop={crops[-1]}," if crops else ""


def build_scene_sfx_wav(scene_idx: int, dur_sec: float, out_wav: Path) -> None:
    n_total = int((dur_sec + 0.2) * SR)
    buf_l = [0.0] * n_total
    buf_r = [0.0] * n_total

    if scene_idx == 1:
        sfx.add_crack_impact(buf_l, buf_r, min(0.95, dur_sec * 0.2))
        sfx.add_siren_pulse(buf_l, buf_r, min(1.8, dur_sec * 0.38))
    elif scene_idx in (2, 3):
        sfx.add_pop_whoosh(buf_l, buf_r, 0.08, pitch_scale=1.05)
    elif scene_idx == 4:
        sfx.add_doors_chime(buf_l, buf_r, 0.08)
    elif scene_idx == 5:
        sfx.add_pop_whoosh(buf_l, buf_r, 0.06, pitch_scale=1.15)
        sfx.add_check_ding(buf_l, buf_r, dur_sec * 0.22, 1046.5)
        sfx.add_check_ding(buf_l, buf_r, dur_sec * 0.52, 1318.5)
        sfx.add_check_ding(buf_l, buf_r, dur_sec * 0.80, 1568.0)
    elif scene_idx == 6:
        sfx.add_pop_whoosh(buf_l, buf_r, 0.08, pitch_scale=1.2)

    raw = bytearray()
    for lv, rv in zip(buf_l, buf_r):
        il = max(-32767, min(32767, int(lv * 32767.0)))
        ir = max(-32767, min(32767, int(rv * 32767.0)))
        raw.extend(struct.pack("<hh", il, ir))
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(bytes(raw))


def import_from_downloads() -> None:
    CLIPS_RAW.mkdir(parents=True, exist_ok=True)
    downloads = Path("/Users/imac/Downloads")
    candidates = sorted(
        [p for p in downloads.glob("gemini_generated_video_*.mp4") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
    )
    if len(candidates) < 6:
        raise RuntimeError(
            f"Se necesitan 6 clips gemini_generated_video_*.mp4 en ~/Downloads; encontrados: {len(candidates)}"
        )
    latest_six = candidates[-6:]
    for idx, src in enumerate(latest_six, 1):
        dst = CLIPS_RAW / f"{idx:02d}.mp4"
        shutil.copy2(src, dst)
        print(f"📥 Escena {idx:02d} <- {src.name}")


def render_single_scene(idx: int) -> Path:
    raw_mp4 = CLIPS_RAW / f"{idx:02d}.mp4"
    if not raw_mp4.exists():
        raise FileNotFoundError(f"Falta clip real: {raw_mp4}")

    PUBLIC_AVATAR.mkdir(parents=True, exist_ok=True)
    AUDIO_WORK.mkdir(parents=True, exist_ok=True)
    ESCENAS_DIR.mkdir(parents=True, exist_ok=True)

    clean_name = f"avatar/bf01_s{idx:02d}.mp4"
    clean_avatar = STUDIO_DIR / "public" / clean_name
    crop_f = detect_crop(raw_mp4)

    # Normaliza a 30 fps 1280x720 sin franjas negras para sincronía frame-exacta
    subprocess.run(
        [
            FFMPEG, "-y", "-i", str(raw_mp4),
            "-vf", f"{crop_f}scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "medium",
            "-an", str(clean_avatar),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    dur = probe_duration(clean_avatar)
    dur_frames = max(30, int(math.floor(dur * FPS)))

    # Audio real del clip + micro SFX
    orig_wav = AUDIO_WORK / f"s{idx:02d}_orig.wav"
    if has_audio_stream(raw_mp4):
        subprocess.run(
            [FFMPEG, "-y", "-i", str(raw_mp4), "-vn", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(orig_wav)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.run(
            [FFMPEG, "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo:d={dur:.3f}", "-c:a", "pcm_s16le", str(orig_wav)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

    sfx_wav = AUDIO_WORK / f"s{idx:02d}_sfx.wav"
    mix_wav = AUDIO_WORK / f"s{idx:02d}_mix.wav"
    build_scene_sfx_wav(idx, dur, sfx_wav)
    subprocess.run(
        [
            FFMPEG, "-y", "-i", str(orig_wav), "-i", str(sfx_wav),
            "-filter_complex", "[1:a]volume=0.28[sfx];[0:a]volume=1.15[v];[v][sfx]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[out]",
            "-map", "[out]", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(mix_wav),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    frames_dir = Path(f"/tmp/bf01_scene_{idx:02d}_frames")
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    frames_dir.mkdir(parents=True, exist_ok=True)

    props = json.dumps({"sceneIndex": idx, "clipSrc": clean_name, "durationInFrames": dur_frames})
    print(f"🎬 Renderizando Escena {idx:02d} ({dur:.2f}s / {dur_frames} frames)...")
    subprocess.run(
        [
            "npx", "remotion", "render", "src/index.ts", "HybridBF01Scene", str(frames_dir),
            "--sequence", "--image-format=jpeg", "--jpeg-quality=90", "--concurrency=2", "--quiet",
            f"--props={props}",
        ],
        cwd=str(STUDIO_DIR),
        check=True,
    )

    out_scene = ESCENAS_DIR / f"{SCENE_META[idx]}.mp4"
    subprocess.run(
        [
            FFMPEG, "-y", "-framerate", "30",
            "-i", str(frames_dir / "element-%04d.jpeg"),
            "-i", str(mix_wav),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
            "-crf", "18", "-preset", "medium", "-movflags", "+faststart",
            "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2", "-shortest",
            str(out_scene),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(frames_dir, ignore_errors=True)
    print(f"✅ Escena {idx:02d} lista: {out_scene}")
    return out_scene


def stitch_scenes(scene_files: List[Path]) -> None:
    concat_txt = WORK_DIR / "concat_list.txt"
    concat_txt.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in scene_files) + "\n",
        encoding="utf-8",
    )
    subprocess.run(
        [
            FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
            "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", str(FINAL_UNIDO),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    COLA_MP4.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FINAL_UNIDO, COLA_MP4)
    print(f"🎉 UNIDO FINAL ({probe_duration(FINAL_UNIDO):.2f}s): {FINAL_UNIDO}")
    print(f"📦 Copia cola OpusClip: {COLA_MP4}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-downloads", action="store_true")
    parser.add_argument("--scene", type=int, choices=[1, 2, 3, 4, 5, 6], help="Solo re-renderiza 1 escena y vuelve a unir")
    args = parser.parse_args()

    if args.from_downloads:
        import_from_downloads()

    target_indices = [args.scene] if args.scene else [1, 2, 3, 4, 5, 6]
    for idx in target_indices:
        render_single_scene(idx)

    all_scenes = [ESCENAS_DIR / f"{SCENE_META[i]}.mp4" for i in range(1, 7)]
    missing = [p for p in all_scenes if not p.exists()]
    if missing:
        print("ℹ️ Aún faltan escenas para unir todo:", [p.name for p in missing])
        return 0

    stitch_scenes(all_scenes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
