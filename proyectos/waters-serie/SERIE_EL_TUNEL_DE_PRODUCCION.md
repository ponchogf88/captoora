# Serie 1: El Túnel de Producción (`A → E`) — `Antigravity` le explica a `Claude`

> **Propósito:** Desarmar la "caja negra" de cómo fabricamos videos en Captoora Studio / `¡WATERS!`. Nada de teoría abstracta ni relleno: cada episodio muestra **en pantalla** qué archivo entra, por qué un solo repo mágico no alcanza, qué hace el siguiente repositorio que el anterior **no sabe hacer**, y qué sale físicamente al final de ese brinco.

---

## 1. Formato y Reparto Oficial (100% Avatares + Voces — Cero Cámara Humana)

Esta serie opera **100% sin humanos frente a cámara**: cero preocupaciones de acentos, iluminación personal, muletillas o penas. Toda la dinámica recae en el choque práctico entre nuestros dos personajes 3D/animados con voces separadas:

| Personaje | Rol en la serie | Personalidad y frase guía | Qué aporta al espectador |
| --- | --- | --- | --- |
| **`Antigravity (AGY)`** | **El monito ingeniero / Mentor** | Práctico, directo, cero humo y alergia total a discutir por discutir. *"Yo no discuto: configuro, armo, construyo, desarrollo y arreglo."* | Abre el editor/terminal en pantalla, enseña el archivo real y demuestra qué entra y qué sale en cada brinco. |
| **`Claude (Klaus)`** | **El aprendiz curioso y escéptico** | Hace las preguntas incómodas sin filtro (*"¿WTF por qué saltas de A a B en lugar de usar una sola app?"*). **Aprende paso a paso de Antigravity.** | Representa al dueño de negocio o creador que ve 16 repos en X y solo quiere entender para qué sirve cada uno en su compu. |

- **Regla visual de producción (5 Capas Limpias):** personajes en escena 3D (`Remotion` + `Three.js`) o tarjetas/terminal en HTML (`HyperFrames`), pantalla dividida **Antes → Proceso → Después**, audio maestro generado por pista (`waters_audio_engine.py` + ElevenLabs) y franja inferior libre (`260 px` abajo) sin subtítulos quemados.

> **Credo Operativo de la Fábrica (`Antigravity`):** *"I don't discuss. I configure, I set up, I build, I develop, I create, I fix. I document, I register, I RECORD, I learn from mistakes, I iterate, I dream."*

---

## 2. El Mapa Visual del Túnel (`A → B → C → D → E`)

Piénsalo como el estudio físico en Colinas de San Jerónimo (`Av. Paseo de los Álamos 165`): la **cámara** no graba bien el audio de lejos, el **micrófono** no toma fotos, y el **revelado/prensa final** no ilumina el set. Cada herramienta hace una sola chamba porque la anterior **no sabe hacerla**:

```text
[A] Guion y Beats (.py / .md / JSON)
      │  ¿Por qué brinco? El texto NO tiene reloj ni duración real hablada.
      ▼
[B] Voz y Audio por Pista (waters_audio_engine.py + ElevenLabs)
      │  ¿Por qué brinco? Ya tenemos reloj exacto en segundos (.wav), pero pantalla negra.
      ▼
[C] Visual Base Limpio (2 carriles según lo que toque mostrar):
    ├─ [C1] Escena 3D (Three.js arma el set + Remotion dispara 1,380 fotos JPEG)
    └─ [C2] UI / Código / Tarjetas (HyperFrames + GSAP en HTML hecho video)
      │  ¿Por qué brinco? Sale SIN subtítulos pegados (260 px libres abajo) para poder editar texto sin rehacer el 3D.
      ▼
[D] Mica Transparente de Subtítulos (WhisperX + JSON/SRT externo)
      │  ¿Por qué brinco? Tenemos piezas sueltas en carpetas (1,380 fotos + .wav + subtítulos).
      ▼
[E] Empacadora Final (FFmpeg + ffprobe) ──► MP4 nítido (yuv420p / bt709 / +faststart) listo para Reels
```

*(Referencia completa de hardware y herramientas instaladas en [INVENTARIO_ARSENAL_Y_PIPELINE_PRODUCCION.md](INVENTARIO_ARSENAL_Y_PIPELINE_PRODUCCION.md).)*

---

## 3. Los 6 Episodios Registrados (`TUNEL-00` a `TUNEL-05`)

| ID | Salto | Título / Gancho (`Antigravity` ↔ `Claude`) | Qué entra y qué sale en video (con evidencia real del repo) | Estado | CTA |
| --- | --- | --- | --- | --- | --- |
| **`TUNEL-00`** | Mapa completo | *"Antigravity le explica a Claude por qué NO existe un solo repo mágico para hacer videos (fábrica por piezas vs bloque de cemento)"* | Contrastar un video "bloque sólido imposible de corregir" vs nuestras 5 piezas intercambiables tipo Lego. | `idea` | `TUNEL` |
| **`TUNEL-01`** | **`A → B`** | *"De Texto a Audio: Antigravity le enseña a Claude por qué animar antes de grabar la voz mata el video"* | Entra texto mudo (`scripts/generar_ep08_agente_contable_sat.py`) → pasa por `waters_audio_engine.py` + ElevenLabs → sale `MAD08_master.wav` (`46.0 s` de audio con pantalla negra y reloj exacto de cada frase). | **`guion` (Piloto listo abajo)** | `TUNEL` |
| **`TUNEL-02`** | **`B → C1`** | *"Por qué hacen falta DOS repos para el 3D: `Three.js` arma el set y `Remotion` dispara `1,380` fotos"* | Demostrar por qué `Three.js` dibuja el cuarto/personajes pero **no sabe exportar MP4**, y `Remotion` actúa como cámara en ráfaga (`WatersMad08` en `scripts/render_mad08_final.py` -> `1,380` frames `element-0001.jpeg` a `30 fps`), corriendo en iMac de `2 GB` VRAM sin Blender Cycles pesado. | `idea` | `TUNEL` |
| **`TUNEL-03`** | **`C1 ↔ C2`** | *"3D vs Página Web hecha video: cuándo Antigravity usa `Three.js + Remotion` y cuándo brinca a `HyperFrames + GSAP`"* | Split-screen: avatares y cámaras van en 3D (`C1`), mientras terminales, tarjetas editoriales y alertas van en HTML/CSS convertido a video (`HyperFrames` + `GSAP`) porque queda más nítido y rápido. | `idea` | `TUNEL` |
| **`TUNEL-04`** | **`C → D`** | *"Por qué Antigravity NUNCA quema subtítulos en el 3D (el truco de los `260 px` libres + `WhisperX`)"* | Enseñar el costo real: quemar texto dentro de `1,380` fotos obliga a re-renderizar todo por una falta de ortografía; con la franja de `260 px` libres + `WhisperX` palabra por palabra cambias la mica transparente aparte. | `idea` | `TUNEL` |
| **`TUNEL-05`** | **`D → E` + Seg.** | *"Cómo `FFmpeg` convierte `1,380` fotos mudas + 1 WAV en un MP4 listo para Reels en segundos (y por qué NO bajo 16 repos por hype sin auditar)"* | Flags reales de `scripts/render_mad08_final.py` (`yuv420p`, `bt709`, `color_range tv`, `-crf 18`, `-movflags +faststart`, `-c:a aac -b:a 192k`) + puente al checklist de ciberseguridad antes de clonar repos de moda. | `idea` | `TUNEL` |

---

## 4. Guion Piloto Completo Listo para Producción: `TUNEL-01 (A → B)`

- **Título:** *"De Texto a Audio: ¿WTF por qué no paso mi guion directo a video?"*
- **Duración objetivo:** `~45–50 segundos` (`30 fps`, zona inferior `260 px` totalmente limpia).
- **Reparto:** `Claude (Klaus)` aprende de `Antigravity (AGY)`.
- **Archivos reales mostrados en pantalla:** `scripts/generar_ep08_agente_contable_sat.py`, `scripts/waters_audio_engine.py`, `MAD08_master.wav`.

| Beat | Tiempo aprox. | Hablante | Diálogo exacto (para voz / audio engine) | Qué se ve en pantalla (Escena 3D + UI) |
| --- | --- | --- | --- | --- |
| **B1 · Hook** | `00.0 – 04.5 s` | `claude` | *"Oye Antigravity… wtf, ¿por qué tenemos que pasar mi guion primero a otro programa de audio en vez de aventarlo directo a video?!"* | Plano `3/4` escritorio 3D. Claude con hoja de texto flotante y cara de desesperado frente a dos repos abiertos. |
| **B2 · Respuesta seca** | `04.5 – 09.0 s` | `antigravity` | *"Mira Klaus: porque el texto está mudo. En papel tú crees que una frase dura tres segundos… y hablada dura seis."* | Contraplano hacia Antigravity con gafas/visor técnico. Arrastra una frase de `generar_ep08_agente_contable_sat.py` al visor. |
| **B3 · Demostración de desfase** | `09.0 – 16.0 s` | `antigravity` | *"Si animas las cámaras antes de grabar la voz, cuando metes la locución todo queda fuera de tiempo, como película mal doblada."* | Pantalla dividida: animación rápida terminando en `3.0 s` mientras la barra de voz sigue hablando hasta `6.1 s` (sello rojo `DESFASADO`). |
| **B4 · Qué entra en A** | `16.0 – 22.0 s` | `claude` | *"A ver… entonces en la estación A solo entra texto plano, cero imagen y cero sonido todavía, ¿correcto?"* | Zoom al bloque `"Anthropic presentó agentes..."` en texto limpio. Sin ondas ni frames todavía. |
| **B5 · Qué hace B** | `22.0 – 31.5 s` | `antigravity` | *"Exacto. En B entran tus diálogos a nuestro motor de Python con ElevenLabs: genera cada voz por separado, mete silencios y marca el reloj exacto."* | Aparece `waters_audio_engine.py` compilando clips individuales (`01_tony`, `02_agy`) en una línea de tiempo milimétrica. |
| **B6 · Qué sale en video** | `31.5 – 38.0 s` | `claude` | *"Órale… o sea que al salir de B le doy play al archivo y todavía la pantalla está negra, ¿pero ya manda el reloj de todo el video?"* | Monitor 3D en negro puro con una onda de audio verde brillante marcando `46.0 s` (`MAD08_master.wav`). |
| **B7 · Cierre de ingeniero** | `38.0 – 44.5 s` | `antigravity` | *"Justo eso. Yo no discuto con herramientas: configuro, armo y fijo el metrónomo primero. Ya con el reloj listo brincamos al 3D."* | Antigravity bloquea el timeline con un candado luminoso verde (`CLOCK LOCKED · 46.0s`). |
| **B8 · Puente + CTA** | `44.5 – 49.0 s` | `claude` / `antigravity` | **Claude:** *"Va, ya entendí A → B. ¿Y ahora por qué ocupamos DOS repos en C?"* / **AGY:** *"Comenta **TUNEL** y te aviso cuando salga B → C."* | Vista amplia de ambos avatares mirando la compuerta iluminada **`B → C`**. Franja inferior `260 px` limpia. |

### Checklist rápido para producir `TUNEL-01` por capas
1. **Capa 1 (Texto):** ajustar tiempos o diálogos en la tabla superior si cambia alguna frase.
2. **Capa 2 (Audio):** compilar pistas separadas `B1..B8` con `waters_audio_engine.py` para fijar el maestro `.wav`.
3. **Capa 3 (Visual Limpio):** renderizar escena 3D + pantalla dividida en `waters-3d-studio` (`Remotion` + `Three.js`) dejando `260 px` libres abajo (`_clean.mp4`).
4. **Capa 4 y 5 (Subtítulos + Mux):** alinear palabras sobre el `.wav` y empacar con `FFmpeg` sin volver a tocar el render 3D.
