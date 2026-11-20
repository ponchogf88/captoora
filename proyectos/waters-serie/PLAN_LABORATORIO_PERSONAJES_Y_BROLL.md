# Plan de Laboratorio Multi-Herramienta (`Waters!` Neon 3D + B-Roll Real + Texturas)

**Objetivo:** Subir el nivel visual y la fluidez de movimiento de los nuevos episodios (`EP05 Fable 5.2 vs. Gemini 4 Hydrogen` y siguientes) igualando o superando la calidad cinematográfica de tus primeros clips (`biblioteca_clips/chuy_reacciones/chuy_01..06.mp4` y `biblioteca_clips/agy_explicando/agy_01..03.mp4`), combinando **todas tus herramientas**:

1. **Nano Banana** (`image-generator`) — Exploración rápida de materiales, texturas y estilos 3D.
2. **ChatGPT Image (`GPT-4o`)** — Hoja de consistencia multi-pose del personaje ganador sin deformar rasgos.
3. **Canva Pro IA** — Limpieza con Borrador/Captura Mágica, separación de capas sobre `#000000`, logos y miniaturas de portada.
4. **Google Flow (Veo)** — Animación física y facial del personaje (`Frames-to-Video` 9:16) + B-Roll generado cuando no haya captura.
5. **Remotion (`proyectos/waters-3d-studio`)** — Ensamblaje híbrido de precisión: `[Personaje Flow arriba] + [Ventana B-Roll real al centro] + [Logos SVG] + [260px inferiores limpios]` + audio `ElevenLabs v3`.
6. **Captions / OpusClip** — Toque final de retención (subtítulos dinámicos palabra por palabra, zooms sutiles, SFX y cortes de aire).

---

## 1. Respuesta directa: ¿Dónde agregamos el clon 3D de GTA 6 y los ejemplos de la casa flotante / Modo IA?

**No se lo pidas a OpusClip ni a Captions.**
- **Captions y OpusClip** tienen funciones de "AI B-Roll", pero solo insertan **clips genéricos de stock** (gente programando, pantallas aleatorias). Nunca te van a mostrar el clon 3D real de GTA 6 hecho en 10 minutos con `Gemini 4 Hydrogen`, ni la comparativa real de `$19 USD / 45 min` vs. `$1.50 USD / 12 min` de la casa flotante, ni la pantalla real de `aistudio.google.com` en `Extra Alto (xhigh)` / `Modo MAX`.
- **La ruta ganadora es Remotion + B-Roll Real (o Flow):**
  1. En **Remotion** ([WatersNeon3DEpisode.tsx](../waters-3d-studio/src/compositions/WatersNeon3DEpisode.tsx) o una evolución híbrida estilo [WatersHybridEpisode.tsx](../waters-3d-studio/src/compositions/WatersHybridEpisode.tsx)), el personaje neón 3D animado vive en la **mitad superior (`0px–820px`)**.
  2. Justo cuando la voz menciona **"un clon 3D completo de GTA 6 en 10 minutos"** o **"una animación de una casa flotante: $19 vs $1.50"**, la tarjeta central (`840px–1580px`) abre una **Ventana B-Roll Holográfica** reproduciendo el video real de ese ejemplo con su etiqueta + logo correspondiente (`Gemini 4`, `Claude Fable 5`, `Google AI Studio`, `GTA VI`).
  3. **Cómo obtenemos los clips de B-Roll para esa ventana (3 fuentes, de mejor a más rápida):**
     - **Fuente 1 (La más auténtica y cero riesgo de terceros):** Grabar 8–10 segundos reales de tu pantalla en `https://aistudio.google.com/apps` corriendo el prompt del clon de GTA 6 en **Modo MAX / Extra Alto** y de `google.com` pestaña **Modo IA**, guardar los `.mp4` en `proyectos/waters-serie/assets/broll_ep05/` y montarlos con `<OffthreadVideo>` en Remotion.
     - **Fuente 2 (Generada sin copyright en Google Flow `16:9`):** Generar un clip cinematográfico 3D del auto/lancha/avión en ciudad tipo Vice City low-poly neón y un clip de casa flotante anime/3D con Flow (`Text-to-Video`), recortado a `16:9` dentro de la tarjeta central.
     - **Fuente 3 (Simulación 3D interactiva nativa en Remotion):** Renderizar una mini escena Three.js en vivo dentro del visor inferior (edificio neón + coche + helicóptero para GTA 6; casa con globos flotando + contador `$19 vs $1.50` para Fable/Hydrogen) con nitidez nativa `1080p`.

> **Regla de oro:** **Captions** y **OpusClip** se usan **AL FINAL**, sobre el MP4 ya renderizado con el personaje + los ejemplos visuales incrustados y la franja inferior de `260px` completamente libre para los subtítulos.

---

## 2. Inventario Fase 1 (YA GENERADO con Nano Banana): 6 Texturas Neon 3D

Todas generadas en formato vertical **`9:16`** sobre **negro puro (`#000000`)** con ojos LED ultra expresivos, guardadas en `proyectos/waters-serie/casting_referencia/`:

| ID | Archivo en Repo | Textura / Dirección Visual | Mejor Uso en la Serie |
| :--- | :--- | :--- | :--- |
| **V01** | `casting_referencia/neon_v01_obsidian_oled_astro.jpg` | Robot flotante en fibra de carbono obsidiana + ojos LED pixelados cian-menta, cejas expresivas y boca waveform + trazos de circuito en el piso `#000000` | Personaje principal tech/IA ("hermano menor" elegante y carismático de Agy) |
| **V02** | `casting_referencia/neon_v02_vinyl_matte_cyber.jpg` | Designer Toy vinyl negro mate con doble antena cian, costuras neón cian y rojo-coral, brazos cruzados y mirada LED escéptica (`🤨`) | Crítica sarcástica de precios y humo tech (`$19 vs $1.50`) |
| **V03** | `casting_referencia/neon_v03_pixar_translucent_smoke.jpg` | Carcasa Pixar de cristal ahumado translúcido dejando ver bobinas de cobre dorado y circuitos cian internos + pose pensativa llevándose la mano al mentón | Explicaciones profundas de arquitectura, tokens, benchmarks |
| **V04** | `casting_referencia/neon_v04_titanium_apple_vision.jpg` | Titanio negro cepillado + visor curvo oscuro estilo Apple Vision Pro con anillos HUD holográficos azul-cian en los ojos y núcleo circular brillante en el pecho | Noticias de big tech, lanzamientos Apple/Google/OpenAI |
| **V05** | `casting_referencia/neon_v05_velvet_felt_neon_stitch.jpg` | Mascotita oso-bot de terciopelo/fieltro carbón táctil con orejitas bordadas y costuras verde neón brillante + ojos LED con destellos de estrella | Hooks de alto contraste táctil (suave + cyber) que detienen el scroll |
| **V06** | `casting_referencia/neon_v06_spiderverse_halftone_neon.jpg` | Estilo *Spider-Verse* 3D cel-shaded + puntos halftone, fragmentos prismáticos y estelas cinéticas cian/magenta con guiño asimétrico | Hooks explosivos estilo gaming/GTA 6 y comparativas de velocidad |

---

## 3. Cómo usar ChatGPT Image + Canva Pro IA + Google Flow paso a paso (El Laboratorio)

### Paso A — `ChatGPT Image (GPT-4o)` · Crear la Hoja de Expresiones Consistentes
Cuando elijas **1 o 2 texturas ganadoras** de `V01` a `V06`, súbela a **ChatGPT Image** y pide poses exactas para que **no cambie el diseño entre clips**.

**Prompt maestro para ChatGPT Image (copia y pega adjuntando la imagen ganadora de `casting_referencia/`):**

```text
Keep the exact same 3D miniature neon robot character design, proportions, materials, and pure pitch-black #000000 background from the uploaded reference image. Do NOT change its body shape or visor style. Generate a vertical 9:16 studio portrait of this EXACT same character positioned in the UPPER HALF of the frame (leaving the bottom 45% pure solid #000000 black space for screen overlays), showing THIS specific expression and pose:
[ELIGE UNA DE LAS 5 POSES DE ABAJO]
No text, no watermarks, crisp rim lighting matching the LED eyes.
```

**Las 5 poses del banco base para sustituir en `[ELIGE UNA DE LAS 5 POSES]`:**
1. **Pose 01 — Hook Shock (`¡WATERS!`):** *"Wide-eyed shock expression on the LED visor (`O_O`), both miniature hands raised near its cheeks, tiny glowing antenna tilting forward, slight dramatic lean toward camera."*
2. **Pose 02 — Escéptico / Comparando Precios:** *"One LED eyebrow arched skeptically (`🤨`), arms crossed smugly or holding a tiny glowing neon holographic scale in one hand, cool analytical head tilt."*
3. **Pose 03 — Señalando B-Roll Abajo:** *"Excited sharp LED eyes (`^ ^`) looking down toward the lower half of the black frame, one index finger pointing decisively downward at the empty black space below its chest."*
4. **Pose 04 — Mente Explotada / Velocidad MAX:** *"Glowing bright cyan-lime star-shaped LED eyes (`★ ★`), sparks of neon cyan-lime circuit light pulsing softly around its shoulders, leaning forward in amazement."*
5. **Pose 05 — Guiño Cierre (`¡Waters!`):** *"Playful warm emerald-green winking LED eye (`😉`) on the visor, giving a confident thumbs-up and pointing lightly toward the bottom corner."*

---

### Paso B — `Canva Pro IA` · Limpieza, Capas y Miniaturas
Usa tu suscripción de **Canva Pro** justo antes de animar en Flow (para perfeccionar el "Ingredient") y para las portadas de cada Short/Reel:

1. **Borrador Mágico (antes de Flow):** Si Nano Banana o ChatGPT sacó un dedo raro, un brillo molesto abajo o texto fantasma, límpialo en 5 segundos con *Editar → Borrador Mágico*. (Google Flow anima cualquier imperfección de la imagen inicial, por eso conviene entrar con imagen limpia).
2. **Quitafondos Pro + Captura Mágica (Magic Grab):**
   - Crea un lienzo **`1080 × 1920`** con fondo **`#000000` puro**.
   - Sube al personaje, usa **Quitafondos Pro** si quieres aislarlo perfectamente del fondo, y ubícalo en el **`45%` superior** dejando el **`55%` inferior totalmente negro `#000000`**. Eso garantiza que en Remotion nunca tape la ventana del clon de GTA 6 ni los logos.
3. **Plantilla de Portada / Thumbnail 9:16 (Brand Kit):**
   - Coloca el personaje arriba, al centro logos oficiales limpios (`Gemini 4` vs `Claude Fable 5`, o `GTA VI`), y titular gigante de 3 palabras (`$19 vs $1.50`, `CLON GTA 6 EN 10m`) exportado en PNG para subir como *Cover* en Reels/TikTok/YouTube Shorts.

---

### Paso C — `Google Flow (Veo)` · Movimiento Nivel Cine (`9:16`, 4–8s)
Por qué tus primeros clips (`chuy_01..06` y `agy_01..03`) quedaron increíbles: **movimiento físico real + cero diálogo hablado en Flow**. Si le pides a Flow que "hable español", deforma el visor/boca o pelea contra ElevenLabs.

**Reglas de oro para Google Flow (`labs.google/fx/tools/flow`):**
- Modo: **`Frames to Video`** (o `Ingredients to Video`).
- Aspect Ratio: **`9:16 Vertical`**, duración **`4s`–`6s`**.
- **Prohibido en el prompt:** texto flotante, subtítulos, diálogo hablado.
- **Obligatorio en el prompt:** mantener fondo `#000000` sólido, movimiento fluido de cámara + gestos claros de manos y LEDs.

**Prompts listos para generar tu banco reutilizable (`biblioteca_clips/neon_bot_reacciones/`):**

1. **`bot_01_shock_hook.mp4`** *(Usar Pose 01 como Start Frame)*
```text
High-end 3D animated character in a pure pitch-black #000000 studio void, no dialogue, no subtitles. Dynamic snappy camera push-in: the miniature neon robot gasps silently in comic shock, LED eyes snap wide open bright cyan, raises both small hands up beside its head, subtle head recoil and rim-light pulse, Pixar-quality 60fps micro-motion.
```

2. **`bot_02_skeptic_compare.mp4`** *(Usar Pose 02 como Start Frame)*
```text
High-end 3D animated character in a pure pitch-black #000000 studio void, no text, no speech. The neon robot tilts its head skeptically, narrows one glowing cyan LED eyebrow, weighs both tiny hands left and right like comparing two invisible options, smooth slow orbiting rim light, crisp tactile surface reflections.
```

3. **`bot_03_point_down_broll.mp4`** *(Usar Pose 03 como Start Frame)*
```text
High-end 3D animated character in a pure pitch-black #000000 studio void, no text, no speech. The neon robot leans slightly forward, looks intentionally down toward the lower black space of the frame with bright focused emerald-cyan LED eyes, points both index fingers downward rhythmically as if presenting an awesome demo below, gentle breathing hover motion.
```

4. **`bot_04_mindblown_fast.mp4`** *(Usar Pose 04 como Start Frame)*
```text
High-end 3D animated character in a pure pitch-black #000000 studio void, no text, no speech. Energetic burst of excitement: the neon robot flashes bright star-shaped lime-cyan LED eyes, nods enthusiastically, neon accent seams pulse fast along its arms, subtle holographic sparks shimmer cleanly against pure black background.
```

5. **`bot_05_wink_waters_cta.mp4`** *(Usar Pose 05 como Start Frame)*
```text
High-end 3D animated character in a pure pitch-black #000000 studio void, no dialogue, no text overlays. Smooth charismatic closing gesture: the neon robot smiles with curved emerald-green LED eyes, executes a clean playful wink with its right LED eye, gives a crisp thumbs-up and points once toward the lower screen, gentle studio bounce.
```

**Prompts extra en Flow (`16:9` horizontal) para generar los B-Roll del Episodio 05 (si no usas captura de pantalla):**
- **`broll_gta6_clone_3d.mp4`:**
```text
3D real-time browser game prototype viewport rendered cleanly inside a neon Vice City palm-tree beachfront avenue at dusk: a stylized sports car speeds past a glowing yellow taxi, a speedboat passes on the ocean and a small plane flies overhead, crisp low-poly futuristic Unreal/Three.js WebGL demo look, smooth 60fps camera tracking.
```
- **`broll_floating_house_3d.mp4`:**
```text
Enchanting stylized 3D animated floating wooden house carried gently upward into golden-blue sunset clouds by dozens of iridescent glowing balloons, gentle breeze swaying ropes and warm window lights, whimsical Pixar/Ghibli miniature diorama lighting, smooth seamless floating loop.
```

---

### Paso D — `Remotion` + `ElevenLabs v3` · Montaje Final Híbrido
Cuando tengas los `bot_01..05.mp4` guardados en `proyectos/waters-serie/biblioteca_clips/neon_bot_reacciones/` y los 2–3 clips de B-roll en `proyectos/waters-serie/assets/broll_ep05/`:
1. En **Remotion** (`proyectos/waters-3d-studio/`), creamos un componente `WatersHybridNeon3D.tsx` que combine:
   - **Capa superior:** `<OffthreadVideo>` con los clips reales de **Google Flow** (`bot_01..05.mp4`) en `blend` limpio sobre `#000000`.
   - **Capa central (`840px–1580px`):** Ventana B-Roll Holográfica que **muestra el clon 3D de GTA 6**, **la casa flotante (`$19 / 45 min` vs `$1.50 / 12 min`)**, y **Google AI Studio (`Extra Alto (xhigh)` / `Modo MAX`)** junto con los logos SVG de [BrandLogos.tsx](../waters-3d-studio/src/components/BrandLogos.tsx).
   - **Capa inferior (`1660px–1920px`):** `260px` completamente limpios reservados para los subtítulos dinámicos de **Captions / OpusClip**.
2. **Audio ElevenLabs (`scripts/generar_ep05_fable_vs_hydrogen.py`):**
   - Regla obligatoria ya aplicada en EP01/EP03/EP05: **"¡Waters!"** siempre en su clip separado con `language_code="en"` (acento americano nativo, jamás pocho), y el cuerpo del guion con `eleven_v3` en español ágil (`0` menciones a `"Chuy"`).
3. **Exportación final universal:** FFmpeg `yuv420p`, `bt709`, `color_range tv`, `-movflags +faststart`.

---

### Paso E — `Captions` + `OpusClip` · Empaque Viral
Sube el `.mp4` renderizado de Remotion a:
1. **Captions App:** Activa subtítulos dinámicos palabra por palabra en la zona libre inferior (`y ≈ 1680px`), añade swoosh/pop sutiles en cambios de beat y exporta en 1080×1920.
2. **OpusClip (`clip.opus.pro`):** Úsalo para A/B testing de título/portada, score de viralidad del hook inicial y programación automática en YouTube Shorts / Instagram Reels / TikTok.

---

## 4. Plan de Experimentación en 5 Rondas (Cómo iteramos sin desperdiciar créditos)

| Ronda | Objetivo del Experimento | Herramientas | Criterio de Éxito para Pasar a Producción |
| :--- | :--- | :--- | :--- |
| **Ronda 1** | Elegir **1–2 texturas ganadoras** entre `V01`..`V06` (ya generadas en `casting_referencia/`) | Nano Banana | Fondo `#000000` puro, ojos muy expresivos, que resalte en miniatura de celular |
| **Ronda 2** | Generar 5 poses consistentes del ganador (`Shock`, `Escéptico`, `Señalando`, `Mindblown`, `Guiño`) | ChatGPT Image + Canva Pro | Cero dedos deformes, exactamente el mismo diseño/material en las 5 poses, mitad inferior libre |
| **Ronda 3** | Probar **animación Flow (`4s` por pose)** hasta lograr física y parpadeo natural | Google Flow (`Frames to Video`) | Se mueve como los clips `chuy_01..06` y `agy_01..03`, sin deformar el visor ni abrir boca rara |
| **Ronda 4** | Conseguir **3 clips reales de B-Roll para EP05** (Clon GTA 6, Casa Flotante, AI Studio Modo MAX) | Grabación propia en `aistudio.google.com` o Google Flow `16:9` | Que el espectador *vea con sus propios ojos* de qué habla el bot cuando dice "clon de GTA 6 en 10 min" |
| **Ronda 5** | Compilar EP05 v2 en **Remotion** + pasar por **Captions** | Remotion + ElevenLabs + Captions | Ritmo de corte cada `2–3s`, B-Roll nítido, `"Waters!"` en inglés limpio, subtítulos sin tapar nada |
