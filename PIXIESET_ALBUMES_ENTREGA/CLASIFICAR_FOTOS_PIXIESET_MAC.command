#!/bin/bash
cd "$(dirname "$0")"

echo "========================================================"
echo "  CAPTOORA STUDIO · ORGANIZADOR PIXIESET (macOS)"
echo "========================================================"

# 1. Clasificar cualquier foto o ZIP que ya esté en ~/Downloads o ~/Desktop
python3 PIXIESET_ALBUMES_ENTREGA/CLASIFICAR_FOTOS_DESCARGADAS.py

# 2. Abrir el Portal Visual y la carpeta en Finder
open ORGANIZADOR_PIXIESET_Y_GALERIAS_CAPTOORA.html
open PIXIESET_ALBUMES_ENTREGA

echo ""
echo "✅ Portal abierto en tu navegador y carpeta abierta en Finder."
echo "⏳ Vigilando tu carpeta ~/Downloads en tiempo real (puedes minimizar esta ventana)..."

# 3. Vigilar ~/Downloads en tiempo real en macOS
python3 -c '
import subprocess, sys, time
from pathlib import Path

downloads = Path.home() / "Downloads"
sorter = Path("PIXIESET_ALBUMES_ENTREGA/CLASIFICAR_FOTOS_DESCARGADAS.py").resolve()
seen = {}
while True:
    try:
        cur = {f.name: (f.stat().st_size, f.stat().st_mtime) for f in downloads.iterdir() if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png", ".zip")}
        if cur != seen and cur and not list(downloads.glob("*.crdownload")) and not list(downloads.glob("*.download")):
            subprocess.run([sys.executable, str(sorter)])
            seen = cur
    except Exception:
        pass
    time.sleep(2.5)
'
