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
    pk.innerHTML = C.packages.map(function (p) {
      var msg = "Hola Captoora, quiero " + p.name + " ($" + p.price.toLocaleString("es-MX") + ").";
      return '<article class="pk__card' + (p.featured ? " pk__card--hot" : "") + '">' +
        (p.badge ? '<span class="pk__badge">' + esc(p.badge) + "</span>" : "") +
        '<h3 class="pk__name">' + esc(p.name) + "</h3>" +
        '<p class="pk__price"><span>$' + p.price.toLocaleString("es-MX") + '</span><small>MXN · ' + esc(p.unit) + "</small></p>" +
        "<ul>" + p.items.map(function (i) { return "<li>" + esc(i) + "</li>"; }).join("") + "</ul>" +
        '<a class="btn ' + (p.featured ? "btn--lime" : "btn--ghost") + ' btn--block" target="_blank" rel="noopener" href="' + wa(msg) + '">Apartar por WhatsApp</a>' +
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

  // Nav al hacer scroll
  var nav = document.getElementById("nav");
  var onScroll = function () { nav.classList.toggle("nav--solid", window.scrollY > 40); };
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
})();
