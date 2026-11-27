import React, { useMemo } from 'react';
import { interpolate, spring } from 'remotion';
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

export type ToyExpression = 'happy' | 'shock' | 'worried' | 'determined' | 'broken';

function makeGridTexture(): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d')!;
  ctx.fillStyle = '#070b12';
  ctx.fillRect(0, 0, 512, 512);

  // Subtle floor sheen bands
  const grad = ctx.createRadialGradient(256, 256, 20, 256, 256, 320);
  grad.addColorStop(0, 'rgba(0, 217, 234, 0.10)');
  grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 512, 512);

  // Crisp cyan neon grid lines (2x2 tiles per repeat)
  ctx.strokeStyle = 'rgba(0, 224, 240, 0.62)';
  ctx.lineWidth = 4;
  ctx.shadowColor = '#00e0f0';
  ctx.shadowBlur = 10;
  for (let i = 0; i <= 2; i++) {
    const p = i * 256;
    ctx.beginPath();
    ctx.moveTo(p, 0);
    ctx.lineTo(p, 512);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, p);
    ctx.lineTo(512, p);
    ctx.stroke();
  }

  const tex = new THREE.CanvasTexture(canvas);
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(9, 9);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  return tex;
}

function makePlateTexture(
  title: string,
  subtitle: string | undefined,
  bgColor: string,
  fgColor: string,
  accentColor: string,
  width = 512,
  height = 256
): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = bgColor;
  ctx.fillRect(0, 0, width, height);

  ctx.strokeStyle = accentColor;
  ctx.lineWidth = 8;
  ctx.strokeRect(10, 10, width - 20, height - 20);

  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  if (subtitle) {
    ctx.fillStyle = fgColor;
    ctx.font = `900 ${Math.round(height * 0.42)}px "Arial Black", "Helvetica Neue", Arial, sans-serif`;
    ctx.shadowColor = accentColor;
    ctx.shadowBlur = 14;
    ctx.fillText(title, width / 2, height * 0.42);

    ctx.shadowBlur = 0;
    ctx.fillStyle = accentColor;
    ctx.font = `800 ${Math.round(height * 0.18)}px "Arial Black", "Helvetica Neue", Arial, sans-serif`;
    ctx.fillText(subtitle, width / 2, height * 0.77);
  } else {
    ctx.fillStyle = fgColor;
    ctx.font = `900 ${Math.round(height * 0.52)}px "Arial Black", "Helvetica Neue", Arial, sans-serif`;
    ctx.shadowColor = accentColor;
    ctx.shadowBlur = 16;
    ctx.fillText(title, width / 2, height * 0.53);
  }

  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  return tex;
}

function makeDoorTexture(num: string, label: string, color: string): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 768;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = '#141925';
  ctx.fillRect(0, 0, 512, 768);

  // Inner lit panel
  const grad = ctx.createLinearGradient(0, 40, 0, 728);
  grad.addColorStop(0, `${color}44`);
  grad.addColorStop(1, '#101420');
  ctx.fillStyle = grad;
  ctx.fillRect(42, 42, 428, 684);

  ctx.strokeStyle = color;
  ctx.lineWidth = 14;
  ctx.strokeRect(42, 42, 428, 684);

  // Giant Door Number
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = '#ffffff';
  ctx.shadowColor = color;
  ctx.shadowBlur = 24;
  ctx.font = '900 260px "Arial Black", "Helvetica Neue", Arial, sans-serif';
  ctx.fillText(num, 256, 300);

  // Bold 2-word pill plate
  ctx.shadowBlur = 0;
  ctx.fillStyle = color;
  ctx.fillRect(62, 495, 388, 128);
  ctx.fillStyle = '#0a0e16';
  ctx.font = '900 36px "Arial Black", "Helvetica Neue", Arial, sans-serif';
  ctx.fillText(label, 256, 562);

  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  return tex;
}

function makeClipboardPaperTexture(items: string[]): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 640;
  canvas.height = 840;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = '#f8f9fc';
  ctx.fillRect(0, 0, 640, 840);

  // Faint divider lines between the 3 checklist items
  ctx.strokeStyle = '#d8dee9';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(40, 290);
  ctx.lineTo(600, 290);
  ctx.moveTo(40, 545);
  ctx.lineTo(600, 545);
  ctx.stroke();

  const ys = [165, 420, 675];
  items.slice(0, 3).forEach((raw, idx) => {
    const y = ys[idx];
    // Checkbox box
    ctx.strokeStyle = '#3b4252';
    ctx.lineWidth = 12;
    ctx.strokeRect(58, y - 58, 116, 116);

    // Text (support explicit "\n" or auto two-line wrap)
    ctx.fillStyle = '#1e2430';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    const lines = raw.includes('\n')
      ? raw.split('\n')
      : raw.length > 13 && raw.includes(' ')
        ? (() => {
            const parts = raw.split(' ');
            const mid = Math.ceil(parts.length / 2);
            return [parts.slice(0, mid).join(' '), parts.slice(mid).join(' ')];
          })()
        : [raw];

    ctx.font = '900 50px "Arial Black", "Helvetica Neue", Arial, sans-serif';
    if (lines.length === 1) {
      ctx.fillText(lines[0], 208, y + 4);
    } else {
      ctx.fillText(lines[0], 208, y - 28);
      ctx.fillText(lines[1], 208, y + 32);
    }
  });

  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  return tex;
}

export const ToyReflectiveGridStage: React.FC<{
  frame: number;
  accentColor: string;
  alertStrength?: number;
}> = ({ frame, accentColor, alertStrength = 0 }) => {
  const gridTex = useMemo(() => makeGridTexture(), []);
  const dots = useMemo(() => {
    const arr: { x: number; y: number; z: number; phase: number; r: number }[] = [];
    for (let i = 0; i < 28; i++) {
      const s1 = Math.sin(i * 19.31) * 43758.5453;
      const s2 = Math.sin(i * 41.73) * 43758.5453;
      const s3 = Math.sin(i * 71.17) * 43758.5453;
      arr.push({
        x: (s1 - Math.floor(s1) - 0.5) * 9.5,
        y: (s2 - Math.floor(s2)) * 4.8 - 0.5,
        z: -1.5 - (s3 - Math.floor(s3)) * 5.0,
        phase: i * 0.45,
        r: 0.022 + (i % 3) * 0.01,
      });
    }
    return arr;
  }, []);

  const lightColor = alertStrength > 0.35 ? '#ff2a4b' : accentColor;

  return (
    <group>
      <color attach="background" args={['#080c14']} />
      <fog attach="fog" args={['#080c14', 6.5, 16.5]} />

      <ambientLight intensity={0.72} color="#d8e9ff" />
      <directionalLight position={[2.8, 5.2, 4.6]} intensity={1.65} color="#ffffff" />
      <directionalLight position={[-3.5, 2.5, 2.5]} intensity={0.95} color="#7de8ff" />
      <pointLight
        position={[0, 1.8, 2.6]}
        intensity={1.5 + alertStrength * 2.4}
        distance={11}
        color={lightColor}
      />

      {/* Glossy under-floor */}
      <mesh position={[0, -1.355, -2.5]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[28, 28]} />
        <meshStandardMaterial color="#070c14" roughness={0.22} metalness={0.55} />
      </mesh>

      {/* Neon cyan perspective grid overlay */}
      <mesh position={[0, -1.345, -2.5]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[26, 26]} />
        <meshBasicMaterial map={gridTex} transparent opacity={0.86} />
      </mesh>

      {/* Subtle back horizon rim wash */}
      <mesh position={[0, 0.8, -7.2]}>
        <planeGeometry args={[18, 7.5]} />
        <meshBasicMaterial
          color={alertStrength > 0.35 ? '#3a0b19' : '#0b2238'}
          transparent
          opacity={0.45}
        />
      </mesh>

      {/* Deterministic ambient floating dust specks */}
      {dots.map((d, idx) => {
        const y = d.y + Math.sin(frame * 0.045 + d.phase) * 0.22;
        const x = d.x + Math.cos(frame * 0.03 + d.phase) * 0.14;
        return (
          <mesh key={idx} position={[x, y, d.z]}>
            <sphereGeometry args={[d.r, 10, 10]} />
            <meshBasicMaterial
              color={idx % 3 === 0 ? lightColor : '#94f2ff'}
              transparent
              opacity={0.65}
            />
          </mesh>
        );
      })}
    </group>
  );
};

export const GlossyToyFace: React.FC<{
  expression?: ToyExpression;
  position?: [number, number, number];
  scale?: number;
}> = ({ expression = 'happy', position = [0, 0, 0], scale = 1 }) => {
  const isShock = expression === 'shock';
  const isWorried = expression === 'worried';
  const isBroken = expression === 'broken';
  const isDetermined = expression === 'determined';

  const browTilt = isWorried ? 0.32 : isDetermined ? -0.32 : isShock ? 0.18 : 0.08;

  return (
    <group position={position} scale={scale}>
      {[-0.22, 0.22].map((ex, i) => (
        <group key={i} position={[ex, 0.06, 0]}>
          {/* Glossy dark eyeball */}
          <mesh>
            <sphereGeometry args={[0.105, 18, 18]} />
            <meshStandardMaterial color="#0c0f16" roughness={0.05} metalness={0.22} />
          </mesh>
          {/* Specular catchlight */}
          <mesh position={[0.032, 0.036, 0.088]}>
            <sphereGeometry args={[0.028, 10, 10]} />
            <meshBasicMaterial color="#ffffff" />
          </mesh>
          {/* Secondary micro catchlight */}
          <mesh position={[-0.028, -0.025, 0.09]}>
            <sphereGeometry args={[0.014, 8, 8]} />
            <meshBasicMaterial color="#d8f7ff" />
          </mesh>
          {/* Horizontal Eyebrow */}
          <mesh
            position={[0, isShock ? 0.185 : 0.16, 0.03]}
            rotation={[0, 0, Math.PI / 2 + (i === 0 ? browTilt : -browTilt)]}
          >
            <capsuleGeometry args={[0.019, 0.12, 6, 10]} />
            <meshStandardMaterial color="#1a1f2b" roughness={0.35} />
          </mesh>
        </group>
      ))}

      {/* Mouth */}
      {isShock ? (
        <mesh position={[0, -0.15, 0.02]}>
          <torusGeometry args={[0.065, 0.022, 10, 20]} />
          <meshStandardMaterial color="#111520" roughness={0.2} />
        </mesh>
      ) : isBroken ? (
        <mesh position={[0, -0.16, 0.02]} rotation={[0, 0, Math.PI * 0.06]}>
          <boxGeometry args={[0.24, 0.04, 0.04]} />
          <meshStandardMaterial color="#ff3355" emissive="#ff3355" emissiveIntensity={0.8} />
        </mesh>
      ) : (
        <mesh
          position={[0, isWorried ? -0.19 : -0.12, 0.02]}
          rotation={[0, 0, isWorried ? Math.PI * 0.12 : Math.PI * 1.12]}
        >
          <torusGeometry args={[0.11, 0.024, 10, 20, Math.PI * 0.76]} />
          <meshStandardMaterial color="#111520" roughness={0.25} />
        </mesh>
      )}
    </group>
  );
};

export const NeonMarquee3D: React.FC<{
  text: string;
  sub?: string;
  color: string;
  frame: number;
  position?: [number, number, number];
  scale?: number;
}> = ({ text, sub, color, frame, position = [0, 1.55, -0.7], scale = 1 }) => {
  const plateTex = useMemo(
    () => makePlateTexture(text, sub, '#121722', '#ffffff', color, 640, 256),
    [text, sub, color]
  );
  const housingGeo = useMemo(() => new RoundedBoxGeometry(2.65, 1.08, 0.22, 4, 0.07), []);
  const pulse = 0.85 + Math.sin(frame * 0.18) * 0.25;

  return (
    <group position={position} scale={scale}>
      {/* Housing */}
      <mesh geometry={housingGeo}>
        <meshStandardMaterial color="#181e2c" roughness={0.35} metalness={0.55} />
      </mesh>
      {/* Front Faceplate */}
      <mesh position={[0, 0, 0.116]}>
        <planeGeometry args={[2.46, 0.92]} />
        <meshBasicMaterial map={plateTex} />
      </mesh>
      {/* Top & bottom marquee glow rails */}
      {[-0.55, 0.55].map((y, idx) => (
        <mesh key={idx} position={[0, y, 0.04]}>
          <boxGeometry args={[2.72, 0.045, 0.24]} />
          <meshStandardMaterial
            color={color}
            emissive={color}
            emissiveIntensity={1.25 * pulse}
          />
        </mesh>
      ))}
    </group>
  );
};

export const AlarmBeacon3D: React.FC<{
  frame: number;
  active?: boolean;
  position?: [number, number, number];
  scale?: number;
}> = ({ frame, active = true, position = [1.05, -0.82, 0.1], scale = 1 }) => {
  const pulse = active ? 0.75 + Math.abs(Math.sin(frame * 0.36)) * 1.45 : 0.12;
  const domeColor = active ? '#ff1f42' : '#4a1c26';

  return (
    <group position={position} scale={scale}>
      {/* Dark Pedestal */}
      <mesh position={[0, -0.28, 0]}>
        <cylinderGeometry args={[0.36, 0.44, 0.48, 24]} />
        <meshStandardMaterial color="#1b2130" roughness={0.4} metalness={0.5} />
      </mesh>
      {/* Glowing Collar */}
      <mesh position={[0, -0.02, 0]}>
        <cylinderGeometry args={[0.32, 0.36, 0.08, 24]} />
        <meshStandardMaterial
          color="#ff4d6d"
          emissive="#ff1f42"
          emissiveIntensity={active ? 0.9 : 0.1}
        />
      </mesh>
      {/* Red Siren Dome */}
      <mesh position={[0, 0.16, 0]}>
        <capsuleGeometry args={[0.24, 0.22, 12, 24]} />
        <meshStandardMaterial
          color={domeColor}
          emissive="#ff1f42"
          emissiveIntensity={pulse}
          roughness={0.12}
          transparent
          opacity={0.92}
        />
      </mesh>
      {/* Rotating Reflector Bar inside dome */}
      <mesh position={[0, 0.2, 0]} rotation={[0, frame * 0.28, 0]}>
        <boxGeometry args={[0.34, 0.16, 0.08]} />
        <meshBasicMaterial color={active ? '#ffd6dc' : '#55222a'} />
      </mesh>
    </group>
  );
};

export const SemiGauge3D: React.FC<{
  targetRatio: number;
  localFrame: number;
  fps: number;
  position?: [number, number, number];
  scale?: number;
}> = ({ targetRatio, localFrame, fps, position = [0, -0.35, -0.95], scale = 1 }) => {
  const needleSpring = spring({
    frame: Math.max(0, localFrame - 8),
    fps,
    config: { damping: 14, stiffness: 90 },
  });
  // Gauge spans PI (left=0) to 0 (right=1)
  const angle = interpolate(
    needleSpring * targetRatio,
    [0, 1],
    [Math.PI * 0.42, -Math.PI * 0.42]
  );

  return (
    <group position={position} scale={scale}>
      {/* Dial Backing Semicircle */}
      <mesh position={[0, 0.05, -0.06]}>
        <circleGeometry args={[1.15, 32, 0, Math.PI]} />
        <meshStandardMaterial color="#f0ead8" roughness={0.35} />
      </mesh>
      {/* Green, Amber, Red Segments */}
      <mesh position={[0, 0.05, 0]} rotation={[0, 0, Math.PI * 0.66]}>
        <torusGeometry args={[0.88, 0.12, 10, 24, Math.PI * 0.34]} />
        <meshStandardMaterial color="#2ed573" emissive="#2ed573" emissiveIntensity={0.45} />
      </mesh>
      <mesh position={[0, 0.05, 0]} rotation={[0, 0, Math.PI * 0.33]}>
        <torusGeometry args={[0.88, 0.12, 10, 24, Math.PI * 0.33]} />
        <meshStandardMaterial color="#ffa502" emissive="#ffa502" emissiveIntensity={0.45} />
      </mesh>
      <mesh position={[0, 0.05, 0]} rotation={[0, 0, 0]}>
        <torusGeometry args={[0.88, 0.12, 10, 24, Math.PI * 0.33]} />
        <meshStandardMaterial color="#ff4757" emissive="#ff4757" emissiveIntensity={0.55} />
      </mesh>

      {/* Needle */}
      <group position={[0, 0.05, 0.08]} rotation={[0, 0, angle]}>
        <mesh position={[0, 0.38, 0]}>
          <boxGeometry args={[0.07, 0.78, 0.05]} />
          <meshStandardMaterial color="#181c24" roughness={0.2} />
        </mesh>
        <mesh>
          <sphereGeometry args={[0.13, 16, 16]} />
          <meshStandardMaterial color="#181c24" roughness={0.2} />
        </mesh>
      </group>

      {/* Console Pedestal */}
      <mesh position={[0, -0.45, 0.05]}>
        <boxGeometry args={[2.55, 0.95, 0.5]} />
        <meshStandardMaterial color="#151b26" roughness={0.38} metalness={0.4} />
      </mesh>
      <mesh position={[0, 0.04, 0.31]}>
        <boxGeometry args={[2.58, 0.06, 0.04]} />
        <meshStandardMaterial color="#00e0f0" emissive="#00e0f0" emissiveIntensity={1.1} />
      </mesh>
    </group>
  );
};

export const CapsuleToyCharacter3D: React.FC<{
  position?: [number, number, number];
  headRotY?: number;
  waveArm?: number;
  expression?: ToyExpression;
  suitColor?: string;
  scale?: number;
}> = ({
  position = [0, -0.78, 0.45],
  headRotY = 0,
  waveArm = 0,
  expression = 'happy',
  suitColor = '#252b3b',
  scale = 1,
}) => {
  return (
    <group position={position} scale={scale}>
      {/* Contact shadow */}
      <mesh position={[0, -0.56, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[0.45, 24]} />
        <meshBasicMaterial color="#020308" transparent opacity={0.45} />
      </mesh>

      {/* Legs */}
      {[-0.14, 0.14].map((x, i) => (
        <mesh key={i} position={[x, -0.32, 0]}>
          <capsuleGeometry args={[0.08, 0.28, 8, 12]} />
          <meshStandardMaterial color="#191e2a" roughness={0.35} />
        </mesh>
      ))}

      {/* Torso */}
      <mesh position={[0, 0.04, 0]}>
        <capsuleGeometry args={[0.24, 0.34, 12, 20]} />
        <meshStandardMaterial color={suitColor} roughness={0.28} metalness={0.18} />
      </mesh>

      {/* Left Arm */}
      <mesh position={[-0.31, 0.08, 0]} rotation={[0, 0, 0.22]}>
        <capsuleGeometry args={[0.065, 0.28, 8, 12]} />
        <meshStandardMaterial color={suitColor} roughness={0.3} />
      </mesh>
      {/* Right Arm (can wave) */}
      <group position={[0.3, 0.16, 0]} rotation={[0, 0, -0.25 + waveArm]}>
        <mesh position={[0.04, -0.1, 0]}>
          <capsuleGeometry args={[0.065, 0.28, 8, 12]} />
          <meshStandardMaterial color={suitColor} roughness={0.3} />
        </mesh>
      </group>

      {/* Head */}
      <group position={[0, 0.62, 0]} rotation={[0, headRotY, 0]}>
        <mesh>
          <sphereGeometry args={[0.33, 24, 24]} />
          <meshStandardMaterial color="#f6efe2" roughness={0.22} />
        </mesh>
        {/* Dark stylized hair cap */}
        <mesh position={[0, 0.22, -0.03]} rotation={[-0.25, 0, 0]} scale={[1.05, 0.55, 1.02]}>
          <sphereGeometry args={[0.31, 20, 16]} />
          <meshStandardMaterial color="#4a3123" roughness={0.45} />
        </mesh>
        <GlossyToyFace expression={expression} position={[0, -0.02, 0.305]} scale={0.58} />
      </group>
    </group>
  );
};

export const BinaryDoors3D: React.FC<{
  frame: number;
  leftNum?: string;
  leftLabel: string;
  rightNum?: string;
  rightLabel: string;
}> = ({ frame, leftNum = '1', leftLabel, rightNum = '2', rightLabel }) => {
  const leftTex = useMemo(() => makeDoorTexture(leftNum, leftLabel, '#ff3366'), [leftNum, leftLabel]);
  const rightTex = useMemo(() => makeDoorTexture(rightNum, rightLabel, '#00e0f0'), [rightNum, rightLabel]);
  const lookSweep = Math.sin(frame * 0.08) * 0.42;

  return (
    <group position={[0, 0.02, -0.35]} scale={0.94}>
      {/* Left Door */}
      <group position={[-0.96, 0.25, 0]}>
        <mesh>
          <boxGeometry args={[1.66, 2.7, 0.26]} />
          <meshStandardMaterial color="#2a1622" emissive="#ff3366" emissiveIntensity={0.45} />
        </mesh>
        <mesh position={[0, 0, 0.135]}>
          <planeGeometry args={[1.52, 2.52]} />
          <meshBasicMaterial map={leftTex} />
        </mesh>
      </group>

      {/* Right Door */}
      <group position={[0.96, 0.25, 0]}>
        <mesh>
          <boxGeometry args={[1.66, 2.7, 0.26]} />
          <meshStandardMaterial color="#122736" emissive="#00e0f0" emissiveIntensity={0.45} />
        </mesh>
        <mesh position={[0, 0, 0.135]}>
          <planeGeometry args={[1.52, 2.52]} />
          <meshBasicMaterial map={rightTex} />
        </mesh>
      </group>

      {/* Character standing in front deciding between both doors */}
      <CapsuleToyCharacter3D
        position={[0, -0.74, 0.95]}
        headRotY={lookSweep}
        expression="worried"
        scale={1.0}
      />
    </group>
  );
};

export const GiantClipboard3D: React.FC<{
  items: string[];
  localFrame: number;
  fps: number;
  frame: number;
}> = ({ items, localFrame, fps, frame }) => {
  const paperTex = useMemo(() => makeClipboardPaperTexture(items), [items]);
  const boardGeo = useMemo(() => new RoundedBoxGeometry(2.65, 3.35, 0.18, 4, 0.08), []);

  const checkDelays = [10, 48, 86];
  const wave = Math.sin(frame * 0.22) * 0.35 + 1.1;

  return (
    <group position={[-0.38, 0.3, -0.3]} scale={0.88}>
      {/* Wooden Clipboard */}
      <mesh geometry={boardGeo}>
        <meshStandardMaterial color="#8c5832" roughness={0.42} metalness={0.1} />
      </mesh>
      {/* Paper Sheet */}
      <mesh position={[0, -0.08, 0.098]}>
        <planeGeometry args={[2.32, 2.95]} />
        <meshBasicMaterial map={paperTex} />
      </mesh>
      {/* Metallic Top Clip */}
      <mesh position={[0, 1.56, 0.14]}>
        <boxGeometry args={[0.92, 0.26, 0.14]} />
        <meshStandardMaterial color="#cfd8e3" roughness={0.2} metalness={0.8} />
      </mesh>

      {/* 3 Chunky Neon Green 3D Checkmarks popping sequentially */}
      {[0.81, -0.08, -0.97].map((rowY, idx) => {
        const pop = spring({
          frame: Math.max(0, localFrame - checkDelays[idx]),
          fps,
          config: { damping: 11, stiffness: 190 },
        });
        const s = Math.max(0.001, pop);
        return (
          <group key={idx} position={[-0.74, rowY, 0.16]} scale={[s, s, s]}>
            <mesh position={[-0.1, -0.02, 0]} rotation={[0, 0, 0.78]}>
              <capsuleGeometry args={[0.042, 0.18, 6, 10]} />
              <meshStandardMaterial color="#2ee87a" emissive="#2ee87a" emissiveIntensity={0.65} />
            </mesh>
            <mesh position={[0.07, 0.03, 0]} rotation={[0, 0, -0.68]}>
              <capsuleGeometry args={[0.042, 0.34, 6, 10]} />
              <meshStandardMaterial color="#2ee87a" emissive="#2ee87a" emissiveIntensity={0.65} />
            </mesh>
          </group>
        );
      })}

      {/* Host peaking beside clipboard waving */}
      <CapsuleToyCharacter3D
        position={[1.55, -0.92, 0.35]}
        headRotY={-0.18}
        waveArm={wave}
        expression="happy"
        scale={0.94}
      />
    </group>
  );
};

export const CarbonCrownBlock3D: React.FC<{
  frame: number;
  fps: number;
}> = ({ frame, fps }) => {
  const t = frame / fps;
  // Transition from bright confident crown block (0..1.0s) -> cracked alert (1.0s..2.2s+)
  const brokenProgress = interpolate(t, [0.95, 2.05], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const isBroken = brokenProgress > 0.35;

  const bodyGeo = useMemo(() => new RoundedBoxGeometry(1.78, 1.95, 1.12, 4, 0.14), []);
  const tileGeo = useMemo(() => new RoundedBoxGeometry(0.62, 0.56, 0.12, 3, 0.06), []);
  const nameTex = useMemo(
    () => makePlateTexture('CARBON 4', isBroken ? 'SIN PRUEBAS' : 'GEMINI AI', '#151b28', '#ffffff', isBroken ? '#ff3355' : '#00e0f0', 512, 180),
    [isBroken]
  );

  const bob = Math.sin(frame * 0.13) * 0.06;
  const tilt = brokenProgress * -0.14 + Math.sin(frame * 0.35) * brokenProgress * 0.035;
  const crownDrop = brokenProgress * 0.22;
  const crownTilt = brokenProgress * 0.42;

  const tileColors = ['#00e0f0', '#38bdf8', '#2ee87a', '#a855f7'];
  const tilePositions: [number, number][] = [
    [-0.38, 0.44],
    [0.38, 0.44],
    [-0.38, -0.22],
    [0.38, -0.22],
  ];

  return (
    <group position={[-0.25, 0.08 + bob, 0]} scale={0.9}>
      {/* Hero Carbon Toy Block */}
      <group rotation={[0, Math.sin(frame * 0.04) * 0.08, tilt]}>
        <mesh geometry={bodyGeo}>
          <meshStandardMaterial
            color={isBroken ? '#202432' : '#1b263b'}
            roughness={0.22}
            metalness={0.4}
          />
        </mesh>

        {/* 4 Glowing Gem Tiles (flicker dark when broken!) */}
        {tilePositions.map(([tx, ty], i) => {
          const dim = interpolate(brokenProgress, [0, 0.4 + i * 0.12, 1], [1, 0.25, 0.12], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          return (
            <mesh key={i} geometry={tileGeo} position={[tx, ty, 0.54]}>
              <meshStandardMaterial
                color={isBroken ? '#2a3040' : tileColors[i]}
                emissive={isBroken ? '#33121a' : tileColors[i]}
                emissiveIntensity={dim * 1.15}
                roughness={0.14}
              />
            </mesh>
          );
        })}

        {/* Glowing Red Crack Zigzag appearing on 1.0s -> 2.0s */}
        {brokenProgress > 0.15 && (
          <group position={[0, 0.05, 0.62]} scale={[1, brokenProgress, 1]}>
            <mesh rotation={[0, 0, -0.48]}>
              <boxGeometry args={[0.07, 0.85, 0.04]} />
              <meshStandardMaterial color="#ff2448" emissive="#ff2448" emissiveIntensity={1.8} />
            </mesh>
            <mesh position={[0.16, -0.28, 0]} rotation={[0, 0, 0.65]}>
              <boxGeometry args={[0.06, 0.55, 0.04]} />
              <meshStandardMaterial color="#ff2448" emissive="#ff2448" emissiveIntensity={1.8} />
            </mesh>
          </group>
        )}

        {/* Glossy Toy Face */}
        <GlossyToyFace
          expression={isBroken ? 'shock' : 'happy'}
          position={[0, -0.68, 0.57]}
          scale={0.95}
        />

        {/* Golden Crown on Top (tilts/slips when broken!) */}
        <group position={[crownDrop, 1.14 - crownDrop * 0.3, 0]} rotation={[0, 0, -crownTilt]}>
          <mesh>
            <cylinderGeometry args={[0.42, 0.36, 0.22, 16]} />
            <meshStandardMaterial color="#ffd166" emissive="#f4a261" emissiveIntensity={0.45} metalness={0.65} roughness={0.22} />
          </mesh>
          {[-0.24, 0, 0.24].map((px, i) => (
            <mesh key={i} position={[px, 0.2, 0]}>
              <coneGeometry args={[0.11, 0.26, 8]} />
              <meshStandardMaterial color="#ffd166" emissive="#f4a261" emissiveIntensity={0.5} metalness={0.65} roughness={0.22} />
            </mesh>
          ))}
        </group>
      </group>

      {/* Carbon Nameplate at feet */}
      <mesh position={[0, -0.92, 0.85]}>
        <boxGeometry args={[1.45, 0.42, 0.22]} />
        <meshStandardMaterial color="#111622" roughness={0.4} />
      </mesh>
      <mesh position={[0, -0.92, 0.965]}>
        <planeGeometry args={[1.38, 0.36]} />
        <meshBasicMaterial map={nameTex} />
      </mesh>

      {/* Flashing Red Alarm Beacon on right */}
      <AlarmBeacon3D frame={frame} active={isBroken} position={[1.38, -0.78, 0.25]} scale={1.08} />
    </group>
  );
};

export const DockerWhaleBox3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
}> = ({ frame, localFrame, fps }) => {
  const whaleGeo = useMemo(() => new RoundedBoxGeometry(2.15, 1.1, 1.25, 4, 0.16), []);
  const crateGeo = useMemo(() => new RoundedBoxGeometry(0.46, 0.36, 0.46, 3, 0.05), []);
  const pop = spring({ frame: localFrame, fps, config: { damping: 12, stiffness: 160 } });
  const bob = Math.sin(frame * 0.12) * 0.05;

  const crateColors = ['#2ee87a', '#00e0f0', '#fbbf24', '#38bdf8'];
  const barGrow = spring({ frame: Math.max(0, localFrame - 14), fps, config: { damping: 14, stiffness: 120 } });

  return (
    <group position={[0, -0.35 + bob, 0]} scale={Math.max(0.01, pop)}>
      {/* Docker Cyan Container Whale */}
      <group position={[-0.35, -0.32, 0.2]}>
        <mesh geometry={whaleGeo}>
          <meshStandardMaterial color="#00a8e8" roughness={0.18} metalness={0.15} />
        </mesh>
        {/* Tail Fin */}
        <mesh position={[-1.25, 0.32, 0]} rotation={[0, 0, 0.45]}>
          <boxGeometry args={[0.45, 0.24, 0.4]} />
          <meshStandardMaterial color="#0096c7" roughness={0.22} />
        </mesh>
        <GlossyToyFace expression="happy" position={[0.45, -0.05, 0.64]} scale={0.92} />

        {/* Stacked Cargo Crates */}
        {crateColors.map((c, i) => (
          <mesh key={i} geometry={crateGeo} position={[-0.45 + (i % 3) * 0.5, i === 3 ? 1.12 : 0.74, 0]}>
            <meshStandardMaterial color={c} emissive={c} emissiveIntensity={0.3} roughness={0.22} />
          </mesh>
        ))}
      </group>

      {/* Clean Comparison Bars (Carbon 88.2 vs Astra 85) */}
      <group position={[1.25, -0.95, -0.25]}>
        <mesh position={[0, 0.9 * barGrow, 0]}>
          <boxGeometry args={[0.52, Math.max(0.05, 1.8 * barGrow), 0.52]} />
          <meshStandardMaterial color="#2ee87a" emissive="#2ee87a" emissiveIntensity={0.45} roughness={0.2} />
        </mesh>
        <mesh position={[0.65, 0.72 * barGrow, 0]}>
          <boxGeometry args={[0.46, Math.max(0.05, 1.44 * barGrow), 0.46]} />
          <meshStandardMaterial color="#64748b" roughness={0.35} />
        </mesh>
      </group>
    </group>
  );
};

export const ExploitTrioBlocks3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
}> = ({ frame, localFrame, fps }) => {
  const grow = spring({ frame: localFrame, fps, config: { damping: 13, stiffness: 130 } });
  const carbonGeo = useMemo(() => new RoundedBoxGeometry(0.86, 1.55, 0.72, 3, 0.1), []);
  const astraGeo = useMemo(() => new RoundedBoxGeometry(0.78, 1.18, 0.68, 3, 0.1), []);
  const opusGeo = useMemo(() => new RoundedBoxGeometry(0.74, 0.95, 0.66, 3, 0.1), []);
  const bob = Math.sin(frame * 0.11) * 0.04;

  return (
    <group position={[0, -0.22, 0.25]}>
      {/* Carbon 54.8% (Winner, Happy) */}
      <group position={[-1.08, -0.35 + bob, 0.15]} scale={[1, Math.max(0.05, grow), 1]}>
        <mesh geometry={carbonGeo}>
          <meshStandardMaterial color="#00d9ea" emissive="#00a8c6" emissiveIntensity={0.38} roughness={0.18} />
        </mesh>
        <GlossyToyFace expression="happy" position={[0, 0.22, 0.37]} scale={0.82} />
      </group>

      {/* Astra 42.4% (Determined) */}
      <group position={[0.02, -0.54 - bob * 0.6, 0.15]} scale={[1, Math.max(0.05, grow), 1]}>
        <mesh geometry={astraGeo}>
          <meshStandardMaterial color="#fb923c" emissive="#ea580c" emissiveIntensity={0.28} roughness={0.22} />
        </mesh>
        <GlossyToyFace expression="determined" position={[0, 0.16, 0.35]} scale={0.76} />
      </group>

      {/* Opus 34.5% (Worried) */}
      <group position={[1.08, -0.66 + bob * 0.5, 0.15]} scale={[1, Math.max(0.05, grow), 1]}>
        <mesh geometry={opusGeo}>
          <meshStandardMaterial color="#8b5cf6" emissive="#6d28d9" emissiveIntensity={0.26} roughness={0.24} />
        </mesh>
        <GlossyToyFace expression="worried" position={[0, 0.12, 0.34]} scale={0.72} />
      </group>
    </group>
  );
};

export const BandagedRepoCube3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
}> = ({ frame, localFrame, fps }) => {
  const cubeGeo = useMemo(() => new RoundedBoxGeometry(1.72, 1.55, 1.25, 4, 0.18), []);
  const patchGeo = useMemo(() => new RoundedBoxGeometry(0.92, 0.28, 0.09, 3, 0.04), []);
  const patchSnap = spring({
    frame: Math.max(0, localFrame - 24),
    fps,
    config: { damping: 11, stiffness: 190 },
  });
  const patchZ = interpolate(patchSnap, [0, 1], [2.4, 0.65]);
  const bob = Math.sin(frame * 0.13) * 0.05;

  return (
    <group position={[0, -0.45 + bob, 0]}>
      {/* Chunky Purple Repo Mascot Cube */}
      <mesh geometry={cubeGeo}>
        <meshStandardMaterial color="#7c5cff" emissive="#4c1d95" emissiveIntensity={0.28} roughness={0.2} />
      </mesh>
      <GlossyToyFace
        expression={patchSnap > 0.6 ? 'happy' : 'worried'}
        position={[0, -0.05, 0.64]}
        scale={0.98}
      />

      {/* Red bug fracture on forehead */}
      <mesh position={[0.25, 0.45, 0.635]} rotation={[0, 0, -0.55]}>
        <boxGeometry args={[0.07, 0.52, 0.03]} />
        <meshStandardMaterial color="#ff2a4b" emissive="#ff2a4b" emissiveIntensity={1.5} />
      </mesh>

      {/* Giant Emerald-Green Self-Healing Patch Bandage slapping onto crack */}
      <group position={[0.22, 0.44, patchZ]} rotation={[0, 0, 0.32]} scale={Math.max(0.01, patchSnap)}>
        <mesh geometry={patchGeo}>
          <meshStandardMaterial color="#2ee87a" emissive="#10b981" emissiveIntensity={0.45} roughness={0.22} />
        </mesh>
        <mesh position={[0, 0, 0.05]}>
          <boxGeometry args={[0.26, 0.22, 0.03]} />
          <meshStandardMaterial color="#f8fafc" roughness={0.35} />
        </mesh>
      </group>
    </group>
  );
};
