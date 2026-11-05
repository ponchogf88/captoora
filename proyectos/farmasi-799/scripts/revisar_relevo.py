"""Read-only handoff audit. No network, generation, editing or charges."""
from pathlib import Path
import collections,json,argparse
p=Path(__file__).resolve().parents[1]
q=argparse.ArgumentParser();q.add_argument('--source');a=q.parse_args()
s=json.loads((p/'registros/fuentes_799.json').read_text());v=json.loads((p/'prompts/ejecutados_exactos.json').read_text())
assert len(s)==799 and len({x['source_name'] for x in s})==799
for n in ['CONTINUAR.md','BITACORA_FARMASI_799.md','prompts/RECETAS_VIGENTES.md','prompts/EJECUTADOS_EXACTOS.md','scripts/editar_pruebas_bebe.py']:
 assert (p/n).is_file(),n
md=(p/'prompts/EJECUTADOS_EXACTOS.md').read_text()
for x in v:assert x['prompt'] in md,x['id']
if a.source:
 rows=[x for x in s if x['source_name']==a.source];assert len(rows)==1,'Unknown source';print(json.dumps(rows[0],ensure_ascii=False,indent=2));print(json.dumps([x for x in v if x.get('source')==a.source],ensure_ascii=False,indent=2))
else:print(json.dumps({'sources':len(s),'prompts_exact':len(v),'state':dict(collections.Counter(x['estado']for x in s)),'current_guide':'CONTINUAR.md','recipes':'prompts/RECETAS_VIGENTES.md','generates_images':False},ensure_ascii=False))
