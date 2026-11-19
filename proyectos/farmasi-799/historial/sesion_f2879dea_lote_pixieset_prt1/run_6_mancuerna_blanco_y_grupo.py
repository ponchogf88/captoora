#!/usr/bin/env python3
"""
Procesador Captoora Studio Retouch (V12) para las 6 fotografías en Fondo Blanco
(3 individuales + 3 grupales) de la Embajadora Mancuerna (Farmasi 799 - 31 de octubre).
"""

import os
import shutil
import cv2
import numpy as np
from PIL import Image
from scipy.ndimage import (
    binary_dilation,
    binary_erosion,
    binary_fill_holes,
    gaussian_filter,
)
import run_5_more_groups as base

BRAIN = "/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f"
SRC_DIR = "/Users/imac/Desktop/31 oct selection 1/FARMASI_799_SELECCION_JPG"
PENDIENTES_DIR = os.path.join(BRAIN, "scratch/cobrizo_5_edit/PENDIENTES_DE_APROBACION")
os.makedirs(PENDIENTES_DIR, exist_ok=True)


def build_mask_v12(orig_u8, cfg):
    H, W = orig_u8.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    xn = xx / float(W)
    yn = yy / float(H)

    orig_f = orig_u8.astype(np.float32)
    r, g, b = orig_f[:, :, 0], orig_f[:, :, 1], orig_f[:, :, 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    sat = np.max(orig_f, axis=2) - np.min(orig_f, axis=2)

    mask = np.zeros((H, W), dtype=np.float32)
    feather_w = cfg.get("feather_w", 0.045)

    # 1. Costura superior del techo
    top_y_l, top_y_r = cfg["top_line_y"]
    if top_y_l > 0 or top_y_r > 0:
        top_line = top_y_l * (1.0 - xn) + top_y_r * xn
        m_top = np.clip((top_line - yn) / feather_w, 0.0, 1.0)
        mask = np.maximum(mask, m_top)

    # 2. Límite izquierdo
    pts_l = cfg["left_boundary_pts"]
    y_pts_l = np.array([p[0] for p in pts_l], dtype=np.float32)
    x_pts_l = np.array([p[1] for p in pts_l], dtype=np.float32)
    x_bound_l = np.interp(yn[:, 0], y_pts_l, x_pts_l)[:, None]
    m_left = np.clip((x_bound_l - xn) / feather_w, 0.0, 1.0)
    mask = np.maximum(mask, m_left)

    # 3. Límite derecho
    pts_r = cfg["right_boundary_pts"]
    y_pts_r = np.array([p[0] for p in pts_r], dtype=np.float32)
    x_pts_r = np.array([p[1] for p in pts_r], dtype=np.float32)
    x_bound_r = np.interp(yn[:, 0], y_pts_r, x_pts_r)[:, None]
    m_right = np.clip((xn - x_bound_r) / feather_w, 0.0, 1.0)
    mask = np.maximum(mask, m_right)

    # 4. Cajas adicionales de limpieza puntual (con pluma suave)
    for cbox in cfg.get("extra_clean_boxes", []):
        cx0, cy0, cx1, cy1 = cbox
        x0i, y0i, x1i, y1i = int(W * cx0), int(H * cy0), int(W * cx1), int(H * cy1)
        box_m = np.zeros((H, W), dtype=np.float32)
        box_m[y0i:y1i, x0i:x1i] = 1.0
        box_m = gaussian_filter(box_m, sigma=36.0)
        mask = np.maximum(mask, np.clip(box_m * 1.35, 0.0, 1.0))

    # 5. Escudo biométrico y de sujeto/producto (`protected`)
    protected = np.zeros((H, W), dtype=bool)
    for pbox in cfg["core_protect_boxes"]:
        px0, py0, px1, py1 = pbox
        protected[int(H * py0):int(H * py1), int(W * px0):int(W * px1)] = True

    for poly in cfg.get("protect_polygons", []):
        protected |= base.rasterize_polygon(H, W, poly)

    for guard in cfg.get("edge_guards", []):
        gx0, gy0, gx1, gy1, gtype = guard
        x0i, y0i, x1i, y1i = int(W * gx0), int(H * gy0), int(W * gx1), int(H * gy1)
        roi_r = r[y0i:y1i, x0i:x1i]
        roi_g = g[y0i:y1i, x0i:x1i]
        roi_b = b[y0i:y1i, x0i:x1i]
        roi_lum = lum[y0i:y1i, x0i:x1i]
        roi_sat = sat[y0i:y1i, x0i:x1i]

        if gtype == "skin_or_red_strict":
            # Protege pierna cálida (r > b + 9 y lum > 135) o vestido rojo (r > b + 28), NUNCA pared oscura/zoclo gris (b > r y lum < 100)
            fg = ((roi_r >= roi_b + 9) & (roi_lum > 135)) | (
                (roi_r > roi_b + 28) & (roi_sat > 28) & (roi_lum > 35)
            )
        elif gtype == "blonde_hair_on_black_wall":
            fg = (roi_r > roi_b + 10) & (roi_sat > 10) & (roi_lum > 38)
        elif gtype == "lilac_sleeve_and_blonde_left":
            # Protege cabello rubio o manga lila (b >= g + 8 y lum > 115), NUNCA el zoclo gris verdoso (b < g) ni el panel negro
            fg = ((roi_r > roi_b + 10) & (roi_sat > 10) & (roi_lum > 38)) | (
                (roi_b >= roi_g + 8) & (roi_lum > 112)
            )
        elif gtype == "right_arm_and_jar_1730":
            # Protege brazo derecho cálido (r > b + 14 y lum > 75) o bote rosa Nutriplus (r > g + 10 y lum > 115)
            fg = ((roi_r > roi_b + 14) & (roi_lum > 72)) | ((roi_r > roi_g + 8) & (roi_lum > 115))
        elif gtype == "right_arm_strict_1730":
            # Protege únicamente la piel cálida del brazo derecho (r >= b + 18 y r >= g + 10), NUNCA la esquina beige de la pared
            fg = (roi_r >= roi_b + 18) & (roi_r >= roi_g + 10) & (roi_lum > 72)
        elif gtype == "purple_boxes_1736":
            # Protege las cajas moradas Nutriplus en primer plano (lum < 108 o b >= g + 5), NUNCA la loseta gris verdosa (lum in [112, 152] y g > b)
            fg = (roi_lum < 108) | ((roi_b >= roi_g + 5) & (roi_sat > 10))
        else:
            fg = np.zeros_like(roi_lum, dtype=bool)

        fg = binary_fill_holes(fg)
        fg = binary_erosion(fg, iterations=1)
        fg = binary_dilation(fg, iterations=2)
        protected[y0i:y1i, x0i:x1i] |= fg

    for fbox in cfg.get("force_clean_boxes", []):
        fx0, fy0, fx1, fy1 = fbox
        x0i, y0i, x1i, y1i = int(W * fx0), int(H * fy0), int(W * fx1), int(H * fy1)
        protected[y0i:y1i, x0i:x1i] = False
        mask[y0i:y1i, x0i:x1i] = 1.0

    # Re-aplicar edge_guards marcados como post_force_guards (para proteger piel sobre force_clean_boxes)
    for guard in cfg.get("post_force_guards", []):
        gx0, gy0, gx1, gy1, gtype = guard
        x0i, y0i, x1i, y1i = int(W * gx0), int(H * gy0), int(W * gx1), int(H * gy1)
        roi_r, roi_g, roi_b, roi_lum = r[y0i:y1i, x0i:x1i], g[y0i:y1i, x0i:x1i], b[y0i:y1i, x0i:x1i], lum[y0i:y1i, x0i:x1i]
        if gtype == "right_arm_strict_1730":
            fg = (roi_r >= roi_b + 18) & (roi_r >= roi_g + 10) & (roi_lum > 72)
            fg = binary_dilation(binary_erosion(binary_fill_holes(fg), iterations=1), iterations=2)
            protected[y0i:y1i, x0i:x1i] |= fg

    mask[protected] = 0.0
    mask = gaussian_filter(mask, sigma=24.0)
    mask[protected] = 0.0

    return mask, protected


SCENES_6_WHITE = [
    # 1. DSC01779.JPG - Solo Fondo Blanco 1 (Perfil con termo Nutriplus rosa)
    {
        "fname": "DSC01779.JPG",
        "slug": "21_DSC01779_MANCUERNA_BLANCO_PERFIL_PRO",
        "title": "Solo Fondo Blanco 1 — Perfil Editorial con Termo Nutriplus",
        "no_op_clean": True,
        "skip_if_exists": True,
    },
    # 2. DSC01782.JPG - Solo Fondo Blanco 2 (Cuerpo completo bebiendo de termo Nutriplus)
    {
        "fname": "DSC01782.JPG",
        "slug": "22_DSC01782_MANCUERNA_BLANCO_BOTELLA_PRO",
        "title": "Solo Fondo Blanco 2 — Cuerpo Completo con Termo Nutriplus",
        "skip_if_exists": True,
        "floor_y": 0.785,
        "min_cloth_lum": 120.0,
        "max_cloth_lum": 245.0,
        "fold_gain": 0.45,
        "rug_cap": 175.0,
        "feather_w": 0.060,
        "top_line_y": (0.00, 0.00),
        "left_boundary_pts": [
            (0.00, 0.250),
            (0.08, 0.220),
            (0.16, 0.080),
            (0.35, 0.050),
            (0.55, 0.050),
            (0.76, 0.085),
            (0.86, 0.050),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.910),
            (0.14, 0.920),
            (0.28, 0.935),
            (0.55, 0.935),
            (0.78, 0.875),
            (0.86, 0.895),
            (1.00, 0.985),
        ],
        "extra_clean_boxes": [],
        "force_clean_boxes": [],
        "core_protect_boxes": [
            (0.23, 0.14, 0.68, 0.99),
        ],
        "subject_exclude_for_bg": [
            (0.20, 0.12, 0.72, 1.00),
        ],
    },
    # 3. DSC01799.JPG - Solo Fondo Blanco 3 (Hincada en tapete con mancuerna negra)
    {
        "fname": "DSC01799.JPG",
        "slug": "23_DSC01799_MANCUERNA_BLANCO_MANCUERNA_PRO",
        "title": "Solo Fondo Blanco 3 — Pose en Tapete con Mancuerna Hexagonal",
        "skip_if_exists": True,
        "floor_y": 0.585,
        "min_cloth_lum": 125.0,
        "max_cloth_lum": 245.0,
        "fold_gain": 0.45,
        "rug_cap": 195.0,
        "feather_w": 0.065,
        "top_line_y": (0.00, 0.00),
        "left_boundary_pts": [
            (0.00, 0.000),
            (0.28, 0.000),
            (0.38, 0.075),
            (0.56, 0.075),
            (0.66, 0.000),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 1.000),
            (1.00, 1.000),
        ],
        "extra_clean_boxes": [],
        "force_clean_boxes": [],
        "core_protect_boxes": [
            (0.22, 0.08, 0.76, 0.98),
        ],
        "subject_exclude_for_bg": [
            (0.20, 0.06, 0.78, 0.99),
        ],
    },
    # 4. DSC01730.JPG - Grupal 1 (4 Embajadoras en conjunto lila + botes Nutriplus)
    {
        "fname": "DSC01730.JPG",
        "slug": "27_DSC01730_MANCUERNA_GRUPO_NUTRIPLUS_PRO",
        "title": "Grupal 1 — Escuadrón Fitness Lila con Botes y Shakers Nutriplus",
        "floor_y": 0.750,
        "min_cloth_lum": 135.0,
        "max_cloth_lum": 240.0,
        "fold_gain": 0.50,
        "rug_cap": 182.0,
        "feather_w": 0.055,
        "top_line_y": (0.00, 0.00),
        "left_boundary_pts": [
            (0.00, 0.215),
            (0.25, 0.220),
            (0.38, 0.215),
            (0.55, 0.195),
            (0.68, 0.190),
            (0.75, 0.060),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.875),
            (0.20, 0.875),
            (0.35, 0.875),
            (0.55, 0.875),
            (0.72, 0.880),
            (0.80, 0.940),
            (1.00, 1.000),
        ],
        "extra_clean_boxes": [],
        "force_clean_boxes": [
            (0.00, 0.00, 0.075, 0.70),
            (0.00, 0.52, 0.163, 0.615),
            (0.00, 0.615, 0.172, 0.70),
            (0.935, 0.00, 1.00, 0.51),
            (0.902, 0.51, 1.00, 0.72),
        ],
        "core_protect_boxes": [
            (0.22, 0.18, 0.86, 0.93),   # Las 4 embajadoras centrales
            (0.18, 0.68, 0.28, 0.91),   # Brazo inferior y pierna embajadora abajo-izquierda
            (0.84, 0.70, 0.93, 0.82),   # Mano derecha abajo de la embajadora abajo-derecha
            (0.18, 0.87, 0.99, 1.00),   # Display de productos Nutriplus abajo
        ],
        "edge_guards": [
            (0.075, 0.36, 0.23, 0.54, "blonde_hair_on_black_wall"),
            (0.145, 0.50, 0.23, 0.72, "lilac_sleeve_and_blonde_left"),
            (0.84, 0.22, 0.935, 0.52, "right_arm_and_jar_1730"),
        ],
        "post_force_guards": [
            (0.84, 0.51, 0.928, 0.72, "right_arm_strict_1730"),
        ],
        "subject_exclude_for_bg": [
            (0.07, 0.16, 0.94, 1.00),
        ],
    },
    # 5. DSC01736.JPG - Grupal 2 (4 Embajadoras en conjunto lila con lentes y brazos cruzados)
    {
        "fname": "DSC01736.JPG",
        "slug": "28_DSC01736_MANCUERNA_GRUPO_LENTES_PRO",
        "title": "Grupal 2 — Escuadrón Fitness Lila con Lentes y Display Nutriplus",
        "floor_y": 0.735,
        "min_cloth_lum": 135.0,
        "max_cloth_lum": 240.0,
        "fold_gain": 0.50,
        "rug_cap": 182.0,
        "feather_w": 0.055,
        "top_line_y": (0.075, 0.095),
        "left_boundary_pts": [
            (0.00, 0.235),
            (0.35, 0.240),
            (0.60, 0.240),
            (0.70, 0.180),
            (0.78, 0.040),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.815),
            (0.35, 0.815),
            (0.65, 0.795),
            (0.75, 0.840),
            (0.84, 0.940),
            (1.00, 1.000),
        ],
        "extra_clean_boxes": [],
        "force_clean_boxes": [
            (0.00, 0.00, 1.00, 0.065),
            (0.00, 0.00, 0.194, 0.614),
            (0.83, 0.00, 1.00, 0.74),
            (0.00, 0.952, 1.00, 1.00),
            (0.00, 0.920, 0.215, 1.00),
        ],
        "core_protect_boxes": [
            (0.24, 0.19, 0.78, 0.90),    # Las 4 embajadoras completas
            (0.196, 0.54, 0.35, 0.616),  # Muslo superior derecho
            (0.172, 0.616, 0.35, 0.75),  # Rodilla izquierda completa extendida y mano apoyada
            (0.21, 0.75, 0.80, 0.88),    # Piernas en el tapete
            (0.215, 0.84, 0.965, 0.946), # Display de productos Nutriplus + borde frontal del tapete
        ],
        "edge_guards": [],
        "subject_exclude_for_bg": [
            (0.17, 0.17, 0.99, 1.00),
        ],
    },
    # 6. DSC08716.JPG - Grupal 3 (Trío en vestidos rojo y cobrizo en fondo blanco)
    {
        "fname": "DSC08716.JPG",
        "slug": "29_DSC08716_MANCUERNA_GRUPO_ROJO_COBRIZO_PRO",
        "title": "Grupal 3 — Trío Editorial en Vestidos Rojo y Cobrizo",
        "skip_if_exists": True,
        "floor_y": 0.785,
        "min_cloth_lum": 216.0,
        "max_cloth_lum": 254.0,
        "fold_gain": 0.95,
        "rug_cap": 244.0,
        "feather_w": 0.055,
        "top_line_y": (0.145, 0.165),
        "left_boundary_pts": [
            (0.00, 0.160),
            (0.35, 0.160),
            (0.68, 0.150),
            (0.85, 0.135),
            (0.92, 0.040),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.885),
            (0.50, 0.885),
            (0.85, 0.875),
            (1.00, 0.875),
        ],
        "extra_clean_boxes": [],
        "force_clean_boxes": [
            (0.00, 0.00, 1.00, 0.130),
            (0.00, 0.00, 0.120, 0.665),
            (0.90, 0.00, 1.00, 1.00),
            (0.00, 0.805, 0.095, 0.88),  # Zoclo/triángulo oscuro debajo del tobillo izquierdo
        ],
        "core_protect_boxes": [
            (0.14, 0.26, 0.78, 0.98),  # Las 3 embajadoras centrales
            (0.125, 0.68, 0.35, 0.96), # Falda roja izquierda
        ],
        "protect_polygons": [],
        "edge_guards": [
            (0.00, 0.66, 0.15, 0.82, "skin_or_red_strict"),
        ],
        "subject_exclude_for_bg": [
            (0.00, 0.25, 0.80, 0.99),
        ],
    },
]


def main():
    ref_7738_u8 = np.asarray(base.load_oriented(os.path.join(SRC_DIR, "DSC07738.JPG")), dtype=np.uint8)
    ref_8485_u8 = np.asarray(base.load_oriented(os.path.join(SRC_DIR, "DSC08485.JPG")), dtype=np.uint8)
    ref_9204_u8 = np.asarray(base.load_oriented(os.path.join(SRC_DIR, "DSC09204 2.JPG")), dtype=np.uint8)
    H0, W0 = ref_7738_u8.shape[:2]
    cloth_folds, rug_detail = base.build_pure_draped_cloth_and_rug_texture(
        H0, W0, ref_7738_u8, ref_8485_u8, ref_9204_u8
    )

    for cfg in SCENES_6_WHITE:
        out_name = f"{cfg['slug']}.jpg"
        p_pend = os.path.join(PENDIENTES_DIR, out_name)
        p_brain = os.path.join(BRAIN, out_name)
        if cfg.get("skip_if_exists", False) and os.path.exists(p_pend) and os.path.exists(p_brain):
            print(f"[SKIP] {out_name} already verified")
            continue

        src_path = os.path.join(SRC_DIR, cfg["fname"])
        orig_im = base.load_oriented(src_path)
        orig_u8 = np.asarray(orig_im, dtype=np.uint8)
        H, W = orig_u8.shape[:2]

        if cfg.get("no_op_clean", False):
            final_u8 = orig_u8.copy()
            prot_changed = 0
        else:
            mask, protected = build_mask_v12(orig_u8, cfg)
            plate = base.synthesize_seamless_backdrop(orig_u8, cloth_folds, rug_detail, cfg, mask)

            if cfg["fname"] == "DSC01736.JPG":
                # Extender textura real del tapete de peluche del área limpia izquierda (x in [0.03, 0.20], y in [0.83, 0.90]) hacia la franja inferior y >= 0.915
                y0_r = int(H * 0.910)
                h_r = H - y0_r
                patch = orig_u8[int(H * 0.81):int(H * 0.81) + h_r, int(W * 0.03):int(W * 0.20), :].astype(np.float32)
                tile_unit = np.concatenate([patch, patch[:, ::-1, :]], axis=1)
                reps = int(np.ceil(W / float(tile_unit.shape[1]))) + 1
                rug_strip = np.tile(tile_unit, (1, reps, 1))[:, :W, :]
                # Igualar gradiente horizontal suave de la placa en el piso
                strip_low = gaussian_filter(rug_strip, sigma=(28.0, 60.0, 0.0))
                plate_low = gaussian_filter(plate[y0_r:, :, :], sigma=(28.0, 60.0, 0.0))
                rug_matched = np.clip(plate_low + (rug_strip - strip_low) * 1.15, 0, 255)
                blend_y = np.linspace(0.0, 1.0, h_r, dtype=np.float32)[:, None, None]
                plate[y0_r:, :, :] = plate[y0_r:, :, :] * (1.0 - blend_y) + rug_matched * blend_y

            m3 = mask[:, :, None]
            comp = orig_u8.astype(np.float32) * (1.0 - m3) + plate * m3
            final_u8 = np.clip(np.round(comp), 0, 255).astype(np.uint8)
            final_u8[protected] = orig_u8[protected]

            diff = np.abs(final_u8.astype(np.int16) - orig_u8.astype(np.int16)).max(axis=2)
            prot_changed = int(diff[protected].max()) if np.any(protected) else 0

        Image.fromarray(final_u8).save(p_pend, quality=96, subsampling=0)
        shutil.copy2(p_pend, p_brain)
        print(f"[OK] {out_name} ({W}x{H}) | protected_changed={prot_changed}")


if __name__ == "__main__":
    main()
