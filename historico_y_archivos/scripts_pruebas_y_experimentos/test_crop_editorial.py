import cv2
from PIL import Image

img = cv2.imread("/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/01_Alta_Resolucion_Cliente/FARMASI_CPT_0845_GRUPAL_HQ.jpg")
h, w, _ = img.shape
print(f"Current shape: {w}x{h}")

# In cropped coordinates:
# Left girl ends around x = 400
# Right girl's knee ends around x = 4600
# Let us crop cleanly so there is zero remnant of power strip or foot clutter!
crop = img[:, 350:4750]
cv2.imwrite("/private/tmp/farmasi_samples/group_editorial_clean_test.jpg", crop)
print("Saved /private/tmp/farmasi_samples/group_editorial_clean_test.jpg")
