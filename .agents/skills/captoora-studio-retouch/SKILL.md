---
name: captoora-studio-retouch
description: Motor oficial de retoque de estudio de Captoora Studio (Textura Real de Tela Blanca que Cae + Tapete de Peluche + Candado Biométrico + Rescate Multi-Toma de Nitidez con SFace/YuNet + Deconvolución sin Halos). Úsese siempre que el usuario pida editar fotografías de estudio en fondo blanco de tela colgada, limpiar paneles acústicos/techo/tripiés, o rescatar fotografías con desenfoque de cámara.
---

# Captoora Studio Retouch & Biometric Rescue Skill (`captoora-studio-retouch`)

Esta **Skill** encapsula la receta maestra probada y aprobada por Poncho para las producciones de **Captoora Studio** (como el proyecto **Farmasi 799 del 31 de Octubre**).

---

## 1. Reglas de Oro Inquebrantables (Ley Visual Captoora)

1. **El fondo blanco NO es un ciclorama plano infinito (`255`):**
   - El set real de Captoora Studio tiene **una tela blanca colgada en la parte trasera con caída y pliegues verticales sutiles (`textura de tela que cae de color blanco`)**, y en el piso un **tapete de peluche blanco (`white plush rug`)**.
   - Jamás quemar el fondo a blanco `255` plano ni generar viñetas blancas o marcos rectangulares.
2. **Igualación Armónica de Luminancia sin Marcos (`distance_transform_edt`):**
   - Para extender la tela blanca hacia las orillas (donde se eliminan paneles acústicos negros 3D, techo, cables, tripiés o muebles), se muestrean los píxeles reales del interior de la tela (`small_mask < 0.03`, `sats < 12.0`, `lums` en el rango real de la tela de esa toma específica, hasta `254.0` cuando el flash la ilumina fuerte, excluyendo las cajas de los sujetos) y se propagan hacia afuera con `scipy.ndimage.distance_transform_edt` + doble suavizado gaussiano (`sigma=(16, 20)` y `sigma=(9, 12)`).
   - Sobre esa base armónica se inyectan los pliegues verticales reales de caída de tela (`cloth_folds`) y en el tercio inferior (`y >= floor_y`) la textura real de alta frecuencia del tapete de peluche blanco (`rug_detail`, acotada en `[-18, +18]`).
3. **Zero Crop (100% Full-Frame) y Candado Biométrico (`protected_changed == 0`):**
   - Prohibido recortar personas, manos, codos, rodillas, tacones o productos.
   - En extremidades que cruzan frente a los paneles acústicos negros (como rodillas o piernas en las orillas), se traza la curva anatómica exacta con una ligera entrada de seguridad (`+0.003`) y pluma corta (`sigma=3.5`) para que no quede ni escalón rectangular ni línea gris del panel negro.

---

## 2. Protocolo de Rescate de Fotos Borrosas (`Biometric Multi-Shot HF Transfer + Halo-Free Deconvolution`)

Cuando una fotografía grupal o individual tenga ligero desenfoque de cámara o movimiento:
1. **Detección y Emparejamiento Biométrico (`YuNet` + `SFace`):**
   - Detectar los rostros y sus 5 puntos biométricos con `/Users/imac/artemis/models/face_detection_yunet.onnx` y extraer embeddings con `/Users/imac/artemis/models/face_recognition_sface.onnx`.
   - Buscar automáticamente en las tomas hermanas de la misma sesión la versión más nítida de cada persona (`sim > 0.62`, máxima varianza de Laplaciano).
2. **Alineación Sub-Píxel (`estimateAffinePartial2D` + `DISOpticalFlow`):**
   - Alinear los 5 landmarks del rostro donante al rostro destino, igualar su iluminación local en el canal `L` (espacio `LAB`) y refinar con flujo óptico denso (`cv2.DISOpticalFlow`).
   - Transferir únicamente el detalle de alta frecuencia (`donor_hf - target_hf`) ponderado por el mapa de coherencia fotométrica y concentrado en ojos, pestañas, cejas y sonrisa.
3. **Deconvolución Bilateral Libre de Halos:**
   - Aplicar 5 iteraciones de deconvolución Richardson-Lucy suave (`sigma=2.8`) combinada con filtro bilateral en el canal `L`, acotando con `tanh` y enmascarando hacia el interior de la silueta (`~binary_dilation(is_bg, iterations=12)`) para evitar cualquier halo blanco alrededor del cabello o brazos.

---

## 3. Protocolo de Retoque en Fondo Negro (`Carbón Profundo + Destello Ámbar`)

Cuando la sesión se toma en el set oscuro de tela carbón con luz lateral cálida (como los retratos editoriales individuales con tatuaje, copa de cristal, periódico o paletas Farmasi):
1. **Orientación Vertical y Full-Frame (`4128x6192`):**
   - Rotar `90°` (`im.rotate(90, expand=True)`) cuando la toma viene acostada en `6192x4128`, conservando el 100% del encuadre sin recortar (`Zero Crop`).
2. **Inpainting del Propio Fondo Oscuro (Cero Halos Ovalados en Cabello):**
   - **Prohibido** sustituir el fondo alrededor de la cabeza por una fórmula sintética de distinto tono que deje un óvalo oscuro visible alrededor de los cabellos sueltos (`flyaways`).
   - Primero se pre-limpian las intrusiones brillantes (columnas blancas, zoclos/rodapiés blancos, esquinas de panel LED o cortinas laterales) con el tono carbón local exacto de la toma (`RGB ~ [12, 11, 11]`), antes de reducir a `1/8` de escala.
   - Después se aplica `cv2.inpaint(..., cv2.INPAINT_TELEA)` + suavizado gaussiano amplio (`sigma=18` a escala `1/8`) sobre el propio fondo oscuro de la fotografía + micro-grano de sensor (`sigma=0.45`). Así los cabellos sueltos dentro del óvalo de protección y el fondo suavizado exterior tienen **exactamente el mismo tono carbón y destello ámbar**, eliminando pliegues de tela y costuras sin ningún borde ni halo.
3. **Recorte Anatómico Exacto junto a Vestido o Hombro:**
   - Cuando un zoclo blanco, cortina o esquina de panel LED toca el borde del vestido beige o del brazo, se traza la curva exacta del borde del vestido (`dress_right_bound` o `left_arm_bound`) fila por fila para limpiar hasta el último píxel de la intrusión sin alterar ni un solo píxel de la embajadora (`protected_changed == 0`).

---

## 4. Scripts de Referencia Probados
- Motor de Lote 5 Vestidos Cobrizos (V9): `/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f/scratch/cobrizo_5_edit/run_5_cobrizo.py`
- Motor de Rescate Óptico + Biométrico (`DSC08355 2.JPG`): `/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f/scratch/cobrizo_5_edit/rescue_01_cobrizo.py`
- Motor de Lote 1 y 2 Grupos en Fondo Blanco (`10 grupales`): `/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f/scratch/cobrizo_5_edit/run_5_grupos.py` y `run_5_grupos_lote2.py`
- Motor de Retratos Individuales en Fondo Negro (`5 retratos tatuaje`): `/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f/scratch/cobrizo_5_edit/run_5_cachorra_negro.py`

