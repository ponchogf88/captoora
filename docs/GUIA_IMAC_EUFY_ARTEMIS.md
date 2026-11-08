# 🎥 GUÍA DE OPERACIÓN EN iMAC 2015: CÁMARA EUFY S350 (ANKER) + ARTEMIS ANDROID

## 1. Arquitectura Multi-Equipo Configurada
- **iMac 2015 (`/Users/imac` · SSD Externo + HDD Interno):** Estación de procesamiento pesado, Canva, TikTok y enlace ADB directo con tu **Xiaomi Redmi Note 8 (`160305c5`)** corriendo **Artemis** y **Eufy Security**.
- **MacBook Pro (`/Users/user` · 256 GB):** Consola ligera y web (`captoora.studio`).
- **Google Drive (`RECAP_DIARIO_CAMARAS`):** Puente automático en la nube donde caen los clips crudos y los Reels 9:16 ya recortados.

---

## 2. Cómo Funciona el Extractor Automático (`eufy_artemis_extractor.py`)
1. **Conexión ADB (`160305c5`):** Busca automáticamente los clips `.mp4` grabados por tu cámara Eufy S350 en el Xiaomi Redmi Note 8 (`/sdcard/DCIM/EufySecurity`, `/sdcard/Movies/EufySecurity`, `/sdcard/Android/data/com.oceanwing.battery.cam/files` y `/sdcard/Download`).
2. **Cero Duplicados:** Registra cada clip extraído en `RECAP_DIARIO_CAMARAS/eufy_extracted_manifest.json` para no volver a descargar videos ya procesados.
3. **Detección de Acción Real (Set Setup & BTS):** Con OpenCV (`cv2.absdiff`), detecta únicamente los segundos donde **tú estás en movimiento acomodando el ciclorama, las luces Godox o el set**, ignorando las horas donde el estudio está vacío.
4. **Exportación 9:16 Vertical (1080×1920):** Guarda los Reels listos para TikTok / Instagram en:
   - `Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/RECAP_DIARIO_CAMARAS/02_REELS_LISTOS_9x16/`

---

## 3. Comando Único en tu iMac 2015
En el iMac 2015 (o pidiéndoselo a Antigravity en el iMac), solo ejecuta:

```bash
git pull origin main && python3 scripts/eufy_artemis_extractor.py --auto
```

Para verificar en cualquier momento el estado del teléfono Android y las rutas en cualquiera de las dos computadoras:

```bash
python3 scripts/eufy_artemis_extractor.py --check
```
