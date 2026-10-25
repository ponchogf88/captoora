import cv2
import numpy as np

img = cv2.imread("/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/CPT_0845.JPG")
h, w, _ = img.shape
print(f"Loaded image: {w}x{h}")

# In original 6000x4000:
# Left door is at x < 900 (at top), x < 600 (at bottom)
# White sheet spans from x ~ 800 to x ~ 4600
# Right yellow wall starts at x > 4400 (top), lamp is around x=4800, y=800-2400
# Model 4 (far right girl) has arm/back at x ~ 4300, leg at x ~ 5300
# Model 1 (redhead, top left) has jar at x ~ 1250, y ~ 850
# Model 2 (sitting left) has leg extending to x ~ 150 at y ~ 3200
# Products on floor span from x ~ 700 to x ~ 4700, y ~ 2900 to 3950

# Let's save a downsampled grid preview with coordinates overlaid to verify
small = cv2.resize(img, (1200, 800))
# Overlay grid lines every 100px (equivalent to 500px in full res)
grid = small.copy()
for x in range(0, 1200, 100):
    cv2.line(grid, (x, 0), (x, 800), (0, 255, 0), 1)
    cv2.putText(grid, f"{x*5}", (x+5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
for y in range(0, 800, 100):
    cv2.line(grid, (0, y), (1200, y), (0, 255, 0), 1)
    cv2.putText(grid, f"{y*5}", (10, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

cv2.imwrite("/private/tmp/farmasi_samples/group_grid_landmarks.jpg", grid)
print("Grid saved to /private/tmp/farmasi_samples/group_grid_landmarks.jpg")
