import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { useThree } from '@react-three/fiber';
import {
  BandagedRepoCube3D,
  BinaryDoors3D,
  CarbonCrownBlock3D,
  DockerWhaleBox3D,
  ExploitTrioBlocks3D,
  GiantClipboard3D,
  NeonMarquee3D,
  SemiGauge3D,
  ToyReflectiveGridStage,
} from '../components/ToyPropKit3D';
import {
  KineticCaptionChunk,
  ToyPropEpisodeConfig,
  ToyPropSceneConfig,
} from '../data/carbonS04ToyProp';

const CameraRig: React.FC<{ frame: number; localFrame: number; isHook: boolean }> = ({
  frame,
  localFrame,
  isHook,
}) => {
  const { camera } = useThree();
  const baseZ = isHook
    ? interpolate(localFrame, [0, 75], [7.45, 7.8], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      })
    : 7.95;
  const swayX = Math.sin(frame * 0.035) * 0.12;
  const swayY = 1.2 + Math.cos(frame * 0.025) * 0.04;
  camera.position.set(swayX, swayY, baseZ);
  camera.lookAt(0, 0.12, 0);
  return null;
};

const SceneStage3D: React.FC<{
  scene: ToyPropSceneConfig;
  frame: number;
  localFrame: number;
  fps: number;
}> = ({ scene, frame, localFrame, fps }) => {
  const t = frame / fps;
  const alertPulse =
    scene.id === 'S1_hook'
      ? interpolate(t, [0.95, 1.8], [0.15, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
      : scene.alertStrength ?? 0;

  return (
    <>
      <CameraRig frame={frame} localFrame={localFrame} isHook={scene.id === 'S1_hook'} />
      <ToyReflectiveGridStage frame={frame} accentColor={scene.accentColor} alertStrength={alertPulse} />

      {scene.marquee && (
        <NeonMarquee3D
          text={scene.marquee.text}
          sub={scene.marquee.sub}
          color={scene.marquee.color}
          frame={frame}
          position={[0, 1.72, -0.7]}
          scale={0.98}
        />
      )}

      {scene.sceneType === 'carbon_crown' && <CarbonCrownBlock3D frame={frame} fps={fps} />}

      {scene.sceneType === 'docker_whale' && (
        <DockerWhaleBox3D frame={frame} localFrame={localFrame} fps={fps} />
      )}

      {scene.sceneType === 'exploit_trio' && (
        <group>
          <SemiGauge3D
            targetRatio={scene.gaugeRatio ?? 0.78}
            localFrame={localFrame}
            fps={fps}
            position={[0, 0.15, -1.05]}
            scale={0.95}
          />
          <ExploitTrioBlocks3D frame={frame} localFrame={localFrame} fps={fps} />
        </group>
      )}

      {scene.sceneType === 'bandaged_repo' && (
        <BandagedRepoCube3D frame={frame} localFrame={localFrame} fps={fps} />
      )}

      {scene.sceneType === 'binary_doors' && scene.doors && (
        <BinaryDoors3D
          frame={frame}
          leftNum={scene.doors.leftNum}
          leftLabel={scene.doors.leftLabel}
          rightNum={scene.doors.rightNum}
          rightLabel={scene.doors.rightLabel}
        />
      )}

      {scene.sceneType === 'giant_clipboard' && (
        <GiantClipboard3D
          items={scene.clipboardItems ?? ['PLAN A', 'PLAN B', 'COMENTA']}
          localFrame={localFrame}
          fps={fps}
          frame={frame}
        />
      )}
    </>
  );
};

export interface ToyPropEpisodeProps {
  config: ToyPropEpisodeConfig;
}

export const ToyPropExplainerEpisode: React.FC<ToyPropEpisodeProps> = ({ config }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps;

  const activeScene =
    config.scenes.find((s) => t >= s.startSec && t < s.endSec) ??
    config.scenes[config.scenes.length - 1];

  const sceneStartFrame = Math.round(activeScene.startSec * fps);
  const localFrame = Math.max(0, frame - sceneStartFrame);

  const activeCaption: KineticCaptionChunk | undefined = activeScene.captions.find(
    (c) => t >= c.startSec && t < c.endSec
  );

  const showHookBanner = t < config.hookBanner.untilSec;
  const hookBannerScale = interpolate(frame, [0, 8], [1.04, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const captionStartFrame = activeCaption ? Math.round(activeCaption.startSec * fps) : frame;
  const captionLocal = Math.max(0, frame - captionStartFrame);
  const captionPop = interpolate(captionLocal, [0, 4], [0.92, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#080c14', fontFamily: '"Arial Black", "Helvetica Neue", Arial, sans-serif' }}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{ position: [0, 1.25, 6.1], fov: 40 }}
        gl={{ antialias: true, powerPreference: 'high-performance' }}
      >
        <SceneStage3D scene={activeScene} frame={frame} localFrame={localFrame} fps={fps} />
      </ThreeCanvas>

      {/* Top Hook Banner (visible at full opacity on Frame 0!) */}
      {showHookBanner && (
        <div
          style={{
            position: 'absolute',
            top: 130,
            left: 52,
            right: 52,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            transform: `scale(${hookBannerScale})`,
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              fontSize: 78,
              fontWeight: 900,
              lineHeight: 1.02,
              letterSpacing: '-0.02em',
              color: '#ffffff',
              textShadow: '0 6px 24px rgba(0,0,0,0.95), 0 0 2px #000',
              WebkitTextStroke: '2px #000',
            }}
          >
            {config.hookBanner.line1}{' '}
            {config.hookBanner.line1Highlight && (
              <span
                style={{
                  color: '#ff2b4a',
                  textShadow: '0 0 26px rgba(255,43,74,0.65), 0 6px 20px #000',
                }}
              >
                {config.hookBanner.line1Highlight}
              </span>
            )}
          </div>
          <div
            style={{
              marginTop: 4,
              fontSize: 74,
              fontWeight: 900,
              lineHeight: 1.02,
              letterSpacing: '-0.02em',
              color: '#ffffff',
              textShadow: '0 6px 24px rgba(0,0,0,0.95)',
              WebkitTextStroke: '2px #000',
            }}
          >
            {config.hookBanner.line2}
          </div>
          <div
            style={{
              marginTop: 14,
              fontSize: 38,
              fontWeight: 800,
              color: '#ffd166',
              textShadow: '0 4px 16px rgba(0,0,0,0.95)',
            }}
          >
            {config.hookBanner.kicker}
          </div>
        </div>
      )}

      {/* Minimal Top-Right Brand Pill on subsequent scenes */}
      {!showHookBanner && !activeScene.marquee && (
        <div
          style={{
            position: 'absolute',
            top: 72,
            left: 0,
            right: 0,
            display: 'flex',
            justifyContent: 'center',
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              padding: '8px 22px',
              borderRadius: 999,
              backgroundColor: 'rgba(10, 14, 22, 0.72)',
              border: `2px solid ${activeScene.accentColor}`,
              color: '#e2e8f0',
              fontSize: 24,
              fontWeight: 800,
              letterSpacing: '0.06em',
            }}
          >
            ¡WATERS! · ¿ORO PURO O PURO HUMO?
          </div>
        </div>
      )}

      {/* Lower-Third Kinetic Captions (above TikTok/Reels HUD) */}
      {activeCaption && (
        <div
          style={{
            position: 'absolute',
            bottom: 205,
            left: 56,
            right: 56,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            transform: `scale(${captionPop})`,
            pointerEvents: 'none',
          }}
        >
          {activeCaption.top && (
            <div
              style={{
                fontSize: 44,
                fontWeight: 800,
                lineHeight: 1.05,
                color: '#ffffff',
                textShadow: '0 4px 14px rgba(0,0,0,0.98)',
                WebkitTextStroke: '1.5px #000',
              }}
            >
              {activeCaption.top}
            </div>
          )}
          <div
            style={{
              fontSize: 82,
              fontWeight: 900,
              lineHeight: 1.04,
              color: activeCaption.highlightColor ?? '#00e0f0',
              textShadow: `0 6px 26px rgba(0,0,0,0.98), 0 0 24px ${activeCaption.highlightColor ?? '#00e0f0'}66`,
              WebkitTextStroke: '2.5px #000',
            }}
          >
            {activeCaption.main}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
