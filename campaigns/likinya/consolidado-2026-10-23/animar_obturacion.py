"""Diagrama animado propio: exposición y movimiento; no fotografías simuladas."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, math

ROOT=Path(__file__).resolve().parent
W,H,FPS=720,1280,24
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(n,b=False): return ImageFont.truetype(BOLD if b else FONT,n)
def render(t):
    im=Image.new('RGB',(W,H),'#10130f');d=ImageDraw.Draw(im)
    d.text((52,80),'CAPTOORA',font=font(26,True),fill='#cef66a')
    d.text((52,140),'TIEMPO Y',font=font(56,True),fill='white')
    d.text((52,205),'MOVIMIENTO',font=font(56,True),fill='white')
    d.text((52,295),'Diagrama ilustrativo',font=font(25),fill='#b7bdb1')
    x=170+370*(0.5+0.5*math.sin(t*0.85))
    for cy,label,trail in [(475,'EXPOSICIÓN MÁS CORTA',0),(755,'EXPOSICIÓN MÁS LARGA',150)]:
        d.rounded_rectangle((45,cy-85,675,cy+130),radius=24,fill='#20261c')
        d.text((70,cy-60),label,font=font(27,True),fill='#cef66a')
        d.line((95,cy+60,625,cy+60),fill='#59614e',width=2)
        if trail:
            for k in range(24):
                xx=x-trail+k*trail/24
                color=(45+5*k,60+5*k,30+2*k)
                d.ellipse((xx-17,cy+8,xx+17,cy+42),fill=color)
        d.ellipse((x-19,cy+6,x+19,cy+44),fill='#dcff87')
    d.text((52,1005),'Mismo movimiento.',font=font(36,True),fill='white')
    d.text((52,1055),'Distinto tiempo de exposición.',font=font(30),fill='white')
    d.text((52,1150),'Al cambiar la velocidad, revisa',font=font(25),fill='#b7bdb1')
    d.text((52,1190),'apertura, ISO y luz.',font=font(25),fill='#b7bdb1')
    return im

if __name__=='__main__':
    out=ROOT/'clips/obturacion-diagrama-v1.mp4'
    render(2).save(ROOT/'clips/obturacion-diagrama-revision.jpg')
    p=subprocess.Popen(['ffmpeg','-v','error','-nostdin','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
    for n in range(round(15.75*FPS)):p.stdin.write(render(n/FPS).tobytes())
    p.stdin.close()
    if p.wait():raise SystemExit('Falló render')
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    print(out, out.stat().st_size)
