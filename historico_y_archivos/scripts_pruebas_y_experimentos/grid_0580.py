import cv2

img = cv2.imread("/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/CPT_0580.JPG")
# Resize to 800x1200
small = cv2.resize(img, (800, 1200))
# Add grid every 100px
for x in range(0, 800, 100):
    cv2.line(small, (x, 0), (x, 1200), (0, 255, 0), 1)
    cv2.putText(small, f"{int(x*5)}", (x+5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
for y in range(0, 1200, 100):
    cv2.line(small, (0, y), (800, y), (0, 255, 0), 1)
    cv2.putText(small, f"{int(y*5)}", (10, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

cv2.imwrite("/private/tmp/farmasi_samples/grid_0580.jpg", small)
print("Saved grid 0580")
