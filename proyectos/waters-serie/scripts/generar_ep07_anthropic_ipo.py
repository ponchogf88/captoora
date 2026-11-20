#!/usr/bin/env python3
"""
Genera audio + SFX ASMR + beat timeline para EP07:
  "Anthropic IPO ($81.3B, 5,100 millonarios, Ashton Kutcher) + Estafas Pre-IPO / Deepfake KYC"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from waters_audio_engine import ROOT, compile_episode_audio

OUT_AUDIO = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP07_ANTHROPIC_IPO"

EP07_SCRIPT = [
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
                "topTag": "NASDAQ: ANT · RÉCORD $81.3B",
                "accentColor": "#22C55E",
                "expression": "star_eyes",
                "cardType": "dual_cards",
                "stageProp": "stock_chart",
                "stepBadge": "🚀",
                "pillText": "Anthropic debutó en Nasdaq hoy",
                "headlinePrefix": "Crearon",
                "headlineFocus": "5,100 millonarios",
                "headlineSuffix": "en 1 día",
                "terminalCmd": "$ quote NASDAQ:ANT --ipo 83.00 --open 111.50",
                "terminalSub": "✓ Récord histórico $81.3B USD · 96% equipo >$1M",
                "cardItems": [
                    {"title": "NASDAQ: ANT", "sub": "$83 ➔ $111.50", "color": "#22C55E"},
                    {"title": "5,100 STAFF", "sub": "Millonarios (papel)", "color": "#DFB15B"},
                ],
                "pops": [2, 8, 20, 32],
            }
        ],
    },
    {
        "id": "02_agy",
        "speaker": "agy",
        "text": "[excited] Anthropic, los dueños de Claude, salieron a la bolsa y crearon cinco mil cien millonarios en una sola noche... y Ashton Kutcher convirtió cuatrocientos millones en diez mil millones de dólares.",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 0.48,
                "topTag": "SALIDA EN BOLSA · CLAUDE",
                "accentColor": "#22C55E",
                "expression": "happy_open",
                "cardType": "dual_cards",
                "stageProp": "stock_chart",
                "stepBadge": "1",
                "pillText": "De $83 a $111.50 USD por acción",
                "headlinePrefix": "Los dueños de Claude en",
                "headlineFocus": "Wall Street",
                "headlineSuffix": "📈",
                "terminalCmd": "$ stats --company Anthropic --employees 5100",
                "terminalSub": "✓ Ojo: riqueza en acciones sujeta a lock-up",
                "cardItems": [
                    {"title": "CLAUDE IPO", "sub": "$81.3 Mil M recaudados", "color": "#22C55E"},
                    {"title": "EQUIPO 96%", "sub": "5,100 con >$1M USD", "color": "#DFB15B"},
                ],
                "pops": [2, 8, 20, 32],
            },
            {
                "ratio": 0.52,
                "topTag": "SOUND VENTURES · ASHTON KUTCHER",
                "accentColor": "#DFB15B",
                "expression": "star_eyes",
                "cardType": "dual_cards",
                "stageProp": "stock_chart",
                "stepBadge": "💰",
                "pillText": "Cómo lo logró Ashton de verdad",
                "headlinePrefix": "Ashton convirtió $435M en",
                "headlineFocus": "$10,000M",
                "headlineSuffix": "",
                "terminalCmd": "$ trace --fund SoundVentures --year 2023 --round private",
                "terminalSub": "✓ Fondo VC acreditado 3 años antes de bolsa",
                "cardItems": [
                    {"title": "2023 · PRIVADO", "sub": "$435M (Fondo VC)", "color": "#DFB15B"},
                    {"title": "2026 · NASDAQ", "sub": "~$7B–$10B estimados", "color": "#22C55E"},
                ],
                "pops": [2, 8, 20, 32],
            },
        ],
    },
    {
        "id": "03_tony",
        "speaker": "tony",
        "text": "[serious] El problema es que al ver dinero tan rápido, miles de personas caen en anuncios prometiendo 'acciones antes de la bolsa como Ashton' por WhatsApp.",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "EL ERROR FOMO · TRAMPA ACTIVA",
                "accentColor": "#FF3B3B",
                "expression": "sad_cloud",
                "cardType": "dual_cards",
                "stageProp": "laptop",
                "stepBadge": "⚠",
                "pillText": "Anuncios falsos de 'Pre-IPO VIP'",
                "headlinePrefix": "El anzuelo en redes:",
                "headlineFocus": "Pre-IPO por DM",
                "headlineSuffix": "❌",
                "terminalCmd": "$ detect --scam 'Compra Claude Pre-IPO hoy por WhatsApp'",
                "terminalSub": "! Nadie vende acciones privadas reales por Instagram",
                "cardItems": [
                    {"title": "ANUNCIO FAKE", "sub": "'Invierte como Ashton'", "color": "#FF3B3B"},
                    {"title": "REALIDAD SEC", "sub": "Solo fondos cerrados", "color": "#00F5D4"},
                ],
                "pops": [2, 8, 20, 32],
            }
        ],
    },
    {
        "id": "04_tony",
        "speaker": "tony",
        "text": "[serious] Aguas: cuando veas dinero fácil y un link milagroso... el negocio no son las acciones: eres tú.",
        "stability": 0.28,
        "lead_silence_sec": 0.35,  # Silencio dramatico antes del Giro
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "EL GIRO CRÍTICO · FOMO",
                "accentColor": "#00F5D4",
                "expression": "shock_sweat",
                "cardType": "giro_punch",
                "stageProp": "laptop",
                "stepBadge": "⚡",
                "pillText": "La regla de oro en inversiones",
                "headlinePrefix": "En links milagrosos,",
                "headlineFocus": "tú eres el negocio",
                "headlineSuffix": "",
                "terminalCmd": "$ audit --promise 'x10 garantizado en 48h'",
                "terminalSub": "⚠ Si viene de un DM o link en comentarios: ES ESTAFA",
                "giroTop": "LINK MILAGROSO = TRAMPA",
                "giroBottom": "⚠ El negocio NO son las acciones: ERES TÚ",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "05_agy",
        "speaker": "agy",
        "text": "[serious] Hoy circulan tres trampas: enlaces de acciones pre-IPO o tokens falsos, videos deepfake pidiendo foto de tu INE y apps piratas de Claude Contador para robarte tu e-firma.",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "3 ESTAFAS CLONADAS CON IA",
                "accentColor": "#FF3B3B",
                "expression": "determined_hacker",
                "cardType": "triple_cards",
                "stageProp": "terminator",
                "stepBadge": "3",
                "pillText": "Las 3 trampas tras el IPO",
                "headlinePrefix": "Cuidado con estas",
                "headlineFocus": "3 trampas",
                "headlineSuffix": "de hoy",
                "terminalCmd": "$ threat-intel --campaign ant_ipo_scams",
                "terminalSub": "! Roban tu depósito, tu INE (KYC) y tu e.firma SAT",
                "cardItems": [
                    {"title": "PRE-IPO / TOKEN", "sub": "$ANT / $CLAUDE fake", "color": "#FF3B3B"},
                    {"title": "DEEPFAKE KYC", "sub": "Pide foto INE + selfie", "color": "#FF3B3B"},
                    {"title": "CONTADOR FAKE", "sub": "Roba tu e.firma SAT", "color": "#FF3B3B"},
                ],
                "pops": [2, 8, 16, 26, 36],
            }
        ],
    },
    {
        "id": "06_agy",
        "speaker": "agy",
        "text": "[serious] Paso uno: jamás compres acciones ni tokens por DM o WhatsApp.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "CANDADO · PASO 1 DE 4",
                "accentColor": "#22C55E",
                "expression": "happy_open",
                "cardType": "step_single",
                "stageProp": "shield_vault",
                "stepBadge": "1",
                "pillText": "Cero compras en chats o links",
                "headlinePrefix": "Paso 1: cero compras por",
                "headlineFocus": "DM o WhatsApp",
                "headlineSuffix": "",
                "terminalCmd": "$ block --source telegram,whatsapp,ig_dm --asset pre_ipo",
                "terminalSub": "✓ No existe venta minorista pre-IPO ni token oficial",
                "stepTitle": "1. Cero Acciones por DM",
                "stepDetail": "Bloquea links que vendan Pre-IPO o $CLAUDE",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "07_agy",
        "speaker": "agy",
        "text": "[serious] Paso dos: verifica el broker ante la CNBV o la SEC antes de mandar tu INE.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "CANDADO · PASO 2 DE 4",
                "accentColor": "#22C55E",
                "expression": "determined_hacker",
                "cardType": "step_single",
                "stageProp": "shield_vault",
                "stepBadge": "2",
                "pillText": "Valida padrón oficial CNBV / SEC",
                "headlinePrefix": "Paso 2: valida el",
                "headlineFocus": "broker regulado",
                "headlineSuffix": "",
                "terminalCmd": "$ verify-broker --registry CNBV_MX,SEC_US --app official_store",
                "terminalSub": "✓ Solo apps oficiales antes de subir INE o pasaporte",
                "stepTitle": "2. Broker Regulado CNBV/SEC",
                "stepDetail": "Jamás subas foto de tu INE a páginas nuevas",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "08_agy",
        "speaker": "agy",
        "text": "[serious] Paso tres: nunca subas tu e-firma del SAT a apps o bots no verificados.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "CANDADO · PASO 3 DE 4",
                "accentColor": "#22C55E",
                "expression": "happy_arcs",
                "cardType": "step_single",
                "stageProp": "tax_vault",
                "safeMode": True,
                "stepBadge": "3",
                "pillText": "Protege tu archivo .cer y .key",
                "headlinePrefix": "Paso 3: no regales tu",
                "headlineFocus": "e.firma SAT",
                "headlineSuffix": "",
                "terminalCmd": "$ guard --files efirma.cer,efirma.key --share NEVER",
                "terminalSub": "✓ Tu e.firma vale igual que tu firma física ante notario",
                "stepTitle": "3. e.firma Siempre Contigo",
                "stepDetail": "No la subas a apps milagro de 'Claude Contador'",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "09_agy",
        "speaker": "agy",
        "text": "[serious] Paso cuatro: desconfía de todo video prometiendo rendimientos garantizados.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "CANDADO · PASO 4 DE 4",
                "accentColor": "#22C55E",
                "expression": "zen_proud",
                "cardType": "step_single",
                "stageProp": "stock_chart",
                "stepBadge": "4",
                "pillText": "En bolsa real no hay retornos fijos x10",
                "headlinePrefix": "Paso 4: huye de",
                "headlineFocus": "retornos garantizados",
                "headlineSuffix": "",
                "terminalCmd": "$ filter --deepfake celebrity --claim 'guaranteed_profit'",
                "terminalSub": "✓ Si promete ganancias seguras y rápidas: es trampa",
                "stepTitle": "4. Cero Promesas Garantizadas",
                "stepDetail": "La bolsa real tiene riesgo y regulación formal",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "10_tony",
        "speaker": "tony",
        "text": "[serious] La inteligencia artificial sí está revolucionando la bolsa y las finanzas... pero quien se apura por avaricia entrega sus llaves y su dinero en cinco minutos.",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "PUENTE · FOMO VS ESTRATEGIA",
                "accentColor": "#DFB15B",
                "expression": "happy_open",
                "cardType": "dual_cards",
                "stageProp": "stock_chart",
                "stepBadge": "⚖",
                "pillText": "No entregues tus llaves por prisa",
                "headlinePrefix": "Invierte con cabeza, no por",
                "headlineFocus": "avaricia FOMO",
                "headlineSuffix": "",
                "terminalCmd": "$ compare --strategy 'Regulado CNBV' vs 'Link DM FOMO'",
                "terminalSub": "✓ Tiempo + regulación ganan al hype de 5 minutos",
                "cardItems": [
                    {"title": "BROKERS REALES", "sub": "Ticker ANT Nasdaq", "color": "#22C55E"},
                    {"title": "PRISA / FOMO", "sub": "Pérdida en 5 min ❌", "color": "#FF3B3B"},
                ],
                "pops": [2, 8, 20, 32],
            }
        ],
    },
    {
        "id": "11_agy",
        "speaker": "agy",
        "text": "[excited] Comenta BOLSA y te mando gratis la guía para invertir sin caer en brokers ni apps falsas.",
        "stability": 0.32,
        "lead_silence_sec": 0.30,  # Pausa breve antes del CTA
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "GUÍA PDF + CHECKLIST 8 PUNTOS",
                "accentColor": "#22C55E",
                "expression": "happy_arcs",
                "cardType": "cta_blinda",
                "stageProp": "kit_box",
                "stepBadge": "🚀",
                "pillText": "Checklist gratis directo a tu DM",
                "headlinePrefix": "Comenta la palabra",
                "headlineFocus": "BOLSA",
                "headlineSuffix": "👇",
                "terminalCmd": "$ send-dm --keyword BOLSA --file guia_bolsa_preipo.pdf",
                "terminalSub": "✓ Caso real Ashton Kutcher + 8 filtros anti-fraude",
                "stepTitle": "BOLSA",
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
                "accentColor": "#22C55E",
                "expression": "wink",
                "cardType": "cta_blinda",
                "stageProp": "kit_box",
                "stepBadge": "🌊",
                "pillText": "¡Toma tus precauciones hoy!",
                "headlinePrefix": "No entregues tu lana:",
                "headlineFocus": "¡WATERS!",
                "headlineSuffix": "🌊📈",
                "terminalCmd": "$ status --shield VERIFIED --cta BOLSA",
                "terminalSub": "✓ Comenta BOLSA para recibir la guía PDF",
                "stepTitle": "¡WATERS! 📈",
                "pops": [2, 8, 18],
            }
        ],
    },
]


def main() -> int:
    return compile_episode_audio(
        ep_tag="EP07",
        beats_key="EP07_ANTHROPIC_IPO",
        out_dir=OUT_AUDIO,
        script=EP07_SCRIPT,
        seed=7772026,
    )


if __name__ == "__main__":
    raise SystemExit(main())
