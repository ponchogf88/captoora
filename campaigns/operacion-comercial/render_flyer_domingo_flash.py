#!/usr/bin/env python3
"""
Renderizador del Flyer Visual Express:
'FLASH SUNDAY: SESIONES DE OTOÑO & HALLOWEEN' (1080x1920 para WhatsApp Status & IG Story)
Ubicación de salida: /Users/imac/Desktop/FLYER_DOMINGO_FLASH_1NOV.png
"""

import os
import subprocess
import base64
import shutil
from pathlib import Path

BASE_DIR = Path("/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO")
OUT_PNG = Path("/Users/imac/Desktop/FLYER_DOMINGO_FLASH_1NOV.png")
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def to_base64_data_uri(path):
    with open(path, "rb") as f:
        data = f.read()
    ext = path.suffix.lower().replace(".", "")
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"

LOGO_URI = to_base64_data_uri(BASE_DIR / "assets/captoora_logo_circle_centered.png")
PHOTO_URI = to_base64_data_uri(BASE_DIR / "assets/referencias_generadas/ref_studio_halloween_9x16.jpg")

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Space+Grotesk:wght@600;700&family=Syncopate:wght@700;800&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    background-color: #000000;
    color: #FFFFFF;
    font-family: 'Plus Jakarta Sans', sans-serif;
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
}}
.container {{
    width: 1080px; height: 1920px;
    position: relative;
    background: #000000;
}}
.bg-photo {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('{PHOTO_URI}');
    background-size: cover;
    background-position: center;
}}
.vignette {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(180deg, 
        rgba(0,0,0,0.85) 0%, 
        rgba(0,0,0,0.2) 28%, 
        rgba(0,0,0,0.15) 55%, 
        rgba(0,0,0,0.92) 80%,
        rgba(0,0,0,0.98) 100%);
    pointer-events: none;
}}
.lit-a {{
    color: #CCFF00 !important;
    text-shadow: 0 0 16px rgba(204, 255, 0, 0.95), 0 0 32px rgba(204, 255, 0, 0.5);
}}

/* ESQUINAS MARCO */
.cb {{ position: absolute; width: 50px; height: 50px; pointer-events: none; z-index: 50; }}
.cb-tl {{ top: 60px; left: 60px; border-top: 3px solid #CCFF00; border-left: 3px solid #CCFF00; }}
.cb-tr {{ top: 60px; right: 60px; border-top: 3px solid #CCFF00; border-right: 3px solid #CCFF00; }}
.cb-bl {{ bottom: 60px; left: 60px; border-bottom: 3px solid #CCFF00; border-left: 3px solid #CCFF00; }}
.cb-br {{ bottom: 60px; right: 60px; border-bottom: 3px solid #CCFF00; border-right: 3px solid #CCFF00; }}

/* HEADER */
.header-box {{
    position: absolute;
    top: 80px;
    left: 80px;
    right: 80px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 60;
}}
.badge-pill {{
    background: rgba(10, 12, 14, 0.85);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    padding: 10px 22px;
    border-radius: 40px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.dot-lime {{
    width: 9px; height: 9px;
    background: #CCFF00;
    border-radius: 50%;
    box-shadow: 0 0 12px #CCFF00;
}}

/* TITULAR SUPERIOR */
.top-title-area {{
    position: absolute;
    top: 170px;
    left: 80px;
    right: 80px;
    z-index: 60;
    text-align: center;
}}
.flash-tag {{
    display: inline-block;
    background: #CCFF00;
    color: #000000;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 6px;
    margin-bottom: 12px;
}}
.main-heading {{
    font-family: 'Syncopate', sans-serif;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: 4px;
    line-height: 1.15;
    text-shadow: 0 4px 20px rgba(0,0,0,0.9);
}}

/* CAJA DE BENEFICIOS Y PRECIO INFERIOR */
.bottom-card {{
    position: absolute;
    bottom: 80px;
    left: 70px;
    right: 70px;
    z-index: 60;
    background: rgba(10, 12, 15, 0.88);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 36px;
    padding: 34px 40px 30px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.9), 0 0 1px rgba(204, 255, 0, 0.4);
}}
.slots-alert {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
    padding-bottom: 18px;
    margin-bottom: 20px;
}}
.slots-count {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #CCFF00;
    letter-spacing: 1.5px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.date-tag {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    letter-spacing: 1px;
}}

.features-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px 16px;
    margin-bottom: 24px;
}}
.feat-item {{
    font-size: 15px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    display: flex;
    align-items: center;
    gap: 10px;
}}
.feat-icon {{
    color: #CCFF00;
    font-size: 16px;
}}

.pricing-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 16px 24px;
    margin-bottom: 20px;
}}
.price-label {{
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
}}
.price-value {{
    font-family: 'Syncopate', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #CCFF00;
    text-shadow: 0 0 15px rgba(204, 255, 0, 0.5);
}}
.price-note {{
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
    margin-top: 2px;
}}

.cta-button {{
    display: block;
    width: 100%;
    background: #CCFF00;
    color: #000000;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    text-align: center;
    padding: 18px 24px;
    border-radius: 50px;
    box-shadow: 0 10px 30px rgba(204, 255, 0, 0.45);
    margin-bottom: 14px;
}}
.footer-geo {{
    text-align: center;
    font-size: 13px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.65);
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}
</style>
</head>
<body>
<div class="container">
    <div class="bg-photo"></div>
    <div class="vignette"></div>
    
    <div class="cb cb-tl"></div>
    <div class="cb cb-tr"></div>
    <div class="cb cb-bl"></div>
    <div class="cb cb-br"></div>
    
    <div class="header-box">
        <div class="badge-pill"><span class="dot-lime"></span>CAPTOOR<span class="lit-a">A</span> STUDIO</div>
        <div class="badge-pill">SAN JERÓNIMO · MTY</div>
    </div>
    
    <div class="top-title-area">
        <div class="flash-tag">⚡️ SOLO ESTE DOMINGO</div>
        <h1 class="main-heading">MINI-SESIONES<br>OTOÑO & HALLOWEEN</h1>
    </div>
    
    <div class="bottom-card">
        <div class="slots-alert">
            <div class="slots-count">⚠️ SÓLO 6 HORARIOS DISPONIBLES</div>
            <div class="date-tag">DOMINGO 1 DE NOVIEMBRE</div>
        </div>
        
        <div class="features-grid">
            <div class="feat-item"><span class="feat-icon">✦</span> 30 min sesión guiada</div>
            <div class="feat-item"><span class="feat-icon">✦</span> Set climatizado de revista</div>
            <div class="feat-item"><span class="feat-icon">✦</span> Parque arbolado con luz dorada</div>
            <div class="feat-item"><span class="feat-icon">✦</span> 8 fotos editadas en alta res</div>
        </div>
        
        <div class="pricing-row">
            <div>
                <div class="price-label">Tarifa Flash Exclusiva</div>
                <div class="price-note">Aparta tu horario con $500 de anticipo</div>
            </div>
            <div class="price-value">$950 <span style="font-size: 16px; font-weight: 700; color: #FFF;">MXN</span></div>
        </div>
        
        <div class="cta-button">📲 WHATSAPP: 81 4005 0088</div>
        <div class="footer-geo">Av. Paseo de los Álamos 165 · Colinas de San Jerónimo</div>
    </div>
</div>
</body>
</html>
"""

def main():
    temp_html = BASE_DIR / "campaigns/operacion-comercial/_temp_flyer_domingo.html"
    temp_html.write_text(html_content, encoding="utf-8")
    
    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--window-size=1080,1920",
        f"--screenshot={OUT_PNG}",
        "--virtual-time-budget=2000",
        f"file://{temp_html}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if temp_html.exists():
        temp_html.unlink()
    print(f"✅ Flyer de Domingo generado exitosamente en el Escritorio: {OUT_PNG}")

if __name__ == "__main__":
    main()
