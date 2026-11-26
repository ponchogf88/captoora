/* Captoora Studio & ¡WATERS! — Modelo de datos verificado (sin servidor, compatible con file://) */
window.CAPTOORA_DATA = {
  schema_version: "1.0",
  meta: {
    workspace: "Captoora Studio · ¡WATERS! / ¿Caíste?",
    subtitulo: "Sala de control de producción, referencias y métricas",
    fecha_corte: "2026-11-26",
    meta_videos_validacion: 20,
    cuota_elevenlabs: {
      disponible: 30184,
      total: 61509,
      unidad: "caracteres"
    },
    audiencia_base_fb: 5600,
    hardware_principal: "iMac Intel i5-6500 · 24 GB RAM · Radeon R9 M380 2 GB VRAM · macOS 12.7.6",
    estacion_movil: "Redmi Note 8 · CapCut Pro ($30 MXN/mes, cuenta user3733613018365)",
    plataformas_nativas: [
      { id: "tiktok", nombre: "TikTok Studio", url: "https://www.tiktok.com/tiktokstudio", nota: "Programa hasta 10 días adelante" },
      { id: "youtube", nombre: "YouTube Studio", url: "https://studio.youtube.com", nota: "Shorts 9:16 y Largo 16:9" },
      { id: "meta", nombre: "Meta Business Suite", url: "https://business.facebook.com", nota: "IG Reels + Facebook Reels (5,600 seguidores)" }
    ],
    inventario_disco: {
      renders_waters_mp4: 25,
      renders_caiste_mp4: 4,
      renders_totales_mp4: 29,
      lead_magnets_pdf: 4,
      pack_ingredientes_sfx: 9,
      pack_ingredientes_halos: 4,
      pack_ingredientes_stickers: 10
    }
  },

  estaciones_relevo: [
    {
      paso: 1,
      codigo: "EST-01",
      nombre: "Ideas y Filtro",
      responsable: "Antigravity + Tú",
      estacion: "iMac / Investigación",
      entra: "Quejas reales de clientes, noticias del día y videos en referencias/inbox/",
      que_hace: "Aplica La Prueba del Ácido (3 filtros: antirreciclado, hardware Mac y señal real)",
      entrega: "Idea aprobada y clasificada como En prueba",
      cuando_se_quita: "Cuando apruebas el ángulo antes de escribir el guion",
      tiempo_estimado: "15 min/sem",
      estado: "Activo",
      detalle: "Incluye el ángulo Antes desordenado -> Después limpio para servicios de Captoora Studio y alertas ¡WATERS!."
    },
    {
      paso: 2,
      codigo: "EST-02",
      nombre: "Guion y Candados",
      responsable: "Antigravity + Tú",
      estacion: "iMac",
      entra: "Idea aprobada de Estación 1",
      que_hace: "Redacta guion 45-60s (enseña primero, producto al final; tiempos 5/7/9s en ¿Caíste?)",
      entrega: "Archivo .json o .md verificado con palabra CTA",
      cuando_se_quita: "Cuando das luz verde al diálogo y gancho inicial (0-2s)",
      tiempo_estimado: "20 min/pieza",
      estado: "Activo",
      detalle: "Sin inventar cifras ni prometer oro antes de probar. Define qué va en 3D, qué va en HTML y qué texto irá aparte."
    },
    {
      paso: 3,
      codigo: "EST-03",
      nombre: "Voz y Reloj Maestro",
      responsable: "waters_audio_engine.py + ElevenLabs",
      estacion: "iMac",
      entra: "Guion aprobado (texto mudo sin tiempos reales)",
      que_hace: "Genera locución por personaje, agrega SFX/cama musical y bloquea la duración exacta",
      entrega: "Pista _master.wav verificada (CLOCK LOCKED)",
      cuando_se_quita: "Al validar duración y volumen exacto con ffprobe",
      tiempo_estimado: "5 min/pieza",
      estado: "Activo",
      detalle: "Cuota actual cuidada: 30,184 de 61,509 caracteres disponibles. Caché de MP3 reutilizable para no pagar dos veces."
    },
    {
      paso: 4,
      codigo: "EST-04",
      nombre: "Visual Base Limpio",
      responsable: "iMac (Three.js + Remotion / HyperFrames + GSAP)",
      estacion: "iMac",
      entra: "Pista _master.wav + guion + Biblioteca de Ingredientes",
      que_hace: "Renderiza MP4 limpio (sin subtítulos quemados, 260 px libres abajo) y empuja al teléfono vía adb",
      entrega: "MP4 base en /sdcard/Movies/Captoora_CapCut/",
      cuando_se_quita: "Al confirmar archivo y carpeta de ingredientes en Redmi Note 8",
      tiempo_estimado: "10-15 min/pieza",
      estado: "Activo",
      detalle: "Ya tienes 29 renders MP4 en disco (25 de ¡WATERS! y 4 de ¿Caíste? + Pack #1 completo de SFX, 4 Halos y 10 PNGs)."
    },
    {
      paso: 5,
      codigo: "EST-05",
      nombre: "Condimentos y Revisión Humana",
      responsable: "Tú en Redmi Note 8 (CapCut Pro)",
      estacion: "Redmi Note 8",
      entra: "MP4 base limpio + 9 SFX teclado + 4 Halos + 10 stickers PNG",
      que_hace: "Agrega subtítulos dinámicos (absorbe a Captions), teclado cremoso, sticker del caso y revisión humana",
      entrega: "MP4 final exportado listo para redes",
      cuando_se_quita: "Al exportar el video final tras tu revisión cuadro a cuadro",
      tiempo_estimado: "10 min/pieza",
      estado: "En turno ahora",
      detalle: "Aquí estás hoy con CAISTE_SHORT_01_P4_CFE_V2_DYNAMIC.mp4 en 01_CAISTE_SHORTS/ y la cuenta CapCut Pro user3733613018365."
    },
    {
      paso: 6,
      codigo: "EST-06",
      nombre: "Programación y Medición",
      responsable: "Tú (TikTok / YT / Meta Business Suite gratis)",
      estacion: "Navegador Web",
      entra: "MP4 final exportado + títulos y CTAs de la cola semanal",
      que_hace: "Programa bloque semanal y registra a los 7 días vistas, retención, guardados y DMs reales",
      entrega: "Métricas verificadas que alimentan la Estación 1",
      cuando_se_quita: "Al cerrar corte semanal y anotar qué se repite o descarta",
      tiempo_estimado: "15 min/sem",
      estado: "Lista hoy",
      detalle: "Mismo video a TikTok, YouTube Shorts, Instagram Reels y Facebook (donde ya tienes 5,600 seguidores)."
    }
  ],

  relevos_banca: [
    {
      herramienta: "Captions (app móvil)",
      estado: "Reemplazado",
      momento: "Ya retirado del flujo",
      motivo: "CapCut Pro ($30 MXN/mes) absorbe por completo los subtítulos dinámicos animados y efectos de texto.",
      accion: "No renovar suscripción aparte."
    },
    {
      herramienta: "Opus Clip",
      estado: "Entra en Fase 2",
      momento: "Hito 4 (19 Dic+)",
      motivo: "No aporta valor en Shorts verticales de 60s. Entra solo cuando grabes episodios horizontales 16:9 de 10 min para trocearlos en 8-10 clips.",
      accion: "Usar con captions apagadas y bajar clips a Estación 5 (CapCut Pro)."
    },
    {
      herramienta: "WhisperX (local)",
      estado: "Siguiente 20%",
      momento: "Fase 3 (automatización Mac)",
      motivo: "Alinea audio WAV palabra por palabra al milisegundo en CPU/M1 para editar la Capa 4 en Mac sin depender solo del teléfono.",
      accion: "Activar tras completar los primeros 20 videos publicados."
    },
    {
      herramienta: "react-postprocessing + Theatre.js + Lemo-Opuscar",
      estado: "Siguiente 20%",
      momento: "Fase 3 (episodios largos 3D)",
      motivo: "Mejora acabados de cámara 3D y colorimetría en waters-3d-studio cuidando el límite de 2 GB VRAM de la iMac.",
      accion: "Incorporar cuando escales a capítulos 16:9."
    },
    {
      herramienta: "ComfyUI / Blender MCP / Higgsfield + n8n",
      estado: "Bóveda de reserva",
      momento: "Pausado por FinOps y hardware",
      motivo: "Piden GPU >= 12 GB VRAM o gasto API recurrente antes de validar retención y ventas reales.",
      accion: "Consultar cuando un cliente pague producción 3D dedicada."
    }
  ],

  roadmap_hitos: [
    {
      id: "H1",
      titulo: "Arranque de volumen (2 -> 11 de 20)",
      ventana: "26 Nov - 01 Dic 2026",
      esfuerzo: "1 semana · ~35 min tuyos",
      resultado_esperado: "55% de la meta sin renderizar nada nuevo",
      detalle: "Programar los 9 videos ya terminados de la cola semanal en TikTok, YT Shorts, IG Reels y Facebook (5,600 seguidores)."
    },
    {
      id: "H2",
      titulo: "Completar los primeros 20 (11 -> 20 de 20)",
      ventana: "02 - 15 Dic 2026",
      esfuerzo: "2 semanas · ~3 h/semana",
      resultado_esperado: "20 videos reales publicados en calle",
      detalle: "Producir 9 piezas nuevas: ¿Caíste? V2 (P2, P8), formato Antes desordenado -> Después limpio (Captoora y ¡WATERS!) y TUNEL-01 / ORO-01."
    },
    {
      id: "H3",
      titulo: "Primer corte de validación real (Día 21)",
      ventana: "16 - 18 Dic 2026",
      esfuerzo: "1 sesión de 45 min",
      resultado_esperado: "Decisión basada en retención, guardados y DMs",
      detalle: "Auditar los 20 videos. Descartar formatos que solo dan ego o cero retención y concentrar 80% de esfuerzo en los 2 ganadores."
    },
    {
      id: "H4",
      titulo: "Escala Largo 16:9 + Opus Clip + WhisperX",
      ventana: "19 Dic 2026 - 15 Ene 2027",
      esfuerzo: "3-4 semanas · ciclo continuo",
      resultado_esperado: "De 1 episodio largo salen 8-10 Shorts",
      detalle: "Activar Opus Clip sobre videos de 10 min y automatizar subtítulos locales con WhisperX manteniendo revisión humana."
    }
  ],

  referencias: [
    {
      id: "REF-01",
      fecha: "2026-11-17",
      fuente: "@heytrip3",
      plataforma: "Threads",
      url: "https://www.threads.com/@heytrip3/post/Df1Pi7vkrFV",
      que_muestra: "Estructura de gancho corto y ritmo ágil para hilos convertidos en video.",
      que_obtuvimos: "Base inicial para probar aperturas directas de 2 segundos antes de pasar al guion completo.",
      donde_vive: "proyectos/waters-serie/CALENDARIO_MAESTRO_30_DIAS_WATERS.md",
      veredicto: "En prueba",
      nota: ""
    },
    {
      id: "REF-02",
      fecha: "2026-11-18",
      fuente: "Reel plastilina / monito 3D",
      plataforma: "Instagram",
      url: "https://www.instagram.com/reels/DfccbDIibJE/",
      que_muestra: "Personaje 3D carismático estilo plastilina narrando temas tech sin rostro humano.",
      que_obtuvimos: "Dirección 100% sin cámara humana con casting de personajes propios (Chispa, Tony, Antigravity, Guardrails).",
      donde_vive: "proyectos/waters-serie/assets/ & PLAN_LABORATORIO_PERSONAJES_Y_BROLL.md",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-03",
      fecha: "2026-11-18",
      fuente: "Soy Vibecoder (Fábrica de Reels)",
      plataforma: "Web / Instagram",
      url: "https://soyvibecoder.com/fabrica#app",
      que_muestra: "Sistema de palabra clave en comentarios que dispara guía PDF o recurso automático.",
      que_obtuvimos: "Mecánica de CTAs con palabra clave (BLINDA, BOLSA, CONTADOR, APPLE) + 4 guías PDF reales.",
      donde_vive: "proyectos/waters-serie/lead_magnets/",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-04",
      fecha: "2026-11-18",
      fuente: "Reel arneses y guardrails IA",
      plataforma: "Instagram",
      url: "https://www.instagram.com/reels/Df5AT_FDG3w/",
      que_muestra: "Riesgos prácticos cuando agentes de IA operan sin arneses, límites ni aprobación.",
      que_obtuvimos: "Pilar de ciberseguridad práctica en ¡WATERS! y el personaje/concepto Guardrails.",
      donde_vive: "proyectos/waters-serie/EPISODIO_MAD04_EL_BOT_QUE_SABIA_DEMASIADO.md",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-05",
      fecha: "2026-11-19",
      fuente: "Mascota 4K en encuadre constante",
      plataforma: "Facebook",
      url: "https://www.facebook.com/reel/1292935342988871",
      que_muestra: "Personaje anclado visualmente sin desarmarse ni desaparecer al mostrar pantallas.",
      que_obtuvimos: "Regla visual de mantener al personaje visible en plano estable y respetar 260 px libres abajo.",
      donde_vive: "proyectos/waters-3d-studio/ & V2 dynamic specs",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-06",
      fecha: "2026-11-20",
      fuente: "Trío estética nocturna (727K likes)",
      plataforma: "Instagram",
      url: "https://www.instagram.com/reels/Df0giB1hM_C/",
      que_muestra: "Susurros, zooms lentos, diseño sonoro suave y clima de madrugada (DedIkqJla4G / Df0giB1hM_C / DfQrytINxzD).",
      que_obtuvimos: "Creación de la vertiente nocturna Historias de Madrugada (MAD08 Cuota y MAD09 Siri 2:47 AM).",
      donde_vive: "proyectos/waters-serie/ESTRATEGIA_DOS_VERTIENTES_Y_OPERACION_14_SEMANA.md",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-07",
      fecha: "2026-11-20",
      fuente: "Fórmula Reel Lynx Studios",
      plataforma: "PDF Local",
      url: "proyectos/waters-serie/referencias/formula-reel-lynxstudios.pdf",
      que_muestra: "Estructura de retención Hook -> Conflicto -> Resolución rápida -> CTA.",
      que_obtuvimos: "Plantilla base de beats para todos los guiones de 45 a 60 segundos.",
      donde_vive: "proyectos/waters-serie/referencias/formula-reel-lynxstudios.pdf",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-08",
      fecha: "2026-11-22",
      fuente: "Stack creativo video IA",
      plataforma: "Facebook / IG",
      url: "https://www.facebook.com/reel/2002879277335603",
      que_muestra: "Promesa de automatización total con herramientas pesadas de video IA (más DgBaMBZT9bB).",
      que_obtuvimos: "Auditoría honesta de capacidad de tu iMac (24 GB RAM / 2 GB VRAM) para no instalar software que traba el equipo.",
      donde_vive: "proyectos/waters-serie/INVENTARIO_ARSENAL_Y_PIPELINE_PRODUCCION.md",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-09",
      fecha: "2026-11-23",
      fuente: "woodxbt · '16 repos. One take.'",
      plataforma: "X (Twitter)",
      url: "https://x.com/woodxbt/status/2124482580896498142",
      que_muestra: "16 repositorios open source para video, UI y subtítulos sin pagar agencias.",
      que_obtuvimos: "Inventario 80/20: 4 upgrades ligeros adoptados/en camino (GSAP, onetake, WhisperX, Theatre.js), 9 en Bóveda y checklist de seguridad postinstall.",
      donde_vive: "proyectos/waters-serie/INVENTARIO_ARSENAL_Y_PIPELINE_PRODUCCION.md",
      veredicto: "Parcial",
      nota: ""
    },
    {
      id: "REF-10",
      fecha: "2026-11-23",
      fuente: "Short gamificado + soul-youtube + CapCut Pro",
      plataforma: "YouTube",
      url: "https://www.youtube.com/watch?v=1stM4GBFeqQ",
      que_muestra: "Formato juego de detección rápida con temporizador, SFX de teclado y stickers visuales.",
      que_obtuvimos: "Serie ¿Caíste o no caíste? V2 (Three.js voxel pastel sin neón) + Pack #1 Biblioteca de Ingredientes + Flujo 2 Estaciones iMac -> CapCut Pro.",
      donde_vive: "proyectos/caiste-o-no-caiste/biblioteca_ingredientes/README_FLOW_Y_BIBLIOTECA.md",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-11",
      fecha: "2026-11-26",
      fuente: "Professor Glitch (Loop 4 pasos)",
      plataforma: "Facebook",
      url: "https://www.facebook.com/share/v/1DZhe36KBy/",
      que_muestra: "Ciclo semanal Ideas -> Guion -> Antes/Después -> Push multiplataforma + regla de primeros 20 videos (con pitch a comunidad de pago al final).",
      que_obtuvimos: "Meta explícita de 20 videos publicados antes de juzgar + ángulo Antes desordenado -> Después limpio para Captoora Studio y ¡WATERS!. Se descarta comprar curso.",
      donde_vive: "proyectos/tablero-control/ (este tablero) + Estación 1 y 6",
      veredicto: "Parcial",
      nota: ""
    }
  ],

  publicados: [
    {
      id: "PUB-01",
      fecha: "2026-11-23",
      titulo: "EP06 · Hackeos en México + Clonación de Voz (BLINDA)",
      serie: "¡WATERS! Día",
      canal: "TikTok",
      vistas: 121,
      retencion_pct: null,
      guardados: null,
      comentarios_cta: null,
      dms_wa: null,
      estado: "En prueba",
      diagnostico: "Formato base anterior sin condimentos CapCut Pro (sin teclado cremoso ni stickers flotantes) y subido solo en 1 plataforma.",
      mejora_siguiente: "Replicar con subtítulos dinámicos + publicar simultáneo en Facebook (5,600 seguidores), IG Reels y YT Shorts."
    },
    {
      id: "PUB-02",
      fecha: "2026-11-23",
      titulo: "EP07 · IPO de Anthropic y Estafas Pre-IPO (BOLSA)",
      serie: "¡WATERS! Día",
      canal: "TikTok",
      vistas: 72,
      retencion_pct: null,
      guardados: null,
      comentarios_cta: null,
      dms_wa: null,
      estado: "En prueba",
      diagnostico: "Gancho inicial 0-2s más lento y tema financiero de nicho; sin contraste visual Antes desordenado -> Después limpio.",
      mejora_siguiente: "Acelerar apertura en primeros 2 segundos con prueba visual tangible en pantalla y registrar retención al segundo 3."
    }
  ],

  cola_semanal: [
    {
      orden: "01",
      archivo_cola: "01_MIE_2000_CAISTE_P4_V2.mp4",
      fecha_mx: "2026-11-25 20:00",
      serie: "¿Caíste o no caíste?",
      formato: "9:16 (1080x1920)",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels", "Facebook Reels"],
      titulo: "¿Caerás en el recibo falso de CFE? (Pon atención al reloj)",
      cta_palabra: "CAÍ / NO CAÍ / GUARDRAILS",
      lead_magnet_pdf: null,
      source_mp4: "proyectos/caiste-o-no-caiste/renders/CAISTE_SHORT_01_P4_CFE_V2_DYNAMIC.mp4",
      estado_slot: "En CapCut Pro",
      feedback: "Listo en Redmi Note 8 (01_CAISTE_SHORTS/) para agregar teclado cremoso, sticker CFE y subtítulos antes de subir."
    },
    {
      orden: "02",
      archivo_cola: "02_JUE_1200_WATERS_EP08_SAT.mp4",
      fecha_mx: "2026-11-26 12:00",
      serie: "¡WATERS! Día",
      formato: "9:16 (1080x1920)",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels", "Facebook Reels"],
      titulo: "Claude como contador vs regalar tu e.firma (.cer/.key) al SAT",
      cta_palabra: "CONTADOR",
      lead_magnet_pdf: "proyectos/waters-serie/lead_magnets/GUIA_CONTADOR_IA_SAT_CAPTOORA.pdf",
      source_mp4: "proyectos/waters-serie/renders/WATERS_CHISPA_EP08_CLAUDE_CONTADOR_SAT_60S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "03",
      archivo_cola: "03_JUE_2200_WATERS_MAD08_CUOTA.mp4",
      fecha_mx: "2026-11-26 22:00",
      serie: "Historias de Madrugada",
      formato: "9:16 (1080x1920)",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels"],
      titulo: "Es por el bien de tu cuota (cuando el bot te frena a las 2 a.m.)",
      cta_palabra: "CUOTA",
      lead_magnet_pdf: null,
      source_mp4: "proyectos/waters-serie/renders/WATERS_CHISPA_MAD08_CUOTA_45S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "04",
      archivo_cola: "04_VIE_1200_ORO_CARBON_SHORT_60S.mp4",
      fecha_mx: "2026-11-27 12:00",
      serie: "¿Oro Puro o Puro Humo?",
      formato: "9:16 (1080x1920, 73.2s)",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels", "Facebook Reels"],
      titulo: "¿Gemini 4 Carbon sí es el rey en ciberseguridad? 3 pruebas + letra chiquita",
      cta_palabra: "CARBON",
      lead_magnet_pdf: null,
      source_mp4: "proyectos/waters-serie/renders/ORO_CARBON_CIBERSEGURIDAD_SHORT_60S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "05",
      archivo_cola: "05_VIE_2000_ORO_CARBON_EXPLICATIVO_3MIN.mp4",
      fecha_mx: "2026-11-27 20:00",
      serie: "¿Oro Puro o Puro Humo? · Deep Dive",
      formato: "16:9 (1920x1080, 273.2s)",
      canales: ["YouTube Largo", "LinkedIn", "X (Twitter)"],
      titulo: "Gemini 4 Carbon vs Astra, Opus, Fable y Grok en Ciberseguridad: Fuentes y Letra Chiquita",
      cta_palabra: "AUDITA",
      lead_magnet_pdf: null,
      source_mp4: "proyectos/waters-serie/renders/ORO_CARBON_CIBERSEGURIDAD_EXPLICATIVO_3MIN.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "06",
      archivo_cola: "06_SAB_1200_WATERS_EP09_APPLE.mp4",
      fecha_mx: "2026-11-28 12:00",
      serie: "¡WATERS! Día",
      formato: "9:16 (1080x1920)",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels", "Facebook Reels"],
      titulo: "Apple Intelligence en tu iPhone: dónde termina tu privacidad y dónde va a la nube",
      cta_palabra: "APPLE",
      lead_magnet_pdf: "proyectos/waters-serie/lead_magnets/CHECKLIST_BLINDAJE_APPLE_INTELLIGENCE.pdf",
      source_mp4: "proyectos/waters-serie/renders/WATERS_CHISPA_EP09_APPLE_60S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "07",
      archivo_cola: "07_SAB_2200_WATERS_MAD09_SIRI.mp4",
      fecha_mx: "2026-11-28 22:00",
      serie: "Historias de Madrugada",
      formato: "9:16 (1080x1920)",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels"],
      titulo: "Lo que pasa cuando dejas a Siri y los permisos abiertos de madrugada",
      cta_palabra: "SIRI",
      lead_magnet_pdf: null,
      source_mp4: "proyectos/waters-serie/renders/WATERS_CHISPA_MAD09_SIRI_45S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "08",
      archivo_cola: "08_DOM_1200_WATERS_EP05_FABLE_VS_HYDROGEN.mp4",
      fecha_mx: "2026-11-29 12:00",
      serie: "¡WATERS! FinOps",
      formato: "9:16 (1080x1920)",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels"],
      titulo: "Fable vs Hydrogen: cómo no quemar tu cuota pagando cañón donde basta resortera",
      cta_palabra: "FINOPS",
      lead_magnet_pdf: null,
      source_mp4: "proyectos/waters-serie/renders/WATERS_NEON3D_EP05_FABLE5_VS_HYDROGEN_60S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "09",
      archivo_cola: "09_LUN_1200_WATERS_EP03_TONY_FINOPS.mp4",
      fecha_mx: "2026-11-30 12:00",
      serie: "¡WATERS! FinOps",
      formato: "9:16 (1080x1920)",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels"],
      titulo: "Por qué se acaba tu cuota a mitad de mes y cómo administrarla como ingeniero",
      cta_palabra: "CUOTA",
      lead_magnet_pdf: null,
      source_mp4: "proyectos/waters-serie/renders/WATERS_HYBRID_EP03_TONY_CUOTA_FINOPS_60S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    }
  ],

  mejoras_activas: [
    {
      id: "MEJ-01",
      titulo: "Gancho visual en los primeros 0-2 segundos",
      hipotesis: "Mostrar el error, recibo o captura real desde el primer cuadro sube la retención al segundo 3 frente a introducciones habladas.",
      aplicada: false
    },
    {
      id: "MEJ-02",
      titulo: "Distribución 4x por pieza (activar Facebook 5,600 seguidores)",
      hipotesis: "Subir el mismo video en TikTok, YT Shorts, IG Reels y Facebook multiplica exposición sin costo extra de producción.",
      aplicada: false
    },
    {
      id: "MEJ-03",
      titulo: "Condimentos de retención en CapCut Pro",
      hipotesis: "Sumar subtítulos cinéticos, teclado cremoso y stickers PNG sin tapar al personaje mejora el tiempo medio de vista.",
      aplicada: true
    },
    {
      id: "MEJ-04",
      titulo: "Formato Antes desordenado -> Después limpio",
      hipotesis: "Enseñar un caso real roto y su solución limpia (para Captoora Studio y ¡WATERS!) genera más guardados y DMs a WhatsApp.",
      aplicada: false
    }
  ]
};
