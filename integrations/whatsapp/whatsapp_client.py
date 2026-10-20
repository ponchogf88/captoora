#!/usr/bin/env python3
"""
Captoora Studio - WhatsApp Business Client & Reasoning Agent Router
Soporta Evolution API (Open Source Baileys REST) y Meta Cloud API oficial.
Diseñado para recepción, agendamiento de influencers y seguimiento de clientes.
"""

import os
import time
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

class WhatsAppEvolutionClient:
    """
    Cliente REST para Evolution API (v2).
    Microservicio local o remoto conectado por WebSockets a WhatsApp.
    """
    def __init__(self, base_url: str = "http://localhost:8080", api_key: str = "", instance_name: str = "captoora_studio"):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.getenv("EVOLUTION_API_KEY", "captoora_secret_api_key_2026")
        self.instance_name = instance_name

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }

    def send_presence(self, number: str, presence: str = "composing", delay_ms: int = 1500) -> bool:
        """Simula que el agente está escribiendo o grabando audio."""
        url = f"{self.base_url}/chat/sendPresence/{self.instance_name}"
        clean_num = "".join(filter(str.isdigit, number))
        payload = {
            "number": clean_num,
            "presence": presence,
            "delay": delay_ms
        }
        return self._post_json(url, payload)

    def send_text(self, number: str, message: str, delay_seconds: float = 2.0) -> Dict[str, Any]:
        """Envía un mensaje de texto con simulación de presencia humana para evitar detección/baneos."""
        clean_num = "".join(filter(str.isdigit, number))
        # 1. Simular presencia escribiendo
        self.send_presence(clean_num, "composing", int(delay_seconds * 1000))
        time.sleep(delay_seconds)

        url = f"{self.base_url}/message/sendText/{self.instance_name}"
        payload = {
            "number": clean_num,
            "options": {
                "delay": 1200,
                "presence": "composing",
                "linkPreview": True
            },
            "textMessage": {
                "text": message
            }
        }
        return self._post_json_response(url, payload)

    def send_image(self, number: str, image_url_or_base64: str, caption: str = "") -> Dict[str, Any]:
        """Envía una imagen fotográfica de portafolio o lookbook."""
        clean_num = "".join(filter(str.isdigit, number))
        url = f"{self.base_url}/message/sendMedia/{self.instance_name}"
        payload = {
            "number": clean_num,
            "options": {
                "delay": 1500,
                "presence": "composing"
            },
            "mediaMessage": {
                "mediatype": "image",
                "caption": caption,
                "media": image_url_or_base64
            }
        }
        return self._post_json_response(url, payload)

    def _post_json(self, url: str, payload: dict) -> bool:
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=self._headers(), method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status in (200, 201)
        except Exception as e:
            print(f"[WhatsAppEvolutionClient] Error en POST {url}: {e}")
            return False

    def _post_json_response(self, url: str, payload: dict) -> Dict[str, Any]:
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=self._headers(), method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except Exception as e:
            print(f"[WhatsAppEvolutionClient] Error en POST {url}: {e}")
            return {"error": str(e)}


class InfluencerCampaignAgent:
    """
    Agente de razonamiento para la gestión de las 25 influencers en WhatsApp.
    Maneja bienvenida, temática elegida (Pumpkin Patch, Halloween, Día de Muertos),
    acuerdo de colaboración (3 Reels + 5 Stories) y reserva de slots.
    """
    SLOTS_TOTALES = 25
    TEMATICAS = {
        "1": "🎃 Pumpkin Patch / Cozy Autumn (Editorial otoñal)",
        "2": "👻 Halloween Fashion & Disfraces (Iluminación creativa de estudio)",
        "3": "🌺 Día de Muertos / Tradición y Elegancia (Catrina moderna con cempasúchil)",
        "4": "🎬 Grabación & Behind The Scenes (UGC de alto impacto)"
    }

    def generate_welcome_message(self, name: str = "") -> str:
        saludo = f"¡Hola {name}!" if name else "¡Hola!"
        return f"""{saludo} 📸 Qué gusto saludarte. Te escribo de parte de Poncho y el equipo de **Captoora Studio**.

Estamos súper contentos con la respuesta para nuestra temporada de colaboraciones. Abrimos únicamente **25 espacios exclusivos** de intercambio creativo para creadoras de contenido de alto perfil.

¿Para cuál de nuestras producciones de temporada te gustaría apartar tu sesión?

1️⃣ 🎃 **Pumpkin Patch / Cozy Autumn** (Set de calabazas, tonos cálidos y texturas de otoño).
2️⃣ 👻 **Halloween Fashion** (Retrato editorial con vestuario y luces creativas de estudio).
3️⃣ 🌺 **Día de Muertos** (Catrina de alta costura, flores de cempasúchil y tradición).
4️⃣ 🎬 **Grabación & Video UGC** (Contenido dinámico para Reels y TikTok).

Respóndeme con el número de tu temática favorita y te paso los horarios disponibles en nuestro estudio de Amapola Eventos. ✨"""

    def generate_agreement_summary(self, influencer_name: str, handle: str, slot_time: str, theme: str) -> str:
        return f"""📋 **RESUMEN DE COLABORACIÓN CREATIVA — CAPTOORA STUDIO**

👤 **Creadora:** {influencer_name} (@{handle.lstrip('@')})
📅 **Cita confirmada:** {slot_time}
🎨 **Temática:** {theme}
📍 **Ubicación:** Captoora Studio (Amapola Eventos, Monterrey)

🎁 **Lo que te entrega Captoora:**
- Sesión guiada de 45 minutos en set profesional.
- Galería digital interactiva para selección el mismo día.
- **5 Fotografías en Alta Resolución (Master Edit)** con piel de seda y color grading profesional.
- Acceso a clips crudos 4K para tus Reels / TikTok.

🤝 **Entregables por intercambio de la creadora:**
- 1 Collab Post en Instagram (Fotografía principal en carrusel).
- 1 Reel / TikTok de Behind The Scenes etiquetando a @captoora.
- 3 a 5 Stories durante y después de la sesión con mención y enlace.

Por favor confírmame con un *"¡Acepto y confirmada!"* para bloquear tu hora en la agenda del fotógrafo. 📸"""

if __name__ == "__main__":
    agent = InfluencerCampaignAgent()
    print("--- DEMO WHATSAPP INFLUENCER AGENT ---")
    print(agent.generate_welcome_message("Valeria"))
    print("\n" + "="*50 + "\n")
    print(agent.generate_agreement_summary("Valeria Garza", "@valeriagarza", "Sábado 24 de Octubre - 3:00 PM", agent.TEMATICAS["1"]))
