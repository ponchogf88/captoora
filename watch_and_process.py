#!/usr/bin/env python3
"""
Watcher & Auto-Processor para Pharmacy Event 13 09 26
Monitorea Downloads y la carpeta del proyecto.
En cuanto detecta el archivo ZIP o la carpeta descargada, ejecuta el lote completo.
"""

import os
import sys
import time
import glob
import zipfile
import subprocess

HOME_DIR = os.path.expanduser("~")
WATCH_DIRS = [
    os.path.join(HOME_DIR, "Downloads"),
    os.path.join(HOME_DIR, "Desktop/Projects/CAPTOORA.STUDIO"),
    os.path.join(HOME_DIR, "Desktop/Projects/PHOTOGRAFY - PHOTOOKIS APP")
]

WORKSPACE = os.path.join(HOME_DIR, "Desktop/Projects/CAPTOORA.STUDIO")
OUTPUT_DIR = os.path.join(WORKSPACE, "Entrega_Pharmacy_Event_130926")

def check_for_event_files():
    # Buscar ZIPs o carpetas
    for wdir in WATCH_DIRS:
        if not os.path.exists(wdir):
            continue
        
        # 1. Buscar archivos ZIP
        zips = glob.glob(os.path.join(wdir, "*Pharmacy*.zip")) + \
               glob.glob(os.path.join(wdir, "*photography*.zip")) + \
               glob.glob(os.path.join(wdir, "*13 09 26*.zip")) + \
               glob.glob(os.path.join(wdir, "*Event*.zip"))

        for z in zips:
            # Esperar a que termine de descargarse (no .crdownload)
            if os.path.exists(z + ".crdownload"):
                print(f"Descarga en progreso detectada: {z}...")
                return None, None

            size1 = os.path.getsize(z)
            time.sleep(1)
            size2 = os.path.getsize(z)
            if size1 == size2 and size1 > 100000: # Archivo estable
                print(f"📦 ¡Archivo ZIP detectado!: {z}")
                extract_path = os.path.join(WORKSPACE, "raw_photos_pharmacy")
                os.makedirs(extract_path, exist_ok=True)
                print(f"Descomprimiendo {z} en {extract_path}...")
                with zipfile.ZipFile(z, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                return extract_path, z

        # 2. Buscar carpetas ya descomprimidas
        subdirs = [os.path.join(wdir, d) for d in os.listdir(wdir) if os.path.isdir(os.path.join(wdir, d))]
        for d in subdirs:
            basename = os.path.basename(d).lower()
            if "pharmacy" in basename or ("13" in basename and "09" in basename and "event" in basename):
                # Verificar si contiene imágenes
                imgs = glob.glob(os.path.join(d, "*.jpg")) + glob.glob(os.path.join(d, "*.JPG"))
                if len(imgs) > 5:
                    print(f"📁 ¡Carpeta de fotos detectada con {len(imgs)} imágenes!: {d}")
                    return d, None

    return None, None

def run_pipeline(photo_dir):
    print("\n🚀 INICIANDO PROCESAMIENTO COMPLETO EN LOTE...")
    # 1. Procesador de Fotos
    processor = os.path.join(WORKSPACE, "pharmacy_event_processor.py")
    subprocess.run(["python3", processor, photo_dir, OUTPUT_DIR])

    # 2. Generador de Videos
    hq_dir = os.path.join(OUTPUT_DIR, "01_Entrega_Cliente_HQ")
    videos_dir = os.path.join(OUTPUT_DIR, "05_Videos_Recap")
    os.makedirs(videos_dir, exist_ok=True)
    video_tool = os.path.join(WORKSPACE, "video_creator.py")
    
    source_for_video = hq_dir if os.path.exists(hq_dir) and len(os.listdir(hq_dir)) > 0 else photo_dir
    print(f"\n🎬 Renderizando videos para TikTok (9:16) y YouTube (16:9)...")
    subprocess.run(["python3", video_tool, source_for_video, videos_dir])

    print(f"\n✨ ¡LOTE COMPLETADO CON ÉXITO!")
    print(f"Todos los archivos listos en: {OUTPUT_DIR}")

if __name__ == "__main__":
    print("Iniciando monitor automático para fotos de Pharmacy Event...")
    p_dir, z_file = check_for_event_files()
    if p_dir:
        run_pipeline(p_dir)
    else:
        print("Esperando la descarga desde el navegador...")
