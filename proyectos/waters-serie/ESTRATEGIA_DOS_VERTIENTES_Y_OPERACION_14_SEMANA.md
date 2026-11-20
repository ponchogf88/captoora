# Estrategia Oficial de Contenido en Dos Vertientes, Operación 14/Semana y FinOps — ¡WATERS! Studio

> Documento rector del canal **¡WATERS! / Soy Chuy · Astronautita Chispa 3D** (`proyectos/waters-serie` + `proyectos/waters-3d-studio`).  
> Complementa y ordena la ejecución semanal sobre los archivos históricos sin borrar activos previos (*Zero Delete Policy*).

---

## 1. Dos Vertientes Oficiales del Canal

El canal opera bajo **dos personalidades complementarias** protagonizadas por **Astronautita Chispa 3D**. Publicar ambas en horarios distintos permite atacar dos hábitos de consumo diferentes (alerta informativa de mediodía vs. narrativa cinematográfica nocturna) sin canibalizar la audiencia.

| Eje | Vertiente A — **☀️ Día: `¡WATERS!` (Noticias, Alertas y Prevención)** | Vertiente B — **🌙 Noche / Madrugada: `Historias de Madrugada` (estilo `vibecoder_es`)** |
| :--- | :--- | :--- |
| **Horario objetivo (MX)** | **12:00 hrs** | **22:00 hrs** |
| **Objetivo algorítmico** | Alcance por coyuntura, guardados por utilidad, captación directa de leads con PDF. | Retención extrema (*open loop*), *replays*, compartidos por identificación emocional (*"me pasó ayer"*). |
| **Segundo 0 (Gancho)** | Energía arriba desde el primer fotograma con gancho **`"¡Waters!"`** (audio en inglés `en`). | **Cero grito inicial.** *Cold Open* atmosférico y tenue: lluvia 3D tras la ventana, cuarto oscuro iluminado por el monitor, voz baja/confidencial en suspenso (*"Mañana tengo que pagar la renta y me quedan 20 pesos..."*). |
| **Estructura y duración** | 55–95 s. Titular viral → 3 riesgos/datos concretos → blindaje práctico → CTA con palabra clave. | 45–55 s. Planteamiento íntimo → escalada con cortes rápidos multi-cámara → silencio seco en remate → **desenlace alternado**. |
| **Fuentes temáticas** | Noticias frescas (resúmenes tipo Jacobo Wong, hackeos MX, IPO/bolsa, SAT, brechas, deepfakes de voz). | Vivencias reales con IA, errores de *vibe coding*, saturación de cuota, permisos peligrosos, dilemas de madrugada. |
| **Ubicación del CTA** | Explícito dentro del cierre del video + entrega de guía PDF descargable. | **Nunca rompe la historia dentro del video** en los finales crudos; el CTA vive en el **caption** (*"Si no quieres que te pase esto, mándame mensaje / comenta..."*). |

### Desenlaces alternados en Vertiente B (Impredecibilidad tipo *Black Mirror*)

Para que la audiencia jamás adivine el final y se quede hasta el último cuadro, la Vertiente B alterna dos cierres:

1. **Final Crudo (sin final feliz):**
   - Comedia negra realista donde la decisión irresponsable con la IA cobra factura real.
   - **Cierre:** corte seco a negro + efecto sonoro diegético real (notificación bancaria, *"El cliente abandonó la reunión"*, *"Cuota agotada hasta dentro de 5 días"*, alerta de Buzón Tributario).
   - Cero discurso comercial en pantalla. En el **caption** y comentario fijado: salida técnica y oferta de blindaje por DM.
2. **Final Rescate (Angelito `Antigravity`):**
   - Cuando el protagonista activa candados a tiempo y entra **Chispa / Antigravity** con superpoderes técnicos reales (**Plan Mode**, **Sandbox**, **Model Routing Flash/Pro**, **Diff Review**), rescatando el entregable en el último segundo.

### Regla editorial y de marca (Parodia inteligente sin riesgo)

- **Nunca se plantea como difamación ni acusación contra una empresa real.** El antagonista cómico en los sketches representa al **Agente Sin Candados / Modo Barato `$1` / Bot Pirata** (el equivalente narrativo del diablito que ejecuta a ciegas, halaga sin verificar o expone credenciales).
- **El héroe técnico es `Antigravity` + Chispa** operando controles de ingeniería reales.
- **Beneficio doble:** posiciona de forma orgánica los términos **`Antigravity`**, **`Vibe Coding`**, **`Tokens`** y **`AI Agents`** en el algoritmo de Instagram Reels, YouTube Shorts y TikTok, mientras construye portafolio vivo de arquitectura y ciberseguridad para entrevistas técnicas.

---

## 2. Motor 3D v2 — Cinematografía Multi-Cámara en 9:16 (`proyectos/waters-3d-studio`)

La versión v1 demostró que el personaje 3D conecta con la audiencia, pero mantuvo cámara fija frontal (`[0, 1.50, 10.15]`) y HUD superior constante. Para lograr acabado cinematográfico en la Vertiente B sin salir de Remotion + Three.js:

1. **Propiedad `cameraShot` por beat (planos cinematográficos reales):**
   - `wide_front`: plano general frontal (establecimiento o respiro).
   - `ots_chispa`: plano sobre el hombro (*Over-the-Shoulder*) de Chispa viendo hacia el monitor o hacia el bot antagonista.
   - `low_villain`: contrapicado desde abajo con luz roja y lente cerrada hacia el bot sin candados.
   - `closeup_face`: primer plano / *crash-zoom* directo al visor de Chispa en el instante del remate o shock.
   - `dutch_panic`: plano holandés inclinado (`±8°`–`12°`) al dispararse la crisis (cuota al 99%, borrado en producción, caída de cliente).
   - `top_desk`: picado a `45°` sobre el escritorio mostrando la laptop/web rota.
   - `side_3q_left` / `side_3q_right`: cámara lateral en ángulo `3/4` (nunca frontal estática), inspirada en la referencia `@daybi_ai` (*"Claude Aguantaaa"*): encuadre cerrado al personaje con fondo nocturno azul, partículas flotantes y letrero neón desenfocado detrás (ej. `captoora.studio` en *bokeh*).
   - `orbit_hero`: barrido orbital curvo cuando entra **Antigravity** al rescate y la iluminación pasa de rojo caos a esmeralda/cian.
2. **Movimiento continuo obligatorio (cero planos muertos):**
   - Ninguna escena se queda fija en tripié: cada beat combina ángulo lateral (`3/4` o perfil) con **zoom progresivo lento (`slow_push_in` / `dolly_zoom`)** o paneo sutil continuo para mantener dinamismo visual.
3. **Escenario 3D con profundidad espacial:**
   - Escritorio, monitor diegético con interfaz renderizada **dentro** del mundo 3D, ventana trasera con lluvia animada, partículas flotantes, letrero neón en *depth-of-field* y contraste dual de iluminación (luz fría de fondo + luz cálida lateral al frente) para que cada ángulo revele volumen real.
4. **Respiración visual (HUD inteligente):**
   - Durante las escenas dramáticas (2–4 s), **apagar la tarjeta HUD fija superior** para que la animación 3D respire como cortometraje puro; reservar las tarjetas para síntesis de datos o remates técnicos.
5. **Diseño sonoro de thriller + comedia:**
   - Lluvia ambiente continua + pulso subgrave de tensión + tic-tac sutil que **corta a silencio seco (`0.3 s`)** justo antes de la frase remate (*punchline*).
6. **Referencias visuales registradas:**
   - `@vibecoder_es` (ritmo de comedia-suspenso con modelos de IA).
   - `@daybi_ai` (*"Claude Aguantaaa"*, captura en sesión): encuadre `3/4` lateral cerrado + letrero neón desenfocado al fondo + partículas nocturnas sin banners superiores.
   - Reel de referencia de cámara lateral con zoom continuo: `https://www.instagram.com/reel/Df8WJlYRy21/` *(acceso público bloqueado por login de Instagram; guardar clip/captura en `referencias/inbox/` para desglose cuadro a cuadro)*.
   - Reel de referencia de atmósfera íntima (`https://www.instagram.com/reels/DedIkqJla4G/`): sonido suave de fondo, susurros cercanos (tono íntimo/ASMR), zooms dinámicos, variedad de encuadres y fondos con profundidad *(depositar clip o grabación de pantalla en `referencias/inbox/` para estudio cuadro a cuadro)*.

---

## 3. Cadencia Operativa: 2 Videos/Día (14/Semana) + Colchón de 7 Días

- **Meta semanal:** `14 publicaciones` = **7 slots Día** (Vertiente A, `12:00 hrs MX`) + **7 slots Noche** (Vertiente B, `22:00 hrs MX`).
- **Colchón obligatorio de 7 días:** nunca operar al día. Siempre debe existir al menos 1 semana completa adelantada entre piezas listas/programadas y el backlog.
- **Ritual Dominical (una sola sesión por semana):**
  1. Revisar el tablero semanal de 14 espacios.
  2. Ajustar el orden de lunes a domingo según coyuntura.
  3. Programar los **14 posts de la semana** en bloque para operar con calma de lunes a sábado.
- **Protocolo *Breaking News* (Arrastra y Suelta entre semana):**
  1. Cuando estalla una noticia urgente en la semana (ej. nuevo hackeo, caída de modelo, alerta SAT), la noticia nueva se produce como **Vertiente A** y se arrastra directamente al slot `☀️ Día` de hoy o mañana.
  2. La tarjeta *evergreen* que ocupaba ese slot **se desliza a otro día libre** o regresa al `Backlog` sin desordenar ni romper la racha de 14/semana.

---

## 4. Arquitectura del Tablero Drag-and-Drop (Esquema Desacoplado)

> **Estado de la interfaz:** **ACTIVA** en [`tablero_calendario_waters.html`](file:///Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie/tablero_calendario_waters.html) — replicada fielmente de `ponchogf88/cv-card-board` (mesa verde de estudio, cartas crema con animación hover tipo Opus Clip, arrastre Pointer Events con intercambio automático de slots, modales `<dialog>` nativos, filtros por vertiente, tray dominical `0/14`, guardado en `localStorage` y exportación/importación JSON).

Mientras tanto, la estructura de datos oficial ya queda viva en [`tablero_semanal_14_slots.json`](file:///Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie/tablero_semanal_14_slots.json):

- **Columnas del tablero:**
  - `Backlog` (reserva de noticias *evergreen* e historias listas para intercambiar).
  - `Lunes`, `Martes`, `Miércoles`, `Jueves`, `Viernes`, `Sábado`, `Domingo`.
- **Carriles por día (2 filas por columna):**
  - `☀️ Día · ¡WATERS! (12:00 MX)`
  - `🌙 Noche · Madrugada (22:00 MX)`
- **Estados oficiales por tarjeta:**
  `idea` → `guion` → `audio` → `render_3d` → `listo_publicar` → `programado` → `publicado` *(más `revision_final` para renders heredados de versiones previas pendientes de control de calidad).*

---

## 5. Manual Operativo de AI FinOps y Gobernanza de Cuota (Producción + Entrevistas)

### Reglas diarias para no quemar la cuota
1. **Higiene de contexto (`1 entregable = 1 chat nuevo`):** cada turno reenvía el historial acumulado del chat. Saludar o pedir ajustes menores en el turno 60 de una conversación con imágenes y PDFs cuesta órdenes de magnitud más que un chat fresco. Usa **`/compact`** si necesitas continuar dentro del mismo hilo o abre conversación nueva al cerrar episodio.
2. **Brief Spec-First en un solo disparo:** entregar objetivo, rutas exactas con `@archivo`/`@carpeta`, restricciones (qué no tocar) y criterio de verificación desde el primer mensaje. Evitar cháchara conversacional innecesaria cuando el agente solo necesita ejecutar.
3. **Aprobación previa a APIs de pago:** en producción audiovisual, aprobar siempre guion y tiempos **antes** de disparar ElevenLabs o renders pesados 3D.
4. **Arquitectura *Progressive Disclosure* / Mapa de Carpetas (insight clave de `@luisdani.fg`):** *"El agente debe saber dónde está qué cosa, no tener cargado todo el contexto de una."* Mantener un índice liviano (`docs/MAPA_REPOSITORIO.md` + este documento + carpetas ordenadas `scripts/`, `renders/`, `lead_magnets/`, `referencias/`) para que cualquier chat nuevo consulte **solo el apartado exacto que necesita** en vez de leer todo el repositorio, reduciendo drásticamente el consumo de memoria/cuota.

### Matriz de Ruteo de Modelos (*Model Cascading*)

| Nivel | Motor / Modelo | Uso recomendado | Evitar para |
| :--- | :--- | :--- | :--- |
| **Nivel 0 (0 tokens)** | Scripts locales (Python, Bash, FFmpeg, `rg`, `json.tool`) | Búsquedas exactas, generación masiva de PDFs (`generar_guias_ep07_ep08_pdf.py`), mezcla de audio (`waters_audio_engine.py`), codificación MP4. | Tareas creativas o ambiguas. |
| **Nivel 1 (Ligero)** | Flash Lite / Modelos locales (Ollama, Gemma, Qwen) | Clasificar ideas, resumir noticias largas, redactar borradores de captions, etiquetado por lote. | Arquitectura o debugging complejo. |
| **Nivel 2 (Ejecución)** | **Gemini Flash** | Ejecutar planes aprobados, editar componentes bien acotados, crear scripts de audio/PDF bajo patrón existente, correr pruebas. | Diseño de sistema ambiguo desde cero. |
| **Nivel 3 (Razonamiento)** | **Gemini Pro / Plan Mode (`/plan`)** | Diseño arquitectónico, diagnóstico de bugs complejos, auditoría de seguridad/ciberseguridad y redacción del plan inicial. | Ajustes cosméticos de 1 línea o iteraciones mecánicas. |

### Guardrails de seguridad y alternativas éticas para carga profesional
- **En Antigravity 2.0:** `request-review` / sandbox en políticas de terminal, *Allowlist* de navegador y permisos de archivo acotados por proyecto para evitar que el agente "peine" directorios irrelevantes.
- **Para escala comercial sin tope de suscripción personal:** API Pay-as-you-go con **Budget Cap estricto** (alertas al 50% / 80% y corte al 100%), **Prompt Caching** para contexto fijo, **Batch API** para tareas asíncronas, y modelos locales (Ollama/LM Studio) para borradores y privacidad sin consumo en la nube.
- **En producción empresarial:** *AI Gateway* con cuotas por servicio/usuario, **Circuit Breakers** (máximo de reintentos antes de escalar a humano), RAG acotado (*top-k*) y métricas FinOps (**costo por tarea resuelta** y **tokens por PR**).

### Pitch de 30 segundos para entrevistas técnicas
> *"Opero agentes de IA como infraestructura cloud con presupuesto finito, no como un chat. Aplico tres capas: primero **Context Hygiene** — sesiones acotadas por entregable, briefs Spec-First con rutas explícitas y compactación de historial. Segundo **Model Routing / Cascading** — reservo modelos de razonamiento pesado solo para arquitectura y planeación, delego la ejecución a modelos rápidos como Flash y bajo todo lo determinista a scripts locales de costo cero. Tercero **Guardrails y FinOps** — sandbox de mínimo privilegio, circuit breakers contra bucles y límites estrictos de presupuesto para maximizar calidad por token."*

---

## 6. Inventario Listo para Publicar + Backlog Semilla Vertiente B

### Episodios 3D Verificados (Listos hoy — Vertiente A)

| Episodio | Tema | CTA | Video MP4 Verificado | Guía PDF Verificada |
| :--- | :--- | :--- | :--- | :--- |
| **EP06** | Hackeos MX + Clonación de voz con IA | `BLINDA` | `renders/WATERS_CHISPA_EP06_HACKEOS_Y_VOZ_60S.mp4` | `lead_magnets/GUIA_BLINDA_HACKEOS_Y_VOZ_CAPTOORA.pdf` |
| **EP07** | IPO Anthropic + Ashton Kutcher + 3 estafas Pre-IPO | `BOLSA` | `renders/WATERS_CHISPA_EP07_ANTHROPIC_IPO_60S.mp4` | `lead_magnets/GUIA_BOLSA_PREIPO_CAPTOORA.pdf` |
| **EP08** | Claude Contador vs. Riesgos `e.firma` SAT | `CONTADOR` | `renders/WATERS_CHISPA_EP08_CLAUDE_CONTADOR_SAT_60S.mp4` | `lead_magnets/GUIA_CONTADOR_IA_SAT_CAPTOORA.pdf` |

*(Además existen renders previos en `renders/` listos para revisión final y relleno de semana en `tablero_semanal_14_slots.json`.)*

### Backlog Semilla — Vertiente B (`Historias de Madrugada`)

| Código | Historia (Gancho de Madrugada) | Desenlace | Eje Técnico / FinOps |
| :--- | :--- | :--- | :--- |
| **MAD-01** | *"Mañana tengo que pagar la renta... le bajé el modelo a $1 para ahorrar cuota."* Bot barato halaga, entrega web rota (*"para eso alcanza con $1"*), sube a modelo grande y agota cuota con un `"hola"`. | **Final Crudo** (cliente abandona Zoom + corte seco a negro + lluvia) | Token FinOps / Model Routing (`CUOTA` en caption) |
| **MAD-02** | *"Le dije al agente: tú arréglalo como veas y me fui por café."* Bot sin sandbox "limpia" archivos de producción y prepara correo comprometedor. | **Rescate Antigravity** (`orbit_hero`, Sandbox + `request-review` + Diff Review) | Permisos de mínimo privilegio / Sandbox |
| **MAD-03** | *"Conseguí un bot que promete pagar $0 al SAT si le subo mi e.firma."* Diablito timbra/clasifica alucinaciones fiscales sobre su RFC a las 2 a.m. | **Final Crudo** (timbre de Buzón Tributario + pantalla en rojo + silencio) | Protección `.cer`/`.key` y Read-Only Copilot |
