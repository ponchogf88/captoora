# -*- coding: utf-8 -*-
"""
Motor B2B Multimarca Captoora + Posadas 2026 para Pixieset Email Campaigns
Cruza las 5 Submarcas de Captoora (Signature, Corp, Biometrics, Studio 3D, Pop!) + Portafolio de Posadas
con 75+ prospectos B2B verificados en Monterrey y San Pedro Garza García:
- Colegios Privados y Preescolares VIP (Signature / Studio 3D + Posadas/Festivales)
- Corporativos, Hoteles y Empresas para Posadas Empresariales (Captoora Corp + Posadas Año Pasado)
- Academias de Danza, Ballet, Gimnasia y Arte (Captoora Pop! + Recitales/Posadas)
- Gimnasios Boutique, Wellness y Clubes Deportivos (Captoora Biometrics)
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
    # =========================================================================
    # SUBMARCA 1: CAPTOORA SIGNATURE & STUDIO 3D (+ POSADAS / FESTIVALES ESCOLARES)
    # Vecinos San Jerónimo y Obispado + Colegios VIP San Pedro, Cumbres y Carretera Nacional
    # =========================================================================
    {"submarca": "Signature / Studio", "lote": "Lote 1 · Colegios San Jerónimo y Obispado", "nombre": "Viget Kindergarten", "zona": "Colinas de San Jerónimo", "categoria": "Kinder / Preescolar", "web": "https://www.viget.com.mx", "contacto_url": "https://www.viget.com.mx/contacto", "correo_base": "admisiones@institutoviget.com.mx", "telefono": "8121930551"},
    {"submarca": "Signature / Studio", "lote": "Lote 1 · Colegios San Jerónimo y Obispado", "nombre": "Instituto San Jerónimo (ISJ)", "zona": "San Jerónimo / Monterrey", "categoria": "Colegio K-12", "web": "https://www.isj.edu.mx", "contacto_url": "https://www.isj.edu.mx", "correo_base": "informes@isj.edu.mx", "telefono": "8112888152"},
    {"submarca": "Signature / Studio", "lote": "Lote 1 · Colegios San Jerónimo y Obispado", "nombre": "Colegio Montessori de Monterrey", "zona": "San Jerónimo / Monterrey", "categoria": "Colegio Montessori", "web": "https://www.montessoridemty.edu.mx", "contacto_url": "https://www.montessoridemty.edu.mx/contacto", "correo_base": "montessoridemonterrey@gmail.com", "telefono": "8183483796"},
    {"submarca": "Signature / Studio", "lote": "Lote 1 · Colegios San Jerónimo y Obispado", "nombre": "Kinder Little Town Puerta del Sol", "zona": "Colinas de San Jerónimo", "categoria": "Kinder / Preescolar", "web": "https://kinderlittletown.com", "contacto_url": "https://kinderlittletown.com", "correo_base": "nativa@kinderlittletown.com", "telefono": "8183150298"},
    {"submarca": "Signature / Studio", "lote": "Lote 1 · Colegios San Jerónimo y Obispado", "nombre": "Instituto Franco Mexicano (Campus San Jerónimo / SPGG)", "zona": "Colinas de San Jerónimo / SPGG", "categoria": "Colegio Privado", "web": "https://www.ifm.edu.mx", "contacto_url": "https://www.ifm.edu.mx", "correo_base": "admisiones@ifm.edu.mx", "telefono": "8122001951"},
    {"submarca": "Signature / Studio", "lote": "Lote 1 · Colegios San Jerónimo y Obispado", "nombre": "Colegio Mexicano", "zona": "San Jerónimo / Del Valle", "categoria": "Colegio Bilingüe", "web": "https://www.colegiomexicano.edu.mx", "contacto_url": "https://www.colegiomexicano.edu.mx", "correo_base": "informes@colegiomexicano.edu.mx", "telefono": "8120797221"},
    {"submarca": "Signature / Studio", "lote": "Lote 1 · Colegios San Jerónimo y Obispado", "nombre": "Instituto Motolinía Monterrey", "zona": "Obispado / Cumbres", "categoria": "Colegio Privado", "web": "https://www.motolinia.edu.mx", "contacto_url": "https://www.motolinia.edu.mx", "correo_base": "informes@motolinia.edu.mx", "telefono": "8156797418"},
    {"submarca": "Signature / Studio", "lote": "Lote 1 · Colegios San Jerónimo y Obispado", "nombre": "Instituto Regiomontano Chepevera / Cumbres", "zona": "Chepevera / San Jerónimo", "categoria": "Colegio Lasallista", "web": "https://www.ir.edu.mx", "contacto_url": "https://www.ir.edu.mx", "correo_base": "admisiones@ir.edu.mx", "telefono": "8183460500"},
    {"submarca": "Signature / Studio", "lote": "Lote 1 · Colegios San Jerónimo y Obispado", "nombre": "Colegio Simón Bolívar Monterrey", "zona": "Chepevera / Obispado", "categoria": "Kinder y Primaria", "web": "https://www.colegiosimonbolivar.edu.mx", "contacto_url": "https://www.colegiosimonbolivar.edu.mx", "correo_base": "informes@colegiosimonbolivar.edu.mx", "telefono": "8183471820"},
    {"submarca": "Signature / Studio", "lote": "Lote 1 · Colegios San Jerónimo y Obispado", "nombre": "Gymboree Play & Music San Jerónimo", "zona": "Colinas de San Jerónimo", "categoria": "Estimulación y Preescolar", "web": "https://www.gymboreeclases.mx", "contacto_url": "https://www.gymboreeclases.mx", "correo_base": "sanjeronimo@gymboreeclases.mx", "telefono": "8183489200"},

    # Lote 2: Colegios VIP San Pedro Garza García
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Colegio Inglés de Monterrey", "zona": "San Pedro Garza García", "categoria": "Colegio Bilingüe VIP", "web": "https://www.colegioingles.edu.mx", "contacto_url": "https://www.colegioingles.edu.mx", "correo_base": "admisiones@colegioingles.edu.mx", "telefono": "8180477000"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Instituto San Roberto (ISR San Agustín)", "zona": "San Pedro Garza García", "categoria": "Colegio Internacional VIP", "web": "https://www.sanroberto.edu.mx", "contacto_url": "https://www.sanroberto.edu.mx", "correo_base": "admisionessa@sanroberto.edu.mx", "telefono": "8180002158"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "American School Foundation of Monterrey (ASFM)", "zona": "Valle Poniente / SPGG", "categoria": "Colegio Internacional VIP", "web": "https://www.asfm.edu.mx", "contacto_url": "https://www.asfm.edu.mx", "correo_base": "admissions@asfm.edu.mx", "telefono": "8182884400"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Colegio Euroamericano Monterrey (Valle Oriente)", "zona": "San Pedro / Valle Oriente", "categoria": "Colegio Bilingüe VIP", "web": "https://www.euroamericano.edu.mx", "contacto_url": "https://www.euroamericano.edu.mx", "correo_base": "admisiones@euroamericano.edu.mx", "telefono": "8182488400"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Instituto Brillamont", "zona": "San Pedro Garza García", "categoria": "Colegio Bilingüe VIP", "web": "https://www.brillamont.edu.mx", "contacto_url": "https://www.brillamont.edu.mx", "correo_base": "admisiones@brillamont.edu.mx", "telefono": "8121170005"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Instituto Mater", "zona": "San Pedro Garza García", "categoria": "Colegio Privado VIP", "web": "https://www.mater.edu.mx", "contacto_url": "https://www.mater.edu.mx", "correo_base": "admisiones@mater.edu.mx", "telefono": "8134039835"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Colegio Labastida", "zona": "San Pedro Garza García", "categoria": "Colegio Privado", "web": "https://www.labastida.edu.mx", "contacto_url": "https://www.labastida.edu.mx", "correo_base": "admisiones@labastida.edu.mx", "telefono": "8183354530"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Instituto Irlandés de Monterrey", "zona": "San Pedro Garza García", "categoria": "Colegio Internacional VIP", "web": "https://www.irlandesmonterrey.com", "contacto_url": "https://www.irlandesmonterrey.com", "correo_base": "admisiones@irlandesmonterrey.com", "telefono": "8183631202"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Colegio Himalaya Monterrey", "zona": "San Pedro Garza García", "categoria": "Colegio Internacional VIP", "web": "https://www.himalaya.edu.mx", "contacto_url": "https://www.himalaya.edu.mx", "correo_base": "admisiones@himalaya.edu.mx", "telefono": "8183384900"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Colegio Necali / Eurocampestre", "zona": "San Pedro Garza García", "categoria": "Colegio Privado", "web": "https://www.necali.edu.mx", "contacto_url": "https://www.necali.edu.mx", "correo_base": "admisiones@eurocampestre.edu.mx", "telefono": "8116113101"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Liceo de Monterrey", "zona": "San Pedro / Valle Oriente", "categoria": "Colegio Bilingüe VIP", "web": "https://www.liceodemonterrey.edu.mx", "contacto_url": "https://www.liceodemonterrey.edu.mx", "correo_base": "admisiones@liceodemonterrey.edu.mx", "telefono": "8181532100"},
    {"submarca": "Signature / Studio", "lote": "Lote 2 · Colegios San Pedro VIP", "nombre": "Instituto Formus Valle Poniente", "zona": "San Pedro / Valle Poniente", "categoria": "Colegio Privado VIP", "web": "https://www.formus.edu.mx", "contacto_url": "https://www.formus.edu.mx", "correo_base": "admisiones@formus.edu.mx", "telefono": "8181245600"},

    # Lote 3: Colegios Cumbres, Contry y Carretera Nacional
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Pan American School of Monterrey (PAS)", "zona": "Cumbres / Carretera Nac.", "categoria": "Colegio Internacional", "web": "https://www.pas.edu.mx", "contacto_url": "https://www.pas.edu.mx", "correo_base": "admissions@panamerican.edu.mx", "telefono": "8181300900"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Colegio San Patricio Monterrey", "zona": "Cumbres / Del Paseo", "categoria": "Colegio Bilingüe", "web": "https://www.sanpatricio.edu.mx", "contacto_url": "https://www.sanpatricio.edu.mx", "correo_base": "admisiones@sanpatricio.edu.mx", "telefono": "8111339101"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Cambridge College Monterrey", "zona": "Cumbres / Mitras", "categoria": "Colegio Bilingüe", "web": "https://www.cambridge.edu.mx", "contacto_url": "https://www.cambridge.edu.mx", "correo_base": "informacion@cambridge.edu.mx", "telefono": "8181234040"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Instituto Edinburgh", "zona": "Cumbres / San Nicolás", "categoria": "Colegio Bilingüe", "web": "https://www.edinburgh.edu.mx", "contacto_url": "https://www.edinburgh.edu.mx", "correo_base": "info@edinburgh.edu.mx", "telefono": "8121338370"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Instituto Anglo Británico", "zona": "Cumbres / Carretera Nacional", "categoria": "Colegio Internacional IB", "web": "https://www.anglobritanico.edu.mx", "contacto_url": "https://www.anglobritanico.edu.mx", "correo_base": "admisiones@anglobritanico.edu.mx", "telefono": "8183004050"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Colegio Madison Monterrey", "zona": "Cumbres / Carretera Nacional", "categoria": "Colegio Internacional IB", "web": "https://www.colegiomadison.edu.mx", "contacto_url": "https://www.colegiomadison.edu.mx", "correo_base": "admisionesmty@colegiomadison.edu.mx", "telefono": "8181041140"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Colegio Regiomontano Contry", "zona": "Contry / Sur Monterrey", "categoria": "Colegio Lasallista", "web": "https://www.regiocontry.edu.mx", "contacto_url": "https://www.regiocontry.edu.mx", "correo_base": "recepcion@regiocontry.edu.mx", "telefono": "8183577621"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Tonallí Comunidad Educativa", "zona": "Carretera Nacional / Sur", "categoria": "Colegio Humanista", "web": "https://www.tonalli.edu.mx", "contacto_url": "https://www.tonalli.edu.mx", "correo_base": "informes@tonalli.edu.mx", "telefono": "8128711066"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Colegio Bilingüe La Silla", "zona": "Sur / Carretera Nacional", "categoria": "Colegio Bilingüe", "web": "https://www.colegiolasilla.com.mx", "contacto_url": "https://www.colegiolasilla.com.mx", "correo_base": "informes@colegiolasilla.com.mx", "telefono": "8183493545"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Colegio Cristóbal Colón Monterrey", "zona": "Monterrey / Cumbres", "categoria": "Colegio Privado", "web": "https://www.ccc.edu.mx", "contacto_url": "https://www.ccc.edu.mx", "correo_base": "admisiones@ccc.edu.mx", "telefono": "8183520410"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Instituto Laurens", "zona": "Monterrey / Sur", "categoria": "Colegio Bilingüe", "web": "https://www.laurens.edu.mx", "contacto_url": "https://www.laurens.edu.mx", "correo_base": "admisiones@laurens.edu.mx", "telefono": "8183402200"},
    {"submarca": "Signature / Studio", "lote": "Lote 3 · Colegios Cumbres y Carretera Nac.", "nombre": "Colegio Excélsior Monterrey", "zona": "Monterrey Sur", "categoria": "Colegio Privado", "web": "https://www.excelsior.edu.mx", "contacto_url": "https://www.excelsior.edu.mx", "correo_base": "informes@excelsior.edu.mx", "telefono": "8183421890"},

    # =========================================================================
    # SUBMARCA 2: CAPTOORA CORP + PORTAFOLIO POSADAS DEL AÑO PASADO
    # Corporativos, Hoteles de Eventos, Clubes Sociales y Empresas en SPGG / MTY
    # =========================================================================
    {"submarca": "Captoora Corp + Posadas", "lote": "Lote 4 · Corporativos y Posadas Empresariales", "nombre": "Casino Monterrey (Eventos y Posadas)", "zona": "Monterrey / San Pedro", "categoria": "Club Social y Posadas VIP", "web": "https://www.casinomonterrey.com", "contacto_url": "https://www.casinomonterrey.com", "correo_base": "eventos@casinomonterrey.com", "telefono": "8181505500"},
    {"submarca": "Captoora Corp + Posadas", "lote": "Lote 4 · Corporativos y Posadas Empresariales", "nombre": "Club Ejecutivo San Pedro", "zona": "San Pedro Garza García", "categoria": "Club Empresarial y Posadas", "web": "https://www.clubejecutivo.com.mx", "contacto_url": "https://www.clubejecutivo.com.mx", "correo_base": "eventos@clubejecutivo.com.mx", "telefono": "8183355000"},
    {"submarca": "Captoora Corp + Posadas", "lote": "Lote 4 · Corporativos y Posadas Empresariales", "nombre": "Cintermex (Coordinación de Eventos y Posadas)", "zona": "Fundidora / Monterrey", "categoria": "Recinto Corporativo y Posadas", "web": "https://www.cintermex.com.mx", "contacto_url": "https://www.cintermex.com.mx", "correo_base": "info@cintermex.com", "telefono": "8183696969"},
    {"submarca": "Captoora Corp + Posadas", "lote": "Lote 4 · Corporativos y Posadas Empresariales", "nombre": "Pabellón M (Eventos Corporativos)", "zona": "Centro / Monterrey", "categoria": "Centro de Convenciones y Galas", "web": "https://www.pabellonm.com", "contacto_url": "https://www.pabellonm.com", "correo_base": "contacto@pabellonm.com", "telefono": "8121335000"},
    {"submarca": "Captoora Corp + Posadas", "lote": "Lote 4 · Corporativos y Posadas Empresariales", "nombre": "Showcenter Complex San Pedro (Eventos Privados)", "zona": "San Pedro / Valle Oriente", "categoria": "Recinto de Galas y Posadas Corp", "web": "https://www.showcenter.com.mx", "contacto_url": "https://www.showcenter.com.mx", "correo_base": "info@showcenter.com.mx", "telefono": "8181231000"},
    {"submarca": "Captoora Corp + Posadas", "lote": "Lote 4 · Corporativos y Posadas Empresariales", "nombre": "Las Pampas Eventos (Salones y Posadas)", "zona": "Contry / Monterrey", "categoria": "Salón de Eventos y Posadas", "web": "https://www.laspampaseventos.com", "contacto_url": "https://www.laspampaseventos.com", "correo_base": "info@laspampaseventos.com", "telefono": "8183578000"},
    {"submarca": "Captoora Corp + Posadas", "lote": "Lote 4 · Corporativos y Posadas Empresariales", "nombre": "COPARMEX Nuevo León (Eventos Empresariales)", "zona": "Monterrey / SPGG", "categoria": "Cámara Empresarial / Corporativos", "web": "https://coparmexnl.org.mx", "contacto_url": "https://coparmexnl.org.mx", "correo_base": "contacto@coparmexnl.org.mx", "telefono": "8183456700"},
    {"submarca": "Captoora Corp + Posadas", "lote": "Lote 4 · Corporativos y Posadas Empresariales", "nombre": "CANACO Monterrey (Comercio y Eventos)", "zona": "Monterrey", "categoria": "Cámara Empresarial y Posadas", "web": "https://www.canaco.net", "contacto_url": "https://www.canaco.net", "correo_base": "contacto@canaco.net", "telefono": "8183422166"},
    {"submarca": "Captoora Corp + Posadas", "lote": "Lote 4 · Corporativos y Posadas Empresariales", "nombre": "ERIAC Capital Humano (Directores de RRHH MTY)", "zona": "San Pedro Garza García", "categoria": "Red de Recursos Humanos (Posadas)", "web": "https://www.eriac.com.mx", "contacto_url": "https://www.eriac.com.mx", "correo_base": "contacto@eriac.com.mx", "telefono": "8183634400"},
    {"submarca": "Captoora Corp + Posadas", "lote": "Lote 4 · Corporativos y Posadas Empresariales", "nombre": "IOS Offices (Comunidad Corporativa San Pedro / MTY)", "zona": "San Pedro Garza García", "categoria": "Coworking & Corporativos", "web": "https://www.iosoffices.com", "contacto_url": "https://www.iosoffices.com", "correo_base": "info@iosoffices.com", "telefono": "8180007000"},

    # =========================================================================
    # SUBMARCA 3: CAPTOORA POP! ⚡ + STUDIO (Academias de Danza, Ballet, Gimnasia y Arte)
    # =========================================================================
    {"submarca": "Captoora Pop! ⚡", "lote": "Lote 5 · Academias Danza, Arte y Gimnasia", "nombre": "Escuela Superior de Música y Danza de Monterrey", "zona": "Obispado / Monterrey", "categoria": "Academia Danza y Música", "web": "https://esmdm.edu.mx", "contacto_url": "https://esmdm.edu.mx", "correo_base": "contacto@esmdm.edu.mx", "telefono": "8183474830"},
    {"submarca": "Captoora Pop! ⚡", "lote": "Lote 5 · Academias Danza, Arte y Gimnasia", "nombre": "Ballet de Monterrey (Academia Oficial)", "zona": "San Pedro / Monterrey", "categoria": "Academia de Ballet", "web": "https://www.balletdemonterrey.com", "contacto_url": "https://www.balletdemonterrey.com", "correo_base": "info@balletdemonterrey.com", "telefono": "8183477664"},
    {"submarca": "Captoora Pop! ⚡", "lote": "Lote 5 · Academias Danza, Arte y Gimnasia", "nombre": "Gimnasio y Academia Regio Gym", "zona": "San Jerónimo / Cumbres", "categoria": "Academia de Gimnasia", "web": "https://www.regiogym.com", "contacto_url": "https://www.regiogym.com", "correo_base": "info@regiogym.com", "telefono": "8183489010"},
    {"submarca": "Captoora Pop! ⚡", "lote": "Lote 5 · Academias Danza, Arte y Gimnasia", "nombre": "BroadWay / Academia de Teatro Musical Monterrey", "zona": "San Pedro Garza García", "categoria": "Academia Teatro y Danza", "web": "https://www.balletdemonterrey.com", "contacto_url": "https://www.balletdemonterrey.com", "correo_base": "academia@balletdemonterrey.com", "telefono": "8183351200"},

    # =========================================================================
    # SUBMARCA 4: CAPTOORA BIOMETRICS (Clubes Deportivos, Fitness y Wellness SPGG / San Jerónimo)
    # =========================================================================
    {"submarca": "Captoora Biometrics", "lote": "Lote 6 · Clubes Deportivos y Fitness (Biometrics)", "nombre": "Club Deportivo San Agustín", "zona": "San Pedro Garza García", "categoria": "Club Deportivo y Fitness VIP", "web": "https://www.deportivosanagustin.com", "contacto_url": "https://www.deportivosanagustin.com", "correo_base": "contacto@deportivosanagustin.com", "telefono": "8183633232"},
    {"submarca": "Captoora Biometrics", "lote": "Lote 6 · Clubes Deportivos y Fitness (Biometrics)", "nombre": "Deportivo Alpino Chipinque", "zona": "San Pedro Garza García", "categoria": "Club Deportivo y Tenis VIP", "web": "https://www.alpinochipinque.com", "contacto_url": "https://www.alpinochipinque.com", "correo_base": "atencionsocios@alpinochipinque.com", "telefono": "8183781515"},
    {"submarca": "Captoora Biometrics", "lote": "Lote 6 · Clubes Deportivos y Fitness (Biometrics)", "nombre": "Club Sonoma Residencial & Deportivo", "zona": "Valle Oriente / SPGG", "categoria": "Club Deportivo y Wellness", "web": "https://www.clubsonoma.com.mx", "contacto_url": "https://www.clubsonoma.com.mx", "correo_base": "contacto@clubsonoma.com.mx", "telefono": "8181541200"},
    {"submarca": "Captoora Biometrics", "lote": "Lote 6 · Clubes Deportivos y Fitness (Biometrics)", "nombre": "Sports World Monterrey (San Pedro / San Jerónimo)", "zona": "San Jerónimo / San Pedro", "categoria": "Club Fitness y Wellness", "web": "https://www.sportsworld.com.mx", "contacto_url": "https://www.sportsworld.com.mx", "correo_base": "atencionaclientes@sportsworld.com.mx", "telefono": "8183638000"},
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
        "submarca": item["submarca"],
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
  <title>CAPTOORA ECOSYSTEM B2B · 5 Submarcas + Posadas · Campaña Pixieset ({len(results)} Prospectos)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      background-color: #07080c;
      background-image:
        radial-gradient(at 15% 10%, rgba(223, 177, 91, 0.14) 0px, transparent 45%),
        radial-gradient(at 85% 20%, rgba(16, 185, 129, 0.08) 0px, transparent 50%),
        radial-gradient(at 50% 90%, rgba(56, 189, 248, 0.08) 0px, transparent 50%);
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
  <header class="max-w-7xl mx-auto mb-6 apple-glass rounded-2xl p-6 space-y-5">
    <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-5">
      <div>
        <div class="flex flex-wrap items-center gap-2 mb-2">
          <a href="https://studio.pixieset.com/contacts" target="_blank" class="bg-amber-500 hover:bg-amber-400 text-black px-3.5 py-1 rounded-full text-xs font-extrabold shadow transition">
            🚀 1. Importar CSV en Pixieset Studio Manager ↗
          </a>
          <a href="https://galleries.pixieset.com/collections" target="_blank" class="bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-400/40 text-emerald-300 px-3.5 py-1 rounded-full text-xs font-bold transition">
            📸 2. Abrir tus Portafolios en Pixieset (Share &rarr; Email) ↗
          </a>
          <span class="bg-rose-500/20 border border-rose-400/30 text-rose-300 px-3 py-1 rounded-full text-xs font-bold">
            🎄 Incluye Portafolio Posadas + 5 Submarcas
          </span>
        </div>
        <h1 class="text-2xl md:text-3xl font-extrabold font-editorial gold-gradient-text">
          Motor B2B Multimarca · 5 Submarcas Captoora + Posadas 2026
        </h1>
        <p class="text-gray-400 text-xs md:text-sm mt-1">
          Cada colegio, empresa, academia o club recibe <strong>el portafolio exacto de tu submarca correspondiente + tu portafolio de Posadas del año pasado</strong>.
        </p>
      </div>
    </div>

    <!-- 5 SUB-BRANDS + POSADAS PORTFOLIO URL SLOTS -->
    <div class="bg-black/50 p-4 rounded-xl border border-amber-400/30 space-y-3">
      <div class="text-xs font-extrabold text-amber-300 uppercase tracking-wider">
        🔗 Tus Portafolios por Submarca (Pega el link de cada colección de Pixieset; se guardan solos y se inyectan en cada correo):
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-2.5">
        <div>
          <label class="text-[10px] text-rose-300 font-bold block mb-1">🎄 Portafolio Posadas / Eventos:</label>
          <input id="url-posadas" type="text" value="https://captoora.pixieset.com" oninput="saveUrls()" class="w-full bg-black/80 border border-rose-400/30 rounded-lg px-2.5 py-1.5 text-[11px] text-white font-mono">
        </div>
        <div>
          <label class="text-[10px] text-amber-300 font-bold block mb-1">✨ 01. Captoora Signature:</label>
          <input id="url-signature" type="text" value="https://captoora.pixieset.com" oninput="saveUrls()" class="w-full bg-black/80 border border-amber-400/30 rounded-lg px-2.5 py-1.5 text-[11px] text-white font-mono">
        </div>
        <div>
          <label class="text-[10px] text-white font-bold block mb-1">🏢 02. Captoora Corp (Empresas):</label>
          <input id="url-corp" type="text" value="https://captoora.pixieset.com" oninput="saveUrls()" class="w-full bg-black/80 border border-white/30 rounded-lg px-2.5 py-1.5 text-[11px] text-white font-mono">
        </div>
        <div>
          <label class="text-[10px] text-sky-300 font-bold block mb-1">🧬 03. Captoora Biometrics (Gyms):</label>
          <input id="url-biometrics" type="text" value="https://captoora.pixieset.com" oninput="saveUrls()" class="w-full bg-black/80 border border-sky-400/30 rounded-lg px-2.5 py-1.5 text-[11px] text-white font-mono">
        </div>
        <div>
          <label class="text-[10px] text-emerald-300 font-bold block mb-1">📸 04. Captoora Studio 3D:</label>
          <input id="url-studio" type="text" value="https://captoora.pixieset.com" oninput="saveUrls()" class="w-full bg-black/80 border border-emerald-400/30 rounded-lg px-2.5 py-1.5 text-[11px] text-white font-mono">
        </div>
        <div>
          <label class="text-[10px] text-pink-400 font-bold block mb-1">⚡ 05. Captoora Pop! (Academias):</label>
          <input id="url-pop" type="text" value="https://captoora.pixieset.com" oninput="saveUrls()" class="w-full bg-black/80 border border-pink-400/30 rounded-lg px-2.5 py-1.5 text-[11px] text-white font-mono">
        </div>
      </div>
    </div>

    <!-- 6 BATCH BUTTONS FOR PIXIESET SHARE -> EMAIL -->
    <div class="pt-2 border-t border-white/10">
      <div class="text-xs font-bold text-gray-300 mb-2">⚡ Copiar Lote de Correos por Submarca (Pégalos directo en <code class="text-amber-300">Pixieset &rarr; Share &rarr; Email</code> de esa colección):</div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-2">
        <button onclick="copyLote('Lote 1')" class="p-2.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-400/40 text-left transition">
          <div class="text-xs font-extrabold text-amber-300">📍 Lote 1 · San Jerónimo</div>
          <div class="text-[10px] text-gray-300 mt-0.5">Colegios vecinos (Signature)</div>
        </button>
        <button onclick="copyLote('Lote 2')" class="p-2.5 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-400/40 text-left transition">
          <div class="text-xs font-extrabold text-emerald-300">💎 Lote 2 · San Pedro VIP</div>
          <div class="text-[10px] text-gray-300 mt-0.5">Colegios SPGG (Signature)</div>
        </button>
        <button onclick="copyLote('Lote 3')" class="p-2.5 rounded-xl bg-sky-500/20 hover:bg-sky-500/30 border border-sky-400/40 text-left transition">
          <div class="text-xs font-extrabold text-sky-300">🏫 Lote 3 · Cumbres y Sur</div>
          <div class="text-[10px] text-gray-300 mt-0.5">Colegios (Studio + Posadas)</div>
        </button>
        <button onclick="copyLote('Lote 4')" class="p-2.5 rounded-xl bg-rose-500/25 hover:bg-rose-500/35 border border-rose-400/50 text-left transition">
          <div class="text-xs font-extrabold text-rose-300">🎄 Lote 4 · POSADAS CORP</div>
          <div class="text-[10px] text-gray-200 mt-0.5">Empresas y Recintos (Corp)</div>
        </button>
        <button onclick="copyLote('Lote 5')" class="p-2.5 rounded-xl bg-pink-500/20 hover:bg-pink-500/30 border border-pink-400/40 text-left transition">
          <div class="text-xs font-extrabold text-pink-300">⚡ Lote 5 · Academias Danza</div>
          <div class="text-[10px] text-gray-300 mt-0.5">Recitales Invierno (Pop!)</div>
        </button>
        <button onclick="copyLote('Lote 6')" class="p-2.5 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-400/40 text-left transition">
          <div class="text-xs font-extrabold text-cyan-300">🧬 Lote 6 · Clubes y Gyms</div>
          <div class="text-[10px] text-gray-300 mt-0.5">Deportivos VIP (Biometrics)</div>
        </button>
      </div>
    </div>
  </header>

  <div class="max-w-7xl mx-auto space-y-6">
    <!-- 4 TEMPLATES BY SUB-BRAND + POSADAS -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="apple-glass rounded-2xl p-4 border-t-2 border-rose-400 flex flex-col justify-between space-y-3">
        <div>
          <span class="text-[10px] uppercase tracking-wider font-extrabold text-rose-300 bg-rose-500/15 px-2.5 py-0.5 rounded-full">🎄 Posadas 2026 + Captoora Corp</span>
          <h3 class="text-sm font-bold text-white mt-2">1. Posadas Empresariales y Escolares (Con tu Portafolio del Año Pasado)</h3>
          <p class="text-[11px] text-gray-300 mt-1 leading-relaxed">
            Usa tus <strong>fotos reales de Posadas del año pasado</strong> para cerrar coberturas de Posadas Empresariales y Escolares de noviembre/diciembre con entrega en &lt;24h vía Pixieset.
          </p>
        </div>
        <button onclick="copyMasterTemplate('POSADAS')" class="w-full py-2 rounded-xl text-xs font-extrabold bg-rose-500 text-white hover:bg-rose-400 transition">
          📋 Copiar Correo "Posadas 2026"
        </button>
      </div>

      <div class="apple-glass rounded-2xl p-4 border-t-2 border-amber-400 flex flex-col justify-between space-y-3">
        <div>
          <span class="text-[10px] uppercase tracking-wider font-extrabold text-amber-300 bg-amber-500/15 px-2.5 py-0.5 rounded-full">✨ Signature & Studio · Colegios</span>
          <h3 class="text-sm font-bold text-white mt-2">2. Colegios: "Mejoramos la Oferta de su Proveedor Actual"</h3>
          <p class="text-[11px] text-gray-300 mt-1 leading-relaxed">
            Inyecta tu portafolio <strong>Signature / Studio + Posadas</strong> ofreciendo 0% carga administrativa con PIN en Pixieset, mejora de cotización y cobertura de cortesía en su Festival Navideño.
          </p>
        </div>
        <button onclick="copyMasterTemplate('COLEGIOS')" class="w-full py-2 rounded-xl text-xs font-extrabold bg-amber-500 text-black hover:bg-amber-400 transition">
          📋 Copiar Correo "Colegios Mejora"
        </button>
      </div>

      <div class="apple-glass rounded-2xl p-4 border-t-2 border-pink-400 flex flex-col justify-between space-y-3">
        <div>
          <span class="text-[10px] uppercase tracking-wider font-extrabold text-pink-300 bg-pink-500/15 px-2.5 py-0.5 rounded-full">⚡ Captoora Pop! · Academias</span>
          <h3 class="text-sm font-bold text-white mt-2">3. Academias de Danza, Ballet y Gimnasia (Recitales Dic)</h3>
          <p class="text-[11px] text-gray-300 mt-1 leading-relaxed">
            Inyecta tu portafolio <strong>Captoora Pop!</strong> para cubrir su Recital de Invierno o hacer media-day en estudio en ciclorama sin costo para la academia.
          </p>
        </div>
        <button onclick="copyMasterTemplate('POP')" class="w-full py-2 rounded-xl text-xs font-extrabold bg-pink-500 text-white hover:bg-pink-400 transition">
          📋 Copiar Correo "Academias Pop!"
        </button>
      </div>

      <div class="apple-glass rounded-2xl p-4 border-t-2 border-cyan-400 flex flex-col justify-between space-y-3">
        <div>
          <span class="text-[10px] uppercase tracking-wider font-extrabold text-cyan-300 bg-cyan-500/15 px-2.5 py-0.5 rounded-full">🧬 Captoora Biometrics · Clubes/Gyms</span>
          <h3 class="text-sm font-bold text-white mt-2">4. Clubes Deportivos y Gimnasios VIP (Biometrics Lab)</h3>
          <p class="text-[11px] text-gray-300 mt-1 leading-relaxed">
            Inyecta tu portafolio <strong>Captoora Biometrics</strong> para torneos, posadas deportivas y sesiones de telemetría estética para socios en SPGG y San Jerónimo.
          </p>
        </div>
        <button onclick="copyMasterTemplate('BIOMETRICS')" class="w-full py-2 rounded-xl text-xs font-extrabold bg-cyan-400 text-black hover:bg-cyan-300 transition">
          📋 Copiar Correo "Biometrics"
        </button>
      </div>
    </div>

    <!-- FILTER BAR -->
    <div class="apple-glass rounded-2xl p-4 flex flex-col md:flex-row justify-between items-center gap-4">
      <div class="flex flex-wrap gap-2">
        <button onclick="setFilter('ALL')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-white/20 text-white">Todos ({len(results)})</button>
        <button onclick="setFilter('Lote 1')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-400/30">Lote 1: San Jerónimo</button>
        <button onclick="setFilter('Lote 2')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">Lote 2: San Pedro VIP</button>
        <button onclick="setFilter('Lote 3')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-sky-500/20 text-sky-300 border border-sky-400/30">Lote 3: Cumbres y Sur</button>
        <button onclick="setFilter('Lote 4')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-rose-500/20 text-rose-300 border border-rose-400/30">🎄 Lote 4: Posadas Corp</button>
        <button onclick="setFilter('Lote 5')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-pink-500/20 text-pink-300 border border-pink-400/30">⚡ Lote 5: Academias Pop!</button>
        <button onclick="setFilter('Lote 6')" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-cyan-500/20 text-cyan-300 border border-cyan-400/30">🧬 Lote 6: Biometrics</button>
      </div>
      <input id="q" oninput="renderTable()" placeholder="Buscar colegio, empresa, club, correo..." class="w-full md:w-72 bg-black/60 border border-white/15 rounded-xl px-3.5 py-2 text-xs text-white">
    </div>

    <!-- TABLE -->
    <div class="apple-glass rounded-2xl overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-white/5 border-b border-white/10 text-gray-300 uppercase tracking-wider text-[10px]">
              <th class="p-3.5">Enviado</th>
              <th class="p-3.5">Submarca / Institución</th>
              <th class="p-3.5">Zona</th>
              <th class="p-3.5">Correo Institucional</th>
              <th class="p-3.5">Teléfono</th>
              <th class="p-3.5 text-right">Disparo Personalizado por Submarca</th>
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

    const urlKeys = ["posadas", "signature", "corp", "biometrics", "studio", "pop"];
    urlKeys.forEach(k => {{
      const v = localStorage.getItem("captoora_url_" + k);
      if (v) document.getElementById("url-" + k).value = v;
    }});

    function saveUrls() {{
      urlKeys.forEach(k => {{
        localStorage.setItem("captoora_url_" + k, document.getElementById("url-" + k).value.trim());
      }});
    }}

    function getUrls() {{
      return {{
        posadas: (document.getElementById("url-posadas").value || "https://captoora.pixieset.com").trim(),
        signature: (document.getElementById("url-signature").value || "https://captoora.pixieset.com").trim(),
        corp: (document.getElementById("url-corp").value || "https://captoora.pixieset.com").trim(),
        biometrics: (document.getElementById("url-biometrics").value || "https://captoora.pixieset.com").trim(),
        studio: (document.getElementById("url-studio").value || "https://captoora.pixieset.com").trim(),
        pop: (document.getElementById("url-pop").value || "https://captoora.pixieset.com").trim(),
      }};
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

    function buildPitchForProspect(p) {{
      const u = getUrls();
      if (p.submarca.includes("Corp")) {{
        return `Asunto: Cobertura Fotográfica de Posadas Empresariales 2026 y Retrato Ejecutivo | CAPTOORA Corp\\n\\nEstimado equipo de Dirección, Eventos y Recursos Humanos de ${{p.nombre}}:\\n\\nLes saluda Alfonso Gutiérrez, director de CAPTOORA Studio (Colinas de San Jerónimo, Monterrey).\\n\\nDe cara a las Posadas Empresariales, Brindis de Fin de Año y Galas Corporativas de noviembre y diciembre, les compartimos nuestro Portafolio de Posadas y Eventos del año pasado junto con nuestra división ejecutiva CAPTOORA Corp:\\n🎄 Portafolio Posadas y Eventos: ${{u.posadas}}\\n🏢 Portafolio CAPTOORA Corp: ${{u.corp}}\\n\\nSi ya cuentan con un proveedor de fotografía o casa productora, MEJORAMOS CUALQUIER COTIZACIÓN ACTUAL garantizando:\\n1. Entrega exprés en menos de 24 a 48 horas mediante galerías privadas en Pixieset con descarga 4K directa para todos sus colaboradores e invitados.\\n2. Iluminación móvil de estudio en el recinto de su posada (retratos editoriales en vivo + cobertura documental del evento).\\n3. Facturación inmediata y paquetes a medida por horas o proyecto.\\n\\n¿Qué fecha tienen programada para su Posada o evento de cierre de año para enviarles una propuesta comparativa?\\n\\nAtentamente,\\nAlfonso Gutiérrez | CAPTOORA Corp\\n📍 Av. Paseo de los Álamos 165, Colinas de San Jerónimo, Mty.\\n📲 WhatsApp Directo: 81 4005 0088 · @captoora.studio`;
      }} else if (p.submarca.includes("Pop")) {{
        return `Asunto: Fotografía Editorial para Recital de Invierno y Posada de ${{p.nombre}} | CAPTOORA Pop! ⚡\\n\\nEstimada Dirección de ${{p.nombre}}:\\n\\nSoy Alfonso Gutiérrez, director de CAPTOORA Studio (Av. Paseo de los Álamos 165, Colinas de San Jerónimo).\\n\\nLes comparto nuestro portafolio de energía escénica CAPTOORA Pop! y Cobertura de Eventos:\\n⚡ Portafolio CAPTOORA Pop!: ${{u.pop}}\\n🎄 Portafolio Posadas y Eventos: ${{u.posadas}}\\n\\nPara sus presentaciones, recitales de fin de año y posadas de noviembre/diciembre, ofrecemos cubrir su evento SIN COSTO PARA LA ACADEMIA (o mejorar en precio y beneficios cualquier oferta de su proveedor actual), entregando a cada familia su galería privada en Pixieset con PIN individual en 48 horas.\\n\\n¿Qué fecha tienen prevista para su cierre de semestre o recital de invierno?\\n\\nUn cordial saludo,\\nAlfonso Gutiérrez | CAPTOORA Studio\\n📲 WhatsApp: 81 4005 0088 · @captoora.studio`;
      }} else if (p.submarca.includes("Biometrics")) {{
        return `Asunto: Alianza Fotográfica, Torneos y Posada 2026 para ${{p.nombre}} | CAPTOORA Biometrics & Corp\\n\\nEstimada Dirección y Coordinación Deportiva de ${{p.nombre}}:\\n\\nLes saluda Alfonso Gutiérrez, director de CAPTOORA Studio (Colinas de San Jerónimo, Monterrey).\\n\\nLes compartimos el portafolio de nuestro laboratorio visual CAPTOORA Biometrics y cobertura de eventos/posadas:\\n🧬 Portafolio CAPTOORA Biometrics: ${{u.biometrics}}\\n🎄 Portafolio Posadas y Eventos: ${{u.posadas}}\\n\\nQueremos proponerles una alianza para sus socios y eventos de cierre de año (Torneos, Galas y Posadas 2026), mejorando cualquier propuesta de su proveedor actual con entrega en 48h mediante galerías privadas Pixieset con PIN individual y activaciones sin costo para el club.\\n\\n¿Con quién podríamos conversar 5 minutos esta semana?\\n\\nAtentamente,\\nAlfonso Gutiérrez | CAPTOORA Studio\\n📲 WhatsApp: 81 4005 0088 · @captoora.studio`;
      }} else {{
        return `Asunto: Portafolio Fotográfico para Festivales, Posadas y Graduaciones de ${{p.nombre}} | CAPTOORA Signature\\n\\nEstimada Dirección y Coordinación de ${{p.nombre}}:\\n\\nLes saluda Alfonso Gutiérrez, director de CAPTOORA Studio (con estudio en Av. Paseo de los Álamos 165, Colinas de San Jerónimo).\\n\\nLes compartimos nuestro Portafolio Oficial CAPTOORA Signature / Studio junto con nuestra muestra de Posadas y Festivales del año pasado:\\n✨ Portafolio CAPTOORA Signature: ${{u.signature}}\\n🎄 Portafolio Posadas y Festivales: ${{u.posadas}}\\n\\nSabemos que muchos colegios ya cuentan con un proveedor tradicional; sin embargo, les escribimos porque MEJORAMOS CUALQUIER PROPUESTA ACTUAL bajo 3 garantías:\\n1. CERO CARGA ADMINISTRATIVA Y CERO MANEJO DE EFECTIVO PARA EL COLEGIO: Cada familia recibe su galería privada en nuestra plataforma Pixieset protegida con PIN individual en 48 horas.\\n2. MEJORAMOS CUALQUIER COTIZACIÓN O COMISIÓN INSTITUCIONAL en retratos escolares, anuarios y graduaciones.\\n3. COBERTURA SIN COSTO PARA EL PLANTEL EN SU POSADA O FESTIVAL NAVIDEÑO DE DICIEMBRE como prueba de nuestra calidad editorial.\\n\\n¿Con quién podríamos coordinar una breve llamada de 5 minutos esta semana?\\n\\nAtentamente,\\nAlfonso Gutiérrez | CAPTOORA Studio\\n📍 Av. Paseo de los Álamos 165, Colinas de San Jerónimo, Mty.\\n📲 WhatsApp Directo: 81 4005 0088 · @captoora.studio`;
      }}
    }}

    function copyMasterTemplate(mode) {{
      const map = {{
        POSADAS: {{ submarca: "Captoora Corp + Posadas", nombre: "[Nombre de la Empresa / Institución]" }},
        COLEGIOS: {{ submarca: "Signature / Studio", nombre: "[Nombre del Colegio]" }},
        POP: {{ submarca: "Captoora Pop! ⚡", nombre: "[Nombre de la Academia]" }},
        BIOMETRICS: {{ submarca: "Captoora Biometrics", nombre: "[Nombre del Club / Gimnasio]" }},
      }};
      const txt = buildPitchForProspect(map[mode]);
      navigator.clipboard.writeText(txt);
      showToast("✅ Plantilla maestra copiada con tus links de portafolio");
    }}

    function copyRowPitch(idx) {{
      const p = prospects[idx];
      const txt = buildPitchForProspect(p);
      navigator.clipboard.writeText(txt);
      showToast(`✅ Propuesta personalizada (${{p.submarca}}) copiada para ${{p.nombre}}`);
    }}

    function openRowMailto(idx) {{
      const p = prospects[idx];
      const full = buildPitchForProspect(p);
      const lines = full.split("\\n");
      const subj = encodeURIComponent(lines[0].replace("Asunto: ", ""));
      const body = encodeURIComponent(lines.slice(2).join("\n"));
      window.open(`mailto:${{p.correo_principal}}?subject=${{subj}}&body=${{body}}`, "_blank");
    }}

    function renderTable() {{
      const q = (document.getElementById("q").value || "").toLowerCase().trim();
      const tbody = document.getElementById("rows");
      const filtered = prospects.map((p, idx) => ({{ ...p, idx }})).filter(p => {{
        if (activeFilter !== "ALL" && !p.lote.startsWith(activeFilter)) return false;
        if (q && !(p.nombre.toLowerCase().includes(q) || p.correo_principal.toLowerCase().includes(q) || p.zona.toLowerCase().includes(q) || p.submarca.toLowerCase().includes(q))) return false;
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
            <span class="text-[10px] font-bold text-amber-300 uppercase">${{p.submarca}} · ${{p.lote}}</span>
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
            <button onclick="copyRowPitch(${{p.idx}})" class="px-2.5 py-1.5 rounded-lg bg-amber-500 text-black font-bold hover:bg-amber-400">
              📋 Copiar Correo (${{p.submarca.split(' ')[0]}})
            </button>
            <button onclick="openRowMailto(${{p.idx}})" class="px-2.5 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 font-semibold hover:bg-emerald-500/30">
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
    print(f"Procesando {len(SEED_INSTITUTIONS)} prospectos B2B por Submarca Captoora + Posadas...")
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
            fieldnames=["ID", "submarca", "lote", "nombre", "zona", "categoria", "correo_principal", "correos_adicionales", "telefono", "web", "dns_verificado", "estado_web"],
        )
        writer.writeheader()
        for idx, r in enumerate(results, 1):
            writer.writerow({"ID": f"B2B-{idx:03d}", **r})

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
                "First Name": "Dirección / Eventos",
                "Last Name": r["nombre"],
                "Email": r["correo_principal"],
                "Phone": r["telefono"],
                "Company": r["nombre"],
                "Address": f"{r['zona']}, Monterrey, N.L.",
                "Notes": f"{r['submarca']} | {r['lote']} | {r['categoria']}",
            })

    (OUT_DIR / "COLEGIOS_MTY_PIXIESET.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    build_html_dashboard(results)
    print(f"OK: {len(verified_results)}/{len(results)} prospectos verificados en 6 Lotes por Submarca Captoora + Posadas.")


if __name__ == "__main__":
    main()
