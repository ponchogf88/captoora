#!/usr/bin/env node
/**
 * Genera 4 fondos dinámicos en loop matemático perfecto (1080x1920, 30fps, 8.0s)
 * por nivel estilo Gemini / Halo de Antigravity (incluyendo blanco hueso final).
 * Cero dependencias externas: Node v24 puro -> pipe raw RGB -> FFmpeg libx264 CRF 16.
 */
import fs from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";

const FFMPEG = "/Users/imac/.local/bin/ffmpeg";
const FFPROBE = "/Users/imac/.local/bin/ffprobe";
const OUT_DIR = "/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/caiste-o-no-caiste/biblioteca_ingredientes/02_halos_dinamicos_por_nivel";

const GW = 180;
const GH = 320;
const FPS = 30;
const FRAMES = 240; // 8.0 segundos exactos en loop perfecto sin saltos

const PRESETS = [
  {
    id: "halo_00_blanco_hueso_final",
    base: [253, 246, 234], // #FDF6EA Blanco hueso cálido del canal
    blendMode: "tint",
    orbs: [
      { col: [249, 209, 75], strength: 0.42, radius: 0.56, fx: 1, fy: 1, ax: 0.26, ay: 0.24, cx: 0.28, cy: 0.25, ph: 0.0 },
      { col: [251, 212, 168], strength: 0.46, radius: 0.62, fx: 1, fy: 2, ax: 0.3, ay: 0.2, cx: 0.72, cy: 0.64, ph: 2.1 },
      { col: [255, 253, 246], strength: 0.35, radius: 0.48, fx: 2, fy: 1, ax: 0.22, ay: 0.28, cx: 0.5, cy: 0.45, ph: 4.0 },
      { col: [232, 246, 238], strength: 0.28, radius: 0.5, fx: 1, fy: 1, ax: 0.24, ay: 0.24, cx: 0.25, cy: 0.8, ph: 5.2 },
    ],
  },
  {
    id: "halo_01_facil_gemini_pastel",
    base: [242, 249, 255], // Base luminosa Nivel Fácil (ChatGPT)
    blendMode: "tint",
    orbs: [
      { col: [86, 182, 235], strength: 0.78, radius: 0.56, fx: 1, fy: 1, ax: 0.34, ay: 0.28, cx: 0.3, cy: 0.28, ph: 0.4 },
      { col: [92, 214, 165], strength: 0.72, radius: 0.54, fx: 1, fy: 2, ax: 0.3, ay: 0.24, cx: 0.74, cy: 0.52, ph: 2.3 },
      { col: [250, 224, 132], strength: 0.68, radius: 0.58, fx: 2, fy: 1, ax: 0.26, ay: 0.28, cx: 0.48, cy: 0.8, ph: 4.1 },
      { col: [165, 206, 252], strength: 0.6, radius: 0.5, fx: 1, fy: 1, ax: 0.26, ay: 0.25, cx: 0.7, cy: 0.22, ph: 5.4 },
    ],
  },
  {
    id: "halo_02_medio_terracota_ambar",
    base: [252, 238, 220], // Arena cálida Nivel Medio (Claude)
    blendMode: "tint",
    orbs: [
      { col: [230, 126, 86], strength: 0.72, radius: 0.56, fx: 1, fy: 1, ax: 0.32, ay: 0.28, cx: 0.26, cy: 0.3, ph: 0.7 },
      { col: [248, 192, 74], strength: 0.68, radius: 0.54, fx: 2, fy: 1, ax: 0.28, ay: 0.26, cx: 0.74, cy: 0.48, ph: 2.6 },
      { col: [214, 158, 208], strength: 0.62, radius: 0.52, fx: 1, fy: 2, ax: 0.28, ay: 0.22, cx: 0.45, cy: 0.82, ph: 4.4 },
      { col: [255, 222, 178], strength: 0.52, radius: 0.48, fx: 1, fy: 1, ax: 0.24, ay: 0.25, cx: 0.65, cy: 0.2, ph: 1.5 },
    ],
  },
  {
    id: "halo_03_dificil_antigravity_halo",
    base: [26, 20, 42], // Ciruela nocturna estilo Halo de Antigravity (MadrugadaStageProps3D)
    blendMode: "screen",
    orbs: [
      { col: [168, 85, 247], strength: 0.62, radius: 0.44, fx: 1, fy: 1, ax: 0.3, ay: 0.26, cx: 0.32, cy: 0.32, ph: 0.0 },
      { col: [56, 189, 248], strength: 0.58, radius: 0.42, fx: 1, fy: 2, ax: 0.32, ay: 0.22, cx: 0.7, cy: 0.52, ph: 2.0 },
      { col: [236, 72, 153], strength: 0.52, radius: 0.42, fx: 2, fy: 1, ax: 0.26, ay: 0.28, cx: 0.44, cy: 0.78, ph: 4.1 },
      { col: [245, 185, 98], strength: 0.26, radius: 0.34, fx: 1, fy: 1, ax: 0.22, ay: 0.22, cx: 0.58, cy: 0.38, ph: 5.1 },
    ],
  },
];

function deterministicNoise(x, y, f) {
  let n = (x * 374761393 + y * 668265263 + f * 2147483647) | 0;
  n = ((n ^ (n >>> 13)) * 1274126177) | 0;
  return ((n ^ (n >>> 16)) >>> 0) / 4294967295;
}

async function renderPreset(preset) {
  const outMp4 = path.join(OUT_DIR, `${preset.id}.mp4`);
  const outPng = path.join(OUT_DIR, `${preset.id}.png`);
  const frameBuf = Buffer.alloc(GW * GH * 3);

  await new Promise((resolve, reject) => {
    const ff = spawn(FFMPEG, [
      "-y",
      "-f", "rawvideo",
      "-pix_fmt", "rgb24",
      "-s", `${GW}x${GH}`,
      "-r", String(FPS),
      "-i", "pipe:0",
      "-vf", "scale=1080:1920:flags=bicubic,format=yuv420p",
      "-c:v", "libx264",
      "-preset", "medium",
      "-crf", "16",
      "-movflags", "+faststart",
      "-loglevel", "error",
      outMp4,
    ]);

    let stderr = "";
    ff.stderr.on("data", (d) => { stderr += d.toString(); });
    ff.on("error", reject);
    ff.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg exited ${code}: ${stderr}`));
    });

    const aspect = GH / GW;
    const isScreen = preset.blendMode === "screen";

    function pushNextFrame(frameIdx) {
      while (frameIdx < FRAMES) {
        const theta = (2.0 * Math.PI * frameIdx) / FRAMES;
        const orbState = preset.orbs.map((o) => ({
          x: o.cx + o.ax * Math.sin(theta * o.fx + o.ph),
          y: o.cy + o.ay * Math.cos(theta * o.fy + o.ph * 0.7),
          r2: o.radius * o.radius,
          col: o.col,
          strength: o.strength,
        }));

        let p = 0;
        for (let y = 0; y < GH; y++) {
          const ny = y / GH;
          for (let x = 0; x < GW; x++) {
            const nx = x / GW;
            let r = preset.base[0];
            let g = preset.base[1];
            let b = preset.base[2];

            if (isScreen) {
              // Screen blend matemático suave: los orbes jamás queman el centro a blanco sólido
              for (let k = 0; k < orbState.length; k++) {
                const o = orbState[k];
                const dx = nx - o.x;
                const dy = (ny - o.y) * aspect * 0.56;
                const d2 = dx * dx + dy * dy;
                const a = Math.min(0.82, Math.exp(-d2 / o.r2) * o.strength);
                r = 255 - ((255 - r) * (255 - o.col[0] * a)) / 255;
                g = 255 - ((255 - g) * (255 - o.col[1] * a)) / 255;
                b = 255 - ((255 - b) * (255 - o.col[2] * a)) / 255;
              }
            } else {
              let wSum = 1.0;
              let rAcc = r;
              let gAcc = g;
              let bAcc = b;
              for (let k = 0; k < orbState.length; k++) {
                const o = orbState[k];
                const dx = nx - o.x;
                const dy = (ny - o.y) * aspect * 0.56;
                const d2 = dx * dx + dy * dy;
                const w = Math.exp(-d2 / o.r2) * o.strength * 1.45;
                wSum += w;
                rAcc += o.col[0] * w;
                gAcc += o.col[1] * w;
                bAcc += o.col[2] * w;
              }
              r = rAcc / wSum;
              g = gAcc / wSum;
              b = bAcc / wSum;
            }

            // Dither triangular determinista para cero banding
            const dither = (deterministicNoise(x, y, frameIdx) - 0.5) * 1.4;
            frameBuf[p++] = Math.max(0, Math.min(255, Math.round(r + dither)));
            frameBuf[p++] = Math.max(0, Math.min(255, Math.round(g + dither)));
            frameBuf[p++] = Math.max(0, Math.min(255, Math.round(b + dither)));
          }
        }

        frameIdx++;
        if (!ff.stdin.write(frameBuf)) {
          ff.stdin.once("drain", () => pushNextFrame(frameIdx));
          return;
        }
      }
      ff.stdin.end();
    }

    pushNextFrame(0);
  });

  // Extraer frame muestra a t = 2.0s y verificar con ffprobe
  await new Promise((resolve, reject) => {
    const ffImg = spawn(FFMPEG, ["-y", "-ss", "2.0", "-i", outMp4, "-frames:v", "1", "-loglevel", "error", outPng]);
    ffImg.on("close", (c) => (c === 0 ? resolve() : reject(new Error(`png fail ${c}`))));
  });

  await new Promise((resolve, reject) => {
    const fp = spawn(FFPROBE, ["-v", "error", "-show_entries", "format=duration:stream=codec_name,width,height,r_frame_rate", "-of", "default=noprint_wrappers=1:nokey=1", outMp4]);
    let out = "";
    fp.stdout.on("data", (d) => { out += d.toString(); });
    fp.on("close", (c) => {
      if (c === 0) {
        const size = fs.statSync(outMp4).size;
        console.log(`OK ${preset.id}.mp4 (${size} B) -> ${out.trim().replace(/\n/g, " | ")}`);
        resolve();
      } else reject(new Error(`ffprobe fail ${c}`));
    });
  });
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  for (const preset of PRESETS) {
    await renderPreset(preset);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
