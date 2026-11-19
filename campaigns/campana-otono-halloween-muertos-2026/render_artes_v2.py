#!/usr/bin/env python3
"""
Renderizador V2 de Artes Captoora — Incorpora feedback directo del fundador:
1. Fotografías reales de PEXELS (Halloween y parque de otoño).
2. Tipografía display futurista / geométrica estilo Stellar (Syncopate + Orbitron).
3. Monograma oficial centrado en el círculo y con fondo transparente.
4. Palabra CAPTOORA iluminando ÚNICAMENTE la letra 'A' en verde lima (#CCFF00).
5. Marco con decoración y telemetría de encuadre de cámara (viewfinder profesional).
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
PHOTO_STORY1_URI = to_base64_data_uri(BASE_DIR / "assets/pexels/story1_kid_pumpkin_5435308.jpg")
PHOTO_POST1_URI = to_base64_data_uri(BASE_DIR / "assets/pexels/post1_studio_halloween_9740407.jpg")
PHOTO_POST2_URI = to_base64_data_uri(BASE_DIR / "assets/pexels/post2_park_autumn_28931714.jpg")

COMMON_HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;800;900&family=Space+Grotesk:wght@500;700&family=Syncopate:wght@700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background-color: #000000;
    color: #FFFFFF;
    font-family: 'Space Grotesk', -apple-system, sans-serif;
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
}
.font-display {
    font-family: 'Syncopate', 'Orbitron', sans-serif;
    text-transform: uppercase;
}
.lit-a {
    color: #CCFF00 !important;
    text-shadow: 0 0 16px rgba(204, 255, 0, 0.9), 0 0 32px rgba(204, 255, 0, 0.4);
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
/* Esquinas de cámara */
.corner-tl {
    position: absolute; top: 60px; left: 50px;
    width: 60px; height: 60px;
    border-top: 3px solid #CCFF00;
    border-left: 3px solid #CCFF00;
}
.corner-tr {
    position: absolute; top: 60px; right: 50px;
    width: 60px; height: 60px;
    border-top: 3px solid #CCFF00;
    border-right: 3px solid #CCFF00;
}
.corner-bl {
    position: absolute; bottom: 60px; left: 50px;
    width: 60px; height: 60px;
    border-bottom: 3px solid #CCFF00;
    border-left: 3px solid #CCFF00;
}
.corner-br {
    position: absolute; bottom: 60px; right: 50px;
    width: 60px; height: 60px;
    border-bottom: 3px solid #CCFF00;
    border-right: 3px solid #CCFF00;
}
/* Retícula central */
.reticle-center {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 50px; height: 50px;
    pointer-events: none;
    opacity: 0.55;
}
.reticle-center::before {
    content: ''; position: absolute;
    top: 24px; left: 0; width: 50px; height: 2px;
    background: #CCFF00;
}
.reticle-center::after {
    content: ''; position: absolute;
    top: 0; left: 24px; width: 2px; height: 50px;
    background: #CCFF00;
}
.telemetry-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Orbitron', monospace;
    font-size: 19px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.85);
}
.rec-dot {
    display: inline-block;
    width: 14px; height: 14px;
    background-color: #FF2E2E;
    border-radius: 50%;
    margin-right: 8px;
    box-shadow: 0 0 10px #FF2E2E;
}
.telemetry-chip {
    background: rgba(10, 10, 10, 0.65);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.15);
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
    print(f"✅ V2 Renderizado: {output_png.name} ({width}x{height})")

# -------------------------------------------------------------
# 1. PIEZA 1: STORY 01 (1080x1920) — Pexels Kid Pumpkin
# -------------------------------------------------------------
html_story1 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_HEAD}
<style>
.container {{
    width: 1080px; height: 1920px;
    position: relative;
    background: #050505;
}}
.bg-img {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('{PHOTO_STORY1_URI}');
    background-size: cover;
    background-position: center 30%;
    filter: brightness(0.78) contrast(1.1);
}}
.overlay-gradient {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(180deg, 
        rgba(0,0,0,0.85) 0%, 
        rgba(0,0,0,0.15) 30%, 
        rgba(0,0,0,0.2) 60%, 
        rgba(0,0,0,0.95) 88%);
}}
.brand-header {{
    position: relative; z-index: 60;
    display: flex; align-items: center; justify-content: space-between;
    padding: 130px 80px 0 80px;
}}
.brand-lockup {{
    display: flex; align-items: center; gap: 20px;
}}
.logo-img {{
    width: 86px; height: 86px; object-fit: contain;
}}
.brand-title {{
    font-family: 'Syncopate', sans-serif;
    font-size: 32px; font-weight: 700; letter-spacing: 6px;
    text-transform: uppercase; color: #FFFFFF;
}}
.story-headline-box {{
    position: absolute; bottom: 330px; left: 80px; right: 80px;
    z-index: 60;
}}
.headline {{
    font-family: 'Syncopate', sans-serif;
    font-size: 50px; font-weight: 700; line-height: 1.18;
    letter-spacing: 2px; text-transform: uppercase;
    color: #FFFFFF; margin-bottom: 35px;
}}
.poll-widget {{
    background: rgba(14, 14, 14, 0.88);
    backdrop-filter: blur(25px);
    border: 1.5px solid rgba(204, 255, 0, 0.4);
    border-radius: 30px;
    padding: 35px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.85);
}}
.poll-question {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px; font-weight: 700; text-align: center;
    margin-bottom: 25px; line-height: 1.3; color: #FFFFFF;
}}
.poll-bar {{
    background: rgba(255,255,255,0.08);
    border: 1.5px solid rgba(255,255,255,0.2);
    border-radius: 18px; padding: 20px 28px;
    font-size: 24px; font-weight: 700;
    display: flex; justify-content: space-between;
    margin-bottom: 14px;
}}
.poll-bar.highlight {{
    background: rgba(204, 255, 0, 0.15);
    border-color: #CCFF00;
    color: #CCFF00;
}}
.footer-geo {{
    position: absolute; bottom: 100px; left: 0; width: 100%;
    text-align: center; font-size: 22px; font-family: 'Orbitron', monospace;
    letter-spacing: 4px; color: rgba(255,255,255,0.6); z-index: 60;
}}
</style>
</head>
<body>
<div class="container">
    <div class="bg-img"></div>
    <div class="overlay-gradient"></div>
    
    <!-- Marco de cámara -->
    <div class="camera-viewfinder">
        <div class="corner-tl"></div>
        <div class="corner-tr"></div>
        <div class="corner-bl"></div>
        <div class="corner-br"></div>
        <div class="reticle-center"></div>
        
        <div class="telemetry-row">
            <div class="telemetry-chip"><span class="rec-dot"></span>REC · 4K</div>
            <div class="telemetry-chip">BAT 92% [▮▮▮▯]</div>
        </div>
        <div class="telemetry-row">
            <div class="telemetry-chip">ISO 200 · 1/250s · f/2.0</div>
            <div class="telemetry-chip">[ 9:16 RAW ]</div>
        </div>
    </div>
    
    <!-- Header de marca con letra A iluminada -->
    <div class="brand-header">
        <div class="brand-lockup">
            <img class="logo-img" src="{LOGO_URI}">
            <div class="brand-title">C<span class="lit-a">A</span>PTOORA</div>
        </div>
    </div>
    
    <div class="story-headline-box">
        <h1 class="headline">El disfraz dura una noche.<br><span class="lit-a">El retrato dura toda la vida.</span></h1>
        
        <div class="poll-widget">
            <div class="poll-question">¿Cuántos disfraces tienes en el clóset que solo salieron en una foto movida?</div>
            <div class="poll-bar highlight">
                <span>Demasiados 😭</span>
                <span>81%</span>
            </div>
            <div class="poll-bar">
                <span>Ni me recuerdes 🙈</span>
                <span>19%</span>
            </div>
        </div>
    </div>
    
    <div class="footer-geo">
        SAN JERÓNIMO · MONTERREY · ESTUDIO & EXTERIOR
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------
# 2. PIEZA 2: POST 01 (1080x1350 Feed) — Pexels Studio Halloween
# -------------------------------------------------------------
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
    background-image: url('{PHOTO_POST1_URI}');
    background-size: cover;
    background-position: center;
}}
.vignette-cinema {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(circle at 50% 50%, rgba(0,0,0,0) 65%, rgba(0,0,0,0.65) 100%);
    pointer-events: none;
}}
.bottom-branding-bar {{
    position: absolute; bottom: 70px; left: 60px; right: 60px;
    display: flex; justify-content: space-between; align-items: center;
    z-index: 60;
}}
.brand-pill {{
    display: flex; align-items: center; gap: 16px;
    background: rgba(10, 10, 10, 0.78);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.18);
    padding: 14px 28px;
    border-radius: 50px;
}}
.brand-logo-small {{
    width: 48px; height: 48px; object-fit: contain;
}}
.brand-word {{
    font-family: 'Syncopate', sans-serif;
    font-size: 24px; font-weight: 700; letter-spacing: 4px;
    text-transform: uppercase; color: #FFFFFF;
}}
.tag-pill {{
    font-family: 'Orbitron', monospace;
    font-size: 17px; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: #CCFF00;
    background: rgba(10, 10, 10, 0.78);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(204, 255, 0, 0.4);
    padding: 14px 24px;
    border-radius: 50px;
}}
</style>
</head>
<body>
<div class="container">
    <div class="main-photo"></div>
    <div class="vignette-cinema"></div>
    
    <!-- Marco de cámara -->
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
            <div class="telemetry-chip">ISO 100 · 1/250s · f/4.0</div>
            <div class="telemetry-chip">[ 4:5 FULL-FRAME ]</div>
        </div>
    </div>
    
    <div class="bottom-branding-bar">
        <div class="brand-pill">
            <img class="brand-logo-small" src="{LOGO_URI}">
            <div class="brand-word">C<span class="lit-a">A</span>PTOORA</div>
        </div>
        <div class="tag-pill">SET CLIMATIZADO · SAN JERÓNIMO</div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------
# 3. PIEZA 3: POST 02 (1080x1350 Feed) — Pexels Park Autumn
# -------------------------------------------------------------
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
.vignette-cinema {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(circle at 50% 50%, rgba(0,0,0,0) 65%, rgba(0,0,0,0.6) 100%);
    pointer-events: none;
}}
.bottom-branding-bar {{
    position: absolute; bottom: 70px; left: 60px; right: 60px;
    display: flex; justify-content: space-between; align-items: center;
    z-index: 60;
}}
.brand-pill {{
    display: flex; align-items: center; gap: 16px;
    background: rgba(10, 10, 10, 0.78);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.18);
    padding: 14px 28px;
    border-radius: 50px;
}}
.brand-logo-small {{
    width: 48px; height: 48px; object-fit: contain;
}}
.brand-word {{
    font-family: 'Syncopate', sans-serif;
    font-size: 24px; font-weight: 700; letter-spacing: 4px;
    text-transform: uppercase; color: #FFFFFF;
}}
.tag-pill {{
    font-family: 'Orbitron', monospace;
    font-size: 17px; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: #CCFF00;
    background: rgba(10, 10, 10, 0.78);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(204, 255, 0, 0.4);
    padding: 14px 24px;
    border-radius: 50px;
}}
</style>
</head>
<body>
<div class="container">
    <div class="main-photo"></div>
    <div class="vignette-cinema"></div>
    
    <!-- Marco de cámara -->
    <div class="camera-viewfinder">
        <div class="corner-tl"></div>
        <div class="corner-tr"></div>
        <div class="corner-bl"></div>
        <div class="corner-br"></div>
        <div class="reticle-center"></div>
        
        <div class="telemetry-row">
            <div class="telemetry-chip"><span class="rec-dot"></span>GOLDEN HOUR</div>
            <div class="telemetry-chip">50mm · NATURAL</div>
        </div>
        <div class="telemetry-row">
            <div class="telemetry-chip">ISO 100 · 1/500s · f/1.8</div>
            <div class="telemetry-chip">[ 4:5 EXTERIOR ]</div>
        </div>
    </div>
    
    <div class="bottom-branding-bar">
        <div class="brand-pill">
            <img class="brand-logo-small" src="{LOGO_URI}">
            <div class="brand-word">C<span class="lit-a">A</span>PTOORA</div>
        </div>
        <div class="tag-pill">LUZ NATURAL · PARQUE CONTIGUO</div>
    </div>
</div>
</body>
</html>
"""

# Renderizar las 3 piezas corregidas
render_html_to_png(html_story1, OUT_DIR / "CPT_OTONO_D1_STORY01_V2.png", 1080, 1920)
render_html_to_png(html_post1, OUT_DIR / "CPT_OTONO_D1_POST01_V2.png", 1080, 1350)
render_html_to_png(html_post2, OUT_DIR / "CPT_OTONO_D1_POST02_V2.png", 1080, 1350)

print("\n🎯 Renders V2 completados al 100%. Listos para revisión del fundador.")
