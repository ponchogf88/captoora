import os
import subprocess
import shutil

OUTPUT_DIR = "/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO/assets/plantillas_oficiales_captoora"
DESKTOP_DIR = "/Users/imac/Desktop/PLANTILLAS_OFICIALES_TRANSPARENTES"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DESKTOP_DIR, exist_ok=True)

LOGO_BLANCO = "/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO/assets/captoora_logo_lente_centrado_blanco.png"
LOGO_NEGRO = "/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO/assets/captoora_logo_lente_centrado_negro.png"

# 5 Options with Dynamic Texts (NO PRICES, LARGE PHONE NUMBERS, SLEEK THIN TYPOGRAPHY, 100% CENTERED LENS LOGO)
TEMPLATES = [
    {
        "id": "OPCION_01_SIGNATURE_EDITORIAL",
        "brand_name": "CAPTOORA SIGNATURE",
        "eyebrow": "HAUTE COUTURE // PRIVATE SESSIONS",
        "hook": "RETRATO EDITORIAL DE AUTOR",
        "sub": "ATMÓSFERA DE GALA · SAN JERÓNIMO, MONTERREY",
        "phone": "WHATSAPP  81 4005 0088",
        "font_family": "'Cinzel', serif",
        "style_variant": "signature"
    },
    {
        "id": "OPCION_02_STUDIO_FAMILIAR",
        "brand_name": "CAPTOORA STUDIO",
        "eyebrow": "CONEXIÓN REAL // MEMORIAS DE HOGAR",
        "hook": "DONDE TODOS FORMAN PARTE DEL RECUERDO",
        "sub": "SET DE ESTUDIO & EXTERIOR ARBOLADO · PET-FRIENDLY",
        "phone": "WHATSAPP  81 4005 0088",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "style_variant": "studio"
    },
    {
        "id": "OPCION_03_CORP_EJECUTIVO",
        "brand_name": "CAPTOORA CORP",
        "eyebrow": "BRANDING PERSONAL & CORPORATIVO",
        "hook": "PROYECCIÓN EJECUTIVA & REPUTACIÓN VISUAL",
        "sub": "ESTUDIO PRIVADO & COBERTURA IN-COMPANY",
        "phone": "WHATSAPP  81 4005 0088",
        "font_family": "'Space Grotesk', sans-serif",
        "style_variant": "corp"
    },
    {
        "id": "OPCION_04_BIOMETRICS_FITNESS",
        "brand_name": "CAPTOORA BIOMETRICS",
        "eyebrow": "TELEMETRÍA VISUAL // ALTO RENDIMIENTO",
        "hook": "REGISTRO ATLÉTICO · RECOMPOSICIÓN CORPORAL",
        "sub": "NIKON Z9 // 50mm f/1.2 S // RAW FX [36x24] · RIM-LIGHT",
        "phone": "WHATSAPP  81 4005 0088",
        "font_family": "'JetBrains Mono', monospace",
        "style_variant": "biometrics"
    },
    {
        "id": "OPCION_05_POP_INFANTIL",
        "brand_name": "CAPTOORA POP!",
        "eyebrow": "MAGIA FESTIVA // FOTOS SIN ESTRÉS",
        "hook": "LA MAGIA SUCEDE CUANDO JUEGAN SIN POSAR",
        "sub": "SET NAVIDEÑO & JUGUETES CLÁSICOS DE MADERA",
        "phone": "WHATSAPP  81 4005 0088",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "style_variant": "pop"
    }
]

def generate_html(template, contrast_mode):
    is_dark = (contrast_mode == "OSCURO")
    
    # Dual Contrast Palette: NO BOLD FONTS. Sleek, thin/regular weights.
    if is_dark:
        logo_path = LOGO_BLANCO
        color_primary = "#FFFFFF"
        color_secondary = "rgba(255, 255, 255, 0.75)"
        color_dim = "rgba(255, 255, 255, 0.45)"
        border_color = "rgba(255, 255, 255, 0.18)"
        pill_bg = "rgba(0, 0, 0, 0.65)"
        accent_color = "#CCFF00"
        phone_color = "#FFFFFF"
    else:
        logo_path = LOGO_NEGRO
        color_primary = "#0F172A"
        color_secondary = "rgba(15, 23, 42, 0.80)"
        color_dim = "rgba(15, 23, 42, 0.50)"
        border_color = "rgba(15, 23, 42, 0.20)"
        pill_bg = "rgba(255, 255, 255, 0.85)"
        accent_color = "#000000"
        phone_color = "#0F172A"

    brand_name = template["brand_name"]
    eyebrow = template["eyebrow"]
    hook = template["hook"]
    sub = template["sub"]
    phone = template["phone"]
    variant = template["style_variant"]

    # Aesthetic variations with SLEEK DYNAMIC THIN TYPOGRAPHY
    if variant == "signature":
        corner_decor = f"""
        <div style="position:absolute; top:28px; left:28px; width:40px; height:40px; border-top:1px solid {border_color}; border-left:1px solid {border_color};"></div>
        <div style="position:absolute; top:28px; right:28px; width:40px; height:40px; border-top:1px solid {border_color}; border-right:1px solid {border_color};"></div>
        <div style="position:absolute; bottom:28px; left:28px; width:40px; height:40px; border-bottom:1px solid {border_color}; border-left:1px solid {border_color};"></div>
        <div style="position:absolute; bottom:28px; right:28px; width:40px; height:40px; border-bottom:1px solid {border_color}; border-right:1px solid {border_color};"></div>
        """
    elif variant == "biometrics":
        corner_decor = f"""
        <div style="position:absolute; top:36px; left:36px; font-family:'JetBrains Mono',monospace; font-size:14px; font-weight:300; letter-spacing:0.18em; color:{color_dim};">AF-C [3D-TRACKING] · 1/250s · f/1.2 · ISO 64</div>
        <div style="position:absolute; top:36px; right:36px; font-family:'JetBrains Mono',monospace; font-size:14px; font-weight:300; letter-spacing:0.18em; color:{accent_color};">● REC 4K60p</div>
        <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:44px; height:44px; border:1px solid {border_color}; pointer-events:none;"></div>
        <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:12px; height:12px; background:{accent_color}; border-radius:50%; opacity:0.6; pointer-events:none;"></div>
        """
    elif variant == "pop":
        corner_decor = f"""
        <div style="position:absolute; top:28px; left:28px; font-size:16px; color:{color_dim};">✦</div>
        <div style="position:absolute; top:28px; right:28px; font-size:16px; color:{color_dim};">✦</div>
        <div style="position:absolute; bottom:28px; left:28px; font-size:16px; color:{color_dim};">✦</div>
        <div style="position:absolute; bottom:28px; right:28px; font-size:16px; color:{color_dim};">✦</div>
        """
    else:
        corner_decor = f"""
        <div style="position:absolute; top:28px; left:28px; width:24px; height:1px; background:{border_color};"></div>
        <div style="position:absolute; top:28px; left:28px; width:1px; height:24px; background:{border_color};"></div>
        <div style="position:absolute; top:28px; right:28px; width:24px; height:1px; background:{border_color};"></div>
        <div style="position:absolute; top:28px; right:28px; width:1px; height:24px; background:{border_color};"></div>
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=JetBrains+Mono:wght@300;400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600&family=Space+Grotesk:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    width: 1080px;
    height: 1350px;
    background: transparent !important;
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
  }}
  .overlay-canvas {{
    position: relative;
    width: 1080px;
    height: 1350px;
    background: transparent !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 50px 60px;
  }}
  
  /* TOP HEADER LOCKUP (Clean, perfectly centered lens logo) */
  .top-lockup {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 12px;
    z-index: 10;
  }}
  
  .logo-img {{
    width: 125px;
    height: 125px;
    object-fit: contain;
    display: block;
    filter: drop-shadow(0 4px 16px rgba(0,0,0,0.35));
  }}
  
  .brand-title {{
    font-family: {template["font_family"]};
    font-size: 20px;
    font-weight: 400;
    letter-spacing: 0.38em;
    color: {color_primary};
    text-transform: uppercase;
  }}
  
  .eyebrow-text {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 400;
    letter-spacing: 0.28em;
    color: {color_dim};
    text-transform: uppercase;
  }}
  
  /* CENTER AREA: 100% UNTOUCHED (Leaves subject completely visible) */
  .center-clearance {{
    flex: 1;
    pointer-events: none;
  }}
  
  /* BOTTOM FOOTER LOCKUP (Large readable phone, sleek thin typography) */
  .bottom-lockup {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 16px;
    z-index: 10;
  }}
  
  .hook-title {{
    font-family: {template["font_family"]};
    font-size: 26px;
    font-weight: 300;
    letter-spacing: 0.16em;
    color: {color_primary};
    text-transform: uppercase;
    text-shadow: 0 2px 10px rgba(0,0,0,0.4);
  }}
  
  .sub-tagline {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13px;
    font-weight: 400;
    letter-spacing: 0.22em;
    color: {color_secondary};
    text-transform: uppercase;
  }}
  
  /* PROMINENT, LARGE, SLEEK PHONE NUMBER BADGE */
  .contact-pill {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    padding: 12px 32px;
    border-radius: 9999px;
    background: {pill_bg};
    border: 1px solid {border_color};
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    margin-top: 4px;
  }}
  
  .wa-icon {{
    width: 22px;
    height: 22px;
    fill: #25D366;
  }}
  
  .phone-text {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 500;
    letter-spacing: 0.14em;
    color: {phone_color};
  }}
</style>
</head>
<body>
  <div class="overlay-canvas">
    {corner_decor}
    
    <!-- TOP LOCKUP -->
    <div class="top-lockup">
      <img src="file://{logo_path}" class="logo-img" alt="Captoora">
      <div class="brand-title">{brand_name}</div>
      <div class="eyebrow-text">{eyebrow}</div>
    </div>
    
    <!-- CENTER OPEN VIEW -->
    <div class="center-clearance"></div>
    
    <!-- BOTTOM LOCKUP -->
    <div class="bottom-lockup">
      <div class="hook-title">{hook}</div>
      <div class="sub-tagline">{sub}</div>
      
      <div class="contact-pill">
        <svg class="wa-icon" viewBox="0 0 24 24">
          <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.074-2.146-.532-1.857-.775-3.037-2.668-3.129-2.793-.093-.125-.751-1.002-.751-1.912 0-.911.477-1.357.646-1.542.169-.185.37-.231.493-.231.124 0 .248.002.354.007.113.006.264-.043.413.317.155.375.529 1.294.576 1.388.046.094.077.203.016.326-.062.125-.093.203-.186.312-.093.11-.195.244-.278.328-.093.093-.19.195-.082.381.108.185.48 1.834 1.705 2.569 1.226.735 1.393.754 1.579.599.186-.155.795-.929.981-1.248.186-.319.37-.266.617-.174.248.093 1.572.741 1.84.875.268.134.448.199.513.312.067.113.067.654-.077 1.059z"/>
        </svg>
        <div class="phone-text">{phone}</div>
      </div>
    </div>
  </div>
</body>
</html>
"""
    return html

def main():
    print("🎨 Renderizando 10 Nuevas Plantillas Oficiales Transparentes (Overlays Sueltos v2)...")
    
    for t in TEMPLATES:
        for mode in ["OSCURO", "CLARO"]:
            file_name = f"{t['id']}_FONDO_{mode}_4x5.png"
            out_file = os.path.join(OUTPUT_DIR, file_name)
            desktop_file = os.path.join(DESKTOP_DIR, file_name)
            
            html = generate_html(t, mode)
            temp_html_path = f"/tmp/{file_name}.html"
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html)
                
            cmd = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars",
                "--window-size=1080,1350",
                "--default-background-color=00000000",
                f"--screenshot={out_file}",
                f"file://{temp_html_path}"
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            shutil.copy2(out_file, desktop_file)
            print(f"✅ Overlay generado: {file_name}")

    print("\n🎉 Todas las 10 plantillas v2 fueron generadas con éxito.")
    print(f"📂 Repositorio: {OUTPUT_DIR}")
    print(f"🖥️ Escritorio: {DESKTOP_DIR}")

if __name__ == "__main__":
    main()
