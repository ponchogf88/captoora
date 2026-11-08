#!/usr/bin/env python3
"""
FotoOrquestador - In-Memory Streaming Batch & Video Processor
Procesa directamente desde los 3 archivos ZIP en RAM (aprovechando los 24 GB de RAM del iMac)
sin saturar el disco de 99% de capacidad.
"""

import os
import sys
import glob
import zipfile
import subprocess
from io import BytesIO
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageStat

WORKSPACE = "/Users/imac/Desktop/Projects/PHOTOGRAFY - PHOTOOKIS APP"
OUTPUT_DIR = os.path.join(WORKSPACE, "Entrega_Pharmacy_Event_130926")

def is_blurry_pil(img, threshold=25.0):
    try:
        # Miniatura rápida para chequeo de nitidez a alta velocidad
        small = img.resize((600, int(600 * img.size[1] / img.size[0])), Image.Resampling.BOX).convert('L')
        edges = small.filter(ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], 1, 0))
        stat = ImageStat.Stat(edges)
        var = stat.var[0]
        return var < threshold, var
    except Exception:
        return False, 100.0

def check_exposure(img):
    try:
        small = img.resize((300, int(300 * img.size[1] / img.size[0])), Image.Resampling.BOX).convert('L')
        hist = small.histogram()
        total_p = sum(hist)
        shadows_ratio = sum(hist[0:15]) / float(total_p)
        highlights_ratio = sum(hist[242:256]) / float(total_p)
        mean_b = ImageStat.Stat(small).mean[0]

        if shadows_ratio > 0.65 or mean_b < 26:
            return True, "Subexpuesta / Muy oscura", mean_b
        elif highlights_ratio > 0.72 or mean_b > 238:
            return True, "Sobreexpuesta / Quemada", mean_b
        return False, "OK", mean_b
    except Exception:
        return False, "OK", 128

def apply_adjustments(img):
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    # Exposición (+0.25 EV)
    img = ImageEnhance.Brightness(img).enhance(1.18)
    # Contraste (+12%)
    img = ImageEnhance.Contrast(img).enhance(1.12)
    # Saturación (+6%)
    img = ImageEnhance.Color(img).enhance(1.06)
    # Nitidez
    img = ImageEnhance.Sharpness(img).enhance(1.25)
    return img

def crop_and_resize(img, ratio, target_size=None, max_long_edge=None):
    w, h = img.size
    if ratio:
        target_w, target_h = ratio
        cur_aspect = w / float(h)
        tgt_aspect = target_w / float(target_h)
        if abs(cur_aspect - tgt_aspect) > 0.01:
            if cur_aspect > tgt_aspect:
                nw = int(h * tgt_aspect)
                off = (w - nw) // 2
                img = img.crop((off, 0, off + nw, h))
            else:
                nh = int(w / tgt_aspect)
                off = (h - nh) // 2
                img = img.crop((0, off, w, off + nh))

    if target_size:
        img = img.resize(target_size, Image.Resampling.LANCZOS)
    elif max_long_edge:
        w, h = img.size
        long_e = max(w, h)
        if long_e > max_long_edge:
            factor = max_long_edge / float(long_e)
            img = img.resize((int(w * factor), int(h * factor)), Image.Resampling.LANCZOS)
    return img

def run_in_memory_stream():
    zip_paths = [
        "/Users/imac/Downloads/FARMASI EVENT 13 09 2026 PHOTOSHOOT-20260913T225830Z-1-001.zip",
        "/Users/imac/Downloads/FARMASI EVENT 13 09 2026 PHOTOSHOOT-20260913T225830Z-1-002.zip",
        "/Users/imac/Downloads/FARMASI EVENT 13 09 2026 PHOTOSHOOT-20260913T225830Z-1-003.zip"
    ]

    hq_dir = os.path.join(OUTPUT_DIR, "01_Entrega_Cliente_HQ")
    feed_dir = os.path.join(OUTPUT_DIR, "02_Redes_Feed_4x5")
    stories_dir = os.path.join(OUTPUT_DIR, "03_Redes_Stories_9x16")
    discard_dir = os.path.join(OUTPUT_DIR, "04_Descartes_Revisar")

    for d in [hq_dir, feed_dir, stories_dir, discard_dir]:
        os.makedirs(d, exist_ok=True)

    # 1. Indexar todas las fotos de los 3 zips
    all_members = [] # (zip_path, member_info)
    for zp in zip_paths:
        if not os.path.exists(zp):
            print(f"Alerta: No se encontró {zp}")
            continue
        zf = zipfile.ZipFile(zp, 'r')
        for m in zf.infolist():
            if m.filename.lower().endswith(('.jpg', '.jpeg')) and not m.filename.startswith('__MACOSX'):
                all_members.append((zp, m))
        zf.close()

    # Ordenar cronológicamente por nombre de archivo DSC_####.JPG
    all_members.sort(key=lambda item: os.path.basename(item[1].filename))
    total = len(all_members)
    print(f"=== FOTOORQUESTADOR STREAM ENGINE ===")
    print(f"Total fotos indexadas en los 3 ZIPs: {total}")
    sys.stdout.flush()

    accepted = 0
    discarded = 0

    # Abrir manejadores de zip
    zip_handles = {zp: zipfile.ZipFile(zp, 'r') for zp in zip_paths if os.path.exists(zp)}

    try:
        for idx, (zp, member) in enumerate(all_members, start=1):
            fname = os.path.basename(member.filename)
            try:
                # Leer directamente en RAM
                data = zip_handles[zp].read(member)
                with Image.open(BytesIO(data)) as raw_img:
                    # 1. Auditoría IA
                    blurry, var_score = is_blurry_pil(raw_img)
                    bad_exp, exp_reason, _ = check_exposure(raw_img)

                    if blurry or bad_exp:
                        discarded += 1
                        reason = f"Desenfoque ({var_score:.1f})" if blurry else exp_reason
                        # Guardar thumbnail ligera de descarte
                        thumb = raw_img.copy()
                        thumb.thumbnail((800, 800))
                        thumb.save(os.path.join(discard_dir, f"DESC_{idx:03d}_{fname}"), quality=70)
                        print(f"[{idx}/{total}] ⚠️ DESCARTADA ({reason}): {fname}")
                        sys.stdout.flush()
                        continue

                    # 2. Ajustes funcionales
                    accepted += 1
                    seq = f"PHARMACY_20260913_{accepted:03d}"
                    edited = apply_adjustments(raw_img)

                    # Salida 1: Cliente HQ (max 2600px, JPG 92)
                    hq = crop_and_resize(edited, ratio=None, max_long_edge=2600)
                    hq.save(os.path.join(hq_dir, f"{seq}_HQ.jpg"), format="JPEG", quality=92, optimize=True)

                    # Salida 2: Instagram Feed (4:5, 1080x1350)
                    feed = crop_and_resize(edited, ratio=(4, 5), target_size=(1080, 1350))
                    feed.save(os.path.join(feed_dir, f"IG_{seq}.jpg"), format="JPEG", quality=85, optimize=True)

                    # Salida 3: Stories / Reels / TikTok (9:16, 1080x1920)
                    story = crop_and_resize(edited, ratio=(9, 16), target_size=(1080, 1920))
                    story.save(os.path.join(stories_dir, f"STORY_{seq}.jpg"), format="JPEG", quality=82, optimize=True)

                    if idx % 10 == 0 or idx == total:
                        print(f"[{idx}/{total}] ✅ Progreso: {accepted} fotos procesadas, {discarded} descartadas...")
                        sys.stdout.flush()

            except Exception as err:
                print(f"[{idx}/{total}] ❌ Error en {fname}: {err}")
                sys.stdout.flush()

    finally:
        for zh in zip_handles.values():
            zh.close()

    print("\n==========================================")
    print(f"🎉 ¡PROCESADO COMPLETADO!")
    print(f"Total: {total} | Aceptadas con éxito: {accepted} | Descartadas: {discarded}")
    print(f"Carpetas generadas en: {OUTPUT_DIR}")
    sys.stdout.flush()

    # 3. Compilación de videos
    print("\n🎬 GENERANDO VIDEOS CON FFMPEG...")
    sys.stdout.flush()
    video_out = os.path.join(OUTPUT_DIR, "05_Videos_Recap")
    os.makedirs(video_out, exist_ok=True)
    video_tool = os.path.join(WORKSPACE, "video_creator.py")
    subprocess.run(["python3", video_tool, hq_dir, video_out])
    print("✅ ¡Videos TikTok 9:16 y YouTube 16:9 generados!")
    sys.stdout.flush()

if __name__ == "__main__":
    run_in_memory_stream()
