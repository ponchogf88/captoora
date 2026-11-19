import React from 'react';
import {
  AbsoluteFill,
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

        {/* Terminal / Status Lines */}
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
