/* Scroll-scrub of a real Nikon still sequence.
   Playhead follows the lens stage only, with adjacent-frame blend. */
(function () {
  "use strict";

  var canvas = document.getElementById("lens-canvas");
  var stage = document.getElementById("lens");
  var hint = document.getElementById("lens-hint");
  if (!canvas || !stage || !canvas.getContext) return;

  var count = Number(canvas.getAttribute("data-count")) || 0;
  var dir = canvas.getAttribute("data-dir") || "assets/landing/frames/";
  var ctx = canvas.getContext("2d", { alpha: false });
  var images = new Array(count);
  var requested = new Array(count);
  var loaded = new Array(count);
  var current = 0;
  var target = 0;
  var last = 0;
  var running = false;
  var viewW = 0;
  var viewH = 0;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function src(index) {
    var n = String(index + 1).padStart(4, "0");
    return new URL(dir + "frame_" + n + ".webp", document.baseURI).href;
  }

  function nearest(index) {
    var i;
    for (i = index; i >= 0; i -= 1) if (loaded[i]) return i;
    for (i = index + 1; i < count; i += 1) if (loaded[i]) return i;
    return -1;
  }

  function requestFrame(index) {
    if (index < 0 || index >= count || requested[index]) return;
    requested[index] = true;
    var img = new Image();
    img.decoding = "async";
    img.onload = function () {
      loaded[index] = true;
      images[index] = img;
      if (index === 0) reveal();
    };
    img.onerror = function () {
      loaded[index] = false;
    };
    img.src = src(index);
  }

  function reveal() {
    canvas.style.opacity = "1";
    var fallback = document.querySelector(".lens-fallback");
    if (fallback) fallback.style.visibility = "hidden";
  }

  function resize() {
    var narrow = window.innerWidth < 800;
    var dpr = Math.min(window.devicePixelRatio || 1, narrow ? 1.5 : 2);
    viewW = canvas.clientWidth;
    viewH = canvas.clientHeight;
    if (!viewW || !viewH) return;
    canvas.width = Math.round(viewW * dpr);
    canvas.height = Math.round(viewH * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function drawCover(img, alpha) {
    var iw = img.naturalWidth;
    var ih = img.naturalHeight;
    if (!iw || !ih) return;
    var scale = Math.max(viewW / iw, viewH / ih);
    var dw = iw * scale;
    var dh = ih * scale;
    ctx.globalAlpha = alpha;
    ctx.drawImage(img, (viewW - dw) / 2, (viewH - dh) / 2, dw, dh);
  }

  function draw() {
    ctx.setTransform(canvas.width / viewW, 0, 0, canvas.height / viewH, 0, 0);
    ctx.fillStyle = "#000";
    ctx.globalAlpha = 1;
    ctx.fillRect(0, 0, viewW, viewH);
    var max = count - 1;
    var frame = Math.min(max, Math.max(0, current));
    var base = Math.floor(frame);
    var frac = frame - base;
    var a = nearest(base);
    var b = frac > 0.001 ? nearest(Math.min(max, base + 1)) : -1;
    if (a >= 0) drawCover(images[a], 1);
    if (b >= 0 && b !== a) drawCover(images[b], frac);
    ctx.globalAlpha = 1;
  }

  function progress() {
    var total = stage.offsetHeight - window.innerHeight;
    if (total <= 0) return 0;
    var y = window.scrollY - stage.offsetTop;
    return Math.min(1, Math.max(0, y / total));
  }

  function loop(now) {
    if (!running) return;
    if (!viewW || !viewH) resize();
    if (!viewW || !viewH) {
      requestAnimationFrame(loop);
      return;
    }
    var dt = Math.min((now - last) / 1000, 0.1);
    last = now;
    var p = reduced ? 0 : progress();
    target = p * (count - 1);
    var alpha = 1 - Math.exp(-dt * 9);
    current += (target - current) * alpha;
    if (Math.abs(target - current) < 0.004) current = target;
    if (hint) hint.style.opacity = p < 0.04 ? "1" : String(Math.max(0, 1 - (p - 0.04) / 0.12));
    draw();
    requestAnimationFrame(loop);
  }

  function start() {
    if (running) return;
    running = true;
    last = performance.now();
    requestAnimationFrame(loop);
  }

  function stop() {
    running = false;
  }

  requestFrame(0);
  var step = 6;
  var i;
  for (i = step; i < count; i += step) requestFrame(i);
  for (i = 1; i < count; i += 1) requestFrame(i);

  resize();
  window.addEventListener("resize", resize);
  if (reduced) {
    current = 0;
    target = 0;
  }
  start();

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      if (entries[0] && entries[0].isIntersecting) start();
      else stop();
    }, { rootMargin: "100px" });
    io.observe(stage);
  }

  window.addEventListener("pagehide", function () {
    stop();
    window.removeEventListener("resize", resize);
  });
})();
