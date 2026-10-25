# BANDA CEREBRO — Estudio de fotos (Captoora)

Actualizado: 2026-09-18. P0 = **publicar en redes del estudio**, no el sitio esqueleto.

## Standing order

Founder dice **“publica esto”** o **“publica plantilla N”** → Grok ejecuta `scripts/publish.py`.  
No pedir password. No re-explicar el negocio. No inventar carrusel.

Skill: `/captoora-ops` → `~/.grok/skills/captoora-ops/SKILL.md`

## Cuentas

| Red | Este negocio | Prohibido (Likinya) |
|---|---|---|
| Instagram | las del estudio (conectar en Publora) | `@likinhya` |
| Facebook | Reacción Fotografía / page del estudio | Likinya Betancourt |
| TikTok | la del estudio | `@likinya8062` |
| X | si existe para el estudio | `@CelestialSSh` |

WhatsApp venta: `+52 81 4005-0088`

## Estado de publicación (2026-09-18)

Publora API key **sí existe** (misma cuenta que Likinya).  
Conexiones actuales en esa key:

| Red | Usuario | Token | ¿Es este estudio? |
|---|---|---|---|
| Instagram | `@likinhya` | **expired** (revocado 17 sep) | NO |
| TikTok | `@likinya8062` | valid | NO |
| X | `@CelestialSSh` | valid | NO |
| Facebook | — | no conectado | — |

Meta token local es `amda makebot` y **no tiene Pages**. No sirve para publicar aquí.

**P0:** conectar en Publora las redes **de este estudio** (una vez, OAuth en el dashboard). Después: `publica plantilla N` y sale.

## Banco

Formato: `docs/TEMPLATES_BTS.md` (29 referencias).  
Assets propios listos: `Entrega_Pharmacy_Event_130926/` (391 fotos + recaps TikTok/YouTube).

## Roles (este proyecto)

| Rol | Hace | No hace |
|---|---|---|
| Grok | `publish.py`, list, log | pedir password |
| Claude | Stories solo si Chrome ya tiene sesión | feed si Publora sirve |
| Codex | captions si se piden | publicar |
| Agy | URL https pública del media | publicar |

## Comando

```bash
cd "/Users/imac/Desktop/Projects/CAPTOORA.STUDIO"
python3 scripts/publish.py list
python3 scripts/publish.py post --template 06 --text "HEADSHOT" --media "https://…"
```
