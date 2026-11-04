"""Rebuild the text-only handoff package. Never generates, uploads or deletes photos."""
from pathlib import Path
import argparse, collections, hashlib, json, re, shutil

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
    approved_counts = collections.Counter(x['title'].split('_')[0] for x in readback.get('approved', {}).get('results', []))
    assert all(n == 1 for n in approved_counts.values()), 'Duplicated versions in approved Drive folder; reconcile before backup'
    known = {x['source_name']: x for x in registry['files']}
    sources = []
    for item in registry['files']:
        # Current status is distinct from rejected historical version fields.
        sources.append({k: item[k] for k in ('source_name', 'source_id', 'source_url', 'estado', 'lote_actual', 'version_actual', 'decision_usuario_actual', 'approved_jpg_drive', 'revision_drive_url', 'correccion_en_revision') if k in item})
    assert len(sources) == 799 and len({x['source_id'] for x in sources}) == 799
    dump(dest / 'registros/fuentes_799.json', sources)
    dump(dest / 'prompts/ejecutados_exactos.json', prompts)
    dump(dest / 'registros/drive_verificado.json', readback)
    dump(dest / 'registros/estado_799.json', dict(collections.Counter(x['estado'] for x in sources)))
    artifacts = []
    sections = [('aprobada', 'approved', production / 'aprobadas/JPG'), ('en_revision', 'review', production / 'lote_04_diversas'), ('en_revision', 'review05', production / 'lote_05_cabello_negro')]
    sections.extend(('en_revision', key, production / directory) for key, directory in readback.get('extra_review_sources', {}).items())
    for state, section, directory in sections:
        for item in readback.get(section, {}).get('results', []):
            source_name = item['title'].split('_')[0] + '.JPG'
            if known.get(source_name, {}).get('estado') != state:
                continue
            current_version = known.get(source_name, {}).get('version_actual')
            if current_version in ('v03','v04') and ('_'+current_version+'.') not in item['title']:
                continue
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
    counts = collections.Counter(x['estado'] for x in sources)
    summary = ('## Estado comprobado\n\n'
        f'- {len(sources)} fuentes JPG inventariadas con ID y enlace de Drive.\n'
        f'- {sum(x["estado"] == "aprobada" for x in artifacts)} JPG aprobados y verificados en Drive.\n'
        f'- {sum(x["estado"] == "en_revision" for x in artifacts)} JPG nuevos o anteriores en revisión; no aprobados automáticamente.\n'
        f'- {len(prompts)} prompts exactos recuperados; incluyen intentos bloqueados sin imagen cuando están identificados así.\n'
        f'- {len(hashes)} originales inspeccionados con SHA-256; no afirmar que los 799 tengan hash comprobado.\n'
        f'- {counts.get("bloqueada_herramienta", 0)} fuentes bloqueadas por herramienta; no cuentan como producción.\n'
        '- Lote01 de veinte: rechazado por cabello y contornos. No reutilizar sus máscaras.\n'
        '- Ver `operacion_nocturna/PLAN_NOCTURNO.json` para el contador de hasta200 nuevas, calendario y reservas activas.\n')
    readme = dest / 'README.md'
    if readme.exists():
        readme.write_text(re.sub(r'## Estado comprobado\n.*?(?=\nEl registro distingue)', summary, readme.read_text(), flags=re.S))
    (dest / 'ESTADO_ACTUAL.md').write_text(summary + '\nEsta sección se reconstruye con el expediente; revisar la fecha de commit remoto antes de usarla.\n')
    for name in ['lote_01/manifiesto.json', 'lote_03_diez/manifiesto.json', 'lote_04_diversas/seleccion.json', 'lote_04_diversas/procedencia_verificacion.json', 'lote_04_diversas/pendientes_omitidas_por_diversidad.json']:
        path = dest / 'historial' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(production / name, path)
    for name in ['seleccion.json', 'procedencia_verificacion.json']:
        src = production / 'lote_05_cabello_negro' / name
        if src.exists():
            path = dest / 'historial/lote_05_cabello_negro' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, path)
    night = production / 'noche_2026-11-04'
    if night.exists():
        target = dest / 'operacion_nocturna'
        target.mkdir(exist_ok=True)
        for src in night.iterdir():
            if src.is_file() and src.suffix in {'.json', '.md'}:
                shutil.copy2(src, target / src.name)
    for directory in readback.get('extra_review_sources', {}).values():
        folder = production / directory
        for src in folder.glob('*.json'):
            target = dest / 'historial' / directory / src.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
    for name in ['FARMASI_799_REQUISITOS.md', 'PLAN_FARMASI_799.md']:
        shutil.copy2(source.parents[1] / name, dest / name)
    scripts = dest / 'scripts'
    scripts.mkdir(exist_ok=True)
    shutil.copy2(Path(__file__), scripts / 'preparar_respaldo.py')
    for name in ['guardar_resultado_nativo.py', 'registrar_lote_nocturno.py', 'restaurar_originales_v03.py', 'transferir_etiqueta_original.py', 'analizar_restauracion_local.py', 'finalizar_correcciones_marcadas.py', 'detectar_textos_originales.swift']:
        helper = source / name
        if helper.exists():
            shutil.copy2(helper, scripts / name)
    print(json.dumps({'sources': len(sources), 'exact_prompts': len(prompts), 'approved_artifacts': sum(x['estado'] == 'aprobada' for x in artifacts), 'review_artifacts': sum(x['estado'] == 'en_revision' for x in artifacts), 'original_hashes': len(hashes)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
