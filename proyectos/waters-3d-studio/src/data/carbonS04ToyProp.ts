export type ToyPropSceneType =
  | 'carbon_crown'
  | 'docker_whale'
  | 'exploit_trio'
  | 'bandaged_repo'
  | 'binary_doors'
  | 'giant_clipboard'
  | 'fairwind_vault'
  | 'ranking_podium'
  | 'surgeon_split';

export interface KineticCaptionChunk {
  startSec: number;
  endSec: number;
  top?: string;
  main: string;
  highlightColor?: string;
}

export interface ToyPropSceneConfig {
  id: string;
  chapterLabel?: string;
  startSec: number;
  endSec: number;
  accentColor: string;
  alertStrength?: number;
  sceneType: ToyPropSceneType;
  marquee?: {
    text: string;
    sub?: string;
    color: string;
  };
  gaugeRatio?: number;
  doors?: {
    leftNum?: string;
    leftLabel: string;
    rightNum?: string;
    rightLabel: string;
  };
  clipboardItems?: string[];
  captions: KineticCaptionChunk[];
}

export interface ToyPropEpisodeConfig {
  hookBanner: {
    untilSec: number;
    line1: string;
    line1Highlight?: string;
    line2: string;
    kicker: string;
  };
  scenes: ToyPropSceneConfig[];
}

export const CARBON_S04_CONFIG: ToyPropEpisodeConfig = {
  hookBanner: {
    untilSec: 7.12,
    line1: '¿EL',
    line1Highlight: 'REY',
    line2: 'DE CIBERSEGURIDAD?',
    kicker: 'sin ver pruebas, NO',
  },
  scenes: [
    {
      id: 'S1_hook',
      startSec: 0,
      endSec: 7.12,
      accentColor: '#00e0f0',
      alertStrength: 1,
      sceneType: 'carbon_crown',
      captions: [
        { startSec: 0.0, endSec: 1.15, top: '¿GEMINI 4', main: 'CARBON', highlightColor: '#00e0f0' },
        { startSec: 1.15, endSec: 2.25, top: 'EL NUEVO', main: 'REY?', highlightColor: '#ff3355' },
        { startSec: 2.25, endSec: 3.55, top: 'EN', main: 'CIBERSEGURIDAD', highlightColor: '#00e0f0' },
        { startSec: 3.55, endSec: 4.95, top: 'AQUÍ NO', main: 'CREEMOS', highlightColor: '#ffffff' },
        { startSec: 4.95, endSec: 7.12, top: 'SIN VER', main: 'PRUEBAS', highlightColor: '#fbbf24' },
      ],
    },
    {
      id: 'S2_secbench',
      startSec: 7.12,
      endSec: 17.93,
      accentColor: '#2ee87a',
      alertStrength: 0,
      sceneType: 'docker_whale',
      marquee: {
        text: '88.2%',
        sub: 'SEC-BENCH PRO',
        color: '#2ee87a',
      },
      captions: [
        { startSec: 7.12, endSec: 9.2, top: 'PRUEBA', main: 'UNO', highlightColor: '#fbbf24' },
        { startSec: 9.2, endSec: 11.4, top: 'SEC-BENCH', main: 'PRO', highlightColor: '#00e0f0' },
        { startSec: 11.4, endSec: 13.7, top: 'CARBON', main: '88.2%', highlightColor: '#2ee87a' },
        { startSec: 13.7, endSec: 15.9, top: 'FALLOS EN', main: 'DOCKER', highlightColor: '#38bdf8' },
        { startSec: 15.9, endSec: 17.93, top: 'ARRIBA DE', main: 'ASTRA', highlightColor: '#fbbf24' },
      ],
    },
    {
      id: 'S3_exploitgym',
      startSec: 17.93,
      endSec: 34.1,
      accentColor: '#00d9ea',
      alertStrength: 0,
      sceneType: 'exploit_trio',
      marquee: {
        text: '54.8%',
        sub: 'EXPLOITGYM',
        color: '#00d9ea',
      },
      gaugeRatio: 0.78,
      captions: [
        { startSec: 17.93, endSec: 20.1, top: 'PRUEBA', main: 'DOS', highlightColor: '#fbbf24' },
        { startSec: 20.1, endSec: 22.5, top: 'EXPLOIT', main: 'GYM', highlightColor: '#00d9ea' },
        { startSec: 22.5, endSec: 25.3, top: 'BERKELEY', main: 'MAX PLANCK', highlightColor: '#ffffff' },
        { startSec: 25.3, endSec: 28.0, top: 'CARBON', main: '54.8%', highlightColor: '#00d9ea' },
        { startSec: 28.0, endSec: 30.8, top: 'ASTRA', main: '42.4%', highlightColor: '#fb923c' },
        { startSec: 30.8, endSec: 34.1, top: 'OPUS 5.5', main: '34.5%', highlightColor: '#a855f7' },
      ],
    },
    {
      id: 'S4_cwebench',
      startSec: 34.1,
      endSec: 49.23,
      accentColor: '#a855f7',
      alertStrength: 0,
      sceneType: 'bandaged_repo',
      marquee: {
        text: '71%',
        sub: 'CWE-BENCH',
        color: '#a855f7',
      },
      captions: [
        { startSec: 34.1, endSec: 36.4, top: 'PRUEBA', main: 'TRES', highlightColor: '#fbbf24' },
        { startSec: 36.4, endSec: 39.2, top: 'CWE-BENCH', main: 'COLLINEAR', highlightColor: '#a855f7' },
        { startSec: 39.2, endSec: 42.4, top: 'PARCHANDO', main: '71%', highlightColor: '#2ee87a' },
        { startSec: 42.4, endSec: 45.2, top: 'SIN PISTA', main: 'PREVIA', highlightColor: '#ffffff' },
        { startSec: 45.2, endSec: 49.23, top: '68% OPENAI', main: '67% CLAUDE', highlightColor: '#fbbf24' },
      ],
    },
    {
      id: 'S5_letrachiquita',
      startSec: 49.23,
      endSec: 64.12,
      accentColor: '#ff3366',
      alertStrength: 0.45,
      sceneType: 'binary_doors',
      doors: {
        leftNum: '1',
        leftLabel: 'QUEMA TOKENS',
        rightNum: '2',
        rightLabel: 'NO SE SUMAN',
      },
      captions: [
        { startSec: 49.23, endSec: 51.8, top: 'PERO VA LA', main: 'LETRA', highlightColor: '#ff3366' },
        { startSec: 51.8, endSec: 54.4, top: 'CHIQUITA:', main: 'NO SUMAN', highlightColor: '#00e0f0' },
        { startSec: 54.4, endSec: 57.2, top: 'ASTRA 100', main: 'EXPLOITBENCH', highlightColor: '#fbbf24' },
        { startSec: 57.2, endSec: 60.4, top: 'CLAUDE FABLE', main: 'CÓDIGO DIARIO', highlightColor: '#38bdf8' },
        { startSec: 60.4, endSec: 64.12, top: 'CARBON QUEMA', main: 'MÁS TOKENS', highlightColor: '#ff3366' },
      ],
    },
    {
      id: 'S6_cta',
      startSec: 64.12,
      endSec: 73.14,
      accentColor: '#2ee87a',
      alertStrength: 0,
      sceneType: 'giant_clipboard',
      clipboardItems: ['AUDITORÍAS', 'NO PARA TODO', 'COMENTA: CARBON'],
      captions: [
        { startSec: 64.12, endSec: 66.8, top: 'EN TU PLAN', main: 'GOOGLE PRO', highlightColor: '#38bdf8' },
        { startSec: 66.8, endSec: 69.0, top: 'ÚSALO EN', main: 'AUDITORÍAS', highlightColor: '#2ee87a' },
        { startSec: 69.0, endSec: 70.7, top: 'NO PARA', main: 'TODO', highlightColor: '#fbbf24' },
        { startSec: 70.7, endSec: 73.14, top: 'COMENTA', main: 'CARBON', highlightColor: '#00e0f0' },
      ],
    },
  ],
};
