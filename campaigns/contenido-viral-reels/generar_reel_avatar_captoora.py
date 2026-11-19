import subprocess
import os

work_dir = '/tmp/reel_build_v4'
os.makedirs(work_dir, exist_ok=True)
audio_dir = '/tmp/captoora_audio'
broll_dir = '/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO/INSPIRACION_VIDEOS_BTS'
font_impact = '/System/Library/Fonts/Supplemental/Impact.ttf'

scenes = [
    {
        "id": "scene1",
        "video": "/tmp/video_apertura_estudio.mp4",
        "ss": "00:00:00.00",
        "duration": "4.92",
        "audio": f"{audio_dir}/scene1_hook.wav",
        "texts": [
            {"text": "¿COMO?", "start": 0.0, "end": 1.6, "color": "0xFFE600", "size": 110, "y": 620},
            {"text": "NO MAS CELULAR", "start": 1.6, "end": 3.2, "color": "0xFFFFFF", "size": 86, "y": 620},
            {"text": "MARCA DE $1M", "start": 3.2, "end": 4.92, "color": "0x00FF66", "size": 94, "y": 620}
        ]
    },
    {
        "id": "scene2",
        "video": f"{broll_dir}/08 - thecollabstudio.tx - 6 studio mistakes I still see way too often… here’.mp4",
        "ss": "00:00:04.00",
        "duration": "8.15",
        "audio": f"{audio_dir}/scene2_pain.wav",
        "texts": [
            {"text": "EL ERROR N1", "start": 0.0, "end": 2.8, "color": "0xFF3333", "size": 96, "y": 620},
            {"text": "FOTOS OSCURAS", "start": 2.8, "end": 5.2, "color": "0xFFFFFF", "size": 86, "y": 620},
            {"text": "90 PIERDE VENTAS", "start": 5.2, "end": 8.15, "color": "0xFFE600", "size": 84, "y": 620}
        ]
    },
    {
        "id": "scene3",
        "video": f"{broll_dir}/02 - austinield - How I capture BTS footage during photoshoots using.mp4",
        "ss": "00:00:02.00",
        "duration": "7.64",
        "audio": f"{audio_dir}/scene3_paso1.wav",
        "texts": [
            {"text": "PASO 1", "start": 0.0, "end": 2.2, "color": "0xFFFFFF", "size": 90, "y": 560},
            {"text": "DIRECCION 1 A 1", "start": 0.0, "end": 3.8, "color": "0xFFE600", "size": 100, "y": 670},
            {"text": "TE GUIAMOS EN VIVO", "start": 3.8, "end": 7.64, "color": "0x00FF66", "size": 80, "y": 620}
        ]
    },
    {
        "id": "scene4",
        "video": f"{broll_dir}/26 - stock_vertical_4k_15984269.mp4",
        "ss": "00:00:00.50",
        "duration": "7.93",
        "audio": f"{audio_dir}/scene4_paso2.wav",
        "texts": [
            {"text": "PASO 2", "start": 0.0, "end": 2.2, "color": "0xFFFFFF", "size": 90, "y": 560},
            {"text": "LUZ COMERCIAL", "start": 0.0, "end": 3.8, "color": "0xFFE600", "size": 94, "y": 670},
            {"text": "TEXTURA REAL", "start": 3.8, "end": 7.93, "color": "0x00FF66", "size": 88, "y": 620}
        ]
    },
    {
        "id": "scene5",
        "video": f"{broll_dir}/28 - stock_vertical_4k_15200654.mp4",
        "ss": "00:00:00.00",
        "duration": "8.23",
        "audio": f"{audio_dir}/scene5_paso3.wav",
        "texts": [
            {"text": "PASO 3", "start": 0.0, "end": 2.2, "color": "0xFFFFFF", "size": 90, "y": 560},
            {"text": "ENTREGA LIMPIA", "start": 0.0, "end": 3.8, "color": "0xFFE600", "size": 94, "y": 670},
            {"text": "GALERIA PRIVADA", "start": 3.8, "end": 8.23, "color": "0x00FF66", "size": 84, "y": 620}
        ]
    },
    {
        "id": "scene6",
        "video": f"{broll_dir}/10 - essencestudio_ - Essence studio es mas que solo fotografía ✅️ Conta.mp4",
        "ss": "00:00:01.00",
        "duration": "7.51",
        "audio": f"{audio_dir}/scene6_experience.wav",
        "texts": [
            {"text": "SAN JERONIMO", "start": 0.0, "end": 3.6, "color": "0xFFFFFF", "size": 90, "y": 560},
            {"text": "MONTERREY", "start": 0.0, "end": 3.6, "color": "0xFFE600", "size": 100, "y": 670},
            {"text": "CAFE Y CERO PRISAS", "start": 3.6, "end": 7.51, "color": "0x00FF66", "size": 84, "y": 620}
        ]
    },
    {
        "id": "scene7",
        "video": "/tmp/video_apertura_estudio.mp4",
        "ss": "00:00:10.00",
        "duration": "6.65",
        "audio": f"{audio_dir}/scene7_cta.wav",
        "texts": [
            {"text": "COMENTA", "start": 0.0, "end": 6.65, "color": "0xFFFFFF", "size": 80, "y": 540},
            {"text": "ESTUDIO", "start": 0.0, "end": 6.65, "color": "0xFFE600", "size": 110, "y": 650},
            {"text": "AGENDA Y GUIA VIP", "start": 3.0, "end": 6.65, "color": "0x00FF66", "size": 76, "y": 790}
        ]
    }
]

rendered_parts = []

for idx, sc in enumerate(scenes):
    out_part = f"{work_dir}/part_{idx}.mp4"
    vf_filters = [
        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
        f"drawtext=fontfile='{font_impact}':text='CAPTOORA STUDIO':fontcolor=white@0.6:fontsize=36:x=(w-text_w)/2:y=1750"
    ]
    
    for t in sc["texts"]:
        draw = (
            f"drawtext=fontfile='{font_impact}':text='{t['text']}':"
            f"fontcolor={t['color']}:fontsize={t['size']}:"
            f"borderw=8:bordercolor=black:"
            f"box=1:boxcolor=black@0.65:boxborderw=18:"
            f"x=(w-text_w)/2:y={t['y']}:"
            f"enable='between(t,{t['start']},{t['end']})'"
        )
        vf_filters.append(draw)
        
    vf_str = ",".join(vf_filters)
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", sc["ss"],
        "-t", sc["duration"],
        "-i", sc["video"],
        "-i", sc["audio"],
        "-filter_complex", f"[0:v]{vf_str}[v];[1:a]aformat=sample_rates=44100:channel_layouts=stereo[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        out_part
    ]
    
    print(f"Rendering part {idx} ({sc['id']})...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print(f"Error {sc['id']}:", res.stderr.decode()[-500:])
        raise RuntimeError(f"Failed {sc['id']}")
    else:
        print(f"✓ Part {idx} success!")
        rendered_parts.append(out_part)

# Concat using filter_complex concat for 100% sync
filter_inputs = "".join([f"[{i}:v][{i}:a]" for i in range(len(rendered_parts))])
concat_filter = f"{filter_inputs}concat=n={len(rendered_parts)}:v=1:a=1[outv][outa]"

final_desktop_video = "/Users/imac/Desktop/VIDEO_VIRAL_01_COMO_FUNCIONA_CAPTOORA.mp4"
concat_cmd = ["ffmpeg", "-y"]
for p in rendered_parts:
    concat_cmd.extend(["-i", p])

concat_cmd.extend([
    "-filter_complex", concat_filter,
    "-map", "[outv]",
    "-map", "[outa]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k",
    final_desktop_video
])

print("Rendering final concat video...")
subprocess.run(concat_cmd, check=True)
print(f"🎉 MASTER REEL COMPLETED: {final_desktop_video}")
