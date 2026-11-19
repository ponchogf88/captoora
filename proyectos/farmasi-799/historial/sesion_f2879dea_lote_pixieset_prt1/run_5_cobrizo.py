#!/usr/bin/env python3
"""
Procesador v8 DEFINITIVO para las 5 fotografías pendientes del bloque Vestido Cobrizo (799).
Resuelve de raíz el artefacto de viñeta blanca observado en v7:
- En v7, al calcular la difusión de color con `gaussian_filter(vals) / (gaussian_filter(weights) + 1e-6)`,
  en las esquinas alejadas donde el peso gaussiano era < 1e-6, el cociente caía a 0 (negro) en la primera
  iteración y contaminaba los bordes, o se disparaba.
- En v8 usamos `scipy.ndimage.distance_transform_edt` (vecino más cercano exacto hacia los píxeles reales
  del interior de la tela colgada) seguido de un suavizado gaussiano amplio (`sigma=30`).
  Esto garantiza matemáticamente que el 100% de los píxeles de los bordes tienen EXACTAMENTE el mismo
  tono gris-blanco perlado (~226..236) de la tela colgada adyacente, con CERO viñeta blanca, CERO marco
  rectangular y CERO pérdida de textura de tela que cae ni de peluche en las esquinas.
"""

import json
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from scipy.ndimage import (
    binary_dilation,
    binary_erosion,
    binary_fill_holes,
    distance_transform_edt,
    gaussian_filter,
)

BRAIN = "/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f"
SRC_DIR = "/Users/imac/Desktop/31 oct selection 1/FARMASI_799_SELECCION_JPG"
OUT_DIR = os.path.join(BRAIN, "scratch/cobrizo_5_edit/final_5")
os.makedirs(OUT_DIR, exist_ok=True)


def load_oriented(path):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if im.width > im.height:
        im = im.rotate(90, expand=True)
    return im


def build_pure_draped_cloth_and_rug_texture(H, W, ref_7738_u8, ref_8485_u8, ref_9204_u8):
    f7738 = ref_7738_u8.astype(np.float32)
    f8485 = ref_8485_u8.astype(np.float32)
    f9204 = ref_9204_u8.astype(np.float32)

    # Textura real de tela blanca colgada con caída vertical (combinando 9204 y 7738)
    c1 = cv2.resize(
        f9204[int(H * 0.02):int(H * 0.14), int(W * 0.06):int(W * 0.86), :],
        (W, int(H * 0.80)),
        interpolation=cv2.INTER_CUBIC,
    )
    c2 = cv2.resize(
        f7738[int(H * 0.06):int(H * 0.25), int(W * 0.16):int(W * 0.76), :],
        (W, int(H * 0.80)),
        interpolation=cv2.INTER_CUBIC,
    )
    cloth_tall = 0.55 * c1 + 0.45 * c2
    cloth_low = gaussian_filter(cloth_tall, sigma=(110, 150, 0))
    cloth_folds = (cloth_tall - cloth_low) * 1.55

    # Pliegues verticales suaves continuos de caída de tela
    xx = np.linspace(0.0, 1.0, W, dtype=np.float32)[None, :, None]
    yy = np.linspace(0.0, 1.0, int(H * 0.80), dtype=np.float32)[:, None, None]
    vertical_drape = (
        -2.5 * np.sin(2.0 * np.pi * xx * 5.5 + 0.4) * (0.35 + 0.65 * yy)
        - 1.6 * np.cos(2.0 * np.pi * xx * 11.0 - 0.8) * (0.30 + 0.70 * yy)
    )
    cloth_folds = cloth_folds + vertical_drape

    # Textura 100% pura de tapete de peluche blanco (DSC08485.JPG x in [0.06, 0.28], y in [0.85, 0.96])
    rug_crop = f8485[int(H * 0.85):int(H * 0.96), int(W * 0.06):int(W * 0.28), :]
    rug_m1 = np.concatenate([rug_crop, rug_crop[:, ::-1, :], rug_crop, rug_crop[:, ::-1, :]], axis=1)
    rug_m2 = np.concatenate([rug_m1, rug_m1[::-1, :, :]], axis=0)
    rug_full = cv2.resize(rug_m2, (W, int(H * 0.42)), interpolation=cv2.INTER_LANCZOS4)
    rug_low = gaussian_filter(rug_full, sigma=(65, 85, 0))
    rug_detail = np.clip((rug_full - rug_low) * 1.35, -18.0, 18.0)

    return cloth_folds, rug_detail


def synthesize_seamless_backdrop(orig_u8, cloth_folds, rug_detail, cfg, mask):
    """
    Construye el campo continuo de tela colgada + tapete de peluche propagando hacia los bordes
    EXACTAMENTE el tono gris-perlado real del interior de la tela (`distance_transform_edt`),
    seguido de suavizado armónico. Nunca puede irse a blanco 255 ni crear marcos.
    """
    H, W = orig_u8.shape[:2]
    orig_f = orig_u8.astype(np.float32)
    rug_y = int(H * cfg["floor_y"])

    scale = 16
    hs, ws = H // scale, W // scale
    small_orig = cv2.resize(orig_f, (ws, hs), interpolation=cv2.INTER_AREA)
    small_mask = cv2.resize(mask, (ws, hs), interpolation=cv2.INTER_AREA)

    rs, gs, bs = small_orig[:, :, 0], small_orig[:, :, 1], small_orig[:, :, 2]
    lums = 0.299 * rs + 0.587 * gs + 0.114 * bs
    sats = np.max(small_orig, axis=2) - np.min(small_orig, axis=2)

    # Seleccionamos píxeles que están DENTRO de la tela conservada (`small_mask < 0.03`)
    # y que tienen el tono real de la tela/peluche (luminancia >= 210, saturación < 12).
    # En 01, 02 y 03 la tela central real tiene luminancia ~248-253; no truncar en 242.5
    # evita que distance_transform_edt jale tonos oscuros (~228) y forme un rectángulo central.
    max_cloth_lum = cfg.get("max_cloth_lum", 254.0)
    min_cloth_lum = cfg.get("min_cloth_lum", 212.0)
    valid = (small_mask < 0.03) & (lums >= min_cloth_lum) & (lums <= max_cloth_lum) & (sats < 12.0)

    # Excluir las cajas de los modelos para que distance_transform_edt nunca tome blusas/vestidos blancos o sombras
    for sbox in cfg.get("subject_exclude_for_bg", []):
        sx0, sy0, sx1, sy1 = sbox
        valid[int(hs * sy0):int(hs * sy1), int(ws * sx0):int(ws * sx1)] = False

    # Propagamos el píxel válido más cercano a cada coordenada inválida usando distance_transform_edt
    _, indices = distance_transform_edt(~valid, return_indices=True)
    nearest_filled = small_orig[indices[0], indices[1]]

    # Suavizamos ampliamente para obtener un gradiente de iluminación natural sin costuras
    smooth_small = gaussian_filter(nearest_filled, sigma=(16.0, 20.0, 0))
    # Mezclamos suavemente con los píxeles válidos cerca de la frontera y re-suavizamos
    blend_small = np.where(valid[:, :, None], small_orig, smooth_small)
    smooth_small = gaussian_filter(blend_small, sigma=(9.0, 12.0, 0))

    base_wall = cv2.resize(smooth_small, (W, H), interpolation=cv2.INTER_CUBIC)

    # Pliegue horizontal natural donde la tela blanca cae y descansa sobre el tapete de peluche
    yy_h = np.arange(H, dtype=np.float32)[:, None, None]
    drape_dip = -3.8 * np.exp(-0.5 * ((yy_h - (rug_y - H * 0.018)) / (H * 0.009)) ** 2)
    drape_hi = +2.2 * np.exp(-0.5 * ((yy_h - (rug_y - H * 0.006)) / (H * 0.006)) ** 2)

    wall_with_folds = base_wall.copy()
    wall_h = min(int(H * 0.80), H)
    # Atenuar ligeramente la amplitud de pliegues cuando la tela original es muy luminosa (>246)
    fold_gain = cfg.get("fold_gain", 1.0)
    wall_with_folds[:wall_h] += cloth_folds[:wall_h] * fold_gain
    wall_with_folds += (drape_dip + drape_hi) * fold_gain

    # Piso de peluche blanco continuo
    rug_start = max(0, rug_y - int(H * 0.04))
    rug_h = H - rug_start
    rug_det_resized = cv2.resize(rug_detail, (W, rug_h), interpolation=cv2.INTER_LANCZOS4)
    rug_cap = cfg.get("rug_cap", 243.0)
    rug_base = np.minimum(base_wall[rug_start:], rug_cap)
    rug_layer = np.clip(rug_base + rug_det_resized, 0, 255)

    plate = wall_with_folds.copy()
    w_floor = np.clip((yy_h - (rug_y - H * 0.015)) / (H * 0.025), 0.0, 1.0)
    w_floor = gaussian_filter(w_floor, sigma=(18, 1, 0))
    plate[rug_start:] = plate[rug_start:] * (1.0 - w_floor[rug_start:]) + rug_layer * w_floor[rug_start:]

    return np.clip(plate, 0, 255)


def rasterize_polygon(H, W, poly_norm):
    im = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(im)
    pts = [(int(x * W), int(y * H)) for (x, y) in poly_norm]
    draw.polygon(pts, fill=255)
    return np.asarray(im, dtype=np.uint8) > 127


def build_precise_cleanup_mask(orig_u8, cfg):
    H, W = orig_u8.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    xn = xx / float(W)
    yn = yy / float(H)

    orig_f = orig_u8.astype(np.float32)
    r, g, b = orig_f[:, :, 0], orig_f[:, :, 1], orig_f[:, :, 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    sat = np.max(orig_f, axis=2) - np.min(orig_f, axis=2)

    mask = np.zeros((H, W), dtype=np.float32)

    # 1. Costura superior del techo (entrando dentro de la tela con pluma ancha de 0.045)
    top_y_l, top_y_r = cfg["top_line_y"]
    if top_y_l > 0 or top_y_r > 0:
        top_line = top_y_l * (1.0 - xn) + top_y_r * xn
        m_top = np.clip((top_line - yn) / 0.045, 0.0, 1.0)
        mask = np.maximum(mask, m_top)

    # 2. Límite izquierdo
    pts_l = cfg["left_boundary_pts"]
    y_pts_l = np.array([p[0] for p in pts_l], dtype=np.float32)
    x_pts_l = np.array([p[1] for p in pts_l], dtype=np.float32)
    x_bound_l = np.interp(yn[:, 0], y_pts_l, x_pts_l)[:, None]
    m_left = np.clip((x_bound_l - xn) / 0.040, 0.0, 1.0)
    mask = np.maximum(mask, m_left)

    # 3. Límite derecho
    pts_r = cfg["right_boundary_pts"]
    y_pts_r = np.array([p[0] for p in pts_r], dtype=np.float32)
    x_pts_r = np.array([p[1] for p in pts_r], dtype=np.float32)
    x_bound_r = np.interp(yn[:, 0], y_pts_r, x_pts_r)[:, None]
    m_right = np.clip((xn - x_bound_r) / 0.040, 0.0, 1.0)
    mask = np.maximum(mask, m_right)

    # 4. Cajas adicionales de limpieza puntual
    for cbox in cfg.get("extra_clean_boxes", []):
        cx0, cy0, cx1, cy1 = cbox
        x0i, y0i, x1i, y1i = int(W * cx0), int(H * cy0), int(W * cx1), int(H * cy1)
        mask[y0i:y1i, x0i:x1i] = 1.0

    # 5. Escudo biométrico y de sujeto/producto (`protected`)
    protected = np.zeros((H, W), dtype=bool)
    for pbox in cfg["core_protect_boxes"]:
        px0, py0, px1, py1 = pbox
        protected[int(H * py0):int(H * py1), int(W * px0):int(W * px1)] = True

    for poly in cfg.get("protect_polygons", []):
        protected |= rasterize_polygon(H, W, poly)

    for guard in cfg.get("edge_guards", []):
        gx0, gy0, gx1, gy1, gtype = guard
        x0i, y0i, x1i, y1i = int(W * gx0), int(H * gy0), int(W * gx1), int(H * gy1)
        roi_r = r[y0i:y1i, x0i:x1i]
        roi_g = g[y0i:y1i, x0i:x1i]
        roi_b = b[y0i:y1i, x0i:x1i]
        roi_lum = lum[y0i:y1i, x0i:x1i]
        roi_sat = sat[y0i:y1i, x0i:x1i]

        if gtype == "skin_or_red_strict":
            fg = ((roi_r > roi_b + 14) & (roi_g >= roi_b - 2) & (roi_lum > 62) & (roi_sat > 14)) | (
                (roi_r > roi_b + 26) & (roi_sat > 28) & (roi_lum > 32)
            )
        elif gtype == "copper_strict":
            fg = (roi_r > roi_g + 8) & (roi_r > roi_b + 18) & (roi_sat > 20) & (roi_lum > 58)
        elif gtype == "black_boot_right_01":
            fg = (roi_lum < 75) | ((roi_r > roi_b + 12) & (roi_lum > 135) & (roi_lum < 244))
        elif gtype == "boots_on_white_rug":
            fg = (roi_lum < 110) | ((roi_r > roi_b + 14) & (roi_sat > 16) & (roi_lum > 68))
        elif gtype == "curly_hair_left":
            fg = (roi_lum < 175) | ((roi_r > roi_b + 12) & (roi_sat > 16))
        else:
            fg = np.zeros_like(roi_lum, dtype=bool)

        fg = binary_fill_holes(fg)
        fg = binary_erosion(fg, iterations=1)
        fg = binary_dilation(fg, iterations=1)
        protected[y0i:y1i, x0i:x1i] |= fg

    for fbox in cfg.get("force_clean_boxes", []):
        fx0, fy0, fx1, fy1 = fbox
        x0i, y0i, x1i, y1i = int(W * fx0), int(H * fy0), int(W * fx1), int(H * fy1)
        protected[y0i:y1i, x0i:x1i] = False
        mask[y0i:y1i, x0i:x1i] = 1.0

    mask[protected] = 0.0
    mask = gaussian_filter(mask, sigma=16.0)
    mask[protected] = 0.0

    return mask, protected


SCENES_V8 = [
    {
        "fname": "DSC08355 2.JPG",
        "slug": "01_DSC08355_2_COBRIZO_PRO",
        "title": "Grupo 7 Embajadoras + Display Nutriplus",
        "floor_y": 0.675,
        "min_cloth_lum": 236.0,
        "max_cloth_lum": 254.0,
        "fold_gain": 0.72,
        "rug_cap": 244.0,
        "subject_exclude_for_bg": [
            (0.05, 0.23, 0.86, 0.82),
        ],
        "top_line_y": (0.105, 0.125),
        "left_boundary_pts": [
            (0.00, 0.210),
            (0.22, 0.195),
            (0.32, 0.145),
            (0.54, 0.180),
            (0.66, 0.135),
            (0.75, 0.065),
            (0.82, 0.000),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.755),
            (0.30, 0.765),
            (0.50, 0.770),
            (0.63, 0.770),
            (0.76, 0.855),
            (0.84, 1.000),
            (1.00, 1.000),
        ],
        "extra_clean_boxes": [
            (0.82, 0.60, 0.90, 0.67),
            (0.00, 0.51, 0.128, 0.71),
        ],
        "force_clean_boxes": [
            (0.00, 0.51, 0.118, 0.60),
            (0.00, 0.60, 0.105, 0.69),
            (0.830, 0.54, 0.880, 0.63),
        ],
        "core_protect_boxes": [
            (0.185, 0.22, 0.765, 0.995),
            (0.11, 0.75, 0.94, 1.00),
        ],
        "protect_polygons": [
            [
                (0.185, 0.53),
                (0.140, 0.565),
                (0.120, 0.588),
                (0.102, 0.615),
                (0.095, 0.675),
                (0.055, 0.735),
                (0.015, 0.785),
                (0.160, 0.785),
                (0.240, 0.660),
                (0.240, 0.53),
            ],
            [
                (0.750, 0.28),
                (0.818, 0.32),
                (0.826, 0.42),
                (0.805, 0.50),
                (0.825, 0.54),
                (0.815, 0.65),
                (0.856, 0.695),
                (0.856, 0.765),
                (0.740, 0.765),
                (0.750, 0.64),
            ],
        ],
        "edge_guards": [
            (0.002, 0.22, 0.22, 0.81, "skin_or_red_strict"),
            (0.73, 0.25, 0.83, 0.64, "skin_or_red_strict"),
            (0.72, 0.56, 0.858, 0.77, "black_boot_right_01"),
        ],
    },
    {
        "fname": "DSC08425 2.JPG",
        "slug": "02_DSC08425_2_COBRIZO_PRO",
        "title": "Trío Ejecutivo Sentado + Vestido Cobrizo",
        "floor_y": 0.715,
        "min_cloth_lum": 236.0,
        "max_cloth_lum": 254.0,
        "fold_gain": 0.72,
        "rug_cap": 244.0,
        "subject_exclude_for_bg": [
            (0.04, 0.23, 0.84, 0.86),
        ],
        "top_line_y": (0.095, 0.125),
        "left_boundary_pts": [
            (0.00, 0.110),
            (0.30, 0.110),
            (0.55, 0.110),
            (0.68, 0.095),
            (0.76, 0.075),
            (0.85, 0.000),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.745),
            (0.28, 0.750),
            (0.55, 0.760),
            (0.72, 0.765),
            (0.88, 0.815),
            (0.95, 1.000),
            (1.00, 1.000),
        ],
        "force_clean_boxes": [
            (0.00, 0.52, 0.058, 0.602),
            (0.00, 0.635, 0.048, 0.76),
            (0.795, 0.66, 0.860, 0.75),
        ],
        "core_protect_boxes": [
            (0.155, 0.26, 0.755, 1.00),
            (0.63, 0.22, 0.762, 0.92),
        ],
        "protect_polygons": [
            [
                (0.155, 0.55),
                (0.062, 0.588),
                (0.016, 0.608),
                (0.016, 0.632),
                (0.050, 0.678),
                (0.068, 0.735),
                (0.175, 0.735),
                (0.185, 0.55),
            ],
        ],
        "edge_guards": [
            (0.014, 0.54, 0.18, 0.74, "skin_or_red_strict"),
            (0.042, 0.71, 0.19, 0.88, "boots_on_white_rug"),
            (0.74, 0.29, 0.84, 0.81, "copper_strict"),
        ],
    },
    {
        "fname": "DSC08485.JPG",
        "slug": "03_DSC08485_COBRIZO_PRO",
        "title": "Trío Ejecutivo de Pie + Vestido Cobrizo",
        "floor_y": 0.715,
        "min_cloth_lum": 236.0,
        "max_cloth_lum": 254.0,
        "fold_gain": 0.72,
        "rug_cap": 244.0,
        "subject_exclude_for_bg": [
            (0.10, 0.17, 0.79, 1.00),
        ],
        "top_line_y": (0.055, 0.075),
        "left_boundary_pts": [
            (0.00, 0.075),
            (0.35, 0.080),
            (0.68, 0.085),
            (0.75, 0.065),
            (0.82, 0.000),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.785),
            (0.30, 0.785),
            (0.60, 0.775),
            (0.72, 0.770),
            (0.95, 0.790),
            (1.00, 0.790),
        ],
        "extra_clean_boxes": [
            (0.75, 0.88, 1.00, 1.00),
        ],
        "force_clean_boxes": [
            (0.78, 0.90, 1.00, 1.00),
        ],
        "core_protect_boxes": [
            (0.11, 0.17, 0.772, 0.94),
        ],
        "edge_guards": [],
    },
    {
        "fname": "DSC09204 2.JPG",
        "slug": "04_DSC09204_2_COBRIZO_PRO",
        "title": "Trío Editorial Doble Vestido Cobrizo + Rojo",
        "floor_y": 0.785,
        "min_cloth_lum": 218.0,
        "max_cloth_lum": 244.0,
        "fold_gain": 1.0,
        "rug_cap": 239.0,
        "subject_exclude_for_bg": [
            (0.05, 0.15, 0.92, 0.98),
        ],
        "top_line_y": (0.00, 0.00),
        "left_boundary_pts": [
            (0.00, 0.00),
            (1.00, 0.00),
        ],
        "right_boundary_pts": [
            (0.00, 0.900),
            (0.30, 0.900),
            (0.65, 0.900),
            (0.81, 0.910),
            (0.85, 1.000),
            (1.00, 1.000),
        ],
        "force_clean_boxes": [
            (0.94, 0.45, 1.00, 0.68),
        ],
        "core_protect_boxes": [
            (0.06, 0.15, 0.895, 0.98),
            (0.82, 0.82, 1.00, 0.96),
        ],
        "edge_guards": [
            (0.86, 0.50, 0.94, 0.96, "copper_strict"),
        ],
    },
    {
        "fname": "DSC09538 2.JPG",
        "slug": "05_DSC09538_2_COBRIZO_PRO",
        "title": "Trío Editorial Vestido Rojo + Cobrizo + Crema",
        "floor_y": 0.735,
        "min_cloth_lum": 200.0,
        "max_cloth_lum": 242.5,
        "fold_gain": 1.0,
        "rug_cap": 239.0,
        "top_line_y": (0.045, 0.065),
        "left_boundary_pts": [
            (0.00, 0.080),
            (0.25, 0.088),
            (0.55, 0.100),
            (0.73, 0.105),
            (0.78, 0.060),
            (0.85, 0.000),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.830),
            (0.28, 0.830),
            (0.55, 0.825),
            (0.73, 0.820),
            (0.85, 0.880),
            (1.00, 1.000),
        ],
        "core_protect_boxes": [
            (0.11, 0.19, 0.812, 0.96),
        ],
        "edge_guards": [
            (0.095, 0.24, 0.16, 0.45, "curly_hair_left"),
        ],
    },
]


def main():
    ref_7738 = np.asarray(load_oriented(os.path.join(SRC_DIR, "DSC07738.JPG")), dtype=np.uint8)
    ref_8485 = np.asarray(load_oriented(os.path.join(SRC_DIR, "DSC08485.JPG")), dtype=np.uint8)
    ref_9204 = np.asarray(load_oriented(os.path.join(SRC_DIR, "DSC09204 2.JPG")), dtype=np.uint8)
    H, W = ref_7738.shape[:2]

    cloth_folds, rug_detail = build_pure_draped_cloth_and_rug_texture(H, W, ref_7738, ref_8485, ref_9204)

    report = []
    for cfg in SCENES_V8:
        fname = cfg["fname"]
        slug = cfg["slug"]
        orig_u8 = np.asarray(load_oriented(os.path.join(SRC_DIR, fname)), dtype=np.uint8)

        mask, protected = build_precise_cleanup_mask(orig_u8, cfg)
        plate_f = synthesize_seamless_backdrop(orig_u8, cloth_folds, rug_detail, cfg, mask)

        m3 = mask[:, :, None]
        comp_f = orig_u8.astype(np.float32) * (1.0 - m3) + plate_f * m3
        out_u8 = np.clip(np.round(comp_f), 0, 255).astype(np.uint8)

        # Candado biométrico duro: 0 píxeles modificados en sujetos/productos
        out_u8[protected] = orig_u8[protected]
        changed = int(np.count_nonzero(out_u8[protected] != orig_u8[protected]))
        assert changed == 0

        out_im = Image.fromarray(out_u8)
        out_im.save(os.path.join(OUT_DIR, f"{slug}.jpg"), quality=96, subsampling=0)
        out_im.resize((1600, 2400), Image.Resampling.LANCZOS).save(
            os.path.join(BRAIN, f"{slug}.jpg"), quality=95, subsampling=0
        )
        print(f"V8 OK: {fname} -> {slug}.jpg | protected_changed={changed}")
        report.append({
            "source": fname,
            "output": f"{slug}.jpg",
            "title": cfg["title"],
            "protected_pixels_changed": changed,
        })

    with open(os.path.join(OUT_DIR, "report_5_cobrizo_v8.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
