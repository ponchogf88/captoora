# Respaldo Íntegro de Conversación — Serie «¡WATERS!», Casting Visual/Voces ElevenLabs v3 y Estudio Remotion 3D

- **Rama principal actualizada:** `main` (`ponchogf88/captoora`)
- **ID de conversación original (Antigravity):** `82fb8bb2-5453-4b16-a6f5-64cfc8a61599`
- **Equipo de origen:** `iMac 2015` (`/Users/imac/Desktop/Projects/CAPTOORA.STUDIO`)
- **Rango temporal:** `2026-11-14 09:02:46` a `2026-11-19 09:13:08` (`America/Monterrey`)
- **Eventos capturados en `raw/transcript_full.jsonl`:** `1,577` (`138` mensajes explícitos del usuario · `137` respuestas visibles del agente)

---

## 🧭 Cómo continuar esta conversación en la computadora del laboratorio

1. Clona o actualiza el repositorio en tu computadora del laboratorio:
   ```bash
   git clone git@github.com:ponchogf88/captoora.git
   cd captoora
   git pull origin main
   ```
   *(Y en `proyectos/waters-3d-studio`, ejecuta `npm install` ya que `node_modules` está excluido en `.gitignore`. En la raíz crea `.env` con `ELEVENLABS_API_KEY=tu_clave`.)*
2. Abre un chat con tu agente en Antigravity sobre este repositorio y pega este prompt exacto:

```text
Lee completa la conversación respaldada en docs/conversaciones/2026-11-19_82fb8bb2_waters_serie_casting_remotion/README.md y CONVERSACION_DIALOGO_LITERAL.md, junto con proyectos/waters-serie/HANDOFF_CONVERSACION_2026-11-19.md y proyectos/waters-serie/casting_referencia/GALERIA_CASTING_WATERS.md. Confirma el estado de WATERS_HYBRID_EP01_GTA6_NEON_60S.mp4 y continuemos desde aquí con: (1) el nuevo guion del episodio SIN decir "Chuy" donde Agy le quita el control mientras juega GTA 6, usando "¡Waters!" al inicio y como firma final ("¡Waters! Toma tus precauciones... ¡Waters!"), y (2) nuevas pruebas de texturas de ambos personajes en pareja más allá de la plastilina (Fieltro/Lana, Vinilo Designer Toy, Cine 3D tipo Pixar y 2D Tinta estilo Spider-Verse).
```

---

## 📂 Qué incluye esta carpeta

| Archivo | Descripción | Cuándo consultarlo |
| --- | --- | --- |
| [`README.md`](./README.md) | Este mapa maestro, estado del render 60s, pendientes inmediatos y prompt de relevo para laboratorio. | Leer primero al retomar en otra computadora. |
| [`CONVERSACION_DIALOGO_LITERAL.md`](./CONVERSACION_DIALOGO_LITERAL.md) | Transcripción cronológica **100% literal** de los `138` turnos del usuario y `137` respuestas visibles del agente. | Para leer toda la charla de punta a punta sin ruido técnico. |
| [`CONVERSACION_BITACORA_TECNICA_COMPLETA.md`](./CONVERSACION_BITACORA_TECNICA_COMPLETA.md) | Bitácora cronológica de los `1,577` eventos con llamadas a herramientas, comandos y extractos de salida. | Para auditar comandos, scripts o renders ejecutados. |
| [`raw/transcript_full.jsonl`](./raw/transcript_full.jsonl) | Log JSONL completo oficial de Antigravity (sanitizado contra secretos/tokens). | Respaldo forense completo sin truncar. |
| [`raw/transcript.jsonl`](./raw/transcript.jsonl) | Log JSONL compacto oficial de Antigravity (sanitizado). | Índice estructural nativo de Antigravity. |

---

## ✅ Estado de Entregables Listos en el Repositorio

### 1. Video Extendido >60s Compatible con QuickTime / OpusClip / Captions
- **Archivo principal:** `proyectos/waters-serie/renders/WATERS_HYBRID_EP01_GTA6_NEON_60S.mp4`
- **Especificaciones técnicas verificadas (`ffprobe`):** `74.87s`, `1080x1920`, `30fps`, `h264`, `yuv420p` (`tv` limited range, `bt709`), audio AAC, sin traslapes de diálogo y zona inferior limpia para subtítulos automáticos de **OpusClip** / **Captions**.
- **Nota técnica clave:** Todo render futuro debe exportarse desde Remotion/FFmpeg con `-vf "scale=in_range=full:out_range=limited,format=yuv420p" -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -movflags +faststart` para evitar `yuvj420p` y asegurar compatibilidad con QuickTime y móviles.

### 2. Casting de Voces (`ElevenLabs eleven_v3` — Expressive Mode)
- **Protagonista masculino:** `Antonio - Confident, Gentle and Clear` (`voice_id: htFfPSZGJwjBv1CL0aMD`)
- **Agy (voz femenina inspirada en `liken.IA`):** `Liza - Natural Mexican Creator` (`voice_id: kl7d390GatBPfqhRTyAl`)
- Muestras y comparativo HTML guardados en `proyectos/waters-serie/renders/casting_voces/`.
- Generador modular del episodio en `proyectos/waters-serie/scripts/generar_ep01_ext.py`.

### 3. Casting Visual, Poses Base y Estudio Remotion 3D
- **Galería de referencia:** `proyectos/waters-serie/casting_referencia/GALERIA_CASTING_WATERS.md` + archivos `.jpg` de estilos (Plastilina, Pixar 3D, Vinilo Designer Toy, Fieltro/Lana, 2D Tinta en 3D, LEGO, Cyber-Regio).
- **Proyecto Remotion 3D/Híbrido:** `proyectos/waters-3d-studio/` (`src/Root.tsx`, `src/episodeBeats.json`, `public/clips/`).
- **Hub y planificación 30 días:** `proyectos/waters-serie/index.html`, `CALENDARIO_MAESTRO_30_DIAS_WATERS.md`, `100_SITUACIONES_WATERS.csv`, `HANDOFF_CONVERSACION_2026-11-19.md` y `HANDOFF_PARA_MACBOOK_YOUTUBE_CHANNEL.md`.

---

## 🔧 Pendientes Inmediatos al Retomar

### 1. Nuevo Guion de EP01 SIN decir «Chuy» + Firma «¡Waters!»
Ajustar el guion y volver a sintetizar voces/render para que:
1. **Arranque (0–4s):** El avatar está jugando **GTA 6** normalmente, confiado y sin sospechar nada.
2. **Interrupción (4–11s):** Llega el otro personaje (Agy / el monito), **le quita el control remoto** de las manos y le dice:
   > *"¡Waters! ¿Qué, vas a jugar GTA seis sin tomar tus controles de seguridad?"*
3. **Reacción sorprendida (11–15s):**
   > *"¿Por qué? ¡Si ya tengo mi contraseña!"*
4. **Explicación con datos reales:**
   > *"¡Ay, no puede ser! Mira, te explico..."* — impacto viral de GTA 6 (9.8M vistas en horas, +$1,000M en preventa, $3,000M estimados antes de fin de año), ataques con Vibe Hacking y blindaje con Gemini 4 Neon.
5. **Firma oficial de cierre:**
   > *"¡Waters! Toma tus precauciones... ¡Waters!"*

### 2. Explorar Nuevas Texturas de Personajes en Pareja (Más allá de la plastilina)
Generar pruebas visuales consistentes con **ambos personajes juntos** en distintos acabados y texturas:
- **Fieltro y Lana Stop-Motion**
- **Designer Toy / Vinilo Mate**
- **Cine 3D estilo Pixar**
- **2D Tinta + Semitono tipo Spider-Verse**
