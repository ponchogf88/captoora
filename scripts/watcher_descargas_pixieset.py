import subprocess
import sys
import time
from pathlib import Path

DOWNLOADS = Path(r"C:\Users\USUARIO\Downloads")
SORTER = Path(r"C:\Users\USUARIO\captoora\PIXIESET_ALBUMES_ENTREGA\CLASIFICAR_FOTOS_DESCARGADAS.py")

seen_state = {}

while True:
    try:
        current = {}
        for f in DOWNLOADS.iterdir():
            if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png", ".zip"):
                current[f.name] = (f.stat().st_size, f.stat().st_mtime)
        if current != seen_state and current:
            # Wait 1.5s to ensure write finished and no .crdownload active
            if not list(DOWNLOADS.glob("*.crdownload")):
                subprocess.run([sys.executable, str(SORTER)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                seen_state = current
    except Exception:
        pass
    time.sleep(2.5)
