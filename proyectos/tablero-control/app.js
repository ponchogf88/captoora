/* Captoora Control — Lógica interactiva, persistencia local y reconciliación en vivo */
(() => {
  const STORAGE_KEY = "captoora_control_state_v1";
  const VALID_ROUTES = ["overview", "flujo", "referencias", "publicados", "cola"];

  const clone = (v) => JSON.parse(JSON.stringify(v));
  const esc = (v) => String(v == null ? "" : v).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const fmtInt = (n) => new Intl.NumberFormat("es-MX").format(Math.round(n));
  const fmtPct = (v) => (v == null || v === "" ? "—" : `${Number(v).toFixed(1)}%`);

  function loadState() {
    const base = clone(window.CAPTOORA_DATA);
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed && parsed.schema_version === base.schema_version) {
          return parsed;
        }
      }
    } catch (_) {}
    return base;
  }

  let state = loadState();
  let currentRoute = "overview";
  let refFilter = "all";
  let colaFilter = "all";
  let searchQuery = "";

  const editorDialog = document.getElementById("editor-dialog");
  const editorTitle = document.getElementById("editor-title");
  const editorBody = document.getElementById("editor-body");
  const drawerDialog = document.getElementById("drawer-dialog");

  function saveState(stampText = "Guardado local actualizado") {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      const el = document.getElementById("save-indicator");
      if (el) el.textContent = stampText;
    } catch (_) {}
  }

  function pillClassFor(label) {
    const v = String(label || "").toLowerCase();
    if (v.includes("adopt") || v.includes("activo") || v.includes("publicado") || v.includes("lista hoy")) return "pill-positive";
    if (v.includes("turno")) return "pill-accent";
    if (v.includes("parcial") || v.includes("prueba") || v.includes("capcut") || v.includes("programado") || v.includes("fase 2") || v.includes("siguiente")) return "pill-warning";
    if (v.includes("pirita") || v.includes("reemplazado")) return "pill-negative";
    return "pill-neutral";
  }

  /* Data reconciliation & assertions (every total computed from rows) */
  function computeMetrics() {
    const pubs = state.publicados;
    const refs = state.referencias;
    const cola = state.cola_semanal;
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

    console.assert(
      refCounts.Adoptado + refCounts.Parcial + refCounts["En prueba"] + refCounts.Pirita === refCounts.all,
      "Reconciliación: suma de veredictos debe igualar total de referencias"
    );
    console.assert(
      colaCounts["Listo en disco"] + colaCounts["En CapCut Pro"] + colaCounts.Programado + colaCounts.Publicado === colaCounts.all,
      "Reconciliación: suma de estados de cola debe igualar total de slots"
    );

    const quotaPct = (meta.cuota_elevenlabs.disponible / meta.cuota_elevenlabs.total) * 100;
    return {
      totalPub,
      target,
      pctGoal,
      totalViews,
      avgViews,
      refCounts,
      colaCounts,
      colaPendientes,
      quotaPct
    };
  }

  function renderAll() {
    const m = computeMetrics();

    /* Header & Sidebar live counters */
    document.getElementById("nav-cola-count").textContent = String(m.colaPendientes);
    document.getElementById("topbar-goal-pill").textContent = `${m.totalPub} de ${m.target} publicados`;
    document.getElementById("topbar-freshness").textContent = `Corte ${state.meta.fecha_corte}`;

    /* Overview KPIs & headline finding */
    const faltan = Math.max(0, m.target - m.totalPub);
    const conCola = Math.min(m.target, m.totalPub + m.colaPendientes);
    document.getElementById("overview-finding").textContent =
      `Llevas ${m.totalPub} de ${m.target} videos publicados (${m.pctGoal.toFixed(1)}%). Tienes ${m.colaPendientes} pendientes en cola para llegar a ${conCola} de ${m.target} esta semana.`;

    document.getElementById("kpi-published").innerHTML = `${fmtInt(m.totalPub)} <span class="kpi-unit">/ ${m.target}</span>`;
    document.getElementById("kpi-published-note").textContent = `${m.pctGoal.toFixed(1)}% · +${m.colaPendientes} listos en cola`;
    document.getElementById("kpi-views").textContent = fmtInt(m.totalViews);
    document.getElementById("kpi-views-note").textContent = `Prom. ${fmtInt(m.avgViews)} por video · ${m.totalPub} registros`;
    document.getElementById("kpi-refs").textContent = fmtInt(m.refCounts.all);
    document.getElementById("kpi-refs-note").textContent = `${m.refCounts.Adoptado} adoptadas · ${m.refCounts.Parcial} parciales · ${m.refCounts["En prueba"]} en prueba`;
    document.getElementById("kpi-quota").innerHTML = `${fmtInt(state.meta.cuota_elevenlabs.disponible)} <span class="kpi-unit">chars</span>`;
    document.getElementById("kpi-quota-note").textContent = `${m.quotaPct.toFixed(1)}% de ${fmtInt(state.meta.cuota_elevenlabs.total)} disponibles`;

    renderRelayTrack();
    renderOverviewCharts(m);
    renderRoadmap();
    renderFlujoTables();
    renderReferencias(m);
    renderPublicados();
    renderCola(m);
    syncMobileDrawerNav();
  }

  function renderRelayTrack() {
    const container = document.getElementById("relay-track");
    container.innerHTML = state.estaciones_relevo.map((st) => {
      const isCurrent = st.estado.toLowerCase().includes("turno");
      return `
        <button type="button" class="relay-node ${isCurrent ? "is-current" : ""}" data-station="${st.paso}">
          <div class="relay-top">
            <span class="relay-code">${esc(st.codigo)}</span>
            <span class="pill ${pillClassFor(st.estado)}">${esc(st.estado)}</span>
          </div>
          <div class="relay-title">${esc(st.paso)}. ${esc(st.nombre)}</div>
          <div class="relay-owner">${esc(st.responsable)}</div>
          <div class="relay-output">${esc(st.entrega)}</div>
        </button>
      `;
    }).join("");
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
        height: 184,
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
        <span><span class="legend-swatch" style="background:#8fbac4"></span>En cola semanal: <strong class="num">${m.colaPendientes}</strong></span>
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
        <div class="roadmap-meta">${esc(h.ventana)} · Meta: ${esc(h.resultado_esperado)}</div>
        <p class="roadmap-desc">${esc(h.detalle)}</p>
      </li>
    `).join("");
  }

  function renderFlujoTables() {
    document.getElementById("hardware-line").textContent =
      `${state.meta.hardware_principal} + ${state.meta.estacion_movil}`;

    document.getElementById("table-estaciones-body").innerHTML = state.estaciones_relevo.map((st) => `
      <tr>
        <td class="mono">${esc(st.codigo)}</td>
        <td>
          <div class="cell-primary">${esc(st.nombre)}</div>
          <div class="cell-secondary">${esc(st.responsable)}</div>
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
        <td class="cell-primary">${esc(b.herramienta)}</td>
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
        ? `<a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer" class="cell-link">${esc(r.fuente)}</a>`
        : `<span class="cell-primary">${esc(r.fuente)}</span>`;
      return `
        <tr>
          <td class="mono">${esc(r.id)}</td>
          <td class="num">${esc(r.fecha)}</td>
          <td>
            ${sourceLink}
            <div class="cell-secondary">${esc(r.plataforma)}</div>
          </td>
          <td>${esc(r.que_muestra)}</td>
          <td>
            <div>${esc(r.que_obtuvimos)}</div>
            <div class="cell-secondary mono">${esc(r.donde_vive)}</div>
            ${r.nota ? `<div class="cell-secondary"><strong>Nota:</strong> ${esc(r.nota)}</div>` : ""}
          </td>
          <td><span class="pill ${pillClassFor(r.veredicto)}">${esc(r.veredicto)}</span></td>
          <td class="num">
            <button type="button" class="btn-ghost btn-sm" data-edit-ref="${esc(r.id)}">Anotar</button>
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
      tbody.innerHTML = filtered.map((p) => `
        <tr>
          <td>
            <div class="cell-primary"><span class="mono">${esc(p.id)}</span> · ${esc(p.titulo)}</div>
            <div class="cell-secondary">${esc(p.fecha)} · ${esc(p.serie)}</div>
            <div class="cell-secondary">${esc(p.diagnostico)}</div>
            <div class="cell-secondary"><strong>Siguiente iteración:</strong> ${esc(p.mejora_siguiente)}</div>
          </td>
          <td>${esc(p.canal)}</td>
          <td class="num">${p.vistas == null ? "—" : fmtInt(p.vistas)}</td>
          <td class="num">${fmtPct(p.retencion_pct)}</td>
          <td class="num">${p.guardados == null ? "—" : fmtInt(p.guardados)}</td>
          <td class="num">${p.dms_wa == null ? "—" : fmtInt(p.dms_wa)}</td>
          <td><span class="pill ${pillClassFor(p.estado)}">${esc(p.estado)}</span></td>
          <td class="num">
            <button type="button" class="btn-ghost btn-sm" data-edit-pub="${esc(p.id)}">Editar</button>
          </td>
        </tr>
      `).join("");
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
      tbody.innerHTML = `<tr><td colspan="7" class="empty-row">Ningún video de la cola coincide con el filtro actual.</td></tr>`;
      return;
    }

    const opts = ["Listo en disco", "En CapCut Pro", "Programado", "Publicado"];
    tbody.innerHTML = filtered.map((c) => `
      <tr>
        <td class="mono num">${esc(c.orden)}</td>
        <td class="num">${esc(c.fecha_mx)}</td>
        <td>
          <div class="cell-primary">${esc(c.titulo)}</div>
          <div class="cell-secondary">${esc(c.serie)} · <span class="mono">${esc(c.archivo_cola)}</span></div>
          ${c.feedback ? `<div class="cell-secondary"><strong>Feedback:</strong> ${esc(c.feedback)}</div>` : ""}
        </td>
        <td>
          <div>${esc(c.formato)}</div>
          <div class="cell-secondary">${esc(c.canales.join(" · "))}</div>
        </td>
        <td>
          <div class="mono">${esc(c.cta_palabra)}</div>
          <div class="cell-secondary">${c.lead_magnet_pdf ? "Incluye guía PDF" : "Sin PDF"}</div>
        </td>
        <td>
          <select class="inline-select" data-slot-status="${esc(c.orden)}" aria-label="Estado de slot ${esc(c.orden)}">
            ${opts.map((o) => `<option value="${esc(o)}" ${c.estado_slot === o ? "selected" : ""}>${esc(o)}</option>`).join("")}
          </select>
        </td>
        <td class="num">
          <button type="button" class="btn-ghost btn-sm" data-edit-slot="${esc(c.orden)}">Revisar</button>
        </td>
      </tr>
    `).join("");
  }

  /* Routing */
  function setRoute(route) {
    if (!VALID_ROUTES.includes(route)) route = "overview";
    currentRoute = route;

    document.querySelectorAll(".view").forEach((sec) => {
      sec.hidden = sec.dataset.view !== route;
    });
    document.querySelectorAll(".nav-item[data-route]").forEach((a) => {
      if (a.dataset.route === route) {
        a.setAttribute("aria-current", "page");
      } else {
        a.removeAttribute("aria-current");
      }
    });
    if (window.location.hash !== `#${route}`) {
      history.replaceState(null, "", `#${route}`);
    }
    syncMobileDrawerNav();
  }

  function syncMobileDrawerNav() {
    const drawerList = document.getElementById("drawer-nav-list");
    if (!drawerList) return;
    const labels = [
      ["overview", "Resumen"],
      ["flujo", "Flujo y relevos"],
      ["referencias", "Referencias"],
      ["publicados", "Publicados"],
      ["cola", "Cola semanal"]
    ];
    drawerList.innerHTML = labels.map(([id, text]) => `
      <a href="#${id}" class="nav-item" data-drawer-route="${id}" ${currentRoute === id ? 'aria-current="page"' : ""}>${esc(text)}</a>
    `).join("");
  }

  /* Native <dialog> Modals */
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
        <dt>Responsable</dt><dd>${esc(st.responsable)}</dd>
        <dt>Estación física</dt><dd>${esc(st.estacion)}</dd>
        <dt>Qué entra</dt><dd>${esc(st.entra)}</dd>
        <dt>Qué entrega</dt><dd>${esc(st.entrega)}</dd>
        <dt>Cuándo se quita</dt><dd>${esc(st.cuando_se_quita)}</dd>
        <dt>Tiempo estimado</dt><dd>${esc(st.tiempo_estimado)}</dd>
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
      vistas: 0,
      retencion_pct: "",
      guardados: "",
      comentarios_cta: "",
      dms_wa: "",
      estado: "En prueba",
      diagnostico: "",
      mejora_siguiente: ""
    };

    openModal(existing ? `Editar métricas · ${p.id}` : "Registrar nueva publicación", `
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
            <label for="pf-ret">Retención % (vacío si no medido)</label>
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
            <label for="pf-diag">Diagnóstico honesto (qué pasó)</label>
            <textarea id="pf-diag" name="diagnostico">${esc(p.diagnostico)}</textarea>
          </div>
          <div class="form-field full">
            <label for="pf-mej">Qué cambiamos en la siguiente iteración</label>
            <textarea id="pf-mej" name="mejora_siguiente">${esc(p.mejora_siguiente)}</textarea>
          </div>
        </div>
        <div class="dialog-actions">
          <button type="button" class="btn-ghost" id="btn-cancel-modal">Cancelar</button>
          <button type="submit" class="btn-primary">Guardar registro</button>
        </div>
      </form>
    `, () => {
      document.getElementById("btn-cancel-modal").addEventListener("click", () => editorDialog.close("cancel"));
      document.getElementById("pub-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const numOrNull = (val) => (String(val).trim() === "" ? null : Number(val));
        const updated = {
          id: p.id,
          fecha: fd.get("fecha"),
          titulo: String(fd.get("titulo")).trim(),
          serie: String(fd.get("serie")).trim() || "¡WATERS!",
          canal: String(fd.get("canal")).trim(),
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
    openModal("Agregar referencia nueva", `
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
            <label for="rf-obt">Qué extraemos o aplicamos en Captoora</label>
            <textarea id="rf-obt" name="que_obtuvimos" required></textarea>
          </div>
          <div class="form-field">
            <label for="rf-ver">Veredicto inicial</label>
            <select id="rf-ver" name="veredicto">
              <option value="En prueba">En prueba</option>
              <option value="Adoptado">Adoptado</option>
              <option value="Parcial">Parcial</option>
              <option value="Pirita">Pirita</option>
            </select>
          </div>
          <div class="form-field">
            <label for="rf-donde">Dónde vive en el proyecto</label>
            <input id="rf-donde" name="donde_vive" value="proyectos/waters-serie/referencias/inbox/">
          </div>
        </div>
        <div class="dialog-actions">
          <button type="button" class="btn-ghost" id="btn-cancel-modal">Cancelar</button>
          <button type="submit" class="btn-primary">Guardar referencia</button>
        </div>
      </form>
    `, () => {
      document.getElementById("btn-cancel-modal").addEventListener("click", () => editorDialog.close("cancel"));
      document.getElementById("ref-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const nextNum = String(state.referencias.length + 1).padStart(2, "0");
        state.referencias.push({
          id: `REF-${nextNum}`,
          fecha: new Date().toISOString().slice(0, 10),
          fuente: String(fd.get("fuente")).trim(),
          plataforma: String(fd.get("plataforma")).trim(),
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
    openModal(`Anotar referencia · ${ref.id}`, `
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
            <label for="rn-nota">Nota de revisión o iteración</label>
            <textarea id="rn-nota" name="nota" autofocus>${esc(ref.nota || "")}</textarea>
          </div>
        </div>
        <div class="dialog-actions">
          <button type="button" class="btn-ghost" id="btn-cancel-modal">Cancelar</button>
          <button type="submit" class="btn-primary">Guardar nota</button>
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
    openModal(`Revisión Slot ${slot.orden} · ${slot.serie}`, `
      <form id="slot-form">
        <dl class="detail-kv">
          <dt>Título</dt><dd>${esc(slot.titulo)}</dd>
          <dt>Programado MX</dt><dd>${esc(slot.fecha_mx)}</dd>
          <dt>Archivo cola</dt><dd class="mono">${esc(slot.archivo_cola)}</dd>
          <dt>Fuente MP4</dt><dd class="mono">${esc(slot.source_mp4)}</dd>
          <dt>CTA / Guía</dt><dd>${esc(slot.cta_palabra)}${slot.lead_magnet_pdf ? ` · ${esc(slot.lead_magnet_pdf)}` : ""}</dd>
        </dl>
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
          <button type="submit" class="btn-primary">Guardar revisión</button>
        </div>
      </form>
    `, () => {
      document.getElementById("btn-cancel-modal").addEventListener("click", () => editorDialog.close("cancel"));
      document.getElementById("slot-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const newStatus = fd.get("estado_slot");
        slot.feedback = String(fd.get("feedback")).trim();
        updateSlotStatus(slot, newStatus);
        editorDialog.close("save");
      });
    });
  }

  function updateSlotStatus(slot, newStatus) {
    slot.estado_slot = newStatus;
    if (newStatus === "Publicado") {
      const pubId = `COLA-${slot.orden}`;
      const already = state.publicados.find((p) => p.id === pubId);
      if (!already) {
        state.publicados.push({
          id: pubId,
          fecha: slot.fecha_mx.slice(0, 10),
          titulo: slot.titulo,
          serie: slot.serie,
          canal: slot.canales.join(" · "),
          vistas: 0,
          retencion_pct: null,
          guardados: null,
          comentarios_cta: null,
          dms_wa: null,
          estado: "En prueba",
          diagnostico: slot.feedback || "Recién promovido desde cola semanal; pendiente de primer corte a los 7 días.",
          mejora_siguiente: "Registrar vistas y retención tras las primeras 72 horas."
        });
      }
    }
    saveState();
    renderAll();
  }

  /* Dialog close reset + Safari light-dismiss fallback (per modern-web-guidance) */
  [editorDialog, drawerDialog].forEach((dlg) => {
    dlg.addEventListener("close", () => {
      dlg.returnValue = "";
    });
  });

  if (!("closedBy" in HTMLDialogElement.prototype)) {
    const outside = (e, dlg) => {
      const r = dlg.getBoundingClientRect();
      return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
    };
    [editorDialog, drawerDialog].forEach((dlg) => {
      let pressedOutside = false;
      dlg.addEventListener("pointerdown", (e) => { pressedOutside = outside(e, dlg); });
      dlg.addEventListener("pointerup", (e) => { if (pressedOutside && outside(e, dlg)) dlg.close("cancel"); });
    });
  }

  /* Event Delegation */
  document.addEventListener("click", (e) => {
    const nav = e.target.closest("[data-route]");
    if (nav) {
      e.preventDefault();
      setRoute(nav.dataset.route);
      return;
    }

    const drawerNav = e.target.closest("[data-drawer-route]");
    if (drawerNav) {
      e.preventDefault();
      drawerDialog.close("navigate");
      setRoute(drawerNav.dataset.drawerRoute);
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

  document.getElementById("btn-open-drawer").addEventListener("click", () => drawerDialog.showModal());
  document.getElementById("btn-open-add-pub-overview").addEventListener("click", () => openEditPubModal(null));
  document.getElementById("btn-open-add-pub").addEventListener("click", () => openEditPubModal(null));
  document.getElementById("btn-open-add-ref").addEventListener("click", () => openAddRefModal());

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
          saveState("Respaldo JSON importado");
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
    saveState("Base restaurada al corte oficial");
    renderAll();
  });

  window.addEventListener("hashchange", () => {
    const h = window.location.hash.replace("#", "");
    if (VALID_ROUTES.includes(h)) setRoute(h);
  });

  const initialHash = window.location.hash.replace("#", "");
  setRoute(VALID_ROUTES.includes(initialHash) ? initialHash : "overview");
  renderAll();
})();
