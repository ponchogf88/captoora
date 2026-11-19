#!/usr/bin/env python3
"""
CAPTOORA SPORTS // GOOGLE MAPS LEAD SCRAPER VIA APIFY
Script automatizado para extraer negocios deportivos, academias de baile, 
clubes de pádel, colegios privados y centros de alto rendimiento en Monterrey y San Pedro.
"""

import os
import sys
import json
import urllib.request
import urllib.parse

# 1. CATEGORÍAS Y KEYWORDS DE BÚSQUEDA EN NUEVO LEÓN
SEARCH_QUERIES = [
    # Pádel & Raqueta
    "club de padel San Pedro Garza Garcia",
    "canchas de padel Monterrey",
    "padel club Carretera Nacional Monterrey",
    "club de tenis San Pedro Garza Garcia",
    
    # Baile, Danza & Fitness Señoras
    "academia de baile San Pedro Garza Garcia",
    "estudio de danza Monterrey",
    "dance studio San Pedro Garza Garcia",
    "clases de ballet y jazz Monterrey",
    "dance fitness San Pedro Garza Garcia",
    "barre studio San Pedro Garza Garcia",
    
    # Porrismo & Gimnasia
    "cheerleading Monterrey",
    "academia de porristas Monterrey",
    "gimnasia artistica San Pedro Garza Garcia",
    "gimnasia ritmica Monterrey",
    
    # Artes Marciales & Combate
    "escuela de taekwondo San Pedro Garza Garcia",
    "academia de jiu jitsu brasileño Monterrey",
    "dojo karate San Pedro Garza Garcia",
    "gimnasio de boxeo San Pedro Garza Garcia",
    "academia artes marciales mixtas Monterrey",
    
    # Fitness de Rendimiento & CrossFit
    "crossfit San Pedro Garza Garcia",
    "gimnasio crossfit Monterrey",
    "hyrox training center Monterrey",
    "pilates reformer San Pedro Garza Garcia",
    
    # Fútbol Americano & Flag Football
    "club futbol americano infantil Monterrey",
    "liga flag football Monterrey",
    "tocho bandera San Pedro Garza Garcia",
    "club MFL San Pedro Garza Garcia",
    
    # Colegios Privados & Academias de Élite
    "colegio privado San Pedro Garza Garcia",
    "instituto bilingüe San Pedro Garza Garcia",
    "academia deportiva juvenil Monterrey"
]

def run_apify_google_maps_scraper(api_token, max_items_per_query=20):
    """
    Ejecuta el Actor de Google Maps en Apify y descarga los resultados limpios en JSON y CSV.
    Actor oficial de referencia: compass/crawler-google-places o apify/google-maps-scraper
    """
    actor_id = "compass~crawler-google-places"
    endpoint = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={api_token}"
    
    payload = {
        "searchStringsArray": SEARCH_QUERIES[:5], # Inicializa con las 5 prioritarias
        "locationQuery": "Monterrey, Nuevo León, México",
        "maxCrawledPlacesPerSearch": max_items_per_query,
        "language": "es",
        "includeWebResults": False,
        "scrapeDirectories": False,
        "extractPopularTimes": False,
        "exportPlaceUrls": True
    }
    
    print(f"[*] Iniciando scraping en Apify para {len(payload['searchStringsArray'])} categorías prioritarias...")
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            items = json.loads(response.read().decode('utf-8'))
            print(f"[✓] Se obtuvieron {len(items)} leads calificados de Google Maps.")
            
            # Limpieza y filtrado
            cleaned_leads = []
            for item in items:
                cleaned_leads.append({
                    "nombre": item.get("title"),
                    "categoria": item.get("categoryName"),
                    "direccion": item.get("address"),
                    "telefono": item.get("phone"),
                    "sitio_web": item.get("website"),
                    "rating": item.get("totalScore"),
                    "resenas": item.get("reviewsCount"),
                    "url_google_maps": item.get("url"),
                    "municipio": "San Pedro Garza García" if "San Pedro" in str(item.get("address")) else "Monterrey"
                })
            
            output_file = "/Users/imac/Documents/antigravity/epic-bohr/dashboard/data/apify_scraped_leads.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(cleaned_leads, f, indent=2, ensure_ascii=False)
            
            print(f"[✓] Leads guardados exitosamente en: {output_file}")
            return cleaned_leads
            
    except Exception as e:
        print(f"[!] Error al conectar con Apify: {e}")
        return None

if __name__ == "__main__":
    token = os.environ.get("APIFY_API_TOKEN")
    if not token and len(sys.argv) > 1:
        token = sys.argv[1]
        
    if not token:
        print("""
================================================================================
CAPTOORA // GUÍA RÁPIDA DE USO DE APIFY:
1. Ve a https://apify.com y crea tu cuenta gratuita (incluye $5 USD de crédito gratis al mes).
2. Ve a Settings -> Integrations -> API Tokens y copia tu Token.
3. Ejecuta el script pasando tu token:
   python3 scripts/apify_lead_scraper.py TU_TOKEN_DE_APIFY
================================================================================
        """)
    else:
        run_apify_google_maps_scraper(token)
