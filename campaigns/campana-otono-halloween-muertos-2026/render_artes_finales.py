#!/usr/bin/env python3
"""
Renderizador de Placas Base Visuales Finales Captoora — Día 1:
Monta las imágenes de referencia aprobadas con:
- Visor / encuadre técnico de cámara (viewfinder).
- Logotipo Captoora grande (160px en Story, 110px en Posts).
- Marca CAPTOORA con la ÚLTIMA 'A' iluminada en verde lima (#CCFF00).
- Espacio limpio y despejado diseñado para superponer subtítulos y textos dinámicos en CapCut / Canva.
"""

import os
import subprocess
import base64
from pathlib import Path

BASE_DIR = Path("/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO")
OUT_DIR = BASE_DIR / "campaigns/campana-otono-halloween-muertos-2026/artes_dia_1"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def to_base64_data_uri(path):
    with open(path, "rb") as f:
        data = f.read()
    ext = path.suffix.lower().replace(".", "")
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"

LOGO_URI = to_base64_data_uri(BASE_DIR / "assets/captoora_logo_circle_centered.png")
PHOTO_STORY1_URI = to_base64_data_uri(BASE_DIR / "assets/referencias_generadas/ref_studio_halloween_9x16.jpg")
PHOTO_POST2_URI = to_base64_data_uri(BASE_DIR / "assets/referencias_generadas/ref_park_autumn_3x4.jpg")

COMMON_HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;800;900&family=Space+Grotesk:wght@500;600;700&family=Syncopate:wght@700&display=swap" rel="stylesheet">
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
    text-shadow: 0 0 16px rgba(204, 255, 0, 0.95), 0 0 32px rgba(204, 255, 0, 0.5);
}

/* MARCO ESTILO ENCUADRE DE CÁMARA (VIEWFINDER PROFESIONAL) */
.camera-viewfinder {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none;
    z-index: 50;
    padding: 60px 50px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.corner-tl {
    position: absolute; top: 60px; left: 50px;
    width: 60px; height: 60px;
    border-top: 3.5px solid #CCFF00;
    border-left: 3.5px solid #CCFF00;
}
.corner-tr {
    position: absolute; top: 60px; right: 50px;
    width: 60px; height: 60px;
    border-top: 3.5px solid #CCFF00;
    border-right: 3.5px solid #CCFF00;
}
.corner-bl {
    position: absolute; bottom: 60px; left: 50px;
    width: 60px; height: 60px;
    border-bottom: 3.5px solid #CCFF00;
    border-left: 3.5px solid #CCFF00;
}
.corner-br {
    position: absolute; bottom: 60px; right: 50px;
    width: 60px; height: 60px;
    border-bottom: 3.5px solid #CCFF00;
    border-right: 3.5px solid #CCFF00;
}
.reticle-center {
    position: absolute;
    top: 48%; left: 50%;
    transform: translate(-50%, -50%);
    width: 44px; height: 44px;
    pointer-events: none;
    opacity: 0.5;
}
.reticle-center::before {
    content: ''; position: absolute;
    top: 21px; left: 0; width: 44px; height: 2px;
    background: #CCFF00;
}
.reticle-center::after {
    content: ''; position: absolute;
    top: 0; left: 21px; width: 2px; height: 44px;
    background: #CCFF00;
}
.telemetry-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Orbitron', monospace;
    font-size: 19px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.9);
}
.rec-dot {
    display: inline-block;
    width: 14px; height: 14px;
    background-color: #FF2E2E;
    border-radius: 50%;
    margin-right: 8px;
    box-shadow: 0 0 12px #FF2E2E;
}
.telemetry-chip {
    background: rgba(10, 10, 10, 0.72);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.16);
    padding: 8px 18px;
    border-radius: 8px;
}
</style>
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
    print(f"✅ Renderizado final: {output_png.name} ({width}x{height})")

# 1. STORY 01 — PLACA BASE LIMPIA PARA CAPCUT / CANVA (1080x1920)
html_story1 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_HEAD}
<style>
.container {{
    width: 1080px; height: 1920px;
    position: relative;
    background: #000000;
}}
.bg-img {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('{PHOTO_STORY1_URI}');
    background-size: cover;
    background-position: center;
}}
.vignette {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(180deg, 
        rgba(0,0,0,0.7) 0%, 
        rgba(0,0,0,0) 25%, 
        rgba(0,0,0,0) 65%, 
        rgba(0,0,0,0.85) 100%);
    pointer-events: none;
}}
.logo-box {{
    position: absolute;
    top: 130px;
    left: 80px;
    z-index: 60;
}}
.logo-large {{
    width: 160px;
    height: 160px;
    object-fit: contain;
    filter: drop-shadow(0 4px 25px rgba(0,0,0,0.9));
}}
.footer-badge {{
    position: absolute;
    bottom: 95px;
    left: 80px;
    right: 80px;
    z-index: 60;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(10, 10, 10, 0.78);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.18);
    padding: 16px 32px;
    border-radius: 50px;
}}
.brand-name {{
    font-family: 'Syncopate', sans-serif;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 5px;
    color: #FFFFFF;
}}
.geo-tag {{
    font-family: 'Orbitron', monospace;
    font-size: 17px;
    letter-spacing: 3px;
    color: #CCFF00;
}}
</style>
</head>
<body>
<div class="container">
    <div class="bg-img"></div>
    <div class="vignette"></div>
    
    <div class="camera-viewfinder">
        <div class="corner-tl"></div>
        <div class="corner-tr"></div>
        <div class="corner-bl"></div>
        <div class="corner-br"></div>
        <div class="reticle-center"></div>
        
        <div class="telemetry-row">
            <div class="telemetry-chip"><span class="rec-dot"></span>REC · 4K</div>
            <div class="telemetry-chip">BAT 96% [▮▮▮▯]</div>
        </div>
        <div class="telemetry-row">
            <div class="telemetry-chip">ISO 200 · 1/250s · f/2.2</div>
            <div class="telemetry-chip">[ 9:16 RAW ]</div>
        </div>
    </div>
    
    <!-- Logo protagonista más grande -->
    <div class="logo-box">
        <img class="logo-large" src="{LOGO_URI}">
    </div>
    
    <!-- Identificador inferior con última 'A' iluminada -->
    <div class="footer-badge">
        <div class="brand-name">CAPTOOR<span class="lit-a">A</span></div>
        <div class="geo-tag">SAN JERÓNIMO · MTY</div>
    </div>
</div>
</body>
</html>
"""

# 2. POST 01 (1080x1350 Feed - Halloween Studio)
html_post1 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_HEAD}
<style>
.container {{
    width: 1080px; height: 1350px;
    position: relative;
    background: #000000;
}}
.main-photo {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('{PHOTO_STORY1_URI}');
    background-size: cover;
    background-position: center;
}}
.vignette {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(circle at 50% 50%, rgba(0,0,0,0) 65%, rgba(0,0,0,0.65) 100%);
    pointer-events: none;
}}
.logo-corner {{
    position: absolute;
    bottom: 65px;
    right: 65px;
    z-index: 60;
}}
.logo-post {{
    width: 110px;
    height: 110px;
    object-fit: contain;
    filter: drop-shadow(0 4px 20px rgba(0,0,0,0.85));
}}
.brand-callout {{
    position: absolute;
    bottom: 75px;
    left: 65px;
    z-index: 60;
    background: rgba(10, 10, 10, 0.82);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.18);
    padding: 14px 26px;
    border-radius: 40px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.brand-name-callout {{
    font-family: 'Syncopate', sans-serif;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #FFFFFF;
}}
.sub-tag {{
    font-family: 'Orbitron', monospace;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #CCFF00;
    border-left: 1px solid rgba(255,255,255,0.3);
    padding-left: 12px;
}}
</style>
</head>
<body>
<div class="container">
    <div class="main-photo"></div>
    <div class="vignette"></div>
    
    <div class="camera-viewfinder">
        <div class="corner-tl"></div>
        <div class="corner-tr"></div>
        <div class="corner-bl"></div>
        <div class="corner-br"></div>
        <div class="reticle-center"></div>
        
        <div class="telemetry-row">
            <div class="telemetry-chip"><span class="rec-dot"></span>STANDBY</div>
            <div class="telemetry-chip">85mm · PRO LIGHT</div>
        </div>
        <div class="telemetry-row">
            <div class="telemetry-chip">ISO 100 · 1/250s · f/2.2</div>
            <div class="telemetry-chip">[ 4:5 FULL-FRAME ]</div>
        </div>
    </div>
    
    <div class="brand-callout">
        <div class="brand-name-callout">CAPTOOR<span class="lit-a">A</span></div>
        <div class="sub-tag">SET CLIMATIZADO</div>
    </div>
    
    <div class="logo-corner">
        <img class="logo-post" src="{LOGO_URI}">
    </div>
</div>
</body>
</html>
"""

# 3. POST 02 (1080x1350 Feed - Parque Exterior)
html_post2 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_HEAD}
<style>
.container {{
    width: 1080px; height: 1350px;
    position: relative;
    background: #000000;
}}
.main-photo {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('{PHOTO_POST2_URI}');
    background-size: cover;
    background-position: center;
}}
.vignette {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(circle at 50% 50%, rgba(0,0,0,0) 65%, rgba(0,0,0,0.6) 100%);
    pointer-events: none;
}}
.logo-corner {{
    position: absolute;
    bottom: 65px;
    right: 65px;
    z-index: 60;
}}
.logo-post {{
    width: 110px;
    height: 110px;
    object-fit: contain;
    filter: drop-shadow(0 4px 20px rgba(0,0,0,0.85));
}}
.brand-callout {{
    position: absolute;
    bottom: 75px;
    left: 65px;
    z-index: 60;
    background: rgba(10, 10, 10, 0.82);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.18);
    padding: 14px 26px;
    border-radius: 40px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.brand-name-callout {{
    font-family: 'Syncopate', sans-serif;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #FFFFFF;
}}
.sub-tag {{
    font-family: 'Orbitron', monospace;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #CCFF00;
    border-left: 1px solid rgba(255,255,255,0.3);
    padding-left: 12px;
}}
</style>
</head>
<body>
<div class="container">
    <div class="main-photo"></div>
    <div class="vignette"></div>
    
    <div class="camera-viewfinder">
        <div class="corner-tl"></div>
        <div class="corner-tr"></div>
        <div class="corner-bl"></div>
        <div class="corner-br"></div>
        <div class="reticle-center"></div>
        
        <div class="telemetry-row">
            <div class="telemetry-chip"><span class="rec-dot"></span>GOLDEN HOUR</div>
            <div class="telemetry-chip">85mm · NATURAL</div>
        </div>
        <div class="telemetry-row">
            <div class="telemetry-chip">ISO 100 · 1/500s · f/1.4</div>
            <div class="telemetry-chip">[ 4:5 EXTERIOR ]</div>
        </div>
    </div>
    
    <div class="brand-callout">
        <div class="brand-name-callout">CAPTOOR<span class="lit-a">A</span></div>
        <div class="sub-tag">PARQUE CONTIGUO</div>
    </div>
    
    <div class="logo-corner">
        <img class="logo-post" src="{LOGO_URI}">
    </div>
</div>
</body>
</html>
"""

render_html_to_png(html_story1, OUT_DIR / "CPT_OTONO_D1_STORY01_FINAL_BASE.png", 1080, 1920)
render_html_to_png(html_post1, OUT_DIR / "CPT_OTONO_D1_POST01_FINAL.png", 1080, 1350)
render_html_to_png(html_post2, OUT_DIR / "CPT_OTONO_D1_POST02_FINAL.png", 1080, 1350)

print("\n🎉 Placas base finales generadas exitosamente en:", OUT_DIR)
