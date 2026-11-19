/* ==========================================================================
   CAPTOORA STUDIO — MOTION ENGINE (LENIS + GSAP PARALLAX + HALO / DUST)
   ========================================================================== */
(function () {
  const theme = document.documentElement.getAttribute("data-theme") || "captoora";

  function initParticles() {
    const canvas = document.getElementById("bg-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);
    const pointer = { x: w * 0.5, y: h * 0.5, tx: w * 0.5, ty: h * 0.5 };

    window.addEventListener("mousemove", (e) => {
      pointer.tx = e.clientX;
      pointer.ty = e.clientY;
    });
    window.addEventListener("resize", () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    });

    if (theme === "antigravity") {
      const rings = 9;
      const particles = [];
      for (let r = 1; r <= rings; r++) {
        const count = 16 + r * 8;
        const baseRadius = 56 + r * 48;
        for (let i = 0; i < count; i++) {
          particles.push({
            angle: (i / count) * Math.PI * 2 + r * 0.25,
            radius: baseRadius + (Math.random() * 14 - 7),
            speed: (0.0014 + (rings - r) * 0.0002) * (r % 2 === 0 ? 1 : -0.65),
            len: 4 + r * 0.95,
            alpha: Math.max(0.14, 0.88 - r * 0.075),
            hue: r < 4 ? "96, 165, 250" : r < 7 ? "59, 130, 246" : "147, 197, 253"
          });
        }
      }
      function loopAnti() {
        ctx.clearRect(0, 0, w, h);
        pointer.x += (pointer.tx - pointer.x) * 0.06;
        pointer.y += (pointer.ty - pointer.y) * 0.06;
        for (const p of particles) {
          p.angle += p.speed;
          const px = pointer.x + Math.cos(p.angle) * p.radius;
          const py = pointer.y + Math.sin(p.angle) * p.radius;
          const a = Math.atan2(py - pointer.y, px - pointer.x);
          ctx.save();
          ctx.translate(px, py);
          ctx.rotate(a);
          ctx.strokeStyle = `rgba(${p.hue}, ${p.alpha})`;
          ctx.lineWidth = 2.2;
          ctx.lineCap = "round";
          ctx.beginPath();
          ctx.moveTo(-p.len * 0.5, 0);
          ctx.lineTo(p.len * 0.5, 0);
          ctx.stroke();
          ctx.restore();
        }
        requestAnimationFrame(loopAnti);
      }
      loopAnti();
    } else {
      // Hermit subtle floating dust motes
      const dust = Array.from({ length: 110 }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.4 + 0.3,
        vx: (Math.random() - 0.5) * 0.22,
        vy: (Math.random() - 0.5) * 0.22,
        a: Math.random() * 0.38 + 0.08
      }));
      function loopDust() {
        ctx.clearRect(0, 0, w, h);
        for (const d of dust) {
          d.x = (d.x + d.vx + w) % w;
          d.y = (d.y + d.vy + h) % h;
          ctx.fillStyle = `rgba(247, 244, 239, ${d.a})`;
          ctx.beginPath();
          ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
          ctx.fill();
        }
        requestAnimationFrame(loopDust);
      }
      loopDust();
    }
  }

  function initGSAP() {
    if (typeof Lenis !== "undefined") {
      const lenis = new Lenis({ duration: 1.2, smoothWheel: true });
      const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }

    if (typeof gsap === "undefined") return;

    // Hermit Hero entrance
    gsap.from(".hermit-giant-text", { y: 40, opacity: 0, duration: 1.1, ease: "power3.out" });
    gsap.from(".hermit-camera-overlay", { scale: 0.88, opacity: 0, duration: 1.2, delay: 0.15, ease: "power3.out" });
    gsap.from(".hermit-sub-left, .hermit-cta-right", { y: 20, opacity: 0, duration: 0.9, delay: 0.35, stagger: 0.12 });

    if (typeof ScrollTrigger === "undefined") return;
    gsap.registerPlugin(ScrollTrigger);

    // Purrweb parallax on tilted frames
    gsap.utils.toArray(".tilted-frame").forEach((card, i) => {
      gsap.to(card, {
        y: i % 2 === 0 ? -55 : 45,
        ease: "none",
        scrollTrigger: {
          trigger: ".purrweb-section",
          start: "top bottom",
          end: "bottom top",
          scrub: 1.2
        }
      });
    });

    // Goxyvi radial fan spread on scroll
    gsap.from(".arc-card", {
      scale: 0.78,
      opacity: 0,
      duration: 0.9,
      stagger: 0.06,
      ease: "power3.out",
      scrollTrigger: {
        trigger: ".goxyvi-finale",
        start: "top 75%",
        once: true
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initParticles();
    initGSAP();
  });
})();
