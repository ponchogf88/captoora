/* ==========================================================================
   CAPTOORA STUDIO HQ — 7 AGENTS GAME SIMULATION, EMPRESA VIEW, ASANA HUB,
   HUMAN TRIGGER APPROVAL QUEUE & 72-HOUR SPRINT COUNTDOWN
   ========================================================================== */

(function () {
  'use strict';

  const LOCAL_STORAGE_KEY = 'captoora_studio_workspace_v1';

  function detectApiBase() {
    if (window.location.protocol.startsWith('http')) {
      return window.location.origin;
    }
    return 'http://127.0.0.1:8765';
  }

  const API_BASE = detectApiBase();

  // Default fallback seed matching dashboard/data/*.json for instant file:// usability
  const DEFAULT_WORKSPACE = {
    server_online: false,
    roster: {
      agents: [
        {
          id: 'chief_of_staff',
          number: 1,
          name: 'Director de Orquesta (Chief of Staff)',
          role_title: 'Estratega & Coordinador General',
          single_job: 'Priorizar el primer "Sí" en 72 horas, delegar entre los 6 bots especialistas y consolidar tu Bandeja de Último Trigger.',
          schedule_label: 'Bajo demanda + Resumen Diario 08:30',
          status: 'ready',
          last_run: '2026-11-15T05:53:57-06:00',
          tools: ['subagents(2..7)', 'projects_asana.json', 'approval_queue.json'],
          safety_boundary: 'Nunca aprueba acciones externas en tu nombre; solo organiza prioridades.'
        },
        {
          id: 'scouting_radar',
          number: 2,
          name: 'Scouting & Radar NL',
          role_title: 'Prospección Apify & Calendario Temporada',
          single_job: 'Extraer y calificar clubes de pádel, academias de danza y boxes en San Pedro y MTY (Torneos del Pavo y Galas).',
          schedule_label: 'Lunes y Jueves 09:00 + Bajo demanda',
          status: 'ready',
          last_run: '2026-11-15T05:53:57-06:00',
          tools: ['apify_scraped_leads.json', 'run_apify_production.py', 'search_web'],
          safety_boundary: 'Solo lectura y calificación; no inicia contacto.'
        },
        {
          id: 'embudo_marketing',
          number: 3,
          name: 'Marketing & Embudo Invisible',
          role_title: 'Arquitectura Pull, Ofertas Autofinanciables & Dossiers',
          single_job: 'Convertir objeciones de gasto en inversiones de estatus riesgo cero (patrocinadores en pádel / preventa en danza).',
          schedule_label: 'Martes 10:00 + Bajo demanda',
          status: 'ready',
          last_run: '2026-11-15T05:53:57-06:00',
          tools: ['ARQUITECTURA_EMBUDO_INVISIBLE_CAPTOORA.md', 'enqueue_human_trigger'],
          safety_boundary: '0% mención IA, sin "presumir" y protección taller 3-5 días.'
        },
        {
          id: 'social_content',
          number: 4,
          name: 'Redes Sociales & Marca (@captoora)',
          role_title: 'Guiones Reels 9:16, Stories & Carruseles',
          single_job: 'Redactar copys mostrando entrega el mismo día y reconocimientos en acrílico óptico iluminados con luz LED cálida.',
          schedule_label: 'Miércoles y Sábado 11:00',
          status: 'waiting_trigger',
          last_run: '2026-11-15T05:53:57-06:00',
          tools: ['assets/portfolio/manifest.json', 'enqueue_human_trigger'],
          safety_boundary: 'Solo encola piezas para tu revisión; no publica directo.'
        },
        {
          id: 'ventas_outreach',
          number: 5,
          name: 'Ventas B2B & Cierre 3 Días',
          role_title: 'WhatsApp Directo, Pixieset Email & Seguimiento 72h',
          single_job: 'Preparar mensajes diagnósticos hiper-personalizados (Torneo del Pavo $12.5k, Gala $14.5k, Sponsor Proof $18.5k).',
          schedule_label: 'Sprint Diario 09:30 & 16:00',
          status: 'waiting_trigger',
          last_run: '2026-11-15T05:53:57-06:00',
          tools: ['apify_scraped_leads.json', 'whatsapp_quick_replies.md', 'enqueue_human_trigger'],
          safety_boundary: 'Bloqueo duro SDK: todo borrador pasa por Tu Último Trigger.'
        },
        {
          id: 'contabilidad_finanzas',
          number: 6,
          name: 'Contabilidad, Cotizaciones & Margen',
          role_title: 'Control de Caja, Maquila, Suscripciones & SAT/CFDI',
          single_job: 'Auditar márgenes (>=70%), validar 50% anticipo / 50% entrega y controlar suscripciones SaaS (Pixieset, Apify).',
          schedule_label: 'Viernes 18:00 + Por cotización',
          status: 'ready',
          last_run: '2026-11-15T05:53:57-06:00',
          tools: ['cotizaciones_y_tarifario.md', 'accounting_ledger.json'],
          safety_boundary: 'No realiza cargos ni timbrados automáticos.'
        },
        {
          id: 'ops_talleres_legal',
          number: 7,
          name: 'Operaciones, Talleres LED & Legal',
          role_title: 'Logística Halftime Blitz, Proveedores & Contratos',
          single_job: 'Separar entrega digital mismo día vs 3-5 días hábiles en talleres locales y blindar derechos morales.',
          schedule_label: 'Pre-evento T-72h / Post-cierre',
          status: 'waiting_trigger',
          last_run: '2026-11-15T05:53:57-06:00',
          tools: ['revision_contratos_guia.md', 'manual_tecnico_courtside.md'],
          safety_boundary: 'Protege cláusula 50/50 y SLAs reales de taller.'
        },
        {
          id: 'marky_marketing',
          number: 8,
          name: 'Marky (Director de Marketing)',
          role_title: 'Director de Marketing, 2x Google Pro & Suscripciones',
          single_job: 'Dirigir a Lupe y Conan sin cuotas Grokbot, sincronizar Dual Google Pro ($395 + $99 Yari), salvar OpusClip Pro y armar Brief Meta Muse móvil.',
          schedule_label: 'Motor Local 0 Cuotas + 08:45',
          status: 'ready',
          last_run: '2026-11-16T03:16:00-06:00',
          tools: ['marketing_hub.py', 'generate_subscription_content_plan', 'muse_mobile_sync'],
          safety_boundary: '100% local sin Grokbot; 0% IA hacia clientes.'
        },
        {
          id: 'lupe_social',
          number: 9,
          name: 'Lupe (Redes, Meta Suite & DMs)',
          role_title: 'Meta Business Suite, TikTok, LinkedIn & DMs (Bajo Marky)',
          single_job: 'Programar IG/FB Meta Business Suite, TikTok y LinkedIn, redactar captions y preparar respuestas a mensajes bajo Trigger Humano.',
          schedule_label: 'Parrilla Semanal + Inbox Diario',
          status: 'waiting_trigger',
          last_run: '2026-11-16T03:16:00-06:00',
          tools: ['marketing_studio.json', 'prepare_lupe_social_post', 'Meta Business Suite'],
          safety_boundary: 'Jamás publica ni responde sin Tu Último Trigger.'
        },
        {
          id: 'conan_content',
          number: 10,
          name: 'Conan (Creación de Contenido)',
          role_title: 'Productor Creativo & Suscripciones (Bajo Marky -> Lupe)',
          single_job: 'Crear piezas para Lupe usando OpusClip Pro (urgente), Captions, Canva, Aftershoot, Evoto, CapCut y motor local.',
          schedule_label: 'Producción Continua -> Lupe',
          status: 'ready',
          last_run: '2026-11-16T03:16:00-06:00',
          tools: ['OpusClip Pro', 'Captions + Canva + CapCut', 'assign_conan_creative_brief'],
          safety_boundary: 'Entrega briefs y piezas en assets/; Lupe gestiona calendario.'
        }
      ]
    },
    whatsapp_cloud: {
      mode: 'wa_me_fallback',
      missing_env: ['WHATSAPP_CLOUD_API_TOKEN', 'WHATSAPP_PHONE_NUMBER_ID']
    },
    asana: {
      sprint: {
        name: "Sprint Cierre Martes 12:00 PM: 1 a 3 Clientes Cerrados ('Sí' Firmado + 50% Anticipo)",
        started_at: '2026-11-15T05:53:57-06:00',
        deadline_at: '2026-11-17T12:00:00-06:00',
        tuesday_noon_label: 'Martes 17 Nov · 12:00 PM (Monterrey CST)',
        target_deals_min: 1,
        target_deals_max: 3,
        goal_revenue_mxn: 12500
      },
      projects: [
        { id: 'proj_sprint_padel', name: '1. Sprint 72h — Pádel San Pedro', priority: 'Crítica', objective: 'Cerrar 1 Torneo del Pavo autofinanciable ($12,500 MXN).' },
        { id: 'proj_galas_danza', name: '2. Galas Navideñas (Danza)', priority: 'Alta', objective: 'Activar preventa White-Glove de marcos Fine Art.' },
        { id: 'proj_social_embudo', name: '3. Motor Inbound (@captoora)', priority: 'Alta', objective: 'Mostrar acrílicos iluminados LED y entrega el mismo día.' },
        { id: 'proj_corp_b2b', name: '4. Corporativos & Sponsor Proof', priority: 'Media-Alta', objective: 'Posadas empresariales con respaldo FEMSA/Tecate/PJENL.' },
        { id: 'proj_finanzas_ops', name: '5. Finanzas SAT, Talleres & Legal', priority: 'Permanente', objective: 'Márgenes >=74%, anticipo 50% y taller Foco Lab / San Pedro.' }
      ],
      tasks: [
        { id: 'TASK-101', project_id: 'proj_sprint_padel', title: 'Borradores Caballo de Troya (Patrocinador + Acrílicos LED) para Cuatro Padel y Padel GM', assigned_agent: 'ventas_outreach', status: 'waiting_trigger', priority: 'Crítica', due_label: 'Hoy (T-68h)', deliverable_ref: 'APR-001, APR-002' },
        { id: 'TASK-102', project_id: 'proj_sprint_padel', title: 'Acercamiento diagnóstico PADELBOSS y SB Pádel ($12.5k)', assigned_agent: 'ventas_outreach', status: 'waiting_trigger', priority: 'Crítica', due_label: 'Hoy (T-64h)', deliverable_ref: 'APR-003' },
        { id: 'TASK-103', project_id: 'proj_sprint_padel', title: 'Enriquecer coordinación deportiva Club Sierra Madre y Deportivo San Agustín', assigned_agent: 'scouting_radar', status: 'in_progress', priority: 'Alta', due_label: 'Día 2 (T-48h)', deliverable_ref: 'apify_scraped_leads.json' },
        { id: 'TASK-104', project_id: 'proj_sprint_padel', title: 'Seguimiento regla 24-48h + Orden de anticipo 50%', assigned_agent: 'chief_of_staff', status: 'backlog', priority: 'Crítica', due_label: 'Día 3 (T-18h)', deliverable_ref: 'Orden Captoora' },
        { id: 'TASK-201', project_id: 'proj_galas_danza', title: 'Propuesta White-Glove para The Movement Dance Project', assigned_agent: 'embudo_marketing', status: 'waiting_trigger', priority: 'Alta', due_label: 'Hoy (Día 1)', deliverable_ref: 'APR-004' },
        { id: 'TASK-202', project_id: 'proj_galas_danza', title: 'Confirmar cupo molduras El Marco San Pedro (ventana 3-5 días)', assigned_agent: 'ops_talleres_legal', status: 'in_progress', priority: 'Alta', due_label: 'Día 2', deliverable_ref: 'Checklist Proveedores' },
        { id: 'TASK-301', project_id: 'proj_social_embudo', title: 'Reel 9:16 y caption acrílicos LED + entrega mismo día', assigned_agent: 'social_content', status: 'waiting_trigger', priority: 'Alta', due_label: 'Día 2', deliverable_ref: 'APR-005' },
        { id: 'TASK-401', project_id: 'proj_corp_b2b', title: 'Campaña Pixieset Posadas Corporativas (respaldo FEMSA/Tecate/PJENL)', assigned_agent: 'embudo_marketing', status: 'backlog', priority: 'Media-Alta', due_label: 'Día 3', deliverable_ref: 'Pixieset' },
        { id: 'TASK-501', project_id: 'proj_finanzas_ops', title: 'Validar margen Paquete Torneo del Pavo ($12.5k vs $2.4k = 80.8%)', assigned_agent: 'contabilidad_finanzas', status: 'done', priority: 'Alta', due_label: 'Completado', deliverable_ref: 'accounting_ledger.json' },
        { id: 'TASK-502', project_id: 'proj_finanzas_ops', title: 'Blindar Orden de Servicio (50/50, autoría moral y nota 3-5 días LED)', assigned_agent: 'ops_talleres_legal', status: 'waiting_trigger', priority: 'Alta', due_label: 'Hoy (Día 1)', deliverable_ref: 'APR-006' }
      ]
    },
    approvals: {
      items: [
        {
          id: 'APR-001',
          agent_id: 'ventas_outreach',
          task_id: 'TASK-101',
          target_name: 'Cuatro Padel (San Pedro Garza García)',
          niche: 'Pádel & Raqueta',
          channel: 'WhatsApp Directo (+52 81 2354 5695)',
          phone: '528123545695',
          package_ref: '4. Torneo del Pavo & Posada Pádel ($12,500 MXN)',
          financial_impact_mxn: 12500,
          estimated_margin_pct: 80.8,
          compliance_flags: ['0% mención IA', "Sin palabra 'presumir'", 'Diagnóstico no-venta', 'Nota taller 3-5d'],
          draft_text: 'Hola, buen día al equipo directivo de Cuatro Padel. Te saluda el equipo de Captoora Sports aquí en San Jerónimo. Al revisar el calendario de cierre de año en San Pedro, vimos que se acercan los Torneos del Pavo y Posadas de socios. Queremos hacerles una consulta breve: ¿tienen ya resuelta la entrega de galería el mismo día para proyectar en redes sociales una imagen profesional al nivel de excelencia de su club y un dossier visual para justificar renovación a sus patrocinadores 2027? Armamos un esquema autofinanciado con los mismos sponsors que incluye 4 trofeos escultóricos en acrílico óptico iluminado con base LED cálida (dejando atrás diplomas de papel o piezas anticuadas).* ¿Te puedo compartir el PDF de 1 minuto para revisarlo?\n\n*Cobertura digital el mismo día; manufactura artesanal en taller local: 3 a 5 días hábiles o entrega en ceremonia.',
          status: 'pending_trigger',
          created_at: '2026-11-15T05:54:00-06:00'
        },
        {
          id: 'APR-002',
          agent_id: 'ventas_outreach',
          task_id: 'TASK-101',
          target_name: 'Padel GM (Av. Gómez Morín, San Pedro)',
          niche: 'Pádel & Raqueta',
          channel: 'WhatsApp Directo (+52 81 1538 7900)',
          phone: '528115387900',
          package_ref: '4. Torneo del Pavo & Posada Pádel ($12,500 MXN)',
          financial_impact_mxn: 12500,
          estimated_margin_pct: 80.8,
          compliance_flags: ['0% mención IA', "Sin palabra 'presumir'", 'Autofinanciado sponsor'],
          draft_text: 'Hola, buen día al equipo de Padel GM. Les escribe Captoora Sports (San Jerónimo / San Pedro). Sabemos que en su Torneo Navideño y posada anual los patrocinadores buscan exposición tangible y los socios agradecen tener sus fotos antes de que acabe la premiación. Preparamos un formato que se paga con el patrocinio de premiación: entrega fotográfica el mismo día para proyectar en redes sociales una imagen profesional al nivel de excelencia de su club, más reconocimientos en acrílico óptico con base de luz LED cálida grabados con la marca del patrocinador.* ¿Con quién de coordinación comercial podemos revisar la propuesta de 1 hoja esta semana?\n\n*Cobertura digital en tiempo real el día del evento; piezas acrílicas LED en taller especializado: 3 a 5 días hábiles.',
          status: 'pending_trigger',
          created_at: '2026-11-15T05:54:00-06:00'
        },
        {
          id: 'APR-003',
          agent_id: 'ventas_outreach',
          task_id: 'TASK-102',
          target_name: 'PADELBOSS & SB Pádel (Lote Prioritario 2)',
          niche: 'Pádel & Raqueta',
          channel: 'WhatsApp Directo (+52 81 8691 7694)',
          phone: '528186917694',
          package_ref: '4. Torneo del Pavo & Posada Pádel ($12,500 MXN)',
          financial_impact_mxn: 12500,
          estimated_margin_pct: 80.8,
          compliance_flags: ['0% mención IA', "Sin palabra 'presumir'", 'Respaldo NL'],
          draft_text: 'Hola, buen día al equipo de PADELBOSS. En Captoora Sports hemos cubierto producciones institucionales para Coca-Cola FEMSA, Heineken y Poder Judicial NL, y hoy estamos apoyando clubes de San Pedro en su Posada y Torneo del Pavo. Nuestra diferencia no es solo la fotografía de acción en cancha: entregamos selección curada el mismo día para proyectar en redes sociales una imagen profesional al nivel de excelencia de su club y creamos trofeos escultóricos en acrílico óptico con luz LED cálida* autofinanciados por sus patrocinadores de cancha. ¿Tienen ya asignado el proveedor visual para su evento de cierre de año?',
          status: 'pending_trigger',
          created_at: '2026-11-15T05:54:00-06:00'
        },
        {
          id: 'APR-004',
          agent_id: 'embudo_marketing',
          task_id: 'TASK-201',
          target_name: 'The Movement Dance Project (Chipinque, San Pedro)',
          niche: 'Baile & Danza Señoras',
          channel: 'WhatsApp Directo (+52 81 2721 4413)',
          phone: '528127214413',
          package_ref: '5. Gala Navideña & Recuerdo de Invierno ($14,500 MXN)',
          financial_impact_mxn: 14500,
          estimated_margin_pct: 78.6,
          compliance_flags: ['White-Glove riesgo cero', '0% mención IA', "Sin palabra 'presumir'"],
          draft_text: "Buenas tardes al equipo de The Movement Dance Project. Les saluda Captoora Studio desde San Jerónimo. Admiramos el nivel escénico de sus montajes y sabemos el reto logístico que implican las galas de fin de año con las familias. Diseñamos un esquema 'White-Glove' donde la academia no arriesga presupuesto: nosotros montamos un mini-estudio editorial en backstage y las familias interesadas pre-ordenan en línea su Set Conmemorativo en marco de madera fina (El Marco San Pedro) o placa acrílica con luz LED cálida.* La academia recibe la cobertura institucional el mismo día para proyectar en redes sociales una imagen profesional al nivel de excelencia de su escuela. ¿Nos permiten enviarles la muestra visual en PDF?\n\n*Galería digital en tiempo real el día de la gala; marcos y placas LED en taller artesanal: 3 a 5 días hábiles previos a Navidad.",
          status: 'pending_trigger',
          created_at: '2026-11-15T05:54:00-06:00'
        },
        {
          id: 'APR-005',
          agent_id: 'social_content',
          task_id: 'TASK-301',
          target_name: 'Instagram Reels & LinkedIn B2B (@captoora)',
          niche: 'Marca & Bucle Viral',
          channel: 'Publicación Orgánica 9:16',
          phone: '',
          package_ref: 'Posicionamiento Embudo Invisible',
          financial_impact_mxn: 0,
          estimated_margin_pct: 100.0,
          compliance_flags: ['0% mención IA', 'Enfoque lujo/estatus', 'Nota fina 3-5d'],
          draft_text: 'GUIÓN REEL (18s): Plano detalle de acrílico óptico encendiéndose con base LED cálida sobre madera + corte rápido a acción congelada a 1/2000s.\n\nCAPTION: Un diploma de papel o una carpeta olvidada en Drive no reflejan el nivel de su torneo ni el valor de sus patrocinadores. Entrega digital el mismo día para proyectar en redes sociales una imagen profesional al nivel de excelencia de su club, y piezas escultóricas de colección en acrílico óptico iluminado para quienes conquistan la cancha.*\n\n*Cobertura digital en vivo el mismo día; manufactura de acrílicos LED y enmarcado fino en taller local: 3 a 5 días hábiles. Agenda Nov–Dic abierta: @captoora.studio · captoora.studio/sports',
          status: 'pending_trigger',
          created_at: '2026-11-15T05:54:00-06:00'
        },
        {
          id: 'APR-006',
          agent_id: 'ops_talleres_legal',
          task_id: 'TASK-502',
          target_name: 'Orden de Servicio Estándar & Checklist Talleres NL',
          niche: 'Operación Interna',
          channel: 'Documento Legal + Taller Local',
          phone: '',
          package_ref: 'Blindaje Contractual + Foco Lab / El Marco San Pedro',
          financial_impact_mxn: 0,
          estimated_margin_pct: 100.0,
          compliance_flags: ['50% anticipo', 'Derechos morales Captoora', 'Ventana 3-5d taller'],
          draft_text: 'CLÁUSULA LISTA PARA ENVIAR AL PRIMER "SÍ":\n1) Anticipo 50% para bloqueo firme de fecha y 50% contra entrega de galería digital.\n2) Entrega digital el mismo día garantizada directamente por Captoora Sports.\n3) Piezas físicas (acrílicos ópticos con luz LED cálida / marcos de madera maciza): taller local de 3 a 5 días hábiles.\n4) Captoora conserva derechos morales de autoría y licencia de portafolio.',
          status: 'pending_trigger',
          created_at: '2026-11-15T05:54:00-06:00'
        }
      ]
    },
    accounting: {
      payment_policy: '50% anticipo obligatorio al reservar fecha + 50% contra entrega de galería digital final.',
      tax_regime_note: 'CFDI 4.0 listo para corporativos y clubes A.C. de San Pedro y Monterrey.',
      packages_catalog: [
        { id: 'PKG-4', name: 'Torneo del Pavo & Posada Pádel', price_mxn: 12500, direct_cost_mxn: 2400, margin_pct: 80.8, digital_sla: 'Halftime Blitz mismo día', physical_sla: '3-5 días hábiles taller LED' },
        { id: 'PKG-5', name: 'Gala Navideña (Danza & Baile)', price_mxn: 14500, direct_cost_mxn: 3100, margin_pct: 78.6, digital_sla: 'Brindis de clausura', physical_sla: '3-5 días hábiles El Marco San Pedro' },
        { id: 'PKG-3', name: 'Sponsor Proof & BTL Corporativo', price_mxn: 18500, direct_cost_mxn: 2800, margin_pct: 84.9, digital_sla: '24h / mismo día', physical_sla: '3-5 días hábiles Carbon4 + San Pedro' }
      ],
      modular_options_matrix: {
        seasonal_discount_pct: 35,
        seasonal_promo_label: '-35% Descuento de Temporada · Navidad & Fin de Año 2026',
        tiers: [
          {
            id: 'OPT-DIGITAL',
            option_num: 1,
            title: 'Solo Fotografía Digital (Mismo Día / Halftime)',
            prices_by_niche: { padel_gym: 4900, danza_colegios: 5500, corp_btl: 6900 },
            seasonal_prices_35_by_niche: { padel_gym: 3185, danza_colegios: 3575, corp_btl: 4485 },
            direct_cost_mxn: 350,
            digital_sla: '10–15 fotos Halftime (15 min) + galería completa mismo día',
            physical_sla: 'Sin elementos físicos obligatorios (upgrade disponible en cualquier momento)',
            deferred_split: { enabled: false, phase_1_digital_mxn: 4900, phase_2_physical_mxn: 0 }
          },
          {
            id: 'OPT-PRINT',
            option_num: 2,
            title: 'Fotografía + Impresión / Marcos Finos',
            prices_by_niche: { padel_gym: 7900, danza_colegios: 8900, corp_btl: 10500 },
            seasonal_prices_35_by_niche: { padel_gym: 5135, danza_colegios: 5785, corp_btl: 6825 },
            direct_cost_mxn: 1600,
            digital_sla: 'Galería en vivo mismo día + reels verticales 9:16',
            physical_sla: '3 a 5 días hábiles (El Marco San Pedro / Foco Lab Fine Art o 2 placas LED)',
            deferred_split: { enabled: true, phase_1_digital_mxn: 4900, phase_2_physical_mxn: 3000 }
          },
          {
            id: 'OPT-FULL-LED',
            option_num: 3,
            title: 'Suite Completa + Ads & Acrílicos LED',
            prices_by_niche: { padel_gym: 11500, danza_colegios: 12500, corp_btl: 15900 },
            seasonal_prices_35_by_niche: { padel_gym: 7475, danza_colegios: 8125, corp_btl: 10335 },
            direct_cost_mxn: 2400,
            digital_sla: 'Halftime Blitz mismo día + Reels listos para Meta Ads',
            physical_sla: '3 a 5 días hábiles (4 acrílicos LED cálida + 20 llaveros; pagaderos en 2do momento)',
            deferred_split: { enabled: true, phase_1_digital_mxn: 5900, phase_2_physical_mxn: 5600 }
          }
        ]
      },
      biogen_pilot_catalog: {
        program_name: 'Captoora Biogen (Beta)',
        seasonal_discount_pct: 35,
        cadences: ['semanal', 'quincenal', 'mensual', 'bimestral'],
        durations: [
          { id: 'BIOGEN-3M', label: '3 Meses (Reto 12 semanas)', months: 3, beta_monthly_mxn: 1950, annual_discount_pct: 0 },
          { id: 'BIOGEN-6M', label: '6 Meses (Transformación Semestral)', months: 6, beta_monthly_mxn: 1750, annual_discount_pct: 10 },
          { id: 'BIOGEN-9M', label: '9 Meses (Preparación Competencia)', months: 9, beta_monthly_mxn: 1600, annual_discount_pct: 18 },
          { id: 'BIOGEN-12M', label: '1 Año / 12 Meses (Ciclo Completo)', months: 12, beta_monthly_mxn: 1450, annual_discount_pct: 25 },
          { id: 'BIOGEN-24M', label: '2 Años / 24 Meses (Atleta Pro)', months: 24, beta_monthly_mxn: 1290, annual_discount_pct: 34 },
          { id: 'BIOGEN-60M', label: '5 Años / 60 Meses (Membresía Fundador Beta)', months: 60, beta_monthly_mxn: 1150, annual_discount_pct: 41 }
        ]
      },
      small_business_catalog: {
        program_name: 'Captoora Small Business',
        seasonal_discount_pct: 35,
        tiers: [
          { id: 'SMB-MAPS', title: 'Impulso Google Maps & Portada 2027', list_price_mxn: 6000, promo_price_mxn: 3900, direct_cost_mxn: 300, margin_pct: 92.3 },
          { id: 'SMB-TOTAL', title: 'Suite Small Business Total (Maps + Meta Business)', list_price_mxn: 10600, promo_price_mxn: 6890, direct_cost_mxn: 450, margin_pct: 93.5 },
          { id: 'SMB-SUITE-2027', title: 'Posicionamiento 2027 + Físico QR LED / Biogen Beta', list_price_mxn: 16000, promo_price_mxn: 10400, direct_cost_mxn: 1450, margin_pct: 86.1 }
        ]
      },
      subscriptions_watchlist: [
        { service: 'Pixieset Email Campaigns', status: 'Activa (Pagada)', role: 'Campañas B2B con tracking', owner_agent: 'contabilidad_finanzas' },
        { service: 'Apify Google Maps Scraper', status: 'Activa ($5 crédito/mes)', role: 'Extracción continua NL', owner_agent: 'scouting_radar' },
        { service: 'Gemini API (Google Antigravity SDK)', status: 'Bajo demanda / Controlado', role: 'Motor 7 Bots Localhost', owner_agent: 'contabilidad_finanzas' }
      ]
    },
    usage_telemetry: {
      semaphore: 'verde',
      action_hint: 'Operación saludable: puedes ejecutar auditorías y campañas bajo demanda con normalidad.',
      tokens: { input: 0, cache_read: 0, output: 0, total: 0, budget: 250000, pct: 0 },
      cost_approx: { usd: 0, mxn: 0, usd_limit: 5.0, usd_pct: 0 },
      activity: { sdk_sessions: 0, model_steps: 0, tool_calls: 0 },
      whatsapp_quota: { month_used: 0, monthly_free_limit: 1000, pct: 0 },
      limits: { dry_run_preferred: false, daily_token_budget: 250000, monthly_whatsapp_limit: 1000, daily_usd_limit: 5.0 }
    },
    gmaps_audits: {
      updated_at: null,
      total_leads: 138,
      total_audited: 0,
      deficient_count: 0,
      captured_count: 0,
      streetview_count: 0,
      zero_photos_count: 0,
      unclaimed_count: 0,
      audits: []
    },
    events: {
      studio_mode: 'idle_ready',
      events: [
        { id: 'EVT-007', timestamp: '2026-11-15T05:54:30-06:00', agent_id: 'ops_talleres_legal', target_agent: 'trigger_gate', zone: 'taller_led', action: 'Blindaje Legal & Talleres', detail: 'Verificó ventana 3-5 días en Foco Lab / El Marco San Pedro y derechos morales (APR-006).', source: 'workspace_init' },
        { id: 'EVT-006', timestamp: '2026-11-15T05:54:25-06:00', agent_id: 'social_content', target_agent: 'trigger_gate', zone: 'estudio_social', action: 'Guión Reel Acrílicos LED', detail: 'Preparó pieza 9:16 contrastando entrega mismo día vs trofeos LED cálidos (APR-005).', source: 'workspace_init' },
        { id: 'EVT-005', timestamp: '2026-11-15T05:54:20-06:00', agent_id: 'ventas_outreach', target_agent: 'trigger_gate', zone: 'trigger_gate', action: 'Encoló Borradores Tier-1', detail: 'Estacionó APR-001..APR-003 esperando Tu Último Trigger hacia clubes de Pádel.', source: 'workspace_init' },
        { id: 'EVT-004', timestamp: '2026-11-15T05:54:15-06:00', agent_id: 'embudo_marketing', target_agent: 'ventas_outreach', zone: 'atelier_embudo', action: 'Filtro Caballo de Troya', detail: 'Estructuró ofertas riesgo cero pagadas por patrocinadores y preventa White-Glove.', source: 'workspace_init' },
        { id: 'EVT-003', timestamp: '2026-11-15T05:54:10-06:00', agent_id: 'contabilidad_finanzas', target_agent: 'chief_of_staff', zone: 'boveda_finanzas', action: 'Auditoría Márgenes', detail: 'Validó 80.8% margen en Torneo del Pavo ($12,500 MXN vs $2,400 maquila).', source: 'workspace_init' },
        { id: 'EVT-002', timestamp: '2026-11-15T05:54:05-06:00', agent_id: 'scouting_radar', target_agent: 'ventas_outreach', zone: 'radar_maps', action: 'Priorización Leads Apify', detail: 'Entregó Cuatro Padel, Padel GM, PADELBOSS y The Movement al equipo de Ventas.', source: 'workspace_init' },
        { id: 'EVT-001', timestamp: '2026-11-15T05:54:00-06:00', agent_id: 'chief_of_staff', target_agent: 'ventas_outreach', zone: 'mesa_directiva', action: 'Despliegue Sprint 72h', detail: 'Activó meta de cierre del primer "Sí" en San Pedro antes del 18 de Noviembre.', source: 'workspace_init' }
      ]
    }
  };

  let workspaceState = loadOfflineOrDefaultState();
  let selectedAgentId = 'chief_of_staff';
  let currentDisplayMode = 'game';
  let showApprovalHistory = false;
  let serverOnline = false;
  let countdownInterval = null;
  let pollInterval = null;

  // Guardrail copy check for client edits inside browser
  function checkClientCopyGuardrail(text) {
    const violations = [];
    if (/\b(inteligencia\s+artificial|i\.?\s*a\.?)\b/i.test(text || '')) {
      violations.push('No incluyas referencias a "IA" / "Inteligencia Artificial" en mensajes hacia clientes.');
    }
    if (/\bpresum[a-z]*\b/i.test(text || '')) {
      violations.push('Sustituye la palabra "presumir" por "proyectar imagen profesional / nivel de excelencia".');
    }
    return violations;
  }

  function showToast(message) {
    const el = document.getElementById('captooraToast');
    if (!el) return;
    el.textContent = message;
    el.classList.add('visible');
    clearTimeout(el._hideTimer);
    el._hideTimer = setTimeout(() => el.classList.remove('visible'), 3600);
  }

  function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  function loadOfflineOrDefaultState() {
    try {
      const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && parsed.roster && parsed.asana && parsed.approvals) {
          if (parsed.asana.sprint && parsed.asana.sprint.deadline_at === '2026-11-18T05:53:57-06:00') {
            parsed.asana.sprint = deepClone(DEFAULT_WORKSPACE.asana.sprint);
          }
          if (!parsed.whatsapp_cloud) {
            parsed.whatsapp_cloud = deepClone(DEFAULT_WORKSPACE.whatsapp_cloud);
          }
          if (!parsed.accounting) parsed.accounting = {};
          if (!parsed.accounting.modular_options_matrix) {
            parsed.accounting.modular_options_matrix = deepClone(DEFAULT_WORKSPACE.accounting.modular_options_matrix);
          }
          if (!parsed.accounting.biogen_pilot_catalog) {
            parsed.accounting.biogen_pilot_catalog = deepClone(DEFAULT_WORKSPACE.accounting.biogen_pilot_catalog);
          }
          if (!parsed.accounting.small_business_catalog) {
            parsed.accounting.small_business_catalog = deepClone(DEFAULT_WORKSPACE.accounting.small_business_catalog);
          }
          if (!parsed.usage_telemetry) {
            parsed.usage_telemetry = deepClone(DEFAULT_WORKSPACE.usage_telemetry);
          }
          if (!parsed.gmaps_audits) {
            parsed.gmaps_audits = deepClone(DEFAULT_WORKSPACE.gmaps_audits);
          }
          if ((parsed.roster.agents || []).length < 10) {
            parsed.roster = deepClone(DEFAULT_WORKSPACE.roster);
          }
          return parsed;
        }
      }
    } catch (e) {
      console.warn('No se pudo leer estado offline:', e);
    }
    return deepClone(DEFAULT_WORKSPACE);
  }

  function saveOfflineState() {
    try {
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(workspaceState));
    } catch (e) {
      console.warn('No se pudo guardar en localStorage:', e);
    }
  }

  function isUserEditingDraft() {
    const active = document.activeElement;
    return active && (active.tagName === 'TEXTAREA' || active.tagName === 'INPUT');
  }

  async function syncWorkspaceFromServer(silent = false) {
    try {
      const res = await fetch(`${API_BASE}/api/workspace`, { method: 'GET', cache: 'no-store' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      serverOnline = true;
      if (!isUserEditingDraft()) {
        workspaceState = data;
      } else {
        workspaceState.roster = data.roster;
        workspaceState.events = data.events;
        workspaceState.asana = data.asana;
        workspaceState.whatsapp_cloud = data.whatsapp_cloud;
        if (data.usage_telemetry) workspaceState.usage_telemetry = data.usage_telemetry;
        if (data.gmaps_audits) workspaceState.gmaps_audits = data.gmaps_audits;
        if (data.marketing_studio) workspaceState.marketing_studio = data.marketing_studio;
      }
      saveOfflineState();
      updateConnectionBadges(true);
      renderAllWorkspacePanels();
      if (!silent) showToast('Sincronizado con Motor SDK en localhost:8765.');
      return true;
    } catch (err) {
      serverOnline = false;
      updateConnectionBadges(false);
      return false;
    }
  }

  function updateConnectionBadges(online) {
    const badge = document.getElementById('agentEngineBadge');
    const dot = document.getElementById('serverStatusDot');
    const label = document.getElementById('serverStatusLabel');
    if (online) {
      if (badge) {
        badge.textContent = 'Motor SDK Activo · localhost:8765 (En Vivo)';
        badge.style.color = '#c2dec8';
        badge.style.borderColor = 'rgba(110, 148, 119, 0.5)';
      }
      if (dot) dot.style.background = 'var(--status-success)';
      if (label) label.textContent = 'Motor SDK :8765 En Vivo';
    } else {
      if (badge) {
        badge.textContent = 'Vista Local Estática (Inicia servidor :8765 para correr SDK)';
        badge.style.color = 'var(--champagne-light)';
        badge.style.borderColor = 'var(--glass-border-subtle)';
      }
      if (dot) dot.style.background = 'var(--status-pending)';
      if (label) label.textContent = 'San Jerónimo · Vista Local';
    }
  }

  // =========================================================================
  // 1. TUESDAY 12PM SPRINT COUNTDOWN TIMER
  // =========================================================================
  function startSprintCountdown() {
    if (countdownInterval) clearInterval(countdownInterval);

    function tick() {
      const sprint = (workspaceState.asana && workspaceState.asana.sprint) || {};
      const deadlineStr = sprint.deadline_at || '2026-11-17T12:00:00-06:00';
      const targetMs = new Date(deadlineStr).getTime();
      const diffMs = targetMs - Date.now();
      const pill = document.getElementById('sprintCountdownPill');
      const asanaBadge = document.getElementById('asanaSprintBadge');
      const smallText = document.getElementById('sprintCountdownText');
      const largeText = document.getElementById('sprintTimerLarge');
      const daysEl = document.getElementById('sprintBedDays');
      const hrsEl = document.getElementById('sprintBedHours');
      const minsEl = document.getElementById('sprintBedMins');
      const secsEl = document.getElementById('sprintBedSecs');
      const targetLabelEl = document.getElementById('sprintDeadlineTargetLabel');

      if (targetLabelEl && sprint.tuesday_noon_label) {
        targetLabelEl.textContent = sprint.tuesday_noon_label;
      }

      let formatted = '00:00:00';
      let isUrgent = false;
      let dStr = '00';
      let hStr = '00';
      let mStr = '00';
      let sStr = '00';

      if (diffMs <= 0) {
        formatted = 'CIERRE 12PM';
        isUrgent = true;
      } else {
        const totalSec = Math.floor(diffMs / 1000);
        const totalHrs = Math.floor(totalSec / 3600);
        const days = Math.floor(totalSec / 86400);
        const remHrs = Math.floor((totalSec % 86400) / 3600);
        const mins = Math.floor((totalSec % 3600) / 60);
        const secs = totalSec % 60;
        formatted = `${String(totalHrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        dStr = String(days).padStart(2, '0');
        hStr = String(remHrs).padStart(2, '0');
        mStr = String(mins).padStart(2, '0');
        sStr = String(secs).padStart(2, '0');
        isUrgent = totalHrs < 12;
      }

      if (smallText) smallText.textContent = formatted;
      if (largeText) largeText.textContent = formatted;
      if (daysEl) daysEl.textContent = dStr;
      if (hrsEl) hrsEl.textContent = hStr;
      if (minsEl) minsEl.textContent = mStr;
      if (secsEl) secsEl.textContent = sStr;
      if (pill) pill.classList.toggle('urgent', isUrgent);
      if (asanaBadge) asanaBadge.classList.toggle('urgent', isUrgent);
    }

    tick();
    countdownInterval = setInterval(tick, 1000);
  }

  // =========================================================================
  // 2. VIDEO GAME STUDIO HQ (CAPTOORA SAN JERÓNIMO 2D INTERACTIVE CANVAS)
  // =========================================================================
  const STATIONS = {
    radar_maps: { x: 135, y: 98, w: 200, h: 118, title: 'RADAR APIFY NL', sub: 'Bot 2 · Scouting', agentId: 'scouting_radar', accent: '#c5a880' },
    mesa_directiva: { x: 375, y: 98, w: 220, h: 118, title: 'MESA DIRECTIVA', sub: 'Bot 1 · Chief of Staff', agentId: 'chief_of_staff', accent: '#dfcbb5' },
    estudio_marky: { x: 625, y: 98, w: 220, h: 118, title: 'MARKETING · MARKY', sub: 'Bot 8 · Dir. Marketing', agentId: 'marky_marketing', accent: '#c6ff00' },
    estudio_conan: { x: 865, y: 98, w: 200, h: 118, title: 'ESTUDIO CONAN', sub: 'Bot 10 · Contenido/Apps', agentId: 'conan_content', accent: '#d8c39b' },
    atelier_embudo: { x: 135, y: 295, w: 200, h: 118, title: 'ATELIER EMBUDO', sub: 'Bot 3 · Pull Strategy', agentId: 'embudo_marketing', accent: '#c5a880' },
    boveda_finanzas: { x: 375, y: 295, w: 200, h: 118, title: 'BÓVEDA CONTABLE', sub: 'Bot 6 · Margen & Subs', agentId: 'contabilidad_finanzas', accent: '#6e9477' },
    estudio_social: { x: 625, y: 295, w: 200, h: 118, title: 'VOZ @CAPTOORA', sub: 'Bot 4 · Guiones 9:16', agentId: 'social_content', accent: '#9bb3c9' },
    cabina_lupe: { x: 865, y: 295, w: 200, h: 118, title: 'CABINA LUPE', sub: 'Bot 9 · Meta/TikTok/LI', agentId: 'lupe_social', accent: '#c6ff00' },
    taller_led: { x: 175, y: 502, w: 230, h: 118, title: 'TALLER LED & LEGAL', sub: 'Bot 7 · 3-5d SLA', agentId: 'ops_talleres_legal', accent: '#c59f6b' },
    desk_ventas: { x: 465, y: 502, w: 230, h: 118, title: 'CABINA CIERRE 72H', sub: 'Bot 5 · Ventas B2B', agentId: 'ventas_outreach', accent: '#c59f6b' },
    trigger_gate: { x: 785, y: 502, w: 300, h: 118, title: 'TU ESCRITORIO · ÚLTIMO TRIGGER', sub: 'Compuerta Humana', agentId: 'trigger_gate', accent: '#dfcbb5' }
  };

  let gamePlaying = true;
  let gameSpeed = 1;
  let hoveredKey = null;
  let lastFrameTs = 0;
  let packetPulses = [];
  let simCycleTimer = 0;
  let simStepIdx = 0;

  const AGENT_SPRITES = {};
  const AGENT_COLORS = {
    chief_of_staff: '#dfcbb5',
    scouting_radar: '#c5a880',
    embudo_marketing: '#b8a58f',
    social_content: '#8fa9bf',
    ventas_outreach: '#d4a36a',
    contabilidad_finanzas: '#7ca886',
    ops_talleres_legal: '#c78c6f',
    marky_marketing: '#c6ff00',
    lupe_social: '#9ae675',
    conan_content: '#e6ca8f'
  };

  function ensureSpritesInitialized() {
    const agents = (workspaceState.roster && workspaceState.roster.agents) || [];
    agents.forEach((ag) => {
      const homeKey = Object.keys(STATIONS).find((k) => STATIONS[k].agentId === ag.id) || 'mesa_directiva';
      const st = STATIONS[homeKey];
      if (!AGENT_SPRITES[ag.id]) {
        AGENT_SPRITES[ag.id] = {
          id: ag.id,
          homeKey,
          x: st.x,
          y: st.y + 30,
          tx: st.x,
          ty: st.y + 30,
          phase: Math.random() * Math.PI * 2,
          bubbleText: 'Listo',
          bubbleTimer: 0
        };
      }
    });
  }

  function spawnPacket(fromZone, toZone, label) {
    const src = STATIONS[fromZone] || STATIONS.mesa_directiva;
    const dst = STATIONS[toZone] || STATIONS.trigger_gate;
    packetPulses.push({
      x0: src.x,
      y0: src.y,
      x1: dst.x,
      y1: dst.y,
      t: 0,
      label: label || ''
    });
  }

  function getAgentThought(agentId) {
    const latestEvt = ((workspaceState.events && workspaceState.events.events) || []).find((e) => e.agent_id === agentId);
    const pendingCount = ((workspaceState.approvals && workspaceState.approvals.items) || []).filter(
      (i) => i.agent_id === agentId && i.status === 'pending_trigger'
    ).length;
    if (pendingCount > 0) {
      return `${pendingCount} esperando Trigger`;
    }
    if (latestEvt && latestEvt.action) {
      return latestEvt.action.slice(0, 26);
    }
    const activeTask = ((workspaceState.asana && workspaceState.asana.tasks) || []).find(
      (t) => t.assigned_agent === agentId && t.status !== 'done'
    );
    if (activeTask) return activeTask.title.slice(0, 26) + '…';
    return 'Monitoreando KPI';
  }

  window.resizeStudioCanvas = function () {
    const canvas = document.getElementById('studioGameCanvas');
    if (!canvas || !canvas.parentElement) return;
    const rect = canvas.parentElement.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    if (rect.width < 10 || rect.height < 10) return;
    canvas.width = Math.round(rect.width * dpr);
    canvas.height = Math.round(rect.height * dpr);
  };

  function drawRoundedRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  function renderStudioCanvasFrame(ts) {
    requestAnimationFrame(renderStudioCanvasFrame);
    const canvas = document.getElementById('studioGameCanvas');
    const tabPanel = document.getElementById('tab-agentes-ia');
    if (!canvas || !tabPanel || !tabPanel.classList.contains('active') || currentDisplayMode !== 'game') {
      lastFrameTs = ts;
      return;
    }

    if (!canvas.width || canvas.width < 10) window.resizeStudioCanvas();
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dt = Math.min(0.05, (ts - (lastFrameTs || ts)) / 1000) * (gamePlaying ? gameSpeed : 0);
    lastFrameTs = ts;
    ensureSpritesInitialized();

    const W = 1000;
    const H = 625;
    ctx.save();
    ctx.scale(canvas.width / W, canvas.height / H);

    // 1. Floorplan Dark Atelier Blueprint Background
    ctx.fillStyle = '#090b10';
    ctx.fillRect(0, 0, W, H);

    // Subtle architectural grid
    ctx.strokeStyle = 'rgba(197, 168, 128, 0.045)';
    ctx.lineWidth = 1;
    for (let gx = 40; gx < W; gx += 40) {
      ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, H); ctx.stroke();
    }
    for (let gy = 40; gy < H; gy += 40) {
      ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(W, gy); ctx.stroke();
    }

    // 2. Corridors connecting Chief -> Specialists (incl. Marky -> Conan & Lupe) -> Trigger Gate
    const routes = [
      ['mesa_directiva', 'radar_maps'],
      ['mesa_directiva', 'estudio_marky'],
      ['mesa_directiva', 'boveda_finanzas'],
      ['estudio_marky', 'estudio_conan'],
      ['estudio_marky', 'estudio_social'],
      ['estudio_conan', 'cabina_lupe'],
      ['estudio_social', 'cabina_lupe'],
      ['radar_maps', 'atelier_embudo'],
      ['atelier_embudo', 'boveda_finanzas'],
      ['boveda_finanzas', 'desk_ventas'],
      ['boveda_finanzas', 'taller_led'],
      ['desk_ventas', 'trigger_gate'],
      ['taller_led', 'trigger_gate'],
      ['cabina_lupe', 'trigger_gate']
    ];
    ctx.lineWidth = 2;
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.07)';
    routes.forEach(([a, b]) => {
      const sa = STATIONS[a];
      const sb = STATIONS[b];
      if (!sa || !sb) return;
      ctx.beginPath();
      ctx.moveTo(sa.x, sa.y);
      ctx.lineTo(sb.x, sb.y);
      ctx.stroke();
    });

    // Periodically animate subtle patrol/handoff visualization while active
    if (gamePlaying) {
      simCycleTimer += dt;
      if (simCycleTimer >= 2.8) {
        simCycleTimer = 0;
        const route = routes[simStepIdx % routes.length];
        simStepIdx += 1;
        spawnPacket(route[0], route[1], '');
      }
    }

    // 3. Render 11 Room Workstations (10 Agents + Human Trigger Gate)
    const pendingItems = ((workspaceState.approvals && workspaceState.approvals.items) || []).filter(
      (i) => i.status === 'pending_trigger'
    );

    Object.entries(STATIONS).forEach(([key, st]) => {
      const isSelected = st.agentId === selectedAgentId || (key === 'trigger_gate' && hoveredKey === 'trigger_gate');
      const isHovered = hoveredKey === key;
      const rx = st.x - st.w / 2;
      const ry = st.y - st.h / 2;

      drawRoundedRect(ctx, rx, ry, st.w, st.h, 12);
      ctx.fillStyle = key === 'trigger_gate'
        ? 'rgba(197, 168, 128, 0.09)'
        : (isSelected ? 'rgba(30, 34, 46, 0.92)' : 'rgba(18, 21, 30, 0.86)');
      ctx.fill();

      ctx.lineWidth = isSelected || isHovered ? 1.8 : 1;
      ctx.strokeStyle = key === 'trigger_gate'
        ? 'rgba(197, 168, 128, 0.65)'
        : (isSelected ? st.accent : 'rgba(255, 255, 255, 0.11)');
      ctx.stroke();

      // Special ambient props per room
      if (key === 'radar_maps') {
        const sweepAngle = (ts * 0.0018) % (Math.PI * 2);
        ctx.strokeStyle = 'rgba(197, 168, 128, 0.22)';
        ctx.beginPath(); ctx.arc(st.x + 68, st.y + 8, 18, 0, Math.PI * 2); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(st.x + 68, st.y + 8);
        ctx.lineTo(st.x + 68 + Math.cos(sweepAngle) * 18, st.y + 8 + Math.sin(sweepAngle) * 18);
        ctx.stroke();
      } else if (key === 'taller_led') {
        // Warm illuminated acrylic trophy pedestal glow
        const glow = 0.2 + 0.12 * Math.sin(ts * 0.004);
        ctx.fillStyle = `rgba(223, 203, 181, ${glow})`;
        ctx.beginPath(); ctx.arc(st.x + 82, st.y + 12, 15, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = 'rgba(223, 203, 181, 0.7)';
        ctx.strokeRect(st.x + 75, st.y + 3, 14, 18);
      }

      // Station headers
      ctx.fillStyle = st.accent;
      ctx.font = '500 10px "JetBrains Mono", monospace';
      ctx.textAlign = 'left';
      ctx.fillText(st.title, rx + 12, ry + 19);

      ctx.fillStyle = '#888d9e';
      ctx.font = '300 10px "Plus Jakarta Sans", sans-serif';
      ctx.fillText(st.sub, rx + 12, ry + 34);

      if (key === 'trigger_gate') {
        const badgeText = `${pendingItems.length} LISTOS PARA TU TRIGGER`;
        drawRoundedRect(ctx, st.x - 108, st.y + 4, 216, 28, 14);
        ctx.fillStyle = pendingItems.length > 0 ? 'rgba(197, 159, 107, 0.22)' : 'rgba(110, 148, 119, 0.2)';
        ctx.fill();
        ctx.strokeStyle = pendingItems.length > 0 ? '#c59f6b' : '#6e9477';
        ctx.stroke();
        ctx.fillStyle = '#f5f4ef';
        ctx.font = '500 10.5px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillText(badgeText, st.x, st.y + 22);
      }
    });

    // 4. Animate Collaboration Light Packets
    packetPulses = packetPulses.filter((p) => p.t < 1);
    packetPulses.forEach((p) => {
      p.t += dt * 0.75;
      const px = p.x0 + (p.x1 - p.x0) * p.t;
      const py = p.y0 + (p.y1 - p.y0) * p.t;
      ctx.fillStyle = 'rgba(223, 203, 181, 0.9)';
      ctx.beginPath();
      ctx.arc(px, py, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(197, 168, 128, 0.25)';
      ctx.beginPath();
      ctx.arc(px, py, 9, 0, Math.PI * 2);
      ctx.fill();
    });

    // 5. Render 7 Animated Agent Characters + Status Halos + Thought Bubbles
    const agents = (workspaceState.roster && workspaceState.roster.agents) || [];
    agents.forEach((ag) => {
      const sp = AGENT_SPRITES[ag.id];
      if (!sp) return;
      const homeSt = STATIONS[sp.homeKey];
      sp.phase += dt * 2.4;

      // Move smoothly around home desk (walking step if waiting_trigger or running)
      const wobbleX = Math.sin(sp.phase * 0.65) * 14;
      const wobbleY = Math.cos(sp.phase * 0.9) * 3.5;
      sp.tx = homeSt.x + wobbleX;
      sp.ty = homeSt.y + 30 + wobbleY;
      sp.x += (sp.tx - sp.x) * Math.min(1, dt * 4 + 0.08);
      sp.y += (sp.ty - sp.y) * Math.min(1, dt * 4 + 0.08);

      const isSel = ag.id === selectedAgentId;
      const color = AGENT_COLORS[ag.id] || '#c5a880';

      // Selection ring
      if (isSel) {
        ctx.strokeStyle = '#f5f4ef';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.arc(sp.x, sp.y, 20 + Math.sin(ts * 0.006) * 2, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Progress / status halo
      ctx.strokeStyle = ag.status === 'running' ? '#dfcbb5' : (ag.status === 'waiting_trigger' ? '#c59f6b' : '#6e9477');
      ctx.lineWidth = 2;
      ctx.beginPath();
      const startAng = ag.status === 'running' ? (ts * 0.004) : 0;
      ctx.arc(sp.x, sp.y, 15, startAng, startAng + (ag.status === 'running' ? Math.PI * 1.35 : Math.PI * 2));
      ctx.stroke();

      // Character Body / Head Avatar
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(sp.x, sp.y - 1.5, 9.5, 0, Math.PI * 2);
      ctx.fill();

      // Character number
      ctx.fillStyle = '#090b10';
      ctx.font = '600 8.5px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(String(ag.number), sp.x, sp.y + 1.5);

      // Thought Bubble below room subtitle & cleanly above sprite
      const thought = getAgentThought(ag.id);
      ctx.font = '400 9.5px "Plus Jakarta Sans", sans-serif';
      const tw = Math.min(182, Math.max(82, ctx.measureText(thought).width + 16));
      const bx = Math.max(12, Math.min(W - tw - 12, sp.x - tw / 2));
      const by = Math.max(10, sp.y - 45);
      drawRoundedRect(ctx, bx, by, tw, 20, 8);
      ctx.fillStyle = 'rgba(10, 12, 18, 0.92)';
      ctx.fill();
      ctx.strokeStyle = ag.status === 'waiting_trigger' ? 'rgba(197, 159, 107, 0.55)' : 'rgba(255, 255, 255, 0.16)';
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.fillStyle = ag.status === 'waiting_trigger' ? '#e7c697' : '#d2d5de';
      ctx.fillText(thought, bx + tw / 2, by + 13.5, tw - 10);
    });

    ctx.restore();
  }

  function setupGameCanvasInteractions() {
    const canvas = document.getElementById('studioGameCanvas');
    if (!canvas) return;

    function getVirtualPos(evt) {
      const rect = canvas.getBoundingClientRect();
      return {
        vx: ((evt.clientX - rect.left) / rect.width) * 1000,
        vy: ((evt.clientY - rect.top) / rect.height) * 625
      };
    }

    canvas.addEventListener('mousemove', (evt) => {
      const { vx, vy } = getVirtualPos(evt);
      let found = null;
      Object.entries(STATIONS).forEach(([k, st]) => {
        if (Math.abs(vx - st.x) <= st.w / 2 && Math.abs(vy - st.y) <= st.h / 2) {
          found = k;
        }
      });
      hoveredKey = found;
      canvas.style.cursor = found ? 'pointer' : 'default';
    });

    canvas.addEventListener('click', (evt) => {
      const { vx, vy } = getVirtualPos(evt);
      // Priority 1: clicked close to any sprite
      let clickedAgent = null;
      Object.values(AGENT_SPRITES).forEach((sp) => {
        if (Math.hypot(vx - sp.x, vy - sp.y) <= 28) clickedAgent = sp.id;
      });
      if (clickedAgent) {
        selectInspectorAgent(clickedAgent);
        return;
      }
      // Priority 2: clicked a station room
      for (const [k, st] of Object.entries(STATIONS)) {
        if (Math.abs(vx - st.x) <= st.w / 2 && Math.abs(vy - st.y) <= st.h / 2) {
          if (k === 'trigger_gate') {
            window.switchTab('proyectos-asana');
            showToast('Abriendo Bandeja de Último Trigger.');
          } else {
            selectInspectorAgent(st.agentId);
          }
          return;
        }
      }
    });

    window.addEventListener('resize', () => window.resizeStudioCanvas());
    requestAnimationFrame(renderStudioCanvasFrame);
  }

  window.toggleGameAnimation = function () {
    gamePlaying = !gamePlaying;
    const btn = document.getElementById('btnGameTogglePlay');
    if (btn) btn.textContent = gamePlaying ? 'Pausar' : 'Reanudar';
  };

  window.cycleGameSpeed = function () {
    gameSpeed = gameSpeed === 1 ? 2 : 1;
    const btn = document.getElementById('btnGameSpeed');
    if (btn) btn.textContent = `Velocidad: ${gameSpeed}x`;
  };

  window.setAgentDisplayMode = function (mode) {
    currentDisplayMode = mode;
    const gameEl = document.getElementById('agentGameView');
    const compEl = document.getElementById('agentCompanyView');
    const btnG = document.getElementById('btnViewGameMode');
    const btnC = document.getElementById('btnViewCompanyMode');
    if (gameEl) gameEl.hidden = mode !== 'game';
    if (compEl) compEl.hidden = mode !== 'company';
    if (btnG) btnG.classList.toggle('active', mode === 'game');
    if (btnC) btnC.classList.toggle('active', mode === 'company');
    if (mode === 'game') requestAnimationFrame(() => window.resizeStudioCanvas());
  };

  window.selectInspectorAgent = function (agentId) {
    selectedAgentId = agentId;
    renderGameInspectorHud();
  };

  window.jumpToAgentTasks = function () {
    const sel = document.getElementById('asanaFilterAgent');
    if (sel) sel.value = selectedAgentId;
    window.switchTab('proyectos-asana');
    window.renderAsanaBoard();
  };

  // =========================================================================
  // 3. RENDERERS: INSPECTOR HUD, EMPRESA VIEW, ASANA BOARD & TRIGGER QUEUE
  // =========================================================================
  function renderGameInspectorHud() {
    const agents = (workspaceState.roster && workspaceState.roster.agents) || [];
    const ag = agents.find((a) => a.id === selectedAgentId) || agents[0];
    if (!ag) return;

    const numEl = document.getElementById('hudAgentNumber');
    const stEl = document.getElementById('hudAgentStatus');
    const nameEl = document.getElementById('hudAgentName');
    const roleEl = document.getElementById('hudAgentRole');
    const jobEl = document.getElementById('hudAgentSingleJob');
    const taskEl = document.getElementById('hudAgentCurrentTask');
    const feedEl = document.getElementById('hudAgentEventsList');

    if (numEl) numEl.textContent = `BOT ${String(ag.number).padStart(2, '0')}`;
    if (stEl) {
      stEl.textContent = ag.status === 'waiting_trigger' ? 'ESPERANDO TRIGGER' : ag.status.toUpperCase();
      stEl.className = `agent-state-pill ${ag.status}`;
    }
    if (nameEl) nameEl.textContent = ag.name;
    if (roleEl) roleEl.textContent = ag.role_title;
    if (jobEl) jobEl.textContent = ag.single_job;

    const tasks = ((workspaceState.asana && workspaceState.asana.tasks) || []).filter((t) => t.assigned_agent === ag.id);
    if (taskEl) {
      const openTasks = tasks.filter((t) => t.status !== 'done');
      taskEl.textContent = openTasks.length > 0
        ? `[${openTasks[0].id}] ${openTasks[0].title} (${openTasks[0].due_label})`
        : 'Todas sus tareas actuales completadas.';
    }

    if (feedEl) {
      const events = ((workspaceState.events && workspaceState.events.events) || []).filter(
        (e) => e.agent_id === ag.id || e.target_agent === ag.id
      );
      feedEl.innerHTML = '';
      if (events.length === 0) {
        feedEl.innerHTML = '<div style="color:var(--slate-muted); font-size:0.74rem;">Sin eventos recientes.</div>';
      } else {
        events.slice(0, 6).forEach((ev) => {
          const row = document.createElement('div');
          row.className = `event-feed-row ${ev.source || ''}`;
          row.innerHTML = `
            <div style="display:flex; justify-content:space-between; color:var(--champagne); font-family:var(--font-mono); font-size:0.64rem; margin-bottom:2px;">
              <span>${ev.action}</span>
              <span>${(ev.timestamp || '').slice(11, 19)}</span>
            </div>
            <div style="color:#cfd3df;">${ev.detail}</div>
          `;
          feedEl.appendChild(row);
        });
      }
    }
  }

  function renderCompanyMode() {
    const cardsBox = document.getElementById('companyRosterCards');
    const feedBox = document.getElementById('companyLiveFeed');
    const agents = (workspaceState.roster && workspaceState.roster.agents) || [];
    const tasks = (workspaceState.asana && workspaceState.asana.tasks) || [];

    if (cardsBox) {
      cardsBox.innerHTML = '';
      agents.forEach((ag) => {
        const myTasks = tasks.filter((t) => t.assigned_agent === ag.id);
        const doneCount = myTasks.filter((t) => t.status === 'done').length;
        const card = document.createElement('div');
        card.className = 'comp-glass-card';
        card.innerHTML = `
          <div>
            <div class="comp-top-strip">
              <span class="comp-name-title">${String(ag.number).padStart(2, '0')}. ${ag.name}</span>
              <span class="agent-state-pill ${ag.status}">${ag.status === 'waiting_trigger' ? 'Trigger' : ag.status}</span>
            </div>
            <div class="comp-meta-row"><strong>Rol:</strong> ${ag.role_title}</div>
            <div class="comp-meta-row"><strong>Misión Única:</strong> ${ag.single_job}</div>
            <div class="comp-meta-row"><strong>Rutina:</strong> ${ag.schedule_label} · <strong>Tareas:</strong> ${doneCount}/${myTasks.length}</div>
            <div class="comp-void-box" style="background: rgba(197, 168, 128, 0.06); border-left-color: var(--champagne); color: #dbd5c7;">
              <strong>Candado de Seguridad:</strong> ${ag.safety_boundary}
            </div>
          </div>
          <div style="margin-top: 12px; display:flex; justify-content:space-between; align-items:center; gap:8px;">
            <button type="button" class="week-btn" onclick="selectInspectorAgent('${ag.id}'); setAgentDisplayMode('game');">Ver en Juego HQ</button>
            <button type="button" class="btn-approve-trigger" style="padding: 5px 12px; font-size:0.7rem;" onclick="runSelectedOrChiefMission('${ag.id}')">Ejecutar SDK &rarr;</button>
          </div>
        `;
        cardsBox.appendChild(card);
      });
    }

    if (feedBox) {
      const events = (workspaceState.events && workspaceState.events.events) || [];
      feedBox.innerHTML = '';
      events.slice(0, 20).forEach((ev) => {
        const row = document.createElement('div');
        row.className = `event-feed-row ${ev.source || ''}`;
        row.innerHTML = `
          <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:6px; margin-bottom:4px;">
            <span style="font-family:var(--font-mono); font-size:0.68rem; color:var(--champagne-light);">
              ${ev.agent_id} ${ev.target_agent ? '&rarr; ' + ev.target_agent : ''} · <strong>${ev.action}</strong>
            </span>
            <span class="source-type-badge">${(ev.source || 'log').toUpperCase()} · ${(ev.timestamp || '').slice(11, 19)}</span>
          </div>
          <div style="color:#d2d5de;">${ev.detail}</div>
        `;
        feedBox.appendChild(row);
      });
    }
  }

  function escapeHtml(raw) {
    return String(raw || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function resolveAssetUrl(relPath) {
    const clean = String(relPath || '').replace(/^\/+/, '');
    if (window.location && String(window.location.protocol).startsWith('http') && clean.startsWith('assets/')) {
      return `/${clean}`;
    }
    return `../${clean}`;
  }

  async function copyAttachmentImage(assetUrl, label) {
    if (!navigator.clipboard || typeof ClipboardItem === 'undefined') {
      window.open(assetUrl, '_blank', 'noopener');
      showToast(`Imagen "${label}" abierta: usa clic derecho → Copiar imagen.`);
      return;
    }
    try {
      const response = await fetch(assetUrl);
      const blob = await response.blob();
      await navigator.clipboard.write([new ClipboardItem({ [blob.type || 'image/png']: blob })]);
      showToast(`Imagen "${label}" copiada al portapapeles (lista para pegar con Cmd+V en WhatsApp).`);
    } catch (_err) {
      window.open(assetUrl, '_blank', 'noopener');
      showToast(`No se pudo copiar directo; se abrió "${label}" para copiar manual o arrastrar.`);
    }
  }

  function renderAttachmentsHtml(attachments) {
    if (!Array.isArray(attachments) || attachments.length === 0) return '';
    const cards = attachments.map((att) => {
      const href = resolveAssetUrl(att.path);
      const label = escapeHtml(att.label || 'Adjunto');
      if (att.type === 'pdf') {
        return `
          <div class="attachment-card">
            <div class="attachment-pdf-box">
              <span class="attachment-pdf-tag">PDF · 1 HOJA</span>
              <span>${label}</span>
            </div>
            <div class="attachment-actions">
              <a class="attachment-btn" href="${escapeHtml(href)}" target="_blank" rel="noopener">Abrir PDF</a>
              <a class="attachment-btn" href="${escapeHtml(href)}" download>Descargar PDF</a>
            </div>
          </div>
        `;
      }
      return `
        <div class="attachment-card">
          <img class="attachment-thumb" src="${escapeHtml(href)}" alt="${label}" loading="lazy" />
          <div class="attachment-label">${label}</div>
          <div class="attachment-actions">
            <button type="button" class="attachment-btn" data-copy-img="${escapeHtml(href)}" data-copy-label="${label}">Copiar PNG (Cmd+V)</button>
            <a class="attachment-btn" href="${escapeHtml(href)}" download>Descargar</a>
          </div>
        </div>
      `;
    }).join('');
    return `<div class="attachment-strip">${cards}</div>`;
  }

  function renderApprovalQueue() {
    const queueBox = document.getElementById('approvalQueueContainer');
    const historyBox = document.getElementById('approvalHistoryContainer');
    const badgeEl = document.getElementById('approvalPendingBadge');
    const chipEl = document.getElementById('headerTriggerCountChip');

    const items = (workspaceState.approvals && workspaceState.approvals.items) || [];
    const pending = items.filter((i) => i.status === 'pending_trigger');
    const decided = items.filter((i) => i.status !== 'pending_trigger');

    if (chipEl) chipEl.textContent = String(pending.length);
    if (badgeEl) {
      badgeEl.textContent = pending.length > 0
        ? `${pending.length} propuesta(s) redactadas y validadas listas esperando Tu Último Trigger para despachar.`
        : 'Bandeja limpia: todas las propuestas actuales ya recibieron tu decisión.';
    }

    if (queueBox) {
      queueBox.innerHTML = '';
      if (pending.length === 0) {
        queueBox.innerHTML = '<div style="color:var(--slate-muted); font-size:0.8rem; padding:12px;">No hay envíos pendientes. Puedes pedirle al Director de Orquesta o a Ventas generar nuevos borradores.</div>';
      } else {
        pending.forEach((item) => {
          const card = document.createElement('div');
          card.className = 'approval-card-glass';
          const flagsHtml = (item.compliance_flags || []).map((f) => `<span class="compliance-chip">✓ ${escapeHtml(f)}</span>`).join('');
          const attachmentsHtml = renderAttachmentsHtml(item.attachments);
          const testPill = String(item.id || '').startsWith('TEST-')
            ? '<span class="badge-test-mode">AUTOPRUEBA · SIN COMPROMISO</span>'
            : '';
          card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; flex-wrap:wrap;">
              <div>
                <span class="task-day-badge">${escapeHtml(item.id)} · ${escapeHtml(item.agent_id)}</span>${testPill}
                <h4 style="font-family:var(--font-display); color:var(--bone-white); font-size:0.95rem; font-weight:500; margin-top:6px;">
                  ${escapeHtml(item.target_name)}
                </h4>
                <div style="font-size:0.74rem; color:var(--slate-muted);">
                  ${escapeHtml(item.channel)} · ${escapeHtml(item.package_ref)}
                </div>
              </div>
              <div style="text-align:right; font-family:var(--font-mono); font-size:0.72rem; color:var(--champagne);">
                ${item.financial_impact_mxn > 0 ? '$' + Number(item.financial_impact_mxn).toLocaleString() + ' MXN' : 'Operación'}
                ${item.financial_impact_mxn > 0 ? `<div style="font-size:0.64rem; color:#9dc0a5;">Margen ${item.estimated_margin_pct}%</div>` : ''}
              </div>
            </div>
            <div style="display:flex; gap:6px; flex-wrap:wrap;">${flagsHtml}</div>
            ${attachmentsHtml}
            <textarea class="draft-editor-area" id="draftEditor_${escapeHtml(item.id)}">${escapeHtml(item.draft_text || '')}</textarea>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
              <button type="button" class="btn-reject-trigger" onclick="handleTriggerDecision('${escapeHtml(item.id)}', 'reject')">✕ Descartar</button>
              <button type="button" class="btn-approve-trigger" onclick="handleTriggerDecision('${escapeHtml(item.id)}', 'approve')">
                ✓ Aprobar Trigger ${item.phone ? '& Abrir WhatsApp' : '& Copiar Texto'} &rarr;
              </button>
            </div>
          `;
          card.querySelectorAll('[data-copy-img]').forEach((btn) => {
            btn.addEventListener('click', () => {
              copyAttachmentImage(btn.dataset.copyImg, btn.dataset.copyLabel || 'Mockup');
            });
          });
          queueBox.appendChild(card);
        });
      }
    }

    if (historyBox) {
      historyBox.hidden = !showApprovalHistory;
      if (showApprovalHistory) {
        historyBox.innerHTML = decided.length === 0
          ? '<div style="color:var(--slate-muted); font-size:0.75rem;">Aún no hay decisiones registradas.</div>'
          : decided.map((item) => `
              <div class="task-liquid-item" style="margin-bottom:8px;">
                <div class="task-left-content">
                  <span class="task-day-badge">${item.id}</span>
                  <span class="task-title-text">${item.target_name} (${item.channel})</span>
                </div>
                <span class="agent-state-pill ${item.status === 'approved' ? 'ready' : ''}" style="${item.status === 'rejected' ? 'color:#dfb2ad;border-color:rgba(184,98,89,0.4);' : ''}">
                  ${item.status === 'approved' ? 'APROBADO' : 'RECHAZADO'}
                </span>
              </div>
            `).join('');
      }
    }
  }

  window.toggleApprovalHistory = function () {
    showApprovalHistory = !showApprovalHistory;
    const btn = document.getElementById('btnToggleHistory');
    if (btn) btn.textContent = showApprovalHistory ? 'Ocultar Historial' : 'Ver Historial Aprobados / Rechazados';
    renderApprovalQueue();
  };

  window.handleTriggerDecision = async function (itemId, decision) {
    const editor = document.getElementById(`draftEditor_${itemId}`);
    const editedText = editor ? editor.value : null;
    const items = (workspaceState.approvals && workspaceState.approvals.items) || [];
    const item = items.find((i) => i.id === itemId);
    if (!item) return;

    if (decision === 'approve' && item.niche !== 'Operación Interna' && editedText !== null) {
      const violations = checkClientCopyGuardrail(editedText);
      if (violations.length > 0) {
        showToast('Bloqueado: ' + violations[0]);
        return;
      }
    }

    let finalUrl = item.whatsapp_url || '';
    if (editedText !== null) {
      item.draft_text = editedText;
      if (item.phone) {
        finalUrl = `https://wa.me/${item.phone}?text=${encodeURIComponent(editedText)}`;
        item.whatsapp_url = finalUrl;
      }
    }

    if (serverOnline) {
      try {
        const res = await fetch(`${API_BASE}/api/approvals/${encodeURIComponent(itemId)}/decision`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ decision, edited_text: editedText })
        });
        if (!res.ok) {
          const errJson = await res.json().catch(() => ({}));
          throw new Error(errJson.detail || 'Error al registrar decisión');
        }
        const payload = await res.json();
        workspaceState = payload.workspace;
      } catch (err) {
        showToast('Error al guardar en servidor: ' + err.message);
        return;
      }
    } else {
      item.status = decision === 'approve' ? 'approved' : 'rejected';
      item.decided_at = new Date().toISOString();
      if (item.task_id && workspaceState.asana && workspaceState.asana.tasks) {
        const linked = workspaceState.asana.tasks.find((t) => t.id === item.task_id);
        if (linked) linked.status = decision === 'approve' ? 'done' : 'backlog';
      }
      saveOfflineState();
    }

    if (decision === 'approve') {
      spawnPacket(item.agent_id === 'ventas_outreach' ? 'desk_ventas' : 'mesa_directiva', 'trigger_gate', itemId);
      if (editedText && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(editedText).catch(() => {});
      }
      if (finalUrl && finalUrl.startsWith('https://wa.me/')) {
        window.open(finalUrl, '_blank', 'noopener');
        showToast(`Trigger ${itemId} aprobado: WhatsApp Web abierto y texto copiado.`);
      } else {
        showToast(`Trigger ${itemId} aprobado y copiado al portapapeles.`);
      }
    } else {
      showToast(`Propuesta ${itemId} descartada.`);
    }

    renderAllWorkspacePanels();
  };

  function populateAsanaSelectors() {
    const projects = (workspaceState.asana && workspaceState.asana.projects) || [];
    const agents = (workspaceState.roster && workspaceState.roster.agents) || [];

    const fProj = document.getElementById('asanaFilterProject');
    const nProj = document.getElementById('newTaskProject');
    const fAg = document.getElementById('asanaFilterAgent');
    const nAg = document.getElementById('newTaskAgent');

    if (fProj && fProj.options.length <= 1) {
      projects.forEach((p) => fProj.add(new Option(p.name, p.id)));
    }
    if (nProj && nProj.options.length === 0) {
      projects.forEach((p) => nProj.add(new Option(p.name, p.id)));
    }
    if (fAg && fAg.options.length <= 1) {
      agents.forEach((a) => fAg.add(new Option(`0${a.number}. ${a.name}`, a.id)));
    }
    if (nAg && nAg.options.length === 0) {
      agents.forEach((a) => nAg.add(new Option(`0${a.number}. ${a.name}`, a.id)));
    }
  }

  window.renderAsanaBoard = function () {
    populateAsanaSelectors();
    const projects = (workspaceState.asana && workspaceState.asana.projects) || [];
    const tasks = (workspaceState.asana && workspaceState.asana.tasks) || [];

    const projFilter = (document.getElementById('asanaFilterProject') || {}).value || 'all';
    const agFilter = (document.getElementById('asanaFilterAgent') || {}).value || 'all';
    const stFilter = (document.getElementById('asanaFilterStatus') || {}).value || 'all';

    // 1. Project Cards Strip
    const strip = document.getElementById('asanaProjectCardsStrip');
    if (strip) {
      strip.innerHTML = '';
      projects.forEach((p) => {
        const pTasks = tasks.filter((t) => t.project_id === p.id);
        const done = pTasks.filter((t) => t.status === 'done').length;
        const pct = pTasks.length > 0 ? Math.round((done / pTasks.length) * 100) : 0;
        const card = document.createElement('div');
        card.className = `asana-project-card ${projFilter === p.id ? 'active' : ''}`;
        card.onclick = () => {
          const sel = document.getElementById('asanaFilterProject');
          if (sel) sel.value = sel.value === p.id ? 'all' : p.id;
          window.renderAsanaBoard();
        };
        card.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin-bottom:6px;">
            <span class="task-day-badge">${p.priority}</span>
            <span style="font-family:var(--font-mono); font-size:0.68rem; color:var(--champagne);">${done}/${pTasks.length}</span>
          </div>
          <div style="color:var(--bone-white); font-size:0.84rem; font-weight:500;">${p.name}</div>
          <div style="color:var(--slate-muted); font-size:0.72rem; margin-top:4px;">${p.objective}</div>
          <div class="progress-track-thin"><div class="progress-fill-champagne" style="width:${pct}%"></div></div>
          <div style="font-family:var(--font-mono); font-size:0.64rem; color:var(--slate-muted);">${pct}% completado</div>
        `;
        strip.appendChild(card);
      });
    }

    // 2. Task List
    const listEl = document.getElementById('asanaTasksList');
    if (listEl) {
      listEl.innerHTML = '';
      const filtered = tasks.filter((t) => {
        return (projFilter === 'all' || t.project_id === projFilter)
          && (agFilter === 'all' || t.assigned_agent === agFilter)
          && (stFilter === 'all' || t.status === stFilter);
      });

      const statusLabels = {
        backlog: 'Pendiente',
        in_progress: 'En Curso',
        waiting_trigger: 'Esperando Trigger',
        done: 'Completado'
      };

      filtered.forEach((t) => {
        const row = document.createElement('div');
        row.className = `task-liquid-item ${t.status === 'done' ? 'done' : ''}`;
        row.innerHTML = `
          <div class="task-left-content" style="flex-wrap:wrap;">
            <span class="task-day-badge">${t.id}</span>
            <span class="task-title-text">${t.title}</span>
          </div>
          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <span class="source-type-badge">${t.assigned_agent}</span>
            <span class="task-channel-tag">${t.due_label}</span>
            <select class="glass-select-input" style="padding:4px 8px; font-size:0.72rem;" onchange="handleTaskStatusChange('${t.id}', this.value)">
              ${Object.entries(statusLabels).map(([val, lbl]) => `<option value="${val}" ${t.status === val ? 'selected' : ''}>${lbl}</option>`).join('')}
            </select>
          </div>
        `;
        listEl.appendChild(row);
      });
    }
  };

  window.handleTaskStatusChange = async function (taskId, newStatus) {
    if (serverOnline) {
      try {
        const res = await fetch(`${API_BASE}/api/tasks/${encodeURIComponent(taskId)}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status: newStatus })
        });
        if (res.ok) {
          const data = await res.json();
          workspaceState = data.workspace;
          renderAllWorkspacePanels();
          showToast(`Tarea ${taskId} actualizada.`);
          return;
        }
      } catch (e) {
        console.warn(e);
      }
    }
    const task = ((workspaceState.asana && workspaceState.asana.tasks) || []).find((t) => t.id === taskId);
    if (task) task.status = newStatus;
    saveOfflineState();
    renderAllWorkspacePanels();
    showToast(`Tarea ${taskId} actualizada en vista local.`);
  };

  window.handleCreateAsanaTask = async function () {
    const titleEl = document.getElementById('newTaskTitle');
    const projEl = document.getElementById('newTaskProject');
    const agEl = document.getElementById('newTaskAgent');
    const prioEl = document.getElementById('newTaskPriority');
    const title = (titleEl && titleEl.value || '').trim();
    if (title.length < 4) {
      showToast('Escribe al menos 4 caracteres para asignar la tarea.');
      return;
    }

    const payload = {
      project_id: (projEl && projEl.value) || 'proj_sprint_padel',
      title,
      assigned_agent: (agEl && agEl.value) || 'ventas_outreach',
      priority: (prioEl && prioEl.value) || 'Alta'
    };

    if (serverOnline) {
      try {
        const res = await fetch(`${API_BASE}/api/tasks`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          const data = await res.json();
          workspaceState = data.workspace;
          titleEl.value = '';
          renderAllWorkspacePanels();
          showToast(`Tarea asignada a ${payload.assigned_agent}.`);
          return;
        }
      } catch (e) {
        console.warn(e);
      }
    }

    const tasks = (workspaceState.asana && workspaceState.asana.tasks) || [];
    const nextId = `TASK-${600 + tasks.length + 1}`;
    tasks.push({
      id: nextId,
      project_id: payload.project_id,
      title: payload.title,
      assigned_agent: payload.assigned_agent,
      status: 'in_progress',
      priority: payload.priority,
      due_label: 'Sprint 72h',
      deliverable_ref: 'Asignada'
    });
    titleEl.value = '';
    saveOfflineState();
    renderAllWorkspacePanels();
    showToast(`Tarea ${nextId} asignada.`);
  };

  function renderAccountingAndSubscriptions() {
    const accBox = document.getElementById('accountingSummaryGrid');
    const subBox = document.getElementById('subscriptionsGrid');
    const acc = workspaceState.accounting || DEFAULT_WORKSPACE.accounting;

    if (accBox) {
      const pendingMxn = ((workspaceState.approvals && workspaceState.approvals.items) || [])
        .filter((i) => i.status === 'pending_trigger')
        .reduce((sum, i) => sum + Number(i.financial_impact_mxn || 0), 0);
      const approvedMxn = ((workspaceState.approvals && workspaceState.approvals.items) || [])
        .filter((i) => i.status === 'approved')
        .reduce((sum, i) => sum + Number(i.financial_impact_mxn || 0), 0);

      accBox.innerHTML = `
        <div class="simulator-output-box" style="margin-bottom:8px;">
          <div class="sim-row"><span class="sim-label">Pipeline Pendiente de Trigger</span><span class="sim-val">$${pendingMxn.toLocaleString()} MXN</span></div>
          <div class="sim-row"><span class="sim-label">Propuestas Aprobadas</span><span class="sim-val profit">$${approvedMxn.toLocaleString()} MXN</span></div>
        </div>
        <div style="font-size:0.75rem; color:#abb0c0;"><strong>Política de Cobro:</strong> ${acc.payment_policy}</div>
        <div style="font-size:0.74rem; color:var(--slate-muted);"><strong>CFDI / SAT:</strong> ${acc.tax_regime_note}</div>
      `;
    }

    if (subBox) {
      subBox.innerHTML = (acc.subscriptions_watchlist || []).map((s) => `
        <div class="supplier-chip">
          <div class="supplier-name-box">
            <strong>${s.service}</strong>
            <span>${s.role} · Encargado: ${s.owner_agent}</span>
          </div>
          <span class="supplier-tag">${s.status}</span>
        </div>
      `).join('') + `
        <div style="font-size:0.71rem; color:#8d92a3; padding:8px 10px; border-left:2px solid var(--champagne-muted);">
          <strong>SLAs Talleres NL (Bot 7):</strong> Digital en vivo (Halftime Blitz 15 min) bajo control 100% Captoora; manufactura física en El Marco San Pedro y Foco Lab requiere 3 a 5 días hábiles.
        </div>
      `;
    }
  }

  // =========================================================================
  // 4. EXECUTE REAL SDK AGENT MISSIONS ON LOCAL SERVER (:8765)
  // =========================================================================
  window.runSelectedBotMission = function () {
    const promptEl = document.getElementById('hudCustomPrompt');
    const customText = promptEl ? promptEl.value.trim() : '';
    window.runSelectedOrChiefMission(selectedAgentId, customText || null);
  };

  window.runSelectedOrChiefMission = async function (agentId, instruction = null) {
    if (!serverOnline) {
      showToast('Inicia el servidor local en Terminal: uv run python -m captoora_agents.server');
      return;
    }

    const agents = (workspaceState.roster && workspaceState.roster.agents) || [];
    const target = agents.find((a) => a.id === agentId);
    if (target) target.status = 'running';
    renderAllWorkspacePanels();
    showToast(`Ejecutando misión con ${agentId} vía Google Antigravity SDK...`);

    try {
      const res = await fetch(`${API_BASE}/api/agents/${encodeURIComponent(agentId)}/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instruction })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al ejecutar agente');
      workspaceState = data.workspace;
      saveOfflineState();
      renderAllWorkspacePanels();
      showToast(`Misión de ${agentId} finalizada y guardada.`);
    } catch (err) {
      if (target) target.status = 'ready';
      renderAllWorkspacePanels();
      showToast('Error SDK: ' + err.message);
    }
  };

  // =========================================================================
  // 5. SPRINT MARTES 12PM: VISUAL BED, POMODORO, PLAN CALENDARIZADO & TOP 10
  // =========================================================================
  const SPRINT_STEPS_STORAGE_KEY = 'captoora_sprint_steps_v1';
  const POMO_STORAGE_KEY = 'captoora_pomo_state_v1';
  const TOP10_STAGES_STORAGE_KEY = 'captoora_top10_stages_v1';

  const POMO_MODES = {
    focus25: { label: 'BLOQUE ENFOQUE · 25 MIN', seconds: 25 * 60 },
    sprint15: { label: 'SPRINT RÁPIDO · 15 MIN', seconds: 15 * 60 },
    break5: { label: 'PAUSA BREVE · 05 MIN', seconds: 5 * 60 },
    break15: { label: 'PAUSA LARGA · 15 MIN', seconds: 15 * 60 }
  };

  const SPRINT_PLAN_STEPS = [
    {
      id: 'STEP-01',
      phase: 'dom15',
      phaseTitle: 'Hoy Domingo 15 Nov · Tarde / Noche (Arranque y Autoprueba)',
      time: 'Dom 15:45 – 16:10',
      title: 'Validar kit visual 2026 (Opc A/B + Dossier PDF + Emails + Firma)',
      detail: 'Abre TEST-001/002 en Cola Trigger y confirma visualmente Opc B con captoora.studio/sports y la Firma Horizontal 2026.',
      pomodoros: 1,
      actionType: 'triggers',
      actionLabel: 'Abrir Autoprueba'
    },
    {
      id: 'STEP-02',
      phase: 'dom15',
      phaseTitle: 'Hoy Domingo 15 Nov · Tarde / Noche (Arranque y Autoprueba)',
      time: 'Dom 16:15 – 17:05',
      title: 'Aprobar y preparar triggers Pádel Tier-1 (APR-002 Padel GM · APR-003 PADELBOSS)',
      detail: 'Revisa los borradores en Bandeja Último Trigger (0% IA, sin "presumir") y deja listo el envío directo.',
      pomodoros: 2,
      actionType: 'triggers',
      actionLabel: 'Ir a Cola Trigger'
    },
    {
      id: 'STEP-03',
      phase: 'dom15',
      phaseTitle: 'Hoy Domingo 15 Nov · Tarde / Noche (Arranque y Autoprueba)',
      time: 'Dom 17:15 – 18:10',
      title: 'Enviar primer bloque WhatsApp + Email 2026 al Top 5 de Pádel',
      detail: 'Contactar Cuatro Padel (seguimiento), Padel GM, PADELBOSS, SB Pádel y PADEL CAMP con Opc A/B y Dossier 1 hoja.',
      pomodoros: 2,
      actionType: 'top10',
      actionLabel: 'Ir a Top 10'
    },
    {
      id: 'STEP-04',
      phase: 'dom15',
      phaseTitle: 'Hoy Domingo 15 Nov · Tarde / Noche (Arranque y Autoprueba)',
      time: 'Dom 18:20 – 19:00',
      title: 'Activar Meta Business Agent 24/7 con el Playbook Captoora',
      detail: 'Pega las instrucciones de docs/meta_business_ai_agent_playbook.md en Meta Business Suite y verifica modo Cloud / fallback.',
      pomodoros: 1,
      actionType: 'playbook',
      actionLabel: 'Copiar Prompt Meta'
    },
    {
      id: 'STEP-05',
      phase: 'lun16_am',
      phaseTitle: 'Lunes 16 Nov · Mañana 09:00 – 13:30 (Seguimiento & Galas Danza)',
      time: 'Lun 09:00 – 10:15',
      title: 'Seguimiento 24h a clubes de domingo + envío de Dossier PDF',
      detail: 'Llamada breve de 2 minutos o nota de voz a gerencias de Padel GM, Cuatro Padel y SB Pádel ofreciendo prueba sin costo.',
      pomodoros: 2,
      actionType: 'top10',
      actionLabel: 'Abrir Mesa Cierre'
    },
    {
      id: 'STEP-06',
      phase: 'lun16_am',
      phaseTitle: 'Lunes 16 Nov · Mañana 09:00 – 13:30 (Seguimiento & Galas Danza)',
      time: 'Lun 10:30 – 12:00',
      title: 'Prospección White-Glove Galas de Danza (The Movement · Danz Studio)',
      detail: 'Aprobar APR-004 y presentar esquema riesgo cero con marcos finos El Marco San Pedro y placas LED navideñas.',
      pomodoros: 2,
      actionType: 'triggers',
      actionLabel: 'Ver APR-004 Danza'
    },
    {
      id: 'STEP-07',
      phase: 'lun16_am',
      phaseTitle: 'Lunes 16 Nov · Mañana 09:00 – 13:30 (Seguimiento & Galas Danza)',
      time: 'Lun 12:15 – 13:30',
      title: 'Contacto institucional Club Sierra Madre, Deportivo San Agustín y TENNIS CENTER',
      detail: 'Enviar Email Oscuro/Claro 2026 + respaldo FEMSA / Tecate / Poder Judicial NL para posadas y torneos navideños.',
      pomodoros: 2,
      actionType: 'email_kit',
      actionLabel: 'Copiar HTML Email'
    },
    {
      id: 'STEP-08',
      phase: 'lun16_pm',
      phaseTitle: 'Lunes 16 Nov · Tarde 15:30 – 19:00 (Cotizaciones & Talleres Locales)',
      time: 'Lun 15:30 – 16:45',
      title: 'Emitir cotizaciones $12.5k/$14.5k y apartar ventana en Foco Lab y El Marco',
      detail: 'Confirmar cupo de producción 3–5 días hábiles para trofeos LED y marcos navideños con Bot 7.',
      pomodoros: 2,
      actionType: 'top10',
      actionLabel: 'Actualizar Etapas'
    },
    {
      id: 'STEP-09',
      phase: 'lun16_pm',
      phaseTitle: 'Lunes 16 Nov · Tarde 15:30 – 19:00 (Cotizaciones & Talleres Locales)',
      time: 'Lun 17:00 – 18:30',
      title: 'Aprobar Reel APR-005 (@captoora.studio) + revisar Orden de Servicio APR-006',
      detail: 'Blindar cláusula 50% anticipo / 50% entrega galería digital y derechos morales antes de cerrar contratos.',
      pomodoros: 2,
      actionType: 'triggers',
      actionLabel: 'Revisar APR-005/006'
    },
    {
      id: 'STEP-10',
      phase: 'mar17_am',
      phaseTitle: 'Martes 17 Nov · Mañana 08:30 – 12:00 PM (Cierre Final 1–3 Clientes)',
      time: 'Mar 08:30 – 10:15',
      title: 'Segundo toque con mockup Opc A/B personalizado al logo del club',
      detail: 'Acelerar decisión de prospectos en etapa "En revisión" recordando disponibilidad limitada de fechas decembrinas.',
      pomodoros: 2,
      actionType: 'top10',
      actionLabel: 'Ver En Revisión'
    },
    {
      id: 'STEP-11',
      phase: 'mar17_am',
      phaseTitle: 'Martes 17 Nov · Mañana 08:30 – 12:00 PM (Cierre Final 1–3 Clientes)',
      time: 'Mar 10:30 – 12:00',
      title: 'Cierre de Orden de Servicio y cobro 50% anticipo (Meta: 1 a 3 cierres)',
      detail: 'Confirmar transferencia 50%, marcar "Cerrado" en Mesa Top 10 y celebrar el objetivo cumplido antes de las 12:00 PM.',
      pomodoros: 2,
      actionType: 'top10',
      actionLabel: 'Registrar Cierre'
    }
  ];

  const TOP_10_PRIORITY_META = [
    {
      rank: 1,
      nombre: 'Cuatro Padel',
      pkg: 'PKG-4 · Torneo del Pavo ($12,500 MXN)',
      margin: '80.8%',
      triggerRef: 'APR-001',
      fallbackPhone: '+52 81 2354 5695',
      fallbackRating: '4.6 (30)',
      fallbackNiche: 'Pádel & Raqueta',
      fallbackMun: 'San Pedro Garza García'
    },
    {
      rank: 2,
      nombre: 'Padel GM',
      pkg: 'PKG-4 · Torneo del Pavo ($12,500 MXN)',
      margin: '80.8%',
      triggerRef: 'APR-002',
      fallbackPhone: '+52 81 1538 7900',
      fallbackRating: '4.7 (36)',
      fallbackNiche: 'Pádel & Raqueta',
      fallbackMun: 'San Pedro Garza García'
    },
    {
      rank: 3,
      nombre: 'PADELBOSS',
      pkg: 'PKG-4 · Torneo del Pavo ($12,500 MXN)',
      margin: '80.8%',
      triggerRef: 'APR-003',
      fallbackPhone: '+52 81 8691 7694',
      fallbackRating: '4.9 (24)',
      fallbackNiche: 'Pádel & Raqueta',
      fallbackMun: 'San Pedro Garza García'
    },
    {
      rank: 4,
      nombre: 'SB Pádel',
      pkg: 'PKG-4 · Torneo del Pavo ($12,500 MXN)',
      margin: '80.8%',
      triggerRef: 'APR-003',
      fallbackPhone: '+52 81 1553 8549',
      fallbackRating: '4.8 (85)',
      fallbackNiche: 'Pádel & Raqueta',
      fallbackMun: 'San Pedro Garza García'
    },
    {
      rank: 5,
      nombre: 'PADEL CAMP',
      pkg: 'PKG-4 · Torneo del Pavo ($12,500 MXN)',
      margin: '80.8%',
      triggerRef: 'Directo Tier-1',
      fallbackPhone: '+52 81 2030 5100',
      fallbackRating: '4.5 (40)',
      fallbackNiche: 'Pádel & Raqueta',
      fallbackMun: 'San Pedro Garza García'
    },
    {
      rank: 6,
      nombre: 'The Movement Dance Project',
      pkg: 'PKG-5 · Gala Navideña ($14,500 MXN)',
      margin: '78.6%',
      triggerRef: 'APR-004',
      fallbackPhone: '+52 81 2721 4413',
      fallbackRating: '5.0 (16)',
      fallbackNiche: 'Baile & Danza Señoras',
      fallbackMun: 'San Pedro Garza García'
    },
    {
      rank: 7,
      nombre: 'Danz Studio',
      pkg: 'PKG-5 · Gala Navideña ($14,500 MXN)',
      margin: '78.6%',
      triggerRef: 'White-Glove',
      fallbackPhone: '+52 81 4276 3853',
      fallbackRating: '4.8 (19)',
      fallbackNiche: 'Baile & Danza Señoras',
      fallbackMun: 'San Pedro Garza García'
    },
    {
      rank: 8,
      nombre: 'Club Sierra Madre',
      pkg: 'PKG-3 · Sponsor Proof Corp ($18,500 MXN)',
      margin: '84.9%',
      triggerRef: 'Institucional',
      fallbackPhone: '+52 81 8248 1500',
      fallbackRating: '4.6 (409)',
      fallbackNiche: 'Deporte de Alto Rendimiento',
      fallbackMun: 'San Pedro Garza García'
    },
    {
      rank: 9,
      nombre: 'Deportivo San Agustin, A.C.',
      pkg: 'PKG-3 · Sponsor Proof Corp ($18,500 MXN)',
      margin: '84.9%',
      triggerRef: 'Institucional',
      fallbackPhone: '+52 81 8133 1900',
      fallbackRating: '4.7 (535)',
      fallbackNiche: 'Deporte de Alto Rendimiento',
      fallbackMun: 'San Pedro Garza García'
    },
    {
      rank: 10,
      nombre: 'TENNIS CENTER',
      pkg: 'PKG-4 · Torneo Raqueta ($12,500 MXN)',
      margin: '80.8%',
      triggerRef: 'Raqueta SPGG',
      fallbackPhone: '+52 81 8363 3130',
      fallbackRating: '4.7 (150)',
      fallbackNiche: 'Pádel & Raqueta',
      fallbackMun: 'San Pedro Garza García'
    }
  ];

  const META_AGENT_FALLBACK_PROMPT = `Eres el asistente comercial oficial de Captoora Sports Studio (Colinas de San Jerónimo, Monterrey, N.L.). Atiendes por WhatsApp e Instagram con tono cálido, ejecutivo y de alto estándar para clubes deportivos, academias de danza y empresas en San Pedro Garza García y Monterrey.

REGLAS ESTRICTAS:
1. Nunca menciones que eres un bot ni uses "IA" o "Inteligencia Artificial" frente al cliente.
2. Nunca uses la palabra "presumir"; utiliza "proyectar una imagen profesional al nivel de excelencia de su club/academia".
3. Diferencia los tiempos de entrega: fotografía digital Halftime Blitz el mismo día; trofeos de acrílico óptico con luz LED y marcos de madera maciza en 3 a 5 días hábiles en taller local (Foco Lab / El Marco San Pedro).
4. Paquetes vigentes 2026: Torneo del Pavo Pádel ($12,500 MXN, autofinanciable por patrocinadores), Gala Navideña Danza White-Glove ($14,500 MXN), Sponsor Proof Corporativo ($18,500 MXN, CFDI 4.0 listo). Pago 50% anticipo / 50% contra entrega de galería.
5. Portafolio oficial: https://captoora.studio/sports y https://galeria.captoora.studio · WhatsApp humano: +52 81 4005 0088 (Jesús Gutiérrez).`;

  let sprintPhaseFilter = 'all';
  let top10NicheFilter = 'all';
  let pomoInterval = null;
  let pomoState = loadPomodoroState();

  function loadJsonStorage(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      if (raw) return JSON.parse(raw);
    } catch (_e) {
      // ignore storage errors in restricted contexts
    }
    return fallback;
  }

  function saveJsonStorage(key, val) {
    try {
      localStorage.setItem(key, JSON.stringify(val));
    } catch (_e) {
      // ignore storage errors
    }
  }

  function loadPomodoroState() {
    const saved = loadJsonStorage(POMO_STORAGE_KEY, null);
    const todayKey = new Date().toISOString().slice(0, 10);
    if (saved && saved.mode && POMO_MODES[saved.mode]) {
      if (saved.dateKey !== todayKey) {
        saved.dateKey = todayKey;
        saved.completedCount = 0;
      }
      if (saved.running && saved.endAtMs) {
        const left = Math.max(0, Math.ceil((saved.endAtMs - Date.now()) / 1000));
        saved.remainingSec = left;
        if (left === 0) {
          saved.running = false;
          saved.endAtMs = null;
        }
      }
      return saved;
    }
    return {
      mode: 'focus25',
      remainingSec: POMO_MODES.focus25.seconds,
      running: false,
      endAtMs: null,
      activeStepId: SPRINT_PLAN_STEPS[0].id,
      completedCount: 0,
      soundEnabled: true,
      dateKey: todayKey
    };
  }

  function savePomodoroState() {
    saveJsonStorage(POMO_STORAGE_KEY, pomoState);
  }

  function announcePomo(msg) {
    const el = document.getElementById('pomoAnnouncer');
    if (el) el.textContent = msg;
  }

  function playPomoChime() {
    if (!pomoState.soundEnabled) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      [528, 792].forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.value = freq;
        const start = ctx.currentTime + idx * 0.16;
        gain.gain.setValueAtTime(0.001, start);
        gain.gain.exponentialRampToValueAtTime(0.14, start + 0.03);
        gain.gain.exponentialRampToValueAtTime(0.001, start + 0.45);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(start);
        osc.stop(start + 0.48);
      });
    } catch (_e) {
      // silent fallback if audio context is blocked
    }
  }

  function getSprintCheckedMap() {
    return loadJsonStorage(SPRINT_STEPS_STORAGE_KEY, {});
  }

  function getTop10StagesMap() {
    const defaults = {};
    const items = (workspaceState.approvals && workspaceState.approvals.items) || [];
    const apr1 = items.find((i) => i.id === 'APR-001');
    if (apr1 && apr1.status === 'approved') {
      defaults['Cuatro Padel'] = 'contactado';
    }
    const stored = loadJsonStorage(TOP10_STAGES_STORAGE_KEY, null);
    return Object.assign({}, defaults, stored || {});
  }

  function getResolvedTop10Leads() {
    const liveList = (typeof window.getCaptooraLeadsCache === 'function' && window.getCaptooraLeadsCache()) || [];
    const stages = getTop10StagesMap();
    return TOP_10_PRIORITY_META.map((meta) => {
      const live = liveList.find((l) => String(l.nombre || '').toLowerCase() === meta.nombre.toLowerCase()) || {};
      const nombre = live.nombre || meta.nombre;
      const telefono = live.telefono || meta.fallbackPhone;
      const nicho = live.nicho || meta.fallbackNiche;
      const rating = live.rating ? `${live.rating} (${live.resenas || 0})` : meta.fallbackRating;
      const municipio = live.municipio || meta.fallbackMun;
      const web = live.sitio_web || 'https://captoora.studio/sports';
      const stage = stages[meta.nombre] || 'pendiente';
      return {
        rank: meta.rank,
        nombre,
        telefono,
        nicho,
        rating,
        municipio,
        web,
        pkg: meta.pkg,
        margin: meta.margin,
        triggerRef: meta.triggerRef,
        stage
      };
    });
  }

  function buildTop10Pitch(lead) {
    let text = `Hola, te saluda Jesús Gutiérrez de Captoora Studio aquí en Monterrey. Para ${lead.nombre} abrimos nuestro -35% Descuento de Temporada 2026 en 3 opciones flexibles (Digital $3,185 · Marcos $5,135 · Suite LED $7,475*, pagando placas LED en 2do momento) + renovación de portada Google Maps y galería el mismo día para proyectar en redes sociales una imagen profesional al nivel de excelencia de su club. Portafolio: https://captoora.studio/sports — ¿lo revisamos 2 minutos?`;
    if (lead.nicho === 'Baile & Danza Señoras') {
      text = `Hola, te saluda Jesús Gutiérrez de Captoora Studio en San Jerónimo, Monterrey. Para la Gala Navideña de ${lead.nombre} tenemos esquema White-Glove y -35% Descuento de Temporada desde $3,575 MXN (digital el mismo día + marcos de madera fina / placas LED en 3 a 5 días hábiles + optimización Google Maps y Meta). Portafolio: https://captoora.studio/sports`;
    } else if (lead.nicho === 'Deporte de Alto Rendimiento') {
      text = `Hola, te saluda Jesús Gutiérrez de Captoora Studio (San Jerónimo, MTY). Contamos con experiencia comprobada para Coca-Cola FEMSA, Tecate y Poder Judicial NL, y hoy ofrecemos a ${lead.nombre} -35% de Temporada en nuestras 3 modalidades (Digital el mismo día + acrílicos LED en 3-5 días en taller local + Small Business 2027) con facturación CFDI 4.0. Portafolio: https://captoora.studio/sports`;
    }
    if (checkClientCopyGuardrail(text).length > 0) {
      return `Hola, te saluda Jesús Gutiérrez de Captoora Studio. Portafolio oficial en https://captoora.studio/sports.`;
    }
    return text;
  }

  function computeVisualBedSummary() {
    const stepsMap = getSprintCheckedMap();
    const stepsDone = SPRINT_PLAN_STEPS.filter((s) => !!stepsMap[s.id]).length;
    const totalSteps = SPRINT_PLAN_STEPS.length;

    const approvalItems = (workspaceState.approvals && workspaceState.approvals.items) || [];
    const pendingTriggers = approvalItems.filter((i) => i.status === 'pending_trigger');
    const approvedTriggers = approvalItems.filter((i) => i.status === 'approved');

    const asanaTasks = (workspaceState.asana && workspaceState.asana.tasks) || [];
    const doneTasks = asanaTasks.filter((t) => t.status === 'done').length;

    const top10 = getResolvedTop10Leads();
    const touchedTop10 = top10.filter((l) => l.stage !== 'pendiente').length;
    const closedTop10 = top10.filter((l) => l.stage === 'cerrado').length;

    const cloud = workspaceState.whatsapp_cloud || DEFAULT_WORKSPACE.whatsapp_cloud;
    const cloudActive = cloud.mode === 'meta_cloud_api';
    const leadsCache = typeof window.getCaptooraLeadsCache === 'function' ? window.getCaptooraLeadsCache() : [];
    const totalLeadsCount = Math.max(leadsCache.length || 0, (workspaceState.gmaps_audits && workspaceState.gmaps_audits.total_leads) || 138);
    const gmapsAuditData = workspaceState.gmaps_audits || {};
    const capturedMapsCount = gmapsAuditData.captured_count || 0;
    const deficientMapsCount = gmapsAuditData.deficient_count || 0;

    const assetWeight = 25;
    const stepsWeight = totalSteps > 0 ? (stepsDone / totalSteps) * 40 : 0;
    const touchWeight = (Math.min(touchedTop10, 5) / 5) * 15;
    const dealWeight = (Math.min(closedTop10, 1) / 1) * 20;
    const readinessPct = Math.min(100, Math.round(assetWeight + stepsWeight + touchWeight + dealWeight));

    const readyItems = [
      {
        title: 'Kit Visual -35%, Biogen & Small Biz 2027',
        badge: 'LISTO',
        desc: 'Opc A/B, Dossier 3 Opciones -35% + Biogen Beta, Antes/Después SMB PNG + PDF y Emails 2026.'
      },
      {
        title: 'Auditor Google Maps Visual (Chrome CDP)',
        badge: capturedMapsCount > 0 ? `${capturedMapsCount} PNGs` : 'LISTO',
        desc: `${deficientMapsCount || '68'} fichas con oportunidad editorial detectada (Street View, 0 fotos, Sin reclamar) en SPGG/MTY.`
      },
      {
        title: 'Base Prospección & 4 Caminos en Paralelo',
        badge: `${totalLeadsCount} LEADS`,
        desc: `Navidad, TotalPass, Biogen Beta y Small Biz 2027 activos con ${approvedTriggers.length} envío(s) aprobado(s).`
      },
      {
        title: 'Motor Local SDK, Semáforo API & Contabilidad',
        badge: `${doneTasks}/${asanaTasks.length} ASANA`,
        desc: 'Márgenes >=68% aún con -35% OFF, póliza 50/50 y split físico diferible en :8765.'
      }
    ];

    const missingItems = [
      {
        title: `Triggers Pendientes (${pendingTriggers.length})`,
        badge: pendingTriggers.length > 0 ? 'POR APROBAR' : 'AL DÍA',
        desc: pendingTriggers.length > 0
          ? `Autorizar y enviar ${pendingTriggers.slice(0, 3).map((i) => i.id).join(', ')} en Bandeja de Último Trigger.`
          : 'Cola de triggers despejada; genera un nuevo lote con Ventas B2B si necesitas más alcance.'
      },
      {
        title: `Plan Horario Sprint (${totalSteps - stepsDone} restantes)`,
        badge: `${stepsDone}/${totalSteps}`,
        desc: 'Ejecutar bloques Dom 15 -> Mar 17 12:00 PM usando el reloj Pomodoro sin saltar seguimiento.'
      },
      {
        title: cloudActive ? 'Meta Cloud API Conectada' : 'Credenciales Meta Cloud (.env)',
        badge: cloudActive ? 'EN VIVO' : 'MODO WA.ME',
        desc: cloudActive
          ? 'Envío directo vía Graph API habilitado sin depender de QR.'
          : 'Operando vía wa.me / WhatsApp Desktop en 1 clic; agrega tokens en .env cuando requieras envío silencioso.'
      },
      {
        title: 'Cierres Confirmados (Meta 1–3)',
        badge: `${closedTop10} / 1–3`,
        desc: closedTop10 >= 1
          ? `¡Excelente! ${closedTop10} cierre(s) registrado(s). Mantén empuje para consolidar hasta 3 acuerdos antes del martes 12 PM.`
          : 'Falta registrar el primer "Sí" firmado + 50% de anticipo en la Mesa de Cierre Top 10.'
      }
    ];

    return {
      readinessPct,
      stepsDone,
      totalSteps,
      pendingTriggersCount: pendingTriggers.length,
      touchedTop10,
      closedTop10,
      cloud,
      readyItems,
      missingItems
    };
  }

  function renderVisualBedAndCloud(summary) {
    const pctEl = document.getElementById('sprintReadinessPctLabel');
    const progEl = document.getElementById('sprintReadinessProgress');
    const stepsEl = document.getElementById('bedStepsMetric');
    const trigEl = document.getElementById('bedTriggersMetric');
    const topEl = document.getElementById('bedTop10Metric');
    const dealsEl = document.getElementById('bedDealsMetric');
    const readyList = document.getElementById('visualBedReadyList');
    const missingList = document.getElementById('visualBedMissingList');
    const cloudBox = document.getElementById('sprintCloudStatusBox');

    if (pctEl) pctEl.textContent = `Avance: ${summary.readinessPct}%`;
    if (progEl) progEl.value = summary.readinessPct;
    if (stepsEl) stepsEl.textContent = `${summary.stepsDone} / ${summary.totalSteps}`;
    if (trigEl) trigEl.textContent = String(summary.pendingTriggersCount);
    if (topEl) topEl.textContent = `${summary.touchedTop10} / 10`;
    if (dealsEl) dealsEl.textContent = `${summary.closedTop10} / 1–3`;

    const rowRenderer = (item) => `
      <div class="bed-item-row">
        <div>
          <strong style="color:var(--bone-white); font-weight:500;">${escapeHtml(item.title)}</strong>
          <div style="color:#9ea3b5; font-size:0.72rem; margin-top:2px;">${escapeHtml(item.desc)}</div>
        </div>
        <span class="source-type-badge" style="white-space:nowrap;">${escapeHtml(item.badge)}</span>
      </div>
    `;

    if (readyList) readyList.innerHTML = summary.readyItems.map(rowRenderer).join('');
    if (missingList) missingList.innerHTML = summary.missingItems.map(rowRenderer).join('');

    if (cloudBox) {
      const c = summary.cloud || {};
      const isCloud = c.mode === 'meta_cloud_api';
      const missingText = Array.isArray(c.missing_env) && c.missing_env.length > 0
        ? c.missing_env.join(', ')
        : 'Ninguna';
      cloudBox.innerHTML = `
        <div class="sim-row"><span class="sim-label">Modo de Despacho</span><span class="sim-val">${isCloud ? 'Meta Cloud API Activo (Zero QR)' : 'Fallback wa.me + Playbook Agent'}</span></div>
        <div class="sim-row"><span class="sim-label">Variables .env Pendientes</span><span class="sim-val" style="font-size:0.7rem;">${escapeHtml(missingText)}</span></div>
      `;
    }
  }

  function renderPomodoroUi() {
    const digitsEl = document.getElementById('pomoTimeDigits');
    const labelEl = document.getElementById('pomoPhaseLabel');
    const progEl = document.getElementById('pomoProgressBar');
    const faceEl = document.getElementById('pomoTimerFace');
    const toggleEl = document.getElementById('pomoToggleBtn');
    const countEl = document.getElementById('pomoCompletedCount');
    const soundEl = document.getElementById('pomoSoundBtn');
    const activeStepEl = document.getElementById('pomoActiveStepLabel');
    const selectEl = document.getElementById('pomoStepSelect');

    const modeCfg = POMO_MODES[pomoState.mode] || POMO_MODES.focus25;
    const rem = Math.max(0, Number(pomoState.remainingSec || 0));
    const mins = Math.floor(rem / 60);
    const secs = rem % 60;
    const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    const pct = modeCfg.seconds > 0
      ? Math.min(100, Math.max(0, Math.round(((modeCfg.seconds - rem) / modeCfg.seconds) * 100)))
      : 0;

    if (digitsEl) digitsEl.textContent = formatted;
    if (labelEl) labelEl.textContent = modeCfg.label;
    if (progEl) progEl.value = pct;
    if (faceEl) faceEl.classList.toggle('running', !!pomoState.running);
    if (toggleEl) toggleEl.textContent = pomoState.running ? '❚❚ Pausar Bloque' : (rem < modeCfg.seconds && rem > 0 ? '▶ Reanudar' : '▶ Iniciar Bloque');
    if (countEl) countEl.textContent = String(pomoState.completedCount || 0);
    if (soundEl) soundEl.textContent = pomoState.soundEnabled ? '🔔 Sonido: Sí' : '🔕 Silencio';

    document.querySelectorAll('[data-pomo-mode]').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.pomoMode === pomoState.mode);
    });

    if (selectEl && selectEl.options.length === 0) {
      SPRINT_PLAN_STEPS.forEach((step) => {
        selectEl.add(new Option(`${step.time} · ${step.title}`, step.id));
      });
    }
    if (selectEl && document.activeElement !== selectEl) {
      selectEl.value = pomoState.activeStepId || SPRINT_PLAN_STEPS[0].id;
    }

    const activeStep = SPRINT_PLAN_STEPS.find((s) => s.id === pomoState.activeStepId) || SPRINT_PLAN_STEPS[0];
    if (activeStepEl && activeStep) {
      activeStepEl.textContent = `En foco: [${activeStep.time}] ${activeStep.title}`;
    }
  }

  function startPomodoroTicker() {
    if (pomoInterval) clearInterval(pomoInterval);
    pomoInterval = setInterval(() => {
      if (!pomoState.running || !pomoState.endAtMs) return;
      const left = Math.max(0, Math.ceil((pomoState.endAtMs - Date.now()) / 1000));
      pomoState.remainingSec = left;
      if (left <= 0) {
        pomoState.running = false;
        pomoState.endAtMs = null;
        if (pomoState.mode === 'focus25' || pomoState.mode === 'sprint15') {
          pomoState.completedCount = (pomoState.completedCount || 0) + 1;
        }
        savePomodoroState();
        playPomoChime();
        announcePomo(`Bloque ${POMO_MODES[pomoState.mode].label} completado.`);
        showToast('¡Bloque Pomodoro completado! Marca tu avance o toma 5 min de pausa.');
      }
      renderPomodoroUi();
    }, 1000);
  }

  window.setPomodoroMode = function (modeKey) {
    if (!POMO_MODES[modeKey]) return;
    pomoState.mode = modeKey;
    pomoState.running = false;
    pomoState.endAtMs = null;
    pomoState.remainingSec = POMO_MODES[modeKey].seconds;
    savePomodoroState();
    renderPomodoroUi();
    announcePomo(`Modo cambiado a ${POMO_MODES[modeKey].label}.`);
  };

  window.togglePomodoroTimer = function () {
    const modeCfg = POMO_MODES[pomoState.mode] || POMO_MODES.focus25;
    if (pomoState.running) {
      pomoState.remainingSec = Math.max(0, Math.ceil((pomoState.endAtMs - Date.now()) / 1000));
      pomoState.running = false;
      pomoState.endAtMs = null;
      savePomodoroState();
      renderPomodoroUi();
      announcePomo('Temporizador Pomodoro en pausa.');
      return;
    }
    if (pomoState.remainingSec <= 0) {
      pomoState.remainingSec = modeCfg.seconds;
    }
    pomoState.running = true;
    pomoState.endAtMs = Date.now() + pomoState.remainingSec * 1000;
    savePomodoroState();
    startPomodoroTicker();
    renderPomodoroUi();
    announcePomo(`Iniciado ${modeCfg.label}.`);
  };

  window.resetPomodoroTimer = function () {
    const modeCfg = POMO_MODES[pomoState.mode] || POMO_MODES.focus25;
    pomoState.running = false;
    pomoState.endAtMs = null;
    pomoState.remainingSec = modeCfg.seconds;
    savePomodoroState();
    renderPomodoroUi();
    announcePomo('Temporizador reiniciado.');
  };

  window.completePomodoroBlock = function (markActiveStepDone = true) {
    const modeCfg = POMO_MODES[pomoState.mode] || POMO_MODES.focus25;
    pomoState.running = false;
    pomoState.endAtMs = null;
    pomoState.remainingSec = modeCfg.seconds;
    pomoState.completedCount = (pomoState.completedCount || 0) + 1;
    if (markActiveStepDone && pomoState.activeStepId) {
      const checked = getSprintCheckedMap();
      checked[pomoState.activeStepId] = true;
      saveJsonStorage(SPRINT_STEPS_STORAGE_KEY, checked);
      const nextOpen = SPRINT_PLAN_STEPS.find((s) => !checked[s.id]);
      if (nextOpen) pomoState.activeStepId = nextOpen.id;
    }
    savePomodoroState();
    playPomoChime();
    announcePomo('Bloque registrado como completado.');
    renderSprintMartesHub();
    showToast('Bloque completado y checklist del sprint actualizado.');
  };

  window.togglePomodoroSound = function () {
    pomoState.soundEnabled = !pomoState.soundEnabled;
    savePomodoroState();
    renderPomodoroUi();
  };

  window.selectPomodoroStep = function (stepId) {
    pomoState.activeStepId = stepId;
    savePomodoroState();
    renderSprintMartesHub();
  };

  window.focusStepInPomodoro = function (stepId, autoStart = true) {
    pomoState.activeStepId = stepId;
    if (pomoState.mode !== 'focus25' && pomoState.mode !== 'sprint15') {
      pomoState.mode = 'focus25';
      pomoState.remainingSec = POMO_MODES.focus25.seconds;
    }
    if (autoStart) {
      if (pomoState.remainingSec <= 0) pomoState.remainingSec = POMO_MODES[pomoState.mode].seconds;
      pomoState.running = true;
      pomoState.endAtMs = Date.now() + pomoState.remainingSec * 1000;
      startPomodoroTicker();
    }
    savePomodoroState();
    renderSprintMartesHub();
    const pomoCard = document.getElementById('pomodoroHeading');
    if (pomoCard && typeof pomoCard.scrollIntoView === 'function') {
      pomoCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    showToast('Paso cargado en Pomodoro: ¡ejecutemos ese bloque!');
  };

  window.toggleSprintStepDone = function (stepId) {
    const checked = getSprintCheckedMap();
    checked[stepId] = !checked[stepId];
    saveJsonStorage(SPRINT_STEPS_STORAGE_KEY, checked);
    renderSprintMartesHub();
  };

  window.setSprintPhaseFilter = function (phase, btnEl) {
    sprintPhaseFilter = phase || 'all';
    document.querySelectorAll('[data-sprint-phase]').forEach((b) => {
      b.classList.toggle('active', b === btnEl || b.dataset.sprintPhase === sprintPhaseFilter);
    });
    renderSprintStepsList();
  };

  window.resetSprintChecklist = function () {
    saveJsonStorage(SPRINT_STEPS_STORAGE_KEY, {});
    renderSprintMartesHub();
    showToast('Checklist horario reiniciado para un nuevo ciclo.');
  };

  window.triggerSprintStepAction = function (actionType) {
    if (actionType === 'triggers') {
      window.switchTab('proyectos-asana');
    } else if (actionType === 'playbook') {
      window.copyMetaAgentPlaybook();
    } else if (actionType === 'email_kit') {
      window.copyTemplateHtmlFile('assets/mockups/test/Captoora_Email_Oscuro_Navidad2026.html', 'Email Oscuro 2026');
    } else if (actionType === 'top10') {
      const el = document.getElementById('sprintTop10Section');
      if (el && typeof el.scrollIntoView === 'function') {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  };

  function renderSprintStepsList() {
    const container = document.getElementById('sprintStepsContainer');
    if (!container) return;

    const checked = getSprintCheckedMap();
    const visibleSteps = SPRINT_PLAN_STEPS.filter((s) => sprintPhaseFilter === 'all' || s.phase === sprintPhaseFilter);

    const groups = [];
    visibleSteps.forEach((step) => {
      let grp = groups.find((g) => g.phase === step.phase);
      if (!grp) {
        grp = { phase: step.phase, phaseTitle: step.phaseTitle, items: [] };
        groups.push(grp);
      }
      grp.items.push(step);
    });

    container.innerHTML = groups.map((grp) => `
      <div class="sprint-phase-group">
        <div class="sprint-phase-header">
          <div class="sprint-phase-title">${escapeHtml(grp.phaseTitle)}</div>
          <span class="source-type-badge">${grp.items.filter((s) => !!checked[s.id]).length}/${grp.items.length} hechos</span>
        </div>
        ${grp.items.map((step) => {
          const isDone = !!checked[step.id];
          const isFocused = pomoState.activeStepId === step.id;
          const chkId = `sprintChk_${step.id}`;
          return `
            <div class="sprint-step-row ${isDone ? 'done' : ''} ${isFocused ? 'focused' : ''}">
              <div class="sprint-step-main">
                <input type="checkbox" id="${chkId}" class="task-checkbox-custom" ${isDone ? 'checked' : ''} onchange="toggleSprintStepDone('${step.id}')">
                <div>
                  <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center; margin-bottom:3px;">
                    <span class="task-day-badge">${escapeHtml(step.time)}</span>
                    <span class="source-type-badge">${step.pomodoros} Pomodoro${step.pomodoros > 1 ? 's' : ''}</span>
                    ${isFocused ? '<span class="badge-test-mode" style="margin:0;">EN FOCO</span>' : ''}
                  </div>
                  <label for="${chkId}" class="sprint-step-title">${escapeHtml(step.title)}</label>
                  <div class="sprint-step-sub">${escapeHtml(step.detail)}</div>
                </div>
              </div>
              <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
                <button type="button" class="week-btn" onclick="triggerSprintStepAction('${step.actionType}')">${escapeHtml(step.actionLabel)} &rarr;</button>
                <button type="button" class="btn-volt-cta" style="padding:6px 12px; font-size:0.72rem;" onclick="focusStepInPomodoro('${step.id}', true)">▶ Enfocar</button>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `).join('');
  }

  window.setTop10NicheFilter = function (niche, btnEl) {
    top10NicheFilter = niche || 'all';
    document.querySelectorAll('[data-top10-niche]').forEach((b) => {
      b.classList.toggle('active', b === btnEl || b.dataset.top10Niche === top10NicheFilter);
    });
    renderTop10LeadsTable();
  };

  window.updateTop10Stage = function (leadName, newStage) {
    const map = getTop10StagesMap();
    map[leadName] = newStage;
    saveJsonStorage(TOP10_STAGES_STORAGE_KEY, map);
    renderSprintMartesHub();
    showToast(`${leadName}: estado actualizado a ${newStage.toUpperCase()}.`);
  };

  function renderTop10LeadsTable() {
    const container = document.getElementById('top10LeadsContainer');
    const summaryEl = document.getElementById('top10DealsSummary');
    if (!container) return;

    const allLeads = getResolvedTop10Leads();
    const closedCount = allLeads.filter((l) => l.stage === 'cerrado').length;
    if (summaryEl) summaryEl.textContent = `${closedCount} cerrados · Meta 1–3`;

    const query = ((document.getElementById('top10SearchInput') || {}).value || '').trim().toLowerCase();
    const filtered = allLeads.filter((l) => {
      const matchesNiche = top10NicheFilter === 'all' || l.nicho === top10NicheFilter;
      const matchesQ = !query
        || l.nombre.toLowerCase().includes(query)
        || l.nicho.toLowerCase().includes(query)
        || l.pkg.toLowerCase().includes(query);
      return matchesNiche && matchesQ;
    });

    if (filtered.length === 0) {
      container.innerHTML = '<div style="color:var(--slate-muted); font-size:0.8rem;">No hay leads con ese filtro en el Top 10.</div>';
      return;
    }

    const stages = [
      { value: 'pendiente', label: 'Sin contactar' },
      { value: 'contactado', label: 'Contactado (WhatsApp/Mail)' },
      { value: 'en_revision', label: 'En revisión / PDF enviado' },
      { value: 'cerrado', label: '✓ Cerrado (50% Anticipo)' }
    ];

    container.innerHTML = '';
    filtered.forEach((lead) => {
      const cleanDigits = String(lead.telefono || '').replace(/[^0-9]/g, '');
      const pitch = buildTop10Pitch(lead);
      const waHref = cleanDigits ? `https://wa.me/${cleanDigits}?text=${encodeURIComponent(pitch)}` : '#';
      const card = document.createElement('div');
      card.className = `top10-lead-card stage-${lead.stage}`;
      const selId = `top10StageSel_${lead.rank}`;
      card.innerHTML = `
        <div>
          <div class="comp-top-strip">
            <span class="comp-name-title">#${lead.rank} · ${escapeHtml(lead.nombre)}</span>
            <span class="task-day-badge">${escapeHtml(lead.triggerRef)}</span>
          </div>
          <div class="comp-meta-row"><strong>Nicho:</strong> ${escapeHtml(lead.nicho)} · ⭐ ${escapeHtml(lead.rating)}</div>
          <div class="comp-meta-row"><strong>Paquete:</strong> ${escapeHtml(lead.pkg)} · <span style="color:#a7c5ad;">Margen ${escapeHtml(lead.margin)}</span></div>
          <div class="comp-meta-row"><strong>Teléfono:</strong> ${escapeHtml(lead.telefono)} · ${escapeHtml(lead.municipio)}</div>
        </div>
        <div style="display:flex; flex-direction:column; gap:10px; border-top:1px solid var(--glass-border-subtle); padding-top:10px;">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap;">
            <label for="${selId}" style="font-family:var(--font-mono); font-size:0.64rem; color:var(--slate-muted);">ESTADO:</label>
            <select id="${selId}" class="glass-select-input" style="flex:1; min-width:170px; padding:5px 8px; font-size:0.74rem;">
              ${stages.map((st) => `<option value="${st.value}" ${lead.stage === st.value ? 'selected' : ''}>${escapeHtml(st.label)}</option>`).join('')}
            </select>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap;">
            <a href="${escapeHtml(lead.web)}" target="_blank" rel="noopener" class="link-source-action" style="font-size:0.7rem;">Web / Perfil &rarr;</a>
            <div style="display:flex; gap:6px;">
              ${cleanDigits ? `<a href="${escapeHtml(waHref)}" target="_blank" rel="noopener" class="btn-portal-link" style="padding:5px 11px; font-size:0.71rem;">WhatsApp Pitch &rarr;</a>` : ''}
            </div>
          </div>
        </div>
      `;
      const selEl = card.querySelector('select');
      if (selEl) {
        selEl.addEventListener('change', (ev) => window.updateTop10Stage(lead.nombre, ev.target.value));
      }
      container.appendChild(card);
    });
  }

  window.copyMetaAgentPlaybook = async function () {
    let content = META_AGENT_FALLBACK_PROMPT;
    try {
      const res = await fetch(resolveAssetUrl('docs/meta_business_ai_agent_playbook.md'));
      if (res.ok) {
        const mdText = await res.text();
        if (mdText && mdText.trim().length > 100) content = mdText;
      }
    } catch (_e) {
      // use inline safe prompt when opened offline
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(content).then(() => {
        showToast('Prompt y Playbook de Meta Business Agent copiado al portapapeles.');
      }).catch(() => {
        showToast('Abre docs/meta_business_ai_agent_playbook.md para copiar el texto.');
      });
    } else {
      showToast('Abre docs/meta_business_ai_agent_playbook.md para copiar el playbook.');
    }
  };

  window.copyTemplateHtmlFile = async function (relPath, label) {
    const url = resolveAssetUrl(relPath);
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const html = await res.text();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(html);
        showToast(`HTML de "${label}" copiado al portapapeles.`);
        return;
      }
    } catch (_e) {
      // fallback opening preview
    }
    window.open(url, '_blank', 'noopener');
    showToast(`Vista previa "${label}" abierta para copiar directo.`);
  };

  window.renderSprintMartesHub = function () {
    const summary = computeVisualBedSummary();
    renderVisualBedAndCloud(summary);
    renderPomodoroUi();
    renderSprintStepsList();
    renderTop10LeadsTable();
  };

  // =========================================================================
  // 6. API TOKEN SEMAPHORE, DRY-RUN SWITCH & SELF-TEST BUNDLE TRIGGER
  // =========================================================================
  function getResolvedTelemetry() {
    return workspaceState.usage_telemetry || DEFAULT_WORKSPACE.usage_telemetry;
  }

  function renderTokenUsageTelemetry() {
    const tel = getResolvedTelemetry();
    const sem = String(tel.semaphore || 'verde').toLowerCase();
    const badgeEl = document.getElementById('tokenSemaphoreBadge');
    const textEl = document.getElementById('tokenSemaphoreText');
    const hintEl = document.getElementById('tokenUsageHint');
    const metricsEl = document.getElementById('tokenUsageMetricsText');
    const waEl = document.getElementById('waQuotaBadge');
    const dryBtn = document.getElementById('btnToggleDryRun');

    const semLabels = {
      verde: 'VERDE · Operación Saludable',
      ambar: 'ÁMBAR · Moderado / Ahorro Sugerido',
      rojo: 'ROJO · Límite Cercano / Usar Modo Cero Tokens'
    };

    if (badgeEl) {
      badgeEl.classList.remove('ambar', 'rojo');
      if (sem === 'ambar' || sem === 'rojo') badgeEl.classList.add(sem);
    }
    if (textEl) textEl.textContent = semLabels[sem] || semLabels.verde;
    if (hintEl) hintEl.textContent = tel.action_hint || 'Operación saludable bajo demanda.';

    const tokens = tel.tokens || {};
    const cost = tel.cost_approx || {};
    const act = tel.activity || {};
    if (metricsEl) {
      const totalTok = Number(tokens.total || 0);
      const budgetTok = Number(tokens.budget || 250000);
      const pctTok = Number(tokens.pct || 0).toFixed(1);
      const usd = Number(cost.usd || 0).toFixed(2);
      const mxn = Number(cost.mxn || 0).toFixed(0);
      metricsEl.textContent = `Tokens: ${totalTok.toLocaleString()} / ${budgetTok.toLocaleString()} (${pctTok}%) · ~US$${usd} ($${mxn} MXN) · ${act.sdk_sessions || 0} sesiones`;
    }

    const wa = tel.whatsapp_quota || {};
    if (waEl) {
      waEl.textContent = `WA Mes: ${Number(wa.month_used || 0).toLocaleString()} / ${Number(wa.monthly_free_limit || 1000).toLocaleString()} gratis`;
    }

    const dryPreferred = Boolean((tel.limits || {}).dry_run_preferred);
    if (dryBtn) {
      dryBtn.textContent = `Modo Cero Tokens: ${dryPreferred ? 'ON' : 'OFF'}`;
      dryBtn.classList.toggle('active', dryPreferred);
    }
  }

  window.toggleDryRunMode = async function () {
    const tel = getResolvedTelemetry();
    const limits = tel.limits || {};
    const nextDry = !Boolean(limits.dry_run_preferred);

    if (serverOnline) {
      try {
        const res = await fetch(`${API_BASE}/api/usage/limits`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            daily_token_budget: Number(limits.daily_token_budget || 250000),
            monthly_whatsapp_limit: Number(limits.monthly_whatsapp_limit || 1000),
            daily_usd_limit: Number(limits.daily_usd_limit || 5.0),
            dry_run_preferred: nextDry
          })
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        if (data.workspace) {
          workspaceState = data.workspace;
        } else if (data.usage_telemetry) {
          workspaceState.usage_telemetry = data.usage_telemetry;
        }
        saveOfflineState();
        renderTokenUsageTelemetry();
        showToast(`Modo Cero Tokens ${nextDry ? 'ACTIVADO (protección activa)' : 'DESACTIVADO'}.`);
        return;
      } catch (err) {
        showToast('Error al actualizar límite: ' + err.message);
        return;
      }
    }

    if (!workspaceState.usage_telemetry) workspaceState.usage_telemetry = deepClone(DEFAULT_WORKSPACE.usage_telemetry);
    workspaceState.usage_telemetry.limits.dry_run_preferred = nextDry;
    saveOfflineState();
    renderTokenUsageTelemetry();
    showToast(`Modo Cero Tokens ${nextDry ? 'ACTIVADO (vista local)' : 'DESACTIVADO'}.`);
  };

  window.triggerGenerateSelfTestBundle = async function () {
    if (!serverOnline) {
      showToast('Inicia el servidor FastAPI (:8765) para regenerar PNGs, PDFs -35% y el archivo .eml.');
      return;
    }
    showToast('Regenerando kit completo (-35%, Biogen Beta, SMB Antes/Después PNG+PDF y .eml)...');
    try {
      const res = await fetch(`${API_BASE}/api/self-test/generate`, { method: 'POST' });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al generar autoprueba');
      if (data.workspace) workspaceState = data.workspace;
      saveOfflineState();
      renderAllWorkspacePanels();
      showToast('Kit de autoprueba completo regenerado en assets/mockups/test/.');
    } catch (err) {
      showToast('Error al generar autoprueba: ' + err.message);
    }
  };

  // =========================================================================
  // 7. CAPTOORA SMALL BUSINESS 2027 & GOOGLE MAPS VISUAL AUDITOR
  // =========================================================================
  function getGmapsAuditsIndex() {
    return workspaceState.gmaps_audits || DEFAULT_WORKSPACE.gmaps_audits;
  }

  function findAuditBySlug(slug) {
    const audits = (getGmapsAuditsIndex().audits) || [];
    return audits.find((a) => a.slug === slug) || null;
  }

  async function fetchStaticGmapsFallback() {
    try {
      const res = await fetch('data/gmaps_audits.json', { cache: 'no-store' });
      if (res.ok) {
        const data = await res.json();
        if (data && Array.isArray(data.audits)) {
          workspaceState.gmaps_audits = data;
          saveOfflineState();
          window.renderGmapsAuditsHub();
          window.renderSprintMartesHub();
          return true;
        }
      }
    } catch (_err) {
      // ignore offline file:// CORS blocks
    }
    return false;
  }

  window.syncGmapsAuditsFromServer = async function (forceRefresh = false) {
    if (serverOnline || window.location.protocol.startsWith('http')) {
      try {
        const res = await fetch(`${API_BASE}/api/gmaps-audits?refresh=${forceRefresh ? 'true' : 'false'}`, { cache: 'no-store' });
        if (res.ok) {
          const data = await res.json();
          workspaceState.gmaps_audits = data;
          saveOfflineState();
          window.renderGmapsAuditsHub();
          window.renderSprintMartesHub();
          if (forceRefresh) showToast(`Auditorías sincronizadas: ${data.total_audited || 0} fichas evaluadas.`);
          return true;
        }
      } catch (_err) {
        // fall through to static JSON fallback
      }
    }
    const ok = await fetchStaticGmapsFallback();
    if (!ok && forceRefresh) {
      showToast('Inicia el servidor :8765 para refrescar auditorías desde Chrome CDP.');
    }
    return ok;
  };

  window.captureGmapsBatch = async function (slug = null, limit = 8) {
    if (!serverOnline) {
      showToast('Inicia el servidor :8765 para ejecutar capturas en Chrome CDP.');
      return;
    }
    const btn = document.getElementById('btnCaptureGmapsBatch');
    if (btn) {
      btn.disabled = true;
      btn.textContent = slug ? 'Capturando ficha...' : 'Capturando lote CDP...';
    }
    showToast(slug ? `Capturando Google Maps real para ${slug}...` : `Capturando hasta ${limit} fichas faltantes en Chrome CDP...`);

    try {
      const res = await fetch(`${API_BASE}/api/gmaps-audits/capture`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ limit: Number(limit) || 8, slug: slug || null, overwrite: Boolean(slug) })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al capturar Google Maps');
      if (data.workspace) workspaceState = data.workspace;
      saveOfflineState();
      renderAllWorkspacePanels();
      const capturedCount = (data.summary && data.summary.captured_count) || (getGmapsAuditsIndex().captured_count || 0);
      showToast(`Captura CDP completada (${capturedCount} PNGs totales en archivo).`);
      if (slug && document.getElementById('smbAuditDialog')?.open) {
        window.openSmbAuditDialog(slug);
      }
    } catch (err) {
      showToast('Error CDP: ' + err.message);
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.textContent = 'Capturar Faltantes (Chrome CDP) →';
      }
    }
  };

  window.generateSmallBusinessAudit = async function (slug, enqueueMode = 'all', afterHeroVariant = 'studio') {
    if (!serverOnline) {
      showToast('Inicia el servidor :8765 para renderizar la lámina Antes/Después y PDF personalizado.');
      return;
    }
    const resolvedVariant = afterHeroVariant === 'sports' ? 'sports' : 'studio';
    showToast(`Generando Antes/Después PNG + Dossier PDF (-35%) para ${slug}...`);
    try {
      const res = await fetch(`${API_BASE}/api/small-business/generate-audit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, enqueue_mode: enqueueMode, after_hero_variant: resolvedVariant })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al generar auditoría SMB');
      if (data.workspace) workspaceState = data.workspace;
      saveOfflineState();
      renderAllWorkspacePanels();
      const enq = Array.isArray(data.enqueued_ids) && data.enqueued_ids.length > 0
        ? ` + encolado ${data.enqueued_ids.join(', ')}`
        : '';
      showToast(`Lámina Antes/Después + PDF listos${enq}.`);
      if (document.getElementById('smbAuditDialog')?.open) {
        window.openSmbAuditDialog(slug);
      }
    } catch (err) {
      showToast('Error Small Business: ' + err.message);
    }
  };

  function copyPlainText(text, successMsg) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => showToast(successMsg)).catch(() => {
        showToast('Selecciona y copia el texto manualmente.');
      });
    } else {
      showToast('Copia manual requerida en este navegador.');
    }
  }

  window.openSmbAuditByName = async function (businessName) {
    let audits = getGmapsAuditsIndex().audits || [];
    if (audits.length === 0) {
      await window.syncGmapsAuditsFromServer(false);
      audits = getGmapsAuditsIndex().audits || [];
    }
    const targetNorm = String(businessName || '').trim().toLowerCase();
    const match = audits.find((a) => String(a.nombre || '').trim().toLowerCase() === targetNorm)
      || audits.find((a) => String(a.nombre || '').toLowerCase().includes(targetNorm));
    if (match) {
      window.openSmbAuditDialog(match.slug);
      return;
    }
    if (typeof window.switchTab === 'function') window.switchTab('small-business');
    const searchEl = document.getElementById('smbAuditSearchInput');
    if (searchEl) {
      searchEl.value = businessName || '';
      window.renderGmapsAuditsHub();
    }
    showToast(`Filtrando auditoría visual para "${businessName}".`);
  };

  window.openSmbAuditDialog = function (slug) {
    const dialog = document.getElementById('smbAuditDialog');
    const item = findAuditBySlug(slug);
    if (!dialog || !item) {
      showToast('No se encontró la ficha en auditorías de Google Maps.');
      return;
    }

    const titleEl = document.getElementById('smbDialogTitle');
    const subEl = document.getElementById('smbDialogSubtitle');
    const scoreEl = document.getElementById('smbDialogScoreBadge');
    const flagsEl = document.getElementById('smbDialogFlags');
    const obsEl = document.getElementById('smbDialogObsBox');
    const mediaEl = document.getElementById('smbDialogMediaRow');
    const actionsEl = document.getElementById('smbDialogActionsBar');
    const modesEl = document.getElementById('smbDialogModesContainer');

    if (titleEl) titleEl.textContent = item.nombre || item.slug;
    if (subEl) {
      const ratingTxt = item.rating != null ? `⭐ ${item.rating} (${item.resenas || 0} reseñas)` : 'Sin calificación visible';
      subEl.textContent = `${item.categoria || 'Negocio Local'} · ${item.municipio || 'Monterrey'} · ${item.telefono || 'Sin teléfono público'} · ${ratingTxt}`;
    }
    if (scoreEl) scoreEl.textContent = `Oportunidad Score: ${item.audit_score || 0}`;

    const alertFlags = new Set(['CARRITO STREET VIEW', '0 FOTOS', '<=5 FOTOS', 'SIN RECLAMAR', 'RED PERSONAL EN RIESGO']);
    if (flagsEl) {
      const flags = item.audit_flags || [];
      flagsEl.innerHTML = flags.length > 0
        ? flags.map((f) => `<span class="audit-flag-chip ${alertFlags.has(f) ? 'alert' : ''}">${escapeHtml(f)}</span>`).join('')
        : '<span class="audit-flag-chip">Perfil Auditado</span>';
    }

    if (obsEl) {
      const obsList = Array.isArray(item.client_observations) ? item.client_observations : [];
      obsEl.innerHTML = `
        <div style="font-weight:500; color:var(--bone-white); margin-bottom:6px;">Diagnóstico Visual &amp; Comercial (-35% Temporada):</div>
        ${obsList.map((o) => `<div style="color:#c8cdd9; margin-bottom:3px;">• ${escapeHtml(o)}</div>`).join('')}
      `;
    }

    if (mediaEl) {
      const parts = [];
      if (item.screenshot_path) {
        const shotUrl = resolveAssetUrl(item.screenshot_path);
        parts.push(`
          <div class="mode-box-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="font-size:0.76rem; color:var(--bone-white);">Captura Real Google Maps (PNG)</strong>
              <a href="${escapeHtml(shotUrl)}" target="_blank" rel="noopener" class="link-source-action" style="font-size:0.68rem;">Abrir &rarr;</a>
            </div>
            <div class="gmaps-shot-frame">
              <img src="${escapeHtml(shotUrl)}" alt="Captura Google Maps de ${escapeHtml(item.nombre)}" loading="lazy">
            </div>
          </div>
        `);
      }
      if (item.before_after_path) {
        const baUrl = resolveAssetUrl(item.before_after_path);
        parts.push(`
          <div class="mode-box-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="font-size:0.76rem; color:#dcf786;">Lámina Antes vs. Después 2027 (PNG)</strong>
              <a href="${escapeHtml(baUrl)}" target="_blank" rel="noopener" class="link-source-action" style="font-size:0.68rem;">Abrir &rarr;</a>
            </div>
            <div class="gmaps-shot-frame">
              <img src="${escapeHtml(baUrl)}" alt="Antes vs Después ${escapeHtml(item.nombre)}" loading="lazy">
            </div>
          </div>
        `);
      } else {
        parts.push(`
          <div class="mode-box-card" style="justify-content:center; align-items:flex-start;">
            <strong style="font-size:0.8rem; color:var(--champagne-light);">Lámina Antes vs. Después + Dossier PDF (-35%)</strong>
            <p style="font-size:0.74rem; color:#aeb4c4; line-height:1.45;">Aún no generada para este prospecto. Genérala en 1 clic con la foto real de su Google Maps para enviar por WhatsApp o Email.</p>
          </div>
        `);
      }
      mediaEl.innerHTML = parts.join('');
    }

    if (actionsEl) {
      actionsEl.innerHTML = '';
      const genBtn = document.createElement('button');
      genBtn.type = 'button';
      genBtn.className = 'btn-volt-cta';
      genBtn.textContent = 'Generar Antes/Después PNG + PDF + Encolar A+B+C';
      genBtn.onclick = () => window.generateSmallBusinessAudit(item.slug, 'all', 'studio');
      actionsEl.appendChild(genBtn);

      const capBtn = document.createElement('button');
      capBtn.type = 'button';
      capBtn.className = 'week-btn';
      capBtn.textContent = item.screenshot_path ? 'Recapturar Maps (Chrome CDP)' : 'Capturar Maps (Chrome CDP)';
      capBtn.onclick = () => window.captureGmapsBatch(item.slug, 1);
      actionsEl.appendChild(capBtn);

      if (item.dossier_pdf_path) {
        const pdfA = document.createElement('a');
        pdfA.href = resolveAssetUrl(item.dossier_pdf_path);
        pdfA.target = '_blank';
        pdfA.rel = 'noopener';
        pdfA.className = 'attachment-btn';
        pdfA.textContent = 'Abrir Dossier PDF (-35%) →';
        actionsEl.appendChild(pdfA);
      }

      if (item.gmaps_url) {
        const mapsA = document.createElement('a');
        mapsA.href = item.gmaps_url;
        mapsA.target = '_blank';
        mapsA.rel = 'noopener';
        mapsA.className = 'link-source-action';
        mapsA.style.fontSize = '0.72rem';
        mapsA.textContent = 'Ver Ficha Viva Google Maps →';
        actionsEl.appendChild(mapsA);
      }
    }

    if (modesEl) {
      modesEl.innerHTML = '';
      const modes = item.outreach_modes || {};
      const cleanDigits = String(item.telefono || '').replace(/[^0-9]/g, '');
      const configs = [
        { key: 'mode_a_directo', enqueueKey: 'mode_a', title: 'Modo A · Directo Visual + PDF (-35%)' },
        { key: 'mode_b_diagnostico', enqueueKey: 'mode_b', title: 'Modo B · Diagnóstico Corto (2 Pasos)' },
        { key: 'mode_c_hibrido', enqueueKey: 'mode_c', title: 'Modo C · Híbrido Web + -35% + Biogen' }
      ];
      configs.forEach((cfg) => {
        const card = document.createElement('div');
        card.className = 'mode-box-card';

        const head = document.createElement('div');
        head.style.cssText = 'display:flex; justify-content:space-between; align-items:center; gap:6px;';
        head.innerHTML = `<strong style="font-size:0.78rem; color:var(--bone-white);">${escapeHtml(cfg.title)}</strong>`;

        const ta = document.createElement('textarea');
        ta.value = modes[cfg.key] || '';

        const btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex; gap:6px; flex-wrap:wrap; align-items:center;';

        const copyBtn = document.createElement('button');
        copyBtn.type = 'button';
        copyBtn.className = 'week-btn';
        copyBtn.style.cssText = 'padding:4px 9px; font-size:0.68rem;';
        copyBtn.textContent = 'Copiar';
        copyBtn.onclick = () => copyPlainText(ta.value, `${cfg.title} copiado.`);
        btnRow.appendChild(copyBtn);

        const enqBtn = document.createElement('button');
        enqBtn.type = 'button';
        enqBtn.className = 'week-btn';
        enqBtn.style.cssText = 'padding:4px 9px; font-size:0.68rem;';
        enqBtn.textContent = 'Encolar Trigger';
        enqBtn.onclick = () => window.generateSmallBusinessAudit(item.slug, cfg.enqueueKey, 'auto');
        btnRow.appendChild(enqBtn);

        if (cleanDigits) {
          const waBtn = document.createElement('a');
          waBtn.className = 'btn-portal-link';
          waBtn.style.cssText = 'padding:4px 10px; font-size:0.68rem;';
          waBtn.target = '_blank';
          waBtn.rel = 'noopener';
          waBtn.textContent = 'WhatsApp →';
          const refreshHref = () => {
            waBtn.href = `https://wa.me/${cleanDigits}?text=${encodeURIComponent(ta.value)}`;
          };
          refreshHref();
          ta.addEventListener('input', refreshHref);
          waBtn.addEventListener('click', (ev) => {
            const violations = checkClientCopyGuardrail(ta.value);
            if (violations.length > 0) {
              ev.preventDefault();
              showToast('Bloqueado: ' + violations[0]);
            }
          });
          btnRow.appendChild(waBtn);
        }

        card.appendChild(head);
        card.appendChild(ta);
        card.appendChild(btnRow);
        modesEl.appendChild(card);
      });
    }

    if (typeof dialog.showModal === 'function') {
      if (!dialog.open) dialog.showModal();
    } else {
      dialog.setAttribute('open', 'open');
    }
  };

  window.renderGmapsAuditsHub = function () {
    const index = getGmapsAuditsIndex();
    const audits = Array.isArray(index.audits) ? index.audits : [];

    const setEl = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = String(val);
    };

    setEl('gmapsStatTotal', index.total_audited || audits.length || 0);
    setEl('gmapsStatCaptured', index.captured_count || 0);
    setEl('gmapsStatStreetView', index.streetview_count || 0);
    setEl('gmapsStatZeroPhotos', index.zero_photos_count || 0);
    setEl('gmapsStatUnclaimed', index.unclaimed_count || 0);

    const summaryEl = document.getElementById('gmapsAuditSummaryLabel');
    if (summaryEl) {
      summaryEl.textContent = audits.length > 0
        ? `${audits.length} fichas auditadas · ${index.deficient_count || 0} prioritarias con oportunidad (-35%) · ${index.captured_count || 0} capturas reales Chrome CDP.`
        : 'Sin fichas cargadas todavía. Presiona "Refrescar Auditorías" o inicia el servidor :8765.';
    }

    const grid = document.getElementById('gmapsAuditsGrid');
    if (!grid) return;

    const query = ((document.getElementById('smbAuditSearchInput') || {}).value || '').trim().toLowerCase();
    const nicheFilter = (document.getElementById('smbAuditNicheFilter') || {}).value || 'all';
    const flagFilter = (document.getElementById('smbAuditFlagFilter') || {}).value || 'deficient';

    const filtered = audits.filter((a) => {
      const matchesNiche = nicheFilter === 'all' || a.nicho === nicheFilter;
      if (!matchesNiche) return false;

      const flags = Array.isArray(a.audit_flags) ? a.audit_flags : [];
      if (flagFilter === 'deficient' && Number(a.audit_score || 0) < 15) return false;
      if (flagFilter === 'captured' && a.capture_status !== 'captured') return false;
      if (!['deficient', 'all', 'captured'].includes(flagFilter) && !flags.includes(flagFilter)) return false;

      if (!query) return true;
      const hay = `${a.nombre || ''} ${a.categoria || ''} ${a.direccion || ''} ${a.zona || ''} ${a.municipio || ''} ${a.nicho || ''} ${flags.join(' ')}`.toLowerCase();
      return hay.includes(query);
    });

    grid.innerHTML = '';
    if (filtered.length === 0) {
      grid.innerHTML = `<div class="liquid-panel-card" style="grid-column: 1 / -1; color: var(--slate-muted);">No hay fichas con los filtros seleccionados (${audits.length} en catálogo).</div>`;
      return;
    }

    const alertFlags = new Set(['CARRITO STREET VIEW', '0 FOTOS', '<=5 FOTOS', 'SIN RECLAMAR', 'RED PERSONAL EN RIESGO']);
    const visible = filtered.slice(0, 48);

    visible.forEach((a) => {
      const card = document.createElement('div');
      card.className = `gmaps-audit-card ${Number(a.audit_score || 0) >= 35 ? 'priority-high' : ''}`;

      const flags = Array.isArray(a.audit_flags) ? a.audit_flags : [];
      const shotUrl = a.screenshot_path ? resolveAssetUrl(a.screenshot_path) : '';
      const baUrl = a.before_after_path ? resolveAssetUrl(a.before_after_path) : '';
      const ratingTxt = a.rating != null ? `⭐ ${a.rating} (${a.resenas || 0})` : 'Sin rating';

      card.innerHTML = `
        <div>
          <div class="comp-top-strip" style="margin-bottom:8px;">
            <span class="comp-name-title" style="font-size:0.95rem;">${escapeHtml(a.nombre || a.slug)}</span>
            <span class="task-day-badge">Score ${Number(a.audit_score || 0)}</span>
          </div>

          <div class="gmaps-shot-frame" style="margin-bottom:10px;">
            ${shotUrl
              ? `<img src="${escapeHtml(shotUrl)}" alt="Google Maps de ${escapeHtml(a.nombre)}" loading="lazy">`
              : `<div style="padding:18px; text-align:center; font-size:0.74rem; color:#8d93a6;">Sin captura PNG aún · Usa "Capturar PNG" o Chrome CDP</div>`}
          </div>

          <div class="audit-flag-strip" style="margin-bottom:8px;">
            ${flags.map((f) => `<span class="audit-flag-chip ${alertFlags.has(f) ? 'alert' : ''}">${escapeHtml(f)}</span>`).join('')}
            ${baUrl ? '<span class="promo-pill-35">ANTES/DESPUÉS LISTO</span>' : ''}
          </div>

          <div class="comp-meta-row"><strong>Nicho:</strong> ${escapeHtml(a.nicho || '')} · <span style="color:var(--champagne);">${escapeHtml(a.zona || a.municipio || '')}</span></div>
          <div class="comp-meta-row"><strong>Ficha:</strong> ${escapeHtml(ratingTxt)} · Fotos: ${a.images_count != null ? escapeHtml(a.images_count) : '0'} · ${escapeHtml(a.telefono || 'Sin teléfono')}</div>
          <div class="comp-void-box" style="margin-top:8px; font-size:0.73rem;">
            ${(a.client_observations || []).slice(0, 2).map((o) => `• ${escapeHtml(o)}`).join('<br>')}
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; border-top:1px solid var(--glass-border-subtle); padding-top:10px;">
          <button type="button" class="btn-volt-cta" style="padding:6px 11px; font-size:0.71rem;" data-open-smb="${escapeHtml(a.slug)}">
            Ver 3 Modos &amp; Visuales
          </button>
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <button type="button" class="week-btn" style="padding:5px 9px; font-size:0.69rem;" data-gen-smb="${escapeHtml(a.slug)}">
              Antes/Después + PDF
            </button>
            <button type="button" class="week-btn" style="padding:5px 9px; font-size:0.69rem;" data-cap-smb="${escapeHtml(a.slug)}">
              ${shotUrl ? 'Recapturar' : 'Capturar PNG'}
            </button>
          </div>
        </div>
      `;

      const openBtn = card.querySelector('[data-open-smb]');
      if (openBtn) openBtn.addEventListener('click', () => window.openSmbAuditDialog(a.slug));
      const genBtn = card.querySelector('[data-gen-smb]');
      if (genBtn) genBtn.addEventListener('click', () => window.generateSmallBusinessAudit(a.slug, 'all', 'auto'));
      const capBtn = card.querySelector('[data-cap-smb]');
      if (capBtn) capBtn.addEventListener('click', () => window.captureGmapsBatch(a.slug, 1));

      grid.appendChild(card);
    });

    if (filtered.length > visible.length) {
      const note = document.createElement('div');
      note.className = 'liquid-panel-card';
      note.style.cssText = 'grid-column: 1 / -1; text-align:center; font-size:0.76rem; color:var(--champagne-light);';
      note.textContent = `Mostrando los ${visible.length} prospectos de mayor oportunidad visual de ${filtered.length} resultados. Usa el buscador para filtrar el resto.`;
      grid.appendChild(note);
    }
  };

  // =========================================================================
  // 8. MODULAR -35% MATRIX ("¿CUÁL PREFIERES?") & BIOGEN BETA CALCULATOR
  // =========================================================================
  window.renderModularAndBiogenCalculators = function () {
    const acc = workspaceState.accounting || DEFAULT_WORKSPACE.accounting;
    const matrix = acc.modular_options_matrix || DEFAULT_WORKSPACE.accounting.modular_options_matrix;
    const biogen = acc.biogen_pilot_catalog || DEFAULT_WORKSPACE.accounting.biogen_pilot_catalog;

    // Part A: Modular 3-Option Matrix (-35% + deferred LED split)
    const modContainer = document.getElementById('modularTiersGridContainer');
    if (modContainer && matrix && Array.isArray(matrix.tiers)) {
      const niche = (document.getElementById('modularNicheSelect') || {}).value || 'padel_gym';
      const discountEl = document.getElementById('modularDiscountToggle');
      const splitEl = document.getElementById('modularSplitToggle');
      const discountOn = discountEl ? discountEl.checked : true;
      const splitOn = splitEl ? splitEl.checked : true;
      const factor = discountOn ? 0.65 : 1.0;

      modContainer.innerHTML = '';
      matrix.tiers.forEach((tier) => {
        const listPrice = Number((tier.prices_by_niche || {})[niche] || 4900);
        const finalPrice = Math.round(listPrice * factor);
        const directCost = Number(tier.direct_cost_mxn || 350);
        const netProfit = Math.round(finalPrice - directCost);
        const marginPct = finalPrice > 0 ? ((netProfit / finalPrice) * 100).toFixed(1) : '0.0';

        const splitCfg = tier.deferred_split || {};
        const splitEnabled = Boolean(splitOn && splitCfg.enabled);
        const phase1Total = splitEnabled
          ? Math.round(Number(splitCfg.phase_1_digital_mxn || listPrice) * factor)
          : finalPrice;
        const phase2Total = splitEnabled ? Math.max(0, finalPrice - phase1Total) : 0;
        const advance50 = Math.round(phase1Total * 0.5);

        const card = document.createElement('div');
        card.className = `modular-tier-card ${tier.id === 'OPT-FULL-LED' ? 'featured' : ''}`;
        card.innerHTML = `
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin-bottom:8px;">
              <span class="task-day-badge">OPCIÓN ${tier.option_num} · ${escapeHtml(tier.id)}</span>
              ${discountOn ? '<span class="promo-pill-35">-35% TEMPORADA</span>' : '<span class="source-type-badge">LISTA</span>'}
            </div>
            <div style="font-size:0.95rem; font-weight:500; color:var(--bone-white); margin-bottom:8px;">${escapeHtml(tier.title)}</div>
            <div class="price-strike-row" style="margin-bottom:8px;">
              ${discountOn ? `<span class="price-list-struck">$${listPrice.toLocaleString()}</span>` : ''}
              <span class="price-promo-now">$${finalPrice.toLocaleString()} MXN</span>
            </div>
            <div style="font-size:0.74rem; color:#b8bdcc; line-height:1.45; margin-bottom:8px;">
              <div><strong>Digital:</strong> ${escapeHtml(tier.digital_sla || '')}</div>
              <div><strong>Físico:</strong> ${escapeHtml(tier.physical_sla || '')}</div>
            </div>
            <div class="simulator-output-box" style="margin:0; font-size:0.72rem;">
              <div class="sim-row"><span class="sim-label">${splitEnabled ? '1er Momento (Digital)' : 'Cobro Digital Total'}</span><span class="sim-val">$${phase1Total.toLocaleString()} MXN</span></div>
              ${splitEnabled ? `<div class="sim-row"><span class="sim-label">2do Momento (LED/Marcos)</span><span class="sim-val">$${phase2Total.toLocaleString()} MXN</span></div>` : ''}
              <div class="sim-row"><span class="sim-label">Anticipo 50% Reserva</span><span class="sim-val">$${advance50.toLocaleString()} MXN</span></div>
              <div class="sim-row"><span class="sim-label">Margen Neto Estimado</span><span class="sim-val profit">$${netProfit.toLocaleString()} (${marginPct}%)</span></div>
            </div>
          </div>
          <div style="display:flex; justify-content:flex-end; margin-top:6px;">
            <button type="button" class="week-btn" style="padding:5px 11px; font-size:0.7rem;" data-copy-tier="${escapeHtml(tier.id)}">
              Copiar Cotización Opción ${tier.option_num}
            </button>
          </div>
        `;

        const copyBtn = card.querySelector('[data-copy-tier]');
        if (copyBtn) {
          copyBtn.addEventListener('click', () => {
            const pitch = `Opción ${tier.option_num} (${tier.title}): $${finalPrice.toLocaleString()} MXN`
              + (discountOn ? ` (con -35% Descuento de Temporada sobre $${listPrice.toLocaleString()})` : '')
              + (splitEnabled
                ? ` — pago flexible en 2 momentos: $${phase1Total.toLocaleString()} MXN cobertura digital (50% anticipo $${advance50.toLocaleString()}) + $${phase2Total.toLocaleString()} MXN en 2do momento al producir piezas físicas en taller MTY/SPGG (3–5 días hábiles).`
                : ` — reserva con 50% de anticipo ($${advance50.toLocaleString()} MXN) y 50% contra entrega digital el mismo día.`);
            copyPlainText(pitch, `Cotización de Opción ${tier.option_num} (-35%) copiada.`);
          });
        }
        modContainer.appendChild(card);
      });
    }

    // Part B: Captoora Biogen (Beta) Calculator
    const bioBox = document.getElementById('biogenOutputBox');
    if (bioBox && biogen && Array.isArray(biogen.durations)) {
      const cadence = (document.getElementById('biogenCadenceSelect') || {}).value || 'mensual';
      const durId = (document.getElementById('biogenDurationSelect') || {}).value || 'BIOGEN-3M';
      const bioDiscEl = document.getElementById('biogenDiscountToggle');
      const bioDiscOn = bioDiscEl ? bioDiscEl.checked : true;

      const plan = biogen.durations.find((d) => d.id === durId) || biogen.durations[0];
      const listMonthly = Number(plan.beta_monthly_mxn || 1950);
      const finalMonthly = bioDiscOn ? Math.round(listMonthly * 0.65) : listMonthly;
      const months = Number(plan.months || 3);
      const totalContract = finalMonthly * months;
      const estCost = 180 * months;
      const net = totalContract - estCost;
      const marginPct = totalContract > 0 ? ((net / totalContract) * 100).toFixed(1) : '0.0';

      const cadenceMeta = {
        semanal: { label: 'Semanal (4 sesiones / mes)', perMonth: 4 },
        quincenal: { label: 'Quincenal (2 sesiones / mes)', perMonth: 2 },
        mensual: { label: 'Mensual (1 sesión / mes)', perMonth: 1 },
        bimestral: { label: 'Bimestral (1 sesión cada 2 meses)', perMonth: 0.5 }
      }[cadence] || { label: 'Mensual', perMonth: 1 };

      const totalSessions = Math.max(1, Math.round(months * cadenceMeta.perMonth));

      bioBox.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:10px; flex-wrap:wrap;">
          <strong style="color:var(--bone-white); font-size:0.9rem;">${escapeHtml(plan.label)} · ${escapeHtml(cadenceMeta.label)}</strong>
          ${bioDiscOn ? '<span class="promo-pill-35">-35% PILOTO BETA</span>' : '<span class="source-type-badge">TARIFA BETA</span>'}
        </div>
        <div class="sim-row">
          <span class="sim-label">Mensualidad por Miembro / Atleta</span>
          <span class="sim-val">${bioDiscOn ? `<s style="color:#7f8596; font-size:0.72rem;">$${listMonthly.toLocaleString()}</s> ` : ''}<strong style="color:#dcf786;">$${finalMonthly.toLocaleString()} MXN/mes</strong></span>
        </div>
        <div class="sim-row">
          <span class="sim-label">Sesiones en Estudio Incluidas (${months}m)</span>
          <span class="sim-val">${totalSessions} comparativas esculturales idénticas</span>
        </div>
        <div class="sim-row">
          <span class="sim-label">Valor Total Contrato (${months} meses)</span>
          <span class="sim-val">$${totalContract.toLocaleString()} MXN</span>
        </div>
        <div class="sim-row">
          <span class="sim-label">Margen Neto Estimado Captoora</span>
          <span class="sim-val profit">$${net.toLocaleString()} MXN (${marginPct}%)</span>
        </div>
        <div style="margin-top:10px; padding-top:8px; border-top:1px solid var(--glass-border-subtle); display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap;">
          <span style="font-size:0.7rem; color:#9ea3b5;">0% mención IA · Registro visual fotográfico en estudio (ángulo e iluminación replicables).</span>
          <button type="button" class="week-btn" style="padding:5px 11px; font-size:0.7rem;" id="btnCopyBiogenPitch">Copiar Pitch Biogen Beta</button>
        </div>
      `;

      const bioCopyBtn = document.getElementById('btnCopyBiogenPitch');
      if (bioCopyBtn) {
        bioCopyBtn.onclick = () => {
          const msg = `Captoora Biogen (Beta · ${plan.label}): registro fotográfico escultural en estudio con luz y encuadre repetible en frecuencia ${cadence} (${totalSessions} sesiones comparativas). Con -35% Descuento de Temporada: $${finalMonthly.toLocaleString()} MXN/mes (antes $${listMonthly.toLocaleString()} MXN/mes). Entrega digital comparativa el mismo día de cada sesión.`;
          copyPlainText(msg, 'Pitch Captoora Biogen Beta (-35%) copiado.');
        };
      }
    }
  };

  // =========================================================================
  // 10. MARKETING HQ · MARKY, LUPE & CONAN (0% GROKBOT · DUAL GOOGLE PRO)
  // =========================================================================
  async function fetchStaticMarketingFallback() {
    try {
      const res = await fetch('./data/marketing_studio.json', { cache: 'no-store' });
      if (res.ok) {
        workspaceState.marketing_studio = await res.json();
        saveOfflineState();
        window.renderMarketingStudioHub();
      }
    } catch (_err) {
      // ignore if browser blocks file:// fetch
    }
  }

  function renderHierarchyBar(mk) {
    const bar = document.getElementById('mkhqHierarchyBar');
    if (!bar) return;
    const reports = (mk.team_hierarchy && mk.team_hierarchy.reports) || [];
    const director = (mk.team_hierarchy && mk.team_hierarchy.director) || {
      agent_id: 'marky_marketing',
      name: 'Marky',
      title: 'Director de Marketing & Estrategia'
    };
    const cards = [
      {
        agent_id: director.agent_id,
        role: 'BOT 08 · DIRECTOR DE MARKETING',
        name: `${director.name} — ${director.title}`,
        detail: 'Supervisa a Lupe y Conan, reparte cuota entre Poncho ($395) y Yari ($99), y mantiene Plan Sin Cuotas.'
      },
      ...reports.map((r, idx) => ({
        agent_id: r.agent_id,
        role: idx === 0 ? 'BOT 09 · REPORTA A MARKY' : 'BOT 10 · REPORTA A MARKY -> LUPE',
        name: `${r.name} — ${r.title}`,
        detail: r.agent_id === 'lupe_social'
          ? 'Meta Business Suite (FB+IG+WA), TikTok, LinkedIn, Captions 0% IA y Playbook DM.'
          : 'Exprime OpusClip Pro, Captions, Canva, Aftershoot, Evoto, CapCut y motor local $0.'
      }))
    ];
    bar.innerHTML = cards.map((c, idx) => `
      <div class="mkhq-card ${idx === 0 ? 'highlight' : ''}">
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
          <span class="task-day-badge">${escapeHtml(c.role)}</span>
          <button type="button" class="week-btn" style="padding:3px 9px; font-size:0.68rem;" onclick="runSelectedOrChiefMission('${escapeHtml(c.agent_id)}')">Correr (0 Tokens)</button>
        </div>
        <strong style="color:var(--bone-white); font-size:0.86rem;">${escapeHtml(c.name)}</strong>
        <p style="font-size:0.74rem; color:#aeb4c4; margin:0; line-height:1.45;">${escapeHtml(c.detail)}</p>
      </div>
    `).join('');
  }

  function renderOpusClipSection(mk) {
    const box = document.getElementById('mkhqOpusClipSection');
    if (!box) return;
    const opus = mk.opusclip_rescue_sprint;
    if (!opus) {
      box.innerHTML = '<div style="font-size:0.78rem; color:#cfd3df;">Cargando plan de rescate OpusClip Pro...</div>';
      return;
    }
    const pillars = (opus.pillars_to_record || []).map((p) => `
      <div class="mkhq-card">
        <div style="display:flex; justify-content:space-between; gap:8px; align-items:center;">
          <span class="audit-flag-chip alert">${escapeHtml(p.id)}</span>
          <span style="font-family:var(--font-mono); font-size:0.65rem; color:#dcf786;">${escapeHtml(p.estimated_clips)}</span>
        </div>
        <strong style="color:var(--bone-white); font-size:0.82rem;">${escapeHtml(p.title)}</strong>
        <div style="font-size:0.71rem; color:var(--champagne);"><strong>Stack:</strong> ${escapeHtml(p.tool)}</div>
        <ul style="margin:0 0 0 16px; padding:0; font-size:0.72rem; color:#cfd3df; line-height:1.45;">
          ${(p.script_bullets || []).map((b) => `<li>${escapeHtml(b)}</li>`).join('')}
        </ul>
      </div>
    `).join('');

    box.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
        <div>
          <span class="audit-flag-chip alert">${escapeHtml(opus.status)}</span>
          <h3 style="font-family:var(--font-display); color:var(--bone-white); font-size:1.08rem; margin:6px 0 4px;">
            Operación Rescate Conan: Exprimir OpusClip Pro Antes de Fin de Prueba
          </h3>
          <p style="font-size:0.76rem; color:#e7c9c6; margin:0;">${escapeHtml(opus.goal)}</p>
        </div>
        <button type="button" class="btn-approve-trigger" onclick="submitOpusClipRescueNow()">
          Crear Briefs OpusClip Pro para Conan
        </button>
      </div>
      <div class="mkhq-grid" style="margin-bottom:12px;">${pillars}</div>
      <div style="font-size:0.72rem; color:#d7dbe7; background:rgba(0,0,0,0.34); padding:10px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.08);">
        <strong>Checklist OpusClip Pro:</strong> ${(opus.settings_checklist || []).map((s) => escapeHtml(s)).join(' · ')}
      </div>
    `;
  }

  function renderGoogleProAndMuseCards(mk) {
    const proCard = document.getElementById('mkhqGoogleProSyncCard');
    const museCard = document.getElementById('mkhqMuseBridgeCard');
    const sync = mk.google_pro_sync;
    const muse = mk.muse_mobile_sync || {};

    if (proCard && sync) {
      proCard.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:8px;">
          <div class="panel-inner-title">${escapeHtml(sync.title)}</div>
          <span class="promo-pill-35">DOBLE CUOTA ACTIVA</span>
        </div>
        <div class="panel-inner-sub">${escapeHtml(sync.summary)}</div>
        <div style="display:flex; flex-direction:column; gap:10px;">
          ${(sync.lanes || []).map((ln) => `
            <div class="mkhq-card">
              <strong style="color:var(--champagne-light); font-size:0.8rem;">${escapeHtml(ln.lane)}</strong>
              <div style="font-size:0.73rem; color:var(--bone-white);">${escapeHtml(ln.focus)}</div>
              <div style="font-size:0.71rem; color:#9ea3b5;">${(ln.assigned_apps || []).map((a) => escapeHtml(a)).join(' · ')}</div>
              <div style="font-size:0.7rem; color:#dcf786;">↳ ${escapeHtml(ln.handoff_rule)}</div>
            </div>
          `).join('')}
        </div>
      `;
    }

    if (museCard) {
      const notesLog = (muse.notes_log || []).slice(0, 3);
      museCard.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:8px;">
          <div class="panel-inner-title">Puente Meta Muse Móvil ↔ Antigravity Mac</div>
          <span class="source-type-badge">SINCRONÍA CALLE</span>
        </div>
        <div class="panel-inner-sub">Cuando salgas del estudio sin notificaciones de Chrome, copia este Context Pack para tu Meta Muse móvil y pega de vuelta tus notas al volver.</div>
        <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:10px;">
          <button type="button" class="btn-volt-cta" style="padding:7px 14px; font-size:0.74rem;" onclick="copyMuseContextBrief()">
            Copiar Brief de Bolsillo p/ Muse
          </button>
          <button type="button" class="week-btn" onclick="openMuseViaWhatsApp()">
            Enviármelo a WA (+52 81 3051 6527) &rarr;
          </button>
        </div>
        <label for="museNotesInput" style="font-family:var(--font-mono); font-size:0.65rem; color:var(--champagne); display:block; margin-bottom:6px;">
          PEGAR NOTAS QUE CAPTURASTE CON MUSE EN LA CALLE (&rarr; ASANA + LUPE/CONAN)
        </label>
        <textarea id="museNotesInput" class="mkhq-textarea" placeholder="Ej. Visité Clínica Vista Hermosa, urge foto fachada -35%. También grabar clip corto mañana en cancha."></textarea>
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-top:8px; flex-wrap:wrap;">
          <select id="museTargetAgentSelect" class="glass-select-input" style="font-size:0.72rem;">
            <option value="marky_marketing">Enviar a Marky (Estrategia)</option>
            <option value="lupe_social">Enviar a Lupe (Redes/DMs)</option>
            <option value="conan_content">Enviar a Conan (Contenido)</option>
          </select>
          <button type="button" class="btn-approve-trigger" onclick="ingestMuseNotesNow()">
            Convertir en Tarea Asana &rarr;
          </button>
        </div>
        ${notesLog.length ? `<div style="margin-top:10px; font-size:0.7rem; color:#abb0c0;"><strong>Últimas notas:</strong> ${notesLog.map((n) => `[${escapeHtml(n.task_id)}] ${escapeHtml(n.notes.slice(0, 65))}`).join(' · ')}</div>` : ''}
      `;
    }
  }

  window.renderMarketingStudioHub = function () {
    const mk = workspaceState.marketing_studio;
    if (!mk) return;

    const grokBadge = document.getElementById('mkhqGrokbotBadge');
    if (grokBadge && mk.grokbot_status) {
      grokBadge.textContent = mk.grokbot_status;
    }

    renderHierarchyBar(mk);
    renderOpusClipSection(mk);
    renderGoogleProAndMuseCards(mk);

    const subsGrid = document.getElementById('mkhqSubscriptionsGrid');
    const subsBadge = document.getElementById('mkhqSubsCountBadge');
    const subs = mk.subscriptions_stack || [];
    if (subsBadge) subsBadge.textContent = `${subs.length} Herramientas Activas`;
    if (subsGrid) {
      subsGrid.innerHTML = subs.map((s) => `
        <div class="mkhq-card ${s.urgency === 'CRÍTICA' ? 'highlight' : ''}">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap;">
            <strong style="color:var(--bone-white); font-size:0.82rem;">${escapeHtml(s.name)}</strong>
            <span class="${s.urgency === 'CRÍTICA' ? 'audit-flag-chip alert' : 'source-type-badge'}">${escapeHtml(s.cost_label)}</span>
          </div>
          <div style="font-size:0.73rem; color:#cbd0df;">${escapeHtml(s.role)}</div>
          <div style="font-size:0.7rem; color:var(--champagne);"><strong>Flujo:</strong> ${escapeHtml(s.daily_workflow)}</div>
          <div style="font-size:0.67rem; color:#8d92a3;">Responsable: ${escapeHtml(s.owner_agent)} · Cuenta: ${escapeHtml(s.account)}</div>
        </div>
      `).join('');
    }

    const calGrid = document.getElementById('mkhqCalendarGrid');
    const platFilter = (document.getElementById('mkhqPlatformFilter') && document.getElementById('mkhqPlatformFilter').value) || 'all';
    const posts = (mk.content_calendar || []).filter((p) => (
      platFilter === 'all' || String(p.platform || '').toLowerCase().includes(platFilter.toLowerCase())
    ));
    if (calGrid) {
      calGrid.innerHTML = posts.map((p) => `
        <div class="mkhq-card">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap;">
            <span class="task-day-badge">${escapeHtml(p.day)} · ${escapeHtml(p.platform)}</span>
            <span class="source-type-badge">${p.status === 'queued_for_trigger' ? 'EN COLA TRIGGER' : 'LISTO P/ LUPE'}</span>
          </div>
          <strong style="color:var(--bone-white); font-size:0.83rem;">${escapeHtml(p.title)}</strong>
          <div style="font-size:0.71rem; color:var(--champagne);">Conan (${escapeHtml(p.conan_tool)}): ${escapeHtml(p.conan_deliverable)}</div>
          <textarea class="mkhq-textarea" style="min-height:92px;" id="lupeCaption_${escapeHtml(p.id)}">${escapeHtml(p.caption + '\n\n' + (p.hashtags || ''))}</textarea>
          <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
            <button type="button" class="week-btn" style="padding:5px 10px; font-size:0.7rem;" onclick="copyLupeCaptionNow('${escapeHtml(p.id)}')">Copiar Caption</button>
            <button type="button" class="btn-approve-trigger" style="padding:5px 10px; font-size:0.7rem;" onclick="enqueueLupePostNow('${escapeHtml(p.id)}')">Enviar a Último Trigger</button>
          </div>
        </div>
      `).join('');
    }

    const briefsEl = document.getElementById('conanBriefsList');
    if (briefsEl) {
      briefsEl.innerHTML = (mk.conan_briefs || []).slice(0, 6).map((b) => `
        <div class="supplier-chip">
          <div class="supplier-name-box">
            <strong>[${escapeHtml(b.id)}] ${escapeHtml(b.title)}</strong>
            <span>${escapeHtml(b.tool_stack)} · Formato: ${escapeHtml(b.output_format)} -> Para ${escapeHtml(b.for_agent)}</span>
          </div>
          <span class="supplier-tag">${escapeHtml(b.status)}</span>
        </div>
      `).join('');
    }

    const dmEl = document.getElementById('lupeDmPlaybookList');
    if (dmEl) {
      dmEl.innerHTML = (mk.lupe_dm_playbook || []).map((d) => `
        <div class="mkhq-card">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap;">
            <strong style="color:var(--champagne-light); font-size:0.78rem;">${escapeHtml(d.trigger_label)}</strong>
            <span class="source-type-badge">${escapeHtml(d.channel)}</span>
          </div>
          <div style="font-size:0.73rem; color:#d2d5de; white-space:pre-line;">${escapeHtml(d.reply_text)}</div>
          <div>
            <button type="button" class="week-btn" style="padding:4px 10px; font-size:0.7rem;" onclick="copyLupeDmNow('${escapeHtml(d.id)}')">Copiar Respuesta Lupe</button>
          </div>
        </div>
      `).join('');
    }
  };

  window.regenerateMarketingPlanNow = async function () {
    if (!serverOnline) {
      showToast('Inicia el servidor :8765 para sincronizar el plan.');
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/api/marketing-studio/generate-plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ focus: 'all', week_label: 'Semana Sprint Nov 2026 (-35% · OpusClip + 2x Google Pro)' })
      });
      const data = await res.json();
      if (data.workspace) workspaceState = data.workspace;
      saveOfflineState();
      renderAllWorkspacePanels();
      showToast('Marky sincronizó el plan semanal y Brief Muse (0 tokens).');
    } catch (e) {
      showToast('Error al regenerar plan: ' + e.message);
    }
  };

  window.copyLupeCaptionNow = function (postId) {
    const ta = document.getElementById(`lupeCaption_${postId}`);
    if (ta) copyPlainText(ta.value, `Caption ${postId} de Lupe copiado (0% IA).`);
  };

  window.copyLupeDmNow = function (dmId) {
    const mk = workspaceState.marketing_studio || {};
    const dm = (mk.lupe_dm_playbook || []).find((x) => x.id === dmId);
    if (dm) copyPlainText(dm.reply_text, `Respuesta ${dmId} de Lupe copiada.`);
  };

  window.enqueueLupePostNow = async function (postId) {
    const ta = document.getElementById(`lupeCaption_${postId}`);
    const customCaption = ta ? ta.value : null;
    if (customCaption) {
      const violations = checkClientCopyGuardrail(customCaption);
      if (violations.length) {
        showToast(violations[0]);
        return;
      }
    }
    if (!serverOnline) {
      showToast('Inicia :8765 para enviar directo a Último Trigger.');
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/api/marketing-studio/enqueue-post`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ post_id: postId, custom_caption: customCaption })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
      if (data.workspace) workspaceState = data.workspace;
      saveOfflineState();
      renderAllWorkspacePanels();
      showToast(`Lupe encoló ${data.enqueued_item.id} en Tu Último Trigger.`);
    } catch (e) {
      showToast('Error: ' + e.message);
    }
  };

  window.submitConanBriefNow = async function () {
    const titleEl = document.getElementById('conanBriefTitleInput');
    const toolEl = document.getElementById('conanBriefToolSelect');
    const fmtEl = document.getElementById('conanBriefFormatSelect');
    const title = (titleEl && titleEl.value || '').trim();
    if (title.length < 4) {
      showToast('Escribe al menos 4 caracteres para el brief de Conan.');
      return;
    }
    if (!serverOnline) {
      showToast('Inicia :8765 para asignar brief a Conan.');
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/api/marketing-studio/conan-brief`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          tool_stack: (toolEl && toolEl.value) || 'OpusClip Pro + CapCut',
          output_format: (fmtEl && fmtEl.value) || 'Reel 9:16',
          target_channel: 'IG Reels + TikTok + LinkedIn (Lupe)'
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
      if (titleEl) titleEl.value = '';
      if (data.workspace) workspaceState = data.workspace;
      saveOfflineState();
      renderAllWorkspacePanels();
      showToast(`Brief ${data.brief.id} y tarea ${data.task.id} asignados a Conan.`);
    } catch (e) {
      showToast('Error: ' + e.message);
    }
  };

  window.submitOpusClipRescueNow = async function () {
    if (!serverOnline) {
      showToast('Inicia :8765 para crear briefs OpusClip Pro.');
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/api/marketing-studio/conan-brief`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: 'Rescate URGENTE OpusClip Pro: 3 grabaciones (Maps OBS + Navidad LED + Biogen) -> 30 clips 9:16',
          tool_stack: 'OBS + Captions + OpusClip Pro + CapCut',
          output_format: '25–30 Reels / TikTok 9:16',
          target_channel: 'Lupe (Meta Suite + TikTok + LinkedIn)'
        })
      });
      const data = await res.json();
      if (data.workspace) workspaceState = data.workspace;
      saveOfflineState();
      renderAllWorkspacePanels();
      showToast('Sprint de Rescate OpusClip Pro enviado a Conan & Asana.');
    } catch (e) {
      showToast('Error: ' + e.message);
    }
  };

  window.copyMuseContextBrief = function () {
    const mk = workspaceState.marketing_studio || {};
    const pack = (mk.muse_mobile_sync && mk.muse_mobile_sync.context_pack) || 'Captoora Studio -35% activo.';
    copyPlainText(pack, 'Brief de Bolsillo copiado para pegar en tu Meta Muse móvil.');
  };

  window.openMuseViaWhatsApp = function () {
    const mk = workspaceState.marketing_studio || {};
    const pack = (mk.muse_mobile_sync && mk.muse_mobile_sync.context_pack) || 'Captoora Studio -35% activo.';
    window.open(`https://wa.me/528130516527?text=${encodeURIComponent(pack)}`, '_blank', 'noopener');
  };

  window.ingestMuseNotesNow = async function () {
    const ta = document.getElementById('museNotesInput');
    const agSel = document.getElementById('museTargetAgentSelect');
    const text = (ta && ta.value || '').trim();
    if (text.length < 4) {
      showToast('Pega al menos 4 caracteres de tus notas de Muse móvil.');
      return;
    }
    if (!serverOnline) {
      showToast('Inicia :8765 para importar notas a Asana.');
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/api/marketing-studio/muse-ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          notes_text: text,
          target_agent: (agSel && agSel.value) || 'marky_marketing'
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
      if (ta) ta.value = '';
      if (data.workspace) workspaceState = data.workspace;
      saveOfflineState();
      renderAllWorkspacePanels();
      showToast(`Nota móvil convertida en ${data.task.id} (${data.task.assigned_agent}).`);
    } catch (e) {
      showToast('Error: ' + e.message);
    }
  };

  function renderAllWorkspacePanels() {
    ensureSpritesInitialized();
    renderTokenUsageTelemetry();
    renderGameInspectorHud();
    renderCompanyMode();
    renderApprovalQueue();
    window.renderAsanaBoard();
    renderAccountingAndSubscriptions();
    window.renderSprintMartesHub();
    window.renderGmapsAuditsHub();
    window.renderModularAndBiogenCalculators();
    window.renderMarketingStudioHub();
  }

  window.syncWorkspaceFromServer = syncWorkspaceFromServer;
  window.captooraShowToast = showToast;

  window.initStudioWorkspace = function () {
    const urlParams = new URLSearchParams(window.location.search);
    const hash = String(window.location.hash || '').replace(/^#/, '');
    const targetTab = urlParams.get('tab') || (hash === 'triggers' ? 'proyectos-asana' : hash) || 'sprint-martes';
    if (targetTab && typeof window.switchTab === 'function' && document.getElementById(`tab-${targetTab}`)) {
      window.switchTab(targetTab);
    }

    renderAllWorkspacePanels();
    setupGameCanvasInteractions();
    startSprintCountdown();
    if (pomoState.running) startPomodoroTicker();
    syncWorkspaceFromServer(true).then((ok) => {
      if (!ok || !(getGmapsAuditsIndex().audits || []).length) {
        fetchStaticGmapsFallback();
      }
      if (!ok || !workspaceState.marketing_studio) {
        fetchStaticMarketingFallback();
      }
    });

    if (!pollInterval) {
      pollInterval = setInterval(() => {
        if (window.location.protocol.startsWith('http') || serverOnline) {
          syncWorkspaceFromServer(true);
        }
      }, 4000);
    }
  };
})();


