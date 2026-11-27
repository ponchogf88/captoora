import React from 'react';
import { interpolate, spring } from 'remotion';

export const HeroHookOverlay: React.FC<{
  frame: number;
  fps: number;
}> = ({ frame, fps }) => {
  const slideIn = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 160 },
  });
  const yShift = interpolate(slideIn, [0, 1], [-30, 0]);
  const pulse = 0.78 + Math.sin(frame * 0.25) * 0.22;

  return (
    <>
      {/* Top Black Friday Alert Strip (leaves bottom 240px clean for OpusClip/Captions) */}
      <div
        style={{
          position: 'absolute',
          top: 44,
          left: 64,
          right: 64,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          transform: `translateY(${yShift}px)`,
          opacity: Math.min(1, slideIn * 1.4),
          pointerEvents: 'none',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 14,
            padding: '12px 24px',
            borderRadius: 14,
            backgroundColor: 'rgba(12, 16, 26, 0.88)',
            border: '2px solid #ff2b4a',
            boxShadow: `0 0 28px rgba(255,43,74,${0.35 * pulse})`,
          }}
        >
          <span
            style={{
              width: 14,
              height: 14,
              borderRadius: '50%',
              backgroundColor: '#ff2b4a',
              boxShadow: '0 0 12px #ff2b4a',
            }}
          />
          <span
            style={{
              fontSize: 24,
              fontWeight: 900,
              letterSpacing: '0.08em',
              color: '#ffffff',
            }}
          >
            BLACK FRIDAY · ALERTA IA
          </span>
        </div>

        <div
          style={{
            padding: '12px 24px',
            borderRadius: 14,
            backgroundColor: 'rgba(255, 43, 74, 0.92)',
            color: '#ffffff',
            fontSize: 28,
            fontWeight: 900,
            letterSpacing: '0.02em',
            boxShadow: '0 10px 30px rgba(0,0,0,0.55)',
          }}
        >
          -$40,000 MXN EN 1 NOCHE
        </div>
      </div>

      {/* Right Concrete Floating Warning Callout */}
      <div
        style={{
          position: 'absolute',
          right: 78,
          top: 250,
          width: 470,
          padding: '22px 26px',
          borderRadius: 18,
          backgroundColor: 'rgba(10, 14, 24, 0.82)',
          border: '2px solid rgba(0, 224, 240, 0.55)',
          boxShadow: '0 18px 45px rgba(0,0,0,0.6)',
          pointerEvents: 'none',
        }}
      >
        <div style={{ fontSize: 19, fontWeight: 800, color: '#ffd166', letterSpacing: '0.06em' }}>
          PRUEBA GRATIS + API CON TARJETA
        </div>
        <div style={{ marginTop: 8, fontSize: 38, fontWeight: 900, lineHeight: 1.08, color: '#ffffff' }}>
          NO METAS TU TARJETA <span style={{ color: '#ff3355' }}>ASÍ</span>
        </div>
        <div
          style={{
            marginTop: 14,
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            fontSize: 21,
            fontWeight: 800,
            color: '#94f2ff',
          }}
        >
          <span>AUTO-RECHARGE: ON</span>
          <span style={{ color: '#ff3355' }}>· TOPE: $0 (APAGADO)</span>
        </div>
      </div>

      {/* Vector Arrow pointing cleanly from left border of callout box toward subject */}
      <svg
        width="230"
        height="120"
        viewBox="0 0 230 120"
        style={{
          position: 'absolute',
          right: 552,
          top: 345,
          pointerEvents: 'none',
        }}
      >
        <defs>
          <marker id="hookArrowHead" markerWidth="12" markerHeight="12" refX="8" refY="6" orient="auto">
            <path d="M0,1 L10,6 L0,11 z" fill="#ff3355" />
          </marker>
        </defs>
        <path
          d="M 218 22 Q 125 88 20 62"
          fill="none"
          stroke="#ff3355"
          strokeWidth="6"
          strokeLinecap="round"
          strokeDasharray="320"
          strokeDashoffset={interpolate(frame, [8, 32], [320, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          })}
          markerEnd="url(#hookArrowHead)"
        />
      </svg>
    </>
  );
};

export const AiPromptBoxOverlay: React.FC<{
  localFrame: number;
  fps: number;
  durationInFrames?: number;
}> = ({ localFrame, fps, durationInFrames = 420 }) => {
  const enter = spring({
    frame: localFrame,
    fps,
    config: { damping: 14, stiffness: 150 },
  });
  const tx = interpolate(enter, [0, 1], [80, 0]);

  const activeTabIdx = Math.floor(localFrame / Math.max(40, Math.round(durationInFrames / 3))) % 3;
  const models = [
    { name: 'Gemini', color: '#38bdf8' },
    { name: 'Claude', color: '#fb923c' },
    { name: 'ChatGPT', color: '#2ee87a' },
  ];

  const promptString =
    'Analiza los 500 clientes y reintenta cada error automáticamente hasta terminar...';
  const typeRate = Math.max(0.72, promptString.length / Math.max(60, durationInFrames * 0.55));
  const typedLen = Math.min(promptString.length, Math.floor(localFrame * typeRate));
  const typedPrompt = promptString.slice(0, typedLen);
  const showCursor = Math.floor(localFrame / 12) % 2 === 0;

  const endFrame = Math.max(90, Math.round(durationInFrames * 0.88));
  const loopProgress = interpolate(localFrame, [24, endFrame], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const retries = Math.max(1, Math.round(loopProgress * 10000));
  const burnUsd = Math.round(loopProgress * 2000);

  return (
    <div
      style={{
        position: 'absolute',
        right: 76,
        top: 120,
        width: 860,
        borderRadius: 24,
        backgroundColor: 'rgba(13, 17, 26, 0.94)',
        border: `2px solid ${models[activeTabIdx].color}88`,
        boxShadow: `0 26px 70px rgba(0,0,0,0.75), 0 0 40px ${models[activeTabIdx].color}22`,
        padding: '28px 32px',
        transform: `translateX(${tx}px)`,
        opacity: enter,
        pointerEvents: 'none',
      }}
    >
      {/* Model Switcher Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 22 }}>
        <div style={{ display: 'flex', gap: 12 }}>
          {models.map((m, i) => {
            const isActive = i === activeTabIdx;
            return (
              <div
                key={m.name}
                style={{
                  padding: '8px 18px',
                  borderRadius: 999,
                  fontSize: 20,
                  fontWeight: 800,
                  backgroundColor: isActive ? m.color : 'rgba(255,255,255,0.06)',
                  color: isActive ? '#090d14' : '#94a3b8',
                }}
              >
                {m.name}
              </div>
            );
          })}
        </div>

        <div
          style={{
            padding: '7px 16px',
            borderRadius: 10,
            backgroundColor: 'rgba(255, 43, 74, 0.16)',
            border: '1px solid #ff3355',
            color: '#ff6b81',
            fontSize: 19,
            fontWeight: 800,
            fontVariantNumeric: 'tabular-nums',
          }}
        >
          AUTO-RECHARGE ON
        </div>
      </div>

      {/* Simulated Prompt Input Box */}
      <div
        style={{
          borderRadius: 16,
          backgroundColor: '#151c2c',
          border: '1px solid rgba(255,255,255,0.14)',
          padding: '22px 24px',
          minHeight: 150,
        }}
      >
        <div style={{ fontSize: 17, fontWeight: 700, color: '#64748b', marginBottom: 10 }}>
          PROMPT DE AGENTE (02:00 AM)
        </div>
        <div style={{ fontSize: 30, fontWeight: 700, lineHeight: 1.35, color: '#f8fafc' }}>
          {typedPrompt}
          <span style={{ color: models[activeTabIdx].color, opacity: showCursor ? 1 : 0 }}>|</span>
        </div>
      </div>

      {/* Live Retry & Spend Explosion Telemetry */}
      <div
        style={{
          marginTop: 22,
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 18,
        }}
      >
        <div
          style={{
            borderRadius: 16,
            backgroundColor: '#111622',
            border: '1px solid rgba(255,255,255,0.08)',
            padding: '18px 22px',
          }}
        >
          <div style={{ fontSize: 18, fontWeight: 700, color: '#94a3b8' }}>BUCLE EN 4 HORAS</div>
          <div
            style={{
              marginTop: 6,
              fontSize: 48,
              fontWeight: 900,
              color: '#fbbf24',
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            {retries.toLocaleString('en-US')}x
          </div>
          <div style={{ fontSize: 17, fontWeight: 700, color: '#cbd5e1' }}>reintentos sin freno</div>
        </div>

        <div
          style={{
            borderRadius: 16,
            backgroundColor: 'rgba(255, 43, 74, 0.12)',
            border: '1px solid rgba(255, 43, 74, 0.55)',
            padding: '18px 22px',
          }}
        >
          <div style={{ fontSize: 18, fontWeight: 700, color: '#fda4af' }}>COBRO ACUMULADO</div>
          <div
            style={{
              marginTop: 6,
              fontSize: 48,
              fontWeight: 900,
              color: '#ff3355',
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            ${burnUsd.toLocaleString('en-US')} USD
          </div>
          <div style={{ fontSize: 17, fontWeight: 700, color: '#fecdd3' }}>sin aviso previo</div>
        </div>
      </div>
    </div>
  );
};

export const SpendingChartOverlay: React.FC<{
  localFrame: number;
  fps: number;
  durationInFrames?: number;
}> = ({ localFrame, fps, durationInFrames = 260 }) => {
  const enter = spring({
    frame: localFrame,
    fps,
    config: { damping: 14, stiffness: 150 },
  });

  const endFrame = Math.max(80, Math.round(durationInFrames * 0.82));
  const progress = interpolate(localFrame, [10, endFrame], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const usd = Math.round(progress * 2000);
  const mxn = usd * 20;

  const bars = [
    { label: '01 AM', val: '$80', maxH: 48, color: '#38bdf8' },
    { label: '02 AM', val: '$420', maxH: 102, color: '#fbbf24' },
    { label: '04 AM', val: '$1,250', maxH: 175, color: '#fb923c' },
    { label: '06 AM', val: '$2,000', maxH: 242, color: '#ff2b4a' },
  ];

  return (
    <div
      style={{
        position: 'absolute',
        right: 76,
        top: 96,
        width: 880,
        borderRadius: 24,
        backgroundColor: 'rgba(13, 17, 26, 0.95)',
        border: '2px solid rgba(255, 43, 74, 0.65)',
        boxShadow: '0 26px 75px rgba(0,0,0,0.8)',
        padding: '28px 34px',
        opacity: enter,
        transform: `translateY(${interpolate(enter, [0, 1], [36, 0])}px)`,
        pointerEvents: 'none',
      }}
    >
      {/* Header + Big Counter */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 22 }}>
        <div>
          <div style={{ fontSize: 19, fontWeight: 800, color: '#94f2ff', letterSpacing: '0.06em' }}>
            CONSOLA DE FACTURACIÓN API
          </div>
          <div style={{ marginTop: 4, fontSize: 32, fontWeight: 900, color: '#ffffff' }}>
            Así sube en una madrugada
          </div>
        </div>

        <div style={{ textAlign: 'right', flexShrink: 0 }}>
          <div
            style={{
              fontSize: 46,
              fontWeight: 900,
              lineHeight: 1.05,
              whiteSpace: 'nowrap',
              color: '#ff3355',
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            ${usd.toLocaleString('en-US')} USD
          </div>
          <div
            style={{
              marginTop: 4,
              fontSize: 21,
              fontWeight: 800,
              whiteSpace: 'nowrap',
              color: '#ffd166',
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            ~${mxn.toLocaleString('en-US')} MXN
          </div>
        </div>
      </div>

      {/* Animated Bars + Pointing Vector Arrow */}
      <div
        style={{
          position: 'relative',
          height: 365,
          backgroundColor: '#0e131e',
          borderRadius: 18,
          border: '1px solid rgba(255,255,255,0.08)',
          padding: '28px 34px 22px',
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'space-around',
        }}
      >
        {bars.map((b, idx) => {
          const barStart = idx * 0.2;
          const barFill = interpolate(progress, [barStart, barStart + 0.28], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const curH = Math.max(8, b.maxH * barFill);
          return (
            <div
              key={b.label}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                width: 150,
              }}
            >
              <div
                style={{
                  marginBottom: 10,
                  fontSize: 26,
                  fontWeight: 900,
                  color: b.color,
                  opacity: barFill > 0.25 ? 1 : 0,
                }}
              >
                {b.val}
              </div>
              <div
                style={{
                  width: 92,
                  height: curH,
                  borderRadius: '14px 14px 4px 4px',
                  backgroundColor: b.color,
                  boxShadow: `0 0 26px ${b.color}55`,
                }}
              />
              <div style={{ marginTop: 12, fontSize: 20, fontWeight: 800, color: '#cbd5e1' }}>
                {b.label}
              </div>
            </div>
          );
        })}

        {/* Curved Arrow pointing at $2,000 spike */}
        <svg
          width="360"
          height="160"
          viewBox="0 0 360 160"
          style={{ position: 'absolute', left: 110, top: 26 }}
        >
          <defs>
            <marker id="chartArrow" markerWidth="12" markerHeight="12" refX="8" refY="6" orient="auto">
              <path d="M0,1 L10,6 L0,11 z" fill="#00e0f0" />
            </marker>
          </defs>
          <path
            d="M 20 130 Q 170 25 325 32"
            fill="none"
            stroke="#00e0f0"
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray="420"
            strokeDashoffset={interpolate(progress, [0.45, 0.92], [420, 0], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            })}
            markerEnd="url(#chartArrow)"
          />
        </svg>
      </div>
    </div>
  );
};
