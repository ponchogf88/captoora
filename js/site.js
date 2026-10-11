(function () {
  var C = window.CAPTOORA || {};
  var wa = function (msg) { return "https://wa.me/" + C.whatsapp + (msg ? "?text=" + encodeURIComponent(msg) : ""); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); };
  var mark = function (s) { return esc(s).replace(/\[PENDIENTE\]/g, '<mark class="todo">PENDIENTE</mark>'); };

  // WhatsApp links
  document.querySelectorAll("[data-wa]").forEach(function (a) { a.href = wa(a.getAttribute("data-wa")); });

  // Evento
  var ev = C.event || {};
  var evSec = document.getElementById("evento");
  if (ev.show === false && evSec) { evSec.remove(); document.querySelectorAll('a[href="#evento"]').forEach(function (a) { a.remove(); }); }
  document.querySelectorAll("[data-ev]").forEach(function (el) {
    var k = el.getAttribute("data-ev"); if (ev[k] != null) el.innerHTML = mark(ev[k]);
  });
  var cta = document.getElementById("ev-cta");
  if (cta) { cta.href = wa(ev.waMessage); if (ev.ctaText) cta.textContent = ev.ctaText; }
  var map = document.getElementById("ev-map"); if (map && ev.mapsUrl) map.href = ev.mapsUrl;

  // Paquetes
  var dep = document.getElementById("deposit"); if (dep && C.deposit) dep.textContent = C.deposit;
  var pk = document.getElementById("packages");
  if (pk && C.packages) {
    var money = function (n) { return "$" + Number(n).toLocaleString("es-MX"); };
    pk.innerHTML = C.packages.map(function (p) {
      var msg = p.waMessage || ("Hola Captoora, quiero " + p.name + (p.price ? " (" + money(p.price) + ")" : "") + ".");
      var cls = "pk__card" + (p.featured ? " pk__card--hot" : "") + (p.secondary ? " pk__card--alt" : "");
      var price = p.price != null
        ? '<p class="pk__price">' + (p.regularPrice ? '<s class="pk__old">' + money(p.regularPrice) + "</s>" : "") +
          "<span>" + money(p.price) + "</span><small>MXN · " + esc(p.unit) + "</small></p>"
        : '<p class="pk__price pk__price--ask"><span>' + esc(p.priceLabel || "Precio por WhatsApp") + "</span></p>";
      return '<article class="' + cls + '">' +
        (p.badge ? '<span class="pk__badge">' + esc(p.badge) + "</span>" : "") +
        '<h3 class="pk__name">' + esc(p.name) + "</h3>" +
        (p.promoLabel ? '<p class="pk__promo">' + esc(p.promoLabel) + "</p>" : "") +
        price +
        (p.desc ? '<p class="pk__desc">' + esc(p.desc) + "</p>" : "") +
        "<ul>" + p.items.map(function (i) { return "<li>" + esc(i) + "</li>"; }).join("") + "</ul>" +
        '<a class="btn ' + (p.featured ? "btn--lime" : p.secondary ? "btn--outline-lime" : "btn--ghost") + ' btn--block" target="_blank" rel="noopener" href="' + wa(msg) + '">' +
        (p.cta || "Apartar por WhatsApp") + "</a>" +
        "</article>";
    }).join("");
  }

  // Redes
  var so = document.getElementById("social");
  if (so && C.social) so.innerHTML = C.social.map(function (s) {
    return '<li><a href="' + s.url + '" target="_blank" rel="noopener"><span>' + esc(s.label) + "</span>" + esc(s.handle) + "</a></li>";
  }).join("");

  // Medios: se guardan como texto base64 (el repo se publica solo con texto)
  var getText = function (url) { return fetch(url).then(function (r) { if (!r.ok) throw 0; return r.text(); }); };
  var imgs = null;
  var asImg = function (key) {
    if (/\.b64$/.test(key)) return getText(key).then(function (t) { return "data:image/jpeg;base64," + t.trim(); });
    imgs = imgs || fetch("assets/media/images.json").then(function (r) { if (!r.ok) throw 0; return r.json(); });
    return imgs.then(function (m) { if (!m[key]) throw 0; return "data:image/jpeg;base64," + m[key]; });
  };
  var asVideo = function (url) {
    return getText(url).then(function (t) {
      var bin = atob(t.trim()), n = bin.length, u = new Uint8Array(n);
      for (var i = 0; i < n; i++) u[i] = bin.charCodeAt(i);
      return URL.createObjectURL(new Blob([u], { type: "video/mp4" }));
    });
  };
  var play = function (vid) { var p = vid.play(); if (p && p.catch) p.catch(function () {}); };
  var loadVideo = function (vid, src, poster) {
    if (poster) asImg(poster).then(function (d) { if (!vid.currentSrc) vid.poster = d; }).catch(function () {});
    asVideo(src).then(function (b) { vid.src = b; vid.classList.add("is-ready"); play(vid); }).catch(function () {});
  };
  var v = document.getElementById("hero-video");
  if (v && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var tall = window.matchMedia("(max-aspect-ratio: 1/1)").matches;
    loadVideo(v, tall ? v.dataset.b64Tall : v.dataset.b64Wide, tall ? v.dataset.posterTall : v.dataset.posterWide);
  }
  document.querySelectorAll("video[data-b64]").forEach(function (vid) {
    var go = function () { loadVideo(vid, vid.dataset.b64, vid.dataset.poster); };
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { io.disconnect(); go(); } }, { rootMargin: "400px" });
      io.observe(vid);
    } else go();
  });
  document.querySelectorAll("img[data-img]").forEach(function (img) {
    asImg(img.dataset.img).then(function (d) { img.src = d; img.classList.add("is-ready"); }).catch(function () {});
  });

  // Escenarios
  var sc = document.getElementById("scenarios");
  var list = (C.scenarios || []).filter(function (x) { return x.show; });
  if (sc && list.length) {
    sc.classList.add("esc__grid--" + list.length);
    sc.innerHTML = list.map(function (x, i) {
      return '<article class="esc__card">' +
        '<figure class="esc__img"><img data-esc="' + i + '" alt="' + esc(x.alt || x.name) + '"></figure>' +
        '<div class="esc__body"><h3 class="esc__name">' + esc(x.name) + "</h3>" +
        (x.desc ? '<p class="esc__desc">' + esc(x.desc) + "</p>" : "") +
        (x.items && x.items.length ? '<ul class="esc__tags">' + x.items.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ul>" : "") +
        (x.note ? '<p class="esc__note">' + esc(x.note) + "</p>" : "") +
        '<a class="btn btn--lime" target="_blank" rel="noopener" href="' + wa(x.waMessage) + '">' + esc(x.cta || "Agendar por WhatsApp") + "</a></div></article>";
    }).join("");
    list.forEach(function (x, i) {
      var img = sc.querySelector('img[data-esc="' + i + '"]');
      if (img && x.image) asImg(x.image).then(function (d) { img.src = d; img.classList.add("is-ready"); }).catch(function () {});
    });
  } else if (sc) {
    var secEl = document.getElementById("escenarios"); if (secEl) secEl.remove();
    document.querySelectorAll('a[href="#escenarios"]').forEach(function (a) { a.remove(); });
  }

  // Portafolio (grid + filtros + lightbox)
  var pg = document.getElementById("portfolio");
  var items = C.portfolio || [];
  if (pg && items.length) {
    var cats = C.portfolioCats || [];
    var catLabel = function (k) { for (var i = 0; i < cats.length; i++) if (cats[i].key === k) return cats[i].label; return ""; };
    pg.innerHTML = items.map(function (x, i) {
      return '<figure class="pf__item" data-cat="' + esc(x.cat) + '" style="aspect-ratio:' + (x.w || 4) + "/" + (x.h || 5) + '">' +
        '<button type="button" class="pf__open" data-i="' + i + '" aria-label="Ver foto: ' + esc(x.alt) + '">' +
        '<img data-pf="' + i + '" alt="' + esc(x.alt) + '"></button>' +
        '<span class="pf__tag">' + esc(catLabel(x.cat)) + "</span></figure>";
    }).join("");
    var fl = document.getElementById("pf-filters");
    var used = cats.filter(function (c) { return items.some(function (x) { return x.cat === c.key; }); });
    if (fl && used.length > 1) {
      fl.innerHTML = '<button type="button" class="is-on" data-f="">Todo</button>' + used.map(function (c) {
        return '<button type="button" data-f="' + esc(c.key) + '">' + esc(c.label) + "</button>"; }).join("");
      fl.addEventListener("click", function (e) {
        var b = e.target.closest("button"); if (!b) return;
        fl.querySelectorAll("button").forEach(function (x) { x.classList.toggle("is-on", x === b); });
        pg.querySelectorAll(".pf__item").forEach(function (f) { f.hidden = !!b.dataset.f && f.dataset.cat !== b.dataset.f; });
      });
    } else if (fl) fl.remove();
    var srcs = [];
    var load = function (i) {
      if (srcs[i]) return srcs[i];
      srcs[i] = asImg(items[i].image);
      srcs[i].then(function (d) { var im = pg.querySelector('img[data-pf="' + i + '"]'); if (im) { im.src = d; im.classList.add("is-ready"); } }).catch(function () {});
      return srcs[i];
    };
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) {
        if (e.isIntersecting) { load(+e.target.querySelector("img").dataset.pf); io.unobserve(e.target); } }); }, { rootMargin: "600px 0px" });
      pg.querySelectorAll(".pf__item").forEach(function (f) { io.observe(f); });
    } else items.forEach(function (_, i) { load(i); });
    var lb = document.getElementById("lightbox");
    if (lb && typeof lb.showModal === "function") {
      var cur = 0, lbImg = lb.querySelector("img"), lbCap = lb.querySelector("figcaption");
      var visible = function () { return [].slice.call(pg.querySelectorAll(".pf__item:not([hidden]) .pf__open")).map(function (b) { return +b.dataset.i; }); };
      var show = function (i) {
        cur = i; lbImg.removeAttribute("src"); lbImg.alt = items[i].alt; lbCap.textContent = catLabel(items[i].cat);
        load(i).then(function (d) { if (cur === i) lbImg.src = d; }).catch(function () {});
      };
      var step = function (d) { var v = visible(); var p = v.indexOf(cur); show(v[(p + d + v.length) % v.length]); };
      pg.addEventListener("click", function (e) { var b = e.target.closest(".pf__open"); if (!b) return; show(+b.dataset.i); lb.showModal(); });
      lb.querySelector(".lb__close").addEventListener("click", function () { lb.close(); });
      lb.querySelector(".lb__prev").addEventListener("click", function () { step(-1); });
      lb.querySelector(".lb__next").addEventListener("click", function () { step(1); });
      lb.addEventListener("click", function (e) { if (e.target === lb) lb.close(); });
      lb.addEventListener("keydown", function (e) { if (e.key === "ArrowLeft") step(-1); if (e.key === "ArrowRight") step(1); });
      var tx = null;
      lb.addEventListener("touchstart", function (e) { tx = e.touches[0].clientX; }, { passive: true });
      lb.addEventListener("touchend", function (e) { if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1); tx = null; });
    }
  } else if (pg) {
    var pfs = document.getElementById("portafolio"); if (pfs) pfs.remove();
    document.querySelectorAll('a[href="#portafolio"]').forEach(function (a) { a.remove(); });
  }

  // Nav al hacer scroll
  var nav = document.getElementById("nav");
  var onScroll = function () { nav.classList.toggle("nav--solid", window.scrollY > 40); };
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
})();
