from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFilter
import numpy as np, cv2,json,hashlib
P=Path(__file__).resolve().parent; O=P/'correccion_cabello_DSC07706_v04'; O.mkdir(exist_ok=True)
bp=P/'correcciones_rostros_textos_v03/entrega_final/DSC07706_v03.png'; sp=P.parent/'piloto/originales/DSC07706.JPG'
b=Image.open(bp).convert('RGB'); s=ImageOps.exif_transpose(Image.open(sp)).convert('RGB'); w,h=b.size;k=w/1536
meta=json.loads((bp.parent/'DSC07706_restauracion.json').read_text()); mat=np.array(meta['regions'][0]['similarity']);mat[:,2]*=k
# Local, hand-traced interior regions; never change the approved face or skin.
polys=[[(697,269),(712,242),(740,218),(764,215),(784,225),(790,242),(769,238),(747,238),(721,251)],[(696,274),(680,299),(649,328),(631,352),(612,380),(598,394),(614,355),(643,320),(675,285)],[(787,280),(794,296),(793,350),(788,404),(786,459),(776,465),(746,457),(728,449),(720,417),(715,380),(709,351),(710,337),(725,337),(743,328),(766,309),(781,289)]]
m=Image.new('L',(w,h));d=ImageDraw.Draw(m)
for p in polys[1:]:d.polygon([(int(x*k),int(y*k)) for x,y in p],fill=255)
m=m.filter(ImageFilter.GaussianBlur(3*k));protect=Image.new('L',(w,h));ImageDraw.Draw(protect).polygon([(int(x*k),int(y*k)) for x,y in meta['regions'][0]['polygon_output_v02']],fill=255);protect=Image.fromarray(cv2.dilate(np.array(protect),np.ones((41,41),np.uint8))); ma=np.array(m);ma[np.array(protect)>0]=0
# Source detail only, with a bounded tonal match to the accepted dark hair.
a=np.array(b); src=cv2.warpAffine(np.array(s),mat,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
valid=(ma>240)&(src.mean(2)<160)&(a.mean(2)<160)
shift=np.median(a[valid].astype(float)-src[valid],axis=0); shift=np.clip(shift,-35,35)
alpha=ma.astype(np.float32)/255; result=a.copy(); sel=ma>0
result[sel]=np.rint(a[sel]*(1-alpha[sel,None])+np.clip(src[sel].astype(float)+shift,0,255)*alpha[sel,None]).astype('uint8')
assert np.count_nonzero(np.any(result[~sel]!=a[~sel],axis=1))==0
assert np.array_equal(result[np.array(protect)>0],a[np.array(protect)>0])
im=Image.fromarray(result);im.save(O/'DSC07706_v04.png');im.save(O/'DSC07706_v04.jpg',quality=97,subsampling=0);Image.fromarray(ma).save(O/'mascara_cabello.png')
preview=Image.new('RGB',(1200,620),'white');draw=ImageDraw.Draw(preview)
for i,x in enumerate([b,im]):
 c=x.crop(tuple(int(v*k) for v in (545,205,810,480)));c.thumbnail((590,580));preview.paste(c,(i*600,35));draw.text((i*600+20,10),['ANTES - v03 aprobada','DESPUES - v04 cabello original'][i],fill='black')
preview.save(O/'ANTES_DESPUES_CABELLO.png');im.thumbnail((1600,1200));im.save(O/'VISTA_COMPLETA.jpg',quality=94)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit={'source':'DSC07706.JPG','version':'v04','estado':'en_revision','method':'Restauracion local de textura original; sin generacion ni alisado geometrico','polygons_1536':polys,'similarity':mat.tolist(),'tonal_offset_rgb':shift.tolist(),'outside_hair_mask_changed_pixels':0,'protected_face_changed_pixels':0,'baseline_sha256':sha(bp),'original_sha256':sha(sp),'png_sha256':sha(O/'DSC07706_v04.png'),'limitacion':'Se conserva la caida real del cabello; no se inventan hebras ni se altera su forma.'}
(O/'AUDITORIA_CABELLO.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit))
