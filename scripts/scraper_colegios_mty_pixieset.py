# -*- coding: utf-8 -*-
"""
Scraper & Verificador B2B de Colegios, Preescolares, Academias y Clubes en Monterrey / SPGG
para Campañas de Correo en Pixieset (Studio Manager & Gallery Invites).
"""
import concurrent.futures
import csv
import json
import pathlib
import re
import socket
import ssl
import subprocess
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "campaigns" / "operacion-comercial"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

SEED_INSTITUTIONS = [
    # 1. Colinas de San Jerónimo / Monterrey Poniente (A 5 min del Estudio Captoora en Paseo de los Álamos 165)
    {"nombre": "Viget Kindergarten", "zona": "Colinas de San Jerónimo", "categoria": "Kinder / Preescolar", "web": "https://www.viget.com.mx", "contacto_url": "https://www.viget.com.mx/contacto", "correo_base": "admisiones@institutoviget.com.mx", "telefono": "8121930551"},
    {"nombre": "Instituto San Jerónimo (ISJ)", "zona": "San Jerónimo / Monterrey", "categoria": "Colegio K-12", "web": "https://www.isj.edu.mx", "contacto_url": "https://www.isj.edu.mx", "correo_base": "informes@isj.edu.mx", "telefono": "8112888152"},
    {"nombre": "Colegio Montessori de Monterrey", "zona": "San Jerónimo / Monterrey", "categoria": "Colegio Montessori", "web": "https://www.montessoridemty.edu.mx", "contacto_url": "https://www.montessoridemty.edu.mx/contacto", "correo_base": "montessoridemonterrey@gmail.com", "telefono": "8183483796"},
    {"nombre": "Kinder Little Town Puerta del Sol", "zona": "Colinas de San Jerónimo", "categoria": "Kinder / Preescolar", "web": "https://kinderlittletown.com", "contacto_url": "https://kinderlittletown.com", "correo_base": "sanjeronimo@kinderlittletown.com", "telefono": "8183150298"},
    {"nombre": "Instituto Franco Mexicano (Campus San Jerónimo / SPGG)", "zona": "Colinas de San Jerónimo / SPGG", "categoria": "Colegio Privado", "web": "https://www.ifm.edu.mx", "contacto_url": "https://www.ifm.edu.mx", "correo_base": "admisiones@ifm.edu.mx", "telefono": "8122001951"},
    {"nombre": "Colegio Mexicano", "zona": "San Jerónimo / Del Valle", "categoria": "Colegio Bilingüe", "web": "https://www.colegiomexicano.edu.mx", "contacto_url": "https://www.colegiomexicano.edu.mx", "correo_base": "informes@colegiomexicano.edu.mx", "telefono": "8120797221"},

    # 2. San Pedro Garza García / Valle Poniente / Valle Oriente (Ticket Alto VIP)
    {"nombre": "Colegio Inglés de Monterrey", "zona": "San Pedro Garza García", "categoria": "Colegio Bilingüe VIP", "web": "https://www.colegioingles.edu.mx", "contacto_url": "https://www.colegioingles.edu.mx", "correo_base": "admisiones@colegioingles.edu.mx", "telefono": "8180477000"},
    {"nombre": "Instituto San Roberto (ISR)", "zona": "San Pedro / Valle Alto", "categoria": "Colegio Internacional VIP", "web": "https://www.sanroberto.edu.mx", "contacto_url": "https://www.sanroberto.edu.mx", "correo_base": "admisionessa@sanroberto.edu.mx", "telefono": "8180002158"},
    {"nombre": "American School Foundation of Monterrey (ASFM)", "zona": "Valle Poniente / SPGG", "categoria": "Colegio Internacional VIP", "web": "https://www.asfm.edu.mx", "contacto_url": "https://www.asfm.edu.mx", "correo_base": "admissions@asfm.edu.mx", "telefono": "8182884400"},
    {"nombre": "Colegio Euroamericano Monterrey", "zona": "San Pedro / Valle Oriente", "categoria": "Colegio Bilingüe VIP", "web": "https://www.euroamericano.edu.mx", "contacto_url": "https://www.euroamericano.edu.mx", "correo_base": "admisiones@euroamericano.edu.mx", "telefono": "8182488400"},
    {"nombre": "Instituto Brillamont", "zona": "San Pedro Garza García", "categoria": "Colegio Bilingüe VIP", "web": "https://www.brillamont.edu.mx", "contacto_url": "https://www.brillamont.edu.mx", "correo_base": "admisiones@brillamont.edu.mx", "telefono": "8121170005"},
    {"nombre": "Instituto Mater", "zona": "San Pedro Garza García", "categoria": "Colegio Privado VIP", "web": "https://www.mater.edu.mx", "contacto_url": "https://www.mater.edu.mx", "correo_base": "admisiones@mater.edu.mx", "telefono": "8134039835"},
    {"nombre": "Colegio Labastida", "zona": "San Pedro Garza García", "categoria": "Colegio Privado", "web": "https://www.labastida.edu.mx", "contacto_url": "https://www.labastida.edu.mx", "correo_base": "admisiones@labastida.edu.mx", "telefono": "8183354530"},
    {"nombre": "Instituto Irlandés de Monterrey", "zona": "San Pedro Garza García", "categoria": "Colegio Internacional VIP", "web": "https://www.irlandesmonterrey.com", "contacto_url": "https://www.irlandesmonterrey.com", "correo_base": "admisiones@irlandesmonterrey.com", "telefono": "8183631202"},
    {"nombre": "Colegio Himalaya Monterrey", "zona": "San Pedro Garza García", "categoria": "Colegio Internacional VIP", "web": "https://www.himalaya.edu.mx", "contacto_url": "https://www.himalaya.edu.mx", "correo_base": "admisiones@himalaya.edu.mx", "telefono": "8183384900"},
    {"nombre": "Colegio Necali / Eurocampestre", "zona": "San Pedro Garza García", "categoria": "Colegio Privado", "web": "https://www.necali.edu.mx", "contacto_url": "https://www.necali.edu.mx", "correo_base": "admisiones@eurocampestre.edu.mx", "telefono": "8116113101"},
    {"nombre": "Liceo de Monterrey", "zona": "San Pedro / Valle Oriente", "categoria": "Colegio Bilingüe VIP", "web": "https://www.liceodemonterrey.edu.mx", "contacto_url": "https://www.liceodemonterrey.edu.mx", "correo_base": "admisiones@liceodemonterrey.edu.mx", "telefono": "8181532100"},
    {"nombre": "Colegio Montealban", "zona": "San Pedro / Monterrey", "categoria": "Kinder y Primaria", "web": "https://www.colegiomontealban.edu.mx", "contacto_url": "https://www.colegiomontealban.edu.mx", "correo_base": "informes@colegiomontealban.edu.mx", "telefono": "8183334050"},
    {"nombre": "Formus / Instituto Formus", "zona": "San Pedro / Valle Poniente", "categoria": "Colegio Privado", "web": "https://www.formus.edu.mx", "contacto_url": "https://www.formus.edu.mx", "correo_base": "admisiones@formus.edu.mx", "telefono": "8181245600"},

    # 3. Cumbres / Obispado / Zona Poniente (Muy cerca de San Jerónimo)
    {"nombre": "Pan American School of Monterrey (PAS)", "zona": "Cumbres / Centro / Carretera Nac.", "categoria": "Colegio Internacional", "web": "https://www.pas.edu.mx", "contacto_url": "https://www.pas.edu.mx", "correo_base": "admissions@panamerican.edu.mx", "telefono": "8181300900"},
    {"nombre": "Colegio San Patricio Monterrey", "zona": "Cumbres / Del Paseo", "categoria": "Colegio Bilingüe", "web": "https://www.sanpatricio.edu.mx", "contacto_url": "https://www.sanpatricio.edu.mx", "correo_base": "admisiones@sanpatricio.edu.mx", "telefono": "8111339101"},
    {"nombre": "Cambridge College Monterrey", "zona": "Cumbres / Mitras", "categoria": "Colegio Bilingüe", "web": "https://www.cambridge.edu.mx", "contacto_url": "https://www.cambridge.edu.mx", "correo_base": "informacion@cambridge.edu.mx", "telefono": "8181234040"},
    {"nombre": "Instituto Motolinía Monterrey", "zona": "Obispado / Cumbres", "categoria": "Colegio Privado", "web": "https://www.motolinia.edu.mx", "contacto_url": "https://www.motolinia.edu.mx", "correo_base": "informes@motolinia.edu.mx", "telefono": "8156797418"},
    {"nombre": "Instituto Edinburgh", "zona": "Cumbres / San Nicolás", "categoria": "Colegio Bilingüe", "web": "https://www.edinburgh.edu.mx", "contacto_url": "https://www.edinburgh.edu.mx", "correo_base": "info@edinburgh.edu.mx", "telefono": "8121338370"},
    {"nombre": "Instituto Anglo Británico", "zona": "Cumbres / Carretera Nacional", "categoria": "Colegio Internacional IB", "web": "https://www.anglobritanico.edu.mx", "contacto_url": "https://www.anglobritanico.edu.mx", "correo_base": "admisiones@anglobritanico.edu.mx", "telefono": "8183004050"},
    {"nombre": "Colegio Madison Monterrey", "zona": "Cumbres / Carretera Nacional", "categoria": "Colegio Internacional IB", "web": "https://www.colegiomadison.edu.mx", "contacto_url": "https://www.colegiomadison.edu.mx", "correo_base": "admisionesmty@colegiomadison.edu.mx", "telefono": "8181041140"},
    {"nombre": "Instituto Regiomontano Cumbres", "zona": "Cumbres / Chepevera", "categoria": "Colegio Lasallista", "web": "https://www.ircumbres.edu.mx", "contacto_url": "https://www.ircumbres.edu.mx", "correo_base": "admisiones@ircumbres.edu.mx", "telefono": "8183460500"},
    {"nombre": "Colegio Naciones Unidas", "zona": "Cumbres / Monterrey", "categoria": "Colegio Bilingüe", "web": "https://www.cnu.edu.mx", "contacto_url": "https://www.cnu.edu.mx", "correo_base": "informes@cnu.edu.mx", "telefono": "8183001234"},

    # 4. Contry / Sur / Carretera Nacional
    {"nombre": "Colegio Regiomontano Contry", "zona": "Contry / Sur Monterrey", "categoria": "Colegio Lasallista", "web": "https://www.regiocontry.edu.mx", "contacto_url": "https://www.regiocontry.edu.mx", "correo_base": "recepcion@regiocontry.edu.mx", "telefono": "8183577621"},
    {"nombre": "Tonallí Comunidad Educativa", "zona": "Carretera Nacional / Sur", "categoria": "Colegio Humanista", "web": "https://www.tonalli.edu.mx", "contacto_url": "https://www.tonalli.edu.mx", "correo_base": "informes@tonalli.edu.mx", "telefono": "8128711066"},
    {"nombre": "Colegio Bilingüe La Silla", "zona": "Sur / Carretera Nacional", "categoria": "Colegio Bilingüe", "web": "https://www.colegiolasilla.com.mx", "contacto_url": "https://www.colegiolasilla.com.mx", "correo_base": "informes@colegiolasilla.com.mx", "telefono": "8183493545"},
    {"nombre": "Colegio Cristóbal Colón Monterrey", "zona": "Monterrey / San Nicolás", "categoria": "Colegio Privado", "web": "https://www.ccc.edu.mx", "contacto_url": "https://www.ccc.edu.mx", "correo_base": "admisiones@ccc.edu.mx", "telefono": "8183520410"},
    {"nombre": "Instituto Laurens", "zona": "Monterrey / Sur", "categoria": "Colegio Bilingüe", "web": "https://www.laurens.edu.mx", "contacto_url": "https://www.laurens.edu.mx", "correo_base": "admisiones@laurens.edu.mx", "telefono": "8183402200"},
    {"nombre": "Colegio Excélsior Monterrey", "zona": "Monterrey", "categoria": "Colegio Privado", "web": "https://www.excelsior.edu.mx", "contacto_url": "https://www.excelsior.edu.mx", "correo_base": "informes@excelsior.edu.mx", "telefono": "8183421890"},

    # 5. Academias de Danza, Ballet, Gimnasia, Arte y Clubes Deportivos (Eventos, Festivales, Recitales y Retratos)
    {"nombre": "Escuela Superior de Música y Danza de Monterrey", "zona": "Obispado / Monterrey", "categoria": "Academia Danza y Música", "web": "https://esmdm.edu.mx", "contacto_url": "https://esmdm.edu.mx", "correo_base": "contacto@esmdm.edu.mx", "telefono": "8183474830"},
    {"nombre": "Ballet de Monterrey (Academia Oficial)", "zona": "San Pedro / Monterrey", "categoria": "Academia de Ballet", "web": "https://www.balletdemonterrey.com", "contacto_url": "https://www.balletdemonterrey.com", "correo_base": "info@balletdemonterrey.com", "telefono": "8183477664"},
    {"nombre": "Club Deportivo San Agustín", "zona": "San Pedro Garza García", "categoria": "Club Deportivo y Academias", "web": "https://www.deportivosanagustin.com", "contacto_url": "https://www.deportivosanagustin.com", "correo_base": "contacto@deportivosanagustin.com", "telefono": "8183633232"},
    {"nombre": "Deportivo Alpino Chipinque", "zona": "San Pedro Garza García", "categoria": "Club Deportivo y Academias", "web": "https://www.alpinochipinque.com", "contacto_url": "https://www.alpinochipinque.com", "correo_base": "atencionsocios@alpinochipinque.com", "telefono": "8183781515"},
    {"nombre": "Casino Monterrey / Club Campestre", "zona": "San Pedro / Monterrey", "categoria": "Club Social y Eventos", "web": "https://www.casinomonterrey.com", "contacto_url": "https://www.casinomonterrey.com", "correo_base": "eventos@casinomonterrey.com", "telefono": "8181505500"},
    {"nombre": "Gimnasio / Academia Regio Gym", "zona": "San Jerónimo / Cumbres", "categoria": "Academia de Gimnasia", "web": "https://www.regiogym.com", "contacto_url": "https://www.regiogym.com", "correo_base": "info@regiogym.com", "telefono": "8183489010"},
]

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"(?:\+?52\s*)?(?:81)[\s.-]*\d{4}[\s.-]*\d{4}")

IGNORE_EMAIL_SUBSTRINGS = (
    "sentry", "wix", "example", "domain", "png", "jpg", "jpeg", "webp", "svg", "2x", "cloudflare", "wordpress", "bootstrap", "u00"
)


def verify_domain_dns(email: str, web_url: str = "") -> bool:
    if "@" not in email:
        return False
    domain = email.split("@", 1)[1].strip().lower()
    for candidate in (domain, "www." + domain):
        try:
            socket.gethostbyname(candidate)
            return True
        except Exception:
            pass
    if web_url:
        try:
            host = urllib.parse.urlparse(web_url).netloc
            if host:
                socket.gethostbyname(host)
                return True
        except Exception:
            pass
    # Also check nslookup MX fallback quickly
    try:
        out = subprocess.check_output(["nslookup", "-type=mx", domain], stderr=subprocess.STDOUT, timeout=3, text=True, errors="ignore")
        if "mail exchanger" in out.lower() or "mx preference" in out.lower():
            return True
    except Exception:
        pass
    return False


def scrape_institution(item: dict) -> dict:
    found_emails = set()
    found_phones = set()
    http_status = "Directorio Verificado"

    for url in {item["web"], item["contacto_url"]}:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=6, context=CTX) as resp:
                http_status = f"Web Activa (HTTP {resp.status})"
                html = resp.read().decode("utf-8", errors="ignore")
                for em in EMAIL_REGEX.findall(html):
                    em_clean = em.strip().lower().rstrip(".")
                    if not any(bad in em_clean for bad in IGNORE_EMAIL_SUBSTRINGS):
                        found_emails.add(em_clean)
                for ph in PHONE_REGEX.findall(html):
                    digits = re.sub(r"\D", "", ph)
                    if len(digits) >= 10:
                        found_phones.add(digits[-10:])
        except Exception:
            pass

    best_email = item["correo_base"]
    if found_emails:
        ranked = sorted(
            found_emails,
            key=lambda e: (
                0 if any(k in e for k in ("admision", "informe", "direccion", "contacto", "vinculacion", "eventos", "recepcion", "info")) else 1,
                len(e),
            ),
        )
        best_email = ranked[0]

    dns_ok = verify_domain_dns(best_email, item["web"])
    best_phone = sorted(found_phones)[0] if found_phones else item["telefono"]

    return {
        "nombre": item["nombre"],
        "zona": item["zona"],
        "categoria": item["categoria"],
        "web": item["web"],
        "correo_principal": best_email,
        "correos_adicionales": "; ".join(sorted(found_emails - {best_email}))[:140],
        "telefono": best_phone,
        "dns_verificado": "VERIFICADO" if dns_ok else "POR_VALIDAR",
        "estado_web": http_status,
    }


def build_html_dashboard(results: list):
    data_json = json.dumps(results, ensure_ascii=False)
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CAPTOORA B2B · Campaña Pixieset para Colegios, Preescolares y Academias (MTY / SPGG)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      background-color: #07080c;
      background-image:
        radial-gradient(at 15% 10%, rgba(223, 177, 91, 0.14) 0px, transparent 45%),
        radial-gradient(at 85% 20%, rgba(16, 185, 129, 0.08) 0px, transparent 50%);
      background-attachment: fixed;
      color: #f3f4f6;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    .font-editorial {{ font-family: 'Cinzel', serif; }}
    .apple-glass {{
      background: rgba(255, 255, 255, 0.045);
      backdrop-filter: blur(22px);
      border: 1px solid rgba(255, 255, 255, 0.12);
    }}
    .gold-gradient-text {{
      background: linear-gradient(135deg, #ffffff 30%, #dfb15b 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
  </style>
</head>
<body class="p-4 md:p-7 min-h-screen">
  <header class="max-w-7xl mx-auto mb-6 apple-glass rounded-2xl p-6 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-5">
    <div>
      <div class="flex flex-wrap items-center gap-2 mb-2">
        <a href="https://studio.pixieset.com/contacts" target="_blank" class="bg-amber-500 hover:bg-amber-400 text-black px-3.5 py-1 rounded-full text-xs font-extrabold shadow transition">
          🚀 1. Abrir Pixieset Studio Manager (Importar CSV) ↗
        </a>
        <a href="https://galleries.pixieset.com/collections" target="_blank" class="bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-400/40 text-emerald-300 px-3.5 py-1 rounded-full text-xs font-bold transition">
          📸 2. Abrir Colecciones Pixieset (Enviar Dossier por Email) ↗
        </a>
        <span class="bg-sky-500/20 border border-sky-400/30 text-sky-300 px-3 py-1 rounded-full text-xs font-semibold">
          Escudo Anti-Rebote DNS Activo
        </span>
      </div>
      <h1 class="text-2xl md:text-3xl font-extrabold font-editorial gold-gradient-text">
        Motor B2B Pixieset · Colegios, Kinders y Academias (MTY & SPGG)
      </h1>
      <p class="text-gray-400 text-xs md:text-sm mt-1">
        Estrategia <strong>"Mejoramos la Oferta de su Proveedor Actual + Galería Privada Pixieset con PIN Individual"</strong> sin riesgo de bloqueo de cuenta.
      </p>
    </div>

    <div class="flex flex-wrap gap-2">
      <button onclick="copyBatchEmails(0, 15)" class="px-4 py-2.5 rounded-xl text-xs font-extrabold bg-amber-500 text-black hover:bg-amber-400 shadow transition">
        📋 Copiar Lote 1 (Top 15 Correos VIP)
      </button>
      <button onclick="copyBatchEmails(15, 35)" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/20 text-white border border-white/15 transition">
        📋 Copiar Lote 2 (Siguientes Correos)
      </button>
    </div>
  </header>

  <div class="max-w-7xl mx-auto space-y-6">
    <!-- 3 TEMPLATES: ROMPE-PROVEEDOR / PIXIESET DOSSIER -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div class="apple-glass rounded-2xl p-5 border-t-2 border-amber-400 flex flex-col justify-between space-y-3">
        <div>
          <span class="text-[10px] uppercase tracking-wider font-extrabold text-amber-300 bg-amber-500/15 px-2.5 py-0.5 rounded-full">Plantilla 1 · Gancho "Mejoramos a su Proveedor"</span>
          <h3 class="text-base font-bold text-white mt-2">Reto de Mejora de Propuesta + Beneficio al Plantel</h3>
          <p class="text-xs text-gray-300 mt-1 leading-relaxed">
            Ideal para colegios que <strong>ya tienen fotógrafo tradicional</strong>. Ofrece entrega digital en 48h con PIN individual por familia en Pixieset, cero cobros en efectivo para el colegio y cobertura de cortesía de su Festival Navideño / Posada.
          </p>
        </div>
        <button onclick="copyMasterTemplate('MEJORA')" class="w-full py-2 rounded-xl text-xs font-extrabold bg-amber-500 text-black hover:bg-amber-400 transition">
          📋 Copiar Plantilla "Mejoramos su Proveedor"
        </button>
      </div>

      <div class="apple-glass rounded-2xl p-5 border-t-2 border-emerald-400 flex flex-col justify-between space-y-3">
        <div>
          <span class="text-[10px] uppercase tracking-wider font-extrabold text-emerald-300 bg-emerald-500/15 px-2.5 py-0.5 rounded-full">Plantilla 2 · Festivales Navideños y Graduaciones</span>
          <h3 class="text-base font-bold text-white mt-2">Piloto sin Compromiso Anual (Festival Dic 2026)</h3>
          <p class="text-xs text-gray-300 mt-1 leading-relaxed">
            Ideal para entrar este mismo mes de noviembre/diciembre cubriendo su <strong>Festival Navideño, Pastorela o Recital de Danza</strong> sin pedirles cambiar su contrato de graduación todavía.
          </p>
        </div>
        <button onclick="copyMasterTemplate('FESTIVAL')" class="w-full py-2 rounded-xl text-xs font-extrabold bg-emerald-500 text-black hover:bg-emerald-400 transition">
          📋 Copiar Plantilla "Festival Navideño / Recital"
        </button>
      </div>

      <div class="apple-glass rounded-2xl p-5 border-t-2 border-sky-400 flex flex-col justify-between space-y-3">
        <div>
          <span class="text-[10px] uppercase tracking-wider font-extrabold text-sky-300 bg-sky-500/15 px-2.5 py-0.5 rounded-full">Cómo usar Pixieset Email sin Bloqueos</span>
          <h3 class="text-base font-bold text-white mt-2">Regla de Oro de Entregabilidad en Pixieset</h3>
          <ul class="text-xs text-gray-300 mt-1 space-y-1 list-disc list-inside">
            <li>Usa el archivo <code>PROSPECTOS_COLEGIOS_PIXIESET_IMPORT.csv</code> en <strong>Studio Manager &rarr; Contacts</strong>.</li>
            <li>Envía en <strong>bloques de 15 a 20 colegios por día</strong> desde tu Galería Portafolio Escolar.</li>
            <li>Cada tarjeta abajo genera el correo <strong>personalizado con el nombre del colegio</strong>.</li>
          </ul>
        </div>
        <button onclick="copyMasterTemplate('SUBJECTS')" class="w-full py-2 rounded-xl text-xs font-bold bg-sky-500/20 text-sky-300 border border-sky-400/30 hover:bg-sky-500/30 transition">
          📋 Copiar 5 Asuntos de Alta Apertura (Open Rate)
        </button>
      </div>
    </div>

    <!-- FILTER BAR -->
    <div class="apple-glass rounded-2xl p-4 flex flex-col md:flex-row justify-between items-center gap-4">
      <div class="flex flex-wrap gap-2">
        <button onclick="setFilter('ALL')" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white/20 text-white">Todos ({len(results)})</button>
        <button onclick="setFilter('San Jerónimo')" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-400/30">📍 Vecinos San Jerónimo</button>
        <button onclick="setFilter('San Pedro')" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">💎 San Pedro Garza García</button>
        <button onclick="setFilter('Cumbres')" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-sky-500/20 text-sky-300 border border-sky-400/30">🏫 Cumbres / Poniente</button>
        <button onclick="setFilter('Academia')" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-purple-500/20 text-purple-300 border border-purple-400/30">🩰 Academias y Clubes</button>
      </div>
      <input id="q" oninput="renderTable()" placeholder="Buscar colegio, correo o zona..." class="w-full md:w-72 bg-black/60 border border-white/15 rounded-xl px-3.5 py-2 text-xs text-white">
    </div>

    <!-- TABLE -->
    <div class="apple-glass rounded-2xl overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-white/5 border-b border-white/10 text-gray-300 uppercase tracking-wider text-[10px]">
              <th class="p-3.5">Institución / Colegio</th>
              <th class="p-3.5">Zona</th>
              <th class="p-3.5">Correo Institucional Extraído</th>
              <th class="p-3.5">Teléfono</th>
              <th class="p-3.5">Estado DNS / Web</th>
              <th class="p-3.5 text-right">Acciones Rápidas Pixieset / Correo</th>
            </tr>
          </thead>
          <tbody id="rows" class="divide-y divide-white/5"></tbody>
        </table>
      </div>
    </div>
  </div>

  <div id="toast" class="fixed bottom-6 right-6 bg-black/95 border border-amber-400/50 text-white px-4 py-3 rounded-xl text-xs font-semibold shadow-2xl hidden z-50 max-w-md"></div>

  <script>
    const prospects = {data_json};
    let activeFilter = "ALL";

    function showToast(msg) {{
      const t = document.getElementById("toast");
      t.textContent = msg;
      t.classList.remove("hidden");
      setTimeout(() => t.classList.add("hidden"), 3500);
    }}

    function setFilter(f) {{
      activeFilter = f;
      renderTable();
    }}

    function copyBatchEmails(start, end) {{
      const verified = prospects.filter(p => p.dns_verificado === "VERIFICADO").slice(start, end);
      const list = verified.map(p => p.correo_principal).join(", ");
      navigator.clipboard.writeText(list);
      showToast(`✅ ${{verified.length}} correos verificados copiados (listos para pegar en Pixieset Share -> Email)`);
    }}

    function copyMasterTemplate(type, schoolName = "[Nombre del Colegio]") {{
      let txt = "";
      if (type === "MEJORA") {{
        txt = `Asunto: Propuesta de Fotografía Escolar y Galerías Privadas 4K para ${{schoolName}} | CAPTOORA Studio\\n\\nEstimada Dirección y Coordinación de ${{schoolName}}:\\n\\nLes saluda Alfonso Gutiérrez, director de CAPTOORA Studio (con estudio en Av. Paseo de los Álamos 165, Colinas de San Jerónimo).\\n\\nSabemos que muchos colegios ya cuentan con un proveedor de fotografía tradicional; sin embargo, les escribimos porque estamos ayudando a instituciones educativas de San Pedro y Monterrey a modernizar la experiencia de sus familias y mejorar cualquier propuesta actual bajo tres garantías:\\n\\n1. CERO CARGA ADMINISTRATIVA PARA EL COLEGIO: Entregamos a cada familia su galería privada en nuestra plataforma Pixieset protegida con PIN individual y selección en línea en 48 horas (sin que el colegio tenga que cobrar sobres en efectivo ni repartir paquetes físicos).\\n2. MEJORAMOS CUALQUIER COTIZACIÓN ACTUAL: Mejoramos el costo para los padres de familia o el porcentaje de beneficio/comisión institucional para el colegio en graduaciones, anuarios y retratos escolares.\\n3. COBERTURA DE CORTESÍA PARA SU PRÓXIMO EVENTO: Para que conozcan nuestra calidad editorial sin ningún compromiso ni cambiar a su proveedor actual, ofrecemos cubrir sin costo para el plantel su próximo Festival Navideño, Posada o presentación artística.\\n\\nAquí pueden ver una muestra de nuestra plataforma de galerías privadas para clientes:\\n🔗 https://captoora.pixieset.com/farmasistudio10oct2026-1/\\n\\n¿Con quién podríamos agendar una breve llamada de 5 minutos esta semana o enviarles nuestra carpeta comparativa?\\n\\nAtentamente,\\nAlfonso Gutiérrez | CAPTOORA Studio\\n📍 Av. Paseo de los Álamos 165, Colinas de San Jerónimo, Mty.\\n📲 WhatsApp Directo: 81 4005 0088 · Instagram: @captoora.studio`;
      }} else if (type === "FESTIVAL") {{
        txt = `Asunto: Cobertura Fotográfica para Festival Navideño / Recital de ${{schoolName}} | CAPTOORA Studio\\n\\nBuen día, Dirección y Coordinación de ${{schoolName}}:\\n\\nSoy Alfonso Gutiérrez, de CAPTOORA Studio (Colinas de San Jerónimo, Monterrey).\\n\\nDe cara a los cierres de semestre, posadas, pastorelas y festivales navideños de noviembre y diciembre, queremos poner a su disposición nuestro equipo de fotografía editorial y cobertura de escenario.\\n\\nCada familia recibe acceso privado con PIN a la galería digital del evento en alta definición (4K) a través de nuestra plataforma Pixieset, permitiendo descargas inmediatas en el celular sin ningún costo ni trámite administrativo para la dirección de ${{schoolName}}.\\n\\nSi ya tienen fotógrafo asignado para graduaciones, podemos apoyarles únicamente como segundo equipo en sus festivales o mejorar las condiciones que tienen actualmente.\\n\\n¿Qué fecha tienen programada para su festival de invierno para compartirles una propuesta a medida?\\n\\nUn cordial saludo,\\nAlfonso Gutiérrez | CAPTOORA Studio\\n📲 WhatsApp: 81 4005 0088 · @captoora.studio`;
      }} else {{
        txt = [
          "1. Fotografía y Galerías Privadas 4K para " + schoolName + " (Mejoramos su propuesta actual)",
          "2. Cobertura sin costo para el plantel: Festival Navideño 2026 | CAPTOORA Studio",
          "3. Modernización de fotografía escolar con PIN privado por familia | CAPTOORA",
          "4. ¿Ya tienen fotógrafo para su Festival de Diciembre en " + schoolName + "?",
          "5. Dossier de Fotografía Escolar y Recitales 2026–2027 | CAPTOORA Studio"
        ].join("\\n");
      }}
      navigator.clipboard.writeText(txt);
      showToast("✅ Plantilla personalizada copiada para " + schoolName);
    }}

    function renderTable() {{
      const q = (document.getElementById("q").value || "").toLowerCase().trim();
      const tbody = document.getElementById("rows");
      const filtered = prospects.filter(p => {{
        if (activeFilter !== "ALL") {{
          const hay = (p.zona + " " + p.categoria).toLowerCase();
          if (!hay.includes(activeFilter.toLowerCase())) return false;
        }}
        if (q && !(p.nombre.toLowerCase().includes(q) || p.correo_principal.toLowerCase().includes(q) || p.zona.toLowerCase().includes(q))) return false;
        return true;
      }});

      tbody.innerHTML = filtered.map(p => `
        <tr class="hover:bg-white/5 transition">
          <td class="p-3.5">
            <div class="font-bold text-white">${{p.nombre}}</div>
            <div class="text-[10px] text-gray-400">${{p.categoria}} · <a href="${{p.web}}" target="_blank" class="text-sky-300 hover:underline">${{p.web.replace('https://','')}} ↗</a></div>
          </td>
          <td class="p-3.5 text-gray-300">${{p.zona}}</td>
          <td class="p-3.5">
            <span class="font-mono text-amber-300 font-semibold">${{p.correo_principal}}</span>
            ${{p.correos_adicionales ? `<div class="text-[10px] text-gray-400 font-mono mt-0.5">+ ${{p.correos_adicionales}}</div>` : ''}}
          </td>
          <td class="p-3.5 font-mono text-gray-300">${{p.telefono}}</td>
          <td class="p-3.5">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${{p.dns_verificado === 'VERIFICADO' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-400/30' : 'bg-amber-500/20 text-amber-300'}}">
              ${{p.dns_verificado}}
            </span>
            <div class="text-[10px] text-gray-400 mt-0.5">${{p.estado_web}}</div>
          </td>
          <td class="p-3.5 text-right space-x-1.5 whitespace-nowrap">
            <button onclick="navigator.clipboard.writeText('${{p.correo_principal}}');showToast('📧 Correo copiado: ${{p.correo_principal}}')" class="px-2.5 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white font-semibold">
              📧 Correo
            </button>
            <button onclick="copyMasterTemplate('MEJORA', '${{p.nombre}}')" class="px-2.5 py-1.5 rounded-lg bg-amber-500 text-black font-bold hover:bg-amber-400">
              📋 Correo "Mejoramos Oferta"
            </button>
            <button onclick="copyMasterTemplate('FESTIVAL', '${{p.nombre}}')" class="px-2.5 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 font-semibold hover:bg-emerald-500/30">
              🎄 Correo Festival
            </button>
          </td>
        </tr>
      `).join("");
    }}

    renderTable();
  </script>
</body>
</html>
"""
    (ROOT / "CAMPAÑA_PIXIESET_COLEGIOS_B2B.html").write_text(html, encoding="utf-8")


def main():
    print(f"Iniciando scraping y verificacion DNS/MX de {len(SEED_INSTITUTIONS)} colegios, kinders y academias en MTY / SPGG...")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        futures = [ex.submit(scrape_institution, item) for item in SEED_INSTITUTIONS]
        for fut in concurrent.futures.as_completed(futures):
            res = fut.result()
            results.append(res)

    zone_rank = {
        "Colinas de San Jerónimo": 0,
        "San Jerónimo / Monterrey": 1,
        "Colinas de San Jerónimo / SPGG": 1,
        "San Pedro Garza García": 2,
        "San Pedro / Valle Alto": 2,
        "San Pedro / Valle Oriente": 2,
        "Valle Poniente / SPGG": 2,
    }
    results.sort(key=lambda r: (0 if r["dns_verificado"] == "VERIFICADO" else 1, zone_rank.get(r["zona"], 5), r["nombre"]))

    master_csv = OUT_DIR / "BASE_MAESTRA_COLEGIOS_MTY_2026.csv"
    with open(master_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["ID", "nombre", "zona", "categoria", "correo_principal", "correos_adicionales", "telefono", "web", "dns_verificado", "estado_web"],
        )
        writer.writeheader()
        for idx, r in enumerate(results, 1):
            writer.writerow({"ID": f"COL-{idx:03d}", **r})

    pixieset_csv = OUT_DIR / "PROSPECTOS_COLEGIOS_PIXIESET_IMPORT.csv"
    verified_results = [r for r in results if r["dns_verificado"] == "VERIFICADO"]
    with open(pixieset_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["First Name", "Last Name", "Email", "Phone", "Company", "Address", "Notes"],
        )
        writer.writeheader()
        for r in verified_results:
            writer.writerow({
                "First Name": "Dirección",
                "Last Name": r["nombre"],
                "Email": r["correo_principal"],
                "Phone": r["telefono"],
                "Company": r["nombre"],
                "Address": f"{r['zona']}, Monterrey, N.L.",
                "Notes": f"{r['categoria']} | Web: {r['web']} | DNS Verificado",
            })

    (OUT_DIR / "COLEGIOS_MTY_PIXIESET.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    build_html_dashboard(results)
    print(f"OK: {len(verified_results)}/{len(results)} colegios/academias verificados DNS y portal CAMPAÑA_PIXIESET_COLEGIOS_B2B.html generado.")


if __name__ == "__main__":
    main()
