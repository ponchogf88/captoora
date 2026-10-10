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
    whatToDo: "Escríbeme por WhatsApp: qué quieres (foto, hora IA o combo), qué día y cuántas personas. Te confirmo y te mando la ubicación.",
    when: "Tú eliges el día. Lo cuadramos por WhatsApp.",
    how: "30% de anticipo por transferencia. El resto, al terminar.",
    address: "Colinas de San Jerónimo 11, Monterrey",
    mapsUrl: "https://www.google.com/maps/search/?api=1&query=Colinas+de+San+Jer%C3%B3nimo+11+Monterrey",
    ctaText: "Agenda por WhatsApp",
    waMessage: "Hola Captoora, quiero agendar una sesión. Me interesa: (foto / hora IA / combo). Día: . Personas: ."
  },

  // ---- PAQUETES (offers.md, 23 sep 2026) -----------------------
  deposit: "Apartas con 30% de anticipo por transferencia. El resto, al terminar.",
  packages: [
    { name: "Sesión básica", price: 1000, unit: "1 hora",
      items: ["1 set con luces", "Te dirijo la pose", "15 fotos editadas"] },
    { name: "Combo Studio + Clips", price: 1600, unit: "2 horas", featured: true,
      badge: "El que recomiendo",
      items: ["Sesión en set", "8 a 12 clips listos para Reels/TikTok", "1 bebida"] },
    { name: "Hora IA", price: 300, unit: "60 min",
      items: ["Mesa y Wi-Fi", "Guía en Opus Clip, Captions, CapCut, Canva", "1 bebida"] },
    { name: "Bloque IA", price: 750, unit: "3 horas",
      items: ["Todo lo de la Hora IA", "Prioridad de render", "2 bebidas"] },
    { name: "Video por encargo", price: 1200, unit: "por video",
      items: ["Hasta 60–90 s", "Mandas brief, guion y referencias", "Te entrego el archivo"] }
  ],

  // ---- REDES -------------------------------------------------
  social: [
    { label: "Instagram", handle: "@Captoora.studio", url: "https://instagram.com/captoora.studio" },
    { label: "TikTok", handle: "@captoora.studiomty", url: "https://www.tiktok.com/@captoora.studiomty" },
    { label: "X", handle: "@captoora_studio", url: "https://x.com/captoora_studio" }
  ]
};
