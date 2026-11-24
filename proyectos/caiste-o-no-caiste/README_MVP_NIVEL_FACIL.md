# `¿Caíste o no caíste?` — Biblia MVP Nivel Fácil (`Semper Ascendens`)

> **Origen consolidado:** Basado en la arquitectura definida en `ponchogf88/soul-youtube` (`CAISTE_O_NO_CAISTE/`, commit `01cc610`) y refinado en nuestra fábrica local de Captoora Studio para ejecutar **1 piloto medible primero** en lugar de publicar 34 videos a ciegas en un solo día.
>
> **Clasificación inicial obligatoria (Regla Anti-Humo):** **`🧪 EN PRUEBA / HIPÓTESIS`**. Se mide retención, comentarios CTA y compartidos en familia antes de escalar los niveles Medio, Difícil y la compilación de 30 minutos.

---

## 1. Concepto, Misión y Ruta Ascendente

- **Canal / Formato:** `¿Caíste o no caíste?` — quiz interactivo de ciberseguridad cotidiana para jugar en familia (niños, papás y abuelos) en español mexicano directo y humano.
- **Metáfora visual (*Semper Ascendens* — al revés de Duolingo):** En lugar de bajar o perder corazones sin rumbo, la ruta **siempre sube por rieles de tren (`Guardrails`)**:
  - La IA va desbocada y sin camino; **`Antigravity "Guardrails"`** (con casco y arnés de seguridad) coloca los **rieles** para que la tecnología avance sin que te estafen.
  - Cada pregunta bien contestada es un escalón hacia arriba sobre los rieles.

---

## 2. Los 5 Candados de Diseño del MVP

| # | Decisión MVP | Por qué lo ajustamos respecto al borrador inicial |
| --- | --- | --- |
| **1** | **Elenco unificado en 3D voxel pastel mate cálido (`CERO NEÓN`)** | **`Antigravity "Guardrails"`** (Guía con casco/arnés sobre rieles) + **`ChatGPT`** (Nivel Fácil, cubo menta/blanco) + **`Claude`** (Nivel Medio, cubo naranja terracota) + **`Grok`** (Nivel Difícil, cubo carbón/ciruela rebelde con lentes oscuros). |
| **2** | **Tiempos ágiles: `5 s` / `7 s` / `9 s`** | En el borrador original eran `5 / 10 / 15 s`. En YouTube y Shorts, `10–15 s` mudos se sienten eternos y matan la retención. **`5 s` (Fácil), `7 s` (Medio), `9 s` (Difícil)** mantienen tensión real. |
| **3** | **Balance `70 / 30` anti-trampa (`7 TRAMPAS + 3 REALES`)** | En `guiones.md` original las 10 preguntas eran trampa (`10/10`), así que desde la #3 el espectador adivinaba sin pensar. Al meter **3 avisos REALES legítimos**, la familia duda de verdad antes de gritar *"¡Trampa!"*. |
| **4** | **Tip Humano: `"El Segundo Robado"` (esporádico)** | Solo en **2 preguntas** estratégicas (nunca en la #1; aquí en **P4 CFE** y **P8 DHL**), el reloj anuncia `5 s` pero cuenta **`5 → 4 → 3 → 1 → ¡TIEMPO!`** (`4 s` reales) con un micro-guiño travieso de `Grok`. Provoca *rewatch*, discusión familiar en casa y comentarios orgánicos (*"¡Me robaste 1 segundo en la 4!"*). Al cierre, `Antigravity` conecta esa sensación con la **prisa artificial** del phishing real. |
| **5** | **FinOps y Stack Local ($0 extra en herramientas redundantes)** | Se edita y corta con nuestro stack real (**`HyperFrames` / `Remotion` + `waters_audio_engine.py` + `FFmpeg` + `CapCut Pro` $30 MXN**), sin pagar `Opus Clip` ni la app `Captions`. Arrancamos con **1 Video Largo Piloto (Nivel Fácil, ~9–10 min)** + **3 Shorts derivados** en lugar de saturar 34 subidas el día 1. |

---

## 3. Activos Visuales del Universo (`3D Low-Poly Voxel Pastel Mate · Cero Neón`)

- **Personajes (`assets/personajes/`):**
  - `guardrails_antigravity` — Guía principal con casco amarillo pastel y arnés junto a los rieles ascendentes.
  - `chatgpt_facil` — Nivel Fácil (`5 s`): cubo verde menta pastel amigable con lentecitos.
  - `claude_medio` — Nivel Medio (`7 s`): cubo naranja terracota cuidadoso con libreta/corbata.
  - `grok_dificil` — Nivel Difícil (`9 s`): cubo carbón/ciruela rebelde con lentes oscuros y cronómetro retro.
- **Escenarios (`assets/escenarios/`):**
  - `escenario_01_facil_casa` — Calle soleada de barrio mexicano con panadería, casa pastel y rieles subiendo.
  - `escenario_02_medio_oficina` — Plaza de oficina y banco con rieles ascendiendo más alto.
  - `escenario_03_dificil_cima_rieles` — Cima al atardecer con sala de servidores voxel y luz cálida ámbar (**cero neón**).
- **Motor local (`Three.js` + Chrome Headless):** los 7 activos 3D se generaron localmente con `voxel_studio.html` y `render_voxel_assets.py` (rig reutilizable para animar los episodios sin costo API).

---

## 4. Estructura de Ritmo por Pregunta (45–55 s c/u)

1. **Caso en pantalla (`~12–15 s`):** `ChatGPT` lee el mensaje exacto que llegó al celular mientras aparece la tarjeta del caso.
2. **Contador (`5 s` normales / `4 s` en P4 y P8):** número grande en centro + reloj tic-tac. En P4 y P8 salta `5 → 4 → 3 → 1 → ¡TIEMPO!` con guiño de `Grok`.
3. **Revelación + 3 pistas (`~20 s`):** **`TRAMPA`** o **`REAL`** + 3 señales concretas que cualquier persona puede detectar en segundos.
4. **Guardrail (`~5–8 s`):** `Antigravity` pone el riel con 1 regla accionable de bolsillo.

---

## 5. Criterio de Validación (Filtro 3 — Calle Real)

Publicar **Piloto 1 (Nivel Fácil horizontal)** + **3 Shorts (`P2`, `P4`, `P8`)** en TikTok / YouTube Shorts / Reels y medir a las 72 h:
- ¿Sube la retención y el número de comentarios frente a la línea base (`72–121` vistas)?
- ¿La gente comenta su marcador (`CAÍ` / `NO CAÍ` / reclamo por el segundo robado en la 4 y la 8)?
- **Solo si supera la prueba de mercado**, producimos Nivel Medio (`Claude 7s`), Nivel Difícil (`Grok 9s`) y la Compilación de 30 min.
