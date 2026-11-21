import React, { useEffect, useMemo } from 'react';
import { spring } from 'remotion';
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

export type MonitorScreenMode =
  | 'quota_low'
  | 'model_selector_1usd'
  | 'bot_flattery'
  | 'broken_web'
  | 'zoom_countdown'
  | 'hola_drain'
  | 'quota_lockout'
  | 'zoom_left';

export const DESK_TOP_Y = -0.83;

function drawRoundedRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number
) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

function drawMonitorArt(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  mode: MonitorScreenMode,
  frame: number,
  localFrame: number
) {
  ctx.clearRect(0, 0, w, h);

  // Base dark IDE / terminal background
  const bg = ctx.createLinearGradient(0, 0, 0, h);
  if (mode === 'quota_lockout') {
    bg.addColorStop(0, '#14060A');
    bg.addColorStop(1, '#070306');
  } else if (mode === 'zoom_left') {
    bg.addColorStop(0, '#0B0F17');
    bg.addColorStop(1, '#05070B');
  } else {
    bg.addColorStop(0, '#091122');
    bg.addColorStop(1, '#040812');
  }
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, w, h);

  // Subtle scanlines / ambient grid
  ctx.strokeStyle = 'rgba(148, 163, 184, 0.06)';
  ctx.lineWidth = 1;
  for (let gx = 0; gx < w; gx += 64) {
    ctx.beginPath();
    ctx.moveTo(gx, 0);
    ctx.lineTo(gx, h);
    ctx.stroke();
  }
  for (let gy = 0; gy < h; gy += 64) {
    ctx.beginPath();
    ctx.moveTo(0, gy);
    ctx.lineTo(w, gy);
    ctx.stroke();
  }

  // Top macOS-like window chrome bar
  ctx.fillStyle = 'rgba(15, 23, 42, 0.92)';
  ctx.fillRect(0, 0, w, 54);
  const dotColors = ['#EF4444', '#F59E0B', '#10B981'];
  dotColors.forEach((c, idx) => {
    ctx.fillStyle = c;
    ctx.beginPath();
    ctx.arc(36 + idx * 28, 27, 8, 0, Math.PI * 2);
    ctx.fill();
  });

  const pulse = Math.sin(frame * 0.25) * 0.5 + 0.5;
  ctx.textBaseline = 'middle';

  if (mode === 'quota_low') {
    ctx.fillStyle = '#94A3B8';
    ctx.font = 'bold 22px ui-monospace, Menlo, monospace';
    ctx.textAlign = 'right';
    ctx.fillText('VIBE STUDIO · ENTREGA FINAL', w - 44, 27);

    // Subtle code lines on left (behind Chispa silhouette)
    ctx.textAlign = 'left';
    const codeW = [300, 220, 340, 190];
    codeW.forEach((cw, i) => {
      ctx.fillStyle = i % 2 === 0 ? 'rgba(56, 189, 248, 0.24)' : 'rgba(148, 163, 184, 0.16)';
      drawRoundedRect(ctx, 48, 96 + i * 44, cw, 20, 6);
      ctx.fill();
    });

    // Right-aligned alerts on right 58% of monitor so Chispa NEVER occludes $20 MXN or RENTA: MAÑANA
    ctx.fillStyle = 'rgba(239, 68, 68, 0.28)';
    ctx.strokeStyle = '#EF4444';
    ctx.lineWidth = 4;
    drawRoundedRect(ctx, 410, 128, 566, 200, 20);
    ctx.fill();
    ctx.stroke();

    ctx.textAlign = 'right';
    ctx.fillStyle = '#FCA5A5';
    ctx.font = 'bold 28px ui-monospace, Menlo, monospace';
    ctx.fillText('CUOTA RESTANTE', 944, 178);
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 84px ui-monospace, Menlo, monospace';
    ctx.fillText('$20 MXN', 944, 266);

    ctx.fillStyle = 'rgba(245, 158, 11, 0.24)';
    ctx.strokeStyle = '#F59E0B';
    drawRoundedRect(ctx, 410, 366, 566, 200, 20);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#FDE68A';
    ctx.font = 'bold 28px ui-monospace, Menlo, monospace';
    ctx.fillText('VENCIMIENTO', 944, 416);
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 56px -apple-system, sans-serif';
    ctx.fillText('RENTA: MAÑANA', 944, 500);
    ctx.textAlign = 'left';
    return;
  }

  if (mode === 'model_selector_1usd') {
    ctx.fillStyle = '#94A3B8';
    ctx.font = 'bold 22px ui-monospace, Menlo, monospace';
    ctx.fillText('AGENT ROUTER · SELECCIONAR MODELO', 135, 27);

    // Dimmed PRO option
    ctx.fillStyle = 'rgba(30, 41, 59, 0.85)';
    ctx.strokeStyle = 'rgba(148, 163, 184, 0.35)';
    ctx.lineWidth = 2;
    drawRoundedRect(ctx, 64, 100, w - 128, 128, 20);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#64748B';
    ctx.font = '700 34px -apple-system, sans-serif';
    ctx.fillText('MODELO PRO · ARQUITECTO', 104, 150);
    ctx.font = '600 24px ui-monospace, Menlo, monospace';
    ctx.fillText('Alto consumo de cuota ($25+)', 104, 196);

    // Highlighted CHEAP $1 option
    const pop = Math.min(1, localFrame / 18);
    ctx.fillStyle = `rgba(245, 158, 11, ${0.18 + pulse * 0.1})`;
    ctx.strokeStyle = '#FBBF24';
    ctx.lineWidth = 5;
    drawRoundedRect(ctx, 64, 260, w - 128, 290, 22);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#FBBF24';
    ctx.font = '900 30px ui-monospace, Menlo, monospace';
    ctx.fillText('✓ SELECCIONADO', 104, 315);

    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 66px -apple-system, sans-serif';
    ctx.fillText('MODO $1 USD', 104, 405);

    ctx.fillStyle = '#FDE68A';
    ctx.font = '800 36px ui-monospace, Menlo, monospace';
    ctx.fillText('AHORRO EXTREMO · CERO REVISIÓN', 104, 488);

    // Pointer cursor clicking
    const cx = 790 - pop * 60;
    const cy = 480 - pop * 45;
    ctx.fillStyle = '#FFFFFF';
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + 38, cy + 28);
    ctx.lineTo(cx + 16, cy + 32);
    ctx.lineTo(cx + 26, cy + 56);
    ctx.lineTo(cx + 14, cy + 60);
    ctx.lineTo(cx + 4, cy + 36);
    ctx.lineTo(cx - 12, cy + 46);
    ctx.closePath();
    ctx.fill();
    return;
  }

  if (mode === 'bot_flattery') {
    ctx.fillStyle = '#34D399';
    ctx.font = 'bold 24px ui-monospace, Menlo, monospace';
    ctx.fillText('AGENTE MODO $1 · ACTIVO', 135, 27);

    ctx.fillStyle = 'rgba(16, 185, 129, 0.16)';
    ctx.strokeStyle = '#10B981';
    ctx.lineWidth = 4;
    drawRoundedRect(ctx, 56, 108, w - 112, 260, 24);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#6EE7B7';
    ctx.font = '800 32px -apple-system, sans-serif';
    ctx.fillText('AGENTE $1 RESPONDE:', 96, 168);

    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 54px -apple-system, sans-serif';
    ctx.fillText('"¡ERES UN GENIO!"', 96, 244);
    ctx.fillStyle = '#A7F3D0';
    ctx.font = '700 34px -apple-system, sans-serif';
    ctx.fillText('Compilando obra maestra en 5s...', 96, 314);

    // Progress bar fake 99%
    ctx.fillStyle = 'rgba(255,255,255,0.12)';
    drawRoundedRect(ctx, 56, 420, w - 112, 46, 23);
    ctx.fill();
    const progW = ((w - 112) * Math.min(99, 45 + localFrame * 0.6)) / 100;
    ctx.fillStyle = '#10B981';
    drawRoundedRect(ctx, 56, 420, progW, 46, 23);
    ctx.fill();

    ctx.fillStyle = '#34D399';
    ctx.font = '900 34px ui-monospace, Menlo, monospace';
    ctx.fillText('TODO PERFECTO · SIN TESTS · $1.00', 56, 526);
    return;
  }

  if (mode === 'broken_web') {
    // Diegetic critical banner INSIDE monitor screen: BUILD: 47 ERRORS
    ctx.fillStyle = '#DC2626';
    ctx.fillRect(0, 54, w, 98);
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 58px ui-monospace, Menlo, monospace';
    ctx.fillText('BUILD: 47 ERRORS', 46, 104);

    ctx.fillStyle = '#FEF08A';
    ctx.font = '800 28px ui-monospace, Menlo, monospace';
    ctx.fillText('CSS ROTO', w - 210, 104);

    // Hilarious broken webpage canvas below the red bar
    ctx.fillStyle = '#E2E8F0';
    ctx.fillRect(36, 174, w - 72, h - 208);

    // Crooked broken nav
    ctx.fillStyle = '#1E293B';
    ctx.fillRect(54, 194, w - 108, 66);
    ctx.fillStyle = '#94A3B8';
    ctx.font = 'bold 26px sans-serif';
    ctx.fillText('MENU [UNDEFINED]   NOSOTROS   [NULL]', 76, 228);

    // Price covered by giant yellow button
    ctx.fillStyle = '#0F172A';
    ctx.font = '900 54px sans-serif';
    ctx.fillText('PRECIO: $9,900', 80, 355);

    ctx.save();
    ctx.translate(420, 360);
    ctx.rotate(-0.08);
    ctx.fillStyle = '#FACC15';
    ctx.strokeStyle = '#DC2626';
    ctx.lineWidth = 6;
    drawRoundedRect(ctx, -230, -68, 460, 136, 22);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#111827';
    ctx.font = '900 52px sans-serif';
    ctx.fillText('COMPRAR', -135, 0);
    ctx.restore();

    // Jagged 404 error box + Lorem Ipsum
    ctx.fillStyle = '#991B1B';
    drawRoundedRect(ctx, 640, 290, 310, 260, 16);
    ctx.fill();
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 84px ui-monospace, Menlo, monospace';
    ctx.fillText('404', 696, 392);
    ctx.font = '700 26px ui-monospace, Menlo, monospace';
    ctx.fillText('NOT FOUND', 696, 472);

    ctx.fillStyle = '#475569';
    ctx.font = 'bold 30px Georgia, serif';
    ctx.fillText('Lorem ipsum dolor sit amet...', 74, 520);
    return;
  }

  if (mode === 'zoom_countdown') {
    // Pulsing urgent red top alert INSIDE monitor: ZOOM EN 02:00 MIN (right-aligned padding avoids Chispa overlap)
    ctx.fillStyle = pulse > 0.4 ? '#DC2626' : '#B91C1C';
    ctx.fillRect(0, 54, w, 146);
    ctx.textAlign = 'right';
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 70px ui-monospace, Menlo, monospace';
    ctx.fillText('ZOOM EN 02:00 MIN', w - 48, 128);

    // Urgent switching box to MODELO ULTRA PRO aligned clearly on right half
    ctx.fillStyle = 'rgba(245, 158, 11, 0.22)';
    ctx.strokeStyle = '#FBBF24';
    ctx.lineWidth = 5;
    drawRoundedRect(ctx, 210, 236, w - 256, 210, 24);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#FDE68A';
    ctx.font = '800 28px ui-monospace, Menlo, monospace';
    ctx.fillText('CAMBIO EMERGENCIA:', w - 78, 292);
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 58px -apple-system, sans-serif';
    ctx.fillText('MODELO ULTRA PRO', w - 78, 376);

    ctx.fillStyle = '#FCA5A5';
    ctx.font = '800 30px ui-monospace, Menlo, monospace';
    ctx.fillText('CONSUMO TOKENS x40 · SIN TOPE', w - 48, 518);
    ctx.textAlign = 'left';
    return;
  }

  if (mode === 'hola_drain') {
    ctx.fillStyle = '#94A3B8';
    ctx.font = 'bold 22px ui-monospace, Menlo, monospace';
    ctx.fillText('MODELO ULTRA PRO · CHAT ACTIVO', 135, 27);

    // User sent only "hola"
    ctx.fillStyle = '#1E3A8A';
    ctx.strokeStyle = '#60A5FA';
    ctx.lineWidth = 3;
    drawRoundedRect(ctx, w - 420, 104, 360, 118, 24);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#93C5FD';
    ctx.font = '700 24px ui-monospace, Menlo, monospace';
    ctx.fillText('TÚ ENVIASTE:', w - 385, 142);
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 54px ui-monospace, Menlo, monospace';
    ctx.fillText('> hola', w - 385, 190);

    // Draining quota meter live from 100% -> 0%
    const drainPct = Math.max(0, 1 - localFrame / 95);
    const barW = w - 112;
    ctx.fillStyle = '#F8FAFC';
    ctx.font = '900 38px ui-monospace, Menlo, monospace';
    ctx.fillText(
      `CUOTA RESTANTE: ${Math.round(drainPct * 100)}%`,
      56,
      320
    );

    ctx.fillStyle = 'rgba(255,255,255,0.12)';
    drawRoundedRect(ctx, 56, 372, barW, 84, 20);
    ctx.fill();

    if (drainPct > 0.01) {
      ctx.fillStyle = drainPct < 0.35 ? '#EF4444' : '#F59E0B';
      drawRoundedRect(ctx, 56, 372, Math.max(24, barW * drainPct), 84, 20);
      ctx.fill();
    }

    ctx.fillStyle = drainPct <= 0.02 ? '#EF4444' : '#FCA5A5';
    ctx.font = '900 44px ui-monospace, Menlo, monospace';
    ctx.fillText(
      drainPct <= 0.02 ? 'SIN CRÉDITOS · BLOQUEADO' : 'REENVIANDO TODO EL CONTEXTO...',
      56,
      528
    );
    return;
  }

  if (mode === 'quota_lockout') {
    // Stark full-screen red/white lockout INSIDE monitor
    ctx.strokeStyle = '#EF4444';
    ctx.lineWidth = 8;
    drawRoundedRect(ctx, 28, 76, w - 56, h - 104, 24);
    ctx.stroke();

    // Padlock icon top center
    const lx = w / 2;
    ctx.strokeStyle = '#EF4444';
    ctx.lineWidth = 14;
    ctx.beginPath();
    ctx.arc(lx, 175, 42, Math.PI, 0);
    ctx.stroke();
    ctx.fillStyle = '#EF4444';
    drawRoundedRect(ctx, lx - 62, 178, 124, 92, 16);
    ctx.fill();

    ctx.textAlign = 'center';
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 108px ui-monospace, Menlo, monospace';
    ctx.fillText('QUOTA 0%', lx, 368);

    ctx.fillStyle = '#DC2626';
    drawRoundedRect(ctx, 96, 446, w - 192, 108, 18);
    ctx.fill();
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 54px ui-monospace, Menlo, monospace';
    ctx.fillText('REGRESA EN 5 DÍAS', lx, 502);
    ctx.textAlign = 'left';
    return;
  }

  // zoom_left
  ctx.fillStyle = '#94A3B8';
  ctx.font = 'bold 22px ui-monospace, Menlo, monospace';
  ctx.fillText('ZOOM · SALA DE ENTREGA · 02:14 AM', 135, 27);

  // Empty dark participant boxes
  [84, 536].forEach((bx) => {
    ctx.fillStyle = '#111827';
    ctx.strokeStyle = '#1F2937';
    ctx.lineWidth = 3;
    drawRoundedRect(ctx, bx, 86, 404, 210, 16);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#374151';
    ctx.beginPath();
    ctx.arc(bx + 202, 186, 44, 0, Math.PI * 2);
    ctx.fill();
  });

  // High-contrast crisp system modal INSIDE monitor
  ctx.fillStyle = '#18181B';
  ctx.strokeStyle = '#F87171';
  ctx.lineWidth = 5;
  drawRoundedRect(ctx, 64, 336, w - 128, 224, 22);
  ctx.fill();
  ctx.stroke();

  ctx.textAlign = 'center';
  ctx.fillStyle = '#F87171';
  ctx.font = '900 28px ui-monospace, Menlo, monospace';
  ctx.fillText('LLAMADA FINALIZADA', w / 2, 386);
  ctx.fillStyle = '#FFFFFF';
  ctx.font = '900 46px -apple-system, sans-serif';
  ctx.fillText('El cliente ha abandonado', w / 2, 456);
  ctx.fillText('la reunión', w / 2, 512);
  ctx.textAlign = 'left';
}

export const DiegeticMonitor3D: React.FC<{
  frame: number;
  localFrame: number;
  mode: MonitorScreenMode;
  position?: [number, number, number];
  rotationY?: number;
  scale?: number;
}> = ({
  frame,
  localFrame,
  mode,
  position = [0.64, DESK_TOP_Y, -0.22],
  rotationY = -0.38,
  scale = 1,
}) => {
  const { canvas, ctx, texture } = useMemo(() => {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 640;
    const context = c.getContext('2d')!;
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.minFilter = THREE.LinearFilter;
    tex.magFilter = THREE.LinearFilter;
    return { canvas: c, ctx: context, texture: tex };
  }, []);

  useEffect(() => {
    return () => {
      texture.dispose();
    };
  }, [texture]);

  // Synchronous draw during Remotion frame render so every still & frame is deterministic
  drawMonitorArt(ctx, canvas.width, canvas.height, mode, frame, localFrame);
  texture.needsUpdate = true;

  const glowColor =
    mode === 'broken_web' ||
    mode === 'zoom_countdown' ||
    mode === 'quota_lockout' ||
    mode === 'hola_drain'
      ? '#EF4444'
      : mode === 'bot_flattery'
        ? '#10B981'
        : mode === 'model_selector_1usd'
          ? '#F59E0B'
          : '#38BDF8';

  const screenGeo = useMemo(
    () => new RoundedBoxGeometry(2.14, 1.38, 0.08, 4, 0.04),
    []
  );

  return (
    <group position={position} rotation={[0, rotationY, 0]} scale={scale}>
      {/* Sleek dark monitor riser + stand base on DESK_TOP_Y so screen clears behind Chispa */}
      <mesh position={[0, 0.07, -0.04]} receiveShadow castShadow>
        <boxGeometry args={[1.38, 0.14, 0.62]} />
        <meshStandardMaterial color="#0F172A" metalness={0.55} roughness={0.4} />
      </mesh>
      <mesh position={[0, 0.16, -0.05]} receiveShadow>
        <boxGeometry args={[0.82, 0.04, 0.48]} />
        <meshStandardMaterial color="#1E293B" metalness={0.75} roughness={0.3} />
      </mesh>
      <mesh position={[0, 0.48, -0.14]}>
        <boxGeometry args={[0.15, 0.64, 0.12]} />
        <meshStandardMaterial color="#334155" metalness={0.75} roughness={0.32} />
      </mesh>

      {/* Main Display Bezel + Luminous Screen Plane */}
      <group position={[0, 1.12, 0]} rotation={[-0.03, 0, 0]}>
        <mesh geometry={screenGeo} castShadow>
          <meshStandardMaterial
            color="#0F172A"
            metalness={0.55}
            roughness={0.28}
            emissive={glowColor}
            emissiveIntensity={0.22}
          />
        </mesh>

        {/* Upright Front Screen Texture (toneMapped=false preserves crisp UI colors) */}
        <mesh position={[0, 0, 0.044]}>
          <planeGeometry args={[2.0, 1.25]} />
          <meshBasicMaterial map={texture} toneMapped={false} />
        </mesh>

        {/* Diegetic monitor light illuminating Chispa & desk */}
        <pointLight
          position={[-0.1, 0.05, 1.35]}
          intensity={mode === 'zoom_left' ? 1.5 : 3.2}
          distance={5.5}
          color={glowColor}
        />
      </group>

      {/* Compact Desk Mechanical Keyboard + Mouse in front of monitor */}
      <mesh position={[-0.25, 0.03, 0.56]} rotation={[0, 0.08, 0]} castShadow>
        <boxGeometry args={[1.06, 0.045, 0.36]} />
        <meshStandardMaterial color="#1E293B" roughness={0.55} metalness={0.3} />
      </mesh>
      <mesh position={[-0.25, 0.056, 0.56]} rotation={[0, 0.08, 0]}>
        <boxGeometry args={[0.96, 0.012, 0.28]} />
        <meshStandardMaterial
          color="#38BDF8"
          emissive={glowColor}
          emissiveIntensity={0.85}
        />
      </mesh>
      <mesh position={[0.45, 0.03, 0.58]}>
        <boxGeometry args={[0.14, 0.05, 0.22]} />
        <meshStandardMaterial color="#334155" roughness={0.4} metalness={0.3} />
      </mesh>
    </group>
  );
};

export const CheapBot1Usd3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
  position?: [number, number, number];
  rotationY?: number;
  scale?: number;
}> = ({
  frame,
  localFrame,
  fps,
  position = [0.68, 0.35, 0.58],
  rotationY = -0.35,
  scale = 0.92,
}) => {
  const t = frame / fps;
  const pop = spring({
    frame: Math.max(0, localFrame),
    fps,
    config: { damping: 11, stiffness: 210 },
  });

  const { badgeCanvas, badgeTex } = useMemo(() => {
    const c = document.createElement('canvas');
    c.width = 256;
    c.height = 160;
    const ctx = c.getContext('2d')!;
    ctx.fillStyle = '#F59E0B';
    ctx.fillRect(0, 0, 256, 160);
    ctx.strokeStyle = '#78350F';
    ctx.lineWidth = 14;
    ctx.strokeRect(8, 8, 240, 144);
    ctx.fillStyle = '#111827';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.font = '900 104px ui-monospace, Menlo, monospace';
    ctx.fillText('$1', 128, 84);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.needsUpdate = true;
    return { badgeCanvas: c, badgeTex: tex };
  }, []);

  useEffect(() => {
    return () => {
      badgeTex.dispose();
    };
  }, [badgeTex]);

  void badgeCanvas;

  const geos = useMemo(
    () => ({
      head: new RoundedBoxGeometry(1.06, 0.78, 0.72, 4, 0.16),
      body: new RoundedBoxGeometry(0.84, 0.54, 0.58, 4, 0.12),
    }),
    []
  );

  const hoverY = Math.sin(t * 4.8) * 0.06;
  const tilt = Math.sin(t * 3.1) * 0.08;

  return (
    <group
      position={[position[0], position[1] + hoverY, position[2]]}
      rotation={[0, rotationY, tilt]}
      scale={scale * Math.max(0.001, pop)}
    >
      {/* Crooked cheap antenna */}
      <group position={[0.25, 0.45, 0]} rotation={[0, 0, -0.35]}>
        <mesh position={[0, 0.14, 0]}>
          <cylinderGeometry args={[0.025, 0.03, 0.28, 10]} />
          <meshStandardMaterial color="#64748B" metalness={0.7} />
        </mesh>
        <mesh position={[0, 0.3, 0]}>
          <sphereGeometry args={[0.08, 14, 14]} />
          <meshStandardMaterial
            color="#F59E0B"
            emissive="#F59E0B"
            emissiveIntensity={2.0}
          />
        </mesh>
      </group>

      {/* Matte charcoal head */}
      <mesh position={[0, 0.12, 0]} geometry={geos.head} castShadow>
        <meshStandardMaterial color="#1F2937" metalness={0.45} roughness={0.4} />
      </mesh>
      {/* Screen face */}
      <mesh position={[0, 0.12, 0.37]}>
        <boxGeometry args={[0.84, 0.5, 0.03]} />
        <meshStandardMaterial color="#090D16" roughness={0.2} />
      </mesh>
      {/* Lopsided cheeky amber/red eyes */}
      <mesh position={[-0.2, 0.19, 0.395]} scale={[1.1, 0.85, 1]}>
        <sphereGeometry args={[0.085, 14, 14]} />
        <meshBasicMaterial color="#FBBF24" />
      </mesh>
      <mesh position={[0.21, 0.16, 0.395]} scale={[0.9, 1.15, 1]}>
        <sphereGeometry args={[0.075, 14, 14]} />
        <meshBasicMaterial color="#F87171" />
      </mesh>
      {/* Smirk mouth */}
      <mesh position={[0.03, -0.02, 0.395]} rotation={[0, 0, 0.14]}>
        <boxGeometry args={[0.28, 0.04, 0.02]} />
        <meshBasicMaterial color="#FBBF24" />
      </mesh>

      {/* Body with crisp $1 badge */}
      <mesh position={[0, -0.45, 0]} geometry={geos.body} castShadow>
        <meshStandardMaterial color="#374151" metalness={0.4} roughness={0.45} />
      </mesh>
      <mesh position={[0, -0.45, 0.298]}>
        <planeGeometry args={[0.48, 0.3]} />
        <meshBasicMaterial map={badgeTex} toneMapped={false} />
      </mesh>

      <pointLight position={[0, 0.2, 1.0]} intensity={1.8} distance={3.5} color="#F59E0B" />
    </group>
  );
};

export const DarkStudioRoom3D: React.FC<{
  frame: number;
  coldLockout?: boolean;
}> = ({ frame, coldLockout = false }) => {
  // Neon bokeh sign texture: captoora.studio
  const { signTex } = useMemo(() => {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 128;
    const ctx = c.getContext('2d')!;
    ctx.clearRect(0, 0, c.width, c.height);

    ctx.shadowColor = '#38BDF8';
    ctx.shadowBlur = 24;
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.45)';
    ctx.lineWidth = 3;
    drawRoundedRect(ctx, 18, 18, 476, 92, 22);
    ctx.stroke();

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = 'rgba(125, 211, 252, 0.72)';
    ctx.font = '700 44px ui-monospace, Menlo, monospace';
    ctx.fillText('captoora.studio', 256, 66);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.needsUpdate = true;
    return { signTex: tex };
  }, []);

  useEffect(() => {
    return () => {
      signTex.dispose();
    };
  }, [signTex]);

  // Deterministic 3D falling rain streaks outside the midnight window
  const rainDrops = useMemo(() => {
    const arr: { x: number; speed: number; phase: number; z: number; len: number }[] = [];
    for (let i = 0; i < 64; i++) {
      const s1 = Math.sin(i * 19.37) * 43758.5453;
      const s2 = Math.sin(i * 41.13) * 43758.5453;
      const s3 = Math.sin(i * 73.91) * 43758.5453;
      arr.push({
        x: ((s1 - Math.floor(s1)) - 0.5) * 4.4,
        speed: 0.08 + (s2 - Math.floor(s2)) * 0.07,
        phase: s3 - Math.floor(s3),
        z: -4.15 - (i % 3) * 0.12,
        len: 0.34 + (i % 4) * 0.1,
      });
    }
    return arr;
  }, []);

  const dust = useMemo(() => {
    const arr: { x: number; y: number; z: number; size: number; cool: boolean }[] = [];
    for (let i = 0; i < 32; i++) {
      const s1 = Math.sin(i * 11.7) * 43758.5453;
      const s2 = Math.sin(i * 29.3) * 43758.5453;
      const s3 = Math.sin(i * 47.1) * 43758.5453;
      arr.push({
        x: ((s1 - Math.floor(s1)) - 0.5) * 5.8,
        y: (s2 - Math.floor(s2)) * 3.4 - 0.7,
        z: -2.2 + (s3 - Math.floor(s3)) * 2.5,
        size: 0.014 + (i % 3) * 0.008,
        cool: i % 2 === 0,
      });
    }
    return arr;
  }, []);

  const deskGeo = useMemo(
    () => new RoundedBoxGeometry(6.8, 0.12, 3.0, 3, 0.03),
    []
  );

  return (
    <group>
      {/* Room floor */}
      <mesh position={[0, -1.75, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[28, 22]} />
        <meshStandardMaterial color="#050811" roughness={0.85} />
      </mesh>

      {/* Dark midnight back wall (positioned behind RainWindow depth plane) */}
      <mesh position={[0, 1.2, -4.25]} receiveShadow>
        <planeGeometry args={[20, 12]} />
        <meshStandardMaterial
          color={coldLockout ? '#090D16' : '#0B1224'}
          roughness={0.88}
        />
      </mesh>

      {/* Desk surface whose top face rests at DESK_TOP_Y (-0.83) */}
      <mesh position={[0, DESK_TOP_Y - 0.06, 0.0]} geometry={deskGeo} receiveShadow castShadow>
        <meshStandardMaterial color="#131926" roughness={0.55} metalness={0.18} />
      </mesh>
      {/* Subtle desk front edge highlight */}
      <mesh position={[0, DESK_TOP_Y - 0.01, 1.48]}>
        <boxGeometry args={[6.78, 0.018, 0.04]} />
        <meshBasicMaterial color="#1E293B" />
      </mesh>

      {/* Bokeh neon sign on left-back wall visible beside/above Chispa */}
      <mesh position={[-0.75, 1.58, -3.25]} rotation={[0, 0.08, 0]}>
        <planeGeometry args={[1.75, 0.44]} />
        <meshBasicMaterial
          map={signTex}
          transparent
          opacity={coldLockout ? 0.42 : 0.88}
          toneMapped={false}
        />
      </mesh>

      {/* Rain Window centered behind studio desk with clearly visible blue night storm + mullions */}
      <group position={[0.35, 1.05, -3.75]}>
        {/* Outer window frame with subtle moonlight edge */}
        <mesh position={[0, 0, -0.02]}>
          <boxGeometry args={[5.5, 3.7, 0.08]} />
          <meshBasicMaterial color="#1E293B" />
        </mesh>
        {/* Night storm sky glow inside window */}
        <mesh position={[0, 0, 0.01]}>
          <planeGeometry args={[5.1, 3.3]} />
          <meshBasicMaterial color={coldLockout ? '#122142' : '#1E3A78'} />
        </mesh>
        {/* Soft distant city bokeh lights */}
        {[
          [-1.7, -0.45, '#38BDF8'],
          [-0.95, -0.75, '#F59E0B'],
          [0.95, -0.55, '#60A5FA'],
          [1.85, -0.35, '#38BDF8'],
          [0.1, -0.88, '#FBBF24'],
          [-1.3, 0.35, '#60A5FA'],
        ].map(([bx, by, col], idx) => (
          <mesh key={idx} position={[bx as number, by as number, 0.03]}>
            <circleGeometry args={[0.16, 16]} />
            <meshBasicMaterial color={col as string} transparent opacity={0.55} />
          </mesh>
        ))}

        {/* Falling slanted 3D rain streaks (fine cinematic threads outside glass) */}
        {rainDrops.map((d, i) => {
          const prog = (frame * d.speed * 0.35 + d.phase) % 1;
          const ry = 1.55 - prog * 3.1;
          return (
            <mesh
              key={i}
              position={[d.x - prog * 0.25, ry, 0.06]}
              rotation={[0, 0, -0.14]}
            >
              <boxGeometry args={[0.015, d.len * 1.15, 0.008]} />
              <meshBasicMaterial
                color="#BAE6FD"
                transparent
                opacity={0.44}
              />
            </mesh>
          );
        })}

        {/* Window Mullions (crossbars) */}
        <mesh position={[0, 0, 0.1]}>
          <boxGeometry args={[0.12, 3.35, 0.05]} />
          <meshBasicMaterial color="#090F1E" />
        </mesh>
        <mesh position={[0, 0.15, 0.1]}>
          <boxGeometry args={[5.15, 0.12, 0.05]} />
          <meshBasicMaterial color="#090F1E" />
        </mesh>
      </group>

      {/* Atmospheric floating dust particles */}
      <group position={[0, Math.sin(frame * 0.02) * 0.08, 0]}>
        {dust.map((p, idx) => (
          <mesh key={idx} position={[p.x, p.y, p.z]}>
            <sphereGeometry args={[p.size, 8, 8]} />
            <meshBasicMaterial
              color={p.cool ? '#7DD3FC' : '#FDE68A'}
              transparent
              opacity={coldLockout ? 0.18 : 0.38}
            />
          </mesh>
        ))}
      </group>
    </group>
  );
};
