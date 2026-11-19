# Handoff de Sesión — Serie «¡WATERS!» (2026-11-19)

Documento de continuidad para retomar el proyecto desde la computadora del laboratorio sin perder nada de contexto tras resetear la Mac anterior.

---

## 1. Decisiones creativas y de marca aprobadas

- **Concepto:** Serie vertical 9:16 de ciberseguridad + IA + cultura pop (**«¡WATERS!»**).
- **Regla de Oro de Subtítulos:** Dejar limpia la zona inferior de la pantalla para que **OpusClip** / **Captions** generen los subtítulos e insertos visuales encima.
- **Formato de video compatible (QuickTime / iPhone / OpusClip / Captions):**
  - Siempre exportar H.264 con `-vf "scale=in_range=full:out_range=limited,format=yuv420p" -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -movflags +faststart`.
  - *(Nota: Si no se convierte `in_range=full:out_range=limited`, los JPEG de Remotion quedan como `yuvj420p` y QuickTime en macOS los rechaza.)*

### Voces seleccionadas (`ElevenLabs eleven_v3` — Expressive Mode)
Se hizo un casting de 8 voces y ritmos con etiquetas de emoción (`[gasps]`, `[serious]`, `[surprised]`, `[excited]`, `[whispering]`, `[nervous]`, `[sighs]`, `[laughs]`):
- **Protagonista masculino:** `Antonio - Confident, Gentle and Clear` (`voice_id: htFfPSZGJwjBv1CL0aMD`)
- **Personaje femenino (Agy / inspiración `liken.IA`):** `Liza - Natural Mexican Creator` (`voice_id: kl7d390GatBPfqhRTyAl`)
- **Configuración API:** La `ELEVENLABS_API_KEY` **no se sube al repo** (está en `.gitignore`). En la compu del laboratorio, crea un `.env` en la raíz con `ELEVENLABS_API_KEY=tu_clave`.

---

## 2. Lo que ya está generado y listo en el repo

| Qué | Ruta en el repo | Estado |
| --- | --- | --- |
| **Render extendido >60s (para OpusClip + Captions)** | `proyectos/waters-serie/renders/WATERS_HYBRID_EP01_GTA6_NEON_60S.mp4` | `74.87s`, `1080x1920`, `30fps`, `yuv420p` (`tv`, `bt709`), 0 traslapes, datos GTA 6 (9.8M vistas, +$1,000M preventa, $3,000M año) |
| **Renders V3 anteriores** | `proyectos/waters-serie/renders/WATERS_HYBRID_EP01_GTA6_NEON_V3.mp4` y `EP02_META_AGENTE_V3.mp4` | Listos (`EP01 V3` quedó en `yuvj420p`; usar `_60S.mp4` para QuickTime) |
| **Script generador EP01 extendido** | `proyectos/waters-serie/scripts/generar_ep01_ext.py` | Genera voces `eleven_v3`, concatena WAV sin traslapes y actualiza `episodeBeats.json` |
| **Proyecto Remotion 3D/Híbrido** | `proyectos/waters-3d-studio/` | Composiciones en `src/Root.tsx` + `src/episodeBeats.json` (ejecutar `npm install` en el lab porque `node_modules` está ignorado) |
| **Biblioteca de clips de Google Flow** | `proyectos/waters-serie/biblioteca_clips/` y `proyectos/waters-3d-studio/public/clips/` | `chuy_01`..`chuy_06` y `agy_01` / `agy_03` (`720x1280`, `24fps`) |
| **Casting de voces HTML + MP3** | `proyectos/waters-serie/renders/casting_voces/` | 8 muestras con Antonio, Liza, Cristian Medina, Merari, etc. |
| **Galería de casting visual (texturas)** | `proyectos/waters-serie/casting_referencia/` | 7+ estilos guardados (`GALERIA_CASTING_WATERS.md` + `.jpg`s: Plastilina, Pixar 3D, Vinilo Designer Toy, Fieltro/Lana, 2D Tinta en 3D, LEGO, Cyber-Regio) |

---

## 3. Pendientes inmediatos para continuar en la computadora del laboratorio

### A. Nuevo guion **SIN decir «Chuy»** + firma **«¡Waters!»**
El usuario pidió cambiar el arranque y el cierre del episodio para no usar el nombre «Chuy» y convertir **«¡Waters!»** en la firma oficial de la serie:
1. **Inicio (0–4s):** El avatar está jugando GTA 6 normalmente, distraído.
2. **Interrupción (4–11s):** Llega el otro personaje (Agy / el monito), **le quita el control remoto** y le dice:
   > `¡Waters! ¿Qué, vas a jugar GTA seis sin tomar tus controles de seguridad?`
3. **Reacción sorprendida (11–15s):**
   > `¿Por qué? ¡Si ya tengo mi contraseña!`
4. **Explicación + Cifras reales:**
   > `¡Ay, no puede ser! Mira, te explico...` -> 9.8 millones de vistas en horas, +$1,000 millones de dólares en pura preventa, $3,000 millones estimados antes de fin de año (superando cualquier película, serie o videojuego), hackers con Vibe Hacking y blindaje con Gemini 4 Neon.
5. **Firma final:**
   > `¡Waters! Toma tus precauciones... ¡Waters!`

### B. Explorar otras texturas de personajes en pareja (más allá de la plastilina)
El usuario quiere ver **varias versiones / texturas** de ambos personajes (el gamer + Agy), por ejemplo:
- **Fieltro y Lana Stop-Motion**
- **Designer Toy / Vinilo Mate**
- **Cine 3D estilo Pixar**
- **2D Tinta + Semitono tipo Spider-Verse**

---

## 4. Comandos rápidos para arrancar en la compu del laboratorio

```bash
git clone git@github.com:ponchogf88/captoora.git
cd captoora/proyectos/waters-3d-studio
npm install
```
Luego crear `.env` en la raíz con `ELEVENLABS_API_KEY=...` y correr:
```bash
python3 proyectos/waters-serie/scripts/generar_ep01_ext.py
```
