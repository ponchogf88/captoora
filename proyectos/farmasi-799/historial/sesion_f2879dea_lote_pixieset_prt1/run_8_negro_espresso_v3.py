#!/usr/bin/env python3
"""
Captoora — Fondo Negro Espresso V3 (24/25/26 Mancuerna).
Cambio clave vs V2: la máscara ya NO es por color pixel a pixel (eso moteaba el cabello).
Ahora: polígonos por foto (fuera = fondo seguro, núcleo = sujeto seguro) + GrabCut en la franja
intermedia + pluma suave. El fondo se reemplaza al 100% (sin restos de tela fría ni arrugas).
Fuente: V1_NEGRO_FRIO (nunca se sobrescribe).
"""
import os, shutil, sys
import numpy as np
import cv2
from PIL import Image
from scipy.ndimage import gaussian_filter, zoom

BRAIN = "/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f"
WD = os.path.join(BRAIN, "scratch/cobrizo_5_edit")
PEND = os.path.join(WD, "PENDIENTES_DE_APROBACION")
V1 = os.path.join(WD, "V1_NEGRO_FRIO")

SCENES = {
    "24_DSC00373_MANCUERNA_NEGRO_PALETA_PRO": dict(
        glow=(0.55, 0.40),
        outer=[[(0.03, 0.21), (0.30, 0.21), (0.31, 0.29), (0.37, 0.29), (0.42, 0.18), (0.50, 0.13),
                (0.64, 0.13), (0.78, 0.16), (0.87, 0.26), (0.93, 0.42), (0.96, 0.62), (0.98, 0.85),
                (0.98, 1.0), (0.40, 1.0), (0.40, 0.84), (0.34, 0.75), (0.22, 0.75), (0.15, 0.70),
                (0.15, 0.47), (0.04, 0.41)]],
        core=[[(0.56, 0.23), (0.70, 0.21), (0.79, 0.34), (0.84, 0.58), (0.87, 0.85), (0.87, 1.0),
               (0.48, 1.0), (0.45, 0.80), (0.38, 0.64), (0.45, 0.52), (0.53, 0.46), (0.53, 0.31)],
              [(0.21, 0.45), (0.25, 0.47), (0.31, 0.69), (0.27, 0.69)]],
    ),
    "25_DSC00408_MANCUERNA_NEGRO_ESPEJO_PRO": dict(
        glow=(0.45, 0.35),
        outer=[[(0.39, 0.19), (0.61, 0.19), (0.68, 0.25), (0.74, 0.14), (0.87, 0.06), (1.0, 0.03),
                (1.0, 1.0), (0.24, 1.0), (0.25, 0.78), (0.29, 0.68), (0.41, 0.62), (0.47, 0.47),
                (0.42, 0.39), (0.39, 0.30)]],
        core=[[(0.80, 0.20), (1.0, 0.12), (1.0, 1.0), (0.69, 1.0), (0.67, 0.60), (0.72, 0.36)],
              [(0.31, 0.86), (0.45, 0.72), (0.62, 0.70), (0.62, 1.0), (0.30, 1.0)],
              [(0.51, 0.46), (0.57, 0.46), (0.57, 0.62), (0.52, 0.62)]],
    ),
    "26_DSC00415_MANCUERNA_NEGRO_COPA_PRO": dict(
        glow=(0.50, 0.30),
        outer=[[(0.16, 0.16), (0.38, 0.16), (0.38, 0.08), (0.48, 0.02), (0.66, 0.0), (0.77, 0.04),
                (0.85, 0.22), (0.91, 0.36), (1.0, 0.40), (1.0, 1.0), (0.04, 1.0), (0.08, 0.78),
                (0.12, 0.70), (0.05, 0.55), (0.05, 0.40), (0.11, 0.30)]],
        core=[[(0.20, 0.22), (0.36, 0.22), (0.42, 0.12), (0.60, 0.07), (0.70, 0.12), (0.78, 0.30),
               (0.88, 0.46), (1.0, 0.51), (1.0, 1.0), (0.12, 1.0), (0.16, 0.80), (0.18, 0.62),
               (0.10, 0.50), (0.13, 0.36)]],
    ),
}

WARM = np.array([1.00, 0.74, 0.52], dtype=np.float32)
LUMW = np.array([0.299, 0.587, 0.114], dtype=np.float32)


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def poly_mask(polys, w, h):
    m = np.zeros((h, w), np.uint8)
    for p in polys:
        pts = np.array([[x * w, y * h] for x, y in p], np.int32)
        cv2.fillPoly(m, [pts], 1)
    return m.astype(bool)


def subject_alpha(img, sc):
    H, W = img.shape[:2]
    s = 4
    small = cv2.resize(img, (W // s, H // s), interpolation=cv2.INTER_AREA)
    h, w = small.shape[:2]
    outer = poly_mask(sc["outer"], w, h)
    core = poly_mask(sc["core"], w, h)
    f = small.astype(np.float32)
    lum = f @ LUMW
    warmth = f[..., 0] - f[..., 2]
    gc = np.full((h, w), cv2.GC_BGD, np.uint8)
    gc[outer] = cv2.GC_PR_BGD
    cue = outer & ((lum > 105) | ((warmth > 22) & (lum > 45)))
    gc[cue] = cv2.GC_PR_FGD
    gc[core] = cv2.GC_FGD
    bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
    bgr = cv2.cvtColor(small, cv2.COLOR_RGB2BGR)
    cv2.grabCut(bgr, gc, None, bgd, fgd, 6, cv2.GC_INIT_WITH_MASK)
    fg = ((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD)).astype(np.uint8)
    # Limpieza morfológica: sin islas ni agujeros (nada de moteado)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, k, iterations=2)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, k, iterations=1)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(fg, 8)
    keep = np.zeros_like(fg)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] > 0.002 * h * w:
            keep[lab == i] = 1
    # rellena huecos internos (tatuaje, copa, sombras del pelo)
    inv = (1 - keep).astype(np.uint8)
    n2, lab2, st2, _ = cv2.connectedComponentsWithStats(inv, 4)
    for i in range(1, n2):
        if st2[i, cv2.CC_STAT_AREA] < 0.004 * h * w:
            keep[lab2 == i] = 1
    keep[core] = 1
    return keep, s


def norm_conv(val, wgt, sig):
    return gaussian_filter(val * wgt, sig) / (gaussian_filter(wgt, sig) + 1e-4)


def up(a, W, H):
    return cv2.resize(a.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)


def process(slug, sc):
    src = os.path.join(V1, slug + ".jpg")
    img_u8 = np.asarray(Image.open(src).convert("RGB"))
    img = img_u8.astype(np.float32)
    H, W = img.shape[:2]
    keep, s = subject_alpha(img_u8, sc)
    h, w_ = keep.shape
    small = cv2.resize(img, (w_, h), interpolation=cv2.INTER_AREA)
    slum = small @ LUMW
    swarm = small[..., 0] - small[..., 2]

    # distancias firmadas a la silueta (escala 1/4)
    d_out = cv2.distanceTransform((1 - keep).astype(np.uint8), cv2.DIST_L2, 5)
    d_in = cv2.distanceTransform(keep.astype(np.uint8), cv2.DIST_L2, 5)
    R_OUT, R_IN = 30.0, 30.0
    sure_bg = d_out > R_OUT
    # color del fondo viejo (suave) y luminancia local del sujeto
    Bold = np.stack([norm_conv(small[..., c], sure_bg.astype(np.float32), 20) for c in range(3)], -1)
    Lb = Bold @ LUMW
    fgw = ((keep > 0) & (slum > 60)).astype(np.float32)
    Lf = norm_conv(slum, fgw, 30)
    a_diff = np.clip((slum - Lb) / np.maximum(Lf - Lb, 30.0), 0, 1)
    a_diff = np.maximum(a_diff, smoothstep(10, 24, swarm) * smoothstep(25, 55, slum))  # cálido = sujeto
    in_w = smoothstep(R_IN * 0.5, R_IN, d_in)          # 1 = adentro profundo
    a_small = np.where(keep > 0, 1 - (1 - a_diff) * (1 - in_w), a_diff)
    s_out = smoothstep(R_OUT * 0.5, R_OUT, d_out)       # 1 = fondo seguro
    a_small = a_small * (1 - s_out)

    alpha = np.clip(up(a_small, W, H), 0, 1)
    # alfa fino a resolución completa: refina con la luminancia real (mechones)
    lum = img @ LUMW
    LbF = up(Lb, W, H); LfF = up(Lf, W, H)
    a_fine = np.clip((lum - LbF) / np.maximum(LfF - LbF, 30.0), 0, 1)
    band = (alpha > 0.01) & (alpha < 0.99)
    alpha = np.where(band, np.clip(0.5 * alpha + 0.5 * a_fine, 0, 1) * (alpha > 0.01), alpha)
    alpha = cv2.GaussianBlur(alpha.astype(np.float32), (0, 0), 1.2)
    BoldF = np.stack([up(Bold[..., c], W, H) for c in range(3)], -1)

    # luz de fondo nueva
    ls = cv2.resize(np.clip(lum, 0, 60), (w_, h), interpolation=cv2.INTER_AREA)
    lowL = up(norm_conv(ls, sure_bg.astype(np.float32), 60), W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    gx, gy = sc["glow"]
    d = np.sqrt(((xx / W - gx) / 0.55) ** 2 + ((yy / H - gy) / 0.60) ** 2)
    halo = np.exp(-(d ** 2) * 1.6)
    vign = 1.0 - 0.55 * smoothstep(0.55, 1.45, d)
    targetL = (7.0 + 0.12 * lowL + 16.0 * halo) * vign
    target = targetL[..., None] * WARM / float(WARM @ LUMW)
    grain = np.random.default_rng(799).normal(0, 1.0, size=(H, W, 1)).astype(np.float32)

    # Sustitución de fondo: el sujeto conserva su pixel; solo se cambia el aporte del fondo viejo.
    A = alpha[..., None]
    resid = img - BoldF
    k = 0.85  # cuánto de la textura de tela vieja se elimina donde hay fondo
    out = img + (1 - A) * (target - BoldF) - k * (1 - A) ** 2 * resid
    out = out + (1 - A) * grain
    out = np.clip(np.round(out), 0, 255).astype(np.uint8)

    subj = alpha > 0.995
    diff = np.abs(out.astype(np.int16) - img_u8.astype(np.int16)).max(axis=2)
    changed = int(np.percentile(diff[subj], 99.9))
    p = os.path.join(PEND, slug + ".jpg")
    Image.fromarray(out).save(p, quality=96, subsampling=0)
    shutil.copy2(p, os.path.join(BRAIN, slug + ".jpg"))
    Image.fromarray((alpha * 255).astype(np.uint8)).resize((W // 6, H // 6)).save(
        os.path.join(WD, slug + "_ALPHA_V4.png"))
    print(f"[OK] {slug} {W}x{H} subj_change_p99.9={changed} subj_frac={float(subj.mean()):.2f}", flush=True)

if __name__ == "__main__":
    only = sys.argv[1:]
    for slug, sc in SCENES.items():
        if only and not any(o in slug for o in only):
            continue
        process(slug, sc)
