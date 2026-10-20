# REGISTRO DE REQUISITOS Y PLAN DE REUTILIZACIÓN DE COMPONENTES
## Captoora Event Curator & Selector (v1.0 Local Dev)
**Fecha:** 20 de Octubre de 2026  
**Entorno de ejecución:** macOS M1 (Apple Silicon) - 8 GB RAM  
**Directorio de desarrollo aislado:** `/Users/user/Desktop/Projects/CAPTOORA.STUDIO/dev_event_curator/`  
**Garantía de integridad:** Cero modificaciones a scripts existentes en `/Users/user/Desktop/Projects/CAPTOORA.STUDIO/`. Cero alteraciones o sobrescritura de archivos originales.

---

### 1. AUDITORÍA DE ARCHIVOS EXISTENTES Y DIAGNÓSTICO

| Archivo auditado | Función actual | Diagnóstico / Hallazgos | Decisión de reutilización |
| :--- | :--- | :--- | :--- |
| `AGENTS.md` | Reglas maestras AMDA Engine | Reglas fundamentales: Cero pasos intermedios, cero fotos de puro texto, 100% full-frame (no crop destructivo de personas/sujetos), verificar antes de avisar. | **Reutilización total**: Gobierna la filosofía de la herramienta. Cero automatismos destructivos. |
| `foto_engine.py` | Motor batch con Pillow | Manejo robusto de orientación EXIF (`ImageOps.exif_transpose`), estructura de presets con factores de escala (exposición, contraste, saturación, nitidez). | **Reutilizado y mejorado**: Se extrae la corrección EXIF y la lógica de escalado eficiente Lanczos. Se migra el cálculo de color a LAB para proteger tonos de piel. |
| `pharmacy_event_processor.py` | Procesador de eventos con filtros | `is_blurry_pil` (varianza de Laplaciano) y `check_exposure` (análisis de histograma: sombras empastadas y altas luces quemadas). **Peligro detectado en el script original:** Descartaba y movía fotos automáticamente a una carpeta de descarte. | **Reutilizado con cambio de paradigma**: Las métricas de nitidez y exposición se usan como **diagnóstico consultivo/sugerido**, NUNCA como descarte automático. Expresiones espontáneas se conservan siempre. |
| `farmasi_retouch_master.py` | Motor de retoque en ciclorama LAB | Excelente conversión a espacio LAB (`cv2.cvtColor(BGR2LAB)`), curva gamma en canal L para levantar sombras sin virar los tonos de piel (`a` y `b`), downscaling inteligente si `max(w, h) > 3000` para no saturar los 8 GB de RAM. | **Reutilizado como base del pipeline tonal**: El espacio LAB es el núcleo para balancear sombras, altas luces y exposición preservando fidedignamente el color de piel. |
| `watch_and_process.py` | Monitor de carpetas y descompresión | Monitoreo pasivo en segundo plano. | **Referencia de arquitectura**: La herramienta local actual se enfoca en interfaz interactiva web/local para selección humana guiada. |
| `organize_master_deliveries.py` | Distribuidor de entregas | Estructura canónica: `01_ORIGINALES_CRUDAS_SESION`, `02_EDICIONES_FINALES_APROBADAS`, `03_HISTORICO_EDICIONES_DESCARTADAS`. | **Reutilizado para el módulo de exportación**: La exportación respeta la jerarquía de carpetas y nunca toca los archivos fuente. |

---

### 2. MATRIZ DE REQUISITOS DEL SISTEMA

1. **Selección y Curaduría Humana Asistida:**
   - Selección de carpeta de entrada (ej. `/Users/user/Desktop/Projects/BACKUP/glotry_staging_oct12`).
   - Carga y generación de miniaturas grandes de alto rendimiento con caché local (`.cache_thumbs/`).
   - Sistema de marcado de 3 estados: **"Sí" (Aprobada)** / **"Revisar" (Duda / Expresión espontánea)** / **"No" (Descarte sugerido)**.
   - **Regla inmutable:** Cero borrado de archivos originales. Todas las operaciones son no destructivas sobre copias.

2. **Diagnósticos Consultivos (Sin Descarte Automático):**
   - **Nitidez (Blur Score):** Varianza del filtro Laplaciano. Si el score es bajo pero hay una expresión irrepetible o gesto espontáneo, el usuario decide conservarla.
   - **Ojos cerrados / Parpadeo:** Detector consultivo de rostros y ojos con Haar Cascades locales para alertar posibles parpadeos en ráfaga.
   - **Detección de duplicados / Ráfagas:** Algoritmo dHash (difference hash) con distancia de Hamming (< 10) para agrupar disparos continuos y permitir que el usuario elija el mejor fotograma.
   - **Exposición:** Detección de subexposición (< 28 en media o > 65% sombras 0-15) y sobreexposición (> 235 o > 70% en 240-255).

3. **3 Estilos Ajustables (Presets de Evento):**
   - **Inicio Fresco:** Luz de día / arranque del evento. Balance neutro-frío muy sutil (-150K temp, +0.10 EV, altas luces controladas, negros limpios).
   - **Transición Equilibrada:** Luz ambiente natural mixta. Tono neutro puro, contraste moderado (+8%), sombras abiertas (+12%), saturación orgánica.
   - **Final Cálido:** Cierre del evento / atardecer / iluminación de fiesta. Temperatura dorada (+250K temp), medios tonos ricos, micro-contraste suave sin empastar.

4. **Controles Moderados y Preservación de Realismo:**
   - Sliders calibrados para rango seguro:
     * Temperatura (-30 a +30) y Tinte verde/magenta (-20 a +20).
     * Exposición (-1.0 a +1.0 EV).
     * Altas luces (Highlights: compresión de -50% a 0%).
     * Sombras (Shadows: elevación de 0% a +50%).
     * Reducción de ruido sutil (Filtro bilateral / Gaussiano leve).
     * Nitidez (Unsharp mask moderado: radio 1.2, amount 0.2 a 1.2).
   - **Prohibición estricta de alteraciones anatómicas o del entorno:** Cero deformación o IA generativa que invente dientes, ojos, caras, cuerpos, vestimenta o mobiliario.

5. **Gestión de Recetas (JSON):**
   - Guardar configuraciones actuales como recetas reutilizables (`.json`).
   - Aplicar una receta guardada a toda la sesión o a fotos marcadas con "Sí" / "Revisar".

6. **Optimización Mac M1 (8 GB RAM):**
   - Miniaturas de visualización rápida generadas a 1200px con compresión WebP/JPEG optimizada.
   - Procesamiento en memoria de una sola imagen completa a la vez durante la exportación; liberación explícita de memoria.

7. **Privacidad y Cero Dependencia de APIs:**
   - 100% ejecución local con Python standard library, Pillow, OpenCV y NumPy.
   - Cero llamadas a internet o subida de fotos por defecto.
   - Modos API opcionales quedan protegidos con barrera de confirmación explícita (costo, modelo, imágenes, límite de lote) y variables de entorno externas.
