import { createHash } from 'node:crypto';
import { chromium } from 'playwright';
import { parse } from 'csv-parse/sync';
import { mkdir, readFile, readdir, stat, unlink, writeFile, rename } from 'node:fs/promises';
import path from 'node:path';
import { createInterface } from 'node:readline/promises';

const config = JSON.parse(await readFile(process.env.CAPTOORA_MOTORES ?? 'motores.json', 'utf8'));
const engines = Object.keys(config);
const defaultEngines = engines.filter(name => config[name]?.activo !== false);
const listedRoutes = [...new Set([...engines, 'meta', 'dola-ai', 'one', 'google-fotos-web', 'google-fotos-android'])];
if (engines.some(name => !/^[a-zA-Z0-9_-]+$/.test(name))) {
  throw new Error('Cada motor necesita un ID que pueda usarse como nombre de archivo.');
}
const direct = process.argv[2] === 'foto';
const mode = direct ? 'ejecutar' : process.argv[2];
const activeEngines = mode === 'calibrar'
  ? [process.argv[3]]
  : mode === 'ejecutar' && !direct && process.argv.length > 4
    ? [...new Set(process.argv.slice(4))]
    : defaultEngines;

if (!['sesion', 'calibrar', 'ejecutar', 'ficha'].includes(mode) || activeEngines.some(name => !engines.includes(name))) {
  console.error('Uso: node piloto.mjs sesion | calibrar MOTOR | ejecutar FOTO_ID [MOTOR...] | ficha FOTO_ID | foto ARCHIVO [RECETA]');
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
  let photoId = process.argv[3];
  let recipe;
  if (direct) {
    if (!photoId || process.argv.length > 5) throw new Error('Uso: node piloto.mjs foto ARCHIVO [RECETA]');
    photo = path.resolve(photoId);
    recipe = process.argv[4];
  } else {
    const rows = parse(await readFile(path.join(workRoot, 'cola.csv'), 'utf8'), { columns: true, skip_empty_lines: true, bom: true });
    const matches = rows.filter(row => row.foto_id === photoId);
    if (!/^[a-zA-Z0-9_-]+$/.test(photoId ?? '') || matches.length !== 1) {
      throw new Error('Indica un foto_id único de cola.csv.');
    }
    photo = path.resolve(workRoot, matches[0].archivo);
    recipe = matches[0].receta;
  }
  if (!/\.(jpe?g|png|webp)$/i.test(photo) || !(await stat(photo)).isFile()) {
    throw new Error('Usa un archivo JPG, PNG o WebP.');
  }
  const recipes = {
    oscuro: 'Mantén el fondo oscuro y su gradación. Recupera detalle visible en las sombras del sujeto y conserva los negros. Evita halos en pelo y ropa.',
    blanco: 'Neutraliza dominantes y suaviza desigualdades en el fondo blanco. Conserva sombras de contacto y detalle en pelo, piel y ropa blanca.',
    grupo: 'Conserva la cantidad, la posición y la identidad de todas las personas. Equilibra la luz entre rostros respetando el tono de piel, las expresiones, las oclusiones y las manos.',
    producto: 'Conserva la forma, la posición, los colores, los logotipos y los textos visibles del producto.',
  };
  const tags = (recipe ?? '').split('+').map(tag => tag.trim().toLowerCase()).filter(Boolean);
  if (tags.some(tag => !Object.hasOwn(recipes, tag)) || (tags.includes('blanco') && tags.includes('oscuro'))) {
    throw new Error('Receta inválida. Usa blanco u oscuro, y combina con grupo o producto cuando corresponda.');
  }
  const basePrompt = (await readFile('prompt.txt', 'utf8')).trim();
  if (!basePrompt) throw new Error('Falta el prompt.');
  prompt = [basePrompt, ...Object.keys(recipes).filter(tag => tags.includes(tag)).map(tag => recipes[tag])].join('\n\n');
  if (direct) {
    const digest = createHash('sha256').update(JSON.stringify([prompt,
      createHash('sha256').update(await readFile(photo)).digest('hex')])).digest('hex');
    photoId = 'foto-' + digest.slice(0, 24);
  }
  directory = path.join(workRoot, 'borradores', photoId);
  await mkdir(directory, { recursive: true });
  existing = await readdir(directory);
  if (direct) {
    console.log(JSON.stringify({ fotoId: photoId, foto: photo, prompt, borradores: directory }));
  }
  if (mode === 'ficha') {
    console.log(JSON.stringify({ fotoId: photoId, foto: photo, prompt, borradores: directory,
      motores: Object.fromEntries(listedRoutes.map(name => [name, {
        url: config[name]?.url ?? null,
        modelo: config[name]?.modelo ?? null,
        activo: defaultEngines.includes(name),
        calibrado: isCalibrated(name),
        destino: path.join(directory, name + '.jpg'),
        archivo: existing.find(file => file.startsWith(name + '.') && /\.(jpe?g|png|webp)$/i.test(file)) ?? null,
        pendiente: existing.includes(name + '.pendiente'),
      }])),
    }, null, 2));
    process.exit(0);
  }
}

function isCalibrated(name) {
  const engine = config[name];
  const steps = engine?.pasos;
  return Boolean(engine?.url && Array.isArray(steps)
    && steps.some(step => ['foto', 'elegir_foto'].includes(step?.accion))
    && steps.some(step => step?.accion === 'prompt')
    && steps.at(-1)?.accion === 'descarga'
    && steps.every(step => ['clic', 'elegir_foto', 'foto', 'prompt', 'descarga'].includes(step?.accion)
      && typeof step.selector === 'string' && step.selector.trim()));
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
    if (mode === 'ejecutar') {
      if (existing.includes(name + '.pendiente')) {
        throw new Error('Hay una ejecución pendiente. Revisa la pestaña antes de repetir.');
      }
      if (!isCalibrated(name)) throw new Error('Calibra este motor en motores.json.');
    }
    const page = await context.newPage();
    await page.goto(config[name].url, { waitUntil: 'domcontentloaded' });
    if (mode === 'calibrar') await page.pause();
    if (mode === 'ejecutar') return run(name, page);
    return 'Página abierta';
  }));
  jobs.forEach((job, index) => console.log(activeEngines[index], job.status === 'fulfilled' ? job.value : job.reason.message));
  if (jobs.some(job => job.status === 'rejected')) process.exitCode = 1;
  if (mode === 'sesion' || (mode === 'ejecutar' && process.exitCode && process.stdin.isTTY)) {
    await ask.question('Pulsa Enter cuando termines de revisar Chrome. ');
  }
} finally {
  ask.close();
  if (browser) await browser.close();
  else await context.close();
}
