# 🛸 CATÁLOGO MAESTRO DE RECURSOS DE DISEÑO, MOTION UI & HERRAMIENTAS WEB
> **Auditoría Técnica Exhaustiva & Cotejo de Referencias · Captoora Studio**  
> **Solicitado por:** Alfonso "Poncho" Gutiérrez Flores (`@ponchogf88`)  
> **Fecha:** 30 de Octubre de 2026 | **Estado:** 100% Cotejado contra Capturas y Logs (Cero Omisiones)  
> **Versión PDF Descargable:** [LISTA_MAESTRA_RECURSOS_DISENO_PAGINAS.pdf](LISTA_MAESTRA_RECURSOS_DISENO_PAGINAS.pdf)

---

## 📊 Métricas del Expediente
- **76 Recursos Totales** documentados con enlaces oficiales y casos de uso.
- **14 Capturas de Pantalla de X (Twitter)** y carrete auditadas exhaustivamente.
- **7 Categorías Especializadas** (Motion UI, Pipeline Opus 5.5, Galerías de Diseño, Shaders/Audio, Open Source, Video/3D e IA).
- **Cero Omisiones:** Cada sitio, repositorio o autor mencionado en los diálogos y capturas está catalogado a continuación.

---

## 📑 Índice de Secciones
1. [El "Santo Grial" de Motion UI & Componentes Interactivos (Noah @noahelhadedy)](#1-el-santo-grial-de-motion-ui--componentes-interactivos)
2. [Arquitectura Opus 5.5 Motion Lab & Pipeline de 4 Fases (60 FPS)](#2-arquitectura-opus-55-motion-lab--pipeline-de-4-fases-60-fps)
3. [Galerías de Diseño, Micro-detalles & Landing Pages (Dev Patel, Bardhyl, Nero, Tripti)](#3-galerías-de-diseño-micro-detalles--landing-pages)
4. [Shaders, Fondos, Audio Háptico, Iconos & Tipografía](#4-shaders-fondos-audio-háptico-iconos--tipografía)
5. [Repositorios Open Source & Infraestructura de Negocio (Radman, Shahid Malik, Trending)](#5-repositorios-open-source--infraestructura-de-negocio)
6. [Motores de Video Programático, 3D & Motion Mencionados en el Diálogo](#6-motores-de-video-programático-3d--motion-mencionados-en-el-diálogo)
7. [Herramientas de IA para Investigación, Creación, Contenido y SEO](#7-herramientas-de-ia-para-investigación-creación-contenido-y-seo)

---

## 1. El "Santo Grial" de Motion UI & Componentes Interactivos
*(Origen: Captura de Noah @noahelhadedy · `media_1793038662459.png`)*

| # | Recurso | Enlace Oficial | Descripción Técnica & Propósito | Aplicación Planteada en Captoora | Origen de la Captura |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | **21st.dev** | [21st.dev](https://21st.dev) | El "npm" de los componentes de diseño. Catálogo comunitario con componentes animados listos para copiar y pegar (Tailwind, Framer Motion, Radix). | Tarjetas interactivas de servicios, modales fluidos y navegación. | `media_1793038662459.png` (Noah #1) |
| **2** | **motion-primitives.com** | [motion-primitives.com](https://motion-primitives.com) | Primitivas avanzadas de animación sobre Motion (Framer Motion): texto revelador, acordeones elásticos y transiciones de layout compartidas. | Revelación suave de citas editoriales y acordeones de preguntas frecuentes. | `media_1793038662459.png` (Noah #2) |
| **3** | **reactbits.dev** | [reactbits.dev](https://reactbits.dev) | Componentes React para fondos interactivos, shaders WebGL, partículas atmosféricas, ruido analógico y refracciones de cristal. | Fondo oscuro *Dark Void* con polvo estelar en suspensión para el Hero web. | `media_1793038662459.png` (Noah #3) |
| **4** | **hover.dev** | [hover.dev](https://hover.dev) | Micro-interacciones animadas para botones, menús, cursores magnéticos y tarjetas con perspectiva 3D al cursor. | Botón magnético de WhatsApp con rebote elástico táctil. | `media_1793038662459.png` (Noah #4) |
| **5** | **ui.aceternity.com** | [ui.aceternity.com](https://ui.aceternity.com) | Biblioteca de componentes premium por Manu Arora (Tailwind + Motion): Bento Grids, 3D Pin, lámparas Spotlight y bordes resplandecientes. | Bento Grid para exhibir tarifas ($1,000 básica, $350 renta) con bordes de 1px. | `media_1793038662459.png` (Noah #5) |
| **6** | **magicui.design** | [magicui.design](https://magicui.design) | +50 componentes animados para landing pages: bordes brillantes en rotación (shimmer), efectos typewriter y destellos. | Bordes dorados/lima giratorios para la tarjeta del paquete Signature. | Thread Noah (Componentes animados) |
| **7** | **cult-ui.com** | [cult-ui.com](https://cult-ui.com) | Primitivas y componentes con estética minimalista, austera y refinada de alto estándar digital. | Selectores de fecha, acordeones técnicos y controles discretos. | Thread Noah (Componentes animados) |

---

## 2. Arquitectura Opus 5.5 Motion Lab & Pipeline de 4 Fases (60 FPS)
*(Origen: Captura de Florian / Skunzu @skunzu · `media_1793038829583.jpg`)*

> **Pipeline Determinista:**  
> `STAGE 01 - AST GEN` (Árbol semántico por LLM) &rarr; `STAGE 02 - PHYSICS` (Simulación de resorte y amortiguación $\zeta$) &rarr; `STAGE 03 - RASTER` (Dibujo Canvas/GL) &rarr; `STAGE 04 - WASM TRANSCODE` (FFmpeg WASM a 60 FPS estables bajo función pura `seek(t)`).

| # | Módulo / Repositorio | Enlace Oficial | Especificación Técnica en Opus 5.5 | Rol en el Storytelling de Cámara |
| :---: | :--- | :--- | :--- | :--- |
| **8** | **three.js** | [threejs.org](https://threejs.org) | 3D Graphics CI, loops 120 FPS, rig orbital (`scene_camera_rig.js`), shaders GLSL (`custom_shaders.glsl`). | Renderizado de lente, curvatura de cristal y rotación 360° en Acto 1. |
| **9** | **motion** | [motion.dev](https://motion.dev) | Motor de físicas de resortes (`spring_physics.ts`), transformaciones FLIP sin salto de DOM (`layout_shift.tsx`). | Respiración óptica del encuadre y desaceleración fluida al detener scroll. |
| **10** | **Fabric.js** | [fabricjs.com](https://fabricjs.com) | Lienzo vectorial 2D interactivo, modelo de objetos JSON (`object_model.js`) e interpolación bezier (`path_tween.js`). | Retícula de enfoque Live View del sensor y gráfico de histograma. |
| **11** | **ffmpeg.wasm** | [ffmpegwasm.netlify.app](https://ffmpegwasm.netlify.app) | Transcodificador WASM, heap buffer de 512MB, frame grabbing (`frame_grab.ts`) y bus de audio a 1.2ms (`audio_join.ts`). | Exportación programática de videos MP4 para redes sociales sin servidor. |
| **12** | **Deck.gl** | [deck.gl](https://deck.gl) | Capas de aceleración WebGL2 para nube de un millón de puntos (`point_cloud.js`) y proyección Mercator 3D (`geo_project.js`). | Nube de partículas 3D que simula el haz de luz del flash. |
| **13** | **canvas-confetti** | [github.com/catdad/canvas-confetti](https://github.com/catdad/canvas-confetti) | Motor de partículas ligero sin dependencias externas: velocidad gravitacional (`particle_vel.js`) y ráfagas a 60 FPS. | Destello de celebración al confirmar reserva o disparar la foto. |
| **14** | **@react-three/drei** | [github.com/pmndrs/drei](https://github.com/pmndrs/drei) | Helpers para R3F: skybox de iluminación HDR de estudio (`hdr_env.tsx`) y controles de órbita amortiguados (`orbit_ctrl.tsx`). | Simulación de reflejos cian/ámbar en el cuerpo de aleación de magnesio. |
| **15** | **cobe** | [github.com/shuding/cobe](https://github.com/shuding/cobe) | Globo terráqueo 3D en WebGL de 5KB por Shu Ding (Vercel): matriz de puntos (`dot_globe.js`) y arcos de coordenadas. | Mapa 3D para clientes foráneos que viajan al set de San Jerónimo 11. |
| **16** | **twgl.js** | [twgljs.org](https://twgljs.org) | "Tiny WebGL" por Greggman: vinculación limpia de buffers (`buffer_bind.js`) y compilación rápida de shaders sin boilerplate. | Diafragma iris de 9 palas con aceleración gráfica pura. |
| **17** | **Rive Runtime** | [rive.app](https://rive.app) | Motor vectorial con máquinas de estados finitos booleanas (`state_machine.ts`), binarios mínimos y bucles a 128 FPS. | Monograma interactivo de Captoora reactivo al cursor y clics. |

---

## 3. Galerías de Diseño, Micro-detalles & Landing Pages
*(Origen: Capturas de Dev Patel, Bardhyl Bytyqi, Nero y Tripti Tripathi)*

| # | Plataforma | Enlace Oficial | Especialidad Visual & Enfoque | Captura de Origen |
| :---: | :--- | :--- | :--- | :--- |
| **18** | **60fps.design** | [60fps.design](https://60fps.design) | Catálogo de micro-interacciones móviles y web ejecutadas a 60 FPS estables. | `media_1793038829919.png` (Dev Patel #1) / `media_1793038932620.png` (Bardhyl #9) |
| **19** | **godly.website** | [godly.website](https://godly.website) | El referente mundial número uno en sitios web premiados, estética oscura de lujo y WebGL. | `media_1793038932620.png` (Bardhyl #8) |
| **20** | **detail.design** | [detail.design](https://detail.design) | Colección enfocada exclusivamente en micro-detalles y pulido fino de producto digital. | `media_1793038829919.png` (Dev Patel #5) |
| **21** | **scrolltide.co** | [scrolltide.co](https://scrolltide.co) | +600 prompts de diseño y código fuente completo para sitios 3D y scroll-driven design. | `media_1793038829919.png` (Tripti #1) / `media_1793038932460.png` (Nero #8) |
| **22** | **landdding.com** | [landdding.com](https://landdding.com) | Directorio de páginas de aterrizaje clasificadas por conversión, estructura y tipografía. | `media_1793038932620.png` (Bardhyl #3) |
| **23** | **modulify.ai** | [modulify.ai/templates](https://modulify.ai/templates) | Plantillas modulares de landing pages listas para producción y maquetación ágil. | `media_1793038932460.png` (Nero #1) / `media_1793038932620.png` (Bardhyl #1) |
| **24** | **motionin.design** | [motionin.design](https://motionin.design) | Galería de inspiración enfocada exclusivamente en diseño de movimiento para UI. | `media_1793038932620.png` (Bardhyl #2) |
| **25** | **inspora.design** | [inspora.design](https://inspora.design) | Inspiración visual diaria extraída de la comunidad creativa global de X. | `media_1793038829919.png` (Dev Patel #4) / `media_1793038932460.png` (Nero #4) |
| **26** | **bestdesignsonx.com** | [bestdesignsonx.com](https://bestdesignsonx.com) | Archivo de los diseños de software, interfaces y webs más virales y aclamados en X. | `media_1793038829919.png` (Dev Patel #6) |
| **27** | **theinternetdesigns.com** | [theinternetdesigns.com](https://theinternetdesigns.com) | Muestrario de interfaces contemporáneas de estudios y creadores independientes. | `media_1793038829919.png` (Dev Patel #7) |
| **28** | **collectui.com** | [collectui.com](https://collectui.com) | Archivo diario de micro-pantallas organizadas por componente (checkout, formularios, etc.). | `media_1793038829919.png` (Dev Patel #2) |
| **29** | **recent.design** | [recent.design](https://recent.design) | Descubrimientos de diseño web frescos y actualizados diariamente. | `media_1793038829919.png` (Dev Patel #3) |
| **30** | **wonderlist.design** | [wonderlist.design](https://wonderlist.design) | Colección curada de archivos, librerías y kits de diseño de élite para Figma. | `media_1793038932620.png` (Bardhyl #4) |
| **31** | **on.design** | [on.design](https://on.design) | Comunidad y directorio de diseño web minimalista y portafolios editoriales. | `media_1793038932620.png` (Bardhyl #7) |
| **32** | **navbar.gallery** | [navbar.gallery](https://navbar.gallery) | Galería de inspiración dedicada exclusivamente a barras de navegación y menús flotantes. | `media_1793038829919.png` (Tripti #2) |
| **33** | **footer.design** | [footer.design](https://footer.design) | Directorio especializado en diseño, arquitectura y estética de pies de página (*footers*). | `media_1793038829919.png` (Tripti #3) / `media_1793038932460.png` (Nero #7) / `media_1793038932620.png` (Bardhyl #10) |

---

## 4. Shaders, Fondos, Audio Háptico, Iconos & Tipografía
*(Origen: Capturas de Nero @neropursue y Bardhyl Bytyqi · `media_1793038932460.png` y `620.png`)*

| # | Recurso | Enlace Oficial | Descripción Técnica | Caso de Uso en Fotografía / Estudio | Origen de la Captura |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **34** | **audiocn.dev** | [audiocn.dev](https://audiocn.dev) | Componentes de audio y catálogo de efectos de sonido (SFX) para interfaces web. | Sonido háptico de obturador de cámara Nikon Z9 al presionar reservar o clickear fotos. | `media_1793038932460.png` (Nero #5) |
| **35** | **squints.app** | [squints.app](https://squints.app) | Editor y generador de shaders, distorsiones ópticas y gradientes dinámicos en código. | Refracción óptica del cristal f/1.2 y destello anamórfico del pentaprisma. | `media_1793038932460.png` (Nero #2) |
| **36** | **backgrounds.supply** | [backgrounds.supply](https://backgrounds.supply) | Texturas de grano analógico (*film grain*), ruido estocástico y gradientes oscuros. | Texturizado del vacío negro (#000000) para evitar fondos planos plásticos. | `media_1793038932460.png` (Nero #3) |
| **37** | **encyclopedia.iconography.co** | [encyclopedia.iconography.co](https://encyclopedia.iconography.co) | Directorio y enciclopedia de iconografía, símbolos técnicos y sistemas semióticos. | Telemetría del visor (ISO, apertura, obturador, retícula de enfoque). | `media_1793038932460.png` (Nero #6) |
| **38** | **iconly.design** | [iconly.design](https://iconly.design) | Sistema vectorial de más de 600 iconos estilizados para interfaces web y móviles. | Iconos de amenidades del set, WhatsApp, ubicación y cotizador. | `media_1793038932620.png` (Bardhyl #5) |
| **39** | **fontinlogo.com** | [fontinlogo.com](https://fontinlogo.com) | Buscador de fuentes tipográficas detrás de logotipos de marcas globales. | Identificación de tipografías display geométricas de lujo para CAPTOORA sin sesgo de IA. | `media_1793038932620.png` (Bardhyl #6) |

---

## 5. Repositorios Open Source & Infraestructura de Negocio
*(Origen: Capturas de Leonard Radman @radmanAI, Trending GitHub y Shahid Malik)*

| # | Repositorio | Enlace Oficial | Arquitectura Técnica | Valor para Captoora Studio | Origen de la Captura |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **40** | **Cal.com** | [github.com/calcom/cal.com](https://github.com/calcom/cal.com) | Plataforma de reserva de citas open-source (alternativa a Calendly) con pagos y sync a Google Calendar. | Reserva instantánea de sesiones y renta de set sin fricción por WhatsApp. | `media_1793038662441.png` (Radman #1) |
| **41** | **n8n** | [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n) | Automatización de flujos de trabajo (*workflow automation*) autoalojada con soporte nativo de agentes IA. | Conexión de WhatsApp Business con Drive (fotos crudas), Sheets y avisos a clientas. | `media_1793038662441.png` (Radman #4) / `media_1793038662528.png` (Shahid Malik) |
| **42** | **Ghost** | [github.com/TryGhost/Ghost](https://github.com/TryGhost/Ghost) | CMS open-source para publicaciones, boletines por correo y membresías en Node.js de alta velocidad. | Publicación del blog fotográfico ("Guía Pumpkin Patch", "Cómo posar"). | `media_1793038662441.png` (Radman #3) |
| **43** | **Plausible Analytics** | [github.com/plausible/analytics](https://github.com/plausible/analytics) | Analítica web ultra-liviana (<1KB), respetuosa de privacidad, sin cookies ni ralentización. | Medición de conversión del sitio web de Captoora en móviles. | `media_1793038662441.png` (Radman #2) |
| **44** | **Supabase** | [github.com/supabase/supabase](https://github.com/supabase/supabase) | Backend Postgres open-source con Auth, Storage para imágenes y suscripciones en tiempo real. | Base de datos de clientas, historial de sesiones y cobros. | `media_1793038662441.png` (Radman #5) |
| **45** | **Medusa** | [github.com/medusajs/medusa](https://github.com/medusajs/medusa) | Motor de comercio electrónico headless modular open-source (alternativa a Shopify). | Venta digital de Gift Cards y paquetes de revelado fotográfico. | `media_1793038662441.png` (Radman #6) |
| **46** | **VoiceStudio** | [github.com/debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | Aplicación local para clonar voces, doblar videos y transcribir en 646 idiomas sin costos de API. | Locuciones en off para reels de Instagram y TikTok con la voz de marca del estudio. | `media_1793038829824.png` (Trending #1 - 57K) |
| **47** | **ppt-master** | [github.com/hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) | Convierte Word o PDF en presentaciones de PowerPoint editables con estructura visual profesional. | Generación automática de Lookbooks para clientas y propuestas de eventos. | `media_1793038829824.png` (Trending #2 - 59K) |
| **48** | **gods-eye-view** | [github.com/bilawalsidhu/gods-eye-view](https://github.com/bilawalsidhu/gods-eye-view) | Visualizador 3D satelital en el navegador con rastreo en vivo de aviones, barcos y cámaras. | Mapa satelital interactivo 3D para la ubicación de San Jerónimo 11. | `media_1793038829824.png` (Trending #3 - 50K) |
| **49** | **REA** | [github.com/morluto/rea](https://github.com/morluto/rea) | Protocolo Clean Room de ingeniería inversa para deconstruir apps y generar un `SPEC.md` con mediciones. | Deconstrucción cuadro por cuadro de animaciones de Duolingo y videos virales. | `media_1793038829823.jpg` (Prompt REA) / `media_1793038829824.png` (Trending #4 - 65K) |
| **50** | **diagram-design** | [github.com/cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | Generador automático de diagramas vectoriales estructurados adaptados a la identidad de marca. | Diagramas del flujo de reserva del cliente y organigrama del escuadrón. | `media_1793038829824.png` (Trending #5 - 49K) |
| **51** | **paperclip** | [github.com/paperclipai/paperclip](https://github.com/paperclipai/paperclip) | Plataforma de orquestación de agentes de IA para operar empresas autónomas con división de roles. | Supervisión autónoma del escuadrón de agentes (Marin, Conan, Lalo). | `media_1793038829824.png` (Trending #6 - 99K) |

---

## 6. Motores de Video Programático, 3D & Motion Mencionados en el Diálogo
*(Origen: Discusiones directas en el chat sobre la web cinemática y video)*

| # | Tecnología | Enlace Oficial | Capacidad Técnica | Discusión / Caso de Uso en el Proyecto |
| :---: | :--- | :--- | :--- | :--- |
| **52** | **Remotion** | [remotion.dev](https://remotion.dev) | Framework para crear videos reales MP4 en React/TypeScript a 60 FPS con sincronización de audio. | Mencionada como el "santo grial de video" para automatizar reels de 15s sin software manual. |
| **53** | **FFmpeg** | [ffmpeg.org](https://ffmpeg.org) | Motor multiplataforma líder para transcodificar, cortar, multiplexar y comprimir video y audio. | Compresión de videos pesados de 80MB del estudio a clips de 4MB de carga inmediata en móvil. |
| **54** | **Rive App** | [rive.app](https://rive.app) | Motor gráfico interactivo con máquinas de estado que sustituye animaciones estáticas JSON (Lottie). | El lente de Captoora que abre y cierra sus palas de diafragma al desplazar la página. |
| **55** | **GSAP + ScrollTrigger** | [gsap.com](https://gsap.com) | Motor de animación web JavaScript estándar para orquestar líneas de tiempo complejas sincronizadas al scroll. | Choreografía de los 5 Actos de scroll (Reveal, Face Off, Flash, Absorption, Galería Vórtice). |
| **56** | **Lenis Smooth Scroll** | [lenis.darkroom.engineering](https://lenis.darkroom.engineering) | Motor de desplazamiento suave accesible que otorga inercia cinematográfica estilo Apple a la página. | Desplazamiento premium con peso físico al navegar el Hero 3D de la cámara. |
| **57** | **React Three Fiber (R3F)** | [docs.pmnd.rs/react-three-fiber](https://docs.pmnd.rs/react-three-fiber) | Renderizador declarativo de Three.js para React con soporte de físicas, shaders y cámaras virtuales. | Renderizado interactivo de hardware con iluminación de doble recorte en tiempo real. |

---

## 7. Herramientas de IA para Investigación, Creación, Contenido y SEO
*(Origen: Capturas de Virginio Gallardo / Sofía Sicilia `media_1793038932904.png`, Tom Zaragoza `media_1793038932527.png`, UI/UX Savior y KlodCat)*

| # | Herramienta | Enlace Oficial | Función Principal & Metodología | Captura de Origen |
| :---: | :--- | :--- | :--- | :--- |
| **58** | **prompts.chat** | [prompts.chat](https://prompts.chat) | Repositorio abierto de prompts con +170k estrellas en GitHub categorizado por roles técnicos y creativos. | `media_1793038662490.png` (UI/UX Savior) |
| **59** | **Searchata.com** | [searchata.com](https://searchata.com) | Protocolo MCP para conectar Claude y ChatGPT directamente a Google Search Console para auditorías SEO. | `media_1793038932527.png` (Tom Zaragoza) |
| **60** | **Consensus** | [consensus.app](https://consensus.app) | Motor de búsqueda de evidencia científica con IA sobre más de 200 millones de publicaciones arbitradas. | `media_1793038932904.png` (Virginio #4) |
| **61** | **Elicit** | [elicit.com](https://elicit.com) | Asistente de IA para automatizar revisiones bibliográficas y síntesis de literatura técnica. | `media_1793038932904.png` (Virginio #6) |
| **62** | **ChatPDF** | [chatpdf.com](https://chatpdf.com) | Extracción de datos, resúmenes y consultas directas sobre documentos PDF con citas textuales. | `media_1793038932904.png` (Virginio #3) |
| **63** | **Humata** | [humata.ai](https://humata.ai) | Análisis interactivo de expedientes legales largos y contratos para responder preguntas al instante. | `media_1793038932904.png` (Virginio #9) |
| **64** | **Paperpal** | [paperpal.com](https://paperpal.com) | Asistente editorial de redacción formal, verificación léxica y consistencia de tono. | `media_1793038932904.png` (Virginio #12) |
| **65** | **Perplexity AI** | [perplexity.ai](https://perplexity.ai) | Motor de búsqueda conversacional fundamentado en fuentes web en tiempo real con citas directas. | `media_1793038932904.png` (Virginio #13) |
| **66** | **Research Rabbit** | [researchrabbit.ai](https://researchrabbit.ai) | Mapeo interactivo de redes y grafos de investigación académica interconectada. | `media_1793038932904.png` (Virginio #14) |
| **67** | **Scite.ai** | [scite.ai](https://scite.ai) | Análisis de citas contextuales para comprobar si afirmaciones han sido respaldadas o refutadas. | `media_1793038932904.png` (Virginio #15) |
| **68** | **Midjourney** | [midjourney.com](https://midjourney.com) | Motor generativo de imágenes de alta fidelidad estética e iluminación cinematográfica. | `media_1793038932904.png` (Virginio #11) |
| **69** | **Stable Diffusion** | [stability.ai](https://stability.ai) | Modelo generativo de imágenes open-source para inferencia local con control de poses (ControlNet). | `media_1793038932904.png` (Virginio #16) |
| **70** | **DeepL** | [deepl.com](https://deepl.com) | Traductor neuronal de alta precisión para localización de interfaces y textos sin pérdida de matiz. | `media_1793038932904.png` (Virginio #5) |
| **71** | **Grammarly** | [grammarly.com](https://grammarly.com) | Corrector de estilo, tono, gramática y claridad para comunicación profesional. | `media_1793038932904.png` (Virginio #8) |
| **72** | **Claude** | [claude.ai](https://claude.ai) | Modelo de lenguaje de Anthropic para razonamiento complejo, análisis documental y código. | `media_1793038932904.png` (Virginio #10) |
| **73** | **ChatGPT / GPT-4o** | [chatgpt.com](https://chatgpt.com) | Modelo conversacional multimodal de OpenAI para redacción comercial y estructuración de ideas. | `media_1793038932904.png` (Virginio #2) |
| **74** | **Google Gemini** | [gemini.google.com](https://gemini.google.com) | Modelo multimodal de Google para procesamiento de video, audio, contexto masivo y análisis visual. | `media_1793038932904.png` (Virginio #7) |
| **75** | **Microsoft Copilot** | [copilot.microsoft.com](https://copilot.microsoft.com) | Asistente de IA integrado para búsqueda conectada y productividad ofimática. | `media_1793038932904.png` (Virginio #1) |
| **76** | **klodcat.com** | [klodcat.com](https://klodcat.com) | Juego interactivo sobre buenas prácticas de Claude Code y seguridad para no exponer API keys en GitHub. | `media_1793038932670.png` (claudecode_es) |

---

*Expediente emitido y resguardado para Alfonso Gutiérrez Flores · Captoora Studio · Monterrey, N.L.*
