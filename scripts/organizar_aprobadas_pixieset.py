# -*- coding: utf-8 -*-
"""
Organizador Maestro Pre-Boom Instagram (8:00 - 10:00 PM) para Pixieset (galeria.captoora.studio)
1. Separa Modelos Individuales (11 álbumes) de Grupales (3 álbumes).
2. Aplica la regla de negocio de entrega inmediata:
   - VIP / Influencers + Evelyn: Reciben TODAS sus fotos listas (>5 fotos).
   - Modelos de Colaboración Estándar: Reciben MÁXIMO 5 FOTOS incluidas en la colaboración
     (las demás fotos ya editadas se apartan en 02_RESERVA_EXTRAS_SI_PIDEN_MAS para no regalarlas).
3. Usa los nombres exactos reales de Google Drive desde CONSERVAR.json y drive_verificado.json.
"""
import csv
import json
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
FARMASI_DIR = ROOT / "proyectos" / "farmasi-799"
OUT_DIR = ROOT / "PIXIESET_ALBUMES_ENTREGA"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_")
    return text


def extract_drive_id(url: str) -> str:
    if not url:
        return ""
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    return m.group(1) if m else ""


def main():
    dash_html = (FARMASI_DIR / "DASHBOARD_FARMASI_799.html").read_text(encoding="utf-8")
    m = re.search(r"const data = (\{.*?\});", dash_html)
    dash_data = json.loads(m.group(1))

    artefactos = json.loads((FARMASI_DIR / "registros" / "artefactos.json").read_text(encoding="utf-8"))
    art_by_source = {a.get("source_name"): a for a in artefactos}

    # Exact filenames from CONSERVAR.json (aprobadas folder 1O70rKDMLZfC9d_eY-0Ugh7MAl-iZuw11)
    conservar_path = FARMASI_DIR / "historial" / "depuracion_ultima_aprobada_2026-11-04" / "CONSERVAR.json"
    conservar_by_src = {}
    if conservar_path.exists():
        for c in json.loads(conservar_path.read_text(encoding="utf-8")):
            if c.get("kind") == "jpg" and c.get("source"):
                conservar_by_src[c["source"] + ".JPG"] = c

    # Exact filenames from drive_verificado.json (review_modelo_D, review_cobrizo_sola, review_blancos_v03)
    dv = json.loads((FARMASI_DIR / "registros" / "drive_verificado.json").read_text(encoding="utf-8"))
    rev_by_src = {}
    for key in ("review_modelo_D", "review_cobrizo_sola", "review_blancos_v03"):
        block = dv.get(key, {})
        results = block.get("results", []) if isinstance(block, dict) else []
        for r in results:
            title = r.get("title", "")
            if title.lower().endswith(".jpg"):
                m_dsc = re.match(r"(DSC\d{5}(?:\s+2)?)", title, re.I)
                if m_dsc:
                    rev_by_src[m_dsc.group(1).upper() + ".JPG"] = r

    items = dash_data["items"]
    enriched_items = []

    for item in items:
        src_name = item["name"]
        estado = item["estado"]
        en_d29 = item.get("en_lote_d29", False)
        reemplazo_d = item.get("reemplazo_d", False)

        if estado not in ("aprobada", "en_revision") and not en_d29:
            continue

        art = art_by_source.get(src_name, {})
        cons = conservar_by_src.get(src_name, {})
        rev = rev_by_src.get(src_name, {})

        approved_url = item.get("approved_url") or cons.get("url") or art.get("drive_url") or ""
        review_url = rev.get("url") or item.get("review_url") or ""
        source_url = item.get("source_url") or ""

        active_url = approved_url if approved_url else review_url
        drive_id = extract_drive_id(active_url) or cons.get("id") or rev.get("id") or art.get("drive_id", "")
        source_id = extract_drive_id(source_url)
        review_id = extract_drive_id(review_url)

        file_name = rev.get("title") if (estado == "en_revision" and rev.get("title")) else (
            cons.get("title") or art.get("file_name") or src_name.replace(".JPG", "_aprobada.jpg")
        )
        size_bytes = int(cons.get("size") or rev.get("size") or art.get("bytes") or art.get("cloud_bytes") or 0)
        sha256 = art.get("sha256") or ""

        enriched_items.append({
            "source_name": src_name,
            "file_name": file_name,
            "cluster": item["cluster"],
            "tipo": item["tipo"],
            "estado": estado,
            "version": item.get("version", ""),
            "en_lote_d29": en_d29,
            "reemplazo_d": reemplazo_d,
            "drive_id": drive_id,
            "review_id": review_id,
            "source_id": source_id,
            "approved_url": approved_url,
            "review_url": review_url,
            "source_url": source_url,
            "thumb_url": f"https://drive.google.com/thumbnail?id={drive_id or review_id or source_id}&sz=w800",
            "download_url": f"https://drive.google.com/uc?export=download&id={drive_id or review_id}",
            "size_mb": round(size_bytes / (1024 * 1024), 2) if size_bytes else 0,
            "sha256": sha256,
        })

    individual_albums = {}
    group_albums = {}
    for it in enriched_items:
        if it["tipo"] == "Individual":
            individual_albums.setdefault(it["cluster"], []).append(it)
        else:
            group_albums.setdefault(it["cluster"], []).append(it)

    # VIP Albums (Evelyn + 3 Influencers receive MORE than 5 photos; Standard Models receive MAX 5 photos)
    vip_clusters = {
        "Modelo Lila (Cabello Negro Largo · D)": "VIP · Evelyn / Modelo Principal Lila (Entrega Completa)",
        "Modelo Vestido Cobrizo (Individual · Sola 6)": "VIP · Modelo Principal Vestido Cobrizo (Entrega Completa)",
        "Madre + Bebé": "VIP · Influencer 1 · Montse 'La China' + Bebé (Entrega Completa)",
        "Piloto Inicial (Set Negro)": "VIP · Influencer 2 · Set Negro Editorial (Entrega Completa)",
        "Modelo Outfit Negro / Tatuaje (Lote 12)": "VIP · Influencer 3 · Outfit Negro Editorial (Entrega Completa)",
    }

    ind_order = [
        "Modelo Lila (Cabello Negro Largo · D)",
        "Modelo Vestido Cobrizo (Individual · Sola 6)",
        "Madre + Bebé",
        "Piloto Inicial (Set Negro)",
        "Modelo Outfit Negro / Tatuaje (Lote 12)",
        "Modelo Socia Lote 13",
        "Modelo Socia Lote 09",
        "Modelo Socia Lote 07",
        "Modelo Rizos (Blusa Blanca)",
        "Modelo Sonrisa Radiante (Lote 05)",
        "Tomas Complementarias / Cobertura",
    ]
    grp_order = [
        "Grupales Equipo Farmasi (Bloque 1)",
        "Grupales con Modelo Cobrizo / Equipo (D)",
        "Grupales y Dinámicas (Bloque 2)",
    ]

    ind_base = OUT_DIR / "01_MODELOS_INDIVIDUALES"
    grp_base = OUT_DIR / "02_ALBUMES_GRUPALES"
    ind_base.mkdir(parents=True, exist_ok=True)
    grp_base.mkdir(parents=True, exist_ok=True)

    summary_albums = []

    for idx, cluster_name in enumerate(ind_order, start=1):
        photos = individual_albums.get(cluster_name, [])
        if not photos:
            continue
        photos.sort(key=lambda x: (0 if x["estado"] == "aprobada" else 1, x["source_name"]))
        is_vip = cluster_name in vip_clusters
        tier_label = vip_clusters.get(cluster_name, "Colaboración Estándar · Máximo 5 Fotos Incluidas")
        max_included = len(photos) if is_vip else 5

        folder_slug = f"{idx:02d}_{'VIP_' if is_vip else 'MAX5_'}{slugify(cluster_name)}"
        album_dir = ind_base / folder_slug
        entrega_dir = album_dir / ("01_ENTREGA_VIP_COMPLETA" if is_vip else "01_ENTREGA_COLABORACION_MAX_5_FOTOS")
        reserva_dir = album_dir / "02_EXTRAS_CON_MARCA_AGUA_SOLO_SI_COMPRAN"
        entrega_dir.mkdir(parents=True, exist_ok=True)
        reserva_dir.mkdir(parents=True, exist_ok=True)

        aprobadas_list = [p for p in photos if p["estado"] == "aprobada"]
        revision_list = [p for p in photos if p["estado"] != "aprobada"]

        for p_i, p in enumerate(photos):
            p["album_folder"] = folder_slug
            p["album_index"] = idx
            p["is_included_collab"] = True if is_vip else (p_i < 5)
            p["is_gift_5"] = p["is_included_collab"]
            p["pixieset_set"] = "Set 1 · Retratos Individuales"

        csv_path = album_dir / "LISTA_ARCHIVOS_PIXIESET.csv"
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Orden", "Incluida_En_Entrega_Hoy", "Archivo_Aprobadas_Drive", "Codigo_Original",
                "Estado", "Carpeta_Local", "Tamano_MB", "Drive_File_ID",
                "URL_Vista_Drive", "URL_Descarga_Directa"
            ])
            for p_i, p in enumerate(photos, start=1):
                inc = "SI_ENTREGAR_HOY" if p["is_included_collab"] else "RESERVA_SI_COMPRA"
                subf = entrega_dir.name if p["is_included_collab"] else reserva_dir.name
                writer.writerow([
                    p_i, inc, p["file_name"], p["source_name"], p["estado"].upper(),
                    subf, p["size_mb"], p["drive_id"],
                    p["approved_url"] or p["review_url"], p["download_url"]
                ])

        pin_code = f"{3100 + idx * 17}"
        short_name = cluster_name.split("(")[0].strip()
        collection_title = f"Farmasi · {short_name} · Captoora Studio"
        slug_url = f"https://galeria.captoora.studio/{slugify(short_name).lower().replace('_', '-')}"
        included_count = sum(1 for p in photos if p["is_included_collab"])
        extra_count = len(photos) - included_count

        album_meta = {
            "id": folder_slug,
            "index": idx,
            "name": cluster_name,
            "short_name": short_name,
            "collection_title": collection_title,
            "tipo": "Individual",
            "is_vip": is_vip,
            "tier_label": tier_label,
            "max_included": max_included,
            "included_count": included_count,
            "extra_count": extra_count,
            "pin": pin_code,
            "slug_url": slug_url,
            "total_ready": len(photos),
            "aprobadas": len(aprobadas_list),
            "en_revision": len(revision_list),
            "gift_count": included_count,
            "photos": photos,
        }
        (album_dir / "MANIFIESTO_ALBUM.json").write_text(
            json.dumps(album_meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        summary_albums.append(album_meta)

    for idx, cluster_name in enumerate(grp_order, start=1):
        photos = group_albums.get(cluster_name, [])
        if not photos:
            continue
        photos.sort(key=lambda x: (0 if x["estado"] == "aprobada" else 1, x["source_name"]))
        folder_slug = f"G{idx:02d}_{slugify(cluster_name)}"
        album_dir = grp_base / folder_slug
        aprob_dir = album_dir / "01_Grupales_Aprobadas_Pixieset"
        aprob_dir.mkdir(parents=True, exist_ok=True)

        aprobadas_list = [p for p in photos if p["estado"] == "aprobada"]
        revision_list = [p for p in photos if p["estado"] != "aprobada"]

        for p_i, p in enumerate(photos):
            p["album_folder"] = folder_slug
            p["album_index"] = 100 + idx
            p["is_included_collab"] = True
            p["is_gift_5"] = True
            p["pixieset_set"] = "Set 2 · Grupales Oficiales Farmasi"

        pin_code = f"{7900 + idx * 11}"
        short_name = cluster_name.split("(")[0].strip()
        collection_title = f"Farmasi · {short_name} · Captoora Studio"
        slug_url = f"https://galeria.captoora.studio/{slugify(short_name).lower().replace('_', '-')}"

        album_meta = {
            "id": folder_slug,
            "index": 100 + idx,
            "name": cluster_name,
            "short_name": short_name,
            "collection_title": collection_title,
            "tipo": "Grupal",
            "is_vip": True,
            "tier_label": "Álbum Grupal Oficial (Separado de Individuales)",
            "max_included": len(photos),
            "included_count": len(photos),
            "extra_count": 0,
            "pin": pin_code,
            "slug_url": slug_url,
            "total_ready": len(photos),
            "aprobadas": len(aprobadas_list),
            "en_revision": len(revision_list),
            "gift_count": len(photos),
            "photos": photos,
        }
        (album_dir / "MANIFIESTO_ALBUM.json").write_text(
            json.dumps(album_meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        summary_albums.append(album_meta)

    master_manifest = {
        "updated_at": "2026-11-06 18:05",
        "boom_window": "20:00 - 22:00 hrs (Hora Boom Instagram)",
        "drive_aprobadas_folder": "https://drive.google.com/drive/folders/1O70rKDMLZfC9d_eY-0Ugh7MAl-iZuw11",
        "drive_d29_folder": "https://drive.google.com/drive/folders/1dCjNfEMUmXyFDu27HtmkpzXkISF3aWlP",
        "drive_cobrizo_sola_folder": "https://drive.google.com/drive/folders/1Y7-si0Zkhxiqi0vf8f-u98B7XPohWWwv",
        "drive_blancos_v03_folder": "https://drive.google.com/drive/folders/13vIl4Xt_R3YIIxkXbqgiSIia1ZL9cjsb",
        "total_ready_photos": len(enriched_items),
        "total_individual_photos": sum(len(a["photos"]) for a in summary_albums if a["tipo"] == "Individual"),
        "total_group_photos": sum(len(a["photos"]) for a in summary_albums if a["tipo"] == "Grupal"),
        "total_collab_delivery_today": sum(a["included_count"] for a in summary_albums if a["tipo"] == "Individual"),
        "total_reserved_upsell_edited": sum(a["extra_count"] for a in summary_albums if a["tipo"] == "Individual"),
        "individual_albums_count": sum(1 for a in summary_albums if a["tipo"] == "Individual"),
        "group_albums_count": sum(1 for a in summary_albums if a["tipo"] == "Grupal"),
        "albums": summary_albums,
    }
    (OUT_DIR / "CATALOGO_MAESTRO_PIXIESET.json").write_text(
        json.dumps(master_manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"OK: {master_manifest['individual_albums_count']} Individuales + {master_manifest['group_albums_count']} Grupales. "
        f"Entrega Hoy Individuales: {master_manifest['total_collab_delivery_today']} fotos "
        f"(+{master_manifest['total_reserved_upsell_edited']} reservadas para venta extra)."
    )


if __name__ == "__main__":
    main()
