import React from 'react';
import * as THREE from 'three';

export type AgyMood = 'alert' | 'cyan' | 'gold' | 'wink';

interface AgyAstronaut3DProps {
  frame: number;
  fps: number;
  mood: AgyMood;
  position?: [number, number, number];
  rotation?: [number, number, number];
  scale?: number;
  waveLeft?: number;
  waveRight?: number;
  headTilt?: [number, number, number];
  winkAmount?: number; // 0 = open, 1 = closed shutter
}

const MOOD_COLORS: Record<AgyMood, { main: string; glow: string }> = {
  alert: { main: '#FF3B3B', glow: '#FF6B6B' },
  cyan: { main: '#38BDF8', glow: '#7DD3FC' },
  gold: { main: '#DFB15B', glow: '#FDE68A' },
  wink: { main: '#DFB15B', glow: '#38BDF8' },
};

export const AgyAstronaut3D: React.FC<AgyAstronaut3DProps> = ({
  frame,
  fps,
  mood,
  position = [0, 0, 0],
  rotation = [0, 0, 0],
  scale = 1,
  waveLeft = 0,
  waveRight = 0,
  headTilt = [0, 0, 0],
  winkAmount = 0,
}) => {
  const t = frame / fps;
  const floatY = Math.sin(t * 2.4) * 0.08;
  const floatRotZ = Math.sin(t * 1.6) * 0.035;
  const thrusterPulse = 0.85 + Math.sin(t * 28) * 0.18;
  const palette = MOOD_COLORS[mood];

  // Subtle automatic blink every ~3.5s unless winking
  const blinkCycle = (t * 0.9) % 3.4;
  const autoBlink = blinkCycle > 3.22 ? Math.sin(((blinkCycle - 3.22) / 0.18) * Math.PI) : 0;
  const shutterClosed = Math.min(1, Math.max(winkAmount, autoBlink));
  const irisScaleY = Math.max(0.08, 1 - shutterClosed * 0.92);

  const suitWhite = '#F1F5F9';
  const suitTrim = '#CBD5E1';
  const darkMetal = '#1E293B';
  const visorBlack = '#070B14';

  return (
    <group
      position={[position[0], position[1] + floatY, position[2]]}
      rotation={[rotation[0], rotation[1], rotation[2] + floatRotZ]}
      scale={scale}
    >
      {/* HEAD + HELMET + CAMERA LENS VISOR */}
      <group position={[0, 0.95, 0]} rotation={headTilt}>
        {/* Outer Helmet Shell */}
        <mesh castShadow receiveShadow>
          <sphereGeometry args={[0.72, 36, 36]} />
          <meshStandardMaterial color={suitWhite} roughness={0.22} metalness={0.1} />
        </mesh>

        {/* Helmet Collar Ring */}
        <mesh position={[0, -0.58, 0]} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[0.48, 0.09, 16, 36]} />
          <meshStandardMaterial color={darkMetal} roughness={0.35} metalness={0.75} />
        </mesh>

        {/* Side Ear Pods */}
        {[-0.72, 0.72].map((x, idx) => (
          <group key={idx} position={[x, 0.02, 0]}>
            <mesh rotation={[0, 0, Math.PI / 2]}>
              <cylinderGeometry args={[0.17, 0.17, 0.14, 24]} />
              <meshStandardMaterial color={suitTrim} roughness={0.3} metalness={0.6} />
            </mesh>
            <mesh position={[x > 0 ? 0.08 : -0.08, 0, 0]} rotation={[0, Math.PI / 2, 0]}>
              <torusGeometry args={[0.1, 0.022, 12, 24]} />
              <meshStandardMaterial
                color={palette.main}
                emissive={palette.main}
                emissiveIntensity={1.6}
              />
            </mesh>
          </group>
        ))}

        {/* Top Antenna */}
        <group position={[0.25, 0.68, -0.05]} rotation={[0, 0, -0.18]}>
          <mesh position={[0, 0.18, 0]}>
            <cylinderGeometry args={[0.02, 0.03, 0.36, 12]} />
            <meshStandardMaterial color={suitTrim} metalness={0.8} roughness={0.2} />
          </mesh>
          <mesh position={[0, 0.38, 0]}>
            <sphereGeometry args={[0.065, 16, 16]} />
            <meshStandardMaterial
              color={palette.main}
              emissive={palette.main}
              emissiveIntensity={2.2 + Math.sin(t * 8) * 0.6}
            />
          </mesh>
        </group>

        {/* Dark Glossy Visor */}
        <mesh position={[0, 0.03, 0.28]} scale={[0.96, 0.82, 0.85]}>
          <sphereGeometry args={[0.58, 48, 48]} />
          <meshStandardMaterial
            color={visorBlack}
            roughness={0.06}
            metalness={0.92}
          />
        </mesh>

        {/* CAMERA LENS INSIDE VISOR (Captoora + Antigravity Soul) */}
        <group position={[0, 0.03, 0.68]} scale={[1, irisScaleY, 1]}>
          {/* Outer Anodized Lens Barrel */}
          <mesh rotation={[Math.PI / 2, 0, 0]}>
            <cylinderGeometry args={[0.31, 0.34, 0.16, 36]} />
            <meshStandardMaterial color="#0F172A" metalness={0.85} roughness={0.25} />
          </mesh>

          {/* Glowing Outer Aperture Ring */}
          <mesh position={[0, 0, 0.08]}>
            <torusGeometry args={[0.26, 0.026, 16, 48]} />
            <meshStandardMaterial
              color={palette.main}
              emissive={palette.main}
              emissiveIntensity={2.4}
            />
          </mesh>

          {/* Inner Precision Ring */}
          <mesh position={[0, 0, 0.095]} rotation={[0, 0, t * 0.9]}>
            <torusGeometry args={[0.17, 0.015, 12, 6]} />
            <meshStandardMaterial
              color={palette.glow}
              emissive={palette.glow}
              emissiveIntensity={1.8}
            />
          </mesh>

          {/* Optical Glass Dome */}
          <mesh position={[0, 0, 0.05]} scale={[1, 1, 0.45]}>
            <sphereGeometry args={[0.21, 28, 28]} />
            <meshStandardMaterial
              color="#0A192F"
              emissive={palette.main}
              emissiveIntensity={0.45}
              roughness={0.05}
              metalness={0.95}
            />
          </mesh>

          {/* Bright Center Pupil / Sensor Core */}
          <mesh position={[0, 0, 0.125]}>
            <sphereGeometry args={[0.075, 20, 20]} />
            <meshStandardMaterial
              color="#FFFFFF"
              emissive={palette.glow}
              emissiveIntensity={2.5}
            />
          </mesh>

          {/* Specular Lens Catchlight */}
          <mesh position={[0.075, 0.085, 0.14]}>
            <sphereGeometry args={[0.028, 12, 12]} />
            <meshBasicMaterial color="#FFFFFF" />
          </mesh>
        </group>
      </group>

      {/* TORSO */}
      <group position={[0, 0.02, 0]}>
        <mesh castShadow receiveShadow>
          <capsuleGeometry args={[0.42, 0.44, 16, 32]} />
          <meshStandardMaterial color={suitWhite} roughness={0.28} metalness={0.08} />
        </mesh>

        {/* Chest Control Pack */}
        <mesh position={[0, 0.08, 0.39]}>
          <boxGeometry args={[0.42, 0.3, 0.12]} />
          <meshStandardMaterial color={suitTrim} roughness={0.3} metalness={0.4} />
        </mesh>
        {/* Chest Core Bar */}
        <mesh position={[0, 0.11, 0.46]}>
          <boxGeometry args={[0.26, 0.08, 0.03]} />
          <meshStandardMaterial
            color={palette.main}
            emissive={palette.main}
            emissiveIntensity={2.0}
          />
        </mesh>
        {/* Belt */}
        <mesh position={[0, -0.24, 0]} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[0.42, 0.05, 12, 32]} />
          <meshStandardMaterial color={darkMetal} metalness={0.7} roughness={0.3} />
        </mesh>
      </group>

      {/* BACKPACK + THRUSTERS */}
      <group position={[0, 0.08, -0.44]}>
        <mesh castShadow>
          <boxGeometry args={[0.56, 0.66, 0.32]} />
          <meshStandardMaterial color={suitTrim} roughness={0.35} metalness={0.25} />
        </mesh>
        {[-0.16, 0.16].map((x, idx) => (
          <group key={idx} position={[x, -0.36, 0]}>
            <mesh>
              <cylinderGeometry args={[0.08, 0.11, 0.16, 16]} />
              <meshStandardMaterial color={darkMetal} metalness={0.8} roughness={0.25} />
            </mesh>
            <mesh position={[0, -0.18 * thrusterPulse, 0]} rotation={[Math.PI, 0, 0]}>
              <coneGeometry args={[0.08, 0.28 * thrusterPulse, 16]} />
              <meshBasicMaterial color={palette.glow} transparent opacity={0.88} />
            </mesh>
          </group>
        ))}
      </group>

      {/* LEFT ARM */}
      <group position={[-0.52, 0.22, 0]} rotation={[0, 0, -0.35 - waveLeft]}>
        <mesh position={[-0.14, -0.18, 0]} rotation={[0, 0, -0.2]}>
          <capsuleGeometry args={[0.12, 0.34, 12, 20]} />
          <meshStandardMaterial color={suitWhite} roughness={0.3} />
        </mesh>
        <mesh position={[-0.22, -0.45, 0]}>
          <sphereGeometry args={[0.14, 18, 18]} />
          <meshStandardMaterial color={darkMetal} roughness={0.4} metalness={0.5} />
        </mesh>
      </group>

      {/* RIGHT ARM */}
      <group position={[0.52, 0.22, 0]} rotation={[0, 0, 0.35 + waveRight]}>
        <mesh position={[0.14, -0.18, 0]} rotation={[0, 0, 0.2]}>
          <capsuleGeometry args={[0.12, 0.34, 12, 20]} />
          <meshStandardMaterial color={suitWhite} roughness={0.3} />
        </mesh>
        <mesh position={[0.22, -0.45, 0]}>
          <sphereGeometry args={[0.14, 18, 18]} />
          <meshStandardMaterial color={darkMetal} roughness={0.4} metalness={0.5} />
        </mesh>
      </group>

      {/* LEGS & BOOTS */}
      {[-0.2, 0.2].map((x, idx) => {
        const kick = Math.sin(t * 3.2 + idx * Math.PI) * 0.12;
        return (
          <group key={idx} position={[x, -0.48, 0]} rotation={[kick, 0, 0]}>
            <mesh position={[0, -0.2, 0]}>
              <capsuleGeometry args={[0.14, 0.26, 12, 20]} />
              <meshStandardMaterial color={suitWhite} roughness={0.3} />
            </mesh>
            <mesh position={[0, -0.44, 0.06]}>
              <boxGeometry args={[0.24, 0.16, 0.34]} />
              <meshStandardMaterial color={darkMetal} roughness={0.35} metalness={0.5} />
            </mesh>
          </group>
        );
      })}
    </group>
  );
};
