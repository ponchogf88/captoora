#!/usr/bin/env python3
"""
Auditor Automático Pre-Vuelo 0-3 s para Captoora Studio & ¡WATERS!.
Lee cola_semanal desde proyectos/tablero-control/data.js, extrae los fotogramas
t=0.0s, 0.5s, 1.5s, 3.0s, mide volumen 0-0.6s, visibilidad de Frame 0 y movimiento 0-1s,
y genera:
  - thumbs/hooks/hook_s{orden}.jpg  (tira 4x1)
  - hooks_audit.json
  - hooks_audit.js   (window.CAPTOORA_HOOKS_AUDIT para uso 100% compatible con file://)
"""
import json
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageChops, ImageDraw, ImageStat

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
TABLERO_DIR = ROOT / "proyectos/tablero-control"
DATA_JS = TABLERO_DIR / "data.js"
HOOKS_DIR = TABLERO_DIR / "thumbs/hooks"
OUT_JSON = TABLERO_DIR / "hooks_audit.json"
OUT_JS = TABLERO_DIR / "hooks_audit.js"

FFMPEG = "/Users/imac/.local/bin/ffmpeg"
FFPROBE = "/Users/imac/.local/bin/ffprobe"


def parse_cola_from_data_js(path: Path) -> List[Dict[str, str]]:
    """Extrae pares (orden, titulo, archivo_cola, source_mp4) de cola_semanal en data.js."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"cola_semanal\s*:\s*\[(.*?)\]\s*,\s*\n\s*mejoras_activas", text, re.S)
    if not m:
        raise RuntimeError("No se encontró bloque cola_semanal en data.js")
    block = m.group(1)

    slots: List[Dict[str, str]] = []
    for obj_m in re.finditer(r"\{([^{}]+)\}", block, re.S):
        chunk = obj_m.group(1)
        orden_m = re.search(r'orden\s*:\s*"([^"]+)"', chunk)
        src_m = re.search(r'source_mp4\s*:\s*"([^"]+)"', chunk)
        tit_m = re.search(r'titulo\s*:\s*"([^"]+)"', chunk)
        file_m = re.search(r'archivo_cola\s*:\s*"([^"]+)"', chunk)
        if orden_m and src_m:
            slots.append(
                {
                    "orden": orden_m.group(1),
                    "titulo": tit_m.group(1) if tit_m else "",
                    "archivo_cola": file_m.group(1) if file_m else "",
                    "source_mp4": src_m.group(1),
                }
            )
    return slots


def probe_duration(mp4_path: Path) -> float:
    out = subprocess.check_output(
        [
            FFPROBE,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(mp4_path),
        ],
        text=True,
    ).strip()
    return float(out)


def detect_audio_0_6s(mp4_path: Path) -> Tuple[Optional[float], Optional[float]]:
    """Mide mean_volume y max_volume en dB dentro de los primeros 0.6 segundos."""
    proc = subprocess.run(
        [
            FFMPEG,
            "-v",
            "info",
            "-i",
            str(mp4_path),
            "-t",
            "0.6",
            "-af",
            "volumedetect",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    stderr = proc.stderr or ""
    mean_m = re.search(r"mean_volume:\s*([-\d.]+)\s*dB", stderr)
    max_m = re.search(r"max_volume:\s*([-\d.]+)\s*dB", stderr)
    mean_db = float(mean_m.group(1)) if mean_m else None
    max_db = float(max_m.group(1)) if max_m else None
    return mean_db, max_db


def extract_frame(mp4_path: Path, t_sec: float, out_png: Path, width: int = 240) -> Image.Image:
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-ss",
            f"{t_sec:.2f}",
            "-i",
            str(mp4_path),
            "-frames:v",
            "1",
            "-vf",
            f"scale={width}:-2",
            str(out_png),
        ],
        check=True,
        capture_output=True,
    )
    return Image.open(out_png).convert("RGB")


def audit_slot(slot: Dict[str, str]) -> Dict[str, Any]:
    orden = slot["orden"]
    mp4_path = ROOT / slot["source_mp4"]
    if not mp4_path.exists():
        return {
            "orden": orden,
            "exists": False,
            "score": 0,
            "hook_estado": "Parchar 0-3s",
            "strip": None,
            "hook_notas": f"Archivo no encontrado: {slot['source_mp4']}",
        }

    dur = probe_duration(mp4_path)
    mean_db, max_db = detect_audio_0_6s(mp4_path)

    timestamps = [0.0, 0.5, 1.5, min(3.0, max(0.5, dur - 0.1))]
    labels = ["0.0s", "0.5s", "1.5s", "3.0s"]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        frames: List[Image.Image] = []
        for idx, ts in enumerate(timestamps):
            img = extract_frame(mp4_path, ts, tmp_dir / f"f_{idx}.png", width=240)
            frames.append(img)

        f1_0 = extract_frame(mp4_path, min(1.0, max(0.2, dur - 0.1)), tmp_dir / "f_1s.png", width=240)
        f2_0 = extract_frame(mp4_path, min(2.0, max(0.3, dur - 0.1)), tmp_dir / "f_2s.png", width=240)

        # Visibilidad Frame 0 (luminosidad y contraste / desviación estándar)
        g0 = frames[0].convert("L")
        stat0 = ImageStat.Stat(g0)
        frame0_luma = round(float(stat0.mean[0]), 1)
        frame0_std = round(float(stat0.stddev[0]), 1)

        # Movimiento 0 -> 1s y 0 -> 2s (diferencia promedio absoluta 0..255)
        diff01 = ImageChops.difference(frames[0], f1_0).convert("L")
        diff02 = ImageChops.difference(frames[0], f2_0).convert("L")
        motion_0_1s = round(float(ImageStat.Stat(diff01).mean[0]), 2)
        motion_0_2s = round(float(ImageStat.Stat(diff02).mean[0]), 2)

        # Ensamblar tira 4x1 uniforme (960 x tile_h) con etiqueta limpia de tiempo arriba
        tile_w = 240
        tile_h = max(im.height for im in frames)
        strip_img = Image.new("RGB", (tile_w * 4, tile_h), (14, 15, 20))
        draw = ImageDraw.Draw(strip_img)
        for idx, im in enumerate(frames):
            y_off = (tile_h - im.height) // 2
            x_off = idx * tile_w
            strip_img.paste(im, (x_off, y_off))
            draw.rectangle([x_off + 6, 6, x_off + 54, 24], fill=(15, 16, 22))
            draw.text((x_off + 12, 9), labels[idx], fill=(226, 232, 240))

        HOOKS_DIR.mkdir(parents=True, exist_ok=True)
        strip_rel = f"thumbs/hooks/hook_s{orden}.jpg"
        strip_img.save(TABLERO_DIR / strip_rel, "JPEG", quality=86)

    # Puntuación objetiva 0..100
    score = 0
    # 1) Audio inmediato (0 - 0.6s) -> 35 pts
    if max_db is not None and max_db > -18.0:
        audio_pts = 35
    elif max_db is not None and max_db > -30.0:
        audio_pts = 18
    else:
        audio_pts = 0
    score += audio_pts

    # 2) Visibilidad Frame 0.0s -> 35 pts (penaliza pantalla plana/vacía con std < 18)
    if frame0_std < 18.0:
        f0_pts = 0
    elif frame0_luma >= 32.0 or frame0_std >= 42.0:
        f0_pts = 35
    elif frame0_luma >= 18.0 or frame0_std >= 24.0:
        f0_pts = 18
    else:
        f0_pts = 0
    score += f0_pts

    # 3) Movimiento real en primer segundo -> 30 pts
    if motion_0_1s >= 4.0:
        mot_pts = 30
    elif motion_0_1s >= 1.5 or motion_0_2s >= 4.0:
        mot_pts = 15
    else:
        mot_pts = 0
    score += mot_pts

    if score >= 80:
        estado = "Listo 0-3s"
    elif score >= 55:
        estado = "Revisar 0-3s"
    else:
        estado = "Parchar 0-3s"

    max_txt = f"{max_db:.1f} dB" if max_db is not None else "sin audio"
    f0_txt = f"Y={frame0_luma:.0f}/std={frame0_std:.0f}"
    notas = f"Audio 0-0.6s: {max_txt} · Frame 0: {f0_txt} · Mov 0-1s: {motion_0_1s:.1f}"

    return {
        "orden": orden,
        "exists": True,
        "duration_s": round(dur, 2),
        "audio_mean_db": mean_db,
        "audio_max_db": max_db,
        "frame0_luma": frame0_luma,
        "frame0_std": frame0_std,
        "motion_0_1s": motion_0_1s,
        "motion_0_2s": motion_0_2s,
        "score": score,
        "hook_estado": estado,
        "strip": strip_rel,
        "hook_notas": notas,
    }


def main() -> int:
    slots = parse_cola_from_data_js(DATA_JS)
    results: Dict[str, Any] = {}
    print(f"Auditando {len(slots)} videos en cola (0-3 s Pre-Vuelo)...")
    print("-" * 96)
    for slot in slots:
        res = audit_slot(slot)
        results[slot["orden"]] = res
        print(
            f"S{slot['orden']} | {res['score']:3d}/100 | {res['hook_estado']:12s} | {res['hook_notas']} | {slot['titulo'][:42]}"
        )
    print("-" * 96)

    payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "slots": results,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    OUT_JS.write_text(
        "/* Generado automáticamente por scripts/auditar_cola_0_3s.py */\n"
        f"window.CAPTOORA_HOOKS_AUDIT = {json.dumps(payload, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    print(f"OK -> {OUT_JSON.name} + {OUT_JS.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
