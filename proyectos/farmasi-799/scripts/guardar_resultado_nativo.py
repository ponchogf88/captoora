"""Persist exact execution metadata and convert output for review; no generation."""
from pathlib import Path
import argparse, json, shutil
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('record_json')
parser.add_argument('--production', type=Path, default=Path(__file__).resolve().parent / 'produccion')
args = parser.parse_args()
record = json.loads(args.record_json)
root = args.production.resolve()
folder = root / record['folder']
folder.mkdir(exist_ok=True)
name = record['source_name'].removesuffix('.JPG')
target = folder / (name + '_ejecucion.json')
target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
if record.get('generated_path'):
    src = Path(record['generated_path'])
    dst = folder / (name + '_v02.png')
    if not dst.exists():
        shutil.copy2(src, dst)
    im = Image.open(dst).convert('RGB')
    im.save(folder / (name + '_v02.jpg'), quality=97, subsampling=0)
    im.thumbnail((600, 900))
    im.save(folder / (name + '_revision.jpg'), quality=94)
print(json.dumps({'source': record['source_name'], 'saved': True, 'estado': record['estado']}))
