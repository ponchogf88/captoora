/**
 * CAPTOORA STUDIO - HIGH-POLY PROCEDURAL 3D STORYTELLING ENGINE
 * Nikon Z9 Mirrorless + Nikkor Z 50mm f/1.2 S Lens + 5 Scroll Acts
 * WebGL (Three.js) + GSAP ScrollTrigger + Lenis + Web Audio API
 */

(function () {
  'use strict';

  // Master namespace
  window.Captoora3D = {
    scene: null,
    camera: null,
    renderer: null,
    cameraRig: null,
    cameraBody: null,
    lensGroup: null,
    shutterButton: null,
    apertureBlades: [],
    dustParticles: null,
    audioCtx: null,
    soundEnabled: true,
    hasFlashedAct3: false,
    actProgress: 0,
    currentAct: 1,

    // Initialize the entire experience
    init: function () {
      const container = document.getElementById('webgl-container');
      if (!container) return;

      this.initScene(container);
      this.initLighting();
      this.buildNikonZ9();
      this.initParticles();
      this.initScrollTrigger();
      this.initInteractions();
      this.animate();

      window.addEventListener('resize', () => this.onWindowResize());
    },

    // 1. SCENE, CAMERA & RENDERER SETUP
    initScene: function (container) {
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0x000000); // Pure #000 void

      const aspect = window.innerWidth / window.innerHeight;
      this.camera = new THREE.PerspectiveCamera(38, aspect, 0.1, 100);
      this.camera.position.set(0, 0, 8.6);

      this.renderer = new THREE.WebGLRenderer({
        canvas: document.getElementById('webgl-canvas'),
        antialias: true,
        alpha: false,
        powerPreference: 'high-performance',
      });
      this.renderer.setSize(window.innerWidth, window.innerHeight);
      this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
      this.renderer.toneMappingExposure = 1.15;
      this.renderer.outputEncoding = THREE.sRGBEncoding;

      this.cameraRig = new THREE.Group();
      this.scene.add(this.cameraRig);
    },

    // 2. CAPTOORA SIGNATURE LIGHTING (CYAN LEFT, AMBER RIGHT, TOP RIM)
    initLighting: function () {
      // Subtle ambient
      const ambLight = new THREE.AmbientLight(0x0a0d14, 0.55);
      this.scene.add(ambLight);

      // Left Rim: Electric Cyan / Ice Blue (#00d4ff)
      this.cyanRim = new THREE.SpotLight(0x00d4ff, 4.2, 35, Math.PI / 4, 0.45, 1);
      this.cyanRim.position.set(-7, 2.5, 1.0);
      this.cyanRim.target = this.cameraRig;
      this.scene.add(this.cyanRim);

      // Right Rim: Warm Amber / Sunset Gold (#f59e0b)
      this.amberRim = new THREE.SpotLight(0xf59e0b, 4.0, 35, Math.PI / 4, 0.45, 1);
      this.amberRim.position.set(7, 2.0, 1.0);
      this.amberRim.target = this.cameraRig;
      this.scene.add(this.amberRim);

      // Top Backlight / Edge Rim (#ffffff)
      const topRim = new THREE.DirectionalLight(0xffffff, 2.0);
      topRim.position.set(0, 6, -2);
      this.scene.add(topRim);

      // Front Fill Soft Light (#e2e8f0)
      const frontFill = new THREE.DirectionalLight(0xe2e8f0, 1.0);
      frontFill.position.set(0, 0.5, 8.5);
      this.scene.add(frontFill);
    },

    // 3. PROCEDURAL TEXTURE GENERATORS
    generateNikonLogoTexture: function () {
      const canvas = document.createElement('canvas');
      canvas.width = 512;
      canvas.height = 160;
      const ctx = canvas.getContext('2d');

      ctx.fillStyle = '#101114';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Subtle metallic noise
      for (let i = 0; i < 4000; i++) {
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height;
        ctx.fillStyle = 'rgba(255,255,255,0.025)';
        ctx.fillRect(x, y, 1, 1);
      }

      // Classic Nikon italic logotype
      ctx.font = 'italic 900 68px "Plus Jakarta Sans", "Helvetica Neue", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = '#ffffff';
      ctx.letterSpacing = '6px';
      ctx.fillText('Nikon', 256, 80);

      const texture = new THREE.CanvasTexture(canvas);
      texture.anisotropy = 8;
      return texture;
    },

    generateZ9BadgeTexture: function () {
      const canvas = document.createElement('canvas');
      canvas.width = 256;
      canvas.height = 128;
      const ctx = canvas.getContext('2d');

      ctx.fillStyle = '#101114';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.font = '900 60px "Space Grotesk", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = '#ffffff';
      ctx.fillText('Z', 90, 64);

      ctx.font = '900 52px "Space Grotesk", sans-serif';
      ctx.fillStyle = '#f59e0b'; // Amber Gold 9
      ctx.fillText('9', 170, 64);

      const texture = new THREE.CanvasTexture(canvas);
      return texture;
    },

    generateRearLcdTexture: function () {
      const canvas = document.createElement('canvas');
      canvas.width = 1024;
      canvas.height = 768;
      const ctx = canvas.getContext('2d');

      // Dark live view display
      ctx.fillStyle = '#06080d';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Subtle grid overlay
      ctx.strokeStyle = 'rgba(0, 212, 255, 0.08)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(341, 0); ctx.lineTo(341, 768);
      ctx.moveTo(682, 0); ctx.lineTo(682, 768);
      ctx.moveTo(0, 256); ctx.lineTo(1024, 256);
      ctx.moveTo(0, 512); ctx.lineTo(1024, 512);
      ctx.stroke();

      // Top Header HUD
      ctx.font = '600 24px "Space Grotesk", monospace';
      ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
      ctx.fillText('FX  [RAW+F]  [3D-TRACK]  AF-C', 40, 50);

      ctx.textAlign = 'right';
      ctx.fillText('1.4K  ⚡  🔋 98%', 984, 50);

      // Center AF Brackets (3D-Tracking Box)
      ctx.textAlign = 'center';
      ctx.strokeStyle = '#10b981'; // Green AF lock
      ctx.lineWidth = 2.5;
      ctx.strokeRect(442, 314, 140, 140);
      ctx.fillStyle = '#10b981';
      ctx.fillRect(507, 379, 10, 10);

      // Artificial Horizon Level (Dual Axis)
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(260, 384); ctx.lineTo(410, 384);
      ctx.moveTo(614, 384); ctx.lineTo(764, 384);
      ctx.stroke();

      // Bottom Telemetry Bar
      ctx.fillStyle = 'rgba(10, 14, 22, 0.9)';
      ctx.fillRect(0, 670, 1024, 98);

      ctx.textAlign = 'left';
      ctx.font = '700 38px "Space Grotesk", monospace';
      ctx.fillStyle = '#ffffff';
      ctx.fillText('1/8000', 40, 735);

      ctx.fillStyle = '#f59e0b'; // Amber Aperture
      ctx.fillText('F1.2', 260, 735);

      ctx.fillStyle = '#ffffff';
      ctx.fillText('ISO 100', 450, 735);

      ctx.font = '600 24px "Space Grotesk", monospace';
      ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
      ctx.fillText('±0.0 EV', 680, 732);

      // RGB Histogram
      ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
      ctx.fillRect(840, 685, 144, 70);
      ctx.fillStyle = 'rgba(0, 212, 255, 0.5)';
      ctx.beginPath();
      ctx.moveTo(840, 755);
      ctx.lineTo(860, 730);
      ctx.lineTo(890, 700);
      ctx.lineTo(920, 740);
      ctx.lineTo(950, 710);
      ctx.lineTo(984, 755);
      ctx.closePath();
      ctx.fill();

      const texture = new THREE.CanvasTexture(canvas);
      texture.anisotropy = 4;
      return texture;
    },

    generateTopLcdTexture: function () {
      const canvas = document.createElement('canvas');
      canvas.width = 512;
      canvas.height = 256;
      const ctx = canvas.getContext('2d');

      ctx.fillStyle = '#020604'; // Deep matrix OLED
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.font = '700 48px "Space Grotesk", monospace';
      ctx.fillStyle = '#22c55e'; // Backlit matrix green
      ctx.fillText('1/8000', 30, 80);
      ctx.fillText('F 1.2', 300, 80);

      ctx.font = '600 36px "Space Grotesk", monospace';
      ctx.fillStyle = '#86efac';
      ctx.fillText('ISO 100', 30, 160);
      ctx.fillText('[ 845 ]', 320, 160);

      ctx.font = '500 24px "Space Grotesk", monospace';
      ctx.fillStyle = '#4ade80';
      ctx.fillText('M  RAW  AF-C  REMOTE', 30, 220);

      const texture = new THREE.CanvasTexture(canvas);
      return texture;
    },

    generateLensBezelTexture: function () {
      const canvas = document.createElement('canvas');
      canvas.width = 1024;
      canvas.height = 1024;
      const ctx = canvas.getContext('2d');

      ctx.fillStyle = '#111317';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Stepped rings
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(512, 512, 480, 0, Math.PI * 2);
      ctx.arc(512, 512, 440, 0, Math.PI * 2);
      ctx.arc(512, 512, 380, 0, Math.PI * 2);
      ctx.stroke();

      // Engraved typography along ring
      ctx.save();
      ctx.translate(512, 512);
      const text = '✦ NIKON  NIKKOR  Z  50mm  1:1.2  S   Ø82   MADE IN JAPAN   [N] ✦';
      const radius = 410;
      const totalAngle = Math.PI * 1.85;
      const startAngle = -totalAngle / 2 - Math.PI / 2;
      const step = totalAngle / text.length;

      ctx.font = '700 28px "Space Grotesk", sans-serif';
      ctx.fillStyle = '#f1f5f9';

      for (let i = 0; i < text.length; i++) {
        const char = text[i];
        const angle = startAngle + i * step;
        ctx.save();
        ctx.rotate(angle);
        ctx.translate(0, -radius);
        if (char === '[N]') {
          ctx.fillStyle = '#f59e0b'; // Gold Nano Coat badge
        } else {
          ctx.fillStyle = '#f1f5f9';
        }
        ctx.fillText(char, -10, 0);
        ctx.restore();
      }
      ctx.restore();

      const texture = new THREE.CanvasTexture(canvas);
      texture.anisotropy = 8;
      return texture;
    },

    generateLensOledTexture: function () {
      const canvas = document.createElement('canvas');
      canvas.width = 512;
      canvas.height = 160;
      const ctx = canvas.getContext('2d');

      ctx.fillStyle = '#06080a';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.font = '700 44px "Space Grotesk", sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.fillText('50mm  f/1.2 S', 40, 70);

      // Focus distance bar
      ctx.strokeStyle = '#00d4ff';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(40, 110); ctx.lineTo(470, 110);
      ctx.stroke();

      ctx.font = '600 20px "Space Grotesk", monospace';
      ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
      ctx.fillText('0.45m', 40, 140);
      ctx.fillText('1.5m', 240, 140);
      ctx.fillText('∞', 460, 140);

      const texture = new THREE.CanvasTexture(canvas);
      return texture;
    },

    // 4. PROCEDURAL HIGH-POLY NIKON Z9 & NIKKOR 50MM F/1.2 S MODEL
    buildNikonZ9: function () {
      const z9Group = new THREE.Group();

      // Materials
      const magnesiumMat = new THREE.MeshStandardMaterial({
        color: 0x131417,
        roughness: 0.38,
        metalness: 0.82,
      });

      const gripRubberMat = new THREE.MeshStandardMaterial({
        color: 0x0a0a0d,
        roughness: 0.85,
        metalness: 0.15,
      });

      const steelChromeMat = new THREE.MeshStandardMaterial({
        color: 0xd4d8de,
        roughness: 0.22,
        metalness: 0.95,
      });

      const goldContactMat = new THREE.MeshStandardMaterial({
        color: 0xf59e0b,
        roughness: 0.3,
        metalness: 0.9,
      });

      const redAccentMat = new THREE.MeshStandardMaterial({
        color: 0xd90429,
        roughness: 0.35,
        metalness: 0.3,
      });

      // A. MAIN CAMERA CHASSIS (Integrated Vertical Grip)
      const bodyWidth = 3.2;
      const bodyHeight = 3.1;
      const bodyDepth = 1.6;

      const bodyGeom = new THREE.BoxGeometry(bodyWidth, bodyHeight, bodyDepth, 2, 2, 2);
      const bodyMesh = new THREE.Mesh(bodyGeom, magnesiumMat);
      bodyMesh.position.set(0, 0, 0);
      z9Group.add(bodyMesh);

      // B. ERGONOMIC HANDGRIP (Right Grip & Vertical Grip)
      const gripGeom = new THREE.CylinderGeometry(0.55, 0.65, bodyHeight * 0.96, 24);
      const gripMesh = new THREE.Mesh(gripGeom, gripRubberMat);
      gripMesh.position.set(1.48, -0.05, 0.42);
      gripMesh.scale.set(0.9, 1.0, 1.4);
      z9Group.add(gripMesh);

      // Front thumb contour
      const thumbRestGeom = new THREE.BoxGeometry(0.4, 1.2, 0.5);
      const thumbRestMesh = new THREE.Mesh(thumbRestGeom, gripRubberMat);
      thumbRestMesh.position.set(1.5, 0.4, 0.95);
      z9Group.add(thumbRestMesh);

      // Nikon signature red accent slash on grip
      const redSwooshGeom = new THREE.BoxGeometry(0.08, 0.45, 0.35);
      const redSwooshMesh = new THREE.Mesh(redSwooshGeom, redAccentMat);
      redSwooshMesh.position.set(1.48, 0.82, 0.88);
      redSwooshMesh.rotation.z = -0.35;
      z9Group.add(redSwooshMesh);

      // C. PENTAPRISM & EVF HOUSING (Top Center)
      const prismGeom = new THREE.CylinderGeometry(0.85, 1.25, 0.9, 4);
      const prismMesh = new THREE.Mesh(prismGeom, magnesiumMat);
      prismMesh.position.set(0, 1.85, 0.05);
      prismMesh.rotation.y = Math.PI / 4;
      z9Group.add(prismMesh);

      // Front Nikon Logotype Plate
      const logoTexture = this.generateNikonLogoTexture();
      const logoMat = new THREE.MeshBasicMaterial({
        map: logoTexture,
        transparent: false,
      });
      const logoPlateGeom = new THREE.PlaneGeometry(1.2, 0.45);
      const logoPlateMesh = new THREE.Mesh(logoPlateGeom, logoMat);
      logoPlateMesh.position.set(0, 1.85, 0.86);
      z9Group.add(logoPlateMesh);

      // "Z 9" Plaque on Front Left Shoulder
      const z9BadgeTex = this.generateZ9BadgeTexture();
      const z9BadgeMat = new THREE.MeshBasicMaterial({ map: z9BadgeTex });
      const z9BadgeGeom = new THREE.PlaneGeometry(0.55, 0.28);
      const z9BadgeMesh = new THREE.Mesh(z9BadgeGeom, z9BadgeMat);
      z9BadgeMesh.position.set(-1.18, 1.05, 0.82);
      z9Group.add(z9BadgeMesh);

      // Hot Shoe Mount on Top
      const hotShoeGeom = new THREE.BoxGeometry(0.55, 0.12, 0.6);
      const hotShoeMesh = new THREE.Mesh(hotShoeGeom, steelChromeMat);
      hotShoeMesh.position.set(0, 2.34, 0.05);
      z9Group.add(hotShoeMesh);

      // Rear Viewfinder Eyepiece
      const evfGeom = new THREE.CylinderGeometry(0.42, 0.45, 0.3, 32);
      const evfMesh = new THREE.Mesh(evfGeom, gripRubberMat);
      evfMesh.position.set(0, 1.85, -0.92);
      evfMesh.rotation.x = Math.PI / 2;
      z9Group.add(evfMesh);

      // D. TOP PLATE CONTROLS & DIALS
      // Shutter Button Assembly (Parented so it depresses in Act 3)
      this.shutterButton = new THREE.Group();
      this.shutterButton.position.set(1.42, 1.62, 0.65);

      const collarGeom = new THREE.CylinderGeometry(0.24, 0.26, 0.12, 24);
      const collarMesh = new THREE.Mesh(collarGeom, magnesiumMat);
      this.shutterButton.add(collarMesh);

      const btnGeom = new THREE.CylinderGeometry(0.18, 0.18, 0.14, 24);
      const btnMesh = new THREE.Mesh(btnGeom, steelChromeMat);
      btnMesh.position.y = 0.06;
      this.shutterButton.add(btnMesh);
      z9Group.add(this.shutterButton);

      // Left Drive Mode Dial
      const driveDialGeom = new THREE.CylinderGeometry(0.48, 0.48, 0.25, 32);
      const driveDialMesh = new THREE.Mesh(driveDialGeom, magnesiumMat);
      driveDialMesh.position.set(-1.15, 1.62, 0.1);
      z9Group.add(driveDialMesh);

      // Red Video Record Button
      const recBtnGeom = new THREE.CylinderGeometry(0.1, 0.1, 0.08, 16);
      const recBtnMesh = new THREE.Mesh(recBtnGeom, redAccentMat);
      recBtnMesh.position.set(1.05, 1.62, 0.3);
      z9Group.add(recBtnMesh);

      // Top OLED Status Display
      const topLcdTex = this.generateTopLcdTexture();
      const topLcdMat = new THREE.MeshBasicMaterial({ map: topLcdTex });
      const topLcdGeom = new THREE.PlaneGeometry(0.85, 0.45);
      const topLcdMesh = new THREE.Mesh(topLcdGeom, topLcdMat);
      topLcdMesh.position.set(0.9, 1.6, -0.3);
      topLcdMesh.rotation.x = -Math.PI / 2;
      z9Group.add(topLcdMesh);

      // E. REAR PLATE & 3.2" LCD MONITOR
      const lcdFrameGeom = new THREE.BoxGeometry(2.3, 1.75, 0.12);
      const lcdFrameMesh = new THREE.Mesh(lcdFrameGeom, magnesiumMat);
      lcdFrameMesh.position.set(-0.25, -0.15, -0.85);
      z9Group.add(lcdFrameMesh);

      const rearLcdTex = this.generateRearLcdTexture();
      const rearLcdMat = new THREE.MeshBasicMaterial({ map: rearLcdTex });
      const rearLcdGeom = new THREE.PlaneGeometry(2.15, 1.6);
      const rearLcdMesh = new THREE.Mesh(rearLcdGeom, rearLcdMat);
      rearLcdMesh.position.set(-0.25, -0.15, -0.92);
      rearLcdMesh.rotation.y = Math.PI;
      z9Group.add(rearLcdMesh);

      // Rear D-Pad & Joystick Controls
      const joystickGeom = new THREE.CylinderGeometry(0.12, 0.14, 0.18, 16);
      const joystickMesh = new THREE.Mesh(joystickGeom, gripRubberMat);
      joystickMesh.position.set(1.2, 0.5, -0.86);
      joystickMesh.rotation.x = Math.PI / 2;
      z9Group.add(joystickMesh);

      const dpadGeom = new THREE.CylinderGeometry(0.28, 0.28, 0.08, 24);
      const dpadMesh = new THREE.Mesh(dpadGeom, magnesiumMat);
      dpadMesh.position.set(1.2, -0.2, -0.86);
      dpadMesh.rotation.x = Math.PI / 2;
      z9Group.add(dpadMesh);

      // F. Z-MOUNT THROAT & FULL-FRAME SENSOR
      const mountFlangeGeom = new THREE.CylinderGeometry(1.08, 1.08, 0.18, 48);
      const mountFlangeMesh = new THREE.Mesh(mountFlangeGeom, steelChromeMat);
      mountFlangeMesh.position.set(0, 0.15, 0.85);
      mountFlangeMesh.rotation.x = Math.PI / 2;
      z9Group.add(mountFlangeMesh);

      // Gold electronic pins
      const pinRingGeom = new THREE.TorusGeometry(0.85, 0.03, 8, 32, Math.PI * 0.8);
      const pinRingMesh = new THREE.Mesh(pinRingGeom, goldContactMat);
      pinRingMesh.position.set(0, 0.15, 0.92);
      z9Group.add(pinRingMesh);

      // Stacked FX Sensor behind mount
      const sensorGeom = new THREE.PlaneGeometry(0.95, 0.65);
      const sensorMat = new THREE.MeshStandardMaterial({
        color: 0x052e25, // Deep iridescent green-cyan optical coating
        roughness: 0.1,
        metalness: 0.9,
      });
      const sensorMesh = new THREE.Mesh(sensorGeom, sensorMat);
      sensorMesh.position.set(0, 0.15, 0.72);
      z9Group.add(sensorMesh);

      // G. NIKKOR Z 50MM F/1.2 S LENS (Flagship Prime)
      this.lensGroup = new THREE.Group();
      this.lensGroup.position.set(0, 0.15, 0.95);

      // Barrel Section 1: Base Mount Collar
      const baseCollarGeom = new THREE.CylinderGeometry(1.05, 1.05, 0.6, 48);
      const baseCollarMesh = new THREE.Mesh(baseCollarGeom, magnesiumMat);
      baseCollarMesh.position.z = 0.3;
      baseCollarMesh.rotation.x = Math.PI / 2;
      this.lensGroup.add(baseCollarMesh);

      // OLED Info Display on Lens Barrel
      const lensOledTex = this.generateLensOledTexture();
      const lensOledMat = new THREE.MeshBasicMaterial({ map: lensOledTex });
      const lensOledGeom = new THREE.PlaneGeometry(0.65, 0.22);
      const lensOledMesh = new THREE.Mesh(lensOledGeom, lensOledMat);
      lensOledMesh.position.set(0, 1.06, 0.45);
      lensOledMesh.rotation.x = -Math.PI / 2;
      this.lensGroup.add(lensOledMesh);

      // Programmable Knurled Control Ring
      const controlRingGeom = new THREE.CylinderGeometry(1.08, 1.08, 0.4, 48);
      const knurledMat = new THREE.MeshStandardMaterial({
        color: 0x1f2127,
        roughness: 0.45,
        metalness: 0.75,
      });
      const controlRingMesh = new THREE.Mesh(controlRingGeom, knurledMat);
      controlRingMesh.position.z = 0.8;
      controlRingMesh.rotation.x = Math.PI / 2;
      this.lensGroup.add(controlRingMesh);

      // Broad Manual Focus Ring (Diamond Rubber Grip)
      const focusRingGeom = new THREE.CylinderGeometry(1.15, 1.15, 1.2, 48);
      const focusRingMesh = new THREE.Mesh(focusRingGeom, gripRubberMat);
      focusRingMesh.position.z = 1.6;
      focusRingMesh.rotation.x = Math.PI / 2;
      this.lensGroup.add(focusRingMesh);

      // Front Barrel Extension
      const frontBarrelGeom = new THREE.CylinderGeometry(1.22, 1.15, 0.8, 48);
      const frontBarrelMesh = new THREE.Mesh(frontBarrelGeom, magnesiumMat);
      frontBarrelMesh.position.z = 2.45;
      frontBarrelMesh.rotation.x = Math.PI / 2;
      this.lensGroup.add(frontBarrelMesh);

      // Front Bezel Ring with Engraved Lettering
      const bezelTex = this.generateLensBezelTexture();
      const bezelMat = new THREE.MeshBasicMaterial({ map: bezelTex });
      const bezelGeom = new THREE.RingGeometry(0.6, 1.2, 48);
      const bezelMesh = new THREE.Mesh(bezelGeom, bezelMat);
      bezelMesh.position.z = 2.86;
      this.lensGroup.add(bezelMesh);

      // Convex Front Glass Meniscus (f/1.2 Pure Optic)
      const glassMat = new THREE.MeshPhysicalMaterial({
        color: 0xffffff,
        metalness: 0.1,
        roughness: 0.03,
        transmission: 0.94,
        ior: 1.54,
        reflectivity: 0.85,
        clearcoat: 1.0,
        clearcoatRoughness: 0.05,
        transparent: true,
        opacity: 0.88,
      });

      const glassGeom = new THREE.SphereGeometry(0.85, 36, 18, 0, Math.PI * 2, 0, Math.PI * 0.42);
      const glassMesh = new THREE.Mesh(glassGeom, glassMat);
      glassMesh.position.z = 2.42;
      this.lensGroup.add(glassMesh);

      // Internal Aperture Iris Mechanism (9 dynamic blades)
      this.irisGroup = new THREE.Group();
      this.irisGroup.position.z = 1.5;

      const bladeMat = new THREE.MeshStandardMaterial({
        color: 0x18191c,
        roughness: 0.35,
        metalness: 0.85,
        side: THREE.DoubleSide,
      });

      for (let i = 0; i < 9; i++) {
        const bladeAngle = (i / 9) * Math.PI * 2;
        const bladeGeom = new THREE.PlaneGeometry(0.55, 0.32);
        const bladeMesh = new THREE.Mesh(bladeGeom, bladeMat);
        bladeMesh.position.set(Math.cos(bladeAngle) * 0.4, Math.sin(bladeAngle) * 0.4, 0);
        bladeMesh.rotation.z = bladeAngle + 0.3;
        this.apertureBlades.push(bladeMesh);
        this.irisGroup.add(bladeMesh);
      }
      this.lensGroup.add(this.irisGroup);

      z9Group.add(this.lensGroup);

      // Mount into rig
      this.cameraBody = z9Group;
      this.cameraRig.add(this.cameraBody);

      // Initial beauty pose: slight isometric tilt
      this.cameraRig.rotation.y = 0.55;
      this.cameraRig.rotation.x = 0.12;
    },

    // 5. ATMOSPHERIC SUSPENDED PARTICLES (FLOATING DUST MOTES)
    initParticles: function () {
      const count = 450;
      const geom = new THREE.BufferGeometry();
      const positions = new Float32Array(count * 3);
      const colors = new Float32Array(count * 3);

      const cyan = new THREE.Color(0x00d4ff);
      const amber = new THREE.Color(0xf59e0b);
      const white = new THREE.Color(0xffffff);

      for (let i = 0; i < count; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 14;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 12;

        const mixColor = Math.random() < 0.45 ? cyan : Math.random() < 0.8 ? amber : white;
        colors[i * 3] = mixColor.r;
        colors[i * 3 + 1] = mixColor.g;
        colors[i * 3 + 2] = mixColor.b;
      }

      geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));

      // Circular particle point
      const pCanvas = document.createElement('canvas');
      pCanvas.width = 32;
      pCanvas.height = 32;
      const pCtx = pCanvas.getContext('2d');
      const grad = pCtx.createRadialGradient(16, 16, 0, 16, 16, 16);
      grad.addColorStop(0, 'rgba(255,255,255,1)');
      grad.addColorStop(0.3, 'rgba(255,255,255,0.7)');
      grad.addColorStop(1, 'rgba(255,255,255,0)');
      pCtx.fillStyle = grad;
      pCtx.fillRect(0, 0, 32, 32);
      const pTex = new THREE.CanvasTexture(pCanvas);

      const pMat = new THREE.PointsMaterial({
        size: 0.12,
        map: pTex,
        vertexColors: true,
        transparent: true,
        opacity: 0.65,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      });

      this.dustParticles = new THREE.Points(geom, pMat);
      this.scene.add(this.dustParticles);
    },

    // 6. SYNTHESIZE NIKON Z9 MECHANICAL SHUTTER SOUND (WEB AUDIO API)
    playNikonZ9Shutter: function () {
      if (!this.soundEnabled) return;
      try {
        if (!this.audioCtx) {
          this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (this.audioCtx.state === 'suspended') {
          this.audioCtx.resume();
        }

        const now = this.audioCtx.currentTime;

        // 1. Initial mechanical button trip (High-Frequency transient)
        const osc1 = this.audioCtx.createOscillator();
        const gain1 = this.audioCtx.createGain();
        osc1.type = 'triangle';
        osc1.frequency.setValueAtTime(320, now);
        osc1.frequency.exponentialRampToValueAtTime(45, now + 0.05);

        gain1.gain.setValueAtTime(0.85, now);
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.05);

        osc1.connect(gain1);
        gain1.connect(this.audioCtx.destination);
        osc1.start(now);
        osc1.stop(now + 0.06);

        // 2. High-speed shutter curtain travel (Bandpass-filtered dual noise burst)
        const bufferSize = this.audioCtx.sampleRate * 0.09;
        const noiseBuf = this.audioCtx.createBuffer(1, bufferSize, this.audioCtx.sampleRate);
        const data = noiseBuf.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.35));
        }

        const noiseNode = this.audioCtx.createBufferSource();
        noiseNode.buffer = noiseBuf;

        const biquad = this.audioCtx.createBiquadFilter();
        biquad.type = 'bandpass';
        biquad.frequency.setValueAtTime(2400, now + 0.01);
        biquad.Q.setValueAtTime(3.0, now + 0.01);

        const noiseGain = this.audioCtx.createGain();
        noiseGain.gain.setValueAtTime(0.7, now + 0.01);
        noiseGain.gain.exponentialRampToValueAtTime(0.01, now + 0.08);

        noiseNode.connect(biquad);
        biquad.connect(noiseGain);
        noiseGain.connect(this.audioCtx.destination);
        noiseNode.start(now + 0.01);

        // 3. Secondary mechanical blade lock / recock (Solid "Clack" at +45ms)
        const osc2 = this.audioCtx.createOscillator();
        const gain2 = this.audioCtx.createGain();
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(140, now + 0.045);
        osc2.frequency.exponentialRampToValueAtTime(28, now + 0.11);

        gain2.gain.setValueAtTime(0.9, now + 0.045);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.11);

        osc2.connect(gain2);
        gain2.connect(this.audioCtx.destination);
        osc2.start(now + 0.045);
        osc2.stop(now + 0.12);
      } catch (err) {
        console.warn('Audio Synthesis:', err);
      }
    },

    // 7. GSAP SCROLLTRIGGER 5-ACT ORCHESTRATION
    initScrollTrigger: function () {
      if (!window.gsap || !window.ScrollTrigger) return;
      gsap.registerPlugin(ScrollTrigger);

      // Initialize Lenis smooth scroll if present
      if (window.Lenis) {
        const lenis = new Lenis({
          duration: 1.2,
          easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
          direction: 'vertical',
          smooth: true,
        });
        function raf(time) {
          lenis.raf(time);
          requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);
        lenis.on('scroll', ScrollTrigger.update);
        gsap.ticker.add((time) => lenis.raf(time * 1000));
        gsap.ticker.lagSmoothing(0);
      }

      // Master Timeline linked to #story-stage (500vh scroll container)
      const storyStage = document.getElementById('story-stage');
      if (!storyStage) return;

      const act1Badge = document.getElementById('act1-hud');
      const act2Quote = document.getElementById('act2-quote');
      const act3Flash = document.getElementById('flash-screen');
      const act3Quote = document.getElementById('act3-quote');
      const galleryStage = document.getElementById('inside-camera-stage');

      ScrollTrigger.create({
        trigger: storyStage,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 1,
        onUpdate: (self) => {
          const progress = self.progress; // 0.00 to 1.00
          this.actProgress = progress;

          // Fade out all HUD telemetry during Act 4 absorption
          const hudOverlay = document.querySelector('.hud-overlay');
          if (hudOverlay) {
            if (progress > 0.82) {
              const fadeOut = Math.max(0, 1 - (progress - 0.82) / 0.12);
              hudOverlay.style.opacity = fadeOut;
            } else {
              hudOverlay.style.opacity = 1;
            }
          }

          // ==========================================
          // ACT 1: THE REVEAL (0.00 -> 0.30)
          // 360° Horizontal Camera Rotation
          // ==========================================
          if (progress <= 0.30) {
            this.currentAct = 1;
            const p = progress / 0.30; // 0 to 1

            // 360° smooth rotation ending directly front-facing at p=1
            this.cameraRig.rotation.y = 0.55 * (1 - p) + p * (Math.PI * 2);
            this.cameraRig.rotation.x = 0.12 * (1 - p) * Math.cos(p * Math.PI * 2);
            this.cameraRig.position.z = 0;
            this.cameraRig.position.y = 0;

            // HUD visibility
            if (act1Badge) act1Badge.style.opacity = Math.max(0, 1 - p * 1.5);
            if (act2Quote) act2Quote.style.opacity = 0;
            if (act3Quote) act3Quote.style.opacity = 0;

            // Aperture at normal f/2.8
            if (this.irisGroup) this.irisGroup.scale.set(0.65, 0.65, 1);
            if (this.shutterButton) this.shutterButton.position.y = 1.62;
          }

          // ==========================================
          // ACT 2: THE FACE OFF (0.30 -> 0.60)
          // Front Lock, Breathing, Quote Fade
          // ==========================================
          else if (progress > 0.30 && progress <= 0.60) {
            this.currentAct = 2;
            const p = (progress - 0.30) / 0.30;

            // Facing front dead center (optical axis straight at user)
            this.cameraRig.rotation.y = Math.PI * 2;
            this.cameraRig.rotation.x = 0;
            this.cameraRig.position.z = 0;
            this.cameraRig.position.y = 0;

            // Fade in quote at bottom center
            if (act1Badge) act1Badge.style.opacity = 0;
            if (act2Quote) {
              const quoteOpacity = p < 0.2 ? p * 5 : p > 0.8 ? (1 - p) * 5 : 1;
              act2Quote.style.opacity = quoteOpacity;
            }
            if (act3Quote) act3Quote.style.opacity = 0;

            // Reset flash trigger if user scrolled backwards
            if (progress < 0.58) this.hasFlashedAct3 = false;
          }

          // ==========================================
          // ACT 3: THE FLASH (0.60 -> 0.85)
          // Shutter Press, 150ms Flash, Shutter Click, Dark Quote
          // ==========================================
          else if (progress > 0.60 && progress <= 0.85) {
            this.currentAct = 3;
            const p = (progress - 0.60) / 0.25;

            this.cameraRig.rotation.y = Math.PI * 2;
            this.cameraRig.rotation.x = 0;
            this.cameraRig.position.z = 0;
            this.cameraRig.position.y = 0;

            if (act2Quote) act2Quote.style.opacity = 0;

            // 1. Shutter button visibly depresses
            if (this.shutterButton) {
              const depress = Math.min(p * 2, 1);
              this.shutterButton.position.y = 1.62 - depress * 0.12;
            }

            // 2. Iris contracts down then snaps open
            if (this.irisGroup) {
              const irisP = Math.sin(p * Math.PI);
              const scale = 0.7 - irisP * 0.55;
              this.irisGroup.scale.set(scale, scale, 1);
            }

            // 3. Strobe Flash Burst & Shutter Audio trigger (at ~68% scroll)
            if (progress >= 0.68 && !this.hasFlashedAct3) {
              this.hasFlashedAct3 = true;
              this.playNikonZ9Shutter();

              if (act3Flash) {
                act3Flash.style.opacity = '1';
                setTimeout(() => {
                  act3Flash.style.opacity = '0';
                }, 150);
              }
            }

            // 4. Quote emerges from black: "Capturamos lo que el tiempo quiere borrar"
            if (act3Quote) {
              if (progress >= 0.72) {
                const quoteP = (progress - 0.72) / 0.13;
                act3Quote.style.opacity = Math.min(quoteP * 1.5, 1);
              } else {
                act3Quote.style.opacity = 0;
              }
            }
          }

          // ==========================================
          // ACT 4: THE ABSORPTION (0.85 -> 1.00)
          // Iris opens to f/1.2, Camera zooms into viewer
          // ==========================================
          else if (progress > 0.85) {
            this.currentAct = 4;
            const p = (progress - 0.85) / 0.15; // 0 to 1

            if (act2Quote) act2Quote.style.opacity = 0;
            if (act3Quote) act3Quote.style.opacity = Math.max(0, 1 - p * 2);

            // Iris opens fully to f/1.2
            if (this.irisGroup) {
              this.irisGroup.scale.set(1.0, 1.0, 1);
            }

            // Camera surges forward directly into viewer's eyes
            // Centering optical axis with viewport
            this.cameraRig.position.z = p * 8.6;
            this.cameraRig.position.y = -p * 0.15;
            this.cameraRig.rotation.y = Math.PI * 2;
            this.cameraRig.rotation.x = 0;
            this.cameraRig.rotation.z = p * 0.35;
          }
        },
      });
    },

    // 8. INTERACTIVE CLICK & SOUND CONTROLS
    initInteractions: function () {
      // Audio toggle button
      const soundBtn = document.getElementById('sound-toggle-btn');
      if (soundBtn) {
        soundBtn.addEventListener('click', () => {
          this.soundEnabled = !this.soundEnabled;
          soundBtn.innerHTML = this.soundEnabled
            ? '<span>SONIDO: ON</span> 🔊'
            : '<span>SONIDO: OFF</span> 🔇';
          soundBtn.classList.toggle('muted', !this.soundEnabled);
          if (this.soundEnabled) this.playNikonZ9Shutter();
        });
      }

      // Re-trigger shutter on canvas or hero click
      const canvas = document.getElementById('webgl-canvas');
      if (canvas) {
        canvas.addEventListener('click', (e) => {
          // Depress shutter & trigger flash
          if (this.shutterButton) {
            this.shutterButton.position.y = 1.5;
            setTimeout(() => {
              this.shutterButton.position.y = 1.62;
            }, 180);
          }
          this.playNikonZ9Shutter();
          const flash = document.getElementById('flash-screen');
          if (flash) {
            flash.style.opacity = '1';
            setTimeout(() => {
              flash.style.opacity = '0';
            }, 120);
          }
        });
      }

      // Mouse Parallax in Act 2
      window.addEventListener('mousemove', (e) => {
        if (this.currentAct === 2 && this.cameraRig) {
          const mouseX = (e.clientX / window.innerWidth - 0.5) * 0.12;
          const mouseY = (e.clientY / window.innerHeight - 0.5) * 0.08;
          this.cameraRig.rotation.y = Math.PI * 2 + mouseX;
          this.cameraRig.rotation.x = mouseY;
        }
      });
    },

    // 9. ANIMATION RENDER LOOP (60-120 FPS)
    animate: function () {
      requestAnimationFrame(() => this.animate());

      const time = performance.now() * 0.001;

      // Subtle breathing in Act 2
      if (this.currentAct === 2 && this.cameraRig) {
        this.cameraRig.position.y = Math.sin(time * 2.2) * 0.04;
      }

      // Floating dust particles slow drift
      if (this.dustParticles) {
        const positions = this.dustParticles.geometry.attributes.position.array;
        for (let i = 0; i < positions.length; i += 3) {
          positions[i + 1] += Math.sin(time + positions[i]) * 0.002;
          positions[i] += Math.cos(time + positions[i + 2]) * 0.0015;
        }
        this.dustParticles.geometry.attributes.position.needsUpdate = true;
        this.dustParticles.rotation.y = time * 0.015;
      }

      this.renderer.render(this.scene, this.camera);
    },

    onWindowResize: function () {
      if (!this.camera || !this.renderer) return;
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    },
  };

  // Auto-init on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.Captoora3D.init());
  } else {
    window.Captoora3D.init();
  }
})();
