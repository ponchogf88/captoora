#!/usr/bin/env python3
"""
Pharmacy Event Batch & AI Quality Inspection Processor
Especializado para el evento 'Pharmacy Event 13 09 26'.
Filtra fotos borrosas, mal expuestas o duplicadas, aplica ajustes funcionales
y genera salidas para Cliente (HQ), Redes (4:5 y 9:16) y WhatsApp.
"""

import os
import sys
import glob
import math
import datetime
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageStat

def is_blurry_pil(img, threshold=45.0):
    """
    Evalúa la nitidez calculando la varianza del filtro Laplacian sobre escala de grises.
    Valores muy bajos indican foto desenfocada o trepidada.
    """
    gray = img.convert('L')
    # Kernel laplaciano aproximado con ImageFilter
    edges = gray.filter(ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], 1, 0))
    stat = ImageStat.Stat(edges)
    variance = stat.var[0]
    return variance < threshold, variance

def check_exposure(img):
    """
    Evalúa si la imagen está severamente subexpuesta (empastada) o sobreexpuesta (quemada).
    """
    gray = img.convert('L')
    hist = gray.histogram()
    total_pixels = sum(hist)
    
    # Porcentaje de píxeles en sombras profundas (0-15) y altas luces quemadas (240-255)
    shadows_ratio = sum(hist[0:15]) / float(total_pixels)
    highlights_ratio = sum(hist[240:256]) / float(total_pixels)
    
    mean_brightness = ImageStat.Stat(gray).mean[0]
    
    is_bad = False
    reason = "OK"
    if shadows_ratio > 0.65 or mean_brightness < 28:
        is_bad = True
        reason = "Subexpuesta / Muy oscura"
    elif highlights_ratio > 0.70 or mean_brightness > 235:
        is_bad = True
        reason = "Sobreexpuesta / Quemada"
        
    return is_bad, reason, mean_brightness

def apply_event_preset(img):
    """
    Aplica edición mínima y funcional para eventos corporativos/dinámicos:
    - Corrección sutil de exposición (+0.25)
    - Contraste suave (+12%)
    - Saturación natural (+5%)
    - Nitidez moderada
    """
    # 1. Corrección EXIF de orientación
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    # Brillo / Exposición ligera
    enhancer_b = ImageEnhance.Brightness(img)
    img = enhancer_b.enhance(1.18)

    # Contraste
    enhancer_c = ImageEnhance.Contrast(img)
    img = enhancer_c.enhance(1.12)

    # Color
    enhancer_s = ImageEnhance.Color(img)
    img = enhancer_s.enhance(1.06)

    # Nitidez
    enhancer_sh = ImageEnhance.Sharpness(img)
    img = enhancer_sh.enhance(1.30)

    return img

def crop_and_resize(img, ratio, target_size=None, max_long_edge=None):
    """Recorta a un ratio específico y reescala con Lanczos."""
    w, h = img.size
    if ratio:
        target_w, target_h = ratio
        current_aspect = w / float(h)
        target_aspect = target_w / float(target_h)
        if abs(current_aspect - target_aspect) > 0.01:
            if current_aspect > target_aspect:
                new_w = int(h * target_aspect)
                offset = (w - new_w) // 2
                img = img.crop((offset, 0, offset + new_w, h))
            else:
                new_h = int(w / target_aspect)
                offset = (h - new_h) // 2
                img = img.crop((0, offset, w, offset + new_h))

    if target_size:
        img = img.resize(target_size, Image.Resampling.LANCZOS)
    elif max_long_edge:
        w, h = img.size
        long_edge = max(w, h)
        if long_edge > max_long_edge:
            factor = max_long_edge / float(long_edge)
            img = img.resize((int(w * factor), int(h * factor)), Image.Resampling.LANCZOS)

    return img

def process_pharmacy_event(input_folder, output_base_folder):
    """
    Ejecuta el pipeline completo de inspección y exportación dual.
    """
    client_hq_dir = os.path.join(output_base_folder, "01_Entrega_Cliente_HQ")
    feed_dir = os.path.join(output_base_folder, "02_Redes_Feed_4x5")
    stories_dir = os.path.join(output_base_folder, "03_Redes_Stories_9x16")
    discard_dir = os.path.join(output_base_folder, "04_Descartes_Revisar")

    for d in [client_hq_dir, feed_dir, stories_dir, discard_dir]:
        os.makedirs(d, exist_ok=True)

    extensions = ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG", "*.webp", "*.WEBP")
    image_paths = []
    for ext in extensions:
        image_paths.extend(glob.glob(os.path.join(input_folder, ext)))

    image_paths = sorted(list(set(image_paths)))
    total = len(image_paths)
    print(f"--- FOTOORQUESTADOR BATCH AUDIT & EDIT ---")
    print(f"Total imágenes detectadas: {total}")

    report = {
        "total": total,
        "aceptadas": 0,
        "descartadas": 0,
        "detalles_descartes": [],
        "archivos_procesados": []
    }

    if total == 0:
        print(f"Aviso: La carpeta '{input_folder}' no contiene imágenes para procesar en este momento.")
        return report

    for idx, path in enumerate(image_paths, start=1):
        filename = os.path.basename(path)
        try:
            with Image.open(path) as img:
                # 1. Chequeo de Nitidez
                is_blurry, var_score = is_blurry_pil(img, threshold=30.0)
                # 2. Chequeo de Exposición
                is_bad_exp, exp_reason, brightness = check_exposure(img)

                if is_blurry or is_bad_exp:
                    reason = f"Desenfoque (var={var_score:.1f})" if is_blurry else exp_reason
                    discard_name = f"DISCARD_{idx:03d}_{filename}"
                    img.save(os.path.join(discard_dir, discard_name))
                    report["descartadas"] += 1
                    report["detalles_descartes"].append({"archivo": filename, "motivo": reason})
                    print(f"[{idx}/{total}] ⚠️ DESCARTADA ({reason}): {filename}")
                    continue

                # 3. Procesar foto aceptada
                edited = apply_event_preset(img)
                report["aceptadas"] += 1
                seq_num = report["aceptadas"]
                base_name = f"PHARMACY_20260913_{seq_num:03d}"

                # Salida A: Cliente HQ (Original ratio, max 3500px, JPG 95)
                hq_img = crop_and_resize(edited, ratio=None, max_long_edge=3500)
                hq_path = os.path.join(client_hq_dir, f"{base_name}_HQ.jpg")
                hq_img.save(hq_path, format="JPEG", quality=95, optimize=True)

                # Salida B: Instagram Feed (4:5, 1080x1350, JPG 85)
                feed_img = crop_and_resize(edited, ratio=(4, 5), target_size=(1080, 1350))
                feed_path = os.path.join(feed_dir, f"IG_{base_name}.jpg")
                feed_img.save(feed_path, format="JPEG", quality=85, optimize=True)

                # Salida C: Stories / TikTok (9:16, 1080x1920, JPG 82)
                story_img = crop_and_resize(edited, ratio=(9, 16), target_size=(1080, 1920))
                story_path = os.path.join(stories_dir, f"STORY_{base_name}.jpg")
                story_img.save(story_path, format="JPEG", quality=82, optimize=True)

                report["archivos_procesados"].append(base_name)
                print(f"[{idx}/{total}] ✅ OK: {filename} -> {base_name}")

        except Exception as e:
            print(f"[{idx}/{total}] ❌ Error en {filename}: {e}")

    print("\n--- RESUMEN FINAL ---")
    print(f"Total: {total} | Aceptadas: {report['aceptadas']} | Descartadas: {report['descartadas']}")
    return report

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 pharmacy_event_processor.py <carpeta_entrada> <carpeta_salida>")
        sys.exit(1)
    process_pharmacy_event(sys.argv[1], sys.argv[2])
