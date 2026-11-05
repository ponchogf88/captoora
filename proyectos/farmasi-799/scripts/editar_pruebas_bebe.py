from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFilter
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;O=P/'pruebas_v01';O.mkdir(exist_ok=True);(O/'PNG').mkdir(exist_ok=True);(O/'JPG').mkdir(exist_ok=True)
# Pixel-local color/exposure curves, no synthesized facial pixels, no morphing,
# no noise smoothing, no substitution from other frames.
names=['DSC08258.JPG','DSC08290 2.JPG','DSC08295.JPG'];records=[];comparison=Image.new('RGB',(1800,1550),'#f1eeea');dr=ImageDraw.Draw(comparison)
for i,n in enumerate(names):
 path=P/'originales'/n;src=ImageOps.exif_transpose(Image.open(path)).convert('RGB').transpose(Image.Transpose.ROTATE_90);w,h=src.size
 # A narrow outer framing adjustment removes the room sliver at the right edge;
 # no body/face geometry is changed. Source stays full-resolution in originales.
 box=(0,0,int(w*.978),h) if n!='DSC08258.JPG' else (0,0,w,h)
 framed=src.crop(box);a=np.array(framed);wb=np.array([1.035,1.0,.974]);v=np.clip(a.astype(np.float32)*wb,0,255);v=v+2.5*np.sin(np.pi*v/255)-8*(v/255)**6;out=np.rint(np.clip(v,0,255)).astype('uint8');im=Image.fromarray(out)
 # Deliberately no sharpening or face beautification: retain the real capture detail.
 stem=Path(n).stem;pp=O/'PNG'/f'{stem}_bebe_v01.png';jp=O/'JPG'/f'{stem}_bebe_v01.jpg';im.save(pp);im.save(jp,quality=97,subsampling=0)
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 records.append({'source_name':n,'original_sha256':sha(path),'png_sha256':sha(pp),'jpg_sha256':sha(jp),'estado':'en_revision','version':'bebe_v01','method':'Curvas locales de color y luz desde pixeles originales, sin generacion','rotate_ccw':90,'crop_box':box,'white_balance_gains':wb.tolist(),'highlight_reduction_at_white':8,'original_size_upright':[w,h],'output_size':list(im.size),'face_geometry_changed':False,'face_regenerated':False,'cross_frame_composite':False,'sharpen_or_denoise':False,'limitations':'Movimiento y luces recortadas de captura no se reconstruyen ni inventan; se seleccionan fuentes con detalle real.'})
 for j,photo in enumerate([framed,im]):
  sm=photo.copy();sm.thumbnail((290,500));x=i*600+j*300;y=35;comparison.paste(sm,(x,y));dr.text((x+5,8),stem+(' ORIGINAL'if j==0 else ' CORREGIDA'),fill='black')
 # Baby-face detail at matched scale to review actual texture, not display-size illusion.
 face_boxes={'DSC08258.JPG':(.22,.29,.59,.53),'DSC08290 2.JPG':(.24,.46,.65,.72),'DSC08295.JPG':(.28,.43,.67,.68)};b=face_boxes[n];fb=tuple(round(z*t)for z,t in zip(b,[im.width,im.height,im.width,im.height]))
 for j,photo in enumerate([framed,im]):
  detail=photo.crop(fb);detail.thumbnail((590,590));x=i*600;y=620+j*470;detail.thumbnail((580,440));comparison.paste(detail,(x,y+20));dr.text((x+5,y),('DETALLE ORIGINAL'if j==0 else 'DETALLE CORREGIDO'),fill='black')
 preview=im.copy();preview.thumbnail((1400,1600));preview.save(O/f'{stem}_VISTA.jpg',quality=95)
comparison.save(O/'COMPARACION_TRES_PRUEBAS.jpg',quality=96);(O/'MANIFIESTO.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));print([(r['source_name'],r['output_size'])for r in records])
