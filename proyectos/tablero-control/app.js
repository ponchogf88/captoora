/* Captoora Control v1.2 — Dark default, real thumbnails, Linux icons & Cuotas */
(() => {
  const STORAGE_KEY = "captoora_control_state_v1";
  const THEME_KEY = "captoora_control_theme";
  const VALID_ROUTES = ["overview", "flujo", "referencias", "publicados", "cola", "cuotas"];
  const ROUTE_TITLES = {
    overview: "Resumen",
    flujo: "Flujo y relevos",
    referencias: "Referencias",
    publicados: "Publicados",
    cola: "Cola semanal",
    cuotas: "Cuotas y membresías"
  };

  /* Crisp 16x16 stroke=1.5 Linux-style symbolic SVG icons */
  const ICONS = {
    terminal: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="1.5" y="2.5" width="13" height="11" rx="1.5"/><path d="M4.5 6.5L7 8.5 4.5 10.5M8 10.5h3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "file-code": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M3.5 2h6l3 3v9h-9z" stroke-linejoin="round"/><path d="M6 8L4.5 9.5 6 11M10 8l1.5 1.5L10 11" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    waveform: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M2 8v0m2.5-3v6m3-8v10m3-6v2m3-4v6" stroke-linecap="round"/></svg>',
    cube: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M8 2l5.5 3v6L8 14l-5.5-3V5L8 2z" stroke-linejoin="round"/><path d="M2.5 5L8 8l5.5-3M8 8v6" stroke-linejoin="round"/></svg>',
    smartphone: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="4.5" y="1.8" width="7" height="12.4" rx="1.4"/><path d="M7.2 12h1.6" stroke-linecap="round"/></svg>',
    calendar: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="2" y="3" width="12" height="10.5" rx="1.5"/><path d="M2 6.5h12M5.5 1.8v2.2M10.5 1.8v2.2" stroke-linecap="round"/></svg>',
    gauge: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M3 11.5a5.5 5.5 0 1110 0" stroke-linecap="round"/><path d="M8 9l2.6-2.6" stroke-linecap="round"/><circle cx="8" cy="9.5" r="0.9" fill="currentColor"/></svg>',
    scissors: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><circle cx="4.5" cy="11.5" r="2"/><circle cx="11.5" cy="11.5" r="2"/><path d="M6 10L12.5 3M10 10L3.5 3" stroke-linecap="round"/></svg>',
    layers: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M8 2.5L13.5 5.5 8 8.5 2.5 5.5 8 2.5z" stroke-linejoin="round"/><path d="M2.5 8.5L8 11.5l5.5-3M2.5 11.2L8 14l5.5-2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    archive: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="2" y="2.5" width="12" height="3" rx="0.8"/><path d="M3 5.5v7.5a1 1 0 001 1h8a1 1 0 001-1V5.5M6.5 8.5h3" stroke-linecap="round"/></svg>',
    ban: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><circle cx="8" cy="8" r="5.5"/><path d="M4.2 4.2l7.6 7.6" stroke-linecap="round"/></svg>',
    plus: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M8 3v10M3 8h10" stroke-linecap="round"/></svg>',
    pencil: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M11.2 2.8l2 2-7.4 7.4-2.6.6.6-2.6 7.4-7.4z" stroke-linejoin="round"/></svg>',
    eye: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M1.8 8s2.3-4 6.2-4 6.2 4 6.2 4-2.3 4-6.2 4-6.2-4-6.2-4z"/><circle cx="8" cy="8" r="1.6"/></svg>',
    note: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M3 2.5h10v8l-3 3H3z" stroke-linejoin="round"/><path d="M10 10.5v3" stroke-linecap="round"/></svg>',
    external: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M9.5 2.5h4v4M13.5 2.5L7.5 8.5M6.5 4H3.5v8.5H12V9.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    sun: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><circle cx="8" cy="8" r="2.8"/><path d="M8 1.8v1.4M8 12.8v1.4M1.8 8h1.4M12.8 8h1.4M3.6 3.6l1 1M11.4 11.4l1 1M12.4 3.6l-1 1M4.6 11.4l-1 1" stroke-linecap="round"/></svg>',
    moon: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M12.8 10.2A5.2 5.2 0 015.8 3.2a5.5 5.5 0 107 7z" stroke-linejoin="round"/></svg>',
    pdf: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M3.5 2h6l3 3v9h-9z" stroke-linejoin="round"/><path d="M6 10.5h4M6 8h4" stroke-linecap="round"/></svg>',
    tiktok: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M9.5 2.5v7.3a2.5 2.5 0 11-1.8-2.4M9.5 2.5c.7 1.6 2 2.4 3.5 2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    youtube: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="1.8" y="3.5" width="12.4" height="9" rx="2.2"/><path d="M6.8 6.2l3.4 1.8-3.4 1.8V6.2z" stroke-linejoin="round"/></svg>',
    instagram: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="2.5" y="2.5" width="11" height="11" rx="3"/><circle cx="8" cy="8" r="2.5"/><circle cx="11.3" cy="4.7" r="0.6" fill="currentColor"/></svg>',
    facebook: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="2.2" y="2.2" width="11.6" height="11.6" rx="2"/><path d="M9.5 13.8V8.8h1.8l.3-2H9.5V5.6c0-.6.3-1 1-1h1V2.9H10c-1.5 0-2.5.9-2.5 2.5v1.4H6v2h1.5v5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    meta: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M2.2 10.2c0-2.5 1.3-4.6 2.8-4.6 1.2 0 2 1.4 3 3.2 1-1.8 1.8-3.2 3-3.2 1.5 0 2.8 2.1 2.8 4.6 0 1.4-.8 2.3-1.9 2.3-1.1 0-1.9-.9-2.9-2.6L8 8.3l-1 1.6c-1 1.7-1.8 2.6-2.9 2.6-1.1 0-1.9-.9-1.9-2.3z" stroke-linejoin="round"/></svg>',
    linkedin: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="2.2" y="2.2" width="11.6" height="11.6" rx="1.8"/><path d="M5.2 7v4.2M5.2 5v.2M8 11.2V7m0 1.5a1.8 1.8 0 013.4.5v2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    x: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M3 3l10 10M13 3L3 13" stroke-linecap="round"/></svg>',
    threads: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><circle cx="8" cy="8" r="5.5"/><path d="M9.8 8.2a1.9 1.9 0 11-1.8-2.2c1.1 0 1.8.8 1.8 2.3v1.2" stroke-linecap="round"/></svg>',
    globe: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><circle cx="8" cy="8" r="5.5"/><path d="M2.5 8h11M8 2.5a8 8 0 010 11 8 8 0 010-11z"/></svg>',
    gemini: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M8 1.5C8.5 5.2 10.8 7.5 14.5 8c-3.7.5-6 2.8-6.5 6.5-.5-3.7-2.8-6-6.5-6.5 3.7-.5 6-2.8 6.5-6.5z" fill="currentColor" stroke="none"/></svg>',
    agy: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><ellipse cx="8" cy="8" rx="6" ry="2.7" transform="rotate(-28 8 8)"/><circle cx="8" cy="8" r="1.9" fill="currentColor" stroke="none"/></svg>',
    python: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M8 2.1c-2.2 0-2.4 1-2.4 2.1v1.4h4v.7H4.2C2.9 6.3 2.1 7.2 2.1 8.8s.8 2.5 2.1 2.5h1.2V10c0-1.2.9-2.2 2.2-2.2h2.7c.9 0 1.5-.6 1.5-1.5V4.1c0-1.1-1.1-2-3.8-2z" stroke-linejoin="round"/><path d="M8 13.9c2.2 0 2.4-1 2.4-2.1v-1.4h-4v-.7h5.4c1.3 0 2.1-.9 2.1-2.5s-.8-2.5-2.1-2.5h-1.2V6c0 1.2-.9 2.2-2.2 2.2H5.7c-.9 0-1.5.6-1.5 1.5v2.2c0 1.1 1.1 2 3.8 2z" stroke-linejoin="round"/><circle cx="6.7" cy="3.8" r="0.6" fill="currentColor" stroke="none"/><circle cx="9.3" cy="12.2" r="0.6" fill="currentColor" stroke="none"/></svg>',
    elevenlabs: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="4.5" y="2.5" width="2.3" height="11" rx="0.4" fill="currentColor" stroke="none"/><rect x="9.2" y="2.5" width="2.3" height="11" rx="0.4" fill="currentColor" stroke="none"/></svg>',
    threejs: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M2.5 3L13.5 6.3 5.5 13.7z" stroke-linejoin="round"/><path d="M8 4.7L9.5 9.9 4 8.3zM8 4.7l1.5 5.2 4-3.6" stroke-linejoin="round"/></svg>',
    hyperframes: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="2" y="2.8" width="12" height="10.4" rx="1.4"/><path d="M2 5.5h12M6.7 7.6l3.2 1.7-3.2 1.7V7.6z" stroke-linejoin="round"/></svg>',
    capcut: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M3 4.2l8.5 7.6M3 11.8l8.5-7.6M11.5 4.2h1.6M11.5 11.8h1.6" stroke-linecap="round"/></svg>',
    opusclip: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="2" y="2.8" width="12" height="10.4" rx="2"/><path d="M6.2 5.8v4.4M9.2 5.8l3 2.2-3 2.2V5.8z" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    captions: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="2" y="3" width="12" height="10" rx="1.6"/><path d="M7 6.5a1.5 1.5 0 100 3M11 6.5a1.5 1.5 0 100 3" stroke-linecap="round"/></svg>',
    canva: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><circle cx="8" cy="8" r="5.8"/><path d="M10.2 6.1a2.4 2.4 0 10.1 3.7" stroke-linecap="round"/></svg>',
    claude: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M8 2v12M2 8h12M3.8 3.8l8.4 8.4M12.2 3.8l-8.4 8.4" stroke-linecap="round"/></svg>',
    chatgpt: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><polygon points="8,2 13,5 13,11 8,14 3,11 3,5" stroke-linejoin="round"/><circle cx="8" cy="8" r="2.1"/></svg>',
    grok: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><circle cx="8" cy="8" r="5.5"/><path d="M3.5 12.5L12.5 3.5" stroke-linecap="round"/></svg>',
    perplexity: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M8 2v12M3.2 4.5l9.6 7M12.8 4.5l-9.6 7" stroke-linecap="round"/><rect x="4.5" y="4.5" width="7" height="7" rx="0.5"/></svg>',
    heygen: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M8 2L13.5 8 8 14 2.5 8z" stroke-linejoin="round"/><path d="M7 6.2l3 1.8-3 1.8V6.2z" fill="currentColor" stroke="none"/></svg>',
    evoto: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><circle cx="8" cy="8" r="5.5"/><path d="M8 2.5l2.5 4.2M13.5 8h-5M11 12.8L8.5 8.5M5 12.8l2.5-4.3M2.5 8h5M5 3.2L7.5 7.5" stroke-linecap="round"/></svg>',
    pixieset: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><rect x="2" y="3" width="12" height="10" rx="1.2"/><path d="M3.5 11.2l3-3 2.2 2 1.8-1.5 2 2.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="5.5" cy="5.8" r="0.8" fill="currentColor" stroke="none"/></svg>',
    icloud: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M4.8 12.5h6.7a2.5 2.5 0 00.3-5A3.6 3.6 0 005 6.8a2.8 2.8 0 00-.2 5.7z" stroke-linejoin="round"/></svg>',
    ollama: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M5.5 13.5v-4L5 4.5 6.5 6h3L11 4.5l-.5 5v4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="6.8" cy="8.8" r="0.5" fill="currentColor" stroke="none"/><circle cx="9.2" cy="8.8" r="0.5" fill="currentColor" stroke="none"/></svg>'
  };

  const iconHtml = (name) => ICONS[name] || ICONS.globe;
  const clone = (v) => JSON.parse(JSON.stringify(v));
  const esc = (v) => String(v == null ? "" : v).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const fmtInt = (n) => new Intl.NumberFormat("es-MX").format(Math.round(n));
  const fmtPct = (v) => (v == null || v === "" ? "—" : `${Number(v).toFixed(1)}%`);

  function channelIconKey(name) {
    const l = String(name || "").toLowerCase();
    if (l.includes("tiktok")) return "tiktok";
    if (l.includes("youtube")) return "youtube";
    if (l.includes("instagram")) return "instagram";
    if (l.includes("facebook")) return "facebook";
    if (l.includes("linkedin")) return "linkedin";
    if (l.includes("x ") || l === "x") return "x";
    if (l.includes("threads")) return "threads";
    return "globe";
  }

  /* Hydrate localStorage safely across versions preserving user edits */
  function loadState() {
    const base = clone(window.CAPTOORA_DATA);
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (!saved) return base;
      const parsed = JSON.parse(saved);
      if (!parsed) return base;
      const schemaChanged = parsed.schema_version !== base.schema_version;
      parsed.schema_version = base.schema_version;
      if (schemaChanged) {
        parsed.meta = { ...(parsed.meta || {}), ...base.meta };
      }
      parsed.estaciones_relevo = (parsed.estaciones_relevo || base.estaciones_relevo).map((st, idx) => ({
        ...(base.estaciones_relevo[idx] || {}),
        ...st,
        icon: (base.estaciones_relevo[idx] || {}).icon || st.icon || "terminal",
        logos: (base.estaciones_relevo[idx] || {}).logos || st.logos || []
      }));
      parsed.relevos_banca = (parsed.relevos_banca || base.relevos_banca).map((b, idx) => ({
        ...(base.relevos_banca[idx] || {}),
        ...b,
        icon: (base.relevos_banca[idx] || {}).icon || b.icon || "archive"
      }));
      const savedRefs = (parsed.referencias || base.referencias).map((r) => {
        const match = base.referencias.find((br) => br.id === r.id) || {};
        return { ...match, ...r, plat_icon: r.plat_icon || match.plat_icon || "globe", thumb: r.thumb !== undefined ? r.thumb : match.thumb };
      });
      const seenRefIds = new Set(savedRefs.map((r) => r.id));
      parsed.referencias = savedRefs.concat(base.referencias.filter((br) => !seenRefIds.has(br.id)));
      parsed.publicados = (parsed.publicados || base.publicados).map((p) => {
        const match = base.publicados.find((bp) => bp.id === p.id) || {};
        return { ...match, ...p, thumb: p.thumb || match.thumb || null };
      });
      const savedCola = (parsed.cola_semanal || base.cola_semanal).map((c) => {
        const match = base.cola_semanal.find((bc) => bc.orden === c.orden) || {};
        return { ...match, ...c, thumb: c.thumb || match.thumb || null };
      });
      const seenColaOrden = new Set(savedCola.map((c) => c.orden));
      parsed.cola_semanal = savedCola.concat(base.cola_semanal.filter((bc) => !seenColaOrden.has(bc.orden)));
      if (Array.isArray(parsed.cuotas)) {
        const savedCuotas = parsed.cuotas.map((q) => {
          const match = base.cuotas.find((bq) => bq.id === q.id) || {};
          if (schemaChanged && q.id === "CTA-01") {
            return { ...q, ...match };
          }
          return { ...match, ...q, icon: match.icon || q.icon || "gauge" };
        });
        const seenQuotaIds = new Set(savedCuotas.map((q) => q.id));
        parsed.cuotas = savedCuotas.concat(base.cuotas.filter((bq) => !seenQuotaIds.has(bq.id)));
      } else {
        parsed.cuotas = base.cuotas;
      }
      return parsed;
    } catch (_) {
      return base;
    }
  }

  let state = loadState();
  let currentRoute = "overview";
  let refFilter = "all";
  let colaFilter = "all";
  let quotaFilter = "all";
  let searchQuery = "";

  const editorDialog = document.getElementById("editor-dialog");
  const editorTitle = document.getElementById("editor-title");
  const editorBody = document.getElementById("editor-body");

  function saveState(stampText = "Local OK") {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      const el = document.getElementById("save-indicator");
      if (el) el.textContent = stampText;
    } catch (_) {}
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem(THEME_KEY, theme); } catch (_) {}
    const btn = document.getElementById("btn-theme-toggle");
    if (btn) {
      btn.innerHTML = theme === "dark" ? ICONS.sun : ICONS.moon;
      btn.title = theme === "dark" ? "Cambiar a modo claro" : "Cambiar a modo oscuro";
      btn.setAttribute("aria-label", btn.title);
    }
  }

  function initTheme() {
    let saved = "dark";
    try {
      const t = localStorage.getItem(THEME_KEY);
      if (t === "light" || t === "dark") saved = t;
    } catch (_) {}
    applyTheme(saved);
  }

  function hydrateStaticIcons() {
    document.querySelectorAll("[data-icon]").forEach((el) => {
      el.innerHTML = iconHtml(el.dataset.icon);
    });
  }

  function pillClassFor(label) {
    const v = String(label || "").toLowerCase();
    if (v.includes("adopt") || v.includes("activo") || v.includes("publicado") || v.includes("lista") || v.includes("local")) return "pill-positive";
    if (v.includes("turno") || v.includes("membership")) return "pill-accent";
    if (v.includes("parcial") || v.includes("prueba") || v.includes("capcut") || v.includes("programado") || v.includes("fase 2") || v.includes("siguiente") || v.includes("trial")) return "pill-warning";
    if (v.includes("pirita") || v.includes("reemplazado")) return "pill-negative";
    return "pill-neutral";
  }

  function syncElevenLabsFromQuota() {
    const elItem = (state.cuotas || []).find((q) => q.id === "CTA-01");
    if (elItem && elItem.disponible != null) {
      state.meta.cuota_elevenlabs.disponible = Number(elItem.disponible);
      if (elItem.total != null) state.meta.cuota_elevenlabs.total = Number(elItem.total);
    }
  }

  function computeMetrics() {
    syncElevenLabsFromQuota();
    const pubs = state.publicados;
    const refs = state.referencias;
    const cola = state.cola_semanal;
    const cuotas = state.cuotas || [];
    const meta = state.meta;

    const totalPub = pubs.length;
    const target = meta.meta_videos_validacion;
    const pctGoal = (totalPub / target) * 100;
    const totalViews = pubs.reduce((acc, p) => acc + (Number(p.vistas) || 0), 0);
    const avgViews = totalPub > 0 ? totalViews / totalPub : 0;

    const refCounts = {
      all: refs.length,
      Adoptado: refs.filter((r) => r.veredicto === "Adoptado").length,
      Parcial: refs.filter((r) => r.veredicto === "Parcial").length,
      "En prueba": refs.filter((r) => r.veredicto === "En prueba").length,
      Pirita: refs.filter((r) => r.veredicto === "Pirita").length
    };

    const colaCounts = {
      all: cola.length,
      "Listo en disco": cola.filter((c) => c.estado_slot === "Listo en disco").length,
      "En CapCut Pro": cola.filter((c) => c.estado_slot === "En CapCut Pro").length,
      Programado: cola.filter((c) => c.estado_slot === "Programado").length,
      Publicado: cola.filter((c) => c.estado_slot === "Publicado").length
    };
    const colaPendientes = cola.length - colaCounts.Publicado;

    const quotaCounts = {
      all: cuotas.length,
      Membership: cuotas.filter((q) => q.tipo === "Membership").length,
      "Free Trial": cuotas.filter((q) => q.tipo === "Free Trial").length,
      Gratis: cuotas.filter((q) => q.tipo === "Gratis").length,
      "Local $0": cuotas.filter((q) => q.tipo === "Local $0").length
    };

    console.assert(
      refCounts.Adoptado + refCounts.Parcial + refCounts["En prueba"] + refCounts.Pirita === refCounts.all,
      "Reconciliación: veredictos == referencias"
    );
    console.assert(
      colaCounts["Listo en disco"] + colaCounts["En CapCut Pro"] + colaCounts.Programado + colaCounts.Publicado === colaCounts.all,
      "Reconciliación: estados == cola"
    );
    console.assert(
      quotaCounts.Membership + quotaCounts["Free Trial"] + quotaCounts.Gratis + quotaCounts["Local $0"] === quotaCounts.all,
      "Reconciliación: tipos == cuotas"
    );

    const quotaPct = meta.cuota_elevenlabs.total > 0
      ? (meta.cuota_elevenlabs.disponible / meta.cuota_elevenlabs.total) * 100
      : 0;
    return { totalPub, target, pctGoal, totalViews, avgViews, refCounts, colaCounts, colaPendientes, quotaCounts, quotaPct };
  }

  function renderAll() {
    const m = computeMetrics();

    document.getElementById("nav-cola-count").textContent = String(m.colaPendientes);
    document.getElementById("topbar-goal-pill").textContent = `${m.totalPub} / ${m.target} publicados`;

    const conCola = Math.min(m.target, m.totalPub + m.colaPendientes);
    document.getElementById("overview-finding").textContent =
      `Llevas ${m.totalPub} de ${m.target} videos publicados (${m.pctGoal.toFixed(1)}%). Tienes ${m.colaPendientes} en cola para llegar a ${conCola} de ${m.target} esta semana.`;

    document.getElementById("kpi-published").innerHTML = `${fmtInt(m.totalPub)} <span class="kpi-unit">/ ${m.target}</span>`;
    document.getElementById("kpi-published-note").textContent = `${m.pctGoal.toFixed(1)}% · +${m.colaPendientes} en cola`;
    document.getElementById("kpi-views").textContent = fmtInt(m.totalViews);
    document.getElementById("kpi-views-note").textContent = `Prom. ${fmtInt(m.avgViews)} por video · ${m.totalPub} registros`;
    document.getElementById("kpi-refs").textContent = fmtInt(m.refCounts.all);
    document.getElementById("kpi-refs-note").textContent = `${m.refCounts.Adoptado} adoptadas · ${m.refCounts.Parcial} parciales · ${m.refCounts["En prueba"]} en prueba`;
    document.getElementById("kpi-quota").innerHTML = `${fmtInt(state.meta.cuota_elevenlabs.disponible)} <span class="kpi-unit">chars</span>`;
    document.getElementById("kpi-quota-note").textContent = `${m.quotaPct.toFixed(1)}% de ${fmtInt(state.meta.cuota_elevenlabs.total)} disponibles`;

    renderRelayTrack();
    renderThumbStrip();
    renderOverviewCharts(m);
    renderRoadmap();
    renderFlujoTables();
    renderReferencias(m);
    renderPublicados();
    renderCola(m);
    renderCuotas(m);
  }

  function renderLogosStrip(logos) {
    if (!logos || !logos.length) return "";
    return `<div class="relay-logos">${logos.map((lg) =>
      `<span class="brand-logo" title="${esc(lg.label)}" aria-label="${esc(lg.label)}">${iconHtml(lg.key)}</span>`
    ).join("")}</div>`;
  }

  function renderRelayTrack() {
    document.getElementById("relay-track").innerHTML = state.estaciones_relevo.map((st) => {
      const isCurrent = st.estado.toLowerCase().includes("turno");
      return `
        <button type="button" class="relay-node ${isCurrent ? "is-current" : ""}" data-station="${st.paso}">
          <div class="relay-top">
            <span class="relay-id-wrap">${iconHtml(st.icon)}<span class="relay-code">${esc(st.codigo)}</span></span>
            <span class="pill ${pillClassFor(st.estado)}">${esc(st.estado)}</span>
          </div>
          <div class="relay-title">${esc(st.nombre)}</div>
          ${renderLogosStrip(st.logos)}
          <div class="relay-owner">${esc(st.responsable)}</div>
          <div class="relay-output">${esc(st.entrega)}</div>
        </button>
      `;
    }).join("");
  }

  function renderThumbStrip() {
    const pubTiles = state.publicados.map((p, idx) => `
      <button type="button" class="thumb-tile" data-edit-pub="${esc(p.id)}" title="${esc(p.titulo)}">
        <div class="thumb-box">
          ${p.thumb ? `<img src="${esc(p.thumb)}" alt="${esc(p.titulo)}">` : ""}
        </div>
        <div class="thumb-meta">
          <span class="thumb-code">PUB-${idx + 1}</span>
          <span class="thumb-dot thumb-dot-pub" aria-hidden="true"></span>
        </div>
        <div class="thumb-cap">${esc(p.titulo)}</div>
      </button>
    `);

    const colaTiles = state.cola_semanal.map((c) => {
      const dotCls = c.estado_slot === "Publicado"
        ? "thumb-dot-pub"
        : c.estado_slot === "En CapCut Pro"
          ? "thumb-dot-capcut"
          : "thumb-dot-ready";
      return `
        <button type="button" class="thumb-tile" data-edit-slot="${esc(c.orden)}" title="${esc(c.titulo)}">
          <div class="thumb-box">
            ${c.thumb ? `<img src="${esc(c.thumb)}" alt="${esc(c.titulo)}">` : ""}
          </div>
          <div class="thumb-meta">
            <span class="thumb-code">S${esc(c.orden)}</span>
            <span class="thumb-dot ${dotCls}" aria-hidden="true"></span>
          </div>
          <div class="thumb-cap">${esc(c.titulo)}</div>
        </button>
      `;
    });

    document.getElementById("overview-thumb-strip").innerHTML = pubTiles.concat(colaTiles).join("");
  }

  function renderOverviewCharts(m) {
    const chartEl = document.getElementById("chart-published-views");
    if (state.publicados.length === 0) {
      chartEl.innerHTML = `<div class="empty-row">Sin publicaciones registradas todavía.</div>`;
    } else if (window.Charts && typeof window.Charts.bars === "function") {
      const labels = state.publicados.map((p) => p.titulo.split("·")[0].trim());
      const values = state.publicados.map((p) => Number(p.vistas) || 0);
      const maxVal = Math.max(...values);
      const hiIdx = values.indexOf(maxVal);
      window.Charts.bars(chartEl, {
        labels,
        values,
        highlight: hiIdx >= 0 ? hiIdx : 0,
        height: 256,
        format: window.Charts.fmt.int
      });
    }

    const porProducir = Math.max(0, m.target - m.totalPub - m.colaPendientes);
    document.getElementById("goal-bar-summary").textContent =
      `${m.totalPub} publicados · ${m.colaPendientes} en cola · ${porProducir} por producir`;

    const pubW = (m.totalPub / m.target) * 100;
    const colaW = (Math.min(m.colaPendientes, m.target - m.totalPub) / m.target) * 100;
    const remW = Math.max(0, 100 - pubW - colaW);
    document.getElementById("chart-goal-plan").innerHTML = `
      <div class="goal-bar-track" role="img" aria-label="Avance hacia 20 videos: ${m.totalPub} publicados, ${m.colaPendientes} en cola, ${porProducir} por producir">
        <div class="goal-seg-pub" style="width:${pubW.toFixed(1)}%"></div>
        <div class="goal-seg-cola" style="width:${colaW.toFixed(1)}%"></div>
        <div class="goal-seg-rem" style="width:${remW.toFixed(1)}%"></div>
      </div>
      <div class="goal-legend">
        <span><span class="legend-swatch" style="background:var(--chart-1)"></span>Publicados: <strong class="num">${m.totalPub}</strong></span>
        <span><span class="legend-swatch" style="background:var(--seg-cola)"></span>En cola: <strong class="num">${m.colaPendientes}</strong></span>
        <span><span class="legend-swatch" style="background:var(--raised);border:1px solid var(--border)"></span>Por producir: <strong class="num">${porProducir}</strong></span>
      </div>
    `;
  }

  function renderRoadmap() {
    document.getElementById("roadmap-list").innerHTML = state.roadmap_hitos.map((h) => `
      <li class="roadmap-item">
        <div class="roadmap-row-head">
          <span class="roadmap-title">${esc(h.titulo)}</span>
          <span class="roadmap-time num">${esc(h.esfuerzo)}</span>
        </div>
        <div class="roadmap-meta">${esc(h.ventana)} · ${esc(h.resultado_esperado)}</div>
        <p class="roadmap-desc">${esc(h.detalle)}</p>
      </li>
    `).join("");
  }

  function renderFlujoTables() {
    document.getElementById("hardware-line").textContent =
      `${state.meta.hardware_principal} + ${state.meta.estacion_movil}`;

    document.getElementById("table-estaciones-body").innerHTML = state.estaciones_relevo.map((st) => `
      <tr>
        <td>
          <div class="inline-icon-label cell-primary">${iconHtml(st.icon)}<span><span class="mono">${esc(st.codigo)}</span> · ${esc(st.nombre)}</span></div>
          <div class="cell-secondary">${esc(st.responsable)} · ${esc(st.estacion)}</div>
          ${renderLogosStrip(st.logos)}
        </td>
        <td>${esc(st.entra)}</td>
        <td>${esc(st.entrega)}</td>
        <td>${esc(st.cuando_se_quita)}</td>
        <td class="num">${esc(st.tiempo_estimado)}</td>
        <td><span class="pill ${pillClassFor(st.estado)}">${esc(st.estado)}</span></td>
      </tr>
    `).join("");

    document.getElementById("table-banca-body").innerHTML = state.relevos_banca.map((b) => `
      <tr>
        <td><div class="inline-icon-label cell-primary">${iconHtml(b.icon)}<span>${esc(b.herramienta)}</span></div></td>
        <td><span class="pill ${pillClassFor(b.estado)}">${esc(b.estado)}</span></td>
        <td>${esc(b.momento)}</td>
        <td>${esc(b.motivo)}</td>
        <td>${esc(b.accion)}</td>
      </tr>
    `).join("");
  }

  function matchesSearch(objText) {
    if (!searchQuery) return true;
    return objText.toLowerCase().includes(searchQuery.toLowerCase());
  }

  function renderReferencias(m) {
    document.getElementById("ref-count-all").textContent = m.refCounts.all;
    document.getElementById("ref-count-adoptado").textContent = m.refCounts.Adoptado;
    document.getElementById("ref-count-parcial").textContent = m.refCounts.Parcial;
    document.getElementById("ref-count-prueba").textContent = m.refCounts["En prueba"];
    document.getElementById("ref-count-pirita").textContent = m.refCounts.Pirita;

    const filtered = state.referencias.filter((r) => {
      const okFilter = refFilter === "all" || r.veredicto === refFilter;
      const okSearch = matchesSearch(`${r.id} ${r.fuente} ${r.plataforma} ${r.que_muestra} ${r.que_obtuvimos} ${r.donde_vive} ${r.nota}`);
      return okFilter && okSearch;
    });

    document.getElementById("refs-filter-summary").textContent = `Mostrando ${filtered.length} de ${m.refCounts.all}`;
    const tbody = document.getElementById("table-referencias-body");
    if (!filtered.length) {
      tbody.innerHTML = `<tr><td colspan="7" class="empty-row">Ninguna referencia coincide con el filtro actual.</td></tr>`;
      return;
    }

    tbody.innerHTML = filtered.map((r) => {
      const isHttp = /^https?:\/\//i.test(r.url);
      const sourceLink = isHttp
        ? `<a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer" class="cell-link"><span>${esc(r.fuente)}</span>${ICONS.external}</a>`
        : `<span class="cell-primary">${esc(r.fuente)}</span>`;
      const visualSlot = r.thumb
        ? `<div class="ref-thumb-slot"><img src="${esc(r.thumb)}" alt="${esc(r.fuente)}"></div>`
        : `<div class="ref-thumb-slot" title="${esc(r.plataforma)}">${iconHtml(r.plat_icon)}</div>`;

      return `
        <tr>
          <td class="mono">${esc(r.id)}</td>
          <td class="num">${esc(r.fecha)}</td>
          <td>
            <div class="media-cell">
              ${visualSlot}
              <div>
                ${sourceLink}
                <div class="cell-secondary">${esc(r.plataforma)}</div>
              </div>
            </div>
          </td>
          <td>${esc(r.que_muestra)}</td>
          <td>
            <div>${esc(r.que_obtuvimos)}</div>
            <div class="cell-secondary mono">${esc(r.donde_vive)}</div>
            ${r.nota ? `<div class="cell-secondary"><strong>Nota:</strong> ${esc(r.nota)}</div>` : ""}
          </td>
          <td><span class="pill ${pillClassFor(r.veredicto)}">${esc(r.veredicto)}</span></td>
          <td class="num">
            <button type="button" class="icon-btn" data-edit-ref="${esc(r.id)}" title="Anotar referencia" aria-label="Anotar ${esc(r.id)}">${ICONS.note}</button>
          </td>
        </tr>
      `;
    }).join("");
  }

  function renderPublicados() {
    const filtered = state.publicados.filter((p) =>
      matchesSearch(`${p.id} ${p.titulo} ${p.serie} ${p.canal} ${p.diagnostico} ${p.mejora_siguiente}`)
    );

    const tbody = document.getElementById("table-publicados-body");
    if (!filtered.length) {
      tbody.innerHTML = `<tr><td colspan="8" class="empty-row">Ninguna publicación coincide con la búsqueda.</td></tr>`;
    } else {
      tbody.innerHTML = filtered.map((p) => {
        const netIcons = (p.canales || [p.canal]).map((c) =>
          `<span class="net-icon" title="${esc(c)}" aria-label="${esc(c)}">${iconHtml(channelIconKey(c))}</span>`
        ).join("");
        return `
          <tr>
            <td>
              <div class="media-cell">
                <button type="button" class="thumb-sm-btn" data-edit-pub="${esc(p.id)}" title="Ver / editar ${esc(p.id)}">
                  ${p.thumb ? `<img src="${esc(p.thumb)}" alt="${esc(p.titulo)}">` : iconHtml("cube")}
                </button>
                <div>
                  <div class="cell-primary"><span class="mono">${esc(p.id)}</span> · ${esc(p.titulo)}</div>
                  <div class="cell-secondary">${esc(p.fecha)} · ${esc(p.serie)}</div>
                  <div class="cell-secondary">${esc(p.diagnostico)}</div>
                  <div class="cell-secondary"><strong>Siguiente:</strong> ${esc(p.mejora_siguiente)}</div>
                </div>
              </div>
            </td>
            <td><div class="net-icons">${netIcons}</div></td>
            <td class="num">${p.vistas == null ? "—" : fmtInt(p.vistas)}</td>
            <td class="num">${fmtPct(p.retencion_pct)}</td>
            <td class="num">${p.guardados == null ? "—" : fmtInt(p.guardados)}</td>
            <td class="num">${p.dms_wa == null ? "—" : fmtInt(p.dms_wa)}</td>
            <td><span class="pill ${pillClassFor(p.estado)}">${esc(p.estado)}</span></td>
            <td class="num">
              <button type="button" class="icon-btn" data-edit-pub="${esc(p.id)}" title="Editar métricas" aria-label="Editar ${esc(p.id)}">${ICONS.pencil}</button>
            </td>
          </tr>
        `;
      }).join("");
    }

    document.getElementById("mejoras-list").innerHTML = state.mejoras_activas.map((mj) => `
      <li class="hypo-item">
        <input type="checkbox" id="chk-${esc(mj.id)}" data-toggle-mejora="${esc(mj.id)}" ${mj.aplicada ? "checked" : ""}>
        <label for="chk-${esc(mj.id)}">
          <div class="hypo-title">${esc(mj.titulo)}</div>
          <div class="hypo-desc">${esc(mj.hipotesis)}</div>
        </label>
      </li>
    `).join("");
  }

  function renderCola(m) {
    document.getElementById("cola-count-all").textContent = m.colaCounts.all;
    document.getElementById("cola-count-disco").textContent = m.colaCounts["Listo en disco"];
    document.getElementById("cola-count-capcut").textContent = m.colaCounts["En CapCut Pro"];
    document.getElementById("cola-count-prog").textContent = m.colaCounts.Programado;
    document.getElementById("cola-count-pub").textContent = m.colaCounts.Publicado;

    const filtered = state.cola_semanal.filter((c) => {
      const okFilter = colaFilter === "all" || c.estado_slot === colaFilter;
      const okSearch = matchesSearch(`${c.orden} ${c.titulo} ${c.serie} ${c.cta_palabra} ${c.archivo_cola} ${c.feedback}`);
      return okFilter && okSearch;
    });

    document.getElementById("cola-filter-summary").textContent = `Mostrando ${filtered.length} de ${m.colaCounts.all}`;
    const tbody = document.getElementById("table-cola-body");
    if (!filtered.length) {
      tbody.innerHTML = `<tr><td colspan="7" class="empty-row">Ningún slot coincide con el filtro actual.</td></tr>`;
      return;
    }

    const opts = ["Listo en disco", "En CapCut Pro", "Programado", "Publicado"];
    tbody.innerHTML = filtered.map((c) => {
      const netIcons = c.canales.map((ch) =>
        `<span class="net-icon" title="${esc(ch)}" aria-label="${esc(ch)}">${iconHtml(channelIconKey(ch))}</span>`
      ).join("") + (c.lead_magnet_pdf ? `<span class="net-icon net-icon-pdf" title="Incluye guía PDF descargable">${ICONS.pdf}</span>` : "");

      return `
        <tr>
          <td class="mono num">${esc(c.orden)}</td>
          <td class="num">${esc(c.fecha_mx)}</td>
          <td>
            <div class="media-cell">
              <button type="button" class="thumb-sm-btn" data-edit-slot="${esc(c.orden)}" title="Revisar slot ${esc(c.orden)}">
                ${c.thumb ? `<img src="${esc(c.thumb)}" alt="${esc(c.titulo)}">` : iconHtml("cube")}
              </button>
              <div>
                <div class="cell-primary">${esc(c.titulo)}</div>
                <div class="cell-secondary">${esc(c.serie)} · ${esc(c.formato)}</div>
                <div class="cell-secondary mono">${esc(c.archivo_cola)}</div>
                ${c.feedback ? `<div class="cell-secondary"><strong>Feedback:</strong> ${esc(c.feedback)}</div>` : ""}
              </div>
            </div>
          </td>
          <td><div class="net-icons">${netIcons}</div></td>
          <td class="mono">${esc(c.cta_palabra)}</td>
          <td>
            <select class="inline-select" data-slot-status="${esc(c.orden)}" aria-label="Estado del slot ${esc(c.orden)}">
              ${opts.map((o) => `<option value="${esc(o)}" ${c.estado_slot === o ? "selected" : ""}>${esc(o)}</option>`).join("")}
            </select>
          </td>
          <td class="num">
            <button type="button" class="icon-btn" data-edit-slot="${esc(c.orden)}" title="Revisar o dejar feedback" aria-label="Revisar slot ${esc(c.orden)}">${ICONS.eye}</button>
          </td>
        </tr>
      `;
    }).join("");
  }

  function renderCuotas(m) {
    const qc = m.quotaCounts;
    const trialItems = (state.cuotas || []).filter((q) => q.tipo === "Free Trial").map((q) => q.herramienta);

    document.getElementById("kpi-q-membership").textContent = fmtInt(qc.Membership);
    document.getElementById("kpi-q-trial").textContent = fmtInt(qc["Free Trial"]);
    document.getElementById("kpi-q-trial-note").textContent = trialItems.length ? `${trialItems.join(" · ")} (vigilar vencimiento)` : "Sin pruebas activas";
    document.getElementById("kpi-q-free").textContent = fmtInt(qc.Gratis + qc["Local $0"]);

    document.getElementById("q-count-all").textContent = qc.all;
    document.getElementById("q-count-membership").textContent = qc.Membership;
    document.getElementById("q-count-trial").textContent = qc["Free Trial"];
    document.getElementById("q-count-gratis").textContent = qc.Gratis;
    document.getElementById("q-count-local").textContent = qc["Local $0"];

    const filtered = (state.cuotas || []).filter((q) => {
      const okFilter = quotaFilter === "all" || q.tipo === quotaFilter;
      const okSearch = matchesSearch(`${q.id} ${q.herramienta} ${q.cuenta} ${q.tipo} ${q.unidad} ${q.origen} ${q.nota}`);
      return okFilter && okSearch;
    });

    document.getElementById("quota-filter-summary").textContent = `Mostrando ${filtered.length} de ${qc.all}`;

    const pagoList = filtered.filter((q) => q.tipo === "Membership" || q.tipo === "Free Trial");
    const gratisList = filtered.filter((q) => q.tipo === "Gratis" || q.tipo === "Local $0");

    const pagoPanel = document.getElementById("panel-cuotas-pago");
    const gratisPanel = document.getElementById("panel-cuotas-gratis");
    pagoPanel.hidden = (quotaFilter === "Gratis" || quotaFilter === "Local $0");
    gratisPanel.hidden = (quotaFilter === "Membership" || quotaFilter === "Free Trial");

    const pagoBody = document.getElementById("table-cuotas-pago-body");
    if (!pagoList.length) {
      pagoBody.innerHTML = `<tr><td colspan="6" class="empty-row">Ninguna suscripción coincide con el filtro actual.</td></tr>`;
    } else {
      pagoBody.innerHTML = pagoList.map((q) => {
        const hasVal = q.disponible != null;
        const hasTotal = q.total != null && Number(q.total) > 0;
        const pct = hasVal && hasTotal ? Math.max(0, Math.min(100, (Number(q.disponible) / Number(q.total)) * 100)) : null;
        const saldoTxt = hasVal
          ? `${fmtInt(q.disponible)}${hasTotal ? ` / ${fmtInt(q.total)}` : ""} ${esc(q.unidad)}`
          : `— ${q.unidad ? esc(q.unidad) : ""}`;
        const extBtn = q.url
          ? `<a href="${esc(q.url)}" target="_blank" rel="noopener noreferrer" class="icon-btn" title="Abrir panel de ${esc(q.herramienta)}" aria-label="Abrir ${esc(q.herramienta)}">${ICONS.external}</a>`
          : "";
        return `
          <tr>
            <td>
              <div class="inline-icon-label cell-primary">${iconHtml(q.icon)}<span>${esc(q.herramienta)}</span></div>
              <div class="cell-secondary">${esc(q.cuenta)} · <span class="mono">${esc(q.id)}</span></div>
            </td>
            <td><span class="pill ${pillClassFor(q.tipo)}">${esc(q.tipo)}</span></td>
            <td class="num">
              <div class="cell-primary">${saldoTxt}</div>
              ${pct != null ? `<div class="quota-bar" aria-label="${pct.toFixed(0)}% restante"><div class="quota-bar-fill" style="width:${pct.toFixed(1)}%"></div></div>` : ""}
            </td>
            <td>
              <div>${esc(q.origen)}</div>
              <div class="cell-secondary">${esc(q.corte)} · ${esc(q.renovacion)}</div>
            </td>
            <td>${esc(q.nota)}</td>
            <td class="num">
              <div class="row-actions">
                ${extBtn}
                <button type="button" class="icon-btn" data-edit-quota="${esc(q.id)}" title="Editar saldo o estado" aria-label="Editar ${esc(q.herramienta)}">${ICONS.pencil}</button>
              </div>
            </td>
          </tr>
        `;
      }).join("");
    }

    const gratisBody = document.getElementById("table-cuotas-gratis-body");
    if (!gratisList.length) {
      gratisBody.innerHTML = `<tr><td colspan="5" class="empty-row">Ninguna herramienta gratuita coincide con el filtro actual.</td></tr>`;
    } else {
      gratisBody.innerHTML = gratisList.map((q) => {
        const extBtn = q.url
          ? `<a href="${esc(q.url)}" target="_blank" rel="noopener noreferrer" class="icon-btn" title="Abrir ${esc(q.herramienta)}" aria-label="Abrir ${esc(q.herramienta)}">${ICONS.external}</a>`
          : "";
        return `
          <tr>
            <td>
              <div class="inline-icon-label cell-primary">${iconHtml(q.icon)}<span>${esc(q.herramienta)}</span></div>
              <div class="cell-secondary">${esc(q.cuenta)} · <span class="mono">${esc(q.id)}</span></div>
            </td>
            <td><span class="pill ${pillClassFor(q.tipo)}">${esc(q.tipo)}</span></td>
            <td>${esc(q.unidad)}</td>
            <td>${esc(q.nota)}</td>
            <td class="num">
              <div class="row-actions">
                ${extBtn}
                <button type="button" class="icon-btn" data-edit-quota="${esc(q.id)}" title="Editar herramienta" aria-label="Editar ${esc(q.herramienta)}">${ICONS.pencil}</button>
              </div>
            </td>
          </tr>
        `;
      }).join("");
    }
  }

  function setRoute(route) {
    if (!VALID_ROUTES.includes(route)) route = "overview";
    currentRoute = route;

    document.querySelectorAll(".view").forEach((sec) => {
      sec.hidden = sec.dataset.view !== route;
    });
    document.querySelectorAll(".rail-item[data-route]").forEach((a) => {
      if (a.dataset.route === route) {
        a.setAttribute("aria-current", "page");
      } else {
        a.removeAttribute("aria-current");
      }
    });
    const viewNameEl = document.getElementById("topbar-view-name");
    if (viewNameEl) viewNameEl.textContent = ROUTE_TITLES[route] || "Resumen";

    if (window.location.hash !== `#${route}`) {
      history.replaceState(null, "", `#${route}`);
    }
  }

  function openModal(title, html, onMount) {
    editorTitle.textContent = title;
    editorBody.innerHTML = html;
    editorDialog.showModal();
    if (onMount) onMount();
  }

  function openStationModal(paso) {
    const st = state.estaciones_relevo.find((x) => Number(x.paso) === Number(paso));
    if (!st) return;
    openModal(`${st.codigo} · ${st.nombre}`, `
      <dl class="detail-kv">
        <dt>Herramientas</dt><dd>${renderLogosStrip(st.logos)}</dd>
        <dt>Responsable</dt><dd>${esc(st.responsable)}</dd>
        <dt>Estación</dt><dd>${esc(st.estacion)}</dd>
        <dt>Qué entra</dt><dd>${esc(st.entra)}</dd>
        <dt>Qué entrega</dt><dd>${esc(st.entrega)}</dd>
        <dt>Cuándo suelta</dt><dd>${esc(st.cuando_se_quita)}</dd>
        <dt>Tiempo</dt><dd>${esc(st.tiempo_estimado)}</dd>
        <dt>Estado</dt><dd><span class="pill ${pillClassFor(st.estado)}">${esc(st.estado)}</span></dd>
      </dl>
      <p class="cell-secondary">${esc(st.detalle)}</p>
      <div class="dialog-actions">
        <form method="dialog"><button type="submit" class="btn-primary" value="close" autofocus>Listo</button></form>
      </div>
    `);
  }

  function openEditPubModal(pubId = null) {
    const existing = pubId ? state.publicados.find((p) => p.id === pubId) : null;
    const p = existing || {
      id: `PUB-0${state.publicados.length + 1}`,
      fecha: new Date().toISOString().slice(0, 10),
      titulo: "",
      serie: "¡WATERS! Día",
      canal: "TikTok · FB · IG · YT",
      canales: ["TikTok", "Facebook Reels", "Instagram Reels", "YouTube Shorts"],
      thumb: null,
      vistas: 0,
      retencion_pct: "",
      guardados: "",
      comentarios_cta: "",
      dms_wa: "",
      estado: "En prueba",
      diagnostico: "",
      mejora_siguiente: ""
    };

    const previewHtml = p.thumb
      ? `<div class="modal-preview-row"><img src="${esc(p.thumb)}" alt="${esc(p.titulo)}" class="modal-preview-img"><dl class="detail-kv"><dt>ID</dt><dd class="mono">${esc(p.id)}</dd><dt>Serie</dt><dd>${esc(p.serie)}</dd><dt>Fecha</dt><dd class="num">${esc(p.fecha)}</dd></dl></div>`
      : "";

    openModal(existing ? `Editar métricas · ${p.id}` : "Registrar publicación", `
      ${previewHtml}
      <form id="pub-form">
        <div class="form-grid">
          <div class="form-field full">
            <label for="pf-titulo">Título o episodio</label>
            <input id="pf-titulo" name="titulo" required value="${esc(p.titulo)}" autofocus>
          </div>
          <div class="form-field">
            <label for="pf-fecha">Fecha</label>
            <input id="pf-fecha" name="fecha" type="date" required value="${esc(p.fecha)}">
          </div>
          <div class="form-field">
            <label for="pf-canal">Canal(es)</label>
            <input id="pf-canal" name="canal" required value="${esc(p.canal)}">
          </div>
          <div class="form-field">
            <label for="pf-serie">Serie</label>
            <input id="pf-serie" name="serie" value="${esc(p.serie)}">
          </div>
          <div class="form-field">
            <label for="pf-estado">Veredicto</label>
            <select id="pf-estado" name="estado">
              ${["En prueba", "Adoptado", "Pirita"].map((o) => `<option value="${o}" ${p.estado === o ? "selected" : ""}>${o}</option>`).join("")}
            </select>
          </div>
          <div class="form-field">
            <label for="pf-vistas">Vistas</label>
            <input id="pf-vistas" name="vistas" type="number" min="0" value="${p.vistas == null ? "" : p.vistas}">
          </div>
          <div class="form-field">
            <label for="pf-ret">Retención %</label>
            <input id="pf-ret" name="retencion_pct" type="number" step="0.1" min="0" max="100" value="${p.retencion_pct == null ? "" : p.retencion_pct}">
          </div>
          <div class="form-field">
            <label for="pf-guard">Guardados</label>
            <input id="pf-guard" name="guardados" type="number" min="0" value="${p.guardados == null ? "" : p.guardados}">
          </div>
          <div class="form-field">
            <label for="pf-dms">DMs WhatsApp / CTA</label>
            <input id="pf-dms" name="dms_wa" type="number" min="0" value="${p.dms_wa == null ? "" : p.dms_wa}">
          </div>
          <div class="form-field full">
            <label for="pf-diag">Diagnóstico honesto</label>
            <textarea id="pf-diag" name="diagnostico">${esc(p.diagnostico)}</textarea>
          </div>
          <div class="form-field full">
            <label for="pf-mej">Siguiente iteración</label>
            <textarea id="pf-mej" name="mejora_siguiente">${esc(p.mejora_siguiente)}</textarea>
          </div>
        </div>
        <div class="dialog-actions">
          <button type="button" class="btn-ghost" id="btn-cancel-modal">Cancelar</button>
          <button type="submit" class="btn-primary">Guardar</button>
        </div>
      </form>
    `, () => {
      document.getElementById("btn-cancel-modal").addEventListener("click", () => editorDialog.close("cancel"));
      document.getElementById("pub-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const numOrNull = (val) => (String(val).trim() === "" ? null : Number(val));
        const canalStr = String(fd.get("canal")).trim();
        const updated = {
          id: p.id,
          fecha: fd.get("fecha"),
          titulo: String(fd.get("titulo")).trim(),
          serie: String(fd.get("serie")).trim() || "¡WATERS!",
          canal: canalStr,
          canales: canalStr.split(/[·,]/).map((s) => s.trim()).filter(Boolean),
          thumb: p.thumb,
          vistas: numOrNull(fd.get("vistas")) || 0,
          retencion_pct: numOrNull(fd.get("retencion_pct")),
          guardados: numOrNull(fd.get("guardados")),
          comentarios_cta: p.comentarios_cta,
          dms_wa: numOrNull(fd.get("dms_wa")),
          estado: fd.get("estado"),
          diagnostico: String(fd.get("diagnostico")).trim(),
          mejora_siguiente: String(fd.get("mejora_siguiente")).trim()
        };
        if (existing) {
          Object.assign(existing, updated);
        } else {
          state.publicados.push(updated);
        }
        saveState();
        renderAll();
        editorDialog.close("save");
      });
    });
  }

  function openAddRefModal() {
    openModal("Agregar referencia", `
      <form id="ref-form">
        <div class="form-grid">
          <div class="form-field">
            <label for="rf-fuente">Autor o nombre</label>
            <input id="rf-fuente" name="fuente" required autofocus>
          </div>
          <div class="form-field">
            <label for="rf-plat">Plataforma</label>
            <input id="rf-plat" name="plataforma" required placeholder="Facebook, IG, YouTube, X">
          </div>
          <div class="form-field full">
            <label for="rf-url">Enlace (URL)</label>
            <input id="rf-url" name="url" placeholder="https://...">
          </div>
          <div class="form-field full">
            <label for="rf-muestra">Qué muestra el video</label>
            <textarea id="rf-muestra" name="que_muestra" required></textarea>
          </div>
          <div class="form-field full">
            <label for="rf-obt">Qué extraemos o aplicamos</label>
            <textarea id="rf-obt" name="que_obtuvimos" required></textarea>
          </div>
          <div class="form-field">
            <label for="rf-ver">Veredicto</label>
            <select id="rf-ver" name="veredicto">
              <option value="En prueba">En prueba</option>
              <option value="Adoptado">Adoptado</option>
              <option value="Parcial">Parcial</option>
              <option value="Pirita">Pirita</option>
            </select>
          </div>
          <div class="form-field">
            <label for="rf-donde">Ruta en proyecto</label>
            <input id="rf-donde" name="donde_vive" value="proyectos/waters-serie/referencias/inbox/">
          </div>
        </div>
        <div class="dialog-actions">
          <button type="button" class="btn-ghost" id="btn-cancel-modal">Cancelar</button>
          <button type="submit" class="btn-primary">Guardar</button>
        </div>
      </form>
    `, () => {
      document.getElementById("btn-cancel-modal").addEventListener("click", () => editorDialog.close("cancel"));
      document.getElementById("ref-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const plat = String(fd.get("plataforma")).trim();
        const nextNum = String(state.referencias.length + 1).padStart(2, "0");
        state.referencias.push({
          id: `REF-${nextNum}`,
          fecha: new Date().toISOString().slice(0, 10),
          fuente: String(fd.get("fuente")).trim(),
          plataforma: plat,
          plat_icon: channelIconKey(plat),
          thumb: null,
          url: String(fd.get("url")).trim() || "Local",
          que_muestra: String(fd.get("que_muestra")).trim(),
          que_obtuvimos: String(fd.get("que_obtuvimos")).trim(),
          donde_vive: String(fd.get("donde_vive")).trim(),
          veredicto: fd.get("veredicto"),
          nota: ""
        });
        saveState();
        renderAll();
        editorDialog.close("save");
      });
    });
  }

  function openEditRefNoteModal(refId) {
    const ref = state.referencias.find((r) => r.id === refId);
    if (!ref) return;
    openModal(`Anotar · ${ref.id}`, `
      <form id="ref-note-form">
        <dl class="detail-kv">
          <dt>Fuente</dt><dd>${esc(ref.fuente)} (${esc(ref.plataforma)})</dd>
          <dt>Aprendizaje</dt><dd>${esc(ref.que_obtuvimos)}</dd>
        </dl>
        <div class="form-grid">
          <div class="form-field">
            <label for="rn-ver">Veredicto</label>
            <select id="rn-ver" name="veredicto">
              ${["Adoptado", "Parcial", "En prueba", "Pirita"].map((o) => `<option value="${o}" ${ref.veredicto === o ? "selected" : ""}>${o}</option>`).join("")}
            </select>
          </div>
          <div class="form-field full">
            <label for="rn-nota">Nota o iteración</label>
            <textarea id="rn-nota" name="nota" autofocus>${esc(ref.nota || "")}</textarea>
          </div>
        </div>
        <div class="dialog-actions">
          <button type="button" class="btn-ghost" id="btn-cancel-modal">Cancelar</button>
          <button type="submit" class="btn-primary">Guardar</button>
        </div>
      </form>
    `, () => {
      document.getElementById("btn-cancel-modal").addEventListener("click", () => editorDialog.close("cancel"));
      document.getElementById("ref-note-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        ref.veredicto = fd.get("veredicto");
        ref.nota = String(fd.get("nota")).trim();
        saveState();
        renderAll();
        editorDialog.close("save");
      });
    });
  }

  function openSlotModal(orden) {
    const slot = state.cola_semanal.find((c) => c.orden === orden);
    if (!slot) return;
    openModal(`Slot ${slot.orden} · ${slot.serie}`, `
      <div class="modal-preview-row">
        ${slot.thumb ? `<img src="${esc(slot.thumb)}" alt="${esc(slot.titulo)}" class="modal-preview-img">` : ""}
        <dl class="detail-kv">
          <dt>Título</dt><dd>${esc(slot.titulo)}</dd>
          <dt>Fecha MX</dt><dd class="num">${esc(slot.fecha_mx)}</dd>
          <dt>Archivo cola</dt><dd class="mono">${esc(slot.archivo_cola)}</dd>
          <dt>CTA / PDF</dt><dd>${esc(slot.cta_palabra)}${slot.lead_magnet_pdf ? ` · PDF` : ""}</dd>
        </dl>
      </div>
      <form id="slot-form">
        <div class="form-grid">
          <div class="form-field full">
            <label for="sl-estado">Estado operativo</label>
            <select id="sl-estado" name="estado_slot">
              ${["Listo en disco", "En CapCut Pro", "Programado", "Publicado"].map((o) => `<option value="${o}" ${slot.estado_slot === o ? "selected" : ""}>${o}</option>`).join("")}
            </select>
          </div>
          <div class="form-field full">
            <label for="sl-fb">Feedback, ajustes de CapCut Pro o resultado tras subir</label>
            <textarea id="sl-fb" name="feedback" autofocus>${esc(slot.feedback || "")}</textarea>
          </div>
        </div>
        <div class="dialog-actions">
          <button type="button" class="btn-ghost" id="btn-cancel-modal">Cancelar</button>
          <button type="submit" class="btn-primary">Guardar</button>
        </div>
      </form>
    `, () => {
      document.getElementById("btn-cancel-modal").addEventListener("click", () => editorDialog.close("cancel"));
      document.getElementById("slot-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        slot.feedback = String(fd.get("feedback")).trim();
        updateSlotStatus(slot, fd.get("estado_slot"));
        editorDialog.close("save");
      });
    });
  }

  function openQuotaModal(quotaId = null) {
    const existing = quotaId ? state.cuotas.find((q) => q.id === quotaId) : null;
    const q = existing || {
      id: `CTA-${String(state.cuotas.length + 1).padStart(2, "0")}`,
      herramienta: "",
      cuenta: "Cuenta principal",
      tipo: "Membership",
      icon: "gauge",
      disponible: null,
      total: null,
      unidad: "créditos",
      origen: "Corte manual 08:00",
      corte: new Date().toISOString().slice(0, 10),
      renovacion: "Mensual",
      url: "",
      nota: ""
    };

    openModal(existing ? `Editar cuota · ${q.herramienta}` : "Agregar herramienta o cuota", `
      <form id="quota-form">
        <div class="form-grid">
          <div class="form-field">
            <label for="qf-herr">Herramienta</label>
            <input id="qf-herr" name="herramienta" required value="${esc(q.herramienta)}" autofocus>
          </div>
          <div class="form-field">
            <label for="qf-cuenta">Cuenta / etiqueta (sin contraseñas)</label>
            <input id="qf-cuenta" name="cuenta" required value="${esc(q.cuenta)}">
          </div>
          <div class="form-field">
            <label for="qf-tipo">Tipo de plan</label>
            <select id="qf-tipo" name="tipo">
              ${["Membership", "Free Trial", "Gratis", "Local $0"].map((o) => `<option value="${o}" ${q.tipo === o ? "selected" : ""}>${o}</option>`).join("")}
            </select>
          </div>
          <div class="form-field">
            <label for="qf-unidad">Unidad (ej. chars, min, cr. Flow)</label>
            <input id="qf-unidad" name="unidad" value="${esc(q.unidad)}">
          </div>
          <div class="form-field">
            <label for="qf-disp">Saldo disponible (vacío si ilimitado)</label>
            <input id="qf-disp" name="disponible" type="number" step="any" value="${q.disponible == null ? "" : q.disponible}">
          </div>
          <div class="form-field">
            <label for="qf-total">Límite o total del ciclo</label>
            <input id="qf-total" name="total" type="number" step="any" value="${q.total == null ? "" : q.total}">
          </div>
          <div class="form-field">
            <label for="qf-corte">Fecha de último corte</label>
            <input id="qf-corte" name="corte" value="${esc(q.corte)}">
          </div>
          <div class="form-field">
            <label for="qf-ren">Renovación / vencimiento</label>
            <input id="qf-ren" name="renovacion" value="${esc(q.renovacion)}">
          </div>
          <div class="form-field full">
            <label for="qf-url">URL del panel de suscripción</label>
            <input id="qf-url" name="url" value="${esc(q.url)}" placeholder="https://...">
          </div>
          <div class="form-field full">
            <label for="qf-nota">Notas o recordatorio 08:00 AM</label>
            <textarea id="qf-nota" name="nota">${esc(q.nota)}</textarea>
          </div>
        </div>
        <div class="dialog-actions">
          <button type="button" class="btn-ghost" id="btn-cancel-modal">Cancelar</button>
          <button type="submit" class="btn-primary">Guardar</button>
        </div>
      </form>
    `, () => {
      document.getElementById("btn-cancel-modal").addEventListener("click", () => editorDialog.close("cancel"));
      document.getElementById("quota-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const numOrNull = (val) => (String(val).trim() === "" ? null : Number(val));
        const updated = {
          id: q.id,
          herramienta: String(fd.get("herramienta")).trim(),
          cuenta: String(fd.get("cuenta")).trim(),
          tipo: fd.get("tipo"),
          icon: q.icon || "gauge",
          disponible: numOrNull(fd.get("disponible")),
          total: numOrNull(fd.get("total")),
          unidad: String(fd.get("unidad")).trim(),
          origen: existing ? (q.id === "CTA-01" ? "API / Editado" : "Corte manual") : "Manual",
          corte: String(fd.get("corte")).trim() || new Date().toISOString().slice(0, 10),
          renovacion: String(fd.get("renovacion")).trim(),
          url: String(fd.get("url")).trim(),
          nota: String(fd.get("nota")).trim()
        };
        if (existing) {
          Object.assign(existing, updated);
        } else {
          state.cuotas.push(updated);
        }
        saveState();
        renderAll();
        editorDialog.close("save");
      });
    });
  }

  function updateSlotStatus(slot, newStatus) {
    slot.estado_slot = newStatus;
    if (newStatus === "Publicado") {
      const pubId = `COLA-${slot.orden}`;
      if (!state.publicados.find((p) => p.id === pubId)) {
        state.publicados.push({
          id: pubId,
          fecha: slot.fecha_mx.slice(0, 10),
          titulo: slot.titulo,
          serie: slot.serie,
          canal: slot.canales.join(" · "),
          canales: slot.canales.slice(),
          thumb: slot.thumb,
          vistas: 0,
          retencion_pct: null,
          guardados: null,
          comentarios_cta: null,
          dms_wa: null,
          estado: "En prueba",
          diagnostico: slot.feedback || "Promovido desde cola semanal; pendiente de primer corte a los 7 días.",
          mejora_siguiente: "Registrar vistas y retención tras primeras 72 horas."
        });
      }
    }
    saveState();
    renderAll();
  }

  editorDialog.addEventListener("close", () => {
    editorDialog.returnValue = "";
  });

  if (!("closedBy" in HTMLDialogElement.prototype)) {
    const outside = (e, dlg) => {
      const r = dlg.getBoundingClientRect();
      return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
    };
    let pressedOutside = false;
    editorDialog.addEventListener("pointerdown", (e) => { pressedOutside = outside(e, editorDialog); });
    editorDialog.addEventListener("pointerup", (e) => { if (pressedOutside && outside(e, editorDialog)) editorDialog.close("cancel"); });
  }

  document.addEventListener("click", (e) => {
    const nav = e.target.closest("[data-route]");
    if (nav) {
      e.preventDefault();
      setRoute(nav.dataset.route);
      return;
    }

    const stBtn = e.target.closest("[data-station]");
    if (stBtn) {
      openStationModal(stBtn.dataset.station);
      return;
    }

    const refFilterBtn = e.target.closest("[data-ref-filter]");
    if (refFilterBtn) {
      refFilter = refFilterBtn.dataset.refFilter;
      document.querySelectorAll("[data-ref-filter]").forEach((b) => b.classList.toggle("is-active", b === refFilterBtn));
      renderAll();
      return;
    }

    const colaFilterBtn = e.target.closest("[data-cola-filter]");
    if (colaFilterBtn) {
      colaFilter = colaFilterBtn.dataset.colaFilter;
      document.querySelectorAll("[data-cola-filter]").forEach((b) => b.classList.toggle("is-active", b === colaFilterBtn));
      renderAll();
      return;
    }

    const quotaFilterBtn = e.target.closest("[data-quota-filter]");
    if (quotaFilterBtn) {
      quotaFilter = quotaFilterBtn.dataset.quotaFilter;
      document.querySelectorAll("[data-quota-filter]").forEach((b) => b.classList.toggle("is-active", b === quotaFilterBtn));
      renderAll();
      return;
    }

    const editPub = e.target.closest("[data-edit-pub]");
    if (editPub) {
      openEditPubModal(editPub.dataset.editPub);
      return;
    }

    const editRef = e.target.closest("[data-edit-ref]");
    if (editRef) {
      openEditRefNoteModal(editRef.dataset.editRef);
      return;
    }

    const editSlot = e.target.closest("[data-edit-slot]");
    if (editSlot) {
      openSlotModal(editSlot.dataset.editSlot);
      return;
    }

    const editQuota = e.target.closest("[data-edit-quota]");
    if (editQuota) {
      openQuotaModal(editQuota.dataset.editQuota);
    }
  });

  document.addEventListener("change", (e) => {
    const sel = e.target.closest("[data-slot-status]");
    if (sel) {
      const slot = state.cola_semanal.find((c) => c.orden === sel.dataset.slotStatus);
      if (slot) updateSlotStatus(slot, sel.value);
      return;
    }

    const chk = e.target.closest("[data-toggle-mejora]");
    if (chk) {
      const mj = state.mejoras_activas.find((x) => x.id === chk.dataset.toggleMejora);
      if (mj) {
        mj.aplicada = chk.checked;
        saveState();
      }
    }
  });

  document.getElementById("btn-theme-toggle").addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "dark";
    applyTheme(cur === "dark" ? "light" : "dark");
    renderAll();
  });

  document.getElementById("btn-open-add-pub-overview").addEventListener("click", () => openEditPubModal(null));
  document.getElementById("btn-open-add-pub").addEventListener("click", () => openEditPubModal(null));
  document.getElementById("btn-open-add-ref").addEventListener("click", () => openAddRefModal());
  document.getElementById("btn-open-add-quota").addEventListener("click", () => openQuotaModal(null));

  document.getElementById("global-search").addEventListener("input", (e) => {
    searchQuery = e.target.value.trim();
    renderAll();
  });

  document.getElementById("btn-export-json").addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `tablero_control_snapshot_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  });

  document.getElementById("input-import-json").addEventListener("change", (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const parsed = JSON.parse(String(reader.result));
        if (parsed && parsed.meta && parsed.referencias && parsed.cola_semanal) {
          state = parsed;
          saveState("Importado");
          renderAll();
        }
      } catch (_) {}
    };
    reader.readAsText(file);
    e.target.value = "";
  });

  document.getElementById("btn-reset-data").addEventListener("click", () => {
    localStorage.removeItem(STORAGE_KEY);
    state = clone(window.CAPTOORA_DATA);
    saveState("Restaurado");
    renderAll();
  });

  window.addEventListener("hashchange", () => {
    const h = window.location.hash.replace("#", "");
    if (VALID_ROUTES.includes(h)) setRoute(h);
  });

  initTheme();
  hydrateStaticIcons();
  const initialHash = window.location.hash.replace("#", "");
  setRoute(VALID_ROUTES.includes(initialHash) ? initialHash : "overview");
  renderAll();
})();
