import React, { useMemo } from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';
import {
  ChispaAstronaut3D,
  ChispaExpression,
} from '../components/ChispaAstronaut3D';
import {
  FloatingHouseDiorama3D,
  GoldenKitBox3D,
  Gta6ViceCityDiorama3D,
  SilverLaptop3D,
  StudioFloor3D,
} from '../components/ChispaStageProps3D';
import {
  ClaudeStarburstLogo,
  GeminiSparkleLogo,
  GoogleGLogo,
  OpenAILogo,
  TerminalHarnessLogo,
} from '../components/BrandLogos';

export type NeonCardType =
  | 'alert_intro'
  | 'vs_duel'
  | 'bench_race'
  | 'gta6_build'
  | 'three_secrets'
  | 'cta_wink';

export type StagePropType =
  | 'none'
  | 'laptop'
  | 'floating_house'
  | 'gta6_city'
  | 'kit_box';

export interface NeonBeatItem {
  durationInFrames: number;
  topTag: string;
  accentColor: string;
  /** Maps both legacy 5 expressions and new 8 Chispa expressions seamlessly */
  expression: ChispaExpression | string;
  cardType: NeonCardType;
  stageProp?: StagePropType;
  stepBadge?: string;
  pillText?: string;
  headlinePrefix?: string;
  headlineFocus?: string;
  headlineSuffix?: string;
  terminalCmd?: string;
  terminalSub?: string;
  heroTitle?: string;
  heroSubtitle?: string;
  speaking?: boolean;
}

export interface Neon3DEpisodeProps {
  episodeLabel: string;
  beats: NeonBeatItem[];
}

function mapExpression(expr: string): ChispaExpression {
  const valid: ChispaExpression[] = [
    'happy_open',
    'sad_cloud',
    'determined_hacker',
    'happy_arcs',
    'wink',
    'zen_proud',
    'shock_sweat',
    'star_eyes',
  ];
  if (valid.includes(expr as ChispaExpression)) {
    return expr as ChispaExpression;
  }
  switch (expr) {
    case 'shock':
      return 'shock_sweat';
    case 'skeptic':
      return 'sad_cloud';
    case 'laser_focus':
      return 'determined_hacker';
    case 'happy_wink':
      return 'wink';
    default:
      return 'happy_open';
  }
}

const POP_FRAMES = [2, 8, 24, 36, 48];

const StudioBackdropParticles: React.FC<{ frame: number; accentColor: string }> = ({
  frame,
  accentColor,
}) => {
  const dots = useMemo(() => {
    const arr: { pos: [number, number, number]; size: number; gold: boolean }[] = [];
    for (let i = 0; i < 42; i++) {
      const s1 = Math.sin(i * 23.17) * 43758.5453;
      const s2 = Math.sin(i * 61.91) * 43758.5453;
      const s3 = Math.sin(i * 11.43) * 43758.5453;
      arr.push({
        pos: [
          (s1 - Math.floor(s1) - 0.5) * 9,
          (s2 - Math.floor(s2)) * 5.8 - 0.3,
          -2.5 - (s3 - Math.floor(s3)) * 5,
        ],
        size: 0.018 + (i % 3) * 0.012,
        gold: i % 2 === 0,
      });
    }
    return arr;
  }, []);

  const floatOffset = ((frame * 0.008) % 2) - 1;

  return (
    <group position={[0, floatOffset * 0.25, 0]}>
      {dots.map((d, idx) => (
        <mesh key={idx} position={d.pos}>
          <sphereGeometry args={[d.size, 8, 8]} />
          <meshBasicMaterial
            color={d.gold ? '#FACC15' : accentColor}
            transparent
            opacity={0.55}
          />
        </mesh>
      ))}
    </group>
  );
};

const ChispaScene3D: React.FC<{
  beat: NeonBeatItem;
  beatIndex: number;
  localFrame: number;
}> = ({ beat, beatIndex, localFrame }) => {
  const globalFrame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { camera } = useThree();
  const t = globalFrame / fps;

  const chispaExpr = mapExpression(beat.expression);
  const propType: StagePropType =
    beat.stageProp ??
    (beat.cardType === 'vs_duel'
      ? 'floating_house'
      : beat.cardType === 'gta6_build'
      ? 'gta6_city'
      : beat.cardType === 'cta_wink'
      ? 'kit_box'
      : beat.cardType === 'bench_race' || beat.cardType === 'three_secrets'
      ? 'laptop'
      : 'none');

  // Dynamic gentle studio camera motion — close juicy designer-toy framing above 260px safe zone
  const shockShake =
    chispaExpr === 'shock_sweat' && localFrame < 14
      ? Math.sin(localFrame * 3.1) * 0.07
      : 0;
  const camX = Math.sin(t * 0.72) * 0.24 + shockShake;
  const camY = 1.50;
  const camZ = 10.15;
  camera.position.set(camX, camY, camZ);
  camera.lookAt(new THREE.Vector3(0, 1.15, 0));

  // Floor color adapts subtly per mood (cool obsidian slate vs warm oak studio desk on CTA/kit beats)
  const floorColor =
    propType === 'kit_box'
      ? '#483226'
      : propType === 'laptop' || propType === 'gta6_city'
      ? '#252B39'
      : '#2B313F';

  // Character X placement balances with side prop on the floor without touching
  let charX = 0;
  let charRotY = 0;
  if (propType === 'floating_house' || propType === 'gta6_city' || propType === 'laptop') {
    charX = -0.90;
    charRotY = 0.22;
  } else if (propType === 'kit_box') {
    charX = 0.82;
    charRotY = -0.22;
  }

  const charY = -0.22; // Soles of moon-boots rest right on floorY = -1.05
  const jumpHeight = Math.abs(Math.sin(t * 4.5)) * 0.08;

  return (
    <>
      <color attach="background" args={['#02040A']} />
      <fog attach="fog" args={['#02040A', 13, 26]} />

      {/* Warm Studio Key + Cool Rim + Accent Fill */}
      <ambientLight intensity={1.05} />
      <directionalLight position={[4, 8, 6]} intensity={2.2} color="#FFFDF7" castShadow />
      <directionalLight position={[-5, 5, 3]} intensity={1.6} color="#93C5FD" />
      <pointLight position={[0, 1.5, 4.5]} intensity={1.9} color={beat.accentColor} />

      <StudioBackdropParticles frame={globalFrame} accentColor={beat.accentColor} />

      <StudioFloor3D
        floorColor={floorColor}
        charPos={[charX, charY, 0.15]}
        charJumpHeight={jumpHeight}
        floorY={-1.05}
      />

      <ChispaAstronaut3D
        frame={globalFrame}
        localFrame={localFrame}
        fps={fps}
        expression={chispaExpr}
        accentColor={beat.accentColor}
        position={[charX, charY, 0.15]}
        rotationY={charRotY}
        scale={1.02}
        speaking={beat.speaking ?? true}
        popFrames={POP_FRAMES}
      />

      {propType === 'laptop' && (
        <SilverLaptop3D
          frame={globalFrame}
          localFrame={localFrame}
          fps={fps}
          position={[0.88, -1.04, -0.06]}
          rotationY={-0.38}
          scale={0.92}
          accentColor={beat.accentColor}
        />
      )}

      {propType === 'floating_house' && (
        <FloatingHouseDiorama3D
          frame={globalFrame}
          localFrame={localFrame}
          fps={fps}
          position={[0.92, -0.04, -0.15]}
          scale={0.88}
        />
      )}

      {propType === 'gta6_city' && (
        <Gta6ViceCityDiorama3D
          frame={globalFrame}
          localFrame={localFrame}
          fps={fps}
          position={[0.94, -0.54, -0.18]}
          scale={0.78}
        />
      )}

      {propType === 'kit_box' && (
        <GoldenKitBox3D
          frame={globalFrame}
          localFrame={localFrame}
          fps={fps}
          position={[-0.86, -0.57, -0.04]}
        />
      )}

      {/* Subtle golden glow light in key beats */}
      {beatIndex >= 2 && (
        <pointLight position={[0.9, 0.5, 2.5]} intensity={0.9} color="#FDE68A" />
      )}
    </>
  );
};

/**
 * Elastic spring Pop-In container synchronized cleanly to exact SFX frames
 */
const PopBox: React.FC<{
  localFrame: number;
  popFrame: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ localFrame, popFrame, children, style }) => {
  const { fps } = useVideoConfig();
  if (localFrame < popFrame) {
    return (
      <div
        style={{
          ...style,
          opacity: 0,
          transform: 'scale(0.65) translateY(12px)',
        }}
      >
        {children}
      </div>
    );
  }
  const s = spring({
    frame: localFrame - popFrame,
    fps,
    config: { damping: 10, stiffness: 260, mass: 0.72 },
  });
  return (
    <div
      style={{
        ...style,
        opacity: interpolate(s, [0, 0.35], [0, 1], { extrapolateRight: 'clamp' }),
        transform: `scale(${s})`,
        transformOrigin: 'center center',
      }}
    >
      {children}
    </div>
  );
};

/**
 * Typewriter component synced to mechanical keyboard ASMR frames [startFrame..endFrame]
 */
function typedSlice(
  text: string,
  localFrame: number,
  startFrame: number,
  endFrame: number
): { shown: string; isTyping: boolean } {
  if (localFrame < startFrame) {
    return { shown: '', isTyping: false };
  }
  const progress = interpolate(localFrame, [startFrame, endFrame], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const count = Math.max(1, Math.floor(progress * text.length));
  return {
    shown: text.slice(0, count),
    isTyping: count < text.length,
  };
}

/**
 * Subtle terminal log rain behind upper canvas — mirrors @lynxstudiosbcn frames
 */
const FaintTerminalWallpaper: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const scroll = (localFrame * 1.4) % 90;
  return (
    <div
      style={{
        position: 'absolute',
        top: -scroll,
        left: 28,
        right: 28,
        height: 820,
        overflow: 'hidden',
        opacity: 0.13,
        fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
        fontSize: 23,
        lineHeight: 1.65,
        color: '#22C55E',
        pointerEvents: 'none',
        userSelect: 'none',
      }}
    >
      <div>uses · 41.2k tokens · model=gemini-4-hydrogen</div>
      <div>&gt; reasoning_effort=xhigh · mode=MAX · 1M context</div>
      <div>Task(vice-city-3d) running... 57.0% Terminal Bench</div>
      <div>✓ floating_house: $1.50 USD (12 min) vs $19.00 (45 min)</div>
      <div>&gt; route google.com --tab=modo-ia --quota=unlimited</div>
      <div>uses · 41.2k tokens · cache_read=10x_efficiency</div>
      <div>$ dispatch 20_agents --parallel --cost=$0.00</div>
      <div>✓ API free tier active: 5 RPM · 250k TPM · gemini-4-hydrogen</div>
    </div>
  );
};

/**
 * Top Kinetic Headline with @lynxstudiosbcn Blue Selection Box + 4 White Corner Handles
 */
const KineticSelectionHeadline: React.FC<{
  prefix: string;
  focus: string;
  suffix?: string;
  localFrame: number;
}> = ({ prefix, focus, suffix = '', localFrame }) => {
  const { fps } = useVideoConfig();
  const fullPrefix = typedSlice(prefix, localFrame, 0, 5).shown;
  const showFocus = localFrame >= 5;
  const focusPop = showFocus
    ? spring({
        frame: localFrame - 5,
        fps,
        config: { damping: 11, stiffness: 250 },
      })
    : 0;

  return (
    <div
      style={{
        textAlign: 'center',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
        fontSize: 44,
        fontWeight: 800,
        lineHeight: 1.24,
        color: '#CBD5E1',
        letterSpacing: -0.6,
        marginBottom: 18,
        minHeight: 72,
      }}
    >
      <span>{fullPrefix} </span>
      {showFocus && (
        <span
          style={{
            display: 'inline-block',
            position: 'relative',
            background: '#050811',
            color: '#FFFFFF',
            fontWeight: 900,
            padding: '2px 14px 4px 14px',
            margin: '0 4px',
            border: '2.5px solid #3B82F6',
            boxShadow: '0 0 18px rgba(59, 130, 246, 0.45)',
            transform: `scale(${focusPop})`,
          }}
        >
          {focus}
          {/* 4 White Square Corner Selection Handles */}
          {[
            { top: -4, left: -4 },
            { top: -4, right: -4 },
            { bottom: -4, left: -4 },
            { bottom: -4, right: -4 },
          ].map((pos, idx) => (
            <span
              key={idx}
              style={{
                position: 'absolute',
                width: 7,
                height: 7,
                background: '#FFFFFF',
                border: '1px solid #1E293B',
                ...pos,
              }}
            />
          ))}
        </span>
      )}
      {localFrame >= 11 && suffix && <span> {suffix}</span>}
    </div>
  );
};

/**
 * Green Numbered Step Pill (@lynxstudiosbcn signature style)
 */
const NumberedGreenPill: React.FC<{
  badge: string;
  text: string;
  localFrame: number;
  accentColor: string;
}> = ({ badge, text, localFrame }) => (
  <PopBox
    localFrame={localFrame}
    popFrame={2}
    style={{ display: 'flex', justifyContent: 'center', marginBottom: 16 }}
  >
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 12,
        background: 'rgba(4, 15, 10, 0.94)',
        border: '2.5px solid #22C55E',
        borderRadius: 999,
        padding: '10px 26px 10px 12px',
        boxShadow: '0 0 26px rgba(34, 197, 94, 0.35)',
      }}
    >
      <div
        style={{
          width: 40,
          height: 40,
          borderRadius: 999,
          background: '#22C55E',
          color: '#030805',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'system-ui, sans-serif',
          fontWeight: 900,
          fontSize: 22,
        }}
      >
        {badge}
      </div>
      <span
        style={{
          fontFamily: 'system-ui, -apple-system, sans-serif',
          fontWeight: 800,
          fontSize: 28,
          color: '#FFFFFF',
          letterSpacing: -0.3,
        }}
      >
        {text}
      </span>
    </div>
  </PopBox>
);

/**
 * Live Typing Terminal Window + Dynamic Popping Result Cards inside upper stage
 */
const TerminalPopWindow: React.FC<{
  beat: NeonBeatItem;
  beatIndex: number;
  localFrame: number;
}> = ({ beat, beatIndex, localFrame }) => {
  const cmd =
    beat.terminalCmd ??
    '$ run gemini-4-hydrogen --mode MAX --reasoning xhigh';
  const sub =
    beat.terminalSub ??
    '> Output: 3.75x faster · 10x cheaper ($1.50 vs $19.00)';

  const cmdState = typedSlice(cmd, localFrame, 9, 32);
  const subState = typedSlice(sub, localFrame, 24, 46);
  const cursorVisible = Math.floor(localFrame / 6) % 2 === 0;

  return (
    <PopBox localFrame={localFrame} popFrame={8}>
      <div
        style={{
          width: '100%',
          background: 'rgba(6, 10, 18, 0.94)',
          border: `2.5px solid ${beat.accentColor}`,
          borderRadius: 24,
          padding: '18px 24px 20px 24px',
          boxShadow: `0 22px 60px rgba(0,0,0,0.85), 0 0 34px ${beat.accentColor}38`,
        }}
      >
        {/* macOS Window Bar */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            paddingBottom: 12,
            marginBottom: 12,
            borderBottom: '1.5px solid rgba(148, 163, 184, 0.22)',
          }}
        >
          <div style={{ display: 'flex', gap: 9 }}>
            <div style={{ width: 13, height: 13, borderRadius: 99, background: '#FF5F56' }} />
            <div style={{ width: 13, height: 13, borderRadius: 99, background: '#FFBD2E' }} />
            <div style={{ width: 13, height: 13, borderRadius: 99, background: '#27C93F' }} />
          </div>
          <span
            style={{
              fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
              fontSize: 18,
              color: '#94A3B8',
              fontWeight: 700,
            }}
          >
            {beat.topTag}
          </span>
        </div>

        {/* Mechanical Keyboard Live Typing Command */}
        <div
          style={{
            fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
            fontSize: 22,
            lineHeight: 1.45,
            marginBottom: 14,
            minHeight: 68,
          }}
        >
          <div style={{ color: '#22C55E', fontWeight: 700 }}>
            {cmdState.shown}
            {(cmdState.isTyping || (!subState.shown && cursorVisible)) && (
              <span style={{ color: '#FFFFFF', marginLeft: 3 }}>▋</span>
            )}
          </div>
          {localFrame >= 24 && (
            <div style={{ color: '#38BDF8', fontWeight: 600, marginTop: 4 }}>
              {subState.shown}
              {(subState.isTyping || cursorVisible) && (
                <span style={{ color: '#00F5D4', marginLeft: 3 }}>▋</span>
              )}
            </div>
          )}
        </div>

        {/* POPPING SUB-CARDS AT FRAMES 24, 36, 48 */}
        {beat.cardType === 'alert_intro' && (
          <div style={{ display: 'flex', gap: 14 }}>
            <PopBox localFrame={localFrame} popFrame={24} style={{ flex: 1 }}>
              <div style={{ background: '#130A10', border: '2px solid #D97757', borderRadius: 16, padding: '12px 16px', display: 'flex', alignItems: 'center', gap: 12 }}>
                <ClaudeStarburstLogo size={38} />
                <div>
                  <div style={{ color: '#FFFFFF', fontWeight: 900, fontSize: 22, fontFamily: 'system-ui, sans-serif' }}>Fable 5.2</div>
                  <div style={{ color: '#FF4D4D', fontWeight: 800, fontSize: 20, fontFamily: 'ui-monospace, monospace' }}>$19.00 · 45m</div>
                </div>
              </div>
            </PopBox>
            <PopBox localFrame={localFrame} popFrame={36} style={{ flex: 1 }}>
              <div style={{ background: '#06191D', border: '2.5px solid #00F5D4', borderRadius: 16, padding: '12px 16px', display: 'flex', alignItems: 'center', gap: 12 }}>
                <GeminiSparkleLogo size={38} />
                <div>
                  <div style={{ color: '#FFFFFF', fontWeight: 900, fontSize: 22, fontFamily: 'system-ui, sans-serif' }}>Gemini 4 Hydro</div>
                  <div style={{ color: '#22C55E', fontWeight: 800, fontSize: 20, fontFamily: 'ui-monospace, monospace' }}>$1.50 / $0 · 12m</div>
                </div>
              </div>
            </PopBox>
          </div>
        )}

        {beat.cardType === 'vs_duel' && (
          <div style={{ display: 'flex', gap: 14 }}>
            <PopBox localFrame={localFrame} popFrame={24} style={{ flex: 1 }}>
              <div style={{ background: '#14090E', border: '2px solid #D97757', borderRadius: 16, padding: '14px 16px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
                  <ClaudeStarburstLogo size={32} />
                  <span style={{ color: '#D97757', fontWeight: 900, fontSize: 20, fontFamily: 'system-ui, sans-serif' }}>FABLE 5.2</span>
                </div>
                <div style={{ color: '#FF4D4D', fontWeight: 900, fontSize: 38, fontFamily: 'ui-monospace, monospace' }}>$19.00</div>
                <div style={{ color: '#CBD5E1', fontSize: 18, fontFamily: 'ui-monospace, monospace' }}>⏱ 45 min · $10/$50 API</div>
              </div>
            </PopBox>
            <PopBox localFrame={localFrame} popFrame={36} style={{ flex: 1 }}>
              <div style={{ background: '#05191A', border: '2.5px solid #22C55E', borderRadius: 16, padding: '14px 16px', boxShadow: '0 0 22px rgba(34,197,94,0.22)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
                  <GeminiSparkleLogo size={32} />
                  <span style={{ color: '#00F5D4', fontWeight: 900, fontSize: 20, fontFamily: 'system-ui, sans-serif' }}>HYDROGEN</span>
                </div>
                <div style={{ color: '#22C55E', fontWeight: 900, fontSize: 38, fontFamily: 'ui-monospace, monospace' }}>$1.50 / $0</div>
                <div style={{ color: '#FFFFFF', fontSize: 18, fontFamily: 'ui-monospace, monospace' }}>⚡ 12 min · 10x MÁS BARATO</div>
              </div>
            </PopBox>
          </div>
        )}

        {beat.cardType === 'bench_race' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {[
              { name: 'Gemini 4 Hydrogen', pct: 57, col: '#00F5D4', pop: 24, note: '57.0% · TOP #5 (Antes 18.2%)', Icon: GeminiSparkleLogo },
              { name: 'Claude Fable 5.1', pct: 46, col: '#D97757', pop: 36, note: 'Superado · $10/$50 API', Icon: ClaudeStarburstLogo },
              { name: 'GPT Astra 6', pct: 44, col: '#10A37F', pop: 48, note: 'Superado · Contexto menor', Icon: OpenAILogo },
            ].map((row, ri) => {
              const barP = interpolate(localFrame, [row.pop, row.pop + 18], [0, row.pct], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              return (
                <PopBox key={ri} localFrame={localFrame} popFrame={row.pop}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12, background: '#0B1220', borderRadius: 14, padding: '10px 14px', border: `1.5px solid ${row.col}55` }}>
                    <row.Icon size={30} />
                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: 'system-ui, sans-serif', fontWeight: 800, fontSize: 19, color: '#FFFFFF', marginBottom: 5 }}>
                        <span>{row.name}</span>
                        <span style={{ color: row.col, fontFamily: 'ui-monospace, monospace' }}>{row.note}</span>
                      </div>
                      <div style={{ height: 9, background: '#1E293B', borderRadius: 99, overflow: 'hidden' }}>
                        <div style={{ width: `${Math.min(100, barP * 1.55)}%`, height: '100%', background: row.col, borderRadius: 99 }} />
                      </div>
                    </div>
                  </div>
                </PopBox>
              );
            })}
          </div>
        )}

        {beat.cardType === 'gta6_build' && (
          <div style={{ display: 'flex', gap: 12 }}>
            <PopBox localFrame={localFrame} popFrame={24} style={{ flex: 1 }}>
              <div style={{ background: '#160B11', border: '2px solid #FF4D4D', borderRadius: 16, padding: '12px 16px' }}>
                <div style={{ color: '#FF4D4D', fontWeight: 900, fontSize: 19, fontFamily: 'system-ui, sans-serif', marginBottom: 4 }}>gemini.google.com ❌</div>
                <div style={{ color: '#CBD5E1', fontSize: 17, fontFamily: 'ui-monospace, monospace' }}>Nivel Bajo: Mapa vacío</div>
              </div>
            </PopBox>
            <PopBox localFrame={localFrame} popFrame={36} style={{ flex: 1.25 }}>
              <div style={{ background: '#061B15', border: '2.5px solid #DFB15B', borderRadius: 16, padding: '12px 16px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                  <GoogleGLogo size={24} />
                  <span style={{ color: '#DFB15B', fontWeight: 900, fontSize: 19, fontFamily: 'system-ui, sans-serif' }}>AI Studio · MODO MAX ✅</span>
                </div>
                <div style={{ color: '#FFFFFF', fontSize: 17, fontFamily: 'ui-monospace, monospace' }}>10 min: Coches, aviones, lancha y 1ra persona</div>
              </div>
            </PopBox>
          </div>
        )}

        {beat.cardType === 'three_secrets' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            <PopBox localFrame={localFrame} popFrame={24}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, background: '#061A12', border: '2px solid #22C55E', borderRadius: 14, padding: '10px 16px' }}>
                <GoogleGLogo size={30} />
                <div style={{ fontFamily: 'system-ui, sans-serif', fontWeight: 800, fontSize: 20, color: '#FFFFFF' }}>
                  1. <span style={{ color: '#22C55E' }}>google.com ➔ MODO IA</span> (Sin límite 5h/semanal)
                </div>
              </div>
            </PopBox>
            <PopBox localFrame={localFrame} popFrame={36}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, background: '#081322', border: '2px solid #38BDF8', borderRadius: 14, padding: '10px 16px' }}>
                <GeminiSparkleLogo size={30} />
                <div style={{ fontFamily: 'system-ui, sans-serif', fontWeight: 800, fontSize: 20, color: '#FFFFFF' }}>
                  2. <span style={{ color: '#38BDF8' }}>aistudio.google.com</span> (Modo MAX · Extra Alto)
                </div>
              </div>
            </PopBox>
            <PopBox localFrame={localFrame} popFrame={48}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, background: '#110D1D', border: '2px solid #A855F7', borderRadius: 14, padding: '10px 16px' }}>
                <TerminalHarnessLogo size={30} />
                <div style={{ fontFamily: 'ui-monospace, monospace', fontWeight: 800, fontSize: 19, color: '#E2E8F0' }}>
                  3. API Gratis: <span style={{ color: '#C084FC' }}>gemini-4-hydrogen</span>
                </div>
              </div>
            </PopBox>
          </div>
        )}

        {beat.cardType === 'cta_wink' && (
          <PopBox localFrame={localFrame} popFrame={beatIndex === 9 ? 24 : 36}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                background: '#FFFFFF',
                borderRadius: 999,
                padding: '10px 16px 10px 14px',
                boxShadow: '0 12px 30px rgba(0,0,0,0.45)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                <div style={{ width: 42, height: 42, borderRadius: 999, background: '#2563EB', color: '#FFFFFF', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 900, fontSize: 18, fontFamily: 'system-ui, sans-serif' }}>
                  TÚ
                </div>
                <span style={{ fontFamily: 'system-ui, sans-serif', fontWeight: 900, fontSize: 28, color: '#0F172A' }}>
                  {beatIndex === 9 ? '¡WATERS! 🌊' : 'HYDROGEN'}
                </span>
              </div>
              <div style={{ width: 42, height: 42, borderRadius: 999, background: '#22C55E', color: '#FFFFFF', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 900, fontSize: 22 }}>
                ✓
              </div>
            </div>
          </PopBox>
        )}
      </div>
    </PopBox>
  );
};

export const WatersNeon3DEpisode: React.FC<Neon3DEpisodeProps> = ({
  episodeLabel,
  beats,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  let acc = 0;
  let activeBeat = beats[0];
  let beatIndex = 0;
  let localFrame = 0;
  for (let i = 0; i < beats.length; i++) {
    const b = beats[i];
    if (frame >= acc && frame < acc + b.durationInFrames) {
      activeBeat = b;
      beatIndex = i;
      localFrame = frame - acc;
      break;
    }
    acc += b.durationInFrames;
  }

  return (
    <AbsoluteFill style={{ backgroundColor: '#02040A' }}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{ position: [0, 1.68, 11.4], fov: 40 }}
        shadows
      >
        <ChispaScene3D
          beat={activeBeat}
          beatIndex={beatIndex}
          localFrame={localFrame}
        />
      </ThreeCanvas>

      {/* FAINT CODE LOG RAIN + UPPER UI OVERLAYS (0px..845px, completely above 3D stage!) */}
      <FaintTerminalWallpaper localFrame={localFrame} />

      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          padding: '84px 44px 0 44px',
          justifyContent: 'flex-start',
        }}
      >
        <KineticSelectionHeadline
          prefix={activeBeat.headlinePrefix ?? 'Gemini 4 Hydrogen'}
          focus={activeBeat.headlineFocus ?? activeBeat.heroTitle ?? '10X AHORRO'}
          suffix={activeBeat.headlineSuffix ?? ''}
          localFrame={localFrame}
        />

        <NumberedGreenPill
          badge={activeBeat.stepBadge ?? String(beatIndex + 1)}
          text={activeBeat.pillText ?? activeBeat.topTag}
          localFrame={localFrame}
          accentColor={activeBeat.accentColor}
        />

        <TerminalPopWindow
          beat={activeBeat}
          beatIndex={beatIndex}
          localFrame={localFrame}
        />
      </AbsoluteFill>

      {/* SUBTLE EPISODE WATERMARK TOP CORNER */}
      <div
        style={{
          position: 'absolute',
          top: 32,
          right: 40,
          fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
          fontSize: 16,
          fontWeight: 700,
          color: 'rgba(148, 163, 184, 0.55)',
          pointerEvents: 'none',
        }}
      >
        {episodeLabel}
      </div>
    </AbsoluteFill>
  );
};
