#!/usr/bin/env python3
"""
Renderizador Autónomo de Artes para el Día 1 de la Campaña de Otoño Captoora
Genera archivos PNG oficiales a 1080x1920 y 1080x1350 respetando la Ley Visual Captoora.
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

LOGO_URI = to_base64_data_uri(BASE_DIR / "assets/captoora_monograma_destello_master.png")
PHOTO_STUDIO_URI = to_base64_data_uri(BASE_DIR / "assets/media_jpg/pf-peloni-02.jpg")
PHOTO_PARK_URI = to_base64_data_uri(BASE_DIR / "assets/media_jpg/pf-chipinque-01.jpg")
PHOTO_GLOW_URI = to_base64_data_uri(BASE_DIR / "assets/media_jpg/pf-glow-cpt_0855.jpg")

COMMON_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background-color: #0A0A0A;
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    overflow: hidden;
}
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
        "--virtual-time-budget=1500",
        f"file://{temp_html}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if temp_html.exists():
        temp_html.unlink()
    print(f"✅ Renderizado: {output_png.name} ({width}x{height})")

# 1. STORY 01 (1080x1920)
html_story1 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.story-container {{
    width: 1080px;
    height: 1920px;
    position: relative;
    background: #0A0A0A;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 100px 80px 140px 80px;
}}
.bg-photo {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('{PHOTO_GLOW_URI}');
    background-size: cover;
    background-position: center;
    opacity: 0.65;
    filter: contrast(1.15) brightness(0.85);
}}
.gradient-overlay {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(180deg, rgba(10,10,10,0.85) 0%, rgba(10,10,10,0.2) 40%, rgba(10,10,10,0.95) 85%);
}}
.header {{
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.logo {{
    width: 140px;
    height: 140px;
    object-fit: contain;
}}
.badge {{
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #CCFF00;
    border: 2px solid #CCFF00;
    padding: 10px 24px;
    border-radius: 40px;
    background: rgba(204, 255, 0, 0.1);
}}
.content-box {{
    position: relative;
    z-index: 10;
    margin-bottom: 80px;
}}
.headline {{
    font-size: 58px;
    font-weight: 800;
    line-height: 1.18;
    letter-spacing: -1.5px;
    margin-bottom: 40px;
    color: #FFFFFF;
}}
.headline span {{
    color: #CCFF00;
}}
.poll-mockup {{
    background: rgba(25, 25, 25, 0.9);
    border: 2px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(20px);
    border-radius: 36px;
    padding: 40px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
}}
.poll-question {{
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 30px;
    line-height: 1.3;
}}
.poll-options {{
    display: flex;
    flex-direction: column;
    gap: 18px;
}}
.poll-opt {{
    background: rgba(255,255,255,0.08);
    border: 2px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 22px;
    font-size: 28px;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.poll-opt.active {{
    border-color: #CCFF00;
    background: rgba(204, 255, 0, 0.15);
    color: #CCFF00;
}}
.footer-text {{
    position: relative;
    z-index: 10;
    text-align: center;
    font-size: 26px;
    color: rgba(255,255,255,0.6);
    letter-spacing: 1px;
}}
</style>
</head>
<body>
<div class="story-container">
    <div class="bg-photo"></div>
    <div class="gradient-overlay"></div>
    
    <div class="header">
        <img class="logo" src="{LOGO_URI}">
        <div class="badge">Captoora Studio</div>
    </div>
    
    <div class="content-box">
        <h1 class="headline">El disfraz dura una noche.<br><span>El retrato dura toda la vida.</span></h1>
        
        <div class="poll-mockup">
            <div class="poll-question">¿Cuántos disfraces tienes en el clóset que solo existen en una foto movida?</div>
            <div class="poll-options">
                <div class="poll-opt active"><span>Demasiados 😭</span> <span>78%</span></div>
                <div class="poll-opt"><span>Ni me recuerdes 🙈</span> <span>22%</span></div>
            </div>
        </div>
    </div>
    
    <div class="footer-text">
        📍 Paseo de los Álamos 165 · San Jerónimo Mty
    </div>
</div>
</body>
</html>
"""

# 2. POST FOTO 01 (1080x1350 Feed - Full-Frame Studio Retrato)
html_post1 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.post-container {{
    width: 1080px;
    height: 1350px;
    position: relative;
    background: #000000;
}}
.main-photo {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('{PHOTO_STUDIO_URI}');
    background-size: cover;
    background-position: center top;
}}
.vignette {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(circle at 50% 40%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.65) 100%);
    pointer-events: none;
}}
.bottom-branding {{
    position: absolute;
    bottom: 50px;
    right: 50px;
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(10, 10, 10, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 12px 24px;
    border-radius: 50px;
}}
.logo-micro {{
    width: 48px;
    height: 48px;
    object-fit: contain;
}}
.brand-name {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FFFFFF;
}}
.brand-name span {{
    color: #CCFF00;
}}
.tag-left {{
    position: absolute;
    top: 50px;
    left: 50px;
    background: rgba(10, 10, 10, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 10px 22px;
    border-radius: 30px;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.85);
}}
</style>
</head>
<body>
<div class="post-container">
    <div class="main-photo"></div>
    <div class="vignette"></div>
    <div class="tag-left">Sesión de Autor · Set Climatizado</div>
    <div class="bottom-branding">
        <img class="logo-micro" src="{LOGO_URI}">
        <div class="brand-name">Capto<span>ora</span></div>
    </div>
</div>
</body>
</html>
"""

# 3. POST FOTO 02 (1080x1350 Feed - Parque Exterior Luz Natural)
html_post2 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.post-container {{
    width: 1080px;
    height: 1350px;
    position: relative;
    background: #000000;
}}
.main-photo {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('{PHOTO_PARK_URI}');
    background-size: cover;
    background-position: center;
}}
.vignette {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(circle at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.6) 100%);
    pointer-events: none;
}}
.bottom-branding {{
    position: absolute;
    bottom: 50px;
    right: 50px;
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(10, 10, 10, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 12px 24px;
    border-radius: 50px;
}}
.logo-micro {{
    width: 48px;
    height: 48px;
    object-fit: contain;
}}
.brand-name {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FFFFFF;
}}
.brand-name span {{
    color: #CCFF00;
}}
.tag-left {{
    position: absolute;
    top: 50px;
    left: 50px;
    background: rgba(10, 10, 10, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 10px 22px;
    border-radius: 30px;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.85);
}}
</style>
</head>
<body>
<div class="post-container">
    <div class="main-photo"></div>
    <div class="vignette"></div>
    <div class="tag-left">Luz Natural · Parque Contiguo</div>
    <div class="bottom-branding">
        <img class="logo-micro" src="{LOGO_URI}">
        <div class="brand-name">Capto<span>ora</span></div>
    </div>
</div>
</body>
</html>
"""

# 4. STORY 03 (1080x1920 - Nocturna + Caja de Preguntas)
html_story3 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.story-container {{
    width: 1080px;
    height: 1920px;
    position: relative;
    background: #0A0A0A;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 100px 80px 140px 80px;
}}
.bg-photo {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('{PHOTO_GLOW_URI}');
    background-size: cover;
    background-position: center;
    opacity: 0.55;
    filter: contrast(1.2) brightness(0.65);
}}
.gradient-overlay {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(180deg, rgba(10,10,10,0.85) 0%, rgba(10,10,10,0.1) 40%, rgba(10,10,10,0.95) 85%);
}}
.header {{
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.logo {{
    width: 140px;
    height: 140px;
    object-fit: contain;
}}
.badge {{
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #CCFF00;
    border: 2px solid #CCFF00;
    padding: 10px 24px;
    border-radius: 40px;
    background: rgba(204, 255, 0, 0.1);
}}
.content-box {{
    position: relative;
    z-index: 10;
    margin-bottom: 80px;
}}
.headline {{
    font-size: 54px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 40px;
    color: #FFFFFF;
}}
.headline span {{
    color: #CCFF00;
}}
.question-mockup {{
    background: rgba(20, 20, 20, 0.95);
    border: 2px solid rgba(204, 255, 0, 0.3);
    border-radius: 36px;
    padding: 40px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.9);
}}
.q-title {{
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 24px;
    text-align: center;
    color: #FFFFFF;
}}
.q-box {{
    background: rgba(255,255,255,0.06);
    border: 2px dashed rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 24px;
    font-size: 26px;
    color: rgba(255,255,255,0.5);
    text-align: center;
}}
.footer-text {{
    position: relative;
    z-index: 10;
    text-align: center;
    font-size: 26px;
    color: rgba(255,255,255,0.6);
    letter-spacing: 1px;
}}
</style>
</head>
<body>
<div class="story-container">
    <div class="bg-photo"></div>
    <div class="gradient-overlay"></div>
    
    <div class="header">
        <img class="logo" src="{LOGO_URI}">
        <div class="badge">Noche en Set</div>
    </div>
    
    <div class="content-box">
        <h1 class="headline">Las sombras más limpias<br><span>se esculpen con luz real.</span></h1>
        
        <div class="question-mockup">
            <div class="q-title">¿Qué disfraz o temática van a usar este año? 📸</div>
            <div class="q-box">Escribe tu respuesta aquí y te decimos cómo se vería iluminado en nuestro set...</div>
        </div>
    </div>
    
    <div class="footer-text">
        WhatsApp: 81 4005 0088 · Colinas de San Jerónimo
    </div>
</div>
</body>
</html>
"""

# Ejecutar renders
render_html_to_png(html_story1, OUT_DIR / "CPT_OTONO_D1_STORY01.png", 1080, 1920)
render_html_to_png(html_post1, OUT_DIR / "CPT_OTONO_D1_POST01.png", 1080, 1350)
render_html_to_png(html_post2, OUT_DIR / "CPT_OTONO_D1_POST02.png", 1080, 1350)
render_html_to_png(html_story3, OUT_DIR / "CPT_OTONO_D1_STORY03.png", 1080, 1920)

print("\n🚀 Todos los artes del Día 1 han sido generados exitosamente en:", OUT_DIR)
