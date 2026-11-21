import React from 'react';
import {
  AbsoluteFill,
  interpolate,
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
  CheapBot1Usd3D,
  DarkStudioRoom3D,
  DESK_TOP_Y,
  DiegeticMonitor3D,
  MonitorScreenMode,
} from '../components/MadrugadaStageProps3D';

export type CameraShot =
  | 'wide_front'
  | 'ots_chispa'
  | 'low_villain'
  | 'closeup_face'
  | 'dutch_panic'
  | 'top_desk'
  | 'side_3q_left'
  | 'side_3q_right'
  | 'orbit_hero';

export interface MadrugadaBeatItem {
  id: string;
  durationInFrames: number;
  cameraShot: CameraShot;
  cutToShot?: CameraShot;
  cutAtFrame?: number;
  screenMode: MonitorScreenMode;
  expression: ChispaExpression;
  accentColor: string;
  showCheapBot?: boolean;
  microShake?: boolean;
  coldLockoutLight?: boolean;
  cutToBlackAtFrame?: number;
  speaking?: boolean;
}

export interface MadrugadaEpisodeProps {
  episodeLabel: string;
  beats: MadrugadaBeatItem[];
}

interface ShotRigSpec {
  fromPos: [number, number, number];
  toPos: [number, number, number];
  fromTarget: [number, number, number];
  toTarget: [number, number, number];
  fromFov: number;
  toFov: number;
  rollDeg: number;
}

function getShotSpec(shot: CameraShot, showCheapBot: boolean): ShotRigSpec {
  switch (shot) {
    case 'side_3q_left':
      return {
        fromPos: [-2.45, 0.62, 5.9],
        toPos: [-2.12, 0.52, 5.2],
        fromTarget: [0.02, 0.34, -0.1],
        toTarget: [-0.02, 0.34, -0.05],
        fromFov: 44,
        toFov: 41,
        rollDeg: 0,
      };
    case 'ots_chispa':
      return {
        fromPos: [-2.25, 0.86, 4.95],
        toPos: [-1.95, 0.74, 4.35],
        fromTarget: [0.34, 0.26, -0.35],
        toTarget: [0.42, 0.28, -0.38],
        fromFov: 44,
        toFov: 41,
        rollDeg: 0,
      };
    case 'low_villain':
      if (showCheapBot) {
        return {
          fromPos: [0.18, -0.52, 4.85],
          toPos: [0.32, -0.38, 4.25],
          fromTarget: [0.72, 0.38, 0.1],
          toTarget: [0.76, 0.4, 0.16],
          fromFov: 43,
          toFov: 40,
          rollDeg: 0,
        };
      }
      return {
        fromPos: [-0.14, -0.45, 6.2],
        toPos: [-0.04, -0.36, 5.55],
        fromTarget: [0.06, 0.34, -0.25],
        toTarget: [0.12, 0.32, -0.28],
        fromFov: 44,
        toFov: 41,
        rollDeg: 0,
      };
    case 'top_desk':
      return {
        fromPos: [-0.05, 3.65, 5.35],
        toPos: [0.18, 3.1, 4.65],
        fromTarget: [0.1, 0.12, -0.22],
        toTarget: [0.22, 0.18, -0.28],
        fromFov: 46,
        toFov: 42,
        rollDeg: 0,
      };
    case 'side_3q_right':
      return {
        fromPos: [2.75, 0.58, 4.75],
        toPos: [2.3, 0.48, 4.05],
        fromTarget: [0.28, 0.26, 0.1],
        toTarget: [0.38, 0.28, 0.18],
        fromFov: 42,
        toFov: 39,
        rollDeg: 0,
      };
    case 'dutch_panic':
      return {
        fromPos: [-0.22, 0.45, 6.35],
        toPos: [-0.05, 0.36, 5.55],
        fromTarget: [0.12, 0.26, -0.18],
        toTarget: [0.2, 0.28, -0.24],
        fromFov: 46,
        toFov: 42,
        rollDeg: -8,
      };
    case 'closeup_face':
      return {
        fromPos: [-0.72, 0.26, 3.45],
        toPos: [-0.68, 0.22, 2.85],
        fromTarget: [-0.78, 0.18, 0.45],
        toTarget: [-0.8, 0.18, 0.45],
        fromFov: 38,
        toFov: 34,
        rollDeg: 0,
      };
    case 'orbit_hero':
      return {
        fromPos: [-1.8, 0.45, 5.5],
        toPos: [1.6, 0.55, 5.2],
        fromTarget: [0.0, 0.24, -0.1],
        toTarget: [0.0, 0.24, -0.1],
        fromFov: 43,
        toFov: 40,
        rollDeg: 0,
      };
    case 'wide_front':
    default:
      return {
        fromPos: [-0.05, 0.45, 6.45],
        toPos: [0.0, 0.6, 7.85],
        fromTarget: [-0.06, 0.28, -0.25],
        toTarget: [-0.06, 0.3, -0.28],
        fromFov: 44,
        toFov: 46,
        rollDeg: 0,
      };
  }
}

const easeOutCubic = (x: number) => 1 - Math.pow(1 - Math.max(0, Math.min(1, x)), 3);

const MadrugadaCameraRig: React.FC<{
  beat: MadrugadaBeatItem;
  localFrame: number;
  globalFrame: number;
}> = ({ beat, localFrame, globalFrame }) => {
  const { camera } = useThree();

  const useCut =
    beat.cutToShot !== undefined &&
    beat.cutAtFrame !== undefined &&
    localFrame >= beat.cutAtFrame;

  const activeShot = useCut ? beat.cutToShot! : beat.cameraShot;
  const segStart = useCut ? beat.cutAtFrame! : 0;
  const segEnd =
    !useCut && beat.cutAtFrame !== undefined
      ? beat.cutAtFrame
      : beat.durationInFrames;

  const rawProgress = interpolate(
    localFrame,
    [segStart, Math.max(segStart + 1, segEnd)],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  const p = easeOutCubic(rawProgress);

  const spec = getShotSpec(activeShot, Boolean(beat.showCheapBot));

  let cx = interpolate(p, [0, 1], [spec.fromPos[0], spec.toPos[0]]);
  let cy = interpolate(p, [0, 1], [spec.fromPos[1], spec.toPos[1]]);
  let cz = interpolate(p, [0, 1], [spec.fromPos[2], spec.toPos[2]]);

  // Curved arc for orbit_hero
  if (activeShot === 'orbit_hero') {
    const angle = interpolate(p, [0, 1], [-0.45, 0.45]);
    const radius = interpolate(p, [0, 1], [5.3, 4.9]);
    cx = Math.sin(angle) * radius;
    cz = Math.cos(angle) * radius;
  }

  // Subtle organic breathing + optional crisis micro-shake
  cx += Math.sin(globalFrame * 0.045) * 0.025;
  cy += Math.cos(globalFrame * 0.038) * 0.02;

  if (beat.microShake) {
    cx += Math.sin(globalFrame * 1.9) * 0.028;
    cy += Math.cos(globalFrame * 2.4) * 0.022;
  }

  const tx = interpolate(p, [0, 1], [spec.fromTarget[0], spec.toTarget[0]]);
  const ty = interpolate(p, [0, 1], [spec.fromTarget[1], spec.toTarget[1]]);
  const tz = interpolate(p, [0, 1], [spec.fromTarget[2], spec.toTarget[2]]);
  const fov = interpolate(p, [0, 1], [spec.fromFov, spec.toFov]);

  camera.position.set(cx, cy, cz);
  camera.lookAt(new THREE.Vector3(tx, ty, tz));

  if (spec.rollDeg !== 0) {
    camera.rotateZ((spec.rollDeg * Math.PI) / 180);
  }

  const persp = camera as THREE.PerspectiveCamera;
  if (persp.fov !== fov) {
    persp.fov = fov;
    persp.updateProjectionMatrix();
  }

  return null;
};

const MadrugadaScene3D: React.FC<{
  beat: MadrugadaBeatItem;
  localFrame: number;
}> = ({ beat, localFrame }) => {
  const globalFrame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const isCold = Boolean(beat.coldLockoutLight);
  const isDanger =
    beat.screenMode === 'broken_web' ||
    beat.screenMode === 'zoom_countdown' ||
    beat.screenMode === 'hola_drain' ||
    beat.screenMode === 'quota_lockout';

  return (
    <>
      <color attach="background" args={[isCold ? '#020408' : '#040712']} />
      <fog attach="fog" args={[isCold ? '#020408' : '#040815', 11.5, 24.0]} />

      <MadrugadaCameraRig
        beat={beat}
        localFrame={localFrame}
        globalFrame={globalFrame}
      />

      {/* Cinematic midnight dual lighting: cool window moonlight + warm desk/monitor key */}
      <ambientLight intensity={isCold ? 0.45 : 0.62} color="#94A3B8" />
      <directionalLight
        position={[3.5, 6.5, 4.5]}
        intensity={isCold ? 1.15 : 1.75}
        color={isCold ? '#BAE6FD' : '#E2E8F0'}
        castShadow
      />
      {/* Cool blue window backlight rim on helmet & shoulders */}
      <directionalLight
        position={[-4.5, 4.2, -3.0]}
        intensity={isCold ? 1.4 : 2.1}
        color="#3B82F6"
      />
      {/* Warm desk lamp / crisis accent fill */}
      <pointLight
        position={[-2.6, 1.4, 2.2]}
        intensity={isDanger ? 2.4 : 1.9}
        distance={8.5}
        color={isDanger ? '#F87171' : '#FBBF24'}
      />

      <DarkStudioRoom3D frame={globalFrame} coldLockout={isCold} />

      <ChispaAstronaut3D
        frame={globalFrame}
        localFrame={localFrame}
        fps={fps}
        expression={beat.expression}
        accentColor={beat.accentColor}
        position={[-0.78, -0.15, 0.46]}
        rotationY={0.34}
        scale={0.8}
        speaking={beat.speaking ?? true}
        popFrames={[]}
      />

      <DiegeticMonitor3D
        frame={globalFrame}
        localFrame={localFrame}
        mode={beat.screenMode}
        position={[0.56, DESK_TOP_Y, -0.45]}
        rotationY={-0.24}
        scale={1.0}
      />

      {beat.showCheapBot && (
        <CheapBot1Usd3D
          frame={globalFrame}
          localFrame={localFrame}
          fps={fps}
          position={[1.05, 0.45, 0.68]}
          rotationY={-0.42}
          scale={0.72}
        />
      )}
    </>
  );
};

export const WatersMadrugadaEpisode: React.FC<MadrugadaEpisodeProps> = ({
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

  const cutToBlack =
    activeBeat.cutToBlackAtFrame !== undefined &&
    localFrame >= activeBeat.cutToBlackAtFrame;

  return (
    <AbsoluteFill style={{ backgroundColor: '#000000' }}>
      {!cutToBlack && (
        <>
          <ThreeCanvas
            width={width}
            height={height}
            camera={{ position: [-2.75, 0.48, 4.8], fov: 42 }}
            shadows
          >
            <MadrugadaScene3D beat={activeBeat} localFrame={localFrame} />
          </ThreeCanvas>

          {/* Subtle cinema edge vignette only — ZERO 2D HUD banners or text overlays */}
          <div
            style={{
              position: 'absolute',
              inset: 0,
              pointerEvents: 'none',
              background:
                'radial-gradient(circle at 50% 45%, rgba(0,0,0,0) 54%, rgba(2,4,10,0.58) 100%)',
            }}
          />
        </>
      )}
    </AbsoluteFill>
  );
};
