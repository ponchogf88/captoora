/* ==========================================================================
   CAPTOORA STUDIO — CORE ENGINE (3D FLOATING CAMERA + HALO CURSOR + GALLERY)
   ========================================================================== */
(function () {
  const theme = document.documentElement.getAttribute("data-theme") || "captoora";

  // ------------------------------------------------------------------------
  // 1. ANTIGRAVITY HALO CURSOR CANVAS (Theme 3 signature + subtle stars)
  // ------------------------------------------------------------------------
  function initHaloCanvas() {
    const canvas = document.getElementById("halo-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);

    const pointer = { x: w * 0.65, y: h * 0.45, tx: w * 0.65, ty: h * 0.45 };
    window.addEventListener("mousemove", (e) => {
      pointer.tx = e.clientX;
      pointer.ty = e.clientY;
    });

    window.addEventListener("resize", () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    });

    if (theme === "antigravity") {
      // Radial particle dashes orbiting like Antigravity IDE download page
      const rings = 9;
      const particles = [];
      for (let r = 1; r <= rings; r++) {
        const count = 14 + r * 8;
        const baseRadius = 55 + r * 46;
        for (let i = 0; i < count; i++) {
          particles.push({
            angle: (i / count) * Math.PI * 2 + (r * 0.2),
            radius: baseRadius + (Math.random() * 14 - 7),
            speed: (0.0012 + (rings - r) * 0.00018) * (r % 2 === 0 ? 1 : -0.6),
            len: 4 + (r * 0.9),
            alpha: Math.max(0.12, 0.85 - r * 0.075),
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

          const dx = px - pointer.x;
          const dy = py - pointer.y;
          const a = Math.atan2(dy, dx);

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
    } else if (theme === "captoora") {
      // Subtle void starfield + faint lime cursor glow
      const stars = Array.from({ length: 75 }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.3 + 0.3,
        a: Math.random() * 0.45 + 0.1
      }));

      function drawCaptoora() {
        ctx.clearRect(0, 0, w, h);
        pointer.x += (pointer.tx - pointer.x) * 0.08;
        pointer.y += (pointer.ty - pointer.y) * 0.08;

        const grad = ctx.createRadialGradient(pointer.x, pointer.y, 0, pointer.x, pointer.y, 280);
        grad.addColorStop(0, "rgba(204, 255, 0, 0.07)");
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

  // ------------------------------------------------------------------------
  // 2. FLOATING 3D CAMERA (Three.js r128)
  // ------------------------------------------------------------------------
  function initCamera3D() {
    const container = document.getElementById("camera-3d-container");
    if (!container || typeof THREE === "undefined") return;

    const width = container.clientWidth || 460;
    const height = container.clientHeight || 420;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(36, width / height, 0.1, 100);
    camera.position.set(0, 0.35, 6.2);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    // Studio Lighting
    const ambient = new THREE.AmbientLight(0xffffff, 0.65);
    scene.add(ambient);

    const keyLight = new THREE.DirectionalLight(0xffffff, 1.8);
    keyLight.position.set(4, 5, 5);
    scene.add(keyLight);

    const accentHex =
      theme === "captoora" ? 0xccff00 : theme === "antigravity" ? 0x60a5fa : 0xffffff;
    const rimLight = new THREE.PointLight(accentHex, 2.2, 12);
    rimLight.position.set(-3.5, 2, -2);
    scene.add(rimLight);

    // Build Minimalist Luxury Camera Group
    const camGroup = new THREE.Group();

    const bodyMat = new THREE.MeshStandardMaterial({
      color: 0x18181b,
      roughness: 0.38,
      metalness: 0.72
    });
    const metalMat = new THREE.MeshStandardMaterial({
      color: 0x3f3f46,
      roughness: 0.25,
      metalness: 0.9
    });
    const accentMat = new THREE.MeshStandardMaterial({
      color: accentHex,
      roughness: 0.25,
      metalness: 0.5,
      emissive: accentHex,
      emissiveIntensity: theme === "spacex" ? 0.08 : 0.35
    });
    const glassMat = new THREE.MeshPhysicalMaterial({
      color: theme === "antigravity" ? 0x1d4ed8 : 0x0f172a,
      roughness: 0.05,
      metalness: 0.2,
      clearcoat: 1.0,
      clearcoatRoughness: 0.05
    });

    // Camera main chassis
    const body = new THREE.Mesh(new THREE.BoxGeometry(2.7, 1.72, 1.05), bodyMat);
    camGroup.add(body);

    // Right ergonomic grip
    const grip = new THREE.Mesh(new THREE.BoxGeometry(0.58, 1.68, 1.25), bodyMat);
    grip.position.set(1.06, -0.02, 0.14);
    camGroup.add(grip);

    // EVF Pentaprism top housing
    const evf = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.48, 0.95), metalMat);
    evf.position.set(-0.08, 1.06, -0.02);
    camGroup.add(evf);

    // Shutter button + Top dial
    const shutter = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.1, 24), accentMat);
    shutter.position.set(1.06, 0.88, 0.32);
    camGroup.add(shutter);

    const dial = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.16, 24), metalMat);
    dial.position.set(-0.92, 0.92, 0);
    camGroup.add(dial);

    // Lens outer barrel
    const barrelOuter = new THREE.Mesh(new THREE.CylinderGeometry(0.78, 0.82, 1.15, 48), metalMat);
    barrelOuter.rotation.x = Math.PI / 2;
    barrelOuter.position.set(-0.08, -0.05, 1.0);
    camGroup.add(barrelOuter);

    // Accent ring on lens
    const accentRing = new THREE.Mesh(new THREE.TorusGeometry(0.79, 0.025, 16, 48), accentMat);
    accentRing.position.set(-0.08, -0.05, 1.38);
    camGroup.add(accentRing);

    // Front lens glass element
    const glass = new THREE.Mesh(new THREE.SphereGeometry(0.62, 32, 32, 0, Math.PI * 2, 0, Math.PI * 0.32), glassMat);
    glass.rotation.x = Math.PI / 2;
    glass.position.set(-0.08, -0.05, 1.28);
    camGroup.add(glass);

    camGroup.rotation.y = -0.35;
    camGroup.rotation.x = 0.12;
    scene.add(camGroup);

    // Drag to rotate + gentle floating
    let isDragging = false;
    let prevX = 0;
    let prevY = 0;
    let targetRotY = -0.35;
    let targetRotX = 0.12;

    container.addEventListener("pointerdown", (e) => {
      isDragging = true;
      prevX = e.clientX;
      prevY = e.clientY;
    });
    window.addEventListener("pointerup", () => { isDragging = false; });
    window.addEventListener("pointermove", (e) => {
      if (!isDragging) return;
      const dx = e.clientX - prevX;
      const dy = e.clientY - prevY;
      targetRotY += dx * 0.008;
      targetRotX = Math.max(-0.5, Math.min(0.5, targetRotX + dy * 0.006));
      prevX = e.clientX;
      prevY = e.clientY;
    });

    window.addEventListener("resize", () => {
      const nw = container.clientWidth || 460;
      const nh = container.clientHeight || 420;
      camera.aspect = nw / nh;
      camera.updateProjectionMatrix();
      renderer.setSize(nw, nh);
    });

    let t = 0;
    function animate() {
      requestAnimationFrame(animate);
      t += 0.016;
      if (!isDragging) {
        targetRotY += 0.0045;
      }
      camGroup.rotation.y += (targetRotY - camGroup.rotation.y) * 0.08;
      camGroup.rotation.x += (targetRotX - camGroup.rotation.x) * 0.08;
      camGroup.position.y = Math.sin(t * 1.4) * 0.14;
      renderer.render(scene, camera);
    }
    animate();
  }

  // ------------------------------------------------------------------------
  // 3. GALLERY FILTERS & LIGHTBOX
  // ------------------------------------------------------------------------
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
    initHaloCanvas();
    initCamera3D();
    initGallery();
  });
})();
