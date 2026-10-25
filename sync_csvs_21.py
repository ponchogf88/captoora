import csv
import os
from PIL import Image

OUT_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/BULK_20_POSTS_RENDERED"
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"
CSV_BUFFER = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/BUFFER_AUTO_CADA_3_HORAS.csv"

with open(CSV_BUFFER, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    fnames = reader.fieldnames
    rows = list(reader)

print("Buffer fieldnames:", fnames)

# Update Post 01 and append Post 21 using actual fieldnames
for r in rows:
    if r.get(fnames[0]) == "01" or "POST_01" in str(r.values()):
        for k in r:
            if "Caption" in k or "Text" in k or "Script" in k:
                r[k] = (
                    "Para ser el dueño y amo y señor de la luz, primero tienes que dominar la oscuridad. 🌙✨🕯️\n\n"
                    "En fotografía de alto nivel, las sombras y la penumbra no son ausencia de imagen: son el lienzo donde "
                    "nace el volumen, el misterio y el carácter.\n\n"
                    "📍 Captoora Studio — Momentos que permanecen. Reserva tu sesión de temporada por DM.\n\n"
                    "#CaptooraStudio #MomentosQuePermanecen #AmoDeLaLuz #FotografiaDeAutor #Monterrey #DiaDeMuertos"
                )

# Add Post 21 if not already present
if not any("POST_21" in str(r.values()) for r in rows):
    new_row = {k: "" for k in fnames}
    for k in fnames:
        kl = k.lower()
        if "id" in kl:
            new_row[k] = "21"
        elif "cat" in kl:
            new_row[k] = "4. Campañas de Temporada"
        elif "text" in kl or "caption" in kl or "script" in kl:
            new_row[k] = (
                "Caminar sobre el Zócalo en esta temporada es pisar el altar más grande del mundo. 🇲🇽🌼💀\n\n"
                "Cuenta la leyenda —y lo confirma la arqueología del INAH— que bajo esta plancha y la Catedral Metropolitana "
                "descansan miles de guerreros caídos en el asedio de 1521, el antiguo cementerio virreinal y las torres de cráneos "
                "del Huei Tzompantli de Tenochtitlan.\n\n"
                "Cuando el cielo se cierra, el asfalto mojado refleja la historia y el cempasúchil enciende la piedra, "
                "la cámara deja de tomar simples fotos: desentierra memoria.\n\n"
                "Para ser el dueño, amo y señor de la luz, primero tienes que saber leer la atmósfera.\n\n"
                "📍 Sesiones Editoriales y Documentales de Temporada — Agenda abierta por DM.\n\n"
                "#CaptooraStudio #DiaDeMuertos #ZocaloCDMX #FotografiaEditorial #Tenochtitlan #HueiTzompantli #MexicoMagico #AmoDeLaLuz"
            )
        elif "img" in kl or "path" in kl or "media" in kl or "archivo" in kl:
            new_row[k] = os.path.join(OUT_DIR, "POST_21_TEMPORADA_ZOCALO_TUMBA_GUERREROS.jpg")
        elif "date" in kl or "sched" in kl or "hora" in kl or "fecha" in kl:
            new_row[k] = "2026-10-18 06:00"
    rows.append(new_row)

with open(CSV_BUFFER, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ {len(rows)} posts sincronizados en BUFFER_AUTO_CADA_3_HORAS.csv")
