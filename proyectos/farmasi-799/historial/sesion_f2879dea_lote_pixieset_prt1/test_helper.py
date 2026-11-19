#!/usr/bin/env python3
"""
Procesador exacto de 5 fotografías pendientes del bloque Vestido Cobrizo (799).
Aplica:
1. 100% preservación estricta de píxeles originales en personas, rostros, cabello,
   vestidos, zapatos, productos Farmasi/Nutriplus y tapete blanco de peluche.
2. Conservación de la caída natural y textura real de la tela blanca del estudio
   (incluyendo el relieve real de tela de DSC07738.JPG y sus sombras suaves).
3. Extensión continua de la tela blanca caída y del tapete de peluche blanco hacia
   los extremos laterales (eliminando paneles acústicos negros, mueble con espejo,
   pinzas, zoclo y piso lateral) con armonización de baja frecuencia (corregir.py)
   para cero costuras.
"""

import glob
import json
import os
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from scipy.ndimage import binary_dilation, binary_erosion, binary_fill_holes, gaussian_filter

BRAIN = "/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f"
SRC_DIR = "/Users/imac/Desktop/31 oct selection 1/FARMASI_799_SELECCION_JPG"
ORIG_DIR = os.path.join(BRAIN, "scratch/cobrizo_5_edit/originals_oriented")
OUT_DIR = os.path.join(BRAIN, "scratch/cobrizo_5_edit/final_5")
os.makedirs(OUT_DIR, exist_ok=True)


def load_oriented(path):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if im.width > im.height:
        im = im.rotate(90, expand=True)
    return im


def build_fabric_relief(target_size):
    """Extrae el relieve real de tela blanca caída desde DSC07738.JPG (Acabado D)."""
    ref = load_oriented(os.path.join(SRC_DIR, "DSC07738.JPG")).resize(target_size, Image.Resampling.LANCZOS)
    a = np.asarray(ref, dtype=np.float32)
    w, h = target_size
    patch = a[int(h * 0.055):int(h * 0.255), int(w * 0.14):int(w * 0.80)]
    tiled = np.tile(patch, (4, 2, 1))[:int(h * 0.72), :w]
    tex = Image.fromarray(np.clip(tiled, 0, 255).astype(np.uint8)).resize(
        (w, int(h * 0.72)), Image.Resampling.BICUBIC
    )
    t = np.asarray(tex, dtype=np.float32)
    low = np.asarray(
        tex.filter(ImageFilter.GaussianBlur(radius=max(12, int(min(w, h) * 0.022)))),
        dtype=np.float32,
    )
    # High-pass + medium-pass fabric folds so it looks like real hanging studio cloth
    very_low = np.asarray(
        tex.filter(ImageFilter.GaussianBlur(radius=max(45, int(min(w, h) * 0.065)))),
        dtype=np.float32,
    )
    relief = (t - low) * 1.45 + (low - very_low) * 0.85
    full = np.zeros((h, w, 3), dtype=np.float32)
    full[:int(h * 0.72)] = relief
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    env = np.clip((0.70 - yy) / 0.20, 0.0, 1.0)
    return full * env


def align_gen_to_orig(orig_rgb, gen_rgb):
    """Alinea la placa generada al tamaño exacto de la original usando SIFT + RANSAC o resize directo."""
    H, W = orig_rgb.shape[:2]
    # Resize first to same aspect
    gen_resized = cv2.resize(gen_rgb, (W, H), interpolation=cv2.INTER_LANCZOS4)
    # SIFT on 1600px working copy for speed and accuracy
    scale = 1600.0 / W
    w_s, h_s = 1600, int(round(H * scale))
    o_s = cv2.resize(orig_rgb, (w_s, h_s), interpolation=cv2.INTER_AREA)
    g_s = cv2.resize(gen_resized, (w_s, h_s), interpolation=cv2.INTER_AREA)

    sift = cv2.SIFT_create(nfeatures=6000)
    kp1, des1 = sift.detectAndCompute(cv2.cvtColor(g_s, cv2.COLOR_RGB2GRAY), None)
    kp2, des2 = sift.detectAndCompute(cv2.cvtColor(o_s, cv2.COLOR_RGB2GRAY), None)
    if des1 is None or des2 is None:
        return gen_resized
    matches = cv2.BFMatcher(cv2.NORM_L2).knnMatch(des1, des2, k=2)
    good = [m for m, n in matches if m.distance < 0.72 * n.distance]
    if len(good) < 20:
        return gen_resized
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2) / scale
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2) / scale
    M, _ = cv2.estimateAffinePartial2D(
        src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=4.0
    )
    if M is None:
        return gen_resized
    # Check if transform is close to identity
    if abs(M[0, 0] - 1.0) > 0.05 or abs(M[1, 1] - 1.0) > 0.05:
        return gen_resized
    return cv2.warpAffine(
        gen_resized, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT_101
    )


def build_clean_cloth_and_rug_plate(orig_u8, gen_u8_opt, scene_cfg, fabric_relief):
    """
    Construye el fondo de tela blanca caída real + tapete de peluche blanco continuo:
    - En el centro se conserva el 100% de la tela blanca original con sus caídas, pliegues
      y sombras reales proyectadas por las modelos.
    - En las orillas donde había paneles acústicos negros, mueble con espejo, pinzas o piso,
      reemplaza con extensión espejo de la propia tela blanca real + textura de caída de tela
      y extensión del tapete de peluche blanco inferior, armonizado sin costuras.
    """
    H, W = orig_u8.shape[:2]
    orig_f = orig_u8.astype(np.float32)

    # Coordenadas de la zona central limpia de la tela blanca en esta foto
    x_cloth_l = int(W * scene_cfg["cloth_left"])
    x_cloth_r = int(W * scene_cfg["cloth_right"])
    y_top_clean = int(H * scene_cfg["cloth_top"])
    y_rug_start = int(H * scene_cfg["rug_top"])

    # 1. Crear un lienzo base a partir de la imagen original reflejando la tela blanca real
    # hacia los lados izquierdo y derecho, y reflejando la tela superior hacia el techo.
    canvas = orig_f.copy()

    # Reflejar banda limpia izquierda de la tela hacia [0 : x_cloth_l]
    span_l = x_cloth_l
    src_l = canvas[:, x_cloth_l:x_cloth_l + span_l, :][:, ::-1, :]
    canvas[:, :x_cloth_l, :] = src_l

    # Reflejar banda limpia derecha de la tela hacia [x_cloth_r : W]
    span_r = W - x_cloth_r
    src_r = canvas[:, x_cloth_r - span_r:x_cloth_r, :][:, ::-1, :]
    canvas[:, x_cloth_r:, :] = src_r

    # Reflejar banda limpia superior de la tela hacia [0 : y_top_clean]
    if y_top_clean > 0:
        src_t = canvas[y_top_clean:y_top_clean * 2, :, :][::-1, :, :]
        canvas[:y_top_clean, :, :] = src_t

    # En la zona inferior (tapete de peluche), si hay esquina derecha/izquierda con mueble,
    # zoclo, taburete gris lateral o piso, rellenar desde el tapete de peluche real o desde gen_u8_opt
    if gen_u8_opt is not None:
        gen_f = gen_u8_opt.astype(np.float32)
        # Armonizar baja frecuencia de gen_f respecto a la tela real central antes de usarla
        # Calculamos el color promedio por fila en la zona de tela limpia de orig_f vs gen_f
        sample_x0 = int(W * 0.22)
        sample_x1 = int(W * 0.76)
        orig_row_mean = np.median(orig_f[:, sample_x0:sample_x1, :], axis=1, keepdims=True)
        gen_row_mean = np.median(gen_f[:, sample_x0:sample_x1, :], axis=1, keepdims=True)
        row_delta = gaussian_filter(orig_row_mean - gen_row_mean, sigma=(48, 1, 0))
        gen_harm = np.clip(gen_f + row_delta, 0, 255)

        # Inyectar el relieve real de tela caída (fabric_relief) sobre gen_harm en la zona de pared/tela
        gen_with_fabric = np.clip(gen_harm + fabric_relief * 1.15, 0, 255)
        canvas = gen_with_fabric
    else:
        # Para fotos sin gen_u8_opt (ej. DSC08425 2), construimos el fondo lateral 100% con
        # la propia tela real de la foto + tapete de peluche real inferior!
        # Limpiar cualquier sombra de personas reflejada en los laterales usando un perfil vertical suave
        # de la tela blanca real + relieve real de tela caída
        sample_l = orig_f[:, x_cloth_l:x_cloth_l + int(W * 0.06), :]
        sample_r = orig_f[:, x_cloth_r - int(W * 0.06):x_cloth_r, :]
        profile_l = gaussian_filter(np.percentile(sample_l, 75, axis=1, keepdims=True), sigma=(35, 1, 0))
        profile_r = gaussian_filter(np.percentile(sample_r, 75, axis=1, keepdims=True), sigma=(35, 1, 0))

        # Llenar pared lateral izquierda y derecha con el perfil luminoso real de la tela + pliegues reales
        wall_l = np.repeat(profile_l, x_cloth_l + int(W * 0.04), axis=1)
        wall_r = np.repeat(profile_r, (W - x_cloth_r) + int(W * 0.04), axis=1)
        canvas[:, :wall_l.shape[1], :] = wall_l
        canvas[:, W - wall_r.shape[1]:, :] = wall_r

        # Parte superior (techo sobre la tela): extender el tono de la tela superior
        top_prof = np.percentile(orig_f[y_top_clean:y_top_clean + int(H * 0.05), x_cloth_l:x_cloth_r, :], 80, axis=0, keepdims=True)
        top_prof = gaussian_filter(top_prof, sigma=(1, 40, 0))
        canvas[:y_top_clean + int(H * 0.02), x_cloth_l:x_cloth_r, :] = np.repeat(
            top_prof, y_top_clean + int(H * 0.02), axis=0
        )

        # Esquina inferior derecha/izquierda del tapete de peluche (donde estaba el puff gris lateral en 8425):
        # Tomamos parches reales de peluche blanco limpio de la parte inferior y los colocamos sin costura
        rug_patch = orig_f[int(H * 0.78):int(H * 0.96), int(W * 0.08):int(W * 0.30), :]
        # Reflejar para cubrir el lado derecho del tapete (x > 0.78, y > 0.62)
        rug_fill = cv2.resize(rug_patch[:, ::-1, :], (int(W * 0.26), int(H * 0.38)), interpolation=cv2.INTER_LANCZOS4)
        canvas[int(H * 0.62):, int(W * 0.74):, :] = rug_fill

        # Añadir el relieve real de tela caída en las zonas laterales y superiores
        canvas = np.clip(canvas + fabric_relief * 1.35, 0, 255)

    return canvas


print("Helper module syntax OK")
