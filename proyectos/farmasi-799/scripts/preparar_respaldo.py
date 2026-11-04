"""Rebuild the text-only handoff package. Never generates, uploads or deletes photos."""
from pathlib import Path
import argparse, collections, hashlib, json, shutil

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--dest', type=Path, required=True)
    args = parser.parse_args()
    source, dest = args.source.resolve(), args.dest.resolve()
    production = source / 'produccion'
    dest.mkdir(parents=True, exist_ok=True)
    registry = json.loads((production / 'REGISTRO_EDICION.json').read_text())
    readback = json.loads((production / 'RESPALDO_DRIVE_READBACK.json').read_text())
    prompts = json.loads((production / 'PROMPTS_EJECUTADOS_RECUPERADOS.json').read_text())
    known = {x['source_name']: x for x in registry['files']}
    sources = []
    for item in registry['files']:
        # Current status is distinct from rejected historical version fields.
        sources.append({k: item[k] for k in ('source_name', 'source_id', 'source_url', 'estado', 'lote_actual', 'version_actual', 'decision_usuario_actual', 'approved_jpg_drive', 'revision_drive_url') if k in item})
    assert len(sources) == 799 and len({x['source_id'] for x in sources}) == 799
    dump(dest / 'registros/fuentes_799.json', sources)
    dump(dest / 'prompts/ejecutados_exactos.json', prompts)
    dump(dest / 'registros/drive_verificado.json', readback)
    dump(dest / 'registros/estado_799.json', dict(collections.Counter(x['estado'] for x in sources)))
    artifacts = []
    for state, section, directory in [('aprobada', 'approved', production / 'aprobadas/JPG'), ('en_revision', 'review', production / 'lote_04_diversas')]:
        for item in readback.get(section, {}).get('results', []):
            file = directory / item['title']
            entry = {'file_name': item['title'], 'source_name': item['title'].split('_')[0] + '.JPG', 'estado': state, 'drive_id': item['id'], 'drive_url': item['url'], 'cloud_bytes': int(item['size'])}
            if file.exists():
                entry.update(bytes=file.stat().st_size, sha256=hashlib.sha256(file.read_bytes()).hexdigest())
                assert entry['bytes'] == entry['cloud_bytes'], file
            artifacts.append(entry)
    dump(dest / 'registros/artefactos.json', artifacts)
    hashes = []
    for file in sorted((source / 'piloto/originales').glob('*.JPG')):
        hashes.append({'source_name': file.name, 'sha256': hashlib.sha256(file.read_bytes()).hexdigest(), 'bytes': file.stat().st_size, 'drive_url': known.get(file.name, {}).get('source_url')})
    dump(dest / 'registros/hashes_originales_inspeccionados.json', hashes)
    for name in ['lote_01/manifiesto.json', 'lote_03_diez/manifiesto.json', 'lote_04_diversas/seleccion.json', 'lote_04_diversas/procedencia_verificacion.json', 'lote_04_diversas/pendientes_omitidas_por_diversidad.json']:
        path = dest / 'historial' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(production / name, path)
    for name in ['FARMASI_799_REQUISITOS.md', 'PLAN_FARMASI_799.md']:
        shutil.copy2(source.parents[1] / name, dest / name)
    scripts = dest / 'scripts'
    scripts.mkdir(exist_ok=True)
    shutil.copy2(Path(__file__), scripts / 'preparar_respaldo.py')
    print(json.dumps({'sources': len(sources), 'exact_prompts': len(prompts), 'approved_artifacts': sum(x['estado'] == 'aprobada' for x in artifacts), 'review_artifacts': sum(x['estado'] == 'en_revision' for x in artifacts), 'original_hashes': len(hashes)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
