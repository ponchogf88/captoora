#!/usr/bin/env python3
"""
Renderizador Oficial de las 5 Plantillas Multimarca de Captoora Studio:
Campaña Navideña 2026 (Preventa Flash $500 / $1,500)

Marcas:
1. Captoora Signature  (Dark Luxury / Gala / Alta Costura)
2. Captoora Studio     (Familiar / Calidez Escandinava / Hogar)
3. Captoora Corp       (Corporativo / Posadas VIP / Brindis de Cierre)
4. Captoora Biometrics (Atletas / Recomposición / HUD de Precisión)
5. Captoora Pop!       (Infantil / Magia Navideña / Juguetes Clásicos)

Cumplimiento estricto:
- Ley Visual Captoora: Cero láminas de solo texto, 100% Full-Frame (cero crop de cabezas, manos o calzado).
- Micro-iconografía y barras flotantes con glassmorphism sin tapar al sujeto.
- Renderizado de alta resolución en formato Feed 4:5 (1080 x 1350 px) con Google Chrome Headless.
"""

import os
import subprocess
import base64
import shutil
from pathlib import Path

BASE_DIR = Path("/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO")
OUT_DIR = BASE_DIR / "campaigns/campana-navidad-2026/artes_plantillas"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def to_base64_data_uri(path):
    with open(path, "rb") as f:
        data = f.read()
    ext = path.suffix.lower().replace(".", "")
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"

# Logos base
LOGO_MASTER_URI = to_base64_data_uri(BASE_DIR / "assets/captoora_monograma_destello_master.png")
LOGO_CIRCLE_URI = to_base64_data_uri(BASE_DIR / "assets/captoora_logo_circle_centered.png")
LOGO_SIG_URI = to_base64_data_uri(BASE_DIR / "assets/captoora_signature_logo.png")

# Fotos oficiales
PHOTO_01_URI = to_base64_data_uri(BASE_DIR / "assets/navidad_2026/01_navidad_signature_luxury.jpg")
PHOTO_02_URI = to_base64_data_uri(BASE_DIR / "assets/navidad_2026/02_navidad_studio_familiar.jpg")
PHOTO_03_URI = to_base64_data_uri(BASE_DIR / "assets/navidad_2026/03_navidad_corp_ejecutivo.jpg")
PHOTO_04_URI = to_base64_data_uri(BASE_DIR / "assets/navidad_2026/04_navidad_biometrics_atletico.jpg")
PHOTO_05_URI = to_base64_data_uri(BASE_DIR / "assets/navidad_2026/05_navidad_pop_infantil.jpg")

COMMON_FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=Syncopate:wght@700;800&family=Cinzel:wght@600;700;800&family=JetBrains+Mono:wght@500;700&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background-color: #000000;
    color: #FFFFFF;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
}
.canvas {
    width: 1080px;
    height: 1350px;
    position: relative;
    overflow: hidden;
    background: #050608;
}
.fullframe-img-box {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
}
.fullframe-img {
    height: 100%;
    width: auto;
    max-width: 100%;
    object-fit: contain;
}
.backdrop-blur {
    position: absolute;
    top: -20px; left: -20px; width: 1120px; height: 1390px;
    background-size: cover;
    background-position: center;
    filter: blur(45px) brightness(0.42);
    opacity: 0.9;
    z-index: 5;
}
.vignette {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(to bottom, rgba(0,0,0,0.55) 0%, transparent 15%, transparent 82%, rgba(0,0,0,0.7) 100%);
    pointer-events: none;
    z-index: 15;
}
</style>
"""

# ==============================================================================
# PLANTILLA 1: CAPTOORA SIGNATURE (Quiet Luxury / Haute Couture / Oro & Esmeralda)
# ==============================================================================
tmpl_signature = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_FONTS}
<style>
.sig-border {{
    position: absolute;
    top: 24px; left: 24px; right: 24px; bottom: 24px;
    border: 1px solid rgba(212, 175, 55, 0.35);
    pointer-events: none;
    z-index: 25;
}}
.sig-corner-mark {{
    position: absolute;
    width: 16px; height: 16px;
    border-color: #D4AF37;
    z-index: 26;
}}
.scm-tl {{ top: 20px; left: 20px; border-top: 2px solid #D4AF37; border-left: 2px solid #D4AF37; }}
.scm-tr {{ top: 20px; right: 20px; border-top: 2px solid #D4AF37; border-right: 2px solid #D4AF37; }}
.scm-bl {{ bottom: 20px; left: 20px; border-bottom: 2px solid #D4AF37; border-left: 2px solid #D4AF37; }}
.scm-br {{ bottom: 20px; right: 20px; border-bottom: 2px solid #D4AF37; border-right: 2px solid #D4AF37; }}

.sig-header {{
    position: absolute;
    top: 48px; left: 60px; right: 60px;
    display: flex; justify-content: space-between; align-items: center;
    z-index: 30;
}}
.sig-pill-gold {{
    background: rgba(10, 15, 12, 0.82);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(212, 175, 55, 0.45);
    padding: 8px 22px;
    border-radius: 30px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #F3E5AB;
    text-transform: uppercase;
    display: flex; align-items: center; gap: 8px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.6);
}}
.sig-star {{
    color: #D4AF37;
    font-size: 14px;
}}
.sig-footer-bar {{
    position: absolute;
    bottom: 52px; left: 50%;
    transform: translateX(-50%);
    background: rgba(6, 9, 8, 0.88);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(212, 175, 55, 0.35);
    box-shadow: 0 20px 50px rgba(0,0,0,0.9), 0 0 20px rgba(212, 175, 55, 0.15);
    padding: 12px 30px;
    border-radius: 60px;
    display: flex; align-items: center; gap: 20px;
    z-index: 30;
    white-space: nowrap;
}}
.sig-logo-img {{
    width: 44px; height: 44px;
    object-fit: contain;
    filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.5));
}}
.sig-title-box {{
    display: flex; flex-direction: column; gap: 2px;
}}
.sig-brand-name {{
    font-family: 'Cinzel', serif;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #FFFFFF;
    line-height: 1.1;
}}
.sig-brand-name span {{ color: #D4AF37; }}
.sig-sub-loc {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 9.5px;
    font-weight: 600;
    letter-spacing: 2px;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
}}
.sig-divider {{
    width: 1px; height: 30px;
    background: rgba(212, 175, 55, 0.3);
}}
.sig-cta-text {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #F3E5AB;
    text-transform: uppercase;
}}
.sig-cta-badge {{
    background: linear-gradient(135deg, #D4AF37 0%, #AA771C 100%);
    color: #0A0D0B;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 1.5px;
    padding: 6px 14px;
    border-radius: 20px;
    text-transform: uppercase;
}}
</style>
</head>
<body>
<div class="canvas">
    <div class="backdrop-blur" style="background-image: url('{PHOTO_01_URI}');"></div>
    <div class="fullframe-img-box">
        <img class="fullframe-img" src="{PHOTO_01_URI}">
    </div>
    <div class="vignette"></div>

    <div class="sig-border"></div>
    <div class="sig-corner-mark scm-tl"></div>
    <div class="sig-corner-mark scm-tr"></div>
    <div class="sig-corner-mark scm-bl"></div>
    <div class="sig-corner-mark scm-br"></div>

    <div class="sig-header">
        <div class="sig-pill-gold"><span class="sig-star">✦</span> CAPTOORA SIGNATURE</div>
        <div class="sig-pill-gold">COLECCIÓN GALA · PREVENTA FLASH</div>
    </div>

    <div class="sig-footer-bar">
        <img class="sig-logo-img" src="{LOGO_SIG_URI}">
        <div class="sig-title-box">
            <div class="sig-brand-name">CAPTOORA <span>SIGNATURE</span></div>
            <div class="sig-sub-loc">SAN JERÓNIMO · MONTERREY</div>
        </div>
        <div class="sig-divider"></div>
        <div class="sig-cta-text">RESERVA PRIVADA · 81 4005 0088</div>
        <div class="sig-cta-badge">APARTA CON $500</div>
    </div>
</div>
</body>
</html>"""

# ==============================================================================
# PLANTILLA 2: CAPTOORA STUDIO (Familiar / Nórdico / Calidez de Hogar / Verde Lima)
# ==============================================================================
tmpl_studio = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_FONTS}
<style>
.stu-header {{
    position: absolute;
    top: 45px; left: 55px; right: 55px;
    display: flex; justify-content: space-between; align-items: center;
    z-index: 30;
}}
.stu-badge {{
    background: rgba(12, 14, 16, 0.85);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.16);
    padding: 9px 20px;
    border-radius: 30px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #FFFFFF;
    display: flex; align-items: center; gap: 9px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.6);
}}
.stu-dot {{
    width: 8px; height: 8px;
    background: #CCFF00;
    border-radius: 50%;
    box-shadow: 0 0 10px #CCFF00, 0 0 18px rgba(204, 255, 0, 0.6);
}}
.stu-pill-nordic {{
    background: rgba(204, 255, 0, 0.14);
    border: 1px solid rgba(204, 255, 0, 0.45);
    color: #CCFF00;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    padding: 8px 18px;
    border-radius: 30px;
    text-transform: uppercase;
}}
.stu-footer-bar {{
    position: absolute;
    bottom: 48px; left: 50%;
    transform: translateX(-50%);
    background: rgba(9, 11, 13, 0.88);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 20px 45px rgba(0,0,0,0.85), 0 0 1px rgba(204, 255, 0, 0.4);
    padding: 12px 28px;
    border-radius: 50px;
    display: flex; align-items: center; gap: 18px;
    z-index: 30;
    white-space: nowrap;
}}
.stu-logo {{
    width: 46px; height: 46px;
    object-fit: contain;
    filter: drop-shadow(0 2px 10px rgba(204, 255, 0, 0.45));
}}
.stu-brand-text {{
    display: flex; flex-direction: column; gap: 2px;
}}
.stu-title {{
    font-family: 'Syncopate', sans-serif;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #FFFFFF;
    line-height: 1.1;
}}
.stu-title .lit-a {{
    color: #CCFF00;
    text-shadow: 0 0 14px rgba(204, 255, 0, 0.85);
}}
.stu-location {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
}}
.stu-divider {{
    width: 1px; height: 28px;
    background: rgba(255, 255, 255, 0.2);
}}
.stu-cta-box {{
    display: flex; align-items: center; gap: 12px;
}}
.stu-phone {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #FFFFFF;
}}
.stu-btn-lime {{
    background: #CCFF00;
    color: #000000;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    padding: 7px 16px;
    border-radius: 20px;
    text-transform: uppercase;
    box-shadow: 0 0 16px rgba(204, 255, 0, 0.4);
}}
</style>
</head>
<body>
<div class="canvas">
    <div class="backdrop-blur" style="background-image: url('{PHOTO_02_URI}');"></div>
    <div class="fullframe-img-box">
        <img class="fullframe-img" src="{PHOTO_02_URI}">
    </div>
    <div class="vignette"></div>

    <div class="stu-header">
        <div class="stu-badge"><span class="stu-dot"></span> SET NAVIDEÑO FAMILIAR</div>
        <div class="stu-pill-nordic">PREVENTA FLASH $1,500</div>
    </div>

    <div class="stu-footer-bar">
        <img class="stu-logo" src="{LOGO_CIRCLE_URI}">
        <div class="stu-brand-text">
            <div class="stu-title">CAPTOOR<span class="lit-a">A</span> STUDIO</div>
            <div class="stu-location">COLINAS DE SAN JERÓNIMO · MTY</div>
        </div>
        <div class="stu-divider"></div>
        <div class="stu-cta-box">
            <span class="stu-phone">WA: 81 4005 0088</span>
            <div class="stu-btn-lime">APARTA CON $500</div>
        </div>
    </div>
</div>
</body>
</html>"""

# ==============================================================================
# PLANTILLA 3: CAPTOORA CORP (Business Edition / Posadas VIP / Azul Acero & Oro)
# ==============================================================================
tmpl_corp = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_FONTS}
<style>
.corp-top-bar {{
    position: absolute;
    top: 40px; left: 50px; right: 50px;
    display: flex; justify-content: space-between; align-items: center;
    z-index: 30;
}}
.corp-badge-main {{
    background: rgba(15, 23, 42, 0.88);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(148, 163, 184, 0.35);
    padding: 9px 22px;
    border-radius: 6px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11.5px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #F8FAFC;
    text-transform: uppercase;
    display: flex; align-items: center; gap: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.7);
}}
.corp-accent-bar {{
    width: 4px; height: 16px;
    background: #38BDF8;
    border-radius: 2px;
    box-shadow: 0 0 10px #38BDF8;
}}
.corp-tag-right {{
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(56, 189, 248, 0.4);
    color: #38BDF8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 8px 18px;
    border-radius: 6px;
    text-transform: uppercase;
}}
.corp-footer-bar {{
    position: absolute;
    bottom: 45px; left: 50%;
    transform: translateX(-50%);
    background: rgba(15, 23, 42, 0.92);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(148, 163, 184, 0.3);
    box-shadow: 0 25px 50px rgba(0,0,0,0.9), 0 0 1px rgba(56, 189, 248, 0.35);
    padding: 13px 32px;
    border-radius: 12px;
    display: flex; align-items: center; gap: 20px;
    z-index: 30;
    white-space: nowrap;
}}
.corp-logo-box {{
    display: flex; align-items: center; gap: 10px;
}}
.corp-logo-symbol {{
    font-family: 'Syncopate', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #38BDF8;
    border: 1.5px solid #38BDF8;
    width: 38px; height: 38px;
    display: flex; justify-content: center; align-items: center;
    border-radius: 6px;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
}}
.corp-title-text {{
    display: flex; flex-direction: column; gap: 2px;
}}
.corp-brand {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #FFFFFF;
    line-height: 1.1;
}}
.corp-brand span {{ color: #38BDF8; }}
.corp-specs {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #94A3B8;
    text-transform: uppercase;
}}
.corp-sep {{
    width: 1px; height: 32px;
    background: rgba(148, 163, 184, 0.3);
}}
.corp-cta-info {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.8px;
    color: #F8FAFC;
    text-transform: uppercase;
}}
.corp-btn {{
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
    color: #FFFFFF;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    padding: 8px 18px;
    border-radius: 6px;
    text-transform: uppercase;
    box-shadow: 0 4px 15px rgba(2, 132, 199, 0.45);
}}
</style>
</head>
<body>
<div class="canvas">
    <div class="backdrop-blur" style="background-image: url('{PHOTO_03_URI}');"></div>
    <div class="fullframe-img-box">
        <img class="fullframe-img" src="{PHOTO_03_URI}">
    </div>
    <div class="vignette"></div>

    <div class="corp-top-bar">
        <div class="corp-badge-main"><span class="corp-accent-bar"></span> CAPTOORA CORP // BUSINESS EDITION</div>
        <div class="corp-tag-right">POSADAS &amp; CIERRE DE CICLO 2026</div>
    </div>

    <div class="corp-footer-bar">
        <div class="corp-logo-box">
            <div class="corp-logo-symbol">C</div>
            <div class="corp-title-text">
                <div class="corp-brand">CAPTOORA <span>CORP</span></div>
                <div class="corp-specs">IN-COMPANY &amp; SAN JERÓNIMO ESTUDIO</div>
            </div>
        </div>
        <div class="corp-sep"></div>
        <div class="corp-cta-info">FACTURA DEDUCIBLE · 81 4005 0088</div>
        <div class="corp-btn">COTIZA TU EQUIPO</div>
    </div>
</div>
</body>
</html>"""

# ==============================================================================
# PLANTILLA 4: CAPTOORA BIOMETRICS (Fitness / HUD / Cyan & Lime / Telemetría)
# ==============================================================================
tmpl_biometrics = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_FONTS}
<style>
/* HUD CORNER BRACKETS */
.hud-corner {{
    position: absolute;
    width: 36px; height: 36px;
    border-color: #00F0FF;
    z-index: 25;
    pointer-events: none;
}}
.hc-tl {{ top: 28px; left: 28px; border-top: 2.5px solid #00F0FF; border-left: 2.5px solid #00F0FF; }}
.hc-tr {{ top: 28px; right: 28px; border-top: 2.5px solid #00F0FF; border-right: 2.5px solid #00F0FF; }}
.hc-bl {{ bottom: 28px; left: 28px; border-bottom: 2.5px solid #00F0FF; border-left: 2.5px solid #00F0FF; }}
.hc-br {{ bottom: 28px; right: 28px; border-bottom: 2.5px solid #00F0FF; border-right: 2.5px solid #00F0FF; }}

.hud-header {{
    position: absolute;
    top: 42px; left: 55px; right: 55px;
    display: flex; justify-content: space-between; align-items: center;
    z-index: 30;
}}
.hud-badge-telemetry {{
    background: rgba(4, 9, 14, 0.88);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0, 240, 255, 0.45);
    padding: 8px 18px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: #00F0FF;
    text-transform: uppercase;
    display: flex; align-items: center; gap: 8px;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.25);
}}
.hud-dot-rec {{
    width: 8px; height: 8px;
    background: #FF0055;
    border-radius: 50%;
    box-shadow: 0 0 10px #FF0055;
}}
.hud-badge-right {{
    background: rgba(4, 9, 14, 0.88);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(204, 255, 0, 0.45);
    padding: 8px 18px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #CCFF00;
    text-transform: uppercase;
}}
.hud-footer-bar {{
    position: absolute;
    bottom: 46px; left: 50%;
    transform: translateX(-50%);
    background: rgba(3, 7, 12, 0.92);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(0, 240, 255, 0.35);
    box-shadow: 0 20px 45px rgba(0,0,0,0.9), 0 0 25px rgba(0, 240, 255, 0.2);
    padding: 12px 28px;
    border-radius: 8px;
    display: flex; align-items: center; gap: 18px;
    z-index: 30;
    white-space: nowrap;
}}
.hud-logo {{
    width: 44px; height: 44px;
    object-fit: contain;
    filter: drop-shadow(0 0 12px rgba(0, 240, 255, 0.6));
}}
.hud-brand-block {{
    display: flex; flex-direction: column; gap: 2px;
}}
.hud-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 3.5px;
    color: #FFFFFF;
    line-height: 1.1;
}}
.hud-title span {{ color: #00F0FF; }}
.hud-meta {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 600;
    letter-spacing: 1.8px;
    color: #94A3B8;
    text-transform: uppercase;
}}
.hud-divider {{
    width: 1px; height: 28px;
    background: rgba(0, 240, 255, 0.3);
}}
.hud-cta {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 1.8px;
    color: #FFFFFF;
}}
.hud-btn {{
    background: #00F0FF;
    color: #000000;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    padding: 7px 16px;
    border-radius: 4px;
    text-transform: uppercase;
    box-shadow: 0 0 16px rgba(0, 240, 255, 0.5);
}}
</style>
</head>
<body>
<div class="canvas">
    <div class="backdrop-blur" style="background-image: url('{PHOTO_04_URI}');"></div>
    <div class="fullframe-img-box">
        <img class="fullframe-img" src="{PHOTO_04_URI}">
    </div>
    <div class="vignette"></div>

    <div class="hud-corner hc-tl"></div>
    <div class="hud-corner hc-tr"></div>
    <div class="hud-corner hc-bl"></div>
    <div class="hud-corner hc-br"></div>

    <div class="hud-header">
        <div class="hud-badge-telemetry"><span class="hud-dot-rec"></span> AF-C [BIOMETRIC LOCK]</div>
        <div class="hud-badge-right">100% FULL-FRAME · RECOMP 2026</div>
    </div>

    <div class="hud-footer-bar">
        <img class="hud-logo" src="{LOGO_MASTER_URI}">
        <div class="hud-brand-block">
            <div class="hud-title">CAPTOORA <span>BIOMETRICS</span></div>
            <div class="hud-meta">DIVISIÓN ATLÉTICA · SAN JERÓNIMO</div>
        </div>
        <div class="hud-divider"></div>
        <div class="hud-cta">REGISTRO FIT · WA: 81 4005 0088</div>
        <div class="hud-btn">APARTA CON $500</div>
    </div>
</div>
</body>
</html>"""

# ==============================================================================
# PLANTILLA 5: CAPTOORA POP! (Infantil / Magia Navideña / Cereza & Oro / Lúdico)
# ==============================================================================
tmpl_pop = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_FONTS}
<style>
.pop-header {{
    position: absolute;
    top: 45px; left: 55px; right: 55px;
    display: flex; justify-content: space-between; align-items: center;
    z-index: 30;
}}
.pop-stamp {{
    background: rgba(18, 10, 12, 0.86);
    backdrop-filter: blur(20px);
    border: 1.5px dashed rgba(225, 29, 72, 0.65);
    padding: 8px 22px;
    border-radius: 20px;
    font-family: 'Outfit', sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #FFE4E6;
    text-transform: uppercase;
    display: flex; align-items: center; gap: 8px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.6);
}}
.pop-sparkle {{
    color: #E11D48;
    font-size: 16px;
}}
.pop-pill-flash {{
    background: linear-gradient(135deg, #E11D48 0%, #BE123C 100%);
    color: #FFFFFF;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    padding: 8px 18px;
    border-radius: 25px;
    text-transform: uppercase;
    box-shadow: 0 4px 18px rgba(225, 29, 72, 0.5);
}}
.pop-footer-bar {{
    position: absolute;
    bottom: 48px; left: 50%;
    transform: translateX(-50%);
    background: rgba(15, 10, 12, 0.90);
    backdrop-filter: blur(24px);
    border: 1.5px solid rgba(225, 29, 72, 0.4);
    box-shadow: 0 20px 45px rgba(0,0,0,0.85), 0 0 20px rgba(225, 29, 72, 0.25);
    padding: 12px 28px;
    border-radius: 50px;
    display: flex; align-items: center; gap: 18px;
    z-index: 30;
    white-space: nowrap;
}}
.pop-logo {{
    width: 48px; height: 48px;
    object-fit: contain;
    filter: drop-shadow(0 2px 12px rgba(225, 29, 72, 0.5));
}}
.pop-brand-box {{
    display: flex; flex-direction: column; gap: 2px;
}}
.pop-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 18px;
    font-weight: 900;
    letter-spacing: 2px;
    color: #FFFFFF;
    line-height: 1.1;
}}
.pop-title span {{ color: #E11D48; }}
.pop-sub {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.8px;
    color: #FDA4AF;
    text-transform: uppercase;
}}
.pop-div {{
    width: 1px; height: 30px;
    background: rgba(225, 29, 72, 0.35);
}}
.pop-phone {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #FFFFFF;
}}
.pop-btn {{
    background: #CCFF00;
    color: #000000;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    padding: 8px 18px;
    border-radius: 25px;
    text-transform: uppercase;
    box-shadow: 0 0 16px rgba(204, 255, 0, 0.45);
}}
</style>
</head>
<body>
<div class="canvas">
    <div class="backdrop-blur" style="background-image: url('{PHOTO_05_URI}');"></div>
    <div class="fullframe-img-box">
        <img class="fullframe-img" src="{PHOTO_05_URI}">
    </div>
    <div class="vignette"></div>

    <div class="pop-header">
        <div class="pop-stamp"><span class="pop-sparkle">★</span> CAPTOORA POP! · EDICIÓN MÁGICA</div>
        <div class="pop-pill-flash">PREVENTA $1,500</div>
    </div>

    <div class="pop-footer-bar">
        <img class="pop-logo" src="{LOGO_CIRCLE_URI}">
        <div class="pop-brand-box">
            <div class="pop-title">CAPTOORA <span>POP!</span></div>
            <div class="pop-sub">SAN JERÓNIMO · FOTOS SIN ESTRÉS</div>
        </div>
        <div class="pop-div"></div>
        <span class="pop-phone">WA: 81 4005 0088</span>
        <div class="pop-btn">¡APARTA CON $500!</div>
    </div>
</div>
</body>
</html>"""

TEMPLATES = [
    ("PLANTILLA_01_CAPTOORA_SIGNATURE_4x5.png", tmpl_signature),
    ("PLANTILLA_02_CAPTOORA_STUDIO_4x5.png", tmpl_studio),
    ("PLANTILLA_03_CAPTOORA_CORP_4x5.png", tmpl_corp),
    ("PLANTILLA_04_CAPTOORA_BIOMETRICS_4x5.png", tmpl_biometrics),
    ("PLANTILLA_05_CAPTOORA_POP_4x5.png", tmpl_pop),
]

def render_html_to_png(html_content, output_png, width=1080, height=1350):
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
    print(f"✅ Plantilla renderizada: {output_png.name} ({width}x{height})")

def main():
    print("🚀 Iniciando renderizado de las 5 Plantillas Multimarca de Captoora...")
    for filename, html_content in TEMPLATES:
        dest_path = OUT_DIR / filename
        render_html_to_png(html_content, dest_path)
    
    print("\n🎉 Todas las 5 plantillas fueron generadas con éxito en:")
    print(f"📂 {OUT_DIR}")

if __name__ == "__main__":
    main()
