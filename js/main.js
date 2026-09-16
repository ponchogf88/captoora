/**
 * CAPTOORA STUDIO - MAIN INTERACTIVE LOGIC
 * Portfolio Filtering, Lightbox, Dynamic Quote Calculator & WhatsApp Deep Links
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initPortfolioFilter();
  initCalculator();
  initFaqAccordion();
  initSmoothScroll();
  initComparisonSlider();
});

/* ===================================================
   1. NAVBAR & MOBILE MENU
   =================================================== */
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const mobileToggle = document.getElementById('mobile-toggle');
  const navLinks = document.getElementById('nav-links');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.style.background = 'rgba(10, 11, 14, 0.95)';
      navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.5)';
    } else {
      navbar.style.background = 'rgba(10, 11, 14, 0.85)';
      navbar.style.boxShadow = 'none';
    }
  });

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
      const icon = mobileToggle.querySelector('i');
      if (navLinks.classList.contains('active')) {
        icon.className = 'fa-solid fa-xmark';
      } else {
        icon.className = 'fa-solid fa-bars-staggered';
      }
    });

    // Close menu when clicking any nav link
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        const icon = mobileToggle.querySelector('i');
        if (icon) icon.className = 'fa-solid fa-bars-staggered';
      });
    });
  }
}

/* ===================================================
   2. PORTFOLIO FILTER & LIGHTBOX
   =================================================== */
function initPortfolioFilter() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioItems = document.querySelectorAll('.portfolio-item');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active button
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      portfolioItems.forEach(item => {
        const itemCategory = item.getAttribute('data-category');

        if (filterValue === 'all' || itemCategory === filterValue) {
          item.style.display = 'block';
          setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'scale(1)';
          }, 50);
        } else {
          item.style.opacity = '0';
          item.style.transform = 'scale(0.95)';
          setTimeout(() => {
            item.style.display = 'none';
          }, 250);
        }
      });
    });
  });
}

// Lightbox Modal Controls
function openLightbox(btn) {
  const portfolioItem = btn.closest('.portfolio-item');
  const img = portfolioItem.querySelector('img');
  const title = portfolioItem.querySelector('.item-title').textContent;
  const category = portfolioItem.querySelector('.item-cat').textContent;

  const modal = document.getElementById('lightbox-modal');
  const modalImg = document.getElementById('lightbox-img');
  const caption = document.getElementById('lightbox-caption');

  modalImg.src = img.src;
  caption.innerHTML = `<span style="color:var(--accent-green);font-size:0.85rem;display:block;margin-bottom:4px;">${category}</span> ${title}`;
  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  const modal = document.getElementById('lightbox-modal');
  modal.classList.remove('active');
  document.body.style.overflow = '';
}

// Close lightbox on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeLightbox();
  }
});

/* ===================================================
   3. DYNAMIC QUOTE CALCULATOR
   =================================================== */
function initCalculator() {
  calculateQuote();
}

function updateSliderValue(val) {
  const sliderNum = document.getElementById('slider-num');
  const sliderUnit = document.getElementById('slider-unit');
  const selectedService = document.querySelector('input[name="calc-service"]:checked').value;

  sliderNum.textContent = val;

  if (selectedService === 'headshots') {
    sliderUnit.textContent = val == 1 ? 'persona' : 'personas';
  } else if (selectedService === 'gastronomica') {
    sliderUnit.textContent = val == 1 ? 'platillo / bebida' : 'platillos / bebidas';
  } else if (selectedService === 'producto') {
    sliderUnit.textContent = val == 1 ? 'producto / item' : 'productos / items';
  } else if (selectedService === 'corporativo') {
    sliderUnit.textContent = val == 1 ? 'colaborador' : 'colaboradores';
  }
}

function calculateQuote() {
  const serviceInput = document.querySelector('input[name="calc-service"]:checked');
  const locInput = document.querySelector('input[name="calc-loc"]:checked');
  const quantityInput = document.getElementById('calc-quantity');

  if (!serviceInput || !locInput || !quantityInput) return;

  const service = serviceInput.value;
  const loc = locInput.value;
  const qty = parseInt(quantityInput.value, 10) || 1;

  // Update slider label context
  const quantityLabel = document.getElementById('quantity-label');
  if (service === 'headshots') {
    quantityLabel.innerHTML = '<i class="fa-solid fa-users"></i> 2. Número de personas a retratar:';
  } else if (service === 'gastronomica') {
    quantityLabel.innerHTML = '<i class="fa-solid fa-utensils"></i> 2. Cantidad de platillos / cócteles en el menú:';
  } else if (service === 'producto') {
    quantityLabel.innerHTML = '<i class="fa-solid fa-box"></i> 2. Cantidad de productos a fotografiar:';
  } else if (service === 'corporativo') {
    quantityLabel.innerHTML = '<i class="fa-solid fa-building"></i> 2. Número de colaboradores del equipo:';
  }

  updateSliderValue(qty);

  let basePrice = 0;
  let serviceName = '';
  let features = [];

  // Service calculation rules
  switch (service) {
    case 'headshots':
      serviceName = `Headshot / Retrato Ejecutivo (${qty} ${qty == 1 ? 'persona' : 'personas'})`;
      if (qty === 1) {
        basePrice = 1450;
      } else {
        basePrice = 1450 + (qty - 1) * 650;
      }
      features = [
        `Sesión guiada de poses para ${qty} ${qty == 1 ? 'persona' : 'personas'}`,
        `${qty * 4} fotos finales con retoque digital de alta gama`,
        'Formatos optimizados para LinkedIn, Web y Prensa'
      ];
      break;

    case 'gastronomica':
      serviceName = `Fotografía Gastronómica (${qty} ${qty == 1 ? 'platillo' : 'platillos'})`;
      if (qty <= 5) {
        basePrice = 2900;
      } else {
        basePrice = 2900 + (qty - 5) * 220;
      }
      features = [
        `Estilismo y toma de ${qty} platillos/bebidas`,
        'Iluminación de estudio en restaurante o cocina',
        'Archivos de alta resolución para menú y apps delivery'
      ];
      break;

    case 'producto':
      serviceName = `Fotografía de Producto E-Commerce (${qty} ${qty == 1 ? 'ítem' : 'ítems'})`;
      if (qty <= 5) {
        basePrice = 2400;
      } else {
        basePrice = 2400 + (qty - 5) * 190;
      }
      features = [
        `Fondo blanco puro o fondo contextual para ${qty} productos`,
        'Tomas de ángulo, escala y detalles de empaque',
        'Resolución calibrada para Amazon, Mercado Libre y Shopify'
      ];
      break;

    case 'corporativo':
      serviceName = `Equipo Corporativo In-Company (${qty} ${qty == 1 ? 'colaborador' : 'colaboradores'})`;
      if (qty <= 5) {
        basePrice = 4500;
      } else {
        basePrice = 4500 + (qty - 5) * 400;
      }
      features = [
        `Estudio móvil en oficinas para ${qty} colaboradores`,
        'Retrato individual por colaborador + foto grupal',
        'Facturación fiscal y entrega ordenada en nube'
      ];
      break;
  }

  // Location fee
  let locFee = 0;
  if (loc === 'location') {
    locFee = 850; // Mobile studio setup fee
  }

  // Addons
  let addonsFee = 0;
  const addonMakeup = document.getElementById('addon-makeup')?.checked;
  const addonExpress = document.getElementById('addon-express')?.checked;
  const addonReels = document.getElementById('addon-reels')?.checked;

  if (addonMakeup) addonsFee += 850;
  if (addonExpress) addonsFee += 600;
  if (addonReels) addonsFee += 1200;

  const totalPrice = basePrice + locFee + addonsFee;

  // Update Summary DOM
  document.getElementById('summary-service-title').textContent = serviceName;
  document.getElementById('summary-total-price').textContent = totalPrice.toLocaleString('es-MX');

  const featuresContainer = document.getElementById('summary-features');
  if (featuresContainer) {
    featuresContainer.innerHTML = features.map(f => `<div><i class="fa-solid fa-check"></i> ${f}</div>`).join('');
    if (loc === 'location') {
      featuresContainer.innerHTML += `<div><i class="fa-solid fa-check"></i> Montaje de estudio móvil en tu locación</div>`;
    }
    if (addonMakeup) featuresContainer.innerHTML += `<div><i class="fa-solid fa-check"></i> Incluye Maquillaje y peinado profesional</div>`;
    if (addonExpress) featuresContainer.innerHTML += `<div><i class="fa-solid fa-check"></i> Entrega Express 24 hrs garantizada</div>`;
    if (addonReels) featuresContainer.innerHTML += `<div><i class="fa-solid fa-check"></i> 2 Videos Reels para Instagram / TikTok</div>`;
  }
}

function sendQuoteWhatsApp() {
  const serviceTitle = document.getElementById('summary-service-title').textContent;
  const totalPrice = document.getElementById('summary-total-price').textContent;
  const loc = document.querySelector('input[name="calc-loc"]:checked').value === 'location' ? 'En mi oficina / local' : 'En Estudio Captoora';
  
  let addons = [];
  if (document.getElementById('addon-makeup')?.checked) addons.push('Maquillaje profesional');
  if (document.getElementById('addon-express')?.checked) addons.push('Entrega Express 24h');
  if (document.getElementById('addon-reels')?.checked) addons.push('Videos Reels');
  
  const addonsText = addons.length > 0 ? addons.join(', ') : 'Ninguno';

  const message = `¡Hola Captoora! 👋\n\nAcabo de realizar una cotización en su sitio web oficial:\n` +
    `📸 *Servicio:* ${serviceTitle}\n` +
    `📍 *Locación:* ${loc}\n` +
    `✨ *Complementos:* ${addonsText}\n` +
    `💰 *Total Estimado:* $${totalPrice} MXN\n\n` +
    `Me gustaría consultar fechas disponibles para agendar. ¿Qué días tienen libres?`;

  const encoded = encodeURIComponent(message);
  const waUrl = `https://wa.me/528140050088?text=${encoded}`;
  window.open(waUrl, '_blank');
}

/* ===================================================
   4. CONTACT FORM TO WHATSAPP
   =================================================== */
function handleContactSubmit(e) {
  e.preventDefault();
  const form = document.getElementById('contact-form');
  const name = document.getElementById('c-name').value;
  const phone = document.getElementById('c-phone').value;
  const service = document.getElementById('c-service').value;
  const msg = document.getElementById('c-msg').value || 'Sin notas adicionales';

  const message = `¡Hola Captoora! 👋\n\n` +
    `Deseo consultar disponibilidad para una sesión fotográfica:\n` +
    `👤 *Nombre:* ${name}\n` +
    `📱 *WhatsApp:* ${phone}\n` +
    `🎯 *Servicio de interés:* ${service}\n` +
    `📝 *Detalles / Fecha tentativa:* ${msg}\n\n` +
    `Quedo atento a su respuesta. ¡Muchas gracias!`;

  const encoded = encodeURIComponent(message);
  const waUrl = `https://wa.me/528140050088?text=${encoded}`;
  window.open(waUrl, '_blank');
}

/* ===================================================
   5. FAQ ACCORDION
   =================================================== */
function initFaqAccordion() {
  // Handled by inline onclick or selector
}

function toggleFaq(btn) {
  const item = btn.closest('.accordion-item');
  const isActive = item.classList.contains('active');

  // Close all other items
  document.querySelectorAll('.accordion-item').forEach(i => i.classList.remove('active'));

  if (!isActive) {
    item.classList.add('active');
  }
}

/* ===================================================
   6. HELPER TO FILTER PACKAGES BY LINK
   =================================================== */
function filterPackage(category) {
  const cards = document.querySelectorAll('.pricing-card');
  cards.forEach(card => {
    const pkgType = card.getAttribute('data-package');
    if (category === 'all' || pkgType === category) {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0) scale(1.02)';
      setTimeout(() => {
        card.style.transform = '';
      }, 600);
    } else {
      card.style.opacity = '0.4';
      setTimeout(() => {
        card.style.opacity = '1';
      }, 1800);
    }
  });
}

function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

/* ===================================================
   7. INTERACTIVE BEFORE / AFTER RETOUCH SLIDER
   =================================================== */
function initComparisonSlider() {
  const container = document.getElementById('comparison-box');
  const overlay = document.getElementById('img-after-overlay');
  const divider = document.getElementById('slider-divider');

  if (!container || !overlay || !divider) return;

  let isDragging = false;

  function moveSlider(clientX) {
    const rect = container.getBoundingClientRect();
    let x = clientX - rect.left;
    if (x < 0) x = 0;
    if (x > rect.width) x = rect.width;

    const percentage = (x / rect.width) * 100;
    overlay.style.width = `${percentage}%`;
    divider.style.left = `${percentage}%`;
  }

  // Mouse Events
  container.addEventListener('mousedown', (e) => {
    isDragging = true;
    moveSlider(e.clientX);
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    moveSlider(e.clientX);
  });

  // Touch Events for Mobile
  container.addEventListener('touchstart', (e) => {
    isDragging = true;
    if (e.touches.length > 0) {
      moveSlider(e.touches[0].clientX);
    }
  }, { passive: true });

  window.addEventListener('touchend', () => {
    isDragging = false;
  });

  window.addEventListener('touchmove', (e) => {
    if (!isDragging) return;
    if (e.touches.length > 0) {
      moveSlider(e.touches[0].clientX);
    }
  }, { passive: true });
}

/* ===================================================
   8. REEL SOUND TOGGLE
   =================================================== */
function toggleReelSound(btn) {
  const card = btn.closest('.reel-card');
  const video = card.querySelector('video');
  if (!video) return;

  video.muted = !video.muted;
  const icon = btn.querySelector('i');
  if (video.muted) {
    icon.className = 'fa-solid fa-volume-xmark';
  } else {
    icon.className = 'fa-solid fa-volume-high';
    video.play();
  }
}

/* ===================================================
   9. MURO DINÁMICO STREAM CARD LIGHTBOX
   =================================================== */
function openStreamCard(card) {
  const img = card.querySelector('img');
  const title = card.querySelector('h5')?.textContent || 'Fotografía de Producción';
  const tag = card.querySelector('.stream-tag')?.textContent || 'Captoora';
  const spec = card.querySelector('small')?.textContent || '';

  const modal = document.getElementById('lightbox-modal');
  const modalImg = document.getElementById('lightbox-img');
  const caption = document.getElementById('lightbox-caption');

  if (modal && modalImg && caption && img) {
    modalImg.src = img.src;
    caption.innerHTML = `<span style="color:var(--accent-green);font-size:0.85rem;display:block;margin-bottom:4px;">${tag} ${spec ? '• ' + spec : ''}</span> ${title}`;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

