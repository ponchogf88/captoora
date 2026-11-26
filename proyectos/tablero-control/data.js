/* Captoora Studio & ¡WATERS! — Modelo de datos verificado v1.1 (Dark + Miniaturas + Íconos Linux) */
window.CAPTOORA_DATA = {
  schema_version: "1.1",
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
    estacion_movil: "Redmi Note 8 · CapCut Pro ($30 MXN/mes, user3733613018365)",
    plataformas_nativas: [
      { id: "tiktok", icon: "tiktok", nombre: "TikTok", url: "https://www.tiktok.com/tiktokstudio", nota: "Programa hasta 10 días adelante" },
      { id: "youtube", icon: "youtube", nombre: "YouTube", url: "https://studio.youtube.com", nota: "Shorts 9:16 y Largo 16:9" },
      { id: "meta", icon: "meta", nombre: "Meta", url: "https://business.facebook.com", nota: "IG Reels + FB Reels (5,600 seguidores)" }
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
      icon: "terminal",
      nombre: "Ideas y Filtro",
      responsable: "AGY + Tú",
      estacion: "iMac / CLI",
      entra: "Quejas de clientes, noticias y referencias/inbox/",
      que_hace: "Aplica La Prueba del Ácido (3 filtros: antirreciclado, hardware Mac y señal real)",
      entrega: "Idea etiquetada En prueba",
      cuando_se_quita: "Cuando apruebas el ángulo antes de escribir el guion",
      tiempo_estimado: "15 min/sem",
      estado: "Activo",
      detalle: "Incluye el ángulo Antes desordenado -> Después limpio para servicios de Captoora Studio y alertas ¡WATERS!."
    },
    {
      paso: 2,
      codigo: "EST-02",
      icon: "file-code",
      nombre: "Guion y Candados",
      responsable: "AGY + Tú",
      estacion: "iMac",
      entra: "Idea aprobada de Estación 1",
      que_hace: "Redacta guion 45-60s (enseña primero, producto al final; tiempos 5/7/9s en ¿Caíste?)",
      entrega: "JSON/MD con palabra CTA",
      cuando_se_quita: "Cuando das luz verde al diálogo y gancho inicial (0-2s)",
      tiempo_estimado: "20 min/pieza",
      estado: "Activo",
      detalle: "Sin inventar cifras ni prometer oro antes de probar. Define qué va en 3D, qué va en HTML y qué texto irá aparte."
    },
    {
      paso: 3,
      codigo: "EST-03",
      icon: "waveform",
      nombre: "Voz y Reloj",
      responsable: "Python + 11Labs",
      estacion: "iMac",
      entra: "Guion aprobado (texto mudo)",
      que_hace: "Genera locución por personaje, agrega SFX/cama musical y bloquea duración exacta",
      entrega: "Pista _master.wav (CLOCK)",
      cuando_se_quita: "Al validar duración y volumen exacto con ffprobe",
      tiempo_estimado: "5 min/pieza",
      estado: "Activo",
      detalle: "Cuota actual cuidada: 30,184 de 61,509 caracteres disponibles. Caché de MP3 reutilizable para no pagar dos veces."
    },
    {
      paso: 4,
      codigo: "EST-04",
      icon: "cube",
      nombre: "Visual Limpio",
      responsable: "Three.js / HyperFrames",
      estacion: "iMac",
      entra: "_master.wav + Ingredientes",
      que_hace: "Renderiza MP4 limpio (260 px libres abajo) y empuja al teléfono vía adb",
      entrega: "MP4 base en /sdcard/Movies/",
      cuando_se_quita: "Al confirmar archivo y carpeta de ingredientes en Redmi Note 8",
      tiempo_estimado: "10-15 min",
      estado: "Activo",
      detalle: "Ya tienes 29 renders MP4 en disco (25 de ¡WATERS! y 4 de ¿Caíste? + Pack #1 de 9 SFX, 4 Halos y 10 PNGs)."
    },
    {
      paso: 5,
      codigo: "EST-05",
      icon: "smartphone",
      nombre: "CapCut Pro",
      responsable: "Tú en Redmi Note 8",
      estacion: "Redmi Note 8",
      entra: "MP4 base + SFX + Halos + PNG",
      que_hace: "Agrega subtítulos dinámicos (absorbe a Captions), teclado cremoso, sticker y revisión humana",
      entrega: "MP4 final exportado",
      cuando_se_quita: "Al exportar el video final tras tu revisión cuadro a cuadro",
      tiempo_estimado: "10 min/pieza",
      estado: "Turno",
      detalle: "Aquí estás hoy con CAISTE_SHORT_01_P4_CFE_V2_DYNAMIC.mp4 en 01_CAISTE_SHORTS/ y cuenta user3733613018365."
    },
    {
      paso: 6,
      codigo: "EST-06",
      icon: "calendar",
      nombre: "Programar y Medir",
      responsable: "TikTok / YT / Meta",
      estacion: "Web gratis",
      entra: "MP4 final + títulos y CTAs",
      que_hace: "Programa bloque semanal y registra a los 7 días vistas, retención, guardados y DMs",
      entrega: "Datos que vuelven a EST-01",
      cuando_se_quita: "Al cerrar corte semanal y anotar qué se repite o descarta",
      tiempo_estimado: "15 min/sem",
      estado: "Lista",
      detalle: "Mismo video a TikTok, YouTube Shorts, Instagram Reels y Facebook (donde ya tienes 5,600 seguidores)."
    }
  ],

  relevos_banca: [
    {
      icon: "ban",
      herramienta: "Captions (app móvil)",
      estado: "Reemplazado",
      momento: "Retirado del flujo",
      motivo: "CapCut Pro ($30 MXN/mes) absorbe por completo los subtítulos dinámicos animados y efectos de texto.",
      accion: "No renovar suscripción aparte."
    },
    {
      icon: "scissors",
      herramienta: "Opus Clip",
      estado: "Fase 2",
      momento: "Hito 4 (19 Dic+)",
      motivo: "No aporta valor en Shorts 9:16 individuales. Entra al grabar episodios horizontales 16:9 de 10 min para trocearlos en 8-10 clips.",
      accion: "Usar con captions apagadas y bajar clips a EST-05."
    },
    {
      icon: "waveform",
      herramienta: "WhisperX (local)",
      estado: "Siguiente 20%",
      momento: "Fase 3 (Mac local)",
      motivo: "Alinea WAV palabra por palabra al milisegundo en CPU/M1 para editar Capa 4 en Mac sin depender solo del teléfono.",
      accion: "Activar tras completar los primeros 20 videos."
    },
    {
      icon: "layers",
      herramienta: "Theatre.js + postprocessing + Lemo-Opuscar",
      estado: "Siguiente 20%",
      momento: "Fase 3 (3D largo)",
      motivo: "Mejora cámara 3D y colorimetría en waters-3d-studio cuidando el límite de 2 GB VRAM de la iMac.",
      accion: "Sumar en episodios 16:9."
    },
    {
      icon: "archive",
      herramienta: "ComfyUI / Blender MCP / Higgsfield + n8n",
      estado: "Reserva",
      momento: "Pausado por FinOps",
      motivo: "Exigen GPU >= 12 GB VRAM o suscripción API recurrente antes de validar retención y clientes.",
      accion: "Activar solo con presupuesto de cliente."
    }
  ],

  roadmap_hitos: [
    {
      id: "H1",
      titulo: "Arranque de volumen (2 -> 11 de 20)",
      ventana: "26 Nov - 01 Dic 2026",
      esfuerzo: "1 sem · ~35 min",
      resultado_esperado: "55% de la meta sin renderizar nada nuevo",
      detalle: "Programar los 9 videos terminados en TikTok, YT Shorts, IG Reels y Facebook (5,600 seguidores)."
    },
    {
      id: "H2",
      titulo: "Completar los primeros 20 (11 -> 20)",
      ventana: "02 - 15 Dic 2026",
      esfuerzo: "2 sem · ~3 h/sem",
      resultado_esperado: "20 videos reales publicados en calle",
      detalle: "Producir 9 piezas nuevas: ¿Caíste? V2 (P2, P8), formato Antes/Después (Captoora y ¡WATERS!) y TUNEL-01 / ORO-01."
    },
    {
      id: "H3",
      titulo: "Primer corte de validación real (Día 21)",
      ventana: "16 - 18 Dic 2026",
      esfuerzo: "1 sesión · 45 min",
      resultado_esperado: "Decisión con retención, guardados y DMs",
      detalle: "Auditar los 20 videos. Descartar pirita y concentrar 80% de esfuerzo en los 2 formatos ganadores."
    },
    {
      id: "H4",
      titulo: "Escala Largo 16:9 + Opus Clip + WhisperX",
      ventana: "19 Dic 2026 - 15 Ene 2027",
      esfuerzo: "3-4 sem · continuo",
      resultado_esperado: "De 1 capítulo largo salen 8-10 Shorts",
      detalle: "Activar Opus Clip en videos de 10 min y automatizar subtítulos locales con WhisperX manteniendo revisión humana."
    }
  ],

  referencias: [
    {
      id: "REF-01",
      fecha: "2026-11-17",
      fuente: "@heytrip3",
      plataforma: "Threads",
      plat_icon: "threads",
      thumb: null,
      url: "https://www.threads.com/@heytrip3/post/Df1Pi7vkrFV",
      que_muestra: "Estructura de gancho corto y ritmo ágil para hilos convertidos en video.",
      que_obtuvimos: "Base inicial para probar aperturas directas de 2 segundos antes del guion completo.",
      donde_vive: "proyectos/waters-serie/CALENDARIO_MAESTRO_30_DIAS_WATERS.md",
      veredicto: "En prueba",
      nota: ""
    },
    {
      id: "REF-02",
      fecha: "2026-11-18",
      fuente: "Monito 3D plastilina",
      plataforma: "Instagram",
      plat_icon: "instagram",
      thumb: "thumbs/pub_02_ep07.jpg",
      url: "https://www.instagram.com/reels/DfccbDIibJE/",
      que_muestra: "Personaje 3D carismático estilo plastilina narrando temas tech sin rostro humano.",
      que_obtuvimos: "Dirección 100% sin cámara humana con casting propio (Chispa, Tony, Antigravity, Guardrails).",
      donde_vive: "proyectos/waters-serie/assets/",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-03",
      fecha: "2026-11-18",
      fuente: "Soy Vibecoder",
      plataforma: "Web / IG",
      plat_icon: "globe",
      thumb: null,
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
      fuente: "Arneses y guardrails IA",
      plataforma: "Instagram",
      plat_icon: "instagram",
      thumb: "thumbs/pub_01_ep06.jpg",
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
      fuente: "Mascota 4K en cuadro",
      plataforma: "Facebook",
      plat_icon: "facebook",
      thumb: "thumbs/slot_09_ep03_tony.jpg",
      url: "https://www.facebook.com/reel/1292935342988871",
      que_muestra: "Personaje anclado visualmente sin desarmarse ni desaparecer al mostrar pantallas.",
      que_obtuvimos: "Regla visual de mantener al personaje estable y respetar 260 px libres abajo.",
      donde_vive: "proyectos/waters-3d-studio/",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-06",
      fecha: "2026-11-20",
      fuente: "Estética nocturna (727K likes)",
      plataforma: "Instagram",
      plat_icon: "instagram",
      thumb: "thumbs/slot_03_mad08_cuota.jpg",
      url: "https://www.instagram.com/reels/Df0giB1hM_C/",
      que_muestra: "Susurros, zooms lentos, diseño sonoro suave y clima nocturno (DedIkqJla4G / Df0giB1hM_C / DfQrytINxzD).",
      que_obtuvimos: "Creación de la vertiente Historias de Madrugada (MAD08 Cuota y MAD09 Siri 2:47 AM).",
      donde_vive: "proyectos/waters-serie/ESTRATEGIA_DOS_VERTIENTES_Y_OPERACION_14_SEMANA.md",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-07",
      fecha: "2026-11-20",
      fuente: "Fórmula Reel Lynx Studios",
      plataforma: "PDF Local",
      plat_icon: "pdf",
      thumb: null,
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
      plat_icon: "facebook",
      thumb: null,
      url: "https://www.facebook.com/reel/2002879277335603",
      que_muestra: "Promesa de automatización total con herramientas pesadas de video IA (más DgBaMBZT9bB).",
      que_obtuvimos: "Auditoría honesta de capacidad de tu iMac (24 GB RAM / 2 GB VRAM) para no trabar el equipo.",
      donde_vive: "proyectos/waters-serie/INVENTARIO_ARSENAL_Y_PIPELINE_PRODUCCION.md",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-09",
      fecha: "2026-11-23",
      fuente: "woodxbt · '16 repos. One take.'",
      plataforma: "X (Twitter)",
      plat_icon: "x",
      thumb: null,
      url: "https://x.com/woodxbt/status/2124482580896498142",
      que_muestra: "16 repositorios open source para video, UI y subtítulos sin pagar agencias.",
      que_obtuvimos: "Inventario 80/20: 4 upgrades ligeros (GSAP, onetake, WhisperX, Theatre.js), 9 en Reserva y filtro postinstall.",
      donde_vive: "proyectos/waters-serie/INVENTARIO_ARSENAL_Y_PIPELINE_PRODUCCION.md",
      veredicto: "Parcial",
      nota: ""
    },
    {
      id: "REF-10",
      fecha: "2026-11-23",
      fuente: "Short gamificado + CapCut Pro",
      plataforma: "YouTube",
      plat_icon: "youtube",
      thumb: "thumbs/slot_01_caiste_p4.jpg",
      url: "https://www.youtube.com/watch?v=1stM4GBFeqQ",
      que_muestra: "Formato juego de detección rápida con temporizador, SFX de teclado y stickers visuales.",
      que_obtuvimos: "Serie ¿Caíste o no caíste? V2 (Three.js voxel pastel sin neón) + Pack #1 Ingredientes + Flujo 2 Estaciones.",
      donde_vive: "proyectos/caiste-o-no-caiste/biblioteca_ingredientes/README_FLOW_Y_BIBLIOTECA.md",
      veredicto: "Adoptado",
      nota: ""
    },
    {
      id: "REF-11",
      fecha: "2026-11-26",
      fuente: "Professor Glitch (Loop 4 pasos)",
      plataforma: "Facebook",
      plat_icon: "facebook",
      thumb: null,
      url: "https://www.facebook.com/share/v/1DZhe36KBy/",
      que_muestra: "Ciclo Ideas -> Guion -> Antes/Después -> Push multiplataforma + regla 20 videos (con pitch de pago).",
      que_obtuvimos: "Meta explícita de 20 videos antes de juzgar + ángulo Antes desordenado -> Después limpio. Sin comprar curso.",
      donde_vive: "proyectos/tablero-control/",
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
      canales: ["TikTok"],
      thumb: "thumbs/pub_01_ep06.jpg",
      vistas: 121,
      retencion_pct: null,
      guardados: null,
      comentarios_cta: null,
      dms_wa: null,
      estado: "En prueba",
      diagnostico: "Formato base anterior sin condimentos CapCut Pro (sin teclado cremoso ni stickers flotantes) y subido solo en 1 red.",
      mejora_siguiente: "Replicar con subtítulos dinámicos + publicar simultáneo en Facebook (5,600 seguidores), IG Reels y YT Shorts."
    },
    {
      id: "PUB-02",
      fecha: "2026-11-23",
      titulo: "EP07 · IPO de Anthropic y Estafas Pre-IPO (BOLSA)",
      serie: "¡WATERS! Día",
      canal: "TikTok",
      canales: ["TikTok"],
      thumb: "thumbs/pub_02_ep07.jpg",
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
      formato: "9:16 · 48.7s",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels", "Facebook Reels"],
      titulo: "¿Caerás en el recibo falso de CFE? (Pon atención al reloj)",
      cta_palabra: "CAÍ / NO CAÍ / GUARDRAILS",
      lead_magnet_pdf: null,
      thumb: "thumbs/slot_01_caiste_p4.jpg",
      source_mp4: "proyectos/caiste-o-no-caiste/renders/CAISTE_SHORT_01_P4_CFE_V2_DYNAMIC.mp4",
      estado_slot: "En CapCut Pro",
      feedback: "Listo en Redmi Note 8 (01_CAISTE_SHORTS/) para agregar teclado cremoso, sticker CFE y subtítulos antes de subir."
    },
    {
      orden: "02",
      archivo_cola: "02_JUE_1200_WATERS_EP08_SAT.mp4",
      fecha_mx: "2026-11-26 12:00",
      serie: "¡WATERS! Día",
      formato: "9:16 · 89.6s",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels", "Facebook Reels"],
      titulo: "Claude como contador vs regalar tu e.firma (.cer/.key) al SAT",
      cta_palabra: "CONTADOR",
      lead_magnet_pdf: "proyectos/waters-serie/lead_magnets/GUIA_CONTADOR_IA_SAT_CAPTOORA.pdf",
      thumb: "thumbs/slot_02_ep08_sat.jpg",
      source_mp4: "proyectos/waters-serie/renders/WATERS_CHISPA_EP08_CLAUDE_CONTADOR_SAT_60S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "03",
      archivo_cola: "03_JUE_2200_WATERS_MAD08_CUOTA.mp4",
      fecha_mx: "2026-11-26 22:00",
      serie: "Historias de Madrugada",
      formato: "9:16 · 46.0s",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels"],
      titulo: "Es por el bien de tu cuota (cuando el bot te frena a las 2 a.m.)",
      cta_palabra: "CUOTA",
      lead_magnet_pdf: null,
      thumb: "thumbs/slot_03_mad08_cuota.jpg",
      source_mp4: "proyectos/waters-serie/renders/WATERS_CHISPA_MAD08_CUOTA_45S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "04",
      archivo_cola: "04_VIE_1200_ORO_CARBON_SHORT_60S.mp4",
      fecha_mx: "2026-11-27 12:00",
      serie: "¿Oro Puro o Puro Humo?",
      formato: "9:16 · 73.2s",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels", "Facebook Reels"],
      titulo: "¿Gemini 4 Carbon sí es el rey en ciberseguridad? 3 pruebas + letra chiquita",
      cta_palabra: "CARBON",
      lead_magnet_pdf: null,
      thumb: "thumbs/slot_04_carbon_short.jpg",
      source_mp4: "proyectos/waters-serie/renders/ORO_CARBON_CIBERSEGURIDAD_SHORT_60S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "05",
      archivo_cola: "05_VIE_2000_ORO_CARBON_EXPLICATIVO_3MIN.mp4",
      fecha_mx: "2026-11-27 20:00",
      serie: "¿Oro Puro o Puro Humo? · Deep Dive",
      formato: "16:9 · 273.2s",
      canales: ["YouTube Largo", "LinkedIn", "X (Twitter)"],
      titulo: "Gemini 4 Carbon vs Astra, Opus, Fable y Grok en Ciberseguridad: Fuentes y Letra Chiquita",
      cta_palabra: "AUDITA",
      lead_magnet_pdf: null,
      thumb: "thumbs/slot_05_carbon_3min.jpg",
      source_mp4: "proyectos/waters-serie/renders/ORO_CARBON_CIBERSEGURIDAD_EXPLICATIVO_3MIN.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "06",
      archivo_cola: "06_SAB_1200_WATERS_EP09_APPLE.mp4",
      fecha_mx: "2026-11-28 12:00",
      serie: "¡WATERS! Día",
      formato: "9:16 · 60.0s",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels", "Facebook Reels"],
      titulo: "Apple Intelligence en tu iPhone: dónde termina tu privacidad y dónde va a la nube",
      cta_palabra: "APPLE",
      lead_magnet_pdf: "proyectos/waters-serie/lead_magnets/CHECKLIST_BLINDAJE_APPLE_INTELLIGENCE.pdf",
      thumb: "thumbs/slot_06_ep09_apple.jpg",
      source_mp4: "proyectos/waters-serie/renders/WATERS_CHISPA_EP09_APPLE_60S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "07",
      archivo_cola: "07_SAB_2200_WATERS_MAD09_SIRI.mp4",
      fecha_mx: "2026-11-28 22:00",
      serie: "Historias de Madrugada",
      formato: "9:16 · 46.0s",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels"],
      titulo: "Lo que pasa cuando dejas a Siri y los permisos abiertos de madrugada",
      cta_palabra: "SIRI",
      lead_magnet_pdf: null,
      thumb: "thumbs/slot_07_mad09_siri.jpg",
      source_mp4: "proyectos/waters-serie/renders/WATERS_CHISPA_MAD09_SIRI_45S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "08",
      archivo_cola: "08_DOM_1200_WATERS_EP05_FABLE_VS_HYDROGEN.mp4",
      fecha_mx: "2026-11-29 12:00",
      serie: "¡WATERS! FinOps",
      formato: "9:16 · 96.4s",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels"],
      titulo: "Fable vs Hydrogen: cómo no quemar tu cuota pagando cañón donde basta resortera",
      cta_palabra: "FINOPS",
      lead_magnet_pdf: null,
      thumb: "thumbs/slot_08_ep05_fable.jpg",
      source_mp4: "proyectos/waters-serie/renders/WATERS_NEON3D_EP05_FABLE5_VS_HYDROGEN_60S.mp4",
      estado_slot: "Listo en disco",
      feedback: ""
    },
    {
      orden: "09",
      archivo_cola: "09_LUN_1200_WATERS_EP03_TONY_FINOPS.mp4",
      fecha_mx: "2026-11-30 12:00",
      serie: "¡WATERS! FinOps",
      formato: "9:16 · 93.2s",
      canales: ["TikTok", "YouTube Shorts", "Instagram Reels"],
      titulo: "Por qué se acaba tu cuota a mitad de mes y cómo administrarla como ingeniero",
      cta_palabra: "CUOTA",
      lead_magnet_pdf: null,
      thumb: "thumbs/slot_09_ep03_tony.jpg",
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
