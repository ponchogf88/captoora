# Scripts de Retoque y Rescate — Sesión `f2879dea` (Lotes `01..29`, Skill `captoora-studio-retouch`)

Respaldo exacto de los **11 scripts Python** creados y ejecutados durante la sesión `2026-11-05` / `2026-11-06` (`f2879dea-081d-4db4-bc8f-53d5a02e349f`), correspondientes al lote **Cobrizo, Grupales, Tatuaje Hombro Rosa (`16..20`) y Mancuerna (`21..29`)** para **Partes 1 y 2** de Pixieset (`Farmasi Studio · Gala & Fit`).

> **Nota de Ley Captoora & Validadores (`validar.py`):** Esta carpeta contiene **únicamente código Python y documentación** (cero imágenes `.jpg`/`.png`). Los scripts conservan las rutas originales usadas en la `iMac 2015` (`/Users/imac/...`) como registro histórico reproducible; para correrlos en **Windows**, cambia `BRAIN`, `SRC_DIR`, `SRC_ALL` y la ruta de `face_detection_yunet.onnx` a tus carpetas temporales locales desde Google Drive (`lic.jagf87@gmail.com`).

## Inventario de Scripts Rescatados

1. **`test_helper.py`**: Utilidades base (orientación EXIF automática, composición de tela blanca y extracción de parches de prueba).
2. **`run_5_cobrizo.py`** y **`rescue_01_cobrizo.py`**: Pipeline del primer lote de **Vestido Cobrizo (`01..05`)** + rescate de detalle/nitidez sobre `01_DSC08355_2` respetando textura real de tela blanca que cae y tapete de peluche. *(Estatus: pendientes de confirmación final).*
3. **`run_5_more_groups.py`** y **`run_11_to_15_groups.py`**: Procesamiento de grupales `06..15` (`DSC08447`..`DSC09341_2`) preservando pies, manos, cuerpos completos y textura de peluche real.
4. **`run_5_cachorra_negro.py`**: Producción de **Tatuaje Hombro Rosa (`16..20`)** (`DSC01880`, `DSC01919`, `DSC01973`, `DSC01982`, `DSC01987`) — **5/5 APROBADAS** por Poncho y entregadas en Google Drive `JPG` / Pixieset Parte 1.
5. **`run_6_mancuerna_blanco_y_grupo.py`**: Set blanco Mancuerna (`21..23`: `DSC01779`, `DSC01782`, `DSC01799`) + base grupal `27..29`.
6. **`run_7_negro_espresso.py`**, **`run_8_negro_espresso_v3.py`** y **`run_negro_velvet_mancuerna.py`**: Evolución del fondo negro terciopelo estilo **"La Morena"** (sin arrugas, halo suave detrás de la cabeza y micro-grano anti-banding) para `24_DSC00373`, `25_DSC00408` y `26_DSC00415`.
   - `25` y `26`: **APROBADAS** y entregadas en Pixieset Parte 1.
   - `24_DSC00373_MANCUERNA_NEGRO_PALETA_PRO`: **RECHAZADA por Poncho** (Step 2410) — debe rehacerse para Parte 2.
7. **`rescue_29_final.py`**: Rescate multi-toma de **ojos (`DSC08712` -> `DSC08716`)** con **OpenCV YuNet (`face_detection_yunet.onnx`)**, igualación colorimétrica LAB en bajas frecuencias, recuperación tonal de altas luces sin posterizar y rescate de nitidez de calzado en `29_DSC08716`.
