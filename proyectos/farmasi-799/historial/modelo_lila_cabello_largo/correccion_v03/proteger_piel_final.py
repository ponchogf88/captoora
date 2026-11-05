from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parents[1];O=Path(__file__).resolve().parent;rows=[]
for f in sorted((O/'PNG').glob('*_lila_v03.png')):
 stem=f.stem.split('_')[0];b=np.array(Image.open(P/'lote_individual_v02/PNG'/(stem+'_lila_v02.png'))).astype('int16');out=np.array(Image.open(f));ma=np.array(Image.open(O/(stem+'_mascara_preservacion.png')));warm=(b[:,:,0]>b[:,:,1]+8)&(b[:,:,0]>b[:,:,2]+8)&(b.mean(2)>100)&(ma==255);n=int(np.count_nonzero(np.any(out[warm]!=b[warm],axis=1)));out[warm]=b[warm].astype('uint8');assert np.array_equal(out[warm],b[warm]);im=Image.fromarray(out);im.save(f);jp=O/'JPG'/(stem+'_lila_v03.jpg');im.save(jp,quality=98,subsampling=0);im.thumbnail((900,1350));im.save(O/(stem+'_VISTA.jpg'),quality=96)
 rec=json.load(open(O/(stem+'_auditoria.json')));rec.update(protected_warm_pixels_changed=0,warm_pixel_protection_count=int(warm.sum()),warm_pixels_restored_after_label_adjustment=n,status='lista_para_revision_usuario_no_aprobada')
 for fmt in ['PNG','JPG']:
  ff=O/fmt/(stem+'_lila_v03.'+fmt.lower());rec[fmt.lower()+'_bytes']=ff.stat().st_size;rec[fmt.lower()+'_sha256']=hashlib.sha256(ff.read_bytes()).hexdigest()
 (O/(stem+'_auditoria.json')).write_text(json.dumps(rec,indent=2)+'\n');rows.append(rec);print(stem,n,flush=True)
(O/'AUDITORIA_LOTE.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
contact=Image.new('RGB',(1800,1140),'#efefef');d=ImageDraw.Draw(contact)
for i,r in enumerate(rows):
 stem=r['source_name'][:-4];im=Image.open(O/(stem+'_VISTA.jpg'));im.thumbnail((350,525));x=i%5*360;y=i//5*570;contact.paste(im,(x,y+30));d.text((x+8,y+8),stem+' - v03',fill='black')
contact.save(O/'CONTACTO_V03.jpg',quality=97)
