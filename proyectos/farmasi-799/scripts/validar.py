"""Audit handoff integrity, without network, generation or image mutations."""
from pathlib import Path
import collections, json

p = Path(__file__).resolve().parents[1]
sources = json.loads((p / 'registros/fuentes_799.json').read_text())
artifacts = json.loads((p / 'registros/artefactos.json').read_text())
prompts = json.loads((p / 'prompts/ejecutados_exactos.json').read_text())
assert len(sources) == 799
assert len({x['source_id'] for x in sources}) == 799
assert len({x['source_name'] for x in sources}) == 799
assert len({x['id'] for x in prompts}) == len(prompts)
assert all(x['prompt'] and x['provenance'] == 'exact_execution_store' for x in prompts)
assert len({x['drive_id'] for x in artifacts}) == len(artifacts)
assert all(x['bytes'] == x['cloud_bytes'] and len(x['sha256']) == 64 for x in artifacts)
assert all(x['drive_url'].startswith('https://drive.google.com/') for x in artifacts)
assert all(x.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.nef', '.zip'} for x in p.rglob('*') if x.is_file())
for x in artifacts:
    source = next(s for s in sources if s['source_name'] == x['source_name'])
    assert source['estado'] == x['estado'], (x['file_name'], source['estado'])
print(json.dumps({'valid': True, 'sources': len(sources), 'exact_prompts': len(prompts), 'artifacts': dict(collections.Counter(x['estado'] for x in artifacts))}, ensure_ascii=False))
