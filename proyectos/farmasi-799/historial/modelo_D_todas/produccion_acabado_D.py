from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import cv2,numpy as np,json,hashlib,sys
P=Path(__file__).resolve().parent;R=P.parent;O=P/'produccion_D_todas';(O/'PNG').mkdir(parents=True,exist_ok=True);(O/'JPG').mkdir(exist_ok=True)
ref=np.array(ImageOps.exif_transpose(Image.open(P/'originales/DSC07738.JPG')).convert('RGB').transpose(Image.Transpose.ROTATE_90).resize((600,900))).astype('float32');lum=ref@np.array([.2126,.7152,.0722],dtype='float32')
def relief(crop,sigma,ww,hh):
 a=cv2.GaussianBlur(crop,(0,0),sigma);yy,xx=np.indices(a.shape,dtype='float32');X=np.column_stack([np.ones(a.size),xx.ravel()/a.shape[1],yy.ravel()/a.shape[0]]);co=np.linalg.lstsq(X,a.ravel(),rcond=None)[0];res=(a-(X@co).reshape(a.shape)).astype('float32');res=np.clip(res/max(.4,float(res.std())),-2,2);return cv2.resize(res,(ww,hh),interpolation=cv2.INTER_CUBIC)
oldfloor={'DSC07706':.58,'DSC07720':.70,'DSC07721':.73,'DSC07722':.67,'DSC07724':.72,'DSC07726':.72,'DSC07731':.68,'DSC07732':.68,'DSC07733':.61,'DSC07734':.61}
newfloor={'DSC07736':580/900,'DSC07739':575/900,'DSC07743':790/900,'DSC07747':800/900,'DSC07762':730/900,'DSC07767':730/900,'DSC07768':730/900,'DSC07772':720/900,'DSC07774':700/900}
reg=json.load(open(R/'REGISTRO_EDICION.json'));records={x['source_name']:x for x in reg['files']};config=[]
for name,floor in oldfloor.items():
 files=list((R/'aprobadas').glob(name+'_*.png'));assert len(files)==1,(name,files);config.append({'source_name':name+'.JPG','base':str(files[0]),'floor':floor,'wardrobe':'lila','previous_state':'aprobada','mask':None})
for name,floor in newfloor.items():config.append({'source_name':name+'.JPG','base':str(P/'correccion_v03/PNG'/(name+'_lila_v03.png')),'floor':floor,'wardrobe':'lila','previous_state':'en_revision','mask':str(P/'correccion_v03'/(name+'_mascara_preservacion.png'))})
for name in ['DSC08454','DSC08456','DSC08457','DSC08459','DSC08466','DSC08471','DSC08477','DSC08479','DSC08481','DSC08484']:
 files=list((R/'aprobadas').glob(name+'_*.png'));assert len(files)==1;config.append({'source_name':name+'.JPG','base':str(files[0]),'floor':.78,'wardrobe':'cobrizo_grupo','previous_state':'aprobada','mask':None})
(O/'CONFIG_BASES.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
only=set(sys.argv[1:]);allrecs=[]
for item in config:
 stem=item['source_name'][:-4]
 if only and stem not in only:continue
 # Explicitly no regeneration, resizing, warping or geometric changes to people or labels.
 b=Image.open(item['base']).convert('RGB');w,h=b.size;src=np.array(b);ww=1200;hh=round(ww*h/w);small=np.array(b.resize((ww,hh)));yy,xx=np.indices((hh,ww),dtype='float32');yn=yy/hh
 if item['mask']:m=np.array(Image.open(item['mask']).resize((ww,hh),Image.Resampling.LANCZOS),dtype='float32')/255
 else:
  a=small.astype('int16');hsv=cv2.cvtColor(small,cv2.COLOR_RGB2HSV);fg=((hsv[:,:,2]<168)|((hsv[:,:,1]>18)&((a[:,:,0]-a[:,:,1]>3)|(a[:,:,2]-a[:,:,1]>4))));fg[:round(.09*hh)]=False;fg[:, :round(.07*ww)]=False;fg[:,round(.96*ww):]=False;fg[round(item['floor']*hh):]=False
  binary=fg.astype('uint8')*255;binary=cv2.morphologyEx(binary,cv2.MORPH_CLOSE,np.ones((13,13),np.uint8));flood=binary.copy();cv2.floodFill(flood,None,(0,0),255);binary=np.maximum(binary,cv2.bitwise_not(flood));binary=cv2.dilate(binary,np.ones((7,7),np.uint8));distance=cv2.distanceTransform(255-binary,cv2.DIST_L2,5);m=np.exp(-np.square(distance/(ww*.018)));m[binary>0]=1
 wallend=item['floor']-45/900;texturefade=1-np.clip((yn-(wallend-100/900))/(100/900),0,1);texturefade=texturefade*texturefade*(3-2*texturefade);fine=relief(lum[12:232,47:505],2.2,ww,hh);broad=cv2.GaussianBlur(relief(lum[35:530,47:115],5,ww,hh),(0,0),18);field=np.clip(fine*3.2+broad*3.8,-12,12)*(1-m)**3*texturefade
 # Only actual upper subject silhouette casts shadows; rug/display never casts a false wall shadow.
 body=((m>.985)&(yn<wallend+10/900)&(yn>.10)&(xx>ww*.07)&(xx<ww*.96)).astype('float32')
 def cast(dx,dy,sigma,opacity):
  mat=np.array([[1,0,dx/600*ww],[0,1,dy/900*hh]],dtype='float32');a=cv2.warpAffine(body,mat,(ww,hh),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT);return cv2.GaussianBlur(a,(0,0),sigma/600*ww)*opacity
 shadow=cast(58,8,11,.075)+cast(-28,10,19,.022);fade=1-np.clip((yn-(wallend-65/900))/(65/900),0,1);fade=fade*fade*(3-2*fade);shadow*=((1-m)**2)*fade
 delta=cv2.resize(field,(w,h),interpolation=cv2.INTER_CUBIC);sh=cv2.resize(shadow,(w,h),interpolation=cv2.INTER_CUBIC);cut=round(h*wallend);delta[cut:]=0;sh[cut:]=0;maskbig=cv2.resize(m,(w,h),interpolation=cv2.INTER_LINEAR);keep=maskbig>230/255
 out=np.clip(np.rint((src.astype('float32')+delta[:,:,None])*(1-sh[:,:,None])),0,255).astype('uint8');out[keep]=src[keep];assert np.array_equal(out[keep],src[keep]);assert np.array_equal(out[cut:],src[cut:]);im=Image.fromarray(out);png=O/'PNG'/(stem+'_D_v06.png');jpg=O/'JPG'/(stem+'_D_v06.jpg');im.save(png);im.save(jpg,quality=98,subsampling=0);im.thumbnail((800,1200));im.save(O/(stem+'_VISTA.jpg'),quality=95)
 sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();rec={**item,'status':'en_revision_no_aprobada','version':'D_v06','baseline_sha256':sha(item['base']),'size':[w,h],'protected_pixels_changed':0,'floor_and_lower_zone_changed':0,'wall_end_fraction':wallend,'method':'Acabado D aprobado: textura real del fondo fuente, sombra suavizada de silueta propia; fusion exclusivamente de pared, sin regeneracion ni cambios geometricos. Mascara existente para nuevas lila; proteccion fotometrica de foreground aceptado para previas.','new_generations':0,'png_sha256':sha(png),'jpg_sha256':sha(jpg),'png_bytes':png.stat().st_size,'jpg_bytes':jpg.stat().st_size};(O/(stem+'_auditoria.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');allrecs.append(rec);print(stem,flush=True)
allrecs=[json.load(open(f))for f in sorted(O.glob('*_auditoria.json'))];(O/'MANIFIESTO.json').write_text(json.dumps(allrecs,ensure_ascii=False,indent=2)+'\n')
for page in range((len(allrecs)+14)//15):
 c=Image.new('RGB',(1800,1620),'#eee');d=ImageDraw.Draw(c)
 for j,r in enumerate(allrecs[page*15:(page+1)*15]):
  s=r['source_name'][:-4];a=Image.open(O/(s+'_VISTA.jpg'));a.thumbnail((350,495));x=j%5*360;y=j//5*540;c.paste(a,(x,y+30));d.text((x+8,y+7),s+' D',fill='black')
 c.save(O/f'CONTACTO_D_{page+1}.jpg',quality=96)
