#!/usr/bin/env python3
"""
Captoora — Fondo Negro Espresso (V2) para 24/25/26 Mancuerna.
Objetivo: igualar el look de las fotos de la morena (DSC01551_v02...):
negro cálido chocolate/espresso, liso (sin arrugas de tela), viñeta suave
y un halo cálido tenue detrás del sujeto. Piel, cabello, vestido y productos intactos.
"""
import os
import shutil
import sys
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, zoom

BRAIN = "/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f"
PEND = os.path.join(BRAIN, "scratch/cobrizo_5_edit/PENDIENTES_DE_APROBACION")
V1 = os.path.join(BRAIN, "scratch/cobrizo_5_edit/V1_NEGRO_FRIO")
os.makedirs(V1, exist_ok=True)

SCENES = [
    # glow = centro (x, y) del halo cálido detrás del sujeto
    {"slug": "24_DSC00373_MANCUERNA_NEGRO_PALETA_PRO", "glow": (0.55, 0.40)},
    {"slug": "25_DSC00408_MANCUERNA_NEGRO_ESPEJO_PRO", "glow": (0.45, 0.35)},
    {"slug": "26_DSC00415_MANCUERNA_NEGRO_COPA_PRO", "glow": (0.50, 0.30)},
]

# Paleta espresso (medida sobre la referencia de la morena): sombras cálidas marrón-negro
WARM = np.array([1.00, 0.74, 0.52], dtype=np.float32)


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def bg_weight(img):
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    sat = img.max(axis=2) - img.min(axis=2)
    warmth = r - b
    # Fondo = oscuro/medio, poco saturado y neutro-frío. Piel/cabello rubio/vino = cálidos o brillantes.
    w_lum = 1.0 - smoothstep(70.0, 118.0, lum)
    w_neutral = 1.0 - smoothstep(6.0, 20.0, warmth)
    w_sat = 1.0 - smoothstep(22.0, 40.0, sat)
    w = w_lum * w_neutral * w_sat
    # Limpieza de ruido: quita puntos aislados, conserva bordes de mechones
    w = gaussian_filter(w, 2.0)
    return np.clip(w, 0, 1), lum


def process(slug, glow):
    src = os.path.join(V1, slug + ".jpg")
    if not os.path.exists(src):
        shutil.copy2(os.path.join(PEND, slug + ".jpg"), src)
    img = np.asarray(Image.open(src).convert("RGB"), dtype=np.float32)
    H, W = img.shape[:2]

    w, lum = bg_weight(img)

    # Luminancia del fondo a baja frecuencia (convolución normalizada) => sin arrugas
    s = 0.125
    lum_s = zoom(lum, s, order=1)
    w_s = zoom(w, s, order=1)
    sig = 60.0
    num = gaussian_filter(lum_s * w_s, sig)
    den = gaussian_filter(w_s, sig) + 1e-4
    lowL = zoom(num / den, (H / lum_s.shape[0], W / lum_s.shape[1]), order=1)[:H, :W]

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    xn, yn = xx / W, yy / H
    gx, gy = glow
    d = np.sqrt(((xn - gx) / 0.55) ** 2 + ((yn - gy) / 0.60) ** 2)
    halo = np.exp(-(d ** 2) * 1.6)              # halo cálido central
    vign = 1.0 - 0.55 * smoothstep(0.55, 1.45, d)  # viñeta hacia los bordes

    # Luminancia objetivo: base muy baja + un poco de la caída natural de luz + halo
    targetL = (7.0 + 0.18 * np.clip(lowL, 0, 80) + 15.0 * halo) * vign
    # Conserva 12% de la textura fina real para que no se vea plano/CGI
    detail = lum - gaussian_filter(lum, 6.0)
    targetL = targetL + 0.12 * np.clip(detail, -25, 25)

    target = targetL[..., None] * WARM[None, None, :] / (WARM @ np.array([0.299, 0.587, 0.114], dtype=np.float32))
    rng = np.random.default_rng(799)
    target += rng.normal(0, 1.1, size=(H, W, 1)).astype(np.float32)

    out = img * (1 - w[..., None]) + target * w[..., None]
    out = np.clip(np.round(out), 0, 255).astype(np.uint8)

    # Auditoría: pixeles de sujeto (w<0.02) sin cambio
    subj = w < 0.02
    diff = np.abs(out.astype(np.int16) - img.astype(np.int16)).max(axis=2)
    changed = int(np.percentile(diff[subj], 99.9)) if subj.any() else 0

    p = os.path.join(PEND, slug + ".jpg")
    Image.fromarray(out).save(p, quality=96, subsampling=0)
    shutil.copy2(p, os.path.join(BRAIN, slug + ".jpg"))
    # Mapa de máscara para auditoría visual
    Image.fromarray((w * 255).astype(np.uint8)).resize((W // 6, H // 6)).save(
        os.path.join(BRAIN, "scratch/cobrizo_5_edit", slug + "_MASK.png"))
    print(f"[OK] {slug} {W}x{H} subj_p99.9_change={changed} bg_frac={float((w>0.5).mean()):.2f}")


if __name__ == "__main__":
    only = sys.argv[1:]
    for sc in SCENES:
        if only and not any(o in sc["slug"] for o in only):
            continue
        process(sc["slug"], sc["glow"])
