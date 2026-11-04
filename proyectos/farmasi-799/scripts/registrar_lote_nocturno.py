"""Register visually reviewed, cloud-verified outputs. No generation or uploads."""
from pathlib import Path
import argparse, hashlib, json

def write(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

parser = argparse.ArgumentParser()
parser.add_argument('--folder', required=True)
parser.add_argument('--readback', required=True)
parser.add_argument('--reviewed', nargs='+', required=True)
parser.add_argument('--production', type=Path, default=Path(__file__).resolve().parent / 'produccion')
args = parser.parse_args()
root = args.production.resolve()
folder = root / args.folder
provider = json.loads(Path(args.readback).read_text())
reviewed = set(args.reviewed)
registry = json.loads((root / 'REGISTRO_EDICION.json').read_text())
prompts = json.loads((root / 'PROMPTS_EJECUTADOS_RECUPERADOS.json').read_text())
plan_file = root / 'noche_2026-11-04/PLAN_NOCTURNO.json'
plan = json.loads(plan_file.read_text())
completed = {x['source_name']: x for x in plan['completadas']}
manifest = []
for file in provider['results']:
    name = file['title'].split('_')[0]
    assert name in reviewed, f'Not visually reviewed: {name}'
    local = folder / file['title']
    assert local.is_file() and local.stat().st_size == int(file['size'])
    record = json.loads((folder / (name + '_ejecucion.json')).read_text())
    assert record['generated_path'] and record['estado'] != 'bloqueada_herramienta'
    source_name = record['source_name']
    manifest.append({**record, 'estado': 'en_revision', 'output': file,
                     'sha256_jpg': hashlib.sha256(local.read_bytes()).hexdigest(),
                     'revision_visual': 'Inspeccionada contra fuente; pendiente aprobacion cliente; no certificacion pixel a pixel o microtexto.'})
    entry = next(x for x in registry['files'] if x['source_name'] == source_name)
    assert entry['estado'] != 'aprobada', f'Would overwrite approved source: {source_name}'
    entry.update(estado='en_revision', lote_actual=args.folder, version_actual='v02',
                 decision_usuario_actual='pendiente', revision_drive_url=file['url'])
    completed[source_name] = {'source_name': source_name, 'drive_id': file['id'],
                              'drive_url': file['url'], 'lote': args.folder}
    prompt = {'id': args.folder + '_' + name, 'source': source_name,
              'prompt': record['prompt'], 'provenance': 'exact_execution_store',
              'status': 'awaiting_user_approval', 'model': record['model']}
    prompts = [x for x in prompts if x['id'] != prompt['id']] + [prompt]
assert len(completed) <= plan['limite_nuevas']
plan['completadas'] = list(completed.values())
plan['producidas_verificadas'] = len(completed)
plan['restantes_hasta_limite'] = plan['limite_nuevas'] - len(completed)
back_file = root / 'RESPALDO_DRIVE_READBACK.json'
back = json.loads(back_file.read_text())
section = 'review_' + args.folder
back.setdefault('extra_review_sources', {})[section] = args.folder
back[section] = provider
write(folder / 'procedencia_verificacion.json', {'files': manifest, 'readback': provider})
write(root / 'REGISTRO_EDICION.json', registry)
write(root / 'PROMPTS_EJECUTADOS_RECUPERADOS.json', prompts)
write(back_file, back)
write(plan_file, plan)
print(json.dumps({'registered': len(manifest), 'night_verified': len(completed),
                  'remaining': plan['restantes_hasta_limite']}))
