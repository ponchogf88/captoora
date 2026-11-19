"""Authorized local pixel restoration. No generative model, network or new text."""
from pathlib import Path
import json,hashlib,cv2,numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parent;P=ROOT/'produccion';D=P/'correcciones_rostros_textos_v03';D.mkdir(exist_ok=True)
S=json.load(open(P/'noche_2026-11-04/SELECCION_PRIORIDAD_07722.json'))
FACE={
'DSC07706':[[711,257],[745,241],[768,243],[778,258],[779,282],[766,305],[741,326],[721,333],[702,320],[690,306],[691,286]],
'DSC07724':[[490,582],[508,573],[525,580],[536,599],[538,613],[551,615],[548,635],[534,642],[520,650],[502,649],[484,640],[475,625],[476,607],[482,590]],
'DSC07731':[[416,628],[440,614],[460,619],[477,634],[486,645],[488,665],[480,683],[460,700],[444,704],[423,690],[410,677],[403,660],[403,643]],
'DSC07732':[[423,617],[440,607],[457,608],[469,620],[472,633],[480,644],[474,651],[475,663],[461,678],[447,682],[431,671],[420,660],[409,647],[404,635],[411,630]],
'DSC08471':[[676,583],[693,574],[709,579],[720,594],[724,613],[727,628],[728,644],[721,660],[707,674],[691,678],[671,672],[653,658],[640,642],[635,623],[641,615],[650,622],[654,609]],
'DSC08479':[[700,489],[717,480],[731,484],[743,498],[750,517],[753,538],[750,557],[747,574],[737,589],[721,595],[702,589],[681,576],[670,560],[660,542],[660,531],[670,526],[677,536],[681,520]],
'DSC08484':[[617,422],[631,413],[646,415],[658,427],[665,444],[667,461],[666,482],[660,501],[645,516],[630,520],[614,514],[597,502],[585,487],[577,474],[576,457],[583,451],[590,461],[597,443]]}
# Product windows are bounded to the held container and foreground display.
HELD={'DSC07720':[309,516,372,586],'DSC07721':[174,290,251,394],'DSC07722':[292,426,365,512],'DSC07724':[350,581,400,633],'DSC07726':[207,536,277,615]}
FOREGROUND={'DSC07706':[250,607,1200,870],'DSC07720':[25,1440,800,1536],'DSC07721':[507,1520,568,1536],'DSC07722':[40,1395,790,1536],'DSC07724':[205,1202,773,1404],'DSC07726':[0,1448,747,1536],'DSC07731':[32,1106,870,1405],'DSC07732':[50,1108,925,1390],'DSC07733':[0,1060,1024,1536],'DSC07734':[0,1085,1024,1536]}
# Restrict broad foreground windows to actual product-color regions plus white containers.
WHITE={'DSC07706':[[950,738,1110,848]],'DSC07720':[[620,1450,800,1536]],'DSC07722':[[590,1420,790,1536]],'DSC07724':[[666,1275,773,1400]],'DSC07726':[[630,1480,747,1536]],'DSC07731':[[730,1230,870,1405]],'DSC07732':[[758,1240,925,1390]],'DSC07733':[[885,1355,1024,1536]],'DSC07734':[[900,1380,1024,1536]]}
SIFT=cv2.SIFT_create(nfeatures=14000);BF=cv2.BFMatcher();AUDIT=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def poly_mask(size,poly,feather=2):
 a=Image.new('L',size);ImageDraw.Draw(a).polygon([tuple(z) for z in poly],fill=255)
 return np.asarray(a.filter(ImageFilter.GaussianBlur(feather)))
def rectpoly(box):x,y,r,b=box;return [[x,y],[r,y],[r,b],[x,b]]
import sys
for x in S:
 if len(sys.argv)>1 and x['source_name'][:-4] not in sys.argv[1:]:continue
 name=x['source_name'][:-4]
 if name not in FACE and name not in FOREGROUND:continue
 folder=P/x['folder'];sp=folder/(name+'_input.png');original=ROOT/'piloto/originales'/x['source_name'];before_hash=sha(original)
 src=cv2.cvtColor(cv2.imread(str(sp)),cv2.COLOR_BGR2RGB);out=cv2.cvtColor(cv2.imread(str(folder/(name+'_v02.png'))),cv2.COLOR_BGR2RGB);h,w=out.shape[:2];sh,sw=src.shape[:2];small=cv2.resize(src,(w,h),interpolation=cv2.INTER_AREA);k1,a=SIFT.detectAndCompute(cv2.cvtColor(small,cv2.COLOR_RGB2GRAY),None);k2,b=SIFT.detectAndCompute(cv2.cvtColor(out,cv2.COLOR_RGB2GRAY),None);good=[u for u,v in BF.knnMatch(a,b,k=2) if u.distance<.72*v.distance];aa=np.float32([k1[m.queryIdx].pt for m in good]);bb=np.float32([k2[m.trainIdx].pt for m in good]);globalM,gi=cv2.estimateAffinePartial2D(aa,bb,method=cv2.RANSAC,ransacReprojThreshold=3,maxIters=10000);assert globalM is not None
 base=np.asarray(Image.fromarray(out).resize((sw,sh),Image.Resampling.LANCZOS)).copy();result=base.copy();union=np.zeros((sh,sw),np.uint8);regions=[];kx=sw/w;ky=sh/h;assert abs(kx-ky)<.01
 plans=[]
 if name in FACE:plans.append(('rostro',FACE[name]))
 if name in HELD:plans.append(('etiqueta_en_mano',rectpoly(HELD[name])))
 if name in FOREGROUND:plans.append(('productos_primer_plano',rectpoly(FOREGROUND[name])))
 for role,poly in plans:
  lo=np.min(poly,axis=0);hi=np.max(poly,axis=0);pad=50 if role!='rostro' else 60;near=(bb[:,0]>lo[0]-pad)&(bb[:,0]<hi[0]+pad)&(bb[:,1]>lo[1]-pad)&(bb[:,1]<hi[1]+pad);M=globalM;nin=int(gi.sum())
  if near.sum()>=6:
   lm,li=cv2.estimateAffinePartial2D(aa[near],bb[near],method=cv2.RANSAC,ransacReprojThreshold=2,maxIters=10000)
   if lm is not None and li.sum()>=6:M=lm;nin=int(li.sum())
  masklow=poly_mask((w,h),poly,1.8 if role=='rostro' else 1)
  if role=='productos_primer_plano':
   # Physical product-color support; no skin/person replacement in display gaps.
   rr,gg,bl=out[:,:,0].astype(float),out[:,:,1].astype(float),out[:,:,2].astype(float)
   pink=(rr-gg>5)&(bl-gg>4)&(rr>90)&(bl>95)
   # Morphology closes printed white letters within the packaging silhouette.
   binary=(pink.astype(np.uint8)*255);binary=cv2.morphologyEx(binary,cv2.MORPH_CLOSE,np.ones((13,13),np.uint8));binary=cv2.dilate(binary,np.ones((5,5),np.uint8))
   # Explicit bounded white-package windows restore their actual printing.
   for box in WHITE.get(name,[]):
    xx,yy,rrr,bbb=box;binary[yy:bbb,xx:rrr]=255
   masklow=np.minimum(masklow,binary)
  mask=np.asarray(Image.fromarray(masklow).resize((sw,sh),Image.Resampling.BILINEAR));polyhi=np.asarray(poly)*[kx,ky];bx0=max(0,int(polyhi[:,0].min())-24);by0=max(0,int(polyhi[:,1].min())-24);bx1=min(sw,int(polyhi[:,0].max())+24);by1=min(sh,int(polyhi[:,1].max())+24)
  # Transform only source pixels with a similarity transform (no face reshaping).
  mh=M.copy();mh[:,2]*=kx;mh[0,2]-=bx0;mh[1,2]-=by0
  warped=cv2.warpAffine(src,mh,(bx1-bx0,by1-by0),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
  m=mask[by0:by1,bx0:bx1];dest=base[by0:by1,bx0:bx1];sel=m>245;assert sel.sum()>0
  a=warped[sel].astype(float);b=dest[sel].astype(float);la=a.mean(1);lb=b.mean(1);spread=max(8,np.percentile(la,80)-np.percentile(la,20));gain=float(np.clip((np.percentile(lb,80)-np.percentile(lb,20))/spread,.8,1.5));offset=np.median(b-gain*a,axis=0);offset=np.clip(offset,-140,80)
  if role=='productos_primer_plano':
   # Preserve source neutral whites; reject empty source floor and absent dark clutter.
   adjusted=np.clip(255-gain*(255-warped.astype(np.float32)),0,255).astype(np.uint8)
   blank=(warped.min(2)>=248)&(dest.mean(2)>=210)
   absent_dark=(warped.mean(2)<80)&(dest.mean(2)>200)
   m=m.copy();m[blank|absent_dark]=0
   mask=mask.copy();mask[by0:by1,bx0:bx1]=m
   offset=np.zeros(3)
  else:adjusted=np.clip(warped.astype(np.float32)*gain+offset,0,255).astype(np.uint8)
  alpha=m.astype(np.float32)[:,:,None]/255
  result[by0:by1,bx0:bx1]=np.rint(result[by0:by1,bx0:bx1]*(1-alpha)+adjusted*alpha).astype(np.uint8);union=np.maximum(union,mask)
  regions.append({'role':role,'polygon_output_v02':poly,'similarity':M.tolist(),'registration_inliers':nin,'light_gain':gain,'light_offset_rgb':offset.tolist(),'original_near_white_fraction':float(np.mean(np.all(a>=250,axis=1))),'pixels_covered':int((mask>0).sum())})
 assert np.array_equal(result[union==0],base[union==0]);assert sha(original)==before_hash
 Image.fromarray(result).save(D/(name+'_v03.png'),compress_level=1);Image.fromarray(result).save(D/(name+'_v03.jpg'),quality=98,subsampling=0);Image.fromarray(union).save(D/(name+'_zonas.png'),compress_level=1)
 preview=Image.fromarray(result);preview.thumbnail((900,1200));preview.save(D/(name+'_revision.jpg'),quality=96)
 rec={'source_name':x['source_name'],'source_id':x['source_id'],'source_url':x['source_url'],'folder_anterior':x['folder'],'version':'v03','method':'restauracion_local_pixeles_originales_autorizada_sin_generacion','original_sha256':before_hash,'base_v02_sha256':sha(folder/(name+'_v02.png')),'size':[sw,sh],'base':'v02 escalada Lanczos a resolucion del original; sin cambiar encuadre','outside_mask_changed_pixels':0,'regions':regions,'estado':'corregida_pendiente_revision','limitations':'No inventa texto/rasgos: detalles quemados o desenfocados en JPG original no son recuperables. Fondo ampliado no adquiere detalle optico nuevo.'};(D/(name+'_restauracion.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2));AUDIT.append(rec);print(name,'saved',len(regions),'regions',flush=True)
(D/'AUDITORIA_RESTAURACION.json').write_text(json.dumps([json.load(open(f)) for f in sorted(D.glob('*_restauracion.json'))],ensure_ascii=False,indent=2))
