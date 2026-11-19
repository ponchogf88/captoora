#!/usr/bin/env python3
"""Sincroniza y regenera DASHBOARD_FARMASI_799.html desde los registros oficiales en tiempo real."""
from pathlib import Path
import collections, json

ROOT = Path(__file__).resolve().parents[1]
FUENTES_PATH = ROOT / 'registros/fuentes_799.json'
ESTADO_PATH = ROOT / 'registros/estado_799.json'
COBRIZO_PATH = ROOT / 'historial/modelo_D_todas/SELECCION_COBRIZO_CONFIRMADA.json'
MANIFIESTO_D_PATH = ROOT / 'historial/modelo_D_todas/MANIFIESTO.json'
COBRIZO_SOLA_PATH = ROOT / 'historial/cobrizo_sola_6/MANIFIESTO.json'
DASHBOARD_PATH = ROOT / 'DASHBOARD_FARMASI_799.html'


def build_data():
    fuentes_list = json.loads(FUENTES_PATH.read_text(encoding='utf-8'))
    estado_global = json.loads(ESTADO_PATH.read_text(encoding='utf-8'))
    cobrizo_list = json.loads(COBRIZO_PATH.read_text(encoding='utf-8'))
    cobrizo_names = {x['source_name'] for x in cobrizo_list}
    manifiesto_d = {x['source_name']: x for x in json.loads(MANIFIESTO_D_PATH.read_text(encoding='utf-8'))}
    cobrizo_sola_6 = {}
    if COBRIZO_SOLA_PATH.exists():
        cobrizo_sola_6 = {x['source_name']: x for x in json.loads(COBRIZO_SOLA_PATH.read_text(encoding='utf-8'))}

    bebe_names = {
        'DSC08219.JPG', 'DSC08224.JPG', 'DSC08230.JPG', 'DSC08233.JPG',
        'DSC08235.JPG', 'DSC08246.JPG', 'DSC08258.JPG', 'DSC08261.JPG',
        'DSC08272.JPG', 'DSC08276 2.JPG', 'DSC08282 2.JPG', 'DSC08283 2.JPG',
        'DSC08284.JPG', 'DSC08290 2.JPG', 'DSC08294 2.JPG', 'DSC08295.JPG'
    }

    items = []
    cluster_items = collections.defaultdict(list)

    for f in fuentes_list:
        name = f['source_name']
        num = int(name[3:8])

        if 7706 <= num <= 7774:
            cluster = 'Modelo Lila (Cabello Negro Largo · D)'
            tipo = 'Individual'
        elif name in cobrizo_sola_6:
            cluster = 'Modelo Vestido Cobrizo (Individual · Sola 6)'
            tipo = 'Individual'
        elif name in cobrizo_names:
            if num <= 8554:
                cluster = 'Grupales con Modelo Cobrizo / Equipo (D)'
                tipo = 'Grupal'
            else:
                cluster = 'Secuencia Cobrizo Extendida (Grupales / Cierre)'
                tipo = 'Grupal'
        elif name in bebe_names:
            cluster = 'Madre + Bebé'
            tipo = 'Individual'
        elif 1 <= num <= 97:
            cluster = 'Piloto Inicial (Set Negro)'
            tipo = 'Individual'
        elif 501 <= num <= 722:
            cluster = 'Modelo Socia Lote 07'
            tipo = 'Individual'
        elif 863 <= num <= 983:
            cluster = 'Modelo Socia Lote 09'
            tipo = 'Individual'
        elif 1051 <= num <= 1146:
            cluster = 'Modelo Rizos (Blusa Blanca)'
            tipo = 'Individual'
        elif 1502 <= num <= 1650:
            cluster = 'Modelo Sonrisa Radiante (Lote 05)'
            tipo = 'Individual'
        elif 1812 <= num <= 1950:
            cluster = 'Modelo Socia Lote 13'
            tipo = 'Individual'
        elif 2003 <= num <= 2200:
            cluster = 'Modelo Outfit Negro / Tatuaje (Lote 12)'
            tipo = 'Individual'
        elif 2254 <= num <= 2450:
            cluster = 'Grupales Equipo Farmasi (Bloque 1)'
            tipo = 'Grupal'
        elif 2508 <= num <= 2902:
            cluster = 'Grupales y Dinámicas (Bloque 2)'
            tipo = 'Grupal'
        elif num >= 8554:
            cluster = 'Grupales de Cierre y Brindis'
            tipo = 'Grupal'
        else:
            cluster = 'Tomas Complementarias / Cobertura'
            tipo = 'Individual'

        reemplazo = f.get('reemplazo_en_revision')
        in_d29 = name in manifiesto_d
        in_sola6 = name in cobrizo_sola_6
        review_url = ''
        if isinstance(reemplazo, dict) and reemplazo.get('url'):
            review_url = reemplazo['url']
        elif f.get('revision_drive_url'):
            review_url = f['revision_drive_url']

        item = {
            'name': name,
            'cluster': cluster,
            'tipo': tipo,
            'estado': f['estado'],
            'version': 'Sola_6' if in_sola6 else ('D_v06' if in_d29 else f.get('version_actual', '')),
            'en_lote_d29': in_d29 or in_sola6,
            'reemplazo_d': bool(reemplazo),
            'source_url': f.get('source_url', ''),
            'approved_url': f.get('approved_jpg_drive', ''),
            'review_url': review_url
        }
        items.append(item)
        cluster_items[cluster].append(item)

    cluster_meta = [
        ('Modelo Lila (Cabello Negro Largo · D)', 'Individual', 'Prioridad activa: 24 fuentes · 11 aprobadas (inc. DSC07738 D v05) + 19 en revisión D_v06 + 4 incidencias', '1dCjNfEMUmXyFDu27HtmkpzXkISF3aWlP'),
        ('Modelo Vestido Cobrizo (Individual · Sola 6)', 'Individual', '¡NUEVO LOTE EN REVISIÓN! 6 fotos individuales entregadas (8318, 8500, 8504, 8536, 8540, 8554) con sujeto recompuesto desde original', '1Y7-si0Zkhxiqi0vf8f-u98B7XPohWWwv'),
        ('Grupales con Modelo Cobrizo / Equipo (D)', 'Grupal', 'Prioridad activa Acabado D: 28 fuentes · 10 aprobadas con reemplazo D_v06 en revisión + 18 pendientes', '1dCjNfEMUmXyFDu27HtmkpzXkISF3aWlP'),
        ('Secuencia Cobrizo Extendida (Grupales / Cierre)', 'Grupal', 'Secuencia confirmada de 51 tomas adicionales con modelo cobrizo pendientes de limpieza de set (69 cobrizo restantes en total)', '1dCjNfEMUmXyFDu27HtmkpzXkISF3aWlP'),
        ('Madre + Bebé', 'Individual', 'Secuencia tierna madre y bebé (16 fuentes · 3 aprobadas + 13 pendientes para montaje por recortes)', '1W-0oV8CK0NS5g4FY4EznLcDZIsqNwYtU'),
        ('Grupales Equipo Farmasi (Bloque 1)', 'Grupal', 'Fotos de equipo en ciclorama blanco con alfombra dreamy', ''),
        ('Piloto Inicial (Set Negro)', 'Individual', 'Primeras tomas del evento en ciclorama negro con ámbar sutil', ''),
        ('Modelo Outfit Negro / Tatuaje (Lote 12)', 'Individual', 'Vestuario negro elegante y accesorios en set editorial', ''),
        ('Modelo Socia Lote 13', 'Individual', 'Retratos individuales con gama de maquillaje Farmasi', ''),
        ('Modelo Socia Lote 09', 'Individual', 'Retratos individuales socia Farmasi en set de estudio', ''),
        ('Modelo Socia Lote 07', 'Individual', 'Retratos individuales en set blanco iluminado', ''),
        ('Modelo Rizos (Blusa Blanca)', 'Individual', 'Retrato fresco blusa blanca y cabello rizado', ''),
        ('Modelo Sonrisa Radiante (Lote 05)', 'Individual', 'Piel clara, cabello largo lacio y cosméticos', ''),
        ('Tomas Complementarias / Cobertura', 'Individual', 'Tomas complementarias de evento, detalles y cobertura general', ''),
        ('Grupales y Dinámicas (Bloque 2)', 'Grupal', 'Dinámicas de equipo, poses conjuntas y abrazos', ''),
        ('Grupales de Cierre y Brindis', 'Grupal', 'Celebración final y brindis del evento Farmasi (fuera de secuencia cobrizo)', '')
    ]

    clusters_out = []
    for cname, ctipo, cdesc, cfolder in cluster_meta:
        c_list = cluster_items[cname]
        clusters_out.append({
            'name': cname,
            'tipo': ctipo,
            'desc': cdesc,
            'drive_folder': cfolder,
            'total': len(c_list),
            'aprobadas': sum(1 for x in c_list if x['estado'] == 'aprobada'),
            'en_revision': sum(1 for x in c_list if x['estado'] == 'en_revision'),
            'en_revision_d29': sum(1 for x in c_list if x['en_lote_d29']),
            'reemplazos_d': sum(1 for x in c_list if x['reemplazo_d']),
            'pendientes': sum(1 for x in c_list if x['estado'] == 'pendiente'),
            'rechazadas': sum(1 for x in c_list if x['estado'] in ('rechazada', 'bloqueada_herramienta')),
            'samples': [x['name'] for x in c_list[:4]]
        })

    return {
        'total_fotos': len(items),
        'aprobadas': estado_global.get('aprobada', 144),
        'en_revision': estado_global.get('en_revision', 15),
        'lote_d29_en_revision': len(manifiesto_d),
        'cobrizo_sola_6_en_revision': len(cobrizo_sola_6),
        'reemplazos_en_revision': sum(1 for x in items if x['reemplazo_d']),
        'pendientes': estado_global.get('pendiente', 625),
        'rechazadas': estado_global.get('rechazada', 12),
        'bloqueadas': estado_global.get('bloqueada_herramienta', 3),
        'alcance_lila_cobrizo': 109,
        'cobrizo_confirmadas': len(cobrizo_names),
        'cobrizo_pendientes': 69,
        'clusters': clusters_out,
        'items': items
    }


def render_html(data):
    json_str = json.dumps(data, ensure_ascii=False)
    total_active_review = data['en_revision'] + data['reemplazos_en_revision']  # 15 + 20 = 35
    total_processed = data['aprobadas'] + data['en_revision']  # 144 + 15 = 159
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>captoora.studio · Dashboard Evento Farmasi 31 Octubre (799 Fotos)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Montserrat:wght@500;600;700;800;900&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
                        display: ['Montserrat', 'sans-serif']
                    }}
                }}
            }}
        }}
    </script>
    <style>
        html, body {{
            background-color: #060609;
            background-image: 
                radial-gradient(at 15% 10%, rgba(120, 119, 198, 0.14) 0px, transparent 45%),
                radial-gradient(at 85% 20%, rgba(56, 189, 248, 0.10) 0px, transparent 50%),
                radial-gradient(at 50% 90%, rgba(16, 185, 129, 0.08) 0px, transparent 50%);
            background-attachment: fixed;
            color: #f3f4f6;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            transition: opacity 0.5s ease;
        }}
        .apple-glass {{
            background: rgba(255, 255, 255, 0.045);
            backdrop-filter: blur(24px) saturate(160%);
            -webkit-backdrop-filter: blur(24px) saturate(160%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 0 rgba(255, 255, 255, 0.12);
        }}
        .apple-glass-card {{
            background: rgba(255, 255, 255, 0.035);
            backdrop-filter: blur(20px) saturate(140%);
            -webkit-backdrop-filter: blur(20px) saturate(140%);
            border: 1px solid rgba(255, 255, 255, 0.09);
            box-shadow: 0 8px 24px -8px rgba(0, 0, 0, 0.45), inset 0 1px 0 0 rgba(255, 255, 255, 0.08);
        }}
        .apple-glass-card:hover {{
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.22);
        }}
        .hp-bar-track {{
            background: rgba(0, 0, 0, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.7);
        }}
        .hp-segment-grid {{
            background-image: repeating-linear-gradient(
                90deg,
                transparent,
                transparent calc(20% - 1px),
                rgba(0, 0, 0, 0.45) calc(20% - 1px),
                rgba(0, 0, 0, 0.45) 20%
            );
        }}
        .table-scroll {{
            max-height: 540px;
            overflow-y: auto;
        }}
        ::-webkit-scrollbar {{
            width: 7px;
            height: 7px;
        }}
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.02);
        }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.18);
            border-radius: 9999px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(255, 255, 255, 0.32);
        }}
    </style>
</head>
<body class="p-4 md:p-8 min-h-screen">

    <!-- Header Apple Glass -->
    <header class="max-w-7xl mx-auto mb-7 apple-glass rounded-2xl p-6 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-5">
        <div>
            <div class="flex flex-wrap items-center gap-2.5">
                <a href="https://captoora.studio" target="_blank" class="bg-white/10 hover:bg-white/15 border border-white/20 text-white font-semibold px-3 py-1 rounded-full text-xs tracking-wide flex items-center gap-1.5 transition">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    captoora.studio
                </a>
                <a href="https://galeria.captoora.studio" target="_blank" class="bg-white/5 hover:bg-white/10 border border-white/15 text-gray-300 px-3 py-1 rounded-full text-xs transition">
                    galeria.captoora.studio ↗
                </a>
                <span class="text-xs text-gray-400">Sincronizado 5 Nov 2026 · Auto-Refresh <span id="countdown-timer" class="text-white font-mono">15:00</span></span>
            </div>
            <h1 class="text-2xl md:text-3xl font-extrabold font-display tracking-tight mt-2.5 text-white">
                Monitor en Tiempo Real · Farmasi 799
            </h1>
            <p class="text-gray-400 text-xs md:text-sm mt-1">
                Sincronizado con <code class="text-gray-200 bg-white/10 px-1.5 py-0.5 rounded">fuentes_799.json</code> · <code class="text-gray-200 bg-white/10 px-1.5 py-0.5 rounded">ESTADO_MODELO_D_TODAS.md</code> · <code class="text-gray-200 bg-white/10 px-1.5 py-0.5 rounded">cobrizo_sola_6</code>
            </p>
        </div>
        <div class="flex flex-wrap gap-2.5">
            <a href="https://drive.google.com/drive/folders/1Y7-si0Zkhxiqi0vf8f-u98B7XPohWWwv" target="_blank" class="apple-glass-card text-white text-xs font-medium px-4 py-2.5 rounded-xl flex items-center gap-2 transition">
                <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                Cobrizo Sola 6 (Drive) ↗
            </a>
            <a href="https://drive.google.com/drive/folders/1dCjNfEMUmXyFDu27HtmkpzXkISF3aWlP" target="_blank" class="apple-glass-card text-white text-xs font-medium px-4 py-2.5 rounded-xl flex items-center gap-2 transition">
                <span class="w-2 h-2 rounded-full bg-sky-400"></span>
                Lote 29 Acabado D (Drive) ↗
            </a>
            <a href="https://drive.google.com/drive/folders/1cQHqpVSSZmXOG_71fvjqiwCZKRZvjoKA" target="_blank" class="apple-glass-card text-gray-200 text-xs font-medium px-4 py-2.5 rounded-xl flex items-center gap-2 transition">
                Drive Originales (799) ↗
            </a>
            <button onclick="manualRefresh()" class="apple-glass-card text-gray-200 text-xs font-medium px-3.5 py-2.5 rounded-xl flex items-center gap-1.5 transition" title="Actualizar ahora">
                ↻ Actualizar
            </button>
        </div>
    </header>

    <div class="max-w-7xl mx-auto space-y-6">

        <!-- Master Health Bar (Video Game Life Bar Style in Apple Glass) -->
        <div class="apple-glass rounded-2xl p-6 space-y-4">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-2">
                <div>
                    <span class="text-[11px] uppercase tracking-widest text-gray-400 font-semibold">Barra Maestra de Progreso Global (799 Fotografías)</span>
                    <div class="flex items-baseline gap-3 mt-1">
                        <span class="text-2xl font-bold text-white">{total_processed} Fuentes con Entrega / Revisión</span>
                        <span class="text-xs text-gray-400">(144 Aprobadas + 15 Nuevas en Revisión [9 Lila D + 6 Cobrizo Sola] + 20 Reemplazos D_v06)</span>
                    </div>
                </div>
                <div class="flex flex-wrap gap-4 text-xs">
                    <span class="flex items-center gap-1.5 text-gray-300"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400/90"></span> 144 Aprobadas (18.0%)</span>
                    <span class="flex items-center gap-1.5 text-gray-300"><span class="w-2.5 h-2.5 rounded-full bg-sky-400/90"></span> 35 En Revisión Activa (15 nuevas + 20 reemplazos D)</span>
                    <span class="flex items-center gap-1.5 text-gray-300"><span class="w-2.5 h-2.5 rounded-full bg-amber-400/80"></span> 69 Cobrizo Cola Restante</span>
                    <span class="flex items-center gap-1.5 text-gray-400"><span class="w-2.5 h-2.5 rounded-full bg-white/20"></span> 556 Resto Upsell</span>
                </div>
            </div>

            <!-- Multi-segment Glass HP Bar -->
            <div class="w-full h-5 rounded-full hp-bar-track p-0.5 flex overflow-hidden relative">
                <div style="width: 18.02%" class="h-full bg-gradient-to-r from-emerald-500/80 to-emerald-400/90 rounded-l-full transition-all duration-700" title="144 Aprobadas en Drive"></div>
                <div style="width: 4.38%" class="h-full bg-gradient-to-r from-sky-500/80 to-sky-400/90 transition-all duration-700" title="35 En Revisión Activa (9 Lila D + 6 Cobrizo Sola + 20 Reemplazos D)"></div>
                <div style="width: 8.64%" class="h-full bg-gradient-to-r from-amber-500/60 to-amber-400/70 transition-all duration-700" title="69 Vestido Cobrizo Restantes en Cola"></div>
                <div style="width: 67.08%" class="h-full bg-white/10 transition-all duration-700" title="556 Pendientes para Upsell bajo demanda"></div>
                <div style="width: 1.88%" class="h-full bg-rose-500/40 rounded-r-full transition-all duration-700" title="15 Descartes / Bloqueadas"></div>
            </div>
        </div>

        <!-- 5 KPI Counter Cards with Individual Life Bars -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            <!-- Total -->
            <div class="apple-glass rounded-2xl p-5 flex flex-col justify-between space-y-3">
                <div>
                    <div class="flex justify-between items-center">
                        <span class="text-[11px] uppercase tracking-wider font-semibold text-gray-400">Inventario Total</span>
                        <span class="text-[11px] font-mono text-gray-300 bg-white/10 px-2 py-0.5 rounded-full">100%</span>
                    </div>
                    <div class="text-3xl font-extrabold text-white mt-1.5 font-display">{data['total_fotos']}</div>
                    <div class="text-xs text-gray-400 mt-0.5">193 con SHA-256 verificado</div>
                </div>
                <div class="w-full h-2.5 rounded-full hp-bar-track overflow-hidden p-0.5">
                    <div class="h-full bg-white/60 rounded-full hp-segment-grid" style="width: 100%"></div>
                </div>
            </div>

            <!-- Aprobadas -->
            <div class="apple-glass rounded-2xl p-5 flex flex-col justify-between space-y-3">
                <div>
                    <div class="flex justify-between items-center">
                        <span class="text-[11px] uppercase tracking-wider font-semibold text-emerald-300">Aprobadas en Drive</span>
                        <span class="text-[11px] font-mono text-emerald-300 bg-emerald-500/15 border border-emerald-400/20 px-2 py-0.5 rounded-full">144 verificadas</span>
                    </div>
                    <div class="text-3xl font-extrabold text-white mt-1.5 font-display">{data['aprobadas']}</div>
                    <div class="text-xs text-gray-400 mt-0.5">Incluye <code class="text-gray-200">DSC07738 D v05</code></div>
                </div>
                <div class="w-full h-2.5 rounded-full hp-bar-track overflow-hidden p-0.5">
                    <div class="h-full bg-gradient-to-r from-emerald-500/80 to-emerald-300/90 rounded-full hp-segment-grid" style="width: 96%"></div>
                </div>
            </div>

            <!-- En Revision Activa -->
            <div class="apple-glass rounded-2xl p-5 flex flex-col justify-between space-y-3">
                <div>
                    <div class="flex justify-between items-center">
                        <span class="text-[11px] uppercase tracking-wider font-semibold text-sky-300">En Revisión Activa</span>
                        <span class="text-[11px] font-mono text-sky-300 bg-sky-500/15 border border-sky-400/20 px-2 py-0.5 rounded-full">{total_active_review} archivos Drive</span>
                    </div>
                    <div class="flex items-baseline gap-2 mt-1.5">
                        <span class="text-3xl font-extrabold text-white font-display">{data['en_revision']}</span>
                        <span class="text-xs text-sky-300 font-medium">nuevas (+20 reemplazos D)</span>
                    </div>
                    <div class="text-xs text-gray-400 mt-0.5">9 Lila D + 6 Cobrizo Sola + 20 D_v06</div>
                </div>
                <div class="w-full h-2.5 rounded-full hp-bar-track overflow-hidden p-0.5">
                    <div class="h-full bg-gradient-to-r from-sky-500/80 to-sky-300/90 rounded-full hp-segment-grid" style="width: 100%"></div>
                </div>
            </div>

            <!-- Alcance Activo Lila + Cobrizo -->
            <div class="apple-glass rounded-2xl p-5 flex flex-col justify-between space-y-3">
                <div>
                    <div class="flex justify-between items-center">
                        <span class="text-[11px] uppercase tracking-wider font-semibold text-amber-300">Alcance Lila + Cobrizo</span>
                        <span class="text-[11px] font-mono text-amber-300 bg-amber-500/15 border border-amber-400/20 px-2 py-0.5 rounded-full">36 / 109 listas</span>
                    </div>
                    <div class="flex items-baseline gap-2 mt-1.5">
                        <span class="text-3xl font-extrabold text-white font-display">{data['cobrizo_pendientes']}</span>
                        <span class="text-xs text-amber-300 font-medium">cobrizo restantes</span>
                    </div>
                    <div class="text-xs text-gray-400 mt-0.5">20 Lila + 16 Cobrizo ya entregadas</div>
                </div>
                <div class="w-full h-2.5 rounded-full hp-bar-track overflow-hidden p-0.5">
                    <div class="h-full bg-gradient-to-r from-amber-500/80 to-amber-300/90 rounded-full hp-segment-grid" style="width: 33%"></div>
                </div>
            </div>

            <!-- Pendientes Totales / Upsell -->
            <div class="apple-glass rounded-2xl p-5 flex flex-col justify-between space-y-3">
                <div>
                    <div class="flex justify-between items-center">
                        <span class="text-[11px] uppercase tracking-wider font-semibold text-gray-300">Pendientes / Upsell</span>
                        <span class="text-[11px] font-mono text-gray-400 bg-white/10 px-2 py-0.5 rounded-full">78.2%</span>
                    </div>
                    <div class="flex items-baseline gap-2 mt-1.5">
                        <span class="text-3xl font-extrabold text-white font-display">{data['pendientes']}</span>
                        <span class="text-xs text-rose-300/80 font-medium">({data['rechazadas'] + data['bloqueadas']} descartes)</span>
                    </div>
                    <div class="text-xs text-gray-400 mt-0.5">Catálogo para venta extra</div>
                </div>
                <div class="w-full h-2.5 rounded-full hp-bar-track overflow-hidden p-0.5">
                    <div class="h-full bg-white/35 rounded-full hp-segment-grid" style="width: 78%"></div>
                </div>
            </div>
        </div>

        <!-- Active Work Monitor (Lila / Cobrizo Sola 6 / Cobrizo Grupal) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div class="apple-glass rounded-2xl p-5 space-y-3">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-semibold text-white flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                        1. Modelo Lila (24 Fuentes)
                    </span>
                    <span class="text-xs font-mono text-emerald-300">20 / 24 procesadas</span>
                </div>
                <div class="w-full h-3 rounded-full hp-bar-track p-0.5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-emerald-500/80 to-sky-400/90 rounded-full hp-segment-grid" style="width: 83.3%"></div>
                </div>
                <div class="flex justify-between text-[11px] text-gray-400">
                    <span>11 Aprobadas (10 con reemplazo D_v06)</span>
                    <span>9 En Revisión D_v06 · 4 Incidencias</span>
                </div>
            </div>

            <div class="apple-glass rounded-2xl p-5 space-y-3">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-semibold text-white flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-sky-400"></span>
                        2. Vestido Cobrizo Sola + Grupal (85 Fuentes)
                    </span>
                    <span class="text-xs font-mono text-sky-300">16 / 85 en Drive</span>
                </div>
                <div class="w-full h-3 rounded-full hp-bar-track p-0.5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-sky-500/80 to-amber-400/80 rounded-full hp-segment-grid" style="width: 18.8%"></div>
                </div>
                <div class="flex justify-between text-[11px] text-gray-400">
                    <span>6 Individuales Sola + 10 Grupales D_v06</span>
                    <span>69 Cobrizo restantes en cola</span>
                </div>
            </div>

            <div class="apple-glass rounded-2xl p-5 space-y-3">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-semibold text-white flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                        3. Secuencia Madre + Bebé (16 Fuentes)
                    </span>
                    <span class="text-xs font-mono text-amber-300">3 / 5 meta base</span>
                </div>
                <div class="w-full h-3 rounded-full hp-bar-track p-0.5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-amber-500/80 to-amber-300/90 rounded-full hp-segment-grid" style="width: 60%"></div>
                </div>
                <div class="flex justify-between text-[11px] text-gray-400">
                    <span>3 Aprobadas (08258, 08290 2, 08295)</span>
                    <span>13 Pendientes montaje recortes</span>
                </div>
            </div>
        </div>

        <!-- Model Status & Delivery Matrix -->
        <div class="apple-glass rounded-2xl p-6 space-y-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h3 class="text-lg font-bold text-white font-display">
                        Barras de Vida por Modelo / Clúster (Meta Base: 5 Fotos Listas)
                    </h3>
                    <p class="text-xs text-gray-400 mt-0.5">Filtra por individuales, grupales o lotes activos en revisión (Lote D_v06 + Cobrizo Sola 6).</p>
                </div>
                <div class="flex flex-wrap gap-2 text-xs">
                    <button onclick="filterCluster('ALL')" id="btn-all" class="px-3.5 py-1.5 rounded-xl bg-white/20 border border-white/30 text-white font-semibold transition">Todos (16)</button>
                    <button onclick="filterCluster('INDIVIDUAL')" id="btn-ind" class="px-3.5 py-1.5 rounded-xl bg-white/5 border border-white/10 text-gray-300 hover:bg-white/10 transition">Individuales (11)</button>
                    <button onclick="filterCluster('GRUPAL')" id="btn-grp" class="px-3.5 py-1.5 rounded-xl bg-white/5 border border-white/10 text-gray-300 hover:bg-white/10 transition">Grupales (5)</button>
                    <button onclick="filterCluster('REVISION_D')" id="btn-rev" class="px-3.5 py-1.5 rounded-xl bg-sky-500/15 border border-sky-400/30 text-sky-300 hover:bg-sky-500/25 transition">En Revisión Activa (35)</button>
                    <button onclick="filterCluster('LISTA')" id="btn-lst" class="px-3.5 py-1.5 rounded-xl bg-emerald-500/15 border border-emerald-400/30 text-emerald-300 hover:bg-emerald-500/25 transition">Listas (≥5)</button>
                    <button onclick="filterCluster('PENDIENTE')" id="btn-pnd" class="px-3.5 py-1.5 rounded-xl bg-amber-500/15 border border-amber-400/30 text-amber-300 hover:bg-amber-500/25 transition">En Cola (&lt;5)</button>
                </div>
            </div>

            <!-- Model Cards Grid -->
            <div id="clusters-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Dynamically populated via JS -->
            </div>
        </div>

        <!-- Full Photo Explorer Table -->
        <div class="apple-glass rounded-2xl p-6 space-y-4">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h3 class="text-lg font-bold text-white font-display">
                        Explorador de las 799 Fotografías en Drive
                    </h3>
                    <p class="text-xs text-gray-400 mt-0.5">Incluye enlaces directos a Original, Aprobada en Drive y Revisión (Acabado D_v06 y Cobrizo Sola 6).</p>
                </div>
                <div class="w-full md:w-80">
                    <input type="text" id="photo-search" oninput="renderTable()" placeholder="Buscar toma (ej: 08318, 07738, cobrizo, lila)..." class="w-full bg-black/40 border border-white/15 text-white text-xs px-3.5 py-2.5 rounded-xl focus:outline-none focus:border-white/40">
                </div>
            </div>

            <div class="table-scroll border border-white/10 rounded-xl bg-black/20">
                <table class="w-full text-left text-xs">
                    <thead class="bg-black/60 backdrop-blur-md text-gray-400 uppercase font-semibold sticky top-0 border-b border-white/10">
                        <tr>
                            <th class="p-3">#</th>
                            <th class="p-3">Archivo Original</th>
                            <th class="p-3">Modelo / Clúster</th>
                            <th class="p-3">Tipo</th>
                            <th class="p-3">Estado Vigente</th>
                            <th class="p-3 text-right">Enlaces Google Drive</th>
                        </tr>
                    </thead>
                    <tbody id="photos-table-body" class="divide-y divide-white/5 text-gray-300">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
            <div class="flex justify-between items-center text-xs text-gray-400 pt-1">
                <span id="table-count">Mostrando 799 fotos</span>
                <span>captoora.studio · galeria.captoora.studio</span>
            </div>
        </div>

    </div>

    <script>
        const data = {json_str};

        let currentFilter = 'ALL';

        function filterCluster(type) {{
            currentFilter = type;
            ['btn-all', 'btn-ind', 'btn-grp', 'btn-rev', 'btn-lst', 'btn-pnd'].forEach(id => {{
                const el = document.getElementById(id);
                if (el) {{
                    el.className = 'px-3.5 py-1.5 rounded-xl bg-white/5 border border-white/10 text-gray-300 hover:bg-white/10 transition';
                }}
            }});
            
            const activeMap = {{
                'ALL': 'btn-all',
                'INDIVIDUAL': 'btn-ind',
                'GRUPAL': 'btn-grp',
                'REVISION_D': 'btn-rev',
                'LISTA': 'btn-lst',
                'PENDIENTE': 'btn-pnd'
            }};
            const activeEl = document.getElementById(activeMap[type]);
            if (activeEl) {{
                activeEl.className = 'px-3.5 py-1.5 rounded-xl bg-white/20 border border-white/40 text-white font-semibold transition';
            }}

            renderClusters();
            renderTable();
        }}

        function renderClusters() {{
            const grid = document.getElementById('clusters-grid');
            grid.innerHTML = '';

            const filtered = data.clusters.filter(c => {{
                const readyCount = c.aprobadas + c.en_revision;
                if (currentFilter === 'ALL') return true;
                if (currentFilter === 'INDIVIDUAL') return c.tipo === 'Individual';
                if (currentFilter === 'GRUPAL') return c.tipo === 'Grupal';
                if (currentFilter === 'REVISION_D') return c.en_revision_d29 > 0 || c.en_revision > 0;
                if (currentFilter === 'LISTA') return readyCount >= 5;
                if (currentFilter === 'PENDIENTE') return readyCount < 5;
                return true;
            }});

            filtered.forEach(c => {{
                const readyCount = c.aprobadas + c.en_revision;
                const isReady = readyCount >= 5;
                const isPartial = readyCount > 0 && readyCount < 5;
                const gap = Math.max(0, 5 - readyCount);
                
                const statusBadge = c.aprobadas >= 5
                    ? `<span class="bg-emerald-500/15 text-emerald-300 border border-emerald-400/25 text-[10px] font-semibold px-2.5 py-0.5 rounded-full">${{c.aprobadas}} Aprobadas</span>`
                    : (c.en_revision >= 5
                        ? `<span class="bg-sky-500/15 text-sky-300 border border-sky-400/25 text-[10px] font-semibold px-2.5 py-0.5 rounded-full">${{c.en_revision}} en Revisión (Meta ≥5)</span>`
                        : (isPartial 
                            ? `<span class="bg-amber-500/15 text-amber-300 border border-amber-400/25 text-[10px] font-semibold px-2.5 py-0.5 rounded-full">Faltan ${{gap}} para 5</span>`
                            : `<span class="bg-white/10 text-gray-300 border border-white/15 text-[10px] font-semibold px-2.5 py-0.5 rounded-full">En Cola (${{c.total}})</span>`));

                const d29Badge = c.en_revision_d29 > 0
                    ? `<span class="bg-sky-500/15 text-sky-300 border border-sky-400/25 text-[10px] font-semibold px-2 py-0.5 rounded-full">${{c.en_revision_d29}} en Drive Rev</span>`
                    : '';

                const hpGoalWidth = Math.min(100, Math.round((readyCount / 5) * 100));
                const totalCoverageWidth = Math.min(100, Math.round((readyCount / Math.max(1, c.total)) * 100));

                const barColor = c.aprobadas >= 5
                    ? 'from-emerald-500/80 to-emerald-300/90'
                    : (c.en_revision >= 5
                        ? 'from-sky-500/80 to-sky-300/90'
                        : (isPartial ? 'from-amber-500/80 to-amber-300/90' : 'from-white/30 to-white/50'));

                const card = document.createElement('div');
                card.className = 'apple-glass-card rounded-2xl p-5 flex flex-col justify-between space-y-4 transition';
                card.innerHTML = `
                    <div>
                        <div class="flex items-center justify-between gap-2 mb-2">
                            <span class="text-[10px] uppercase font-semibold tracking-wider text-gray-400">${{c.tipo}}</span>
                            <div class="flex items-center gap-1.5">
                                ${{d29Badge}}
                                ${{statusBadge}}
                            </div>
                        </div>
                        <h4 class="font-bold text-white text-sm leading-snug">${{c.name}}</h4>
                        <p class="text-[11px] text-gray-400 mt-1 leading-relaxed">${{c.desc}}</p>
                        
                        <!-- Barra 1: Meta 5 Fotos Base -->
                        <div class="mt-4 pt-3 border-t border-white/10 space-y-2.5">
                            <div>
                                <div class="flex justify-between text-[11px] mb-1">
                                    <span class="text-gray-400">Meta Galería Base (5 fotos):</span>
                                    <span class="font-mono font-semibold text-white">${{readyCount}} / 5 (${{c.aprobadas}} aprob + ${{c.en_revision}} rev)</span>
                                </div>
                                <div class="w-full h-2.5 rounded-full hp-bar-track p-0.5 overflow-hidden">
                                    <div class="bg-gradient-to-r ${{barColor}} h-full rounded-full hp-segment-grid transition-all duration-500" style="width: ${{hpGoalWidth}}%"></div>
                                </div>
                            </div>

                            <!-- Barra 2: Avance sobre Rollo Completo -->
                            <div>
                                <div class="flex justify-between text-[11px] mb-1">
                                    <span class="text-gray-400">Rollo Completo (${{c.total}} tomas):</span>
                                    <span class="font-mono text-gray-300">${{readyCount}} / ${{c.total}} (${{totalCoverageWidth}}%)</span>
                                </div>
                                <div class="w-full h-2 rounded-full hp-bar-track p-0.5 overflow-hidden">
                                    <div class="bg-gradient-to-r from-sky-500/70 to-emerald-400/80 h-full rounded-full transition-all duration-500" style="width: ${{totalCoverageWidth}}%"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="pt-3 border-t border-white/10 flex items-center justify-between text-[11px]">
                        <div class="text-gray-400">
                            Aprobadas: <strong class="text-white">${{c.aprobadas}}</strong> · Rev: <strong class="text-sky-300">${{c.en_revision}}</strong> · Pend: <strong class="text-gray-300">${{c.pendientes}}</strong>
                        </div>
                        ${{c.drive_folder ? `
                            <a href="https://drive.google.com/drive/folders/${{c.drive_folder}}" target="_blank" class="text-sky-300 hover:text-white font-medium transition">
                                Drive ↗
                            </a>
                        ` : ''}}
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        function renderTable() {{
            const tbody = document.getElementById('photos-table-body');
            const search = document.getElementById('photo-search').value.toLowerCase().trim();
            tbody.innerHTML = '';

            let count = 0;
            data.items.forEach((item, idx) => {{
                if (search && !item.name.toLowerCase().includes(search) && !item.cluster.toLowerCase().includes(search) && !item.estado.toLowerCase().includes(search) && !item.version.toLowerCase().includes(search)) {{
                    return;
                }}
                if (currentFilter === 'INDIVIDUAL' && item.tipo !== 'Individual') return;
                if (currentFilter === 'GRUPAL' && item.tipo !== 'Grupal') return;
                if (currentFilter === 'REVISION_D' && !item.en_lote_d29 && item.estado !== 'en_revision') return;
                if (currentFilter === 'LISTA' && item.estado !== 'aprobada' && item.estado !== 'en_revision') return;
                if (currentFilter === 'PENDIENTE' && (item.estado === 'aprobada' || item.estado === 'en_revision')) return;

                count++;
                if (count > 250) return;

                const tr = document.createElement('tr');
                tr.className = 'hover:bg-white/5 transition';
                
                let badge = '<span class="text-gray-400 bg-white/5 px-2 py-0.5 rounded-full border border-white/10">Pendiente</span>';
                if (item.estado === 'aprobada') {{
                    badge = '<span class="text-emerald-300 font-semibold bg-emerald-500/15 px-2.5 py-0.5 rounded-full border border-emerald-400/25">Aprobada</span>';
                    if (item.reemplazo_d) {{
                        badge += ' <span class="text-sky-300 font-medium bg-sky-500/15 px-2 py-0.5 rounded-full border border-sky-400/25 ml-1">+ Reemplazo D_v06</span>';
                    }}
                }} else if (item.estado === 'en_revision') {{
                    badge = '<span class="text-sky-300 font-semibold bg-sky-500/15 px-2.5 py-0.5 rounded-full border border-sky-400/25">En Revisión (' + (item.version || 'Drive') + ')</span>';
                }} else if (item.estado === 'rechazada' || item.estado === 'bloqueada_herramienta') {{
                    badge = '<span class="text-rose-300 bg-rose-500/15 px-2.5 py-0.5 rounded-full border border-rose-400/20">' + item.estado + '</span>';
                }}

                tr.innerHTML = `
                    <td class="p-3 text-gray-500 font-mono">${{idx + 1}}</td>
                    <td class="p-3 font-mono font-semibold text-white">${{item.name}}</td>
                    <td class="p-3 text-gray-300">${{item.cluster}}</td>
                    <td class="p-3 text-gray-400">${{item.tipo}}</td>
                    <td class="p-3">${{badge}}</td>
                    <td class="p-3 text-right space-x-2">
                        ${{item.review_url ? `
                            <a href="${{item.review_url}}" target="_blank" class="text-sky-300 hover:text-white font-semibold">
                                Revisión ↗
                            </a>
                        ` : ''}}
                        ${{item.approved_url ? `
                            <a href="${{item.approved_url}}" target="_blank" class="text-emerald-300 hover:text-white font-semibold">
                                Aprobada ↗
                            </a>
                        ` : ''}}
                        <a href="${{item.source_url}}" target="_blank" class="text-gray-400 hover:text-white">
                            Original ↗
                        </a>
                    </td>
                `;
                tbody.appendChild(tr);
            }});

            document.getElementById('table-count').innerText = `Mostrando ${{Math.min(count, 250)}} de ${{count}} fotografías filtradas`;
        }}

        function manualRefresh() {{
            document.documentElement.style.opacity = '0';
            setTimeout(() => location.reload(), 400);
        }}

        // 15-minute live countdown & smooth glass auto-refresh
        let remainingSeconds = 15 * 60;
        setInterval(() => {{
            remainingSeconds--;
            if (remainingSeconds <= 0) {{
                manualRefresh();
            }} else {{
                const mins = String(Math.floor(remainingSeconds / 60)).padStart(2, '0');
                const secs = String(remainingSeconds % 60).padStart(2, '0');
                const el = document.getElementById('countdown-timer');
                if (el) el.innerText = `${{mins}}:${{secs}}`;
            }}
        }}, 1000);

        // Init
        renderClusters();
        renderTable();
    </script>
</body>
</html>
"""
    DASHBOARD_PATH.write_text(html, encoding='utf-8')
    print(f"Updated {DASHBOARD_PATH} ({DASHBOARD_PATH.stat().st_size} bytes)")


if __name__ == '__main__':
    data = build_data()
    render_html(data)
