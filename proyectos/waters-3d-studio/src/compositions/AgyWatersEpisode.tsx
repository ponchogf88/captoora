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
import { AgyAstronaut3D, AgyMood } from '../components/AgyAstronaut3D';

interface CaptionCue {
  startFrame: number;
  endFrame: number;
  badge: string;
  line1: string;
  highlight: string;
  accentColor: string;
}

const CAPTION_CUES: CaptionCue[] = [
  {
    startFrame: 0,
    endFrame: 90,
    badge: '🚨 ALERTA MÁXIMA · 0:00',
    line1: '[SUSPIRO] 😱',
    highlight: '¡¡¡WATERS GAMERS!!!',
    accentColor: '#FF4D4D',
  },
  {
    startFrame: 90,
    endFrame: 240,
    badge: '🎮 HOY SALIÓ GTA 6 · 9.8M VIEWS',
    line1: 'TODO MUNDO BUSCA JUGARLO',
    highlight: 'PERO AGUAS CON EL HYPE',
    accentColor: '#38BDF8',
  },
  {
    startFrame: 240,
    endFrame: 390,
    badge: '🤖 VIBE HACKING + IA',
    line1: 'HACKERS USAN CLAUDE PARA',
    highlight: 'INGENIERÍA INVERSA',
    accentColor: '#38BDF8',
  },
  {
    startFrame: 390,
    endFrame: 630,
    badge: '☠️ TRAMPA MORTAL',
    line1: 'LINKS FALSOS Y CRACKS DE GTA 6',
    highlight: 'TRAEN INFOSTEALERS',
    accentColor: '#FF4D4D',
  },
  {
    startFrame: 630,
    endFrame: 870,
    badge: '💸 ROBO EN SEGUNDOS',
    line1: 'SE LLEVAN TUS TARJETAS Y TU',
    highlight: 'CUENTA PSN / XBOX / STEAM',
    accentColor: '#FF4D4D',
  },
  {
    startFrame: 870,
    endFrame: 1050,
    badge: '🛡️ GEMINI 4 NEON · ANTIGRAVITY',
    line1: 'EL NUEVO RAZONAMIENTO NEON',
    highlight: 'BLINDA TUS CUENTAS',
    accentColor: '#DFB15B',
  },
  {
    startFrame: 1050,
    endFrame: 1200,
    badge: '🔐 DEFENSA REAL',
    line1: 'DETECTA LINKS FALSOS, ACTIVA 2FA',
    highlight: 'Y PROTEGE TU PROGRESO',
    accentColor: '#DFB15B',
  },
  {
    startFrame: 1200,
    endFrame: 1440,
    badge: '🚀 CAPTOORA × ANTIGRAVITY',
    line1: '¿QUIERES LA GUÍA DE BLINDAJE?',
    highlight: 'COMENTA: NEON',
    accentColor: '#DFB15B',
  },
];

const StarField: React.FC<{ frame: number }> = ({ frame }) => {
  const stars = useMemo(() => {
    const arr: { pos: [number, number, number]; size: number; color: string }[] = [];
    for (let i = 0; i < 90; i++) {
      // Deterministic pseudo-random distribution
      const s1 = Math.sin(i * 12.9898) * 43758.5453;
      const s2 = Math.sin(i * 78.233) * 43758.5453;
      const s3 = Math.sin(i * 41.123) * 43758.5453;
      const rx = (s1 - Math.floor(s1) - 0.5) * 18;
      const ry = (s2 - Math.floor(s2) - 0.5) * 24;
      const rz = -2 - (s3 - Math.floor(s3)) * 14;
      const colors = ['#FFFFFF', '#38BDF8', '#DFB15B', '#94A3B8'];
      arr.push({
        pos: [rx, ry, rz],
        size: 0.025 + (i % 4) * 0.012,
        color: colors[i % colors.length],
      });
    }
    return arr;
  }, []);

  const driftY = (frame * 0.008) % 6;

  return (
    <group position={[0, -driftY * 0.25, 0]}>
      {stars.map((s, idx) => (
        <mesh key={idx} position={s.pos}>
          <sphereGeometry args={[s.size, 8, 8]} />
          <meshBasicMaterial color={s.color} />
        </mesh>
      ))}
    </group>
  );
};

const SceneContent: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { camera } = useThree();
  const t = frame / fps;

  // Determine mood & scene
  let mood: AgyMood = 'cyan';
  if (frame < 90) mood = 'alert';
  else if (frame < 390) mood = 'cyan';
  else if (frame < 870) mood = 'alert';
  else if (frame < 1200) mood = 'gold';
  else mood = 'wink';

  // Camera choreography per scene
  let camPos: [number, number, number] = [0, 0.4, 4.6];
  let lookTarget: [number, number, number] = [0, 0.3, 0];

  if (frame < 90) {
    // Scene 1: Dramatic zoom-in + subtle shake at 0:00
    const z = interpolate(frame, [0, 20, 90], [6.6, 4.35, 4.55], { extrapolateRight: 'clamp' });
    const shake = frame < 20 ? Math.sin(frame * 3.1) * 0.08 * (1 - frame / 20) : 0;
    camPos = [shake, 0.45 + shake * 0.6, z];
    lookTarget = [0, 0.4, 0];
  } else if (frame < 390) {
    // Scene 2: Smooth 3/4 orbit left-to-right
    const p = (frame - 90) / 300;
    const angle = interpolate(p, [0, 1], [-0.45, 0.35]);
    camPos = [Math.sin(angle) * 5.0, 0.45, Math.cos(angle) * 5.0];
    lookTarget = [0, 0.25, 0];
  } else if (frame < 870) {
    // Scene 3: Urgent tighter push-in with slight dynamic arc
    const p = (frame - 390) / 480;
    const angle = interpolate(p, [0, 1], [0.4, -0.35]);
    const dist = interpolate(p, [0, 0.5, 1], [4.9, 4.3, 4.7]);
    camPos = [Math.sin(angle) * dist, 0.25 + Math.sin(t * 2) * 0.08, Math.cos(angle) * dist];
    lookTarget = [0, 0.3, 0];
  } else if (frame < 1200) {
    // Scene 4: Heroic low-angle looking up slightly at shielded Agy
    const p = (frame - 870) / 330;
    const angle = interpolate(p, [0, 1], [-0.3, 0.25]);
    camPos = [Math.sin(angle) * 5.3, -0.1, Math.cos(angle) * 5.3];
    lookTarget = [0, 0.3, 0];
  } else {
    // Scene 5: Close-up CTA wink
    const p = spring({ frame: frame - 1200, fps, config: { damping: 14, stiffness: 90 } });
    const z = interpolate(p, [0, 1], [4.8, 3.1]);
    camPos = [0.15, 0.75, z];
    lookTarget = [0, 0.75, 0];
  }

  camera.position.set(camPos[0], camPos[1], camPos[2]);
  camera.lookAt(new THREE.Vector3(lookTarget[0], lookTarget[1], lookTarget[2]));

  // Agy expressive arms & head
  let waveLeft = Math.sin(t * 2.5) * 0.12;
  let waveRight = Math.sin(t * 2.5 + 1) * 0.12;
  let headTilt: [number, number, number] = [0, Math.sin(t * 1.4) * 0.12, 0];
  let winkAmount = 0;

  if (frame < 90) {
    // Both arms raised in "¡WATERS!" alarm
    waveLeft = 1.35 + Math.sin(t * 14) * 0.22;
    waveRight = 1.35 + Math.sin(t * 14) * 0.22;
    headTilt = [-0.1, Math.sin(t * 10) * 0.08, 0];
  } else if (frame < 390) {
    // Explaining / gesturing
    waveRight = 0.7 + Math.sin(t * 4) * 0.35;
    headTilt = [0.05, -0.18 + Math.sin(t * 2) * 0.15, 0.04];
  } else if (frame < 870) {
    // Urgent pointing at threat prisms
    waveLeft = 0.9 + Math.sin(t * 6) * 0.3;
    waveRight = 0.4 + Math.cos(t * 5) * 0.25;
    headTilt = [0.06, Math.sin(t * 3.5) * 0.2, -0.05];
  } else if (frame < 1200) {
    // Confident open stance presenting Gemini 4 Neon shield
    waveLeft = 0.65;
    waveRight = 0.65;
    headTilt = [-0.06, Math.sin(t * 1.5) * 0.1, 0];
  } else {
    // Friendly wave + camera-lens wink around frame 1290-1325
    waveRight = 1.2 + Math.sin(t * 9) * 0.35;
    headTilt = [0.04, 0.08, -0.06];
    if (frame >= 1280 && frame <= 1320) {
      winkAmount = Math.sin(((frame - 1280) / 40) * Math.PI);
    }
  }

  return (
    <>
      <color attach="background" args={['#050814']} />
      <fog attach="fog" args={['#050814', 7, 19]} />

      {/* Lighting */}
      <ambientLight intensity={0.75} />
      <directionalLight position={[4, 6, 5]} intensity={1.8} color="#FFFFFF" />
      <directionalLight position={[-4, 2, -3]} intensity={1.1} color="#38BDF8" />
      <pointLight
        position={[0, 1.5, 2.5]}
        intensity={1.4}
        color={mood === 'alert' ? '#FF4D4D' : mood === 'gold' || mood === 'wink' ? '#DFB15B' : '#38BDF8'}
      />

      <StarField frame={frame} />

      {/* Subtle Neon Floor Grid */}
      <gridHelper
        args={[18, 24, mood === 'alert' ? '#FF4D4D' : mood === 'gold' ? '#DFB15B' : '#1E3A5F', '#0F172A']}
        position={[0, -1.65, 0]}
      />

      {/* AGY PROTAGONIST */}
      <AgyAstronaut3D
        frame={frame}
        fps={fps}
        mood={mood}
        waveLeft={waveLeft}
        waveRight={waveRight}
        headTilt={headTilt}
        winkAmount={winkAmount}
      />

      {/* SCENE 1: Alert Shockwave Rings */}
      {frame < 90 &&
        [0, 1, 2].map((i) => {
          const ringProgress = ((frame + i * 24) % 72) / 72;
          const rScale = 0.8 + ringProgress * 2.6;
          return (
            <mesh key={i} position={[0, 0.5, -0.3]} scale={[rScale, rScale, 1]}>
              <torusGeometry args={[1, 0.02, 12, 48]} />
              <meshBasicMaterial
                color="#FF4D4D"
                transparent
                opacity={(1 - ringProgress) * 0.85}
              />
            </mesh>
          );
        })}

      {/* SCENE 2: Floating Cyber Hologram Monoliths (GTA 6 + Vibe Hacking) */}
      {frame >= 90 && frame < 390 && (
        <group>
          <mesh position={[-1.45, 0.85 + Math.sin(t * 2) * 0.1, -0.4]} rotation={[0.1, 0.4, 0.05]}>
            <boxGeometry args={[0.85, 1.1, 0.05]} />
            <meshStandardMaterial
              color="#0EA5E9"
              emissive="#0284C7"
              emissiveIntensity={0.8}
              transparent
              opacity={0.55}
            />
          </mesh>
          <mesh position={[1.45, 0.25 + Math.cos(t * 2.2) * 0.1, -0.3]} rotation={[-0.1, -0.45, -0.05]}>
            <boxGeometry args={[0.8, 0.9, 0.05]} />
            <meshStandardMaterial
              color="#38BDF8"
              emissive="#38BDF8"
              emissiveIntensity={0.7}
              transparent
              opacity={0.5}
            />
          </mesh>
        </group>
      )}

      {/* SCENE 3: Orbiting Red/Amber Infostealer Threat Prisms */}
      {frame >= 390 && frame < 870 &&
        [0, 1, 2, 3].map((i) => {
          const a = t * 1.4 + (i * Math.PI) / 2;
          const rx = Math.cos(a) * 1.55;
          const rz = Math.sin(a) * 1.1;
          const ry = 0.35 + Math.sin(t * 2.6 + i) * 0.35;
          return (
            <mesh key={i} position={[rx, ry, rz]} rotation={[t * 1.8, t * 1.3, 0]}>
              <octahedronGeometry args={[0.24, 0]} />
              <meshStandardMaterial
                color="#FF3B3B"
                emissive="#FF3B3B"
                emissiveIntensity={1.4}
              />
            </mesh>
          );
        })}

      {/* SCENE 4: Gemini 4 Neon Protective Shield Rings & Hex Core */}
      {frame >= 870 && frame < 1200 && (
        <group position={[0, -0.05, -0.25]}>
          <mesh rotation={[Math.PI / 2.15, t * 0.8, 0.22]}>
            <torusGeometry args={[2.05, 0.032, 16, 6]} />
            <meshStandardMaterial color="#DFB15B" emissive="#DFB15B" emissiveIntensity={2.0} />
          </mesh>
          <mesh rotation={[-Math.PI / 2.15, -t * 0.9, -0.22]}>
            <torusGeometry args={[2.28, 0.024, 16, 6]} />
            <meshStandardMaterial color="#38BDF8" emissive="#38BDF8" emissiveIntensity={1.8} />
          </mesh>
          <mesh position={[0, 0.3, 0]}>
            <icosahedronGeometry args={[1.95, 1]} />
            <meshBasicMaterial color="#DFB15B" wireframe transparent opacity={0.14} />
          </mesh>
        </group>
      )}
    </>
  );
};

export const AgyWatersEpisode: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const activeCue =
    CAPTION_CUES.find((c) => frame >= c.startFrame && frame < c.endFrame) ??
    CAPTION_CUES[CAPTION_CUES.length - 1];

  return (
    <AbsoluteFill style={{ backgroundColor: '#050814' }}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{ position: [0, 0.4, 4.6], fov: 42 }}
      >
        <SceneContent />
      </ThreeCanvas>

      {/* TOP HUD BAR */}
      <AbsoluteFill style={{ pointerEvents: 'none', padding: '64px 48px' }}>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            background: 'rgba(5, 8, 20, 0.72)',
            border: `2px solid ${activeCue.accentColor}`,
            borderRadius: 999,
            padding: '16px 28px',
            boxShadow: `0 0 28px ${activeCue.accentColor}44`,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <div
              style={{
                width: 16,
                height: 16,
                borderRadius: 999,
                backgroundColor: activeCue.accentColor,
                boxShadow: `0 0 14px ${activeCue.accentColor}`,
              }}
            />
            <span
              style={{
                fontFamily: 'system-ui, -apple-system, sans-serif',
                fontWeight: 900,
                fontSize: 26,
                letterSpacing: 1.5,
                color: '#FFFFFF',
              }}
            >
              AGY · ANTIGRAVITY
            </span>
          </div>
          <span
            style={{
              fontFamily: 'system-ui, -apple-system, sans-serif',
              fontWeight: 800,
              fontSize: 22,
              color: activeCue.accentColor,
            }}
          >
            EP. 01 · GTA 6
          </span>
        </div>
      </AbsoluteFill>

      {/* BOTTOM HORMOZI CAPTIONS */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          justifyContent: 'flex-end',
          alignItems: 'center',
          padding: '0 44px 120px 44px',
        }}
      >
        <div
          style={{
            background: 'rgba(5, 8, 20, 0.84)',
            border: `3px solid ${activeCue.accentColor}`,
            borderRadius: 28,
            padding: '26px 34px',
            textAlign: 'center',
            width: '100%',
            boxShadow: `0 16px 48px rgba(0,0,0,0.65), 0 0 32px ${activeCue.accentColor}33`,
          }}
        >
          <div
            style={{
              fontFamily: 'system-ui, -apple-system, sans-serif',
              fontWeight: 800,
              fontSize: 24,
              color: activeCue.accentColor,
              letterSpacing: 1.4,
              marginBottom: 10,
            }}
          >
            {activeCue.badge}
          </div>
          <div
            style={{
              fontFamily: 'system-ui, -apple-system, sans-serif',
              fontWeight: 900,
              fontSize: 44,
              lineHeight: 1.12,
              color: '#FFFFFF',
              textShadow: '0 4px 12px rgba(0,0,0,0.9)',
              marginBottom: 8,
            }}
          >
            {activeCue.line1}
          </div>
          <div
            style={{
              fontFamily: 'system-ui, -apple-system, sans-serif',
              fontWeight: 900,
              fontSize: 54,
              lineHeight: 1.08,
              color: activeCue.accentColor,
              textShadow: '0 4px 16px rgba(0,0,0,0.95)',
            }}
          >
            {activeCue.highlight}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
