#!/usr/bin/env python3
"""
Genera el Lead Magnet oficial del Episodio DIA-APPLE:
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
BORDER_COLOR = colors.HexColor("#E2E8F0")

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
    c.drawString(40, h - 35, "SERIE ¡WATERS! · CAPTOORA.STUDIO · GUÍA TÉCNICA OFICIAL")

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, h - 65, "Checklist de Blindaje: Apple Intelligence & Siri")

    c.setFont("Helvetica", 10)
    c.drawString(40, h - 85, "5 Switches de Seguridad y Privacidad tras las Confesiones Reales de Siri (iOS 18+ / macOS Sequoia)")

    # Caja Contexto: Lo que Siri confesó
    y = h - 145
    c.setFillColor(WHITE)
    c.setStrokeColor(BORDER_COLOR)
    c.roundRect(40, y - 50, w - 80, 70, 8, fill=True, stroke=True)

    c.setFillColor(RED_ALERT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(55, y + 5, "⚠️ LO QUE SIRI CONFIRMÓ EN LA MADRUGADA:")

    c.setFillColor(INK_DARK)
    c.setFont("Helvetica", 9)
    c.drawString(55, y - 12, "• Ataque Serpent: Robo de tokens de Apple Intelligence en Mac para consumir cuota ajena.")
    c.drawString(55, y - 26, "• Prompt Injection: Texto invisible en correos e imágenes que engaña a Siri para filtrar PII.")
    c.drawString(55, y - 40, "• Cuotas iCloud+: Planes de 2TB y 6TB dan hasta 20x más IA diaria, pero aumentan la superficie de ataque.")

    # Los 5 Switches
    switches = [
        ("1. Activar Protección de Datos Avanzada (Cifrado E2E Total)",
         "Ruta: Ajustes > [Tu Nombre] > iCloud > Protección de Datos Avanzada",
         "Por defecto, Apple conserva claves de recuperación en la nube. Al activar este switch, absolutamente todo tu iCloud (fotos, notas, backups) se cifra de extremo a extremo y ni siquiera Apple con orden judicial puede descifrarlo."),

        ("2. Apagar 'Mejorar Siri y Dictado' (Cortar retención de 2 años)",
         "Ruta: Ajustes > Privacidad y Seguridad > Análisis y Mejoras > Mejorar Siri [OFF]",
         "Si está encendido, Apple guarda grabaciones de tu voz y textos de interacciones hasta por 24 meses en servidores para 'entrenar'. Apágalo para garantizar cero retención externa de tu voz."),

        ("3. Borrar el Historial de Interacciones de Siri",
         "Ruta: Ajustes > Siri (o Siri y Buscar) > Historial de Siri y Dictado > Eliminar historial",
         "Borra de inmediato las muestras asociadas a identificadores aleatorios en la nube de Apple. Realiza esto una vez al mes para evitar que se acumule contexto personal sensible."),

        ("4. Reemplazar Códigos SMS con Llaves Físicas (FIDO2 / YubiKey)",
         "Ruta: Ajustes > [Tu Nombre] > Inicio de sesión y seguridad > Llaves de seguridad",
         "El SIM Swapping es el vector #1 de hackeo a Apple IDs. Una llave física USB/NFC anula por completo el robo de cuenta aunque el atacante clone tu chip telefónico."),

        ("5. Auditar Acceso de Siri a Aplicaciones y Búsqueda en Pantalla",
         "Ruta: Ajustes > Siri > [Seleccionar Apps Críticas como Banca, SAT, Bitwarden] > Apagar 'Aprender de esta app'",
         "Evita que Apple Intelligence indexe de forma proactiva pantallas con estados de cuenta, contraseñas o tokens bancarios cuando le pides sugerencias contextuales.")
    ]

    y_cur = y - 80
    for title, path_str, desc in switches:
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER_COLOR)
        c.roundRect(40, y_cur - 46, w - 80, 56, 6, fill=True, stroke=True)

        c.setFillColor(INK_DARK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(52, y_cur - 2, title)

        c.setFillColor(colors.HexColor("#0F766E"))
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(52, y_cur - 16, path_str)

        c.setFillColor(INK_MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(52, y_cur - 30, desc[:120])
        if len(desc) > 120:
            c.drawString(52, y_cur - 40, desc[120:])

        y_cur -= 66

    # Footer
    c.setFillColor(OBSIDIAN)
    c.rect(0, 0, w, 40, fill=True, stroke=False)

    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, 16, "¡WATERS! · Ciberseguridad & AI Governance · captoora.studio")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 8)
    c.drawRightString(w - 40, 16, "Comparte este checklist con quien use iPhone o Mac · Código: APPLE")

    c.save()
    print(f"✅ PDF generado exitosamente: {OUT_PDF}")

if __name__ == "__main__":
    build_pdf()
