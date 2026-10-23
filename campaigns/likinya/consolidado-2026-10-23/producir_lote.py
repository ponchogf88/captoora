"""Prepara clips propios de apoyo; no genera avatar ni consume cuotas de IA."""
import base64
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/Users/user/captoora/assets/media/studio-vertical.mp4.b64')

def main():
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        raise SystemExit('Falta ffmpeg; no se instala automáticamente.')
    if shutil.disk_usage(ROOT).free < 8 * 1024**3:
        raise SystemExit('Lote detenido: menos de 8 GiB libres.')
    output = ROOT / 'clips'
    output.mkdir(exist_ok=True)
    manifest_path = ROOT / 'manifest.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {'clips': []}
    raw = base64.b64decode(SOURCE.read_bytes())
    fingerprint = hashlib.sha256(raw).hexdigest()
    source = output / 'fuente-estudio.mp4'
    if not source.exists() or hashlib.sha256(source.read_bytes()).hexdigest() != fingerprint:
        source.write_bytes(raw)
    info = subprocess.run([ffmpeg, '-hide_banner', '-i', str(source)], capture_output=True, text=True)
    match = re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)', info.stderr)
    if not match:
        raise SystemExit('No se pudo medir la duración del archivo fuente.')
    hours, minutes, seconds = map(float, match.groups())
    total = hours * 3600 + minutes * 60 + seconds
    span = min(4.0, total / 3)
    if span < 1:
        raise SystemExit('Fuente demasiado corta para tres clips distintos.')
    created = []
    for index in range(3):
        start = index * total / 3
        path = output / f'estudio-apoyo-{index+1:02}.mp4'
        key = f'{fingerprint}:{start:.3f}:{span:.3f}:fit1080-v1'
        old = next((x for x in manifest['clips'] if x['key'] == key), None)
        if old and path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == old['sha256']:
            continue
        temp = path.with_suffix('.partial.mp4')
        subprocess.run([ffmpeg, '-v', 'error', '-nostdin', '-y', '-ss', str(start), '-i', str(source),
                        '-t', str(span), '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1',
                        '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(temp)], check=True)
        subprocess.run([ffmpeg, '-v', 'error', '-nostdin', '-i', str(temp), '-f', 'null', '-'], check=True)
        temp.replace(path)
        item = {'key': key, 'path': str(path), 'source': str(SOURCE), 'source_sha256': fingerprint,
                'start_seconds': start, 'duration_seconds_target': span, 'bytes': path.stat().st_size,
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'status': 'decoded_ok_visual_review_pending', 'kind': 'b_roll_without_voice'}
        manifest['clips'] = [x for x in manifest['clips'] if x['path'] != str(path)] + [item]
        created.append(str(path))
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    report = {'at_utc': datetime.now(timezone.utc).isoformat(), 'new_files': created,
              'verified_clip_count': len(manifest['clips']),
              'clip_bytes': sum(x['bytes'] for x in manifest['clips']),
              'ai_credits_consumed_by_local_batch': 0,
              'usable_clip_count': sum(x.get('status') == 'visual_approved' for x in manifest['clips']),
              'rejected_clip_count': sum(x.get('status') == 'rejected_for_educational_pilot' for x in manifest['clips']),
              'status': 'support_clips_only_not_final_reels',
              'pending': ['Rejected support clips must not enter educational reels; see reporte.json for provider and pilot status']}
    (ROOT / 'reporte_lote_local.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    summary_path = ROOT / 'reporte.json'
    summary = json.loads(summary_path.read_text()) if summary_path.exists() else {}
    summary['local_batch_check'] = report
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    with (ROOT / 'ejecuciones.jsonl').open('a') as history:
        history.write(json.dumps(report, ensure_ascii=False) + '\n')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()
