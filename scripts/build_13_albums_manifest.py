#!/usr/bin/env python3
"""
CAPTOORA STUDIO — Generador del Manifiesto Oficial de los 13 Álbumes de Portafolio Autorizado
Sincroniza data/portafolio_13_albumes.json y organiza la carpeta PORTAFOLIO_AUTORIZADO_13_ALBUMES en Google Drive.
"""
import json
import shutil
from pathlib import Path
import captoora_paths as cp

ALBUMS = [
    {
        "id": "album-01",
        "number": "01",
        "slug": "01_Sesion_2025_Personal_Branding",
        "title": "Sesión 2025 · Personal Branding",
        "category": "editorial",
        "category_label": "Editorial & Branding",
        "location": "Monterrey, N.L.",
        "gear": "Nikon Z · 50mm f/1.2 · Luz Dorada",
        "cover": "assets/media_jpg/pf-poncho25-01.jpg",
        "photos": [
            "assets/media_jpg/pf-poncho25-01.jpg",
            "assets/media_jpg/pf-poncho25-02.jpg",
            "assets/media_jpg/pf-1946.jpg",
            "assets/media_jpg/pf-1957.jpg",
        ],
    },
    {
        "id": "album-02",
        "number": "02",
        "slug": "02_Peloni_9_Anos_Gala",
        "title": "Peloni · 9 Años Gala",
        "category": "familia",
        "category_label": "Familia & Niños",
        "location": "Monterrey, N.L.",
        "gear": "Óptica Fija · Retrato Cándido",
        "cover": "assets/media_jpg/pf-peloni-01.jpg",
        "photos": [
            "assets/media_jpg/pf-peloni-01.jpg",
            "assets/media_jpg/pf-peloni-02.jpg",
            "assets/media_jpg/pf-peloni-03.jpg",
        ],
    },
    {
        "id": "album-03",
        "number": "03",
        "slug": "03_Parque_Rufino_Tamayo",
        "title": "Parque Rufino Tamayo · Exterior",
        "category": "exteriores",
        "category_label": "Exteriores & Bosque",
        "location": "San Pedro Garza García, N.L.",
        "gear": "Luz Natural de Tarde · 24MP",
        "cover": "assets/media_jpg/pf-tamayo-01.jpg",
        "photos": [
            "assets/media_jpg/pf-tamayo-01.jpg",
            "assets/media_jpg/pf-tamayo-02.jpg",
            "assets/media_jpg/pf-tamayo-03.jpg",
        ],
    },
    {
        "id": "album-04",
        "number": "04",
        "slug": "04_Mama_65_Celebracion",
        "title": "Mamá 65 · Celebración Familiar",
        "category": "eventos",
        "category_label": "Eventos & Celebraciones",
        "location": "Monterrey, N.L.",
        "gear": "Cobertura Documental & Retrato",
        "cover": "assets/media_jpg/pf-mama65-01.jpg",
        "photos": [
            "assets/media_jpg/pf-mama65-01.jpg",
            "assets/media_jpg/pf-mama65-02.jpg",
        ],
    },
    {
        "id": "album-05",
        "number": "05",
        "slug": "05_Peloni_7_Infantil",
        "title": "Peloni 7 · Retrato Infantil",
        "category": "familia",
        "category_label": "Familia & Niños",
        "location": "Monterrey, N.L.",
        "gear": "Retrato Espontáneo · Luz Suave",
        "cover": "assets/media_jpg/pf-0032.jpg",
        "photos": [
            "assets/media_jpg/pf-0032.jpg",
            "assets/media_jpg/pf-0041.jpg",
        ],
    },
    {
        "id": "album-06",
        "number": "06",
        "slug": "06_Princis_33_Estudio",
        "title": "Princis 33 · Ciclorama Estudio",
        "category": "estudio",
        "category_label": "Estudio & Ciclorama",
        "location": "Captoora Studio · San Jerónimo",
        "gear": "Iluminación Godox · High-Key",
        "cover": "assets/media_jpg/pf-princis-01.jpg",
        "photos": [
            "assets/media_jpg/pf-princis-01.jpg",
            "assets/media_jpg/pf-w0818.jpg",
            "assets/media_jpg/pf-w0828.jpg",
            "assets/media_jpg/pf-w0842.jpg",
        ],
    },
    {
        "id": "album-07",
        "number": "07",
        "slug": "07_Barbie_Lulu_Editorial",
        "title": "Barbie Lulú · Set Editorial",
        "category": "estudio",
        "category_label": "Estudio & Ciclorama",
        "location": "Captoora Studio · San Jerónimo",
        "gear": "Set Temático · Dirección de Pose",
        "cover": "assets/media_jpg/pf-barbie-01.jpg",
        "photos": [
            "assets/media_jpg/pf-barbie-01.jpg",
            "assets/media_jpg/pf-barbie-02.jpg",
            "assets/media_jpg/pf-barbie-03.jpg",
        ],
    },
    {
        "id": "album-08",
        "number": "08",
        "slug": "08_Peloni_Retrato_Clasico",
        "title": "Peloni · Retrato Clásico",
        "category": "familia",
        "category_label": "Familia & Niños",
        "location": "Monterrey, N.L.",
        "gear": "Óptica de Retrato · Piel Real",
        "cover": "assets/media_jpg/pf-0867.jpg",
        "photos": [
            "assets/media_jpg/pf-0867.jpg",
            "assets/media_jpg/pf-0912.jpg",
        ],
    },
    {
        "id": "album-09",
        "number": "09",
        "slug": "09_Mama_64_Conmemorativo",
        "title": "Mamá 64 · Retrato Conmemorativo",
        "category": "eventos",
        "category_label": "Eventos & Celebraciones",
        "location": "Monterrey, N.L.",
        "gear": "Iluminación Cálida · Retrato Familiar",
        "cover": "assets/media_jpg/pf-1027.jpg",
        "photos": [
            "assets/media_jpg/pf-1027.jpg",
            "assets/media_jpg/pf-1042.jpg",
            "assets/media_jpg/pf-1062.jpg",
        ],
    },
    {
        "id": "album-10",
        "number": "10",
        "slug": "10_Abuela_Legado_Familiar",
        "title": "Abuela · Legado & Familia",
        "category": "familia",
        "category_label": "Familia & Niños",
        "location": "Monterrey, N.L.",
        "gear": "Retrato Emotivo · Luz Natural",
        "cover": "assets/media_jpg/pf-abuela-01.jpg",
        "photos": [
            "assets/media_jpg/pf-abuela-01.jpg",
        ],
    },
    {
        "id": "album-11",
        "number": "11",
        "slug": "11_Sierra_de_Chipinque",
        "title": "Sierra de Chipinque · Bosque & Familia",
        "category": "exteriores",
        "category_label": "Exteriores & Bosque",
        "location": "Parque Ecológico Chipinque, N.L.",
        "gear": "Full 4K · Luz de Bosque",
        "cover": "assets/media_jpg/pf-chipinque-01.jpg",
        "photos": [
            "assets/media_jpg/pf-chipinque-01.jpg",
            "assets/media_jpg/pf-chipinque-02.jpg",
            "assets/media_jpg/pf-chipinque-fam.jpg",
        ],
    },
    {
        "id": "album-12",
        "number": "12",
        "slug": "12_Editorial_y_Viajes_Villarreal_Cuba_Texas",
        "title": "Editorial & Viajes · Villarreal, GIO, Cuba & Texas",
        "category": "editorial",
        "category_label": "Editorial & Branding",
        "location": "Monterrey · La Habana · Texas",
        "gear": "24MP Réflex · Street & Fashion",
        "cover": "assets/media_jpg/pf-villarreal-01.jpg",
        "photos": [
            "assets/media_jpg/pf-villarreal-01.jpg",
            "assets/media_jpg/pf-villarreal-02.jpg",
            "assets/media_jpg/pf-gio-01.jpg",
            "assets/media_jpg/pf-cuba-01.jpg",
            "assets/media_jpg/pf-texas-01.jpg",
            "assets/media_jpg/pf-texas-02.jpg",
        ],
    },
    {
        "id": "album-13",
        "number": "13",
        "slug": "13_Farmasi_y_GlowTours_Studio_Pro",
        "title": "Farmasi & GlowTours · Studio Pro",
        "category": "estudio",
        "category_label": "Estudio & Ciclorama",
        "location": "Captoora Studio · San Jerónimo 11",
        "gear": "Ciclorama Blanco Puro & Set Amapola",
        "cover": "assets/media_jpg/FARMASI_CPT_0554_BRENDA_ESTUDIO_PRO.jpg",
        "photos": [
            "assets/media_jpg/FARMASI_CPT_0554_BRENDA_ESTUDIO_PRO.jpg",
            "assets/media_jpg/FARMASI_CPT_0558_BRENDA_ESTUDIO_PRO.jpg",
            "assets/media_jpg/FARMASI_CPT_0724_LULU_ESTUDIO_PRO.jpg",
            "assets/media_jpg/FARMASI_CPT_0728_LULU_ESTUDIO_PRO.jpg",
            "assets/media_jpg/FARMASI_CPT_0735_LULU_ESTUDIO_PRO.jpg",
            "assets/media_jpg/FARMASI_CPT_0741_LULU_ESTUDIO_PRO.jpg",
            "assets/media_jpg/FARMASI_CPT_0745_LULU_ESTUDIO_PRO.jpg",
            "assets/media_jpg/FARMASI_CPT_0750_LULU_ESTUDIO_PRO.jpg",
            "assets/media_jpg/FARMASI_CPT_0766_LULU_ESTUDIO_PRO.jpg",
            "assets/media_jpg/FARMASI_CPT_0845_GRUPAL_4x5.jpg",
            "assets/media_jpg/pf-glow-cpt_0853.jpg",
            "assets/media_jpg/pf-glow-cpt_0855.jpg",
            "assets/media_jpg/pf-glow-cpt_0863.jpg",
            "assets/media_jpg/pf-glow-cpt_0878.jpg",
        ],
    },
]


def main():
    cp.REPO_DATA.mkdir(parents=True, exist_ok=True)
    cp.DRIVE_PORTAFOLIO_AUTORIZADO_13.mkdir(parents=True, exist_ok=True)

    manifest = {
        "domain": "https://captoora.studio",
        "updated_at": "2026-11-07",
        "total_albums": len(ALBUMS),
        "total_curated_photos": sum(len(a["photos"]) for a in ALBUMS),
        "categories": [
            {"id": "all", "label": "Todos los Álbumes (13)"},
            {"id": "estudio", "label": "Estudio & Ciclorama"},
            {"id": "editorial", "label": "Editorial & Viajes"},
            {"id": "familia", "label": "Familia & Niños"},
            {"id": "exteriores", "label": "Exteriores & Bosque"},
            {"id": "eventos", "label": "Eventos & Celebraciones"},
        ],
        "albums": ALBUMS,
    }

    cp.REPO_PORTAFOLIO_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for alb in ALBUMS:
        alb_dir = cp.DRIVE_PORTAFOLIO_AUTORIZADO_13 / alb["slug"]
        alb_dir.mkdir(parents=True, exist_ok=True)
        for rel_p in alb["photos"]:
            src_p = cp.REPO_ROOT / rel_p
            if src_p.exists():
                shutil.copy2(src_p, alb_dir / src_p.name)

    shutil.copy2(cp.REPO_PORTAFOLIO_JSON, cp.DRIVE_PORTAFOLIO_AUTORIZADO_13 / "portafolio_13_albumes.json")

    md_lines = [
        "# 📸 PORTAFOLIO AUTORIZADO CAPTOORA STUDIO — 13 ÁLBUMES OFICIALES",
        "",
        "- **Dominio Web:** `https://captoora.studio`",
        f"- **Total de Álbumes:** {manifest['total_albums']}",
        f"- **Total de Fotografías Curadas:** {manifest['total_curated_photos']}",
        "",
        "| # | Carpeta / Álbum | Categoría | Fotos Curadas | Portada |",
        "| :---: | :--- | :--- | :---: | :--- |",
    ]
    for a in ALBUMS:
        cover_name = Path(a["cover"]).name
        md_lines.append(f"| **{a['number']}** | `{a['slug']}` | {a['category_label']} | {len(a['photos'])} | `{cover_name}` |")

    (cp.DRIVE_PORTAFOLIO_AUTORIZADO_13 / "INDICE_13_ALBUMES.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"[OK] 13 álbumes creados con {manifest['total_curated_photos']} fotos en {cp.REPO_PORTAFOLIO_JSON} y Google Drive.")


if __name__ == "__main__":
    main()
