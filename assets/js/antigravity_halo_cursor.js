/**
 * ============================================================================
 * ANTIGRAVITY ORBITAL HALO CURSOR ENGINE (v1.0)
 * ============================================================================
 * Reproduce la danza hipnótica de partículas orbitales alrededor del cursor
 * estilo antigravity.google:
 *   - Física de resortes amortiguados por capas (Spring-Damper Staggered Lag)
 *   - Ondulación cimática multi-armónica (las partículas bailan en sincronía)
 *   - Micro-cápsulas orientadas al vector tangencial/velocidad
 *   - Compatible con interfaces Apple Liquid Glass (visionOS Glassmorphism)
 * ============================================================================
 */
(function () {
  function initAntigravityHalo(userOptions = {}) {
    const opts = Object.assign(
      {
        particleCount: 240,
        baseRadius: 72,
        radiusSpread: 68,
        palette: [
          "#4285F4", // Google Blue
          "#7B61FF", // Cosmic Violet
          "#A855F7", // Electric Purple
          "#EC4899", // Rose Halo
          "#38BDF8", // Liquid Cyan
          "#F5C542"  // Captoora Gold accent
        ],
        opacity: 0.88,
        zIndex: 1
      },
      userOptions
    );

    let canvas = document.getElementById("antigravityHaloCanvas");
    if (!canvas) {
      canvas = document.createElement("canvas");
      canvas.id = "antigravityHaloCanvas";
      document.body.prepend(canvas);
    }

    Object.assign(canvas.style, {
      position: "fixed",
      inset: "0",
      width: "100vw",
      height: "100vh",
      pointerEvents: "none",
      zIndex: String(opts.zIndex),
      opacity: String(opts.opacity)
    });

    const ctx = canvas.getContext("2d");
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const mouse = {
      x: width * 0.5,
      y: height * 0.5,
      tx: width * 0.5,
      ty: height * 0.5,
      vx: 0,
      vy: 0,
      active: false
    };

    window.addEventListener("resize", () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    window.addEventListener("mousemove", (e) => {
      mouse.vx = e.clientX - mouse.tx;
      mouse.vy = e.clientY - mouse.ty;
      mouse.tx = e.clientX;
      mouse.ty = e.clientY;
      mouse.active = true;
    });

    // Crear enjambre orbital distribuido en anillos concéntricos armónicos
    const particles = [];
    for (let i = 0; i < opts.particleCount; i++) {
      const layer = (i % 5) / 4; // 0..1 (anillo interior -> exterior)
      const angle = (i / opts.particleCount) * Math.PI * 2 + layer * 0.6;
      const ringRadius = opts.baseRadius + layer * opts.radiusSpread + (Math.random() - 0.5) * 18;

      particles.push({
        x: mouse.x + Math.cos(angle) * ringRadius,
        y: mouse.y + Math.sin(angle) * ringRadius,
        vx: 0,
        vy: 0,
        baseAngle: angle,
        orbitSpeed: (0.0045 + (1 - layer) * 0.004) * (i % 2 === 0 ? 1 : 0.85),
        ringRadius: ringRadius,
        layer: layer,
        // Resortes escalonados: el anillo interior responde rápido, el exterior hace estela de seda
        spring: 0.042 - layer * 0.024,
        friction: 0.84 + layer * 0.05,
        phase: Math.random() * Math.PI * 2,
        length: 4.5 + (1 - layer) * 3.5,
        thickness: 1.5 + (1 - layer) * 0.9,
        color: opts.palette[i % opts.palette.length],
        alpha: 0.45 + (1 - layer) * 0.5
      });
    }

    let time = 0;

    function render() {
      time += 0.018;
      ctx.clearRect(0, 0, width, height);

      // Suavizado del centro del atractor
      mouse.x += (mouse.tx - mouse.x) * 0.18;
      mouse.y += (mouse.ty - mouse.y) * 0.18;

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.baseAngle += p.orbitSpeed;

        // Danza cimática: modulación armónica del radio y ángulo
        const wave1 = Math.sin(p.baseAngle * 3 + time * 1.7 + p.phase) * 14;
        const wave2 = Math.cos(p.baseAngle * 5 - time * 1.2 + p.layer * 2) * 8;
        const breathing = Math.sin(time * 0.9 + p.layer * 1.5) * 10;

        const dynamicRadius = p.ringRadius + wave1 + wave2 + breathing;
        const targetX = mouse.x + Math.cos(p.baseAngle) * dynamicRadius;
        const targetY = mouse.y + Math.sin(p.baseAngle) * dynamicRadius;

        // Fuerza de resorte hacia su posición en la coreografía orbital
        const dx = targetX - p.x;
        const dy = targetY - p.y;
        p.vx = (p.vx + dx * p.spring) * p.friction;
        p.vy = (p.vy + dy * p.spring) * p.friction;

        p.x += p.vx;
        p.y += p.vy;

        // Orientación de la micro-cápsula según su velocidad + tangente orbital
        const speed = Math.hypot(p.vx, p.vy);
        const moveAngle = speed > 0.35 ? Math.atan2(p.vy, p.vx) : p.baseAngle + Math.PI * 0.5;
        const stretch = Math.min(p.length + speed * 0.65, 18);

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(moveAngle);
        ctx.globalAlpha = p.alpha;
        ctx.strokeStyle = p.color;
        ctx.lineWidth = p.thickness;
        ctx.lineCap = "round";
        ctx.beginPath();
        ctx.moveTo(-stretch * 0.5, 0);
        ctx.lineTo(stretch * 0.5, 0);
        ctx.stroke();
        ctx.restore();
      }

      requestAnimationFrame(render);
    }

    requestAnimationFrame(render);
    return { canvas, particles, mouse };
  }

  window.initAntigravityHalo = initAntigravityHalo;
})();
