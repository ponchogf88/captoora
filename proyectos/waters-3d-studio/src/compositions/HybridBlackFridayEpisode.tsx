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
import bf01Timings from '../data/bf01Timings.json';

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
  startFrom?: number;
}> = ({ src, mode, scalePush = 1, startFrom = 24 }) => {
  const safeStart = Math.max(0, Math.min(100, startFrom));
  const loopFrames = 180;
  const videoEl = (
    <Loop durationInFrames={loopFrames}>
      <Video
        src={src}
        startFrom={safeStart}
        endAt={safeStart + loopFrames}
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

  const clipMap = Object.fromEntries(bf01Timings.clips.map((c) => [c.id, c]));
  const a1 = clipMap.A1_hook;
  const a2 = clipMap.A2_bucle;
  const a3a = clipMap.A3a_grafica;
  const a3b = clipMap.A3b_gauge;
  const a4 = clipMap.A4_puertas;
  const a5a = clipMap.A5a_candados;
  const a5b = clipMap.A5b_cta;

  const isAct1 = frame >= a1.startFrame && frame < a1.startFrame + a1.durationInFrames;
  const isAct2 = frame >= a2.startFrame && frame < a2.startFrame + a2.durationInFrames;
  const isAct3b = frame >= a3b.startFrame && frame < a3b.startFrame + a3b.durationInFrames;
  const isAct4 = frame >= a4.startFrame && frame < a4.startFrame + a4.durationInFrames;
  const isAct5a = frame >= a5a.startFrame && frame < a5a.startFrame + a5a.durationInFrames;
  const isAct5b = frame >= a5b.startFrame;

  const in3DWorld = isAct3b || isAct4 || isAct5a;

  const hookPush = isAct1
    ? interpolate(frame - a1.startFrame, [0, a1.durationInFrames], [1.0, 1.07], {
        extrapolateRight: 'clamp',
      })
    : 1.0;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#080c14',
        fontFamily: '"Arial Black", "Helvetica Neue", Arial, sans-serif',
      }}
    >
      {/* ACT 1: Hook Black Friday Fullscreen */}
      <Sequence from={a1.startFrame} durationInFrames={a1.durationInFrames}>
        <AvatarLayer src={clipHook} mode="fullscreen" scalePush={hookPush} startFrom={18} />
        <HeroHookOverlay frame={Math.max(0, frame - a1.startFrame)} fps={fps} />
      </Sequence>

      {/* ACT 2: Split Avatar + Typing AI Prompt Box */}
      <Sequence from={a2.startFrame} durationInFrames={a2.durationInFrames}>
        <AvatarLayer src={clipBucle} mode="split_left" startFrom={54} />
        <AiPromptBoxOverlay localFrame={Math.max(0, frame - a2.startFrame)} fps={fps} />
      </Sequence>

      {/* ACT 3A: Split Avatar + Animated $2,000 Spending Chart */}
      <Sequence from={a3a.startFrame} durationInFrames={a3a.durationInFrames}>
        <AvatarLayer src={clipChart} mode="split_left" startFrom={88} />
        <SpendingChartOverlay localFrame={Math.max(0, frame - a3a.startFrame)} fps={fps} />
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
                  localFrame={Math.max(0, frame - a3b.startFrame)}
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
                  localFrame={Math.max(0, frame - a5a.startFrame)}
                  fps={fps}
                  frame={frame}
                  checkDelays={bf01Timings.check_delays as [number, number, number]}
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

          <AvatarLayer src={clipPip} mode="pip_top_right" startFrom={isAct4 ? 40 : isAct5a ? 72 : 12} />
        </AbsoluteFill>
      )}

      {/* ACT 5B: Clean Fullscreen Avatar CTA (bottom 220px clear for Captions!) */}
      <Sequence from={a5b.startFrame} durationInFrames={a5b.durationInFrames}>
        <AvatarLayer src={clipCta} mode="fullscreen" scalePush={1.03} startFrom={100} />
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

export interface HybridBF01SceneProps {
  sceneIndex: 1 | 2 | 3 | 4 | 5 | 6;
  clipSrc: string;
  durationInFrames: number;
}

const SingleAvatarClip: React.FC<{
  clipSrc: string;
  mode: 'fullscreen' | 'split_left' | 'pip_top_right';
  scalePush?: number;
}> = ({ clipSrc, mode, scalePush = 1 }) => {
  const resolved = clipSrc.startsWith('http') || clipSrc.startsWith('/') ? clipSrc : staticFile(clipSrc);
  const videoEl = (
    <Video
      src={resolved}
      muted
      style={{
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        objectPosition: mode === 'split_left' ? '50% 18%' : '50% 22%',
        transform: `scale(${scalePush})`,
      }}
    />
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
              'linear-gradient(180deg, rgba(8,12,20,0.46) 0%, rgba(8,12,20,0.0) 24%, rgba(8,12,20,0.0) 78%, rgba(8,12,20,0.36) 100%)',
          }}
        />
      </AbsoluteFill>
    );
  }

  if (mode === 'split_left') {
    return (
      <AbsoluteFill style={{ backgroundColor: '#080c14' }}>
        <div style={{ position: 'absolute', top: 0, bottom: 0, left: 0, width: 1020, overflow: 'hidden' }}>
          {videoEl}
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background: 'linear-gradient(90deg, rgba(8,12,20,0.10) 0%, rgba(8,12,20,0) 58%, #080c14 98%)',
            }}
          />
        </div>
      </AbsoluteFill>
    );
  }

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

export const HybridBF01Scene: React.FC<HybridBF01SceneProps> = ({
  sceneIndex,
  clipSrc,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const checkDelays: [number, number, number] = [
    Math.max(4, Math.round(durationInFrames * 0.22)),
    Math.max(16, Math.round(durationInFrames * 0.52)),
    Math.max(28, Math.round(durationInFrames * 0.8)),
  ];

  if (sceneIndex === 1) {
    const push = interpolate(frame, [0, Math.max(30, durationInFrames)], [1.0, 1.06], {
      extrapolateRight: 'clamp',
    });
    return (
      <AbsoluteFill style={{ backgroundColor: '#080c14', fontFamily: '"Arial Black", "Helvetica Neue", Arial, sans-serif' }}>
        <SingleAvatarClip clipSrc={clipSrc} mode="fullscreen" scalePush={push} />
        <HeroHookOverlay frame={frame} fps={fps} />
      </AbsoluteFill>
    );
  }

  if (sceneIndex === 2) {
    return (
      <AbsoluteFill style={{ backgroundColor: '#080c14', fontFamily: '"Arial Black", "Helvetica Neue", Arial, sans-serif' }}>
        <SingleAvatarClip clipSrc={clipSrc} mode="split_left" />
        <AiPromptBoxOverlay localFrame={frame} fps={fps} durationInFrames={durationInFrames} />
      </AbsoluteFill>
    );
  }

  if (sceneIndex === 3) {
    return (
      <AbsoluteFill style={{ backgroundColor: '#080c14', fontFamily: '"Arial Black", "Helvetica Neue", Arial, sans-serif' }}>
        <SingleAvatarClip clipSrc={clipSrc} mode="split_left" />
        <SpendingChartOverlay localFrame={frame} fps={fps} durationInFrames={durationInFrames} />
      </AbsoluteFill>
    );
  }

  if (sceneIndex === 6) {
    const push = interpolate(frame, [0, Math.max(30, durationInFrames)], [1.0, 1.04], {
      extrapolateRight: 'clamp',
    });
    return (
      <AbsoluteFill style={{ backgroundColor: '#080c14', fontFamily: '"Arial Black", "Helvetica Neue", Arial, sans-serif' }}>
        <SingleAvatarClip clipSrc={clipSrc} mode="fullscreen" scalePush={push} />
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
      </AbsoluteFill>
    );
  }

  // Scenes 4 & 5: Toy-Prop 3D world + Top-Right real lip-sync PiP
  return (
    <AbsoluteFill style={{ backgroundColor: '#080c14', fontFamily: '"Arial Black", "Helvetica Neue", Arial, sans-serif' }}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{ position: [0, 0.95, 6.0], fov: 38 }}
        gl={{ antialias: true, powerPreference: 'high-performance' }}
      >
        <Stage3DCamera frame={frame} />
        <ToyReflectiveGridStage
          frame={frame}
          accentColor={sceneIndex === 4 ? '#00e0f0' : '#2ee87a'}
          alertStrength={sceneIndex === 4 ? 0.35 : 0}
        />

        {sceneIndex === 4 && (
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

        {sceneIndex === 5 && (
          <group scale={0.84} position={[-0.2, 0.05, 0]}>
            <GiantClipboard3D
              items={['HARD LIMIT $20', 'TARJETA VIRTUAL', 'COMENTA: PRESUPUESTO']}
              localFrame={frame}
              fps={fps}
              frame={frame}
              checkDelays={checkDelays}
            />
          </group>
        )}
      </ThreeCanvas>

      <div
        style={{
          position: 'absolute',
          top: 38,
          left: 48,
          padding: '10px 20px',
          borderRadius: 12,
          backgroundColor: 'rgba(10, 14, 22, 0.85)',
          border: `2px solid ${sceneIndex === 4 ? '#00e0f0' : '#2ee87a'}`,
          color: '#f8fafc',
          fontSize: 22,
          fontWeight: 800,
          letterSpacing: '0.05em',
        }}
      >
        {sceneIndex === 4 ? 'BLACK FRIDAY · ELIGE BIEN' : '3 CANDADOS EN 3 MINUTOS'}
      </div>

      <SingleAvatarClip clipSrc={clipSrc} mode="pip_top_right" />
    </AbsoluteFill>
  );
};
