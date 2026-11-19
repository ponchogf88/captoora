from pathlib import Path
import cv2,numpy as np,json
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent/'produccion';d=p/'correcciones_rostros_textos_v03';s=json.load(open(p/'noche_2026-11-04/SELECCION_PRIORIDAD_07722.json'));targets=['DSC07706','DSC07724','DSC07731','DSC07732','DSC08471','DSC08479','DSC08484'];sift=cv2.SIFT_create(nfeatures=10000);bf=cv2.BFMatcher();report=[]; maps=json.load(open(d/'MAPEO_CAPTURAS.json'))
for name in targets:
 x=next(x for x in s if x['source_name']==name+'.JPG');folder=p/x['folder'];src=cv2.imread(str(folder/(name+'_input.png')));out=cv2.imread(str(folder/(name+'_v02.png')));h,w=out.shape[:2];small=cv2.resize(src,(w,h),interpolation=cv2.INTER_AREA);g1=cv2.cvtColor(small,cv2.COLOR_BGR2GRAY);g2=cv2.cvtColor(out,cv2.COLOR_BGR2GRAY);k1,a=sift.detectAndCompute(g1,None);k2,b=sift.detectAndCompute(g2,None);good=[u for u,v in bf.knnMatch(a,b,k=2) if u.distance<.72*v.distance];aa=np.float32([k1[m.queryIdx].pt for m in good]);bb=np.float32([k2[m.trainIdx].pt for m in good]);M,mask=cv2.estimateAffinePartial2D(aa,bb,method=cv2.RANSAC,ransacReprojThreshold=3,maxIters=10000)

 item=next(z['candidates'][0] for z in maps if z['candidates'][0]['photo']==name);cc=np.array(item['corners']);lo=cc.min(0);hi=cc.max(0);face=[int(lo[0]),int(lo[1]),int(hi[0]-lo[0]),int(hi[1]-lo[1])];faces=[face]
 localM=None;local_in=0
 if face:
  fx,fy,fw,fh=face;near=(bb[:,0]>fx-fw*.8)&(bb[:,0]<fx+fw*1.8)&(bb[:,1]>fy-fh*.8)&(bb[:,1]<fy+fh*1.8)
  if near.sum()>=5:
   localM,lmask=cv2.estimateAffinePartial2D(aa[near],bb[near],method=cv2.RANSAC,ransacReprojThreshold=2,maxIters=10000);local_in=int(lmask.sum()) if lmask is not None else 0
 chosen=localM if localM is not None and local_in>=5 else M
 warp=cv2.warpAffine(small,chosen,(w,h));panel=Image.new('RGB',(900,480),'#ddd');draw=ImageDraw.Draw(panel)
 if face:
  fx,fy,fw,fh=face;box=(max(0,int(fx-fw*.4)),max(0,int(fy-fh*.5)),min(w,int(fx+fw*1.4)),min(h,int(fy+fh*1.5)))
  for i,(im,label) in enumerate([(out,'v02 generada'),(warp,'original alineado')]):
   a=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).crop(box);a.thumbnail((440,435));panel.paste(a,(i*450,30));draw.text((i*450+5,5),name+' '+label,fill='black')
 panel.save(d/(name+'_comparacion_fuente.jpg'))
 report.append({'source':name,'folder':x['folder'],'global_matches':len(good),'global_inliers':int(mask.sum()),'matrix_global':M.tolist(),'matrix_used':chosen.tolist(),'local_inliers':local_in,'face_output':face,'faces_output_all':faces,'source_size':[src.shape[1],src.shape[0]],'output_size':[w,h]});print(name,'face',face,'inliers',int(mask.sum()),local_in)
(d/'ALINEACION_PRELIMINAR.json').write_text(json.dumps(report,indent=2))
