import React, { useMemo } from 'react';
import { spring } from 'remotion';
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

export type ChispaExpression =
  | 'happy_open'
  | 'sad_cloud'
  | 'determined_hacker'
  | 'happy_arcs'
  | 'wink'
  | 'zen_proud'
  | 'shock_sweat'
  | 'star_eyes';

interface ChispaAstronaut3DProps {
  frame: number;
  localFrame: number;
  fps: number;
  expression: ChispaExpression;
  accentColor: string;
  position?: [number, number, number];
  rotationY?: number;
  scale?: number;
  speaking?: boolean;
  /** Frames within the beat where UI cards pop in — character hops & sparkles in sync */
  popFrames?: number[];
}

function createFourPointStarShape(outerR = 0.22, innerR = 0.065): THREE.Shape {
  const shape = new THREE.Shape();
  const points = 8;
  for (let i = 0; i < points; i++) {
    const r = i % 2 === 0 ? outerR : innerR;
    const angle = (i / points) * Math.PI * 2 - Math.PI / 2;
    const x = Math.cos(angle) * r;
    const y = Math.sin(angle) * r;
    if (i === 0) shape.moveTo(x, y);
    else shape.lineTo(x, y);
  }
  shape.closePath();
  return shape;
}

/**
 * Astronautita "Chispa" 3D — coleccionable astronaut toy inspired by @lynxstudiosbcn's
 * bouncy expressive charm: chunky matte pearl helmet, recessed ice-pearl face shield,
 * 4 stubby walking moon-boots, 2 expressive mini arms, and 8 full 3D emotional modes.
 */
export const ChispaAstronaut3D: React.FC<ChispaAstronaut3DProps> = ({
  frame,
  localFrame,
  fps,
  expression,
  accentColor,
  position = [0, 0, 0],
  rotationY = 0,
  scale = 1,
  speaking = true,
  popFrames = [2, 8, 24, 36, 48],
}) => {
  const t = frame / fps;

  // Compute reusable smooth geometries once
  const geos = useMemo(() => {
    const helmetShell = new RoundedBoxGeometry(1.56, 1.06, 0.98, 6, 0.24);
    const visorGasket = new RoundedBoxGeometry(1.30, 0.80, 0.22, 5, 0.16);
    const facePlate = new RoundedBoxGeometry(1.18, 0.70, 0.16, 5, 0.14);
    const torso = new RoundedBoxGeometry(1.24, 0.42, 0.78, 5, 0.14);
    const backpack = new RoundedBoxGeometry(0.84, 0.64, 0.34, 4, 0.12);
    const boot = new RoundedBoxGeometry(0.22, 0.30, 0.26, 4, 0.08);
    const arm = new RoundedBoxGeometry(0.22, 0.36, 0.22, 4, 0.09);
    const starShape = createFourPointStarShape(0.18, 0.052);
    const starGeo = new THREE.ExtrudeGeometry(starShape, {
      depth: 0.045,
      bevelEnabled: true,
      bevelThickness: 0.015,
      bevelSize: 0.012,
      bevelSegments: 2,
    });
    starGeo.center();

    const eyeStarShape = createFourPointStarShape(0.145, 0.045);
    const eyeStarGeo = new THREE.ExtrudeGeometry(eyeStarShape, {
      depth: 0.035,
      bevelEnabled: true,
      bevelThickness: 0.01,
      bevelSize: 0.008,
      bevelSegments: 2,
    });
    eyeStarGeo.center();

    // Crisp cartoon D-shaped open mouth cavity (flat upper lip, curved lower lip)
    const dMouthShape = new THREE.Shape();
    dMouthShape.moveTo(-0.115, 0.045);
    dMouthShape.lineTo(0.115, 0.045);
    dMouthShape.bezierCurveTo(0.115, -0.105, -0.115, -0.105, -0.115, 0.045);
    const dMouthGeo = new THREE.ExtrudeGeometry(dMouthShape, {
      depth: 0.025,
      bevelEnabled: true,
      bevelThickness: 0.008,
      bevelSize: 0.006,
      bevelSegments: 2,
    });

    return {
      helmetShell,
      visorGasket,
      facePlate,
      torso,
      backpack,
      boot,
      arm,
      starGeo,
      eyeStarGeo,
      dMouthGeo,
    };
  }, []);

  // Elastic entrance hop + mini hops right on UI Pop timestamps
  const introHop = spring({
    frame: localFrame,
    fps,
    config: { damping: 10, stiffness: 190, mass: 0.85 },
  });
  let totalPopPulse = Math.sin(introHop * Math.PI) * 0.28;
  for (const pf of popFrames) {
    if (localFrame >= pf && localFrame < pf + 16) {
      const pSpring = spring({
        frame: localFrame - pf,
        fps,
        config: { damping: 11, stiffness: 260, mass: 0.7 },
      });
      totalPopPulse += Math.sin(pSpring * Math.PI) * 0.13;
    }
  }

  // Rhythmic energetic idle bounce ("cómo brinca")
  const rhythmFreq =
    expression === 'star_eyes' || expression === 'happy_open' ? 7.4 : 4.2;
  const idleHop = Math.abs(Math.sin(t * rhythmFreq)) * 0.075;
  const jumpY = idleHop + totalPopPulse;

  // Squash & stretch matching Claudio's tactile bounce
  const squashStretch = 1 + totalPopPulse * 0.22 - idleHop * 0.18;
  const stretchXZ = 1 / Math.sqrt(Math.max(0.75, squashStretch));

  // Tilt / lean per expression
  let tiltZ = Math.sin(t * 2.6) * 0.035;
  let tiltX = 0;
  let headBobY = Math.sin(t * 5.0) * 0.025;
  let yawJitter = Math.sin(t * 1.9) * 0.06;

  if (expression === 'wink') {
    tiltZ = 0.15 + Math.sin(t * 5.2) * 0.04;
    yawJitter = -0.14;
  } else if (expression === 'sad_cloud') {
    tiltZ = -0.05;
    tiltX = 0.12;
    headBobY = -0.04 + Math.sin(t * 2.2) * 0.015;
  } else if (expression === 'determined_hacker') {
    tiltX = 0.08;
    yawJitter = 0.12 + Math.sin(t * 12) * 0.02;
  } else if (expression === 'shock_sweat') {
    tiltZ = localFrame < 16 ? Math.sin(localFrame * 3.2) * 0.08 : 0;
    tiltX = -0.08;
  } else if (expression === 'star_eyes') {
    tiltZ = Math.sin(t * 5.8) * 0.08;
  }

  // Eye tracking ("mueve los ojitos"): glances up at terminal while typing, then back to viewer
  const isTypingWindow = localFrame >= 8 && localFrame <= 48;
  const lookX = isTypingWindow
    ? Math.sin((localFrame - 8) * 0.42) * 0.052
    : Math.sin(t * 2.1) * 0.032;
  const lookY = isTypingWindow ? 0.038 : Math.cos(t * 1.6) * 0.018;

  // Quick snappy natural blink for pill eyes
  const blinkMod = t % 3.1;
  const blinkFactor =
    expression !== 'shock_sweat' &&
    expression !== 'star_eyes' &&
    blinkMod > 2.94
      ? Math.max(0.08, 1 - Math.sin(((blinkMod - 2.94) / 0.16) * Math.PI) * 0.92)
      : 1;

  // Arms choreography
  let leftArmRotZ = -0.45 - Math.sin(t * 5.2) * 0.16;
  let rightArmRotZ = 0.45 + Math.cos(t * 5.2) * 0.16;
  let leftArmRotX = 0;
  let rightArmRotX = 0;

  if (expression === 'happy_open' || expression === 'star_eyes') {
    rightArmRotZ = 2.15 + Math.sin(t * 9.5) * 0.25;
    leftArmRotZ = -0.65 - Math.sin(t * 5.5) * 0.15;
  } else if (expression === 'shock_sweat') {
    leftArmRotZ = -2.35 - Math.sin(t * 14) * 0.15;
    rightArmRotZ = 2.35 + Math.sin(t * 14) * 0.15;
  } else if (expression === 'determined_hacker') {
    // Rapid typing arm motion!
    leftArmRotX = -0.75 + Math.sin(t * 28) * 0.18;
    rightArmRotX = -0.75 + Math.cos(t * 28) * 0.18;
    leftArmRotZ = -0.25;
    rightArmRotZ = 0.25;
  } else if (expression === 'sad_cloud') {
    leftArmRotZ = -0.18;
    rightArmRotZ = 0.18;
  } else if (expression === 'wink') {
    rightArmRotZ = 1.65 + Math.sin(t * 7) * 0.15;
  }

  // Materials palette — Matte pearl spacesuit + space slate gasket + luminous cyan/gold trim
  const pearlWhite = '#F3F6FC';
  const pearlShadow = '#DCE4F0';
  const gasketDark = '#1A2233';
  const visorTint = '#DCEBFA';
  const goldAccent = '#F5C451';
  const blackInk = '#0A0D14';
  const tonguePink = '#FF7EB6';
  const blushPink = '#FF8FB3';
  const mouthSpeakScale = speaking
    ? 0.88 + Math.abs(Math.sin(t * 15)) * 0.28
    : 1;

  const showSparkles =
    expression === 'happy_open' ||
    expression === 'zen_proud' ||
    expression === 'star_eyes' ||
    expression === 'wink';
  const sparkleScale = spring({
    frame: Math.max(0, localFrame - 6),
    fps,
    config: { damping: 9, stiffness: 200 },
  });

  return (
    <group
      position={[position[0], position[1] + jumpY, position[2]]}
      rotation={[tiltX, rotationY + yawJitter, tiltZ]}
      scale={[scale * stretchXZ, scale * squashStretch, scale * stretchXZ]}
    >
      {/* HERO ASTRONAUT HELMET + UPPER SUIT */}
      <group position={[0, 0.34 + headBobY, 0]}>
        {/* Chunky Rounded Pearl Astronaut Helmet */}
        <mesh geometry={geos.helmetShell} castShadow receiveShadow>
          <meshStandardMaterial
            color={pearlWhite}
            roughness={0.34}
            metalness={0.08}
          />
        </mesh>

        {/* Helmet Top Glowing Crest & Bobbing Antenna */}
        <mesh position={[0, 0.54, 0]}>
          <boxGeometry args={[0.52, 0.08, 0.42]} />
          <meshStandardMaterial
            color={pearlShadow}
            roughness={0.3}
            metalness={0.3}
          />
        </mesh>
        <group
          position={[0.38, 0.54, -0.04]}
          rotation={[0, 0, -0.22 + Math.sin(t * 8) * 0.12]}
        >
          <mesh position={[0, 0.13, 0]}>
            <cylinderGeometry args={[0.024, 0.034, 0.26, 12]} />
            <meshStandardMaterial color={gasketDark} metalness={0.7} roughness={0.25} />
          </mesh>
          <mesh position={[0, 0.28, 0]}>
            <sphereGeometry args={[0.075, 18, 18]} />
            <meshStandardMaterial
              color={accentColor}
              emissive={accentColor}
              emissiveIntensity={2.0 + Math.sin(t * 10) * 0.5}
              roughness={0.2}
            />
          </mesh>
        </group>

        {/* Side Space Ear-Comm Pods with Neon Rings */}
        {[-0.81, 0.81].map((ex, idx) => (
          <group key={idx} position={[ex, 0.02, 0]}>
            <mesh rotation={[0, 0, Math.PI / 2]}>
              <cylinderGeometry args={[0.20, 0.20, 0.12, 24]} />
              <meshStandardMaterial color={gasketDark} roughness={0.3} metalness={0.65} />
            </mesh>
            <mesh
              position={[ex > 0 ? 0.065 : -0.065, 0, 0]}
              rotation={[0, Math.PI / 2, 0]}
            >
              <torusGeometry args={[0.125, 0.024, 12, 24]} />
              <meshStandardMaterial
                color={accentColor}
                emissive={accentColor}
                emissiveIntensity={1.8}
              />
            </mesh>
          </group>
        ))}

        {/* Dark Space-Rubber Helmet Gasket Framing the Visor */}
        <mesh position={[0, 0.01, 0.43]} geometry={geos.visorGasket}>
          <meshStandardMaterial
            color={gasketDark}
            roughness={0.45}
            metalness={0.45}
          />
        </mesh>

        {/* Ice-Pearl Panoramic Face Visor Shield (High Contrast for Toy Expressions) */}
        <mesh position={[0, 0.01, 0.48]} geometry={geos.facePlate}>
          <meshStandardMaterial
            color={visorTint}
            roughness={0.22}
            metalness={0.05}
          />
        </mesh>

        {/* Subtle Glowing Cyan Rim Strip Under Gasket */}
        <mesh position={[0, -0.40, 0.48]}>
          <boxGeometry args={[0.92, 0.032, 0.05]} />
          <meshStandardMaterial
            color={accentColor}
            emissive={accentColor}
            emissiveIntensity={1.9}
          />
        </mesh>

        {/* ============================================================
            FACIAL EXPRESSIONS LAYER (Front Z = 0.575)
           ============================================================ */}
        <group position={[0, 0.01, 0.575]}>
          {/* ROSY BLUSH CHEEKS on warm/happy modes */}
          {(expression === 'happy_open' ||
            expression === 'happy_arcs' ||
            expression === 'wink' ||
            expression === 'zen_proud' ||
            expression === 'star_eyes') &&
            [-0.41, 0.41].map((bx, i) => (
              <mesh
                key={`blush-${i}`}
                position={[bx, -0.11, 0.005]}
                scale={[1.35, 0.85, 0.3]}
              >
                <sphereGeometry args={[0.055, 16, 16]} />
                <meshBasicMaterial color={blushPink} transparent opacity={0.55} />
              </mesh>
            ))}

          {/* EYES BY EXPRESSION */}
          {[-0.25, 0.25].map((eyeX, idx) => {
            const isRight = idx === 1;

            // 1. PILL EYES (happy_open, sad_cloud, determined_hacker)
            if (
              expression === 'happy_open' ||
              expression === 'sad_cloud' ||
              expression === 'determined_hacker'
            ) {
              return (
                <group
                  key={`eye-${idx}`}
                  position={[eyeX + lookX, 0.07 + lookY, 0]}
                  scale={[1, blinkFactor, 1]}
                >
                  {/* Glossy Pill Eye */}
                  <mesh scale={[1, 1.38, 0.35]}>
                    <capsuleGeometry args={[0.088, 0.07, 12, 20]} />
                    <meshStandardMaterial
                      color={blackInk}
                      roughness={0.08}
                      metalness={0.35}
                    />
                  </mesh>
                  {/* Big Specular Catchlight Glint (like Claudio!) */}
                  <mesh position={[-0.032, 0.075, 0.032]}>
                    <sphereGeometry args={[0.028, 12, 12]} />
                    <meshBasicMaterial color="#FFFFFF" />
                  </mesh>
                  {/* Secondary subtle glint */}
                  <mesh position={[0.034, -0.055, 0.028]}>
                    <sphereGeometry args={[0.013, 10, 10]} />
                    <meshBasicMaterial color="#FFFFFF" />
                  </mesh>
                </group>
              );
            }

            // 2. HAPPY ARCS ◠ ◠ or ZEN ARCS ◡ ◡
            if (expression === 'happy_arcs' || expression === 'zen_proud') {
              const rotZ = expression === 'happy_arcs' ? 0 : Math.PI;
              return (
                <mesh
                  key={`arc-${idx}`}
                  position={[eyeX, 0.05, 0.01]}
                  rotation={[0, 0, rotZ]}
                >
                  <torusGeometry args={[0.10, 0.026, 12, 24, Math.PI]} />
                  <meshStandardMaterial color={blackInk} roughness={0.2} />
                </mesh>
              );
            }

            // 3. WINK (Left = happy arc ◠, Right = cheeky horizontal bar —)
            if (expression === 'wink') {
              if (!isRight) {
                return (
                  <mesh
                    key={`wink-l`}
                    position={[eyeX, 0.05, 0.01]}
                    rotation={[0, 0, 0]}
                  >
                    <torusGeometry args={[0.10, 0.026, 12, 24, Math.PI]} />
                    <meshStandardMaterial color={blackInk} roughness={0.2} />
                  </mesh>
                );
              }
              return (
                <mesh key={`wink-r`} position={[eyeX, 0.06, 0.015]}>
                  <boxGeometry args={[0.17, 0.052, 0.03]} />
                  <meshStandardMaterial color={blackInk} roughness={0.2} />
                </mesh>
              );
            }

            // 4. SHOCK BIG WHITE EYES (O O)
            if (expression === 'shock_sweat') {
              const jiggle = 1 + Math.sin(t * 22 + idx) * 0.06;
              return (
                <group
                  key={`shock-${idx}`}
                  position={[eyeX, 0.06, 0]}
                  scale={[jiggle, jiggle, 1]}
                >
                  <mesh scale={[1, 1, 0.35]}>
                    <sphereGeometry args={[0.145, 22, 22]} />
                    <meshStandardMaterial color="#FFFFFF" roughness={0.18} />
                  </mesh>
                  <mesh position={[lookX * 0.4, lookY * 0.4, 0.048]} scale={[1, 1, 0.4]}>
                    <sphereGeometry args={[0.064, 16, 16]} />
                    <meshStandardMaterial color={blackInk} roughness={0.1} />
                  </mesh>
                  <mesh position={[-0.025, 0.035, 0.072]}>
                    <sphereGeometry args={[0.020, 10, 10]} />
                    <meshBasicMaterial color="#FFFFFF" />
                  </mesh>
                </group>
              );
            }

            // 5. GOLDEN STAR EYES ✦ ✦
            return (
              <mesh
                key={`stareye-${idx}`}
                geometry={geos.eyeStarGeo}
                position={[eyeX, 0.06, 0.012]}
                rotation={[0, 0, Math.sin(t * 5 + idx) * 0.14]}
                scale={1.06 + Math.sin(t * 8 + idx) * 0.08}
              >
                <meshStandardMaterial
                  color="#FFF4B8"
                  emissive={goldAccent}
                  emissiveIntensity={2.3}
                  roughness={0.2}
                />
              </mesh>
            );
          })}

          {/* EYEBROWS FOR SAD CLOUD (/ \) AND DETERMINED HACKER (\ /) */}
          {expression === 'sad_cloud' &&
            [-0.25, 0.25].map((bx, idx) => (
              <mesh
                key={`sadbrow-${idx}`}
                position={[bx, 0.23, 0.035]}
                rotation={[0, 0, idx === 0 ? 0.32 : -0.32]}
              >
                <boxGeometry args={[0.20, 0.044, 0.04]} />
                <meshStandardMaterial color={pearlShadow} roughness={0.3} />
              </mesh>
            ))}

          {expression === 'determined_hacker' &&
            [-0.25, 0.25].map((bx, idx) => (
              <mesh
                key={`hackbrow-${idx}`}
                position={[bx, 0.22, 0.035]}
                rotation={[0, 0, idx === 0 ? -0.36 : 0.36]}
              >
                <boxGeometry args={[0.21, 0.046, 0.04]} />
                <meshStandardMaterial color={gasketDark} roughness={0.25} />
              </mesh>
            ))}

          {/* MOUTH BY EXPRESSION */}
          {(expression === 'happy_open' || expression === 'star_eyes') && (
            <group position={[0, -0.155, 0.006]} scale={[1, mouthSpeakScale, 1]}>
              <mesh geometry={geos.dMouthGeo}>
                <meshStandardMaterial color={blackInk} roughness={0.2} />
              </mesh>
              <mesh position={[0, -0.025, 0.026]} scale={[1.25, 0.72, 0.45]}>
                <sphereGeometry args={[0.048, 16, 16]} />
                <meshStandardMaterial color={tonguePink} roughness={0.25} />
              </mesh>
            </group>
          )}

          {expression === 'sad_cloud' && (
            <mesh position={[0, -0.19, 0.015]} rotation={[0, 0, 0]}>
              <torusGeometry args={[0.09, 0.024, 12, 24, Math.PI]} />
              <meshStandardMaterial color={blackInk} roughness={0.2} />
            </mesh>
          )}

          {expression === 'determined_hacker' && (
            <mesh position={[0, -0.15, 0.015]}>
              <boxGeometry args={[0.15, 0.04, 0.03]} />
              <meshStandardMaterial color={blackInk} roughness={0.2} />
            </mesh>
          )}

          {(expression === 'happy_arcs' ||
            expression === 'wink' ||
            expression === 'zen_proud') && (
            <mesh position={[0, -0.12, 0.015]} rotation={[0, 0, Math.PI]}>
              <torusGeometry args={[0.095, 0.024, 12, 24, Math.PI]} />
              <meshStandardMaterial color={blackInk} roughness={0.2} />
            </mesh>
          )}

          {expression === 'shock_sweat' && (
            <group position={[0, -0.16, 0.015]}>
              {[-0.08, 0, 0.08].map((wx, wi) => (
                <mesh
                  key={wi}
                  position={[wx, wi % 2 === 0 ? 0.018 : -0.018, 0]}
                  rotation={[0, 0, wi % 2 === 0 ? 0.45 : -0.45]}
                >
                  <boxGeometry args={[0.095, 0.036, 0.03]} />
                  <meshStandardMaterial color={blackInk} roughness={0.2} />
                </mesh>
              ))}
            </group>
          )}
        </group>

        {/* ============================================================
            EMOTIONAL FLOATING 3D PROPS ABOVE HELMET (Stars / Cloud / Sweat)
           ============================================================ */}
        {showSparkles && (
          <group position={[0.66, 0.78, 0.18]} scale={sparkleScale}>
            <mesh
              geometry={geos.starGeo}
              position={[0, Math.sin(t * 5.5) * 0.04, 0]}
              rotation={[0, 0.15, Math.sin(t * 3.5) * 0.22]}
              scale={1.12 + Math.sin(t * 8) * 0.12}
            >
              <meshStandardMaterial
                color="#FFE57A"
                emissive={goldAccent}
                emissiveIntensity={1.65}
                roughness={0.2}
                metalness={0.3}
              />
            </mesh>
            <mesh
              geometry={geos.starGeo}
              position={[0.28, -0.22 + Math.cos(t * 5.5) * 0.035, 0.08]}
              rotation={[0, -0.15, 0.35 + Math.cos(t * 3.5) * 0.15]}
              scale={0.64 + Math.cos(t * 8) * 0.08}
            >
              <meshStandardMaterial
                color="#FFE57A"
                emissive={goldAccent}
                emissiveIntensity={1.5}
                roughness={0.2}
              />
            </mesh>
          </group>
        )}

        {/* FLOATING 3D RAIN CLOUD ABOVE HELMET FOR sad_cloud */}
        {expression === 'sad_cloud' && (
          <group position={[0, 1.05 + Math.sin(t * 2.5) * 0.04, 0]}>
            {[
              [0, 0.05, 0, 0.22],
              [-0.22, -0.02, 0.04, 0.17],
              [0.23, -0.02, 0.04, 0.16],
              [-0.10, 0.14, -0.04, 0.16],
              [0.12, 0.13, -0.04, 0.15],
            ].map(([cx, cy, cz, cr], ci) => (
              <mesh key={ci} position={[cx, cy, cz]}>
                <sphereGeometry args={[cr, 18, 18]} />
                <meshStandardMaterial color="#8A96B0" roughness={0.65} />
              </mesh>
            ))}
            {/* Animated Falling Cyan Raindrops */}
            {[
              [-0.22, 0],
              [0.02, 0.35],
              [0.22, 0.7],
            ].map(([rx, phase], ri) => {
              const dropP = (t * 1.45 + phase) % 1;
              return (
                <mesh key={ri} position={[rx, -0.16 - dropP * 0.48, 0.15]}>
                  <capsuleGeometry args={[0.024, 0.08, 6, 12]} />
                  <meshStandardMaterial
                    color="#7DD3FC"
                    emissive="#38BDF8"
                    emissiveIntensity={1.4}
                  />
                </mesh>
              );
            })}
          </group>
        )}

        {/* SWEAT DROPS FOR shock_sweat */}
        {expression === 'shock_sweat' && (
          <group position={[0.18, 0.78, 0.2]}>
            {[0, 0.5].map((phase, si) => {
              const p = (t * 1.8 + phase) % 1;
              return (
                <mesh
                  key={si}
                  position={[si === 0 ? -0.16 : 0.14, p * 0.22, 0.08]}
                  scale={[1, 1.35, 1]}
                >
                  <sphereGeometry args={[0.052 * (1 - p * 0.35), 14, 14]} />
                  <meshStandardMaterial
                    color="#7DD3FC"
                    emissive="#38BDF8"
                    emissiveIntensity={1.3}
                  />
                </mesh>
              );
            })}
          </group>
        )}
      </group>

      {/* CHUNKY MINI ASTRONAUT TORSO + BELT + BACKPACK */}
      <group position={[0, -0.34, 0]}>
        <mesh geometry={geos.torso} castShadow receiveShadow>
          <meshStandardMaterial color={pearlWhite} roughness={0.35} metalness={0.08} />
        </mesh>
        {/* Chest Control Badge */}
        <mesh position={[0, 0.03, 0.40]}>
          <boxGeometry args={[0.38, 0.22, 0.05]} />
          <meshStandardMaterial color={gasketDark} roughness={0.35} metalness={0.45} />
        </mesh>
        <mesh position={[0, 0.03, 0.43]}>
          <boxGeometry args={[0.24, 0.075, 0.02]} />
          <meshStandardMaterial
            color={accentColor}
            emissive={accentColor}
            emissiveIntensity={2.0}
          />
        </mesh>
        {/* Backpack Life-Support Pack */}
        <mesh position={[0, 0.22, -0.52]} geometry={geos.backpack} castShadow>
          <meshStandardMaterial color={pearlShadow} roughness={0.35} metalness={0.22} />
        </mesh>
      </group>

      {/* TWO STUBBY ARTICULATED SPACE ARMS */}
      <group
        position={[-0.74, -0.18, 0]}
        rotation={[leftArmRotX, 0, leftArmRotZ]}
      >
        <mesh position={[0, -0.14, 0]} geometry={geos.arm} castShadow>
          <meshStandardMaterial color={pearlWhite} roughness={0.35} />
        </mesh>
        <mesh position={[0, -0.31, 0]}>
          <sphereGeometry args={[0.115, 16, 16]} />
          <meshStandardMaterial color={gasketDark} roughness={0.35} metalness={0.4} />
        </mesh>
      </group>

      <group
        position={[0.74, -0.18, 0]}
        rotation={[rightArmRotX, 0, rightArmRotZ]}
      >
        <mesh position={[0, -0.14, 0]} geometry={geos.arm} castShadow>
          <meshStandardMaterial color={pearlWhite} roughness={0.35} />
        </mesh>
        <mesh position={[0, -0.31, 0]}>
          <sphereGeometry args={[0.115, 16, 16]} />
          <meshStandardMaterial color={gasketDark} roughness={0.35} metalness={0.4} />
        </mesh>
      </group>

      {/* FOUR CHUNKY STUBBY ASTRONAUT MOON-BOOTS ("4 patitas" like Claudio) */}
      {[-0.44, -0.15, 0.15, 0.44].map((lx, idx) => {
        const walkPhase = idx % 2 === 0 ? 0 : Math.PI;
        const stepRotX = Math.sin(t * 7.5 + walkPhase) * 0.18;
        const stepY = Math.max(0, Math.sin(t * 7.5 + walkPhase)) * 0.04;
        return (
          <group
            key={idx}
            position={[lx, -0.66 + stepY, 0.04]}
            rotation={[stepRotX, 0, 0]}
          >
            <mesh geometry={geos.boot} castShadow receiveShadow>
              <meshStandardMaterial color={pearlShadow} roughness={0.4} />
            </mesh>
            {/* Dark Moon Boot Sole */}
            <mesh position={[0, -0.13, 0.03]}>
              <boxGeometry args={[0.23, 0.075, 0.28]} />
              <meshStandardMaterial color={gasketDark} roughness={0.5} metalness={0.3} />
            </mesh>
          </group>
        );
      })}
    </group>
  );
};
