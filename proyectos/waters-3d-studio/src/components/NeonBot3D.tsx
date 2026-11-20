import React from 'react';
import { interpolate } from 'remotion';

export type NeonExpression =
  | 'shock'
  | 'skeptic'
  | 'star_eyes'
  | 'laser_focus'
  | 'happy_wink';

interface NeonBot3DProps {
  frame: number;
  fps: number;
  expression: NeonExpression;
  accentColor: string;
  speaking?: boolean;
  position?: [number, number, number];
  scale?: number;
}

/**
 * Stylized obsidian-black & neon robot character with large expressive LED eyes,
 * articulated eyebrows, and animated voice equalizer on pure void background.
 */
export const NeonBot3D: React.FC<NeonBot3DProps> = ({
  frame,
  fps,
  expression,
  accentColor,
  speaking = true,
  position = [0, 0, 0],
  scale = 1,
}) => {
  const t = frame / fps;
  const hoverY = Math.sin(t * 2.6) * 0.08;
  const bodyTiltZ = Math.sin(t * 1.4) * 0.04;

  // Periodic natural blink unless shocking or winking
  const blinkCycle = t % 3.2;
  const naturalBlink =
    expression !== 'shock' && expression !== 'happy_wink' && blinkCycle > 3.02
      ? Math.sin(((blinkCycle - 3.02) / 0.18) * Math.PI)
      : 0;
  const eyeOpenFactor = Math.max(0.1, 1 - naturalBlink * 0.9);

  // Per-expression choreography
  let headRot: [number, number, number] = [0, Math.sin(t * 1.5) * 0.12, 0];
  let leftArmRotZ = -0.35 - Math.sin(t * 2.8) * 0.12;
  let rightArmRotZ = 0.35 + Math.cos(t * 2.8) * 0.12;
  let leftBrowOffset = 0.0;
  let leftBrowAngle = 0.0;
  let rightBrowOffset = 0.0;
  let rightBrowAngle = 0.0;
  let leftEyeScale: [number, number] = [1, eyeOpenFactor];
  let rightEyeScale: [number, number] = [1, eyeOpenFactor];
  let pupilOffsetX = Math.sin(t * 2.1) * 0.03;
  let pupilOffsetY = 0;

  if (expression === 'shock') {
    const jitter = frame < 20 ? Math.sin(frame * 2.8) * 0.07 : 0;
    headRot = [-0.12, jitter, 0];
    leftArmRotZ = -1.65 - Math.sin(t * 14) * 0.2;
    rightArmRotZ = 1.65 + Math.sin(t * 14) * 0.2;
    leftBrowOffset = 0.09;
    rightBrowOffset = 0.09;
    leftBrowAngle = 0.22;
    rightBrowAngle = -0.22;
    leftEyeScale = [1.24, 1.24];
    rightEyeScale = [1.24, 1.24];
    pupilOffsetX = 0;
    pupilOffsetY = 0.015;
  } else if (expression === 'skeptic') {
    headRot = [0.06, -0.22 + Math.sin(t * 1.8) * 0.06, 0.07];
    leftArmRotZ = -0.55;
    rightArmRotZ = 0.95 + Math.sin(t * 4) * 0.22;
    leftBrowOffset = 0.08;
    leftBrowAngle = 0.28;
    rightBrowOffset = -0.05;
    rightBrowAngle = -0.32;
    leftEyeScale = [1.05, 1.05 * eyeOpenFactor];
    rightEyeScale = [1.0, 0.52 * eyeOpenFactor];
    pupilOffsetX = 0.055;
  } else if (expression === 'star_eyes') {
    headRot = [-0.06, Math.sin(t * 2.2) * 0.14, 0];
    leftArmRotZ = -1.1 - Math.sin(t * 7) * 0.25;
    rightArmRotZ = 1.1 + Math.sin(t * 7) * 0.25;
    leftBrowOffset = 0.07;
    rightBrowOffset = 0.07;
    leftBrowAngle = 0.16;
    rightBrowAngle = -0.16;
    leftEyeScale = [1.14, 1.14 * eyeOpenFactor];
    rightEyeScale = [1.14, 1.14 * eyeOpenFactor];
  } else if (expression === 'laser_focus') {
    headRot = [0.04, Math.sin(t * 2.4) * 0.18, -0.04];
    leftArmRotZ = -0.75 - Math.sin(t * 5) * 0.28;
    rightArmRotZ = 0.75 + Math.cos(t * 5) * 0.28;
    leftBrowOffset = -0.04;
    rightBrowOffset = -0.04;
    leftBrowAngle = -0.26;
    rightBrowAngle = 0.26;
    leftEyeScale = [1.12, 0.66 * eyeOpenFactor];
    rightEyeScale = [1.12, 0.66 * eyeOpenFactor];
  } else if (expression === 'happy_wink') {
    headRot = [0.04, 0.12, -0.08];
    leftArmRotZ = -0.45;
    rightArmRotZ = 1.55 + Math.sin(t * 10) * 0.35;
    leftBrowOffset = 0.06;
    rightBrowOffset = 0.05;
    leftBrowAngle = 0.18;
    rightBrowAngle = -0.15;
    leftEyeScale = [1.12, 1.12];
    rightEyeScale = [1.12, 0.22];
  }

  const obsidian = '#141B2D';
  const darkChrome = '#334155';
  const visorGlass = '#02040A';
  const scanOffset = interpolate((frame % 42), [0, 42], [-0.45, 0.45]);

  return (
    <group
      position={[position[0], position[1] + hoverY, position[2]]}
      rotation={[0, 0, bodyTiltZ]}
      scale={scale}
    >
      {/* ORBITING NEON BACK HALO */}
      <group position={[0, 0.85, -0.65]}>
        <mesh rotation={[0.2, 0.1, t * 0.7]}>
          <torusGeometry args={[1.45, 0.025, 12, 6]} />
          <meshStandardMaterial
            color={accentColor}
            emissive={accentColor}
            emissiveIntensity={2.2}
          />
        </mesh>
        <mesh rotation={[-0.25, -0.15, -t * 0.55]}>
          <torusGeometry args={[1.65, 0.015, 12, 48]} />
          <meshStandardMaterial
            color="#FFFFFF"
            emissive={accentColor}
            emissiveIntensity={1.6}
          />
        </mesh>
      </group>

      {/* HEAD & EXPRESSIVE VISOR */}
      <group position={[0, 0.92, 0]} rotation={headRot}>
        {/* Sleek Wide Obsidian Head Shell */}
        <mesh scale={[1.18, 0.92, 0.95]}>
          <sphereGeometry args={[0.72, 40, 40]} />
          <meshStandardMaterial color={obsidian} roughness={0.22} metalness={0.68} />
        </mesh>

        {/* Neon Rim Trim Around Head */}
        <mesh position={[0, 0, 0.05]} rotation={[0.08, 0, 0]} scale={[1.18, 0.92, 1]}>
          <torusGeometry args={[0.72, 0.022, 14, 48]} />
          <meshStandardMaterial
            color={accentColor}
            emissive={accentColor}
            emissiveIntensity={2.4}
          />
        </mesh>

        {/* Twin Neon Antenna Horns */}
        {[-0.52, 0.52].map((x, idx) => (
          <group key={idx} position={[x, 0.62, -0.04]} rotation={[0, 0, x > 0 ? -0.32 : 0.32]}>
            <mesh position={[0, 0.15, 0]}>
              <cylinderGeometry args={[0.024, 0.036, 0.3, 12]} />
              <meshStandardMaterial color={darkChrome} metalness={0.85} roughness={0.2} />
            </mesh>
            <mesh position={[0, 0.32, 0]}>
              <sphereGeometry args={[0.068, 16, 16]} />
              <meshStandardMaterial
                color={accentColor}
                emissive={accentColor}
                emissiveIntensity={2.6 + Math.sin(t * 10 + idx) * 0.6}
              />
            </mesh>
          </group>
        ))}

        {/* Side Audio Ear Pods */}
        {[-0.86, 0.86].map((x, idx) => (
          <group key={idx} position={[x, 0.02, 0]}>
            <mesh rotation={[0, 0, Math.PI / 2]}>
              <cylinderGeometry args={[0.19, 0.19, 0.14, 24]} />
              <meshStandardMaterial color={darkChrome} roughness={0.25} metalness={0.85} />
            </mesh>
            <mesh position={[x > 0 ? 0.08 : -0.08, 0, 0]} rotation={[0, Math.PI / 2, 0]}>
              <torusGeometry args={[0.13, 0.024, 12, 28]} />
              <meshStandardMaterial
                color={accentColor}
                emissive={accentColor}
                emissiveIntensity={2.2}
              />
            </mesh>
          </group>
        ))}

        {/* Deep Black Panoramic Screen Visor */}
        <mesh position={[0, 0.02, 0.25]} scale={[1.12, 0.78, 0.85]}>
          <sphereGeometry args={[0.64, 48, 48]} />
          <meshStandardMaterial color={visorGlass} roughness={0.05} metalness={0.95} />
        </mesh>

        {/* EXPRESSIVE LED EYES + ARTICULATED BROWS */}
        <group position={[0, 0.05, 0.79]}>
          {/* Left Eye (-0.27) & Right Eye (+0.27) */}
          {[-0.27, 0.27].map((ex, idx) => {
            const isRight = idx === 1;
            const eScale = isRight ? rightEyeScale : leftEyeScale;
            const browY = 0.24 + (isRight ? rightBrowOffset : leftBrowOffset);
            const browRot = isRight ? rightBrowAngle : leftBrowAngle;

            return (
              <group key={idx} position={[ex, 0, 0]}>
                {/* Eyebrow LED Bar */}
                <mesh position={[0, browY, 0.02]} rotation={[0, 0, browRot]}>
                  <boxGeometry args={[0.24, 0.045, 0.03]} />
                  <meshStandardMaterial
                    color="#FFFFFF"
                    emissive={accentColor}
                    emissiveIntensity={2.4}
                  />
                </mesh>

                {/* Main Glowing LED Eye */}
                <group scale={[eScale[0], eScale[1], 1]}>
                  {/* Outer Glowing Ring / Iris */}
                  <mesh position={[0, 0, 0]}>
                    <sphereGeometry args={[0.165, 28, 28]} />
                    <meshStandardMaterial
                      color={accentColor}
                      emissive={accentColor}
                      emissiveIntensity={2.2}
                    />
                  </mesh>

                  {/* Bright White Expressive Pupil */}
                  <mesh position={[pupilOffsetX, pupilOffsetY, 0.08]}>
                    <sphereGeometry args={[0.095, 20, 20]} />
                    <meshBasicMaterial color="#FFFFFF" />
                  </mesh>

                  {/* Starburst Overlay for star_eyes */}
                  {expression === 'star_eyes' && (
                    <mesh position={[0, 0, 0.13]} rotation={[0, 0, t * 3 + idx]}>
                      <octahedronGeometry args={[0.075, 0]} />
                      <meshBasicMaterial color="#FFFFFF" />
                    </mesh>
                  )}

                  {/* Catchlight Sparkle */}
                  <mesh position={[0.055, 0.06, 0.145]}>
                    <sphereGeometry args={[0.032, 12, 12]} />
                    <meshBasicMaterial color="#FFFFFF" />
                  </mesh>
                </group>
              </group>
            );
          })}

          {/* Laser Scan Beam Across Visor during laser_focus */}
          {expression === 'laser_focus' && (
            <mesh position={[scanOffset, 0.01, 0.12]}>
              <boxGeometry args={[0.025, 0.34, 0.02]} />
              <meshBasicMaterial color="#FFFFFF" transparent opacity={0.85} />
            </mesh>
          )}

          {/* Voice Equalizer Mouth Bars (5 LED segments) */}
          <group position={[0, -0.25, -0.02]}>
            {[-2, -1, 0, 1, 2].map((b) => {
              const barH = speaking
                ? 0.035 + Math.abs(Math.sin(t * 18 + b * 1.3)) * 0.085
                : 0.032;
              return (
                <mesh key={b} position={[b * 0.07, 0, 0]}>
                  <boxGeometry args={[0.042, barH, 0.03]} />
                  <meshStandardMaterial
                    color="#FFFFFF"
                    emissive={accentColor}
                    emissiveIntensity={2.3}
                  />
                </mesh>
              );
            })}
          </group>
        </group>
      </group>

      {/* SLEEK TORSO & CHEST REACTOR */}
      <group position={[0, -0.02, 0]}>
        <mesh>
          <capsuleGeometry args={[0.41, 0.42, 16, 32]} />
          <meshStandardMaterial color={obsidian} roughness={0.28} metalness={0.65} />
        </mesh>

        {/* Glowing Chest Ring Reactor */}
        <mesh position={[0, 0.09, 0.42]}>
          <torusGeometry args={[0.14, 0.028, 12, 32]} />
          <meshStandardMaterial
            color={accentColor}
            emissive={accentColor}
            emissiveIntensity={2.5}
          />
        </mesh>
        <mesh position={[0, 0.09, 0.42]}>
          <sphereGeometry args={[0.07, 16, 16]} />
          <meshBasicMaterial color="#FFFFFF" />
        </mesh>

        {/* Belt Trim */}
        <mesh position={[0, -0.25, 0]} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[0.42, 0.04, 12, 36]} />
          <meshStandardMaterial
            color={darkChrome}
            emissive={accentColor}
            emissiveIntensity={0.45}
            metalness={0.85}
          />
        </mesh>
      </group>

      {/* LEFT ARM */}
      <group position={[-0.54, 0.16, 0]} rotation={[0, 0, leftArmRotZ]}>
        <mesh position={[-0.12, -0.18, 0]} rotation={[0, 0, -0.2]}>
          <capsuleGeometry args={[0.11, 0.32, 12, 20]} />
          <meshStandardMaterial color={obsidian} roughness={0.28} metalness={0.65} />
        </mesh>
        <mesh position={[-0.2, -0.44, 0]}>
          <sphereGeometry args={[0.135, 18, 18]} />
          <meshStandardMaterial
            color={darkChrome}
            emissive={accentColor}
            emissiveIntensity={0.8}
            metalness={0.75}
          />
        </mesh>
      </group>

      {/* RIGHT ARM */}
      <group position={[0.54, 0.16, 0]} rotation={[0, 0, rightArmRotZ]}>
        <mesh position={[0.12, -0.18, 0]} rotation={[0, 0, 0.2]}>
          <capsuleGeometry args={[0.11, 0.32, 12, 20]} />
          <meshStandardMaterial color={obsidian} roughness={0.28} metalness={0.65} />
        </mesh>
        <mesh position={[0.2, -0.44, 0]}>
          <sphereGeometry args={[0.135, 18, 18]} />
          <meshStandardMaterial
            color={darkChrome}
            emissive={accentColor}
            emissiveIntensity={0.8}
            metalness={0.75}
          />
        </mesh>
      </group>

      {/* HOVER BOOTS + NEON THRUSTERS */}
      {[-0.2, 0.2].map((x, idx) => (
        <group key={idx} position={[x, -0.68, 0]}>
          <mesh>
            <capsuleGeometry args={[0.125, 0.24, 12, 20]} />
            <meshStandardMaterial color={obsidian} roughness={0.3} metalness={0.6} />
          </mesh>
          <mesh position={[0, -0.22, 0]} rotation={[Math.PI, 0, 0]}>
            <coneGeometry args={[0.09, 0.26 + Math.sin(t * 24 + idx) * 0.05, 16]} />
            <meshBasicMaterial color={accentColor} transparent opacity={0.88} />
          </mesh>
        </group>
      ))}
    </group>
  );
};
