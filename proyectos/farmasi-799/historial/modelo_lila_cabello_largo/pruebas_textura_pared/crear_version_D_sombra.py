from pathlib import Path
from PIL import Image,ImageDraw
import cv2,numpy as np,json,hashlib
O=Path(__file__).resolve().parent;P=O.parent;baseline=O/'DSC07738_pared_B_v04.png';maskfile=P/'correccion_v03/DSC07738_mascara_preservacion.png';b=Image.open(baseline).convert('RGB');w,h=b.size;src=np.array(b);ww,hh=1200,1800;m=np.array(Image.open(maskfile).resize((ww,hh),Image.Resampling.LANCZOS),dtype='float32')/255
# Use the actual protected silhouette, only above the real rug/product display.
y,x=np.indices((hh,ww),dtype='float32');yn=y/hh;roi=(x>=108*2)&(x<460*2)&(y>=230*2)&(y<510*2);body=((m>.985)&roi).astype('float32')
def projected(dx,dy,sigma,opacity):
 a=cv2.warpAffine(body,np.array([[1,0,dx*2],[0,1,dy*2]],dtype='float32'),(ww,hh),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT);a=cv2.GaussianBlur(a,(0,0),sigma*2);return a*opacity
shadow=projected(58,8,11,.075)+projected(-28,10,19,.022)
# Shadow belongs to backdrop, not to the person. Entire lower zone remains exactly as before.
wall=1-np.clip((yn-435/900)/(65/900),0,1);wall=wall*wall*(3-2*wall);shadow*=((1-m)**2)*wall;shadow=cv2.resize(shadow,(w,h),interpolation=cv2.INTER_CUBIC);shadow[round(h*500/900):]=0;keep=np.array(Image.open(maskfile))>230;shadow[keep]=0
out=np.clip(np.rint(src.astype('float32')*(1-shadow[:,:,None])),0,255).astype('uint8');out[keep]=src[keep];cut=round(h*500/900);assert np.array_equal(out[keep],src[keep]);assert np.array_equal(out[cut:],src[cut:]);im=Image.fromarray(out);name='DSC07738_pared_D_sombra_v05';pp=O/(name+'.png');jp=O/(name+'.jpg');im.save(pp);im.save(jp,quality=98,subsampling=0);v=im.copy();v.thumbnail((1000,1500));v.save(O/(name+'_VISTA.jpg'),quality=97)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();rec={'source_name':'DSC07738.JPG','variant':'D','label':'Textura y sombra suave de la modelo','baseline':'DSC07738_pared_B_v04.png','baseline_sha256':sha(baseline),'silhouette_mask_sha256':sha(maskfile),'method':'Sombra fotografica local a partir de silueta real protegida, dos proyecciones muy suaves sobre pared. Sin generacion de modelo, rostros, letras ni objetos.','primary_shadow_600x900':{'shift':[58,8],'sigma':11,'opacity':.075},'secondary_shadow_600x900':{'shift':[-28,10],'sigma':19,'opacity':.022},'wall_fade_600x900':[435,500],'max_actual_shadow_opacity':float(shadow.max()),'protected_subject_pixels_changed':0,'floor_and_all_pixels_below_500_changed':0,'new_generations':0,'status':'en_revision_no_aprobada','size':[w,h],'png_sha256':sha(pp),'jpg_sha256':sha(jp),'png_bytes':pp.stat().st_size,'jpg_bytes':jp.stat().st_size,'files':{'png':str(pp.resolve()),'jpg':str(jp.resolve())}}
(O/'MANIFIESTO_VERSION_D.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
c=Image.new('RGB',(1400,1080),'#eee');d=ImageDraw.Draw(c)
for i,(label,f)in enumerate([('B - textura y sombras del fondo',baseline),('D - sombra adicional de ella',pp)]):
 a=Image.open(f);a.thumbnail((690,1035));c.paste(a,(i*700,40));d.text((i*700+15,12),label,fill='black')
c.save(O/'COMPARACION_B_D.jpg',quality=97);print(json.dumps(rec,ensure_ascii=False))
