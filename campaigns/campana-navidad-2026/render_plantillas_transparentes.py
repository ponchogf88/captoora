#!/usr/bin/env python3
"""
Renderizador de Plantillas Oficiales Transparentes (Overlays Sueltos):
CAPTOORA STUDIO · Versión Oficial 2026

Características clave según retroalimentación:
1. Plantillas SUELTAS con fondo 100% transparente (sin foto incrustada).
2. Logotipo de Captoora Oficial (monograma de lente con destello estelar) GRANDE, protagónico y legible.
3. Regla de contraste dual:
   - EDICIÓN FONDO OSCURO: Logotipo y tipografías en blanco puro (#FFFFFF) con sutil halo/sombra para fondos oscuros o nocturnos.
   - EDICIÓN FONDO CLARO: Logotipo y tipografías en negro azabache (#0A0A0A) para ciclorama blanco o luz de día.
4. Tipografía y marcas reales:
   - Captoora Biometrics utiliza telemetría REAL de cámara Nikon Z9 (AF-C 3D, 1/250s, f/1.2, ISO 64, RAW FX), nada de fuentes "IA chafa".
   - Captoora Signature utiliza diseño editorial de lujo (Haute Couture / Vogue style) minimalista con filete fino.
   - Captoora Studio, Corp y Pop utilizan el logotipo maestro oficial unificado con su submarca clara y visible.
"""

import os
import subprocess
import base64
from pathlib import Path

BASE_DIR = Path("/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO")
OUT_DIR = BASE_DIR / "assets/plantillas_oficiales_captoora"
OUT_DIR.mkdir(parents=True, exist_ok=True)
DESKTOP_DIR = Path("/Users/imac/Desktop/PLANTILLAS_OFICIALES_TRANSPARENTES")
DESKTOP_DIR.mkdir(parents=True, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def to_base64_data_uri(path):
    with open(path, "rb") as f:
        data = f.read()
    ext = path.suffix.lower().replace(".", "")
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"

LOGO_MASTER_URI = to_base64_data_uri(BASE_DIR / "assets/captoora_monograma_destello_master.png")

COMMON_FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700;800&display=swap" rel="stylesheet">
"""

def generate_html(brand, mode):
    is_dark = (mode == "oscuro")
    # Paleta según fondo
    # En fondo oscuro, el overlay debe ser BLANCO
    # En fondo claro, el overlay debe ser NEGRO
    primary_color = "#FFFFFF" if is_dark else "#0A0A0A"
    sub_color = "rgba(255, 255, 255, 0.75)" if is_dark else "rgba(10, 10, 10, 0.75)"
    accent_lime = "#CCFF00" if is_dark else "#228B22"
    accent_gold = "#E5C07B" if is_dark else "#8C6D23"
    accent_cyan = "#00F0FF" if is_dark else "#008B8B"
    accent_cherry = "#FF2A55" if is_dark else "#990022"
    border_color = "rgba(255, 255, 255, 0.35)" if is_dark else "rgba(10, 10, 10, 0.35)"
    glass_bg = "rgba(5, 5, 5, 0.75)" if is_dark else "rgba(255, 255, 255, 0.82)"
    text_shadow = "0 2px 10px rgba(0,0,0,0.85)" if is_dark else "0 1px 4px rgba(255,255,255,0.85)"
    logo_filter = "drop-shadow(0 2px 12px rgba(0,0,0,0.85))" if is_dark else "brightness(0) drop-shadow(0 1px 4px rgba(255,255,255,0.8))"

    # ==========================================
    # 1. SIGNATURE (Luxury Editorial / Vogue)
    # ==========================================
    if brand == "signature":
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_FONTS}
<style>
html, body {{
    background: transparent !important;
    margin: 0; padding: 0;
    width: 1080px; height: 1350px;
    overflow: hidden;
    font-family: 'Inter', -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.frame-box {{
    width: 1080px; height: 1350px;
    position: relative;
    box-sizing: border-box;
}}
.inner-border {{
    position: absolute;
    top: 36px; left: 36px; right: 36px; bottom: 36px;
    border: 1px solid {border_color};
    pointer-events: none;
}}
.top-header {{
    position: absolute;
    top: 55px; left: 60px; right: 60px;
    display: flex; justify-content: space-between; align-items: center;
    color: {primary_color};
    text-shadow: {text_shadow};
}}
.brand-category {{
    font-family: 'Cinzel', serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: {accent_gold};
}}
.edition-tag {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: {sub_color};
}}
.bottom-signature-bar {{
    position: absolute;
    bottom: 55px; left: 60px; right: 60px;
    display: flex; justify-content: space-between; align-items: flex-end;
    color: {primary_color};
}}
.logo-lockup {{
    display: flex; align-items: center; gap: 20px;
}}
.logo-img {{
    width: 90px; height: 90px;
    object-fit: contain;
    filter: {logo_filter};
}}
.brand-text-box {{
    display: flex; flex-direction: column; gap: 4px;
}}
.brand-main {{
    font-family: 'Cinzel', serif;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 6px;
    color: {primary_color};
    text-shadow: {text_shadow};
    line-height: 1;
}}
.brand-main span {{ color: {accent_gold}; }}
.brand-loc {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    color: {sub_color};
    text-transform: uppercase;
}}
.cta-block {{
    text-align: right;
    display: flex; flex-direction: column; gap: 6px;
}}
.cta-label {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {accent_gold};
    text-transform: uppercase;
    text-shadow: {text_shadow};
}}
.cta-phone {{
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: {primary_color};
    text-shadow: {text_shadow};
}}
</style>
</head>
<body>
<div class="frame-box">
    <div class="inner-border"></div>
    <div class="top-header">
        <span class="brand-category">CAPTOORA SIGNATURE</span>
        <span class="edition-tag">COLLECTION 2026 // EDICIÓN LIMITADA</span>
    </div>
    <div class="bottom-signature-bar">
        <div class="logo-lockup">
            <img class="logo-img" src="{LOGO_MASTER_URI}">
            <div class="brand-text-box">
                <div class="brand-main">CAPTOORA <span>SIGNATURE</span></div>
                <div class="brand-loc">COLINAS DE SAN JERÓNIMO · MONTERREY</div>
            </div>
        </div>
        <div class="cta-block">
            <div class="cta-label">RESERVA PRIVADA // PREVENTA FLASH</div>
            <div class="cta-phone">WA: 81 4005 0088</div>
        </div>
    </div>
</div>
</body>
</html>"""

    # ==========================================
    # 2. STUDIO (Auténtico Estudio Fotográfico)
    # ==========================================
    elif brand == "studio":
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_FONTS}
<style>
html, body {{
    background: transparent !important;
    margin: 0; padding: 0;
    width: 1080px; height: 1350px;
    overflow: hidden;
    font-family: 'Inter', -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.frame-box {{
    width: 1080px; height: 1350px;
    position: relative;
    box-sizing: border-box;
}}
.studio-top {{
    position: absolute;
    top: 48px; left: 55px; right: 55px;
    display: flex; justify-content: space-between; align-items: center;
}}
.badge-glass {{
    background: {glass_bg};
    backdrop-filter: blur(16px);
    border: 1px solid {border_color};
    padding: 10px 22px;
    border-radius: 40px;
    display: flex; align-items: center; gap: 10px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
}}
.studio-dot {{
    width: 9px; height: 9px;
    background: {accent_lime};
    border-radius: 50%;
    box-shadow: 0 0 10px {accent_lime};
}}
.badge-text {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: {primary_color};
    text-transform: uppercase;
}}
.studio-right-tag {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {accent_lime};
    text-transform: uppercase;
    text-shadow: {text_shadow};
}}
.studio-bottom {{
    position: absolute;
    bottom: 48px; left: 55px; right: 55px;
    display: flex; justify-content: space-between; align-items: flex-end;
}}
.studio-logo-group {{
    display: flex; align-items: center; gap: 22px;
}}
.studio-logo-img {{
    width: 105px; height: 105px;
    object-fit: contain;
    filter: {logo_filter};
}}
.studio-names {{
    display: flex; flex-direction: column; gap: 4px;
}}
.studio-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: 4px;
    color: {primary_color};
    text-shadow: {text_shadow};
    line-height: 1;
}}
.studio-title span {{ color: {accent_lime}; }}
.studio-meta {{
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2.5px;
    color: {sub_color};
    text-transform: uppercase;
}}
.studio-booking {{
    background: {glass_bg};
    backdrop-filter: blur(20px);
    border: 1px solid {border_color};
    padding: 12px 26px;
    border-radius: 50px;
    text-align: right;
    box-shadow: 0 15px 35px rgba(0,0,0,0.5);
}}
.booking-label {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {accent_lime};
    text-transform: uppercase;
}}
.booking-wa {{
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 900;
    letter-spacing: 1px;
    color: {primary_color};
}}
</style>
</head>
<body>
<div class="frame-box">
    <div class="studio-top">
        <div class="badge-glass">
            <span class="studio-dot"></span>
            <span class="badge-text">CAPTOORA STUDIO</span>
        </div>
        <div class="studio-right-tag">SET NAVIDEÑO FAMILIAR // PREVENTA</div>
    </div>
    <div class="studio-bottom">
        <div class="studio-logo-group">
            <img class="studio-logo-img" src="{LOGO_MASTER_URI}">
            <div class="studio-names">
                <div class="studio-title">CAPTOOR<span>A</span> STUDIO</div>
                <div class="studio-meta">SAN JERÓNIMO · FOTOGRAFÍA PROFESIONAL</div>
            </div>
        </div>
        <div class="studio-booking">
            <div class="booking-label">APARTA CON $500</div>
            <div class="booking-wa">WA: 81 4005 0088</div>
        </div>
    </div>
</div>
</body>
</html>"""

    # ==========================================
    # 3. CORP (Corporativo / Posadas / Business)
    # ==========================================
    elif brand == "corp":
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_FONTS}
<style>
html, body {{
    background: transparent !important;
    margin: 0; padding: 0;
    width: 1080px; height: 1350px;
    overflow: hidden;
    font-family: 'Inter', -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.frame-box {{
    width: 1080px; height: 1350px;
    position: relative;
    box-sizing: border-box;
}}
.corp-header {{
    position: absolute;
    top: 45px; left: 55px; right: 55px;
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1.5px solid {border_color};
    padding-bottom: 15px;
}}
.corp-badge-tag {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
    color: {primary_color};
    text-transform: uppercase;
    text-shadow: {text_shadow};
}}
.corp-meta-specs {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    color: {sub_color};
    text-transform: uppercase;
}}
.corp-footer {{
    position: absolute;
    bottom: 45px; left: 55px; right: 55px;
    display: flex; justify-content: space-between; align-items: flex-end;
    border-top: 1.5px solid {border_color};
    padding-top: 18px;
}}
.corp-logo-wrap {{
    display: flex; align-items: center; gap: 20px;
}}
.corp-logo-img {{
    width: 95px; height: 95px;
    object-fit: contain;
    filter: {logo_filter};
}}
.corp-text {{
    display: flex; flex-direction: column; gap: 4px;
}}
.corp-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 4px;
    color: {primary_color};
    text-shadow: {text_shadow};
    line-height: 1;
}}
.corp-title span {{ color: #38BDF8; }}
.corp-service {{
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.5px;
    color: {sub_color};
    text-transform: uppercase;
}}
.corp-contact-info {{
    text-align: right;
    display: flex; flex-direction: column; gap: 4px;
}}
.corp-factura {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #38BDF8;
    text-transform: uppercase;
}}
.corp-phone {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: {primary_color};
    text-shadow: {text_shadow};
}}
</style>
</head>
<body>
<div class="frame-box">
    <div class="corp-header">
        <span class="corp-badge-tag">CAPTOORA CORP // BUSINESS EDITION</span>
        <span class="corp-meta-specs">CIERRE DE CICLO 2026 · IN-COMPANY &amp; ESTUDIO</span>
    </div>
    <div class="corp-footer">
        <div class="corp-logo-wrap">
            <img class="corp-logo-img" src="{LOGO_MASTER_URI}">
            <div class="corp-text">
                <div class="corp-title">CAPTOORA <span>CORP</span></div>
                <div class="corp-service">COBERTURA DE POSADAS &amp; RETRATO EJECUTIVO</div>
            </div>
        </div>
        <div class="corp-contact-info">
            <div class="corp-factura">FACTURACIÓN DEDUCIBLE 100%</div>
            <div class="corp-phone">WA: 81 4005 0088</div>
        </div>
    </div>
</div>
</body>
</html>"""

    # ==============================================================
    # 4. BIOMETRICS (Auténtico Visor de Cámara Nikon Z9 / Real EVF)
    # ==============================================================
    elif brand == "biometrics":
        bracket_color = accent_cyan if is_dark else "#007A87"
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_FONTS}
<style>
html, body {{
    background: transparent !important;
    margin: 0; padding: 0;
    width: 1080px; height: 1350px;
    overflow: hidden;
    font-family: 'JetBrains Mono', monospace;
    -webkit-font-smoothing: antialiased;
}}
.frame-box {{
    width: 1080px; height: 1350px;
    position: relative;
    box-sizing: border-box;
}}

/* AUTÉNTICOS CORNER BRACKETS DE VISOR DE CÁMARA (NIKON Z9) */
.cam-corner {{
    position: absolute;
    width: 32px; height: 32px;
    border-color: {bracket_color};
    z-index: 20;
    pointer-events: none;
}}
.cc-tl {{ top: 38px; left: 38px; border-top: 2px solid {bracket_color}; border-left: 2px solid {bracket_color}; }}
.cc-tr {{ top: 38px; right: 38px; border-top: 2px solid {bracket_color}; border-right: 2px solid {bracket_color}; }}
.cc-bl {{ bottom: 38px; left: 38px; border-bottom: 2px solid {bracket_color}; border-left: 2px solid {bracket_color}; }}
.cc-br {{ bottom: 38px; right: 38px; border-bottom: 2px solid {bracket_color}; border-right: 2px solid {bracket_color}; }}

/* AUTÉNTICA TELEMETRÍA DE CÁMARA NIKON Z9 EVF */
.nikon-top-osd {{
    position: absolute;
    top: 50px; left: 80px; right: 80px;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {primary_color};
    text-shadow: {text_shadow};
}}
.osd-af {{
    color: {bracket_color};
    display: flex; align-items: center; gap: 8px;
}}
.rec-dot {{
    width: 9px; height: 9px;
    background: #FF0055;
    border-radius: 50%;
    box-shadow: 0 0 10px #FF0055;
}}
.osd-specs {{
    color: {sub_color};
    font-size: 11.5px;
}}

/* RETÍCULA CENTRAL SUTIL DE ENFOQUE (CROSSHAIRS) */
.cam-crosshair {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 120px; height: 120px;
    pointer-events: none;
    opacity: 0.35;
}}
.ch-line-h {{
    position: absolute; top: 60px; left: 0; width: 120px; height: 1px;
    background: {primary_color};
}}
.ch-line-v {{
    position: absolute; top: 0; left: 60px; width: 1px; height: 120px;
    background: {primary_color};
}}
.ch-bracket-l {{
    position: absolute; top: 40px; left: 40px; width: 8px; height: 40px;
    border-left: 1.5px solid {primary_color}; border-top: 1.5px solid {primary_color}; border-bottom: 1.5px solid {primary_color};
}}
.ch-bracket-r {{
    position: absolute; top: 40px; right: 40px; width: 8px; height: 40px;
    border-right: 1.5px solid {primary_color}; border-top: 1.5px solid {primary_color}; border-bottom: 1.5px solid {primary_color};
}}

/* BARRA INFERIOR DE CÁMARA Y BRANDING CAPTOORA */
.nikon-bottom-osd {{
    position: absolute;
    bottom: 50px; left: 75px; right: 75px;
    display: flex; justify-content: space-between; align-items: flex-end;
}}
.bio-logo-group {{
    display: flex; align-items: center; gap: 18px;
}}
.bio-logo-img {{
    width: 95px; height: 95px;
    object-fit: contain;
    filter: {logo_filter};
}}
.bio-brand-info {{
    display: flex; flex-direction: column; gap: 3px;
}}
.bio-brand-name {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 3px;
    color: {primary_color};
    text-shadow: {text_shadow};
    line-height: 1;
}}
.bio-brand-name span {{ color: {bracket_color}; }}
.bio-sub {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    color: {sub_color};
    text-transform: uppercase;
}}
.cam-settings-box {{
    text-align: right;
    display: flex; flex-direction: column; gap: 5px;
}}
.cam-shutter {{
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 2px;
    color: {bracket_color};
    text-shadow: {text_shadow};
}}
.cam-wa {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: {primary_color};
    text-shadow: {text_shadow};
}}
</style>
</head>
<body>
<div class="frame-box">
    <div class="cam-corner cc-tl"></div>
    <div class="cam-corner cc-tr"></div>
    <div class="cam-corner cc-bl"></div>
    <div class="cam-corner cc-br"></div>

    <div class="nikon-top-osd">
        <div class="osd-af"><span class="rec-dot"></span> [AF-C · 3D-TRACKING]</div>
        <div class="osd-specs">NIKON Z9 // 50mm f/1.2 S // RAW FX [100% FULL-FRAME]</div>
    </div>

    <!-- SUTIL RETÍCULA DE ENFOQUE CENTRAL -->
    <div class="cam-crosshair">
        <div class="ch-line-h"></div>
        <div class="ch-line-v"></div>
        <div class="ch-bracket-l"></div>
        <div class="ch-bracket-r"></div>
    </div>

    <div class="nikon-bottom-osd">
        <div class="bio-logo-group">
            <img class="bio-logo-img" src="{LOGO_MASTER_URI}">
            <div class="bio-brand-info">
                <div class="bio-brand-name">CAPTOORA <span>BIOMETRICS</span></div>
                <div class="bio-sub">REGISTRO ANATÓMICO // SAN JERÓNIMO MTY</div>
            </div>
        </div>
        <div class="cam-settings-box">
            <div class="cam-shutter">1/250s · F1.2 · ISO 64</div>
            <div class="cam-wa">APARTA CON $500 · WA: 81 4005 0088</div>
        </div>
    </div>
</div>
</body>
</html>"""

    # ==========================================
    # 5. POP! (Magia Infantil / Festiva / Cherry)
    # ==========================================
    elif brand == "pop":
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{COMMON_FONTS}
<style>
html, body {{
    background: transparent !important;
    margin: 0; padding: 0;
    width: 1080px; height: 1350px;
    overflow: hidden;
    font-family: 'Inter', -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.frame-box {{
    width: 1080px; height: 1350px;
    position: relative;
    box-sizing: border-box;
}}
.pop-top {{
    position: absolute;
    top: 48px; left: 55px; right: 55px;
    display: flex; justify-content: space-between; align-items: center;
}}
.pop-stamp-clean {{
    background: {glass_bg};
    backdrop-filter: blur(16px);
    border: 1.5px dashed {accent_cherry};
    padding: 9px 24px;
    border-radius: 30px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2.5px;
    color: {primary_color};
    text-transform: uppercase;
    display: flex; align-items: center; gap: 8px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}}
.pop-star {{ color: {accent_cherry}; font-size: 15px; }}
.pop-preventa-tag {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    color: {accent_cherry};
    text-transform: uppercase;
    text-shadow: {text_shadow};
}}
.pop-bottom {{
    position: absolute;
    bottom: 48px; left: 55px; right: 55px;
    display: flex; justify-content: space-between; align-items: flex-end;
}}
.pop-logo-combo {{
    display: flex; align-items: center; gap: 20px;
}}
.pop-logo-img {{
    width: 100px; height: 100px;
    object-fit: contain;
    filter: {logo_filter};
}}
.pop-title-wrap {{
    display: flex; flex-direction: column; gap: 3px;
}}
.pop-brand {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 3px;
    color: {primary_color};
    text-shadow: {text_shadow};
    line-height: 1;
}}
.pop-brand span {{ color: {accent_cherry}; }}
.pop-claim {{
    font-family: 'Inter', sans-serif;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {sub_color};
    text-transform: uppercase;
}}
.pop-cta-card {{
    background: {glass_bg};
    backdrop-filter: blur(20px);
    border: 1.5px solid {accent_cherry};
    padding: 12px 26px;
    border-radius: 40px;
    text-align: right;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
}}
.pop-cta-badge {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: {accent_cherry};
    text-transform: uppercase;
}}
.pop-cta-phone {{
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 900;
    letter-spacing: 1px;
    color: {primary_color};
}}
</style>
</head>
<body>
<div class="frame-box">
    <div class="pop-top">
        <div class="pop-stamp-clean">
            <span class="pop-star">★</span> CAPTOORA POP! · EDICIÓN MÁGICA
        </div>
        <div class="pop-preventa-tag">PREVENTA FLASH $1,500</div>
    </div>
    <div class="pop-bottom">
        <div class="pop-logo-combo">
            <img class="pop-logo-img" src="{LOGO_MASTER_URI}">
            <div class="pop-title-wrap">
                <div class="pop-brand">CAPTOORA <span>POP!</span></div>
                <div class="pop-claim">MAGIA INFANTIL · SAN JERÓNIMO</div>
            </div>
        </div>
        <div class="pop-cta-card">
            <div class="pop-cta-badge">¡APARTA CON $500!</div>
            <div class="pop-cta-phone">WA: 81 4005 0088</div>
        </div>
    </div>
</div>
</body>
</html>"""

def render_transparent_png(html_content, output_png):
    temp_html = OUT_DIR / f"_temp_{output_png.stem}.html"
    temp_html.write_text(html_content, encoding="utf-8")
    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--default-background-color=00000000",
        "--window-size=1080,1350",
        f"--screenshot={output_png}",
        "--virtual-time-budget=2000",
        f"file://{temp_html}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if temp_html.exists():
        temp_html.unlink()
    
    # Copiar también al Escritorio para acceso inmediato
    desktop_copy = DESKTOP_DIR / output_png.name
    import shutil
    shutil.copyfile(output_png, desktop_copy)
    print(f"✅ Overlay Transparente generado: {output_png.name}")

def main():
    brands = ["signature", "studio", "corp", "biometrics", "pop"]
    modes = ["oscuro", "claro"]

    print("🚀 Renderizando 10 Plantillas Oficiales Transparentes (Overlays Sueltos)...")
    for b in brands:
        for m in modes:
            filename = f"OVERLAY_{b.upper()}_FONDO_{m.upper()}_4x5.png"
            dest = OUT_DIR / filename
            html = generate_html(b, m)
            render_transparent_png(html, dest)

    print("\n🎉 Todas las plantillas transparentes fueron creadas exitosamente.")
    print(f"📂 Repositorio: {OUT_DIR}")
    print(f"🖥️ Escritorio: {DESKTOP_DIR}")

if __name__ == "__main__":
    main()
