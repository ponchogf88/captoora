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
import {
  CyberBeatItem,
  WatersChispaCyberEpisode,
} from './compositions/WatersChispaCyberEpisode';
import {
  MadrugadaBeatItem,
  WatersMadrugadaEpisode,
} from './compositions/WatersMadrugadaEpisode';
import { ToyPropExplainerEpisode } from './compositions/ToyPropExplainerEpisode';
import { CARBON_S04_CONFIG } from './data/carbonS04ToyProp';
import { CARBON_S05_CONFIG } from './data/carbonS05ToyProp';
import beatsData from './episodeBeats.json';

const EP01_BEATS = (beatsData as Record<string, BeatItem[]>).EP01;
const EP02_BEATS = (beatsData as Record<string, BeatItem[]>).EP02;
const EP01_EXT_BEATS = (beatsData as Record<string, BeatItem[]>).EP01_EXT ?? EP01_BEATS;
const EP03_BEATS = (beatsData as Record<string, BeatItem[]>).EP03_TONY_CUOTA ?? EP01_BEATS;
const EP05_BEATS = (beatsData as Record<string, NeonBeatItem[]>).EP05_FABLE_HYDROGEN ?? [];
const EP06_BEATS = (beatsData as unknown as Record<string, CyberBeatItem[]>).EP06_HACKEOS_Y_VOZ ?? [];
const EP07_BEATS = (beatsData as unknown as Record<string, CyberBeatItem[]>).EP07_ANTHROPIC_IPO ?? [];
const EP08_BEATS = (beatsData as unknown as Record<string, CyberBeatItem[]>).EP08_AGENTE_CONTABLE ?? [];
const EP09_BEATS = (beatsData as unknown as Record<string, CyberBeatItem[]>).EP09_APPLE_INTELLIGENCE ?? [];
const MAD01_BEATS = (beatsData as unknown as Record<string, MadrugadaBeatItem[]>).MAD01_RENTA_UN_DOLAR ?? [];
const MAD08_BEATS = (beatsData as unknown as Record<string, MadrugadaBeatItem[]>).MAD08_ES_POR_EL_BIEN_DE_TU_CUOTA ?? [];
const MAD09_BEATS = (beatsData as unknown as Record<string, MadrugadaBeatItem[]>).MAD09_SIRI_SUFICIENTE_INTERNET ?? [];

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
      <Composition
        id="WatersChispaEp06"
        component={WatersChispaCyberEpisode}
        durationInFrames={sumFrames(EP06_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'EP. 06 · ¡WATERS! VOZ & DATOS',
          beats: EP06_BEATS,
        }}
      />
      <Composition
        id="WatersChispaEp07"
        component={WatersChispaCyberEpisode}
        durationInFrames={sumFrames(EP07_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'EP. 07 · ANTHROPIC IPO',
          beats: EP07_BEATS,
        }}
      />
      <Composition
        id="WatersChispaEp08"
        component={WatersChispaCyberEpisode}
        durationInFrames={sumFrames(EP08_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'EP. 08 · CLAUDE CONTADOR SAT',
          beats: EP08_BEATS,
        }}
      />
      <Composition
        id="WatersChispaEp09"
        component={WatersChispaCyberEpisode}
        durationInFrames={sumFrames(EP09_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'EP. 09 · SIRI AI SEGURIDAD',
          beats: EP09_BEATS,
        }}
      />
      <Composition
        id="WatersMadrugadaMad01"
        component={WatersMadrugadaEpisode as unknown as React.ComponentType<Record<string, unknown>>}
        durationInFrames={sumFrames(MAD01_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'MAD-01',
          beats: MAD01_BEATS,
        }}
      />
      <Composition
        id="WatersMad08"
        component={WatersMadrugadaEpisode as unknown as React.ComponentType<Record<string, unknown>>}
        durationInFrames={sumFrames(MAD08_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'MAD-08 · ES POR EL BIEN DE TU CUOTA',
          beats: MAD08_BEATS,
        }}
      />
      <Composition
        id="WatersMad09"
        component={WatersMadrugadaEpisode as unknown as React.ComponentType<Record<string, unknown>>}
        durationInFrames={sumFrames(MAD09_BEATS)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episodeLabel: 'MAD-09 · SUFICIENTE INTERNET',
          beats: MAD09_BEATS,
        }}
      />
      <Composition
        id="ToyPropCarbonS04"
        component={ToyPropExplainerEpisode as unknown as React.ComponentType<Record<string, unknown>>}
        durationInFrames={2195}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          config: CARBON_S04_CONFIG,
        }}
      />
      <Composition
        id="ToyPropCarbonS05"
        component={ToyPropExplainerEpisode as unknown as React.ComponentType<Record<string, unknown>>}
        durationInFrames={8195}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          config: CARBON_S05_CONFIG,
        }}
      />
    </>
  );
};
