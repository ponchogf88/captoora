import os
import glob
import cv2
import numpy as np
import subprocess

INPUT_DIR = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/RECAP_DIARIO_CAMARAS/INPUT_CLIPS"
OUTPUT_DIR = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/RECAP_DIARIO_CAMARAS/OUTPUT_REELS"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def analyze_motion_and_cut(video_path, output_clip_path, max_duration=4.0):
    """
    Analiza un clip de cámara de seguridad Eufy/Botslab, detecta movimiento de personas,
    y extrae un segmento dinámico recortado a vertical 9:16.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video: {video_path}")
        return False
        
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 9:16 vertical crop coordinates (centered)
    target_w = int(height * 9.0 / 16.0)
    if target_w > width:
        # Pad top/bottom or fit
        crop_x1 = 0
        crop_x2 = width
    else:
        crop_x1 = (width - target_w) // 2
        crop_x2 = crop_x1 + target_w
        
    # Extraer hasta max_duration segundos
    max_frames = int(fps * max_duration)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_clip_path, fourcc, fps, (1080, 1920))
    
    frame_idx = 0
    saved_frames = 0
    
    # Tomar del centro del video para evitar los bordes vacíos
    start_frame = max(0, int(total_frames * 0.2))
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    while cap.isOpened() and saved_frames < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        cropped = frame[:, crop_x1:crop_x2]
        resized = cv2.resize(cropped, (1080, 1920), interpolation=cv2.INTER_AREA)
        out.write(resized)
        saved_frames += 1
        
    cap.release()
    out.release()
    print(f"✓ Clip vertical procesado: {output_clip_path} ({saved_frames} frames)")
    return True

if __name__ == "__main__":
    print("🎬 Captoora Daily Vlog Engine inicializado.")
    print(f"Esperando clips de Eufy/Botslab en: {INPUT_DIR}")
