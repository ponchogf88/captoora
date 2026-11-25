import * as THREE from "./lib/three/three.module.js";
import { RoundedBoxGeometry } from "./lib/three/RoundedBoxGeometry.js";

/**
 * Deterministic 3D pastel matte voxel world for ¿Caíste o no caíste? (Short 01: P4 CFE).
 * Strictly zero neon. Pure function renderAt(t) driven by HyperFrames hf-seek / GSAP proxy.
 */
export function initWorld3D(canvas, config = {}) {
  const TIMINGS = {
    hookStart: config.hookStart ?? 0.0,
    hookEnd: config.hookEnd ?? 11.74,
    countdownStart: config.countdownStart ?? 11.74,
    countdownEnd: config.countdownEnd ?? 15.74,
    stealTime: config.stealTime ?? 14.39,
    revealStart: config.revealStart ?? 15.74,
    revealEnd: config.revealEnd ?? 35.44,
    guardrailStart: config.guardrailStart ?? 35.44,
    totalDuration: config.totalDuration ?? 48.67,
  };

  const WIDTH = 1080;
  const HEIGHT = 1920;

  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    preserveDrawingBuffer: true,
    powerPreference: "high-performance",
  });
  renderer.setPixelRatio(1);
  renderer.setSize(WIDTH, HEIGHT, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.06;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, WIDTH / HEIGHT, 0.2, 160);

  // Math helpers
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, t) => a + (b - a) * clamp(t, 0, 1);
  const smoothstep = (a, b, x) => {
    const u = clamp((x - a) / (b - a), 0, 1);
    return u * u * (3 - 2 * u);
  };
  const easeOutBack = (x) => {
    const u = clamp(x, 0, 1);
    const c1 = 1.70158;
    const c3 = c1 + 1;
    return 1 + c3 * Math.pow(u - 1, 3) + c1 * Math.pow(u - 1, 2);
  };

  // Sky texture (warm sunlit pastel gradient, zero neon)
  function makeSkyTexture() {
    const c = document.createElement("canvas");
    c.width = 16;
    c.height = 512;
    const ctx = c.getContext("2d");
    const g = ctx.createLinearGradient(0, 0, 0, 512);
    g.addColorStop(0.0, "#CBE7F7");
    g.addColorStop(0.52, "#EDF5EB");
    g.addColorStop(1.0, "#FDF0DA");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 16, 512);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
  }
  scene.background = makeSkyTexture();
  scene.fog = new THREE.Fog(0xfaeed8, 28, 72);

  // Lighting
  const hemi = new THREE.HemisphereLight(0xfff9ef, 0xdcc9b2, 1.0);
  scene.add(hemi);

  const keyLight = new THREE.DirectionalLight(0xfff0d4, 1.42);
  keyLight.castShadow = true;
  keyLight.shadow.mapSize.set(1024, 1024);
  keyLight.shadow.bias = -0.0005;
  const shadowSpan = 16;
  keyLight.shadow.camera.left = -shadowSpan;
  keyLight.shadow.camera.right = shadowSpan;
  keyLight.shadow.camera.top = shadowSpan;
  keyLight.shadow.camera.bottom = -shadowSpan;
  keyLight.shadow.camera.near = 2;
  keyLight.shadow.camera.far = 45;
  scene.add(keyLight);
  scene.add(keyLight.target);

  const fillLight = new THREE.DirectionalLight(0xdeeeff, 0.48);
  fillLight.position.set(-10, 8, 9);
  scene.add(fillLight);

  const rimLight = new THREE.DirectionalLight(0xffe0b2, 0.38);
  rimLight.position.set(-5, 9, -12);
  scene.add(rimLight);

  // Shared materials & geometry cache
  const matCache = new Map();
  function mat(color, opts = {}) {
    const key = `${color}_${opts.rough ?? 0.84}_${opts.metal ?? 0.04}_${opts.emissive ?? 0}_${opts.ei ?? 0}`;
    if (matCache.has(key)) return matCache.get(key);
    const m = new THREE.MeshStandardMaterial({
      color,
      roughness: opts.rough ?? 0.84,
      metalness: opts.metal ?? 0.04,
      emissive: opts.emissive ?? 0x000000,
      emissiveIntensity: opts.ei ?? 0,
    });
    matCache.set(key, m);
    return m;
  }

  function addBox(parent, size, pos, material, opts = {}) {
    const [w, h, d] = size;
    const radius = opts.radius ?? Math.min(w, h, d) * 0.16;
    const segs = opts.segs ?? 2;
    const geom =
      radius > 0.001
        ? new RoundedBoxGeometry(w, h, d, segs, radius)
        : new THREE.BoxGeometry(w, h, d);
    const mesh = new THREE.Mesh(geom, material);
    mesh.position.set(pos[0], pos[1], pos[2]);
    if (opts.rot) mesh.rotation.set(opts.rot[0], opts.rot[1], opts.rot[2]);
    mesh.castShadow = opts.cast !== false;
    mesh.receiveShadow = opts.recv !== false;
    parent.add(mesh);
    return mesh;
  }

  function addCyl(parent, rTop, rBot, h, pos, material, opts = {}) {
    const mesh = new THREE.Mesh(
      new THREE.CylinderGeometry(rTop, rBot, h, opts.seg ?? 20),
      material
    );
    mesh.position.set(pos[0], pos[1], pos[2]);
    if (opts.rot) mesh.rotation.set(opts.rot[0], opts.rot[1], opts.rot[2]);
    mesh.castShadow = opts.cast !== false;
    mesh.receiveShadow = opts.recv !== false;
    parent.add(mesh);
    return mesh;
  }

  // Rail path geometry: Semper Ascendens from bottom-left to summit-right
  const RAIL_START = new THREE.Vector3(-12.0, 0.45, 2.2);
  const RAIL_END = new THREE.Vector3(20.0, 6.65, -1.0);
  const RAIL_DIR = new THREE.Vector3().subVectors(RAIL_END, RAIL_START);
  const RAIL_LEN = RAIL_DIR.length();
  const RAIL_UNIT = RAIL_DIR.clone().normalize();
  const RAIL_YAW = Math.atan2(RAIL_DIR.x, RAIL_DIR.z);
  const RAIL_PITCH = -Math.asin(RAIL_DIR.y / RAIL_LEN);

  function railPos(u, target = new THREE.Vector3()) {
    return target.lerpVectors(RAIL_START, RAIL_END, u);
  }

  // Ground base pedestal & cobbled neighborhood lane
  addBox(scene, [54, 1.2, 22], [4, -0.6, -1.0], mat(0xd8ead2, { rough: 0.9 }), {
    radius: 0.2,
    cast: false,
  });
  addBox(scene, [54.4, 0.5, 22.4], [4, -1.35, -1.0], mat(0xc3ac8e, { rough: 0.92 }), {
    radius: 0.16,
    cast: false,
  });
  // Pastel cobblestone sidewalk strip along track corridor
  addBox(scene, [48, 0.12, 4.4], [4, 0.04, 1.4], mat(0xede2cf, { rough: 0.9 }), {
    radius: 0.05,
    cast: false,
  });

  // Neighborhood buildings & trees along the uphill corridor (all positioned behind track)
  function addVoxelTree(pos, foliageHex = 0x99d69c, height = 1.8) {
    const g = new THREE.Group();
    g.position.set(...pos);
    const trunkH = height * 0.45;
    addBox(g, [0.28, trunkH, 0.28], [0, trunkH * 0.5, 0], mat(0x9a7154), { radius: 0.05 });
    addBox(g, [1.05, 0.78, 1.05], [0, trunkH + 0.34, 0], mat(foliageHex), { radius: 0.16 });
    addBox(g, [0.7, 0.54, 0.7], [0, trunkH + 0.82, 0], mat(foliageHex), { radius: 0.14 });
    scene.add(g);
  }

  // 1) Pastel Panadería at x = -7.2
  {
    const bakery = new THREE.Group();
    bakery.position.set(-7.2, 0, -2.5);
    addBox(bakery, [3.8, 2.8, 2.8], [0, 1.4, 0], mat(0xf7cfd0), { radius: 0.14 });
    addBox(bakery, [4.0, 0.34, 3.0], [0, 2.9, 0], mat(0xf2a79f), { radius: 0.08 });
    for (let i = 0; i < 6; i++) {
      const col = i % 2 === 0 ? 0xf6988e : 0xfff8ed;
      addBox(bakery, [0.58, 0.22, 1.05], [-1.45 + i * 0.58, 1.65, 1.72], mat(col), {
        radius: 0.04,
        rot: [0.28, 0, 0],
      });
    }
    addBox(bakery, [0.8, 1.2, 0.14], [-1.0, 0.6, 1.4], mat(0x9d7052), { radius: 0.04 });
    addBox(bakery, [1.65, 0.9, 0.14], [0.6, 0.85, 1.4], mat(0xfff1c7, { emissive: 0xffd580, ei: 0.14 }), {
      radius: 0.06,
    });
    scene.add(bakery);
  }

  // 2) Sunny yellow Mexican house near P4 (x = -0.6)
  {
    const house = new THREE.Group();
    house.position.set(-0.6, 0, -2.8);
    addBox(house, [3.4, 3.3, 2.6], [0, 1.65, 0], mat(0xfbe39c), { radius: 0.14 });
    addBox(house, [3.65, 0.44, 2.85], [0, 3.45, 0], mat(0xde8263), { radius: 0.1 });
    addBox(house, [0.86, 1.35, 0.14], [0, 0.68, 1.3], mat(0x7fb4b8), { radius: 0.04 });
    addBox(house, [0.76, 0.76, 0.14], [-0.95, 2.25, 1.3], mat(0xfff5d8), { radius: 0.04 });
    addBox(house, [0.76, 0.76, 0.14], [0.95, 2.25, 1.3], mat(0xfff5d8), { radius: 0.04 });
    scene.add(house);
  }

  // 3) Mint corner office & ochre casita around Clues 1–2 (x = 5.4 and 10.6)
  {
    const mintShop = new THREE.Group();
    mintShop.position.set(5.6, 0, -3.1);
    addBox(mintShop, [3.5, 4.1, 2.7], [0, 2.05, 0], mat(0xbcd6c8), { radius: 0.14 });
    addBox(mintShop, [3.75, 0.34, 2.95], [0, 4.22, 0], mat(0xdf9273), { radius: 0.08 });
    for (let row = 0; row < 2; row++) {
      for (let col = 0; col < 3; col++) {
        addBox(
          mintShop,
          [0.68, 0.64, 0.12],
          [-0.95 + col * 0.95, 1.85 + row * 1.15, 1.35],
          mat(0xfff4cf, { emissive: 0xffd78a, ei: 0.12 }),
          { radius: 0.04 }
        );
      }
    }
    scene.add(mintShop);

    const casita = new THREE.Group();
    casita.position.set(11.2, 0, -3.6);
    addBox(casita, [3.8, 4.8, 2.8], [0, 2.4, 0], mat(0xf6dfba), { radius: 0.14 });
    addBox(casita, [4.05, 0.4, 3.05], [0, 4.95, 0], mat(0xc97b63), { radius: 0.08 });
    addBox(casita, [0.9, 1.1, 0.12], [-0.95, 3.6, 1.4], mat(0xfff5d8), { radius: 0.04 });
    addBox(casita, [0.9, 1.1, 0.12], [0.95, 3.6, 1.4], mat(0xfff5d8), { radius: 0.04 });
    addBox(casita, [0.95, 1.5, 0.14], [0, 0.75, 1.4], mat(0x6b7c93), { radius: 0.04 });
    scene.add(casita);
  }

  // 4) Sunny plaza terrace behind P5 crest (x = 16.5)
  {
    const terrace = new THREE.Group();
    terrace.position.set(16.6, 0, -3.2);
    addBox(terrace, [5.6, 4.2, 3.6], [0, 2.1, 0], mat(0xe8dac4), { radius: 0.16 });
    addBox(terrace, [3.2, 2.4, 2.4], [0.5, 5.4, -0.3], mat(0xf9d8b6), { radius: 0.14 });
    addBox(terrace, [3.45, 0.34, 2.6], [0.5, 6.72, -0.3], mat(0x7fb4b8), { radius: 0.08 });
    scene.add(terrace);
  }

  // Trees & cozy lamps framing corridor cleanly behind/beside rails
  [
    [-10.8, 0, -1.4, 0x99d69c, 2.0],
    [-4.1, 0, -2.0, 0xa5dd9e, 1.85],
    [2.5, 0, -2.4, 0x8bc996, 2.1],
    [8.4, 0, -2.8, 0x9bd79e, 2.2],
    [13.6, 0, -2.2, 0x87c694, 2.4],
    [19.8, 0, -2.4, 0x96d49b, 2.5],
  ].forEach(([x, y, z, col, h]) => addVoxelTree([x, y, z], col, h));

  // Vintage pastel streetlamps behind track corridor so legs & shoes on rails are 100% unobstructed
  for (const lx of [-6.0, 2.2, 10.2]) {
    const lamp = new THREE.Group();
    lamp.position.set(lx, 0, -1.65);
    addBox(lamp, [0.16, 2.15, 0.16], [0, 1.08, 0], mat(0x626978), { radius: 0.04 });
    addBox(lamp, [0.42, 0.38, 0.42], [0, 2.28, 0], mat(0xffe9a6, { emissive: 0xffd275, ei: 0.22 }), {
      radius: 0.08,
    });
    scene.add(lamp);
  }

  // Continuous Ascending Viaduct Guardrails + Wooden Ties + Cream Stone Piers
  const trackGroup = new THREE.Group();
  const trackMid = new THREE.Vector3().addVectors(RAIL_START, RAIL_END).multiplyScalar(0.5);
  const trackHolder = new THREE.Group();
  trackHolder.position.copy(trackMid);
  trackHolder.rotation.order = "YXZ";
  trackHolder.rotation.y = RAIL_YAW;
  trackHolder.rotation.x = RAIL_PITCH;

  const railMat = mat(0x98a4b3, { rough: 0.38, metal: 0.55 });
  const tieMat = mat(0x9c6e4b, { rough: 0.86 });
  const pierMat = mat(0xe6d6bf, { rough: 0.88 });
  const gauge = 0.86;

  // Base rails up to u = 0.71, plus fixed final extension after u = 0.84
  const seg1Len = RAIL_LEN * 0.71;
  const seg1CenterZ = (0.355 - 0.5) * RAIL_LEN;
  addBox(trackHolder, [0.13, 0.14, seg1Len], [-gauge * 0.5, 0.12, seg1CenterZ], railMat, { radius: 0.03 });
  addBox(trackHolder, [0.13, 0.14, seg1Len], [gauge * 0.5, 0.12, seg1CenterZ], railMat, { radius: 0.03 });

  const seg3Len = RAIL_LEN * 0.16;
  const seg3CenterZ = (0.92 - 0.5) * RAIL_LEN;
  addBox(trackHolder, [0.13, 0.14, seg3Len], [-gauge * 0.5, 0.12, seg3CenterZ], railMat, { radius: 0.03 });
  addBox(trackHolder, [0.13, 0.14, seg3Len], [gauge * 0.5, 0.12, seg3CenterZ], railMat, { radius: 0.03 });

  // Detachable Warm-Gold Guardrail Segment (u in [0.71, 0.84]) placed by Antigravity at t = 35.44..38.2s
  const goldRailSeg = new THREE.Group();
  const goldSegLen = RAIL_LEN * 0.145;
  const goldSegCenterZ = (0.775 - 0.5) * RAIL_LEN;
  const goldBeamMat = mat(0xf6c945, { rough: 0.42, metal: 0.25, emissive: 0xe6a825, ei: 0.18 });
  goldRailSeg.position.set(0, 0, goldSegCenterZ);
  addBox(goldRailSeg, [0.16, 0.16, goldSegLen], [-gauge * 0.5, 0.13, 0], goldBeamMat, { radius: 0.04 });
  addBox(goldRailSeg, [0.16, 0.16, goldSegLen], [gauge * 0.5, 0.13, 0], goldBeamMat, { radius: 0.04 });
  for (let k = -2; k <= 2; k++) {
    addBox(goldRailSeg, [gauge + 0.5, 0.1, 0.2], [0, 0.04, k * (goldSegLen * 0.2)], tieMat, { radius: 0.025 });
  }
  trackHolder.add(goldRailSeg);

  // Ties along entire viaduct
  const TIE_COUNT = 44;
  for (let i = 0; i < TIE_COUNT; i++) {
    const u = i / (TIE_COUNT - 1);
    const z = (u - 0.5) * (RAIL_LEN - 0.5);
    addBox(trackHolder, [gauge + 0.48, 0.1, 0.2], [0, 0.03, z], tieMat, { radius: 0.025 });
  }
  trackGroup.add(trackHolder);

  // Viaduct support piers down to ground
  for (let i = 0; i < 11; i++) {
    const u = 0.04 + (i / 10) * 0.92;
    const p = railPos(u);
    const h = Math.max(0.3, p.y);
    addBox(trackGroup, [0.54, h, 0.54], [p.x, h * 0.5, p.z], pierMat, { radius: 0.08 });
  }
  scene.add(trackGroup);

  // Circular Duolingo-in-Reverse Checkpoint Pads on track
  const pads = [
    { u: 0.1, r: 0.72, top: 0xeec467, rim: 0xc29336 }, // P3 passed
    { u: 0.345, r: 1.05, top: 0xf9d14b, rim: 0xd19f24 }, // P4 main station!
    { u: 0.48, r: 0.76, top: 0xf5ecd9, rim: 0xcbbba0 }, // Clue 1
    { u: 0.6, r: 0.76, top: 0xf5ecd9, rim: 0xcbbba0 }, // Clue 2
    { u: 0.71, r: 0.8, top: 0xf5ecd9, rim: 0xcbbba0 }, // Clue 3 / Guardrail junction
    { u: 0.88, r: 0.95, top: 0x7be0b4, rim: 0x4ca87f }, // P5 crest
  ];
  pads.forEach((pd) => {
    const p = railPos(pd.u);
    addCyl(scene, pd.r, pd.r * 1.06, 0.16, [p.x, p.y + 0.06, p.z], mat(pd.top, { rough: 0.72 }), { seg: 24 });
    addCyl(scene, pd.r * 1.06, pd.r * 1.08, 0.1, [p.x, p.y - 0.04, p.z], mat(pd.rim, { rough: 0.85 }), { seg: 24 });
  });

  // 3 Milestone Flip Flags along u = 0.48, 0.60, 0.71 (spring up when hero climbs past!)
  const milestoneFlags = [0.48, 0.6, 0.71].map((u) => {
    const p = railPos(u);
    const grp = new THREE.Group();
    grp.position.set(p.x, p.y + 0.14, p.z - 0.92);
    addBox(grp, [0.12, 1.35, 0.12], [0, 0.68, 0], mat(0x6b5b4f), { radius: 0.03 });
    const flagPivot = new THREE.Group();
    flagPivot.position.set(0, 1.22, 0);
    const banner = addBox(flagPivot, [0.72, 0.44, 0.09], [0.36, 0, 0], mat(0xf6c945), { radius: 0.04 });
    grp.add(flagPivot);
    scene.add(grp);
    return { grp, flagPivot, banner, u };
  });

  // Golden Finish Arch at P5 crest (u = 0.895, cleanly behind/ahead of final wave stop at u = 0.85)
  {
    const crest = railPos(0.895);
    const arch = new THREE.Group();
    arch.position.set(crest.x, crest.y + 0.14, crest.z);
    arch.rotation.y = RAIL_YAW;
    const gold = mat(0xeec467, { rough: 0.42, metal: 0.28 });
    addBox(arch, [0.24, 2.3, 0.24], [-0.92, 1.15, 0], gold, { radius: 0.05 });
    addBox(arch, [0.24, 2.3, 0.24], [0.92, 1.15, 0], gold, { radius: 0.05 });
    addBox(arch, [2.2, 0.36, 0.36], [0, 2.36, 0], gold, { radius: 0.07 });
    addBox(arch, [0.58, 0.4, 0.12], [0.9, 2.74, 0], mat(0xe38a73), { radius: 0.04 });
    scene.add(arch);
  }

  // Drifting pastel clouds in sky (purely deterministic wrt t)
  const clouds = [];
  for (let i = 0; i < 6; i++) {
    const cl = new THREE.Group();
    const bx = -14 + i * 7.2;
    const by = 8.4 + (i % 3) * 1.4;
    const bz = -9.5 - (i % 2) * 3.0;
    addBox(cl, [2.6, 0.85, 1.3], [0, 0, 0], mat(0xfffdf8, { rough: 0.95 }), { radius: 0.28, cast: false });
    addBox(cl, [1.5, 0.72, 1.1], [0.35, 0.55, 0], mat(0xfffdf8, { rough: 0.95 }), { radius: 0.24, cast: false });
    cl.position.set(bx, by, bz);
    scene.add(cl);
    clouds.push({ mesh: cl, baseX: bx, y: by, z: bz, speed: 0.14 + (i % 3) * 0.05 });
  }

  // Shared cute cube face builder returning eye meshes for natural blinking!
  function addCubeFace(head, opts = {}) {
    const z = (opts.depth ?? 1.24) * 0.5 + 0.02;
    const eyeY = opts.eyeY ?? 0.04;
    const eyeX = opts.eyeX ?? 0.29;
    const eyeMat = mat(0x232026, { rough: 0.25, metal: 0.1 });
    const hlMat = mat(0xffffff, { rough: 0.2 });
    const eyes = [];

    if (opts.sunglasses) {
      const frame = mat(0x1f1d26, { rough: 0.3, metal: 0.2 });
      addBox(head, [0.48, 0.28, 0.1], [-0.31, eyeY + 0.03, z + 0.04], frame, { radius: 0.06 });
      addBox(head, [0.48, 0.28, 0.1], [0.31, eyeY + 0.03, z + 0.04], frame, { radius: 0.06 });
      addBox(head, [0.18, 0.07, 0.08], [0, eyeY + 0.07, z + 0.04], frame, { radius: 0.02 });
    } else {
      for (const sx of [-1, 1]) {
        const eg = new THREE.Group();
        eg.position.set(sx * eyeX, eyeY, z);
        addBox(eg, [0.16, 0.22, 0.08], [0, 0, 0], eyeMat, { radius: 0.04 });
        addBox(eg, [0.055, 0.055, 0.03], [0.035, 0.055, 0.04], hlMat, { radius: 0.01, cast: false });
        head.add(eg);
        eyes.push(eg);
      }
    }

    if (opts.glasses) {
      const ringMat = mat(0x3a373d, { rough: 0.35, metal: 0.35 });
      for (const sx of [-1, 1]) {
        const g = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.032, 10, 20), ringMat);
        g.position.set(sx * eyeX, eyeY, z + 0.05);
        head.add(g);
      }
      addBox(head, [0.26, 0.04, 0.04], [0, eyeY + 0.02, z + 0.05], ringMat, { radius: 0.01 });
    }

    if (opts.cheeks !== false) {
      const cheekMat = mat(opts.cheekCol ?? 0xf49d92, { rough: 0.85 });
      addBox(head, [0.16, 0.08, 0.04], [-0.44, eyeY - 0.19, z], cheekMat, { radius: 0.025, cast: false });
      addBox(head, [0.16, 0.08, 0.04], [0.44, eyeY - 0.19, z], cheekMat, { radius: 0.025, cast: false });
    }

    const mouthMat = mat(0x3a2a28, { rough: 0.5 });
    if (opts.smirk) {
      addBox(head, [0.24, 0.06, 0.04], [0.07, eyeY - 0.27, z], mouthMat, {
        radius: 0.02,
        rot: [0, 0, 0.16],
        cast: false,
      });
    } else {
      addBox(head, [0.26, 0.065, 0.04], [0, eyeY - 0.27, z], mouthMat, { radius: 0.025, cast: false });
      addBox(head, [0.07, 0.07, 0.04], [-0.14, eyeY - 0.24, z], mouthMat, { radius: 0.02, cast: false });
      addBox(head, [0.07, 0.07, 0.04], [0.14, eyeY - 0.24, z], mouthMat, { radius: 0.02, cast: false });
    }
    return eyes;
  }

  // --- ARTICULATED RIG 1: Antigravity "Guardrails" ---
  function buildGuardrailsRig() {
    const root = new THREE.Group();
    const walkPivot = new THREE.Group();
    root.add(walkPivot);

    const shoeMat = mat(0x6b7c93);
    const pantsMat = mat(0xe3cfa9);
    const bodyMat = mat(0x7cc4e8);
    const skinMat = mat(0xf8cfb8);
    const harnessY = mat(0xf6c945);
    const harnessC = mat(0xf08c6c);
    const helmetMat = mat(0xf9d14b, { rough: 0.65 });

    // Hip pivots so soles cleanly sit at y = 0 at rest
    const leftLeg = new THREE.Group();
    leftLeg.position.set(-0.28, 0.68, 0);
    addBox(leftLeg, [0.38, 0.46, 0.4], [0, -0.22, 0], pantsMat, { radius: 0.08 });
    addBox(leftLeg, [0.42, 0.24, 0.58], [0, -0.56, 0.06], shoeMat, { radius: 0.07 });
    walkPivot.add(leftLeg);

    const rightLeg = new THREE.Group();
    rightLeg.position.set(0.28, 0.68, 0);
    addBox(rightLeg, [0.38, 0.46, 0.4], [0, -0.22, 0], pantsMat, { radius: 0.08 });
    addBox(rightLeg, [0.42, 0.24, 0.58], [0, -0.56, 0.06], shoeMat, { radius: 0.07 });
    walkPivot.add(rightLeg);

    // Torso pivot
    const torso = new THREE.Group();
    torso.position.set(0, 0.72, 0);
    addBox(torso, [1.14, 1.02, 0.78], [0, 0.46, 0], bodyMat, { radius: 0.18 });
    addBox(torso, [0.22, 1.06, 0.85], [-0.34, 0.47, 0], harnessY, { radius: 0.05 });
    addBox(torso, [0.22, 1.06, 0.85], [0.34, 0.47, 0], harnessY, { radius: 0.05 });
    addBox(torso, [1.22, 0.18, 0.86], [0, 0.18, 0], harnessC, { radius: 0.05 });
    addBox(torso, [0.85, 0.14, 0.86], [0, 0.45, 0], harnessY, { radius: 0.04, rot: [0, 0, 0.45] });
    addBox(torso, [0.85, 0.14, 0.86], [0, 0.45, 0], harnessY, { radius: 0.04, rot: [0, 0, -0.45] });
    addBox(torso, [0.28, 0.22, 0.1], [0, 0.42, 0.43], mat(0xd8b16a, { rough: 0.35, metal: 0.6 }), { radius: 0.04 });

    const leftArm = new THREE.Group();
    leftArm.position.set(-0.68, 0.82, 0);
    addBox(leftArm, [0.32, 0.66, 0.34], [-0.08, -0.28, 0], bodyMat, { radius: 0.1 });
    addBox(leftArm, [0.28, 0.25, 0.28], [-0.08, -0.66, 0.02], skinMat, { radius: 0.09 });
    torso.add(leftArm);

    const rightArm = new THREE.Group();
    rightArm.position.set(0.68, 0.82, 0);
    addBox(rightArm, [0.32, 0.66, 0.34], [0.08, -0.28, 0], bodyMat, { radius: 0.1 });
    addBox(rightArm, [0.28, 0.25, 0.28], [0.08, -0.66, 0.02], skinMat, { radius: 0.09 });
    torso.add(rightArm);

    // Carried golden beam (shown overhead when placing guardrail around 35.44..37.2s)
    const heldBeam = new THREE.Group();
    heldBeam.position.set(0, 2.25, 0.25);
    addBox(heldBeam, [2.1, 0.2, 0.24], [0, 0, 0], goldBeamMat, { radius: 0.05 });
    addBox(heldBeam, [0.22, 0.24, 0.56], [-0.85, 0, 0], tieMat, { radius: 0.03 });
    addBox(heldBeam, [0.22, 0.24, 0.56], [0.85, 0, 0], tieMat, { radius: 0.03 });
    heldBeam.visible = false;
    torso.add(heldBeam);

    const head = new THREE.Group();
    head.position.set(0, 1.48, 0);
    addBox(head, [1.34, 1.18, 1.24], [0, 0, 0], skinMat, { radius: 0.24 });
    const eyes = addCubeFace(head, { depth: 1.24, eyeY: 0.02, eyeX: 0.29 });
    addBox(head, [1.5, 0.58, 1.38], [0, 0.56, -0.02], helmetMat, { radius: 0.22 });
    addBox(head, [1.14, 0.24, 1.12], [0, 0.84, -0.02], helmetMat, { radius: 0.1 });
    addBox(head, [1.46, 0.12, 0.46], [0, 0.34, 0.68], helmetMat, { radius: 0.05 });
    addBox(head, [0.28, 0.26, 0.1], [0, 0.62, 0.67], bodyMat, { radius: 0.04 });
    torso.add(head);

    walkPivot.add(torso);
    scene.add(root);
    return { root, walkPivot, leftLeg, rightLeg, torso, leftArm, rightArm, head, eyes, heldBeam };
  }
  const hero = buildGuardrailsRig();

  // --- ARTICULATED RIG 2: ChatGPT (Mint Host on P4 Terrace) ---
  function buildChatGptRig() {
    const root = new THREE.Group();
    const bounce = new THREE.Group();
    root.add(bounce);

    const mint = mat(0x7be0b4);
    const cream = mat(0xfaf8f0);
    addBox(bounce, [0.4, 0.24, 0.48], [-0.34, 0.12, 0.05], cream, { radius: 0.08 });
    addBox(bounce, [0.4, 0.24, 0.48], [0.34, 0.12, 0.05], cream, { radius: 0.08 });
    addBox(bounce, [1.46, 1.46, 1.34], [0, 0.98, 0], mint, { radius: 0.26 });
    addBox(bounce, [1.08, 0.4, 0.16], [0, 0.52, 0.64], cream, { radius: 0.08 });
    addBox(bounce, [0.16, 0.26, 0.16], [0, 1.82, 0], cream, { radius: 0.05 });
    addBox(bounce, [0.32, 0.22, 0.32], [0, 1.98, 0], mat(0xa8ecd0), { radius: 0.09 });

    const leftArm = new THREE.Group();
    leftArm.position.set(-0.84, 1.2, 0.02);
    addBox(leftArm, [0.3, 0.66, 0.3], [0, -0.24, 0], cream, { radius: 0.1 });
    bounce.add(leftArm);

    const rightArm = new THREE.Group();
    rightArm.position.set(0.84, 1.2, 0.02);
    addBox(rightArm, [0.3, 0.66, 0.3], [0, -0.24, 0], cream, { radius: 0.1 });
    bounce.add(rightArm);

    const face = new THREE.Group();
    face.position.set(0, 1.08, 0);
    const eyes = addCubeFace(face, { depth: 1.34, glasses: true, eyeY: 0.06, eyeX: 0.31 });
    bounce.add(face);

    const p4 = railPos(0.395);
    root.position.set(p4.x + 0.35, p4.y + 0.05, p4.z - 1.15);
    root.rotation.y = -0.28;
    scene.add(root);
    return { root, bounce, leftArm, rightArm, eyes };
  }
  const chatgpt = buildChatGptRig();

  // --- 3D VOXEL "2" CUBE ON P4 PEDESTAL + GROK THIEF RIG ---
  function makeDigitTexture(digitStr) {
    const c = document.createElement("canvas");
    c.width = 256;
    c.height = 256;
    const ctx = c.getContext("2d");
    ctx.fillStyle = "#FFF7E8";
    ctx.fillRect(0, 0, 256, 256);
    ctx.strokeStyle = "#2B2420";
    ctx.lineWidth = 18;
    ctx.strokeRect(12, 12, 232, 232);
    ctx.fillStyle = "#DC554B";
    ctx.font = "900 175px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(digitStr, 128, 136);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
  }
  const digit2Group = new THREE.Group();
  const d2Tex = makeDigitTexture("2");
  const d2Mat = new THREE.MeshStandardMaterial({ map: d2Tex, roughness: 0.55 });
  const d2Mesh = new THREE.Mesh(new RoundedBoxGeometry(0.95, 0.95, 0.95, 2, 0.12), d2Mat);
  d2Mesh.castShadow = true;
  digit2Group.add(d2Mesh);
  scene.add(digit2Group);

  function buildGrokRig() {
    const root = new THREE.Group();
    const body = new THREE.Group();
    root.add(body);

    const charcoal = mat(0x3f4052);
    const plum = mat(0x6d568c);
    const plumSoft = mat(0x8a70ad);
    const cream = mat(0xf6ecd9);

    const leftLeg = new THREE.Group();
    leftLeg.position.set(-0.34, 0.34, 0);
    addBox(leftLeg, [0.42, 0.28, 0.54], [0, -0.2, 0.04], charcoal, { radius: 0.08 });
    body.add(leftLeg);

    const rightLeg = new THREE.Group();
    rightLeg.position.set(0.34, 0.34, 0);
    addBox(rightLeg, [0.42, 0.28, 0.54], [0, -0.2, 0.04], charcoal, { radius: 0.08 });
    body.add(rightLeg);

    addBox(body, [1.5, 1.48, 1.36], [0, 1.05, 0], charcoal, { radius: 0.26 });
    addBox(body, [1.58, 0.58, 1.44], [0, 0.62, 0], plum, { radius: 0.2 });
    addBox(body, [1.64, 0.34, 0.54], [0, 1.48, -0.48], plumSoft, { radius: 0.14 });

    const leftArm = new THREE.Group();
    leftArm.position.set(-0.88, 1.24, 0);
    addBox(leftArm, [0.3, 0.68, 0.3], [0, -0.26, 0], plum, { radius: 0.1 });
    body.add(leftArm);

    const rightArm = new THREE.Group();
    rightArm.position.set(0.88, 1.24, 0);
    addBox(rightArm, [0.3, 0.68, 0.3], [0, -0.26, 0], plum, { radius: 0.1 });
    // Oversized brass stopwatch in right hand
    const watch = new THREE.Group();
    watch.position.set(0.1, -0.66, 0.26);
    const brass = mat(0xdab068, { rough: 0.38, metal: 0.45 });
    addCyl(watch, 0.36, 0.36, 0.16, [0, 0, 0], brass, { rot: [Math.PI / 2, 0, 0], seg: 18 });
    addCyl(watch, 0.28, 0.28, 0.18, [0, 0, 0.01], cream, { rot: [Math.PI / 2, 0, 0], seg: 18 });
    addBox(watch, [0.05, 0.2, 0.04], [0.06, 0.06, 0.1], mat(0xd45b55), { radius: 0.02, rot: [0, 0, -0.7] });
    rightArm.add(watch);
    body.add(rightArm);

    const face = new THREE.Group();
    face.position.set(0, 1.22, 0);
    addCubeFace(face, { depth: 1.36, sunglasses: true, smirk: true, cheeks: false, eyeY: 0.05 });
    body.add(face);

    scene.add(root);
    return { root, body, leftLeg, rightLeg, leftArm, rightArm };
  }
  const grok = buildGrokRig();

  // Deterministic puff dust cubes when Grok bolts away
  const dustPuffs = [];
  for (let i = 0; i < 4; i++) {
    const m = addBox(scene, [0.42, 0.42, 0.42], [0, -5, 0], mat(0xeae0f4), { radius: 0.12 });
    m.visible = false;
    dustPuffs.push(m);
  }

  // Natural deterministic blink helper
  function applyBlink(eyes, t, offset = 0) {
    const cyc = (t + offset) % 3.6;
    const blinkScale = cyc < 0.14 ? 0.12 : 1.0;
    for (const e of eyes) e.scale.y = blinkScale;
  }

  // Walk cycle + smooth idle pose blending
  function poseHeroWalking(walkPhase, walkAmt, jumpY = 0, handsUp = 0, fistPump = 0, waveAmt = 0) {
    const stride = Math.sin(walkPhase) * 0.62 * walkAmt;
    hero.leftLeg.rotation.x = stride;
    hero.rightLeg.rotation.x = -stride;

    // Counter-swinging arms unless overridden by reaction/wave/fist
    let lArmX = -stride * 0.85;
    let rArmX = stride * 0.85;
    let lArmZ = -0.14;
    let rArmZ = 0.14;

    if (handsUp > 0) {
      rArmZ = lerp(rArmZ, 2.35, handsUp);
      lArmZ = lerp(lArmZ, -2.25, handsUp);
      rArmX = lerp(rArmX, -0.3, handsUp);
      lArmX = lerp(lArmX, -0.3, handsUp);
    }
    if (fistPump > 0) {
      rArmZ = lerp(rArmZ, 2.55, fistPump);
      rArmX = lerp(rArmX, -0.2, fistPump);
    }
    if (waveAmt > 0) {
      rArmZ = lerp(rArmZ, 2.3 + Math.sin(walkPhase * 1.4) * 0.25, waveAmt);
      rArmX = lerp(rArmX, -0.15, waveAmt);
    }

    hero.leftArm.rotation.set(lArmX, 0, lArmZ);
    hero.rightArm.rotation.set(rArmX, 0, rArmZ);

    const stepBob = Math.abs(Math.sin(walkPhase)) * 0.14 * walkAmt;
    hero.walkPivot.position.y = stepBob + jumpY;
    hero.torso.rotation.x = 0.09 * walkAmt;
    hero.torso.rotation.y = Math.cos(walkPhase) * 0.08 * walkAmt;
  }

  // Hero u(t) trajectory along the ascending rails (P3->P4->Clue1->Clue2->Clue3->P5)
  function heroProgressAt(t) {
    if (t <= 11.15) {
      return lerp(0.08, 0.345, smoothstep(0.0, 11.15, t));
    }
    if (t <= 16.5) {
      return 0.345;
    }
    if (t <= 22.8) {
      return lerp(0.345, 0.48, smoothstep(16.5, 22.1, t));
    }
    if (t <= 29.0) {
      return lerp(0.48, 0.6, smoothstep(22.8, 28.3, t));
    }
    if (t <= 35.44) {
      return lerp(0.6, 0.71, smoothstep(29.0, 34.7, t));
    }
    if (t <= 38.2) {
      return 0.71;
    }
    return lerp(0.71, 0.85, smoothstep(38.2, 47.6, t));
  }

  // Hero speed factor for continuous walk weight
  function isWalkingWeight(t) {
    if (t < 10.95) return 1.0 - smoothstep(10.8, 11.2, t);
    if (t >= 16.4 && t < 22.25) return smoothstep(16.4, 16.75, t) * (1 - smoothstep(21.9, 22.25, t));
    if (t >= 22.7 && t < 28.45) return smoothstep(22.7, 23.05, t) * (1 - smoothstep(28.1, 28.45, t));
    if (t >= 28.9 && t < 34.85) return smoothstep(28.9, 29.25, t) * (1 - smoothstep(34.5, 34.85, t));
    if (t >= 38.15 && t < 47.65) return smoothstep(38.15, 38.55, t) * (1 - smoothstep(47.15, 47.65, t));
    return 0.0;
  }

  let lastRenderedT = -1;
  const _heroPos = new THREE.Vector3();
  const _camTarget = new THREE.Vector3();
  const _camPos = new THREE.Vector3();

  function renderAt(rawT) {
    const t = clamp(Number(rawT) || 0, 0, TIMINGS.totalDuration);
    if (Math.abs(t - lastRenderedT) < 1e-5) return;
    lastRenderedT = t;

    // 1) Clouds gently drifting left-to-right across sky
    clouds.forEach((c) => {
      c.mesh.position.x = c.baseX + t * c.speed;
    });

    // 2) Hero progression & acting along ascending rails
    const u = heroProgressAt(t);
    railPos(u, _heroPos);
    hero.root.position.set(_heroPos.x, _heroPos.y + 0.14, _heroPos.z + 0.05);

    const wAmt = isWalkingWeight(t);
    const walkPhase = t * 6.8 + 0.9; // Frame 0 starts crisply mid-stride!

    // Facing angle: 3/4 uphill while walking, turns smoothly toward camera when acting
    const yawWalk = 0.88;
    const yawCam = 0.24;
    hero.root.rotation.y = lerp(yawCam, yawWalk, wAmt);

    // Special reactions:
    let jumpY = 0;
    let handsUp = 0;
    let fistPump = 0;
    let waveAmt = 0;
    let squashY = 1.0;

    // Stolen-second reaction hop at t = 14.39..15.55
    if (t >= 14.38 && t <= 15.65) {
      const rp = (t - 14.38) / 1.15;
      jumpY = Math.sin(clamp(rp, 0, 1) * Math.PI) * 0.65;
      handsUp = Math.sin(clamp(rp, 0, 1) * Math.PI);
      squashY = rp < 0.15 ? 0.84 : rp < 0.45 ? 1.12 : 1.0;
      hero.head.rotation.y = lerp(0, 0.45, Math.sin(clamp(rp, 0, 1) * Math.PI));
    } else if (t >= 15.74 && t <= 16.65) {
      fistPump = Math.sin(smoothstep(15.74, 16.05, t) * Math.PI * 0.5) * (1 - smoothstep(16.35, 16.65, t));
      hero.head.rotation.y = 0;
    } else if (t >= 35.44 && t <= 38.2) {
      // Holding & placing the golden guardrail beam
      const liftP = smoothstep(35.44, 36.4, t);
      const dropP = smoothstep(36.4, 37.25, t);
      handsUp = (1 - dropP) * liftP;
      hero.heldBeam.visible = t < 37.15;
      hero.heldBeam.position.y = lerp(2.05, 1.35, dropP);
      if (t >= 37.15 && t <= 37.55) {
        const sp = (t - 37.15) / 0.4;
        squashY = 1 - Math.sin(sp * Math.PI) * 0.14;
      }
      hero.head.rotation.y = 0;
    } else {
      hero.heldBeam.visible = false;
      hero.head.rotation.y = Math.sin(t * 1.1) * 0.16;
    }

    if (t >= 43.8) {
      waveAmt = smoothstep(43.8, 44.3, t);
    }

    poseHeroWalking(walkPhase, wAmt, jumpY, handsUp, fistPump, waveAmt);
    hero.root.scale.set(1 / Math.sqrt(squashY), squashY, 1 / Math.sqrt(squashY));
    applyBlink(hero.eyes, t, 0.4);

    // 3) Golden detachable track segment flies smoothly from Antigravity into viaduct (t=36.5..37.4s)
    if (t < 36.4) {
      goldRailSeg.visible = false;
    } else if (t < 37.4) {
      goldRailSeg.visible = true;
      const dropEase = easeOutBack((t - 36.4) / 0.9);
      goldRailSeg.position.y = lerp(2.2, 0.0, dropEase);
    } else {
      goldRailSeg.visible = true;
      goldRailSeg.position.y = 0.0;
    }

    // 4) Milestone flags spring up brightly as hero climbs past each checkpoint
    milestoneFlags.forEach((mf) => {
      const pop = easeOutBack((u - (mf.u - 0.02)) / 0.04);
      const reached = u >= mf.u - 0.02;
      mf.flagPivot.scale.setScalar(reached ? Math.max(0.15, pop) : 0.25);
      mf.banner.material = reached ? mat(0xf6c945) : mat(0xd8cfc2);
    });

    // 5) ChatGPT cheers on P4 platform
    const gptHop = Math.abs(Math.sin(t * 3.8)) * 0.12;
    chatgpt.bounce.position.y = gptHop;
    chatgpt.rightArm.rotation.z = 1.9 + Math.sin(t * 4.5) * 0.28;
    chatgpt.leftArm.rotation.z = -0.25;
    applyBlink(chatgpt.eyes, t, 1.8);

    // 6) Floating 3D "2" cube + Grok heist at P4 (t = 14.15..15.65)
    const p4Station = railPos(0.375);
    const p4CubeRestX = p4Station.x + 1.05;
    const p4CubeRestY = p4Station.y + 1.65;
    const p4CubeRestZ = p4Station.z + 0.35;

    if (t >= 11.74 && t <= 15.65) {
      if (t < 14.12) {
        grok.root.visible = false;
        digit2Group.visible = true;
        digit2Group.position.set(p4CubeRestX, p4CubeRestY + Math.sin(t * 3.2) * 0.1, p4CubeRestZ);
        digit2Group.rotation.set(0, Math.sin(t * 2.0) * 0.25, 0);
        digit2Group.scale.setScalar(smoothstep(11.74, 12.1, t));
      } else {
        grok.root.visible = true;
        const heistPhase = t - 14.12; // 0..1.53s (steal at ~0.27s = t 14.39)
        const grabDone = smoothstep(0.0, 0.34, heistPhase); // reaches cube around t=14.46
        const dashOut = smoothstep(0.48, 1.48, heistPhase);

        const gx = lerp(p4CubeRestX + 4.2, p4CubeRestX - 0.15, grabDone) + dashOut * 6.4;
        const gy = p4Station.y + 0.1 + Math.abs(Math.sin(t * 14)) * 0.22;
        const gz = p4CubeRestZ + 0.28;
        grok.root.position.set(gx, gy, gz);
        grok.root.rotation.y = dashOut > 0.05 ? 0.95 : -0.65;
        grok.leftLeg.rotation.x = Math.sin(t * 15) * 0.72;
        grok.rightLeg.rotation.x = -Math.sin(t * 15) * 0.72;
        grok.leftArm.rotation.z = -1.75;
        grok.rightArm.rotation.z = 0.55 + Math.sin(t * 15) * 0.35;

        // "2" cube stays at pedestal until Grok's arm arrives, then rides on Grok's shoulder!
        digit2Group.visible = true;
        if (t < TIMINGS.stealTime) {
          digit2Group.position.set(p4CubeRestX, p4CubeRestY, p4CubeRestZ);
          digit2Group.rotation.set(0, 0, 0);
        } else {
          digit2Group.position.set(gx - 0.15, gy + 2.35, gz + 0.25);
          digit2Group.rotation.set(0.25, t * 4.5, -0.3);
        }

        // Dust puffs trail behind Grok when bolting away
        dustPuffs.forEach((dp, idx) => {
          const dt = t - (TIMINGS.stealTime + 0.08 + idx * 0.1);
          if (dt > 0 && dt < 0.55) {
            dp.visible = true;
            dp.position.set(p4CubeRestX + idx * 1.1, p4Station.y + 0.35 + dt * 1.3, gz);
            dp.scale.setScalar(1 - dt / 0.55);
          } else {
            dp.visible = false;
          }
        });
      }
    } else {
      grok.root.visible = false;
      digit2Group.visible = false;
      dustPuffs.forEach((dp) => (dp.visible = false));
    }

    // 7) Dynamic Camera Choreography (aim above hero so hero sits cleanly at lower-center y=780..1460px!)
    const hBase = _heroPos;
    // Target point offset UP by +2.55 so screen center sits above hero, keeping upper 40% clear for HUD cards!
    const tgtY = hBase.y + 2.58;
    const tgtX = hBase.x + 0.35;
    const tgtZ = hBase.z - 0.2;

    let camOffX = 1.9;
    let camOffY = 1.65;
    let camOffZ = 12.2;
    let fov = 38;

    if (t < TIMINGS.countdownStart) {
      // Smooth push-in & arc during Hook walk
      const hp = t / TIMINGS.countdownStart;
      camOffX = lerp(2.4, 1.5, hp);
      camOffY = lerp(1.75, 1.55, hp);
      camOffZ = lerp(12.6, 11.4, hp);
      fov = lerp(38.5, 36.5, hp);
    } else if (t < TIMINGS.countdownEnd) {
      // Wider framing on P4 + ChatGPT + right flank so Grok + brass stopwatch + stolen "2" stay 100% in frame!
      const cp = (t - TIMINGS.countdownStart) / 4.0;
      camOffX = lerp(1.6, 2.55, cp);
      camOffY = 1.6;
      camOffZ = lerp(11.8, 13.4, cp);
      fov = lerp(38.0, 40.5, cp);
      if (t >= TIMINGS.stealTime && t <= TIMINGS.stealTime + 0.3) {
        const kp = (t - TIMINGS.stealTime) / 0.3;
        const kick = Math.sin(kp * Math.PI * 6) * (1 - kp) * 0.24;
        camOffX += kick;
        camOffY += kick * 0.7;
      }
    } else if (t < TIMINGS.guardrailStart) {
      // Dynamic tracking glide following Antigravity uphill through Clues 1, 2, 3
      const rp = (t - TIMINGS.revealStart) / (TIMINGS.guardrailStart - TIMINGS.revealStart);
      camOffX = 2.0 + Math.sin(rp * Math.PI * 2) * 1.1;
      camOffY = lerp(1.65, 1.85, rp);
      camOffZ = lerp(11.8, 12.6, Math.sin(rp * Math.PI));
      fov = 37.5;
      if (t >= TIMINGS.revealStart && t <= TIMINGS.revealStart + 0.28) {
        const kp = (t - TIMINGS.revealStart) / 0.28;
        camOffY += Math.sin(kp * Math.PI * 5) * (1 - kp) * 0.22;
      }
    } else {
      // Heroic Guardrail & Victory climb crane shot toward P5 crest
      const gp = (t - TIMINGS.guardrailStart) / (TIMINGS.totalDuration - TIMINGS.guardrailStart);
      camOffX = lerp(2.1, 1.1, gp);
      camOffY = lerp(1.6, 2.05, gp);
      camOffZ = lerp(11.4, 13.0, gp);
      fov = lerp(36.5, 39.0, gp);
    }

    _camTarget.set(tgtX, tgtY, tgtZ);
    _camPos.set(tgtX + camOffX, tgtY + camOffY, tgtZ + camOffZ);
    camera.position.copy(_camPos);
    camera.fov = fov;
    camera.updateProjectionMatrix();
    camera.lookAt(_camTarget);

    // Keep shadow frustum centered cleanly around hero
    keyLight.position.set(hBase.x + 8, hBase.y + 13, hBase.z + 9);
    keyLight.target.position.set(hBase.x + 1, hBase.y + 1, hBase.z);
    keyLight.target.updateMatrixWorld();

    renderer.render(scene, camera);
  }

  return { renderAt };
}
