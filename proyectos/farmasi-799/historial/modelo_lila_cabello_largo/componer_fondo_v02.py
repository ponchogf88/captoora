from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFilter
import numpy as np,cv2,json,hashlib,shutil
P=Path(__file__).resolve().parent;O=P/'lote_individual_v02';(O/'PNG').mkdir(parents=True,exist_ok=True);(O/'JPG').mkdir(exist_ok=True)
plate=P/'hibrido/fondo_vacio_nativo.png'
C={'DSC07736':(.035,.81,.66,0),'DSC07738':(.09,.845,.70,0),'DSC07739':(.075,.81,.70,0),'DSC07743':(.205,.88,.84,.22),'DSC07747':(.30,.96,.86,.23),'DSC07762':(.215,.84,.90,.13),'DSC07767':(.05,1,.8,0),'DSC07768':(.05,1,.8,0),'DSC07772':(.14,.90,.89,.07),'DSC07774':(.185,.87,.89,.15)}
records=[]
for stem,(left,right,endy,top) in C.items():
 f=P/'originales'/(stem+'.JPG');im=ImageOps.exif_transpose(Image.open(f)).convert('RGB').transpose(Image.Transpose.ROTATE_90);w,h=im.size;src=np.array(im)
 lut=np.rint(np.interp(np.arange(256),[0,32,64,128,160,192,216,232,248,255],[0,27,55,105,136,169,197,218,240,248])).astype('uint8');base=lut[src];bg=np.array(Image.open(plate).convert('RGB').resize((w,h),Image.Resampling.LANCZOS))
 m=Image.new('L',(w,h));d=ImageDraw.Draw(m)
 if left:d.polygon([(0,0),(int(left*w),0),(int(left*w),int(endy*h)),(0,int((endy+.04)*h))],fill=255)
 if right<1:d.polygon([(int(right*w),0),(w,0),(w,int((endy+.04)*h)),(int(right*w),int(endy*h))],fill=255)
 if top:d.rectangle((0,0,w,int(top*h)),fill=255)
 # Soft extension exclusively across empty original paper. Native plate has no people/products.
 raw=np.array(m);dist=cv2.distanceTransform(255-raw,cv2.DIST_L2,5);ma=np.maximum(0,1-dist/(w*.04));ma[raw>0]=1
 if stem in ['DSC07743','DSC07747']:
  # Original elbow touches room foam: keep the genuine skin pixels, never synthesize anatomy.
  region=np.zeros((h,w),bool);region[int(.35*h):int(.67*h),int(.08*w):int(.35*w)]=True
  skin=region&(src[:,:,0]>src[:,:,2]*1.04)&(src[:,:,0]>src[:,:,1]*1.015)&(src.mean(2)>120)
  guard=skin;ma[guard]=0
 out=base.copy();sel=ma>0;out[sel]=np.rint(base[sel]*(1-ma[sel,None])+bg[sel]*ma[sel,None]).astype('uint8')
 pp=O/'PNG'/(stem+'_lila_v02.png');jp=O/'JPG'/(stem+'_lila_v02.jpg');res=Image.fromarray(out);res.save(pp);res.save(jp,quality=97,subsampling=0);Image.fromarray((ma*255).astype('uint8')).save(O/(stem+'_mascara_fondo.png'));res.thumbnail((800,1200));res.save(O/(stem+'_VISTA.jpg'),quality=95)
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();records.append({'source_name':stem+'.JPG','estado':'revision_tecnica_interna','method':'Fondo vacio nativo compuesto solo sobre cuarto; persona,productos y alfombra originales con curva tonal monotona. Sin generacion de sujetos.','source_sha256':sha(f),'png_sha256':sha(pp),'jpg_sha256':sha(jp),'outside_background_mask_changed_pixels':int(np.count_nonzero(np.any(out[~sel]!=base[~sel],axis=1))),'rotation_ccw':90,'size':[w,h],'background_parameters':C[stem]});print(stem,flush=True)
(O/'AUDITORIA.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
contact=Image.new('RGB',(1500,1000),'#ddd');d=ImageDraw.Draw(contact)
for i,stem in enumerate(C):
 im=Image.open(O/(stem+'_VISTA.jpg'));im.thumbnail((290,465));x=i%5*300;y=i//5*500;contact.paste(im,(x,y+25));d.text((x+5,y+5),stem,fill='black')
contact.save(O/'CONTACTO.jpg',quality=95)
