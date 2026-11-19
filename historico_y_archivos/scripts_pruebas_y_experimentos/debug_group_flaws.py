import cv2
import numpy as np

# Load original high-res image
orig = cv2.imread("/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/CPT_0845.JPG")
h, w, _ = orig.shape
print(f"Orig: {w}x{h}")

# Check current export
cur = cv2.imread("/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/01_Alta_Resolucion_Cliente/FARMASI_CPT_0845_GRUPAL_HQ.jpg")
print(f"Current export: {cur.shape}")
