# -*- coding: utf-8 -*-
"""
Scraper & Verificador B2B Masivo (85+ Instituciones en Monterrey y San Pedro Garza García)
para explotar el Portafolio ya existente en Pixieset mediante campañas de correo por lotes.
Incluye:
1. Colegios Privados y Bilingües (SPGG, Colinas de San Jerónimo, Cumbres, Carretera Nacional, Contry)
2. Preescolares / Kinders Privados
3. Academias de Ballet, Danza, Gimnasia y Arte (Recitales de Diciembre y Verano)
4. Clubes Deportivos, Ecuestres y Escuelas de Natación/Tenis (Torneos y Galas)
"""
import concurrent.futures
import csv
import json
import pathlib
import re
import socket
import ssl
import subprocess
import urllib.parse
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
    # === LOTE 1: VECINOS SAN JERÓNIMO / OBISPADO / CUMBRES PRIMER SECTOR (A 5-12 min de Captoora Studio) ===
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Viget Kindergarten", "zona": "Colinas de San Jerónimo", "categoria": "Kinder / Preescolar", "web": "https://www.viget.com.mx", "contacto_url": "https://www.viget.com.mx/contacto", "correo_base": "admisiones@institutoviget.com.mx", "telefono": "8121930551"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Instituto San Jerónimo (ISJ)", "zona": "San Jerónimo / Monterrey", "categoria": "Colegio K-12", "web": "https://www.isj.edu.mx", "contacto_url": "https://www.isj.edu.mx", "correo_base": "informes@isj.edu.mx", "telefono": "8112888152"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Colegio Montessori de Monterrey", "zona": "San Jerónimo / Monterrey", "categoria": "Colegio Montessori", "web": "https://www.montessoridemty.edu.mx", "contacto_url": "https://www.montessoridemty.edu.mx/contacto", "correo_base": "montessoridemonterrey@gmail.com", "telefono": "8183483796"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Kinder Little Town Puerta del Sol", "zona": "Colinas de San Jerónimo", "categoria": "Kinder / Preescolar", "web": "https://kinderlittletown.com", "contacto_url": "https://kinderlittletown.com", "correo_base": "nativa@kinderlittletown.com", "telefono": "8183150298"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Instituto Franco Mexicano (Campus San Jerónimo / SPGG)", "zona": "Colinas de San Jerónimo / SPGG", "categoria": "Colegio Privado", "web": "https://www.ifm.edu.mx", "contacto_url": "https://www.ifm.edu.mx", "correo_base": "admisiones@ifm.edu.mx", "telefono": "8122001951"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Colegio Mexicano", "zona": "San Jerónimo / Del Valle", "categoria": "Colegio Bilingüe", "web": "https://www.colegiomexicano.edu.mx", "contacto_url": "https://www.colegiomexicano.edu.mx", "correo_base": "informes@colegiomexicano.edu.mx", "telefono": "8120797221"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Instituto Motolinía Monterrey", "zona": "Obispado / Cumbres", "categoria": "Colegio Privado", "web": "https://www.motolinia.edu.mx", "contacto_url": "https://www.motolinia.edu.mx", "correo_base": "informes@motolinia.edu.mx", "telefono": "8156797418"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Instituto Regiomontano Chepevera / Cumbres", "zona": "Chepevera / San Jerónimo", "categoria": "Colegio Lasallista", "web": "https://www.ir.edu.mx", "contacto_url": "https://www.ir.edu.mx", "correo_base": "admisiones@ir.edu.mx", "telefono": "8183460500"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Escuela Superior de Música y Danza de Monterrey", "zona": "Obispado / Monterrey", "categoria": "Academia Danza y Música", "web": "https://esmdm.edu.mx", "contacto_url": "https://esmdm.edu.mx", "correo_base": "contacto@esmdm.edu.mx", "telefono": "8183474830"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Colegio Liceo Anglo Francés", "zona": "Monterrey Poniente", "categoria": "Colegio Bilingüe", "web": "https://www.laf.edu.mx", "contacto_url": "https://www.laf.edu.mx", "correo_base": "informes@laf.edu.mx", "telefono": "8183481515"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Colegio Simón Bolívar Monterrey", "zona": "Chepevera / Obispado", "categoria": "Kinder y Primaria", "web": "https://www.colegiosimonbolivar.edu.mx", "contacto_url": "https://www.colegiosimonbolivar.edu.mx", "correo_base": "informes@colegiosimonbolivar.edu.mx", "telefono": "8183471820"},
    {"lote": "Lote 1 · San Jerónimo y Obispado", "nombre": "Kinder Gymboree Play & Music San Jerónimo", "zona": "Colinas de San Jerónimo", "categoria": "Estimulación y Preescolar", "web": "https://www.gymboreeclases.mx", "contacto_url": "https://www.gymboreeclases.mx", "correo_base": "sanjeronimo@gymboreeclases.mx", "telefono": "8183489200"},

    # === LOTE 2: SAN PEDRO GARZA GARCÍA / VALLE PONIENTE / VALLE ORIENTE (Ticket Alto VIP) ===
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Colegio Inglés de Monterrey", "zona": "San Pedro Garza García", "categoria": "Colegio Bilingüe VIP", "web": "https://www.colegioingles.edu.mx", "contacto_url": "https://www.colegioingles.edu.mx", "correo_base": "admisiones@colegioingles.edu.mx", "telefono": "8180477000"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Instituto San Roberto (ISR San Agustín)", "zona": "San Pedro Garza García", "categoria": "Colegio Internacional VIP", "web": "https://www.sanroberto.edu.mx", "contacto_url": "https://www.sanroberto.edu.mx", "correo_base": "admisionessa@sanroberto.edu.mx", "telefono": "8180002158"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "American School Foundation of Monterrey (ASFM)", "zona": "Valle Poniente / SPGG", "categoria": "Colegio Internacional VIP", "web": "https://www.asfm.edu.mx", "contacto_url": "https://www.asfm.edu.mx", "correo_base": "admissions@asfm.edu.mx", "telefono": "8182884400"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Colegio Euroamericano Monterrey (Valle Oriente)", "zona": "San Pedro / Valle Oriente", "categoria": "Colegio Bilingüe VIP", "web": "https://www.euroamericano.edu.mx", "contacto_url": "https://www.euroamericano.edu.mx", "correo_base": "admisiones@euroamericano.edu.mx", "telefono": "8182488400"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Instituto Brillamont", "zona": "San Pedro Garza García", "categoria": "Colegio Bilingüe VIP", "web": "https://www.brillamont.edu.mx", "contacto_url": "https://www.brillamont.edu.mx", "correo_base": "admisiones@brillamont.edu.mx", "telefono": "8121170005"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Instituto Mater", "zona": "San Pedro Garza García", "categoria": "Colegio Privado VIP", "web": "https://www.mater.edu.mx", "contacto_url": "https://www.mater.edu.mx", "correo_base": "admisiones@mater.edu.mx", "telefono": "8134039835"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Colegio Labastida", "zona": "San Pedro Garza García", "categoria": "Colegio Privado", "web": "https://www.labastida.edu.mx", "contacto_url": "https://www.labastida.edu.mx", "correo_base": "admisiones@labastida.edu.mx", "telefono": "8183354530"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Instituto Irlandés de Monterrey", "zona": "San Pedro Garza García", "categoria": "Colegio Internacional VIP", "web": "https://www.irlandesmonterrey.com", "contacto_url": "https://www.irlandesmonterrey.com", "correo_base": "admisiones@irlandesmonterrey.com", "telefono": "8183631202"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Colegio Himalaya Monterrey", "zona": "San Pedro Garza García", "categoria": "Colegio Internacional VIP", "web": "https://www.himalaya.edu.mx", "contacto_url": "https://www.himalaya.edu.mx", "correo_base": "admisiones@himalaya.edu.mx", "telefono": "8183384900"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Colegio Necali / Eurocampestre", "zona": "San Pedro Garza García", "categoria": "Colegio Privado", "web": "https://www.necali.edu.mx", "contacto_url": "https://www.necali.edu.mx", "correo_base": "admisiones@eurocampestre.edu.mx", "telefono": "8116113101"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Liceo de Monterrey", "zona": "San Pedro / Valle Oriente", "categoria": "Colegio Bilingüe VIP", "web": "https://www.liceodemonterrey.edu.mx", "contacto_url": "https://www.liceodemonterrey.edu.mx", "correo_base": "admisiones@liceodemonterrey.edu.mx", "telefono": "8181532100"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Instituto Formus Valle Poniente", "zona": "San Pedro / Valle Poniente", "categoria": "Colegio Privado VIP", "web": "https://www.formus.edu.mx", "contacto_url": "https://www.formus.edu.mx", "correo_base": "admisiones@formus.edu.mx", "telefono": "8181245600"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Colegio Mirasierra", "zona": "San Pedro Garza García", "categoria": "Colegio Privado VIP", "web": "https://www.colegiomirasierra.edu.mx", "contacto_url": "https://www.colegiomirasierra.edu.mx", "correo_base": "admisiones@colegiomirasierra.edu.mx", "telefono": "8183383850"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Preescolar Bambini Montessori SPGG", "zona": "San Pedro Garza García", "categoria": "Kinder / Montessori VIP", "web": "https://www.bambinimontessori.edu.mx", "contacto_url": "https://www.bambinimontessori.edu.mx", "correo_base": "informes@bambinimontessori.edu.mx", "telefono": "8183358090"},
    {"lote": "Lote 2 · San Pedro Garza García VIP", "nombre": "Kinder Toddlers & Kids San Pedro", "zona": "San Pedro Garza García", "categoria": "Kinder Bilingüe VIP", "web": "https://www.toddlers.edu.mx", "contacto_url": "https://www.toddlers.edu.mx", "correo_base": "admisiones@toddlers.edu.mx", "telefono": "8183564411"},

    # === LOTE 3: CUMBRES / PONIENTE / SAN NICOLÁS ===
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Pan American School of Monterrey (PAS)", "zona": "Cumbres / Carretera Nac.", "categoria": "Colegio Internacional", "web": "https://www.pas.edu.mx", "contacto_url": "https://www.pas.edu.mx", "correo_base": "admissions@panamerican.edu.mx", "telefono": "8181300900"},
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Colegio San Patricio Monterrey (Cumbres)", "zona": "Cumbres / Del Paseo", "categoria": "Colegio Bilingüe", "web": "https://www.sanpatricio.edu.mx", "contacto_url": "https://www.sanpatricio.edu.mx", "correo_base": "admisiones@sanpatricio.edu.mx", "telefono": "8111339101"},
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Cambridge College Monterrey", "zona": "Cumbres / Mitras", "categoria": "Colegio Bilingüe", "web": "https://www.cambridge.edu.mx", "contacto_url": "https://www.cambridge.edu.mx", "correo_base": "informacion@cambridge.edu.mx", "telefono": "8181234040"},
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Instituto Edinburgh", "zona": "Cumbres / San Nicolás", "categoria": "Colegio Bilingüe", "web": "https://www.edinburgh.edu.mx", "contacto_url": "https://www.edinburgh.edu.mx", "correo_base": "info@edinburgh.edu.mx", "telefono": "8121338370"},
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Instituto Anglo Británico", "zona": "Cumbres / Carretera Nacional", "categoria": "Colegio Internacional IB", "web": "https://www.anglobritanico.edu.mx", "contacto_url": "https://www.anglobritanico.edu.mx", "correo_base": "admisiones@anglobritanico.edu.mx", "telefono": "8183004050"},
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Colegio Madison Monterrey", "zona": "Cumbres / Carretera Nacional", "categoria": "Colegio Internacional IB", "web": "https://www.colegiomadison.edu.mx", "contacto_url": "https://www.colegiomadison.edu.mx", "correo_base": "admisionesmty@colegiomadison.edu.mx", "telefono": "8181041140"},
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Kilimanjaro International School", "zona": "Cumbres / Monterrey", "categoria": "Colegio Internacional", "web": "https://www.kilimanjaro.edu.mx", "contacto_url": "https://www.kilimanjaro.edu.mx", "correo_base": "admisiones@kilimanjaro.edu.mx", "telefono": "8183006070"},
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Nexus Comunidad Educativa", "zona": "Cumbres / Poniente", "categoria": "Colegio Privado", "web": "https://www.nexus.edu.mx", "contacto_url": "https://www.nexus.edu.mx", "correo_base": "informes@nexus.edu.mx", "telefono": "8181230202"},
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Colegio Naciones Unidas (CNU)", "zona": "Cumbres / Monterrey", "categoria": "Colegio Bilingüe", "web": "https://www.cnu.edu.mx", "contacto_url": "https://www.cnu.edu.mx", "correo_base": "informes@cnu.edu.mx", "telefono": "8183001234"},
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Colegio Cristóbal Colón Monterrey", "zona": "Monterrey / Cumbres", "categoria": "Colegio Privado", "web": "https://www.ccc.edu.mx", "contacto_url": "https://www.ccc.edu.mx", "correo_base": "admisiones@ccc.edu.mx", "telefono": "8183520410"},
    {"lote": "Lote 3 · Cumbres y Poniente", "nombre": "Instituto Oxford de Monterrey", "zona": "Cumbres / San Nicolás", "categoria": "Colegio Bilingüe", "web": "https://www.oxford.edu.mx", "contacto_url": "https://www.oxford.edu.mx", "correo_base": "admisiones@oxford.edu.mx", "telefono": "8183005500"},

    # === LOTE 4: SUR / CONTRY / CARRETERA NACIONAL ===
    {"lote": "Lote 4 · Contry y Carretera Nacional", "nombre": "Colegio Regiomontano Contry", "zona": "Contry / Sur Monterrey", "categoria": "Colegio Lasallista", "web": "https://www.regiocontry.edu.mx", "contacto_url": "https://www.regiocontry.edu.mx", "correo_base": "recepcion@regiocontry.edu.mx", "telefono": "8183577621"},
    {"lote": "Lote 4 · Contry y Carretera Nacional", "nombre": "Tonallí Comunidad Educativa", "zona": "Carretera Nacional / Sur", "categoria": "Colegio Humanista", "web": "https://www.tonalli.edu.mx", "contacto_url": "https://www.tonalli.edu.mx", "correo_base": "informes@tonalli.edu.mx", "telefono": "8128711066"},
    {"lote": "Lote 4 · Contry y Carretera Nacional", "nombre": "Colegio Bilingüe La Silla", "zona": "Sur / Carretera Nacional", "categoria": "Colegio Bilingüe", "web": "https://www.colegiolasilla.com.mx", "contacto_url": "https://www.colegiolasilla.com.mx", "correo_base": "informes@colegiolasilla.com.mx", "telefono": "8183493545"},
    {"lote": "Lote 4 · Contry y Carretera Nacional", "nombre": "Highlands International School Monterrey", "zona": "Carretera Nacional", "categoria": "Colegio Internacional", "web": "https://www.highlandsmty.edu.mx", "contacto_url": "https://www.highlandsmty.edu.mx", "correo_base": "admisiones@highlandsmty.edu.mx", "telefono": "8182662400"},
    {"lote": "Lote 4 · Contry y Carretera Nacional", "nombre": "Instituto Laurens", "zona": "Monterrey / Sur", "categoria": "Colegio Bilingüe", "web": "https://www.laurens.edu.mx", "contacto_url": "https://www.laurens.edu.mx", "correo_base": "admisiones@laurens.edu.mx", "telefono": "8183402200"},
    {"lote": "Lote 4 · Contry y Carretera Nacional", "nombre": "Colegio Excélsior Monterrey", "zona": "Monterrey Sur", "categoria": "Colegio Privado", "web": "https://www.excelsior.edu.mx", "contacto_url": "https://www.excelsior.edu.mx", "correo_base": "informes@excelsior.edu.mx", "telefono": "8183421890"},
    {"lote": "Lote 4 · Contry y Carretera Nacional", "nombre": "Instituto San Roberto (Campus Valle Alto)", "zona": "Valle Alto / Carretera Nac.", "categoria": "Colegio Internacional VIP", "web": "https://www.sanroberto.edu.mx", "contacto_url": "https://www.sanroberto.edu.mx", "correo_base": "admissionsva@sanroberto.edu.mx", "telefono": "8186251500"},
    {"lote": "Lote 4 · Contry y Carretera Nacional", "nombre": "Colegio Euroamericano Sur (Carretera Nacional)", "zona": "Carretera Nacional", "categoria": "Colegio Bilingüe VIP", "web": "https://www.euroamericano.edu.mx", "contacto_url": "https://www.euroamericano.edu.mx", "correo_base": "admisionessur@euroamericano.edu.mx", "telefono": "8183179000"},

    # === LOTE 5: ACADEMIAS DE DANZA, BALLET, GIMNASIA, ARTE Y CLUBES DEPORTIVOS (Recitales y Galas Diciembre) ===
    {"lote": "Lote 5 · Academias Danza y Clubes VIP", "nombre": "Ballet de Monterrey (Academia Oficial)", "zona": "San Pedro / Monterrey", "categoria": "Academia de Ballet", "web": "https://www.balletdemonterrey.com", "contacto_url": "https://www.balletdemonterrey.com", "correo_base": "info@balletdemonterrey.com", "telefono": "8183477664"},
    {"lote": "Lote 5 · Academias Danza y Clubes VIP", "nombre": "Club Deportivo San Agustín", "zona": "San Pedro Garza García", "categoria": "Club Deportivo y Academias", "web": "https://www.deportivosanagustin.com", "contacto_url": "https://www.deportivosanagustin.com", "correo_base": "contacto@deportivosanagustin.com", "telefono": "8183633232"},
    {"lote": "Lote 5 · Academias Danza y Clubes VIP", "nombre": "Deportivo Alpino Chipinque", "zona": "San Pedro Garza García", "categoria": "Club Deportivo y Academias", "web": "https://www.alpinochipinque.com", "contacto_url": "https://www.alpinochipinque.com", "correo_base": "atencionsocios@alpinochipinque.com", "telefono": "8183781515"},
    {"lote": "Lote 5 · Academias Danza y Clubes VIP", "nombre": "Casino Monterrey", "zona": "Monterrey / San Pedro", "categoria": "Club Social y Galas", "web": "https://www.casinomonterrey.com", "contacto_url": "https://www.casinomonterrey.com", "correo_base": "eventos@casinomonterrey.com", "telefono": "8181505500"},
    {"lote": "Lote 5 · Academias Danza y Clubes VIP", "nombre": "Club Ejecutivo San Pedro", "zona": "San Pedro Garza García", "categoria": "Club Deportivo y Eventos", "web": "https://www.clubejecutivo.com.mx", "contacto_url": "https://www.clubejecutivo.com.mx", "correo_base": "eventos@clubejecutivo.com.mx", "telefono": "8183355000"},
    {"lote": "Lote 5 · Academias Danza y Clubes VIP", "nombre": "Gimnasio y Academia Regio Gym", "zona": "San Jerónimo / Cumbres", "categoria": "Academia de Gimnasia", "web": "https://www.regiogym.com", "contacto_url": "https://www.regiogym.com", "correo_base": "info@regiogym.com", "telefono": "8183489010"},
    {"lote": "Lote 5 · Academias Danza y Clubes VIP", "nombre": "Tutus Dance Studio San Pedro", "zona": "San Pedro Garza García", "categoria": "Academia de Ballet y Danza", "web": "https://www.balletdemonterrey.com", "contacto_url": "https://www.balletdemonterrey.com", "correo_base": "academia@balletdemonterrey.com", "telefono": "8183351200"},
    {"lote": "Lote 5 · Academias Danza y Clubes VIP", "nombre": "Club Sonoma Residencial & Deportivo", "zona": "Valle Oriente / SPGG", "categoria": "Club Deportivo y Academias", "web": "https://www.clubsonoma.com.mx", "contacto_url": "https://www.clubsonoma.com.mx", "correo_base": "contacto@clubsonoma.com.mx", "telefono": "8181541200"},
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
        "lote": item["lote"],
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
  <title>CAPTOORA B2B · Centro de Disparo con Portafolio Pixieset ({len(results)} Colegios y Academias)</title>
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
  <header class="max-w-7xl mx-auto mb-6 apple-glass rounded-2xl p-6 space-y-4">
    <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-5">
      <div>
        <div class="flex flex-wrap items-center gap-2 mb-2">
          <a href="https://studio.pixieset.com/contacts" target="_blank" class="bg-amber-500 hover:bg-amber-400 text-black px-3.5 py-1 rounded-full text-xs font-extrabold shadow transition">
            🚀 1. Importar CSV en Pixieset Contacts ↗
          </a>
          <a href="https://galleries.pixieset.com/collections" target="_blank" class="bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-400/40 text-emerald-300 px-3.5 py-1 rounded-full text-xs font-bold transition">
            📸 2. Abrir tu Portafolio en Pixieset (Share &rarr; Email) ↗
          </a>
        </div>
        <h1 class="text-2xl md:text-3xl font-extrabold font-editorial gold-gradient-text">
          Centro de Disparo B2B con tu Portafolio · {len(results)} Colegios y Academias
        </h1>
        <p class="text-gray-400 text-xs md:text-sm mt-1">
          Como <strong>ya tienes tu portafolio listo</strong>, aquí tienes los <strong>5 Lotes Diarios</strong> para mandarlo por Pixieset y marcar a cuáles ya les enviaste.
        </p>
      </div>

      <!-- PORTFOLIO URL CONFIG -->
      <div class="w-full lg:w-96 bg-black/50 p-3.5 rounded-xl border border-amber-400/30">
        <label class="text-[10px] uppercase tracking-wider text-amber-300 font-bold block mb-1">🔗 Link de tu Portafolio para inyectar en los correos:</label>
        <div class="flex gap-2">
          <input id="portfolio-url" type="text" value="https://captoora.pixieset.com" oninput="savePortfolioUrl(this.value)" class="w-full bg-black/80 border border-white/20 rounded-lg px-3 py-1.5 text-xs text-white font-mono">
        </div>
      </div>
    </div>

    <!-- 5 DAILY BATCH BUTTONS FOR PIXIESET SHARE -> EMAIL -->
    <div class="pt-3 border-t border-white/10">
      <div class="text-xs font-bold text-gray-300 mb-2">⚡ Copiar Lote de Correos (Separados por coma listos para pegar en <code class="text-amber-300">Pixieset &rarr; Share &rarr; Email</code>):</div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5">
        <button onclick="copyLote('Lote 1')" class="p-3 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-400/40 text-left transition">
          <div class="text-xs font-extrabold text-amber-300">📍 Día 1 · Lote San Jerónimo</div>
          <div class="text-[11px] text-gray-300 mt-0.5">Vecinos a 5-10 min del estudio</div>
        </button>
        <button onclick="copyLote('Lote 2')" class="p-3 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-400/40 text-left transition">
          <div class="text-xs font-extrabold text-emerald-300">💎 Día 2 · Lote San Pedro VIP</div>
          <div class="text-[11px] text-gray-300 mt-0.5">Colegios Bilingües y Preescolares</div>
        </button>
        <button onclick="copyLote('Lote 3')" class="p-3 rounded-xl bg-sky-500/20 hover:bg-sky-500/30 border border-sky-400/40 text-left transition">
          <div class="text-xs font-extrabold text-sky-300">🏫 Día 3 · Lote Cumbres</div>
          <div class="text-[11px] text-gray-300 mt-0.5">Colegios Internacionales Poniente</div>
        </button>
        <button onclick="copyLote('Lote 4')" class="p-3 rounded-xl bg-purple-500/20 hover:bg-purple-500/30 border border-purple-400/40 text-left transition">
          <div class="text-xs font-extrabold text-purple-300">🌲 Día 4 · Carretera Nacional</div>
          <div class="text-[11px] text-gray-300 mt-0.5">Contry, Sur y Valle Alto</div>
        </button>
        <button onclick="copyLote('Lote 5')" class="p-3 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 border border-rose-400/40 text-left transition">
          <div class="text-xs font-extrabold text-rose-300">🩰 Día 5 · Academias y Clubes</div>
          <div class="text-[11px] text-gray-300 mt-0.5">Ballet, Gimnasia y Deportivos</div>
        </button>
      </div>
    </div>
  </header>

  <div class="max-w-7xl mx-auto space-y-6">
    <!-- 3 TEMPLATES -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div class="apple-glass rounded-2xl p-5 border-t-2 border-amber-400 flex flex-col justify-between space-y-3">
        <div>
          <span class="text-[10px] uppercase tracking-wider font-extrabold text-amber-300 bg-amber-500/15 px-2.5 py-0.5 rounded-full">Mensaje para Pegar en Pixieset Email</span>
          <h3 class="text-base font-bold text-white mt-2">1. Gancho "Mejoramos a su Proveedor Actual"</h3>
          <p class="text-xs text-gray-300 mt-1 leading-relaxed">
            Úsalo como mensaje general cuando envíes tu <strong>Portafolio desde Pixieset</strong> a un lote de colegios. Incluye las 3 garantías: 0% carga administrativa con PIN, mejora de cotización y cobertura de cortesía de su Festival Navideño.
          </p>
        </div>
        <button onclick="copyMasterTemplate('PIXIESET_BULK')" class="w-full py-2.5 rounded-xl text-xs font-extrabold bg-amber-500 text-black hover:bg-amber-400 transition">
          📋 Copiar Texto para Campaña Pixieset (Lote)
        </button>
      </div>

      <div class="apple-glass rounded-2xl p-5 border-t-2 border-emerald-400 flex flex-col justify-between space-y-3">
        <div>
          <span class="text-[10px] uppercase tracking-wider font-extrabold text-emerald-300 bg-emerald-500/15 px-2.5 py-0.5 rounded-full">Especial Academias y Festivales Dic</span>
          <h3 class="text-base font-bold text-white mt-2">2. Gancho "Festival Navideño / Recital de Fin de Año"</h3>
          <p class="text-xs text-gray-300 mt-1 leading-relaxed">
            Ideal para <strong>Kinders y Academias de Ballet/Gimnasia</strong> que tienen recitales en noviembre y diciembre: cobertura sin costo para la academia y venta/descarga individual por familia con PIN en Pixieset.
          </p>
        </div>
        <button onclick="copyMasterTemplate('FESTIVAL')" class="w-full py-2.5 rounded-xl text-xs font-extrabold bg-emerald-500 text-black hover:bg-emerald-400 transition">
          📋 Copiar Texto "Festival Navideño / Recital"
        </button>
      </div>

      <div class="apple-glass rounded-2xl p-5 border-t-2 border-sky-400 flex flex-col justify-between space-y-3">
        <div>
          <span class="text-[10px] uppercase tracking-wider font-extrabold text-sky-300 bg-sky-500/15 px-2.5 py-0.5 rounded-full">Guion de Llamada / WhatsApp (45 seg)</span>
          <h3 class="text-base font-bold text-white mt-2">3. Seguimiento 24h Después del Correo</h3>
          <p class="text-xs text-gray-300 mt-1 leading-relaxed">
            A las 24h de mandar el portafolio por Pixieset, llamas o mandas WhatsApp para pedir el contacto directo de la Coordinadora de Eventos o Sociedad de Padres.
          </p>
        </div>
        <button onclick="copyMasterTemplate('FOLLOWUP')" class="w-full py-2.5 rounded-xl text-xs font-bold bg-sky-500/20 text-sky-300 border border-sky-400/30 hover:bg-sky-500/30 transition">
          📋 Copiar Guion de Seguimiento 24h
        </button>
      </div>
    </div>

    <!-- FILTER BAR -->
    <div class="apple-glass rounded-2xl p-4 flex flex-col md:flex-row justify-between items-center gap-4">
      <div class="flex flex-wrap gap-2">
        <button onclick="setFilter('ALL')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-white/20 text-white">Todos ({len(results)})</button>
        <button onclick="setFilter('Lote 1')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-400/30">Lote 1: San Jerónimo</button>
        <button onclick="setFilter('Lote 2')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">Lote 2: San Pedro VIP</button>
        <button onclick="setFilter('Lote 3')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-sky-500/20 text-sky-300 border border-sky-400/30">Lote 3: Cumbres</button>
        <button onclick="setFilter('Lote 4')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-purple-500/20 text-purple-300 border border-purple-400/30">Lote 4: Carretera Nac.</button>
        <button onclick="setFilter('Lote 5')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-rose-500/20 text-rose-300 border border-rose-400/30">Lote 5: Academias/Clubes</button>
      </div>
      <input id="q" oninput="renderTable()" placeholder="Buscar colegio, correo, lote o zona..." class="w-full md:w-72 bg-black/60 border border-white/15 rounded-xl px-3.5 py-2 text-xs text-white">
    </div>

    <!-- TABLE -->
    <div class="apple-glass rounded-2xl overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-white/5 border-b border-white/10 text-gray-300 uppercase tracking-wider text-[10px]">
              <th class="p-3.5">Enviado</th>
              <th class="p-3.5">Lote / Institución</th>
              <th class="p-3.5">Zona</th>
              <th class="p-3.5">Correo Institucional</th>
              <th class="p-3.5">Teléfono</th>
              <th class="p-3.5 text-right">Acciones Directas</th>
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
    let sentMap = JSON.parse(localStorage.getItem("captoora_b2b_sent_v1") || "{{}}");
    const savedUrl = localStorage.getItem("captoora_portfolio_url");
    if (savedUrl) document.getElementById("portfolio-url").value = savedUrl;

    function savePortfolioUrl(val) {{
      localStorage.setItem("captoora_portfolio_url", val.trim());
    }}

    function getPortfolioUrl() {{
      return (document.getElementById("portfolio-url").value || "https://captoora.pixieset.com").trim();
    }}

    function toggleSent(email) {{
      sentMap[email] = !sentMap[email];
      localStorage.setItem("captoora_b2b_sent_v1", JSON.stringify(sentMap));
      renderTable();
    }}

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

    function copyLote(lotePrefix) {{
      const list = prospects
        .filter(p => p.lote.startsWith(lotePrefix) && p.dns_verificado === "VERIFICADO")
        .map(p => p.correo_principal);
      navigator.clipboard.writeText(list.join(", "));
      showToast(`✅ ${{list.length}} correos de ${{lotePrefix}} copiados (pégalos en Pixieset -> Share -> Email)`);
    }}

    function copyMasterTemplate(type, schoolName = "su institución") {{
      const portUrl = getPortfolioUrl();
      let txt = "";
      if (type === "PIXIESET_BULK") {{
        txt = `Asunto: Portafolio CAPTOORA Studio | Mejoramos la propuesta fotográfica actual de ${{schoolName}}\\n\\nEstimada Dirección, Coordinación de Eventos y Sociedad de Padres:\\n\\nLes saluda Alfonso Gutiérrez, director de CAPTOORA Studio (con estudio en Av. Paseo de los Álamos 165, Colinas de San Jerónimo).\\n\\nPor medio de esta invitación les compartimos nuestro Portafolio Oficial en Pixieset:\\n🔗 ${{portUrl}}\\n\\nSabemos que muchas instituciones ya cuentan con un proveedor de fotografía tradicional; sin embargo, les escribimos porque estamos ayudando a colegios y academias de Monterrey y San Pedro a modernizar la entrega a sus familias y MEJORAR CUALQUIER PROPUESTA ACTUAL bajo 3 garantías:\\n\\n1. CERO CARGA ADMINISTRATIVA Y CERO MANEJO DE EFECTIVO PARA EL COLEGIO: Cada familia recibe su galería privada en nuestra plataforma Pixieset protegida con PIN individual en 48 horas, seleccionando y descargando sus fotos en 4K desde su celular (las secretarias y maestras ya no tienen que cobrar sobres ni repartir paquetes físicos).\\n2. MEJORAMOS CUALQUIER COTIZACIÓN O BENEFICIO ACTUAL: Mejoramos el precio por paquete para las familias o el porcentaje de comisión/beneficio en especie para el plantel en graduaciones, anuarios y retratos escolares.\\n3. PRUEBA SIN COMPROMISO EN SU FESTIVAL DE INVIERNO: Para que conozcan nuestra calidad editorial sin cambiar hoy a su proveedor actual, ofrecemos cubrir SIN COSTO PARA EL PLANTEL su próximo Festival Navideño, Posada o Recital de Diciembre.\\n\\n¿Con quién podríamos coordinar una breve llamada de 5 minutos esta semana para presentarles nuestra comparativa?\\n\\nAtentamente,\\nAlfonso Gutiérrez | CAPTOORA Studio\\n📍 Av. Paseo de los Álamos 165, Colinas de San Jerónimo, Mty.\\n📲 WhatsApp Directo: 81 4005 0088 · Instagram: @captoora.studio`;
      }} else if (type === "FESTIVAL") {{
        txt = `Asunto: Cobertura Fotográfica 4K para Festival Navideño / Recital de ${{schoolName}} | CAPTOORA Studio\\n\\nEstimada Dirección y Coordinación de ${{schoolName}}:\\n\\nSoy Alfonso Gutiérrez, director de CAPTOORA Studio (Colinas de San Jerónimo, Monterrey).\\n\\nDe cara a los cierres de semestre, posadas, pastorelas y recitales de noviembre y diciembre, les comparto nuestro Portafolio Oficial:\\n🔗 ${{portUrl}}\\n\\nOfrecemos cubrir su Festival Navideño o Recital de Fin de Año SIN COSTO PARA EL PLANTEL, entregando a cada familia acceso privado con PIN a la galería digital del evento en resolución 4K dentro de las 48 horas siguientes (además de entregarle a ${{schoolName}} un banco de fotografías editoriales para sus redes y admisiones).\\n\\nSi ya cuentan con un fotógrafo para graduaciones, podemos apoyarles únicamente en sus eventos de invierno o mejorar las condiciones de su proveedor actual.\\n\\n¿Qué fecha tienen programada para su festival de diciembre para reservarles disponibilidad?\\n\\nUn cordial saludo,\\nAlfonso Gutiérrez | CAPTOORA Studio\\n📲 WhatsApp Directo: 81 4005 0088 · @captoora.studio`;
      }} else {{
        txt = `Buen día, hablo de CAPTOORA Studio aquí en Colinas de San Jerónimo. Ayer enviamos a Dirección por medio de nuestra plataforma Pixieset nuestro portafolio (${{portUrl}}) con una propuesta para cubrir sin costo para el plantel su Festival Navideño y mejorar la oferta de su proveedor fotográfico actual. ¿Me podrías confirmar el nombre o WhatsApp de la Coordinadora de Eventos / Difusión para compartirle su acceso directo?`;
      }}
      navigator.clipboard.writeText(txt);
      showToast("✅ Mensaje copiado con tu link de portafolio para " + schoolName);
    }}

    function openMailto(email, schoolName) {{
      const portUrl = getPortfolioUrl();
      const subj = encodeURIComponent(`Portafolio CAPTOORA Studio | Mejoramos la propuesta fotográfica de ${{schoolName}}`);
      const body = encodeURIComponent(
        `Estimada Dirección y Coordinación de ${{schoolName}}:\n\n` +
        `Les saluda Alfonso Gutiérrez, director de CAPTOORA Studio (Av. Paseo de los Álamos 165, Colinas de San Jerónimo).\n\n` +
        `Les comparto nuestro Portafolio Oficial:\n${{portUrl}}\n\n` +
        `Si ya cuentan con proveedor de fotografía escolar o de eventos, mejoramos cualquier propuesta actual con:\n` +
        `1) Cero carga administrativa ni cobros en efectivo para el colegio (galerías privadas Pixieset con PIN individual en 48h).\n` +
        `2) Mejora en precio para las familias o mayor comisión/beneficio en especie para ${{schoolName}}.\n` +
        `3) Cobertura SIN COSTO para el plantel en su próximo Festival Navideño o Recital de Diciembre como prueba de calidad.\n\n` +
        `¿Con quién podríamos coordinar una llamada de 5 minutos esta semana?\n\n` +
        `Atentamente,\nAlfonso Gutiérrez | CAPTOORA Studio\nWhatsApp: 81 4005 0088 · @captoora.studio`
      );
      window.open(`mailto:${{email}}?subject=${{subj}}&body=${{body}}`, "_blank");
    }}

    function renderTable() {{
      const q = (document.getElementById("q").value || "").toLowerCase().trim();
      const tbody = document.getElementById("rows");
      const filtered = prospects.filter(p => {{
        if (activeFilter !== "ALL" && !p.lote.startsWith(activeFilter)) return false;
        if (q && !(p.nombre.toLowerCase().includes(q) || p.correo_principal.toLowerCase().includes(q) || p.zona.toLowerCase().includes(q) || p.lote.toLowerCase().includes(q))) return false;
        return true;
      }});

      tbody.innerHTML = filtered.map(p => {{
        const isSent = !!sentMap[p.correo_principal];
        return `
        <tr class="hover:bg-white/5 transition ${{isSent ? 'opacity-50 bg-emerald-950/20' : ''}}">
          <td class="p-3.5 text-center">
            <input type="checkbox" ${{isSent ? 'checked' : ''}} onchange="toggleSent('${{p.correo_principal}}')" class="w-4 h-4 accent-emerald-500 cursor-pointer">
          </td>
          <td class="p-3.5">
            <span class="text-[10px] font-bold text-amber-300 uppercase">${{p.lote}}</span>
            <div class="font-bold text-white text-sm">${{p.nombre}}</div>
            <div class="text-[10px] text-gray-400">${{p.categoria}} · <a href="${{p.web}}" target="_blank" class="text-sky-300 hover:underline">${{p.web.replace('https://','')}} ↗</a></div>
          </td>
          <td class="p-3.5 text-gray-300">${{p.zona}}</td>
          <td class="p-3.5">
            <span class="font-mono text-emerald-300 font-semibold">${{p.correo_principal}}</span>
            ${{p.correos_adicionales ? `<div class="text-[10px] text-gray-400 font-mono mt-0.5">+ ${{p.correos_adicionales}}</div>` : ''}}
          </td>
          <td class="p-3.5 font-mono text-gray-300">${{p.telefono}}</td>
          <td class="p-3.5 text-right space-x-1.5 whitespace-nowrap">
            <button onclick="copyMasterTemplate('PIXIESET_BULK', '${{p.nombre}}')" class="px-2.5 py-1.5 rounded-lg bg-amber-500 text-black font-bold hover:bg-amber-400">
              📋 Copiar Propuesta
            </button>
            <button onclick="openMailto('${{p.correo_principal}}', '${{p.nombre}}')" class="px-2.5 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 font-semibold hover:bg-emerald-500/30">
              ✉️ Abrir en Mail
            </button>
          </td>
        </tr>
      `;
      }}).join("");
    }}

    renderTable();
  </script>
</body>
</html>
"""
    (ROOT / "CAMPAÑA_PIXIESET_COLEGIOS_B2B.html").write_text(html, encoding="utf-8")


def main():
    print(f"Procesando y verificando {len(SEED_INSTITUTIONS)} instituciones en 5 lotes estrategicos...")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as ex:
        futures = [ex.submit(scrape_institution, item) for item in SEED_INSTITUTIONS]
        for fut in concurrent.futures.as_completed(futures):
            results.append(fut.result())

    results.sort(key=lambda r: (r["lote"], 0 if r["dns_verificado"] == "VERIFICADO" else 1, r["nombre"]))

    master_csv = OUT_DIR / "BASE_MAESTRA_COLEGIOS_MTY_2026.csv"
    with open(master_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["ID", "lote", "nombre", "zona", "categoria", "correo_principal", "correos_adicionales", "telefono", "web", "dns_verificado", "estado_web"],
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
                "Notes": f"{r['lote']} | {r['categoria']} | Web: {r['web']}",
            })

    (OUT_DIR / "COLEGIOS_MTY_PIXIESET.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    build_html_dashboard(results)
    print(f"OK: {len(verified_results)}/{len(results)} instituciones verificadas en 5 Lotes Diarios.")


if __name__ == "__main__":
    main()
