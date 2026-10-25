import cv2
import numpy as np

img = cv2.imread("/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/CPT_0845.JPG")
# Crop right side: x from 4000 to 6000, y from 0 to 4000
right_crop = img[:, 4000:]
h, w, _ = right_crop.shape

# Save with grid
grid = cv2.resize(right_crop, (1000, 2000))
for x in range(0, 1000, 100):
    cv2.line(grid, (x, 0), (x, 2000), (0, 255, 0), 1)
    cv2.putText(grid, f"{4000 + x*2}", (x+5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
for y in range(0, 2000, 100):
    cv2.line(grid, (0, y), (1000, y), (0, 255, 0), 1)
    cv2.putText(grid, f"{y*2}", (10, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

cv2.imwrite("/private/tmp/farmasi_samples/right_side_grid.jpg", grid)
print("Saved right side grid")
