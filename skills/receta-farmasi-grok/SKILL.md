---
name: receta-farmasi-grok
description: Protocolo y receta operativa para ejecución por lotes de 10 fotos Farmasi con Grok, preservación de identidad/etiquetas y conciliación durable en ledger.
---

# Receta Operativa: Ejecución de Fotos FARMASI en Lotes Automáticos de 10 con Grok

Este skill documenta la receta técnica comprobada, el prompt exacto y el flujo de automatización validado para el procesamiento masivo de la sesión Farmasi Studio en lotes de diez fotos, preservando al 100% las identidades, micro-detalles, etiquetas de producto y texturas.

---

## 1. El Flujo Comprobado y Recetas Exactas

A través de la interacción directa en el entorno de Grok (`Imagine Agent Mode` y Workspace `799`), se establecieron dos modalidades complementarias:

### A. Modalidad Compuesta: Chroma-Key + Seamless Studio Composite
Utilizada para composiciones de alta precisión y extracción limpia de figuras humanas complejas (grupos, cabello fino, vestidos y calzado):

1. **Paso 1: Extracción con Pantalla Verde (#00ff00):**
```text
Re-render this exact image with the main subject perfectly preserved, replacing the entire background with a perfectly flat solid #00ff00 chroma-key background. The background must be one uniform color with no shadows, gradients, texture, reflections, or lighting variation. Keep the subject fully separated from the background with crisp edges. Do not use #00ff00 anywhere on the subject. No cast shadow, no contact shadow, no reflection.
```

2. **Paso 2: Composición Fotográfica sobre Fondo de Estudio Captoora (`fondocaptoora`):**
```text
Take the exact cutout group of people, poses, expressions, clothing and composition from the first image as the primary subjects. Place them naturally onto the clean seamless soft cream/beige Captoora fabric backdrop and soft floor from the second reference image. Integrate ultra-realistic soft contact shadows and gentle cast shadows under every model, shoes and the dark stool so they ground solidly on the floor. Match and equalize all color tones, skin tones, lighting temperature and fabric sheen of the subjects to the warm even Captoora studio lighting of the second image. Preserve every subject perfectly: all faces, features, expressions, hair edges, flyaways and textures with photorealistic ultra-realism and no cutout halos. Keep original poses and framing. Photoreal professional studio composite that looks like one single photograph.
```

### B. Modalidad Directa por Lotes de Estudio (Drive Workspace `799`)
Utilizada para la corrección masiva de carpetas en Google Drive vinculadas al workspace `799`:

- **Segmentación por fondo original:**
  - **Fondos negros:** Ciclorama negro cálido + piso peluche negro + luz cálida de estudio.
  - **Fondos blancos:** Ciclorama blanco limpio + piso peluche blanco + luz fresca de estudio.
- **Reglas no negociables de preservación:**
  - Cero alteración o derrame de rostros (sin efecto plástico o cera).
  - Ojos intactos en forma, apertura y color original del iris.
  - Micro-detalle en cabello y bordes (flyaways naturales, sin recortes duros ni halos).
  - Preservación íntegra de logotipos y etiquetas (Farmasi, Nutriplus, etc.) sin alucinaciones tipográficas.
  - Todas las tomas alineadas de pie y orientación vertical profesional.

---

## 2. Parámetros Técnicos de Imagine / Grok

- **Modelo:** `imagine-image-edit` / `grok-4` (Expert mode)
- **Aspect Ratio:** `[3, 2]` o vertical `[2, 3]` / original sensor aspect ratio
- **Resolución:** `1k` / nativa de archivo fuente
- **Lote:** Bloques exactos de 10 unidades (`batch_size = 10`)
- **Workspace:** `e706f407-df5c-4cbd-811d-61b675daef92` (Drive Root: `1fnUJljKnCMEuGlozJg8wxVTEDnWAI9lv`)

---

## 3. Arquitectura del Ledger Durable y Bloqueo de Concurrencia

Para garantizar que ningún lote se duplique, pierda o colisione:

1. **Bloqueo de Concurrencia:**
   - Archivo lock único: `.coordinator.lock`.
   - Sólo un proceso coordinador activo puede reclamar y despachar lotes.

2. **Estados del Ciclo de Vida por ID Original:**
   - `pending`: Archivo original inventariado disponible para procesamiento.
   - `submitting`: Transición atómica persistida en disco **antes** de emitir la llamada de generación.
   - `running`: Lote recibido y aceptado por el motor generativo en espera de render.
   - `generated`: Archivo resultante generado con ID de activo o ruta en Drive asignada.
   - `needs_review`: En cola de revisión técnica paralela (aprobación final de Chuy).
   - `blocked`: Fuente omitida o no procesable por límites o incompatibilidad documentada.

3. **Reconciliación Automática ante Timeout:**
   - Antes de reintentar cualquier tarea marcada como `submitting` o `running` que exceda el tiempo límite, se consulta el endpoint histórico de respuestas (`/rest/app-chat/conversations/{id}/responses` o `/rest/workspaces/{id}/files`) para reconciliar si la generación ya concluyó efectivamente.

---

## 4. Política de Cuotas y Límites Reales

- No intentar saltarse límites ni alterar configuraciones de seguridad.
- Checkpoint inmediato al detectar advertencia de límite de cuota (guardar estado en `ledger.json` y pausar hasta ventana de reseteo).
- No subir entregas a Pixieset automáticamente ni publicar sin el visto bueno de Chuy.
