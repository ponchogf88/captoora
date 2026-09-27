(function () {
  var canvas = document.getElementById("hero-stars");
  if (!canvas) return;
  var ctx = canvas.getContext("2d");
  var stars = [];
  var COUNT = 42;

  function resize() {
    var hero = canvas.parentElement;
    canvas.width = hero.clientWidth;
    canvas.height = hero.clientHeight;
  }

  function seed() {
    stars = [];
    for (var i = 0; i < COUNT; i++) {
      stars.push({
        x: Math.random(),
        y: Math.random(),
        r: Math.random() < 0.82 ? 0.6 + Math.random() * 0.7 : 1.2 + Math.random() * 0.8,
        a: 0.25 + Math.random() * 0.55,
        tw: Math.random() * Math.PI * 2,
        sp: 0.004 + Math.random() * 0.01
      });
    }
  }

  function draw(t) {
    var w = canvas.width;
    var h = canvas.height;
    ctx.clearRect(0, 0, w, h);
    for (var i = 0; i < stars.length; i++) {
      var s = stars[i];
      var tw = 0.55 + 0.45 * Math.sin(t * s.sp + s.tw);
      ctx.beginPath();
      ctx.fillStyle = "rgba(236,230,220," + (s.a * tw) + ")";
      ctx.arc(s.x * w, s.y * h, s.r, 0, Math.PI * 2);
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }

  resize();
  seed();
  window.addEventListener("resize", function () {
    resize();
  });
  requestAnimationFrame(draw);
})();
