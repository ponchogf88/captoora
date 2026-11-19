#!/usr/bin/env python3
"""
CAPTOORA STUDIO — Universal Multi-Equipment Path Resolver (MacBook Pro 256GB <-> iMac 2015)
Detecta automáticamente en qué computadora está corriendo (/Users/user vs /Users/imac),
resuelve las rutas de Google Drive, iCloud/Desktop y el repositorio activo,
y protege el SSD de 256GB de la MacBook Pro.
"""
import os
import sys
import json
from pathlib import Path

HOME = Path.home()
USERNAME = HOME.name

# Identificación automática del equipo
if USERNAME == "imac":
    MACHINE_ROLE = "IMAC_2015_HEAVY_STATION"
elif USERNAME == "user":
    MACHINE_ROLE = "MACBOOK_PRO_256GB_LIGHT"
else:
    MACHINE_ROLE = f"MAC_STATION_{USERNAME.upper()}"

# Raíz del repositorio (resuelta dinámicamente desde la ubicación de este archivo)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Búsqueda automática de Google Drive montado
CLOUD_STORAGE = HOME / "Library" / "CloudStorage"
GOOGLE_DRIVE_ROOT = None
if CLOUD_STORAGE.exists():
    for d in sorted(CLOUD_STORAGE.iterdir()):
        if d.is_dir() and d.name.startswith("GoogleDrive-"):
            mi_unidad = d / "Mi unidad"
            if mi_unidad.exists():
                GOOGLE_DRIVE_ROOT = mi_unidad
                break
            my_drive = d / "My Drive"
            if my_drive.exists():
                GOOGLE_DRIVE_ROOT = my_drive
                break

if GOOGLE_DRIVE_ROOT is None:
    # Fallback estándar
    GOOGLE_DRIVE_ROOT = CLOUD_STORAGE / "GoogleDrive-lic.jagf87@gmail.com" / "Mi unidad"

# Rutas Maestras en Google Drive
DRIVE_AI_CAPTOORA = GOOGLE_DRIVE_ROOT / "PROJECTS" / "RESPALDOS_PROYECTOS" / "AI CAPTOORA"
DRIVE_ESTUDIO_CAPTOORA = GOOGLE_DRIVE_ROOT / "PROJECTS" / "ESTUDIO CAPTOORA"
DRIVE_STUDIO_CAPTURA = GOOGLE_DRIVE_ROOT / "PROJECTS" / "STUDIO.CAPTURA" / "CAPTURA"

# Portafolio y Cámara Eufy 24/7 en Google Drive
DRIVE_PORTAFOLIO = DRIVE_AI_CAPTOORA / "PORTAFOLIO"
DRIVE_PORTAFOLIO_AUTORIZADO_13 = DRIVE_AI_CAPTOORA / "PORTAFOLIO_AUTORIZADO_13_ALBUMES"
DRIVE_RECAP_CAMARAS = DRIVE_AI_CAPTOORA / "RECAP_DIARIO_CAMARAS"
DRIVE_EUFY_INPUT = DRIVE_RECAP_CAMARAS / "01_CLIPS_CRUDOS_EUFY"
DRIVE_EUFY_OUTPUT_REELS = DRIVE_RECAP_CAMARAS / "02_REELS_LISTOS_9x16"
DRIVE_HISTORICO = DRIVE_AI_CAPTOORA / "03_HISTORICO_Y_ARCHIVOS"

# Rutas dentro del Repositorio Maestro
REPO_HISTORICO = REPO_ROOT / "historico_y_archivos"
REPO_DATA = REPO_ROOT / "data"
REPO_PORTAFOLIO_JSON = REPO_DATA / "portafolio_13_albumes.json"
REPO_ASSETS_PORTAFOLIO = REPO_ROOT / "assets" / "media_jpg"

# Configuración ADB / Artemis / Cámara Eufy S350 (Xiaomi Redmi Note 8)
ADB_DEVICE_SERIAL = "160305c5"
ANDROID_EUFY_DIRS = [
    "/sdcard/DCIM/EufySecurity",
    "/sdcard/DCIM/eufySecurity",
    "/sdcard/Movies/EufySecurity",
    "/sdcard/Movies/eufySecurity",
    "/sdcard/Android/data/com.oceanwing.battery.cam/files",
    "/sdcard/Download/Eufy",
    "/sdcard/Download"
]


def get_environment_summary() -> dict:
    """Devuelve el diagnóstico completo de rutas y estado en la máquina actual."""
    return {
        "username": USERNAME,
        "home": str(HOME),
        "machine_role": MACHINE_ROLE,
        "repo_root": str(REPO_ROOT),
        "google_drive_root": str(GOOGLE_DRIVE_ROOT),
        "google_drive_mounted": GOOGLE_DRIVE_ROOT.exists(),
        "paths": {
            "drive_ai_captoora": str(DRIVE_AI_CAPTOORA),
            "drive_portafolio_original": str(DRIVE_PORTAFOLIO),
            "drive_portafolio_autorizado_13": str(DRIVE_PORTAFOLIO_AUTORIZADO_13),
            "drive_eufy_input": str(DRIVE_EUFY_INPUT),
            "drive_eufy_output_reels": str(DRIVE_EUFY_OUTPUT_REELS),
            "repo_historico": str(REPO_HISTORICO),
            "repo_portafolio_json": str(REPO_PORTAFOLIO_JSON),
        },
        "eufy_adb_device": ADB_DEVICE_SERIAL,
    }


if __name__ == "__main__":
    summary = get_environment_summary()
    print("=" * 72)
    print(f"CAPTOORA MULTI-HOST PATH RESOLVER · [{summary['machine_role']}]")
    print("=" * 72)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
