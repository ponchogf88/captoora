#!/usr/bin/env python3
"""
Procesador Captoora Studio Retouch (V10) para las fotos 11 a 15 de grupo
del Primer Lote (Farmasi 799 - 31 de octubre) y consolidación de las 9 aprobadas (02..10).
"""

import json
import os
import shutil
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

import run_5_more_groups as base

BRAIN = base.BRAIN
SRC_DIR = base.SRC_DIR
OUT_DIR = base.OUT_DIR
APPROVED_BATCH1_DIR = os.path.join(BRAIN, "scratch/cobrizo_5_edit/LOTE_1_GRUPOS_APROBADAS")
PENDING_REVIEW_DIR = os.path.join(BRAIN, "scratch/cobrizo_5_edit/PENDIENTES_DE_APROBACION")
os.makedirs(APPROVED_BATCH1_DIR, exist_ok=True)
os.makedirs(PENDING_REVIEW_DIR, exist_ok=True)


def consolidate_approved_02_to_10():
    # Move/copy 01 to PENDING_REVIEW_DIR
    p01 = os.path.join(BRAIN, "01_DSC08355_2_COBRIZO_PRO.jpg")
    if os.path.exists(p01):
        shutil.copy2(p01, os.path.join(PENDING_REVIEW_DIR, "01_DSC08355_2_COBRIZO_PRO.jpg"))

    approved_slugs = [
        "02_DSC08425_2_COBRIZO_PRO.jpg",
        "03_DSC08485_COBRIZO_PRO.jpg",
        "04_DSC09204_2_COBRIZO_PRO.jpg",
        "05_DSC09538_2_COBRIZO_PRO.jpg",
        "06_DSC08447_GRUPO_PRO.jpg",
        "07_DSC08477_GRUPO_PRO.jpg",
        "08_DSC08697_2_GRUPO_PRO.jpg",
        "09_DSC09319_2_GRUPO_PRO.jpg",
        "10_DSC09541_2_GRUPO_PRO.jpg",
    ]
    for fn in approved_slugs:
        full_src = os.path.join(OUT_DIR, fn)
        if not os.path.exists(full_src):
            full_src = os.path.join(BRAIN, fn)
        if os.path.exists(full_src):
            shutil.copy2(full_src, os.path.join(APPROVED_BATCH1_DIR, fn))
            print(f"[APROBADA -> LOTE 1] {fn}")


SCENES_11_TO_15 = [
    {
        "fname": "DSC08484.JPG",
        "slug": "11_DSC08484_GRUPO_PRO",
        "title": "Trío Embajadores Pose Acción Pulgar Arriba",
        "floor_y": 0.745,
        "min_cloth_lum": 208.0,
        "max_cloth_lum": 248.0,
        "fold_gain": 0.95,
        "rug_cap": 243.0,
        "top_line_y": (0.045, 0.088),
        "left_boundary_pts": [
            (0.00, 0.025),
            (0.35, 0.032),
            (0.55, 0.045),
            (0.75, 0.045),
            (0.82, 0.000),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.800),
            (0.25, 0.790),
            (0.48, 0.775),
            (0.68, 0.755),
            (0.84, 0.775),
            (0.92, 0.805),
            (1.00, 0.815),
        ],
        "extra_clean_boxes": [
            (0.778, 0.15, 1.00, 0.68),
            (0.805, 0.65, 1.00, 0.99),
        ],
        "force_clean_boxes": [
            (0.00, 0.28, 0.035, 0.74),
            (0.00, 0.00, 1.00, 0.045),
            (0.780, 0.15, 1.00, 0.68),
            (0.810, 0.65, 1.00, 0.99),
        ],
        "edge_guards": [
            (0.60, 0.22, 0.805, 0.82, "copper_strict"),
        ],
        "core_protect_boxes": [
            (0.08, 0.20, 0.745, 0.90),
        ],
        "subject_exclude_for_bg": [
            (0.06, 0.18, 0.82, 0.92),
        ],
    },
    {
        "fname": "DSC08710.JPG",
        "slug": "12_DSC08710_GRUPO_PRO",
        "title": "Trío Embajadoras Celebrando en Movimiento (Rojo y Cobrizo)",
        "floor_y": 0.815,
        "min_cloth_lum": 212.0,
        "max_cloth_lum": 252.0,
        "fold_gain": 0.90,
        "rug_cap": 245.0,
        "top_line_y": (0.105, 0.125),
        "left_boundary_pts": [
            (0.00, 0.065),
            (0.25, 0.072),
            (0.45, 0.088),
            (0.62, 0.095),
            (0.72, 0.040),
            (0.76, 0.000),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.875),
            (0.35, 0.875),
            (0.65, 0.865),
            (0.85, 0.860),
            (1.00, 0.880),
        ],
        "extra_clean_boxes": [
            (0.875, 0.00, 1.00, 0.92),
            (0.00, 0.00, 0.085, 0.72),
        ],
        "force_clean_boxes": [
            (0.880, 0.00, 1.00, 0.92),
            (0.00, 0.00, 1.00, 0.095),
        ],
        "edge_guards": [
            (0.00, 0.52, 0.28, 0.93, "skin_or_red_strict"),
            (0.10, 0.20, 0.25, 0.35, "skin_or_red_strict"),
        ],
        "core_protect_boxes": [
            (0.16, 0.21, 0.82, 0.96),
            (0.00, 0.70, 0.26, 0.92),
        ],
        "subject_exclude_for_bg": [
            (0.00, 0.19, 0.86, 0.97),
        ],
    },
    {
        "fname": "DSC09214 2.JPG",
        "slug": "13_DSC09214_2_GRUPO_PRO",
        "title": "Trío Embajadoras Pose Editorial (Dos Vestidos Cobrizos + Vestido Rojo)",
        "floor_y": 0.775,
        "min_cloth_lum": 218.0,
        "max_cloth_lum": 254.0,
        "fold_gain": 0.85,
        "rug_cap": 247.0,
        "top_line_y": (0.000, 0.000),
        "left_boundary_pts": [
            (0.00, 0.000),
            (0.35, 0.000),
            (0.45, 0.038),
            (0.76, 0.038),
            (0.82, 0.000),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 1.000),
            (1.00, 1.000),
        ],
        "extra_clean_boxes": [],
        "force_clean_boxes": [
            (0.00, 0.42, 0.032, 0.76),
        ],
        "edge_guards": [
            (0.11, 0.14, 0.98, 0.91, "copper_strict"),
        ],
        "core_protect_boxes": [
            (0.11, 0.14, 0.99, 0.90),
            (0.20, 0.90, 0.65, 1.00),
        ],
        "subject_exclude_for_bg": [
            (0.10, 0.12, 0.99, 0.99),
        ],
    },
    {
        "fname": "DSC09346 2.JPG",
        "slug": "14_DSC09346_2_GRUPO_PRO",
        "title": "Trío Editorial In My Boss Era + Periódicos y Nutriplus",
        "floor_y": 0.745,
        "min_cloth_lum": 212.0,
        "max_cloth_lum": 250.0,
        "fold_gain": 0.92,
        "rug_cap": 244.0,
        "top_line_y": (0.000, 0.000),
        "left_boundary_pts": [
            (0.00, 0.115),
            (0.30, 0.138),
            (0.60, 0.148),
            (0.73, 0.142),
            (0.80, 0.000),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 0.975),
            (0.25, 0.960),
            (0.55, 0.910),
            (0.75, 0.895),
            (0.90, 0.930),
            (1.00, 1.000),
        ],
        "extra_clean_boxes": [
            (0.910, 0.10, 1.00, 0.82),
        ],
        "force_clean_boxes": [
            (0.00, 0.00, 0.132, 0.72),
            (0.920, 0.05, 1.00, 0.80),
        ],
        "edge_guards": [
            (0.14, 0.22, 0.84, 0.88, "copper_strict"),
        ],
        "core_protect_boxes": [
            (0.165, 0.22, 0.82, 0.88),
            (0.20, 0.83, 0.84, 1.00),
        ],
        "subject_exclude_for_bg": [
            (0.14, 0.20, 0.85, 0.99),
        ],
    },
    {
        "fname": "DSC09341 2.JPG",
        "slug": "15_DSC09341_2_GRUPO_PRO",
        "title": "Trío Editorial The Boss Era (Mirada al Frente + Periódicos en Tapete)",
        "floor_y": 0.765,
        "min_cloth_lum": 212.0,
        "max_cloth_lum": 250.0,
        "fold_gain": 0.92,
        "rug_cap": 244.0,
        "top_line_y": (0.000, 0.000),
        "left_boundary_pts": [
            (0.00, 0.052),
            (0.35, 0.068),
            (0.65, 0.078),
            (0.75, 0.075),
            (0.82, 0.000),
            (1.00, 0.000),
        ],
        "right_boundary_pts": [
            (0.00, 1.000),
            (1.00, 1.000),
        ],
        "extra_clean_boxes": [],
        "force_clean_boxes": [
            (0.00, 0.00, 0.068, 0.74),
        ],
        "edge_guards": [
            (0.08, 0.12, 0.88, 0.88, "copper_strict"),
        ],
        "core_protect_boxes": [
            (0.095, 0.12, 0.88, 0.88),
            (0.18, 0.85, 0.85, 1.00),
        ],
        "subject_exclude_for_bg": [
            (0.08, 0.11, 0.90, 0.99),
        ],
    },
]


def main():
    consolidate_approved_02_to_10()

    ref_7738 = np.asarray(base.load_oriented(os.path.join(SRC_DIR, "DSC07738.JPG")), dtype=np.uint8)
    ref_8485 = np.asarray(base.load_oriented(os.path.join(SRC_DIR, "DSC08485.JPG")), dtype=np.uint8)
    ref_9204 = np.asarray(base.load_oriented(os.path.join(SRC_DIR, "DSC09204 2.JPG")), dtype=np.uint8)
    H, W = ref_7738.shape[:2]

    cloth_folds, rug_detail = base.build_pure_draped_cloth_and_rug_texture(H, W, ref_7738, ref_8485, ref_9204)

    report = []
    for cfg in SCENES_11_TO_15:
        fname = cfg["fname"]
        slug = cfg["slug"]
        orig_u8 = np.asarray(base.load_oriented(os.path.join(SRC_DIR, fname)), dtype=np.uint8)

        mask, protected = base.build_precise_cleanup_mask(orig_u8, cfg)
        plate_f = base.synthesize_seamless_backdrop(orig_u8, cloth_folds, rug_detail, cfg, mask)

        m3 = mask[:, :, None]
        comp_f = orig_u8.astype(np.float32) * (1.0 - m3) + plate_f * m3
        out_u8 = np.clip(np.round(comp_f), 0, 255).astype(np.uint8)

        out_u8[protected] = orig_u8[protected]
        changed = int(np.count_nonzero(out_u8[protected] != orig_u8[protected]))
        assert changed == 0

        out_im = Image.fromarray(out_u8)
        out_im.save(os.path.join(OUT_DIR, f"{slug}.jpg"), quality=96, subsampling=0)
        out_im.resize((1600, 2400), Image.Resampling.LANCZOS).save(
            os.path.join(BRAIN, f"{slug}.jpg"), quality=95, subsampling=0
        )
        print(f"V10 OK: {fname} -> {slug}.jpg | protected_changed={changed}")
        report.append({
            "source": fname,
            "output": f"{slug}.jpg",
            "title": cfg["title"],
            "protected_pixels_changed": changed,
        })

    with open(os.path.join(OUT_DIR, "report_11_to_15_v10.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
