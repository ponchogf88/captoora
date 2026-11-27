# Reglas Obligatorias de Producción Híbrida (`¡WATERS!` / Captoora)

Estas reglas rigen **todos** los videos con avatar humano + Motion UI / Toy-Prop 3D a partir de hoy:

1. **1 escena / frase = 1 clip real independiente con lip-sync**
   - Queda estrictamente prohibido reciclar un solo clip mudo en `<Loop>` debajo de una pista de audio completa.
   - Cada escena (`5–8 s`) debe provenir de su propio clip donde el personaje pronuncie exactamente su frase correspondiente, usando el audio original limpio de ese clip (nunca desfasado).

2. **Variación obligatoria de ángulo y encuadre entre escenas**
   - Ningún par de escenas consecutivas debe repetir el mismo ángulo fijo de cámara:
     - **Escena 1 (Hook)**: Close-Up frontal urgente mirando directo a lente.
     - **Escena 2 (Problema / Cajita IA)**: Plano 3/4 mirando ligeramente hacia la derecha (`screen-right`) donde aparece la UI de Gemini/Claude/ChatGPT.
     - **Escena 3 (Evidencia / Gráfica)**: Plano medio abierto o contrapicado suave con espacio para gráfica y flechas animadas.
     - **Escena 4 (Dilema 3D)**: Encuadre 3/4 contrario (izquierda) dentro de tarjeta PiP mientras corre `BinaryDoors3D` con cámara orbital.
     - **Escena 5 (Checklist / Pasos)**: Plano pecho (`chest-up`) contando 1-2-3 con la mano en PiP sobre `GiantClipboard3D`.
     - **Escena 6 (CTA Final)**: Close-Up limpio a la altura de ojos (`eye-level`) rematando la palabra clave.

3. **Doble entrega obligatoria en cada producción**
   - **Carpeta `escenas/`**: cada escena renderizada como MP4 independiente (`01_*.mp4`, `02_*.mp4`, ..., `06_*.mp4`) con su audio real + SFX ya mezclados, para poder revisar o regenerar solo 1 escena (`--scene N`) sin rehacer el video entero.
   - **Master unido (`*_COMPLETO_UNIDO.mp4`)**: ensamblado final de todas las escenas aprobadas vía `ffmpeg` `concat` listo para publicar o meter en OpusClip.

4. **Master limpio para OpusClip + Captions**
   - Formato `1920×1080` (`16:9`), `30 fps`, `yuv420p`, `bt709`.
   - Dejar los últimos `220 px` inferiores libres de subtítulos quemados para evitar colisión con los subtítulos de OpusClip y Captions.
