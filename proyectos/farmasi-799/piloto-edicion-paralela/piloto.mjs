import { chromium } from 'playwright';
import { parse } from 'csv-parse/sync';
import { mkdir, readFile, readdir, stat, unlink, writeFile, rename } from 'node:fs/promises';
import path from 'node:path';
import { createInterface } from 'node:readline/promises';

const engines = ['picsart', 'grok', 'gemini', 'chatgpt'];
const config = JSON.parse(await readFile(process.env.CAPTOORA_MOTORES ?? 'motores.json', 'utf8'));
const mode = process.argv[2];
const activeEngines = mode === 'calibrar'
  ? [process.argv[3]]
  : mode === 'ejecutar' && process.argv.length > 4
    ? [...new Set(process.argv.slice(4))]
    : engines;

if (!['sesion', 'calibrar', 'ejecutar', 'ficha'].includes(mode) || activeEngines.some(name => !engines.includes(name))) {
  console.error('Uso: node piloto.mjs sesion | calibrar MOTOR | ejecutar FOTO_ID [MOTOR...] | ficha FOTO_ID');
  process.exit(1);
}

let photo;
let prompt;
let directory;
let existing = [];
if (['ejecutar', 'ficha'].includes(mode)) {
  const workRoot = process.env.CAPTOORA_WORK_DIR;
  if (!workRoot || !path.isAbsolute(workRoot)) {
    throw new Error('Define CAPTOORA_WORK_DIR con una carpeta absoluta de trabajo en el SSD externo.');
  }
  const rows = parse(await readFile(path.join(workRoot, 'cola.csv'), 'utf8'), { columns: true, skip_empty_lines: true, bom: true });
  const photoId = process.argv[3];
  const matches = rows.filter(row => row.foto_id === photoId);
  if (!/^[a-zA-Z0-9_-]+$/.test(photoId ?? '') || matches.length !== 1) {
    throw new Error('Indica un foto_id único de cola.csv.');
  }
  photo = path.resolve(workRoot, matches[0].archivo);
  if (!/\.(jpe?g|png|webp)$/i.test(photo) || !(await stat(photo)).isFile()) {
    throw new Error('Usa un archivo JPG, PNG o WebP.');
  }
  prompt = (await readFile('prompt.txt', 'utf8')).trim();
  if (!prompt) throw new Error('Falta el prompt.');
  directory = path.join(workRoot, 'borradores', photoId);
  await mkdir(directory, { recursive: true });
  existing = await readdir(directory);
  if (mode === 'ficha') {
    console.log(JSON.stringify({ fotoId: photoId, foto: photo, prompt, borradores: directory,
      motores: Object.fromEntries([...engines, 'meta', 'google-fotos-web', 'google-fotos-android'].map(name => [name, {
        url: config[name]?.url ?? null,
        destino: path.join(directory, name + '.jpg'),
        archivo: existing.find(file => file.startsWith(name + '.') && /\.(jpe?g|png|webp)$/i.test(file)) ?? null,
        pendiente: existing.includes(name + '.pendiente'),
      }])),
    }, null, 2));
    process.exit(0);
  }
  for (const name of activeEngines) {
    if (existing.some(file => /\.(jpe?g|png|webp)$/i.test(file) && file.startsWith(name + '.'))) continue;
    const steps = config[name]?.pasos;
    if (!Array.isArray(steps) || !steps.some(step => ['foto', 'elegir_foto'].includes(step.accion)) ||
        !steps.some(step => step.accion === 'prompt') || steps.at(-1)?.accion !== 'descarga' ||
        steps.some(step => !['clic', 'elegir_foto', 'foto', 'prompt', 'descarga'].includes(step.accion) ||
          typeof step.selector !== 'string' || !step.selector.trim())) {
      throw new Error('Calibra los pasos de ' + name + ' en motores.json.');
    }
  }
  if (activeEngines.some(name => existing.includes(name + '.pendiente'))) {
    throw new Error('Hay una ejecución pendiente. Revisa la pestaña y el marcador antes de repetir.');
  }
}

const profile = path.resolve('.chrome-captoora');
const endpoint = process.env.CAPTOORA_CDP_URL;
const browser = endpoint ? await chromium.connectOverCDP(endpoint) : null;
const context = browser
  ? browser.contexts()[0] ?? await browser.newContext({ acceptDownloads: true })
  : await chromium.launchPersistentContext(profile, { channel: 'chrome', headless: false, acceptDownloads: true, downloadsPath: directory });
context.setDefaultTimeout(15000);

async function run(name, page) {
  const marker = path.join(directory, name + '.pendiente');
  await writeFile(marker, 'Revisa si el motor recibió la foto o la generación antes de repetir.\n', { flag: 'wx' });
  for (const step of config[name].pasos) {
    const locator = page.locator(step.selector);
    switch (step.accion) {
      case 'clic':
        await locator.click();
        break;
      case 'elegir_foto': {
        const [chooser] = await Promise.all([page.waitForEvent('filechooser'), locator.click()]);
        await chooser.setFiles(photo);
        break;
      }
      case 'foto':
        await locator.setInputFiles(photo);
        break;
      case 'prompt':
        await locator.fill(prompt);
        break;
      case 'descarga': {
        await locator.waitFor({ timeout: 480000 });
        const [download] = await Promise.all([page.waitForEvent('download'), locator.click()]);
        const extension = path.extname(download.suggestedFilename()).toLowerCase();
        if (!['.jpg', '.jpeg', '.png', '.webp'].includes(extension)) {
          throw new Error('Descarga inesperada: ' + download.suggestedFilename());
        }
        const output = path.join(directory, name + extension);
        const partial = output + '.partial';
        await download.saveAs(partial);
        if (!(await stat(partial)).size) throw new Error('La descarga está vacía.');
        await rename(partial, output);
        await unlink(marker);
        return output;
      }
    }
  }
}

const ask = createInterface({ input: process.stdin, output: process.stdout });
try {
  const jobs = await Promise.allSettled(activeEngines.map(async name => {
    if (mode === 'ejecutar' && existing.some(file => file.startsWith(name + '.') && /\.(jpe?g|png|webp)$/i.test(file))) {
      return 'Archivo ya guardado';
    }
    const page = await context.newPage();
    await page.goto(config[name].url, { waitUntil: 'domcontentloaded' });
    if (mode === 'calibrar') await page.pause();
    if (mode === 'ejecutar') return run(name, page);
    return 'Página abierta';
  }));
  jobs.forEach((job, index) => console.log(activeEngines[index], job.status === 'fulfilled' ? job.value : job.reason.message));
  if (jobs.some(job => job.status === 'rejected')) process.exitCode = 1;
  if (mode === 'sesion' || (mode === 'ejecutar' && process.exitCode)) {
    await ask.question('Pulsa Enter cuando termines de revisar Chrome. ');
  }
} finally {
  ask.close();
  if (browser) await browser.close();
  else await context.close();
}
