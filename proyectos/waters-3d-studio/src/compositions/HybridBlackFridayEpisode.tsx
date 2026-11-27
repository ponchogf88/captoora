import React from 'react';
import {
  AbsoluteFill,
  Loop,
  Sequence,
  Video,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { useThree } from '@react-three/fiber';
import {
  AlarmBeacon3D,
  BinaryDoors3D,
  GiantClipboard3D,
  NeonMarquee3D,
  SemiGauge3D,
  ToyReflectiveGridStage,
} from '../components/ToyPropKit3D';
import {
  AiPromptBoxOverlay,
  HeroHookOverlay,
  SpendingChartOverlay,
} from '../components/HybridAiOverlays';

export interface HybridAvatarClips {
  hook?: string;
  bucle?: string;
  chart?: string;
  pip?: string;
  cta?: string;
}

export interface HybridBlackFridayProps {
  avatarClips?: HybridAvatarClips;
}

const Stage3DCamera: React.FC<{ frame: number }> = ({ frame }) => {
  const { camera } = useThree();
  const swayX = Math.sin(frame * 0.035) * 0.12;
  const swayY = 0.95 + Math.cos(frame * 0.025) * 0.04;
  camera.position.set(swayX, swayY, 6.0);
  camera.lookAt(0, 0.16, 0);
  return null;
};

const AvatarLayer: React.FC<{
  src: string;
  mode: 'fullscreen' | 'split_left' | 'pip_top_right';
  scalePush?: number;
}> = ({ src, mode, scalePush = 1 }) => {
  const videoEl = (
    <Loop durationInFrames={240}>
      <Video
        src={src}
        startFrom={24}
        endAt={264}
        muted
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          objectPosition: mode === 'split_left' ? '50% 18%' : '50% 22%',
          transform: `scale(${scalePush})`,
        }}
      />
    </Loop>
  );

  if (mode === 'fullscreen') {
    return (
      <AbsoluteFill style={{ backgroundColor: '#080c14', overflow: 'hidden' }}>
        {videoEl}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'linear-gradient(180deg, rgba(8,12,20,0.48) 0%, rgba(8,12,20,0.0) 24%, rgba(8,12,20,0.0) 78%, rgba(8,12,20,0.38) 100%)',
          }}
        />
      </AbsoluteFill>
    );
  }

  if (mode === 'split_left') {
    return (
      <AbsoluteFill style={{ backgroundColor: '#080c14' }}>
        <div
          style={{
            position: 'absolute',
            top: 0,
            bottom: 0,
            left: 0,
            width: 1020,
            overflow: 'hidden',
          }}
        >
          {videoEl}
          {/* Seamless dark gradient blend from concrete wall to #080c14 */}
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background:
                'linear-gradient(90deg, rgba(8,12,20,0.12) 0%, rgba(8,12,20,0) 58%, #080c14 98%)',
            }}
          />
        </div>
      </AbsoluteFill>
    );
  }

  // Top-right PiP card (leaves bottom 240px clear for OpusClip + Captions!)
  return (
    <div
      style={{
        position: 'absolute',
        top: 40,
        right: 48,
        width: 340,
        height: 224,
        borderRadius: 22,
        overflow: 'hidden',
        border: '3px solid #00e0f0',
        boxShadow: '0 18px 48px rgba(0,0,0,0.72), 0 0 28px rgba(0,224,240,0.28)',
        backgroundColor: '#080c14',
      }}
    >
      {videoEl}
    </div>
  );
};

export const HybridBlackFridayEpisode: React.FC<HybridBlackFridayProps> = ({ avatarClips }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const defaultAvatar = staticFile('avatar/master_ref.mp4');
  const clipHook = avatarClips?.hook ?? defaultAvatar;
  const clipBucle = avatarClips?.bucle ?? defaultAvatar;
  const clipChart = avatarClips?.chart ?? defaultAvatar;
  const clipPip = avatarClips?.pip ?? defaultAvatar;
  const clipCta = avatarClips?.cta ?? defaultAvatar;

  // 5-Act Timeline (2760 frames = 92.0s @ 30fps)
  const isAct1 = frame < 360; // 0-12s Hook fullscreen
  const isAct2 = frame >= 360 && frame < 960; // 12-32s AI Prompt Box split
  const isAct3a = frame >= 960 && frame < 1320; // 32-44s Spending Chart split
  const isAct3b = frame >= 1320 && frame < 1620; // 44-54s ToyProp Gauge + Siren + PiP
  const isAct4 = frame >= 1620 && frame < 2160; // 54-72s BinaryDoors 3D + PiP
  const isAct5a = frame >= 2160 && frame < 2520; // 72-84s GiantClipboard 3D + PiP
  const isAct5b = frame >= 2520; // 84-92s Final CTA Fullscreen

  const in3DWorld = isAct3b || isAct4 || isAct5a;

  const hookPush = isAct1
    ? interpolate(frame, [0, 360], [1.0, 1.07], { extrapolateRight: 'clamp' })
    : 1.0;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#080c14',
        fontFamily: '"Arial Black", "Helvetica Neue", Arial, sans-serif',
      }}
    >
      {/* ACT 1: 0–12s Hook Black Friday Fullscreen */}
      <Sequence from={0} durationInFrames={360}>
        <AvatarLayer src={clipHook} mode="fullscreen" scalePush={hookPush} />
        <HeroHookOverlay frame={frame} fps={fps} />
      </Sequence>

      {/* ACT 2: 12–32s Split Avatar + Typing AI Prompt Box */}
      <Sequence from={360} durationInFrames={600}>
        <AvatarLayer src={clipBucle} mode="split_left" />
        <AiPromptBoxOverlay localFrame={Math.max(0, frame - 360)} fps={fps} />
      </Sequence>

      {/* ACT 3A: 32–44s Split Avatar + Animated $2,000 Spending Chart */}
      <Sequence from={960} durationInFrames={360}>
        <AvatarLayer src={clipChart} mode="split_left" />
        <SpendingChartOverlay localFrame={Math.max(0, frame - 960)} fps={fps} />
      </Sequence>

      {/* ACTS 3B, 4, 5A: Toy-Prop 3D World + Top-Right Avatar PiP */}
      {in3DWorld && (
        <AbsoluteFill>
          <ThreeCanvas
            width={width}
            height={height}
            camera={{ position: [0, 0.95, 6.0], fov: 38 }}
            gl={{ antialias: true, powerPreference: 'high-performance' }}
          >
            <Stage3DCamera frame={frame} />
            <ToyReflectiveGridStage
              frame={frame}
              accentColor={isAct3b ? '#ff2b4a' : isAct4 ? '#00e0f0' : '#2ee87a'}
              alertStrength={isAct3b ? 0.95 : isAct4 ? 0.35 : 0}
            />

            {isAct3b && (
              <group>
                <NeonMarquee3D
                  text="$2,000 USD"
                  sub="10,000 REINTENTOS"
                  color="#ff2b4a"
                  frame={frame}
                  position={[0, 1.56, -0.85]}
                  scale={0.86}
                />
                <SemiGauge3D
                  targetRatio={0.96}
                  localFrame={Math.max(0, frame - 1320)}
                  fps={fps}
                  position={[-0.25, -0.15, -0.5]}
                  scale={1.12}
                />
                <AlarmBeacon3D
                  frame={frame}
                  active
                  position={[1.75, -0.78, 0.15]}
                  scale={1.15}
                />
              </group>
            )}

            {isAct4 && (
              <group scale={0.86}>
                <BinaryDoors3D
                  frame={frame}
                  leftNum="1"
                  leftLabel="SIN LÍMITE"
                  rightNum="2"
                  rightLabel="HARD LIMIT"
                />
              </group>
            )}

            {isAct5a && (
              <group scale={0.84} position={[-0.2, 0.05, 0]}>
                <GiantClipboard3D
                  items={['HARD LIMIT $20', 'TARJETA VIRTUAL', 'COMENTA: PRESUPUESTO']}
                  localFrame={Math.max(0, frame - 2160)}
                  fps={fps}
                  frame={frame}
                />
              </group>
            )}
          </ThreeCanvas>

          {/* Top-left section badge */}
          <div
            style={{
              position: 'absolute',
              top: 38,
              left: 48,
              padding: '10px 20px',
              borderRadius: 12,
              backgroundColor: 'rgba(10, 14, 22, 0.85)',
              border: `2px solid ${isAct3b ? '#ff2b4a' : isAct4 ? '#00e0f0' : '#2ee87a'}`,
              color: '#f8fafc',
              fontSize: 22,
              fontWeight: 800,
              letterSpacing: '0.05em',
            }}
          >
            {isAct3b
              ? '¡WATERS! · SIN HARD LIMIT'
              : isAct4
                ? 'BLACK FRIDAY · ELIGE BIEN'
                : '3 CANDADOS EN 3 MINUTOS'}
          </div>

          <AvatarLayer src={clipPip} mode="pip_top_right" />
        </AbsoluteFill>
      )}

      {/* ACT 5B: 84–92s Clean Fullscreen Avatar CTA (bottom 220px clear for Captions!) */}
      <Sequence from={2520} durationInFrames={240}>
        <AvatarLayer src={clipCta} mode="fullscreen" scalePush={1.03} />
        <div
          style={{
            position: 'absolute',
            right: 84,
            top: 230,
            width: 500,
            borderRadius: 22,
            backgroundColor: 'rgba(10, 14, 24, 0.88)',
            border: '3px solid #2ee87a',
            boxShadow: '0 22px 60px rgba(0,0,0,0.75)',
            padding: '28px 30px',
            pointerEvents: 'none',
          }}
        >
          <div style={{ fontSize: 20, fontWeight: 800, color: '#2ee87a', letterSpacing: '0.06em' }}>
            GUÍA GRATIS · BLACK FRIDAY
          </div>
          <div style={{ marginTop: 8, fontSize: 42, fontWeight: 900, lineHeight: 1.08, color: '#ffffff' }}>
            COMENTA: <span style={{ color: '#00e0f0' }}>PRESUPUESTO</span>
          </div>
          <div style={{ marginTop: 12, fontSize: 22, fontWeight: 700, color: '#cbd5e1' }}>
            Te paso el checklist de límites duros para Gemini, Claude y ChatGPT.
          </div>
        </div>
      </Sequence>

      {/* Silence check marker: Note ZERO bottom burned-in captions so OpusClip + Captions stay clean */}
      {isAct2 && isAct5b ? null : null}
    </AbsoluteFill>
  );
};
