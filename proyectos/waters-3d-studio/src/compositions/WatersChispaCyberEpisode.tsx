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
  EvilTerminatorBot3D,
  GoldenKitBox3D,
  ShieldVault3D,
  SilverLaptop3D,
  StudioFloor3D,
  VoiceWaveClone3D,
} from '../components/ChispaStageProps3D';
import {
  BankShieldIcon,
  GovLeakBadge,
  MastercardCircles,
  TerminatorEyeIcon,
  VisaWordmark,
  VoiceWaveIcon,
} from '../components/BrandLogos';

export type CyberCardType =
  | 'cyber_hook'
  | 'breach_evidence'
  | 'voice_clone_trap'
  | 'giro_punch'
  | 'three_shields'
  | 'terminator_cameo'
  | 'step_single'
  | 'chaos_bridge'
  | 'cta_blinda';

export type CyberStageProp =
  | 'none'
  | 'laptop'
  | 'voice_wave'
  | 'terminator'
  | 'shield_vault'
  | 'kit_box';

export interface CyberBeatItem {
  durationInFrames: number;
  topTag: string;
  accentColor: string;
  expression: ChispaExpression;
  cardType: CyberCardType;
  stageProp: CyberStageProp;
  stepBadge: string;
  pillText: string;
  headlinePrefix: string;
  headlineFocus: string;
  headlineSuffix?: string;
  terminalCmd: string;
  terminalSub: string;
  stepTitle?: string;
  stepDetail?: string;
  pops?: number[];
  speaking?: boolean;
}

export interface CyberEpisodeProps {
  episodeLabel: string;
  beats: CyberBeatItem[];
}

const DEFAULT_POPS = [2, 8, 20, 32];

const CyberBackdropDots: React.FC<{ frame: number; accentColor: string }> = ({
  frame,
  accentColor,
}) => {
  const dots = useMemo(() => {
    const arr: { pos: [number, number, number]; size: number; alt: boolean }[] = [];
    for (let i = 0; i < 36; i++) {
      const s1 = Math.sin(i * 17.71) * 43758.5453;
      const s2 = Math.sin(i * 53.33) * 43758.5453;
      const s3 = Math.sin(i * 19.91) * 43758.5453;
      arr.push({
        pos: [
          (s1 - Math.floor(s1) - 0.5) * 9,
          (s2 - Math.floor(s2)) * 5.6 - 0.3,
          -2.4 - (s3 - Math.floor(s3)) * 4.5,
        ],
        size: 0.018 + (i % 3) * 0.01,
        alt: i % 3 === 0,
      });
    }
    return arr;
  }, []);

  const drift = ((frame * 0.008) % 2) - 1;

  return (
    <group position={[0, drift * 0.22, 0]}>
      {dots.map((d, i) => (
        <mesh key={i} position={d.pos}>
          <sphereGeometry args={[d.size, 8, 8]} />
          <meshBasicMaterial
            color={d.alt ? '#FF3B3B' : accentColor}
            transparent
            opacity={0.48}
          />
        </mesh>
      ))}
    </group>
  );
};

const CyberScene3D: React.FC<{
  beat: CyberBeatItem;
  localFrame: number;
}> = ({ beat, localFrame }) => {
  const globalFrame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { camera } = useThree();
  const t = globalFrame / fps;

  const isTerminator = beat.stageProp === 'terminator';
  const isHeroCenter = beat.stageProp === 'none';

  const shockShake =
    (beat.expression === 'shock_sweat' || isTerminator) && localFrame < 12
      ? Math.sin(localFrame * 3.4) * 0.075
      : 0;
  const camX = Math.sin(t * 0.72) * 0.22 + shockShake;
  const camY = 1.50;
  const camZ = 10.15;
  camera.position.set(camX, camY, camZ);
  camera.lookAt(new THREE.Vector3(0, 1.15, 0));

  const floorColor = isTerminator
    ? '#23161C'
    : beat.stageProp === 'kit_box'
    ? '#3D2B22'
    : '#212735';

  let charX = 0;
  let charRotY = 0;
  if (beat.stageProp === 'kit_box') {
    charX = 0.84;
    charRotY = -0.22;
  } else if (beat.stageProp === 'terminator') {
    charX = -0.96;
    charRotY = 0.26;
  } else if (!isHeroCenter) {
    charX = -0.90;
    charRotY = 0.24;
  }

  const charY = -0.22; // boots sit right on floorY = -1.05
  const jumpHeight = Math.abs(Math.sin(t * 4.8)) * 0.08;
  const popFrames = beat.pops ?? DEFAULT_POPS;

  return (
    <>
      <color attach="background" args={['#02040A']} />
      <fog attach="fog" args={['#02040A', 13, 26]} />

      <ambientLight intensity={1.05} />
      <directionalLight position={[4, 8, 6]} intensity={2.2} color="#FFFDF7" castShadow />
      <directionalLight position={[-5, 5, 3]} intensity={1.65} color="#93C5FD" />
      <pointLight
        position={[isTerminator ? 1.1 : 0, 1.4, 4.4]}
        intensity={isTerminator ? 2.6 : 1.9}
        color={isTerminator ? '#FF2E3B' : beat.accentColor}
      />

      <CyberBackdropDots frame={globalFrame} accentColor={beat.accentColor} />

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
        expression={beat.expression}
        accentColor={beat.accentColor}
        position={[charX, charY, 0.15]}
        rotationY={charRotY}
        scale={1.0}
        speaking={beat.speaking ?? true}
        popFrames={popFrames}
      />

      {beat.stageProp === 'laptop' && (
        <SilverLaptop3D
          frame={globalFrame}
          localFrame={localFrame}
          fps={fps}
          position={[0.88, -1.04, -0.05]}
          rotationY={-0.38}
          scale={0.92}
          accentColor={beat.accentColor}
        />
      )}

      {beat.stageProp === 'voice_wave' && (
        <VoiceWaveClone3D
          frame={globalFrame}
          localFrame={localFrame}
          fps={fps}
          position={[0.92, -0.32, -0.04]}
          scale={0.94}
        />
      )}

      {beat.stageProp === 'terminator' && (
        <EvilTerminatorBot3D
          frame={globalFrame}
          localFrame={localFrame}
          fps={fps}
          position={[0.98, -0.22, 0.08]}
          rotationY={-0.32}
          scale={0.94}
          blocked={true}
        />
      )}

      {beat.stageProp === 'shield_vault' && (
        <ShieldVault3D
          frame={globalFrame}
          localFrame={localFrame}
          fps={fps}
          position={[0.92, -0.28, -0.04]}
          accentColor={beat.accentColor}
        />
      )}

      {beat.stageProp === 'kit_box' && (
        <GoldenKitBox3D
          frame={globalFrame}
          localFrame={localFrame}
          fps={fps}
          position={[-0.86, -0.57, -0.04]}
        />
      )}
    </>
  );
};

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
          transform: 'scale(0.65) translateY(10px)',
        }}
      >
        {children}
      </div>
    );
  }
  const s = spring({
    frame: localFrame - popFrame,
    fps,
    config: { damping: 10, stiffness: 270, mass: 0.7 },
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

const FaintCyberLogs: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const scroll = (localFrame * 1.35) % 88;
  return (
    <div
      style={{
        position: 'absolute',
        top: -scroll,
        left: 28,
        right: 28,
        height: 820,
        overflow: 'hidden',
        opacity: 0.11,
        fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
        fontSize: 22,
        lineHeight: 1.65,
        color: '#00F5D4',
        pointerEvents: 'none',
        userSelect: 'none',
      }}
    >
      <div>[ALERT] IMSS_PENSIONADOS_2025: 20,000,000 records</div>
      <div>&gt; SAT_INE_DUMP: 150 GB · n0n_vendor: JPMorgan · Visa</div>
      <div>[!] Voice Clone Risk: 3.2s audio sample -&gt; spoof=99.4%</div>
      <div>&gt; trap_question(&quot;clave_familiar&quot;) == FAIL -&gt; HANGUP()</div>
      <div>✓ Token App + NIP activo | Biometria Pasiva = OFF</div>
      <div>uses · protocolo_blinda · 10_puntos_verificados</div>
    </div>
  );
};

const KineticHeadline: React.FC<{
  prefix: string;
  focus: string;
  suffix?: string;
  localFrame: number;
  highlightColor?: string;
}> = ({ prefix, focus, suffix = '', localFrame, highlightColor = '#3B82F6' }) => {
  const { fps } = useVideoConfig();
  const fullPrefix = typedSlice(prefix, localFrame, 0, 5).shown;
  const showFocus = localFrame >= 4;
  const focusPop = showFocus
    ? spring({
        frame: localFrame - 4,
        fps,
        config: { damping: 11, stiffness: 260 },
      })
    : 0;

  return (
    <div
      style={{
        textAlign: 'center',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
        fontSize: 42,
        fontWeight: 800,
        lineHeight: 1.24,
        color: '#CBD5E1',
        letterSpacing: -0.6,
        marginBottom: 16,
        minHeight: 68,
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
            border: `2.5px solid ${highlightColor}`,
            boxShadow: `0 0 18px ${highlightColor}77`,
            transform: `scale(${focusPop})`,
          }}
        >
          {focus}
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
                border: '1px solid #0F172A',
                ...pos,
              }}
            />
          ))}
        </span>
      )}
      {localFrame >= 9 && suffix && <span> {suffix}</span>}
    </div>
  );
};

const CyberStepPill: React.FC<{
  badge: string;
  text: string;
  localFrame: number;
  isDanger?: boolean;
}> = ({ badge, text, localFrame, isDanger = false }) => {
  const pillColor = isDanger ? '#FF3B3B' : '#00F5D4';
  const bg = isDanger ? 'rgba(26, 6, 10, 0.94)' : 'rgba(4, 18, 18, 0.94)';
  return (
    <PopBox
      localFrame={localFrame}
      popFrame={2}
      style={{ display: 'flex', justifyContent: 'center', marginBottom: 14 }}
    >
      <div
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: 12,
          background: bg,
          border: `2.5px solid ${pillColor}`,
          borderRadius: 999,
          padding: '8px 24px 8px 10px',
          boxShadow: `0 0 24px ${pillColor}55`,
        }}
      >
        <div
          style={{
            width: 38,
            height: 38,
            borderRadius: 999,
            background: pillColor,
            color: '#030808',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontFamily: 'system-ui, sans-serif',
            fontWeight: 900,
            fontSize: 21,
          }}
        >
          {badge}
        </div>
        <span
          style={{
            fontFamily: 'system-ui, -apple-system, sans-serif',
            fontWeight: 800,
            fontSize: 27,
            color: '#FFFFFF',
            letterSpacing: -0.3,
          }}
        >
          {text}
        </span>
      </div>
    </PopBox>
  );
};

const CyberTerminalCard: React.FC<{
  beat: CyberBeatItem;
  localFrame: number;
}> = ({ beat, localFrame }) => {
  const pops = beat.pops ?? DEFAULT_POPS;
  const cmdEnd = beat.cardType === 'terminator_cameo' ? 24 : 30;
  const subStart = pops[2] ?? 20;
  const subEnd = Math.max(subStart + 16, (pops[3] ?? 32) + 8);

  const cmdState = typedSlice(beat.terminalCmd, localFrame, 8, cmdEnd);
  const subState = typedSlice(beat.terminalSub, localFrame, subStart, subEnd);
  const cursorVisible = Math.floor(localFrame / 5) % 2 === 0;
  const isDanger = beat.accentColor === '#FF3B3B';

  return (
    <PopBox localFrame={localFrame} popFrame={8}>
      <div
        style={{
          width: '100%',
          background: 'rgba(6, 10, 18, 0.94)',
          border: `2.5px solid ${beat.accentColor}`,
          borderRadius: 24,
          padding: '16px 24px 18px 24px',
          boxShadow: `0 22px 60px rgba(0,0,0,0.88), 0 0 34px ${beat.accentColor}38`,
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            paddingBottom: 10,
            marginBottom: 12,
            borderBottom: '1.5px solid rgba(148, 163, 184, 0.22)',
          }}
        >
          <div style={{ display: 'flex', gap: 9 }}>
            <div style={{ width: 12, height: 12, borderRadius: 99, background: '#FF5F56' }} />
            <div style={{ width: 12, height: 12, borderRadius: 99, background: '#FFBD2E' }} />
            <div style={{ width: 12, height: 12, borderRadius: 99, background: '#27C93F' }} />
          </div>
          <span
            style={{
              fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
              fontSize: 17,
              color: isDanger ? '#FCA5A5' : '#94A3B8',
              fontWeight: 700,
            }}
          >
            {beat.topTag}
          </span>
        </div>

        {/* Live Typing Command */}
        <div
          style={{
            fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
            fontSize: 21,
            lineHeight: 1.42,
            marginBottom: 14,
            minHeight: 62,
          }}
        >
          <div style={{ color: isDanger ? '#FF6B6B' : '#00F5D4', fontWeight: 700 }}>
            {cmdState.shown}
            {(cmdState.isTyping || (!subState.shown && cursorVisible)) && (
              <span style={{ color: '#FFFFFF', marginLeft: 3 }}>▋</span>
            )}
          </div>
          {localFrame >= subStart && (
            <div style={{ color: '#E2E8F0', fontWeight: 600, marginTop: 4 }}>
              {subState.shown}
              {(subState.isTyping || cursorVisible) && (
                <span style={{ color: beat.accentColor, marginLeft: 3 }}>▋</span>
              )}
            </div>
          )}
        </div>

        {/* SUB-CARDS BY BEAT TYPE */}
        {beat.cardType === 'cyber_hook' && (
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            <PopBox localFrame={localFrame} popFrame={pops[2] ?? 20} style={{ flex: 1 }}>
              <div style={{ background: '#0B1220', border: '2px solid #00F5D4', borderRadius: 16, padding: '10px 14px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ color: '#FFFFFF', fontWeight: 900, fontSize: 19, fontFamily: 'system-ui, sans-serif' }}>JPMorgan</span>
                <VisaWordmark size={30} />
                <MastercardCircles size={28} />
              </div>
            </PopBox>
            <PopBox localFrame={localFrame} popFrame={pops[3] ?? 32} style={{ flex: 0.72 }}>
              <div style={{ background: '#1F090E', border: '2px solid #FF3B3B', borderRadius: 16, padding: '10px 14px', textAlign: 'center' }}>
                <div style={{ color: '#FF3B3B', fontWeight: 900, fontSize: 21, fontFamily: 'system-ui, sans-serif' }}>+10 HACKEOS</div>
                <div style={{ color: '#FCA5A5', fontSize: 15, fontFamily: 'ui-monospace, monospace' }}>IMSS · SAT · INE</div>
              </div>
            </PopBox>
          </div>
        )}

        {beat.cardType === 'breach_evidence' && (
          <div style={{ display: 'flex', gap: 10 }}>
            <PopBox localFrame={localFrame} popFrame={pops[2] ?? 20} style={{ flex: 1 }}>
              <div style={{ background: '#1A080C', border: '2px solid #FF3B3B', borderRadius: 14, padding: '10px 12px', display: 'flex', alignItems: 'center', gap: 10 }}>
                <GovLeakBadge size={34} />
                <div>
                  <div style={{ color: '#FFFFFF', fontWeight: 900, fontSize: 18, fontFamily: 'system-ui, sans-serif' }}>IMSS · 20M</div>
                  <div style={{ color: '#FCA5A5', fontSize: 15, fontFamily: 'ui-monospace, monospace' }}>CURP, NSS y Salud</div>
                </div>
              </div>
            </PopBox>
            <PopBox localFrame={localFrame} popFrame={pops[3] ?? 32} style={{ flex: 1 }}>
              <div style={{ background: '#1A080C', border: '2px solid #FF3B3B', borderRadius: 14, padding: '10px 12px' }}>
                <div style={{ color: '#FF3B3B', fontWeight: 900, fontSize: 18, fontFamily: 'system-ui, sans-serif' }}>SAT &amp; INE · 150 GB</div>
                <div style={{ color: '#E2E8F0', fontSize: 15, fontFamily: 'ui-monospace, monospace' }}>+ Teléfono Presidencial</div>
              </div>
            </PopBox>
          </div>
        )}

        {beat.cardType === 'voice_clone_trap' && (
          <div style={{ display: 'flex', gap: 12 }}>
            <PopBox localFrame={localFrame} popFrame={pops[2] ?? 20} style={{ flex: 1 }}>
              <div style={{ background: '#07171B', border: '2px solid #00F5D4', borderRadius: 14, padding: '10px 14px', display: 'flex', alignItems: 'center', gap: 10 }}>
                <BankShieldIcon size={34} />
                <div>
                  <div style={{ color: '#00F5D4', fontWeight: 900, fontSize: 18, fontFamily: 'system-ui, sans-serif' }}>Banco: Biometría Voz</div>
                  <div style={{ color: '#CBD5E1', fontSize: 15, fontFamily: 'ui-monospace, monospace' }}>Riesgo: Llave única</div>
                </div>
              </div>
            </PopBox>
            <PopBox localFrame={localFrame} popFrame={pops[3] ?? 32} style={{ flex: 1 }}>
              <div style={{ background: '#1D080D', border: '2.5px solid #FF3B3B', borderRadius: 14, padding: '10px 14px', display: 'flex', alignItems: 'center', gap: 10 }}>
                <VoiceWaveIcon size={34} />
                <div>
                  <div style={{ color: '#FF3B3B', fontWeight: 900, fontSize: 18, fontFamily: 'system-ui, sans-serif' }}>ElevenLabs / IA</div>
                  <div style={{ color: '#FFFFFF', fontSize: 15, fontFamily: 'ui-monospace, monospace' }}>Clona en 3–10 seg</div>
                </div>
              </div>
            </PopBox>
          </div>
        )}

        {beat.cardType === 'giro_punch' && (
          <PopBox localFrame={localFrame} popFrame={pops[2] ?? 18}>
            <div style={{ background: '#041418', border: '2.5px solid #00F5D4', borderRadius: 16, padding: '14px 18px', textAlign: 'center' }}>
              <div style={{ color: '#FFFFFF', fontWeight: 900, fontSize: 28, fontFamily: 'system-ui, sans-serif' }}>
                IA <span style={{ color: '#FF3B3B' }}>&gt;</span> Ciberseguridad
              </div>
              <div style={{ color: '#00F5D4', fontWeight: 800, fontSize: 20, fontFamily: 'ui-monospace, monospace', marginTop: 4 }}>
                ⚠ Hoy ya NO confíes ni en tu propia voz
              </div>
            </div>
          </PopBox>
        )}

        {beat.cardType === 'three_shields' && (
          <div style={{ display: 'flex', gap: 10 }}>
            {[
              { title: '1. SIN VOZ', sub: 'Exige token', pop: pops[1] ?? 14 },
              { title: '2. CLAVE', sub: 'Trampa T2', pop: pops[2] ?? 24 },
              { title: '3. TU APP', sub: 'Cuelga ya', pop: pops[3] ?? 34 },
            ].map((item, idx) => (
              <PopBox key={idx} localFrame={localFrame} popFrame={item.pop} style={{ flex: 1 }}>
                <div style={{ background: '#061B1A', border: '2px solid #00F5D4', borderRadius: 14, padding: '10px 8px', textAlign: 'center' }}>
                  <div style={{ color: '#00F5D4', fontWeight: 900, fontSize: 18, fontFamily: 'system-ui, sans-serif' }}>{item.title}</div>
                  <div style={{ color: '#FFFFFF', fontSize: 15, fontFamily: 'ui-monospace, monospace', marginTop: 2 }}>{item.sub}</div>
                </div>
              </PopBox>
            ))}
          </div>
        )}

        {beat.cardType === 'terminator_cameo' && (
          <div style={{ display: 'flex', gap: 10 }}>
            <PopBox localFrame={localFrame} popFrame={pops[2] ?? 14} style={{ flex: 1 }}>
              <div style={{ background: '#1A080C', border: '2px solid #FF3B3B', borderRadius: 14, padding: '10px 12px', display: 'flex', alignItems: 'center', gap: 10 }}>
                <TerminatorEyeIcon size={34} />
                <div>
                  <div style={{ color: '#FF6B6B', fontWeight: 900, fontSize: 17, fontFamily: 'system-ui, sans-serif' }}>T-800 Bot IA</div>
                  <div style={{ color: '#FFFFFF', fontSize: 15, fontFamily: 'ui-monospace, monospace' }}>&quot;Falla pregunta trampa&quot;</div>
                </div>
              </div>
            </PopBox>
            <PopBox localFrame={localFrame} popFrame={pops[3] ?? 22} style={{ flex: 1 }}>
              <div style={{ background: '#051B18', border: '2.5px solid #00F5D4', borderRadius: 14, padding: '10px 12px', textAlign: 'center' }}>
                <div style={{ color: '#00F5D4', fontWeight: 900, fontSize: 18, fontFamily: 'system-ui, sans-serif' }}>❌ CLON DETECTADO</div>
                <div style={{ color: '#FFFFFF', fontSize: 16, fontWeight: 800, fontFamily: 'ui-monospace, monospace' }}>☎️ ¡CUELGA EN SECO!</div>
              </div>
            </PopBox>
          </div>
        )}

        {beat.cardType === 'step_single' && (
          <PopBox localFrame={localFrame} popFrame={pops[2] ?? 18}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14, background: '#061B1A', border: '2.5px solid #00F5D4', borderRadius: 16, padding: '12px 18px' }}>
              <BankShieldIcon size={40} />
              <div>
                <div style={{ color: '#00F5D4', fontWeight: 900, fontSize: 23, fontFamily: 'system-ui, sans-serif' }}>
                  {beat.stepTitle ?? 'Acción Inmediata'}
                </div>
                <div style={{ color: '#FFFFFF', fontSize: 18, fontFamily: 'ui-monospace, monospace', marginTop: 2 }}>
                  {beat.stepDetail ?? 'Cierra la puerta antes de la llamada'}
                </div>
              </div>
            </div>
          </PopBox>
        )}

        {beat.cardType === 'chaos_bridge' && (
          <div style={{ display: 'flex', gap: 10 }}>
            {[
              { lbl: 'IMSS · 20M', col: '#FF3B3B', p: pops[2] ?? 16 },
              { lbl: 'SAT/INE · 150GB', col: '#FF3B3B', p: pops[3] ?? 26 },
              { lbl: '+ VOZ IA 10s', col: '#00F5D4', p: pops[4] ?? 36 },
            ].map((chip, ci) => (
              <PopBox key={ci} localFrame={localFrame} popFrame={chip.p} style={{ flex: 1 }}>
                <div style={{ background: '#140A10', border: `2px solid ${chip.col}`, borderRadius: 12, padding: '10px 8px', textAlign: 'center', fontFamily: 'ui-monospace, monospace', fontWeight: 900, fontSize: 17, color: '#FFFFFF' }}>
                  {chip.lbl}
                </div>
              </PopBox>
            ))}
          </div>
        )}

        {beat.cardType === 'cta_blinda' && (
          <PopBox localFrame={localFrame} popFrame={pops[2] ?? 18}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                background: '#FFFFFF',
                borderRadius: 999,
                padding: '10px 16px',
                boxShadow: '0 12px 30px rgba(0,0,0,0.45)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                <div style={{ width: 42, height: 42, borderRadius: 999, background: '#080C17', color: '#00F5D4', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 900, fontSize: 17, fontFamily: 'system-ui, sans-serif' }}>
                  TÚ
                </div>
                <span style={{ fontFamily: 'system-ui, sans-serif', fontWeight: 900, fontSize: 29, color: '#0F172A' }}>
                  {beat.stepTitle ?? 'BLINDA'}
                </span>
              </div>
              <div style={{ width: 42, height: 42, borderRadius: 999, background: '#00C896', color: '#FFFFFF', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 900, fontSize: 22 }}>
                ✓
              </div>
            </div>
          </PopBox>
        )}
      </div>
    </PopBox>
  );
};

export const WatersChispaCyberEpisode: React.FC<CyberEpisodeProps> = ({
  episodeLabel,
  beats,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  let acc = 0;
  let activeBeat = beats[0];
  let localFrame = 0;
  for (let i = 0; i < beats.length; i++) {
    const b = beats[i];
    if (frame >= acc && frame < acc + b.durationInFrames) {
      activeBeat = b;
      localFrame = frame - acc;
      break;
    }
    acc += b.durationInFrames;
  }

  const isDanger = activeBeat.accentColor === '#FF3B3B';

  return (
    <AbsoluteFill style={{ backgroundColor: '#02040A' }}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{ position: [0, 1.50, 10.15], fov: 40 }}
        shadows
      >
        <CyberScene3D beat={activeBeat} localFrame={localFrame} />
      </ThreeCanvas>

      <FaintCyberLogs localFrame={localFrame} />

      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          padding: '84px 44px 0 44px',
          justifyContent: 'flex-start',
        }}
      >
        <KineticHeadline
          prefix={activeBeat.headlinePrefix}
          focus={activeBeat.headlineFocus}
          suffix={activeBeat.headlineSuffix}
          localFrame={localFrame}
          highlightColor={isDanger ? '#FF3B3B' : '#3B82F6'}
        />

        <CyberStepPill
          badge={activeBeat.stepBadge}
          text={activeBeat.pillText}
          localFrame={localFrame}
          isDanger={isDanger}
        />

        <CyberTerminalCard beat={activeBeat} localFrame={localFrame} />
      </AbsoluteFill>

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
