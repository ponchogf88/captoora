"""Transfer an actual photographed label from the sharper same-container frame."""
from pathlib import Path
from PIL import Image,ImageFilter
import cv2,numpy as np,json,hashlib
p=Path(__file__).resolve().parent/'produccion';d=p/'correcciones_rostros_textos_v03';donor=np.asarray(Image.open(d/'DSC07722_v03.png').convert('RGB'));k=donor.shape[1]/1024
srcbox=np.array([[298,440],[355,440],[355,499],[298,499]],np.float32)*k
crop=donor[int(srcbox[0,1]):int(srcbox[2,1])+1,int(srcbox[0,0]):int(srcbox[2,0])+1].copy()
for name,box in {'DSC07720':[317,534,367,581],'DSC07721':[182,311,243,384],'DSC07724':[356,592,394,625],'DSC07726':[214,545,271,609]}.items():
 im=np.asarray(Image.open(d/(name+'_v03.png')).convert('RGB')).copy();mask=np.asarray(Image.open(d/(name+'_zonas.png'))).copy();scale=im.shape[1]/1024;x,y,r,b=[int(v*scale) for v in box];cw,ch=r-x,b-y
 a=cv2.resize(crop,(cw,ch),interpolation=cv2.INTER_CUBIC).astype(np.float32);target=im[y:b,x:r].astype(np.float32);offset=np.clip(np.median(target.reshape(-1,3)-a.reshape(-1,3),axis=0),-22,22);a=np.clip(a+offset,0,255)
 m=Image.new('L',(cw,ch),255);# inner crop avoids reintroducing label/container edges
 ar=np.asarray(m).copy();ar[:4]=0;ar[-4:]=0;ar[:,:4]=0;ar[:,-4:]=0;ar=np.asarray(Image.fromarray(ar).filter(ImageFilter.GaussianBlur(3)));alpha=ar[:,:,None]/255
 im[y:b,x:r]=np.rint(target*(1-alpha)+a*alpha).astype(np.uint8);mask[y:b,x:r]=np.maximum(mask[y:b,x:r],ar)
 Image.fromarray(im).save(d/(name+'_v03.png'),compress_level=1);Image.fromarray(im).save(d/(name+'_v03.jpg'),quality=98,subsampling=0);Image.fromarray(mask).save(d/(name+'_zonas.png'),compress_level=1);pr=Image.fromarray(im);pr.thumbnail((900,1200));pr.save(d/(name+'_revision.jpg'),quality=96)
 j=json.load(open(d/(name+'_restauracion.json')));j['regions'].append({'role':'etiqueta_donante_original_mismo_envase','donor':'DSC07722.JPG','donor_source_url':'https://drive.google.com/file/d/1IJYYz51EGYI39ADAUpnJdOTLq1TBpWmc/view','donor_output_box':[298,440,355,499],'target_output_box':box,'light_offset_rgb':offset.tolist(),'text_generation':False,'nota':'Detalle fotografico de la misma impresion/envase en secuencia; no transcripcion ni caracteres inventados.'});(d/(name+'_restauracion.json')).write_text(json.dumps(j,ensure_ascii=False,indent=2))
print('four real-label transfers; no generated characters')
