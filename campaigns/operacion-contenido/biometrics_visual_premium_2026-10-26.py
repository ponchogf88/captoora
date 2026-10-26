from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,Color
from PIL import Image
import os,fitz
D=os.path.dirname(__file__)
pdfmetrics.registerFont(TTFont('Sans','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
W,H=720,960
out=D+'/CAPTOORA_Biometrics_Visual_Premium.pdf'
c=canvas.Canvas(out,pagesize=(W,H));c.setTitle('CAPTOORA Biometrics | Propuesta visual');c.setAuthor('CAPTOORA Studio')
CY='#58E4FF'; LIME='#BDFB59';WHITE='#F3F5F7'
def txt(x,y,t,size=15,color=WHITE,font='Sans'):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,y,t)
def lines(x,y,ls,size=19,step=29,color=WHITE,font='Sans'):
 for s in ls:txt(x,y,s,size,color,font);y-=step
def bg(n,kicker):
 c.setFillColor(HexColor('#070B11'));c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFillColor(HexColor('#0C1822'));c.circle(670,920,220,fill=1,stroke=0)
 txt(38,922,'CAPTOORA',15,WHITE,'Bold');txt(38,903,'B I O M E T R I C S',8,CY)
 txt(38,866,kicker.upper(),10,CY,'Bold')
 c.setStrokeColor(HexColor('#23333F'));c.line(38,45,682,45)
 txt(38,26,'DIRECCIÓN VISUAL · 26 OCT 2026',8,'#8A9CA9');txt(634,26,f'{n:02d} / 12',8,'#8A9CA9')
def photo(name,x,y,w,h):
 p=name if str(name).startswith('/') else D+'/pexels-'+str(name)+'.jpg'
 im=Image.open(p); iw,ih=im.size;s=min(w/iw,h/ih);dw,dh=iw*s,ih*s
 c.drawImage(p,x+(w-dw)/2,y+(h-dh)/2,dw,dh,mask='auto')
def glass(x,y,w,h):
 c.saveState();c.setFillColor(Color(.1,.17,.22,alpha=.65));c.setStrokeColor(Color(.35,.65,.7,alpha=.35));c.roundRect(x,y,w,h,14,fill=1,stroke=1);c.restoreState()
def end():c.showPage()
ai='/workspace/generated_images/exec-ba82db1d-249b-41f1-a7f9-527674798559.png'

bg(1,'Una etapa merece una imagen')
photo(29479983,275,145,420,675)
lines(38,775,['TU CUERPO.','TU HISTORIA.'],38,49,font='Bold')
lines(40,632,['Retrato deportivo.','Registro visual.','Contenido propio.'],17,29,color='#BDCED8')
glass(38,96,286,122);txt(56,181,'LA PROPUESTA',10,CY,'Bold');lines(56,150,['Guardar lo que eres hoy.','Preparar lo que viene.'],15,25)
txt(38,62,'Fotografía de referencia · Pexels 29479983 · No es sesión CAPTOORA',8,'#8A9CA9');end()

bg(2,'Así queremos que se vea')
lines(38,807,['LUZ QUE DEFINE.','PRESENCIA QUE SE SIENTE.'],28,37,font='Bold')
photo(29479983,38,250,310,455);photo(ai,370,250,310,455)
txt(40,223,'AZUL + ROJO',13,CY,'Bold');txt(373,223,'CIAN + VERDE',13,CY,'Bold')
lines(40,188,['Referencia fotográfica','Pexels · luz dramática'],12,20,color='#AABBC7')
lines(373,188,['Concepto IA ya existente','Sin nueva generación'],12,20,color='#AABBC7')
txt(38,104,'Dos caminos de luz. Probarlos en estudio antes de ofrecer el resultado.',12)
txt(38,71,'Referencias visuales, no portafolio de clientes.',9,'#8A9CA9');end()

bg(3,'Cuatro formas de retratarte')
txt(38,806,'UNA MARCA. VARIAS MIRADAS.',27,WHITE,'Bold')
photo(14252108,38,337,310,409);photo(29479983,371,337,310,409)
glass(38,210,310,108);glass(371,210,310,108)
lines(55,282,['01  ACCIÓN','Movimiento y fuerza.'],15,26,font='Bold');lines(388,282,['02  REGISTRO','Frente, perfil, fechas.'],15,26,font='Bold')
lines(40,155,['03  ARTÍSTICO / BOUDOIR','Luz, pose y expresión adulta.'],13,25)
lines(373,155,['04  ÍNTIMO ADULTO','Límites y permisos específicos.'],13,25)
txt(38,70,'Las líneas 03–04 se desarrollan aparte; no se muestran casos ficticios.',9,'#8A9CA9');end()

bg(4,'Guardar el proceso')
txt(38,806,'LA MISMA PERSONA. OTRA FECHA.',26,WHITE,'Bold')
photo(ai,222,249,465,510)
for y,t,sub in [(694,'FRENTE','Postura acordada'),(550,'PERFIL','Condiciones repetibles'),(405,'REGISTRO','Fecha y contexto')]:
 txt(38,y,t,14,CY,'Bold');txt(38,y-25,sub,10,'#AABBC7')
glass(38,97,644,108);lines(57,167,['Antes / después: solo con un caso real autorizado.','Sin modificar anatomía ni inventar resultados.'],16,28)
txt(38,70,'Concepto IA existente. Fotografía no equivale a diagnóstico o escaneo.',9,'#8A9CA9');end()

bg(5,'Tu campaña de enero empieza antes')
txt(38,807,'COACHES + CREADORES',29,WHITE,'Bold')
photo(30283455,307,207,375,552)
lines(38,685,['PRESENTACIÓN','ACCIÓN','DETALLE'],20,57,font='Bold')
lines(38,447,['Un banco de imágenes','para comunicar','tu trabajo.'],16,27,color='#BACAD6')
glass(38,99,644,91);txt(59,155,'CTA',10,CY,'Bold');txt(59,127,'«Consulta tu producción para enero».',20,WHITE,'Bold')
txt(38,71,'Referencia Pexels 30283455 · Producción especial por cotizar.',9,'#8A9CA9');end()

bg(6,'La puerta de entrada')
photo(ai,310,183,379,640)
lines(38,784,['TU PRIMERA','SESIÓN.'],33,43,font='Bold')
txt(38,647,'$1,000',49,CY,'Bold');txt(40,616,'MXN · BÁSICA VIGENTE',10,'#ADC0CD')
lines(40,535,['1 hora','1 set con luces','Dirección de pose','15 fotos editadas'],17,37)
glass(38,103,644,79);txt(57,151,'CONSULTA FECHA POR WHATSAPP',11,CY,'Bold');txt(57,124,'81 4005 0088',21,WHITE,'Bold')
txt(38,70,'Concepto IA · confirmar disponibilidad, entrega y condiciones de reserva.',9,'#8A9CA9');end()

bg(7,'Que el beneficio ya esté incluido')
txt(38,807,'TRES FORMAS DE LLEGAR.',29,WHITE,'Bold')
photo(30283455,415,392,265,365)
for y,n,t,sub in [(690,'01','DIRECTO','La persona contrata.'),(554,'02','GIMNASIO','Compra un bloque para socios.'),(418,'03','TOTALPASS','Solicitar evaluación de alianza.')]:
 txt(38,y,n,33,CY,'Bold');txt(108,y+6,t,17,WHITE,'Bold');txt(108,y-22,sub,11,'#B4C4D0')
glass(38,137,644,171);lines(58,270,['Primero un piloto pagado.','Después, visitas y alcance definidos.'],22,37,font='Bold');txt(58,180,'Sin membresías ilimitadas ni alianza TotalPass anunciada.',12,'#B4C4D0')
txt(38,70,'Referencia Pexels · TotalPass: elegibilidad y remuneración pendientes.',9,'#8A9CA9');end()

bg(8,'Capti / concepto de producto')
txt(38,807,'TU PLAN. BIEN ORGANIZADO.',28,WHITE,'Bold')
photo(1640777,38,238,322,477)
glass(383,218,299,511)
txt(405,684,'CAPTI',24,CY,'Bold');txt(405,657,'TU BITÁCORA PERSONAL',9,'#A9BDCA')
for y,head,sub in [(589,'08:00 / REGISTRAR','¿Qué desayunaste?'),(476,'14:00 / RECORDAR','Tu horario configurado.'),(363,'20:00 / RESUMIR','Revisa y comparte tu registro.')]:
 c.setStrokeColor(HexColor('#324653'));c.line(404,y+35,661,y+35);txt(405,y,head,11,CY,'Bold');txt(405,y-28,sub,11)
lines(38,154,['Tú aportas el plan de tu profesional.','Capti organiza; no prescribe.'],20,32,font='Bold')
txt(38,70,'Pexels 1640777 · Interfaz conceptual, aplicación aún no construida.',9,'#8A9CA9');end()

bg(9,'Video / el valor del recuerdo')
txt(38,807,'«¿TIENES UNA FOTO?»',31,WHITE,'Bold')
photo(6973110 if os.path.exists(D+'/pexels-6973110.jpg') else 8057028,38,369,644,379)
glass(38,191,644,151)
lines(58,304,['01  «Yo también entrenaba así».','02  «¿Tienes una foto?»','03  «Dale una imagen a esta etapa».'],18,39)
txt(38,130,'30 segundos · conversación + recuerdo + retrato actual',13,CY,'Bold')
txt(38,76,'Referencia de casting/atmósfera Pexels · dramatización por producir.',9,'#8A9CA9');end()

bg(10,'Cómo convertir atención en venta')
txt(38,807,'UNA IMAGEN. UN SIGUIENTE PASO.',25,WHITE,'Bold')
photo(29479983,378,225,304,520)
for y,a,b in [(710,'VER','Foto real autorizada.'),(582,'PREGUNTAR','WhatsApp + objetivo + fecha.'),(454,'DECIDIR','Incluidos y propuesta clara.'),(326,'COBRAR','Pago completo con evidencia.')]:
 txt(38,y,a,23,CY,'Bold');txt(38,y-31,b,12)
glass(38,103,644,78);txt(59,148,'La recompra crea recurrencia.',21,WHITE,'Bold');txt(59,121,'No los seguidores. No los regalos. No los documentos.',12,'#B4C4D0')
txt(38,70,'Referencia Pexels · cero pauta inicial.',9,'#8A9CA9');end()

bg(11,'El orden para arrancar')
txt(38,807,'PROBAR. VENDER. REPETIR.',29,WHITE,'Bold')
photo(ai,420,279,262,468)
for y,n,t,sub in [(701,'AHORA','Oferta básica','Primera sesión cobrada.'),(555,'NOVIEMBRE','Piloto fitness','Costo y entrega reales.'),(409,'DICIEMBRE','Preparar enero','Alcance y agenda aprobados.'),(263,'ENERO','Volver a contratar','Medir margen y recompra.')]:
 txt(38,y,n,10,CY,'Bold');txt(38,y-32,t,24,WHITE,'Bold');txt(38,y-61,sub,12,'#B4C4D0')
txt(38,113,'Capti y TotalPass avanzan en paralelo; no bloquean vender hoy.',12)
txt(38,70,'Concepto IA existente · sin inversión publicitaria nueva.',9,'#8A9CA9');end()

bg(12,'Selección visual / procedencia')
txt(38,807,'REFERENCIAS, CON CLARIDAD.',27,WHITE,'Bold')
photo(29479983,38,412,202,325);photo(30283455,257,412,202,325);photo(ai,477,412,202,325)
lines(38,368,['PEXELS','29479983 · 30283455','14252108 · 1640777','6973110 / 8057028'],12,23)
lines(376,368,['CONCEPTO IA EXISTENTE','Atleta con kettlebell.','Reutilizado; sin créditos nuevos.'],12,23)
glass(38,113,644,137);lines(58,212,['Son referencias, no clientes de CAPTOORA.','Licencia: pexels.com/license','El detalle operativo permanece en GitHub.'],14,31)
txt(38,70,'Canva: búsqueda consultada; diseño de marca sin permiso de acceso.',9,'#8A9CA9');end()
c.save()
d=fitz.open(out)
for i in range(len(d)):
 d[i].get_pixmap(matrix=fitz.Matrix(.55,.55)).save(D+f'/visual-{i+1:02d}.png')
print(out, 'páginas:',len(d))
