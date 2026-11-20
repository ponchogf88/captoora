#!/usr/bin/env python3
"""
Genera audio + SFX ASMR + beat timeline para EP08:
  "Claude Tu Nuevo Contador: Qué Buena Ayuda (tickets/CFDI) vs. Peligro Mortal (e.firma, PDF Injection, SAT)"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from waters_audio_engine import ROOT, compile_episode_audio

OUT_AUDIO = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP08_AGENTE_CONTABLE"

EP08_SCRIPT = [
    {
        "id": "01_tony",
        "speaker": "tony",
        "text": "[serious] Waters!",
        "language_code": "en",
        "stability": 0.35,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "IA CONTABLE · TICKETS Y CFDI",
                "accentColor": "#00F5D4",
                "expression": "star_eyes",
                "cardType": "dual_cards",
                "stageProp": "tax_vault",
                "safeMode": True,
                "stepBadge": "✦",
                "pillText": "Agentes contables de nueva generación",
                "headlinePrefix": "Tu nuevo",
                "headlineFocus": "contador IA",
                "headlineSuffix": "¿ayuda o bomba?",
                "terminalCmd": "$ agent-fiscal --scan tickets_mes.jpg cfdi_40.xml",
                "terminalSub": "✓ Ordena facturas y gastos en segundos... PERO OJO",
                "cardItems": [
                    {"title": "LO BUENO ⚡", "sub": "Ordena XML en segundos", "color": "#22C55E"},
                    {"title": "EL PELIGRO 🔥", "sub": "Llaves SAT en riesgo", "color": "#FF3B3B"},
                ],
                "pops": [2, 8, 20, 32],
            }
        ],
    },
    {
        "id": "02_agy",
        "speaker": "agy",
        "text": "[excited] Anthropic presentó agentes que le toman foto a cada ticket y te arman toda tu contabilidad y XML en segundos... pero ¡cuidado!",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "LO BUENO · AUTOMATIZACIÓN BRUTAL",
                "accentColor": "#22C55E",
                "expression": "happy_open",
                "cardType": "dual_cards",
                "stageProp": "tax_vault",
                "safeMode": True,
                "stepBadge": "1",
                "pillText": "De tickets sueltos a carpeta lista",
                "headlinePrefix": "Foto al ticket y XML listos en",
                "headlineFocus": "segundos",
                "headlineSuffix": "",
                "terminalCmd": "$ claude-tax --extract RFC,IVA,concepto --build carpeta",
                "terminalSub": "✓ Detecta gastos y prepara tu pre-cierre mensual",
                "cardItems": [
                    {"title": "OCR TICKETS", "sub": "RFC + IVA automático", "color": "#22C55E"},
                    {"title": "CRUCE XML 4.0", "sub": "Pre-cierre al instante", "color": "#00F5D4"},
                ],
                "pops": [2, 8, 20, 32],
            }
        ],
    },
    {
        "id": "03_tony",
        "speaker": "tony",
        "text": "[serious] La mayoría se emociona y le suelta estados de cuenta, contraseñas y hasta su e-firma del SAT directo a cualquier bot.",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "EL ERROR FATAL · SIN CANDADOS",
                "accentColor": "#FF3B3B",
                "expression": "sad_cloud",
                "cardType": "dual_cards",
                "stageProp": "tax_vault",
                "safeMode": False,
                "stepBadge": "⚠",
                "pillText": "Subir tus llaves privadas a ciegas",
                "headlinePrefix": "Error: regalar tu",
                "headlineFocus": "e.firma SAT",
                "headlineSuffix": "al bot",
                "terminalCmd": "$ warn --upload efirma.cer,efirma.key --cloud_bot UNSAFE",
                "terminalSub": "! Entregas firma legal + movimientos bancarios reales",
                "cardItems": [
                    {"title": ".CER + .KEY + CIEC", "sub": "Firma ante notario", "color": "#FF3B3B"},
                    {"title": "PDFs BANCARIOS", "sub": "Fuga de datos PII", "color": "#FF3B3B"},
                ],
                "pops": [2, 8, 20, 32],
            }
        ],
    },
    {
        "id": "04_tony",
        "speaker": "tony",
        "text": "[serious] Es una ayuda brutal... pero si la IA se equivoca o te hackean, la multa del SAT no la paga Claude: la pagas tú.",
        "stability": 0.28,
        "lead_silence_sec": 0.35,  # Silencio dramatico antes del Giro!
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "EL GIRO FISCAL · RESPONSABILIDAD",
                "accentColor": "#00F5D4",
                "expression": "shock_sweat",
                "cardType": "giro_punch",
                "stageProp": "tax_vault",
                "safeMode": False,
                "stepBadge": "⚡",
                "pillText": "Quien responde ante el SAT eres tú",
                "headlinePrefix": "La multa del SAT la",
                "headlineFocus": "pagas tú",
                "headlineSuffix": "",
                "terminalCmd": "$ audit --rfc YOUR_RFC --liability owner=100%",
                "terminalSub": "⚠ El modelo alucina: los recargos van a tu RFC",
                "giroTop": "SI EL AGENTE FALLA O TE HACKEAN",
                "giroBottom": "⚠ La multa NO la paga Claude: LA PAGAS TÚ",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "05_agy",
        "speaker": "agy",
        "text": "[serious] Tienes tres peligros gigantes: exponer tu e-firma legal, facturas PDF con comandos ocultos para desviar pagos y deducciones inventadas en tu RFC.",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "3 PELIGROS REALES · SAT + CYBER",
                "accentColor": "#FF3B3B",
                "expression": "determined_hacker",
                "cardType": "triple_cards",
                "stageProp": "terminator",
                "stepBadge": "3",
                "pillText": "Ataques y errores invisibles hoy",
                "headlinePrefix": "Los 3 peligros con",
                "headlineFocus": "agentes fiscales",
                "headlineSuffix": "",
                "terminalCmd": "$ scan-pdf --payload hidden_prompt_injection",
                "terminalSub": "! Una factura maliciosa puede cambiar tu CLABE de pago",
                "cardItems": [
                    {"title": "E.FIRMA LEGAL", "sub": "Pueden facturar por ti", "color": "#FF3B3B"},
                    {"title": "PDF INJECTION", "sub": "Desvía pagos ocultos", "color": "#FF3B3B"},
                    {"title": "ALUCINACIÓN SAT", "sub": "Multas en tu RFC", "color": "#FF3B3B"},
                ],
                "pops": [2, 8, 16, 26, 36],
            }
        ],
    },
    {
        "id": "06_agy",
        "speaker": "agy",
        "text": "[serious] Paso uno: úsalo en modo borrador solo lectura; cero pagos ni timbrados autónomos.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "ARQUITECTURA · PASO 1 DE 4",
                "accentColor": "#00F5D4",
                "expression": "happy_open",
                "cardType": "step_single",
                "stageProp": "shield_vault",
                "stepBadge": "1",
                "pillText": "Copiloto Read-Only en borrador",
                "headlinePrefix": "Paso 1: solo",
                "headlineFocus": "modo borrador",
                "headlineSuffix": "Read-Only",
                "terminalCmd": "$ agent-policy --mode READ_ONLY --autonomous-pay BLOCKED",
                "terminalSub": "✓ La IA ordena Excel/pre-pólizas; tú autorizas todo",
                "stepTitle": "1. Modo Borrador Read-Only",
                "stepDetail": "Cero transferencias SPEI o timbrados autónomos",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "07_agy",
        "speaker": "agy",
        "text": "[serious] Paso dos: jamás subas tu e-firma ni contraseña del SAT a chats o plugins.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "ARQUITECTURA · PASO 2 DE 4",
                "accentColor": "#00F5D4",
                "expression": "zen_proud",
                "cardType": "step_single",
                "stageProp": "tax_vault",
                "safeMode": True,
                "stepBadge": "2",
                "pillText": "Tu firma privada nunca entra al chat",
                "headlinePrefix": "Paso 2: cero",
                "headlineFocus": ".cer y .key",
                "headlineSuffix": "en la nube",
                "terminalCmd": "$ vault --keep-local efirma_usb --cloud-upload DENIED",
                "terminalSub": "✓ Solo firma trámites directo en el portal oficial SAT",
                "stepTitle": "2. Llaves e.firma 100% Locales",
                "stepDetail": "Nunca entregues .cer, .key ni CIEC a bots",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "08_agy",
        "speaker": "agy",
        "text": "[serious] Paso tres: oculta RFC y cuentas bancarias antes de analizar estados de cuenta.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "ARQUITECTURA · PASO 3 DE 4",
                "accentColor": "#00F5D4",
                "expression": "determined_hacker",
                "cardType": "step_single",
                "stageProp": "laptop",
                "stepBadge": "3",
                "pillText": "Sanitiza CSVs y PDFs bancarios",
                "headlinePrefix": "Paso 3: anonimiza",
                "headlineFocus": "CLABE y RFC",
                "headlineSuffix": "primero",
                "terminalCmd": "$ scrub --mask clabe,rfc,nombre --before-prompt true",
                "terminalSub": "✓ Clasifica montos y fechas sin regalar identidad",
                "stepTitle": "3. Enmascara Datos Antes del LLM",
                "stepDetail": "Valida XML estructurado y activa Zero-Retention",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "09_agy",
        "speaker": "agy",
        "text": "[serious] Paso cuatro: tu contador humano siempre revisa y valida antes de declarar al SAT.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "ARQUITECTURA · PASO 4 DE 4",
                "accentColor": "#00F5D4",
                "expression": "happy_arcs",
                "cardType": "step_single",
                "stageProp": "shield_vault",
                "stepBadge": "4",
                "pillText": "Revisión profesional Human-in-the-Loop",
                "headlinePrefix": "Paso 4: tu",
                "headlineFocus": "contador humano",
                "headlineSuffix": "valida",
                "terminalCmd": "$ sign-off --reviewer CPA_Humano --check 69B_SAT PASS",
                "terminalSub": "✓ Revisa UUID vigente y lista negra 69-B antes del envío",
                "stepTitle": "4. Doble Check con Contador Real",
                "stepDetail": "IA agiliza el orden; el criterio fiscal es humano",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "10_tony",
        "speaker": "tony",
        "text": "[confident] Que la inteligencia artificial haga el noventa por ciento de la talacha de orden... pero tus llaves del SAT y tu firma siempre se quedan en tus manos.",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "LA FÓRMULA GANADORA",
                "accentColor": "#00F5D4",
                "expression": "happy_open",
                "cardType": "dual_cards",
                "stageProp": "tax_vault",
                "safeMode": True,
                "stepBadge": "💎",
                "pillText": "Productividad brutal sin riesgo fiscal",
                "headlinePrefix": "IA hace el 90%: tu",
                "headlineFocus": "firma siempre tuya",
                "headlineSuffix": "",
                "terminalCmd": "$ balance --ai-work 90%_orden --human-keys 100%_control",
                "terminalSub": "✓ Ahorras horas cada cierre sin abrir brechas al SAT",
                "cardItems": [
                    {"title": "90% IA COPILOTO", "sub": "Ordena tickets y XML", "color": "#22C55E"},
                    {"title": "100% TU FIRMA", "sub": "Llaves locales + Contador", "color": "#00F5D4"},
                ],
                "pops": [2, 8, 20, 32],
            }
        ],
    },
    {
        "id": "11_agy",
        "speaker": "agy",
        "text": "[excited] Comenta CONTADOR y te mando gratis el checklist para usar IA fiscal sin entregar tus llaves al SAT.",
        "stability": 0.32,
        "lead_silence_sec": 0.30,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "GUÍA PDF + CHECKLIST 8 PUNTOS",
                "accentColor": "#00F5D4",
                "expression": "happy_arcs",
                "cardType": "cta_blinda",
                "stageProp": "kit_box",
                "stepBadge": "🚀",
                "pillText": "Checklist IA + SAT gratis en tu DM",
                "headlinePrefix": "Comenta la palabra",
                "headlineFocus": "CONTADOR",
                "headlineSuffix": "👇",
                "terminalCmd": "$ send-dm --keyword CONTADOR --file guia_contador_sat.pdf",
                "terminalSub": "✓ Arquitectura Read-Only + Defensa PDF Injection",
                "stepTitle": "CONTADOR",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "12_tony",
        "speaker": "tony",
        "text": "[excited] Waters!",
        "language_code": "en",
        "stability": 0.35,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "SERIE ¡WATERS! · CAPTOORA",
                "accentColor": "#00F5D4",
                "expression": "wink",
                "cardType": "cta_blinda",
                "stageProp": "kit_box",
                "stepBadge": "🌊",
                "pillText": "¡Automatiza con candado!",
                "headlinePrefix": "Cuida tu RFC y llaves:",
                "headlineFocus": "¡WATERS!",
                "headlineSuffix": "🌊🛡️",
                "terminalCmd": "$ status --tax-shield ACTIVE --cta CONTADOR",
                "terminalSub": "✓ Comenta CONTADOR para recibir la guía PDF",
                "stepTitle": "¡WATERS! 💼",
                "pops": [2, 8, 18],
            }
        ],
    },
]


def main() -> int:
    return compile_episode_audio(
        ep_tag="EP08",
        beats_key="EP08_AGENTE_CONTABLE",
        out_dir=OUT_AUDIO,
        script=EP08_SCRIPT,
        seed=8882026,
    )


if __name__ == "__main__":
    raise SystemExit(main())
