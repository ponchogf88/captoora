/* =========================================================
   CAPTOORA — DATOS EDITABLES (un solo lugar)
   Cambia aquí el evento, precios y contacto. Nada más.
   ========================================================= */
window.CAPTOORA = {
  whatsapp: "528140050088",          // sin + ni espacios
  whatsappLabel: "81 4005 0088",

  // ---- ESTUDIO ABIERTO / AGENDA ------------------------------
  // Si hay un evento con fecha, cambia estos textos aquí.
  event: {
    show: true,
    kicker: "El estudio está abierto",
    title: "Agenda tu sesión.",
    whatToDo: "Escríbeme por WhatsApp: qué quieres (sesión fotográfica o renta del estudio), qué día y cuántas personas. Te confirmo y te mando la ubicación.",
    when: "Tú eliges el día. Lo cuadramos por WhatsApp.",
    how: "30% de anticipo por transferencia. El resto, al terminar.",
    address: "Av. Paseo de los Álamos 165, Colinas de San Jerónimo, Monterrey, N.L., CP 64630",
    mapsUrl: "https://www.google.com/maps/search/?api=1&query=Av.+Paseo+de+los+%C3%81lamos+165,+Colinas+de+San+Jer%C3%B3nimo,+Monterrey,+N.L.+64630",
    // Mapa embebido (satélite, sin API key). t=k satélite, z=zoom.
    mapEmbed: "https://maps.google.com/maps?q=Av.+Paseo+de+los+%C3%81lamos+165,+Colinas+de+San+Jer%C3%B3nimo,+Monterrey,+N.L.+64630&t=k&z=18&output=embed",
    ctaText: "Agenda por WhatsApp",
    waMessage: "Hola Captoora, quiero agendar una sesión. Me interesa: (sesión fotográfica / renta del estudio). Día: . Personas: ."
  },

  // ---- HORARIO (cámbialo cuando haya horario fijo) ----------------
  hours: "Con cita, escríbenos para horarios.",

  // ---- PARQUE (punto de venta para papás) ------------------------
  park: {
    title: "Parque justo afuera: exterior con luz natural + estudio.",
    text: "Al salir del estudio hay un parque. En una misma visita tus peques juegan afuera con luz natural y luego pasamos al set con luz profesional. Dos looks, cero traslados."
  },

  // ---- PAQUETES (offers.md, 23 sep 2026) -----------------------
  deposit: "Apartas con 30% de anticipo por transferencia. El resto, al terminar.",
  // Orden = orden en la página. featured = destacado lima; secondary = destacado suave.
  // Para promos: price = precio de promo, regularPrice = precio tachado, promoLabel = texto.
  // Cuando acabe la promo, borra regularPrice y promoLabel y pon el precio normal en price.
  packages: [
    { name: "Clónate con inteligencia artificial", price: null, priceLabel: "Cotización personalizada",
      badge: "CAPTOORA Biometrics", secondary: true,
      desc: "Sesiones piloto de clon digital. Tu presencia frente a cámara, preparada en estudio. Te guiamos para grabar el material de tu clon digital con iluminación profesional, encuadre cuidado y voz clara.",
      items: ["Preparación de imagen y guía frente a cámara", "Set e iluminación profesional para video", "Grabación de tomas de referencia y revisión técnica", "Asistencia para configurar y probar tu avatar con tu autorización", "Plataforma, videos y costos de uso definidos en tu cotización"],
      cta: "Quiero mi clon digital",
      waMessage: "Hola Captoora, quiero información de la sesión para crear mi clon digital con inteligencia artificial." },
    { name: "Combo Studio + Clips", price: 1600, unit: "2 horas", featured: true,
      badge: "El que recomiendo",
      items: ["Sesión en set", "8 a 12 clips listos para Reels/TikTok"] },
    { name: "Clase de cámara", price: 350, regularPrice: 500, unit: "por hora",
      promoLabel: "Promoción de octubre", validUntil: "Válido hasta el 31 de octubre", secondary: true, badge: "Promo octubre",
      kicker: "Para dominar la luz, primero tienes que aprender a controlar la oscuridad.",
      desc: "Para dominar la luz, primero tienes que aprender a controlar la oscuridad. Una hora de clase práctica en el estudio con tu propia cámara: aprende a dominar el modo manual, el control de sombras, la velocidad de obturación y la dirección de luz directamente en el set.",
      items: ["Con tu propia cámara (Nikon, Canon, Sony)", "Para dominar la luz, primero aprendes a controlar la oscuridad", "Práctica real en set, cero teoría aburrida", "Sales dominando el modo manual"],
      cta: "Agendar mi clase de cámara",
      waMessage: "Hola Captoora, quiero agendar mi Clase de Cámara (Para dominar la luz, primero tienes que aprender a controlar la oscuridad)." },
    { name: "Renta de estudio", price: 350, regularPrice: 500, unit: "por hora",
      promoLabel: "Promoción de octubre", validUntil: "Válido hasta el 31 de octubre", secondary: true, badge: "Promo octubre",
      desc: "Renta un espacio amplio con tres escenarios diferentes para tu sesión. Atención personalizada en Colinas de San Jerónimo, Monterrey, con opción a exterior.",
      items: ["Tres escenarios diferentes", "Softbox, cicloramas, fondos y luces profesionales", "Baño, espejos y pantallas", "Internet y climatización", "Sonido envolvente", "Atención personalizada y opción a exterior", "Apartas por WhatsApp"],
      cta: "Rentar una hora",
      waMessage: "Hola, quiero rentar el estudio por una hora." },
    // Sesión infantil / familiar: precio y promo vecinos SIN confirmar.
    // Cuando estén: pon price: 1000 (número) y llena neighborPromo; borra priceLabel.
    { name: "Sesión infantil / familiar", price: null, priceLabel: "Precio y promo vecinos: pregunta por WhatsApp",
      neighborPromo: "", badge: "Set de otoño", secondary: true,
      desc: "Set de temporada para peques y familia: Pumpkin Patch, Halloween y Día de Muertos. Parque justo afuera para fotos con luz natural + estudio.",
      items: ["Set de otoño: Pumpkin Patch, Halloween, Día de Muertos", "Exterior en el parque + interior en el estudio", "Te dirijo: los peques juegan, yo capturo", "Promo para vecinos y familias de kínders cercanos"],
      cta: "Preguntar por la sesión infantil",
      waMessage: "Hola Captoora, quiero info de la sesión infantil / familiar de otoño (precio y promo vecinos)." },
    { name: "Sesión básica", price: 1000, unit: "1 hora",
      items: ["1 set con luces", "Te dirijo la pose", "15 fotos editadas"] },
    { name: "Video por encargo", price: 1200, unit: "por video",
      items: ["Hasta 60–90 s", "Mandas brief, guion y referencias", "Te entrego el archivo"] }
  ],

  // ---- ESCENARIOS (sets del estudio) ----------------------------
  // Hasta 3. show:false = oculto. comingSoon:true = tarjeta "Próximamente" (quítalo al poner image). Para agregar uno: pon show:true, texto e imagen
  // (image = ruta a un .jpg.b64 en assets/media).
  scenarios: [
    { show: true, name: "Escenario 1", image: "assets/media/escenario-1.jpg.b64",
      alt: "Escenario 1 de Captoora: ciclorama blanco, TV, vitrina, softbox y tripié",
      desc: "Uno de los espacios de Captoora. Aquí tienes con qué jugar: ciclorama blanco o negro, luz de todo tipo y varios rincones para cambiar de fondo sin salir del set.",
      items: ["TV", "Espejos", "Armario", "Softbox", "Tripiés", "Iluminación de todo tipo", "Ciclorama blanco o negro", "Algunos sets, elementos y herramientas para tu sesión"],
      note: "Incluido en la Renta de estudio.",
      cta: "Agendar el Escenario 1",
      waMessage: "Hola, quiero agendar el Escenario 1." },
    { show: true, comingSoon: true, name: "Escenario 2", image: "", alt: "", desc: "", items: [], waMessage: "Hola, quiero agendar el Escenario 2." },
    { show: true, comingSoon: true, name: "Escenario 3", image: "", alt: "", desc: "", items: [], waMessage: "Hola, quiero agendar el Escenario 3." }
  ],

  // ---- PORTAFOLIO --------------------------------------------------
  // Únicamente fotografía real aprobada: GlowTours y Chipinque.
  portfolioCats: [
    { key: "glowtours", label: "GlowTours" },
    { key: "chipinque", label: "Chipinque" }
  ],
  portfolio: [
    { cat: "glowtours", image: "assets/media/pf-glow-cpt_0853.jpg.b64", w: 1200, h: 800, alt: "Fotografía oficial de evento GlowTours en Amapola Eventos" },
    { cat: "glowtours", image: "assets/media/pf-glow-cpt_0855.jpg.b64", w: 800,  h: 1200, alt: "Retrato de participante en evento GlowTours con luz de autor" },
    { cat: "glowtours", image: "assets/media/pf-glow-cpt_0863.jpg.b64", w: 1200, h: 800, alt: "Dinámica y activación en set GlowTours" },
    { cat: "glowtours", image: "assets/media/pf-glow-cpt_0878.jpg.b64", w: 1200, h: 800, alt: "Momento estelar y energía en GlowTours" },
    { cat: "chipinque",  image: "assets/media/pf-chipinque-01.jpg.b64", w: 1200, h: 900, alt: "Paseo familiar por el sendero arbolado en Parque Ecológico Chipinque" },
    { cat: "chipinque",  image: "assets/media/pf-chipinque-02.jpg.b64", w: 1200, h: 900, alt: "Retrato exterior con luz natural y vegetación en Chipinque" },
    { cat: "chipinque",  image: "assets/media/pf-chipinque-fam.jpg.b64", w: 1200, h: 900, alt: "Retrato grupal de familia completa en exteriores bajo los pinos de Chipinque" }
  ],

  // ---- PREGUNTAS FRECUENTES ---------------------------------------
  faq: [
    { q: "¿Cómo funciona la sesión para crear mi clon digital?", a: "Preparamos tu imagen, luces y encuadre; te dirigimos durante la grabación y revisamos el material para configurar y probar tu avatar en la plataforma acordada. Trabajamos con tu autorización y cotizamos el alcance antes de comenzar." },
    { q: "¿El clon digital incluye videos ilimitados o una suscripción?", a: "La cantidad de videos, la plataforma, sus licencias y los costos de generación se especifican en cada cotización. La semejanza, voz y gestos se revisan en una prueba; los resultados dependen del material y de la plataforma." },
    { q: "¿Hay estacionamiento?", a: "Pregúntanos por WhatsApp y te decimos dónde dejar el carro." },
    { q: "¿Cuántas personas caben?", a: "Depende del escenario y del tipo de sesión. Pregúntanos y lo vemos para tu grupo." },
    { q: "¿Puedo llevar a mi mascota?", a: "Pregúntanos antes de tu sesión." },
    { q: "¿Cómo aparto?", a: "Con 30% de anticipo por transferencia. El resto, al terminar." },
    { q: "¿Se pueden hacer fotos en exterior?", a: "Sí. Hay un parque justo afuera del estudio: fotos con luz natural y luego al set." }
  ],

  // ---- RESEÑAS (nada de reseñas inventadas) ------------------------
  // Pega aquí el link de reseñas de Google Business cuando exista.
  reviews: { googleUrl: "" },

  // ---- REDES -------------------------------------------------
  social: [
    { label: "Instagram", handle: "@Captoora.studio", url: "https://instagram.com/captoora.studio" },
    { label: "TikTok", handle: "@captoora.studiomty", url: "https://www.tiktok.com/@captoora.studiomty" },
    { label: "X", handle: "@captoora_studio", url: "https://x.com/captoora_studio" }
  ]
};
