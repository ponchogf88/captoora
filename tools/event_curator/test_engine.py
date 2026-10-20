#!/usr/bin/env python3
"""
Test script for curator_engine on 3 representative images.
"""
import os
import json
from curator_engine import generate_preview_and_metrics, export_curated_batch, PRESETS, apply_color_grading, load_image_normalized
import cv2

TEST_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/dev_event_curator/test_samples"
CACHE_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/dev_event_curator/cache_test"
OUT_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/dev_event_curator/test_output"

images = sorted([os.path.join(TEST_DIR, f) for f in os.listdir(TEST_DIR) if f.upper().endswith(('.JPG', '.JPEG', '.PNG'))])
print(f"Encontradas {len(images)} imágenes de prueba: {images}")

results = []
for img_path in images:
    info = generate_preview_and_metrics(img_path, CACHE_DIR, PRESETS["transicion_equilibrada"])
    results.append(info)
    print(f"\n--- {info['filename']} ---")
    print(f"Nitidez: {info['sharpness']['score']} ({info['sharpness']['label']})")
    print(f"Exposición: {info['exposure']['label']} (Media={info['exposure']['mean']}, Sombras={info['exposure']['shadows_percent']}%, Luces={info['exposure']['highlights_percent']}%)")
    print(f"Rostros / Ojos: {info['eyes']['label']} (Rostros={info['eyes']['faces_detected']})")
    print(f"dHash: {info['dhash']}")

# Probar exportación asignando decisiones de prueba
results[0]["decision"] = "yes"
results[1]["decision"] = "review"
results[2]["decision"] = "yes"

report = export_curated_batch(results, OUT_DIR, PRESETS["transicion_equilibrada"], client_tag="GLOWTTERY")
print("\nExportación completada:")
print(json.dumps(report, indent=2, ensure_ascii=False))

# Generar comparativas visuales side-by-side de las 3 imágenes
side_by_side_dir = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/dev_event_curator/test_comparisons"
os.makedirs(side_by_side_dir, exist_ok=True)

for item in results:
    f_raw = item["raw_thumb"]
    f_graded = item["graded_thumb"]
    raw_img = cv2.imread(f_raw)
    graded_img = cv2.imread(f_graded)
    
    # Concatenar horizontalmente
    h, w, _ = raw_img.shape
    # Añadir barra divisoria o etiquetas
    combined = cv2.hconcat([raw_img, graded_img])
    out_cmp = os.path.join(side_by_side_dir, f"COMPARATIVA_{item['filename']}")
    cv2.imwrite(out_cmp, combined, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(f"Guardada comparativa visual: {out_cmp}")
