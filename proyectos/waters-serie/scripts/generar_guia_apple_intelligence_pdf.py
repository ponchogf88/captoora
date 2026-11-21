#!/usr/bin/env python3
"""
Genera el Lead Magnet oficial del Díptico Apple (EP09 / MAD-09):
  proyectos/waters-serie/lead_magnets/CHECKLIST_BLINDAJE_APPLE_INTELLIGENCE.pdf
"""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ROOT = Path("/Users/user/captoora")
OUT_PDF = ROOT / "proyectos/waters-serie/lead_magnets/CHECKLIST_BLINDAJE_APPLE_INTELLIGENCE.pdf"

OBSIDIAN = colors.HexColor("#080C17")
SLATE_CARD = colors.HexColor("#111827")
CYAN = colors.HexColor("#00F5D4")
GOLD = colors.HexColor("#DFB15B")
RED_ALERT = colors.HexColor("#EF4444")
INK_DARK = colors.HexColor("#0F172A")
INK_MUTED = colors.HexColor("#64748B")
WHITE = colors.white
LIGHT_BG = colors.HexColor("#F8FAFC")
BORDER_COLOR = colors.HexColor("#CBD5E1")

def build_pdf():
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT_PDF), pagesize=letter)
    w, h = letter

    # Fondo claro profesional
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, w, h, fill=True, stroke=False)

    # Header Obsidian / Neón
    c.setFillColor(OBSIDIAN)
    c.rect(0, h - 110, w, 110, fill=True, stroke=False)

    # Acento Neón Cyan
    c.setFillColor(CYAN)
    c.rect(0, h - 114, w, 4, fill=True, stroke=False)

    # Textos Header
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, h - 35, "SERIE ¡WATERS! · CAPTOORA.STUDIO · GUÍA TÉCNICA OFICIAL (DÍPTICO EP09)")

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(40, h - 65, "Checklist de Blindaje Familiar: Apple Intelligence")

    c.setFont("Helvetica", 9.5)
    c.drawString(40, h - 85, "Los 4 Botones de Protección + Lo que Siri AI Confesó en Privado sobre Ciberseguridad")

    # Caja Contexto: Las 4 Confesiones Técnicas de Siri
    y = h - 140
    c.setFillColor(WHITE)
    c.setStrokeColor(BORDER_COLOR)
    c.roundRect(40, y - 58, w - 80, 78, 8, fill=True, stroke=True)

    c.setFillColor(RED_ALERT)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(55, y + 5, "🔍 4 COSAS QUE LA PROPIA SIRI AI CONFESÓ SOBRE SEGURIDAD:")

    c.setFillColor(INK_DARK)
    c.setFont("Helvetica", 8.5)
    c.drawString(55, y - 10, "1. Ataque Serpent (Mitigado): Investigadores probaron que malware en Mac podía extraer tokens para usar tu cuota.")
    c.drawString(55, y - 22, "2. Prompt Injection: Órdenes invisibles en imágenes o correos que engañan a la IA para cruzar tus notas personales.")
    c.drawString(55, y - 34, "3. Bug Bounty de $1,000,000 USD: Recompensa preventiva que Apple ofrece a investigadores éticos en Private Cloud Compute.")
    c.drawString(55, y - 46, "4. Multiplicadores de Cuota en iCloud+: 200 GB = 2x | 2 TB = 5x | 6 TB = 10x | 12 TB = 20x más capacidad diaria.")

    # Los 4 Botones de Blindaje Familiar (+ 1 Extra)
    switches = [
        ("1. Verificación de Seguridad (Safety Check Familiar)",
         "Ruta: Ajustes > Privacidad y Seguridad > Verificación de Seguridad",
         "Permite revisar y revocar de golpe cualquier acceso a tu ubicación, fotos o datos que compartas con familiares o apps de terceros. Vital para auditar el ecosistema familiar en segundos."),

        ("2. Apagar 'Mejorar Siri y Dictado' (Cero retención de 2 años)",
         "Ruta: Ajustes > Privacidad y Seguridad > Análisis y Mejoras > Mejorar Siri [OFF]",
         "Si está encendido, Apple almacena grabaciones de tu voz y textos en servidores por hasta 24 meses para 'entrenar'. Apagarlo garantiza que tus conversaciones nocturnas no queden guardadas."),

        ("3. Activar Protección de Datos Avanzada (Cifrado E2E Total)",
         "Ruta: Ajustes > [Tu Nombre] > iCloud > Protección de Datos Avanzada [ACTIVADA]",
         "Cifra de extremo a extremo tus notas, fotos y respaldos en iCloud. Ni Apple con orden judicial puede acceder a tus claves. Exige configurar un contacto de recuperación o clave de 28 dígitos."),

        ("4. Regla de Oro Familiar: Jamás resumir correos o adjuntos desconocidos",
         "Protocolo Familiar de Prevención contra Prompt Injection",
         "Enseña a tu familia a no pedirle a Siri que 'resuma' correos, capturas o facturas sospechosas. Una orden en texto invisible (blanco sobre blanco) puede forzar a la IA a filtrar información privada."),

        ("5. Llaves de Seguridad Físicas FIDO2 / YubiKey (Blindaje Antirrobo)",
         "Ruta: Ajustes > [Tu Nombre] > Inicio de sesión y seguridad > Llaves de seguridad",
         "Elimina los códigos SMS (vulnerables a clonación de chip / SIM Swapping). Requiere una llave física USB/NFC para autorizar cualquier cambio de contraseña o inicio de sesión en tu Apple ID.")
    ]

    y_cur = y - 82
    for title, path_str, desc in switches:
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER_COLOR)
        c.roundRect(40, y_cur - 46, w - 80, 56, 6, fill=True, stroke=True)

        c.setFillColor(INK_DARK)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(52, y_cur - 2, title)

        c.setFillColor(colors.HexColor("#0F766E"))
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(52, y_cur - 15, path_str)

        c.setFillColor(INK_MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(52, y_cur - 29, desc[:120])
        if len(desc) > 120:
            c.drawString(52, y_cur - 39, desc[120:])

        y_cur -= 64

    # Footer
    c.setFillColor(OBSIDIAN)
    c.rect(0, 0, w, 40, fill=True, stroke=False)

    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, 16, "¡WATERS! · Ciberseguridad & Gobernanza de IA · captoora.studio")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 8)
    c.drawRightString(w - 40, 16, "Comparte este checklist con tu familia · Palabra clave: APPLE")

    c.save()
    print(f"✅ PDF corregido generado exitosamente: {OUT_PDF}")

if __name__ == "__main__":
    build_pdf()
