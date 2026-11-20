#!/usr/bin/env python3
"""
Genera el Lead Magnet oficial del Episodio 06:
  proyectos/waters-serie/lead_magnets/GUIA_BLINDA_HACKEOS_Y_VOZ_CAPTOORA.pdf
"""
from pathlib import Path
from typing import List, Tuple

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
OUT_PDF = ROOT / "proyectos/waters-serie/lead_magnets/GUIA_BLINDA_HACKEOS_Y_VOZ_CAPTOORA.pdf"

# Captoora Dark + Cyan + Gold + Alert Red Palette
OBSIDIAN = colors.HexColor("#080C17")
SLATE_CARD = colors.HexColor("#111827")
SOFT_BG = colors.HexColor("#F8FAFC")
BORDER_LIGHT = colors.HexColor("#CBD5E1")
CYAN = colors.HexColor("#00F5D4")
TEAL_DARK = colors.HexColor("#0F766E")
GOLD = colors.HexColor("#DFB15B")
RED_ALERT = colors.HexColor("#DC2626")
INK_DARK = colors.HexColor("#0F172A")
INK_MUTED = colors.HexColor("#475569")
WHITE = colors.white


def wrap_text(c: canvas.Canvas, text: str, font: str, size: float, max_w: float) -> List[str]:
    c.setFont(font, size)
    words = text.split()
    lines: List[str] = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if c.stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y_top: float,
    font: str,
    size: float,
    max_w: float,
    leading: float,
    color=INK_DARK,
) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    lines = wrap_text(c, text, font, size, max_w)
    cur_y = y_top
    for line in lines:
        c.drawString(x, cur_y, line)
        cur_y -= leading
    return cur_y


def build_pdf(out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = letter  # 612 x 792
    c = canvas.Canvas(str(out_path), pagesize=letter)
    c.setTitle("GUIA BLINDA - Hackeos Masivos y Clonacion de Voz IA | Captoora Studio")

    # =========================================================================
    # PAGE 1: CONTEXTO REAL + 4 ESCUDOS INMEDIATOS
    # =========================================================================
    c.setFillColor(SOFT_BG)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    # Top Dark Hero Header
    header_h = 132
    c.setFillColor(OBSIDIAN)
    c.rect(0, h - header_h, w, header_h, stroke=0, fill=1)
    c.setFillColor(CYAN)
    c.rect(0, h - header_h, w, 4, stroke=0, fill=1)

    # Top Pill Tag
    c.setFillColor(colors.HexColor("#06292B"))
    c.roundRect(40, h - 40, 210, 20, 10, stroke=0, fill=1)
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(52, h - 33, "CAPTOORA STUDIO  ·  PROTOCOLO WATERS")

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(w - 40, h - 33, "ACTUALIZADO NOVIEMBRE 2026")

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, h - 72, "GUÍA BLINDA: Hackeos y Clonación de Voz IA")

    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.setFont("Helvetica", 10.5)
    c.drawString(
        40,
        h - 94,
        "Qué pasó con JPMorgan, Visa, IMSS, SAT e INE — y cómo proteger tu dinero y tu familia",
    )
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(
        40,
        h - 114,
        "Regla de oro: hoy la IA avanza más rápido que la ciberseguridad. Ni tu propia voz es prueba segura.",
    )

    # Section 1 Title
    c.setFillColor(INK_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, h - 160, "1. Lo que ya ocurrió (por qué recibes llamadas que saben todo de ti)")

    # 3 Evidence Cards horizontally
    cards_y = h - 292
    card_w = 168
    card_h = 118
    gap = 14
    evidence: List[Tuple[str, str, str, object]] = [
        (
            "JPMORGAN · VISA · MASTERCARD",
            "Proveedores externos (Nov 2026)",
            "El grupo n0n filtró datos de proveedores de lealtad y marketing (~16 mil registros Reserve). No cayeron tarjetas, pero expusieron nombres, correos y teléfonos.",
            RED_ALERT,
        ),
        (
            "IMSS · SAT · INE (MÉXICO)",
            "+10 hackeos y bases a la venta",
            "En foros clandestinos han circulado 20M de registros de pensionados IMSS, 150 GB atribuibles a SAT/INE y fugas de CURP, NSS, domicilios e historiales.",
            TEAL_DARK,
        ),
        (
            "VOZ CLONADA EN 3–10 SEG",
            "Crisis de biometría vocal",
            "Con un audio corto en llamada o red social, la IA (tipo ElevenLabs) clona tu voz o la de tu familia. Si un banco aún valida solo por voz, hay riesgo real.",
            GOLD,
        ),
    ]

    for idx, (tag, sub, body, bar_col) in enumerate(evidence):
        cx = 40 + idx * (card_w + gap)
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER_LIGHT)
        c.setLineWidth(1)
        c.roundRect(cx, cards_y, card_w, card_h, 8, stroke=1, fill=1)

        c.setFillColor(bar_col)
        c.roundRect(cx, cards_y + card_h - 6, card_w, 6, 3, stroke=0, fill=1)

        c.setFillColor(INK_DARK)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(cx + 10, cards_y + card_h - 22, tag)

        c.setFillColor(TEAL_DARK if bar_col != RED_ALERT else RED_ALERT)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(cx + 10, cards_y + card_h - 35, sub)

        draw_wrapped(
            c,
            body,
            cx + 10,
            cards_y + card_h - 51,
            "Helvetica",
            8,
            card_w - 20,
            10.5,
            INK_MUTED,
        )

    # Section 2: 4 Shields
    sec2_top = cards_y - 24
    c.setFillColor(INK_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, sec2_top, "2. Los 4 Escudos Inmediatos para blindar tu dinero hoy")

    shields = [
        (
            "1",
            "DESACTIVA LA AUTENTICACIÓN SOLO POR VOZ EN TU BANCO",
            "Si tu banco usa biometría telefónica pasiva ('tu voz es tu contraseña'), solicita cambiar a validación estricta con token digital en app oficial o NIP dinámico. Nunca dependas de una sola huella vocal.",
            TEAL_DARK,
        ),
        (
            "2",
            "REGLA DE LOS 10 SEGUNDOS: CUELGA ANTE URGENCIAS",
            "Los estafadores buscan mantenerte hablando para validar tu voz o sacarte códigos OTP bajo pánico ('cargo por $18,000'). Cuelga de inmediato y llama tú desde el número al reverso de tu tarjeta o entra a tu app.",
            RED_ALERT,
        ),
        (
            "3",
            "ALERTAS DESDE $1 MXN + TARJETA DIGITAL APAGADA",
            "Configura notificaciones push y correo desde el monto mínimo ($1). Mantén apagadas tu tarjeta digital y tus tarjetas físicas en la app hasta el segundo exacto en que vas a pagar.",
            colors.HexColor("#1D4ED8"),
        ),
        (
            "4",
            "PROTOCOLO TERMINATOR: PREGUNTA TRAMPA Y PALABRA CLAVE",
            "Como en Terminator 2: lanza una pregunta trampa (un dato que solo tu familia sabe, un apodo falso o palabra clave secreta). Si la voz suena igual pero duda o falla la clave: es clon de IA — cuelga en seco y marca directo.",
            GOLD,
        ),
    ]

    sh_y = sec2_top - 18
    sh_h = 84
    sh_gap = 11
    for num, title, desc, badge_col in shields:
        cy = sh_y - sh_h
        c.setFillColor(SLATE_CARD if num == "4" else WHITE)
        c.setStrokeColor(GOLD if num == "4" else BORDER_LIGHT)
        c.setLineWidth(1.5 if num == "4" else 1)
        c.roundRect(40, cy, w - 80, sh_h, 9, stroke=1, fill=1)

        # Number badge
        c.setFillColor(badge_col)
        c.circle(64, cy + sh_h - 24, 13, stroke=0, fill=1)
        c.setFillColor(INK_DARK if num == "4" else WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(64, cy + sh_h - 28, num)

        c.setFillColor(GOLD if num == "4" else INK_DARK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(86, cy + sh_h - 27, title)

        draw_wrapped(
            c,
            desc,
            86,
            cy + sh_h - 44,
            "Helvetica",
            8.8,
            w - 140,
            11.5,
            colors.HexColor("#E2E8F0") if num == "4" else INK_MUTED,
        )
        sh_y = cy - sh_gap

    # Footer Page 1
    c.setFillColor(INK_MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(40, 28, "captoora.studio  ·  Serie ¡WATERS! Ciberseguridad Práctica  ·  WhatsApp +52 81 4005 0088")
    c.drawRightString(w - 40, 28, "Página 1 de 2")

    c.showPage()

    # =========================================================================
    # PAGE 2: CHECKLIST DE 10 PUNTOS + PROTOCOLO SI YA REVELASTE DATOS
    # =========================================================================
    c.setFillColor(SOFT_BG)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    c.setFillColor(OBSIDIAN)
    c.rect(0, h - 76, w, 76, stroke=0, fill=1)
    c.setFillColor(CYAN)
    c.rect(0, h - 76, w, 3.5, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, h - 42, "CHECKLIST DE 10 PUNTOS · BLINDAJE INMEDIATO")
    c.setFillColor(CYAN)
    c.setFont("Helvetica", 9.5)
    c.drawString(40, h - 60, "Marca cada casilla hoy mismo (tiempo estimado: 15 minutos)")

    checklist_items = [
        ("BANCA Y DINERO", "1. Activar alertas instantáneas por cualquier cargo desde $1 MXN en todas tus apps bancarias."),
        ("BANCA Y DINERO", "2. Apagar tarjeta digital / CVV dinámico y tarjetas físicas no utilizadas cuando no estés pagando."),
        ("BANCA Y DINERO", "3. Solicitar baja de autenticación solo por voz pasiva en tu banco; exigir token en app + NIP."),
        ("BANCA Y DINERO", "4. Poner límites máximos bajos a transferencias SPEI y retiros sin tarjeta desde tu app."),
        ("VOZ E IA", "5. Definir en persona una Palabra Clave Familiar para validar emergencias por teléfono o WhatsApp."),
        ("VOZ E IA", "6. Grabar buzón de voz neutro (sin decir tu nombre completo ni confirmar identidad en saludos largos)."),
        ("VOZ E IA", "7. Nunca responder llamadas desconocidas con 'Sí, diga' ni regalar >5 seg hablando antes de saber quién llama."),
        ("CUENTAS Y DATOS", "8. Cambiar contraseñas repetidas usando un gestor (Bitwarden / 1Password / Apple Passwords); nunca la misma clave."),
        ("CUENTAS Y DATOS", "9. Activar verificación en dos pasos (2FA) con app autenticadora o Passkey — evita SMS en cuentas críticas."),
        ("CUENTAS Y DATOS", "10. Activar el PIN de verificación en dos pasos en WhatsApp y correo (Ajustes -> Cuenta -> Verificación en dos pasos)."),
    ]

    cur_y = h - 102
    row_h = 44
    last_cat = ""
    for cat, text in checklist_items:
        if cat != last_cat:
            c.setFillColor(TEAL_DARK)
            c.setFont("Helvetica-Bold", 8.5)
            c.drawString(40, cur_y, cat)
            cur_y -= 14
            last_cat = cat

        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER_LIGHT)
        c.setLineWidth(0.9)
        c.roundRect(40, cur_y - row_h + 10, w - 80, row_h - 6, 6, stroke=1, fill=1)

        # Checkbox square
        c.setStrokeColor(INK_DARK)
        c.setLineWidth(1.2)
        c.rect(52, cur_y - 20, 12, 12, stroke=1, fill=0)

        draw_wrapped(
            c,
            text,
            74,
            cur_y - 12,
            "Helvetica",
            9,
            w - 130,
            11.5,
            INK_DARK,
        )
        cur_y -= row_h

    # Emergency Action Box at bottom
    box_h = 112
    box_y = 66
    c.setFillColor(OBSIDIAN)
    c.roundRect(40, box_y, w - 80, box_h, 10, stroke=0, fill=1)
    c.setFillColor(RED_ALERT)
    c.roundRect(40, box_y + box_h - 5, w - 80, 5, 2, stroke=0, fill=1)

    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, box_y + box_h - 24, "¿Qué hacer si ya contestaste una llamada sospechosa o diste un código?")

    steps_emerg = [
        "1. CONGELA DE INMEDIATO tus tarjetas y cuentas desde la app bancaria oficial (o llama al número impreso en tu plástico).",
        "2. CIERRA SESIONES Y CAMBIA CLAVES de correo principal y banca + activa 2FA por aplicación autenticadora.",
        "3. REPORTA EL FOLIO ante tu banco / CONDUSEF y avisa a tus contactos cercanos si intentan suplantar tu voz o tu WhatsApp.",
    ]
    ey = box_y + box_h - 44
    for s in steps_emerg:
        ey = draw_wrapped(c, s, 56, ey, "Helvetica", 8.8, w - 112, 11.5, WHITE) - 3

    # Footer Page 2
    c.setFillColor(INK_MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(40, 28, "captoora.studio  ·  Comparte este PDF con tu familia para prevenir fraudes con IA  ·  @captoora.studio")
    c.drawRightString(w - 40, 28, "Página 2 de 2")

    c.save()
    print(f"✅ PDF generado: {out_path} ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    build_pdf(OUT_PDF)
