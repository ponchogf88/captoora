import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

BASE_DIR = Path(r"C:\Users\USUARIO\captoora")
PIXIESET_DIR = BASE_DIR / "PIXIESET_ALBUMES_ENTREGA"
CATALOG_PATH = PIXIESET_DIR / "CATALOGO_MAESTRO_PIXIESET.json"
CACHE_DIR = PIXIESET_DIR / "00_CACHE_JPG_ORIGINALES"
DOWNLOADS_DIR = Path(r"C:\Users\USUARIO\Downloads")
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_target_dest(album: dict, photo: dict) -> Path:
    if album["tipo"] == "Individual":
        base_album = PIXIESET_DIR / "01_MODELOS_INDIVIDUALES" / album["id"]
        if album["is_vip"]:
            return base_album / "01_ENTREGA_VIP_COMPLETA" / photo["file_name"]
        else:
            if photo.get("is_included_collab"):
                return base_album / "01_ENTREGA_COLABORACION_MAX_5_FOTOS" / photo["file_name"]
            else:
                return base_album / "02_EXTRAS_CON_MARCA_AGUA_SOLO_SI_COMPRAN" / photo["file_name"]
    else:
        base_album = PIXIESET_DIR / "02_ALBUMES_GRUPALES" / album["id"]
        return base_album / "01_Grupales_Aprobadas_Pixieset" / photo["file_name"]


def is_valid_jpg(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 10_000:
        return False
    with open(path, "rb") as f:
        header = f.read(3)
    return header == b"\xff\xd8\xff"


def main():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    albums = catalog["albums"]

    # Build ordered list of download tasks:
    # Priority 1: Individual included (VIP full + Collab max 5)
    # Priority 2: Group albums
    # Priority 3: Individual extra reserved (upsell)
    p1, p2, p3 = [], [], []
    for album in albums:
        for photo in album["photos"]:
            dest = get_target_dest(album, photo)
            item = {
                "file_name": photo["file_name"],
                "drive_id": photo["drive_id"],
                "sha256": photo.get("sha256", ""),
                "dest": dest,
                "album_id": album["id"],
                "tipo": album["tipo"],
                "is_included": photo.get("is_included_collab", True),
            }
            if album["tipo"] == "Individual" and photo.get("is_included_collab", True):
                p1.append(item)
            elif album["tipo"] != "Individual":
                p2.append(item)
            else:
                p3.append(item)

    all_items = p1 + p2 + p3
    print(f"Total photos in catalog: {len(all_items)} (P1 Ind Today={len(p1)}, P2 Group={len(p2)}, P3 Extras={len(p3)})")

    # First, check if any are already in Downloads or Cache or Dest
    pending = []
    for item in all_items:
        fname = item["file_name"]
        cache_path = CACHE_DIR / fname
        dl_path = DOWNLOADS_DIR / fname
        dest_path = item["dest"]
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # If in Downloads and valid, move to cache
        if is_valid_jpg(dl_path) and not is_valid_jpg(cache_path):
            shutil.copy2(dl_path, cache_path)
            try:
                dl_path.unlink()
            except Exception:
                pass

        # If in dest and valid, copy to cache
        if is_valid_jpg(dest_path) and not is_valid_jpg(cache_path):
            shutil.copy2(dest_path, cache_path)

        # If in cache, copy to dest
        if is_valid_jpg(cache_path):
            if not is_valid_jpg(dest_path):
                shutil.copy2(cache_path, dest_path)
        else:
            pending.append(item)

    print(f"Already cached & placed: {len(all_items) - len(pending)} | Remaining to download: {len(pending)}")

    BATCH_SIZE = 12
    for batch_idx in range(0, len(pending), BATCH_SIZE):
        batch = pending[batch_idx : batch_idx + BATCH_SIZE]
        print(f"\n--- Batch {batch_idx // BATCH_SIZE + 1} ({len(batch)} files) ---")

        # Clean up any stale partial files or duplicate names in Downloads before launching
        for item in batch:
            dl_file = DOWNLOADS_DIR / item["file_name"]
            if dl_file.exists():
                try:
                    dl_file.unlink()
                except Exception:
                    pass

        urls = [
            f"https://drive.usercontent.google.com/download?id={item['drive_id']}&export=download&confirm=t&authuser=1"
            for item in batch
        ]
        cmd = [CHROME_EXE, '--profile-directory=Profile 2'] + urls
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait up to 45 seconds for all files in batch to appear in Downloads
        t0 = time.time()
        remaining_in_batch = list(batch)
        while remaining_in_batch and (time.time() - t0) < 50:
            time.sleep(1.0)
            still_waiting = []
            for item in remaining_in_batch:
                fname = item["file_name"]
                dl_path = DOWNLOADS_DIR / fname
                crdownload = DOWNLOADS_DIR / (fname + ".crdownload")
                if crdownload.exists():
                    still_waiting.append(item)
                    continue
                if is_valid_jpg(dl_path):
                    cache_path = CACHE_DIR / fname
                    dest_path = item["dest"]
                    shutil.copy2(dl_path, cache_path)
                    shutil.copy2(cache_path, dest_path)
                    try:
                        dl_path.unlink()
                    except Exception:
                        pass
                    print(f"  [OK] {fname} -> {dest_path.parent.parent.name}/{dest_path.parent.name}")
                else:
                    still_waiting.append(item)
            remaining_in_batch = still_waiting

        if remaining_in_batch:
            print(f"  [WARN] {len(remaining_in_batch)} files in batch did not finish in 50s: {[x['file_name'] for x in remaining_in_batch]}")

    # Second pass for any stragglers
    stragglers = [item for item in all_items if not is_valid_jpg(item["dest"])]
    if stragglers:
        print(f"\nRetrying {len(stragglers)} stragglers in smaller batches of 5...")
        for batch_idx in range(0, len(stragglers), 5):
            batch = stragglers[batch_idx : batch_idx + 5]
            urls = [
                f"https://drive.usercontent.google.com/download?id={item['drive_id']}&export=download&confirm=t&authuser=1"
                for item in batch
            ]
            subprocess.Popen([CHROME_EXE, '--profile-directory=Profile 2'] + urls, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            t0 = time.time()
            rem = list(batch)
            while rem and (time.time() - t0) < 45:
                time.sleep(1.0)
                nxt = []
                for item in rem:
                    fname = item["file_name"]
                    dl_path = DOWNLOADS_DIR / fname
                    if not (DOWNLOADS_DIR / (fname + ".crdownload")).exists() and is_valid_jpg(dl_path):
                        cache_path = CACHE_DIR / fname
                        dest_path = item["dest"]
                        shutil.copy2(dl_path, cache_path)
                        shutil.copy2(cache_path, dest_path)
                        try:
                            dl_path.unlink()
                        except Exception:
                            pass
                        print(f"  [RETRY OK] {fname}")
                    else:
                        nxt.append(item)
                rem = nxt

    # Final audit
    ok_total = sum(1 for item in all_items if is_valid_jpg(item["dest"]))
    ok_p1 = sum(1 for item in p1 if is_valid_jpg(item["dest"]))
    ok_p2 = sum(1 for item in p2 if is_valid_jpg(item["dest"]))
    ok_p3 = sum(1 for item in p3 if is_valid_jpg(item["dest"]))
    print("\n==========================================")
    print(f"FINAL AUDIT: {ok_total}/{len(all_items)} JPGs downloaded & verified!")
    print(f"  - P1 (Individual Delivery Today): {ok_p1}/{len(p1)}")
    print(f"  - P2 (Group Albums Today):        {ok_p2}/{len(p2)}")
    print(f"  - P3 (Extras Reserved Upsell):    {ok_p3}/{len(p3)}")
    print("==========================================")


if __name__ == "__main__":
    main()
