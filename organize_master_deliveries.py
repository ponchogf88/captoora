import os
import shutil

raw_dir = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026"
final_hq_dir = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/01_Alta_Resolucion_Cliente"
final_4x5_dir = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/02_Redes_Instagram_4x5"
final_9x16_dir = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/03_Stories_Reels_9x16"

# Target bases
targets = [
    # 1. Google Drive in PROJECTS / ESTUDIO CAPTOORA
    "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/ESTUDIO CAPTOORA/ENTREGAS_FARMASI_SESION_10_OCT",
    # 2. Google Drive in AI CAPTOORA / PORTAFOLIO / GROUPS / FARMASI SESSION 10 10 2026 / ENTREGA_OFICIAL
    "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/ENTREGA_OFICIAL_ORGANIZADA",
    # 3. iCloud Drive for instant phone access
    os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Captoora/ENTREGA_FARMASI_TERE_10_OCT")
]

core_photos = ["CPT_0550.JPG", "CPT_0580.JPG", "CPT_0630.JPG", "CPT_0700.JPG", "CPT_0750.JPG", "CPT_0800.JPG", "CPT_0845.JPG"]

for base in targets:
    f1 = os.path.join(base, "01_ORIGINALES_CRUDAS_SESION")
    f2 = os.path.join(base, "02_EDICIONES_FINALES_APROBADAS")
    f2_hq = os.path.join(f2, "Alta_Resolucion")
    f2_4x5 = os.path.join(f2, "Instagram_Feed_4x5")
    f2_9x16 = os.path.join(f2, "Stories_Reels_9x16")
    f3 = os.path.join(base, "03_HISTORICO_EDICIONES_DESCARTADAS")
    
    os.makedirs(f1, exist_ok=True)
    os.makedirs(f2_hq, exist_ok=True)
    os.makedirs(f2_4x5, exist_ok=True)
    os.makedirs(f2_9x16, exist_ok=True)
    os.makedirs(f3, exist_ok=True)
    
    # Copy 01 Originales Crudas
    for cp in core_photos:
        src = os.path.join(raw_dir, cp)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(f1, cp))
            
    # Copy 02 Ediciones Finales Aprobadas
    for hq_file in os.listdir(final_hq_dir):
        if hq_file.endswith(".jpg"):
            shutil.copy2(os.path.join(final_hq_dir, hq_file), os.path.join(f2_hq, hq_file))
            
    for f4 in os.listdir(final_4x5_dir):
        if f4.endswith(".jpg"):
            shutil.copy2(os.path.join(final_4x5_dir, f4), os.path.join(f2_4x5, f4))
            
    for f9 in os.listdir(final_9x16_dir):
        if f9.endswith(".jpg"):
            shutil.copy2(os.path.join(final_9x16_dir, f9), os.path.join(f2_9x16, f9))
            
    # Copy 03 Historico de ediciones descartadas
    # Discarded versions from /private/tmp/farmasi_samples/
    discarded_samples = [
        "/private/tmp/farmasi_samples/group_CPT_0845_FINAL.jpg",
        "/private/tmp/farmasi_samples/outpainted_0845.jpg",
        "/private/tmp/farmasi_samples/group_flaws_fixed_v3.jpg",
        "/private/tmp/farmasi_samples/retouched_0550_crop4x5.jpg",
        "/private/tmp/farmasi_samples/retouched_0750.jpg",
        "/private/tmp/farmasi_samples/retouched_0800.jpg"
    ]
    for ds in discarded_samples:
        if os.path.exists(ds):
            shutil.copy2(ds, os.path.join(f3, "Descartada_" + os.path.basename(ds)))
            
    # Write a clean explanation note in each folder
    with open(os.path.join(base, "LEEME_ESTRUCTURA_CARPETAS.md"), "w") as f:
        f.write("""# 📁 ESTRUCTURA OFICIAL DE ENTREGA - ESTUDIO CAPTOORA
Sesión: Farmasi Nutriplus - 10 de Octubre de 2026
Cliente: Lic. Tere y Socias

Esta carpeta contiene exactamente las 3 categorías solicitadas por Poncho:

### 1. `01_ORIGINALES_CRUDAS_SESION/`
Los negativos digitales directos de la Nikon D3500, 100% intactos sin ningún retoque.

### 2. `02_EDICIONES_FINALES_APROBADAS/`
Las versiones maestras oficiales terminadas:
* Fondo de ciclorama blanco continuo sin puertas ni paredes amarillas.
* Suelo de estudio limpio sin azulejos ni arrugas de plástico celofán.
* Siluetas limpias sin telas azules ni estelas de soportes.
* Piel de seda iluminada (+0.35 EV) y realce estético natural.
* Organizadas en: `Alta_Resolucion/`, `Instagram_Feed_4x5/` y `Stories_Reels_9x16/`.

### 3. `03_HISTORICO_EDICIONES_DESCARTADAS/`
Todas las pruebas intermedias generadas durante el proceso que contenían defectos (como el corte en la rodilla, el borde de clóset o las líneas de piso) para que quede registro histórico de la evolución del retoque.
""")
        
    print(f"✓ Estructura completada en: {base}")

print("🎉 Organización maestra finalizada con éxito.")
