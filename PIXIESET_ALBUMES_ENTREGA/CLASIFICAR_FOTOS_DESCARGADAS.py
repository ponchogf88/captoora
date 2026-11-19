# -*- coding: utf-8 -*-
"""
Clasificador Automático Pre-Boom Instagram (8:00 - 10:00 PM) para Pixieset
Separa automáticamente cualquier carpeta o archivo .ZIP descargado de Google Drive en:
1. 01_MODELOS_INDIVIDUALES:
   - VIP / Influencers + Evelyn -> 01_ENTREGA_VIP_COMPLETA (Todas sus fotos listas)
   - Colaboración Estándar -> 01_ENTREGA_COLABORACION_MAX_5_FOTOS (Máximo 5 fotos)
     + 02_EXTRAS_CON_MARCA_AGUA_SOLO_SI_COMPRAN (El resto ya editadas guardadas aparte)
2. 02_ALBUMES_GRUPALES:
   - Separadas en sus 3 bloques grupales listas para subir a Pixieset.
"""
import json
import pathlib
import re
import shutil
import sys
import zipfile

BASE_DIR = pathlib.Path(__file__).resolve().parent
CATALOG_FILE = BASE_DIR / "CATALOGO_MAESTRO_PIXIESET.json"

SEARCH_DIRS = [
    pathlib.Path.home() / "Downloads",
    pathlib.Path.home() / "OneDrive" / "Escritorio",
    pathlib.Path.home() / "Desktop",
    BASE_DIR / "ENTRADA_DESCARGAS_DRIVE",
]


def extract_dsc_code(filename: str) -> str:
    m = re.search(r"(DSC\d{5}(?:\s+2)?)", filename, re.IGNORECASE)
    return m.group(1).upper() if m else ""


def main():
    if len(sys.argv) > 1:
        custom_dir = pathlib.Path(sys.argv[1])
        if custom_dir.exists():
            SEARCH_DIRS.insert(0, custom_dir)

    (BASE_DIR / "ENTRADA_DESCARGAS_DRIVE").mkdir(parents=True, exist_ok=True)
    catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))

    dsc_map = {}
    for alb in catalog["albums"]:
        tipo = alb["tipo"]
        folder_id = alb["id"]
        is_vip = alb.get("is_vip", False)
        if tipo == "Individual":
            alb_dir = BASE_DIR / "01_MODELOS_INDIVIDUALES" / folder_id
            sub_main = "01_ENTREGA_VIP_COMPLETA" if is_vip else "01_ENTREGA_COLABORACION_MAX_5_FOTOS"
            sub_extra = "02_EXTRAS_CON_MARCA_AGUA_SOLO_SI_COMPRAN"
        else:
            alb_dir = BASE_DIR / "02_ALBUMES_GRUPALES" / folder_id
            sub_main = "01_Grupales_Aprobadas_Pixieset"
            sub_extra = "01_Grupales_Aprobadas_Pixieset"

        for p in alb["photos"]:
            code = p["source_name"].replace(".JPG", "").upper()
            dst_folder = alb_dir / (sub_main if p.get("is_included_collab", True) else sub_extra)
            dsc_map.setdefault(code, []).append(dst_folder / p["file_name"])

    found_count = 0
    copied_files = 0

    print("=== BUSCANDO FOTOS O ZIPS DE GOOGLE DRIVE EN DESCARGAS / ESCRITORIO ===")
    for sdir in SEARCH_DIRS:
        if not sdir.exists():
            continue
        for img_path in sdir.rglob("*"):
            if not img_path.is_file():
                continue
            if BASE_DIR in img_path.parents and img_path.parent.name != "ENTRADA_DESCARGAS_DRIVE":
                continue
            ext = img_path.suffix.lower()
            if ext in (".jpg", ".jpeg", ".png"):
                code = extract_dsc_code(img_path.name)
                if code and code in dsc_map:
                    found_count += 1
                    for dst in dsc_map[code]:
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(img_path, dst)
                        copied_files += 1
            elif ext == ".zip":
                try:
                    with zipfile.ZipFile(img_path, "r") as zf:
                        for member in zf.namelist():
                            if member.lower().endswith((".jpg", ".jpeg", ".png")):
                                code = extract_dsc_code(member)
                                if code and code in dsc_map:
                                    data = zf.read(member)
                                    found_count += 1
                                    for dst in dsc_map[code]:
                                        dst.parent.mkdir(parents=True, exist_ok=True)
                                        dst.write_bytes(data)
                                        copied_files += 1
                except Exception:
                    pass

    print(f"Resultado: {found_count} fotos identificadas -> {copied_files} archivos clasificados en carpetas Pixieset.")
    if found_count == 0:
        print("\nPASO RAPIDO: Descarga la carpeta 'Aprobadas' de Google Drive (se baja como .zip en Descargas)")
        print("y haz doble clic en CLASIFICAR_FOTOS_PIXIESET.bat. Se separaran solas en segundos.")


if __name__ == "__main__":
    main()
