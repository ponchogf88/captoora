/* Captoora — cielo con pocas estrellas. Un canvas fijo para toda la página + el del hero. */
(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var skies = [];

  function Sky(canvas) {
    this.c = canvas; this.ctx = canvas.getContext("2d");
    this.fixed = canvas.getAttribute("data-fixed") === "1";
    this.base = parseInt(canvas.getAttribute("data-count") || "42", 10);
    this.stars = []; this.resize(); this.seed();
  }
  Sky.prototype.resize = function () {
    var w = this.fixed ? window.innerWidth : this.c.parentElement.clientWidth;
    var h = this.fixed ? window.innerHeight : this.c.parentElement.clientHeight;
    this.w = w; this.h = h;
    this.c.width = Math.round(w * dpr); this.c.height = Math.round(h * dpr);
    this.c.style.width = w + "px"; this.c.style.height = h + "px";
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  Sky.prototype.seed = function () {
    var n = Math.round(this.base * Math.min(1.4, Math.max(0.6, (this.w * this.h) / (1440 * 900))));
    this.stars = [];
    for (var i = 0; i < n; i++) this.stars.push({
      x: Math.random(), y: Math.random(),
      r: Math.random() < 0.82 ? 0.5 + Math.random() * 0.6 : 1.0 + Math.random() * 0.7,
      a: 0.18 + Math.random() * 0.5, tw: Math.random() * 6.28, sp: 0.0006 + Math.random() * 0.0016
    });
  };
  Sky.prototype.draw = function (t) {
    var ctx = this.ctx; ctx.clearRect(0, 0, this.w, this.h);
    for (var i = 0; i < this.stars.length; i++) {
      var s = this.stars[i], k = reduce ? 1 : 0.55 + 0.45 * Math.sin(t * s.sp + s.tw);
      ctx.beginPath(); ctx.fillStyle = "rgba(236,232,222," + (s.a * k).toFixed(3) + ")";
      ctx.arc(s.x * this.w, s.y * this.h, s.r, 0, 6.2832); ctx.fill();
    }
  };

  document.querySelectorAll("canvas.stars-canvas").forEach(function (c) { skies.push(new Sky(c)); });
  if (!skies.length) return;

  function drawAll(t) { for (var i = 0; i < skies.length; i++) skies[i].draw(t || 0); }
  var rt;
  window.addEventListener("resize", function () {
    clearTimeout(rt); rt = setTimeout(function () { skies.forEach(function (s) { s.resize(); s.seed(); }); drawAll(performance.now()); }, 150);
  });

  if (reduce) { drawAll(0); return; }            // estático si piden menos movimiento
  var last = 0;
  function loop(t) {
    if (!document.hidden && t - last > 50) { last = t; drawAll(t); }   // ~20 fps, basta para el parpadeo
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
})();
