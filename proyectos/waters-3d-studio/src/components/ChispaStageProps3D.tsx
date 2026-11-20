import React, { useMemo } from 'react';
import { spring } from 'remotion';
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

export const StudioFloor3D: React.FC<{
  floorColor?: string;
  charPos?: [number, number, number];
  charJumpHeight?: number;
  floorY?: number;
}> = ({
  floorColor = '#282E3B',
  charPos = [0, 0, 0],
  charJumpHeight = 0,
  floorY = -1.35,
}) => {
  const shadowScale = Math.max(0.65, 1 - charJumpHeight * 0.6);

  return (
    <group>
      {/* Large seamless studio table / cyc floor */}
      <mesh position={[0, floorY, -1.0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[28, 22]} />
        <meshStandardMaterial color={floorColor} roughness={0.62} metalness={0.14} />
      </mesh>

      {/* Soft back horizon strip for studio cyclorama gradient */}
      <mesh position={[0, floorY + 0.02, -6.5]}>
        <planeGeometry args={[28, 0.6]} />
        <meshBasicMaterial color="#020308" transparent opacity={0.55} />
      </mesh>

      {/* Contact shadow under Astronautita Chispa */}
      <mesh
        position={[charPos[0], floorY + 0.012, charPos[2] + 0.05]}
        rotation={[-Math.PI / 2, 0, 0]}
        scale={[1.15 * shadowScale, 0.78 * shadowScale, 1]}
      >
        <circleGeometry args={[0.92, 32]} />
        <meshBasicMaterial color="#030408" transparent opacity={0.42 * shadowScale} />
      </mesh>
    </group>
  );
};

export const SilverLaptop3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
  position?: [number, number, number];
  rotationY?: number;
  scale?: number;
  accentColor?: string;
}> = ({
  frame,
  localFrame,
  fps,
  position = [1.0, -1.33, -0.35],
  rotationY = -0.35,
  scale = 1,
  accentColor = '#00F5D4',
}) => {
  const t = frame / fps;
  const pop = spring({
    frame: Math.max(0, localFrame - 6),
    fps,
    config: { damping: 12, stiffness: 200 },
  });

  const baseGeo = useMemo(
    () => new RoundedBoxGeometry(1.55, 0.06, 1.02, 4, 0.02),
    []
  );

  // Subtle scrolling code bars on the laptop screen
  const scanBar = ((frame % 24) / 24) * 0.55;

  return (
    <group
      position={position}
      rotation={[0, rotationY, 0]}
      scale={scale * Math.max(0.001, pop)}
    >
      {/* Contact shadow under laptop */}
      <mesh position={[0, 0.008, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[1.75, 1.25]} />
        <meshBasicMaterial color="#020308" transparent opacity={0.4} />
      </mesh>

      {/* Silver MacBook Base */}
      <mesh position={[0, 0.03, 0]} geometry={baseGeo} castShadow receiveShadow>
        <meshStandardMaterial color="#CBD5E1" metalness={0.78} roughness={0.28} />
      </mesh>
      {/* Dark Keyboard Recessed Pad */}
      <mesh position={[0, 0.062, -0.06]}>
        <boxGeometry args={[1.32, 0.01, 0.56]} />
        <meshStandardMaterial color="#111827" roughness={0.6} />
      </mesh>
      {/* Trackpad */}
      <mesh position={[0, 0.062, 0.31]}>
        <boxGeometry args={[0.52, 0.008, 0.24]} />
        <meshStandardMaterial color="#94A3B8" metalness={0.5} roughness={0.4} />
      </mesh>

      {/* Hinged Display Lid with Luminous White Edge Border (like @lynxstudiosbcn!) */}
      <group position={[0, 0.05, -0.49]} rotation={[-0.22, 0, 0]}>
        {/* Outer White Rim Glow */}
        <mesh position={[0, 0.52, -0.01]}>
          <boxGeometry args={[1.58, 1.04, 0.03]} />
          <meshStandardMaterial
            color="#FFFFFF"
            emissive="#FFFFFF"
            emissiveIntensity={1.25}
          />
        </mesh>
        {/* Black Screen Interior */}
        <mesh position={[0, 0.52, 0.01]}>
          <boxGeometry args={[1.48, 0.94, 0.02]} />
          <meshStandardMaterial color="#050811" roughness={0.18} metalness={0.2} />
        </mesh>

        {/* Traffic Lights on Miniature Terminal */}
        {[
          [-0.64, '#FF5F56'],
          [-0.57, '#FFBD2E'],
          [-0.50, '#27C93F'],
        ].map(([dx, col], i) => (
          <mesh key={i} position={[dx as number, 0.91, 0.025]}>
            <sphereGeometry args={[0.02, 10, 10]} />
            <meshBasicMaterial color={col as string} />
          </mesh>
        ))}

        {/* Typing Code Lines Inside Screen */}
        {[0.76, 0.64, 0.52, 0.40, 0.28].map((ly, li) => {
          const lineW = Math.max(
            0.05,
            ((Math.sin(t * 9 + li * 1.7) * 0.5 + 0.5) * 0.65 + 0.35) * 1.15
          );
          return (
            <mesh
              key={li}
              position={[-0.62 + lineW / 2, ly, 0.025]}
            >
              <boxGeometry args={[lineW, 0.042, 0.008]} />
              <meshBasicMaterial
                color={li % 2 === 0 ? accentColor : '#94A3B8'}
              />
            </mesh>
          );
        })}

        {/* Active Blinking Cursor Line */}
        <mesh position={[-0.56 + scanBar, 0.16, 0.026]}>
          <boxGeometry args={[0.045, 0.055, 0.01]} />
          <meshBasicMaterial color="#22C55E" />
        </mesh>
      </group>
    </group>
  );
};

export const FloatingHouseDiorama3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
  position?: [number, number, number];
  scale?: number;
}> = ({
  frame,
  localFrame,
  fps,
  position = [1.05, -0.35, -0.25],
  scale = 1,
}) => {
  const t = frame / fps;
  const pop = spring({
    frame: Math.max(0, localFrame - 10),
    fps,
    config: { damping: 10, stiffness: 185 },
  });
  const floatY = Math.sin(t * 2.8) * 0.12;
  const swayZ = Math.sin(t * 1.9) * 0.06;

  const balloons: { pos: [number, number, number]; r: number; col: string }[] = [
    { pos: [0, 1.05, 0], r: 0.21, col: '#00F5D4' },
    { pos: [-0.24, 0.94, 0.12], r: 0.18, col: '#FF4D6D' },
    { pos: [0.25, 0.92, 0.1], r: 0.18, col: '#FFD166' },
    { pos: [-0.14, 1.24, -0.08], r: 0.17, col: '#38BDF8' },
    { pos: [0.16, 1.22, -0.06], r: 0.17, col: '#A855F7' },
    { pos: [-0.32, 1.12, -0.14], r: 0.15, col: '#22C55E' },
    { pos: [0.33, 1.10, -0.12], r: 0.15, col: '#FB923C' },
  ];

  return (
    <group
      position={[position[0], position[1] + floatY, position[2]]}
      rotation={[0, -0.28, swayZ]}
      scale={scale * Math.max(0.001, pop)}
    >
      {/* Cute House Base */}
      <mesh position={[0, 0, 0]} castShadow>
        <boxGeometry args={[0.72, 0.56, 0.62]} />
        <meshStandardMaterial color="#FFF7E8" roughness={0.45} />
      </mesh>
      {/* Turquoise & Coral Trim Floor */}
      <mesh position={[0, -0.30, 0]}>
        <boxGeometry args={[0.82, 0.08, 0.72]} />
        <meshStandardMaterial color="#38BDF8" roughness={0.35} />
      </mesh>
      {/* Pitched Gable Roof */}
      <mesh position={[0, 0.44, 0]} rotation={[0, Math.PI / 4, 0]}>
        <coneGeometry args={[0.58, 0.44, 4]} />
        <meshStandardMaterial color="#FF5D73" roughness={0.35} />
      </mesh>
      {/* Warm Glowing Front Windows & Door */}
      <mesh position={[-0.17, 0.04, 0.315]}>
        <boxGeometry args={[0.16, 0.16, 0.02]} />
        <meshStandardMaterial
          color="#FDE047"
          emissive="#FACC15"
          emissiveIntensity={1.6}
        />
      </mesh>
      <mesh position={[0.17, 0.04, 0.315]}>
        <boxGeometry args={[0.16, 0.16, 0.02]} />
        <meshStandardMaterial
          color="#FDE047"
          emissive="#FACC15"
          emissiveIntensity={1.6}
        />
      </mesh>
      <mesh position={[0, -0.12, 0.315]}>
        <boxGeometry args={[0.15, 0.26, 0.02]} />
        <meshStandardMaterial color="#8B5A3C" roughness={0.6} />
      </mesh>

      {/* Strings + Glossy Colorful Balloons Lifting the House */}
      {balloons.map((b, i) => (
        <group key={i}>
          <mesh position={[b.pos[0] * 0.45, (b.pos[1] + 0.5) * 0.5, b.pos[2] * 0.45]}>
            <cylinderGeometry args={[0.008, 0.008, b.pos[1] - 0.35, 6]} />
            <meshBasicMaterial color="#CBD5E1" transparent opacity={0.75} />
          </mesh>
          <mesh position={b.pos} scale={[1, 1.15, 1]}>
            <sphereGeometry args={[b.r, 18, 18]} />
            <meshStandardMaterial
              color={b.col}
              emissive={b.col}
              emissiveIntensity={0.45}
              roughness={0.18}
              metalness={0.12}
            />
          </mesh>
        </group>
      ))}
    </group>
  );
};

export const Gta6ViceCityDiorama3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
  position?: [number, number, number];
  scale?: number;
}> = ({
  frame,
  localFrame,
  fps,
  position = [0.95, -0.78, -0.45],
  scale = 1,
}) => {
  const t = frame / fps;
  const pop = spring({
    frame: Math.max(0, localFrame - 8),
    fps,
    config: { damping: 11, stiffness: 195 },
  });

  // Animated vehicles cruising in the 3D GTA 6 clone!
  const carZ = ((t * 1.4) % 1.9) - 0.95;
  const taxiZ = -(((t * 1.1) % 1.9) - 0.95);
  const boatX = Math.sin(t * 1.6) * 0.45;
  const planeAngle = t * 1.8;

  const baseGeo = useMemo(
    () => new RoundedBoxGeometry(2.15, 0.14, 2.15, 4, 0.05),
    []
  );

  return (
    <group
      position={position}
      rotation={[0.28, -0.58 + Math.sin(t * 0.8) * 0.06, 0]}
      scale={scale * Math.max(0.001, pop)}
    >
      {/* Isometric Base Slab (like the 3D Virtual Office diorama!) */}
      <mesh geometry={baseGeo} castShadow receiveShadow>
        <meshStandardMaterial color="#1A2234" roughness={0.4} metalness={0.35} />
      </mesh>
      {/* Neon Trim Frame Around Map */}
      <mesh position={[0, 0.075, 0]}>
        <boxGeometry args={[2.18, 0.025, 2.18]} />
        <meshStandardMaterial
          color="#DFB15B"
          emissive="#DFB15B"
          emissiveIntensity={0.65}
        />
      </mesh>

      {/* Ocean Strip (Right side of Vice City) */}
      <mesh position={[0.68, 0.085, 0]}>
        <boxGeometry args={[0.70, 0.02, 2.02]} />
        <meshStandardMaterial
          color="#0284C7"
          emissive="#00F5D4"
          emissiveIntensity={0.45}
          roughness={0.12}
        />
      </mesh>
      {/* Speedboat Cruising */}
      <mesh position={[0.68 + boatX * 0.25, 0.14, Math.sin(t * 2.2) * 0.6]}>
        <boxGeometry args={[0.14, 0.08, 0.34]} />
        <meshStandardMaterial
          color="#FFFFFF"
          emissive="#38BDF8"
          emissiveIntensity={0.6}
        />
      </mesh>

      {/* Vice Beach Road + Dashed Neon Centerline */}
      <mesh position={[0.02, 0.086, 0]}>
        <boxGeometry args={[0.48, 0.02, 2.02]} />
        <meshStandardMaterial color="#0F172A" roughness={0.6} />
      </mesh>
      {[-0.72, -0.36, 0, 0.36, 0.72].map((dz, di) => (
        <mesh key={di} position={[0.02, 0.10, dz]}>
          <boxGeometry args={[0.04, 0.01, 0.18]} />
          <meshBasicMaterial color="#FACC15" />
        </mesh>
      ))}

      {/* Red Sports Car & Yellow Taxi Moving Live */}
      <mesh position={[-0.08, 0.14, carZ]}>
        <boxGeometry args={[0.15, 0.09, 0.28]} />
        <meshStandardMaterial
          color="#FF2E63"
          emissive="#FF2E63"
          emissiveIntensity={0.65}
        />
      </mesh>
      <mesh position={[0.13, 0.14, taxiZ]}>
        <boxGeometry args={[0.15, 0.09, 0.26]} />
        <meshStandardMaterial
          color="#FACC15"
          emissive="#DFB15B"
          emissiveIntensity={0.55}
        />
      </mesh>

      {/* Neon Vice High-Rises (Left City Block) */}
      {[
        [-0.62, 0.38, -0.58, 0.38, 0.62, '#A855F7'],
        [-0.58, 0.52, 0.08, 0.42, 0.88, '#00F5D4'],
        [-0.62, 0.32, 0.68, 0.34, 0.48, '#FF4D8D'],
      ].map(([bx, bh, bz, bw, bl, col], bi) => (
        <group key={bi} position={[bx as number, (bh as number) + 0.08, bz as number]}>
          <mesh>
            <boxGeometry args={[bw as number, (bh as number) * 2, bw as number]} />
            <meshStandardMaterial color="#1E293B" roughness={0.28} metalness={0.5} />
          </mesh>
          <mesh position={[0, bh as number, 0]}>
            <boxGeometry args={[(bw as number) + 0.03, 0.06, (bw as number) + 0.03]} />
            <meshStandardMaterial
              color={col as string}
              emissive={col as string}
              emissiveIntensity={1.6}
            />
          </mesh>
        </group>
      ))}

      {/* Miniature Palm Trees */}
      {[
        [0.32, -0.65],
        [0.32, 0.05],
        [0.32, 0.70],
      ].map(([px, pz], pi) => (
        <group key={pi} position={[px, 0.09, pz]}>
          <mesh position={[0, 0.15, 0]}>
            <cylinderGeometry args={[0.02, 0.03, 0.30, 8]} />
            <meshStandardMaterial color="#92400E" />
          </mesh>
          <mesh position={[0, 0.32, 0]}>
            <sphereGeometry args={[0.11, 10, 10]} />
            <meshStandardMaterial color="#22C55E" emissive="#16A34A" emissiveIntensity={0.35} />
          </mesh>
        </group>
      ))}

      {/* Circular Flying Mini-Plane Overhead */}
      <group
        position={[
          Math.cos(planeAngle) * 0.72,
          1.22 + Math.sin(t * 3) * 0.06,
          Math.sin(planeAngle) * 0.72,
        ]}
        rotation={[0, -planeAngle, 0.25]}
      >
        <mesh>
          <boxGeometry args={[0.08, 0.06, 0.28]} />
          <meshStandardMaterial color="#F8FAFC" emissive="#38BDF8" emissiveIntensity={0.5} />
        </mesh>
        <mesh>
          <boxGeometry args={[0.38, 0.02, 0.10]} />
          <meshStandardMaterial color="#00F5D4" emissive="#00F5D4" emissiveIntensity={0.8} />
        </mesh>
      </group>
    </group>
  );
};

export const GoldenKitBox3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
  position?: [number, number, number];
}> = ({ frame, localFrame, fps, position = [-1.05, -0.82, -0.1] }) => {
  const t = frame / fps;
  const pop = spring({
    frame: Math.max(0, localFrame - 6),
    fps,
    config: { damping: 11, stiffness: 190 },
  });

  const boxGeo = useMemo(
    () => new RoundedBoxGeometry(1.05, 0.96, 0.92, 4, 0.08),
    []
  );

  return (
    <group
      position={position}
      rotation={[0, 0.32 + Math.sin(t * 2) * 0.05, 0]}
      scale={Math.max(0.001, pop)}
    >
      {/* Sleek Black Box */}
      <mesh geometry={boxGeo} castShadow>
        <meshStandardMaterial color="#0A0D14" roughness={0.35} metalness={0.4} />
      </mesh>
      {/* Golden Frame Trim */}
      <mesh position={[0, 0, 0.465]}>
        <boxGeometry args={[0.92, 0.82, 0.02]} />
        <meshStandardMaterial color="#111622" roughness={0.3} />
      </mesh>
      <mesh position={[0, 0.36, 0.48]}>
        <boxGeometry args={[0.84, 0.04, 0.02]} />
        <meshStandardMaterial color="#FACC15" emissive="#DFB15B" emissiveIntensity={1.2} />
      </mesh>
      {/* Front Gold Typography Block Emblem ("KIT · HYDROGEN") */}
      <mesh position={[0, 0.21, 0.485]}>
        <boxGeometry args={[0.56, 0.055, 0.015]} />
        <meshStandardMaterial color="#E2E8F0" emissive="#94A3B8" emissiveIntensity={0.45} />
      </mesh>
      <mesh position={[0, 0.03, 0.485]}>
        <boxGeometry args={[0.74, 0.16, 0.02]} />
        <meshStandardMaterial color="#FACC15" emissive="#DFB15B" emissiveIntensity={1.45} />
      </mesh>
      <mesh position={[0, -0.36, 0.48]}>
        <boxGeometry args={[0.84, 0.04, 0.02]} />
        <meshStandardMaterial color="#FACC15" emissive="#DFB15B" emissiveIntensity={1.2} />
      </mesh>
      {/* 3 Subagent Colored Dots (Cyan, Gold, Coral) */}
      {[
        [-0.16, '#38BDF8'],
        [0, '#FACC15'],
        [0.16, '#FF4D6D'],
      ].map(([dx, c], i) => (
        <mesh key={i} position={[dx as number, -0.22, 0.485]}>
          <sphereGeometry args={[0.042, 12, 12]} />
          <meshStandardMaterial
            color={c as string}
            emissive={c as string}
            emissiveIntensity={1.5}
          />
        </mesh>
      ))}
      {/* Slightly Open Gold Lid + Floating Cards */}
      <mesh position={[0, 0.56, -0.05]} rotation={[-0.28, 0, 0]}>
        <boxGeometry args={[1.12, 0.12, 1.0]} />
        <meshStandardMaterial color="#DFB15B" metalness={0.75} roughness={0.22} />
      </mesh>
      {[
        [-0.22, 0.68, '#38BDF8'],
        [0, 0.74, '#FACC15'],
        [0.22, 0.66, '#22C55E'],
      ].map(([cx, cy, ccol], ci) => (
        <mesh
          key={ci}
          position={[cx as number, (cy as number) + Math.sin(t * 4 + ci) * 0.04, 0]}
          rotation={[0, 0, (ci - 1) * -0.12]}
        >
          <boxGeometry args={[0.26, 0.34, 0.03]} />
          <meshStandardMaterial
            color={ccol as string}
            emissive={ccol as string}
            emissiveIntensity={0.45}
          />
        </mesh>
      ))}
    </group>
  );
};

/**
 * Evil dark-chrome Terminator-style AI villain robot with glowing red LED eyes,
 * crimson laser visor scanner, phone voice-spoofing prop, and hangup block barrier.
 */
export const EvilTerminatorBot3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
  position?: [number, number, number];
  rotationY?: number;
  scale?: number;
  blocked?: boolean;
}> = ({
  frame,
  localFrame,
  fps,
  position = [0.92, -0.22, 0.05],
  rotationY = -0.32,
  scale = 0.96,
  blocked = true,
}) => {
  const t = frame / fps;
  const pop = spring({
    frame: Math.max(0, localFrame - 4),
    fps,
    config: { damping: 10, stiffness: 210 },
  });
  const blockSpring = spring({
    frame: Math.max(0, localFrame - 24),
    fps,
    config: { damping: 9, stiffness: 260 },
  });

  const geos = useMemo(
    () => ({
      skull: new RoundedBoxGeometry(1.30, 1.04, 0.88, 4, 0.14),
      visorInset: new RoundedBoxGeometry(1.06, 0.56, 0.16, 3, 0.08),
      torso: new RoundedBoxGeometry(1.08, 0.44, 0.70, 4, 0.10),
      arm: new RoundedBoxGeometry(0.19, 0.36, 0.19, 3, 0.06),
      leg: new RoundedBoxGeometry(0.20, 0.32, 0.24, 3, 0.06),
    }),
    []
  );

  const gunmetal = '#4B5565';
  const darkSteel = '#11151E';
  const chrome = '#CBD5E1';
  const crimson = '#FF1E2D';
  const hover = Math.sin(t * 6.0) * 0.035;
  const scanX = Math.sin(t * 7.5) * 0.34;
  const ringPulse = (t * 1.9) % 1;

  return (
    <group
      position={[position[0], position[1] + hover, position[2]]}
      rotation={[0, rotationY, blocked && localFrame >= 24 ? -0.09 : 0]}
      scale={scale * Math.max(0.001, pop)}
    >
      {/* Dedicated crimson/steel rim light so dark chrome T-800 gleams cleanly */}
      <pointLight position={[0.4, 0.9, 1.2]} intensity={2.2} color="#E2E8F0" />
      <pointLight position={[0, 0.3, 1.0]} intensity={1.8} color="#FF2E3B" />
      {/* Contact shadow under villain bot */}
      <mesh position={[0, -0.81, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[0.82, 28]} />
        <meshBasicMaterial color="#020308" transparent opacity={0.44} />
      </mesh>

      {/* EVIL ANGULAR CHROME HEAD */}
      <group position={[0, 0.34, 0]}>
        <mesh geometry={geos.skull} castShadow>
          <meshStandardMaterial color={gunmetal} metalness={0.82} roughness={0.22} />
        </mesh>

        {/* Armored Cheek Blades & Red Ear Sensors */}
        {[-0.69, 0.69].map((ex, i) => (
          <mesh key={i} position={[ex, 0.04, 0]} rotation={[0, 0, Math.PI / 2]}>
            <cylinderGeometry args={[0.14, 0.14, 0.10, 18]} />
            <meshStandardMaterial color={crimson} emissive={crimson} emissiveIntensity={1.6} />
          </mesh>
        ))}

        {/* Dark Recessed Optical Faceplate */}
        <mesh position={[0, 0.05, 0.40]} geometry={geos.visorInset}>
          <meshStandardMaterial color={darkSteel} metalness={0.7} roughness={0.18} />
        </mesh>

        {/* Intense Glowing Blood-Red Terminator LED Eyes */}
        {[-0.24, 0.24].map((ex, i) => (
          <group key={i} position={[ex, 0.06, 0.49]}>
            <mesh>
              <sphereGeometry args={[0.095, 18, 18]} />
              <meshStandardMaterial
                color={crimson}
                emissive={crimson}
                emissiveIntensity={3.0}
              />
            </mesh>
            <mesh position={[0, 0, 0.055]}>
              <sphereGeometry args={[0.042, 12, 12]} />
              <meshBasicMaterial color="#FFD1D1" />
            </mesh>
            {/* Angry Metallic Brow Slash (\ /) */}
            <mesh position={[0, 0.13, 0.02]} rotation={[0, 0, i === 0 ? -0.34 : 0.34]}>
              <boxGeometry args={[0.25, 0.045, 0.05]} />
              <meshStandardMaterial color={chrome} metalness={0.9} roughness={0.18} />
            </mesh>
          </group>
        ))}

        {/* Sweeping Red Scanner Dot Across Visor */}
        <mesh position={[scanX, 0.05, 0.50]}>
          <boxGeometry args={[0.05, 0.36, 0.015]} />
          <meshBasicMaterial color="#FF4D4D" transparent opacity={0.55} />
        </mesh>

        {/* Metallic Jaw Grille Teeth */}
        <mesh position={[0, -0.32, 0.45]}>
          <boxGeometry args={[0.56, 0.14, 0.05]} />
          <meshStandardMaterial color={darkSteel} metalness={0.8} roughness={0.3} />
        </mesh>
        {[-0.18, -0.09, 0, 0.09, 0.18].map((tx, ti) => (
          <mesh key={ti} position={[tx, -0.32, 0.48]}>
            <boxGeometry args={[0.032, 0.11, 0.02]} />
            <meshStandardMaterial color={chrome} metalness={0.9} roughness={0.2} />
          </mesh>
        ))}
      </group>

      {/* ARMORED TORSO + CRIMSON REACTOR */}
      <group position={[0, -0.32, 0]}>
        <mesh geometry={geos.torso} castShadow>
          <meshStandardMaterial color={gunmetal} metalness={0.82} roughness={0.25} />
        </mesh>
        <mesh position={[0, 0.04, 0.36]}>
          <torusGeometry args={[0.12, 0.025, 12, 24]} />
          <meshStandardMaterial color={crimson} emissive={crimson} emissiveIntensity={2.4} />
        </mesh>
        <mesh position={[0, 0.04, 0.36]}>
          <sphereGeometry args={[0.06, 14, 14]} />
          <meshBasicMaterial color="#FFB4B4" />
        </mesh>
      </group>

      {/* LEFT ARM HOLDING SPOOFED SMARTPHONE + VOICE RINGS */}
      <group position={[-0.64, -0.18, 0.12]} rotation={[-0.75, 0.1, -0.25]}>
        <mesh position={[0, -0.14, 0]} geometry={geos.arm}>
          <meshStandardMaterial color={gunmetal} metalness={0.8} roughness={0.25} />
        </mesh>
        {/* Dark Smartphone emitting spoofed crimson rings */}
        <group position={[-0.08, -0.36, 0.12]} rotation={[0.4, 0, 0]}>
          <mesh>
            <boxGeometry args={[0.20, 0.34, 0.03]} />
            <meshStandardMaterial color="#090D16" metalness={0.5} />
          </mesh>
          <mesh position={[0, 0, 0.018]}>
            <boxGeometry args={[0.16, 0.28, 0.01]} />
            <meshBasicMaterial color={crimson} />
          </mesh>
          <mesh
            position={[0, 0, 0.04]}
            scale={0.55 + ringPulse * 1.1}
          >
            <torusGeometry args={[0.16, 0.018, 8, 24]} />
            <meshBasicMaterial
              color="#FF5555"
              transparent
              opacity={(1 - ringPulse) * 0.9}
            />
          </mesh>
        </group>
      </group>

      {/* RIGHT ARM */}
      <group position={[0.64, -0.18, 0]} rotation={[0, 0, 0.32]}>
        <mesh position={[0, -0.14, 0]} geometry={geos.arm}>
          <meshStandardMaterial color={gunmetal} metalness={0.8} roughness={0.25} />
        </mesh>
      </group>

      {/* 4 STURDY METALLIC BOOTS */}
      {[-0.36, -0.12, 0.12, 0.36].map((lx, i) => (
        <mesh key={i} position={[lx, -0.66, 0.02]} geometry={geos.leg}>
          <meshStandardMaterial color={darkSteel} metalness={0.85} roughness={0.3} />
        </mesh>
      ))}

      {/* POPPING 'HANGUP / CLONE BLOCKED' X BARRIER ABOVE BETWEEN BOTS */}
      {blocked && localFrame >= 24 && (
        <group
          position={[-0.78, 0.96, 0.28]}
          rotation={[0, 0.18, 0]}
          scale={0.76 * Math.max(0.001, blockSpring)}
        >
          <mesh>
            <torusGeometry args={[0.36, 0.045, 14, 32]} />
            <meshStandardMaterial
              color="#00F5D4"
              emissive="#00F5D4"
              emissiveIntensity={2.0}
            />
          </mesh>
          <mesh rotation={[0, 0, Math.PI / 4]}>
            <boxGeometry args={[0.48, 0.075, 0.05]} />
            <meshStandardMaterial color={crimson} emissive={crimson} emissiveIntensity={2.4} />
          </mesh>
          <mesh rotation={[0, 0, -Math.PI / 4]}>
            <boxGeometry args={[0.48, 0.075, 0.05]} />
            <meshStandardMaterial color={crimson} emissive={crimson} emissiveIntensity={2.4} />
          </mesh>
        </group>
      )}
    </group>
  );
};

/**
 * Animated 3D Smartphone Voice-Wave Pedestal showing voiceprint morphing from
 * natural cyan wave into crimson AI clone waveform.
 */
export const VoiceWaveClone3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
  position?: [number, number, number];
  scale?: number;
}> = ({
  frame,
  localFrame,
  fps,
  position = [0.92, -0.32, -0.05],
  scale = 0.96,
}) => {
  const t = frame / fps;
  const pop = spring({
    frame: Math.max(0, localFrame - 6),
    fps,
    config: { damping: 11, stiffness: 200 },
  });
  const isCloned = localFrame >= 28;
  const waveColor = isCloned ? '#FF3B3B' : '#00F5D4';

  return (
    <group
      position={position}
      rotation={[0, -0.35 + Math.sin(t * 1.4) * 0.06, 0]}
      scale={scale * Math.max(0.001, pop)}
    >
      {/* Sleek Circular Tech Base on Floor (relative y = -0.73 -> floorY = -1.05) */}
      <mesh position={[0, -0.68, 0]}>
        <cylinderGeometry args={[0.64, 0.72, 0.10, 32]} />
        <meshStandardMaterial color="#111827" metalness={0.7} roughness={0.3} />
      </mesh>
      <mesh position={[0, -0.63, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[0.65, 0.025, 12, 36]} />
        <meshStandardMaterial
          color={waveColor}
          emissive={waveColor}
          emissiveIntensity={2.0}
        />
      </mesh>

      {/* Floating Glass Smartphone Frame */}
      <mesh position={[0, 0.10, 0]}>
        <boxGeometry args={[0.98, 1.48, 0.09]} />
        <meshStandardMaterial color="#090D16" metalness={0.75} roughness={0.2} />
      </mesh>
      <mesh position={[0, 0.10, 0.05]}>
        <boxGeometry args={[0.86, 1.34, 0.015]} />
        <meshStandardMaterial color="#030712" roughness={0.1} />
      </mesh>

      {/* 7 Animated 3D Equalizer Bars Inside Phone */}
      {[-0.30, -0.20, -0.10, 0, 0.10, 0.20, 0.30].map((bx, idx) => {
        const barH =
          0.18 +
          Math.abs(Math.sin(t * 11 + idx * 0.9)) * 0.62 +
          Math.cos(t * 6 - idx) * 0.10;
        return (
          <mesh key={idx} position={[bx, 0.12, 0.08]}>
            <boxGeometry args={[0.065, Math.max(0.14, barH), 0.05]} />
            <meshStandardMaterial
              color={waveColor}
              emissive={waveColor}
              emissiveIntensity={2.2}
            />
          </mesh>
        );
      })}
    </group>
  );
};

/**
 * Rotating Hexagonal Cyber Shield + Padlock Vault on Pedestal
 */
export const ShieldVault3D: React.FC<{
  frame: number;
  localFrame: number;
  fps: number;
  position?: [number, number, number];
  accentColor?: string;
}> = ({
  frame,
  localFrame,
  fps,
  position = [0.92, -0.28, -0.05],
  accentColor = '#00F5D4',
}) => {
  const t = frame / fps;
  const pop = spring({
    frame: Math.max(0, localFrame - 6),
    fps,
    config: { damping: 11, stiffness: 205 },
  });
  const hover = Math.sin(t * 3.0) * 0.07;

  return (
    <group position={position} scale={Math.max(0.001, pop)}>
      {/* Base Pad on Studio Floor */}
      <mesh position={[0, -0.72, 0]}>
        <cylinderGeometry args={[0.60, 0.68, 0.10, 28]} />
        <meshStandardMaterial color="#0F172A" metalness={0.75} roughness={0.28} />
      </mesh>
      {/* Orbiting Neon Hexagon Shield Frame */}
      <group position={[0, hover + 0.05, 0]} rotation={[0, Math.sin(t * 1.5) * 0.28, 0]}>
        <mesh>
          <torusGeometry args={[0.62, 0.055, 12, 6]} />
          <meshStandardMaterial
            color={accentColor}
            emissive={accentColor}
            emissiveIntensity={2.1}
          />
        </mesh>
        {/* Golden Padlock Core Inside Shield */}
        <mesh position={[0, -0.08, 0]}>
          <boxGeometry args={[0.48, 0.40, 0.18]} />
          <meshStandardMaterial
            color="#FACC15"
            emissive="#DFB15B"
            emissiveIntensity={0.65}
            metalness={0.75}
            roughness={0.22}
          />
        </mesh>
        <mesh position={[0, 0.16, 0]}>
          <torusGeometry args={[0.15, 0.042, 12, 24, Math.PI]} />
          <meshStandardMaterial color="#F8FAFC" metalness={0.85} roughness={0.18} />
        </mesh>
      </group>
    </group>
  );
};
