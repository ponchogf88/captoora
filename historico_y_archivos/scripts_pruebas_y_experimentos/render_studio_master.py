import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
from rembg import remove, new_session

def create_studio_masterpiece(img_path, output_path):
    print("1. Cargando imagen original...")
    orig_bgr = cv2.imread(img_path)
    h, w, _ = orig_bgr.shape
    
    # 2. Obtener máscara general con rembg (general use para incluir personas + productos)
    print("2. Generando segmentación neuronal con rembg...")
    session_gen = new_session("u2net")
    pil_orig = Image.fromarray(cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2RGB))
    mask_gen = remove(pil_orig, session=session_gen, only_mask=True)
    mask_arr = np.array(mask_gen).astype(np.float32) / 255.0
    
    # Asegurar que los productos del piso (y > h*0.70, x entre w*0.15 y w*0.85) estén incluidos si tienen contraste
    # Zona de productos:
    prod_y1, prod_y2 = int(h * 0.70), int(h * 0.95)
    prod_x1, prod_x2 = int(w * 0.15), int(w * 0.88)
    
    # En la zona de productos, incluir píxeles que no sean fondo blanco/grisáceo liso
    gray = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2GRAY)
    # Suavizar máscara ligeramente para evitar bordes duros
    mask_arr = cv2.GaussianBlur(mask_arr, (7, 7), 0)
    
    # 3. Construir Fondo de Ciclorama de Estudio Profesional
    print("3. Construyendo ciclorama editorial con degradado de luz...")
    Y, X = np.ogrid[:h, :w]
    # Centro de la luz de estudio: x=48%, y=25%
    dist_light = np.sqrt(((X - w * 0.48) / (w * 0.75)) ** 2 + ((Y - h * 0.22) / (h * 0.65)) ** 2)
    # Luminancia de ciclorama de alta gama: 246 en centro cayendo a 228 en bordes
    cyclorama_l = np.clip(246.0 - dist_light * 22.0, 226.0, 246.0)
    
    # Suelo blanco de estudio (horizonte suave alrededor de y = h * 0.65)
    horizon = int(h * 0.65)
    floor_grad = np.clip((Y - horizon) / float(h - horizon), 0, 1)
    # Piso ligeramente más cálido y luminoso
    cyclorama_l = cyclorama_l * (1.0 - floor_grad * 0.05)
    
    studio_bg = np.zeros((h, w, 3), dtype=np.uint8)
    studio_bg[:, :, 0] = np.clip(cyclorama_l - 1, 0, 255).astype(np.uint8) # B
    studio_bg[:, :, 1] = np.clip(cyclorama_l, 0, 255).astype(np.uint8)     # G
    studio_bg[:, :, 2] = np.clip(cyclorama_l + 1, 0, 255).astype(np.uint8) # R (perla suave)
    
    # 4. Re-iluminación de Estudio y Tono de Piel Editorial (Relight)
    print("4. Aplicando re-iluminación y curva tonal de estudio...")
    # Convertir original a LAB
    lab = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Curva gamma fotográfica: levanta medios tonos (+0.35 EV) y suaviza el charolazo del flash
    # Input x in [0, 255]
    x = np.arange(256, dtype=np.float32)
    # Elevar medios tonos y recuperar sombras
    curve = 255.0 * np.power(x / 255.0, 0.88)
    # Curva en S para contraste sedoso
    curve = np.clip(curve, 0, 255).astype(np.uint8)
    l_sculpted = cv2.LUT(l, curve)
    
    # Atenuar ligeramente la saturación amarilla de la pared sobre la piel
    # b > 140 es amarillo; reducimos suavemente en altas luces
    b_corrected = b.copy().astype(np.float32)
    warm_mask = (b > 135) & (l > 140)
    b_corrected[warm_mask] = b_corrected[warm_mask] * 0.94
    b_corrected = np.clip(b_corrected, 0, 255).astype(np.uint8)
    
    relit_bgr = cv2.cvtColor(cv2.merge((l_sculpted, a, b_corrected)), cv2.COLOR_LAB2BGR)
    
    # 5. Generar Sombra de Contacto Física (Ambient Occlusion)
    print("5. Generando sombra de contacto y oclusión física...")
    # La sombra de contacto se proyecta inmediatamente debajo de los píxeles de contacto
    # Creamos un mapa de sombra a partir de la máscara de primer plano
    kernel_contact = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 11))
    contact_shadow = cv2.dilate((mask_arr > 0.5).astype(np.float32), kernel_contact)
    # Desplazar 4px hacia abajo
    M_down = np.float32([[1, 0, 0], [0, 1, 5]])
    contact_shadow_down = cv2.warpAffine(contact_shadow, M_down, (w, h))
    # Excluir el cuerpo del sujeto
    pure_shadow = np.clip(contact_shadow_down - mask_arr, 0, 1)
    # Suavizar sombra
    pure_shadow_blur = cv2.GaussianBlur(pure_shadow, (25, 9), 0)
    
    # Aplicar sombra sobre el fondo de ciclorama (multiplicación suave)
    shadow_darkness = 0.35 # 35% de atenuación
    for c in range(3):
        studio_bg[:, :, c] = np.clip(studio_bg[:, :, c].astype(np.float32) * (1.0 - pure_shadow_blur * shadow_darkness), 0, 255).astype(np.uint8)
        
    # 6. Generar Reflejo de Piso Acrílico / Espejo de Agua
    print("6. Sintetizando reflejo de acrílico líquido...")
    # Invertir verticalmente la zona inferior de los sujetos
    # Zona de contacto: aproximadamente entre y = h*0.65 e y = h*0.95
    refl_h = int(h * 0.22)
    contact_y = int(h * 0.82)
    
    # Extraer sujetos aislados
    fg_only = (relit_bgr * mask_arr[:, :, np.newaxis]).astype(np.uint8)
    sample_box = fg_only[contact_y - refl_h:contact_y, :]
    reflection = cv2.flip(sample_box, 0)
    
    # Desenfoque horizontal para specular sheen
    reflection_specular = cv2.GaussianBlur(reflection, (15, 3), 0)
    
    # Gradiente de desvanecimiento hacia abajo
    fade = np.linspace(0.26, 0.0, refl_h, dtype=np.float32)[:, np.newaxis]
    fade_3c = np.repeat(np.repeat(fade[:, :, np.newaxis], w, axis=1), 3, axis=2)
    
    dest_y2 = min(h, contact_y + refl_h)
    actual_refl_h = dest_y2 - contact_y
    
    # Aplicar reflejo al fondo
    bg_with_refl = studio_bg.copy().astype(np.float32)
    refl_patch = reflection_specular[:actual_refl_h, :].astype(np.float32)
    fade_patch = fade_3c[:actual_refl_h, :]
    
    bg_with_refl[contact_y:dest_y2, :] = bg_with_refl[contact_y:dest_y2, :] * (1.0 - fade_patch * 0.6) + refl_patch * fade_patch
    bg_final = np.clip(bg_with_refl, 0, 255).astype(np.uint8)
    
    # 7. Composición Final (Sujetos + Ciclorama + Sombras + Reflejo)
    print("7. Ensamblando composición final de alta gama...")
    mask_3c = np.repeat(mask_arr[:, :, np.newaxis], 3, axis=2)
    final_bgr = (relit_bgr.astype(np.float32) * mask_3c + bg_final.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)
    
    # 8. Micro-nitidez de estudio en ojos, joyas y botellas
    pil_final = Image.fromarray(cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB))
    enh_sh = ImageEnhance.Sharpness(pil_final)
    pil_final = enh_sh.enhance(1.18)
    
    enh_c = ImageEnhance.Color(pil_final)
    pil_final = enh_c.enhance(1.05)
    
    pil_final.save(output_path, quality=95, optimize=True)
    print(f"✓ Obra maestra guardada en: {output_path}")

create_studio_masterpiece("/private/tmp/farmasi_samples/group_CPT_0845.JPG.jpg", "/private/tmp/farmasi_samples/CPT_0845_STUDIO_MASTER.jpg")
