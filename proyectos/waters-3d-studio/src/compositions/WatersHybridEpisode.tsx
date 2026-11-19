import React from 'react';
import {
  AbsoluteFill,
  Img,
  interpolate,
  Series,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Video,
} from 'remotion';

export type BeatItem =
  | {
      kind: 'clip';
      durationInFrames: number;
      videoFile: string;
      topTag: string;
      accentColor: string;
      zoomStart?: number;
      zoomEnd?: number;
      shakeIntro?: boolean;
    }
  | {
      kind: 'broll';
      durationInFrames: number;
      topTag: string;
      monitorTitle: string;
      headline: string;
      lines: string[];
      screenshotFile?: string;
      ctaText?: string;
      accentColor: string;
    };

export interface HybridEpisodeProps {
  episodeLabel: string;
  beats: BeatItem[];
}

const ClipBeat: React.FC<{ beat: Extract<BeatItem, { kind: 'clip' }> }> = ({ beat }) => {
  const frame = useCurrentFrame();
  const z0 = beat.zoomStart ?? 1.0;
  const z1 = beat.zoomEnd ?? 1.09;
  const scale = interpolate(frame, [0, beat.durationInFrames], [z0, z1], {
    extrapolateRight: 'clamp',
  });

  const shakeX =
    beat.shakeIntro && frame < 15
      ? Math.sin(frame * 2.9) * 14 * (1 - frame / 15)
      : 0;
  const shakeY =
    beat.shakeIntro && frame < 15
      ? Math.cos(frame * 3.4) * 10 * (1 - frame / 15)
      : 0;

  return (
    <AbsoluteFill style={{ backgroundColor: '#050814', overflow: 'hidden' }}>
      <AbsoluteFill
        style={{
          transform: `translate(${shakeX}px, ${shakeY}px) scale(${scale})`,
        }}
      >
        <Video
          src={staticFile(`clips/${beat.videoFile}`)}
          muted
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
      </AbsoluteFill>

      {/* Subtle top vignette for readability without blocking bottom area for Captions */}
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(5,8,20,0.68) 0%, rgba(5,8,20,0) 24%, rgba(5,8,20,0) 100%)',
          pointerEvents: 'none',
        }}
      />

      {beat.shakeIntro && frame < 8 && (
        <AbsoluteFill
          style={{
            backgroundColor: beat.accentColor,
            opacity: interpolate(frame, [0, 8], [0.32, 0]),
            pointerEvents: 'none',
          }}
        />
      )}
    </AbsoluteFill>
  );
};

const getDrainColor = (pct: number) =>
  pct > 50 ? '#22C55E' : pct > 20 ? '#F59E0B' : '#FF4D4D';

const QUOTA_MODEL_CARDS = [
  { label: 'GEMINI MODELS', delay: 0 },
  { label: 'CLAUDE & GPT', delay: 10 },
  { label: 'GEMINI 4 ARGON', delay: 20 },
];

/** Dynamic 100%->0% battery drain, staggered model meters, and decorated screenshot frame. */
const QuotaDrainHUD: React.FC<{
  screenshotFile: string;
  accentColor: string;
  durationInFrames: number;
}> = ({ screenshotFile, accentColor, durationInFrames }) => {
  const frame = useCurrentFrame();
  const drainEnd = Math.max(20, Math.min(75, durationInFrames - 30));
  const pct = Math.round(
    interpolate(frame, [4, drainEnd], [100, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    })
  );
  const mainColor = getDrainColor(pct);
  const isEmpty = pct === 0;
  const alertPulse = isEmpty ? 0.65 + 0.35 * Math.sin(frame * 0.45) : 1;
  const scannerY = interpolate(frame % 54, [0, 54], [0, 100]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
      {/* Battery / Pila Principal 100% -> 0% */}
      <div
        style={{
          background: '#040710',
          border: `2px solid ${mainColor}`,
          borderRadius: 20,
          padding: '16px 20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 18,
          boxShadow: `0 0 28px ${mainColor}33`,
        }}
      >
        <div style={{ flex: 1 }}>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: 10,
            }}
          >
            <span
              style={{
                fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
                fontSize: 20,
                fontWeight: 800,
                color: mainColor,
                opacity: alertPulse,
                letterSpacing: 1,
              }}
            >
              {isEmpty ? '🚨 ¡CUOTA AGOTADA!' : '⚡ DRENANDO CUOTA SEMANAL'}
            </span>
          </div>
          {/* Battery graphic */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <div
              style={{
                flex: 1,
                height: 36,
                borderRadius: 10,
                border: `3px solid ${mainColor}`,
                padding: 4,
                background: '#0A0F1F',
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  width: `${pct}%`,
                  height: '100%',
                  borderRadius: 5,
                  background: `linear-gradient(90deg, ${mainColor}AA 0%, ${mainColor} 100%)`,
                  boxShadow: `0 0 18px ${mainColor}`,
                }}
              />
            </div>
            <div
              style={{
                width: 8,
                height: 18,
                borderRadius: '0 4px 4px 0',
                backgroundColor: mainColor,
              }}
            />
          </div>
        </div>
        <div
          style={{
            fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
            fontWeight: 900,
            fontSize: 54,
            lineHeight: 1,
            color: mainColor,
            fontVariantNumeric: 'tabular-nums',
            minWidth: 138,
            textAlign: 'right',
            textShadow: `0 0 20px ${mainColor}66`,
          }}
        >
          {pct}%
        </div>
      </div>

      {/* 3 Contenedores Dinámicos por Familia de Modelos */}
      <div style={{ display: 'flex', gap: 12 }}>
        {QUOTA_MODEL_CARDS.map((card) => {
          const cardEnd = Math.max(18, Math.min(58 + card.delay, durationInFrames - 20));
          const cardPct = Math.round(
            interpolate(frame, [4 + card.delay, cardEnd], [100, 0], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            })
          );
          const cardColor = getDrainColor(cardPct);
          return (
            <div
              key={card.label}
              style={{
                flex: 1,
                background: '#040710',
                border: `2px solid ${cardColor}88`,
                borderRadius: 16,
                padding: '12px 14px',
              }}
            >
              <div
                style={{
                  fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
                  fontSize: 15,
                  fontWeight: 800,
                  color: '#CBD5E1',
                  marginBottom: 6,
                }}
              >
                {card.label}
              </div>
              <div
                style={{
                  fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
                  fontSize: 32,
                  fontWeight: 900,
                  color: cardColor,
                  fontVariantNumeric: 'tabular-nums',
                  marginBottom: 8,
                }}
              >
                {cardPct}%
              </div>
              <div
                style={{
                  height: 8,
                  borderRadius: 99,
                  background: '#1E293B',
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    width: `${cardPct}%`,
                    height: '100%',
                    background: cardColor,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Screenshot Real Decorado + Escáner Láser + Pill Overages */}
      <div
        style={{
          position: 'relative',
          background: '#040710',
          border: `3px solid ${accentColor}`,
          borderRadius: 22,
          padding: 12,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          overflow: 'hidden',
          boxShadow: `0 0 36px ${accentColor}33`,
        }}
      >
        <Img
          src={staticFile(screenshotFile)}
          style={{
            width: '100%',
            maxHeight: 620,
            objectFit: 'contain',
            borderRadius: 14,
          }}
        />
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: `${scannerY}%`,
            height: 4,
            background: `linear-gradient(90deg, transparent 0%, ${accentColor} 50%, transparent 100%)`,
            boxShadow: `0 0 18px ${accentColor}`,
            pointerEvents: 'none',
          }}
        />
        <div
          style={{
            position: 'absolute',
            top: 22,
            right: 22,
            background: 'rgba(5, 8, 20, 0.92)',
            border: '2px solid #22C55E',
            borderRadius: 999,
            padding: '8px 18px',
            fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
            fontSize: 18,
            fontWeight: 900,
            color: '#22C55E',
            boxShadow: '0 4px 16px rgba(0,0,0,0.6)',
          }}
        >
          ✓ ENABLE OVERAGES: OFF
        </div>
      </div>
    </div>
  );
};

const BRollMonitorBeat: React.FC<{ beat: Extract<BeatItem, { kind: 'broll' }> }> = ({
  beat,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  const slowZoom = interpolate(frame, [0, beat.durationInFrames], [0.97, 1.04], {
    extrapolateRight: 'clamp',
  });

  // Typewriter progress for code/log lines
  const totalChars = beat.lines.join('\n').length;
  const revealedChars = Math.floor(
    interpolate(frame, [6, Math.max(18, beat.durationInFrames - 18)], [0, totalChars], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    })
  );

  let consumed = 0;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#060913',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '120px 56px 260px 56px',
      }}
    >
      {/* Animated Tech Grid Background */}
      <AbsoluteFill
        style={{
          backgroundImage: `radial-gradient(${beat.accentColor}28 1.5px, transparent 1.5px)`,
          backgroundSize: '36px 36px',
          opacity: 0.75,
        }}
      />

      {/* Glowing Monitor Card */}
      <div
        style={{
          width: '100%',
          transform: `scale(${pop * slowZoom})`,
          background: 'linear-gradient(180deg, #0D1428 0%, #070B16 100%)',
          border: `4px solid ${beat.accentColor}`,
          borderRadius: 36,
          padding: 40,
          boxShadow: `0 24px 80px rgba(0,0,0,0.8), 0 0 48px ${beat.accentColor}44`,
        }}
      >
        {/* Window Chrome */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderBottom: `2px solid ${beat.accentColor}44`,
            paddingBottom: 20,
            marginBottom: 28,
          }}
        >
          <div style={{ display: 'flex', gap: 12 }}>
            <div style={{ width: 18, height: 18, borderRadius: 99, background: '#FF5F56' }} />
            <div style={{ width: 18, height: 18, borderRadius: 99, background: '#FFBD2E' }} />
            <div style={{ width: 18, height: 18, borderRadius: 99, background: '#27C93F' }} />
          </div>
          <span
            style={{
              fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
              fontSize: 22,
              fontWeight: 700,
              color: beat.accentColor,
              letterSpacing: 1.2,
            }}
          >
            {beat.monitorTitle}
          </span>
        </div>

        {/* Big Headline */}
        <div
          style={{
            fontFamily: 'system-ui, -apple-system, sans-serif',
            fontWeight: 900,
            fontSize: 52,
            lineHeight: 1.12,
            color: '#FFFFFF',
            marginBottom: 28,
            textShadow: `0 0 24px ${beat.accentColor}55`,
          }}
        >
          {beat.headline}
        </div>

        {/* Screenshot Real con HUD Dinámico OR Terminal / Status Lines */}
        {beat.screenshotFile ? (
          <QuotaDrainHUD
            screenshotFile={beat.screenshotFile}
            accentColor={beat.accentColor}
            durationInFrames={beat.durationInFrames}
          />
        ) : (
          <div
            style={{
              background: '#040710',
              border: `2px solid ${beat.accentColor}55`,
              borderRadius: 22,
              padding: '26px 28px',
              display: 'flex',
              flexDirection: 'column',
              gap: 16,
            }}
          >
            {beat.lines.map((line, i) => {
              const start = consumed;
              consumed += line.length + 1;
              const visibleCount = Math.max(0, Math.min(line.length, revealedChars - start));
              const shown = line.slice(0, visibleCount);
              const showCursor = visibleCount > 0 && visibleCount < line.length;
              return (
                <div
                  key={i}
                  style={{
                    fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
                    fontSize: 28,
                    fontWeight: 700,
                    lineHeight: 1.35,
                    color: i === beat.lines.length - 1 ? beat.accentColor : '#E2E8F0',
                    minHeight: 38,
                  }}
                >
                  {shown}
                  {showCursor ? '▌' : ''}
                </div>
              );
            })}
          </div>
        )}

        {/* Optional CTA Pill inside Monitor */}
        {beat.ctaText && (
          <div
            style={{
              marginTop: 32,
              backgroundColor: beat.accentColor,
              color: '#050814',
              fontFamily: 'system-ui, -apple-system, sans-serif',
              fontWeight: 900,
              fontSize: 42,
              textAlign: 'center',
              padding: '22px 28px',
              borderRadius: 22,
              letterSpacing: 1,
            }}
          >
            {beat.ctaText}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

export const WatersHybridEpisode: React.FC<HybridEpisodeProps> = ({
  episodeLabel,
  beats,
}) => {
  const frame = useCurrentFrame();

  // Find active beat for the top HUD badge
  let acc = 0;
  let activeBeat = beats[0];
  for (const b of beats) {
    if (frame >= acc && frame < acc + b.durationInFrames) {
      activeBeat = b;
      break;
    }
    acc += b.durationInFrames;
  }

  return (
    <AbsoluteFill style={{ backgroundColor: '#050814' }}>
      <Series>
        {beats.map((beat, idx) => (
          <Series.Sequence key={idx} durationInFrames={beat.durationInFrames}>
            {beat.kind === 'clip' ? (
              <ClipBeat beat={beat} />
            ) : (
              <BRollMonitorBeat beat={beat} />
            )}
          </Series.Sequence>
        ))}
      </Series>

      {/* Clean Top HUD Pill (leaves bottom 100% open for Captions app) */}
      <AbsoluteFill style={{ pointerEvents: 'none', padding: '56px 40px' }}>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            background: 'rgba(5, 8, 20, 0.78)',
            border: `2px solid ${activeBeat.accentColor}`,
            borderRadius: 999,
            padding: '14px 26px',
            boxShadow: `0 0 24px ${activeBeat.accentColor}44`,
          }}
        >
          <span
            style={{
              fontFamily: 'system-ui, -apple-system, sans-serif',
              fontWeight: 900,
              fontSize: 24,
              color: '#FFFFFF',
              letterSpacing: 1,
            }}
          >
            {activeBeat.topTag}
          </span>
          <span
            style={{
              fontFamily: 'system-ui, -apple-system, sans-serif',
              fontWeight: 800,
              fontSize: 20,
              color: activeBeat.accentColor,
            }}
          >
            {episodeLabel}
          </span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
