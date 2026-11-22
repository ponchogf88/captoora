/* ==========================================================================
   CAPTOORA GROWTH COMMAND & MONTERREY GEO-RADAR (PHASE 4)
   - Zero-neon Liquid Glass UI (#08090c, Champagne #c5a880, Sage #6e9477)
   - Interactive Monterrey & SPGG 141-Pin Map + TSP Multi-Stop Route Optimizer
   - PFAE 612 Accountant (RFC GUFJ870801NA6) + $0 Debt Self-Funded Ads Gate
   - 7+1 Executive Growth Engines + 24/7 Scheduler + WA Web 1-Click Supervisor
   ========================================================================== */

(function () {
  'use strict';

  const API_BASE = window.location.protocol.startsWith('http')
    ? window.location.origin
    : 'http://127.0.0.1:8765';

  const cmdState = {
    geo: null,
    growth: null,
    statusFilter: 'all',
    categoryFilter: 'all',
    searchQuery: '',
    selectedSlugs: [],
    optimizedRoute: null,
    originMode: 'base',
    customOrigin: null,
    leafletMap: null,
    pinsLayer: null,
    routeLayer: null,
    mapInitialized: false,
    lastClipFilter: 'all',
    activeSubSection: 'all',
  };

  function toast(msg) {
    if (typeof window.captooraShowToast === 'function') {
      window.captooraShowToast(msg);
      return;
    }
    const el = document.getElementById('captooraToast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('visible');
    clearTimeout(el._hideTimer);
    el._hideTimer = setTimeout(() => el.classList.remove('visible'), 3600);
  }

  function esc(val) {
    return String(val ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function money(n) {
    const num = Number(n || 0);
    return '$' + num.toLocaleString('es-MX', { minimumFractionDigits: 0, maximumFractionDigits: 2 }) + ' MXN';
  }

  async function apiJson(path, options = {}) {
    const res = await fetch(`${API_BASE}${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.detail || `HTTP ${res.status}`);
    }
    return data;
  }

  function copyText(text, okMsg = 'Copiado al portapapeles.') {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(String(text || '')).then(() => toast(okMsg)).catch(() => {
        toast('Selecciona y copia el texto manualmente.');
      });
    } else {
      toast('Copia manual requerida en este navegador.');
    }
  }

  function statusColor(campaignStatus) {
    if (campaignStatus === 'atacado_aprobado') return '#6e9477';
    if (campaignStatus === 'en_cola_pendiente') return '#c5a880';
    if (campaignStatus === 'dolor_critico_sin_atacar') return '#b86259';
    return '#888d9e';
  }

  function statusBadgeStyle(campaignStatus) {
    if (campaignStatus === 'atacado_aprobado') {
      return 'background: rgba(110,148,119,0.16); color:#c2dec8; border:1px solid rgba(110,148,119,0.45);';
    }
    if (campaignStatus === 'en_cola_pendiente') {
      return 'background: rgba(197,168,128,0.16); color:#dfcbb5; border:1px solid rgba(197,168,128,0.45);';
    }
    if (campaignStatus === 'dolor_critico_sin_atacar') {
      return 'background: rgba(184,98,89,0.16); color:#e8b3ad; border:1px solid rgba(184,98,89,0.48);';
    }
    return 'background: rgba(136,141,158,0.14); color:#d2d5de; border:1px solid rgba(255,255,255,0.12);';
  }

  function precisionBadge(precision) {
    if (precision === 'apify_exact') return 'GPS Exacto (Apify)';
    if (precision === 'osm_geocoded') return 'OSM Geocodificado';
    return 'Centroide Zona';
  }

  function resolveDocHref(relPath) {
    if (!relPath) return '#';
    const clean = String(relPath).replace(/^\/+/, '');
    if (window.location.protocol.startsWith('http')) return '/' + clean;
    return '../' + clean;
  }

  // ==========================================================================
  // DATA LOADERS (GEO + GROWTH SUITE)
  // ==========================================================================
  window.loadGeoAndGrowthData = async function (silent = true) {
    try {
      const [geoRes, growthRes] = await Promise.all([
        apiJson('/api/geo/leads'),
        apiJson('/api/growth/state'),
      ]);
      cmdState.geo = geoRes;
      cmdState.growth = growthRes;
      renderGeoCommandTab();
      renderExecutiveGrowthTab();
      if (!silent) toast('Radar MTY (141 pines) y Centro Ejecutivo sincronizados.');
      return true;
    } catch (err) {
      if (!silent) toast('No se pudo conectar con :8765 (' + err.message + ')');
      return false;
    }
  };

  // ==========================================================================
  // TAB 1: MONTERREY & SPGG PIN MAP + TSP ROUTE OPTIMIZER
  // ==========================================================================
  function getFilteredPins() {
    const pins = (cmdState.geo && cmdState.geo.pins) || [];
    const q = (cmdState.searchQuery || '').trim().toLowerCase();
    return pins.filter((p) => {
      if (cmdState.statusFilter !== 'all' && p.campaign_status !== cmdState.statusFilter) return false;
      if (cmdState.categoryFilter !== 'all' && p.map_category !== cmdState.categoryFilter) return false;
      if (q) {
        const hay = `${p.nombre} ${p.nicho} ${p.map_category} ${p.municipio} ${p.zona} ${p.direccion}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }

  function ensureLeafletMap() {
    const container = document.getElementById('mtyGeoLeafletMap');
    if (!container || !window.L) return null;

    if (!cmdState.leafletMap) {
      const base = (cmdState.geo && cmdState.geo.base) || { lat: 25.6788, lng: -100.3694, name: 'Captoora Base Operativa' };
      const map = L.map(container, {
        center: [base.lat, base.lng],
        zoom: 12,
        zoomControl: true,
        preferCanvas: true,
      });

      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19,
      }).addTo(map);

      cmdState.pinsLayer = L.layerGroup().addTo(map);
      cmdState.routeLayer = L.layerGroup().addTo(map);
      cmdState.leafletMap = map;
      cmdState.mapInitialized = true;
    }

    return cmdState.leafletMap;
  }

  function renderLeafletMarkers(filteredPins) {
    const map = ensureLeafletMap();
    if (!map || !cmdState.pinsLayer || !cmdState.routeLayer) return;

    cmdState.pinsLayer.clearLayers();
    cmdState.routeLayer.clearLayers();

    const base = (cmdState.geo && cmdState.geo.base) || { lat: 25.6788, lng: -100.3694, name: 'Base Operativa', address: '' };
    const baseIcon = L.divIcon({
      className: 'captoora-base-marker',
      html: `<div style="width:26px;height:26px;border-radius:999px;background:#08090c;border:2px solid #c5a880;color:#c5a880;display:flex;align-items:center;justify-content:center;font-size:13px;box-shadow:0 0 14px rgba(197,168,128,0.45);">★</div>`,
      iconSize: [26, 26],
      iconAnchor: [13, 13],
    });
    L.marker([base.lat, base.lng], { icon: baseIcon })
      .bindPopup(`
        <div style="font-family:Plus Jakarta Sans,sans-serif;color:#f5f4ef;min-width:210px;">
          <div style="font-size:10px;letter-spacing:1.4px;color:#c5a880;text-transform:uppercase;">Origen de Rutas</div>
          <div style="font-size:13px;font-weight:500;margin:4px 0;">${esc(base.name)}</div>
          <div style="font-size:11px;color:#888d9e;">${esc(base.address || 'San Jerónimo, Monterrey')}</div>
        </div>
      `)
      .addTo(cmdState.pinsLayer);

    const selectedSet = new Set(cmdState.selectedSlugs);
    filteredPins.forEach((pin) => {
      const inRoute = selectedSet.has(pin.slug);
      const color = statusColor(pin.campaign_status);
      const marker = L.circleMarker([pin.lat, pin.lng], {
        radius: inRoute ? 8.5 : 6.2,
        color: inRoute ? '#f5f4ef' : '#08090c',
        weight: inRoute ? 2.2 : 1.3,
        fillColor: color,
        fillOpacity: 0.92,
      });

      const flagsHtml = (pin.audit_flags || [])
        .slice(0, 3)
        .map((f) => `<span style="display:inline-block;padding:2px 6px;border-radius:4px;font-size:10px;background:rgba(184,98,89,0.2);color:#e8b3ad;margin:2px 4px 2px 0;">${esc(f)}</span>`)
        .join('');

      const phoneDigits = String(pin.telefono || '').replace(/\D+/g, '');
      const waMsg = encodeURIComponent(
        `Hola equipo de ${pin.nombre}, soy Jesús Gutiérrez de Captoora Studio (https://captoora.studio/sports). Preparamos su análisis visual y producción 1/2000s en sitio para proyectar su marca en 2027. ¿Te lo comparto?`
      );
      const waLink = phoneDigits ? `https://web.whatsapp.com/send?phone=${phoneDigits.length === 10 ? '52' + phoneDigits : phoneDigits}&text=${waMsg}` : '';

      const popupHtml = `
        <div style="font-family:Plus Jakarta Sans,sans-serif;color:#f5f4ef;min-width:245px;max-width:290px;">
          <div style="display:flex;justify-content:space-between;gap:6px;align-items:center;margin-bottom:4px;">
            <span style="font-size:10px;padding:2px 7px;border-radius:99px;${statusBadgeStyle(pin.campaign_status)}">${esc(pin.status_label)}</span>
            <span style="font-size:10px;color:#888d9e;">${pin.distance_from_base_km} km</span>
          </div>
          <div style="font-size:13.5px;font-weight:500;color:#f5f4ef;margin-bottom:2px;">${esc(pin.nombre)}</div>
          <div style="font-size:11px;color:#c5a880;margin-bottom:4px;">${esc(pin.map_category)} · ${esc(pin.municipio)}</div>
          <div style="font-size:11px;color:#abb0c0;margin-bottom:6px;">${esc(pin.direccion || 'Monterrey / SPGG')}</div>
          <div style="font-size:10.5px;color:#888d9e;margin-bottom:6px;">
            ${pin.rating ? `★ ${pin.rating} (${pin.resenas || 0} reseñas) · ` : ''}${esc(precisionBadge(pin.geo_precision))} · CRM: <strong style="color:#dfcbb5;">${esc(pin.crm_stage)}</strong>
          </div>
          ${flagsHtml ? `<div style="margin-bottom:8px;">${flagsHtml}</div>` : ''}
          <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">
            <button type="button" onclick="window.toggleRouteSlug('${esc(pin.slug)}')"
              style="cursor:pointer;padding:5px 9px;border-radius:6px;border:1px solid #c5a880;background:rgba(197,168,128,0.16);color:#f5f4ef;font-size:11px;">
              ${inRoute ? 'Quitar de Ruta' : '+ Agregar a Ruta'}
            </button>
            ${waLink ? `<a href="${waLink}" target="_blank" rel="noopener" style="padding:5px 9px;border-radius:6px;border:1px solid rgba(110,148,119,0.5);background:rgba(110,148,119,0.16);color:#c2dec8;font-size:11px;text-decoration:none;">WA Web</a>` : ''}
            ${pin.gmaps_url ? `<a href="${esc(pin.gmaps_url)}" target="_blank" rel="noopener" style="padding:5px 9px;border-radius:6px;border:1px solid rgba(255,255,255,0.18);color:#d2d5de;font-size:11px;text-decoration:none;">Maps</a>` : ''}
            <a href="${esc(resolveDocHref(pin.dossier_pdf_path))}" target="_blank" rel="noopener" style="padding:5px 9px;border-radius:6px;border:1px solid rgba(255,255,255,0.18);color:#d2d5de;font-size:11px;text-decoration:none;">PDF</a>
          </div>
        </div>
      `;

      marker.bindPopup(popupHtml, { maxWidth: 310 });
      marker.addTo(cmdState.pinsLayer);
    });

    // Draw optimized route polyline & numbered stop pins if calculated
    const opt = cmdState.optimizedRoute;
    if (opt && Array.isArray(opt.stops) && opt.stops.length > 0) {
      const coords = [[opt.origin.lat, opt.origin.lng], ...opt.stops.map((s) => [s.lat, s.lng])];
      L.polyline(coords, {
        color: '#c5a880',
        weight: 3,
        opacity: 0.9,
        dashArray: '7, 6',
      }).addTo(cmdState.routeLayer);

      opt.stops.forEach((s) => {
        const stopIcon = L.divIcon({
          className: 'captoora-stop-num',
          html: `<div style="width:22px;height:22px;border-radius:999px;background:#c5a880;color:#08090c;font-weight:600;font-size:11px;display:flex;align-items:center;justify-content:center;border:2px solid #08090c;">${s.stop_number}</div>`,
          iconSize: [22, 22],
          iconAnchor: [11, 11],
        });
        L.marker([s.lat, s.lng], { icon: stopIcon })
          .bindTooltip(`#${s.stop_number} · ${s.nombre} (+${s.leg_distance_km} km)`, { direction: 'top' })
          .addTo(cmdState.routeLayer);
      });
    }
  }

  function renderGeoCommandTab() {
    const geo = cmdState.geo;
    if (!geo) return;

    const sc = geo.status_counts || {};
    const pc = geo.precision_counts || {};
    const filtered = getFilteredPins();

    // Update KPI pills if mounted
    const kpiEl = document.getElementById('geoRadarKpiBar');
    if (kpiEl) {
      kpiEl.innerHTML = `
        <div class="kpi-liquid-card">
          <div class="kpi-top-tag"><span class="kpi-tag-label">Pines MTY &amp; SPGG</span><span class="kpi-specular-icon">⌖</span></div>
          <div class="kpi-num-display">${geo.total_pins || 0}</div>
          <div class="kpi-desc-sub">Exactos Apify: ${pc.apify_exact || 0} · OSM: ${pc.osm_geocoded || 0} · Zona: ${pc.zone_centroid || 0}</div>
        </div>
        <div class="kpi-liquid-card">
          <div class="kpi-top-tag"><span class="kpi-tag-label">Atacados / En Cola</span><span class="kpi-specular-icon">✓</span></div>
          <div class="kpi-num-display">${(sc.atacado_aprobado || 0) + (sc.en_cola_pendiente || 0)}</div>
          <div class="kpi-desc-sub">Atacados: ${sc.atacado_aprobado || 0} · Trigger pendiente: ${sc.en_cola_pendiente || 0}</div>
        </div>
        <div class="kpi-liquid-card">
          <div class="kpi-top-tag"><span class="kpi-tag-label">Dolor Crítico Libre</span><span class="kpi-specular-icon">⚑</span></div>
          <div class="kpi-num-display" style="color:#e8b3ad;">${sc.dolor_critico_sin_atacar || 0}</div>
          <div class="kpi-desc-sub">Street View / Sin reclamar listos para ruta o WA</div>
        </div>
        <div class="kpi-liquid-card">
          <div class="kpi-top-tag"><span class="kpi-tag-label">Rutas Guardadas</span><span class="kpi-specular-icon">⇢</span></div>
          <div class="kpi-num-display">${(geo.saved_routes || []).length}</div>
          <div class="kpi-desc-sub">Seleccionados ahora: ${cmdState.selectedSlugs.length} parada(s)</div>
        </div>
      `;
    }

    const countBadge = document.getElementById('geoVisibleCountBadge');
    if (countBadge) {
      countBadge.textContent = `${filtered.length} de ${geo.total_pins} pines visibles`;
    }

    renderLeafletMarkers(filtered);
    renderRoutePlannerPanel();
    renderGeoPinsTable(filtered);
  }

  function renderRoutePlannerPanel() {
    const selList = document.getElementById('geoSelectedStopsList');
    const outBox = document.getElementById('geoOptimizedRouteOutput');
    const savedBox = document.getElementById('geoSavedRoutesHistory');
    const geo = cmdState.geo;
    if (!geo) return;

    const bySlug = {};
    (geo.pins || []).forEach((p) => { bySlug[p.slug] = p; });

    if (selList) {
      if (!cmdState.selectedSlugs.length) {
        selList.innerHTML = `<div style="font-size:0.75rem;color:var(--slate-muted);padding:10px;border:1px dashed var(--glass-border);border-radius:8px;">Haz clic en cualquier pin del mapa o marca casillas en la lista inferior para armar tu ruta de hoy.</div>`;
      } else {
        selList.innerHTML = cmdState.selectedSlugs.map((slug, idx) => {
          const p = bySlug[slug];
          if (!p) return '';
          return `
            <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;padding:7px 10px;border-radius:8px;background:rgba(255,255,255,0.03);border:1px solid var(--glass-border);">
              <div style="min-width:0;">
                <div style="font-size:0.76rem;color:var(--bone-white);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${idx + 1}. ${esc(p.nombre)}</div>
                <div style="font-size:0.68rem;color:var(--slate-muted);">${esc(p.map_category)} · ${esc(p.municipio)} · ${p.distance_from_base_km} km</div>
              </div>
              <button type="button" class="btn-reject-trigger" style="padding:4px 8px;font-size:0.68rem;" onclick="window.toggleRouteSlug('${esc(slug)}')">Quitar</button>
            </div>
          `;
        }).join('');
      }
    }

    if (outBox) {
      const opt = cmdState.optimizedRoute;
      if (!opt) {
        outBox.innerHTML = `<div style="font-size:0.74rem;color:var(--slate-muted);">Presiona <strong>Trazar Ruta Más Eficiente</strong> para ordenar paradas por menor kilometraje (Nearest-Neighbor + 2-opt).</div>`;
      } else {
        outBox.innerHTML = `
          <div style="padding:12px;border-radius:10px;background:rgba(197,168,128,0.08);border:1px solid rgba(197,168,128,0.35);margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;margin-bottom:8px;">
              <strong style="color:var(--champagne);font-weight:500;">${opt.stops_count} paradas · ${opt.total_distance_km} km totales</strong>
              <span style="font-size:0.74rem;color:var(--platinum);">~${opt.estimated_total_drive_min} min manejo est.</span>
            </div>
            <div style="display:flex;flex-direction:column;gap:5px;margin-bottom:10px;">
              ${opt.stops.map((s) => `
                <div style="font-size:0.73rem;color:var(--platinum);display:flex;justify-content:space-between;gap:8px;border-bottom:1px solid rgba(255,255,255,0.05);padding-bottom:4px;">
                  <span><strong style="color:var(--champagne);">#${s.stop_number}</strong> ${esc(s.nombre)} <span style="color:var(--slate-muted);">(${esc(s.municipio)})</span></span>
                  <span style="white-space:nowrap;font-family:var(--font-mono);color:var(--champagne-light);">+${s.leg_distance_km} km</span>
                </div>
              `).join('')}
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
              <a href="${esc(opt.google_maps_route_url)}" target="_blank" rel="noopener" class="btn-approve-trigger" style="text-decoration:none;display:inline-flex;align-items:center;">Abrir en Google Maps Multi-Parada &rarr;</a>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr auto;gap:8px;">
            <input type="text" id="geoSaveRouteTitleInput" class="glass-select-input" placeholder="Nombre ruta (ej. Mañana Valle + Colegios)" value="Ruta MTY (${opt.stops_count} paradas · ${opt.total_distance_km} km)">
            <button type="button" class="week-btn" onclick="window.saveOptimizedGeoRoute()">Guardar en Bitácora</button>
          </div>
        `;
      }
    }

    if (savedBox) {
      const routes = geo.saved_routes || [];
      if (!routes.length) {
        savedBox.innerHTML = `<div style="font-size:0.74rem;color:var(--slate-muted);">Aún no hay rutas guardadas.</div>`;
      } else {
        savedBox.innerHTML = routes.slice(0, 6).map((r) => `
          <div style="padding:9px 11px;border-radius:8px;background:rgba(255,255,255,0.025);border:1px solid var(--glass-border-subtle);display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;">
            <div>
              <div style="font-size:0.76rem;color:var(--bone-white);">${esc(r.id)} · ${esc(r.title)}</div>
              <div style="font-size:0.68rem;color:var(--slate-muted);">${esc(r.scheduled_date)} · ${r.stops_count} paradas · ${r.total_distance_km} km</div>
            </div>
            <a href="${esc(r.google_maps_route_url)}" target="_blank" rel="noopener" class="week-btn" style="font-size:0.7rem;padding:4px 9px;text-decoration:none;">Abrir Maps &rarr;</a>
          </div>
        `).join('');
      }
    }
  }

  function renderGeoPinsTable(filtered) {
    const tbody = document.getElementById('geoLeadsTableBody');
    if (!tbody) return;
    const selectedSet = new Set(cmdState.selectedSlugs);
    const crmStages = ['Nuevo', 'Contactado', 'Respondio', 'Calendly', 'Cotizado', 'Anticipo_50', 'Cerrado', 'Descartado'];

    tbody.innerHTML = filtered.slice(0, 80).map((p) => {
      const checked = selectedSet.has(p.slug) ? 'checked' : '';
      const digits = String(p.telefono || '').replace(/\D+/g, '');
      const waDigits = digits ? (digits.length === 10 ? '52' + digits : digits) : '';
      const waText = encodeURIComponent(
        `Hola equipo de ${p.nombre}, soy Jesús Gutiérrez de Captoora Studio (https://captoora.studio/sports). Preparamos su análisis visual y producción en sede 1/2000s para su vitrina 2027. ¿Te lo comparto?`
      );
      return `
        <tr>
          <td><input type="checkbox" ${checked} onchange="window.toggleRouteSlug('${esc(p.slug)}')" aria-label="Incluir ${esc(p.nombre)} en ruta"></td>
          <td>
            <div style="color:var(--bone-white);font-weight:400;">${esc(p.nombre)}</div>
            <div style="font-size:0.68rem;color:var(--slate-muted);">${esc(p.map_category)} · ${esc(p.municipio)} · ${p.distance_from_base_km} km</div>
          </td>
          <td><span style="padding:2px 8px;border-radius:99px;font-size:0.68rem;white-space:nowrap;${statusBadgeStyle(p.campaign_status)}">${esc(p.status_label)}</span></td>
          <td style="font-size:0.72rem;color:var(--platinum);">${esc(precisionBadge(p.geo_precision))}</td>
          <td>
            <select class="glass-select-input" style="padding:4px 6px;font-size:0.7rem;" onchange="window.quickUpdatePinCrm('${esc(p.slug)}', '${esc(p.nombre)}', this.value)">
              ${crmStages.map((st) => `<option value="${st}" ${p.crm_stage === st ? 'selected' : ''}>${st}</option>`).join('')}
            </select>
          </td>
          <td>
            <div style="display:flex;gap:5px;flex-wrap:wrap;">
              <button type="button" class="week-btn" style="padding:4px 8px;font-size:0.68rem;" onclick="window.focusPinOnMap('${esc(p.slug)}')">Ver Pin</button>
              ${waDigits ? `<a href="https://web.whatsapp.com/send?phone=${waDigits}&text=${waText}" target="_blank" rel="noopener" class="week-btn" style="padding:4px 8px;font-size:0.68rem;text-decoration:none;border-color:rgba(110,148,119,0.45);color:#c2dec8;">WA Web</a>` : ''}
            </div>
          </td>
        </tr>
      `;
    }).join('');
  }

  window.setGeoStatusFilter = function (st) {
    cmdState.statusFilter = st || 'all';
    document.querySelectorAll('[data-geo-status-btn]').forEach((btn) => {
      btn.classList.toggle('active', btn.getAttribute('data-geo-status-btn') === cmdState.statusFilter);
    });
    renderGeoCommandTab();
  };

  window.setGeoCategoryFilter = function (cat) {
    cmdState.categoryFilter = cat || 'all';
    renderGeoCommandTab();
  };

  window.setGeoSearchQuery = function (q) {
    cmdState.searchQuery = q || '';
    renderGeoCommandTab();
  };

  window.toggleRouteSlug = function (slug) {
    const idx = cmdState.selectedSlugs.indexOf(slug);
    if (idx >= 0) {
      cmdState.selectedSlugs.splice(idx, 1);
    } else {
      if (cmdState.selectedSlugs.length >= 12) {
        toast('Máximo 12 paradas por ruta diaria en Google Maps.');
        return;
      }
      cmdState.selectedSlugs.push(slug);
    }
    cmdState.optimizedRoute = null;
    renderGeoCommandTab();
  };

  window.selectSmartGeoBatch = function (mode) {
    const filtered = getFilteredPins();
    let picks = [];
    if (mode === 'critical') {
      picks = filtered
        .filter((p) => p.campaign_status === 'dolor_critico_sin_atacar' || (p.audit_flags || []).length > 0)
        .sort((a, b) => a.distance_from_base_km - b.distance_from_base_km)
        .slice(0, 6);
    } else if (mode === 'nearest') {
      picks = [...filtered].sort((a, b) => a.distance_from_base_km - b.distance_from_base_km).slice(0, 6);
    }
    cmdState.selectedSlugs = picks.map((p) => p.slug);
    cmdState.optimizedRoute = null;
    renderGeoCommandTab();
    if (picks.length) {
      toast(`${picks.length} paradas cargadas; presiona "Trazar Ruta Más Eficiente".`);
    } else {
      toast('No hubo coincidencias con el filtro actual.');
    }
  };

  window.clearGeoRouteSelection = function () {
    cmdState.selectedSlugs = [];
    cmdState.optimizedRoute = null;
    renderGeoCommandTab();
  };

  window.useBrowserLocationAsOrigin = function () {
    if (!navigator.geolocation) {
      toast('Tu navegador no permite geolocalización; usando Base Operativa.');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        cmdState.originMode = 'gps';
        cmdState.customOrigin = {
          lat: Number(pos.coords.latitude.toFixed(6)),
          lng: Number(pos.coords.longitude.toFixed(6)),
          name: 'Mi Ubicación Actual GPS',
        };
        const badge = document.getElementById('geoOriginLabel');
        if (badge) badge.textContent = `Origen: GPS Actual (${cmdState.customOrigin.lat}, ${cmdState.customOrigin.lng})`;
        toast('Origen actualizado a tu GPS actual.');
      },
      () => toast('Permiso GPS rechazado; se mantiene Base Operativa.')
    );
  };

  window.optimizeGeoRouteNow = async function () {
    if (!cmdState.selectedSlugs.length) {
      toast('Selecciona al menos 1 parada en el mapa o tabla.');
      return;
    }
    try {
      const body = { slugs: cmdState.selectedSlugs };
      if (cmdState.originMode === 'gps' && cmdState.customOrigin) {
        body.origin_lat = cmdState.customOrigin.lat;
        body.origin_lng = cmdState.customOrigin.lng;
        body.origin_name = cmdState.customOrigin.name;
      }
      const plan = await apiJson('/api/geo/routes/optimize', {
        method: 'POST',
        body: JSON.stringify(body),
      });
      cmdState.optimizedRoute = plan;
      renderGeoCommandTab();
      toast(`Ruta trazada: ${plan.stops_count} paradas · ${plan.total_distance_km} km totales.`);
    } catch (err) {
      toast('Error trazando ruta: ' + err.message);
    }
  };

  window.saveOptimizedGeoRoute = async function () {
    if (!cmdState.optimizedRoute || !cmdState.selectedSlugs.length) {
      toast('Primero calcula la ruta optimizada.');
      return;
    }
    const titleEl = document.getElementById('geoSaveRouteTitleInput');
    const title = (titleEl && titleEl.value.trim()) || 'Ruta Monterrey';
    try {
      const body = {
        title,
        slugs: cmdState.optimizedRoute.stops.map((s) => s.slug),
      };
      if (cmdState.originMode === 'gps' && cmdState.customOrigin) {
        body.origin_lat = cmdState.customOrigin.lat;
        body.origin_lng = cmdState.customOrigin.lng;
      }
      const res = await apiJson('/api/geo/routes/save', {
        method: 'POST',
        body: JSON.stringify(body),
      });
      cmdState.geo = res.geo;
      renderGeoCommandTab();
      if (typeof window.syncWorkspaceFromServer === 'function') window.syncWorkspaceFromServer(true);
      toast(`Ruta ${res.route.id} guardada en bitácora.`);
    } catch (err) {
      toast('Error guardando ruta: ' + err.message);
    }
  };

  window.focusPinOnMap = function (slug) {
    const pins = (cmdState.geo && cmdState.geo.pins) || [];
    const pin = pins.find((p) => p.slug === slug);
    if (!pin || !cmdState.leafletMap) return;
    cmdState.leafletMap.setView([pin.lat, pin.lng], 15, { animate: true });
    window.scrollTo({ top: 180, behavior: 'smooth' });
  };

  window.quickUpdatePinCrm = async function (slug, nombre, stage) {
    try {
      await apiJson('/api/growth/crm/upsert', {
        method: 'POST',
        body: JSON.stringify({ slug, nombre, stage }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`CRM de ${nombre}: ${stage}`);
    } catch (err) {
      toast('Error CRM: ' + err.message);
    }
  };

  // ==========================================================================
  // TAB 2: CONTADOR PFAE 612 (GUFJ870801NA6) + 7+1 MOTORES + DESPERTADOR 24/7
  // ==========================================================================
  function renderExecutiveGrowthTab() {
    const g = cmdState.growth;
    if (!g) return;
    renderDailyPipelinePanel(g.daily_automation);
    renderAccountantPanel(g.accountant);
    renderWhatsAppSupervisorPanel(g.whatsapp_web_supervisor);
    renderScheduler247Panel(g.scheduler);
    renderSeoAnd20ClipsPanel(g.seo_status, g.growth_suite.seo_and_clips);
    renderCeoAgendaCalendlyPanel(g.growth_suite, g.weekly_report);
    renderMailCrmApifyPanel(g.growth_suite, g.presets);
  }

  function renderAccountantPanel(acct) {
    const box = document.getElementById('growthAccountantPanel');
    if (!box || !acct) return;
    const fp = acct.fiscal_profile || {};
    const s = acct.summary || {};
    const fc = acct.first_sale_forecast || {};
    const ap = fc.active_pipeline || {};
    const gateColor = s.ads_unlocked
      ? 'border-color:rgba(110,148,119,0.5);background:rgba(110,148,119,0.12);color:#c2dec8;'
      : 'border-color:rgba(184,98,89,0.45);background:rgba(184,98,89,0.12);color:#e8b3ad;';

    box.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:14px;">
        <div>
          <div class="panel-inner-title">1 · Agente Contador · Régimen ${esc(fp.regime_code || '612')} SAT · RFC ${esc(fp.rfc || 'GUFJ870801NA6')}</div>
          <div class="panel-inner-sub" style="margin-bottom:0;">${esc(fp.regime_name || 'Persona Física con Actividades Empresariales y Profesionales')} · Regla Cero Deuda en Pauta.</div>
        </div>
        <div style="padding:7px 12px;border-radius:99px;font-size:0.74rem;border:1px solid;${gateColor}">
          ${esc(s.ads_gate_status)}
        </div>
      </div>

      <div class="kpi-liquid-row" style="margin-bottom:16px;">
        <div class="kpi-liquid-card">
          <div class="kpi-top-tag"><span class="kpi-tag-label">Cobrado Real en Caja</span><span>$</span></div>
          <div class="kpi-num-display">${money(s.gross_collected_mxn)}</div>
          <div class="kpi-desc-sub">${s.paid_sales_count || 0} ventas cobradas · Costo directo: ${money(s.direct_production_costs_mxn)}</div>
        </div>
        <div class="kpi-liquid-card">
          <div class="kpi-top-tag"><span class="kpi-tag-label">Reserva Impuestos SAT</span><span>⚖</span></div>
          <div class="kpi-num-display">${money(s.total_tax_reserve_mxn)}</div>
          <div class="kpi-desc-sub">IVA 16%: ${money(s.iva_payable_sat_mxn)} · ISR (${fp.isr_reserve_pct}%): ${money(s.isr_estimated_reserve_mxn)}</div>
        </div>
        <div class="kpi-liquid-card">
          <div class="kpi-top-tag"><span class="kpi-tag-label">Utilidad Libre Neta</span><span>✦</span></div>
          <div class="kpi-num-display" style="color:${(s.free_net_profit_mxn || 0) > 0 ? '#c2dec8' : 'var(--bone-white)'};">${money(s.free_net_profit_mxn)}</div>
          <div class="kpi-desc-sub">Gastos deducibles: ${money(s.deductible_expenses_mxn)}</div>
        </div>
        <div class="kpi-liquid-card">
          <div class="kpi-top-tag"><span class="kpi-tag-label">Bolsa Ads Autorizada (${fp.ads_reinvestment_pct || 20}%)</span><span>◈</span></div>
          <div class="kpi-num-display" style="color:${s.ads_unlocked ? '#c5a880' : '#e8b3ad'};">${money(s.authorized_ads_budget_mxn)}</div>
          <div class="kpi-desc-sub">${s.ads_unlocked ? 'Listo para invertir sin deuda' : 'Desbloquea tras 1er anticipo 50%'}</div>
        </div>
      </div>

      <div style="padding:12px 14px;border-radius:10px;background:rgba(197,168,128,0.07);border:1px solid rgba(197,168,128,0.25);margin-bottom:16px;font-size:0.76rem;color:var(--platinum);">
        <strong style="color:var(--champagne);">Pronóstico 1ª Venta:</strong> ${esc(fc.estimated_window || '')} ·
        Pipeline activo: <strong>${ap.approved_ready || 0} aprobados</strong>, <strong>${ap.pending_trigger || 0} en cola</strong>, <strong>${ap.deficient_gmaps_targets || 0} Maps deficientes</strong> ·
        1er anticipo 50% ref: <strong>${money(fc.expected_first_advance_50_mxn)}</strong> &rarr; desbloquea aprox. <strong>${money(fc.estimated_ads_unlock_on_first_sale_mxn)}</strong> de pauta libre.
      </div>

      <div class="mvp-grid-layout" style="margin-bottom:16px;">
        <div style="padding:14px;border-radius:12px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);">
          <div style="font-size:0.82rem;color:var(--champagne);margin-bottom:8px;">Registrar Cobro Real (Desbloquea Bolsa Ads)</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
            <input type="text" id="acctSaleClient" class="glass-select-input" placeholder="Cliente / Negocio">
            <input type="text" id="acctSalePkg" class="glass-select-input" placeholder="Paquete (ej. Maps Visual 3,900)">
            <input type="number" id="acctSaleAmt" class="glass-select-input" placeholder="Monto cobrado MXN" min="1" step="10">
            <input type="number" id="acctSaleCost" class="glass-select-input" placeholder="Costo taller MXN (ej. 0 o 450)" min="0" step="10" value="0">
          </div>
          <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;font-size:0.73rem;margin-bottom:10px;color:var(--platinum);">
            <label><input type="checkbox" id="acctSaleIva" checked> Incluye IVA 16%</label>
            <label><input type="checkbox" id="acctSalePm"> Cliente Persona Moral (Retención 10% ISR)</label>
          </div>
          <button type="button" class="btn-approve-trigger" onclick="window.submitAccountantSale()">Registrar Cobro en Caja</button>
        </div>

        <div style="padding:14px;border-radius:12px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);">
          <div style="font-size:0.82rem;color:var(--champagne);margin-bottom:8px;">Registrar Gasto CFDI &amp; Parámetros Fiscales 612</div>
          <div style="display:grid;grid-template-columns:1.4fr 1fr;gap:8px;margin-bottom:8px;">
            <input type="text" id="acctExpConcept" class="glass-select-input" placeholder="Gasto deducible (ej. Acrílico LED taller)">
            <input type="number" id="acctExpAmt" class="glass-select-input" placeholder="Monto MXN" min="1" step="10">
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:12px;">
            <label style="font-size:0.73rem;color:var(--platinum);"><input type="checkbox" id="acctExpIva" checked> Tiene CFDI con IVA acreditable</label>
            <button type="button" class="week-btn" onclick="window.submitAccountantExpense()">+ Registrar Gasto</button>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr auto;gap:8px;align-items:center;border-top:1px solid var(--glass-border-subtle);padding-top:10px;">
            <label style="font-size:0.7rem;color:var(--slate-muted);">Reserva ISR % <input type="number" id="acctCfgIsr" class="glass-select-input" value="${fp.isr_reserve_pct || 20}" min="0" max="45" step="1" style="margin-top:3px;"></label>
            <label style="font-size:0.7rem;color:var(--slate-muted);">Reinversión Ads % <input type="number" id="acctCfgAds" class="glass-select-input" value="${fp.ads_reinvestment_pct || 20}" min="0" max="50" step="1" style="margin-top:3px;"></label>
            <button type="button" class="week-btn" style="margin-top:14px;" onclick="window.saveFiscalConfig()">Guardar %</button>
          </div>
        </div>
      </div>

      <div class="mvp-grid-layout">
        <div>
          <div style="font-size:0.8rem;color:var(--bone-white);margin-bottom:8px;">Distribución Autorizada de Pauta ($0 hasta cobrar ventas reales)</div>
          <div style="display:flex;flex-direction:column;gap:6px;">
            ${(acct.platform_allocations || []).map((p) => `
              <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;padding:8px 10px;border-radius:8px;background:rgba(255,255,255,0.025);border:1px solid var(--glass-border-subtle);font-size:0.74rem;">
                <div>
                  <div style="color:var(--bone-white);">${esc(p.platform)} <span style="color:var(--champagne);">(${p.share_pct}%)</span></div>
                  <div style="font-size:0.68rem;color:var(--slate-muted);">${esc(p.role)}</div>
                </div>
                <strong style="font-family:var(--font-mono);color:${Number(p.authorized_mxn) > 0 ? '#c2dec8' : '#e8b3ad'};white-space:nowrap;">${money(p.authorized_mxn)}</strong>
              </div>
            `).join('')}
          </div>
        </div>

        <div>
          <div style="font-size:0.8rem;color:var(--bone-white);margin-bottom:6px;">Auditor Fiscal &amp; Flujo de Contratos (PFAE 612)</div>
          <textarea id="acctContractInput" class="mkhq-textarea" style="min-height:92px;margin-bottom:8px;" placeholder="Pega cláusulas de pago, retenciones PM o cesión de derechos del contrato del cliente para auditar riesgo SAT y flujo 50/50..."></textarea>
          <button type="button" class="week-btn" onclick="window.runContractTaxAudit()">Auditar Contrato Fiscalmente</button>
          <div id="acctContractAuditResult" style="margin-top:8px;font-size:0.73rem;color:var(--platinum);"></div>
        </div>
      </div>
    `;
  }

  function renderWhatsAppSupervisorPanel(wa) {
    const box = document.getElementById('growthWhatsappSupervisorPanel');
    if (!box || !wa) return;
    const items = wa.items || [];
    const pct = Math.min(100, Math.round(((wa.sent_today || 0) / (wa.daily_safe_limit || 20)) * 100));

    box.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:12px;">
        <div>
          <div class="panel-inner-title">2 · Supervisor Seguro WhatsApp Web 1-Clic (Cero Baneo)</div>
          <div class="panel-inner-sub" style="margin-bottom:0;">Modo: <strong>${esc(wa.mode)}</strong> · Tope sano: ${wa.daily_safe_limit || 20} conversaciones nuevas/día. Tú abres y confirmas manualmente.</div>
        </div>
        <div style="font-family:var(--font-mono);font-size:0.78rem;color:var(--champagne);">
          Hoy: ${wa.sent_today || 0} / ${wa.daily_safe_limit || 20} (Quedan ${wa.remaining_today_safe || 0} seguras)
        </div>
      </div>
      <div style="height:6px;border-radius:99px;background:rgba(255,255,255,0.07);overflow:hidden;margin-bottom:14px;">
        <div style="width:${pct}%;height:100%;background:#6e9477;"></div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;">
        ${items.slice(0, 8).map((it) => `
          <div style="padding:13px;border-radius:12px;background:rgba(0,0,0,0.32);border:1px solid var(--glass-border);display:flex;flex-direction:column;gap:8px;">
            <div style="display:flex;justify-content:space-between;gap:6px;align-items:center;">
              <strong style="color:var(--bone-white);font-weight:500;font-size:0.82rem;">${esc(it.nombre)}</strong>
              <span style="font-size:0.66rem;padding:2px 7px;border-radius:99px;background:rgba(197,168,128,0.14);color:var(--champagne-light);">${esc(it.queue_status)}</span>
            </div>
            <div style="font-size:0.7rem;color:var(--slate-muted);">${esc(it.nicho)} · +${esc(it.phone)}</div>
            <div style="font-size:0.72rem;color:var(--platinum);background:rgba(255,255,255,0.03);padding:8px;border-radius:6px;max-height:76px;overflow:auto;">${esc(it.message)}</div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;">
              <a href="${esc(it.web_whatsapp_url)}" target="_blank" rel="noopener" class="btn-approve-trigger" style="text-decoration:none;font-size:0.72rem;padding:6px 10px;">Abrir WA Web &rarr;</a>
              <button type="button" class="week-btn" style="font-size:0.72rem;padding:6px 10px;" onclick="window.confirmWaWebSent('${esc(it.slug)}','${esc(it.nombre)}','${esc(it.phone)}')">
                ${it.already_sent_logged ? 'Ya Registrado ✓' : 'Marcar Enviado'}
              </button>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  function renderScheduler247Panel(sched) {
    const box = document.getElementById('growthSchedulerPanel');
    if (!box || !sched) return;
    const slots = sched.slots || [];
    box.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:12px;">
        <div>
          <div class="panel-inner-title">3 · Despertador 24/7 (Monterrey CST) &amp; Launchd macOS</div>
          <div class="panel-inner-sub" style="margin-bottom:0;">Corre automático cada 60s dentro del servidor y con respaldo launchd al encender la Mac. Nunca envía externos sin tu clic.</div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
          <span style="font-size:0.72rem;padding:4px 10px;border-radius:99px;border:1px solid ${sched.launchd_installed ? 'rgba(110,148,119,0.5)' : 'rgba(197,159,107,0.45)'};color:${sched.launchd_installed ? '#c2dec8' : '#dfcbb5'};">
            launchd: ${sched.launchd_installed ? 'Instalado' : 'Pendiente instalar'}
          </span>
          <button type="button" class="week-btn" onclick="window.copyLaunchdInstallCmd()">Copiar Comando launchd</button>
          <button type="button" class="${sched.enabled ? 'btn-approve-trigger' : 'btn-reject-trigger'}" onclick="window.toggleSchedulerEnabled(${!sched.enabled})">
            ${sched.enabled ? 'Despertador ACTIVO (Pausar)' : 'Despertador PAUSADO (Activar)'}
          </button>
        </div>
      </div>
      <div style="font-size:0.72rem;color:var(--slate-muted);margin-bottom:10px;">
        Último tick: ${esc(sched.last_tick || 'Esperando ciclo 60s')} ${sched.last_executed_slot ? `· Último slot: ${esc(sched.last_executed_slot.slot_id)} (${esc(sched.last_executed_slot.detail)})` : ''}
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;">
        ${slots.map((sl) => `
          <div style="padding:11px;border-radius:10px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);display:flex;flex-direction:column;gap:8px;">
            <div style="font-size:0.77rem;color:var(--bone-white);">${esc(sl.label)}</div>
            <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">
              <span style="font-size:0.68rem;color:var(--champagne);">${(sched.ran_slots_today || {})[sl.id] ? 'Ejecutado: ' + (sched.ran_slots_today || {})[sl.id] : 'En espera de hora CST'}</span>
              <button type="button" class="week-btn" style="padding:4px 8px;font-size:0.68rem;" onclick="window.runSchedulerSlotNow('${esc(sl.id)}')">Probar Ahora</button>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  function renderSeoAnd20ClipsPanel(seo, clipsState) {
    const box = document.getElementById('growthSeoClipsPanel');
    if (!box || !seo) return;
    const checks = [
      ['sitemap.xml', seo.sitemap_xml_ready],
      ['robots.txt', seo.robots_txt_ready],
      ['llms.txt (ChatGPT/AEO)', seo.llms_txt_ready],
      ['JSON-LD Schema', seo.json_ld_ready],
      ['0% Presumir Colonia', seo.no_neighborhood_brag],
      ['GA4 ID (.env)', seo.ga4_configured],
      ['Meta Pixel (.env)', seo.meta_pixel_configured],
    ];
    const clips = (clipsState && clipsState.clips_20) || [];

    box.innerHTML = `
      <div class="panel-inner-title">4 · Motor SEO + AEO (ChatGPT Search) &amp; Matriz 20 Clips desde 1 Tema</div>
      <div class="panel-inner-sub">${esc(seo.note || '')}</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
        ${checks.map(([label, ok]) => `
          <span style="font-size:0.71rem;padding:4px 10px;border-radius:99px;border:1px solid ${ok ? 'rgba(110,148,119,0.5)' : 'rgba(197,159,107,0.4)'};background:${ok ? 'rgba(110,148,119,0.12)' : 'rgba(197,159,107,0.08)'};color:${ok ? '#c2dec8' : '#dfcbb5'};">
            ${ok ? '✓' : '○'} ${esc(label)}
          </span>
        `).join('')}
      </div>
      <div style="display:grid;grid-template-columns:1fr auto;gap:8px;margin-bottom:14px;">
        <input type="text" id="growth20ClipsTopicInput" class="glass-select-input" value="${esc((clipsState && clipsState.last_topic) || 'Auditoría Google Maps + Alta Velocidad 1/2000s')}" placeholder="Tema central para desdoblar en 20 clips 9:16...">
        <button type="button" class="btn-approve-trigger" onclick="window.generate20ClipsNow()">Generar 20 Clips 9:16</button>
      </div>
      <div style="max-height:310px;overflow:auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(275px,1fr));gap:8px;">
        ${clips.map((c) => `
          <div style="padding:10px;border-radius:8px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border-subtle);font-size:0.73rem;">
            <div style="display:flex;justify-content:space-between;color:var(--champagne);margin-bottom:4px;">
              <span>${esc(c.id)} · ${esc(c.pillar)}</span>
              <span>${esc(c.platform)}</span>
            </div>
            <div style="color:var(--bone-white);margin-bottom:6px;">&ldquo;${esc(c.hook_0_3s)}&rdquo;</div>
            <div style="display:flex;justify-content:space-between;align-items:center;color:var(--slate-muted);font-size:0.68rem;">
              <span>${esc(c.tool)} · ${esc(c.duration)}</span>
              <button type="button" class="week-btn" style="padding:3px 8px;font-size:0.66rem;" onclick="window.copyClipScript('${esc(c.hook_0_3s)} | CTA: ${esc(c.cta)}')">Copiar</button>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  function renderCeoAgendaCalendlyPanel(gs, report) {
    const box = document.getElementById('growthCeoAgendaCalendlyPanel');
    if (!box || !gs) return;
    const ceo = gs.ceo_plan || {};
    const ag = gs.agenda || {};
    const cal = gs.calendly || {};
    const fm = (report && report.funnel_metrics) || {};

    box.innerHTML = `
      <div class="mvp-grid-layout" style="margin-bottom:16px;">
        <div style="padding:16px;border-radius:14px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);">
          <div class="panel-inner-title">5 · CEO Personal &amp; Reporte Semanal Automático</div>
          <div style="display:flex;gap:8px;margin:10px 0;">
            <input type="text" id="ceoFocusInput" class="glass-select-input" value="${esc(ceo.week_focus || '')}">
            <button type="button" class="week-btn" onclick="window.refreshCeoPlanNow()">Actualizar Foco</button>
          </div>
          <div style="font-size:0.74rem;color:var(--champagne);margin:8px 0 4px;">Ganchos de Alta Conversión en Monterrey:</div>
          <ul style="padding-left:16px;font-size:0.73rem;color:var(--platinum);margin-bottom:12px;">
            ${(ceo.trending_hooks_mty || []).map((h) => `<li style="margin-bottom:3px;">${esc(h)}</li>`).join('')}
          </ul>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding-top:10px;border-top:1px solid var(--glass-border-subtle);text-align:center;">
            <div><div style="font-size:1rem;color:var(--bone-white);">${fm.pending_trigger || 0}</div><div style="font-size:0.66rem;color:var(--slate-muted);">Cola Trigger</div></div>
            <div><div style="font-size:1rem;color:var(--bone-white);">${fm.whatsapp_web_sent || 0}</div><div style="font-size:0.66rem;color:var(--slate-muted);">WA Web Reg.</div></div>
            <div><div style="font-size:1rem;color:var(--bone-white);">${fm.zoho_emails_sent || 0}</div><div style="font-size:0.66rem;color:var(--slate-muted);">Correos Zoho</div></div>
            <div><div style="font-size:1rem;color:var(--champagne);">${fm.routes_logged || 0}</div><div style="font-size:0.66rem;color:var(--slate-muted);">Rutas Guard.</div></div>
          </div>
        </div>

        <div style="padding:16px;border-radius:14px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);">
          <div class="panel-inner-title">6 · Agenda Hoy / Mañana &amp; Generador Calendly</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;">
            <div>
              <div style="font-size:0.72rem;color:var(--champagne);margin-bottom:4px;">Hoy</div>
              ${(ag.today_blocks || []).slice(0, 4).map((b) => `<div style="font-size:0.7rem;color:var(--platinum);margin-bottom:3px;"><strong>${esc(b.time)}</strong> ${esc(b.title)}</div>`).join('')}
            </div>
            <div>
              <div style="font-size:0.72rem;color:#c2dec8;margin-bottom:4px;">Mañana</div>
              ${(ag.tomorrow_blocks || []).map((b) => `<div style="font-size:0.7rem;color:var(--platinum);margin-bottom:3px;"><strong>${esc(b.time)}</strong> ${esc(b.title)}</div>`).join('')}
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr auto;gap:8px;margin-bottom:12px;">
            <input type="email" id="tomorrowReminderEmail" class="glass-select-input" placeholder="Email opcional (vacío = registro interno)">
            <button type="button" class="week-btn" onclick="window.triggerTomorrowReminderNow()">Recordatorio Mañana</button>
          </div>
          <div style="border-top:1px solid var(--glass-border-subtle);padding-top:10px;">
            <div style="display:grid;grid-template-columns:1fr auto;gap:8px;margin-bottom:8px;">
              <input type="text" id="calendlyBaseUrlInput" class="glass-select-input" value="${esc(cal.base_url || 'https://calendly.com/captoora')}" placeholder="https://calendly.com/tu-usuario">
              <button type="button" class="week-btn" onclick="window.saveCalendlyBaseUrlNow()">Guardar Base Calendly</button>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr auto;gap:8px;">
              <input type="text" id="calendlyProspectInput" class="glass-select-input" placeholder="Nombre del prospecto (ej. Dra. Elena)">
              <select id="calendlyEventSelect" class="glass-select-input">
                ${(cal.event_types || []).map((e) => `<option value="${esc(e.id)}">${esc(e.label)}</option>`).join('')}
              </select>
              <button type="button" class="btn-approve-trigger" onclick="window.generateCalendlyLinkNow()">Generar Link</button>
            </div>
            <div id="calendlyGeneratedPreview" style="margin-top:8px;font-size:0.72rem;color:var(--champagne-light);">
              ${(cal.generated_links || [])[0] ? `Último: <a href="${esc(cal.generated_links[0].url)}" target="_blank" rel="noopener" style="color:var(--champagne);">${esc(cal.generated_links[0].url)}</a>` : ''}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  function renderMailCrmApifyPanel(gs, presets) {
    const box = document.getElementById('growthMailCrmApifyPanel');
    if (!box || !gs) return;
    const zones = (presets && presets.zones) || {};
    const niches = (presets && presets.niches) || {};
    const crmRows = Object.values(gs.crm_records || {});

    box.innerHTML = `
      <div class="mvp-grid-layout">
        <div style="padding:16px;border-radius:14px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
            <div class="panel-inner-title" style="margin-bottom:0;">7 · Zoho Mail (chuy@) + Buscador de Correos</div>
            <button type="button" class="week-btn" onclick="window.enrichEmailsNow()">Escanear Sitios Web por Correos</button>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
            <input type="email" id="mailToInput" class="glass-select-input" placeholder="Correo destino prospecto">
            <input type="text" id="mailProspectInput" class="glass-select-input" placeholder="Nombre negocio / doctor / escuela">
            <select id="mailOfferSelect" class="glass-select-input">
              <option value="small_business">Small Business Maps &amp; 2027 (-35%)</option>
              <option value="navidad_led">Eventos + Trofeos LED (-35%)</option>
              <option value="biogen">Captoora Biogen Atletas</option>
            </select>
            <input type="text" id="mailAttachSlugInput" class="glass-select-input" placeholder="Slug PDF opcional (ej. 11_11_fitness_top_obispado)">
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;">
            <label style="font-size:0.73rem;color:var(--platinum);"><input type="checkbox" id="mailDryRunChk" checked> Modo Simulación (Dry-Run · destilda para envío real SMTP)</label>
            <button type="button" class="btn-approve-trigger" onclick="window.sendGrowthMailNow()">Preparar / Enviar Correo</button>
          </div>
          <div id="mailEnrichStatusBox" style="margin-top:10px;font-size:0.72rem;color:var(--slate-muted);">
            Últimos envíos: ${(gs.mail_campaigns_log || []).slice(0, 3).map((m) => `${esc(m.prospect_name)} (${esc(m.status)})`).join(' · ') || 'Sin envíos aún'}
          </div>
        </div>

        <div style="padding:16px;border-radius:14px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);">
          <div class="panel-inner-title">8 · CRM / KYC (GoHighLevel) &amp; Barrido Apify Multi-Zona</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
            <input type="text" id="crmNombreInput" class="glass-select-input" placeholder="Negocio / Cliente">
            <select id="crmStageSelect" class="glass-select-input">
              <option value="Nuevo">Nuevo</option>
              <option value="Contactado">Contactado</option>
              <option value="Respondio">Respondió</option>
              <option value="Calendly">Calendly Agendado</option>
              <option value="Cotizado">Cotizado</option>
              <option value="Anticipo_50">Anticipo 50% Cobrado</option>
              <option value="Cerrado">Cerrado Ganado</option>
            </select>
            <input type="text" id="crmDecisorInput" class="glass-select-input" placeholder="Nombre decisor">
            <input type="text" id="crmRfcInput" class="glass-select-input" placeholder="RFC (KYC Facturación)">
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
            <label style="font-size:0.72rem;color:var(--platinum);"><input type="checkbox" id="crmSyncGhlChk"> Enviar también a GHL Webhook (.env)</label>
            <button type="button" class="week-btn" onclick="window.upsertCrmKycNow()">Guardar CRM/KYC (${crmRows.length})</button>
          </div>
          <div style="border-top:1px solid var(--glass-border-subtle);padding-top:10px;">
            <div style="font-size:0.74rem;color:var(--champagne);margin-bottom:6px;">Planificador de Barrido Apify Nuevo León:</div>
            <div style="display:flex;flex-wrap:wrap;gap:8px;font-size:0.71rem;margin-bottom:8px;color:var(--platinum);">
              ${Object.entries(zones).map(([k, z]) => `<label><input type="checkbox" name="apifyZoneChk" value="${esc(k)}" ${k === 'valle_san_pedro' ? 'checked' : ''}> ${esc(z.label)}</label>`).join('')}
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:8px;font-size:0.71rem;margin-bottom:10px;color:var(--champagne-light);">
              ${Object.entries(niches).map(([k]) => `<label><input type="checkbox" name="apifyNicheChk" value="${esc(k)}" ${k === 'kinder_colegio' ? 'checked' : ''}> ${esc(k)}</label>`).join('')}
            </div>
            <button type="button" class="week-btn" onclick="window.runApifySweepNow(true)">Planificar Barrido (Dry-Run)</button>
          </div>
        </div>
      </div>
    `;
  }

  // Action Handlers for Executive Growth Tab
  window.submitAccountantSale = async function () {
    const client_name = (document.getElementById('acctSaleClient')?.value || '').trim();
    const package_ref = (document.getElementById('acctSalePkg')?.value || '').trim() || 'Paquete Captoora';
    const amount_collected_mxn = Number(document.getElementById('acctSaleAmt')?.value || 0);
    const direct_cost_mxn = Number(document.getElementById('acctSaleCost')?.value || 0);
    const includes_iva = Boolean(document.getElementById('acctSaleIva')?.checked);
    const client_is_persona_moral = Boolean(document.getElementById('acctSalePm')?.checked);
    if (!client_name || amount_collected_mxn <= 0) {
      toast('Ingresa nombre del cliente y monto cobrado > 0 MXN.');
      return;
    }
    try {
      await apiJson('/api/growth/accountant/record-sale', {
        method: 'POST',
        body: JSON.stringify({ client_name, package_ref, amount_collected_mxn, direct_cost_mxn, includes_iva, client_is_persona_moral }),
      });
      await window.loadGeoAndGrowthData(true);
      toast('Cobro registrado en Contador PFAE 612.');
    } catch (err) {
      toast('Error Contador: ' + err.message);
    }
  };

  window.submitAccountantExpense = async function () {
    const concept = (document.getElementById('acctExpConcept')?.value || '').trim();
    const amount_mxn = Number(document.getElementById('acctExpAmt')?.value || 0);
    const has_cfdi_iva = Boolean(document.getElementById('acctExpIva')?.checked);
    if (!concept || amount_mxn <= 0) {
      toast('Ingresa concepto y monto > 0 MXN del gasto.');
      return;
    }
    try {
      await apiJson('/api/growth/accountant/record-expense', {
        method: 'POST',
        body: JSON.stringify({ concept, amount_mxn, has_cfdi_iva }),
      });
      await window.loadGeoAndGrowthData(true);
      toast('Gasto CFDI registrado.');
    } catch (err) {
      toast('Error Gasto: ' + err.message);
    }
  };

  window.saveFiscalConfig = async function () {
    const isr_reserve_pct = Number(document.getElementById('acctCfgIsr')?.value || 20);
    const ads_reinvestment_pct = Number(document.getElementById('acctCfgAds')?.value || 20);
    try {
      await apiJson('/api/growth/accountant/config', {
        method: 'POST',
        body: JSON.stringify({ isr_reserve_pct, ads_reinvestment_pct }),
      });
      await window.loadGeoAndGrowthData(true);
      toast('Porcentajes SAT 612 y reinversión actualizados.');
    } catch (err) {
      toast('Error Config: ' + err.message);
    }
  };

  window.runContractTaxAudit = async function () {
    const contract_text = (document.getElementById('acctContractInput')?.value || '').trim();
    if (contract_text.length < 10) {
      toast('Pega al menos 10 caracteres del contrato a auditar.');
      return;
    }
    try {
      const res = await apiJson('/api/growth/accountant/audit-contract', {
        method: 'POST',
        body: JSON.stringify({ contract_text }),
      });
      const out = document.getElementById('acctContractAuditResult');
      if (out) {
        out.innerHTML = `<div style="color:var(--champagne);margin-bottom:4px;">${esc(res.regime)}</div>` +
          (res.alerts || []).map((a) => `<div style="margin-bottom:3px;">• ${esc(a)}</div>`).join('');
      }
      toast('Auditoría fiscal completada.');
    } catch (err) {
      toast('Error Auditoría: ' + err.message);
    }
  };

  window.confirmWaWebSent = async function (slug, nombre, phone) {
    try {
      await apiJson('/api/whatsapp/web-mark-sent', {
        method: 'POST',
        body: JSON.stringify({ slug, nombre, phone, notes: 'Despachado 1-clic desde Supervisor WA Web' }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`WhatsApp Web registrado para ${nombre}.`);
    } catch (err) {
      toast('Error WA Web: ' + err.message);
    }
  };

  window.copyLaunchdInstallCmd = function () {
    copyText('bash scripts/install_launchd_24_7.sh', 'Comando copiado: pégalo en Terminal para activar launchd 24/7.');
  };

  window.toggleSchedulerEnabled = async function (enabled) {
    try {
      await apiJson('/api/scheduler/toggle', {
        method: 'POST',
        body: JSON.stringify({ enabled: Boolean(enabled) }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`Despertador 24/7 ${enabled ? 'ACTIVADO' : 'PAUSADO'}.`);
    } catch (err) {
      toast('Error Scheduler: ' + err.message);
    }
  };

  window.runSchedulerSlotNow = async function (slotId) {
    try {
      const res = await apiJson('/api/scheduler/run-slot', {
        method: 'POST',
        body: JSON.stringify({ slot_id: slotId }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`Slot ${slotId}: ${res.executed.detail}`);
    } catch (err) {
      toast('Error Slot: ' + err.message);
    }
  };

  window.generate20ClipsNow = async function () {
    const topic = (document.getElementById('growth20ClipsTopicInput')?.value || '').trim();
    if (topic.length < 3) {
      toast('Escribe un tema base.');
      return;
    }
    try {
      await apiJson('/api/growth/content/20-clips', {
        method: 'POST',
        body: JSON.stringify({ topic }),
      });
      await window.loadGeoAndGrowthData(true);
      toast('20 clips generados con guardrail limpio.');
    } catch (err) {
      toast('Error 20 Clips: ' + err.message);
    }
  };

  window.copyClipScript = function (txt) {
    copyText(txt, 'Hook y CTA del clip copiados.');
  };

  window.refreshCeoPlanNow = async function () {
    const custom_focus = (document.getElementById('ceoFocusInput')?.value || '').trim();
    try {
      await apiJson('/api/growth/ceo/plan', {
        method: 'POST',
        body: JSON.stringify({ custom_focus }),
      });
      await window.loadGeoAndGrowthData(true);
      toast('Plan semanal CEO actualizado.');
    } catch (err) {
      toast('Error CEO: ' + err.message);
    }
  };

  window.triggerTomorrowReminderNow = async function () {
    const send_email_to = (document.getElementById('tomorrowReminderEmail')?.value || '').trim();
    try {
      const res = await apiJson('/api/growth/agenda/remind-tomorrow', {
        method: 'POST',
        body: JSON.stringify({ send_email_to, dry_run: !send_email_to }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`Recordatorio agenda mañana procesado (${res.reminder.blocks_count} bloques).`);
    } catch (err) {
      toast('Error Agenda: ' + err.message);
    }
  };

  window.saveCalendlyBaseUrlNow = async function () {
    const base_url = (document.getElementById('calendlyBaseUrlInput')?.value || '').trim();
    if (!base_url.startsWith('http')) {
      toast('Ingresa una URL válida de Calendly (https://...).');
      return;
    }
    try {
      await apiJson('/api/growth/calendly/base-url', {
        method: 'POST',
        body: JSON.stringify({ base_url }),
      });
      await window.loadGeoAndGrowthData(true);
      toast('URL base de Calendly guardada.');
    } catch (err) {
      toast('Error Calendly: ' + err.message);
    }
  };

  window.generateCalendlyLinkNow = async function () {
    const prospect_name = (document.getElementById('calendlyProspectInput')?.value || '').trim();
    const event_type_id = document.getElementById('calendlyEventSelect')?.value || 'maps_audit_15';
    if (prospect_name.length < 2) {
      toast('Escribe el nombre del prospecto.');
      return;
    }
    try {
      const res = await apiJson('/api/growth/calendly/link', {
        method: 'POST',
        body: JSON.stringify({ prospect_name, event_type_id }),
      });
      await window.loadGeoAndGrowthData(true);
      copyText(res.link.whatsapp_message, 'Enlace Calendly e invitación WhatsApp copiados.');
    } catch (err) {
      toast('Error Link Calendly: ' + err.message);
    }
  };

  window.enrichEmailsNow = async function () {
    toast('Escaneando sitios web verificados para detectar correos...');
    try {
      const res = await apiJson('/api/growth/crm/enrich-emails', {
        method: 'POST',
        body: JSON.stringify({}),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`Revisados ${res.checked_websites} sitios · Detectados ${(res.emails_found || []).length} correos.`);
    } catch (err) {
      toast('Error Scanner Web: ' + err.message);
    }
  };

  window.sendGrowthMailNow = async function () {
    const to_email = (document.getElementById('mailToInput')?.value || '').trim();
    const prospect_name = (document.getElementById('mailProspectInput')?.value || '').trim();
    const offer_track = document.getElementById('mailOfferSelect')?.value || 'small_business';
    const attach_slug = (document.getElementById('mailAttachSlugInput')?.value || '').trim();
    const dry_run = Boolean(document.getElementById('mailDryRunChk')?.checked);
    if (!to_email || !prospect_name) {
      toast('Ingresa correo y nombre del prospecto.');
      return;
    }
    try {
      const res = await apiJson('/api/growth/mail/send', {
        method: 'POST',
        body: JSON.stringify({ to_email, prospect_name, offer_track, attach_slug, dry_run }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`Correo (${res.mode || res.status || 'ok'}) procesado para ${prospect_name}.`);
    } catch (err) {
      toast('Error Zoho Mail: ' + err.message);
    }
  };

  window.upsertCrmKycNow = async function () {
    const nombre = (document.getElementById('crmNombreInput')?.value || '').trim();
    const stage = document.getElementById('crmStageSelect')?.value || 'Nuevo';
    const decisor_name = (document.getElementById('crmDecisorInput')?.value || '').trim();
    const rfc = (document.getElementById('crmRfcInput')?.value || '').trim();
    const sync_ghl = Boolean(document.getElementById('crmSyncGhlChk')?.checked);
    if (!nombre) {
      toast('Ingresa el nombre del negocio / cliente.');
      return;
    }
    try {
      const res = await apiJson('/api/growth/crm/upsert', {
        method: 'POST',
        body: JSON.stringify({ nombre, stage, decisor_name, rfc, sync_ghl }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`CRM/KYC actualizado (${res.record.stage}).`);
    } catch (err) {
      toast('Error CRM/KYC: ' + err.message);
    }
  };

  window.runApifySweepNow = async function (dryRun = true) {
    const zones = Array.from(document.querySelectorAll('input[name="apifyZoneChk"]:checked')).map((el) => el.value);
    const niches = Array.from(document.querySelectorAll('input[name="apifyNicheChk"]:checked')).map((el) => el.value);
    if (!zones.length || !niches.length) {
      toast('Selecciona al menos una zona y un giro.');
      return;
    }
    try {
      const res = await apiJson('/api/growth/apify/sweep', {
        method: 'POST',
        body: JSON.stringify({ zones, niches, dry_run: dryRun }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`Barrido Apify planificado: ${res.sweep.queries.length} consultas.`);
    } catch (err) {
      toast('Error Apify Sweep: ' + err.message);
    }
  };

  function renderDailyPipelinePanel(da) {
    const box = document.getElementById('growthDailyPipelinePanel');
    if (!box) return;
    const data = da || {};
    const settings = data.settings || {};
    const mix = settings.territory_mix || { mty: 10, pv: 10, biogen: 5 };
    const batch = data.daily_email_batch || {};
    const batchItems = batch.items || [];
    const due = (data.due_followups && data.due_followups.items) || [];
    const variants = data.ab_variants || {};
    const iter = data.last_iteration_report || {};
    const logs = data.negotiation_logs || [];
    const playbooks = data.objection_playbooks || {};
    cmdState._copyMap = cmdState._copyMap || {};

    const smtpBadge = data.smtp_configured
      ? 'border-color:rgba(110,148,119,0.5);background:rgba(110,148,119,0.12);color:#c2dec8;'
      : 'border-color:rgba(197,159,107,0.45);background:rgba(197,159,107,0.12);color:#dfcbb5;';

    batchItems.forEach((it, idx) => {
      cmdState._copyMap[`batch_${idx}`] = `${it.subject || ''}\n\n${it.plain_text || ''}`;
    });
    due.forEach((f, idx) => {
      cmdState._copyMap[`due_${idx}`] = f.message || '';
    });

    box.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:14px;">
        <div>
          <div class="panel-inner-title">0 · Piloto Diario Automático · Correos (25/día), Seguimiento 48h/72h, Cierre e Iteración</div>
          <div class="panel-inner-sub" style="margin-bottom:0;">Correos listos con email: <strong>${data.crm_with_email || 0}</strong> (${data.uncontacted_with_email || 0} sin primer envío) · Webs escaneadas: ${data.scanned_websites_count || 0}</div>
        </div>
        <span style="padding:6px 12px;border-radius:99px;font-size:0.72rem;border:1px solid;${smtpBadge}">
          ${data.smtp_configured ? 'Zoho SMTP Activo (chuy@captoora.studio)' : 'Falta SMTP_PASS en .env → Exporta .eml + 1-Clic'}
        </span>
      </div>

      <div class="mvp-grid-layout" style="margin-bottom:14px;">
        <!-- 1. LOTE DIARIO ZOHO -->
        <div style="padding:14px;border-radius:12px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);">
          <div style="font-size:0.84rem;color:var(--champagne);margin-bottom:8px;">1 · Lote Diario de Correos (Tope Seguro: ${settings.daily_email_cap || 25}/día)</div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:8px;">
            <label style="font-size:0.68rem;color:var(--slate-muted);">Tope/Día <input type="number" id="daCapInput" class="glass-select-input" value="${settings.daily_email_cap || 25}" min="1" max="50"></label>
            <label style="font-size:0.68rem;color:var(--slate-muted);">MTY <input type="number" id="daMixMty" class="glass-select-input" value="${mix.mty ?? 10}" min="0" max="50"></label>
            <label style="font-size:0.68rem;color:var(--slate-muted);">Vallarta <input type="number" id="daMixPv" class="glass-select-input" value="${mix.pv ?? 10}" min="0" max="50"></label>
            <label style="font-size:0.68rem;color:var(--slate-muted);">Biogen <input type="number" id="daMixBio" class="glass-select-input" value="${mix.biogen ?? 5}" min="0" max="50"></label>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:10px;">
            <label style="font-size:0.72rem;color:var(--platinum);"><input type="checkbox" id="daAutoSendChk" ${settings.auto_send_enabled !== false ? 'checked' : ''}> Auto-enviar a las 09:15 CST</label>
            <button type="button" class="week-btn" style="font-size:0.7rem;" onclick="window.saveDailyAutomationSettingsNow()">Guardar Regla</button>
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">
            <button type="button" class="week-btn" onclick="window.prepareDailyBatchNow(true)">Escanear Webs + Armar Lote</button>
            <button type="button" class="btn-approve-trigger" onclick="window.dispatchDailyBatchNow()">${data.smtp_configured ? 'Enviar Lote Hoy por Zoho' : 'Generar Borradores .eml Hoy'}</button>
          </div>
          <div style="max-height:175px;overflow:auto;display:flex;flex-direction:column;gap:6px;">
            ${batchItems.length ? batchItems.map((it, idx) => `
              <div style="padding:8px;border-radius:8px;background:rgba(255,255,255,0.03);border:1px solid var(--glass-border-subtle);font-size:0.71rem;display:flex;justify-content:space-between;gap:8px;align-items:center;">
                <div style="min-width:0;">
                  <div style="color:var(--bone-white);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${esc(it.nombre)} <span style="color:var(--champagne);">[${esc(String(it.territory || '').toUpperCase())}]</span></div>
                  <div style="color:var(--slate-muted);font-size:0.67rem;">${esc(it.email)} · ${esc(it.ab_variant)} · <strong style="color:${it.status === 'sent_zoho' ? '#c2dec8' : '#dfcbb5'};">${esc(it.status)}</strong></div>
                </div>
                <button type="button" class="week-btn" style="padding:3px 7px;font-size:0.66rem;" onclick="window.copyDailyDraftByKey('batch_${idx}')">Copiar</button>
              </div>
            `).join('') : '<div style="font-size:0.73rem;color:var(--slate-muted);">Presiona "Escanear Webs + Armar Lote" para cargar los prospectos con correo listo hoy.</div>'}
          </div>
        </div>

        <!-- 2. SEGUIMIENTOS AUTOMATICOS 48H / 72H / DIA 7 -->
        <div style="padding:14px;border-radius:12px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
            <div style="font-size:0.84rem;color:var(--champagne);">2 · Seguimientos Vencidos (${due.length})</div>
            <button type="button" class="week-btn" style="font-size:0.7rem;" onclick="window.dispatchDueFollowupsNow()">Procesar Vencidos Hoy</button>
          </div>
          <div style="max-height:260px;overflow:auto;display:flex;flex-direction:column;gap:8px;">
            ${due.length ? due.slice(0, 10).map((f, idx) => `
              <div style="padding:9px;border-radius:8px;background:rgba(255,255,255,0.03);border:1px solid var(--glass-border-subtle);font-size:0.72rem;">
                <div style="display:flex;justify-content:space-between;gap:6px;margin-bottom:4px;">
                  <strong style="color:var(--bone-white);">${esc(f.nombre)}</strong>
                  <span style="color:var(--champagne);">${esc(f.current_stage)} &rarr; ${esc(f.next_stage)}</span>
                </div>
                <div style="color:var(--platinum);margin-bottom:6px;">${esc(f.message)}</div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;">
                  ${f.web_whatsapp_url ? `<a href="${esc(f.web_whatsapp_url)}" target="_blank" rel="noopener" class="btn-approve-trigger" style="text-decoration:none;font-size:0.68rem;padding:4px 8px;">WA Web 1-Clic &rarr;</a><button type="button" class="week-btn" style="font-size:0.68rem;padding:4px 8px;" onclick="window.confirmWaWebSent('${esc(f.slug)}','${esc(f.nombre)}','${esc(f.phone)}')">Marcar WA Enviado</button>` : ''}
                  <button type="button" class="week-btn" style="font-size:0.68rem;padding:4px 8px;" onclick="window.copyDailyDraftByKey('due_${idx}')">Copiar Mensaje</button>
                </div>
              </div>
            `).join('') : '<div style="font-size:0.73rem;color:var(--slate-muted);">Sin seguimientos vencidos en este momento. Cada envío por Zoho o WhatsApp programa su toque a 48h, 72h y Día 7.</div>'}
          </div>
        </div>
      </div>

      <div class="mvp-grid-layout">
        <!-- 3. CONCRETAR NEGOCIACIONES (OBJECIONES + CIERRE 50/50 + CAJA 612) -->
        <div style="padding:14px;border-radius:12px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);">
          <div style="font-size:0.84rem;color:var(--champagne);margin-bottom:8px;">3 · Mesa de Negociación &amp; Cierre 50/50 (PFAE 612)</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
            <input type="text" id="negNombreInput" class="glass-select-input" placeholder="Negocio / Prospecto que respondió">
            <select id="negOutcomeSelect" class="glass-select-input">
              <option value="objecion">Respondió con Objeción</option>
              <option value="pidio_cotizacion">Pidió Cotización / Datos</option>
              <option value="agendo_calendly">Agendó en Calendly</option>
              <option value="positivo">Interés Positivo</option>
              <option value="cerrado_anticipo">Cerrado · Cobró Anticipo 50%</option>
              <option value="no_interesado">Descartado</option>
            </select>
            <select id="negObjectionSelect" class="glass-select-input">
              ${Object.entries(playbooks).map(([k, lbl]) => `<option value="${esc(k)}">${esc(lbl)}</option>`).join('')}
            </select>
            <input type="number" id="negCollectedInput" class="glass-select-input" placeholder="Cobro MXN (solo si ya pagó 50%)" min="0" step="10" value="0">
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:8px;">
            <label style="font-size:0.71rem;color:var(--platinum);"><input type="checkbox" id="negPmChk"> Persona Moral (Retenciones 612)</label>
            <button type="button" class="btn-approve-trigger" onclick="window.submitNegotiationReplyNow()">Generar Respuesta / Registrar Cierre</button>
          </div>
          <div id="negResultBox" style="font-size:0.72rem;color:var(--platinum);">
            ${logs[0] ? `<div style="padding:8px;border-radius:8px;background:rgba(197,168,128,0.08);border:1px solid rgba(197,168,128,0.3);"><strong>${esc(logs[0].nombre)} (${esc(logs[0].new_stage)}):</strong> ${esc(logs[0].suggested_reply)}</div>` : ''}
          </div>
        </div>

        <!-- 4. ITERADOR DIARIO A/B -->
        <div style="padding:14px;border-radius:12px;background:rgba(0,0,0,0.28);border:1px solid var(--glass-border);">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
            <div style="font-size:0.84rem;color:var(--champagne);">4 · Iteración Diaria A/B (18:15 CST)</div>
            <button type="button" class="week-btn" style="font-size:0.7rem;" onclick="window.runIterationCycleNow()">Iterar &amp; Optimizar Ahora</button>
          </div>
          <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:10px;">
            ${Object.entries(variants).map(([vid, v]) => {
              const sent = Number(v.sent || 0);
              const rep = Number(v.replies || 0);
              const rate = sent ? ((rep / sent) * 100).toFixed(1) : '0.0';
              const isWin = iter.winner_variant_id === vid;
              return `
                <div style="padding:8px 10px;border-radius:8px;background:rgba(255,255,255,0.03);border:1px solid ${isWin ? 'rgba(197,168,128,0.55)' : 'var(--glass-border-subtle)'};font-size:0.71rem;display:flex;justify-content:space-between;gap:8px;">
                  <span style="color:var(--bone-white);">${isWin ? '★ ' : ''}${esc(v.label)} ${v.active === false ? '(Pausada)' : ''}</span>
                  <span style="font-family:var(--font-mono);color:var(--champagne-light);white-space:nowrap;">${sent} env · ${rep} resp (${rate}%) · ${v.closes || 0} cierres</span>
                </div>
              `;
            }).join('')}
          </div>
          <div style="font-size:0.71rem;color:var(--slate-muted);">
            ${(iter.recommendations || []).map((r) => `<div>• ${esc(r)}</div>`).join('') || 'Ejecuta la iteración al final del día para promover la variante ganadora al lote de mañana.'}
          </div>
        </div>
      </div>
    `;
  }

  window.copyDailyDraft = function (txt) {
    copyText(txt, 'Texto copiado al portapapeles.');
  };

  window.copyDailyDraftByKey = function (key) {
    const map = cmdState._copyMap || {};
    copyText(map[key] || '', 'Texto copiado al portapapeles.');
  };

  window.saveDailyAutomationSettingsNow = async function () {
    const daily_email_cap = Number(document.getElementById('daCapInput')?.value || 25);
    const auto_send_enabled = Boolean(document.getElementById('daAutoSendChk')?.checked);
    const territory_mix = {
      mty: Number(document.getElementById('daMixMty')?.value || 10),
      pv: Number(document.getElementById('daMixPv')?.value || 10),
      biogen: Number(document.getElementById('daMixBio')?.value || 5),
    };
    try {
      await apiJson('/api/growth/automation-settings', {
        method: 'POST',
        body: JSON.stringify({ auto_send_enabled, daily_email_cap, territory_mix }),
      });
      await window.loadGeoAndGrowthData(true);
      toast('Reglas del piloto diario guardadas.');
    } catch (err) {
      toast('Error Config Piloto: ' + err.message);
    }
  };

  window.prepareDailyBatchNow = async function (scanWebs = true) {
    toast('Escaneando sitios web y armando lote diario seguro...');
    try {
      const res = await apiJson('/api/growth/daily/prepare-batch', {
        method: 'POST',
        body: JSON.stringify({ scan_websites_first: scanWebs }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`Lote preparado con ${(res.batch.items || []).length} prospectos.`);
    } catch (err) {
      toast('Error Lote Diario: ' + err.message);
    }
  };

  window.dispatchDailyBatchNow = async function () {
    try {
      const res = await apiJson('/api/growth/daily/dispatch-batch', {
        method: 'POST',
        body: JSON.stringify({ dry_run: false }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`Lote procesado: ${res.sent_count} SMTP · ${res.eml_exported_count} borradores .eml`);
    } catch (err) {
      toast('Error Dispatch Lote: ' + err.message);
    }
  };

  window.dispatchDueFollowupsNow = async function () {
    try {
      const res = await apiJson('/api/growth/followups/dispatch', {
        method: 'POST',
        body: JSON.stringify({ channel: 'all', dry_run: false }),
      });
      await window.loadGeoAndGrowthData(true);
      toast(`Seguimientos: ${res.processed_due} procesados (${res.email_sent} SMTP · ${res.eml_saved} .eml · ${res.whatsapp_ready} WA).`);
    } catch (err) {
      toast('Error Seguimientos: ' + err.message);
    }
  };

  window.submitNegotiationReplyNow = async function () {
    const nombre = (document.getElementById('negNombreInput')?.value || '').trim();
    const outcome = document.getElementById('negOutcomeSelect')?.value || 'objecion';
    const objection_key = document.getElementById('negObjectionSelect')?.value || 'demo_y_cierre';
    const collected_mxn = Number(document.getElementById('negCollectedInput')?.value || 0);
    const client_is_persona_moral = Boolean(document.getElementById('negPmChk')?.checked);
    if (!nombre) {
      toast('Escribe el nombre del negocio que respondió.');
      return;
    }
    try {
      const res = await apiJson('/api/growth/negotiation/reply-and-close', {
        method: 'POST',
        body: JSON.stringify({
          slug: nombre.toLowerCase().replace(/[^a-z0-9]+/g, '_'),
          nombre,
          outcome,
          objection_key,
          collected_mxn,
          client_is_persona_moral,
        }),
      });
      await window.loadGeoAndGrowthData(true);
      const box = document.getElementById('negResultBox');
      if (box) {
        cmdState._copyMap = cmdState._copyMap || {};
        cmdState._copyMap['neg_latest'] = res.suggested_reply || '';
        box.innerHTML = `<div style="padding:9px;border-radius:8px;background:rgba(110,148,119,0.12);border:1px solid rgba(110,148,119,0.45);">
          <div style="margin-bottom:6px;"><strong>${esc(res.crm_record.nombre)} &rarr; ${esc(res.crm_record.stage)}</strong></div>
          <div style="margin-bottom:8px;">${esc(res.suggested_reply)}</div>
          <div style="display:flex;gap:6px;flex-wrap:wrap;">
            <button type="button" class="week-btn" style="font-size:0.68rem;" onclick="window.copyDailyDraftByKey('neg_latest')">Copiar Respuesta</button>
            ${res.web_whatsapp_url ? `<a href="${esc(res.web_whatsapp_url)}" target="_blank" rel="noopener" class="btn-approve-trigger" style="text-decoration:none;font-size:0.68rem;padding:4px 8px;">Enviar en WA Web &rarr;</a>` : ''}
          </div>
        </div>`;
      }
      toast(collected_mxn > 0 ? 'Cierre registrado y reflejado en Contador PFAE 612.' : 'Respuesta de negociación lista.');
    } catch (err) {
      toast('Error Negociación: ' + err.message);
    }
  };

  window.runIterationCycleNow = async function () {
    try {
      const res = await apiJson('/api/growth/iteration/run', { method: 'POST' });
      await window.loadGeoAndGrowthData(true);
      toast(`Iteración lista · Ganadora: ${res.report.winner_variant_id}`);
    } catch (err) {
      toast('Error Iteración: ' + err.message);
    }
  };

  window.renderGeoMapOnTabOpen = function () {
    if (!cmdState.geo || !cmdState.growth) {
      window.loadGeoAndGrowthData(true).then(() => {
        if (cmdState.leafletMap) setTimeout(() => cmdState.leafletMap.invalidateSize(), 120);
      });
    } else if (cmdState.leafletMap) {
      setTimeout(() => cmdState.leafletMap.invalidateSize(), 120);
    }
  };

  document.addEventListener('DOMContentLoaded', () => {
    window.loadGeoAndGrowthData(true);
  });
})();
