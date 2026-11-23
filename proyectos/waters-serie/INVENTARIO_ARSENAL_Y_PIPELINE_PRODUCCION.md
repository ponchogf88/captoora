# Inventario Verificado de Arsenal, Pipeline Modular por Capas y Bóvedas de Reserva y Seguridad (`¡WATERS!` / Captoora Studio)

> **Propósito:** Documento maestro *Zero-Delete* que responde exactamente: **(1)** por qué nuestros videos están pensados por capas editables sin re-renderizar todo desde cero, **(2)** qué herramientas y hardware tienes **realmente instalados y verificados** hoy en esta iMac, **(3)** cuáles son los **4 upgrades gratuitos** del hilo/video de X que sí conviene sumar ya, **(4)** la **Bóveda de Reserva** (nada se tira a la basura: cada repo queda catalogado con su uso real y cuándo activarlo o recomendarlo), y **(5)** la **Bóveda de Riesgos y Ciberseguridad** convertida en guion viral para **`¡WATERS!`**.

---

## Arquitectura Modular por 5 Capas (¿Cómo editas sin rehacer todo el video?)

**Aclaración clave sobre tus episodios actuales (`EP06`, `EP07`, `EP08`):**
- **NO tienen subtítulos quemados sobre la escena.** Los renders actuales mantienen limpia la zona inferior (`260 px` libres abajo), precisamente para que el texto dinámico, las tarjetas o los subtítulos no queden soldados encima del 3D ni te arruinen el encuadre si después quieres cambiar tipografía, corregir una palabra o ajustar un CTA.

Para que editar cualquier episodio sea tan sencillo como cambiar una pieza de Lego (sin rehacer todo el video cada vez), la fábrica trabaja separando **5 capas independientes**:

| Capa | Qué contiene | Formato / Piezas en el repo | Qué te permite editar sin rehacer el resto |
| --- | --- | --- | --- |
| **1. Guion, Beats y Metadata** | Hook, diálogo por bloques, tiempos por escena, captions y CTA | `tablero_semanal_14_slots.json`, scripts `generar_ep*.py`, `EPISODIO_MAD08_ES_POR_EL_BIEN_DE_TU_CUOTA.md` | Cambiar textos de descripción, horarios, CTA o ajustar la duración de un beat antes de renderizar. |
| **2. Audio y Voz por Pista** | Locución/voces separadas, SFX y base musical mezclada en pista aparte | `waters_audio_engine.py`, `generar_voces_elevenlabs.py`, `generar_casting_voces.py`, pistas `.wav`/`.mp3` | Corregir una frase o cambiar el tono de voz en un segmento puntual sin tocar los modelos ni cámaras 3D. |
| **3. Visual Base Limpio (`_clean.mp4`)** | Escena 3D (`Three.js` / `@react-three/fiber` en `Remotion`) o HTML animado (`HyperFrames`) **sin texto inferior quemado** | `proyectos/waters-3d-studio/` (`Remotion` + `Three.js`), composiciones HTML `HyperFrames`, renders con `260 px` inferiores libres | Reutilizar el mismo plano limpio para versiones A/B, otros idiomas, otros CTAs o reediciones en el futuro. |
| **4. Subtítulos y Overlays Externos** | Subtítulos sincronizados palabra por palabra, look cinematográfico, tarjetas/banners | Archivos `.srt` / `.ass` / JSON de timestamps (`WhisperX` recomendado), overlays HTML/CSS o React | Cambiar tamaño, color, posición o corregir una palabra escrita en pantalla en segundos, sin tocar el 3D base. |
| **5. Ensamblado Final (`Mux`)** | Unión rápida de **Visual Base Limpio + Audio Final + Subtítulos/Overlays** | `FFmpeg` + `ffprobe` (`/Users/imac/.local/bin/ffmpeg`) | Exportar el `.mp4` final (`1080×1920`) en cuestión de segundos cuando solo ajustaste subtítulos, música o voz. |

> **Regla operativa recomendada:** conservar siempre la salida limpia de la **Capa 3** (`_clean.mp4`) y las pistas de la **Capa 2** antes de aplicar los subtítulos de la **Capa 4** en el mux de la **Capa 5**. Así nunca quedas atrapado en un video monolítico.

---

## 1. Inventario Verificado Actual (Lo que YA tienes hoy en esta Mac)

Todo lo listado aquí fue verificado directamente en disco, binarios, `package.json`, scripts y perfil de sistema de este equipo.

### 1.1 Hardware y Capacidad Real Confirmada
- **Estación principal actual (este equipo):** iMac con procesador `Intel(R) Core(TM) i5-6500 CPU @ 3.20GHz` (4 núcleos físicos / 4 hilos), **`24 GB` RAM** (`25769803776` bytes), GPU dedicada **`AMD Radeon R9 M380` (`2 GB` VRAM)**, **`macOS 12.7.6` (`Build 21H1320`)**.
  - *Implicación técnica:* Muy capaz para código, `Remotion` 2D/3D ligero, `HyperFrames`, `FFmpeg`, mezcla de audio en Python y edición por capas; **no** es apta para correr localmente modelos pesados de generación de video IA ni escenas pesadas de Blender Cycles en GPU de `2 GB` VRAM.
- **Equipos y nube complementarios confirmados:**
  - Laptop **MacBook Pro M1 (2020)** (`8 GB` RAM, `256 GB` SSD) — Apple Silicon ágil para movilidad y pruebas ligeras, con almacenamiento limitado.
  - **Dell Windows 10 Pro** (`Intel HD Graphics 530`, `8 GB` RAM, `512 GB` HDD) — útil como nodo auxiliar / utilidades Windows.
  - **`iPhone 17 Pro Max`** — captura principal en estudio y referencia móvil real.
  - **`iCloud+ 6 TB`** (con cuota ampliada en ecosistema Apple) — respaldo continuo entre equipos y espejo de producción.
- **Datos oficiales del estudio físico (`js/config.js`):**
  - Marca: **Captoora Studio** (`https://captoora.studio`, galerías en `https://galeria.captoora.studio`).
  - Dirección: `Av. Paseo de los Álamos 165, Colinas de San Jerónimo, Monterrey, N.L., CP 64630`.
  - WhatsApp Business: `+52 81 4005 0088`.

### 1.2 Skills Instaladas en `.agents/skills/` (14 elementos verificados)
- `antigravity-animated-icons`
- `captoora-studio-retouch`
- `cartoon-3d-short`
- `design-taste-frontend`
- `figma`
- `hyperframes`
- `hyperframes-cli`
- `hyperframes-registry`
- `media-use`
- `python-encoding.test.mjs`
- `remotion-to-hyperframes`
- `reverse-any-video`
- `slideshow`
- `taste-skill`

### 1.3 Binarios Locales Verificados en `/Users/imac/.local/bin/`
- **Video, audio y medios:** `ffmpeg`, `ffprobe`, `hyperframes`, `yt-dlp`, `gallery-dl`, `gallery-dlp`, `galeria-dl`
- **Python y entorno:** `python3.12`, `uv`, `uvx`
- **Dispositivos móvil / Android:** `adb`, `fastboot`, `scrcpy`
- **Agentes y utilidades CLI:** `agy` (y respaldo `agy.1795203269636494000.old`), `agent`, `artemis`, `codex`, `codex-code-mode-host`, `grok`, `notebooklm`, `notebooklm-mcp`, `notebooklm-server`

### 1.4 Stack 3D / Video Web Instalado en `proyectos/waters-3d-studio/package.json`
- `@remotion/cli`: `^4.0.240`
- `remotion`: `^4.0.240`
- `@remotion/three`: `^4.0.240`
- `@react-three/fiber`: `^8.17.10`
- `three`: `^0.170.0`
- `react` / `react-dom`: `^18.3.1`
- `typescript`: `^5.6.3` (`@types/react: ^18.3.12`, `@types/react-dom: ^18.3.1`, `@types/three: ^0.170.0`)

### 1.5 Motores Propios, Scripts de Episodios y Tablero en `proyectos/waters-serie/`
- **Motores y utilidades en `proyectos/waters-serie/scripts/` (13 scripts):**
  - Audio y voces: `waters_audio_engine.py`, `generar_voces_elevenlabs.py`, `generar_casting_voces.py`, `generar_mad08_audio.py`, `render_mad08_final.py`
  - Generadores de episodios: `generar_ep01_ext.py`, `generar_ep03_tony_cuota.py`, `generar_ep05_fable_vs_hydrogen.py`, `generar_ep06_hackeos_y_voz.py`, `generar_ep07_anthropic_ipo.py`, `generar_ep08_agente_contable_sat.py`
  - Generadores de Lead Magnets PDF: `generar_guia_blinda_pdf.py`, `generar_guias_ep07_ep08_pdf.py`
- **Operación editorial, tableros y ventas activos:**
  - `ESTRATEGIA_DOS_VERTIENTES_Y_OPERACION_14_SEMANA.md`
  - `tablero_semanal_14_slots.json`
  - `tablero_calendario_waters.html`
  - `referencias/inbox/README.md`
  - `EPISODIO_MAD08_ES_POR_EL_BIEN_DE_TU_CUOTA.md`
  - Entregables publicados recientes (`EP07` `WATERS_CHISPA_EP07_ANTHROPIC_IPO_60S.mp4` + `GUIA_BOLSA_PREIPO_CAPTOORA.pdf`, `EP08` `WATERS_CHISPA_EP08_CLAUDE_CONTADOR_SAT_60S.mp4` + `GUIA_CONTADOR_IA_SAT_CAPTOORA.pdf`)
  - Kit comercial B2B: `docs/propuestas_comerciales/KIT_VENTAS_CASA_PRODUCTORA_CAPTOORA.md`

### 1.6 ¿Qué puedes producir HOY mismo sin instalar nada nuevo?
Con lo que ya tienes instalado puedes sacar en serie:
1. Shorts/Reels híbridos 3D (`Remotion` + `Three.js`) y motion HTML (`HyperFrames`) con zona inferior limpia (`260 px`).
2. Pistas de voz y SFX mezcladas desde Python (`waters_audio_engine.py`) y ensamblado limpio vía `FFmpeg`.
3. Guías PDF descargables listas para CTA automático en comentarios/WhatsApp.
4. Descarga local limpia de referencias visuales con `yt-dlp` para estudiar ritmo y encuadres sin entrar a sitios basura.
5. Micro-animaciones e interfaces con estándares visuales exigentes usando `design-taste-frontend`, `taste-skill` y `antigravity-animated-icons`.

---

## 2. Los 4 Upgrades Gratuitos Listos para Tu Mac (Del Hilo/Video de X)

De las herramientas mostradas en el video y capturas de `https://x.com/woodxbt/status/2124482580896498142`, estas **4 piezas** embonan directo en nuestra arquitectura por capas **sin pedir GPU pesada ni suscripción**:

| # | Upgrade | Capa que mejora | Qué aporta exactamente a `¡WATERS!` y Captoora | Viabilidad en esta iMac (`24 GB` RAM / `macOS 12.7.6` / `R9 M380 2 GB`) |
| --- | --- | --- | --- | --- |
| **1** | **`WhisperX`** (`github.com/m-bain/whisperX`) | **Capa 4 (Subtítulos externos)** | Alineación forzada de audio a texto **palabra por palabra al milisegundo**. Convierte el WAV de la Capa 2 en JSON/SRT exacto para generar subtítulos dinámicos editables sin quemarlos en la Capa 3. | **Alta (en CPU / modelo pequeño-medio o en MacBook M1).** Sin necesitar GPU NVIDIA; en esta iMac Intel corre en CPU para audios de 60s en pocos segundos/minutos (y en M1 aún más rápido). |
| **2** | **`react-postprocessing` + `Theatre.js`** | **Capa 3 (Visual Base 3D)** | Añade acabado cinematográfico en tiempo real (bloom sutil, viñeta, grano, DOF ligero) sobre nuestro `@react-three/fiber` actual + líneas de tiempo visuales de cámara sin pelear solo con números en código. | **Alta dentro de `waters-3d-studio`.** Ya tenemos `three ^0.170.0` y `@react-three/fiber ^8.17.10`; solo hay que dosificar efectos para no saturar los `2 GB` VRAM de la M380. |
| **3** | **`GSAP`** (`github.com/greensock/GSAP`) | **Capa 3 y 4 (HTML / `HyperFrames` / Overlays)** | Curvas de easing profesionales, *timelines* encadenados y secuenciación súper fluida para tarjetas, HUDs de ciberseguridad, texto cinético y transiciones dentro de `HyperFrames`. | **100% nativa y ligera.** Corre en navegador/headless Chromium sin carga pesada de GPU. |
| **4** | **`onetake`** (`github.com/feitangyuan/onetake`) + paquete de acabado visual (**`Lemo-Opuscar`** `github.com/lemomo-ai/lemo-opuscar`, **`Hallmark`** `github.com/Nutlope/hallmark`, **`Impeccable`** `github.com/pbakaus/impeccable`) | **Capas 3 y 4 (Dirección de cámara y estética anti-IA)** | `onetake` aporta planos secuencia continuos sin cortes abruptos; `Lemo-Opuscar` suma **99 looks cinematográficos reproducibles en código**; `Hallmark` e `Impeccable` complementan a `taste-skill` para erradicar el "look genérico de IA". | **100% viable (son código, prompts/skills y parámetros CSS/shader ligeros).** Se integran gradualmente previa auditoría de seguridad (ver Sección 4). |

*(Nota de inventario honesto: en el video original también aparece `Remotion Skills` de `remotion-dev/skills`; ya usamos `Remotion` y podemos sumar su skill oficial cuando ampliemos escenas en `waters-3d-studio`.)*

---

## 3. Bóveda de Reserva (Herramientas Guardadas, Cero Basura)

Ninguna herramienta que nos compartiste se descarta ni se tira. Aquí quedan **ordenadas por nombre, fuente real y condición exacta** para activarlas cuando convenga (o recomendárselas a un cliente o colega cuyo flujo sí las necesite):

| Herramienta / Patrón | Fuente / Referencia | Qué hace | Por qué está en Reserva hoy (no activa por defecto) | Cuándo sacarla de la Bóveda o a quién recomendarla |
| --- | --- | --- | --- | --- |
| **`ComfyUI`** | `github.com/Comfy-Org/ComfyUI` | Motor nodal local para generación y pipelines de imagen/video por IA. | Exige GPU moderna con bastante VRAM (ideal 8–24 GB VRAM CUDA/Apple Silicon amplio) y decenas de GB en checkpoints; nuestra iMac tiene `AMD R9 M380` de `2 GB` VRAM en macOS 12. | Activar en nube GPU bajo demanda o si incorporamos estación Apple Silicon M-series con >=32 GB / PC con NVIDIA RTX (>=12 GB VRAM). Ideal para colegas con PC gamer que hacen generación pesada local. |
| **`Blender MCP` / *La Fábrica de Reels*** | `github.com/ahujasid/mcp-for-blender` + arquitectura de escena 3D en Blender | Permite que un agente controle Blender por MCP para modelar, iluminar y renderizar escenas 3D completas. | Instalar Blender + Cycles + simulaciones pesadas satura GPU de `2 GB` VRAM y alarga tiempos de render frente a `Remotion + Three.js` y `HyperFrames`. | Cuando un comercial de cliente (o un episodio especial de Captoora) pida un plano 3D hiperrealista específico, o para un estudio 3D con workstation dedicada. |
| **`Higgsfield API` + `n8n`** | Flujo externo automatizado (API comercial + orquestador `n8n`) | Orquestación automática de prompts, generación de clips con avatars/video IA en la nube y publicación conectada por webhooks. | Implica costo recurrente por API/créditos (FinOps) y riesgo de automatizar publicaciones sin filtro humano antes de validar audiencia y marca. | Activar solo para clientes que paguen bolsa mensual de producción automatizada o tras consolidar nuestro sistema editorial base con métricas reales. |
| **`huashu-motion`** | `github.com/alchaincyf/huashu-motion` | Generación de *launch films* que incluso generan/sincronizan su propia música. | Ya tenemos pipeline más controlable con `HyperFrames` + `waters_audio_engine.py`; meter otro framework entero hoy duplicaría esfuerzo. | Probar como referencia para videos de lanzamiento rápido de productos SaaS o startups que pidan "demo cinematográfica con música en 1 día". |
| **`anything2explainer`** | `github.com/Vincentwei1021...` | Convierte un tema cualquiera en un video explicativo narrado automáticamente. | Tendencia al formato genérico si no pasa por nuestra dirección de arte (`¡WATERS!`) y escritura propia. | Útil para investigar estructuras de explicadores rápidos o prototipar borradores internos de capacitación B2B antes de pasarlos a guion real. |
| **`OpenScreen`** | `github.com/getopenscreen/...` | Grabaciones de pantalla que lucen como demos pulidas (zooms, cursor limpio, fondo). | Aún no hemos hecho tutoriales intensivos de software/pantalla en `¡WATERS!`. | **Altísima utilidad inmediata** apenas grabemos cápsulas de ciberseguridad mostrando terminal, navegador, inspección de repos o WhatsApp/CRM en pantalla. |
| **`EffectCraft`** | `github.com/storytold/effectcraft` | Toolkit de VFX gratuitos listos para reutilizar en web/video. | Primero consolidamos nuestra librería base (`hyperframes-registry` + `Three.js`) para no inflar el stack. | Cuando un guion pida un efecto visual puntual (partículas, distorsión de señal, glitch de hackeo) sin programarlo desde cero. |
| **`Open Design`** | `github.com/nexu-io/open-design` | Workspace open source de diseño asistido por IA sin suscripción mensual. | Ya cubrimos diseño/UI con `Figma` + skills locales de diseño y retoque de estudio (`captoora-studio-retouch`). | Útil si queremos reemplazar herramientas de pago para prototipado colaborativo o recomendar una alternativa libre a clientes pyme. |
| **`video-use`** | `github.com/browser-use/video-use` | Pipeline agéntico de `"raw footage in, final.mp4 out"`. | En producciones comerciales preferimos control explícito por capas (Capas 1–5) antes que caja negra total. | Evaluarlo para cortes automáticos de bruto largo (ej. podcasts, charlas de 20 min o grabaciones de backstage sin editar del estudio). |

---

## 4. Bóveda de Riesgos y Ciberseguridad (Y Concepto Listo de Reel `¡WATERS!`)

Esta sección convierte los errores típicos de internet ("bájate todo gratis ahorita") en **blindaje operativo para Captoora Studio** y en **material directo para el personaje de Ciberseguridad de `¡WATERS!`** (aplicando ilegalidades/malas conductas digitales con ejemplos reales y tangibles, sin paja técnica vacía).

### 4.1 Los 4 Peligros Reales a Evitar en Nuestra Fábrica
1. **Clonación ciega de "16 repos gratis de IA por hype" (Ataques de Supply Chain):**
   - **Typosquatting y repos trampa:** al teclear rápido el nombre de un repo viral en X o buscarlo en Google, es común caer en un fork falso (cambia una letra o un guion) diseñado para robar llaves.
   - **Código malicioso al instalar (`postinstall` en `package.json`, `setup.py` / `pyproject.toml`, `.sh`, `.bat`):** un `npm install` o `pip install` ejecuta código en tu máquina *antes* de que tú corras el programa; ahí pueden leer tu `.env`, llaves `~/.ssh`, tokens de sesiones o credenciales guardadas.
   - **Prompt injection escondida en `README.md` o skills copiadas sin leer:** si le pasas una skill o repo sin revisar a tu agente con acceso al sistema, instrucciones ocultas en texto pueden intentar hacer que el agente lea archivos privados o ejecute comandos no autorizados.
   - **Binarios precompilados opacos:** archivos `.dmg`, `.exe` o `.whl` sin verificación ni código legible que coincida con el build.
2. **Sitios web "descargadores gratis" y scrapers dudosos:**
   - Páginas llenas de botones falsos de descarga, malvertising o extensiones de navegador que capturan **cookies de sesión** (secuestro de cuenta de Instagram, Facebook, Google o GitHub sin necesitar tu contraseña ni tu 2FA). En Captoora usamos herramientas locales auditables como `yt-dlp` en terminal, nunca extensiones piratas ni sitios puente sospechosos.
3. **Encadenar múltiples cuentas web gratuitas para evadir cuotas:**
   - Además de violar Términos de Servicio (riesgo de baneo en cadena de cuentas del estudio o del negocio), fragmenta historiales, deja sesiones abiertas en equipos compartidos y destruye el control de costos real (FinOps).
4. **Agentes corriendo sin límites ni aislamiento ("permisos totales en disco principal"):**
   - Dar acceso abierto sin reglas a correos, carpetas de respaldos, navegadores con bancos o producción de clientes convierte cualquier error o repo infectado en fuga de información real (recuerda nuestra regla: fotos de sesiones de clientes no tocan el disco interno ni repos públicos, y los secretos solo viven referenciados fuera de Git).

### 4.2 Checklist de Auditoría en 60 Segundos Antes de Clonar Cualquier Repo
Antes de correr `npm install`, `pip install` o `uv` sobre cualquier repo nuevo (aunque salga en un hilo con 50,000 likes):
1. **Verifica al autor real y la URL exacta:** entra directo desde el enlace oficial verificado y confirma historial de commits, colaboradores y licencia (`MIT`/`Apache-2.0`), nunca desde búsquedas apresuradas ni mirrors raros.
2. **Clona sin ejecutar (`git clone --depth 1` en carpeta sandbox `/tmp` o carpeta de pruebas) e inspecciona primero:**
   - En proyectos JS/TS: abre `package.json` y revisa la sección `"scripts"` (`preinstall`, `install`, `postinstall`).
   - En proyectos Python: revisa `setup.py`, `pyproject.toml` y `requirements.txt` en busca de URLs extrañas o código ejecutándose al importar/instalar.
   - Revisa cualquier `.sh`, `.command`, `.bat` o `Makefile`.
3. **Escanea llamadas sensibles:** busca referencias a `.env`, `.ssh`, `.aws`, `keychain`, `Cookies`, `curl ... | sh`, `base64 -d` o envíos HTTP salientes en archivos de instalación o skills.
4. **Aísla dependencias y cero secretos cargados:** prueba primero en un entorno limpio (`uv venv` / carpeta temporal) **sin** variables `.env` productivas ni llaves de clientes en el mismo directorio.
5. **Filtro Captoora FinOps + Hardware:** pregúntate *"¿Esto resuelve un cuello de botella real que no cubrimos hoy y corre bien en nuestra iMac (`24 GB` RAM / `2 GB` VRAM)?"*. Si no, se guarda en la **Bóveda de Reserva**, no en tu disco productivo.

---

### 4.3 Concepto Listo para Grabar: Reel `¡WATERS!` de Ciberseguridad
- **Título / Hook (0–3s):** *"No bajes esos '16 repos gratis de IA' por hype sin revisar esto (así te roban tus cuentas)"*
- **Analogía tangible (modelo Captoora / mundo real -> mundo digital):**
  - Así como nadie mete a su estudio de fotografía una caja cerrada que alguien dejó en la banqueta porque decía *"equipo gratis"* y la conecta directo a la red eléctrica y a la computadora donde están los contratos y cuentas de clientes...
  - Clonar un repo viral y tirar `npm install` o `pip install` sin mirar qué trae adentro es exactamente darle llave maestra de tu cuarto de archivos al desconocido que armó la caja.
- **Desarrollo rápido (15–45s):**
  1. Muestra el clásico hilo viral de X ("16 repos gratis para reemplazar agencias").
  2. Explica en 10 segundos qué es un `postinstall` trampa o un repo con nombre casi idéntico (typosquatting): cuando instalas, sin que tú abras la app todavía, ya pudo leer tu archivo `.env` (donde están tus llaves de API), tu carpeta `.ssh` o tus cookies de sesión.
  3. Muestra los **3 checks en 60 segundos** antes de instalar nada: (1) verificar autor/URL exacta, (2) abrir `package.json` / `setup.py` antes de instalar, (3) probar en carpeta aislada sin secretos.
- **Puente al estudio y CTA (45–60s):**
  - *"La inteligencia artificial no te protege sola; la arquitectura y el criterio sí. Esto también aplica para proteger las cuentas, catálogos y operación de tu negocio."*
  - **CTA en pantalla / descripción:** Comenta **`AUDITA`** y te mando la lista corta de verificación de 60 segundos antes de instalar cualquier herramienta de IA en tu compu.
