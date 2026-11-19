/* ==========================================================================
   CAPTOORA STUDIO — GSAP SCROLL + LENIS + ANTIGRAVITY HALO ENGINE
   ========================================================================== */
(function () {
  const theme = document.documentElement.getAttribute("data-theme") || "captoora";

  function initHalo() {
    const canvas = document.getElementById("halo-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);

    const pointer = { x: w * 0.65, y: h * 0.48, tx: w * 0.65, ty: h * 0.48 };
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

      function drawAntigravity() {
        ctx.clearRect(0, 0, w, h);
        pointer.x += (pointer.tx - pointer.x) * 0.06;
        pointer.y += (pointer.ty - pointer.y) * 0.06;

        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];
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
        requestAnimationFrame(drawAntigravity);
      }
      drawAntigravity();
    } else {
      const stars = Array.from({ length: 85 }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.4 + 0.3,
        a: Math.random() * 0.5 + 0.1
      }));

      function drawCaptoora() {
        ctx.clearRect(0, 0, w, h);
        pointer.x += (pointer.tx - pointer.x) * 0.08;
        pointer.y += (pointer.ty - pointer.y) * 0.08;

        const grad = ctx.createRadialGradient(pointer.x, pointer.y, 0, pointer.x, pointer.y, 320);
        grad.addColorStop(0, "rgba(204, 255, 0, 0.08)");
        grad.addColorStop(1, "rgba(0, 0, 0, 0)");
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);

        for (const s of stars) {
          ctx.fillStyle = `rgba(255,255,255,${s.a})`;
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
          ctx.fill();
        }
        requestAnimationFrame(drawCaptoora);
      }
      drawCaptoora();
    }
  }

  function initMotion() {
    if (typeof Lenis !== "undefined") {
      const lenis = new Lenis({ duration: 1.15, smoothWheel: true });
      function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
      }
      requestAnimationFrame(raf);
    }

    if (typeof gsap !== "undefined") {
      gsap.from(".hero-copy > *", {
        y: 28,
        opacity: 0,
        duration: 0.9,
        stagger: 0.1,
        ease: "power3.out"
      });
      gsap.from(".hero-3d-wrap", {
        scale: 0.92,
        opacity: 0,
        duration: 1.1,
        delay: 0.2,
        ease: "power3.out"
      });

      if (typeof ScrollTrigger !== "undefined") {
        gsap.registerPlugin(ScrollTrigger);
        gsap.utils.toArray(".ed-card, .pkg-card, .gal-item, .closer-box").forEach((el) => {
          gsap.from(el, {
            y: 36,
            opacity: 0,
            duration: 0.85,
            ease: "power3.out",
            scrollTrigger: {
              trigger: el,
              start: "top 88%",
              once: true
            }
          });
        });
      }
    }
  }

  function initGallery() {
    const btns = document.querySelectorAll(".filter-btn");
    const items = document.querySelectorAll(".gal-item");
    btns.forEach((btn) => {
      btn.addEventListener("click", () => {
        btns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const cat = btn.getAttribute("data-filter");
        items.forEach((el) => {
          el.style.display = cat === "all" || el.getAttribute("data-cat") === cat ? "" : "none";
        });
      });
    });

    const lb = document.getElementById("lightbox");
    const lbImg = document.getElementById("lightbox-img");
    const lbClose = document.getElementById("lightbox-close");
    if (!lb || !lbImg) return;

    document.querySelectorAll("[data-lightbox]").forEach((card) => {
      card.addEventListener("click", () => {
        lbImg.src = card.getAttribute("data-lightbox");
        lb.classList.add("open");
      });
    });

    const close = () => lb.classList.remove("open");
    if (lbClose) lbClose.addEventListener("click", close);
    lb.addEventListener("click", (e) => { if (e.target === lb) close(); });
    window.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initHalo();
    initMotion();
    initGallery();
  });
})();
