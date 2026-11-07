# -*- coding: utf-8 -*-
"""
Genera:
1. PIXIESET_ALBUMES_ENTREGA/CLASIFICAR_FOTOS_DESCARGADAS.py (+ .bat de 1 clic)
   que separa físicamente:
   - Las 4 VIP (Evelyn + 3 Influencers): Todas sus fotos listas.
   - El resto de Modelos Individuales: ESTRICTAMENTE MÁXIMO 5 FOTOS en la carpeta de entrega
     de colaboración, y aparta las demás en 02_EXTRAS_CON_MARCA_AGUA_SOLO_SI_COMPRAN.
   - Los 3 Álbumes Grupales: Separados de las individuales.
2. ORGANIZADOR_PIXIESET_Y_GALERIAS_CAPTOORA.html con cuenta regresiva a las 8:00 PM
   (Hora Boom Instagram), selector interactivo VIP vs. Máx 5 Fotos, y plantillas oficiales
   de WhatsApp (Montse La China, Evelyn/Influencers y Embajadoras 5 Fotos).
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "PIXIESET_ALBUMES_ENTREGA"
CATALOG_PATH = OUT_DIR / "CATALOGO_MAESTRO_PIXIESET.json"


def build_sorter_script():
    sorter_code = '''# -*- coding: utf-8 -*-
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
    m = re.search(r"(DSC\\d{5}(?:\\s+2)?)", filename, re.IGNORECASE)
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
        print("\\nPASO RAPIDO: Descarga la carpeta 'Aprobadas' de Google Drive (se baja como .zip en Descargas)")
        print("y haz doble clic en CLASIFICAR_FOTOS_PIXIESET.bat. Se separaran solas en segundos.")


if __name__ == "__main__":
    main()
'''
    (OUT_DIR / "CLASIFICAR_FOTOS_DESCARGADAS.py").write_text(sorter_code, encoding="utf-8")


def build_html():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    catalog_json = json.dumps(catalog, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CAPTOORA STUDIO · Operación Boom 8-10 PM · Pixieset (VIP vs Máx 5 Fotos)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #07080c;
      --gold: #dfb15b;
    }}
    body {{
      background-color: var(--bg);
      background-image:
        radial-gradient(at 15% 10%, rgba(223, 177, 91, 0.14) 0px, transparent 45%),
        radial-gradient(at 85% 20%, rgba(56, 189, 248, 0.08) 0px, transparent 50%),
        radial-gradient(at 50% 90%, rgba(16, 185, 129, 0.08) 0px, transparent 50%);
      background-attachment: fixed;
      color: #f3f4f6;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    .font-editorial {{ font-family: 'Cinzel', serif; }}
    .apple-glass {{
      background: rgba(255, 255, 255, 0.045);
      backdrop-filter: blur(24px) saturate(160%);
      border: 1px solid rgba(255, 255, 255, 0.12);
      box-shadow: 0 12px 32px -10px rgba(0, 0, 0, 0.65), inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
    }}
    .apple-glass-card {{
      background: rgba(255, 255, 255, 0.032);
      backdrop-filter: blur(18px);
      border: 1px solid rgba(255, 255, 255, 0.09);
      transition: all 0.2s ease;
    }}
    .apple-glass-card:hover {{
      background: rgba(255, 255, 255, 0.06);
      border-color: rgba(223, 177, 91, 0.45);
      transform: translateY(-2px);
    }}
    .gold-gradient-text {{
      background: linear-gradient(135deg, #ffffff 30%, #dfb15b 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .watermark-overlay {{
      background: repeating-linear-gradient(
        -32deg,
        rgba(255,255,255,0.0) 0px,
        rgba(255,255,255,0.0) 55px,
        rgba(223,177,91,0.10) 55px,
        rgba(223,177,91,0.10) 57px
      );
    }}
  </style>
</head>
<body class="p-4 md:p-7 min-h-screen">

  <!-- URGENCY BANNER: HORA BOOM INSTAGRAM 8:00 - 10:00 PM -->
  <div class="max-w-7xl mx-auto mb-4 rounded-2xl bg-gradient-to-r from-amber-500/20 via-rose-500/15 to-emerald-500/20 border border-amber-400/40 px-5 py-3.5 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
    <div class="flex items-center gap-3">
      <span class="w-3 h-3 rounded-full bg-amber-400 animate-ping"></span>
      <div class="text-xs md:text-sm">
        <strong class="text-amber-300 uppercase tracking-wider">OPERACIÓN HORA BOOM INSTAGRAM (8:00 – 10:00 PM):</strong>
        <span class="text-gray-200 ml-1">Cero edición de fotos no pedidas · <strong>VIP (Evelyn + 3 Influencers) = Álbum Completo</strong> · <strong>Resto de Modelos = Máximo 5 Fotos Colaboración</strong> · <strong>Grupales Separadas</strong>.</span>
      </div>
    </div>
    <div class="flex items-center gap-2 shrink-0">
      <span class="text-[11px] uppercase tracking-wider text-gray-300">Tiempo para las 8:00 PM:</span>
      <span id="boom-countdown" class="font-mono text-sm font-extrabold bg-black/70 text-amber-300 px-3 py-1 rounded-lg border border-amber-400/30">--:--:--</span>
    </div>
  </div>

  <!-- HEADER -->
  <header class="max-w-7xl mx-auto mb-6 apple-glass rounded-2xl p-6 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-5">
    <div>
      <div class="flex flex-wrap items-center gap-2 mb-2">
        <a href="https://galleries.pixieset.com/collections" target="_blank" class="bg-amber-500 hover:bg-amber-400 text-black px-3.5 py-1 rounded-full text-xs font-extrabold shadow-lg transition">
          🚀 1. Abrir Panel Pixieset (Liberar Galerías) ↗
        </a>
        <a href="https://drive.google.com/drive/u/1/folders/1O70rKDMLZfC9d_eY-0Ugh7MAl-iZuw11" target="_blank" class="bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-400/40 text-emerald-300 px-3 py-1 rounded-full text-xs font-bold transition">
          2. Carpeta Drive Aprobadas (144) ↗
        </a>
        <a href="https://drive.google.com/drive/u/1/folders/1dCjNfEMUmXyFDu27HtmkpzXkISF3aWlP" target="_blank" class="bg-sky-500/20 hover:bg-sky-500/30 border border-sky-400/40 text-sky-300 px-3 py-1 rounded-full text-xs font-semibold transition">
          3. Drive Acabado D (29) ↗
        </a>
        <a href="https://drive.google.com/drive/u/1/folders/1Y7-si0Zkhxiqi0vf8f-u98B7XPohWWwv" target="_blank" class="bg-purple-500/20 hover:bg-purple-500/30 border border-purple-400/40 text-purple-300 px-3 py-1 rounded-full text-xs font-semibold transition">
          4. Drive Cobrizo Sola (6) ↗
        </a>
        <a href="https://captoora.pixieset.com/farmasistudio10oct2026-1/" target="_blank" class="bg-white/10 hover:bg-white/15 border border-white/20 text-white px-3 py-1 rounded-full text-xs font-semibold transition">
          Ver Galería Activa Pixieset ↗
        </a>
      </div>
      <h1 class="text-2xl md:text-3xl font-extrabold font-editorial gold-gradient-text">
        Centro de Liberación de Galerías · Individuales (VIP vs Máx 5) & Grupales
      </h1>
      <p class="text-gray-400 text-xs md:text-sm mt-1">
        Tus <strong>14 álbumes</strong> están separados y listos: <strong class="text-amber-300">🌟 VIP (Evelyn + 3 Influencers = Entrega Completa)</strong> · <strong class="text-emerald-300">🎁 Colaboración (Máximo 5 Fotos c/u)</strong> · <strong class="text-sky-300">👥 3 Álbumes Grupales Separados</strong>.
      </p>
    </div>

    <div class="flex flex-wrap gap-2">
      <button onclick="switchMainView('albums')" id="tab-albums" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-amber-500 text-black shadow-lg transition">
        1. Álbumes Pixieset (11 Ind / 3 Grup)
      </button>
      <button onclick="switchMainView('photos')" id="tab-photos" class="px-4 py-2.5 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/15 text-white border border-white/15 transition">
        2. Elegir las 5 Fotos / Mover (159)
      </button>
      <button onclick="switchMainView('preview')" id="tab-preview" class="px-4 py-2.5 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/15 text-white border border-white/15 transition">
        3. Vista Previa Galería Clienta
      </button>
      <button onclick="exportUpdatedCatalog()" class="px-3.5 py-2.5 rounded-xl text-xs font-semibold bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-400/30 transition">
        ⬇ Guardar JSON
      </button>
    </div>
  </header>

  <div class="max-w-7xl mx-auto space-y-6">

    <!-- KPI SUMMARY BAR -->
    <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
      <div class="apple-glass rounded-2xl p-4 border-l-2 border-amber-400">
        <div class="text-[11px] uppercase tracking-wider text-amber-300 font-bold">🌟 VIP (3 Influencers + Evelyn)</div>
        <div class="text-2xl font-extrabold text-white mt-1"><span id="kpi-vip-albums">5</span> <span class="text-xs font-normal text-gray-400">álbumes VIP</span></div>
        <div class="text-[11px] text-gray-300 mt-0.5"><span id="kpi-vip-photos">60</span> fotos (Reciben TODAS)</div>
      </div>
      <div class="apple-glass rounded-2xl p-4 border-l-2 border-emerald-400">
        <div class="text-[11px] uppercase tracking-wider text-emerald-300 font-bold">🎁 Colaboración (Máx 5 Fotos)</div>
        <div class="text-2xl font-extrabold text-white mt-1"><span id="kpi-std-albums">6</span> <span class="text-xs font-normal text-gray-400">modelos</span></div>
        <div class="text-[11px] text-gray-300 mt-0.5"><span id="kpi-std-included">30</span> fotos a entregar hoy (5 c/u)</div>
      </div>
      <div class="apple-glass rounded-2xl p-4 border-l-2 border-purple-400">
        <div class="text-[11px] uppercase tracking-wider text-purple-300 font-bold">🔒 Extras Ya Editadas (Upsell)</div>
        <div class="text-2xl font-extrabold text-white mt-1" id="kpi-extra-reserved">27</div>
        <div class="text-[11px] text-gray-400 mt-0.5">Apartadas solo si compran</div>
      </div>
      <div class="apple-glass rounded-2xl p-4 border-l-2 border-sky-400">
        <div class="text-[11px] uppercase tracking-wider text-sky-300 font-bold">👥 Grupales Separadas</div>
        <div class="text-2xl font-extrabold text-white mt-1"><span id="kpi-grp-photos">42</span> <span class="text-xs font-normal text-gray-400">fotos</span></div>
        <div class="text-[11px] text-gray-300 mt-0.5">En 3 bloques grupales</div>
      </div>
      <div class="apple-glass rounded-2xl p-4">
        <div class="text-[11px] uppercase tracking-wider text-gray-400 font-bold">Pendientes Sin Editar</div>
        <div class="text-2xl font-extrabold text-gray-300 mt-1">625</div>
        <div class="text-[11px] text-rose-300 mt-0.5">0 min invertidos salvo pedido</div>
      </div>
    </div>

    <!-- ==================== VIEW 1: ALBUMS BUILDER ==================== -->
    <div id="view-albums" class="space-y-5">
      <div class="apple-glass rounded-2xl p-4 flex flex-wrap justify-between items-center gap-4">
        <div class="flex flex-wrap gap-2">
          <button onclick="filterAlbumType('ALL')" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white/20 text-white border border-white/30">
            Todos (14)
          </button>
          <button onclick="filterAlbumType('VIP')" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-400/40 hover:bg-amber-500/30">
            🌟 Solo VIP / Influencers + Evelyn
          </button>
          <button onclick="filterAlbumType('MAX5')" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-400/40 hover:bg-emerald-500/30">
            🎁 Solo Colaboración (Máx 5 Fotos)
          </button>
          <button onclick="filterAlbumType('Grupal')" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-sky-500/20 text-sky-300 border border-sky-400/40 hover:bg-sky-500/30">
            👥 Solo Grupales Separadas (3)
          </button>
        </div>
        <div class="text-xs text-gray-300">
          Haz clic en <span class="px-2 py-0.5 rounded bg-white/10 font-mono text-amber-300">Cambiar VIP ↔ Máx 5</span> en cualquier tarjeta si deseas ajustar quién recibe más de 5 fotos.
        </div>
      </div>

      <div id="albums-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5"></div>
    </div>

    <!-- ==================== VIEW 2: VISUAL PHOTO SEPARATOR ==================== -->
    <div id="view-photos" class="hidden space-y-5">
      <div class="apple-glass rounded-2xl p-5 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div class="flex flex-wrap gap-2 items-center">
          <button onclick="setPhotoFilter('ALL')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-white/20 text-white">Todas (159)</button>
          <button onclick="setPhotoFilter('DELIVER_TODAY')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">✅ Entregar Hoy (VIP + 5 Collab)</button>
          <button onclick="setPhotoFilter('RESERVED_EXTRA')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-purple-500/20 text-purple-300 border border-purple-400/30">🔒 Extras Reservadas (Solo Venta)</button>
          <button onclick="setPhotoFilter('Grupal')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-sky-500/20 text-sky-300 border border-sky-400/30">👥 Grupales (42)</button>
          <select id="album-dropdown-filter" onchange="setPhotoAlbumFilter(this.value)" class="bg-black/70 border border-white/20 text-white text-xs rounded-xl px-3 py-1.5"></select>
        </div>
        <div class="w-full lg:w-72">
          <input type="text" id="search-input" oninput="renderPhotosGrid()" placeholder="Buscar DSC07706, DSC00001..." class="w-full bg-black/50 border border-white/15 rounded-xl px-3.5 py-2 text-xs text-white focus:outline-none focus:border-amber-400">
        </div>
      </div>

      <div id="photos-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"></div>
    </div>

    <!-- ==================== VIEW 3: CLIENT GALLERY SIMULATOR ==================== -->
    <div id="view-preview" class="hidden space-y-6">
      <div class="apple-glass rounded-2xl p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div class="flex flex-wrap items-center gap-3">
          <label class="text-xs text-gray-300 font-semibold">Ver Galería de:</label>
          <select id="sim-album-select" onchange="renderSimulator()" class="bg-black/70 border border-amber-400/40 text-white text-xs font-semibold rounded-xl px-4 py-2"></select>
          <button onclick="toggleSimSet('IND')" id="sim-set-ind" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500 text-black">
            Set 1 · Sus Fotos Individuales
          </button>
          <button onclick="toggleSimSet('GRP')" id="sim-set-grp" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-white/10 text-gray-300 border border-white/15">
            Set 2 · Grupales Farmasi (42)
          </button>
        </div>
        <div class="flex items-center gap-3">
          <span id="sim-pin-badge" class="text-xs font-mono bg-white/10 px-3 py-1.5 rounded-xl text-amber-300 border border-amber-400/20">PIN: 3117</span>
          <button onclick="toggleSimUnlock()" class="px-4 py-1.5 rounded-xl text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 hover:bg-emerald-500/30">
            🔓 Alternar Vista Desbloqueada / Con Marca de Agua
          </button>
        </div>
      </div>

      <div class="apple-glass rounded-2xl p-6 text-center space-y-2 border border-amber-400/20">
        <div id="sim-tier-pill" class="inline-block text-[11px] uppercase tracking-widest text-amber-300 font-bold bg-amber-500/15 px-3 py-1 rounded-full border border-amber-400/30"></div>
        <h2 id="sim-title" class="text-2xl md:text-3xl font-extrabold font-editorial gold-gradient-text"></h2>
        <p id="sim-subtitle" class="text-xs text-gray-300 max-w-2xl mx-auto"></p>
      </div>

      <div id="sim-photos-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"></div>
    </div>

  </div>

  <!-- TOAST -->
  <div id="toast" class="fixed bottom-6 right-6 bg-black/95 border border-amber-400/50 text-white px-4 py-3 rounded-xl text-xs font-semibold shadow-2xl hidden z-50 max-w-md"></div>

  <script>
    const initialCatalog = {catalog_json};
    let catalog = JSON.parse(localStorage.getItem("captoora_pixieset_boom_v2") || "null") || initialCatalog;

    let currentAlbumFilter = "ALL";
    let currentPhotoTypeFilter = "ALL";
    let currentPhotoAlbumFilter = "ALL";
    let simSelectedAlbumId = catalog.albums[0].id;
    let simActiveSet = "IND";
    let simUnlocked = false;

    // Countdown to 8:00 PM (20:00)
    function updateCountdown() {{
      const now = new Date();
      const target = new Date();
      target.setHours(20, 0, 0, 0);
      const endBoom = new Date();
      endBoom.setHours(22, 0, 0, 0);
      const el = document.getElementById("boom-countdown");
      if (now < target) {{
        const diff = Math.floor((target - now) / 1000);
        const h = String(Math.floor(diff / 3600)).padStart(2, "0");
        const m = String(Math.floor((diff % 3600) / 60)).padStart(2, "0");
        const s = String(diff % 60).padStart(2, "0");
        el.textContent = `FALTAN ${{h}}:${{m}}:${{s}}`;
      }} else if (now <= endBoom) {{
        el.textContent = "🔥 ¡EN HORA BOOM AHORA (8-10 PM)!";
      }} else {{
        el.textContent = "VENTANA NOCTURNA ACTIVA";
      }}
    }}
    setInterval(updateCountdown, 1000);
    updateCountdown();

    function saveCatalog() {{
      localStorage.setItem("captoora_pixieset_boom_v2", JSON.stringify(catalog));
      updateKPIs();
    }}

    function showToast(msg) {{
      const t = document.getElementById("toast");
      t.textContent = msg;
      t.classList.remove("hidden");
      setTimeout(() => t.classList.add("hidden"), 3500);
    }}

    function updateKPIs() {{
      let vipAlbums = 0, vipPhotos = 0, stdAlbums = 0, stdIncluded = 0, extraReserved = 0, grpPhotos = 0;
      catalog.albums.forEach(a => {{
        if (a.tipo === "Individual") {{
          const inc = a.photos.filter(p => p.is_included_collab).length;
          const ext = a.photos.length - inc;
          extraReserved += ext;
          if (a.is_vip) {{
            vipAlbums++;
            vipPhotos += inc;
          }} else {{
            stdAlbums++;
            stdIncluded += inc;
          }}
        }} else {{
          grpPhotos += a.photos.length;
        }}
      }});
      document.getElementById("kpi-vip-albums").textContent = vipAlbums;
      document.getElementById("kpi-vip-photos").textContent = vipPhotos;
      document.getElementById("kpi-std-albums").textContent = stdAlbums;
      document.getElementById("kpi-std-included").textContent = stdIncluded;
      document.getElementById("kpi-extra-reserved").textContent = extraReserved;
      document.getElementById("kpi-grp-photos").textContent = grpPhotos;
    }}

    function switchMainView(view) {{
      ["albums", "photos", "preview"].forEach(v => {{
        document.getElementById("view-" + v).classList.toggle("hidden", v !== view);
        const btn = document.getElementById("tab-" + v);
        btn.className = v === view
          ? "px-4 py-2.5 rounded-xl text-xs font-bold bg-amber-500 text-black shadow-lg transition"
          : "px-4 py-2.5 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/15 text-white border border-white/15 transition";
      }});
      if (view === "albums") renderAlbums();
      if (view === "photos") renderPhotosGrid();
      if (view === "preview") renderSimulator();
    }}

    function filterAlbumType(type) {{
      currentAlbumFilter = type;
      renderAlbums();
    }}

    function toggleAlbumVip(albumId) {{
      const a = catalog.albums.find(x => x.id === albumId);
      if (!a || a.tipo !== "Individual") return;
      a.is_vip = !a.is_vip;
      a.photos.forEach((p, idx) => {{
        p.is_included_collab = a.is_vip ? true : (idx < 5);
        p.is_gift_5 = p.is_included_collab;
      }});
      a.included_count = a.photos.filter(p => p.is_included_collab).length;
      a.extra_count = a.photos.length - a.included_count;
      saveCatalog();
      renderAlbums();
      showToast(a.is_vip
        ? `🌟 ${{a.name}} cambiada a VIP (Recibe sus ${{a.photos.length}} fotos completas)`
        : `🎁 ${{a.name}} cambiada a Colaboración Estándar (Máximo 5 fotos incluidas; ${{a.extra_count}} apartadas para venta)`);
    }}

    function renderAlbums() {{
      const container = document.getElementById("albums-container");
      const filtered = catalog.albums.filter(a => {{
        if (currentAlbumFilter === "ALL") return true;
        if (currentAlbumFilter === "VIP") return a.tipo === "Individual" && a.is_vip;
        if (currentAlbumFilter === "MAX5") return a.tipo === "Individual" && !a.is_vip;
        if (currentAlbumFilter === "Grupal") return a.tipo === "Grupal";
        return true;
      }});

      container.innerHTML = filtered.map(a => {{
        const isInd = a.tipo === "Individual";
        const incCount = a.photos.filter(p => p.is_included_collab).length;
        const extCount = a.photos.length - incCount;

        let badgeHtml = "";
        if (!isInd) {{
          badgeHtml = `<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border bg-sky-500/20 text-sky-300 border-sky-400/40">👥 ÁLBUM GRUPAL SEPARADO</span>`;
        }} else if (a.is_vip) {{
          badgeHtml = `<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border bg-amber-500/25 text-amber-300 border-amber-400/50">🌟 VIP · INFLUENCER / EVELYN (TODAS)</span>`;
        }} else {{
          badgeHtml = `<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border bg-emerald-500/20 text-emerald-300 border-emerald-400/40">🎁 COLABORACIÓN (MÁX 5 FOTOS)</span>`;
        }}

        const includedPhotos = a.photos.filter(p => p.is_included_collab).slice(0, 5);

        return `
          <div class="apple-glass-card rounded-2xl p-5 flex flex-col justify-between space-y-4 ${{a.is_vip && isInd ? 'border-amber-400/35' : ''}}">
            <div class="space-y-3">
              <div class="flex justify-between items-center gap-2">
                ${{badgeHtml}}
                <span class="text-xs font-mono text-gray-400">PIN: <strong class="text-amber-300">${{a.pin}}</strong></span>
              </div>

              <div class="flex justify-between items-start gap-2">
                <div>
                  <h3 class="text-base font-bold text-white leading-snug">${{a.name}}</h3>
                  <p class="text-[11px] text-gray-400 font-mono mt-0.5">${{a.collection_title}}</p>
                </div>
                ${{isInd ? `
                  <button onclick="toggleAlbumVip('${{a.id}}')" class="shrink-0 px-2.5 py-1 rounded-lg text-[10px] font-bold bg-white/10 hover:bg-white/20 text-amber-300 border border-white/15 transition" title="Alternar entre VIP (Todas) y Colaboración (Máx 5)">
                    ${{a.is_vip ? 'Pasar a Máx 5' : 'Hacer VIP'}}
                  </button>
                ` : ''}}
              </div>

              <!-- Counters -->
              <div class="grid grid-cols-3 gap-2 text-center bg-black/40 rounded-xl p-2.5 border border-white/5">
                <div>
                  <div class="text-base font-extrabold text-emerald-400">${{incCount}}</div>
                  <div class="text-[10px] text-gray-300 font-semibold">Entregar Hoy</div>
                </div>
                <div>
                  <div class="text-base font-extrabold ${{extCount > 0 ? 'text-purple-300' : 'text-gray-500'}}">${{extCount}}</div>
                  <div class="text-[10px] text-gray-400">Extras Venta</div>
                </div>
                <div>
                  <div class="text-base font-extrabold text-white">${{a.photos.length}}</div>
                  <div class="text-[10px] text-gray-400">Total Listas</div>
                </div>
              </div>

              <!-- Preview of the 5 (or VIP) photos included today -->
              <div>
                <div class="text-[10px] uppercase tracking-wider text-gray-400 mb-1.5 font-semibold">
                  ${{isInd ? (a.is_vip ? `Fotos VIP a entregar hoy (${{incCount}}):` : `Las ${{incCount}} Fotos de Colaboración a entregar hoy:`) : `Muestra Grupales (${{incCount}}):`}}
                </div>
                <div class="grid grid-cols-5 gap-1.5">
                  ${{includedPhotos.map(p => `
                    <a href="${{p.approved_url || p.review_url}}" target="_blank" class="block aspect-[3/4] rounded-lg overflow-hidden bg-black/60 border border-emerald-400/30 relative group" title="${{p.source_name}} -> ${{p.file_name}}">
                      <img src="https://drive.google.com/thumbnail?id=${{p.drive_id}}&sz=w800&authuser=1" alt="${{p.source_name}}" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition" onerror="if(!this.dataset.retried){{this.dataset.retried='1';this.src='https://drive.google.com/thumbnail?id=${{p.drive_id}}&sz=w800&authuser=0';}}">
                      <span class="absolute bottom-0 inset-x-0 bg-black/80 text-[8px] font-mono text-center text-emerald-300 py-0.5">${{p.source_name.replace('.JPG','')}}</span>
                    </a>
                  `).join('')}}
                </div>
              </div>

              <!-- Exact filenames list for fast Pixieset upload -->
              <div class="bg-black/45 rounded-xl p-2.5 border border-white/5">
                <div class="text-[10px] text-gray-400 mb-1 font-semibold">Archivos a subir hoy a su galería Pixieset:</div>
                <div class="text-[10px] font-mono text-gray-200 max-h-14 overflow-y-auto leading-relaxed">
                  ${{a.photos.filter(p => p.is_included_collab).map(p => p.source_name.replace('.JPG','')).join(', ')}}
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="space-y-2 pt-2 border-t border-white/10">
              <button onclick="downloadAlbumPhotos('${{a.id}}')" class="w-full px-3 py-2 rounded-xl text-xs font-extrabold bg-amber-500 text-black hover:bg-amber-400 shadow transition">
                ⬇ Descargar las ${{incCount}} Fotos de este Álbum (4K)
              </button>
              <div class="grid grid-cols-2 gap-2">
                <button onclick="copyWhatsAppMsg('${{a.id}}')" class="px-3 py-2 rounded-xl text-xs font-bold bg-emerald-500 text-black hover:bg-emerald-400 transition">
                  💬 Copiar WhatsApp Hoy
                </button>
                <button onclick="copyPixiesetConfig('${{a.id}}')" class="px-3 py-2 rounded-xl text-xs font-semibold bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-400/30 transition">
                  📋 Copiar Lista Pixieset
                </button>
                <button onclick="openAlbumInSeparator('${{a.id}}')" class="px-3 py-2 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/20 text-white transition">
                  🎯 Elegir cuáles 5 dar
                </button>
                <button onclick="openAlbumInSimulator('${{a.id}}')" class="px-3 py-2 rounded-xl text-xs font-semibold bg-sky-500/15 hover:bg-sky-500/25 text-sky-300 border border-sky-400/30 transition">
                  👁️ Simular Galería
                </button>
              </div>
            </div>
          </div>
        `;
      }}).join("");
    }}

    function downloadAlbumPhotos(albumId) {{
      const a = catalog.albums.find(x => x.id === albumId);
      if (!a) return;
      const incPhotos = a.photos.filter(p => p.is_included_collab);
      showToast(`⬇ Descargando ${{incPhotos.length}} fotos de ${{a.name}} (se clasifican solas en tu carpeta Pixieset)...`);
      incPhotos.forEach((p, idx) => {{
        setTimeout(() => {{
          const iframe = document.createElement("iframe");
          iframe.style.display = "none";
          iframe.src = `https://drive.usercontent.google.com/download?id=${{p.drive_id}}&export=download&confirm=t&authuser=1`;
          document.body.appendChild(iframe);
        }}, idx * 1400);
      }});
    }}

    function copyWhatsAppMsg(albumId) {{
      const a = catalog.albums.find(x => x.id === albumId);
      if (!a) return;
      const incCount = a.photos.filter(p => p.is_included_collab).length;

      let msg = "";
      if (a.name.toLowerCase().includes("madre") || a.name.toLowerCase().includes("montse")) {{
        msg = `¡Hola, mi queridísima China hermosa! ✨🤍\\n\\nQueríamos escribirte con todo el corazón para agradecerte por haber venido a romperla al estudio el 31 de octubre. ¡Qué vibra tan espectacular trajiste y qué bendición tan grande fue la participación de tu hermoso bebé, que ya es embajador oficial de Captoora! 👶✨\\n\\nAquí tienes tu galería personal VIP con tus fotografías y las grupales del equipo listas en alta definición:\\n🔗 *Tu Galería VIP*: ${{a.slug_url}}\\n🔑 *Tu PIN de Descarga Directa*: ${{a.pin}}\\n\\n🎟️ Además, estás formalmente invitada al estreno de *Captoora Biométricos* (100% GRATIS para ti).\\n\\n¡Si las compartes hoy en tus Historias o Reels, etiquétanos en *@captoora.studio* y *@ponchogf88* para presumirte con todo el amor! 📸🔥`;
      }} else if (a.is_vip && a.tipo === "Individual") {{
        msg = `¡Hola hermosa! ✨🖤\\n\\nMuchísimas gracias por la energía tan espectacular que trajiste al estudio este 31 de octubre. Como embajadora VIP de *Captoora Studio*, te preparamos tu galería especial con tus *${{incCount}} fotografías individuales* + el álbum de *fotos grupales oficiales* en máxima resolución:\\n\\n🔗 *Tu Galería VIP*: ${{a.slug_url}}\\n🔑 *Tu PIN de Descarga*: ${{a.pin}}\\n\\n🎟️ Además tienes pase VIP 100% GRATIS para el estreno de *Captoora Biométricos*.\\n\\n¡Nos encantará verte brillar esta noche en tus Historias y Reels! Etiquétanos en *@captoora.studio* y *@ponchogf88* para compartirte en la cuenta oficial. 📸✨`;
      }} else {{
        msg = `¡Hola hermosa! ✨🤍\\n\\nQueríamos agradecerte de todo corazón por haber venido al estudio el pasado 31 de octubre. Oficialmente ya eres parte de nuestra familia como embajadora de *Captoora Studio*. 📸\\n\\nAquí tienes tu enlace personal con tus *${{incCount}} fotografías oficiales incluidas en tu colaboración* + el acceso a las fotos grupales:\\n🔗 *Tu Galería Privada*: ${{a.slug_url}}\\n🔑 *Tu PIN de Descarga (${{incCount}} Fotos Cortesía 4K)*: ${{a.pin}}\\n\\n🎁 *Sorpresa de Embajadora*:\\n1. Descarga tus ${{incCount}} fotos de regalo y súbelas hoy a tus Historias etiquetando a *@captoora.studio* y *@ponchogf88*.\\n2. Si deseas adquirir fotos adicionales de tu sesión, mándanos captura de tu historia por aquí para activarte tu beneficio preferencial y tu invitación al piloto de *Captoora Biométricos*. 💫🖤`;
      }}
      navigator.clipboard.writeText(msg);
      showToast("✅ Mensaje de WhatsApp copiado para " + a.name);
    }}

    function copyPixiesetConfig(albumId) {{
      const a = catalog.albums.find(x => x.id === albumId);
      if (!a) return;
      const incPhotos = a.photos.filter(p => p.is_included_collab);
      const extPhotos = a.photos.filter(p => !p.is_included_collab);
      const text = [
        `COLECCIÓN PIXIESET: ${{a.collection_title}}`,
        `TIPO: ${{a.is_vip ? 'VIP ENTREGA COMPLETA' : 'COLABORACIÓN MÁXIMO 5 FOTOS'}}`,
        `PIN DESCARGA: ${{a.pin}} (Límite de descargas gratis: ${{incPhotos.length}})`,
        `--- FOTOS A ENTREGAR HOY (${{incPhotos.length}}) ---`,
        incPhotos.map(p => `${{p.source_name}} -> ${{p.file_name}}`).join("\\n"),
        extPhotos.length ? `\\n--- FOTOS EXTRAS RESERVADAS PARA VENTA CON MARCA DE AGUA (${{extPhotos.length}}) ---\\n` + extPhotos.map(p => `${{p.source_name}} -> ${{p.file_name}}`).join("\\n") : ""
      ].join("\\n");
      navigator.clipboard.writeText(text);
      showToast(`📋 Lista de ${{incPhotos.length}} archivos copiada para subir a Pixieset`);
    }}

    function openAlbumInSeparator(albumId) {{
      currentPhotoAlbumFilter = albumId;
      document.getElementById("album-dropdown-filter").value = albumId;
      switchMainView("photos");
    }}

    function openAlbumInSimulator(albumId) {{
      simSelectedAlbumId = albumId;
      document.getElementById("sim-album-select").value = albumId;
      simActiveSet = "IND";
      switchMainView("preview");
    }}

    function populateDropdowns() {{
      const sel = document.getElementById("album-dropdown-filter");
      const simSel = document.getElementById("sim-album-select");
      sel.innerHTML = `<option value="ALL">Todos los Álbumes (14)</option>` +
        catalog.albums.map(a => `<option value="${{a.id}}">${{a.tipo === 'Individual' ? (a.is_vip ? '🌟' : '🎁') : '👥'}} ${{a.name}} (${{a.photos.filter(p=>p.is_included_collab).length}}/${{a.photos.length}})</option>`).join("");
      simSel.innerHTML = catalog.albums.map(a => `<option value="${{a.id}}">${{a.tipo === 'Individual' ? (a.is_vip ? '🌟 VIP:' : '🎁 Máx 5:') : '👥 Grupal:'}} ${{a.name}}</option>`).join("");
    }}

    function setPhotoFilter(f) {{
      currentPhotoTypeFilter = f;
      renderPhotosGrid();
    }}

    function setPhotoAlbumFilter(val) {{
      currentPhotoAlbumFilter = val;
      renderPhotosGrid();
    }}

    function renderPhotosGrid() {{
      const grid = document.getElementById("photos-grid");
      const q = (document.getElementById("search-input").value || "").toLowerCase().trim();

      let allPhotos = [];
      catalog.albums.forEach(a => {{
        a.photos.forEach(p => {{
          allPhotos.push({{ ...p, albumId: a.id, albumName: a.name, albumTipo: a.tipo, albumVip: a.is_vip }});
        }});
      }});

      const filtered = allPhotos.filter(p => {{
        if (currentPhotoTypeFilter === "DELIVER_TODAY" && !(p.albumTipo === "Individual" && p.is_included_collab)) return false;
        if (currentPhotoTypeFilter === "RESERVED_EXTRA" && !(p.albumTipo === "Individual" && !p.is_included_collab)) return false;
        if (currentPhotoTypeFilter === "Grupal" && p.albumTipo !== "Grupal") return false;
        if (currentPhotoAlbumFilter !== "ALL" && p.albumId !== currentPhotoAlbumFilter) return false;
        if (q && !(p.source_name.toLowerCase().includes(q) || p.file_name.toLowerCase().includes(q) || p.albumName.toLowerCase().includes(q))) return false;
        return true;
      }});

      grid.innerHTML = filtered.map(p => `
        <div class="apple-glass-card rounded-2xl overflow-hidden flex flex-col justify-between ${{p.is_included_collab ? 'border-emerald-400/30' : 'opacity-80'}}">
          <div>
            <div class="relative aspect-[3/4] bg-black/60 overflow-hidden">
              <img src="https://drive.google.com/thumbnail?id=${{p.drive_id}}&sz=w800&authuser=1" alt="${{p.source_name}}" loading="lazy" class="w-full h-full object-cover" onerror="if(!this.dataset.retried){{this.dataset.retried='1';this.src='https://drive.google.com/thumbnail?id=${{p.drive_id}}&sz=w800&authuser=0';}}">
              <div class="absolute top-2 left-2 flex flex-wrap gap-1">
                <span class="px-2 py-0.5 rounded-md text-[10px] font-bold ${{p.albumTipo === 'Individual' ? 'bg-amber-500 text-black' : 'bg-sky-500 text-black'}}">
                  ${{p.albumTipo === 'Individual' ? '👤 IND' : '👥 GRUP'}}
                </span>
                ${{p.is_included_collab
                  ? '<span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-500 text-black">✅ ENTREGAR HOY</span>'
                  : '<span class="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-purple-900/90 text-purple-200 border border-purple-400/30">🔒 RESERVA VENTA</span>'}}
              </div>
              <div class="absolute bottom-2 right-2">
                <a href="${{p.approved_url || p.review_url}}" target="_blank" class="px-2.5 py-1 rounded-lg bg-black/80 hover:bg-black text-[10px] text-amber-300 border border-amber-400/30 font-semibold">
                  Ver en Drive ↗
                </a>
              </div>
            </div>

            <div class="p-3.5 space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-sm font-extrabold text-white font-mono">${{p.source_name}}</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full ${{p.estado === 'aprobada' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-sky-500/20 text-sky-300'}}">${{p.estado}}</span>
              </div>
              <div class="text-[11px] text-gray-300 font-mono truncate" title="${{p.file_name}}">${{p.file_name}}</div>

              <div class="pt-1">
                <label class="text-[10px] text-gray-400 block mb-1">Cambiar de Álbum (Individual / Grupal):</label>
                <select onchange="movePhotoToAlbum('${{p.source_name}}', '${{p.albumId}}', this.value)" class="w-full bg-black/70 border border-white/15 rounded-lg px-2 py-1.5 text-[11px] text-white">
                  ${{catalog.albums.map(a => `
                    <option value="${{a.id}}" ${{a.id === p.albumId ? 'selected' : ''}}>
                      ${{a.tipo === 'Individual' ? '👤' : '👥'}} ${{a.name}}
                    </option>
                  `).join('')}}
                </select>
              </div>
            </div>
          </div>

          <div class="px-3.5 pb-3.5 pt-1">
            <button onclick="toggleGiftStatus('${{p.source_name}}', '${{p.albumId}}')" class="w-full py-1.5 rounded-lg text-[11px] font-bold border transition ${{p.is_included_collab ? 'bg-emerald-500/20 text-emerald-300 border-emerald-400/40' : 'bg-white/5 text-gray-300 border-white/10 hover:bg-white/15'}}">
              ${{p.is_included_collab ? '✓ Incluida en Entrega Hoy (Clic para apartar)' : '+ Incluir en Entrega de Hoy'}}
            </button>
          </div>
        </div>
      `).join("");
    }}

    function movePhotoToAlbum(sourceName, fromAlbumId, toAlbumId) {{
      if (fromAlbumId === toAlbumId) return;
      const fromAlb = catalog.albums.find(a => a.id === fromAlbumId);
      const toAlb = catalog.albums.find(a => a.id === toAlbumId);
      if (!fromAlb || !toAlb) return;

      const idx = fromAlb.photos.findIndex(p => p.source_name === sourceName);
      if (idx === -1) return;
      const [photo] = fromAlb.photos.splice(idx, 1);
      photo.cluster = toAlb.name;
      photo.tipo = toAlb.tipo;
      photo.album_folder = toAlb.id;
      toAlb.photos.push(photo);

      saveCatalog();
      populateDropdowns();
      renderPhotosGrid();
      showToast(`✅ ${{sourceName}} movida a ${{toAlb.name}}`);
    }}

    function toggleGiftStatus(sourceName, albumId) {{
      const alb = catalog.albums.find(a => a.id === albumId);
      if (!alb) return;
      const p = alb.photos.find(x => x.source_name === sourceName);
      if (!p) return;
      p.is_included_collab = !p.is_included_collab;
      p.is_gift_5 = p.is_included_collab;
      alb.included_count = alb.photos.filter(x => x.is_included_collab).length;
      alb.extra_count = alb.photos.length - alb.included_count;
      saveCatalog();
      renderPhotosGrid();
      showToast(p.is_included_collab
        ? `✅ ${{sourceName}} incluida en la entrega de hoy (${{alb.included_count}} en este álbum)`
        : `🔒 ${{sourceName}} apartada como extra de venta (${{alb.included_count}} en entrega hoy)`);
    }}

    function toggleSimSet(setMode) {{
      simActiveSet = setMode;
      document.getElementById("sim-set-ind").className = setMode === "IND"
        ? "px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500 text-black"
        : "px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-white/10 text-gray-300 border border-white/15";
      document.getElementById("sim-set-grp").className = setMode === "GRP"
        ? "px-3.5 py-1.5 rounded-xl text-xs font-bold bg-sky-500 text-black"
        : "px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-white/10 text-gray-300 border border-white/15";
      renderSimulator();
    }}

    function toggleSimUnlock() {{
      simUnlocked = !simUnlocked;
      renderSimulator();
    }}

    function renderSimulator() {{
      const albumId = document.getElementById("sim-album-select").value || simSelectedAlbumId;
      const alb = catalog.albums.find(a => a.id === albumId) || catalog.albums[0];
      const incCount = alb.photos.filter(p => p.is_included_collab).length;

      document.getElementById("sim-title").textContent = alb.collection_title;
      document.getElementById("sim-pin-badge").textContent = "PIN VIP: " + alb.pin;
      document.getElementById("sim-tier-pill").textContent = alb.is_vip
        ? `🌟 EMBAJADORA VIP · ENTREGA COMPLETA (${{incCount}} FOTOS LIBERADAS)`
        : `🎁 COLABORACIÓN OFICIAL · ${{incCount}} FOTOS DE REGALO INCLUIDAS`;
      document.getElementById("sim-subtitle").innerHTML = alb.is_vip
        ? `Tienes acceso libre en 4K a tus <strong>${{incCount}} fotografías individuales</strong> y a las grupales del evento. ¡Etiquétanos hoy entre 8 y 10 PM en <strong>@captoora.studio</strong> y <strong>@ponchogf88</strong>!`
        : `Tu colaboración incluye <strong>${{incCount}} fotografías en resolución 4K sin marca de agua</strong> listas para descargar con tu PIN <code>${{alb.pin}}</code>. Si deseas solicitar o desbloquear fotografías adicionales de tu sesión, sube tu Historia etiquetando a <strong>@captoora.studio</strong> y escríbenos por WhatsApp.`;

      let photosToShow = [];
      if (simActiveSet === "IND") {{
        photosToShow = alb.photos;
      }} else {{
        catalog.albums.filter(a => a.tipo === "Grupal").forEach(ga => {{
          photosToShow.push(...ga.photos);
        }});
      }}

      const grid = document.getElementById("sim-photos-grid");
      grid.innerHTML = photosToShow.map(p => {{
        const unlocked = simUnlocked || p.is_included_collab;
        return `
          <div class="apple-glass-card rounded-2xl overflow-hidden flex flex-col justify-between">
            <div class="relative aspect-[3/4] bg-black/70 overflow-hidden select-none">
              <img src="https://drive.google.com/thumbnail?id=${{p.drive_id}}&sz=w800&authuser=1" alt="${{p.source_name}}" loading="lazy" class="w-full h-full object-cover" onerror="if(!this.dataset.retried){{this.dataset.retried='1';this.src='https://drive.google.com/thumbnail?id=${{p.drive_id}}&sz=w800&authuser=0';}}">
              ${{!unlocked ? `
                <div class="absolute inset-0 watermark-overlay flex items-center justify-center p-4 text-center pointer-events-none">
                  <div class="border border-white/25 bg-black/65 backdrop-blur-sm px-3 py-1.5 rounded-lg text-[10px] font-bold tracking-widest text-white/90 uppercase">
                    CAPTOORA STUDIO · FOTO ADICIONAL BAJO PEDIDO
                  </div>
                </div>
              ` : ''}}
              <div class="absolute top-2.5 left-2.5">
                ${{unlocked
                  ? '<span class="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500 text-black">✅ INCLUIDA · DESCARGA 4K</span>'
                  : '<span class="px-2.5 py-1 rounded-full text-[10px] font-bold bg-black/85 text-amber-300 border border-amber-400/30">🔒 FOTO EXTRA ADICIONAL</span>'}}
              </div>
            </div>
            <div class="p-3.5 flex justify-between items-center">
              <div>
                <div class="text-xs font-bold text-white font-mono">${{p.source_name}}</div>
                <div class="text-[10px] text-gray-400">${{unlocked ? 'Incluida en tu entrega de hoy' : 'Disponible bajo pedido ($399 / $499)'}}</div>
              </div>
              ${{unlocked
                ? `<a href="https://drive.usercontent.google.com/download?id=${{p.drive_id}}&export=download&confirm=t&authuser=1" target="_blank" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-emerald-500 text-black hover:bg-emerald-400 transition">⬇ 4K</a>`
                : `<button onclick="showToast('📲 Solicita esta foto extra por WhatsApp tras subir tu Historia etiquetando a @captoora.studio')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-400/30">Pedir Extra</button>`
              }}
            </div>
          </div>
        `;
      }}).join("");
    }}

    function exportUpdatedCatalog() {{
      const blob = new Blob([JSON.stringify(catalog, null, 2)], {{ type: "application/json" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "CATALOGO_MAESTRO_PIXIESET_ACTUALIZADO.json";
      a.click();
      showToast("⬇ Catálogo JSON actualizado exportado");
    }}

    populateDropdowns();
    updateKPIs();
    renderAlbums();
  </script>
</body>
</html>
"""
    (ROOT / "ORGANIZADOR_PIXIESET_Y_GALERIAS_CAPTOORA.html").write_text(html, encoding="utf-8")
    print("OK: Portal Pre-Boom 8-10 PM actualizado.")


if __name__ == "__main__":
    build_sorter_script()
    build_html()
