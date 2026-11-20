import React from 'react';
import { Composition } from 'remotion';
import { AgyWatersEpisode } from './compositions/AgyWatersEpisode';
import {
  BeatItem,
  WatersHybridEpisode,
} from './compositions/WatersHybridEpisode';
import {
  NeonBeatItem,
  WatersNeon3DEpisode,
} from './compositions/WatersNeon3DEpisode';
import beatsData from './episodeBeats.json';

const EP01_BEATS = (beatsData as Record<string, BeatItem[]>).EP01;
const EP02_BEATS = (beatsData as Record<string, BeatItem[]>).EP02;
const EP01_EXT_BEATS = (beatsData as Record<string, BeatItem[]>).EP01_EXT ?? EP01_BEATS;
const EP03_BEATS = (beatsData as Record<string, BeatItem[]>).EP03_TONY_CUOTA ?? EP01_BEATS;
const EP05_BEATS = (beatsData as Record<string, NeonBeatItem[]>).EP05_FABLE_HYDROGEN ?? [];

const sumFrames = (beats: { durationInFrames: number }[]) =>
  Math.max(1, beats.reduce((acc, b) => acc + b.durationInFrames, 0));

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="AgyWatersGTA6"
        component={AgyWatersEpisode}
        durationInFrames={1440}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="WatersHybridEp01"
        component={WatersHybridEpisode}
        durationInFrames={sumFrames(EP01_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'EP. 01 · ¡WATERS!',
          beats: EP01_BEATS,
        }}
      />
      <Composition
        id="WatersHybridEp01Ext"
        component={WatersHybridEpisode}
        durationInFrames={sumFrames(EP01_EXT_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'EP. 01 · GTA 6 ($3B)',
          beats: EP01_EXT_BEATS,
        }}
      />
      <Composition
        id="WatersHybridEp02"
        component={WatersHybridEpisode}
        durationInFrames={sumFrames(EP02_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'EP. 02 · ¡WATERS!',
          beats: EP02_BEATS,
        }}
      />
      <Composition
        id="WatersHybridEp03"
        component={WatersHybridEpisode}
        durationInFrames={sumFrames(EP03_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'EP. 03 · 0% CUOTA IA',
          beats: EP03_BEATS,
        }}
      />
      <Composition
        id="WatersNeon3DEp05"
        component={WatersNeon3DEpisode}
        durationInFrames={sumFrames(EP05_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'EP. 05 · FABLE vs HYDROGEN',
          beats: EP05_BEATS,
        }}
      />
    </>
  );
};
