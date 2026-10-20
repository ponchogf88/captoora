#!/usr/bin/env python3
"""
Captoora Studio - Event Photo Curator & Processor Engine
100% Local, Offline, Preservación Estricta de Sujetos y Entorno.
Optimizado para Apple Silicon Mac M1 (8GB RAM).
"""

import os
import sys
import json
import math
import glob
from pathlib import Path
from PIL import Image, ImageOps, ImageStat
import numpy as np
import cv2

# Rutas de modelos para análisis consultivo de rostro y ojos
LOCAL_CASCADE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cascades")
YUNET_MODEL = os.path.join(LOCAL_CASCADE_DIR, "face_detection_yunet.onnx")

yunet_detector = None
if os.path.exists(YUNET_MODEL) and hasattr(cv2, 'FaceDetectorYN_create'):
    try:
        yunet_detector = cv2.FaceDetectorYN_create(YUNET_MODEL, '', (300, 300), score_threshold=0.6)
    except Exception as e:
        yunet_detector = None

PRESETS = {
    "inicio_fresco": {
        "id": "inicio_fresco",
        "name": "Inicio Fresco (Día / Apertura)",
        "description": "Tonos limpios, sutil frialdad matutina, balance equilibrado de blancos y negros puros.",
        "temp": -6,          # -6 frío sutil
        "tint": 0,           # Neutro
        "exposure": 0.15,    # +0.15 EV
        "highlights": -15,   # -15 recuperación de altas luces
        "shadows": 12,       # +12 apertura de sombras
        "denoise": 5,        # 5% limpieza sutil
        "sharpness": 25      # Micro-contraste fino
    },
    "transicion_equilibrada": {
        "id": "transicion_equilibrada",
        "name": "Transición Equilibrada (Comercial / Natural)",
        "description": "Tono fiel a la realidad del evento, contraste orgánico, piel luminosa sin saturación excesiva.",
        "temp": 2,           # Neutro cálido orgánico
        "tint": 1,
        "exposure": 0.10,    # +0.10 EV
        "highlights": -10,
        "shadows": 15,       # +15 sombras abiertas
        "denoise": 5,
        "sharpness": 20
    },
    "final_calido": {
        "id": "final_calido",
        "name": "Final Cálido (Atardecer / Fiesta)",
        "description": "Atmósfera dorada envolvente para momentos nocturnos o cierres emotivos.",
        "temp": 14,          # +14 calidez dorada
        "tint": 2,           # Sutil magenta compensatorio
        "exposure": 0.18,    # +0.18 EV
        "highlights": -18,
        "shadows": 20,       # +20 sombras ricas
        "denoise": 10,
        "sharpness": 22
    }
}

def load_image_normalized(image_path, max_dim=None):
    """
    Carga la imagen respetando orientación EXIF.
    Opcionalmente redimensiona manteniendo relación de aspecto para uso ágil en memoria (M1 8GB).
    """
    with Image.open(image_path) as pil_img:
        pil_img = ImageOps.exif_transpose(pil_img)
        if pil_img.mode not in ("RGB", "L"):
            pil_img = pil_img.convert("RGB")
        
        w, h = pil_img.size
        if max_dim and max(w, h) > max_dim:
            scale = max_dim / float(max(w, h))
            new_size = (int(w * scale), int(h * scale))
            pil_img = pil_img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convertir a arreglo BGR de OpenCV
        rgb_arr = np.array(pil_img)
        if len(rgb_arr.shape) == 2:
            rgb_arr = cv2.cvtColor(rgb_arr, cv2.COLOR_GRAY2RGB)
        bgr_arr = cv2.cvtColor(rgb_arr, cv2.COLOR_RGB2BGR)
        return pil_img, bgr_arr

def compute_dhash(img_bgr, hash_size=8):
    """
    Calcula el difference hash (dHash) para detectar fotos en ráfaga / duplicadas.
    """
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hash_size + 1, hash_size), interpolation=cv2.INTER_AREA)
    diff = resized[:, 1:] > resized[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def hamming_distance(h1, h2):
    """Distancia de bits entre dos hashes."""
    return bin(h1 ^ h2).count("1")

def analyze_sharpness(img_bgr):
    """
    Calcula la varianza del filtro Laplaciano sobre escala de grises.
    Métrica de nitidez relativa:
    - > 120: Nítida / Excelente foco
    - 45 - 120: Nitidez moderada / Aceptable
    - 20 - 45: Suave / Posible movimiento leve (apta para expresiones espontáneas)
    - < 20: Desenfoque severo / Ópticamente irrecuperable sin inventar detalles
    """
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    variance = float(lap.var())
    
    if variance >= 100.0:
        label = "Nítida"
        badge = "success"
    elif variance >= 40.0:
        label = "Moderada"
        badge = "info"
    elif variance >= 20.0:
        label = "Suave / Movimiento leve"
        badge = "warning"
    else:
        label = "Desenfoque severo"
        badge = "danger"
        
    return {
        "score": round(variance, 1),
        "label": label,
        "badge": badge,
        "is_severely_blurred": variance < 20.0
    }

def analyze_exposure(img_bgr):
    """
    Analiza histograma de luminancia en espacio LAB para determinar exposición real.
    """
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l_channel = lab[:, :, 0]
    hist, _ = np.histogram(l_channel, bins=256, range=(0, 256))
    total_pixels = float(l_channel.size)
    
    shadows_ratio = float(np.sum(hist[0:15]) / total_pixels)
    highlights_ratio = float(np.sum(hist[240:256]) / total_pixels)
    mean_lum = float(np.mean(l_channel))
    
    if shadows_ratio > 0.60 or mean_lum < 32.0:
        label = "Subexpuesta / Oscura"
        badge = "warning"
    elif highlights_ratio > 0.65 or mean_lum > 225.0:
        label = "Sobreexpuesta / Altas luces quemadas"
        badge = "warning"
    else:
        label = "Equilibrada"
        badge = "success"
        
    return {
        "label": label,
        "badge": badge,
        "mean": round(mean_lum, 1),
        "shadows_percent": round(shadows_ratio * 100, 1),
        "highlights_percent": round(highlights_ratio * 100, 1)
    }

def analyze_eyes_and_faces(img_bgr):
    """
    Diagnóstico consultivo de rostros y parpadeos usando YuNet local (OpenCV).
    Nunca descarta automáticamente; solo orienta al humano.
    """
    if yunet_detector is None:
        return {"faces_detected": 0, "blink_suspected": False, "label": "Detector no disponible"}
    
    h, w, _ = img_bgr.shape
    scale = 1.0
    max_dim = 1000
    if max(w, h) > max_dim:
        scale = max_dim / float(max(w, h))
        sw, sh = int(w * scale), int(h * scale)
        small_bgr = cv2.resize(img_bgr, (sw, sh))
    else:
        sw, sh = w, h
        small_bgr = img_bgr
        
    try:
        yunet_detector.setInputSize((sw, sh))
        status, faces = yunet_detector.detect(small_bgr)
    except Exception:
        return {"faces_detected": 0, "blink_suspected": False, "label": "Error en detección"}

    if faces is None or len(faces) == 0:
        return {"faces_detected": 0, "blink_suspected": False, "label": "Sin rostros identificados"}

    faces_count = len(faces)
    gray = cv2.cvtColor(small_bgr, cv2.COLOR_BGR2GRAY)
    blink_suspected = False

    for face in faces:
        # Landmarks: [4,5]=right eye, [6,7]=left eye
        rex, rey = int(face[4]), int(face[5])
        lex, ley = int(face[6]), int(face[7])
        eye_box_radius = max(6, int(face[2] * 0.08))

        # Evaluar contraste y varianza en las regiones de ojos
        for (ex, ey) in [(rex, rey), (lex, ley)]:
            if 0 <= ey - eye_box_radius and ey + eye_box_radius < sh and 0 <= ex - eye_box_radius and ex + eye_box_radius < sw:
                patch = gray[ey - eye_box_radius : ey + eye_box_radius, ex - eye_box_radius : ex + eye_box_radius]
                # Si el rango dinámico del ojo es muy plano (ojo cerrado/párpado homogéneo)
                p_min, p_max = np.min(patch), np.max(patch)
                if (p_max - p_min) < 35:
                    blink_suspected = True
                    break
        if blink_suspected:
            break

    label = "Revisar posible parpadeo" if blink_suspected else f"{faces_count} rostro(s) claro(s)"
    return {
        "faces_detected": int(faces_count),
        "blink_suspected": blink_suspected,
        "label": label
    }

def build_adjustment_lut(exposure=0.0, highlights=0.0, shadows=0.0):
    """
    Construye una tabla de correspondencias (LUT) de 256 niveles para el canal L (Luminancia).
    - Preserva los extremos (0 y 255) sin artefactos.
    - exposure: Desplaza la curva tonal suavemente.
    - highlights: Comprime o expande el tercio superior (altas luces).
    - shadows: Levanta o profundiza el tercio inferior (sombras) sin deslavar el negro.
    """
    x = np.arange(256, dtype=np.float32) / 255.0
    
    # 1. Corrección de exposición como ganancia gamma suave
    gamma = 1.0 - (exposure * 0.45)
    gamma = np.clip(gamma, 0.4, 1.8)
    curva = np.power(x, gamma)
    
    # 2. Sombras: afecta rango 0 a 0.5
    if shadows != 0.0:
        shadow_weight = np.clip(1.0 - (curva / 0.5), 0.0, 1.0)
        # Atenuación cerca de 0 para proteger el punto negro
        black_protection = np.sin(np.clip(curva / 0.5, 0.0, 1.0) * np.pi)
        delta_shadows = (shadows / 100.0) * 0.25 * black_protection
        curva = np.clip(curva + delta_shadows, 0.0, 1.0)
        
    # 3. Altas luces: afecta rango 0.5 a 1.0
    if highlights != 0.0:
        highlight_weight = np.clip((curva - 0.5) / 0.5, 0.0, 1.0)
        # Atenuación cerca de 1.0 para suavidad
        delta_hl = (highlights / 100.0) * 0.25 * highlight_weight
        curva = np.clip(curva + delta_hl, 0.0, 1.0)
        
    lut = np.clip(curva * 255.0, 0, 255).astype(np.uint8)
    return lut

def apply_color_grading(img_bgr, settings):
    """
    Aplica el pipeline de revelado fotográfico:
    1. Balance de blancos (Temp / Tint) en RGB.
    2. Ajuste tonal fino (Exposición, Altas luces, Sombras) en canal L de LAB (protección total de piel).
    3. Reducción de ruido moderada (Bilateral en luminancia).
    4. Nitidez / Micro-contraste (Unsharp Masking no destructivo).
    """
    temp = float(settings.get("temp", 0))
    tint = float(settings.get("tint", 0))
    exposure = float(settings.get("exposure", 0.0))
    highlights = float(settings.get("highlights", 0.0))
    shadows = float(settings.get("shadows", 0.0))
    denoise = float(settings.get("denoise", 0))
    sharpness = float(settings.get("sharpness", 0))

    # --- PASO 1: BALANCE DE BLANCOS (RGB) ---
    result_bgr = img_bgr.astype(np.float32)
    # Temperatura: cálido suma Rojo y resta Azul; frío suma Azul y resta Rojo
    if temp != 0:
        factor_r = 1.0 + (temp * 0.005)
        factor_b = 1.0 - (temp * 0.005)
        result_bgr[:, :, 2] = np.clip(result_bgr[:, :, 2] * factor_r, 0, 255)
        result_bgr[:, :, 0] = np.clip(result_bgr[:, :, 0] * factor_b, 0, 255)

    # Tinte: magenta suma R y B, resta G; verde suma G
    if tint != 0:
        factor_g = 1.0 - (tint * 0.004)
        result_bgr[:, :, 1] = np.clip(result_bgr[:, :, 1] * factor_g, 0, 255)

    img_uint8 = np.clip(result_bgr, 0, 255).astype(np.uint8)

    # --- PASO 2: AJUSTE TONAL EN LAB (Luminancia pura, color intacto) ---
    lab = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    lut = build_adjustment_lut(exposure=exposure, highlights=highlights, shadows=shadows)
    l_adjusted = cv2.LUT(l, lut)

    # --- PASO 3: REDUCCIÓN DE RUIDO MODERADA ---
    if denoise > 0:
        # Filtro bilateral sobre la luminancia para preservar bordes finos
        d = 5
        sigma_color = int(denoise * 0.5) + 5
        sigma_space = int(denoise * 0.5) + 5
        l_adjusted = cv2.bilateralFilter(l_adjusted, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)

    # --- PASO 4: NITIDEZ / MICRO-CONTRASTE (Unsharp Masking) ---
    if sharpness > 0:
        # Desenfoque gaussiano para extraer alta frecuencia
        gaussian = cv2.GaussianBlur(l_adjusted, (0, 0), sigmaX=1.2)
        amount = (sharpness / 100.0) * 1.5
        # l_sharp = l_adjusted + amount * (l_adjusted - gaussian)
        diff = cv2.subtract(l_adjusted, gaussian)
        l_sharp = cv2.addWeighted(l_adjusted, 1.0, diff, amount, 0)
        l_final = np.clip(l_sharp, 0, 255).astype(np.uint8)
    else:
        l_final = l_adjusted

    lab_final = cv2.merge((l_final, a, b))
    final_bgr = cv2.cvtColor(lab_final, cv2.COLOR_LAB2BGR)
    return final_bgr

def generate_preview_and_metrics(image_path, cache_dir, settings=None):
    """
    Genera la miniatura optimizada de previsualización (1200px max)
    y calcula todas las métricas consultivas.
    """
    os.makedirs(cache_dir, exist_ok=True)
    file_id = Path(image_path).stem
    cache_thumb_raw = os.path.join(cache_dir, f"{file_id}_raw.jpg")
    cache_thumb_graded = os.path.join(cache_dir, f"{file_id}_graded.jpg")

    # Cargar versión optimizada para preview
    _, bgr_raw = load_image_normalized(image_path, max_dim=1200)

    # Métricas sobre el crudo
    sharpness_info = analyze_sharpness(bgr_raw)
    exposure_info = analyze_exposure(bgr_raw)
    eyes_info = analyze_eyes_and_faces(bgr_raw)
    dhash_val = compute_dhash(bgr_raw)

    # Guardar thumbnail crudo si no existe
    if not os.path.exists(cache_thumb_raw):
        cv2.imwrite(cache_thumb_raw, bgr_raw, [cv2.IMWRITE_JPEG_QUALITY, 85])

    # Aplicar settings actuales para el previsualizador Before/After
    effective_settings = settings or PRESETS["transicion_equilibrada"]
    bgr_graded = apply_color_grading(bgr_raw, effective_settings)
    cv2.imwrite(cache_thumb_graded, bgr_graded, [cv2.IMWRITE_JPEG_QUALITY, 85])

    return {
        "filename": os.path.basename(image_path),
        "path": image_path,
        "raw_thumb": cache_thumb_raw,
        "graded_thumb": cache_thumb_graded,
        "dhash": dhash_val,
        "sharpness": sharpness_info,
        "exposure": exposure_info,
        "eyes": eyes_info,
        "decision": "pending"  # "yes", "review", "no"
    }

def export_curated_batch(items, output_folder, recipe_settings, client_tag="EVENTO"):
    """
    Exporta las fotos seleccionadas con la receta aprobada.
    NUNCA modifica los originales. Procesa una imagen full-res a la vez (M1 8GB friendly).
    """
    os.makedirs(output_folder, exist_ok=True)
    out_approved = os.path.join(output_folder, "01_SELECCION_APROBADA")
    out_review = os.path.join(output_folder, "02_REVISAR_O_ESPONTANEAS")
    os.makedirs(out_approved, exist_ok=True)
    os.makedirs(out_review, exist_ok=True)

    report = {
        "fecha": str(np.datetime64('now')),
        "receta_aplicada": recipe_settings,
        "total_procesadas": 0,
        "aprobadas": 0,
        "para_revisar": 0,
        "archivos": []
    }

    for item in items:
        decision = item.get("decision", "pending")
        if decision not in ("yes", "review"):
            continue

        src_path = item["path"]
        base_name = Path(src_path).stem
        target_dir = out_approved if decision == "yes" else out_review

        # Procesar a resolución completa
        _, bgr_full = load_image_normalized(src_path, max_dim=None)
        bgr_graded = apply_color_grading(bgr_full, recipe_settings)

        out_filename = f"{client_tag}_{base_name}_EDITED.jpg"
        dest_path = os.path.join(target_dir, out_filename)
        cv2.imwrite(dest_path, bgr_graded, [cv2.IMWRITE_JPEG_QUALITY, 95])

        # Liberar memoria de imagen completa inmediatamente
        del bgr_full
        del bgr_graded

        report["total_procesadas"] += 1
        if decision == "yes":
            report["aprobadas"] += 1
        else:
            report["para_revisar"] += 1

        report["archivos"].append({
            "original": src_path,
            "destino": dest_path,
            "decision": decision
        })

    # Guardar reporte de auditoría
    with open(os.path.join(output_folder, "reporte_curaduria_evento.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report
