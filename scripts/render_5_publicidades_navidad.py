import os
import subprocess
import shutil

OUTPUT_DIR = "/Users/imac/Desktop/PUBLICIDADES_NAVIDAD_CAPTOORA"
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOGO_WHITE = "/Users/imac/captoora/assets/captoora_logo_lente_centrado_blanco.png"

ADS = [
    {
        "filename": "01_PUBLICIDAD_CAPTOORA_STUDIO_FAMILIAR.png",
        "brand_title": "CAPTOORA STUDIO",
        "eyebrow": "SET NAVIDEÑO 2026 // MONTERREY, N.L.",
        "is_collage": False,
        "image_path": "/Users/imac/captoora/assets/navidad_2026/02_navidad_studio_familiar.jpg",
        "package_title": "PAQUETE FAMILIAR DIGITAL",
        "bullets": [
            "Hasta 6 personas (o 4 personas + 2 mascotas)",
            "1 hora completa en set navideño cálido",
            "2 cambios de vestuario incluidos",
            "Galería digital privada en alta resolución",
            "Retoque editorial piel por piel sin marcas de agua"
        ],
        "price": "$3,500",
        "currency": "MXN",
        "deposit_pill": "Aparta hoy con $1,500",
        "theme_accent": "#E5B25D",
        "theme_pill_bg": "#E5B25D",
        "theme_pill_text": "#1A1208"
    },
    {
        "filename": "02_PUBLICIDAD_CAPTOORA_SIGNATURE_GALA2027.png",
        "brand_title": "CAPTOORA SIGNATURE",
        "eyebrow": "HAUTE COUTURE // GALA AÑO NUEVO 2027",
        "is_collage": False,
        "image_path": "/Users/imac/captoora/assets/navidad_2026/01_navidad_signature_luxury.jpg",
        "package_title": "PAQUETE GALA AÑO NUEVO 2027",
        "bullets": [
            "Parejas o individual de gala / vestidos de noche",
            "Set exclusivo: champagne real y globos 2027",
            "1 hora completa de iluminación editorial de autor",
            "2 cambios de outfit (black-tie & fiesta de gala)",
            "Retoque de estándar revista de moda internacional"
        ],
        "price": "$4,500",
        "currency": "MXN",
        "deposit_pill": "Aparta hoy con $2,000",
        "theme_accent": "#F3E5AB",
        "theme_pill_bg": "#D4AF37",
        "theme_pill_text": "#0F0C05"
    },
    {
        "filename": "03_PUBLICIDAD_CAPTOORA_PETS_NAVIDAD.png",
        "brand_title": "CAPTOORA PETS",
        "eyebrow": "PET-FRIENDLY STUDIO // EDICIÓN NAVIDEÑA",
        "is_collage": True,
        "collage_main": "/Users/imac/captoora/assets/navidad_2026/07_navidad_duena_con_perro.jpg",
        "collage_top": "/Users/imac/captoora/assets/navidad_2026/06_navidad_pets_perro.jpg",
        "collage_bottom": "/Users/imac/captoora/assets/navidad_2026/08_navidad_perro_regalos.jpg",
        "package_title": "PAQUETE NAVIDAD PELUDA",
        "bullets": [
            "Hasta 2 mascotas + dueños incluidos",
            "Tú y tu mejor amigo en el Set Navideño",
            "Accesorios: gorritos navideños, bufandas y moños",
            "Premios hipoalergénicos y paciencia total en set",
            "Galería digital completa en alta resolución"
        ],
        "price": "$3,500",
        "currency": "MXN",
        "deposit_pill": "Aparta hoy con $1,500",
        "theme_accent": "#FFB86C",
        "theme_pill_bg": "#FFB86C",
        "theme_pill_text": "#221300"
    },
    {
        "filename": "04_PUBLICIDAD_CAPTOORA_BIOMETRICS_2027.png",
        "brand_title": "CAPTOORA BIOMETRICS",
        "eyebrow": "PREVENTA 2027 // TU PRIME FÍSICO EN ALTA DEFINICIÓN",
        "is_collage": False,
        "image_path": "/Users/imac/captoora/assets/biometrics_athlete_rimlight.jpg",
        "package_title": "PAQUETE PRIME FÍSICO 2027",
        "bullets": [
            "Iluminación quirúrgica Rim-Light de modelado",
            "Ciclorama negro y simetría anatómica sin distorsión",
            "Enfoque en definición muscular y recomposición",
            "Telemetría deportiva HUD para atletas y gym",
            "Preventa: aparta en Diciembre, tómala en Enero"
        ],
        "price": "$3,500",
        "currency": "MXN",
        "deposit_pill": "Aparta hoy con $1,500",
        "theme_accent": "#00F0FF",
        "theme_pill_bg": "#00F0FF",
        "theme_pill_text": "#001D24"
    },
    {
        "filename": "05_PUBLICIDAD_CAPTOORA_POP_KIDS.png",
        "brand_title": "CAPTOORA POP!",
        "eyebrow": "MINI-SESIONES // FOTOS SIN ESTRÉS",
        "is_collage": False,
        "image_path": "/Users/imac/captoora/assets/navidad_2026/05_navidad_pop_infantil.jpg",
        "package_title": "PAQUETE KIDS & CARTAS A SANTA",
        "bullets": [
            "Bebés y niños pequeños (hasta 3 hermanitos)",
            "Pijamadas navideñas o trajes festivos",
            "Set interactivo con galletas y buzón de Santa",
            "45 minutos de fotos espontáneas sin poses rígidas",
            "Galería digital completa en alta resolución"
        ],
        "price": "$2,900",
        "currency": "MXN",
        "deposit_pill": "Aparta hoy con $1,000",
        "theme_accent": "#FF5376",
        "theme_pill_bg": "#FF5376",
        "theme_pill_text": "#240008"
    }
]

def generate_html(ad):
    bullets_html = "".join([f"<li><span class='bullet-icon'>✦</span> {b}</li>" for b in ad["bullets"]])
    
    if ad.get("is_collage"):
        photo_markup = f"""
        <div class="photo-collage">
          <div class="collage-main">
            <img src="file://{ad['collage_main']}" class="collage-img" alt="Main">
          </div>
          <div class="collage-side">
            <div class="collage-side-top">
              <img src="file://{ad['collage_top']}" class="collage-img" alt="Top">
            </div>
            <div class="collage-side-bottom">
              <img src="file://{ad['collage_bottom']}" class="collage-img" alt="Bottom">
            </div>
          </div>
        </div>
        """
    else:
        photo_markup = f"""
        <div class="photo-frame">
          <img src="file://{ad['image_path']}" class="hero-photo" alt="Set">
          <div class="photo-overlay"></div>
        </div>
        """
        
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Cinzel:wght@600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap');
    
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    
    body {{
      width: 1080px;
      height: 1350px;
      background: radial-gradient(circle at 50% 15%, #1f1815 0%, #0d0a09 70%, #050404 100%);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      color: #FFFFFF;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 38px 46px 32px 46px;
    }}
    
    /* TOP HEADER & LOGO */
    .header {{
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      position: relative;
      z-index: 10;
    }}
    
    .logo-container {{
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 6px;
    }}
    
    .logo-img {{
      height: 72px;
      width: auto;
      object-fit: contain;
      filter: drop-shadow(0 4px 12px rgba(0,0,0,0.6));
    }}
    
    .brand-title {{
      font-family: 'Cinzel', serif;
      font-size: 34px;
      font-weight: 800;
      letter-spacing: 4px;
      color: #FFFFFF;
      text-transform: uppercase;
      text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }}
    
    .eyebrow {{
      font-size: 13.5px;
      font-weight: 600;
      letter-spacing: 3.5px;
      color: {ad["theme_accent"]};
      text-transform: uppercase;
    }}
    
    /* SINGLE PHOTO FRAME */
    .photo-frame {{
      width: 100%;
      height: 730px;
      border-radius: 20px;
      overflow: hidden;
      position: relative;
      box-shadow: 0 20px 50px rgba(0,0,0,0.7), 0 0 0 1px rgba(255,255,255,0.08);
      border: 1px solid rgba(229, 178, 93, 0.25);
    }}
    
    .hero-photo {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      display: block;
    }}
    
    .photo-overlay {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 140px;
      background: linear-gradient(to top, rgba(13,10,9,0.85) 0%, transparent 100%);
    }}
    
    /* 3-PHOTO COLLAGE (MATCHING USER REFERENCE) */
    .photo-collage {{
      width: 100%;
      height: 730px;
      display: flex;
      gap: 12px;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 20px 50px rgba(0,0,0,0.7), 0 0 0 1px rgba(255,255,255,0.08);
      border: 1px solid rgba(229, 178, 93, 0.25);
      background: #0d0a09;
      padding: 6px;
    }}
    
    .collage-main {{
      flex: 1.55;
      height: 100%;
      overflow: hidden;
      border-radius: 14px;
    }}
    
    .collage-side {{
      flex: 1;
      height: 100%;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    
    .collage-side-top, .collage-side-bottom {{
      flex: 1;
      overflow: hidden;
      border-radius: 14px;
    }}
    
    .collage-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    
    /* BOTTOM CARD */
    .bottom-card {{
      background: rgba(22, 17, 15, 0.92);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 22px;
      padding: 28px 34px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 15px 40px rgba(0,0,0,0.6);
      position: relative;
    }}
    
    .left-col {{
      flex: 1;
      padding-right: 24px;
    }}
    
    .package-name {{
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 2px;
      color: {ad["theme_accent"]};
      text-transform: uppercase;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    
    .bullet-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    
    .bullet-list li {{
      font-size: 14.5px;
      font-weight: 500;
      color: rgba(255, 255, 255, 0.92);
      line-height: 1.35;
      display: flex;
      align-items: flex-start;
      gap: 8px;
    }}
    
    .bullet-icon {{
      color: {ad["theme_accent"]};
      font-size: 13px;
      line-height: 1.35;
    }}
    
    .right-col {{
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      justify-content: center;
      min-width: 290px;
      border-left: 1px solid rgba(255, 255, 255, 0.12);
      padding-left: 28px;
    }}
    
    .price-box {{
      display: flex;
      align-items: baseline;
      gap: 6px;
      margin-bottom: 12px;
    }}
    
    .price-amount {{
      font-family: 'Playfair Display', serif;
      font-size: 56px;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1;
      letter-spacing: -0.5px;
      text-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}
    
    .price-currency {{
      font-size: 15px;
      font-weight: 700;
      letter-spacing: 1.5px;
      color: {ad["theme_accent"]};
    }}
    
    .deposit-pill {{
      background: {ad["theme_pill_bg"]};
      color: {ad["theme_pill_text"]};
      font-size: 16px;
      font-weight: 800;
      padding: 12px 22px;
      border-radius: 50px;
      letter-spacing: 0.3px;
      box-shadow: 0 8px 25px rgba(0,0,0,0.45), 0 0 15px {ad["theme_pill_bg"]}40;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
    }}
    
    /* FOOTER */
    .footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 10px;
      font-size: 12px;
      color: rgba(255, 255, 255, 0.55);
      font-weight: 500;
      letter-spacing: 1.2px;
      text-transform: uppercase;
    }}
    
    .footer-left {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    
    .footer-right {{
      display: flex;
      align-items: center;
      gap: 8px;
      color: {ad["theme_accent"]};
      font-weight: 700;
    }}
  </style>
</head>
<body>

  <!-- TOP HEADER -->
  <div class="header">
    <div class="logo-container">
      <img src="file://{LOGO_WHITE}" class="logo-img" alt="Captoora">
      <div class="brand-title">{ad["brand_title"]}</div>
    </div>
    <div class="eyebrow">{ad["eyebrow"]}</div>
  </div>

  <!-- SHOWCASE PHOTO / COLLAGE -->
  {photo_markup}

  <!-- BOTTOM CARD -->
  <div class="bottom-card">
    <div class="left-col">
      <div class="package-name">{ad["package_title"]}</div>
      <ul class="bullet-list">
        {bullets_html}
      </ul>
    </div>
    <div class="right-col">
      <div class="price-box">
        <span class="price-amount">{ad["price"]}</span>
        <span class="price-currency">{ad["currency"]}</span>
      </div>
      <div class="deposit-pill">
        {ad["deposit_pill"]}
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div class="footer-left">📍 San Jerónimo / Barrio Antiguo · Monterrey, N.L.</div>
    <div class="footer-right">AGENDA VÍA WHATSAPP · @CAPTOORA.STUDIO</div>
  </div>

</body>
</html>
"""
    return html

def main():
    print("🎨 Renderizando artes actualizados con collage de Captoora Pets...")
    for ad in ADS:
        out_file = os.path.join(OUTPUT_DIR, ad["filename"])
        html_code = generate_html(ad)
        temp_html = f"/tmp/{ad['filename']}.html"
        
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(html_code)
            
        cmd = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1080,1350",
            f"--screenshot={out_file}",
            f"file://{temp_html}"
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"✅ Generado: {ad['filename']}")

    print(f"\n🎉 ¡Las 5 publicidades fueron creadas en {OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
