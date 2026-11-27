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
  FairwindVault3D,
  GiantClipboard3D,
  NeonMarquee3D,
  RankingPodium3D,
  SemiGauge3D,
  SurgeonSplit3D,
  ToyReflectiveGridStage,
} from '../components/ToyPropKit3D';
import {
  KineticCaptionChunk,
  ToyPropEpisodeConfig,
  ToyPropSceneConfig,
} from '../data/carbonS04ToyProp';

const CameraRig: React.FC<{
  frame: number;
  localFrame: number;
  isHook: boolean;
  isLandscape: boolean;
}> = ({ frame, localFrame, isHook, isLandscape }) => {
  const { camera } = useThree();
  const baseZ = isLandscape
    ? isHook
      ? interpolate(localFrame, [0, 75], [5.7, 6.05], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      : 6.15
    : isHook
      ? interpolate(localFrame, [0, 75], [7.45, 7.8], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      : 7.95;
  const swayX = Math.sin(frame * 0.035) * (isLandscape ? 0.14 : 0.12);
  const swayY = (isLandscape ? 0.95 : 1.2) + Math.cos(frame * 0.025) * 0.04;
  camera.position.set(swayX, swayY, baseZ);
  camera.lookAt(0, isLandscape ? 0.16 : 0.12, 0);
  return null;
};

const SceneStage3D: React.FC<{
  scene: ToyPropSceneConfig;
  frame: number;
  localFrame: number;
  fps: number;
  isLandscape: boolean;
}> = ({ scene, frame, localFrame, fps, isLandscape }) => {
  const t = frame / fps;
  const alertPulse =
    scene.id === 'S1_hook' || scene.id === 'L01_hook'
      ? interpolate(t, [0.95, 1.8], [0.15, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
      : scene.alertStrength ?? 0;

  return (
    <>
      <CameraRig
        frame={frame}
        localFrame={localFrame}
        isHook={scene.id === 'S1_hook' || scene.id === 'L01_hook'}
        isLandscape={isLandscape}
      />
      <ToyReflectiveGridStage frame={frame} accentColor={scene.accentColor} alertStrength={alertPulse} />

      {scene.marquee && (
        <NeonMarquee3D
          text={scene.marquee.text}
          sub={scene.marquee.sub}
          color={scene.marquee.color}
          frame={frame}
          position={isLandscape ? [0, 1.56, -0.85] : [0, 1.72, -0.7]}
          scale={isLandscape ? 0.84 : 0.98}
        />
      )}

      {scene.sceneType === 'carbon_crown' && (
        <group scale={isLandscape ? 0.88 : 1} position={isLandscape ? [0, -0.05, 0] : [0, 0, 0]}>
          <CarbonCrownBlock3D frame={frame} fps={fps} />
        </group>
      )}

      {scene.sceneType === 'docker_whale' && (
        <DockerWhaleBox3D frame={frame} localFrame={localFrame} fps={fps} />
      )}

      {scene.sceneType === 'exploit_trio' && (
        <group scale={isLandscape ? 0.92 : 1}>
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
        <group scale={isLandscape ? 0.92 : 1}>
          {typeof scene.gaugeRatio === 'number' && (
            <SemiGauge3D
              targetRatio={scene.gaugeRatio}
              localFrame={localFrame}
              fps={fps}
              position={[1.75, 0.1, -1.1]}
              scale={0.82}
            />
          )}
          <BandagedRepoCube3D frame={frame} localFrame={localFrame} fps={fps} />
        </group>
      )}

      {scene.sceneType === 'binary_doors' && scene.doors && (
        <group scale={isLandscape ? 0.86 : 1}>
          <BinaryDoors3D
            frame={frame}
            leftNum={scene.doors.leftNum}
            leftLabel={scene.doors.leftLabel}
            rightNum={scene.doors.rightNum}
            rightLabel={scene.doors.rightLabel}
          />
        </group>
      )}

      {scene.sceneType === 'giant_clipboard' && (
        <group scale={isLandscape ? 0.82 : 1} position={isLandscape ? [0, 0.05, 0] : [0, 0, 0]}>
          <GiantClipboard3D
            items={scene.clipboardItems ?? ['PLAN A', 'PLAN B', 'COMENTA']}
            localFrame={localFrame}
            fps={fps}
            frame={frame}
          />
        </group>
      )}

      {scene.sceneType === 'fairwind_vault' && (
        <FairwindVault3D frame={frame} localFrame={localFrame} fps={fps} />
      )}

      {scene.sceneType === 'ranking_podium' && (
        <RankingPodium3D frame={frame} localFrame={localFrame} fps={fps} />
      )}

      {scene.sceneType === 'surgeon_split' && (
        <SurgeonSplit3D frame={frame} localFrame={localFrame} fps={fps} />
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
  const isLandscape = width > height;

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
        camera={{ position: [0, isLandscape ? 0.95 : 1.25, isLandscape ? 5.9 : 7.6], fov: isLandscape ? 38 : 40 }}
        gl={{ antialias: true, powerPreference: 'high-performance' }}
      >
        <SceneStage3D
          scene={activeScene}
          frame={frame}
          localFrame={localFrame}
          fps={fps}
          isLandscape={isLandscape}
        />
      </ThreeCanvas>

      {/* Top Hook Banner (visible at full opacity on Frame 0!) */}
      {showHookBanner && (
        <div
          style={{
            position: 'absolute',
            top: isLandscape ? 40 : 130,
            left: isLandscape ? 80 : 52,
            right: isLandscape ? 80 : 52,
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
              fontSize: isLandscape ? 56 : 78,
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
              fontSize: isLandscape ? 52 : 74,
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
              marginTop: isLandscape ? 8 : 14,
              fontSize: isLandscape ? 28 : 38,
              fontWeight: 800,
              color: '#ffd166',
              textShadow: '0 4px 16px rgba(0,0,0,0.95)',
            }}
          >
            {config.hookBanner.kicker}
          </div>
        </div>
      )}

      {/* Landscape Chapter Progress Pill (16:9) */}
      {isLandscape && !showHookBanner && activeScene.chapterLabel && (
        <div
          style={{
            position: 'absolute',
            top: 32,
            left: 44,
            padding: '8px 18px',
            borderRadius: 10,
            backgroundColor: 'rgba(10, 14, 22, 0.82)',
            border: `2px solid ${activeScene.accentColor}`,
            color: '#f8fafc',
            fontSize: 22,
            fontWeight: 800,
            letterSpacing: '0.04em',
            pointerEvents: 'none',
          }}
        >
          {activeScene.chapterLabel}
        </div>
      )}

      {/* Minimal Top Brand Pill when no marquee */}
      {!showHookBanner && !activeScene.marquee && (
        <div
          style={{
            position: 'absolute',
            top: isLandscape ? 32 : 72,
            left: 0,
            right: isLandscape ? 44 : 0,
            display: 'flex',
            justifyContent: isLandscape ? 'flex-end' : 'center',
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
              fontSize: isLandscape ? 20 : 24,
              fontWeight: 800,
              letterSpacing: '0.06em',
            }}
          >
            ¡WATERS! · ¿ORO PURO O PURO HUMO?
          </div>
        </div>
      )}

      {/* Lower-Third Kinetic Captions */}
      {activeCaption && (
        <div
          style={{
            position: 'absolute',
            bottom: isLandscape ? 38 : 205,
            left: isLandscape ? 120 : 56,
            right: isLandscape ? 120 : 56,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            transform: `scale(${captionPop})`,
            pointerEvents: 'none',
          }}
        >
          <div
            style={
              isLandscape
                ? {
                    padding: '10px 28px',
                    borderRadius: 14,
                    backgroundColor: 'rgba(8, 12, 20, 0.72)',
                    border: '1px solid rgba(255,255,255,0.1)',
                  }
                : undefined
            }
          >
            {activeCaption.top && (
              <div
                style={{
                  fontSize: isLandscape ? 26 : 44,
                  fontWeight: 800,
                  lineHeight: 1.05,
                  color: '#ffffff',
                  textShadow: '0 4px 14px rgba(0,0,0,0.98)',
                  WebkitTextStroke: isLandscape ? '1px #000' : '1.5px #000',
                }}
              >
                {activeCaption.top}
              </div>
            )}
            <div
              style={{
                fontSize: isLandscape ? 52 : 82,
                fontWeight: 900,
                lineHeight: 1.04,
                color: activeCaption.highlightColor ?? '#00e0f0',
                textShadow: `0 6px 26px rgba(0,0,0,0.98), 0 0 24px ${activeCaption.highlightColor ?? '#00e0f0'}66`,
                WebkitTextStroke: isLandscape ? '1.8px #000' : '2.5px #000',
              }}
            >
              {activeCaption.main}
            </div>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
