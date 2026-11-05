from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import numpy as np,cv2,json,hashlib
P=Path(__file__).resolve().parents[1];O=Path(__file__).resolve().parent;stem='DSC07738';baseline=P/'correccion_v03/PNG'/(stem+'_lila_v03.png');source=P/'originales'/(stem+'.JPG');b=Image.open(baseline).convert('RGB');w,h=b.size;src=np.array(b);original=ImageOps.exif_transpose(Image.open(source)).convert('RGB').transpose(Image.Transpose.ROTATE_90);small=np.array(original.resize((600,900),Image.Resampling.LANCZOS)).astype('float32');lum=small@np.array([.2126,.7152,.0722],dtype='float32');workw,workh=1200,1800

def real_relief(crop,sigma):
 a=cv2.GaussianBlur(crop,(0,0),sigma);yy,xx=np.indices(a.shape,dtype='float32');X=np.column_stack([np.ones(a.size),xx.ravel()/a.shape[1],yy.ravel()/a.shape[0]]);coef=np.linalg.lstsq(X,a.ravel(),rcond=None)[0];res=(a-(X@coef).reshape(a.shape)).astype('float32');std=max(.4,float(res.std()));res=np.clip(res/std,-2,2);return cv2.resize(res,(workw,workh),interpolation=cv2.INTER_CUBIC),std
# Only empty real paper: no people, products, home-room edges, cloning or invented typography.
fine,fs=real_relief(lum[12:232,47:505],2.2);broad,bs=real_relief(lum[35:530,47:115],5.0);broad=cv2.GaussianBlur(broad,(0,0),18)
mask=np.array(Image.open(P/'correccion_v03'/(stem+'_mascara_preservacion.png')).resize((workw,workh),Image.Resampling.LANCZOS),dtype='float32')/255;yy,xx=np.indices((workh,workw),dtype='float32');yn=yy/workh;wall=1-np.clip((yn-400/900)/(100/900),0,1);wall=wall*wall*(3-2*wall);weight=(1-mask)**3*wall
variants=[('A','Textura tenue',3.1,1.6,(0,0,0)),('B','Sombras de fondo suaves',3.2,3.8,(0,0,0)),('C','Relieve calido discreto',2.5,2.7,(1.1,.45,-.45))];records=[]
for code,label,famp,bamp,warm in variants:
 field=np.clip(fine*famp+broad*bamp,-12,12);delta=(field[:,:,None]+np.array(warm,dtype='float32'))*weight[:,:,None];delta=cv2.resize(delta,(w,h),interpolation=cv2.INTER_CUBIC)
 # Hard safety boundary below the wall: exact original rug, products, hands and lower shadows.
 floor_y=round(h*500/900);delta[floor_y:]=0
 out=np.clip(np.rint(src.astype('float32')+delta),0,255).astype('uint8');keep=np.array(Image.open(P/'correccion_v03'/(stem+'_mascara_preservacion.png')))>230;out[keep]=src[keep];assert np.array_equal(out[keep],src[keep]);assert np.array_equal(out[floor_y:],src[floor_y:]);im=Image.fromarray(out);name=f'{stem}_pared_{code}_v04';pp=O/(name+'.png');jp=O/(name+'.jpg');im.save(pp);im.save(jp,quality=98,subsampling=0);preview=im.copy();preview.thumbnail((900,1350));preview.save(O/(name+'_VISTA.jpg'),quality=97)
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();records.append({'source_name':stem+'.JPG','variant':code,'label':label,'status':'en_revision_no_aprobada','baseline_sha256':sha(baseline),'original_sha256':sha(source),'method':'Relieve luminico de zonas vacias del fondo ORIGINAL, eliminacion de plano de exposicion, suavizado y restitucion solo en pared; sin generacion. No recorta ni regenera modelo ni texto.','paper_regions_600x900':[[47,12,505,232],[47,35,115,530]],'texture_standard_deviations':[fs,bs],'amplitudes':[famp,bamp],'warm_offset_rgb':warm,'max_texture_change':12,'wall_fade_600x900':[400,500],'protected_subject_pixels_changed':0,'floor_and_all_pixels_below_500_changed':0,'png_sha256':sha(pp),'jpg_sha256':sha(jp),'png_bytes':pp.stat().st_size,'jpg_bytes':jp.stat().st_size,'size':[w,h],'files':{'png':str(pp.resolve()),'jpg':str(jp.resolve())}});print(code,flush=True)
(O/'MANIFIESTO_TRES_VERSIONES.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
contact=Image.new('RGB',(1800,960),'#eee');d=ImageDraw.Draw(contact)
for i,(code,label,*_) in enumerate(variants):
 im=Image.open(O/f'{stem}_pared_{code}_v04_VISTA.jpg');im.thumbnail((590,890));contact.paste(im,(i*600,45));d.text((i*600+15,15),code+' - '+label,fill='black')
contact.save(O/'TRES_VERSIONES_PARED.jpg',quality=97)
# Detail of upper wall including upper arm for scale, not a separate requested variant.
detail=Image.new('RGB',(1800,500),'#eee');d=ImageDraw.Draw(detail)
for i,(code,label,*_) in enumerate(variants):
 im=Image.open(O/f'{stem}_pared_{code}_v04.jpg');im=im.crop((0,0,w,round(h*.32)));im.thumbnail((590,440));detail.paste(im,(i*600,40));d.text((i*600+15,10),code+' - '+label,fill='black')
detail.save(O/'DETALLE_PARED_TRES.jpg',quality=97)
