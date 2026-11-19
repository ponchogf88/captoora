#!/usr/bin/env python3
"""
Renderizador Maestro del Arte Corregido de Captoora Studio:
Post 01 - Campaña de Otoño / Halloween 2026 (Retrato Infantil en Set)

Cumplimiento estricto:
1. Cero Crop (100% Full-Frame): Sin amputar cabeza, manos, capa, botas ni calabazas.
2. Logotipo unificado y protagonista: Monograma de lente concéntrico con destello estelar
   + Tipografía Syncopate 'CAPTOORA' con ÚNICAMENTE la última 'A' iluminada en verde lima (#CCFF00).
3. Textos editoriales de alta gama: Se eliminan textos técnicos genéricos ('STANDBY', '85MM', 'SET CLIMATIZADO', 'ISO')
   y se sustituyen por leyendas de colección de autor ('EDICIÓN ESPECIAL OTOÑO 2026', 'COLINAS DE SAN JERÓNIMO · MTY').
4. Cero colisiones ni empalmes visuales.
"""

import os
import subprocess
import base64
import shutil
from pathlib import Path

BASE_DIR = Path("/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO")
OUT_DIR = BASE_DIR / "campaigns/campana-otono-halloween-muertos-2026/artes_dia_1"
OUT_DIR.mkdir(parents=True, exist_ok=True)
DESKTOP_DIR = Path("/Users/imac/Desktop")

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def to_base64_data_uri(path):
    with open(path, "rb") as f:
        data = f.read()
    ext = path.suffix.lower().replace(".", "")
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"

LOGO_URI = to_base64_data_uri(BASE_DIR / "assets/captoora_logo_circle_centered.png")
PHOTO_URI = to_base64_data_uri(BASE_DIR / "assets/referencias_generadas/ref_studio_halloween_9x16.jpg")

COMMON_HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700&family=Space+Grotesk:wght@500;600;700&family=Syncopate:wght@700;800&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background-color: #000000;
    color: #FFFFFF;
    font-family: 'Space Grotesk', -apple-system, sans-serif;
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
}
.lit-a {
    color: #CCFF00 !important;
    text-shadow: 0 0 16px rgba(204, 255, 0, 0.95), 0 0 32px rgba(204, 255, 0, 0.55);
}

/* MARCO EDITORIAL DE VISOR MINIMALISTA */
.corner-bracket {
    position: absolute;
    width: 44px; height: 44px;
    pointer-events: none;
    z-index: 50;
}
.cb-tl {
    top: 32px; left: 32px;
    border-top: 2.5px solid #CCFF00;
    border-left: 2.5px solid #CCFF00;
}
.cb-tr {
    top: 32px; right: 32px;
    border-top: 2.5px solid #CCFF00;
    border-right: 2.5px solid #CCFF00;
}
.cb-bl {
    bottom: 32px; left: 32px;
    border-bottom: 2.5px solid #CCFF00;
    border-left: 2.5px solid #CCFF00;
}
.cb-br {
    bottom: 32px; right: 32px;
    border-bottom: 2.5px solid #CCFF00;
    border-right: 2.5px solid #CCFF00;
}

/* HEADER EDITORIAL */
.editorial-header {
    position: absolute;
    top: 42px;
    left: 95px;
    right: 95px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 60;
}
.header-badge {
    background: rgba(10, 12, 14, 0.78);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.16);
    padding: 9px 20px;
    border-radius: 30px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.92);
    display: flex;
    align-items: center;
    gap: 9px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}
.header-dot {
    width: 8px;
    height: 8px;
    background: #CCFF00;
    border-radius: 50%;
    box-shadow: 0 0 10px #CCFF00, 0 0 18px rgba(204, 255, 0, 0.6);
}

/* FOOTER UNIFICADO DE PRESTIGIO */
.signature-bar {
    position: absolute;
    bottom: 45px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 60;
    background: rgba(8, 10, 12, 0.85);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.85), 0 0 1px rgba(204, 255, 0, 0.4);
    padding: 12px 28px 12px 22px;
    border-radius: 50px;
    display: flex;
    align-items: center;
    gap: 16px;
    white-space: nowrap;
}
.sig-logo {
    width: 46px;
    height: 46px;
    object-fit: contain;
    filter: drop-shadow(0 2px 10px rgba(204, 255, 0, 0.45));
}
.sig-brand-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.sig-title {
    font-family: 'Syncopate', sans-serif;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #FFFFFF;
    line-height: 1.1;
}
.sig-location {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    color: rgba(255, 255, 255, 0.75);
    text-transform: uppercase;
}
.sig-divider {
    width: 1px;
    height: 28px;
    background: rgba(255, 255, 255, 0.22);
    margin: 0 4px;
}
.sig-tag {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2.2px;
    color: #CCFF00;
    text-transform: uppercase;
}
</style>
"""

# -------------------------------------------------------------
# 1. POST FEED 4:5 (1080 x 1350) — ZERO CROP / 100% FULL-FRAME
# -------------------------------------------------------------
html_post_4x5 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_HEAD}
<style>
.container {{
    width: 1080px; height: 1350px;
    position: relative;
    background: #08090b;
    overflow: hidden;
}}
/* FONDO EXPANDIDO SUAVE QUE INTEGRA PERFECTAMENTE EL SET DE ESTUDIO */
.backdrop-blur {{
    position: absolute;
    top: -40px; left: -40px; width: 1160px; height: 1430px;
    background-image: url('{PHOTO_URI}');
    background-size: cover;
    background-position: center;
    filter: blur(40px) brightness(0.48);
    opacity: 0.95;
    transform: scale(1.06);
}}
/* FOTO CENTRAL EN FULL-FRAME (100% COMPLETA: CABEZA A BOTAS Y CALABAZAS) */
.fullframe-wrapper {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
}}
.fullframe-img {{
    height: 100%;
    width: auto;
    max-width: 100%;
    object-fit: contain;
    /* Suavizado imperceptible de bordes extremos para continuidad perfecta */
    mask-image: linear-gradient(to right, transparent 0%, black 4%, black 96%, transparent 100%);
    -webkit-mask-image: linear-gradient(to right, transparent 0%, black 4%, black 96%, transparent 100%);
}}
.vignette-overlay {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 65%, rgba(0,0,0,0.5) 100%),
                linear-gradient(to bottom, rgba(0,0,0,0.35) 0%, transparent 16%, transparent 84%, rgba(0,0,0,0.45) 100%);
    pointer-events: none;
    z-index: 20;
}}
</style>
</head>
<body>
<div class="container">
    <div class="backdrop-blur"></div>
    <div class="fullframe-wrapper">
        <img class="fullframe-img" src="{PHOTO_URI}">
    </div>
    <div class="vignette-overlay"></div>
    
    <!-- ESQUINAS DE ENCUADRE DE AUTOR -->
    <div class="corner-bracket cb-tl"></div>
    <div class="corner-bracket cb-tr"></div>
    <div class="corner-bracket cb-bl"></div>
    <div class="corner-bracket cb-br"></div>
    
    <!-- HEADER EDITORIAL LIMPIO -->
    <div class="editorial-header">
        <div class="header-badge"><span class="header-dot"></span>CAPTOORA STUDIO</div>
        <div class="header-badge">EDICIÓN ESPECIAL OTOÑO 2026</div>
    </div>
    
    <!-- SIGNATURE BAR UNIFICADA Y SIN EMPALMES -->
    <div class="signature-bar">
        <img class="sig-logo" src="{LOGO_URI}">
        <div class="sig-brand-text">
            <div class="sig-title">CAPTOOR<span class="lit-a">A</span></div>
            <div class="sig-location">SAN JERÓNIMO · MONTERREY</div>
        </div>
        <div class="sig-divider"></div>
        <div class="sig-tag">DONDE LA MAGIA SUCEDE</div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------
# 2. STORY / REELS 9:16 (1080 x 1920) — NATIVE RATIO FULL-FRAME
# -------------------------------------------------------------
html_story_9x16 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_HEAD}
<style>
.container {{
    width: 1080px; height: 1920px;
    position: relative;
    background: #000000;
    overflow: hidden;
}}
.main-photo {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('{PHOTO_URI}');
    background-size: cover;
    background-position: center;
}}
.vignette-overlay {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(180deg, 
        rgba(0,0,0,0.65) 0%, 
        rgba(0,0,0,0) 22%, 
        rgba(0,0,0,0) 72%, 
        rgba(0,0,0,0.75) 100%);
    pointer-events: none;
    z-index: 20;
}}
.story-header {{
    position: absolute;
    top: 90px;
    left: 80px;
    right: 80px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 60;
}}
.story-footer {{
    position: absolute;
    bottom: 90px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 60;
    background: rgba(8, 10, 12, 0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.85), 0 0 1px rgba(204, 255, 0, 0.35);
    padding: 14px 34px 14px 24px;
    border-radius: 50px;
    display: flex;
    align-items: center;
    gap: 18px;
    white-space: nowrap;
}}
.story-logo {{
    width: 52px;
    height: 52px;
    object-fit: contain;
    filter: drop-shadow(0 2px 12px rgba(204, 255, 0, 0.45));
}}
.story-title {{
    font-family: 'Syncopate', sans-serif;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 5px;
    color: #FFFFFF;
    line-height: 1.1;
}}
.story-sub {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2.5px;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
}}
.story-tag {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #CCFF00;
    text-transform: uppercase;
}}
</style>
</head>
<body>
<div class="container">
    <div class="main-photo"></div>
    <div class="vignette-overlay"></div>
    
    <!-- ESQUINAS DE ENCUADRE -->
    <div class="corner-bracket cb-tl" style="top: 70px; left: 60px;"></div>
    <div class="corner-bracket cb-tr" style="top: 70px; right: 60px;"></div>
    <div class="corner-bracket cb-bl" style="bottom: 70px; left: 60px;"></div>
    <div class="corner-bracket cb-br" style="bottom: 70px; right: 60px;"></div>
    
    <!-- HEADER -->
    <div class="story-header">
        <div class="header-badge" style="font-size: 14px; padding: 10px 22px;"><span class="header-dot"></span>CAPTOORA STUDIO</div>
        <div class="header-badge" style="font-size: 14px; padding: 10px 22px;">EDICIÓN OTOÑO 2026</div>
    </div>
    
    <!-- FOOTER SIGNATURE -->
    <div class="story-footer">
        <img class="story-logo" src="{LOGO_URI}">
        <div style="display: flex; flex-direction: column; gap: 2px;">
            <div class="story-title">CAPTOOR<span class="lit-a">A</span></div>
            <div class="story-sub">COLINAS DE SAN JERÓNIMO · MTY</div>
        </div>
        <div class="sig-divider" style="height: 32px;"></div>
        <div class="story-tag">MEMORIAS QUE TRASCIENDEN</div>
    </div>
</div>
</body>
</html>
"""

def render_html_to_png(html_content, output_png, width, height):
    temp_html = OUT_DIR / f"_temp_{output_png.stem}.html"
    temp_html.write_text(html_content, encoding="utf-8")
    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={output_png}",
        "--virtual-time-budget=2000",
        f"file://{temp_html}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if temp_html.exists():
        temp_html.unlink()
    print(f"✅ Renderizado generado: {output_png} ({width}x{height})")

def main():
    post_4x5_path = OUT_DIR / "CPT_OTONO_D1_POST01_FINAL.png"
    story_9x16_path = OUT_DIR / "CPT_OTONO_D1_POST01_STORY_FINAL.png"
    desktop_copy = DESKTOP_DIR / "CPT_POST01_CORREGIDO_FINAL.png"
    
    render_html_to_png(html_post_4x5, post_4x5_path, 1080, 1350)
    render_html_to_png(html_story_9x16, story_9x16_path, 1080, 1920)
    
    # Copia al escritorio para acceso inmediato del usuario
    shutil.copyfile(post_4x5_path, desktop_copy)
    print(f"✅ Copia directa al Escritorio: {desktop_copy}")

if __name__ == "__main__":
    main()
