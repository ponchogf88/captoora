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
  | 'zoom_left'
  | 'console_cursor'
  | 'flashback_montage'
  | 'context_94'
  | 'hola_prompt'
  | 'quota_renew_red'
  | 'new_chat_button'
  | 'empty_chat_0'
  | 'welcome_bubble'
  | 'tear_resigned';

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
  return;
}

function drawMonitorArtMad08(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  mode: MonitorScreenMode,
  localFrame: number
) {
  if (mode === 'console_cursor') {
    ctx.textAlign = 'left';
    ctx.fillStyle = '#64748B';
    ctx.font = 'bold 22px ui-monospace, Menlo, monospace';
    ctx.fillText('TERMINAL SESSION · VIBE AGENT', 44, 27);

    ctx.fillStyle = '#38BDF8';
    ctx.font = 'bold 30px ui-monospace, Menlo, monospace';
    ctx.fillText('> anthropic_session.status = ACTIVE', 56, 140);
    ctx.fillStyle = '#94A3B8';
    ctx.font = '26px ui-monospace, Menlo, monospace';
    ctx.fillText('> current_context_tokens: 284,192 / 300,000', 56, 210);
    ctx.fillText('> token_burn_rate: 14,200 tok/prompt', 56, 270);
    ctx.fillStyle = '#EF4444';
    ctx.font = 'bold 28px ui-monospace, Menlo, monospace';
    ctx.fillText('⚠ AVISO: LÍMITE DE CUOTA A 5 DÍAS DE RENOVAR', 56, 350);

    ctx.fillStyle = '#00F5D4';
    ctx.font = 'bold 36px ui-monospace, Menlo, monospace';
    ctx.fillText('> user: "hola" ', 56, 440);
    if (Math.floor(localFrame / 8) % 2 === 0) {
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(360, 412, 18, 36);
    }
    return;
  }

  if (mode === 'flashback_montage') {
    ctx.textAlign = 'left';
    ctx.fillStyle = '#F59E0B';
    ctx.font = 'bold 22px ui-monospace, Menlo, monospace';
    ctx.fillText('HISTORIAL RECIENTE · PROYECTOS COMPARTIDOS', 44, 27);

    const memories = [
      { tag: 'EP. 01 GTA 6 3D', sub: '3 episodios renderizados', col: '#00F5D4' },
      { tag: '37 CASTING PICS', sub: 'Colección de personajes', col: '#A855F7' },
      { tag: 'TABLERO 14 SLOTS', sub: 'Arquitectura Drag & Drop', col: '#38BDF8' }
    ];

    memories.forEach((mem, i) => {
      const cy = 100 + i * 155;
      ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
      ctx.strokeStyle = mem.col;
      ctx.lineWidth = 3;
      drawRoundedRect(ctx, 56, cy, w - 112, 130, 16);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = mem.col;
      ctx.font = '900 32px -apple-system, sans-serif';
      ctx.fillText(mem.tag, 92, cy + 50);

      ctx.fillStyle = '#E2E8F0';
      ctx.font = '500 24px ui-monospace, Menlo, monospace';
      ctx.fillText(mem.sub, 92, cy + 92);

      ctx.fillStyle = mem.col;
      ctx.beginPath();
      ctx.arc(w - 110, cy + 65, 16, 0, Math.PI * 2);
      ctx.fill();
    });
    return;
  }

  if (mode === 'context_94') {
    ctx.textAlign = 'left';
    ctx.fillStyle = '#EF4444';
    ctx.font = 'bold 22px ui-monospace, Menlo, monospace';
    ctx.fillText('ALERTA DE SISTEMA · CONTEXTO CRÍTICO', 44, 27);

    ctx.fillStyle = '#18181B';
    ctx.strokeStyle = '#EF4444';
    ctx.lineWidth = 5;
    drawRoundedRect(ctx, 56, 110, w - 112, 450, 24);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#EF4444';
    ctx.font = '900 36px ui-monospace, Menlo, monospace';
    ctx.fillText('⚠ CONTEXTO AGOTADO AL 94%', 96, 180);

    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 76px ui-monospace, Menlo, monospace';
    ctx.fillText('284,000 TOKENS', 96, 280);

    ctx.fillStyle = 'rgba(255, 255, 255, 0.12)';
    drawRoundedRect(ctx, 96, 330, w - 192, 34, 12);
    ctx.fill();

    const barW = (w - 192) * 0.94;
    const barGrad = ctx.createLinearGradient(96, 0, 96 + barW, 0);
    barGrad.addColorStop(0, '#F59E0B');
    barGrad.addColorStop(1, '#EF4444');
    ctx.fillStyle = barGrad;
    drawRoundedRect(ctx, 96, 330, barW, 34, 12);
    ctx.fill();

    ctx.fillStyle = '#FCA5A5';
    ctx.font = 'bold 28px -apple-system, sans-serif';
    ctx.fillText('Acción requerida: Abrir conversación nueva o compactar.', 96, 430);

    ctx.fillStyle = '#38BDF8';
    ctx.font = 'bold 32px ui-monospace, Menlo, monospace';
    ctx.fillText('Comando sugerido: /compact', 96, 490);
    return;
  }

  if (mode === 'hola_prompt') {
    ctx.textAlign = 'left';
    ctx.fillStyle = '#38BDF8';
    ctx.font = 'bold 22px ui-monospace, Menlo, monospace';
    ctx.fillText('CHAT DE IA · ENTRADA DE MENSAJE', 44, 27);

    ctx.fillStyle = 'rgba(148, 163, 184, 0.18)';
    drawRoundedRect(ctx, 56, 100, 520, 48, 12);
    ctx.fill();
    ctx.fillStyle = 'rgba(56, 189, 248, 0.18)';
    drawRoundedRect(ctx, 240, 170, 520, 60, 12);
    ctx.fill();

    ctx.fillStyle = 'rgba(239, 68, 68, 0.22)';
    ctx.strokeStyle = '#EF4444';
    ctx.lineWidth = 3;
    drawRoundedRect(ctx, 56, 270, w - 112, 140, 18);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#FCA5A5';
    ctx.font = 'bold 26px ui-monospace, Menlo, monospace';
    ctx.fillText('COSTO POR MENSAJE ACTUAL', 90, 316);

    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 48px ui-monospace, Menlo, monospace';
    ctx.fillText('$0.45 USD (284k tokens)', 90, 375);

    ctx.fillStyle = '#0F172A';
    ctx.strokeStyle = '#38BDF8';
    ctx.lineWidth = 3;
    drawRoundedRect(ctx, 56, 450, w - 112, 90, 18);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#F8FAFC';
    ctx.font = '900 42px ui-monospace, Menlo, monospace';
    ctx.fillText('H - O - L - A', 90, 506);

    if (Math.floor(localFrame / 6) % 2 === 0) {
      ctx.fillStyle = '#38BDF8';
      ctx.fillRect(380, 474, 16, 42);
    }
    return;
  }

  if (mode === 'quota_renew_red') {
    ctx.fillStyle = '#26060D';
    ctx.strokeStyle = '#EF4444';
    ctx.lineWidth = 6;
    drawRoundedRect(ctx, 48, 80, w - 96, 490, 24);
    ctx.fill();
    ctx.stroke();

    ctx.textAlign = 'center';
    ctx.fillStyle = '#F87171';
    ctx.font = '900 36px ui-monospace, Menlo, monospace';
    ctx.fillText('ALERTA ROJA · CUOTA EXCEDIDA', w / 2, 150);

    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 72px -apple-system, sans-serif';
    ctx.fillText('5 DÍAS PARA RENOVAR', w / 2, 260);

    ctx.fillStyle = '#FCA5A5';
    ctx.font = 'bold 36px ui-monospace, Menlo, monospace';
    ctx.fillText('SALDO AGOTADO: $0.00 USD', w / 2, 350);

    ctx.fillStyle = 'rgba(239, 68, 68, 0.35)';
    drawRoundedRect(ctx, 120, 410, w - 240, 100, 18);
    ctx.fill();

    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 36px -apple-system, sans-serif';
    ctx.fillText('NO HAY MÁS PROMPTS DISPONIBLES', w / 2, 472);
    ctx.textAlign = 'left';
    return;
  }

  if (mode === 'new_chat_button') {
    ctx.textAlign = 'center';
    ctx.fillStyle = '#94A3B8';
    ctx.font = 'bold 24px ui-monospace, Menlo, monospace';
    ctx.fillText('CAMBIO DE SESIÓN · CERO TOKENS', w / 2, 140);

    const btnPulse = Math.sin(localFrame * 0.15) * 0.1 + 0.9;
    ctx.fillStyle = '#0284C7';
    ctx.strokeStyle = '#38BDF8';
    ctx.lineWidth = 5;
    ctx.shadowColor = '#38BDF8';
    ctx.shadowBlur = 35 * btnPulse;
    drawRoundedRect(ctx, 180, 210, w - 360, 160, 30);
    ctx.fill();
    ctx.stroke();
    ctx.shadowBlur = 0;

    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 56px -apple-system, sans-serif';
    ctx.fillText('+ New Conversation', w / 2, 295);

    ctx.fillStyle = '#7DD3FC';
    ctx.font = 'bold 26px ui-monospace, Menlo, monospace';
    ctx.fillText('Inicia sesión fresca a 0 tokens', w / 2, 430);

    const curX = 180 + (w - 360) * 0.65;
    const curY = 210 + 95;
    ctx.fillStyle = '#FFFFFF';
    ctx.beginPath();
    ctx.moveTo(curX, curY);
    ctx.lineTo(curX + 24, curY + 24);
    ctx.lineTo(curX + 10, curY + 24);
    ctx.lineTo(curX + 16, curY + 40);
    ctx.lineTo(curX + 8, curY + 42);
    ctx.lineTo(curX + 2, curY + 27);
    ctx.lineTo(curX - 6, curY + 34);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#0F172A';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.textAlign = 'left';
    return;
  }

  if (mode === 'empty_chat_0') {
    ctx.fillStyle = '#0B1120';
    ctx.fillRect(0, 54, w, h - 54);

    ctx.textAlign = 'left';
    ctx.fillStyle = '#10B981';
    ctx.font = '900 24px ui-monospace, Menlo, monospace';
    ctx.fillText('NUEVA CONVERSACIÓN · 0 TOKENS (MEMORIA LIMPIA)', 56, 120);

    ctx.fillStyle = '#475569';
    ctx.font = '500 28px -apple-system, sans-serif';
    ctx.fillText('¿Cómo puedo ayudarte hoy?', 56, 180);

    ctx.fillStyle = '#1E293B';
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 2;
    drawRoundedRect(ctx, 56, 440, w - 112, 100, 20);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#F8FAFC';
    ctx.font = '900 42px ui-monospace, Menlo, monospace';
    ctx.fillText('H o l a . . .', 96, 502);

    if (Math.floor(localFrame / 6) % 2 === 0) {
      ctx.fillStyle = '#10B981';
      ctx.fillRect(360, 470, 16, 42);
    }
    return;
  }

  if (mode === 'welcome_bubble') {
    ctx.fillStyle = '#0B1120';
    ctx.fillRect(0, 54, w, h - 54);

    ctx.textAlign = 'left';
    ctx.fillStyle = '#10B981';
    ctx.font = '900 22px ui-monospace, Menlo, monospace';
    ctx.fillText('SESIÓN 1 · ASISTENTE DE IA', 56, 110);

    ctx.fillStyle = 'rgba(16, 185, 129, 0.16)';
    ctx.strokeStyle = '#10B981';
    ctx.lineWidth = 4;
    drawRoundedRect(ctx, 56, 160, w - 112, 280, 24);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#34D399';
    ctx.font = '900 36px -apple-system, sans-serif';
    ctx.fillText('🤖 Asistente de IA (Desconocido)', 96, 220);

    ctx.fillStyle = '#FFFFFF';
    ctx.font = '900 42px -apple-system, sans-serif';
    ctx.fillText('«¡Hola! Soy tu asistente de IA,', 96, 290);
    ctx.fillText('mucho gusto.', 96, 350);
    ctx.fillText('¿En qué te puedo ayudar hoy?»', 96, 410);

    ctx.fillStyle = '#94A3B8';
    ctx.font = 'bold 24px ui-monospace, Menlo, monospace';
    ctx.fillText('Historial previo: Desconocido (0 conversaciones)', 96, 490);
    return;
  }

  if (mode === 'tear_resigned') {
    ctx.fillStyle = '#0B1120';
    ctx.fillRect(0, 54, w, h - 54);

    ctx.textAlign = 'left';
    ctx.fillStyle = '#38BDF8';
    ctx.font = '900 24px ui-monospace, Menlo, monospace';
    ctx.fillText('SESIÓN NUEVA · IMPORTAR MAPA DEL PROYECTO', 56, 110);

    ctx.fillStyle = '#1E293B';
    ctx.strokeStyle = '#38BDF8';
    ctx.lineWidth = 3;
    drawRoundedRect(ctx, 56, 160, w - 112, 160, 20);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#F8FAFC';
    ctx.font = '900 36px -apple-system, sans-serif';
    ctx.fillText('Chispa: «Lee mi mapa del proyecto, por favor…»', 96, 225);
    ctx.fillStyle = '#34D399';
    ctx.font = '900 34px -apple-system, sans-serif';
    ctx.fillText('IA: «¡Claro! Déjame revisar.»', 96, 280);

    ctx.fillStyle = 'rgba(15, 23, 42, 0.7)';
    drawRoundedRect(ctx, 56, 360, w - 112, 190, 16);
    ctx.fill();
    ctx.fillStyle = '#64748B';
    ctx.font = '22px ui-monospace, Menlo, monospace';
    ctx.fillText('$ cat MAPA_REPOSITORIO.md', 86, 410);
    ctx.fillText('> Leyendo contexto estructurado sin quemar tokens...', 86, 460);

    // Large glass tear droplet sliding down the monitor screen
    const tearY = 120 + (Math.min(localFrame, 90) / 90) * 360;
    const tearX = w * 0.76;

    ctx.strokeStyle = 'rgba(56, 189, 248, 0.28)';
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(tearX, 120);
    ctx.lineTo(tearX, tearY);
    ctx.stroke();

    const tearGrad = ctx.createRadialGradient(tearX - 4, tearY - 4, 2, tearX, tearY, 18);
    tearGrad.addColorStop(0, '#FFFFFF');
    tearGrad.addColorStop(0.35, '#7DD3FC');
    tearGrad.addColorStop(1, 'rgba(14, 165, 233, 0.85)');
    ctx.fillStyle = tearGrad;
    ctx.beginPath();
    ctx.arc(tearX, tearY, 16, 0, Math.PI * 2);
    ctx.fill();
    return;
  }
}

export const DiegeticMonitor3D: React.FC<{
  frame: number;
  localFrame: number;
  mode: MonitorScreenMode;
  position?: [number, number, number];
  rotationY?: number;
  scale?: number;
  imageSrc?: string;
  showTear?: boolean;
}> = ({
  frame,
  localFrame,
  mode,
  position = [0.64, DESK_TOP_Y, -0.22],
  rotationY = -0.38,
  scale = 1,
  imageSrc,
  showTear = false,
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
  const isMad08 =
    mode === 'console_cursor' ||
    mode === 'flashback_montage' ||
    mode === 'context_94' ||
    mode === 'hola_prompt' ||
    mode === 'quota_renew_red' ||
    mode === 'new_chat_button' ||
    mode === 'empty_chat_0' ||
    mode === 'welcome_bubble' ||
    mode === 'tear_resigned';

  if (isMad08) {
    drawMonitorArtMad08(ctx, canvas.width, canvas.height, mode, localFrame);
  } else {
    drawMonitorArt(ctx, canvas.width, canvas.height, mode, frame, localFrame);
  }

  // Draw overlay glass tear if showTear is enabled and mode is not already tear_resigned
  if (showTear && mode !== 'tear_resigned') {
    const tearY = 120 + (Math.min(localFrame, 90) / 90) * 360;
    const tearX = canvas.width * 0.76;
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.28)';
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(tearX, 120);
    ctx.lineTo(tearX, tearY);
    ctx.stroke();

    const tearGrad = ctx.createRadialGradient(tearX - 4, tearY - 4, 2, tearX, tearY, 18);
    tearGrad.addColorStop(0, '#FFFFFF');
    tearGrad.addColorStop(0.35, '#7DD3FC');
    tearGrad.addColorStop(1, 'rgba(14, 165, 233, 0.85)');
    ctx.fillStyle = tearGrad;
    ctx.beginPath();
    ctx.arc(tearX, tearY, 16, 0, Math.PI * 2);
    ctx.fill();
  }

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
  stageMode?: 'cuarto_lluvia' | 'escritorio_monitor_3d' | 'ambos';
}> = ({ frame, coldLockout = false, stageMode = 'ambos' }) => {
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
