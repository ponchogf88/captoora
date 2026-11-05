from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent/'produccion';D=P/'correcciones_rostros_textos_v03';E=D/'entrega_final';E.mkdir(exist_ok=True);records=[]
for name in ['DSC07706','DSC07724','DSC07731','DSC07732','DSC08471','DSC08479','DSC08484','DSC07726']:
 j=json.load(open(D/(name+'_restauracion.json')));current=np.asarray(Image.open(D/(name+'_v03.png')).convert('RGB'));base=np.asarray(Image.open(P/j['folder_anterior']/(name+'_v02.png')).convert('RGB').resize((current.shape[1],current.shape[0]),Image.Resampling.LANCZOS));out=base.copy();mask=np.zeros(current.shape[:2],np.uint8);k=current.shape[1]/(1536 if name=='DSC07706' else 1024);roles=['etiqueta_en_mano'] if name=='DSC07726' else ['rostro'];kept=[]
 for r in j['regions']:
  if r['role'] not in roles:continue
  a=Image.new('L',(current.shape[1],current.shape[0]));poly=[tuple(np.array(z)*k) for z in r['polygon_output_v02']];ImageDraw.Draw(a).polygon(poly,fill=255);a=a.filter(ImageFilter.GaussianBlur((1.8 if r['role']=='rostro' else 1)*k));m=np.asarray(a);mask=np.maximum(mask,m);kept.append(r)
 out[mask>0]=current[mask>0];assert np.array_equal(out[mask==0],base[mask==0]);Image.fromarray(out).save(E/(name+'_v03.png'),compress_level=1);Image.fromarray(out).save(E/(name+'_v03.jpg'),quality=98,subsampling=0);Image.fromarray(mask).save(E/(name+'_zonas.png'),compress_level=1);pr=Image.fromarray(out);pr.thumbnail((900,1200));pr.save(E/(name+'_revision.jpg'),quality=96)
 if name=='DSC07726':kept.extend(r for r in j['regions'] if r['role']=='etiqueta_donante_original_mismo_envase')
 rec={**j,'regions':kept,'estado':'correccion_marcada_en_revision','outside_mask_changed_pixels':0,'scope':'Solo zonas de captura usuario; no restauracion general de envases no marcados','limitacion':('Desenfoque presente en original; no se invento cara nitida.' if name=='DSC08479' else 'Reflejo/sobreexposicion impide lectura completa de letra fina; fuente alternativaDSC07722 misma impresion.' if name=='DSC07726' else None),'png_sha256':hashlib.sha256((E/(name+'_v03.png')).read_bytes()).hexdigest()};records.append(rec);(E/(name+'_restauracion.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2))
 r=kept[0];pts=np.array(r['polygon_output_v02']);lo=pts.min(0)-[14,14];hi=pts.max(0)+[14,14];box=tuple(int(v*k) for v in [*lo,*hi]);c=Image.new('RGB',(1000,620),'#eee');dr=ImageDraw.Draw(c)
 for i,(arr,label) in enumerate([(base,'ANTES v02'),(out,'RESTAURADO del original')]):
  a=Image.fromarray(arr).crop(box);a.thumbnail((485,575));c.paste(a,(i*500,35));dr.text((i*500+8,8),name+' '+label,fill='black')
 c.save(E/(name+'_ANTES_DESPUES.png'));print(name,'final',flush=True)
(E/'AUDITORIA_FINAL.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
for start in [0,4]:
 c=Image.new('RGB',(2000,1240),'#eee')
 for i,r in enumerate(records[start:start+4]):c.paste(Image.open(E/(r['source_name'][:-4]+'_ANTES_DESPUES.png')),(i%2*1000,i//2*620))
 c.save(E/('COMPARATIVA_'+('A' if start==0 else 'B')+'.png'))
