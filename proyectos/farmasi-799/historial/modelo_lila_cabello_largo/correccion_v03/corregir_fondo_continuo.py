from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageOps
import cv2,numpy as np,json,sys,hashlib
P=Path(__file__).resolve().parents[1];O=P/'correccion_v03';(O/'PNG').mkdir(exist_ok=True);(O/'JPG').mkdir(exist_ok=True)
# Coordinates in an inspected600x900view; broad search windows only, not delivered polygon cutouts.
C={'DSC07736':((55,300,470,700),580), 'DSC07738':((108,235,495,670),545),'DSC07739':((87,255,474,680),575),'DSC07743':((54,325,452,900),790),'DSC07747':((141,335,463,900),800),'DSC07762':((145,258,410,760),730),'DSC07767':((122,90,482,867),730),'DSC07768':((120,92,477,863),730),'DSC07772':((163,213,434,773),720),'DSC07774':((164,235,407,742),700)}
# Verbatim white held packages, manually bounded, opaque original source printing.
WHITE={'DSC07743':[(384,247),(412,247),(420,417),(382,421)],'DSC07747':[(383,253),(408,251),(427,417),(390,420)]}
# Opaque garment guards traced INSIDE the real clothing contours so white print is never erased by chroma segmentation.
BODY={
'DSC07736':[(160,393),(207,399),(236,415),(247,435),(250,462),(264,505),(276,533),(340,549),(380,573),(412,606),(426,638),(355,655),(294,627),(215,627),(198,602),(199,553),(188,509),(166,480)],
'DSC07738':[(180,351),(235,364),(264,380),(284,404),(289,447),(288,483),(318,503),(370,518),(420,548),(441,573),(451,604),(420,610),(355,598),(290,588),(236,580),(226,562),(228,533),(239,491),(223,458),(199,427),(181,404)],
'DSC07739':[(172,378),(210,382),(243,396),(273,413),(285,438),(288,469),(282,507),(324,531),(365,548),(395,571),(422,602),(422,628),(355,627),(285,609),(235,604),(209,591),(205,569),(214,529),(215,500),(197,457)],
'DSC07743':[(193,426),(244,432),(278,428),(293,442),(305,480),(301,526),(298,558),(301,600),(314,654),(341,710),(355,761),(346,824),(330,832),(315,764),(280,706),(260,666),(248,705),(236,765),(229,845),(201,853),(190,781),(188,735),(180,692),(173,650),(168,620),(173,584),(180,549),(189,520),(190,480)],
'DSC07747':[(221,418),(257,424),(283,422),(302,444),(317,483),(314,531),(315,573),(325,608),(349,670),(366,737),(369,812),(353,824),(335,788),(319,740),(301,703),(279,666),(267,704),(251,749),(242,800),(211,799),(200,748),(194,689),(195,638),(202,602),(210,580),(225,561),(213,537),(213,483),(205,465)],
'DSC07762':[(220,355),(282,363),(294,392),(293,422),(299,454),(297,479),(335,486),(380,499),(394,512),(391,536),(371,558),(344,583),(324,607),(309,601),(322,577),(337,551),(298,548),(282,576),(280,622),(276,673),(271,705),(252,705),(248,656),(240,602),(233,560),(226,535),(223,502),(233,470),(246,453),(242,430),(217,404)],
'DSC07767':[(202,234),(243,235),(290,274),(309,294),(310,335),(305,374),(307,414),(388,438),(444,456),(468,480),(469,500),(455,525),(427,558),(403,592),(386,621),(374,617),(355,603),(377,574),(395,548),(350,550),(303,546),(296,584),(288,641),(285,696),(268,735),(248,735),(245,686),(241,638),(232,587),(220,548),(205,527),(200,503),(204,474),(218,441),(225,415),(224,382),(210,355),(196,323),(189,286)],
'DSC07768':[(200,234),(243,237),(288,276),(305,297),(306,337),(302,374),(304,414),(385,438),(440,456),(466,480),(467,500),(453,525),(425,558),(400,592),(383,621),(370,617),(352,603),(374,574),(393,548),(348,550),(302,546),(295,584),(287,641),(284,696),(267,735),(247,735),(244,686),(240,638),(231,587),(219,548),(204,527),(199,503),(203,474),(217,441),(224,415),(223,382),(209,355),(195,323),(188,286)],
'DSC07772':[(219,321),(267,325),(291,355),(300,386),(300,419),(299,453),(347,466),(392,481),(417,500),(416,519),(396,543),(372,566),(351,594),(337,608),(319,600),(330,578),(349,550),(322,543),(301,544),(291,580),(287,624),(281,676),(276,711),(259,711),(256,659),(250,612),(242,567),(232,540),(225,522),(225,500),(234,471),(239,446),(233,416),(222,388)],
'DSC07774':[(222,334),(258,337),(289,365),(295,401),(295,435),(290,459),(338,464),(382,477),(400,493),(399,512),(376,540),(352,570),(331,597),(315,593),(326,569),(345,543),(318,535),(295,537),(286,578),(283,625),(277,674),(272,697),(257,697),(254,649),(248,608),(238,561),(228,535),(224,511),(228,486),(236,459),(235,425),(225,389)]}
HEAD={'DSC07736':(65,302,181,397),'DSC07738':(117,268,226,365),'DSC07739':(102,284,221,391),'DSC07743':(180,325,267,430),'DSC07747':(202,335,294,434),'DSC07762':(191,261,271,359),'DSC07767':(137,96,244,245),'DSC07768':(133,99,243,247),'DSC07772':(174,219,270,329),'DSC07774':(168,247,268,344)}
SHOE={'DSC07762':(283,590,340,665),'DSC07767':(290,615,392,728),'DSC07768':(286,614,389,729),'DSC07772':(300,588,361,678),'DSC07774':(285,565,345,647)}
HELD={'DSC07762':(321,270,352,349),'DSC07767':(318,102,364,246),'DSC07768':(305,112,350,258),'DSC07772':(281,237,305,348),'DSC07774':(272,286,299,365)}
sel=sys.argv[1:]or list(C)
for stem in sel:
 b=Image.open(P/'lote_individual_v02/PNG'/(stem+'_lila_v02.png')).convert('RGB');w,h=b.size;src=np.array(b)
 if stem in ['DSC07736','DSC07738','DSC07739']:
  # Restore the whole genuine foreground display from the untouched original; v02 side fills partly faded peripheral bottle tops.
  real=np.array(ImageOps.exif_transpose(Image.open(P/'originales'/(stem+'.JPG'))).convert('RGB').transpose(Image.Transpose.ROTATE_90));lutbase=np.rint(np.interp(np.arange(256),[0,32,64,128,160,192,216,232,248,255],[0,27,55,105,136,169,197,218,240,248])).astype('uint8');real=lutbase[real]
  start={'DSC07736':590,'DSC07738':550,'DSC07739':580}[stem];weight=np.clip((np.arange(h)/(h/900)-start)/20,0,1).astype('float32')[:,None,None];src=np.rint(src*(1-weight)+real*weight).astype('uint8')
 a=np.array(Image.fromarray(src).resize((1200,1800),Image.Resampling.LANCZOS));roi,floor=C[stem];x0,y0,x1,y1=[int(x*2)for x in roi];ys,xs=np.indices(a.shape[:2]);inside=(xs>=x0)&(xs<x1)&(ys>=y0)&(ys<y1);hsv=cv2.cvtColor(a,cv2.COLOR_RGB2HSV);sat=hsv[:,:,1];val=hsv[:,:,2]
 mask=np.full(a.shape[:2],cv2.GC_BGD,dtype='uint8');mask[inside]=cv2.GC_PR_FGD
 # Learn actual foreground/background colors within inspected windows; no generative subject editing.
 rr=a[:,:,0].astype('int16');gg=a[:,:,1].astype('int16');bb=a[:,:,2].astype('int16');fg=inside&((val<125)|((rr-gg>8)&(rr-bb>5))|((rr-gg>4)&(bb-gg>4)));bg=inside&(((sat<8)&(val>230))|((gg-rr>2)&(bb-rr>0)&(val>145)));mask[fg]=cv2.GC_FGD;mask[bg]=cv2.GC_PR_BGD
 for poly in [WHITE.get(stem,[])]:
  if poly:cv2.fillPoly(mask,[np.array(poly,dtype='int32')*2],cv2.GC_FGD)
 cv2.grabCut(a,mask,None,np.zeros((1,65),np.float64),np.zeros((1,65),np.float64),4,cv2.GC_INIT_WITH_MASK)
 binary=((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD)).astype('uint8')*255
 # White garment print, eyes, teeth and package letters inside silhouettes remain opaque.
 cv2.fillPoly(binary,[np.array(BODY[stem],dtype='int32')*2],255)
 # Keep genuine openings between arms/torso out of filled silhouette, determined from source paper.
 # Filled interiors are checked visually before any delivery.
 binary=cv2.morphologyEx(binary,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
 hx,hy,hr,hb=HEAD[stem];cv2.ellipse(binary,((hx+hr),(hy+hb)),((hr-hx),(hb-hy)),0,0,360,255,-1)
 if stem in SHOE:
  sx,sy,sr,sb=SHOE[stem];cv2.rectangle(binary,(sx*2,sy*2),(sr*2,sb*2),255,-1)
 if stem in HELD:
  px,py,pr,pb=HELD[stem];cv2.rectangle(binary,(px*2,py*2),(pr*2,pb*2),255,-1)
 product_top={'DSC07736':605,'DSC07738':570,'DSC07739':590,'DSC07762':825,'DSC07772':825,'DSC07774':795}.get(stem)
 if product_top is not None:
  pinkall=((rr-gg>3)&(bb-gg>3)&(val>100)).astype('uint8')*255;pinkall[:product_top*2]=0
  pinkall=cv2.morphologyEx(pinkall,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8));binary=np.maximum(binary,pinkall)
 matte=Image.fromarray(binary).resize((w,h),Image.Resampling.LANCZOS);core=np.array(matte)>127;distance=cv2.distanceTransform((~core).astype('uint8'),cv2.DIST_L2,5);alpha=np.exp(-np.square(distance/(w*.033)));alpha[core]=1;alpha[alpha<.002]=0
 # Native plate remapped to each real floor height; one surface across the ENTIRE wall, never side strips.
 plate=np.array(Image.open(P/'hibrido/fondo_vacio_nativo.png').convert('RGB').resize((w,h),Image.Resampling.LANCZOS));yy=np.arange(h,dtype='float32')/h;horizon=(floor-15)/900;sy=np.where(yy<horizon,yy*.8/horizon,.8+(yy-horizon)*.2/(1-horizon));mapy=np.broadcast_to((sy*h).astype('float32')[:,None],(h,w));mapx=np.broadcast_to(np.arange(w,dtype='float32')[None,:],(h,w));plate=cv2.remap(plate,mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
 # Keep real original rug and all foreground containers below room boundaries, broad horizontal rug blend.
 flooralpha=np.clip((yy-(floor-25)/900)/(50/900),0,1);alpha=np.maximum(alpha,flooralpha[:,None]);alpha[alpha>.999]=1
 # Retain fine contact shadows on rug; empty backdrop has restrained natural depth.
 out=np.rint(src*alpha[:,:,None]+plate*(1-alpha[:,:,None])).astype('uint8')
 # Label enhancement uses authentic pixels only, no letters reconstructed or drawn.
 lm=Image.new('L',(w,h));ld=ImageDraw.Draw(lm);scale=w/600
 if stem in WHITE:ld.polygon([(round(x*scale),round(y*scale))for x,y in WHITE[stem]],fill=255)
 if stem in HELD:
  xx,yy,rr,bb=HELD[stem];ld.rectangle(tuple(round(v*scale)for v in (xx,yy,rr,bb)),fill=255)
 # Tight product-only masks in the real foreground display; excludes skin and clothing by both location and package hue.
 foreground_y={'DSC07736':700,'DSC07738':700,'DSC07739':700,'DSC07762':830,'DSC07772':830,'DSC07774':800}.get(stem)
 lma=np.array(lm)
 if foreground_y is not None:
  pink=(src[:,:,0].astype('int16')-src[:,:,1]>3)&(src[:,:,2].astype('int16')-src[:,:,1]>3);pink[:round(foreground_y*scale)]=False
  pm=cv2.morphologyEx(pink.astype('uint8')*255,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8));lma=np.maximum(lma,pm)
 lma=np.array(Image.fromarray(lma).filter(ImageFilter.GaussianBlur(2)));la=lma.astype('float32')/255;la[alpha<.999]=0
 detail=np.array(Image.fromarray(src).filter(ImageFilter.UnsharpMask(radius=1.1,percent=70,threshold=3)))
 if stem in WHITE:
  lut=np.rint(np.interp(np.arange(256),[0,128,180,205,220,232,240,248,255],[0,120,165,185,202,222,234,248,255])).astype('uint8');detail=lut[detail]
 before_labels=out.copy();out=np.rint(out*(1-la[:,:,None])+detail*la[:,:,None]).astype('uint8')
 # All protected face pixels must remain exactly as accepted v02, not just visually similar.
 headmask=np.zeros((h,w),np.uint8);cv2.ellipse(headmask,(round((hx+hr)/2*scale),round((hy+hb)/2*scale)),(round((hr-hx)/2*scale*.85),round((hb-hy)/2*scale*.85)),0,0,360,255,-1)
 face_changed=int(np.count_nonzero(np.any(out[headmask>0]!=src[headmask>0],axis=1)));assert face_changed==0,(stem,face_changed)
 accepted=np.array(b);warm=(accepted[:,:,0].astype('int16')>accepted[:,:,1].astype('int16')+8)&(accepted[:,:,0].astype('int16')>accepted[:,:,2].astype('int16')+8)&(accepted.mean(2)>100)&(alpha>.998);out[warm]=accepted[warm]
 im=Image.fromarray(out);im.save(O/'PNG'/(stem+'_lila_v03.png'));im.save(O/'JPG'/(stem+'_lila_v03.jpg'),quality=98,subsampling=0);matte=Image.fromarray(np.rint(alpha*255).astype('uint8'));matte.save(O/(stem+'_mascara_preservacion.png'));im.thumbnail((900,1350));im.save(O/(stem+'_VISTA.jpg'),quality=96)
 rec={'source_name':stem+'.JPG','baseline':'lila_v02_rechazada_solo_fondo','method':'Superficie completa nativa vacia con mascara fotometrica local, sujetos y productos desde pixeles v02 originales; sin generacion de personas','status':'revision_tecnica_interna','foreground_window_600x900':roi,'floor_600x900':floor,'preserved_opaque_pixels':int((alpha==1).sum()),'opaque_nonlabel_changed_pixels':int(np.count_nonzero(np.any(out[(alpha==1)&(la==0)]!=src[(alpha==1)&(la==0)],axis=1))),'protected_face_changed_pixels':face_changed,'label_pixels_modified':int(np.count_nonzero(np.any(out!=before_labels,axis=2))),'label_method':'UnsharpMask radius1.1percent70threshold3; whitepackages monotone contrast curve; no synthesized text','png_sha256':hashlib.sha256((O/'PNG'/(stem+'_lila_v03.png')).read_bytes()).hexdigest()};(O/(stem+'_auditoria.json')).write_text(json.dumps(rec,indent=2));print(stem,flush=True)
