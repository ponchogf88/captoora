// Captoora Studio - Event Curator & Processor Frontend Logic
let appState = {
  items: [],
  currentIndex: null,
  activeFilter: 'all',
  activePresetId: 'transicion_equilibrada',
  recipe: {
    temp: 2,
    tint: 1,
    exposure: 0.10,
    highlights: -10,
    shadows: 15,
    denoise: 5,
    sharpness: 20
  },
  presets: {}
};

// Elementos DOM
const galleryGrid = document.getElementById('gallery-grid');
const countYes = document.getElementById('count-yes');
const countReview = document.getElementById('count-review');
const countNo = document.getElementById('count-no');
const countTotal = document.getElementById('count-total');

const inputFolder = document.getElementById('input-folder');
const outputFolder = document.getElementById('output-folder');
const clientTag = document.getElementById('client-tag');
const btnScan = document.getElementById('btn-scan');

// Modales
const inspectorModal = document.getElementById('inspector-modal');
const modalFilename = document.getElementById('modal-filename');
const modalBadges = document.getElementById('modal-badges');
const imgBefore = document.getElementById('img-before');
const imgAfter = document.getElementById('img-after');
const splitOverlay = document.getElementById('split-overlay');
const sliderHandle = document.getElementById('slider-handle');
const sliderContainer = document.getElementById('slider-container');
const noticeDesc = document.getElementById('notice-desc');

const exportModal = document.getElementById('export-modal');
const btnOpenExport = document.getElementById('btn-open-export');
const btnCloseExport = document.getElementById('btn-close-export');
const btnCancelExport = document.getElementById('btn-cancel-export');
const btnRunExport = document.getElementById('btn-run-export');
const finalExportPath = document.getElementById('final-export-path');
const expCountYes = document.getElementById('exp-count-yes');
const expCountReview = document.getElementById('exp-count-review');
const expCountNo = document.getElementById('exp-count-no');
const exportProgress = document.getElementById('export-progress');

// Controles de ajuste
const sliderTemp = document.getElementById('slider-temp');
const sliderTint = document.getElementById('slider-tint');
const sliderExp = document.getElementById('slider-exp');
const sliderHl = document.getElementById('slider-hl');
const sliderShadows = document.getElementById('slider-shadows');
const sliderDenoise = document.getElementById('slider-denoise');
const sliderSharpness = document.getElementById('slider-sharpness');

const valTemp = document.getElementById('val-temp');
const valTint = document.getElementById('val-tint');
const valExp = document.getElementById('val-exp');
const valHl = document.getElementById('val-hl');
const valShadows = document.getElementById('val-shadows');
const valDenoise = document.getElementById('val-denoise');
const valSharpness = document.getElementById('val-sharpness');

// Inicialización
document.addEventListener('DOMContentLoaded', async () => {
  await fetchStatus();
  setupEventListeners();
  setupKeyboardShortcuts();
});

async function fetchStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    if (data.presets) appState.presets = data.presets;
    if (data.input_folder) inputFolder.value = data.input_folder;
    if (data.output_folder) outputFolder.value = data.output_folder;
    if (data.client_tag) clientTag.value = data.client_tag;
    if (data.active_recipe) {
      appState.recipe = { ...data.active_recipe };
      syncSlidersWithState();
    }
    if (data.total_items > 0) {
      const itemsRes = await fetch('/api/items');
      const itemsData = await itemsRes.json();
      appState.items = itemsData.items;
      renderGallery();
      updateCounters();
    }
  } catch (err) {
    console.error('Error cargando estado inicial:', err);
  }
}

function setupEventListeners() {
  // Cargar carpeta
  btnScan.addEventListener('click', scanFolder);

  // Filtros
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      appState.activeFilter = e.target.dataset.filter;
      renderGallery();
    });
  });

  // Presets
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      const pKey = e.target.dataset.preset;
      applyPreset(pKey);
    });
  });

  // Modal Inspector
  document.getElementById('btn-close-modal').addEventListener('click', closeModal);
  document.getElementById('btn-prev-photo').addEventListener('click', () => navigateModal(-1));
  document.getElementById('btn-next-photo').addEventListener('click', () => navigateModal(1));

  // Decisiones modal
  document.getElementById('btn-dec-yes').addEventListener('click', () => setDecision(appState.currentIndex, 'yes'));
  document.getElementById('btn-dec-review').addEventListener('click', () => setDecision(appState.currentIndex, 'review'));
  document.getElementById('btn-dec-no').addEventListener('click', () => setDecision(appState.currentIndex, 'no'));

  // Split slider Before/After
  setupSplitSlider();

  // Sliders de ajuste con debounce
  [sliderTemp, sliderTint, sliderExp, sliderHl, sliderShadows, sliderDenoise, sliderSharpness].forEach(sl => {
    sl.addEventListener('input', debounce(onSliderChange, 200));
  });

  // Aplicar receta a todo el lote
  document.getElementById('btn-apply-batch').addEventListener('click', applyRecipeToAll);

  // Guardar y Cargar Recetas JSON
  document.getElementById('btn-save-recipe').addEventListener('click', promptSaveRecipe);
  document.getElementById('btn-load-recipe').addEventListener('click', showLoadRecipeDialog);

  // Modal Exportar
  btnOpenExport.addEventListener('click', openExportModal);
  btnCloseExport.addEventListener('click', closeExportModal);
  btnCancelExport.addEventListener('click', closeExportModal);
  btnRunExport.addEventListener('click', executeExport);
}

// Escanear carpeta
async function scanFolder() {
  const inDir = inputFolder.value.trim();
  const outDir = outputFolder.value.trim();
  const cTag = clientTag.value.trim() || 'EVENTO';

  if (!inDir) {
    alert('Ingresa la ruta de la carpeta de fotos.');
    return;
  }

  btnScan.textContent = '⏳ Escaneando y analizando...';
  btnScan.disabled = true;

  try {
    const res = await fetch('/api/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input_folder: inDir, output_folder: outDir, client_tag: cTag })
    });
    const data = await res.json();
    if (data.error) {
      alert(data.error);
    } else {
      appState.items = data.items;
      renderGallery();
      updateCounters();
    }
  } catch (err) {
    alert('Error al escanear la carpeta: ' + err);
  } finally {
    btnScan.textContent = '⚡ Cargar Carpeta';
    btnScan.disabled = false;
  }
}

// Renderizado del Grid
function renderGallery() {
  galleryGrid.innerHTML = '';

  const filtered = appState.items.filter(item => {
    if (appState.activeFilter === 'all') return true;
    if (appState.activeFilter === 'yes') return item.decision === 'yes';
    if (appState.activeFilter === 'review') return item.decision === 'review';
    if (appState.activeFilter === 'no') return item.decision === 'no';
    if (appState.activeFilter === 'burst') return item.is_burst_duplicate;
    return true;
  });

  if (filtered.length === 0) {
    galleryGrid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">📂</div>
        <h2>Sin fotos en esta vista</h2>
        <p>No se encontraron fotografías bajo el filtro activo.</p>
      </div>`;
    return;
  }

  filtered.forEach(item => {
    const card = document.createElement('div');
    card.className = `photo-card selected-${item.decision || 'pending'}`;
    card.dataset.index = item.index;

    // Estampilla de decisión
    let stampHtml = '';
    if (item.decision === 'yes') stampHtml = '<span class="card-decision-stamp stamp-yes">SÍ (Aprobada)</span>';
    else if (item.decision === 'review') stampHtml = '<span class="card-decision-stamp stamp-review">REVISAR (Espontánea)</span>';
    else if (item.decision === 'no') stampHtml = '<span class="card-decision-stamp stamp-no">NO (Descarte)</span>';

    // Badges de análisis
    const sharpBadge = `<span class="badge badge-${item.sharpness.badge}">Nitidez: ${item.sharpness.score} (${item.sharpness.label})</span>`;
    const expBadge = `<span class="badge badge-${item.exposure.badge}">${item.exposure.label}</span>`;
    const burstBadge = item.is_burst_duplicate ? `<span class="badge badge-warning">🔄 Ráfaga duplicada</span>` : '';
    const eyesBadge = item.eyes.blink_suspected ? `<span class="badge badge-danger">⚠️ Parpadeo?</span>` : (item.eyes.faces_detected > 0 ? `<span class="badge badge-info">👤 ${item.eyes.faces_detected} rostro(s)</span>` : '');

    card.innerHTML = `
      <div class="card-thumb-wrap">
        <img class="card-thumb" src="/api/thumb?path=${encodeURIComponent(item.graded_thumb)}&t=${Date.now()}" alt="${item.filename}" loading="lazy">
        ${stampHtml}
      </div>
      <div class="card-info">
        <div class="card-title-row">
          <span class="card-filename">${item.filename}</span>
        </div>
        <div class="card-badges">
          ${sharpBadge}
          ${expBadge}
          ${eyesBadge}
          ${burstBadge}
        </div>
        <div class="card-btn-bar">
          <button class="card-action-btn ${item.decision === 'yes' ? 'active-yes' : ''}" data-act="yes">✅ Sí</button>
          <button class="card-action-btn ${item.decision === 'review' ? 'active-review' : ''}" data-act="review">⚠️ Revisar</button>
          <button class="card-action-btn ${item.decision === 'no' ? 'active-no' : ''}" data-act="no">❌ No</button>
        </div>
      </div>
    `;

    // Click en la tarjeta abre el inspector
    card.querySelector('.card-thumb-wrap').addEventListener('click', () => openModal(item.index));
    card.querySelector('.card-title-row').addEventListener('click', () => openModal(item.index));

    // Botones rápidos de decisión en tarjeta
    card.querySelectorAll('.card-action-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        setDecision(item.index, btn.dataset.act);
      });
    });

    galleryGrid.appendChild(card);
  });
}

function updateCounters() {
  const yes = appState.items.filter(i => i.decision === 'yes').length;
  const review = appState.items.filter(i => i.decision === 'review').length;
  const no = appState.items.filter(i => i.decision === 'no').length;
  countYes.textContent = yes;
  countReview.textContent = review;
  countNo.textContent = no;
  countTotal.textContent = appState.items.length;
}

// Modal Inspector
function openModal(index) {
  if (index < 0 || index >= appState.items.length) return;
  appState.currentIndex = index;
  const item = appState.items[index];

  modalFilename.textContent = item.filename;
  imgBefore.src = `/api/thumb?path=${encodeURIComponent(item.raw_thumb)}&t=${Date.now()}`;
  imgAfter.src = `/api/thumb?path=${encodeURIComponent(item.graded_thumb)}&t=${Date.now()}`;

  // Reseteo slider 50%
  splitOverlay.style.width = '50%';
  sliderHandle.style.left = '50%';

  // Badges modal
  modalBadges.innerHTML = `
    <span class="badge badge-${item.sharpness.badge}">Nitidez: ${item.sharpness.score} (${item.sharpness.label})</span>
    <span class="badge badge-${item.exposure.badge}">${item.exposure.label}</span>
    <span class="badge badge-info">${item.eyes.label}</span>
    ${item.is_burst_duplicate ? '<span class="badge badge-warning">🔄 Parte de ráfaga continua</span>' : ''}
  `;

  // Explicación de la Realidad Óptica de Nitidez
  let optText = '';
  if (item.sharpness.is_severely_blurred) {
    optText = `⚠️ <strong>Desenfoque óptico fuerte (${item.sharpness.score}):</strong> Esta foto presenta movimiento pronunciado o foco perdido en origen. Unsharp mask sólo puede elevar el micro-contraste existente; no es posible "re-enfocar" ópticamente sin inventar rasgos con IA generativa (estrictamente prohibido). Si la expresión emocional es irrepetible o espontánea, márcala como <strong>"REVISAR"</strong> para entrega especial con ambiente real.`;
  } else if (item.sharpness.score < 50) {
    optText = `ℹ️ <strong>Nitidez suave / movimiento natural (${item.sharpness.score}):</strong> El sujeto conserva su expresión viva. El realce de micro-contraste calibrado (+${appState.recipe.sharpness}%) define bordes sin generar artefactos ni alterar la textura de la piel.`;
  } else {
    optText = `✅ <strong>Óptica nítida (${item.sharpness.score}):</strong> Excelente micro-contraste en el plano focal. Texturas de cabello, ojos y vestimenta 100% fidedignas.`;
  }
  noticeDesc.innerHTML = optText;

  inspectorModal.classList.remove('hidden');
}

function closeModal() {
  inspectorModal.classList.add('hidden');
}

function navigateModal(step) {
  if (appState.currentIndex === null) return;
  const next = appState.currentIndex + step;
  if (next >= 0 && next < appState.items.length) {
    openModal(next);
  }
}

// Split slider interactivo
function setupSplitSlider() {
  let isDragging = false;

  const onMove = (e) => {
    if (!isDragging) return;
    const rect = sliderContainer.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    let x = clientX - rect.left;
    x = Math.max(0, Math.min(x, rect.width));
    const percent = (x / rect.width) * 100;
    splitOverlay.style.width = `${percent}%`;
    sliderHandle.style.left = `${percent}%`;
  };

  sliderContainer.addEventListener('mousedown', (e) => { isDragging = true; onMove(e); });
  window.addEventListener('mouseup', () => { isDragging = false; });
  window.addEventListener('mousemove', onMove);

  sliderContainer.addEventListener('touchstart', (e) => { isDragging = true; onMove(e); });
  window.addEventListener('touchend', () => { isDragging = false; });
  window.addEventListener('touchmove', onMove);
}

// Decisión de selección
async function setDecision(index, decision) {
  if (index === null || index < 0 || index >= appState.items.length) return;
  appState.items[index].decision = decision;

  try {
    await fetch('/api/decision', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ index, decision })
    });
  } catch (err) {
    console.error('Error guardando decisión:', err);
  }

  updateCounters();
  renderGallery();

  // Avanzar a la siguiente foto automáticamente en el modal
  if (!inspectorModal.classList.contains('hidden')) {
    if (index + 1 < appState.items.length) {
      openModal(index + 1);
    }
  }
}

// Presets
function applyPreset(presetKey) {
  const p = appState.presets[presetKey];
  if (!p) return;
  appState.activePresetId = presetKey;
  appState.recipe = {
    temp: p.temp,
    tint: p.tint,
    exposure: p.exposure,
    highlights: p.highlights,
    shadows: p.shadows,
    denoise: p.denoise,
    sharpness: p.sharpness
  };
  syncSlidersWithState();
  onSliderChange();
}

function syncSlidersWithState() {
  sliderTemp.value = appState.recipe.temp;
  valTemp.textContent = appState.recipe.temp > 0 ? `+${appState.recipe.temp}` : appState.recipe.temp;

  sliderTint.value = appState.recipe.tint;
  valTint.textContent = appState.recipe.tint > 0 ? `+${appState.recipe.tint}` : appState.recipe.tint;

  sliderExp.value = appState.recipe.exposure;
  valExp.textContent = (appState.recipe.exposure >= 0 ? '+' : '') + appState.recipe.exposure.toFixed(2);

  sliderHl.value = appState.recipe.highlights;
  valHl.textContent = `${appState.recipe.highlights}%`;

  sliderShadows.value = appState.recipe.shadows;
  valShadows.textContent = `${appState.recipe.shadows}%`;

  sliderDenoise.value = appState.recipe.denoise;
  valDenoise.textContent = appState.recipe.denoise;

  sliderSharpness.value = appState.recipe.sharpness;
  valSharpness.textContent = appState.recipe.sharpness;
}

// Actualización de sliders de revelado
async function onSliderChange() {
  appState.recipe.temp = parseInt(sliderTemp.value);
  appState.recipe.tint = parseInt(sliderTint.value);
  appState.recipe.exposure = parseFloat(sliderExp.value);
  appState.recipe.highlights = parseInt(sliderHl.value);
  appState.recipe.shadows = parseInt(sliderShadows.value);
  appState.recipe.denoise = parseInt(sliderDenoise.value);
  appState.recipe.sharpness = parseInt(sliderSharpness.value);
  syncSlidersWithState();

  // Enviar cambio al backend para la foto actual en el modal
  if (appState.currentIndex !== null) {
    try {
      await fetch('/api/update_recipe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          settings: appState.recipe,
          target_index: appState.currentIndex,
          apply_to_all: false
        })
      });
      // Refrescar imagen con timestamp
      const item = appState.items[appState.currentIndex];
      imgAfter.src = `/api/thumb?path=${encodeURIComponent(item.graded_thumb)}&t=${Date.now()}`;
    } catch (err) {
      console.error('Error actualizando previsualización:', err);
    }
  }
}

// Aplicar receta a todo el lote
async function applyRecipeToAll() {
  if (!confirm('¿Deseas aplicar esta receta de revelado a todas las fotos del lote?')) return;
  const btn = document.getElementById('btn-apply-batch');
  btn.textContent = '⏳ Renderizando vistas previas...';
  btn.disabled = true;

  try {
    await fetch('/api/update_recipe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        settings: appState.recipe,
        apply_to_all: true
      })
    });
    renderGallery();
    if (appState.currentIndex !== null) {
      const item = appState.items[appState.currentIndex];
      imgAfter.src = `/api/thumb?path=${encodeURIComponent(item.graded_thumb)}&t=${Date.now()}`;
    }
    alert('✨ Receta aplicada a todo el lote con éxito.');
  } catch (err) {
    alert('Error aplicando receta al lote: ' + err);
  } finally {
    btn.textContent = '✨ Aplicar esta receta a todo el lote';
    btn.disabled = false;
  }
}

// Guardar receta JSON
async function promptSaveRecipe() {
  const name = prompt('Nombre para la receta (ej. glowttery_amapola_tarde):', 'receta_evento_personalizada');
  if (!name) return;
  try {
    const res = await fetch('/api/save_recipe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, settings: appState.recipe })
    });
    const data = await res.json();
    alert('✅ Receta guardada exitosamente en:\n' + data.saved_file);
  } catch (err) {
    alert('Error guardando receta: ' + err);
  }
}

// Cargar receta JSON
async function showLoadRecipeDialog() {
  try {
    const res = await fetch('/api/recipes');
    const data = await res.json();
    if (!data.recipes || data.recipes.length === 0) {
      alert('Aún no hay recetas guardadas.');
      return;
    }
    const names = data.recipes.map((r, i) => `${i + 1}. ${r.filename}`).join('\n');
    const pick = prompt(`Selecciona el número de la receta a cargar:\n${names}`);
    const num = parseInt(pick);
    if (!isNaN(num) && num >= 1 && num <= data.recipes.length) {
      const chosen = data.recipes[num - 1].data.settings;
      appState.recipe = { ...chosen };
      syncSlidersWithState();
      onSliderChange();
      alert(`Receta "${data.recipes[num - 1].filename}" cargada.`);
    }
  } catch (err) {
    alert('Error cargando recetas: ' + err);
  }
}

// Exportación
function openExportModal() {
  const yes = appState.items.filter(i => i.decision === 'yes').length;
  const review = appState.items.filter(i => i.decision === 'review').length;
  const no = appState.items.filter(i => i.decision === 'no').length;

  if (yes === 0 && review === 0) {
    alert('Aún no has marcado ninguna foto como "Sí" o "Revisar". Selecciona al menos una foto antes de exportar.');
    return;
  }

  expCountYes.textContent = yes;
  expCountReview.textContent = review;
  expCountNo.textContent = no;
  finalExportPath.value = outputFolder.value.trim() || '/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/CURATED_EVENT';
  exportProgress.classList.add('hidden');
  btnRunExport.disabled = false;
  exportModal.classList.remove('hidden');
}

function closeExportModal() {
  exportModal.classList.add('hidden');
}

async function executeExport() {
  const targetPath = finalExportPath.value.trim();
  const cTag = clientTag.value.trim() || 'EVENTO';
  if (!targetPath) {
    alert('Especifica una carpeta destino.');
    return;
  }

  btnRunExport.disabled = true;
  exportProgress.classList.remove('hidden');

  try {
    const res = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        output_folder: targetPath,
        client_tag: cTag
      })
    });
    const data = await res.json();
    if (data.status === 'ok') {
      alert(`🎉 ¡Exportación completada con éxito!\n\nTotal procesadas: ${data.report.total_procesadas}\nAprobadas: ${data.report.aprobadas}\nRevisar/Espontáneas: ${data.report.para_revisar}\n\nCarpeta: ${targetPath}`);
      closeExportModal();
    } else {
      alert('Error en exportación: ' + data.error);
    }
  } catch (err) {
    alert('Error ejecutando exportación: ' + err);
  } finally {
    btnRunExport.disabled = false;
    exportProgress.classList.add('hidden');
  }
}

// Atajos de teclado para selección a velocidad de ráfaga
function setupKeyboardShortcuts() {
  window.addEventListener('keydown', (e) => {
    // Si el usuario está escribiendo en un input, ignorar atajos
    if (e.target.tagName === 'INPUT') return;

    if (!inspectorModal.classList.contains('hidden')) {
      if (e.key === 'ArrowLeft') {
        navigateModal(-1);
      } else if (e.key === 'ArrowRight') {
        navigateModal(1);
      } else if (e.key === '1') {
        setDecision(appState.currentIndex, 'yes');
      } else if (e.key === '2') {
        setDecision(appState.currentIndex, 'review');
      } else if (e.key === '3') {
        setDecision(appState.currentIndex, 'no');
      } else if (e.key === 'Escape') {
        closeModal();
      }
    }
  });
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}
