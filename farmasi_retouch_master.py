#!/usr/bin/env python3
"""
Captoora Studio - Farmasi Master Retouch Engine (v3.0)
Diseñado para retrato de estudio en ciclorama blanco.
Resuelve:
1. Suavizado de arrugas y textura de tela en ciclorama sin 'look Mercado Libre'.
2. Preservación estricta de sombras de contacto en piso y tacones.
3. Respeto absoluto a transparencias, encajes (tul de lunares) y cabello rizado sin halos.
4. Curva tonal de retrato: brillo sedoso en piel y negros profundos sin empaste.
5. Exportación multi-formato: Alta Resolución (3:2), Redes (4:5) y Stories (9:16).
"""

import os
import sys
import glob
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

def process_studio_portrait(img_path, output_dir, base_name=None):
    os.makedirs(output_dir, exist_ok=True)
    dir_hq = os.path.join(output_dir, "01_Alta_Resolucion_Cliente")
    dir_4x5 = os.path.join(output_dir, "02_Redes_Instagram_4x5")
    dir_story = os.path.join(output_dir, "03_Stories_Reels_9x16")
    
    for d in (dir_hq, dir_4x5, dir_story):
        os.makedirs(d, exist_ok=True)
        
    if not base_name:
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        
    print(f"-> Procesando: {os.path.basename(img_path)}...")
    
    # 1. Cargar y normalizar orientación EXIF
    orig = Image.open(img_path)
    orig = ImageOps.exif_transpose(orig)
    w, h = orig.size
    
    img_bgr = cv2.cvtColor(np.array(orig.convert("RGB")), cv2.COLOR_RGB2BGR)
    
    # 2. Curva tonal en espacio LAB (Luminancia pura sin desplazar tonos de piel)
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Curva gamma suave (0.90) para levantar sombras y medios tonos (+0.3 EV) sin quemar
    x = np.arange(256, dtype=np.float32)
    curve = np.clip(255.0 * np.power(x / 255.0, 0.90), 0, 255).astype(np.uint8)
    l_tone = cv2.LUT(l, curve)
    
    base_bgr = cv2.cvtColor(cv2.merge((l_tone, a, b)), cv2.COLOR_LAB2BGR)
    
    # 3. Separación de frecuencias y detección de ciclorama
    # Ciclorama blanco: L alta (>150), croma baja (|a-128| < 15, |b-128| < 20)
    a_diff = np.abs(a.astype(int) - 128)
    b_diff = np.abs(b.astype(int) - 128)
    is_backdrop = (l > 145) & (a_diff < 16) & (b_diff < 22)
    
    # Protección de bordes: Erosionar máscara para que NUNCA toque la silueta del sujeto
    # En imágenes full resolution (6000x4000), radio de erosión proporcional
    k_size = max(25, int(min(w, h) * 0.015))
    if k_size % 2 == 0:
        k_size += 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k_size, k_size))
    backdrop_safe = cv2.erode(is_backdrop.astype(np.uint8), kernel)
    
    # Suavizado de arrugas de tela en ciclorama con bilateral + gaussian
    # Escala para velocidad y suavidad uniforme
    down_scale = 0.5 if max(w, h) > 3000 else 1.0
    if down_scale < 1.0:
        small_base = cv2.resize(base_bgr, (int(w * down_scale), int(h * down_scale)), interpolation=cv2.INTER_AREA)
        small_smooth = cv2.bilateralFilter(small_base, d=15, sigmaColor=60, sigmaSpace=60)
        small_smooth = cv2.GaussianBlur(small_smooth, (31, 31), 0)
        smooth_bg = cv2.resize(small_smooth, (w, h), interpolation=cv2.INTER_LINEAR)
    else:
        smooth_bg = cv2.bilateralFilter(base_bgr, d=21, sigmaColor=60, sigmaSpace=60)
        smooth_bg = cv2.GaussianBlur(smooth_bg, (31, 31), 0)
        
    # Añadir elevación sutil a la zona segura del ciclorama (+10 niveles)
    smooth_bg_lifted = cv2.add(smooth_bg, np.array([10, 10, 10], dtype=np.uint8))
    
    # Difuminado suave del borde de la máscara segura
    mask_blur_radius = max(15, int(k_size * 0.6))
    if mask_blur_radius % 2 == 0:
        mask_blur_radius += 1
    mask_feathered = cv2.GaussianBlur(backdrop_safe.astype(np.float32), (mask_blur_radius, mask_blur_radius), 0)
    mask_3c = np.repeat(mask_feathered[:, :, np.newaxis], 3, axis=2)
    
    # Fusión limpia: fondo suavizado en área segura; sujeto y transición 100% nítidos
    result_bgr = (smooth_bg_lifted * mask_3c + base_bgr * (1.0 - mask_3c)).astype(np.uint8)
    
    # 4. Polish final con PIL (Micro-nitidez y tono sedoso)
    result_pil = Image.fromarray(cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB))
    
    enhancer_sh = ImageEnhance.Sharpness(result_pil)
    result_pil = enhancer_sh.enhance(1.18)
    
    enhancer_col = ImageEnhance.Color(result_pil)
    result_pil = enhancer_col.enhance(1.04)
    
    # 5. Guardar 01: Alta Resolución (3:2)
    path_hq = os.path.join(dir_hq, f"FARMASI_{base_name}_HQ.jpg")
    result_pil.save(path_hq, quality=95, optimize=True)
    
    # 6. Guardar 02: Instagram Feed 4:5 (1080x1350 o proporcional)
    target_aspect = 4.0 / 5.0
    curr_aspect = w / float(h)
    if curr_aspect > target_aspect:
        crop_w = int(h * target_aspect)
        offset = (w - crop_w) // 2
        img_4x5 = result_pil.crop((offset, 0, offset + crop_w, h))
    else:
        crop_h = int(w / target_aspect)
        offset = (h - crop_h) // 2
        img_4x5 = result_pil.crop((0, offset, w, offset + crop_h))
        
    path_4x5 = os.path.join(dir_4x5, f"IG_{base_name}_4x5.jpg")
    img_4x5.save(path_4x5, quality=92, optimize=True)
    
    # 7. Guardar 03: Stories / Reels 9:16
    target_aspect_story = 9.0 / 16.0
    if curr_aspect > target_aspect_story:
        crop_w = int(h * target_aspect_story)
        offset = (w - crop_w) // 2
        img_story = result_pil.crop((offset, 0, offset + crop_w, h))
    else:
        crop_h = int(w / target_aspect_story)
        offset = (h - crop_h) // 2
        img_story = result_pil.crop((0, offset, w, offset + crop_h))
        
    path_story = os.path.join(dir_story, f"STORY_{base_name}_9x16.jpg")
    img_story.save(path_story, quality=90, optimize=True)
    
    print(f"✓ Guardado: {os.path.basename(path_hq)}, {os.path.basename(path_4x5)}, {os.path.basename(path_story)}")
    return {
        "hq": path_hq,
        "feed": path_4x5,
        "story": path_story
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 farmasi_retouch_master.py <archivo_o_directorio> <directorio_salida>")
        sys.exit(1)
        
    target = sys.argv[1]
    out_dir = sys.argv[2]
    
    if os.path.isfile(target):
        process_studio_portrait(target, out_dir)
    elif os.path.isdir(target):
        files = sorted(glob.glob(os.path.join(target, "*.JPG")) + glob.glob(os.path.join(target, "*.jpg")))
        print(f"Iniciando procesado por lotes de {len(files)} imágenes...")
        for f in files:
            process_studio_portrait(f, out_dir)
