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
import { NeonBot3D, NeonExpression } from '../components/NeonBot3D';
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

export interface NeonBeatItem {
  durationInFrames: number;
  topTag: string;
  accentColor: string;
  expression: NeonExpression;
  cardType: NeonCardType;
  heroTitle?: string;
  heroSubtitle?: string;
  speaking?: boolean;
}

export interface Neon3DEpisodeProps {
  episodeLabel: string;
  beats: NeonBeatItem[];
}

const NeonParticles: React.FC<{ frame: number; accentColor: string }> = ({
  frame,
  accentColor,
}) => {
  const stars = useMemo(() => {
    const arr: { pos: [number, number, number]; size: number; alt: boolean }[] = [];
    for (let i = 0; i < 85; i++) {
      const s1 = Math.sin(i * 19.31) * 43758.5453;
      const s2 = Math.sin(i * 73.17) * 43758.5453;
      const s3 = Math.sin(i * 41.89) * 43758.5453;
      arr.push({
        pos: [
          (s1 - Math.floor(s1) - 0.5) * 16,
          (s2 - Math.floor(s2) - 0.5) * 20,
          -1.5 - (s3 - Math.floor(s3)) * 12,
        ],
        size: 0.02 + (i % 4) * 0.012,
        alt: i % 3 === 0,
      });
    }
    return arr;
  }, []);

  const drift = (frame * 0.01) % 6;

  return (
    <group position={[0, -drift * 0.2, 0]}>
      {stars.map((s, idx) => (
        <mesh key={idx} position={s.pos}>
          <sphereGeometry args={[s.size, 8, 8]} />
          <meshBasicMaterial color={s.alt ? accentColor : '#94A3B8'} />
        </mesh>
      ))}
    </group>
  );
};

const NeonScene3D: React.FC<{
  beat: NeonBeatItem;
  localFrame: number;
}> = ({ beat, localFrame }) => {
  const globalFrame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { camera } = useThree();
  const t = globalFrame / fps;

  const isHeroCenter =
    beat.cardType === 'alert_intro' || beat.cardType === 'cta_wink';

  const camX = isHeroCenter
    ? Math.sin(t * 1.1) * 0.4 +
      (beat.expression === 'shock' && localFrame < 14
        ? Math.sin(localFrame * 3.1) * 0.1
        : 0)
    : Math.sin(t * 0.85) * 0.65;
  const camY = isHeroCenter ? 0.45 : -0.25;
  const camZ = isHeroCenter
    ? interpolate(localFrame, [0, 18], [8.2, 6.8], { extrapolateRight: 'clamp' })
    : 8.7;
  const targetY = isHeroCenter ? -0.32 : -1.2;

  camera.position.set(camX, camY, camZ);
  camera.lookAt(new THREE.Vector3(0, targetY, 0));

  return (
    <>
      <color attach="background" args={['#020308']} />
      <fog attach="fog" args={['#020308', 9, 22]} />

      <ambientLight intensity={0.95} />
      <directionalLight position={[4, 7, 6]} intensity={2.3} color="#FFFFFF" />
      <directionalLight position={[-5, 4, 2]} intensity={2.2} color={beat.accentColor} />
      <directionalLight position={[5, -2, -3]} intensity={1.8} color="#38BDF8" />
      <pointLight position={[0, 1.8, 3.6]} intensity={2.8} color={beat.accentColor} />

      <NeonParticles frame={globalFrame} accentColor={beat.accentColor} />

      <gridHelper
        args={[20, 24, beat.accentColor, '#0A1020']}
        position={[0, -1.65, 0]}
      />

      <NeonBot3D
        frame={globalFrame}
        fps={fps}
        expression={beat.expression}
        accentColor={beat.accentColor}
        speaking={beat.speaking ?? true}
        scale={isHeroCenter ? 1.05 : 0.96}
      />

      {beat.expression === 'shock' &&
        [0, 1, 2].map((i) => {
          const p = ((localFrame + i * 20) % 60) / 60;
          const s = 0.85 + p * 2.5;
          return (
            <mesh key={i} position={[0, 0.55, -0.45]} scale={[s, s, 1]}>
              <torusGeometry args={[1, 0.025, 12, 48]} />
              <meshBasicMaterial
                color={beat.accentColor}
                transparent
                opacity={(1 - p) * 0.85}
              />
            </mesh>
          );
        })}
    </>
  );
};

const CardShell: React.FC<{
  accentColor: string;
  headerRight: string;
  title: string;
  children: React.ReactNode;
}> = ({ accentColor, headerRight, title, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame, fps, config: { damping: 14, stiffness: 120 } });

  return (
    <div
      style={{
        width: '100%',
        transform: `scale(${interpolate(pop, [0, 1], [0.92, 1])})`,
        background: 'rgba(4, 7, 16, 0.88)',
        border: `3px solid ${accentColor}`,
        borderRadius: 32,
        padding: '28px 32px',
        boxShadow: `0 24px 70px rgba(0,0,0,0.9), 0 0 42px ${accentColor}44`,
      }}
    >
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          borderBottom: `2px solid ${accentColor}44`,
          paddingBottom: 14,
          marginBottom: 20,
        }}
      >
        <div style={{ display: 'flex', gap: 10 }}>
          <div style={{ width: 14, height: 14, borderRadius: 99, background: '#FF5F56' }} />
          <div style={{ width: 14, height: 14, borderRadius: 99, background: '#FFBD2E' }} />
          <div style={{ width: 14, height: 14, borderRadius: 99, background: '#27C93F' }} />
        </div>
        <span
          style={{
            fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: accentColor,
            letterSpacing: 1.1,
          }}
        >
          {headerRight}
        </span>
      </div>
      <div
        style={{
          fontFamily: 'system-ui, -apple-system, sans-serif',
          fontWeight: 900,
          fontSize: 44,
          lineHeight: 1.1,
          color: '#FFFFFF',
          marginBottom: 22,
          textShadow: `0 0 22px ${accentColor}55`,
        }}
      >
        {title}
      </div>
      {children}
    </div>
  );
};

const VsDuelCard: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const progress = interpolate(localFrame, [4, 52], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const fableCost = (19.0 * progress).toFixed(2);
  const hydroCost = (1.5 * progress).toFixed(2);
  const fableMin = Math.round(45 * progress);
  const hydroMin = Math.round(12 * progress);

  return (
    <CardShell
      accentColor="#00F5D4"
      headerRight="DUELO · MISMA ANIMACIÓN 3D"
      title="MISMO VIDEO... FRACCIÓN DE PRECIO"
    >
      <div style={{ display: 'flex', gap: 18, marginBottom: 20 }}>
        {/* Fable 5.2 Card */}
        <div
          style={{
            flex: 1,
            background: '#0A0D16',
            border: '2px solid #D97757',
            borderRadius: 22,
            padding: 20,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14 }}>
            <ClaudeStarburstLogo size={42} />
            <div>
              <div style={{ color: '#D97757', fontWeight: 900, fontSize: 22, fontFamily: 'system-ui, sans-serif' }}>
                FABLE 5.2
              </div>
              <div style={{ color: '#94A3B8', fontSize: 16, fontFamily: 'ui-monospace, monospace' }}>
                Anthropic API
              </div>
            </div>
          </div>
          <div style={{ fontFamily: 'ui-monospace, monospace', fontWeight: 900, fontSize: 52, color: '#FF4D4D', fontVariantNumeric: 'tabular-nums' }}>
            ${fableCost}
          </div>
          <div style={{ color: '#CBD5E1', fontSize: 22, fontWeight: 700, marginTop: 6, fontFamily: 'ui-monospace, monospace' }}>
            ⏱ +{fableMin} MINUTOS
          </div>
          <div style={{ height: 12, background: '#1E293B', borderRadius: 99, marginTop: 12, overflow: 'hidden' }}>
            <div style={{ width: `${Math.round(progress * 100)}%`, height: '100%', background: '#FF4D4D' }} />
          </div>
          <div style={{ color: '#94A3B8', fontSize: 16, marginTop: 12, fontFamily: 'ui-monospace, monospace' }}>
            API: $10 IN / $50 OUT
          </div>
        </div>

        {/* Gemini 4 Hydrogen Card */}
        <div
          style={{
            flex: 1,
            background: '#05151C',
            border: '3px solid #00F5D4',
            borderRadius: 22,
            padding: 20,
            boxShadow: '0 0 28px rgba(0, 245, 212, 0.25)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14 }}>
            <GeminiSparkleLogo size={42} />
            <div>
              <div style={{ color: '#00F5D4', fontWeight: 900, fontSize: 22, fontFamily: 'system-ui, sans-serif' }}>
                GEMINI 4 HYDRO
              </div>
              <div style={{ color: '#7DD3FC', fontSize: 16, fontFamily: 'ui-monospace, monospace' }}>
                Google AI / Gratis
              </div>
            </div>
          </div>
          <div style={{ fontFamily: 'ui-monospace, monospace', fontWeight: 900, fontSize: 52, color: '#22C55E', fontVariantNumeric: 'tabular-nums' }}>
            ${hydroCost}
          </div>
          <div style={{ color: '#E2E8F0', fontSize: 22, fontWeight: 700, marginTop: 6, fontFamily: 'ui-monospace, monospace' }}>
            ⚡ {hydroMin} MINUTOS
          </div>
          <div style={{ height: 12, background: '#1E293B', borderRadius: 99, marginTop: 12, overflow: 'hidden' }}>
            <div style={{ width: `${Math.round(progress * 27)}%`, height: '100%', background: '#22C55E' }} />
          </div>
          <div style={{ color: '#7DD3FC', fontSize: 16, marginTop: 12, fontFamily: 'ui-monospace, monospace' }}>
            API: $1.50 / $7.50 (o $0)
          </div>
        </div>
      </div>

      <div
        style={{
          background: 'linear-gradient(90deg, #00F5D4 0%, #22C55E 100%)',
          color: '#020308',
          borderRadius: 18,
          padding: '16px 20px',
          textAlign: 'center',
          fontFamily: 'system-ui, sans-serif',
          fontWeight: 900,
          fontSize: 30,
        }}
      >
        🚀 10X MÁS BARATO · 3.75X MÁS RÁPIDO
      </div>
    </CardShell>
  );
};

const BenchRaceCard: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const benchVal = interpolate(localFrame, [4, 58], [18.2, 57.0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  }).toFixed(1);

  return (
    <CardShell
      accentColor="#38BDF8"
      headerRight="TERMINAL BENCH 4.1 · TOP #5"
      title="SALTO DE 18.2% A 57.0% EN CÓDIGO"
    >
      <div
        style={{
          background: '#050A14',
          border: '2px solid #38BDF8',
          borderRadius: 20,
          padding: '18px 22px',
          marginBottom: 18,
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <GeminiSparkleLogo size={38} />
            <span style={{ color: '#FFFFFF', fontWeight: 900, fontSize: 28, fontFamily: 'system-ui, sans-serif' }}>
              GEMINI 4 HYDROGEN
            </span>
          </div>
          <span style={{ color: '#00F5D4', fontWeight: 900, fontSize: 48, fontFamily: 'ui-monospace, monospace', fontVariantNumeric: 'tabular-nums' }}>
            {benchVal}%
          </span>
        </div>
        <div style={{ height: 18, borderRadius: 99, background: '#1E293B', overflow: 'hidden' }}>
          <div
            style={{
              width: `${benchVal}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #38BDF8 0%, #00F5D4 100%)',
            }}
          />
        </div>
        <div style={{ color: '#94A3B8', fontSize: 18, marginTop: 10, fontFamily: 'ui-monospace, monospace' }}>
          Anterior 3.8 Flash: 18.2% ➔ 2.5x más veloz · Contexto 1M
        </div>
      </div>

      <div style={{ display: 'flex', gap: 12 }}>
        <div style={{ flex: 1, background: '#090D18', border: '2px solid #D97757', borderRadius: 16, padding: 14, display: 'flex', alignItems: 'center', gap: 10 }}>
          <ClaudeStarburstLogo size={32} />
          <div>
            <div style={{ color: '#FFFFFF', fontWeight: 800, fontSize: 18, fontFamily: 'system-ui, sans-serif' }}>Fable 5.1</div>
            <div style={{ color: '#D97757', fontSize: 15, fontFamily: 'ui-monospace, monospace' }}>SUPERADO ✓</div>
          </div>
        </div>
        <div style={{ flex: 1, background: '#090D18', border: '2px solid #10A37F', borderRadius: 16, padding: 14, display: 'flex', alignItems: 'center', gap: 10 }}>
          <OpenAILogo size={32} />
          <div>
            <div style={{ color: '#FFFFFF', fontWeight: 800, fontSize: 18, fontFamily: 'system-ui, sans-serif' }}>GPT Astra 6</div>
            <div style={{ color: '#10A37F', fontSize: 15, fontFamily: 'ui-monospace, monospace' }}>SUPERADO ✓</div>
          </div>
        </div>
        <div style={{ flex: 1, background: '#090D18', border: '2px solid #DFB15B', borderRadius: 16, padding: 14, display: 'flex', alignItems: 'center', gap: 10 }}>
          <GeminiSparkleLogo size={32} />
          <div>
            <div style={{ color: '#FFFFFF', fontWeight: 800, fontSize: 18, fontFamily: 'system-ui, sans-serif' }}>4 Argon</div>
            <div style={{ color: '#DFB15B', fontSize: 15, fontFamily: 'ui-monospace, monospace' }}>SUPERADO ✓</div>
          </div>
        </div>
      </div>
    </CardShell>
  );
};

const GtaBuildCard: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const minVal = Math.round(
    interpolate(localFrame, [4, 52], [0, 10], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
  );
  return (
    <CardShell
      accentColor="#DFB15B"
      headerRight="GOOGLE AI STUDIO · MODO MAX"
      title="CLON 3D DE GTA 6 EN 10 MINUTOS"
    >
      <div style={{ display: 'flex', gap: 16, marginBottom: 18 }}>
        <div style={{ flex: 1, background: '#14080C', border: '2px solid #FF4D4D', borderRadius: 18, padding: 18 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
            <GeminiSparkleLogo size={30} />
            <span style={{ color: '#FF4D4D', fontWeight: 900, fontSize: 20, fontFamily: 'system-ui, sans-serif' }}>
              gemini.google.com
            </span>
          </div>
          <div style={{ color: '#CBD5E1', fontSize: 20, fontFamily: 'ui-monospace, monospace', lineHeight: 1.45 }}>
            • Nivel Bajo por defecto
            <br />• Mapa vacío ❌
            <br />• Sin coches ni aviones
          </div>
        </div>

        <div style={{ flex: 1, background: '#0B1610', border: '2px solid #DFB15B', borderRadius: 18, padding: 18 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
            <GoogleGLogo size={30} />
            <span style={{ color: '#DFB15B', fontWeight: 900, fontSize: 20, fontFamily: 'system-ui, sans-serif' }}>
              AI Studio · EXTRA ALTO
            </span>
          </div>
          <div style={{ color: '#FFFFFF', fontSize: 20, fontFamily: 'ui-monospace, monospace', lineHeight: 1.45 }}>
            • Modo MAX activado ✅
            <br />• Motos, aviones, barcos
            <br />• Grúas + 1ra persona
          </div>
        </div>
      </div>

      <div style={{ background: '#040710', border: '2px solid #DFB15B88', borderRadius: 18, padding: '14px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ color: '#CBD5E1', fontWeight: 800, fontSize: 22, fontFamily: 'ui-monospace, monospace' }}>
          ANTES: 30-40 MIN ➔ AHORA:
        </span>
        <span style={{ color: '#DFB15B', fontWeight: 900, fontSize: 40, fontFamily: 'ui-monospace, monospace' }}>
          {minVal} MIN ⚡
        </span>
      </div>
    </CardShell>
  );
};

const ThreeSecretsCard: React.FC = () => (
  <CardShell
    accentColor="#22C55E"
    headerRight="ZERO CUOTA · ECOSISTEMA GOOGLE"
    title="3 TRUCOS PARA USARLO GRATIS"
  >
    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, background: '#051510', border: '2px solid #22C55E', borderRadius: 18, padding: '16px 20px' }}>
        <GoogleGLogo size={40} />
        <div>
          <div style={{ color: '#22C55E', fontWeight: 900, fontSize: 24, fontFamily: 'system-ui, sans-serif' }}>
            1. google.com ➔ Pestaña MODO IA
          </div>
          <div style={{ color: '#FFFFFF', fontSize: 20, fontFamily: 'ui-monospace, monospace' }}>
            ¡Ya usa Gemini 4 Hydrogen ILIMITADO! (Sin freno 5h/semanal)
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 16, background: '#070F1C', border: '2px solid #38BDF8', borderRadius: 18, padding: '16px 20px' }}>
        <GeminiSparkleLogo size={40} />
        <div>
          <div style={{ color: '#38BDF8', fontWeight: 900, fontSize: 24, fontFamily: 'system-ui, sans-serif' }}>
            2. aistudio.google.com ➔ MODO MAX
          </div>
          <div style={{ color: '#E2E8F0', fontSize: 20, fontFamily: 'ui-monospace, monospace' }}>
            Desbloquea 4to nivel: Razonamiento Extra Alto (xhigh)
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 16, background: '#0F0D18', border: '2px solid #A855F7', borderRadius: 18, padding: '16px 20px' }}>
        <TerminalHarnessLogo size={40} />
        <div>
          <div style={{ color: '#C084FC', fontWeight: 900, fontSize: 24, fontFamily: 'system-ui, sans-serif' }}>
            3. API Gratis (5 RPM / 250K TPM / 20 RPD)
          </div>
          <div style={{ color: '#E2E8F0', fontSize: 20, fontFamily: 'ui-monospace, monospace' }}>
            ID oculto en agentes: gemini-4-hydrogen
          </div>
        </div>
      </div>
    </div>
  </CardShell>
);

export const WatersNeon3DEpisode: React.FC<Neon3DEpisodeProps> = ({
  episodeLabel,
  beats,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  let acc = 0;
  let activeBeat = beats[0];
  let localFrame = 0;
  for (const b of beats) {
    if (frame >= acc && frame < acc + b.durationInFrames) {
      activeBeat = b;
      localFrame = frame - acc;
      break;
    }
    acc += b.durationInFrames;
  }

  return (
    <AbsoluteFill style={{ backgroundColor: '#020308' }}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{ position: [0, 0.35, 4.4], fov: 42 }}
      >
        <NeonScene3D beat={activeBeat} localFrame={localFrame} />
      </ThreeCanvas>

      {/* TOP HUD PILL */}
      <AbsoluteFill style={{ pointerEvents: 'none', padding: '56px 40px' }}>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            background: 'rgba(2, 3, 8, 0.82)',
            border: `2px solid ${activeBeat.accentColor}`,
            borderRadius: 999,
            padding: '14px 26px',
            boxShadow: `0 0 28px ${activeBeat.accentColor}55`,
          }}
        >
          <span
            style={{
              fontFamily: 'system-ui, -apple-system, sans-serif',
              fontWeight: 900,
              fontSize: 24,
              color: '#FFFFFF',
              letterSpacing: 1.1,
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

      {/* MIDDLE HOLOGRAPHIC OVERLAY ZONE (leaves top for 3D bot & bottom 260px clean for Captions) */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          justifyContent: 'flex-end',
          alignItems: 'center',
          padding: '0 44px 260px 44px',
        }}
      >
        {(activeBeat.cardType === 'alert_intro' || activeBeat.cardType === 'cta_wink') &&
          activeBeat.heroTitle && (
            <div
              style={{
                width: '100%',
                background: 'rgba(2, 3, 8, 0.88)',
                border: `3px solid ${activeBeat.accentColor}`,
                borderRadius: 28,
                padding: '24px 32px',
                textAlign: 'center',
                boxShadow: `0 0 42px ${activeBeat.accentColor}55`,
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 18, marginBottom: 10 }}>
                <ClaudeStarburstLogo size={46} />
                <span style={{ color: '#94A3B8', fontSize: 28, fontWeight: 900, fontFamily: 'system-ui, sans-serif' }}>VS</span>
                <GeminiSparkleLogo size={46} />
              </div>
              <div
                style={{
                  fontFamily: 'system-ui, -apple-system, sans-serif',
                  fontWeight: 900,
                  fontSize: 48,
                  color: activeBeat.accentColor,
                  lineHeight: 1.1,
                }}
              >
                {activeBeat.heroTitle}
              </div>
              {activeBeat.heroSubtitle && (
                <div
                  style={{
                    fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
                    fontWeight: 800,
                    fontSize: 24,
                    color: '#FFFFFF',
                    marginTop: 8,
                  }}
                >
                  {activeBeat.heroSubtitle}
                </div>
              )}
            </div>
          )}

        {activeBeat.cardType === 'vs_duel' && <VsDuelCard localFrame={localFrame} />}
        {activeBeat.cardType === 'bench_race' && <BenchRaceCard localFrame={localFrame} />}
        {activeBeat.cardType === 'gta6_build' && <GtaBuildCard localFrame={localFrame} />}
        {activeBeat.cardType === 'three_secrets' && <ThreeSecretsCard />}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
