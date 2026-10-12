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
    { name: "Combo Studio + Clips", price: 1600, unit: "2 horas", featured: true,
      badge: "El que recomiendo",
      items: ["Sesión en set", "8 a 12 clips listos para Reels/TikTok"] },
    { name: "Clase de cámara", price: 350, regularPrice: 500, unit: "por hora",
      promoLabel: "Promoción de octubre", validUntil: "Válido hasta el 31 de octubre", secondary: true, badge: "Promo octubre",
      desc: "¿Tienes cámara profesional y no sabes usarla? Vente al estudio y te enseño. Una hora de clase práctica con tu propia cámara: modo manual, luz y enfoque, disparando en el set.",
      items: ["Con tu propia cámara", "Práctica en el set, no teoría", "Sales sabiendo usar el modo manual"],
      cta: "Agendar mi clase",
      waMessage: "Hola, quiero agendar una clase de cámara." },
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
  // Fotos propias (nada de banco ni IA). Para agregar una: sube el .jpg.b64 a
  // assets/media/ y añade un objeto aquí. cat = una de las claves de portfolioCats.
  // w/h = tamaño real de la foto (para que el grid no brinque al cargar).
  portfolioCats: [
    { key: "retrato", label: "Retrato" },
    { key: "eventos", label: "Eventos" },
    { key: "marca",   label: "Producto y marca" },
    { key: "fondoblanco", label: "Fondo blanco" },
    // Sin fotos todavía: salen como "Próximamente" hasta que agregues fotos con ese cat.
    { key: "ninos",   label: "Niños / Familia", soon: true },
    { key: "parque",  label: "Parque", soon: true },
    { key: "fachada", label: "Fachada", soon: true }
  ],
  portfolio: [
    { cat: "retrato", image: "assets/media/pf-1946.jpg.b64", w: 800,  h: 1200, alt: "Retrato de hombre en exterior, luz de tarde" },
    { cat: "eventos", image: "assets/media/pf-0032.jpg.b64", w: 1200, h: 800,  alt: "Foto grupal de un evento de bienestar al aire libre" },
    { cat: "marca",   image: "assets/media/pf-1027.jpg.b64", w: 1200, h: 800,  alt: "Exhibición de productos Nutriplus y Dr. C. Tuna en evento Farmasi" },
    { cat: "retrato", image: "assets/media/pf-0912.jpg.b64", w: 800,  h: 1200, alt: "Atleta haciendo parada de manos junto a la alberca" },
    { cat: "eventos", image: "assets/media/pf-1042.jpg.b64", w: 1200, h: 800,  alt: "Coaches dirigiendo al grupo frente al banner del evento" },
    { cat: "marca",   image: "assets/media/pf-1062.jpg.b64", w: 800,  h: 1200, alt: "Activación de marca Farmasi con entrenamiento al aire libre" },
    { cat: "retrato", image: "assets/media/pf-1957.jpg.b64", w: 902,  h: 1200, alt: "Retrato de hombre con camisa negra" },
    { cat: "eventos", image: "assets/media/pf-0867.jpg.b64", w: 1200, h: 800,  alt: "Vista general del evento con banner Nutriplus" },
    { cat: "marca",   image: "assets/media/pf-0041.jpg.b64", w: 1200, h: 800,  alt: "Momento de baño de hielo durante la activación de marca" },
    { cat: "fondoblanco", image: "assets/media/pf-w0818.jpg.b64", w: 800, h: 1200, alt: "Grupo de modelos Farmasi en fondo blanco" },
    { cat: "fondoblanco", image: "assets/media/pf-w0828.jpg.b64", w: 1200, h: 800, alt: "Cuatro modelos Farmasi de pie en fondo blanco" },
    { cat: "fondoblanco", image: "assets/media/pf-w0842.jpg.b64", w: 1200, h: 800, alt: "Modelos Farmasi con productos Nutriplus en fondo blanco" }
  ],

  // ---- PREGUNTAS FRECUENTES ---------------------------------------
  faq: [
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
