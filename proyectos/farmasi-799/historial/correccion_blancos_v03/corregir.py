from pathlib import Path
import json,cv2,numpy as np,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;E=P.parent/'ENTREGA';M=json.load(open(E/'MANIFIESTO.json'));G=json.load(open(P.parent/'GENERACIONES.json'));records=[]
for n in ['DSC08500','DSC08504','DSC08536','DSC08554']:
 rec=next(r for r in M if r['source_name']==n+'.JPG');f=E/rec['png'];im=Image.open(f).convert('RGB');w,h=im.size;hh=1500;ww=round(w*hh/h);a=np.array(im.resize((ww,hh))).astype('float32');gen=np.array(Image.open(G[n]).convert('RGB').resize((ww,hh)));H=np.array(rec['background_alignment']);bg=cv2.warpAffine(gen,H,(ww,hh),borderMode=cv2.BORDER_REFLECT).astype('float32')
 # Neutral backdrop only; copper skin/hair are excluded and expanded as a safety margin.
 warm=((a[:,:,0]-a[:,:,1]>7)&(a[:,:,0]-a[:,:,2]>12));dark=a.min(2)<125;subject=(warm|dark).astype('uint8');valid=(subject==0)&(a.min(2)>125)&(a.max(2)-a.min(2)<45)&(bg.min(2)>150)&(bg.max(2)-bg.min(2)<45)
 weight=valid.astype('float32');sigma=32;den=cv2.GaussianBlur(weight,(0,0),sigma);delta=np.zeros_like(a)
 for c in range(3):delta[:,:,c]=cv2.GaussianBlur((bg[:,:,c]-a[:,:,c])*weight,(0,0),sigma)/np.maximum(den,.001)
 # Correct broad mismatch only: retain high-frequency backdrop/plush texture and actual shadow edges.
 correction=np.clip(delta,-28,28);apply=(subject==0).astype('float32');apply=cv2.GaussianBlur(apply,(0,0),1);apply[subject>0]=0
 raw=np.array(im);full=cv2.resize(correction,(w,h));mask=cv2.resize(apply,(w,h));protect=cv2.resize(subject,(w,h),interpolation=cv2.INTER_NEAREST)>0;out=np.clip(np.rint(raw.astype('float32')+full*mask[:,:,None]),0,255).astype('uint8');out[protect]=raw[protect];assert np.array_equal(out[protect],raw[protect]);png=P/(n+'_blancos_v03.png');Image.fromarray(out).save(png);jpg=png.with_suffix('.jpg');Image.fromarray(out).save(jpg,quality=97,subsampling=0);v=Image.fromarray(out);v.thumbnail((700,1050));v.save(P/(n+'_VISTA.jpg'),quality=95);records.append({'source_name':n+'.JPG','file':jpg.name,'png':png.name,'bytes':jpg.stat().st_size,'sha256':hashlib.sha256(jpg.read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'protected_subject_pixels_changed':0,'method':'Correccion cromatica y luminancia de baja frecuencia solo fondo neutro; conserva detalle fino y bordes de sombras. Piel/cobre/cabello excluidos y resguardados. Sin nueva generacion.','status':'en_revision'});print(n,flush=True)
(P/'MANIFIESTO.json').write_text(json.dumps(records,indent=2));s=Image.new('RGB',(1600,640),'#eee');d=ImageDraw.Draw(s)
for i,r in enumerate(records):
 im=Image.open(P/(r['source_name'][:-4]+'_VISTA.jpg'));im.thumbnail((390,1170));s.paste(im,(i*400,35));d.text((i*400+10,10),r['source_name'][:-4],fill='black')
s.save(P/'CONTACTO.jpg',quality=95)
