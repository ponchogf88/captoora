#!/usr/bin/env python3
"""
CAPTOORA STUDIO — Extractor Automatizado Cámara Eufy S350 (Anker) + Artemis Android (ADB)
Diseñado para correr en el iMac 2015 (/Users/imac) y sincronizar con Google Drive
sin saturar los 256 GB de la MacBook Pro (/Users/user).

Funciones:
1. Conecta vía ADB al Xiaomi Redmi Note 8 (160305c5) con Artemis / Eufy Security.
2. Extrae únicamente los videos nuevos grabados por la cámara Eufy 24/7 hacia Google Drive.
3. Analiza con OpenCV los cuadros con movimiento real (Poncho acomodando el set, luces, ciclorama).
4. Recorta automáticamente a formato vertical 9:16 (1080x1920) para TikTok / Reels / Shorts
   y arma el Timelapse diario de detrás de cámaras (BTS).
"""
import os
import sys
import glob
import json
import shutil
import argparse
import datetime
import subprocess
from pathlib import Path

# Importar el resolvedor universal de rutas multi-equipo
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captoora_paths as cp

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


MANIFEST_PATH = cp.DRIVE_RECAP_CAMARAS / "eufy_extracted_manifest.json"


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        try:
            return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"extracted_files": {}, "processed_reels": [], "last_run": None}


def save_manifest(data: dict):
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["last_run"] = datetime.datetime.now().isoformat()
    MANIFEST_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_adb_connection() -> dict:
    """Verifica si adb está instalado y si el Xiaomi Redmi Note 8 (160305c5) está conectado."""
    adb_bin = shutil.which("adb")
    if not adb_bin:
        for candidate in [
            "/opt/homebrew/bin/adb",
            "/usr/local/bin/adb",
            str(cp.HOME / "Library/Android/sdk/platform-tools/adb"),
        ]:
            if os.path.exists(candidate):
                adb_bin = candidate
                break

    if not adb_bin:
        return {"adb_available": False, "devices": [], "target_connected": False, "adb_bin": None}

    try:
        res = subprocess.run([adb_bin, "devices"], capture_output=True, text=True, timeout=8)
        lines = [l.strip() for l in res.stdout.splitlines()[1:] if l.strip() and "\t" in l]
        devices = [l.split("\t")[0] for l in lines if "device" in l.split("\t")[1]]
        target_ok = (cp.ADB_DEVICE_SERIAL in devices) or (len(devices) > 0)
        return {
            "adb_available": True,
            "adb_bin": adb_bin,
            "devices": devices,
            "target_connected": target_ok,
            "active_device": cp.ADB_DEVICE_SERIAL if cp.ADB_DEVICE_SERIAL in devices else (devices[0] if devices else None),
        }
    except Exception as e:
        return {"adb_available": True, "adb_bin": adb_bin, "devices": [], "target_connected": False, "error": str(e)}


def pull_new_eufy_videos_via_adb(adb_info: dict, manifest: dict) -> list:
    """Extrae vía ADB los videos MP4 nuevos de las carpetas de Eufy en el Android conectado."""
    if not adb_info.get("target_connected"):
        return []

    adb_bin = adb_info["adb_bin"]
    device = adb_info["active_device"]
    cp.DRIVE_EUFY_INPUT.mkdir(parents=True, exist_ok=True)
    pulled = []

    for remote_dir in cp.ANDROID_EUFY_DIRS:
        cmd = [adb_bin, "-s", device, "shell", f"find '{remote_dir}' -type f -name '*.mp4' 2>/dev/null"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            remote_files = [l.strip() for l in res.stdout.splitlines() if l.strip().endswith(".mp4")]
            for rfile in remote_files:
                # Filtrar solo videos de Eufy o cámara si viene de /sdcard/Download
                fname = os.path.basename(rfile)
                if remote_dir == "/sdcard/Download" and not any(k in fname.lower() for k in ("eufy", "anker", "cam", "s350", "cpt", "2026")):
                    continue
                if rfile in manifest["extracted_files"]:
                    continue

                local_dst = cp.DRIVE_EUFY_INPUT / fname
                pull_cmd = [adb_bin, "-s", device, "pull", rfile, str(local_dst)]
                pr = subprocess.run(pull_cmd, capture_output=True, text=True, timeout=120)
                if pr.returncode == 0 and local_dst.exists():
                    manifest["extracted_files"][rfile] = {
                        "local_path": str(local_dst),
                        "pulled_at": datetime.datetime.now().isoformat(),
                        "bytes": local_dst.stat().st_size,
                    }
                    pulled.append(local_dst)
                    print(f"[ADB EUFY] Extraído: {fname} ({local_dst.stat().st_size // 1024} KB)")
        except Exception as e:
            print(f"[ADB WARN] {remote_dir}: {e}")

    save_manifest(manifest)
    return pulled


def extract_active_motion_reel_9x16(video_path: Path, output_clip_path: Path, max_duration: float = 8.0) -> bool:
    """
    Analiza un video de la cámara Eufy S350 y extrae únicamente los cuadros donde hay movimiento real
    (Poncho acomodando el set, luces o ciclorama), recortando a vertical 9:16 (1080x1920).
    """
    if not HAS_CV2:
        print("[WARN] OpenCV (cv2) no disponible en este entorno.")
        return False

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return False

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        cap.release()
        return False

    # Recorte 9:16 centrado
    target_w = int(height * 9.0 / 16.0)
    if target_w > width:
        crop_x1, crop_x2 = 0, width
    else:
        crop_x1 = (width - target_w) // 2
        crop_x2 = crop_x1 + target_w

    max_frames = int(fps * max_duration)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_clip_path.parent.mkdir(parents=True, exist_ok=True)
    out = cv2.VideoWriter(str(output_clip_path), fourcc, fps, (1080, 1920))

    prev_gray = None
    saved_frames = 0
    motion_grace_frames = 0

    while cap.isOpened() and saved_frames < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        small = cv2.resize(frame, (320, 180))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (15, 15), 0)

        is_moving = False
        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            thresh = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY)[1]
            motion_ratio = np.count_nonzero(thresh) / float(thresh.size)
            if motion_ratio > 0.012:  # Umbral de persona acomodando el set
                is_moving = True
                motion_grace_frames = int(fps * 1.5)  # Mantener 1.5s de fluidez tras movimiento

        prev_gray = gray

        if is_moving or motion_grace_frames > 0:
            if motion_grace_frames > 0:
                motion_grace_frames -= 1
            cropped = frame[:, crop_x1:crop_x2]
            resized = cv2.resize(cropped, (1080, 1920), interpolation=cv2.INTER_AREA)
            out.write(resized)
            saved_frames += 1

    cap.release()
    out.release()

    # Si el video tenía menos de 1 segundo de acción real, descartar archivo vacío
    if saved_frames < int(fps * 1.0):
        if output_clip_path.exists():
            output_clip_path.unlink()
        return False

    return True


def run_pipeline(check_only: bool = False):
    cp.DRIVE_EUFY_INPUT.mkdir(parents=True, exist_ok=True)
    cp.DRIVE_EUFY_OUTPUT_REELS.mkdir(parents=True, exist_ok=True)
    legacy_input = cp.DRIVE_RECAP_CAMARAS / "INPUT_CLIPS"
    legacy_input.mkdir(parents=True, exist_ok=True)

    adb_info = check_adb_connection()
    manifest = load_manifest()

    status = {
        "machine_role": cp.MACHINE_ROLE,
        "adb_status": adb_info,
        "eufy_input_dir": str(cp.DRIVE_EUFY_INPUT),
        "eufy_output_reels_dir": str(cp.DRIVE_EUFY_OUTPUT_REELS),
        "previously_extracted_count": len(manifest.get("extracted_files", {})),
        "previously_processed_reels": len(manifest.get("processed_reels", [])),
    }

    if check_only:
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return

    # 1. Extraer nuevos videos vía ADB si el Android está conectado
    if adb_info.get("target_connected"):
        pull_new_eufy_videos_via_adb(adb_info, manifest)

    # 2. Procesar todos los clips en 01_CLIPS_CRUDOS_EUFY y en INPUT_CLIPS
    candidates = sorted(list(cp.DRIVE_EUFY_INPUT.glob("*.mp4")) + list(legacy_input.glob("*.mp4")))
    for vid in candidates:
        if vid.name in manifest["processed_reels"]:
            continue
        out_name = f"REEL_BTS_SET_{vid.stem}_9x16.mp4"
        out_path = cp.DRIVE_EUFY_OUTPUT_REELS / out_name
        print(f"[MOTION ENGINE] Analizando movimiento real en {vid.name}...")
        ok = extract_active_motion_reel_9x16(vid, out_path)
        manifest["processed_reels"].append(vid.name)
        if ok:
            print(f"[OK] Reel 9:16 generado: {out_path}")
        else:
            print(f"[SKIP] Sin movimiento relevante en {vid.name}")

    save_manifest(manifest)
    print(json.dumps(status, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extractor Eufy S350 + Artemis Android para Captoora Studio")
    parser.add_argument("--check", action="store_true", help="Verifica estado de rutas y conexión ADB")
    parser.add_argument("--auto", action="store_true", help="Ejecuta extracción ADB y recorte 9:16 automático")
    args = parser.parse_args()
    run_pipeline(check_only=args.check and not args.auto)
