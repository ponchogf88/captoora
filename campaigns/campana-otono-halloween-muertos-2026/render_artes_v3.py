#!/usr/bin/env python3
"""
Renderizador V3 de Artes Captoora:
1. Fotografías ultra-profesionales estilo Canva (Pexels #13601726 niña calabaza, #5859337 niña brujita estudio, #28931714 parque otoño).
2. Textos revisados con espaciado generoso para garantizar CERO empalmes.
3. Logotipo de Captoora sustancialmente MÁS GRANDE (160px en Story, 105px en Post) y ÚNICAMENTE el logo como isotipo protagonista.
4. En la palabra CAPTOORA, se ilumina ÚNICAMENTE la ÚLTIMA letra ('A'): CAPTOOR<span class="lit-a">A</span>.
5. Marco decorativo estilo cámara fotográfica profesional (viewfinder con esquinas, telemetría y retícula).
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
PHOTO_STORY1_URI = to_base64_data_uri(BASE_DIR / "assets/pexels/story1_girl_pumpkin_13601726.jpg")
PHOTO_POST1_URI = to_base64_data_uri(BASE_DIR / "assets/pexels/post1_witch_child_5859337.jpg")
PHOTO_POST2_URI = to_base64_data_uri(BASE_DIR / "assets/pexels/post2_park_autumn_28931714.jpg")

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
    top: 45%; left: 50%;
    transform: translate(-50%, -50%);
    width: 44px; height: 44px;
    pointer-events: none;
    opacity: 0.55;
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
    color: rgba(255, 255, 255, 0.88);
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
    background: rgba(10, 10, 10, 0.7);
    backdrop-filter: blur(12px);
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
    print(f"✅ V3 Renderizado: {output_png.name} ({width}x{height})")

# -------------------------------------------------------------
# 1. PIEZA 1: STORY 01 (1080x1920)
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
    background-position: center 20%;
    filter: brightness(0.85) contrast(1.08);
}}
.overlay-gradient {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(180deg, 
        rgba(0,0,0,0.85) 0%, 
        rgba(0,0,0,0.1) 28%, 
        rgba(0,0,0,0.15) 55%, 
        rgba(0,0,0,0.95) 82%,
        rgba(0,0,0,1) 100%);
}}
.logo-container {{
    position: absolute;
    top: 130px;
    left: 80px;
    z-index: 60;
}}
.logo-large {{
    width: 160px;
    height: 160px;
    object-fit: contain;
    filter: drop-shadow(0 4px 20px rgba(0,0,0,0.8));
}}
.story-bottom-box {{
    position: absolute;
    bottom: 90px;
    left: 70px;
    right: 70px;
    z-index: 60;
    display: flex;
    flex-direction: column;
    gap: 28px;
}}
.headline {{
    font-family: 'Syncopate', sans-serif;
    font-size: 38px;
    font-weight: 700;
    line-height: 1.3;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FFFFFF;
    text-shadow: 0 4px 15px rgba(0,0,0,0.9);
}}
.poll-card {{
    background: rgba(14, 14, 14, 0.92);
    backdrop-filter: blur(25px);
    border: 1.5px solid rgba(204, 255, 0, 0.4);
    border-radius: 28px;
    padding: 30px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    display: flex;
    flex-direction: column;
    gap: 18px;
}}
.poll-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 700;
    text-align: center;
    color: #FFFFFF;
    line-height: 1.35;
}}
.poll-choice {{
    background: rgba(255,255,255,0.08);
    border: 1.5px solid rgba(255,255,255,0.22);
    border-radius: 16px;
    padding: 18px 24px;
    font-size: 23px;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.poll-choice.featured {{
    background: rgba(204, 255, 0, 0.16);
    border-color: #CCFF00;
    color: #CCFF00;
}}
.footer-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Orbitron', monospace;
    font-size: 20px;
    letter-spacing: 3px;
    color: rgba(255,255,255,0.75);
    padding: 0 10px;
}}
.footer-brand {{
    font-family: 'Syncopate', sans-serif;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #FFFFFF;
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
            <div class="telemetry-chip">BAT 96% [▮▮▮▯]</div>
        </div>
        <div class="telemetry-row">
            <div class="telemetry-chip">ISO 200 · 1/250s · f/2.0</div>
            <div class="telemetry-chip">[ 9:16 RAW ]</div>
        </div>
    </div>
    
    <!-- Logo ÚNICAMENTE el logo y MÁS GRANDE -->
    <div class="logo-container">
        <img class="logo-large" src="{LOGO_URI}">
    </div>
    
    <!-- Textos con espaciado amplio para evitar empalmes -->
    <div class="story-bottom-box">
        <h1 class="headline">El disfraz dura una noche.<br>El recuerdo dura toda la vida.</h1>
        
        <div class="poll-card">
            <div class="poll-title">¿Cuántos disfraces tienes en el clóset que solo salieron en una foto movida?</div>
            <div class="poll-choice featured">
                <span>Demasiados 😭</span>
                <span>83%</span>
            </div>
            <div class="poll-choice">
                <span>Ni me recuerdes 🙈</span>
                <span>17%</span>
            </div>
        </div>
        
        <div class="footer-bar">
            <div class="footer-brand">CAPTOOR<span class="lit-a">A</span> STUDIO</div>
            <div>SAN JERÓNIMO MTY</div>
        </div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------
# 2. PIEZA 2: POST 01 (1080x1350 Feed - Halloween Studio)
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
/* Logo grande independiente */
.logo-corner {{
    position: absolute;
    bottom: 65px;
    right: 65px;
    z-index: 60;
}}
.logo-post {{
    width: 108px;
    height: 108px;
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
    
    <!-- Identificador con última letra 'A' iluminada -->
    <div class="brand-callout">
        <div class="brand-name-callout">CAPTOOR<span class="lit-a">A</span></div>
        <div class="sub-tag">SET CLIMATIZADO</div>
    </div>
    
    <!-- Únicamente el logo y más grande -->
    <div class="logo-corner">
        <img class="logo-post" src="{LOGO_URI}">
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------
# 3. PIEZA 3: POST 02 (1080x1350 Feed - Parque Otoño)
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
.logo-corner {{
    position: absolute;
    bottom: 65px;
    right: 65px;
    z-index: 60;
}}
.logo-post {{
    width: 108px;
    height: 108px;
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
    
    <!-- Identificador con última letra 'A' iluminada -->
    <div class="brand-callout">
        <div class="brand-name-callout">CAPTOOR<span class="lit-a">A</span></div>
        <div class="sub-tag">PARQUE CONTIGUO</div>
    </div>
    
    <!-- Únicamente el logo y más grande -->
    <div class="logo-corner">
        <img class="logo-post" src="{LOGO_URI}">
    </div>
</div>
</body>
</html>
"""

# Renderizar los 3 artes V3
render_html_to_png(html_story1, OUT_DIR / "CPT_OTONO_D1_STORY01_V3.png", 1080, 1920)
render_html_to_png(html_post1, OUT_DIR / "CPT_OTONO_D1_POST01_V3.png", 1080, 1350)
render_html_to_png(html_post2, OUT_DIR / "CPT_OTONO_D1_POST02_V3.png", 1080, 1350)

print("\n🚀 Renders V3 completados exitosamente en:", OUT_DIR)
