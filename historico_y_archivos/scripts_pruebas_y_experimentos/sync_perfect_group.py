from PIL import Image
import os

src = Image.open("/private/tmp/farmasi_samples/group_flaws_fixed_v4.jpg")
w, h = src.size

# 1. HQ
hq_loc = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/01_Alta_Resolucion_Cliente/FARMASI_CPT_0845_GRUPAL_HQ.jpg"
hq_icloud = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Captoora/ENTREGA_FARMASI_TERE_10_OCT/01_Alta_Resolucion_Cliente/FARMASI_CPT_0845_GRUPAL_HQ.jpg")
src.save(hq_loc, quality=96)
src.save(hq_icloud, quality=96)
print("Updated HQ in Local and iCloud")

# 2. 4x5
target_w, target_h = 1080, 1350
scale = target_w / float(w)
new_w, new_h = target_w, int(h * scale)
resized_4x5 = src.resize((new_w, new_h), Image.Resampling.LANCZOS)
canvas_4x5 = Image.new("RGB", (target_w, target_h), (245, 245, 245))
canvas_4x5.paste(resized_4x5, (0, (target_h - new_h) // 2))

loc_4x5 = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/02_Redes_Instagram_4x5/FARMASI_CPT_0845_GRUPAL_4x5.jpg"
icloud_4x5 = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Captoora/ENTREGA_FARMASI_TERE_10_OCT/02_Redes_Instagram_4x5/FARMASI_CPT_0845_GRUPAL_4x5.jpg")
canvas_4x5.save(loc_4x5, quality=95)
canvas_4x5.save(icloud_4x5, quality=95)
print("Updated 4x5 in Local and iCloud")

# 3. 9x16
target_sw, target_sh = 1080, 1920
scale_s = target_sw / float(w)
new_sw, new_sh = target_sw, int(h * scale_s)
resized_9x16 = src.resize((new_sw, new_sh), Image.Resampling.LANCZOS)
canvas_9x16 = Image.new("RGB", (target_sw, target_sh), (242, 242, 242))
canvas_9x16.paste(resized_9x16, (0, (target_sh - new_sh) // 2))

loc_9x16 = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/03_Stories_Reels_9x16/FARMASI_CPT_0845_GRUPAL_9x16.jpg"
icloud_9x16 = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Captoora/ENTREGA_FARMASI_TERE_10_OCT/03_Stories_Reels_9x16/FARMASI_CPT_0845_GRUPAL_9x16.jpg")
canvas_9x16.save(loc_9x16, quality=95)
canvas_9x16.save(icloud_9x16, quality=95)
print("Updated 9x16 in Local and iCloud")
