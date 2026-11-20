#!/usr/bin/env python3
"""
Genera los 2 Lead Magnets oficiales para EP07 y EP08:
  1. proyectos/waters-serie/lead_magnets/GUIA_BOLSA_PREIPO_CAPTOORA.pdf (CTA: BOLSA)
  2. proyectos/waters-serie/lead_magnets/GUIA_CONTADOR_IA_SAT_CAPTOORA.pdf (CTA: CONTADOR)
"""
from pathlib import Path
from typing import List, Tuple

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
OUT_DIR = ROOT / "proyectos/waters-serie/lead_magnets"

OBSIDIAN = colors.HexColor("#080C17")
SLATE_CARD = colors.HexColor("#111827")
SOFT_BG = colors.HexColor("#F8FAFC")
BORDER_LIGHT = colors.HexColor("#CBD5E1")
EMERALD = colors.HexColor("#10B981")
CYAN = colors.HexColor("#00F5D4")
TEAL_DARK = colors.HexColor("#0F766E")
GOLD = colors.HexColor("#DFB15B")
RED_ALERT = colors.HexColor("#DC2626")
BLUE_ACC = colors.HexColor("#1D4ED8")
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


def build_two_page_guide(
    out_path: Path,
    doc_title: str,
    pill_tag: str,
    date_tag: str,
    hero_h1: str,
    hero_sub: str,
    hero_rule: str,
    accent_bar: object,
    sec1_title: str,
    evidence: List[Tuple[str, str, str, object]],
    sec2_title: str,
    shields: List[Tuple[str, str, str, object, bool]],
    p2_title: str,
    p2_sub: str,
    checklist_items: List[Tuple[str, str]],
    emerg_title: str,
    emerg_steps: List[str],
    footer_left: str,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = letter
    c = canvas.Canvas(str(out_path), pagesize=letter)
    c.setTitle(doc_title)

    # =========================================================================
    # PAGE 1
    # =========================================================================
    c.setFillColor(SOFT_BG)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    header_h = 132
    c.setFillColor(OBSIDIAN)
    c.rect(0, h - header_h, w, header_h, stroke=0, fill=1)
    c.setFillColor(accent_bar)
    c.rect(0, h - header_h, w, 4, stroke=0, fill=1)

    c.setFillColor(colors.HexColor("#06292B"))
    c.roundRect(40, h - 40, 220, 20, 10, stroke=0, fill=1)
    c.setFillColor(accent_bar)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(52, h - 33, pill_tag)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(w - 40, h - 33, date_tag)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 19.5)
    c.drawString(40, h - 72, hero_h1)

    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.setFont("Helvetica", 10.2)
    c.drawString(40, h - 94, hero_sub)

    c.setFillColor(accent_bar)
    c.setFont("Helvetica-Bold", 9.3)
    c.drawString(40, h - 114, hero_rule)

    c.setFillColor(INK_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, h - 160, sec1_title)

    cards_y = h - 294
    card_w = 168
    card_h = 120
    gap = 14
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

        c.setFillColor(RED_ALERT if bar_col == RED_ALERT else TEAL_DARK)
        c.setFont("Helvetica-Bold", 8.4)
        c.drawString(cx + 10, cards_y + card_h - 35, sub)

        draw_wrapped(
            c,
            body,
            cx + 10,
            cards_y + card_h - 50,
            "Helvetica",
            7.9,
            card_w - 20,
            10.3,
            INK_MUTED,
        )

    sec2_top = cards_y - 24
    c.setFillColor(INK_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, sec2_top, sec2_title)

    sh_y = sec2_top - 16
    sh_h = 84
    sh_gap = 11
    for num, title, desc, badge_col, dark_card in shields:
        cy = sh_y - sh_h
        c.setFillColor(SLATE_CARD if dark_card else WHITE)
        c.setStrokeColor(GOLD if dark_card else BORDER_LIGHT)
        c.setLineWidth(1.5 if dark_card else 1)
        c.roundRect(40, cy, w - 80, sh_h, 9, stroke=1, fill=1)

        c.setFillColor(badge_col)
        c.circle(64, cy + sh_h - 24, 13, stroke=0, fill=1)
        c.setFillColor(INK_DARK if dark_card else WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(64, cy + sh_h - 28, num)

        c.setFillColor(GOLD if dark_card else INK_DARK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(86, cy + sh_h - 27, title)

        draw_wrapped(
            c,
            desc,
            86,
            cy + sh_h - 44,
            "Helvetica",
            8.7,
            w - 140,
            11.4,
            colors.HexColor("#E2E8F0") if dark_card else INK_MUTED,
        )
        sh_y = cy - sh_gap

    c.setFillColor(INK_MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(40, 28, footer_left)
    c.drawRightString(w - 40, 28, "Página 1 de 2")

    c.showPage()

    # =========================================================================
    # PAGE 2
    # =========================================================================
    c.setFillColor(SOFT_BG)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    c.setFillColor(OBSIDIAN)
    c.rect(0, h - 76, w, 76, stroke=0, fill=1)
    c.setFillColor(accent_bar)
    c.rect(0, h - 76, w, 3.5, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, h - 42, p2_title)
    c.setFillColor(accent_bar)
    c.setFont("Helvetica", 9.5)
    c.drawString(40, h - 60, p2_sub)

    cur_y = h - 104
    row_h = 50
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
        c.roundRect(40, cur_y - row_h + 12, w - 80, row_h - 6, 6, stroke=1, fill=1)

        c.setStrokeColor(INK_DARK)
        c.setLineWidth(1.2)
        c.rect(52, cur_y - 20, 12, 12, stroke=1, fill=0)

        draw_wrapped(c, text, 74, cur_y - 11, "Helvetica", 9, w - 130, 11.8, INK_DARK)
        cur_y -= row_h

    box_h = 114
    box_y = 64
    c.setFillColor(OBSIDIAN)
    c.roundRect(40, box_y, w - 80, box_h, 10, stroke=0, fill=1)
    c.setFillColor(RED_ALERT)
    c.roundRect(40, box_y + box_h - 5, w - 80, 5, 2, stroke=0, fill=1)

    c.setFillColor(accent_bar)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, box_y + box_h - 24, emerg_title)

    ey = box_y + box_h - 44
    for s in emerg_steps:
        ey = draw_wrapped(c, s, 56, ey, "Helvetica", 8.8, w - 112, 11.5, WHITE) - 3

    c.setFillColor(INK_MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(40, 28, "captoora.studio  ·  Serie ¡WATERS! Ciberseguridad Práctica  ·  @captoora.studio")
    c.drawRightString(w - 40, 28, "Página 2 de 2")

    c.save()
    print(f"✅ PDF generado: {out_path} ({out_path.stat().st_size} bytes)")


def main() -> int:
    # 1) GUIA_BOLSA_PREIPO_CAPTOORA.pdf (EP07)
    build_two_page_guide(
        out_path=OUT_DIR / "GUIA_BOLSA_PREIPO_CAPTOORA.pdf",
        doc_title="GUIA BOLSA - Anthropic IPO y Estafas Pre-IPO | Captoora Studio",
        pill_tag="CAPTOORA STUDIO  ·  GUÍA BOLSA",
        date_tag="IPO NASDAQ: ANT · NOV 2026",
        hero_h1="GUÍA BOLSA: Anthropic IPO & Estafas Pre-IPO",
        hero_sub="Cómo invirtió Ashton Kutcher de verdad — y las 3 trampas FOMO que vacían cuentas hoy",
        hero_rule="Regla de oro: si te venden 'acciones antes de la bolsa' por WhatsApp o DM, eres la víctima.",
        accent_bar=EMERALD,
        sec1_title="1. Hechos del debut récord (y por qué disparan estafas globales)",
        evidence=[
            (
                "NASDAQ: ANT (19 NOV 2026)",
                "IPO récord de $81.3B USD",
                "Anthropic salió a $83 y abrió en $111.50 USD. Cerca de 5,100 empleados (~96%) alcanzaron >$1M en papel (sujeto a lock-up).",
                EMERALD,
            ),
            (
                "ASHTON KUTCHER (VC)",
                "~$435M ➔ $7B–$10B USD",
                "Sound Ventures (con Guy Oseary) entró desde 2023 en rondas privadas institucionales años antes de Nasdaq. Nunca compró por DM.",
                GOLD,
            ),
            (
                "3 ESTAFAS ACTIVAS HOY",
                "Pre-IPO · Deepfake · KYC",
                "Anuncios falsos prometen acceso 'como Ashton' o tokens $ANT/$CLAUDE, roban dinero y capturan fotos de tu INE y selfie.",
                RED_ALERT,
            ),
        ],
        sec2_title="2. Los 4 Candados antes de invertir un solo peso en Bolsa o IA",
        shields=[
            (
                "1",
                "NUNCA COMPRES 'ACCIONES PRE-IPO' POR DM, TELEGRAM O WHATSAPP",
                "Las rondas privadas (como Sound Ventures) solo admiten fondos e inversionistas institucionales acreditados con contratos SEC. Jamás se venden por link en comentarios ni transferencias SPEI a personas.",
                RED_ALERT,
                False,
            ),
            (
                "2",
                "VERIFICA EL REGISTRO REGULATORIO ANTES DE SUBIR TU INE (KYC)",
                "Los brokers clonados usan deepfakes de celebridades para robarte dos veces: primero tu depósito inicial y luego la foto frontal de tu INE + selfie para abrir créditos a tu nombre.",
                BLUE_ACC,
                False,
            ),
            (
                "3",
                "DESCONFÍA DE TOKENS '$CLAUDE' O 'BONOS DE LANZAMIENTO' CRIPTO",
                "Anthropic cotiza en Nasdaq bajo el ticker ANT en bolsa tradicional; no existe ningún token oficial ni airdrop de lanzamiento para multiplicar tu depósito x10 en 24 horas.",
                TEAL_DARK,
                False,
            ),
            (
                "4",
                "OPERA SOLO EN CASAS DE BOLSA REGULADAS (CNBV / SEC / FINRA)",
                "Si quieres invertir legalmente en acciones tech como ANT, hazlo directo desde brokers regulados en México o EE. UU. (ej. GBM, Bursanet, Interactive Brokers, Schwab) bajados de la tienda oficial.",
                GOLD,
                True,
            ),
        ],
        p2_title="CHECKLIST DE 8 PUNTOS · INVIERTE SIN CAER EN ESTAFAS",
        p2_sub="Revisa estos 8 puntos antes de mandar tu dinero o tus documentos a cualquier app",
        checklist_items=[
            ("REGULACIÓN Y BROKER", "1. Confirmar que el broker aparezca en el padrón oficial de la CNBV (México) o BrokerCheck / SEC (EE. UU.)."),
            ("REGULACIÓN Y BROKER", "2. Descargar la app directo de App Store / Google Play verificando el desarrollador oficial — jamás APK o link."),
            ("PRE-IPO Y ANUNCIOS", "3. Rechazar de inmediato cualquier anuncio con deepfake de Ashton Kutcher, Dario Amodei o 'acceso Pre-IPO VIP'."),
            ("PRE-IPO Y ANUNCIOS", "4. Verificar en fuentes oficiales que NO existen tokens cripto ni memecoins respaldadas por Anthropic Nasdaq."),
            ("IDENTIDAD Y KYC", "5. Nunca enviar foto de INE, pasaporte o comprobante de domicilio por WhatsApp o formularios web sin verificación."),
            ("IDENTIDAD Y KYC", "6. Pagar únicamente a cuentas CLABE a nombre de la institución financiera regulada — nunca a cuentas personales."),
            ("SEGURIDAD CUENTA", "7. Activar 2FA con app autenticadora (no SMS) y contraseña única en tu cuenta de broker y correo ligado."),
            ("SEGURIDAD CUENTA", "8. Aplicar regla de oro: todo rendimiento 'garantizado o multiplicado en días' es estafa matemática garantizada."),
        ],
        emerg_title="¿Ya depositaste o mandaste foto de tu INE a un falso broker?",
        emerg_steps=[
            "1. CONGELA TRANSFERENCIAS Y TARJETAS en tu banco y conserva capturas de la página, cuentas CLABE/cripto y conversaciones.",
            "2. ALERTA EN BURO DE CRÉDITO / CÍRCULO DE CRÉDITO (bloqueo preventivo) para impedir préstamos apócrifos con tu INE.",
            "3. DENUNCIA ante Policía Cibernética y CONDUSEF si hubo suplantación financiera; jamás pagues 'comisiones para liberar ganancias'.",
        ],
        footer_left="captoora.studio  ·  Serie ¡WATERS! Ciberseguridad Financiera  ·  CTA: BOLSA",
    )

    # 2) GUIA_CONTADOR_IA_SAT_CAPTOORA.pdf (EP08)
    build_two_page_guide(
        out_path=OUT_DIR / "GUIA_CONTADOR_IA_SAT_CAPTOORA.pdf",
        doc_title="GUIA CONTADOR - IA Contable Segura sin Riesgos ante el SAT | Captoora Studio",
        pill_tag="CAPTOORA STUDIO  ·  GUÍA CONTADOR",
        date_tag="ARQUITECTURA IA + SAT 2026",
        hero_h1="GUÍA CONTADOR: Automatiza con IA sin Regalar el SAT",
        hero_sub="Cómo usar agentes contables (tipo Claude Contador) para ordenar tickets y XML sin exponer tu e.firma",
        hero_rule="Regla de oro: la IA hace el 90% de la talacha de orden; las llaves del SAT y la firma son 100% humanas.",
        accent_bar=CYAN,
        sec1_title="1. Gran ayuda vs. Peligro mortal al usar agentes contables de IA",
        evidence=[
            (
                "LO BUENO (PRODUCTIVIDAD)",
                "Tickets y XML en minutos",
                "Extrae RFC, IVA y conceptos de fotos de tickets, clasifica CFDI 4.0 y prepara pre-cierre y conciliación en segundos.",
                EMERALD,
            ),
            (
                "PELIGRO 1 Y 2 (CIBERSEGURIDAD)",
                "e.firma + PDF Injection",
                "Subir .cer/.key y CIEC entrega firma autógrafa digital; una factura PDF maliciosa puede ocultar instrucciones para desviar pagos.",
                RED_ALERT,
            ),
            (
                "PELIGRO 3 (FISCAL SAT)",
                "Alucinaciones en tu RFC",
                "Si la IA clasifica mal un gasto o inventa deducibles en RESICO/PFAE, la multa y recargos caen 100% sobre tu RFC.",
                GOLD,
            ),
        ],
        sec2_title="2. Los 4 Candados de Arquitectura Segura (IA Copiloto Read-Only)",
        shields=[
            (
                "1",
                "MODO BORRADOR SOLO LECTURA (CERO PAGOS NI TIMBRADOS AUTÓNOMOS)",
                "Conecta el agente para generar tablas Excel, clasificar XMLs y redactar pre-pólizas. Jamás le des permisos para ejecutar transferencias SPEI ni presentar declaraciones definitivas sin clic humano.",
                TEAL_DARK,
                False,
            ),
            (
                "2",
                "JAMÁS SUBAS TU E.FIRMA (.CER / .KEY) NI CONTRASEÑA CIEC A CHATS",
                "En México la e.firma equivale legalmente a tu firma ante notario. Ningún bot, extensión de navegador o plugin sin auditoría debe almacenar tus archivos privados ni tu contraseña fiscal.",
                RED_ALERT,
                False,
            ),
            (
                "3",
                "PROTEGE CONTRA 'PROMPT INJECTION' EN FACTURAS DE TERCEROS",
                "Trata todo PDF externo como texto no confiable: usa validadores de esquema XML oficial antes del LLM y exige aprobación humana explícita ante cualquier cambio de CLABE bancaria o correo.",
                BLUE_ACC,
                False,
            ),
            (
                "4",
                "DIVIDE EL FLUJO: IA ORDENA (90%) + CONTADOR HUMANO VALIDA Y FIRMA (100%)",
                "Anonimiza o enmascara números de cuenta antes de subir CSVs bancarios. Deja que la IA prepare tu carpeta ordenada y que tu contador certificado valide deducibilidad antes de declarar.",
                GOLD,
                True,
            ),
        ],
        p2_title="CHECKLIST DE 8 PUNTOS · IA CONTABLE BLINDADA ANTE EL SAT",
        p2_sub="Audita tu flujo antes de conectar cualquier agente contable con tus finanzas",
        checklist_items=[
            ("LLAVES Y ACCESOS", "1. Verificar que ningún archivo .cer, .key ni contraseña CIEC del SAT esté en chats, prompts, plugins o repositorios."),
            ("LLAVES Y ACCESOS", "2. Resguardar la e.firma física en USB cifrado local; firmar trámites únicamente en el portal oficial del SAT."),
            ("PRIVACIDAD Y DATOS", "3. Enmascarar RFC completos y cuentas CLABE en CSVs/estados bancarios antes de analizar gastos con modelos públicos."),
            ("PRIVACIDAD Y DATOS", "4. Activar configuración Enterprise / Zero-Data-Retention cuando proceses estados financieros de tu empresa."),
            ("DEFENSA INJECTION", "5. Bloquear acciones externas automáticas (envío de correos, transferencias, webhooks) sin aprobación Human-in-the-Loop."),
            ("DEFENSA INJECTION", "6. Extraer datos de CFDI directamente del XML estructurado oficial en vez de confiar solo en el texto libre del PDF."),
            ("CONTROL FISCAL", "7. Cruzar siempre UUID de facturas contra lista negra Art. 69-B y estatus Vigente en el verificador del SAT."),
            ("CONTROL FISCAL", "8. Pasar siempre el pre-cierre generado por IA a revisión de tu contador público antes de presentar pago provisional."),
        ],
        emerg_title="¿Subiste tu e.firma o sospechas de una app pirata de 'Claude Contador'?",
        emerg_steps=[
            "1. REVOCA DE INMEDIATO tu e.firma desde SAT ID o presencialmente y tramita renovación + cambia contraseña CIEC.",
            "2. REVISA TU BUZÓN TRIBUTARIO y CFDIs emitidos/recibidos recientemente para detectar facturas apócrifas bajo tu RFC.",
            "3. DESINSTALA EXTENSIONES O SCRIPTS NO OFICIALES y rota contraseñas bancarias y de correo corporativo.",
        ],
        footer_left="captoora.studio  ·  Serie ¡WATERS! Ciberseguridad Fiscal IA  ·  CTA: CONTADOR",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
