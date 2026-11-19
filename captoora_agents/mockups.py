"""Deterministic editorial PNG mockup and 1-page PDF dossier renderer via Chrome Headless."""

from __future__ import annotations

import argparse
import base64
import html
import mimetypes
import os
import re
import shutil
import subprocess
import tempfile
import urllib.parse
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Any, Literal

from . import ROOT_DIR
from .config import slugify, validate_client_copy


def _find_chrome_binary() -> Path:
    """Resolve Google Chrome / Edge executable across macOS, Windows, and Linux."""
    env_override = os.environ.get("CHROME_BIN")
    if env_override:
        return Path(env_override)
    candidates = [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ]
    for cand in candidates:
        if cand.exists():
            return cand
    for exe in ("google-chrome", "chromium", "chrome", "msedge"):
        found = shutil.which(exe)
        if found:
            return Path(found)
    return candidates[0]


CHROME_BIN = _find_chrome_binary()
MOCKUPS_DIR = ROOT_DIR / "assets" / "mockups"
BASES_DIR = MOCKUPS_DIR / "bases"
NICHE_HEROES_DIR = ROOT_DIR / "assets" / "niche_heroes"
CLUB_LOGOS_DIR = ROOT_DIR / "assets" / "club_logos"
ACRYLIC_BLANK_PATH = BASES_DIR / "padel_acrylic_blank.jpg"
DANCE_ACRYLIC_BLANK_PATH = BASES_DIR / "dance_acrylic_blank.jpg"
PADEL_ACTION_PATH = BASES_DIR / "padel_action_clean.jpg"
CAPTOORA_LOGO_PATH = ROOT_DIR / "assets" / "CAPTOORA_LOGO_TRANSPARENT.png"


@dataclass(frozen=True)
class MockupSpec:
    """Client-safe visual configuration for Captoora PNG mockups, PDFs, and email templates."""

    club_name: str
    tournament_name: str
    season_label: str = "NAVIDAD 2026"
    year: str = "2026"
    category_label: str = "PREMIO OFICIAL"
    sponsor_label: str = "ESPACIO PATROCINADOR 2026"
    city_label: str = "MONTERREY · SAN PEDRO"
    package_label: str = "HALFTIME BLITZ + TROFEOS ACRÍLICO LED"
    director_name: str = "Jesús Gutiérrez"
    director_role: str = "FOTÓGRAFO Y DIRECTOR · CAPTOORA STUDIO"
    email_address: str = "chuy@captoora.studio"
    website_url: str = "https://captoora.studio/sports"
    gallery_url: str = "https://galeria.captoora.studio"
    instagram_handle: str = "@captoora.studio"
    address_line: str = "Av. Paseo de los Álamos 165, Colinas de San Jerónimo, Monterrey, N.L."
    hours_line: str = "Lunes a domingo, 8:00 AM a 11:00 PM"
    whatsapp_display: str = "+52 81 4005 0088"
    whatsapp_url: str = "https://wa.me/528140050088"
    hero_photo_path: Path | None = None
    acrylic_base_path: Path | None = None
    plate_style: Literal["padel", "dance"] = "padel"
    club_logo_path: Path | None = None
    header_brand_title: str = "CAPTOORA SPORTS"
    hero_metrics: tuple[str, str, str] = ("RAW 1/2000s", "REELS VERTICALES", "CERO LOGÍSTICA EXTRA")
    extra_card: tuple[str, str, str, str] | None = None


def validate_mockup_spec(spec: MockupSpec) -> None:
    """Enforce Captoora client copy rules and mandatory 2026 edition identifier."""
    combined = " | ".join(
        [
            spec.club_name,
            spec.tournament_name,
            spec.season_label,
            spec.year,
            spec.category_label,
            spec.sponsor_label,
            spec.city_label,
            spec.package_label,
            spec.director_name,
            spec.director_role,
            *(spec.extra_card or ()),
        ]
    )
    violations = validate_client_copy(combined)
    if violations:
        raise ValueError(f"MockupSpec contiene términos prohibidos: {'; '.join(violations)}")
    if spec.year not in spec.season_label and spec.year != "2026":
        raise ValueError("El mockup debe identificar explícitamente el año vigente.")
    if "2026" not in f"{spec.year} {spec.season_label}":
        raise ValueError("Cada mockup navideño/editorial 2026 debe incluir el año 2026.")


@dataclass(frozen=True)
class NicheProfile:
    """Niche-specific visual hero, pillars, pricing descriptions, and WhatsApp snippets."""

    niche_key: str
    hero_path: Path
    after_tag: str
    after_overlay_sub: str
    hero_intro: str
    pillars: tuple[tuple[str, str], tuple[str, str], tuple[str, str]]
    tier1: tuple[str, str, str, str]
    tier2: tuple[str, str, str, str]
    tier3: tuple[str, str, str, str]
    wa_tier1: str
    wa_tier2: str
    wa_tier3: str
    wa_extra_bullet: str


NICHE_PROFILES: dict[str, NicheProfile] = {
    "Pádel & Raqueta": NicheProfile(
        niche_key="Pádel & Raqueta",
        hero_path=PADEL_ACTION_PATH,
        after_tag="MAPS + TORNEOS + LED",
        after_overlay_sub="Canchas nocturnas 1/2000s · Botón WhatsApp · Galería de Torneos",
        hero_intro=(
            "El nivel de tus canchas y torneos merece verse desde la primera búsqueda en Google Maps. "
            "Elevamos tu ficha con acción real en pista y dejamos tu Meta Business Suite en regla para llenar retas y posadas."
        ),
        pillars=(
            (
                "Pilar 1 · Fotografía de Cancha y Torneo 1/2000s",
                "Acción nocturna sin barrido, fachadas, terraza social y Reels 9:16 entregados el mismo día de evento.",
            ),
            (
                "Pilar 2 · Google Maps Verificado para Reservas",
                "Reclamamos tu ficha, subimos portada pro + 20–40 fotos de pista y activamos enlace directo a Playtomic/WhatsApp.",
            ),
            (
                "Pilar 3 · Patrocinadores y Acrílicos LED 2do Momento",
                "Unificamos Meta Business sin bloqueos y te entregamos trofeos acrílicos LED grabados con logos patrocinadores.",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · IMPULSO GOOGLE MAPS (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotos de pista, clubhouse y comunidad + verificación y carga directa en ficha de Google Maps.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE CLUB TOTAL (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 + Google Maps al 100% + Meta Business Portfolio (FB + IG + WhatsApp sin bloqueos).",
        ),
        tier3=(
            "OPCIÓN 3 · CLUB + TORNEO & LED QR (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Club Total + placa acrílica LED QR para reseñas/reservas + cobertura de Torneo / Posada financiable con marcas.",
        ),
        wa_tier1="1) Impulso Google Maps 2027: $6,000 -> $3,900 MXN (sesión pro de canchas + verificación y carga directa en Maps).",
        wa_tier2="2) Suite Club Total: $10,600 -> $6,890 MXN (foto 1/2000s + Reels + Maps + Setup Meta Business Portfolio sin bloqueos).",
        wa_tier3="3) Club + Posada & Placa LED QR: $16,000 -> $10,400 MXN (piezas acrílicas en taller MTY en 2do momento opcional).*",
        wa_extra_bullet="• Opción de combinarlo con su Torneo del Pavo / Posada y patrocinadores para autofinanciar premios LED.",
    ),
    "Fitness & CrossFit": NicheProfile(
        niche_key="Fitness & CrossFit",
        hero_path=NICHE_HEROES_DIR / "niche_fitness_gym.jpg",
        after_tag="MAPS + TOTALPASS + BIOGEN",
        after_overlay_sub="Portada de estudio · Ficha TotalPass / Maps · Piloto Biogen Beta",
        hero_intro=(
            "Un gimnasio o estudio de élite vende desde su energía visual en Google Maps y TotalPass. "
            "Producimos tu vitrina 2027, ordenamos Meta Business y sumamos el piloto Captoora Biogen Beta para fidelizar socios."
        ),
        pillars=(
            (
                "Pilar 1 · Producción Editorial Gym & Atletas",
                "Iluminación de alto contraste en zona de racks/turf, retratos de coaches y Reels 9:16 (+ piloto Captoora Biogen Beta).",
            ),
            (
                "Pilar 2 · Carga Directa Google Maps & TotalPass",
                "Reclamamos tu perfil, subimos portada pro + 20–40 fotos curadas y enlaces directos a clase prueba.",
            ),
            (
                "Pilar 3 · Meta Business Portfolio Cero Bloqueos",
                "Unificamos Facebook, Instagram Profesional y WhatsApp Business listos para pautar inscripciones enero 2027.",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · IMPULSO MAPS / TOTALPASS (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotos pro de instalaciones, equipo y clases + optimización directa de Google Maps y perfil TotalPass.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE STUDIO FITNESS TOTAL (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 + Google Maps/TotalPass al 100% + Meta Business Portfolio sin riesgo de bloqueos.",
        ),
        tier3=(
            "OPCIÓN 3 · ESTUDIO + PILOTO BIOGEN BETA (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Total + placa LED QR de reseñas + activación piloto Captoora Biogen Beta para socios (semanal/mensual).",
        ),
        wa_tier1="1) Impulso Google Maps / TotalPass: $6,000 -> $3,900 MXN (sesión pro + verificación y subida directa a Maps y TotalPass).",
        wa_tier2="2) Suite Studio Fitness Total: $10,600 -> $6,890 MXN (foto + Reels + Maps/TotalPass + Meta Business Portfolio en regla).",
        wa_tier3="3) Posicionamiento + Placa LED QR / Biogen Beta: $16,000 -> $10,400 MXN (acrílico LED diferible a un 2do momento).*",
        wa_extra_bullet="• Acceso preferente al piloto Captoora Biogen (Beta) de seguimiento visual de progreso en estudio (desde $1,268/mes -35%).",
    ),
    "Baile & Danza Señoras": NicheProfile(
        niche_key="Baile & Danza Señoras",
        hero_path=NICHE_HEROES_DIR / "niche_danza_studio.jpg",
        after_tag="MAPS + GALAS + META",
        after_overlay_sub="Editorial escenario y salón · Botón inscripciones · Meta Business",
        hero_intro=(
            "La elegancia, técnica y comunidad de tu academia de danza merecen proyectarse desde el primer vistazo en Google Maps y redes sociales. "
            "Curamos tu imagen 2027 y facilitamos cobertura de festivales sin fricción para dirección."
        ),
        pillars=(
            (
                "Pilar 1 · Retrato Escénico & Salones con Luz Cálida",
                "Sesión editorial de coreografías, maestras y salones con movimiento limpio y Reels 9:16 listos para inscripciones.",
            ),
            (
                "Pilar 2 · Google Maps Reclamado para Nuevas Alumnas",
                "Actualizamos tu ficha con portada editorial, horarios claros, galería curada y enlace directo a clase muestra.",
            ),
            (
                "Pilar 3 · Meta Business & Opcional Gala Navideña",
                "Ordenamos FB + IG + WhatsApp sin bloqueos y cubrimos tus galas con entrega digital el mismo día + trofeos LED opcionales.",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · IMPULSO GOOGLE MAPS DANZA (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotografías editoriales de salones, clases y maestras + carga y verificación directa en Google Maps.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE ACADEMIA TOTAL (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 + ficha de Google Maps optimizada + Meta Business Portfolio (FB + IG + WhatsApp).",
        ),
        tier3=(
            "OPCIÓN 3 · SUITE + COBERTURA GALA / LED (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Academia Total + placa LED QR de reseñas en recepción + crédito preferente para Gala Navideña 2026 / 2027.",
        ),
        wa_tier1="1) Impulso Google Maps Academia: $6,000 -> $3,900 MXN (sesión pro de clases y salones + carga directa en Maps).",
        wa_tier2="2) Suite Academia Total: $10,600 -> $6,890 MXN (foto editorial + Reels 9:16 + Maps + Meta Business en regla).",
        wa_tier3="3) Suite + Placa LED QR / Cobertura Gala: $16,000 -> $10,400 MXN (elementos físicos en taller MTY en 2do momento).*",
        wa_extra_bullet="• Opción White-Glove de galería privada y marcos de regalo para papás/alumnas en su festival o gala navideña.",
    ),
    "Clínicas & Consultorios": NicheProfile(
        niche_key="Clínicas & Consultorios",
        hero_path=NICHE_HEROES_DIR / "niche_clinica_dental.jpg",
        after_tag="MAPS + CONFIANZA MÉDICA",
        after_overlay_sub="Retrato clínico de confianza · Consultorio pro · Cita directa WhatsApp",
        hero_intro=(
            "Un paciente elige especialista por confianza antes de pisar el consultorio. "
            "Transformamos tu ficha de Google Maps en una carta de presentación limpia, humana y verificada lista para agendar citas."
        ),
        pillars=(
            (
                "Pilar 1 · Fotografía Médica Humana y de Instalaciones",
                "Retrato editorial de doctores y equipo con luz cálida, salas clínicas limpias y Reels 9:16 educativos.",
            ),
            (
                "Pilar 2 · Ficha Google Maps Segura para Pacientes",
                "Reclamamos tu ubicación, reemplazamos la vista Street View, subimos 20–40 fotos reales y link directo a cita.",
            ),
            (
                "Pilar 3 · Meta Business Portfolio en Regla Médica",
                "Conectamos Facebook, Instagram Profesional y WhatsApp Business sin bloqueos publicitarios ni pérdidas de cuenta.",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · IMPULSO GOOGLE MAPS CLÍNICO (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotos pro del consultorio, equipo médico y fachada + verificación oficial y subida directa a Google Maps.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE CLÍNICA TOTAL (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 de confianza + Google Maps al 100% + Meta Business Portfolio (FB + IG + WhatsApp).",
        ),
        tier3=(
            "OPCIÓN 3 · POSICIONAMIENTO + DISPLAY QR (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Clínica Total + placa LED acrílica elegante con QR directo a reseñas verificadas en Google Maps (entrega 3–5d).",
        ),
        wa_tier1="1) Impulso Google Maps Clínico: $6,000 -> $3,900 MXN (retrato médico + consultorio y verificación en Google Maps).",
        wa_tier2="2) Suite Clínica Total: $10,600 -> $6,890 MXN (30–40 fotos + Reels + Google Maps al 100% + Meta Business sin bloqueos).",
        wa_tier3="3) Posicionamiento + Display QR en Recepción: $16,000 -> $10,400 MXN (display físico en taller MTY en 2do momento).*",
        wa_extra_bullet="• Display acrílico discreto con código QR en mostrador diseñado para multiplicar reseñas de 5 estrellas.",
    ),
    "Colegios & Jardines de Niños": NicheProfile(
        niche_key="Colegios & Jardines de Niños",
        hero_path=NICHE_HEROES_DIR / "niche_kinder_montessori.jpg",
        after_tag="MAPS + CONFIANZA FAMILIAR",
        after_overlay_sub="Aulas luminosas y seguras · Docentes verificados · Botón informes WhatsApp",
        hero_intro=(
            "Cuando una familia busca jardín de niños en Monterrey, Google Maps es su primer filtro de seguridad y calidez. "
            "Proyectamos el cuidado real de tus aulas y maestras mientras blindamos tus canales oficiales."
        ),
        pillars=(
            (
                "Pilar 1 · Recorrido Visual Seguro y Aulas Cálidas",
                "Fotografía respetuosa y luminosa de instalaciones, áreas verdes, material didáctico y retratos directivos de confianza.",
            ),
            (
                "Pilar 2 · Perfil Verificado Google Maps Admisiones",
                "Reclamamos la ficha del plantel, quitamos el Street View frío y ordenamos horarios, fotos y WhatsApp de informes.",
            ),
            (
                "Pilar 3 · Meta Business Familiar + Galerías Privadas",
                "Unificamos FB + IG sin bloqueos y te habilitamos galerías con contraseña para festivales navideños o graduaciones.",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · IMPULSO GOOGLE MAPS ESCOLAR (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotos cálidas de aulas, patio seguro y fachada + verificación oficial y carga directa en Google Maps.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE ADMISIONES 2027 (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 institucionales + ficha Maps completa + Meta Business Portfolio sin bloqueos.",
        ),
        tier3=(
            "OPCIÓN 3 · PLANTEL + FESTIVAL / DISPLAY (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Admisiones Total + placa LED institucional con QR a reseñas/informes + cobertura opcional de festival decembrino.",
        ),
        wa_tier1="1) Impulso Google Maps Escolar: $6,000 -> $3,900 MXN (fotos cálidas de aulas y áreas seguras + carga directa en Maps).",
        wa_tier2="2) Suite Admisiones 2027: $10,600 -> $6,890 MXN (30–40 fotos + Reels 9:16 + Maps + Meta Business en regla para inscripciones).",
        wa_tier3="3) Plantel + Placa QR / Festival Fin de Año: $16,000 -> $10,400 MXN (piezas físicas y gala en 2do momento opcional).*",
        wa_extra_bullet="• Galerías privadas con clave de acceso pensadas para proteger a las familias en festivales y cierres de ciclo.",
    ),
    "Colegios Privados Élite": NicheProfile(
        niche_key="Colegios Privados Élite",
        hero_path=NICHE_HEROES_DIR / "niche_colegio_elite.jpg",
        after_tag="CAMPUS + DEPORTES + GALAS",
        after_overlay_sub="Editorial campus & equipos · Anuarios y copas · Galerías privadas",
        hero_intro=(
            "Las familias exigen excelencia en cada punto de contacto digital del colegio. "
            "Actualizamos la imagen institucional en Maps/Meta y cubrimos copas, ceremonias y deportes con entrega el mismo día."
        ),
        pillars=(
            (
                "Pilar 1 · Producción Institucional y Deportes a 1/2000s",
                "Campus, laboratorios, selecciones deportivas y ceremonias con nivel editorial + Reels 9:16 para admisiones.",
            ),
            (
                "Pilar 2 · Google Maps & Reputación de Campus",
                "Curamos hasta 40 fotografías institucionales actualizadas con enlace oficial al portal de admisiones.",
            ),
            (
                "Pilar 3 · Galerías Seguras + Reconocimientos LED",
                "Galería digital con acceso controlado para familias el mismo día y trofeos LED grabados para copas intercolegiales.",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · VITRINA GOOGLE MAPS CAMPUS (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotos arquitectónicas y deportivas de campus + curaduría y carga directa en ficha oficial de Google Maps.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE INSTITUCIONAL 2027 (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 para admisiones + Google Maps al 100% + Meta Business Portfolio institucional.",
        ),
        tier3=(
            "OPCIÓN 3 · CAMPUS + COBERTURA COPA & LED (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Institucional + cobertura deportiva/ceremonia con entrega el mismo día + reconocimientos LED en base de nogal.",
        ),
        wa_tier1="1) Vitrina Google Maps Campus: $6,000 -> $3,900 MXN (fotografía arquitectónica y de instalaciones + carga directa en Maps).",
        wa_tier2="2) Suite Institucional 2027: $10,600 -> $6,890 MXN (30–40 fotos + 2 Reels admisiones + Maps + Meta Business institucional).",
        wa_tier3="3) Campus + Cobertura Copa / Reconocimientos LED: $16,000 -> $10,400 MXN (acrílicos físicos en taller MTY 2do momento).*",
        wa_extra_bullet="• Entrega mismo día en copas intercolegiales y ceremonias mediante galería privada institucional con acceso protegido.",
    ),
    "Restaurantes & Cafés Boutique": NicheProfile(
        niche_key="Restaurantes & Cafés Boutique",
        hero_path=NICHE_HEROES_DIR / "niche_cafe_restaurante.jpg",
        after_tag="MAPS + ANTOJO + RESERVAS",
        after_overlay_sub="Editorial gastronómico · Menú verificado Maps · Meta Business",
        hero_intro=(
            "En gastronomía la decisión sucede en segundos al abrir el mapa y ver el plato o café de portada. "
            "Creamos imágenes editoriales que despiertan apetito real y optimizamos Maps + Instagram para llenar mesas."
        ),
        pillars=(
            (
                "Pilar 1 · Fotografía Gastronómica y Ambiente Boutique",
                "Platillos insignia, barra de espresso/mixología, salón con luz cálida y Reels 9:16 listos para antojo.",
            ),
            (
                "Pilar 2 · Ficha Google Maps con Menú y Reservas",
                "Actualizamos portada, 20–40 fotos calibradas, horarios de fin de semana y enlace directo a WhatsApp / menú.",
            ),
            (
                "Pilar 3 · Meta Business Portfolio & Display QR",
                "Blindamos tus cuentas de IG + FB + WhatsApp sin bloqueos y sumamos display LED QR en caja para reseñas.",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · IMPULSO GOOGLE MAPS GASTRO (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotos editoriales de platillos estrella, barra e interior + verificación y carga directa en Google Maps.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE RESTAURANTE TOTAL (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 de preparación/ambiente + Maps al 100% + Meta Business Portfolio sin bloqueos.",
        ),
        tier3=(
            "OPCIÓN 3 · GASTRO + DISPLAY LED QR MESA (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Restaurante Total + placa LED acrílica QR en barra/caja vinculada directo a reseñas 5★ y menú digital.",
        ),
        wa_tier1="1) Impulso Google Maps Gastro: $6,000 -> $3,900 MXN (15–20 fotos pro de platillos/ambiente + subida directa en Maps).",
        wa_tier2="2) Suite Restaurante Total: $10,600 -> $6,890 MXN (30–40 fotos + 2 Reels antojo 9:16 + Maps + Meta Business en regla).",
        wa_tier3="3) Gastro + Display LED QR en Barra: $16,000 -> $10,400 MXN (display físico en taller MTY en 2do momento opcional).*",
        wa_extra_bullet="• Placa LED discreta con QR en barra o caja para capturar reseñas mientras el comensal disfruta el café.",
    ),
    "Deporte de Alto Rendimiento": NicheProfile(
        niche_key="Deporte de Alto Rendimiento",
        hero_path=ROOT_DIR / "assets" / "hero-portrait.png",
        after_tag="MAPS + LIGAS 1/2000s + LED",
        after_overlay_sub="Cobertura liga mismo día · Ficha club verificada · Trofeos LED nogal",
        hero_intro=(
            "Tu complejo o liga merece verse al nivel de las finales que organiza. "
            "Actualizamos la vitrina digital del club en Google Maps y cubrimos jornadas, finales y premiación LED sin carga operativa."
        ),
        pillars=(
            (
                "Pilar 1 · Cobertura Deportiva a 1/2000s + Instalaciones",
                "Acción limpia de jugadores y equipos, canchas nocturnas y Reels 9:16 entregados el mismo día de partido.",
            ),
            (
                "Pilar 2 · Ficha Google Maps Verificada del Club",
                "Reclamamos la sede, quitamos fotos desactualizadas y activamos enlaces directos a inscripciones y torneos.",
            ),
            (
                "Pilar 3 · Meta Business + Premiación Acrílico LED",
                "Ordenamos FB + IG + WhatsApp y fabricamos trofeos de acrílico LED grabados sobre nogal (pago físico diferible).",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · IMPULSO GOOGLE MAPS DEPORTIVO (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotos de instalaciones, canchas y acción deportiva + carga y verificación directa en Google Maps.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE DEPORTIVA TOTAL (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 + Google Maps al 100% + Meta Business Portfolio (FB + IG + WhatsApp sin bloqueos).",
        ),
        tier3=(
            "OPCIÓN 3 · SEDE + TORNEO & LED QR (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Deportiva + cobertura de jornada/final mismo día + trofeos/placas acrílicas LED financiables con patrocinadores.",
        ),
        wa_tier1="1) Impulso Google Maps Deportivo: $6,000 -> $3,900 MXN (sesión pro de canchas/equipos + carga directa en Maps).",
        wa_tier2="2) Suite Deportiva Total: $10,600 -> $6,890 MXN (30–40 fotos + Reels 1/2000s + Maps + Meta Business en regla).",
        wa_tier3="3) Sede + Finales & Acrílicos LED QR: $16,000 -> $10,400 MXN (elementos físicos en taller MTY en 2do momento).*",
        wa_extra_bullet="• Opción Halftime Blitz con galerías el mismo día y trofeos LED patrocinables sin presión presupuestal.",
    ),
    "Hoteles, Resorts & Beach Clubs": NicheProfile(
        niche_key="Hoteles, Resorts & Beach Clubs",
        hero_path=NICHE_HEROES_DIR / "niche_comercio_boutique.jpg",
        after_tag="MAPS + HOSPITALIDAD EDITORIAL",
        after_overlay_sub="Arquitectura, alberca y habitaciones · Reserva directa · Meta Business",
        hero_intro=(
            "Un huésped decide dónde reservar en los primeros segundos al abrir Google Maps y comparar fotografías reales. "
            "Elevamos tu vitrina visual con técnica editorial de hospitalidad y dejamos tu ficha y Meta Business listos para reserva directa."
        ),
        pillars=(
            (
                "Pilar 1 · Fotografía Editorial de Hospitalidad & Amenidades",
                "Habitaciones, albercas, beach club, fachada al atardecer y Reels 9:16 con luz calibrada que proyectan el nivel real de tu propiedad.",
            ),
            (
                "Pilar 2 · Ficha Google Maps Optimizada para Reserva Directa",
                "Reclamamos tu perfil, reemplazamos vistas Street View, subimos 20–40 fotos curadas y enlazamos directo a motor de reservas/WhatsApp.",
            ),
            (
                "Pilar 3 · Meta Business Portfolio & Display QR en Lobby",
                "Unificamos Facebook, Instagram y WhatsApp Business sin riesgo de bloqueos e integramos placas LED QR discretas para reseñas 5★.",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · IMPULSO GOOGLE MAPS HOSPITALIDAD (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotos editoriales de fachada, lobby, alberca/terraza y habitaciones clave + carga directa en Google Maps.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE PROPIEDAD TOTAL (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 de experiencia y amenidades + Google Maps al 100% + Meta Business Portfolio sin bloqueos.",
        ),
        tier3=(
            "OPCIÓN 3 · RESORT / BEACH CLUB + DISPLAY QR (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Propiedad Total + placas acrílicas LED en nogal con QR a reseñas y concierge/menú digital (taller artesanal 3–5 días).",
        ),
        wa_tier1="1) Impulso Google Maps Hospitalidad: $6,000 -> $3,900 MXN (15–20 fotos editoriales de propiedad y carga directa en Maps).",
        wa_tier2="2) Suite Propiedad Total: $10,600 -> $6,890 MXN (30–40 fotos + 2 Reels 9:16 + Maps + Meta Business sin bloqueos).",
        wa_tier3="3) Propiedad + Placa LED QR Concierge/Reseñas: $16,000 -> $10,400 MXN (pieza artesanal diferible a un 2do momento).*",
        wa_extra_bullet="• Enfoque técnico en arquitectura, luz natural costera y colorimetría fiel para convertir búsquedas en reservas directas.",
    ),
    "Tiendas, Boutiques & Comercios": NicheProfile(
        niche_key="Tiendas, Boutiques & Comercios",
        hero_path=NICHE_HEROES_DIR / "niche_comercio_boutique.jpg",
        after_tag="MAPS + VITRINA BOUTIQUE",
        after_overlay_sub="Escaparate editorial · Catálogo WhatsApp · Meta Business en regla",
        hero_intro=(
            "El estilo de tu tienda y la curaduría de tus productos merecen destacarse desde el primer clic en Google Maps. "
            "Producimos tu vitrina visual con iluminación editorial y ordenamos tu Meta Business Portfolio para vender por catálogo y WhatsApp."
        ),
        pillars=(
            (
                "Pilar 1 · Producción Editorial de Tienda, Productos y Equipo",
                "Escaparate limpio, interior con luz cuidada, lookbook o productos estrella y Reels 9:16 listos para atraer visitantes.",
            ),
            (
                "Pilar 2 · Google Maps Verificado para Tráfico a Tienda",
                "Reclamamos tu ubicación, quitamos el Street View frío, actualizamos horarios turísticos y activamos enlace directo a WhatsApp.",
            ),
            (
                "Pilar 3 · Meta Business Portfolio & QR de Mostrador",
                "Conectamos Instagram Shopping/Catálogo, Facebook y WhatsApp Business sin bloqueos y sumamos display QR LED en caja.",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · IMPULSO GOOGLE MAPS BOUTIQUE (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotos pro de escaparate, interior y productos clave + verificación oficial y carga directa en Google Maps.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE COMERCIO TOTAL (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 de producto/espacio + Google Maps al 100% + Meta Business Portfolio sin bloqueos.",
        ),
        tier3=(
            "OPCIÓN 3 · COMERCIO + DISPLAY LED QR CAJA (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Comercio Total + placa acrílica LED en nogal con QR directo a reseñas 5★ y catálogo (taller artesanal 3–5 días).",
        ),
        wa_tier1="1) Impulso Google Maps Boutique: $6,000 -> $3,900 MXN (15–20 fotos pro de tienda y producto + carga directa en Maps).",
        wa_tier2="2) Suite Comercio Total: $10,600 -> $6,890 MXN (30–40 fotos + 2 Reels + Maps al 100% + Meta Business sin bloqueos).",
        wa_tier3="3) Comercio + Display LED QR en Caja: $16,000 -> $10,400 MXN (pieza física artesanal diferible a un 2do momento).*",
        wa_extra_bullet="• Display QR discreto en mostrador para convertir compradores presenciales en reseñas verificadas de 5★.",
    ),
    "Small Business & Comercios": NicheProfile(
        niche_key="Small Business & Comercios",
        hero_path=NICHE_HEROES_DIR / "niche_comercio_boutique.jpg",
        after_tag="MAPS + META BUSINESS",
        after_overlay_sub="Vitrina boutique curada · Enlace directo WhatsApp · Cero bloqueos",
        hero_intro=(
            "La calidad real de tu espacio y atención merece reflejarse desde el primer clic en Google Maps. "
            "Hacemos la producción editorial en tu local y dejamos tu ficha y Meta Business Portfolio listos para vender en 2027."
        ),
        pillars=(
            (
                "Pilar 1 · Producción Editorial de Local & Equipo",
                "Fachada limpia, interiores con iluminación cuidada, productos clave, retratos de equipo y Reels 9:16.",
            ),
            (
                "Pilar 2 · Carga Directa y Verificación Google Maps",
                "Reclamamos tu ficha, subimos portada pro + 20–40 fotos curadas, horarios y botón directo a WhatsApp.",
            ),
            (
                "Pilar 3 · Meta Business Portfolio Cero Bloqueos",
                "Unificamos Facebook, Instagram Profesional y WhatsApp Business en regla para operar pautas y catálogo 2027.",
            ),
        ),
        tier1=(
            "OPCIÓN 1 · IMPULSO GOOGLE MAPS (-35%)",
            "$6,000",
            "$3,900 MXN",
            "15–20 fotos pro de fachada, interior y equipo + verificación oficial y subida directa a tu perfil de Google Maps.",
        ),
        tier2=(
            "OPCIÓN 2 · SUITE SMALL BUSINESS TOTAL (-35%)",
            "$10,600",
            "$6,890 MXN",
            "30–40 fotos + 2 Reels 9:16 + Google Maps al 100% + Meta Business Portfolio (FB + IG + WhatsApp sin bloqueos).",
        ),
        tier3=(
            "OPCIÓN 3 · POSICIONAMIENTO + DISPLAY LED QR (-35%)",
            "$16,000",
            "$10,400 MXN",
            "Suite Total + placa acrílica LED en nogal con código QR directo a reseñas/catálogo (fabricación diferible en taller artesanal).",
        ),
        wa_tier1="1) Impulso Google Maps 2027: $6,000 -> $3,900 MXN (15–20 fotos pro de local y equipo + carga directa en Maps).",
        wa_tier2="2) Suite Small Business Total: $10,600 -> $6,890 MXN (30–40 fotos + 2 Reels + Maps al 100% + Meta Business sin bloqueos).",
        wa_tier3="3) Posicionamiento + Display LED QR: $16,000 -> $10,400 MXN (pieza física artesanal liquidable en 2do momento).*",
        wa_extra_bullet="• Placa acrílica LED con QR de mostrador para convertir clientes presenciales en reseñas verificadas de 5★.",
    ),
}


def resolve_niche_profile(niche: str | None = None, *, name: str = "", category: str = "") -> NicheProfile:
    """Resolve the matching NicheProfile deterministically without generic cross-niche leakage."""
    if niche and niche in NICHE_PROFILES and niche != "Small Business & Comercios":
        return NICHE_PROFILES[niche]
    joined = f"{niche or ''} {name} {category}".lower()
    cat_low = (category or "").lower()
    if any(w in joined for w in ("padel", "pádel", "tenis", "raqueta", "playtomic")):
        return NICHE_PROFILES["Pádel & Raqueta"]
    if any(w in joined for w in ("hotel", "resort", "beach club", "hostal", "hospedaje", "alojamiento", "suites", "villa", "complejo hotelero")):
        return NICHE_PROFILES["Hoteles, Resorts & Beach Clubs"]
    if any(w in joined for w in ("fitness", "crossfit", "hyrox", "gym", "gimnasio", "pilates", "totalpass", "body x", "vacu", "core", "yoga", "centro deportivo")):
        return NICHE_PROFILES["Fitness & CrossFit"]
    if any(w in joined for w in ("danza", "dance", "baile", "ballet", "salsa", "bachata")) and "yoga" not in (name or "").lower():
        return NICHE_PROFILES["Baile & Danza Señoras"]
    if any(w in joined for w in ("dental", "dentist", "clínic", "clinic", "médic", "medic", "consultor", "fisioter", "dermat", "nutri", "spa", "estétic", "estetic", "masaj", "wellness")):
        return NICHE_PROFILES["Clínicas & Consultorios"]
    if any(w in joined for w in ("kinder", "jardín", "jardin", "guarder", "preescolar", "reino encantado")):
        return NICHE_PROFILES["Colegios & Jardines de Niños"]
    if any(w in joined for w in ("liceo", "asfm", "san roberto", "mater", "brillamont", "labastida", "prepatec", "udem", "irish", "franco mexicano", "colegios privados")):
        return NICHE_PROFILES["Colegios Privados Élite"]
    if any(w in joined for w in ("café", "cafe", "coffee", "restauran", "brunch", "bistro", "panader", "bakery", "bar ", "cocktail", "coctel", "cervecer", "cantina", "mariscos", "tacos")):
        return NICHE_PROFILES["Restaurantes & Cafés Boutique"]
    if any(w in joined for w in ("deportiv", "alto rendimiento", "colinas", "deportivo san agustin", "deportivo san agustín", "tym", "sierra madre")):
        return NICHE_PROFILES["Deporte de Alto Rendimiento"]
    if any(w in joined for w in ("tienda", "boutique", "ropa", "recuerdo", "souvenir", "artesan", "conveniencia", "abarrotes", "minimarket", "licor", "joyer", "regalo", "zapater", "galer", "mercado")) or "mercado" in cat_low:
        return NICHE_PROFILES["Tiendas, Boutiques & Comercios"]
    return NICHE_PROFILES["Small Business & Comercios"]


def resolve_club_logo_path(name: str, explicit_logo: str | None = None) -> Path | None:
    """Find an authentic club/prospect logo file from explicit metadata or assets/club_logos/."""
    if explicit_logo:
        cand = (ROOT_DIR / explicit_logo) if not Path(explicit_logo).is_absolute() else Path(explicit_logo)
        if cand.exists() and cand.is_file():
            return cand
    if not CLUB_LOGOS_DIR.exists():
        return None
    slug = slugify(name)
    for ext in ("png", "svg", "jpg", "jpeg", "webp"):
        cand = CLUB_LOGOS_DIR / f"{slug}.{ext}"
        if cand.exists():
            return cand
    low = (name or "").strip().lower()
    keyword_map = {
        "cuatro padel": "cuatro_padel.svg",
        "padel gm": "padel_gm.png",
        "padel camp": "padel_camp.svg",
        "club sierra madre": "club_sierra_madre.png",
        "sb padel": "sb_padel.svg",
        "sb pádel": "sb_padel.svg",
        "tennis center": "tennis_center.jpg",
        "deportivo san agustin": "deportivo_san_agustin.png",
        "deportivo san agustín": "deportivo_san_agustin.png",
        "the movement": "the_movement.png",
        "danz studio": "danz_studio.png",
        "club deportivo colinas": "deportivo_colinas.png",
        "american gym": "american_gym.svg",
        "11:11": "eleven_fitness.png",
    }
    if low == "padelboss":
        cand = CLUB_LOGOS_DIR / "padelboss.svg"
        if cand.exists():
            return cand
    for kw, fname in keyword_map.items():
        if kw in low:
            cand = CLUB_LOGOS_DIR / fname
            if cand.exists():
                return cand
    return None


@dataclass(frozen=True)
class SmallBusinessSpec:
    """Client-safe configuration for Captoora Small Business 2027 visual Maps/Meta audit."""

    business_name: str
    category_label: str = "Negocio Local · MTY / SPGG"
    city_label: str = "SAN JERÓNIMO · SAN PEDRO · MTY"
    maps_screenshot_path: Path | None = None
    after_hero_path: Path = NICHE_HEROES_DIR / "niche_comercio_boutique.jpg"
    rating_label: str = "4.8 ★ en Google Maps"
    observations: tuple[str, ...] = (
        "Tu portada actual en Google Maps puede transmitir mayor solidez mostrando fachada y equipo profesional.",
        "La ficha tiene oportunidad de verificación oficial, enlace a sitio/catálogo y WhatsApp directo.",
        "Integrar Facebook, Instagram y WhatsApp en un Meta Business Portfolio formal evita bloqueos al vender en 2027.",
    )
    niche_label: str = ""
    after_tag: str = ""
    after_overlay_sub: str = ""
    hero_intro: str = ""
    pillars: tuple[tuple[str, str], ...] = ()
    tier_cards: tuple[tuple[str, str, str, str], ...] = ()
    prospect_logo_path: Path | None = None
    discount_pct: int = 35
    season_tag: str = "ARRANCA 2027 · -35% TEMPORADA"
    director_name: str = "Jesús Gutiérrez"
    director_role: str = "FOTÓGRAFO Y DIRECTOR · CAPTOORA SMALL BUSINESS"
    email_address: str = "chuy@captoora.studio"
    website_url: str = "https://captoora.studio/sports"
    gallery_url: str = "https://galeria.captoora.studio"
    instagram_handle: str = "@captoora.studio"
    address_line: str = "Av. Paseo de los Álamos 165, Colinas de San Jerónimo, Monterrey, N.L."
    whatsapp_display: str = "+52 81 4005 0088"
    whatsapp_url: str = "https://wa.me/528140050088"
    sla_footer_note: str = (
        "*Entrega digital en 48–72h (mismo día en eventos) · "
        "Placa acrílica LED en taller MTY/SPGG: 3–5 días hábiles · -35% vigente Fin de Año 2026."
    )


def _is_non_nl_territory(municipio: str) -> bool:
    low = (municipio or "").strip().lower()
    return bool(low) and low not in {"monterrey", "san pedro garza garcía", "san pedro garza garcia", "santa catarina", "san pedro"}


def _neutralize_origin_text(text: str) -> str:
    """Strip Nuevo León / Monterrey origin phrasing for external territories."""
    return (
        text.replace("en taller MTY/SPGG", "en taller artesanal")
        .replace("taller MTY/SPGG", "taller artesanal")
        .replace("en taller MTY", "en taller artesanal")
        .replace("taller local MTY/SPGG", "taller artesanal")
        .replace("en Monterrey", "en tu ciudad")
    )


def build_small_business_spec_from_record(
    record: dict[str, Any],
    *,
    hero_override: Literal["auto", "sports", "studio"] = "auto",
    screenshot_override: Path | None = None,
) -> SmallBusinessSpec:
    """Build a fully personalized SmallBusinessSpec from a gmaps_audits / leads record."""
    name = str(record.get("nombre") or record.get("slug") or "Negocio Local").strip()
    niche = str(record.get("nicho") or "").strip()
    category = str(record.get("categoria") or "Negocio Local").strip()
    profile = resolve_niche_profile(niche, name=name, category=category)

    if hero_override == "sports":
        after_hero = PADEL_ACTION_PATH
    elif hero_override == "studio":
        after_hero = profile.hero_path if profile.hero_path.exists() else (ROOT_DIR / "assets" / "hero-portrait.png")
    else:
        after_hero = profile.hero_path if profile.hero_path.exists() else PADEL_ACTION_PATH

    shot_abs = screenshot_override
    if shot_abs is None:
        shot_rel = str(record.get("screenshot_path") or record.get("gmaps_screenshot") or "").strip()
        if shot_rel:
            cand = ROOT_DIR / shot_rel
            if cand.exists():
                shot_abs = cand
        if shot_abs is None:
            slug = str(record.get("slug") or slugify(name))
            cand = ROOT_DIR / "assets" / "gmaps_audits" / f"{slug}.png"
            if cand.exists() and cand.stat().st_size > 10_000:
                shot_abs = cand

    rating_val = record.get("rating")
    resenas_val = int(record.get("resenas") or 0)
    flags = [str(f) for f in (record.get("audit_flags") or [])]
    if rating_val is not None:
        rating_label = f"{rating_val} ★ ({resenas_val} reseñas) · Google Maps"
    elif flags:
        rating_label = f"Google Maps · {', '.join(flags[:2])}"
    else:
        rating_label = f"Google Maps · {profile.niche_key}"

    raw_obs = [str(o).strip() for o in (record.get("client_observations") or ()) if str(o).strip()]
    if not raw_obs:
        raw_obs = [
            f"Oportunidad directa para destacar {name} en {profile.niche_key} frente a competidores locales.",
            "Optimización de portada editorial en Google Maps + enlace directo a citas/informes por WhatsApp.",
            "Consolidación de Facebook, Instagram y WhatsApp en Meta Business Portfolio oficial para 2027.",
        ]

    municipio = str(record.get("municipio") or "Monterrey").strip()
    zona = str(record.get("zona") or "").strip()
    logo_abs = resolve_club_logo_path(name, record.get("logo"))
    external_territory = _is_non_nl_territory(municipio)

    hero_intro = _neutralize_origin_text(profile.hero_intro) if external_territory else profile.hero_intro
    tier_cards = (
        tuple(tuple(_neutralize_origin_text(part) for part in card) for card in (profile.tier1, profile.tier2, profile.tier3))  # type: ignore[arg-type]
        if external_territory
        else (profile.tier1, profile.tier2, profile.tier3)
    )
    address_line = (
        "Portafolio Editorial & Estrategia Google Maps · https://captoora.studio/sports"
        if external_territory
        else SmallBusinessSpec.address_line
    )
    sla_footer = (
        "*Entrega digital en 48–72h (mismo día en eventos) · Pieza acrílica LED en taller artesanal: 3–5 días hábiles · -35% vigente."
        if external_territory
        else SmallBusinessSpec.sla_footer_note
    )

    return SmallBusinessSpec(
        business_name=name,
        category_label=f"{category} · {municipio}",
        city_label=_format_city_label(zona, municipio),
        maps_screenshot_path=shot_abs,
        after_hero_path=after_hero,
        rating_label=rating_label,
        observations=tuple(raw_obs[:3]),
        niche_label=profile.niche_key,
        after_tag=profile.after_tag,
        after_overlay_sub=profile.after_overlay_sub,
        hero_intro=hero_intro,
        pillars=profile.pillars,
        tier_cards=tier_cards,
        prospect_logo_path=logo_abs,
        address_line=address_line,
        sla_footer_note=sla_footer,
    )


def _format_city_label(zona: str, municipio: str) -> str:
    z = zona.strip()
    m = municipio.strip() or "Monterrey"
    if not z or z.lower() in m.lower():
        return m.upper()
    return f"{z.upper()} · {m.upper()}"


def validate_smb_spec(spec: SmallBusinessSpec) -> None:
    """Ensure all Captoora Small Business visuals maintain zero AI mentions and respectful tone."""
    pillar_texts = [t for p in spec.pillars for t in p]
    tier_texts = [t for c in spec.tier_cards for t in c]
    combined = " | ".join(
        [
            spec.business_name,
            spec.category_label,
            spec.city_label,
            spec.season_tag,
            spec.director_name,
            spec.director_role,
            spec.hero_intro,
            spec.after_tag,
            spec.after_overlay_sub,
            *spec.observations,
            *pillar_texts,
            *tier_texts,
        ]
    )
    violations = validate_client_copy(combined)
    if violations:
        raise ValueError(f"SmallBusinessSpec contiene términos prohibidos: {'; '.join(violations)}")


def _file_data_uri(path: Path) -> str:
    """Encode an existing local image asset as a base64 data URI for deterministic rendering."""
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el asset visual requerido: {path}")
    suffix = path.suffix.lower().lstrip(".")
    if suffix in {"jpg", "jpeg"}:
        mime = "image/jpeg"
    elif suffix == "svg":
        mime = "image/svg+xml"
    else:
        mime = f"image/{suffix}"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _run_chrome(args: list[str]) -> None:
    """Invoke local Google Chrome headless cleanly without sandbox hacks."""
    if not CHROME_BIN.exists():
        raise FileNotFoundError(f"No se encontró Google Chrome en {CHROME_BIN}")
    cmd = [
        str(CHROME_BIN),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        *args,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=45, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"Chrome Headless falló ({proc.returncode}): {proc.stderr.strip()}")


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


def _plate_club_logo_html(spec: MockupSpec, logo_uri: str, *, compact: bool = False) -> str:
    """Return crystal-etched mark HTML using either the club's own logo or Captoora emblem."""
    if spec.club_logo_path and spec.club_logo_path.exists():
        club_uri = _file_data_uri(spec.club_logo_path)
        ext = spec.club_logo_path.suffix.lower()
        cls = "engraved-club-logo-badge" if ext in {".jpg", ".jpeg"} else "engraved-club-logo"
        if compact:
            cls += " compact"
        return f'<img class="{cls}" src="{club_uri}" alt="{_esc(spec.club_name)}" />'
    return f'<div class="engraved-mark" style="-webkit-mask-image:url(\'{logo_uri}\'); mask-image:url(\'{logo_uri}\');"></div>'


def _shared_plate_variant_css() -> str:
    """Shared CSS for club logos engraved in crystal and dance trophy geometry."""
    return """
  .engraved-club-logo {
    max-width: 118px;
    max-height: 48px;
    width: auto;
    height: auto;
    object-fit: contain;
    filter: brightness(0) invert(1) drop-shadow(0 0 8px rgba(255, 224, 158, 0.72));
    opacity: 0.92;
    margin-bottom: 2px;
  }
  .engraved-club-logo.compact {
    max-width: 92px;
    max-height: 36px;
  }
  .engraved-club-logo-badge {
    max-width: 96px;
    max-height: 44px;
    object-fit: contain;
    border-radius: 6px;
    padding: 3px 6px;
    background: rgba(255, 250, 240, 0.88);
    box-shadow: 0 0 12px rgba(255, 224, 158, 0.45);
    margin-bottom: 2px;
  }
  .engraved-club-logo-badge.compact {
    max-width: 76px;
    max-height: 34px;
  }
  .acrylic-plate.plate-dance {
    left: 30.8%;
    top: 26.2%;
    width: 37.8%;
    height: 42.8%;
    transform: perspective(900px) rotateY(-10deg) skewY(2.2deg) rotateZ(0.2deg);
  }
  .wood-engraving.plate-dance {
    left: 23.5%;
    top: 76.2%;
    width: 49%;
    transform-origin: center center;
    transform: perspective(900px) rotateY(-10deg) skewY(1.8deg);
  }
    """


def _build_engraved_plate_html(
    spec: MockupSpec,
    logo_uri: str,
    *,
    compact: bool = False,
) -> str:
    """Return HTML markup for warm frosted LED laser engraving centered inside the crystal pane."""
    scale_cls = "plate-compact" if compact else "plate-full"
    style_cls = "plate-dance" if spec.plate_style == "dance" else "plate-padel"
    mark_html = _plate_club_logo_html(spec, logo_uri, compact=compact)
    return f"""
    <div class="acrylic-plate {scale_cls} {style_cls}">
      <div class="plate-glow-floor"></div>
      <div class="plate-content">
        {mark_html}
        <div class="engraved-kicker">{_esc(spec.category_label.upper())}</div>
        <div class="engraved-club">{_esc(spec.club_name.upper())}</div>
        <div class="engraved-rule"></div>
        <div class="engraved-tournament">{_esc(spec.tournament_name.upper())}</div>
        <div class="engraved-year-pill">{_esc(spec.season_label.upper())}</div>
        <div class="engraved-sponsor-box">
          <span class="sponsor-caption">PATROCINADO POR</span>
          <span class="sponsor-slot">{_esc(spec.sponsor_label.upper())}</span>
        </div>
      </div>
    </div>
    """


def _build_option_a_html(spec: MockupSpec) -> str:
    """Opción A: Minimalista Luxury 4:5 portrait — crystal LED acrylic hero with subtle framing."""
    acrylic_uri = _file_data_uri(spec.acrylic_base_path or ACRYLIC_BLANK_PATH)
    logo_uri = _file_data_uri(CAPTOORA_LOGO_PATH)
    plate_html = _build_engraved_plate_html(spec, logo_uri, compact=False)
    style_cls = "plate-dance" if spec.plate_style == "dance" else "plate-padel"

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1080px;
    height: 1350px;
    overflow: hidden;
    background: #07080b;
    font-family: 'Avenir Next', 'Montserrat', 'Helvetica Neue', sans-serif;
    color: #f5efe6;
  }}
  .canvas {{
    position: relative;
    width: 1080px;
    height: 1350px;
    overflow: hidden;
    background: #07080b;
  }}
  /* Lock 896x1200 base proportions -> 1080x1446 centered slightly high so bottom vignette holds clean legal copy */
  .scene-frame {{
    position: absolute;
    left: 0;
    top: -42px;
    width: 1080px;
    height: 1446px;
  }}
  .scene-photo {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: contrast(1.04) brightness(0.98);
  }}
  .top-vignette {{
    position: absolute;
    inset: 0 0 auto 0;
    height: 220px;
    background: linear-gradient(180deg, rgba(6,7,10,0.88) 0%, rgba(6,7,10,0.38) 55%, rgba(6,7,10,0) 100%);
    pointer-events: none;
  }}
  .bottom-vignette {{
    position: absolute;
    inset: auto 0 0 0;
    height: 230px;
    background: linear-gradient(0deg, rgba(6,7,10,0.95) 0%, rgba(6,7,10,0.62) 55%, rgba(6,7,10,0) 100%);
    pointer-events: none;
  }}
  /* Exact 3D plane aligned inside the glass pane of padel_acrylic_blank.jpg */
  .acrylic-plate {{
    position: absolute;
    left: 35.1%;
    top: 31.2%;
    width: 31.2%;
    height: 38.8%;
    transform-origin: center center;
    transform: perspective(900px) rotateY(15deg) skewY(-3.8deg) rotateZ(-0.4deg);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px 16px 26px;
    overflow: hidden;
  }}
  .plate-glow-floor {{
    position: absolute;
    left: 8%;
    right: 8%;
    bottom: -14px;
    height: 44%;
    background: radial-gradient(ellipse at 50% 100%, rgba(255, 224, 158, 0.34) 0%, rgba(214, 178, 114, 0.08) 58%, transparent 80%);
    pointer-events: none;
  }}
  .plate-content {{
    position: relative;
    z-index: 2;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 10px;
  }}
  .engraved-mark {{
    width: 52px;
    height: 52px;
    background: linear-gradient(180deg, rgba(255,250,238,0.92) 0%, rgba(240,206,142,0.88) 100%);
    -webkit-mask-size: contain;
    mask-size: contain;
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    -webkit-mask-position: center;
    mask-position: center;
    filter: drop-shadow(0 0 8px rgba(255, 220, 148, 0.65));
    margin-bottom: 2px;
  }}
  .engraved-kicker {{
    font-size: 11px;
    letter-spacing: 0.28em;
    font-weight: 600;
    color: rgba(248, 229, 190, 0.88);
    text-shadow: 0 0 8px rgba(245, 206, 130, 0.55);
  }}
  .engraved-club {{
    font-family: 'Didot', 'Bodoni 72', 'Georgia', serif;
    font-size: 32px;
    line-height: 1.02;
    letter-spacing: 0.08em;
    font-weight: 700;
    color: rgba(255, 250, 240, 0.96);
    text-shadow: 0 0 14px rgba(255, 224, 158, 0.65), 0 0 2px rgba(255,255,255,0.85);
  }}
  .engraved-rule {{
    width: 72%;
    height: 1.5px;
    background: linear-gradient(90deg, transparent, rgba(255, 229, 175, 0.92), transparent);
    box-shadow: 0 0 6px rgba(255, 220, 150, 0.6);
  }}
  .engraved-tournament {{
    font-size: 15px;
    letter-spacing: 0.16em;
    font-weight: 600;
    color: rgba(255, 245, 224, 0.94);
    text-shadow: 0 0 10px rgba(255, 220, 145, 0.5);
  }}
  .engraved-year-pill {{
    margin-top: 2px;
    padding: 7px 18px;
    border-radius: 999px;
    border: 1.5px solid rgba(255, 228, 172, 0.85);
    background: linear-gradient(180deg, rgba(255, 232, 182, 0.16), rgba(214, 172, 100, 0.08));
    font-size: 15px;
    letter-spacing: 0.22em;
    font-weight: 700;
    color: #fff6e0;
    text-shadow: 0 0 12px rgba(255, 224, 154, 0.8);
    box-shadow: 0 0 16px rgba(246, 206, 130, 0.28), inset 0 0 10px rgba(255, 245, 215, 0.18);
  }}
  .engraved-sponsor-box {{
    margin-top: 16px;
    width: 84%;
    padding: 9px 10px;
    border: 1px dashed rgba(255, 228, 176, 0.62);
    border-radius: 6px;
    background: rgba(255, 242, 212, 0.05);
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}
  .sponsor-caption {{
    font-size: 9px;
    letter-spacing: 0.22em;
    color: rgba(248, 225, 178, 0.78);
  }}
  .sponsor-slot {{
    font-size: 11px;
    letter-spacing: 0.12em;
    font-weight: 600;
    color: rgba(255, 247, 230, 0.92);
    text-shadow: 0 0 8px rgba(255, 220, 150, 0.45);
  }}
  /* Walnut base dark burn stamp */
  .wood-engraving {{
    position: absolute;
    left: 36.2%;
    top: 76.2%;
    width: 37.5%;
    transform-origin: left center;
    transform: perspective(900px) rotateY(15deg) skewY(-4.6deg);
    text-align: center;
    font-size: 12px;
    letter-spacing: 0.34em;
    font-weight: 600;
    color: rgba(240, 208, 156, 0.62);
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.88), 0 0 6px rgba(236, 194, 128, 0.16);
    pointer-events: none;
  }}
  {_shared_plate_variant_css()}
  .header-overlay {{
    position: absolute;
    top: 38px;
    left: 48px;
    right: 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }}
  .header-brand {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .header-logo {{
    width: 34px;
    height: 34px;
    background: #e5c997;
    -webkit-mask-size: contain;
    mask-size: contain;
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
  }}
  .header-title {{
    font-family: 'Didot', 'Bodoni 72', serif;
    font-size: 20px;
    letter-spacing: 0.22em;
    color: #f5efe6;
  }}
  .header-sub {{
    font-size: 10px;
    letter-spacing: 0.24em;
    color: #d4b483;
    margin-top: 2px;
  }}
  .option-pill {{
    padding: 8px 16px;
    border: 1px solid rgba(212, 180, 131, 0.55);
    background: rgba(12, 13, 18, 0.72);
    border-radius: 999px;
    font-size: 11px;
    letter-spacing: 0.18em;
    color: #ebd3aa;
    font-weight: 600;
  }}
  .header-volt-rule {{
    position: absolute;
    top: 94px;
    left: 48px;
    right: 48px;
    height: 2px;
    background: linear-gradient(90deg, #c6ff00 0%, rgba(198, 255, 0, 0.35) 55%, rgba(212, 180, 131, 0.12) 100%);
    z-index: 10;
  }}
  .footer-overlay {{
    position: absolute;
    bottom: 34px;
    left: 48px;
    right: 48px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .footer-main {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-top: 1px solid rgba(212, 180, 131, 0.28);
    padding-top: 16px;
  }}
  .footer-left-kicker {{
    font-size: 11px;
    letter-spacing: 0.22em;
    color: #d4b483;
    font-weight: 600;
  }}
  .footer-left-title {{
    font-family: 'Didot', 'Bodoni 72', serif;
    font-size: 26px;
    color: #f5efe6;
    margin-top: 4px;
  }}
  .footer-right {{
    text-align: right;
    font-size: 11.5px;
    letter-spacing: 0.12em;
    color: #d6d0c4;
  }}
  .footer-sla {{
    font-size: 10.5px;
    letter-spacing: 0.08em;
    color: rgba(214, 208, 196, 0.72);
  }}
</style>
</head>
<body>
  <div class="canvas">
    <div class="scene-frame">
      <img class="scene-photo" src="{acrylic_uri}" alt="Acrílico LED Captoora" />
      {plate_html}
      <div class="wood-engraving {style_cls}">CAPTOORA · {_esc(spec.year)}</div>
    </div>

    <div class="top-vignette"></div>
    <div class="bottom-vignette"></div>

    <div class="header-overlay">
      <div class="header-brand">
        <div class="header-logo" style="-webkit-mask-image:url('{logo_uri}'); mask-image:url('{logo_uri}');"></div>
        <div>
          <div class="header-title">CAPTOORA STUDIO</div>
          <div class="header-sub">{_esc(spec.instagram_handle.upper())} · {_esc(spec.city_label)}</div>
        </div>
      </div>
      <div class="option-pill">OPCIÓN A · ACRÍLICO LED {_esc(spec.year)}</div>
    </div>
    <div class="header-volt-rule"></div>

    <div class="footer-overlay">
      <div class="footer-main">
        <div>
          <div class="footer-left-kicker">MOCKUP PERSONALIZADO PARA {_esc(spec.club_name.upper())}</div>
          <div class="footer-left-title">{_esc(spec.club_name)} · {_esc(spec.season_label)}</div>
        </div>
        <div class="footer-right">
          <div>{_esc(spec.website_url.replace('https://', ''))} · {_esc(spec.gallery_url.replace('https://', ''))}</div>
          <div style="color:#c6ff00; margin-top:3px; font-weight:600;">WA {_esc(spec.whatsapp_display)}</div>
        </div>
      </div>
      <div class="footer-sla">
        *Cobertura fotográfica y reels el mismo día del evento · Manufactura de acrílico LED en taller local MTY/SPGG: 3–5 días hábiles.
      </div>
    </div>
  </div>
</body>
</html>"""


def _build_option_b_html(spec: MockupSpec) -> str:
    """Opción B: Editorial Split 1/2000s Action Hero + Illuminated Crystal Trophy Navidad 2026."""
    action_uri = _file_data_uri(spec.hero_photo_path or PADEL_ACTION_PATH)
    acrylic_uri = _file_data_uri(spec.acrylic_base_path or ACRYLIC_BLANK_PATH)
    logo_uri = _file_data_uri(CAPTOORA_LOGO_PATH)
    plate_html = _build_engraved_plate_html(spec, logo_uri, compact=True)
    style_cls = "plate-dance" if spec.plate_style == "dance" else "plate-padel"
    hero_obj_pos = "60% 24%" if spec.plate_style == "dance" else "66% 36%"

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1080px;
    height: 1350px;
    overflow: hidden;
    background: #07080b;
    font-family: 'Avenir Next', 'Montserrat', 'Helvetica Neue', sans-serif;
    color: #f5efe6;
  }}
  .canvas {{
    width: 1080px;
    height: 1350px;
    display: flex;
    flex-direction: column;
    background: #07080b;
  }}
  .top-hero {{
    position: relative;
    width: 1080px;
    height: 676px;
    overflow: hidden;
    background: #06070a;
  }}
  .action-img {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: {hero_obj_pos};
    filter: contrast(1.06);
  }}
  .action-scrim {{
    position: absolute;
    inset: 0;
    background: linear-gradient(100deg, rgba(6,7,11,0.92) 0%, rgba(6,7,11,0.68) 38%, rgba(6,7,11,0.08) 72%, rgba(6,7,11,0.22) 100%),
                linear-gradient(180deg, rgba(6,7,11,0.45) 0%, rgba(6,7,11,0) 25%, rgba(6,7,11,0.75) 100%);
  }}
  .top-bar {{
    position: absolute;
    top: 30px;
    left: 44px;
    right: 44px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 4;
  }}
  .brand-lockup {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .brand-logo {{
    width: 30px;
    height: 30px;
    background: #e5c997;
    -webkit-mask-size: contain;
    mask-size: contain;
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
  }}
  .brand-text {{
    font-family: 'Didot', 'Bodoni 72', serif;
    font-size: 18px;
    letter-spacing: 0.22em;
    color: #f5efe6;
  }}
  .option-badge {{
    padding: 7px 14px;
    border-radius: 999px;
    border: 1px solid rgba(212, 180, 131, 0.6);
    background: rgba(8, 9, 13, 0.76);
    font-size: 10.5px;
    letter-spacing: 0.16em;
    color: #ebd3aa;
    font-weight: 600;
  }}
  .editorial-lockup {{
    position: absolute;
    left: 44px;
    bottom: 52px;
    width: 470px;
    z-index: 4;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  .blitz-pill {{
    align-self: flex-start;
    padding: 6px 12px;
    background: rgba(212, 180, 131, 0.16);
    border: 1px solid rgba(212, 180, 131, 0.55);
    border-radius: 6px;
    font-size: 10.5px;
    letter-spacing: 0.2em;
    font-weight: 700;
    color: #f2dab0;
  }}
  .hero-club {{
    font-family: 'Didot', 'Bodoni 72', serif;
    font-size: 48px;
    line-height: 0.98;
    color: #faf6ee;
    letter-spacing: 0.04em;
  }}
  .hero-tourney {{
    font-size: 16px;
    letter-spacing: 0.18em;
    color: #d4b483;
    font-weight: 600;
  }}
  .hero-metrics {{
    display: flex;
    gap: 18px;
    margin-top: 4px;
    font-size: 11px;
    letter-spacing: 0.14em;
    color: #cfc8bc;
  }}
  .hero-metrics span {{
    border-left: 2px solid #d4b483;
    padding-left: 8px;
  }}
  .divider-strip {{
    position: relative;
    height: 3px;
    background: linear-gradient(90deg, rgba(198,255,0,0.22), #c6ff00 26%, #d4b483 55%, rgba(212,180,131,0.18));
    z-index: 10;
  }}
  .divider-tag {{
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    padding: 7px 22px;
    background: #0d0e14;
    border: 1px solid #d4b483;
    border-radius: 999px;
    font-size: 10.5px;
    letter-spacing: 0.22em;
    font-weight: 700;
    color: #f4dfba;
    white-space: nowrap;
  }}
  .bottom-trophy {{
    position: relative;
    width: 1080px;
    height: 671px;
    overflow: hidden;
    background: #07080b;
  }}
  /* Align proportional 896x1200 scene centered cleanly over lower pane + walnut block */
  .acrylic-scene {{
    position: absolute;
    left: 50%;
    top: -222px;
    transform: translateX(-50%);
    width: 820px;
    height: 1098px;
  }}
  .acrylic-scene img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .bottom-vignette {{
    position: absolute;
    inset: 0;
    background:
      linear-gradient(90deg, #07080b 0%, #07080b 14%, rgba(7,8,11,0) 29%, rgba(7,8,11,0) 71%, #07080b 86%, #07080b 100%),
      radial-gradient(circle at 50% 48%, rgba(7,8,11,0) 32%, rgba(7,8,11,0.88) 88%),
      linear-gradient(180deg, rgba(7,8,11,0.7) 0%, rgba(7,8,11,0) 22%, rgba(7,8,11,0) 76%, rgba(7,8,11,0.96) 100%);
    pointer-events: none;
  }}
  .acrylic-plate {{
    position: absolute;
    left: 35.1%;
    top: 31.2%;
    width: 31.2%;
    height: 38.8%;
    transform-origin: center center;
    transform: perspective(900px) rotateY(15deg) skewY(-3.8deg) rotateZ(-0.4deg);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 14px 12px 20px;
  }}
  .plate-glow-floor {{
    position: absolute;
    left: 8%;
    right: 8%;
    bottom: -10px;
    height: 44%;
    background: radial-gradient(ellipse at 50% 100%, rgba(255, 224, 158, 0.34) 0%, rgba(214, 178, 114, 0.08) 58%, transparent 80%);
  }}
  .plate-content {{
    position: relative;
    z-index: 2;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 7px;
  }}
  .engraved-mark {{
    width: 38px;
    height: 38px;
    background: linear-gradient(180deg, rgba(255,250,238,0.92), rgba(240,206,142,0.88));
    -webkit-mask-size: contain;
    mask-size: contain;
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    filter: drop-shadow(0 0 6px rgba(255, 220, 148, 0.65));
  }}
  .engraved-kicker {{
    font-size: 9px;
    letter-spacing: 0.24em;
    font-weight: 600;
    color: rgba(248, 229, 190, 0.88);
  }}
  .engraved-club {{
    font-family: 'Didot', 'Bodoni 72', serif;
    font-size: 24px;
    line-height: 1.02;
    letter-spacing: 0.08em;
    font-weight: 700;
    color: rgba(255, 250, 240, 0.96);
    text-shadow: 0 0 12px rgba(255, 224, 158, 0.65);
  }}
  .engraved-rule {{
    width: 72%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 229, 175, 0.92), transparent);
  }}
  .engraved-tournament {{
    font-size: 11.5px;
    letter-spacing: 0.14em;
    font-weight: 600;
    color: rgba(255, 245, 224, 0.94);
  }}
  .engraved-year-pill {{
    padding: 5px 13px;
    border-radius: 999px;
    border: 1.2px solid rgba(255, 228, 172, 0.85);
    background: rgba(255, 232, 182, 0.14);
    font-size: 11.5px;
    letter-spacing: 0.18em;
    font-weight: 700;
    color: #fff6e0;
    text-shadow: 0 0 10px rgba(255, 224, 154, 0.78);
  }}
  .engraved-sponsor-box {{
    margin-top: 8px;
    width: 84%;
    padding: 6px 8px;
    border: 1px dashed rgba(255, 228, 176, 0.6);
    border-radius: 5px;
    background: rgba(255, 242, 212, 0.05);
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}
  .sponsor-caption {{
    font-size: 7.5px;
    letter-spacing: 0.2em;
    color: rgba(248, 225, 178, 0.78);
  }}
  .sponsor-slot {{
    font-size: 9px;
    letter-spacing: 0.1em;
    font-weight: 600;
    color: rgba(255, 247, 230, 0.92);
  }}
  .wood-engraving {{
    position: absolute;
    left: 36.2%;
    top: 76.2%;
    width: 37.5%;
    transform-origin: left center;
    transform: perspective(900px) rotateY(15deg) skewY(-4.6deg);
    text-align: center;
    font-size: 9.5px;
    letter-spacing: 0.32em;
    font-weight: 600;
    color: rgba(240, 208, 156, 0.64);
  }}
  {_shared_plate_variant_css()}
  .side-callout-left {{
    position: absolute;
    left: 44px;
    top: 56px;
    width: 240px;
    z-index: 5;
  }}
  .callout-title {{
    font-size: 11px;
    letter-spacing: 0.2em;
    color: #d4b483;
    font-weight: 700;
  }}
  .callout-body {{
    font-size: 13px;
    line-height: 1.45;
    color: #ded7ca;
    margin-top: 6px;
  }}
  .side-callout-right {{
    position: absolute;
    right: 44px;
    top: 56px;
    width: 230px;
    text-align: right;
    z-index: 5;
  }}
  .bottom-footer {{
    position: absolute;
    left: 44px;
    right: 44px;
    bottom: 24px;
    z-index: 6;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(212, 180, 131, 0.28);
    padding-top: 12px;
    font-size: 10.5px;
    color: rgba(220, 214, 204, 0.8);
    letter-spacing: 0.06em;
  }}
</style>
</head>
<body>
  <div class="canvas">
    <section class="top-hero">
      <img class="action-img" src="{action_uri}" alt="{_esc(spec.club_name)} Editorial 1/2000s Captoora" />
      <div class="action-scrim"></div>
      <div class="top-bar">
        <div class="brand-lockup">
          <div class="brand-logo" style="-webkit-mask-image:url('{logo_uri}'); mask-image:url('{logo_uri}');"></div>
          <span class="brand-text">{_esc(spec.header_brand_title)}</span>
        </div>
        <div class="option-badge">OPCIÓN B · EDITORIAL + ACRÍLICO LED {_esc(spec.year)}</div>
      </div>
      <div class="editorial-lockup">
        <div class="blitz-pill">HALFTIME BLITZ · ENTREGA MISMO DÍA</div>
        <h1 class="hero-club">{_esc(spec.club_name)}</h1>
        <div class="hero-tourney">{_esc(spec.tournament_name.upper())} · {_esc(spec.season_label.upper())}</div>
        <div class="hero-metrics">
          <span>{_esc(spec.hero_metrics[0])}</span>
          <span>{_esc(spec.hero_metrics[1])}</span>
          <span>{_esc(spec.hero_metrics[2])}</span>
        </div>
      </div>
    </section>

    <div class="divider-strip">
      <div class="divider-tag">COBERTURA EN VIVO + TROFEO LED {_esc(spec.season_label.upper())}</div>
    </div>

    <section class="bottom-trophy">
      <div class="acrylic-scene">
        <img src="{acrylic_uri}" alt="Trofeo Acrílico LED" />
        {plate_html}
        <div class="wood-engraving {style_cls}">CAPTOORA · {_esc(spec.year)}</div>
      </div>
      <div class="bottom-vignette"></div>

      <div class="side-callout-left">
        <div class="callout-title">EDICIÓN {_esc(spec.season_label.upper())}</div>
        <div class="callout-body">
          Acrílico óptico cortado y grabado con láser en base sólida de nogal iluminada.
        </div>
      </div>

      <div class="side-callout-right">
        <div class="callout-title">MODELO PATROCINADO</div>
        <div class="callout-body">
          Incluye espacio para marca patrocinadora y financiación hasta 100% sin costo para el club.
        </div>
      </div>

      <div class="bottom-footer">
        <span>*Fotos y reels el mismo día · Acrílico LED en taller MTY/SPGG: 3–5 días hábiles.</span>
        <span style="color:#c6ff00; font-weight:600;">{_esc(spec.website_url.replace('https://', ''))} · {_esc(spec.gallery_url.replace('https://', ''))} · WA {_esc(spec.whatsapp_display)}</span>
      </div>
    </section>
  </div>
</body>
</html>"""


def _build_dossier_pdf_html(spec: MockupSpec, mockup_a_path: Path, mockup_b_path: Path) -> str:
    """Strictly 1-page Letter PDF dossier styled after Captoora Studio (Jet Black + Volt #C6FF00 + Gold)."""
    logo_uri = _file_data_uri(CAPTOORA_LOGO_PATH)
    opc_a_uri = _file_data_uri(mockup_a_path)
    opc_b_uri = _file_data_uri(mockup_b_path)
    club_badge_html = ""
    if spec.club_logo_path and spec.club_logo_path.exists():
        club_badge_html = (
            f'<div class="club-crest-pill">'
            f'<img src="{_file_data_uri(spec.club_logo_path)}" alt="{_esc(spec.club_name)}" />'
            f'</div>'
        )
    extra_kicker, extra_old, extra_price, extra_desc = spec.extra_card or (
        "PILOTO · CAPTOORA BIOGEN (BETA -35%)",
        "$1,950",
        "$1,268 /mes",
        "Seguimiento físico escultórico en estudio (semanal/mensual · 3 a 60 meses) p/ gyms y atletas.",
    )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @page {{
    size: letter;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}
  html, body {{
    width: 8.5in;
    height: 11in;
    overflow: hidden;
    background: #000000;
    color: #f4efe6;
    font-family: 'Avenir Next', 'Helvetica Neue', sans-serif;
  }}
  .page {{
    width: 8.5in;
    height: 11in;
    padding: 0.34in 0.46in 0.28in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #000000;
  }}
  .topbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
  }}
  .topbar-right {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .club-crest-pill {{
    height: 28px;
    padding: 3px 9px;
    border-radius: 5px;
    background: rgba(250, 246, 238, 0.94);
    border: 1px solid #c9a23f;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .club-crest-pill img {{
    max-height: 20px;
    max-width: 78px;
    object-fit: contain;
    display: block;
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 11px;
  }}
  .brand-mark {{
    width: 34px;
    height: 34px;
    background: #ffffff;
    -webkit-mask-size: contain;
    mask-size: contain;
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
  }}
  .brand-name {{
    font-family: 'Didot', 'Bodoni 72', serif;
    font-size: 17px;
    letter-spacing: 0.22em;
    color: #ffffff;
  }}
  .brand-sub {{
    font-size: 8px;
    letter-spacing: 0.18em;
    color: #c9a23f;
    margin-top: 2px;
    font-weight: 600;
  }}
  .doc-tag {{
    padding: 5px 12px;
    border-radius: 4px;
    border: 1px solid #c6ff00;
    background: #050505;
    font-size: 8.5px;
    letter-spacing: 0.16em;
    font-weight: 700;
    color: #c6ff00;
    white-space: nowrap;
  }}
  .volt-rule {{
    width: 100%;
    height: 2px;
    background: #c6ff00;
    margin-bottom: 10px;
  }}
  .hero {{
    margin-top: 2px;
  }}
  .hero-kicker {{
    font-size: 8.5px;
    letter-spacing: 0.22em;
    color: #c9a23f;
    font-weight: 700;
  }}
  .hero h1 {{
    font-family: 'Didot', 'Bodoni 72', serif;
    font-size: 24px;
    line-height: 1.12;
    color: #ffffff;
    margin-top: 3px;
    font-weight: 500;
  }}
  .hero-lead {{
    font-size: 10.2px;
    line-height: 1.42;
    color: #d0d0d0;
    margin-top: 5px;
  }}
  .visual-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 10px;
  }}
  .visual-card {{
    background: #070709;
    border: 1px solid rgba(201, 162, 63, 0.38);
    border-radius: 8px;
    padding: 7px;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}
  .visual-card img {{
    width: 100%;
    height: 3.08in;
    object-fit: contain;
    background: #050507;
    border-radius: 5px;
    display: block;
  }}
  .visual-caption {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2px 4px;
    font-size: 8px;
    letter-spacing: 0.12em;
    color: #c9a23f;
    font-weight: 700;
  }}
  .pillars {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 8px;
  }}
  .pillar {{
    background: #070709;
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 6px;
    padding: 7px 9px;
  }}
  .pillar-num {{
    font-size: 7.4px;
    letter-spacing: 0.16em;
    color: #c9a23f;
    font-weight: 700;
  }}
  .pillar-title {{
    font-size: 9.8px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 2px;
  }}
  .pillar-copy {{
    font-size: 8px;
    line-height: 1.34;
    color: #bcbcbc;
    margin-top: 2px;
  }}
  .options-ladder {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1.12fr;
    gap: 7px;
    margin-top: 7px;
  }}
  .opt-card {{
    background: #08090c;
    border: 1px solid rgba(198, 255, 0, 0.28);
    border-radius: 6px;
    padding: 6px 8px;
  }}
  .opt-card.biogen {{
    border-color: rgba(201, 162, 63, 0.55);
    background: #0b0a08;
  }}
  .opt-kicker {{
    font-size: 7px;
    letter-spacing: 0.14em;
    color: #c6ff00;
    font-weight: 700;
  }}
  .opt-card.biogen .opt-kicker {{
    color: #c9a23f;
  }}
  .opt-price {{
    font-size: 10px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 1px;
  }}
  .opt-desc {{
    font-size: 7.5px;
    line-height: 1.3;
    color: #bdbdbd;
    margin-top: 2px;
  }}
  .trust-strip {{
    margin-top: 7px;
    padding: 6px 11px;
    border-radius: 6px;
    background: #08080a;
    border: 1px solid rgba(201, 162, 63, 0.34);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }}
  .trust-label {{
    font-size: 7.6px;
    letter-spacing: 0.18em;
    color: #c9a23f;
    font-weight: 700;
    white-space: nowrap;
  }}
  .trust-brands {{
    font-size: 9.2px;
    letter-spacing: 0.06em;
    color: #f4f4f4;
    font-weight: 600;
  }}
  .cta-box {{
    margin-top: 7px;
    padding: 8px 13px;
    border-radius: 6px;
    background: #060608;
    border: 1px solid rgba(255, 255, 255, 0.22);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }}
  .cta-info h3 {{
    font-size: 12.2px;
    font-weight: 700;
    color: #ffffff;
  }}
  .cta-info p {{
    font-size: 8px;
    color: #b8b8b8;
    margin-top: 2px;
  }}
  .cta-links {{
    display: flex;
    gap: 8px;
    flex-shrink: 0;
  }}
  /* Signature Captoora button exact style from template: black fill + #C6FF00 Volt text & border */
  .btn-wa-volt {{
    text-decoration: none;
    padding: 8px 14px;
    border-radius: 4px;
    border: 1.2px solid #c6ff00;
    background: #000000;
    color: #c6ff00;
    font-size: 8.5px;
    font-weight: 700;
    letter-spacing: 0.14em;
    white-space: nowrap;
  }}
  .btn-gallery-gold {{
    text-decoration: none;
    padding: 8px 12px;
    border-radius: 4px;
    border: 1px solid #c9a23f;
    background: rgba(201, 162, 63, 0.12);
    color: #f4e6c6;
    font-size: 8.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    white-space: nowrap;
  }}
  .signature-footer {{
    margin-top: 7px;
    border-top: 1px solid rgba(255, 255, 255, 0.24);
    padding-top: 6px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 12px;
  }}
  .sig-name {{
    font-size: 10.5px;
    font-weight: 700;
    color: #ffffff;
  }}
  .sig-role {{
    font-size: 7.8px;
    letter-spacing: 0.16em;
    color: #c9a23f;
    margin-top: 1px;
    font-weight: 600;
  }}
  .sig-meta {{
    font-size: 7.8px;
    line-height: 1.42;
    color: #cfcfcf;
    margin-top: 3px;
  }}
  .sig-meta a {{
    color: #cfcfcf;
    text-decoration: none;
  }}
  .sig-legal {{
    text-align: right;
    font-size: 7.4px;
    line-height: 1.4;
    color: #8f8f8f;
    max-width: 2.75in;
  }}
</style>
</head>
<body>
  <div class="page">
    <div>
      <header class="topbar">
        <div class="brand">
          <div class="brand-mark" style="-webkit-mask-image:url('{logo_uri}'); mask-image:url('{logo_uri}');"></div>
          <div>
            <div class="brand-name">CAPTOORA STUDIO</div>
            <div class="brand-sub">{_esc(spec.director_name.upper())} · {_esc(spec.instagram_handle.upper())}</div>
          </div>
        </div>
        <div class="topbar-right">
          {club_badge_html}
          <div class="doc-tag">DOSSIER PERSONALIZADO · {_esc(spec.season_label.upper())}</div>
        </div>
      </header>
      <div class="volt-rule"></div>

      <section class="hero">
        <div class="hero-kicker">PREPARADO PARA {_esc(spec.club_name.upper())} · {_esc(spec.city_label.upper())}</div>
        <h1>{_esc(spec.tournament_name)} · {_esc(spec.season_label)}: Cobertura en Vivo y Trofeos LED</h1>
        <p class="hero-lead">
          Propuesta modular a elegir para {_esc(spec.club_name)}: galerías a 1/2000s entregadas el mismo día, opción impresa/marcos y trofeos LED — con pago de elementos físicos diferible a un segundo momento y opción autofinanciada con patrocinadores.
        </p>
      </section>

      <section class="visual-grid">
        <div class="visual-card">
          <img src="{opc_a_uri}" alt="Opción A Minimalista Acrílico LED" />
          <div class="visual-caption">
            <span>OPCIÓN A · ACRÍLICO LED {_esc(spec.year)}</span>
            <span>NOGAL + LÁSER</span>
          </div>
        </div>
        <div class="visual-card">
          <img src="{opc_b_uri}" alt="Opción B Editorial 1/2000s + Trofeo" />
          <div class="visual-caption">
            <span>OPCIÓN B · EDITORIAL + TROFEO LED</span>
            <span>MISMO DÍA</span>
          </div>
        </div>
      </section>

      <section class="pillars">
        <div class="pillar">
          <div class="pillar-num">01 · HALFTIME BLITZ</div>
          <div class="pillar-title">Galería Digital Mismo Día</div>
          <p class="pillar-copy">
            Fotos a 1/2000s y reels curados en ({_esc(spec.gallery_url.replace('https://', ''))}) el mismo día para proyectar imagen profesional.
          </p>
        </div>
        <div class="pillar">
          <div class="pillar-num">02 · PREMIACIÓN {_esc(spec.year)}</div>
          <div class="pillar-title">Acrílico Óptico LED</div>
          <p class="pillar-copy">
            Placas grabadas con {_esc(spec.club_name)} sobre nogal iluminado en taller local MTY/SPGG (3–5 días hábiles).
          </p>
        </div>
        <div class="pillar">
          <div class="pillar-num">03 · PAGO EN 2 MOMENTOS</div>
          <div class="pillar-title">Cero Presión Presupuestal</div>
          <p class="pillar-copy">
            Aparta solo cobertura digital hoy; decide acrílicos, marcos finos o patrocinadores en un segundo momento.
          </p>
        </div>
      </section>

      <section class="options-ladder">
        <div class="opt-card">
          <div class="opt-kicker">OPCIÓN 1 · SOLO DIGITAL (-35%)</div>
          <div class="opt-price"><span style="text-decoration:line-through; color:#777; font-size:8px; font-weight:400;">$4,900</span> $3,185 MXN</div>
          <p class="opt-desc">Cobertura 1/2000s + galería mismo día. Sin elementos físicos obligatorios.</p>
        </div>
        <div class="opt-card">
          <div class="opt-kicker">OPCIÓN 2 · FOTO + IMPRESIÓN (-35%)</div>
          <div class="opt-price"><span style="text-decoration:line-through; color:#777; font-size:8px; font-weight:400;">$7,900</span> $5,135 MXN</div>
          <p class="opt-desc">Cobertura digital + impresiones Fine Art / marcos (liquidable en 2do momento).</p>
        </div>
        <div class="opt-card">
          <div class="opt-kicker">OPCIÓN 3 · SUITE FULL + LED (-35%)</div>
          <div class="opt-price"><span style="text-decoration:line-through; color:#777; font-size:8px; font-weight:400;">$11,500</span> $7,475 MXN</div>
          <p class="opt-desc">Cobertura + Reels Meta Ads + 4 acrílicos LED + 20 llaveros (físicos en 2do momento).</p>
        </div>
        <div class="opt-card biogen">
          <div class="opt-kicker">{_esc(extra_kicker)}</div>
          <div class="opt-price"><span style="text-decoration:line-through; color:#8d7849; font-size:8px; font-weight:400;">{_esc(extra_old)}</span> {_esc(extra_price)}</div>
          <p class="opt-desc">{_esc(extra_desc)}</p>
        </div>
      </section>
    </div>

    <div>
      <section class="trust-strip">
        <span class="trust-label">RESPALDO COMPROBADO</span>
        <span class="trust-brands">Coca-Cola FEMSA · Heineken / Tecate · Poder Judicial de Nuevo León</span>
      </section>

      <section class="cta-box">
        <div class="cta-info">
          <h3>¿Cuál de las 3 opciones (-35% Temporada) revisamos para {_esc(spec.season_label)}?</h3>
          <p>Escríbeme por WhatsApp o explora el Portal 3D y galerías recientes en captoora.studio/sports.</p>
        </div>
        <div class="cta-links">
          <a class="btn-gallery-gold" href="{_esc(spec.gallery_url)}">VER GALERÍA</a>
          <a class="btn-wa-volt" href="{_esc(spec.whatsapp_url)}">ESCRÍBEME POR WHATSAPP</a>
        </div>
      </section>

      <footer class="signature-footer">
        <div>
          <div class="sig-name">{_esc(spec.director_name)}</div>
          <div class="sig-role">{_esc(spec.director_role)}</div>
          <div class="sig-meta">
            WhatsApp: <a href="{_esc(spec.whatsapp_url)}">{_esc(spec.whatsapp_display)}</a> · Correo: <a href="mailto:{_esc(spec.email_address)}">{_esc(spec.email_address)}</a><br>
            Web: <a href="{_esc(spec.website_url)}">{_esc(spec.website_url.replace('https://', ''))}</a> · Galería: <a href="{_esc(spec.gallery_url)}">{_esc(spec.gallery_url.replace('https://', ''))}</a> · IG: {_esc(spec.instagram_handle)}<br>
            {_esc(spec.address_line)} · {_esc(spec.hours_line)}
          </div>
        </div>
        <div class="sig-legal">
          *Descuento de temporada -35% vigente en agenda Nov–Dic 2026.<br>
          Digital el mismo día · Acrílicos LED y marcos en taller MTY/SPGG: 3–5 días hábiles.
        </div>
      </footer>
    </div>
  </div>
</body>
</html>"""


def _build_signature_block_html(spec: MockupSpec, logo_uri: str, *, theme: Literal["dark", "light"]) -> str:
    """Two-column horizontal signature matching Captoora Studio visual card."""
    is_dark = theme == "dark"
    fg = "#f4f4f4" if is_dark else "#111111"
    muted = "#c8c8c8" if is_dark else "#333333"
    line_color = "rgba(255,255,255,0.28)" if is_dark else "#111111"
    logo_filter = "" if is_dark else "filter: invert(1);"

    return f"""<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-top:1px solid {line_color}; padding-top:22px;">
  <tr>
    <td width="136" valign="middle" align="center" style="width:136px; padding:10px 18px 10px 0; border-right:1px solid {line_color};">
      <img src="{logo_uri}" alt="Captoora Studio" width="76" style="display:block; border:0; {logo_filter}" />
    </td>
    <td valign="middle" style="padding:4px 0 4px 22px; font-family:'Helvetica Neue', Arial, sans-serif; color:{muted}; font-size:12.5px; line-height:1.62;">
      <div style="font-size:15.5px; font-weight:700; color:{fg};">{_esc(spec.director_name)}</div>
      <div style="font-size:10.5px; letter-spacing:0.18em; color:#c9a23f; font-weight:700; padding-bottom:10px; margin-bottom:10px; border-bottom:1px solid {line_color};">
        {_esc(spec.director_role)}
      </div>
      <div>WhatsApp: <a href="{_esc(spec.whatsapp_url)}" style="color:{muted}; text-decoration:none;">{_esc(spec.whatsapp_display)}</a> &nbsp;·&nbsp; Correo: <a href="mailto:{_esc(spec.email_address)}" style="color:{muted}; text-decoration:none;">{_esc(spec.email_address)}</a></div>
      <div>Web: <a href="{_esc(spec.website_url)}" style="color:{muted}; text-decoration:none;">{_esc(spec.website_url.replace('https://', ''))}</a> &nbsp;·&nbsp; Galería: <a href="{_esc(spec.gallery_url)}" style="color:{muted}; text-decoration:none;">{_esc(spec.gallery_url.replace('https://', ''))}</a></div>
      <div>Instagram: {_esc(spec.instagram_handle)} &nbsp;·&nbsp; {_esc(spec.address_line)}</div>
      <div style="font-size:11.5px; margin-top:4px;">{_esc(spec.hours_line)}</div>
      <div style="font-size:10.5px; color:#888888; margin-top:6px;">
        *Cobertura digital mismo día · Manufactura de acrílicos LED en taller MTY/SPGG: 3–5 días hábiles.
      </div>
    </td>
  </tr>
</table>"""


def _build_signature_html(spec: MockupSpec) -> str:
    """Standalone horizontal email signature card matching reference signature mockup."""
    logo_uri = _file_data_uri(CAPTOORA_LOGO_PATH)
    sig_table = _build_signature_block_html(spec, logo_uri, theme="light")
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Firma Captoora Studio · {_esc(spec.director_name)}</title>
</head>
<body style="margin:0; padding:24px; background:#ffffff; color:#111111; font-family:'Helvetica Neue', Arial, sans-serif;">
  <table role="presentation" width="640" cellspacing="0" cellpadding="0" style="max-width:640px; width:100%; background:#ffffff;">
    <tr>
      <td style="height:2px; background:#c6ff00; font-size:0; line-height:0;">&nbsp;</td>
    </tr>
    <tr>
      <td style="padding-top:16px;">
        {sig_table}
      </td>
    </tr>
  </table>
</body>
</html>"""


def _build_email_html(spec: MockupSpec, *, theme: Literal["dark", "light"]) -> str:
    """Build Captoora Studio HTML email matching Jet Black / Crisp White + #C6FF00 + Gold + 2-col Signature."""
    logo_uri = _file_data_uri(CAPTOORA_LOGO_PATH)
    is_dark = theme == "dark"
    bg = "#000000" if is_dark else "#ffffff"
    fg = "#f4f4f4" if is_dark else "#111111"
    btn_bg = "#000000"
    btn_border = "1.5px solid #c6ff00" if is_dark else "none"
    secondary_color = "#dfcbb5" if is_dark else "#6e5620"
    logo_filter = "" if is_dark else "filter: invert(1);"
    signature_html = _build_signature_block_html(spec, logo_uri, theme=theme)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Captoora Studio · {_esc(spec.club_name)} ({_esc(spec.season_label)})</title>
</head>
<body style="margin:0; padding:0; background:{bg}; color:{fg}; font-family:'Helvetica Neue', Arial, sans-serif;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:{bg}; padding:36px 20px;">
    <tr>
      <td align="center">
        <table role="presentation" width="620" cellspacing="0" cellpadding="0" style="max-width:620px; width:100%; background:{bg};">
          <tr>
            <td style="padding:0 0 24px 56px;">
              <img src="{logo_uri}" alt="Captoora Studio" width="74" style="display:block; border:0; {logo_filter}" />
            </td>
          </tr>
          <tr>
            <td style="height:3px; background:#c6ff00; font-size:0; line-height:0;">&nbsp;</td>
          </tr>
          <tr>
            <td style="padding:32px 24px 0 24px; font-size:15px; line-height:1.65; color:{fg};">
              <p style="margin:0 0 16px 0;">Hola equipo de <strong>{_esc(spec.club_name)}</strong> 👋,</p>
              <p style="margin:0 0 16px 0;">
                Vimos que se acerca su <strong>{_esc(spec.tournament_name)} · {_esc(spec.season_label)}</strong> 🎾🎄 y preparamos vistas previas personalizadas (Acrílico LED 2026 + Acción 1/2000s) junto con su Dossier Ejecutivo y el beneficio vigente de <strong>-35% Descuento de Temporada</strong>.
              </p>
              <p style="margin:0 0 12px 0;">
                Trabajan directamente con <strong>tres opciones a elegir ("¿Cuál prefieres?")</strong>:
              </p>
              <div style="margin:0 0 18px 0; padding:14px 16px; border:1px solid {('rgba(198,255,0,0.38)' if is_dark else 'rgba(110,86,32,0.28)')}; border-radius:8px; background:{('rgba(255,255,255,0.03)' if is_dark else '#f8f7f3')}; font-size:13.5px; line-height:1.6;">
                <div><strong>1 · Solo Digital (<span style="text-decoration:line-through;opacity:.6;">$4,900</span> $3,185 MXN · -35%):</strong> Cobertura 1/2000s + galería mismo día en <strong>{_esc(spec.gallery_url.replace('https://', ''))}</strong> para proyectar imagen profesional.</div>
                <div style="margin-top:6px;"><strong>2 · Foto + Impresión / Marcos (<span style="text-decoration:line-through;opacity:.6;">$7,900</span> $5,135 MXN · -35%):</strong> Digital el mismo día + impresiones Fine Art o marcos finos.</div>
                <div style="margin-top:6px;"><strong>3 · Suite Full + Ads &amp; Acrílicos LED (<span style="text-decoration:line-through;opacity:.6;">$11,500</span> $7,475 MXN · -35%):</strong> Cobertura + Reels p/ Meta Ads + 4 placas LED + 20 llaveros (autofinanciable por patrocinadores).</div>
                <div style="margin-top:8px; padding-top:8px; border-top:1px solid {('rgba(255,255,255,0.14)' if is_dark else '#e2ddd2')}; font-size:12.5px; color:{secondary_color};">
                  <strong>Pago en 2do momento disponible:</strong> Aparten hoy solo la cobertura digital ($3,185 MXN c/ -35%) y decidan o liquiden placas LED, impresiones y Ads en un segundo momento.
                </div>
              </div>
              <p style="margin:0 0 14px 0; font-size:14px;">
                🧬 <strong>Programa Piloto Captoora Biogen (Beta · -35%):</strong> Documentación fotográfica escultórica en estudio de progreso físico (semanal, quincenal, mensual o bimestral en ciclos de 3 a 60 meses, desde <span style="text-decoration:line-through;opacity:.6;">$1,950</span> <strong>$1,268 MXN/mes</strong>).
              </p>
              <p style="margin:0 0 16px 0; font-size:13.5px;">
                📍 <strong>Captoora Small Business ("Arranca 2027 · -35%"):</strong> También renovamos su ficha de <strong>Google Maps</strong> (reemplazando vistas genéricas de Street View o galerías incompletas) + configuración formal en <strong>Meta Business Portfolio</strong> (FB + IG + WhatsApp sin bloqueos) desde <strong>$3,900 MXN</strong> (precio regular $6,000) o Suite Total <strong>$6,890 MXN</strong> (antes $10,600).
              </p>
              <p style="margin:0 0 22px 0; font-size:13.5px;">
                Respaldo institucional comprobado: <strong>Coca-Cola FEMSA · Heineken / Tecate · Poder Judicial de Nuevo León</strong>.<br>
                <span style="color:{secondary_color}; font-size:12.5px;">*Entrega digital el mismo día · Acrílicos LED y marcos en taller MTY/SPGG: 3–5 días hábiles.</span>
              </p>
              <p style="margin:0 0 4px 0;">Un saludo,</p>
              <p style="margin:0 0 4px 0; font-size:16px; font-weight:700; color:{fg};">{_esc(spec.director_name)}</p>
              <p style="margin:0 0 22px 0; font-size:11px; letter-spacing:0.2em; color:#c9a23f; font-weight:600;">FOTÓGRAFO Y DIRECTOR</p>
              <table role="presentation" cellspacing="0" cellpadding="0" style="margin-bottom:28px;">
                <tr>
                  <td style="background:{btn_bg}; border:{btn_border}; border-radius:4px;">
                    <a href="{_esc(spec.whatsapp_url)}" style="display:inline-block; padding:14px 26px; color:#c6ff00; text-decoration:none; font-size:12px; font-weight:700; letter-spacing:0.16em; text-transform:uppercase;">
                      ESCRÍBEME POR WHATSAPP
                    </a>
                  </td>
                  <td style="padding-left:18px; vertical-align:middle;">
                    <a href="{_esc(spec.website_url)}" style="color:{secondary_color}; text-decoration:none; font-size:12px; letter-spacing:0.08em; border-bottom:1px solid {secondary_color}; padding-bottom:2px;">
                      Portal 3D &amp; Sports &rarr;
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding:0 24px;">
              {signature_html}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def _build_before_after_audit_html(spec: SmallBusinessSpec) -> str:
    """Build 1200x1500 Antes vs Después graphic comparing current Google Maps vs Captoora 2027."""
    profile = resolve_niche_profile(spec.niche_label, name=spec.business_name, category=spec.category_label)
    hero_path = spec.after_hero_path if spec.after_hero_path.exists() else profile.hero_path
    if not hero_path.exists():
        hero_path = PADEL_ACTION_PATH

    logo_uri = _file_data_uri(CAPTOORA_LOGO_PATH)
    after_uri = _file_data_uri(hero_path)
    before_uri = ""
    if spec.maps_screenshot_path and spec.maps_screenshot_path.exists():
        before_uri = _file_data_uri(spec.maps_screenshot_path)

    prospect_logo_html = ""
    if spec.prospect_logo_path and spec.prospect_logo_path.exists():
        prospect_logo_html = (
            f'<div class="prospect-logo-pill">'
            f'<img src="{_file_data_uri(spec.prospect_logo_path)}" alt="{_esc(spec.business_name)}" />'
            f'</div>'
        )

    after_tag = spec.after_tag or profile.after_tag
    after_overlay_sub = spec.after_overlay_sub or profile.after_overlay_sub
    hero_intro = spec.hero_intro or profile.hero_intro
    pillars = spec.pillars or profile.pillars
    tier_cards = spec.tier_cards or (profile.tier1, profile.tier2, profile.tier3)

    obs_html = "".join(
        f'<li><span class="dot">•</span><span>{_esc(line)}</span></li>'
        for line in (spec.observations[:3] or ("Oportunidad visual en portada de Google Maps.",))
    )
    pillars_html = "".join(
        f'<li><span class="dot">✓</span><span><strong>{_esc(title)}:</strong> {_esc(desc)}</span></li>'
        for title, desc in pillars[:3]
    )
    tiers_html = "".join(
        f"""<div class="tier-box{' featured' if idx == 1 else ''}">
          <div class="tier-kicker">{_esc(kicker)}</div>
          <div class="tier-price-row"><span class="tier-old">{_esc(old_p)}</span><span class="tier-new">{_esc(new_p)}</span></div>
          <div class="tier-desc">{_esc(desc)}</div>
        </div>"""
        for idx, (kicker, old_p, new_p, desc) in enumerate(tier_cards[:3])
    )

    before_panel_media = (
        f'<img src="{before_uri}" alt="Captura actual en Google Maps de {_esc(spec.business_name)}" />'
        if before_uri
        else f"""<div class="mock-before-placeholder">
          <div class="mock-street-banner">VISTA AUTOMÁTICA / SIN CURADURÍA</div>
          <div class="mock-before-title">{_esc(spec.business_name)}</div>
          <div class="mock-before-sub">{_esc(spec.category_label)}</div>
          <div class="mock-before-warn">Ficha sin portada editorial optimizada ni enlace Business Portfolio</div>
        </div>"""
    )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1200px;
    height: 1500px;
    overflow: hidden;
    background: #050608;
    color: #f4f4f4;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }}
  .canvas {{
    width: 1200px;
    height: 1500px;
    padding: 40px 44px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 82% 8%, rgba(198,255,0,0.08), transparent 42%),
                radial-gradient(circle at 12% 92%, rgba(201,162,63,0.10), transparent 45%),
                #050608;
  }}
  .topbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 18px;
    border-bottom: 2px solid #c6ff00;
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .brand img {{ width: 52px; height: auto; display: block; }}
  .brand-name {{ font-family: 'Didot', 'Georgia', serif; font-size: 24px; letter-spacing: 0.2em; color: #fff; }}
  .brand-sub {{ font-size: 11px; letter-spacing: 0.18em; color: #c9a23f; font-weight: 700; margin-top: 3px; }}
  .topbar-right {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .prospect-logo-pill {{
    height: 40px;
    padding: 5px 12px;
    border-radius: 8px;
    background: rgba(250, 246, 238, 0.95);
    border: 1px solid rgba(201, 162, 63, 0.72);
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .prospect-logo-pill img {{
    max-height: 28px;
    max-width: 112px;
    width: auto;
    height: auto;
    object-fit: contain;
    display: block;
  }}
  .season-pill {{
    padding: 9px 18px;
    border-radius: 999px;
    border: 1.5px solid #c6ff00;
    background: rgba(198,255,0,0.1);
    color: #c6ff00;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.14em;
  }}
  .hero-title-wrap {{ margin-top: 18px; }}
  .hero-kicker {{ font-size: 12px; letter-spacing: 0.22em; color: #c9a23f; font-weight: 700; }}
  .hero-title-wrap h1 {{ font-family: 'Didot', 'Georgia', serif; font-size: 38px; line-height: 1.12; color: #fff; margin-top: 6px; font-weight: 500; }}
  .hero-title-wrap p {{ font-size: 15.5px; color: #d0d3dc; line-height: 1.48; margin-top: 8px; max-width: 1020px; }}
  .compare-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 22px;
    margin-top: 18px;
  }}
  .pane {{
    border-radius: 14px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  .pane.before {{
    background: #0c0d12;
    border: 1px solid rgba(255,255,255,0.18);
  }}
  .pane.after {{
    background: linear-gradient(160deg, rgba(16,18,22,0.98), rgba(7,8,10,0.98));
    border: 1.5px solid #c6ff00;
    box-shadow: 0 18px 40px rgba(0,0,0,0.65);
  }}
  .pane-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .pane-badge {{
    font-size: 11px;
    letter-spacing: 0.16em;
    font-weight: 700;
    padding: 5px 11px;
    border-radius: 999px;
  }}
  .pane.before .pane-badge {{ background: rgba(255,255,255,0.08); color: #d8c8ad; border: 1px solid rgba(216,200,173,0.3); }}
  .pane.after .pane-badge {{ background: rgba(198,255,0,0.14); color: #c6ff00; border: 1px solid rgba(198,255,0,0.6); }}
  .media-box {{
    width: 100%;
    height: 360px;
    border-radius: 10px;
    overflow: hidden;
    position: relative;
    background: #07080a;
    border: 1px solid rgba(255,255,255,0.14);
  }}
  .media-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: left top;
    display: block;
  }}
  .pane.after .media-box img {{
    object-position: center center;
  }}
  .after-overlay-card {{
    position: absolute;
    left: 14px;
    right: 14px;
    bottom: 14px;
    background: rgba(6,7,10,0.88);
    border: 1px solid rgba(201,162,63,0.55);
    border-radius: 10px;
    padding: 12px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }}
  .after-overlay-title {{ font-size: 16px; font-weight: 700; color: #fff; }}
  .after-overlay-sub {{ font-size: 11.5px; color: #dfcbb5; margin-top: 2px; }}
  .after-stars {{ font-size: 12px; color: #c6ff00; font-weight: 700; white-space: nowrap; }}
  .mock-before-placeholder {{
    width: 100%; height: 100%; padding: 28px; display: flex; flex-direction: column; justify-content: center; gap: 12px;
    background: linear-gradient(150deg, #16181f, #0a0b0e);
  }}
  .mock-street-banner {{ font-size: 11px; letter-spacing: 0.16em; color: #d8c8ad; font-weight: 700; }}
  .mock-before-title {{ font-size: 26px; font-weight: 700; color: #fff; }}
  .mock-before-sub {{ font-size: 14px; color: #aaa; }}
  .mock-before-warn {{ padding: 10px 12px; border-left: 3px solid #c9a23f; background: rgba(201,162,63,0.08); font-size: 13px; color: #f1dec0; }}
  .bullet-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 13.5px;
    line-height: 1.42;
    color: #cfd4df;
  }}
  .bullet-list li {{ display: flex; gap: 8px; align-items: flex-start; }}
  .bullet-list .dot {{ color: #c9a23f; font-weight: 700; }}
  .pane.after .bullet-list .dot {{ color: #c6ff00; }}
  .tiers-strip {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 16px;
  }}
  .tier-box {{
    background: #090a0d;
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 10px;
    padding: 14px 16px;
  }}
  .tier-box.featured {{
    border-color: #c6ff00;
    background: rgba(198,255,0,0.04);
  }}
  .tier-kicker {{ font-size: 10.5px; letter-spacing: 0.14em; color: #c9a23f; font-weight: 700; }}
  .tier-box.featured .tier-kicker {{ color: #c6ff00; }}
  .tier-price-row {{ margin-top: 6px; display: flex; align-items: baseline; gap: 8px; }}
  .tier-old {{ text-decoration: line-through; color: #7e8390; font-size: 13px; }}
  .tier-new {{ font-size: 21px; font-weight: 700; color: #fff; }}
  .tier-desc {{ font-size: 12.2px; color: #c1c6d2; line-height: 1.38; margin-top: 6px; }}
  .footer-bar {{
    margin-top: 14px;
    padding-top: 14px;
    border-top: 1px solid rgba(255,255,255,0.22);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
  }}
  .footer-left {{ font-size: 13px; color: #d4d4d4; line-height: 1.48; }}
  .footer-left strong {{ color: #fff; font-size: 15px; }}
  .cta-pill {{
    padding: 13px 22px;
    border-radius: 8px;
    border: 1.5px solid #c6ff00;
    background: #000;
    color: #c6ff00;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.12em;
    white-space: nowrap;
  }}
</style>
</head>
<body>
  <div class="canvas">
    <div>
      <header class="topbar">
        <div class="brand">
          <img src="{logo_uri}" alt="Captoora Studio" />
          <div>
            <div class="brand-name">CAPTOORA SMALL BUSINESS</div>
            <div class="brand-sub">{_esc(spec.director_name.upper())} · {_esc(spec.city_label.upper())}</div>
          </div>
        </div>
        <div class="topbar-right">
          {prospect_logo_html}
          <div class="season-pill">{_esc(spec.season_tag)}</div>
        </div>
      </header>

      <section class="hero-title-wrap">
        <div class="hero-kicker">DIAGNÓSTICO VISUAL PERSONALIZADO · {_esc(profile.niche_key.upper())} · GOOGLE MAPS + META</div>
        <h1>{_esc(spec.business_name)}: Tu Vitrina Digital Hoy vs. 2027</h1>
        <p>{_esc(hero_intro)}</p>
      </section>

      <section class="compare-grid">
        <article class="pane before">
          <div class="pane-header">
            <span class="pane-badge">ANTES · FICHA ACTUAL EN GOOGLE MAPS</span>
            <span style="font-size:12px; color:#9da3b2;">{_esc(spec.rating_label)}</span>
          </div>
          <div class="media-box">
            {before_panel_media}
          </div>
          <ul class="bullet-list">
            {obs_html}
          </ul>
        </article>

        <article class="pane after">
          <div class="pane-header">
            <span class="pane-badge">DESPUÉS · LLAVE EN MANO CAPTOORA 2027</span>
            <span style="font-size:12px; color:#c6ff00; font-weight:700;">{_esc(after_tag)}</span>
          </div>
          <div class="media-box">
            <img src="{after_uri}" alt="Propuesta visual editorial {_esc(spec.business_name)} Captoora 2027" />
            <div class="after-overlay-card">
              <div>
                <div class="after-overlay-title">{_esc(spec.business_name)} · Ficha Verificada 2027</div>
                <div class="after-overlay-sub">{_esc(after_overlay_sub)}</div>
              </div>
              <div class="after-stars">5.0 PRO</div>
            </div>
          </div>
          <ul class="bullet-list">
            {pillars_html}
          </ul>
        </article>
      </section>

      <section class="tiers-strip">
        {tiers_html}
      </section>
    </div>

    <footer class="footer-bar">
      <div class="footer-left">
        <strong>{_esc(spec.director_name)}</strong> · {_esc(spec.director_role)}<br>
        WhatsApp: {_esc(spec.whatsapp_display)} · {_esc(spec.email_address)} · Web: {_esc(spec.website_url.replace('https://', ''))} · {_esc(spec.instagram_handle)}<br>
        <span style="font-size:11.5px; color:#8d92a0;">{_esc(spec.sla_footer_note)}</span>
      </div>
      <div class="cta-pill">WHATSAPP · ¿CUÁL PREFIERES?</div>
    </footer>
  </div>
</body>
</html>"""


def _build_smb_dossier_pdf_html(spec: SmallBusinessSpec, before_after_path: Path) -> str:
    """Wrap the high-res Antes vs Después visual and 3-tier -35% SMB architecture into a 1-page Letter PDF."""
    visual_uri = _file_data_uri(before_after_path)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @page {{ size: letter portrait; margin: 0.25in; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    background: #000000;
    color: #f4f4f4;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .page {{
    width: 8in;
    height: 10.45in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    background: #000;
  }}
  .visual-hero {{
    width: 100%;
    height: 9.75in;
    object-fit: contain;
    display: block;
    border-radius: 6px;
  }}
  .pdf-links-bar {{
    width: 100%;
    padding: 7px 14px;
    border-top: 1px solid #c6ff00;
    background: #07080b;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 9px;
  }}
  .pdf-links-bar a {{
    color: #c6ff00;
    text-decoration: none;
    font-weight: 700;
    letter-spacing: 0.08em;
  }}
</style>
</head>
<body>
  <div class="page">
    <img class="visual-hero" src="{visual_uri}" alt="Auditoría Antes vs Después {_esc(spec.business_name)}" />
    <div class="pdf-links-bar">
      <span>CAPTOORA SMALL BUSINESS 2027 · {_esc(spec.business_name.upper())} · -35% TEMPORADA</span>
      <div style="display:flex; gap:14px;">
        <a href="{_esc(spec.website_url)}">PORTAL 3D &amp; PORTFOLIO &rarr;</a>
        <a href="{_esc(spec.gallery_url)}">GALERÍAS EN VIVO &rarr;</a>
        <a href="{_esc(spec.whatsapp_url)}">ESCRIBIR POR WHATSAPP &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>"""


def _strip_data_uris(html_text: str) -> str:
    return re.sub(r"data:[^\"'\s>]+", "data:omitted", html_text)


def render_before_after_audit_png(spec: SmallBusinessSpec, output_path: Path) -> Path:
    """Render 1200x1500 Antes vs Después Google Maps/Meta audit visual via Chrome Headless."""
    validate_smb_spec(spec)
    html_content = _build_before_after_audit_html(spec)
    if validate_client_copy(_strip_data_uris(html_content)):
        raise ValueError("Antes/Después HTML contiene términos bloqueados por guardrail.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_html = Path(tmp_dir) / "smb_before_after.html"
        tmp_png = Path(tmp_dir) / "smb_before_after.png"
        tmp_html.write_text(html_content, encoding="utf-8")
        _run_chrome(
            [
                "--window-size=1200,1500",
                "--force-device-scale-factor=1",
                f"--screenshot={tmp_png}",
                tmp_html.as_uri(),
            ]
        )
        shutil.move(str(tmp_png), str(output_path))
    return output_path


def render_small_business_dossier_pdf(
    spec: SmallBusinessSpec,
    output_path: Path,
    *,
    before_after_png_path: Path | None = None,
) -> Path:
    """Render 1-page Letter PDF dossier for Captoora Small Business 2027."""
    validate_smb_spec(spec)
    temp_ba = None
    if before_after_png_path is None:
        temp_ba = output_path.with_suffix(".png")
        render_before_after_audit_png(spec, temp_ba)
        ba_path = temp_ba
    else:
        ba_path = before_after_png_path
        if not ba_path.exists():
            render_before_after_audit_png(spec, ba_path)

    html_content = _build_smb_dossier_pdf_html(spec, ba_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_html = Path(tmp_dir) / "smb_dossier.html"
        tmp_pdf = Path(tmp_dir) / "smb_dossier.pdf"
        tmp_html.write_text(html_content, encoding="utf-8")
        _run_chrome(
            [
                "--no-pdf-header-footer",
                f"--print-to-pdf={tmp_pdf}",
                tmp_html.as_uri(),
            ]
        )
        shutil.move(str(tmp_pdf), str(output_path))
    return output_path


_PROTO_FORBIDDEN_ORIGIN_TERMS = (
    "colinas de san jerónimo",
    "colinas de san jeronimo",
    "san jerónimo",
    "san jeronimo",
    "monterrey",
    "mty",
    "spgg",
    "san pedro garza",
)

_SOCIAL_ONLY_DOMAINS = (
    "instagram.com",
    "facebook.com",
    "fb.com",
    "linktr.ee",
    "wa.me",
    "tiktok.com",
    "api.whatsapp.com",
)


def _clean_wa_phone_digits(phone: str) -> str:
    """Normalize local/Mexican telephone strings into WhatsApp wa.me digits."""
    digits = "".join(ch for ch in (phone or "") if ch.isdigit())
    if len(digits) == 10:
        return f"52{digits}"
    return digits


def _detect_website_status(sitio_web: str, flags: set[str]) -> str:
    low = (sitio_web or "").strip().lower()
    if "SIN SITIO WEB" in flags or not low or "google.com/maps" in low:
        return "sin_web"
    if "RED PERSONAL EN RIESGO" in flags or any(dom in low for dom in _SOCIAL_ONLY_DOMAINS):
        return "solo_red_social"
    return "mejorable"


def _assert_origin_and_copy_clean(text: str, *, external_territory: bool, context: str) -> None:
    violations = validate_client_copy(text)
    if violations:
        raise ValueError(f"{context} contiene copy bloqueado por guardrail Captoora: {'; '.join(violations)}")
    if external_territory:
        low = text.lower()
        for term in _PROTO_FORBIDDEN_ORIGIN_TERMS:
            if term in low:
                raise ValueError(f"{context} filtró referencia geográfica externa no permitida ('{term}').")


def build_gbp_optimization_checklist(record: dict[str, Any]) -> dict[str, Any]:
    """Generate a tailored Google Business Profile update & web-upgrade checklist from a prospect record."""
    name = str(record.get("nombre") or record.get("slug") or "Negocio Local").strip()
    category = str(record.get("categoria") or "Negocio Local").strip()
    niche = str(record.get("nicho") or "").strip()
    profile = resolve_niche_profile(niche, name=name, category=category)
    municipio = str(record.get("municipio") or "Puerto Vallarta").strip()
    zona = str(record.get("zona") or municipio).strip()
    subzona = str(record.get("subzona") or zona).strip()
    external_territory = _is_non_nl_territory(municipio)

    flags_list = [str(f) for f in (record.get("audit_flags") or [])]
    flags = set(flags_list)
    score = int(record.get("audit_score") or 0)
    sitio_web = str(record.get("sitio_web") or "").strip()
    imgs = record.get("images_count")
    resenas = int(record.get("resenas") or 0)
    website_status = _detect_website_status(sitio_web, flags)

    tasks: list[dict[str, str]] = [
        {
            "area": "Verificación & Categorías Locales",
            "status": "critico" if "SIN RECLAMAR" in flags else "optimizar",
            "action": (
                f"Completar reclamo oficial en Google Business Profile para {name}, blindar propiedad, pin exacto y configurar categoría principal + secundarias ES/EN en {subzona}."
                if "SIN RECLAMAR" in flags
                else f"Auditar administradores activos, categoría principal ({category}) y atributos ES/EN en {subzona} para captar búsquedas de alta intención."
            ),
            "impact": "Evita ediciones externas y posiciona la ficha por giro real.",
        },
        {
            "area": "Sitio Web Express & Enlace Directo UTM",
            "status": "critico" if website_status in {"sin_web", "solo_red_social"} else "optimizar",
            "action": (
                f"Publicar Página Web Express propia con catálogo/reservas e insertarla en Google Maps (?utm_source=google_maps) — hoy la ficha no tiene sitio propio."
                if website_status == "sin_web"
                else (
                    f"Reemplazar enlace a red social ({sitio_web[:48]}) por Página Web Express rápida (sin exigir inicio de sesión) con botón WhatsApp."
                    if website_status == "solo_red_social"
                    else "Conectar Landing Express móvil de carga inmediata y botón WhatsApp visible desde el primer scroll."
                )
            ),
            "impact": "Convierte visitas del mapa en mensajes y reservas directas.",
        },
        {
            "area": "Portada & Galería Editorial en Maps",
            "status": "critico" if flags & {"CARRITO STREET VIEW", "0 FOTOS", "<=5 FOTOS"} else "optimizar",
            "action": (
                f"Reemplazar vista Street View / ficha sin portada curada cargando 20–40 fotografías editoriales de fachada, interiores y servicio con luz calibrada."
                if flags & {"CARRITO STREET VIEW", "0 FOTOS"}
                else (
                    f"Ampliar la galería ({imgs if imgs is not None else 'pocas'} fotos) a 20–40 fotografías profesionales geolocalizadas de espacio y equipo."
                    if "<=5 FOTOS" in flags
                    else f"Renovar fotografía de portada y servicios estelares con técnica editorial para elevar el porcentaje de clics frente a competidores de {zona}."
                )
            ),
            "impact": "Primera impresión visual sólida en búsquedas locales y turísticas.",
        },
        {
            "area": "Teléfono, WhatsApp Business & Horarios",
            "status": "critico" if "SIN TELÉFONO" in flags else "optimizar",
            "action": (
                f"Registrar teléfono comercial verificado en Google Business Profile, activar enlace directo a WhatsApp y cargar horarios extendidos de temporada."
                if "SIN TELÉFONO" in flags
                else f"Sincronizar horarios de temporada alta, días festivos y acceso directo a WhatsApp Business en ficha y página web."
            ),
            "impact": "Elimina llamadas perdidas y dudas de horario en visitantes.",
        },
        {
            "area": "Motor de Reseñas 5★ & Display LED QR",
            "status": "critico" if "POCAS RESEÑAS" in flags else "optimizar",
            "action": (
                f"Activar meta de reseñas recientes (actual: {resenas}) con placa acrílica LED QR personalizada en mostrador/recepción y protocolo de respuesta ES/EN <24h."
                if "POCAS RESEÑAS" in flags
                else f"Sostener flujo semanal de reseñas 5★ con placa acrílica LED QR en punto de contacto para blindar reputación en {zona}."
            ),
            "impact": "Aumenta relevancia local y confianza antes de reservar.",
        },
        {
            "area": "Meta Business Portfolio & Consistencia NAP",
            "status": "optimizar",
            "action": f"Unificar Facebook, Instagram y WhatsApp Business en un solo Meta Business Portfolio con nombre, dirección y teléfono idénticos a Google Maps.",
            "impact": "Operación comercial y publicitaria ordenada sin bloqueos.",
        },
    ]

    if score >= 40:
        priority_level = "Crítica"
    elif score >= 20:
        priority_level = "Alta"
    else:
        priority_level = "Estratégica"

    urgent_count = sum(1 for t in tasks if t["status"] == "critico")
    if website_status == "sin_web":
        headline = f"{name} aparece hoy sin página web propia en Google Maps ({urgent_count} ajustes críticos prioritarios)."
    elif website_status == "solo_red_social":
        headline = f"{name} dirige tráfico de Maps únicamente a red social; una Web Express propia + ajuste de ficha acelera reservas directas."
    else:
        headline = f"Ficha en {subzona} con {urgent_count} mejoras inmediatas detectadas para elevar reservas y confianza visual."

    payload = {
        "business_name": name,
        "slug": str(record.get("slug") or slugify(name)),
        "category": category,
        "niche": profile.niche_key,
        "zone": zona,
        "subzone": subzona,
        "priority_level": priority_level,
        "audit_score": score,
        "website_status": website_status,
        "website_current": sitio_web,
        "headline_diagnosis": headline,
        "urgent_count": urgent_count,
        "total_actions": len(tasks),
        "sla_note": "Entrega digital (Web Express + actualización GBP + fotografía): 48–72h. Display acrílico LED QR en taller artesanal: 3–5 días hábiles.",
        "tasks": tasks,
    }
    combined = " ".join([headline, *[t["action"] + " " + t["impact"] for t in tasks]])
    _assert_origin_and_copy_clean(combined, external_territory=external_territory, context="Checklist GBP")
    return payload


_PROTOTYPE_THEME_MAP: dict[str, dict[str, Any]] = {
    "Hoteles, Resorts & Beach Clubs": {
        "layout_mode": "split-stage",
        "direction": "Hospitalidad Costera Editorial",
        "hero_asset": "niche_heroes/pv_hospitality_resort.jpg",
        "bg": "#FBF8F3",
        "surface": "#F2ECE1",
        "surface_alt": "#FFFFFF",
        "ink": "#0E171D",
        "muted": "#4E5D66",
        "accent": "#9E6830",
        "accent_ink": "#FFFFFF",
        "border": "rgba(14, 23, 29, 0.13)",
        "font_display": "'Cormorant Garamond', Georgia, serif",
        "eyebrow": "ESTANCIA & RESERVA DIRECTA",
        "hero_sub": "Arquitectura costera, habitaciones iluminadas y reserva directa por WhatsApp sin comisiones ni demoras.",
        "cta_primary": "Consultar Disponibilidad",
        "cta_secondary": "Abrir en Google Maps",
        "highlights": (
            ("Reserva Directa sin Intermediarios", "Atención ágil por WhatsApp con confirmación en el momento en español e inglés."),
            ("Habitaciones, Alberca & Beach Club", "Galería real con colorimetría fiel de suites, terrazas y amenidades."),
            ("Ubicación & Concierge Local", "Pin exacto en mapa oficial, horarios de check-in y recomendaciones de zona."),
        ),
        "faq": (
            ("¿Cómo confirmo disponibilidad y tarifa directa?", "Escríbenos directo por WhatsApp desde esta página para recibir disponibilidad actualizada y atención personalizada sin recargos de plataforma."),
            ("¿Cuentan con recomendaciones de horarios y traslado?", "Sí, te compartimos referencias exactas desde Google Maps, acceso recomendado y tiempos aproximados en la bahía."),
        ),
    },
    "Restaurantes & Cafés Boutique": {
        "layout_mode": "pinned-poster",
        "direction": "Terraza & Cocina Editorial",
        "hero_asset": "niche_heroes/pv_gastronomy_terrace.jpg",
        "bg": "#FAF6EE",
        "surface": "#EFE8DA",
        "surface_alt": "#FFFFFF",
        "ink": "#1A1412",
        "muted": "#5D4F47",
        "accent": "#9E472A",
        "accent_ink": "#FFFFFF",
        "border": "rgba(26, 20, 18, 0.13)",
        "font_display": "'Cormorant Garamond', Georgia, serif",
        "eyebrow": "COCINA, CAFÉ & MESA DIRECTA",
        "hero_sub": "Mesa abierta, barra de especialidad y reservación directa para comidas, atardeceres o celebraciones privadas.",
        "cta_primary": "Reservar Mesa por WhatsApp",
        "cta_secondary": "Cómo Llegar en Maps",
        "highlights": (
            ("Platillos Insignia & Barra", "Presentación visual clara de menú, especialidades de temporada y bebidas."),
            ("Mesas, Grupos & Eventos", "Aparta mesa para desayunos, cenas o posadas con un mensaje directo."),
            ("Ubicación & Horario en Vivo", "Ruta directa en Google Maps con horarios actualizados para residentes y visitantes."),
        ),
        "faq": (
            ("¿Necesito reservación previa o manejan walk-ins?", "Recibimos visitas directas y reservaciones anticipadas por WhatsApp para asegurar mesa en horarios de mayor afluencia."),
            ("¿Pueden atender eventos privados o cenas de grupo?", "Sí, coordinamos mesas amplias, menú grupal y requerimientos alimenticios directo por WhatsApp."),
        ),
    },
    "Tiendas, Boutiques & Comercios": {
        "layout_mode": "editorial-report",
        "direction": "Vitrina & Lookbook de Galería",
        "hero_asset": "niche_heroes/niche_comercio_boutique.jpg",
        "bg": "#F7F5F0",
        "surface": "#EAE5DC",
        "surface_alt": "#FFFFFF",
        "ink": "#121212",
        "muted": "#59554D",
        "accent": "#8C6B28",
        "accent_ink": "#FFFFFF",
        "border": "rgba(18, 18, 18, 0.13)",
        "font_display": "'Cormorant Garamond', Georgia, serif",
        "eyebrow": "CURADURÍA & ATENCIÓN EN TIENDA",
        "hero_sub": "Piezas seleccionadas, asesoría directa por WhatsApp y vitrina verificada para ubicarnos a la primera.",
        "cta_primary": "Consultar Piezas por WhatsApp",
        "cta_secondary": "Ver Ubicación en Maps",
        "highlights": (
            ("Selección & Novedades", "Vitrina curada para conocer estilo, materiales y disponibilidad antes de visitarnos."),
            ("Atención Directa & Apartados", "Resuelve dudas de medidas, precios y existencia en minutos vía WhatsApp."),
            ("Visita en Corredor Comercial", "Ubicación exacta y horarios de temporada confirmados en Google Maps."),
        ),
        "faq": (
            ("¿Puedo preguntar disponibilidad antes de ir a la tienda?", "Sí, escríbenos por WhatsApp para confirmar piezas en existencia, tallas o envíos locales."),
            ("¿Cuáles son sus horarios de atención en tienda?", "Mantén horarios actualizados tanto aquí como en Google Business Profile para visitas entre semana y fines de semana."),
        ),
    },
    "Clínicas & Consultorios": {
        "layout_mode": "editorial-report",
        "direction": "Precisión Clínica & Confianza",
        "hero_asset": "niche_heroes/niche_clinica_dental.jpg",
        "bg": "#F4F7F6",
        "surface": "#E4ECE9",
        "surface_alt": "#FFFFFF",
        "ink": "#10242A",
        "muted": "#475F66",
        "accent": "#1F6355",
        "accent_ink": "#FFFFFF",
        "border": "rgba(16, 36, 42, 0.13)",
        "font_display": "'Plus Jakarta Sans', sans-serif",
        "eyebrow": "ATENCIÓN CLÍNICA & CITAS",
        "hero_sub": "Valoración clara, protocolos limpios y agenda directa por WhatsApp sin formularios complicados.",
        "cta_primary": "Agendar Cita por WhatsApp",
        "cta_secondary": "Ver Ubicación Clínica",
        "highlights": (
            ("Agenda Directa & Urgencias", "Confirmación de horarios y disponibilidad en minutos vía WhatsApp."),
            ("Instalaciones & Equipo Visible", "Espacios limpios, atención cálida y explicación honesta en español e inglés."),
            ("Ubicación & Reseñas Reales", "Acceso directo en Google Maps con opiniones verificadas de pacientes."),
        ),
        "faq": (
            ("¿Atienden consultas de primera vez y turismo de bienestar?", "Sí, coordinamos citas de diagnóstico y seguimiento con comunicación bilingüe y tiempos transparentes."),
            ("¿Cómo agendo o modifico una cita?", "Directamente por WhatsApp o teléfono oficial de la ficha en Google Maps."),
        ),
    },
    "Pádel & Raqueta": {
        "layout_mode": "split-stage",
        "direction": "Kinetic Club High Contrast",
        "hero_asset": "mockups/bases/padel_action_clean.jpg",
        "bg": "#090B10",
        "surface": "#131722",
        "surface_alt": "#1A2030",
        "ink": "#F4F5F2",
        "muted": "#9EA5B5",
        "accent": "#C6FF00",
        "accent_ink": "#090B10",
        "border": "rgba(255, 255, 255, 0.13)",
        "font_display": "'Cinzel', serif",
        "eyebrow": "CLUB DE RAQUETA & RESERVAS",
        "hero_sub": "Reserva pista, reta abierta o torneo de temporada en segundos con acceso directo en mapa.",
        "cta_primary": "Apartar Pista por WhatsApp",
        "cta_secondary": "Ubicación del Club",
        "highlights": (
            ("Renta de Pistas & Retas", "Consulta horarios disponibles de mañana, tarde y turno nocturno."),
            ("Torneos & Clínicas de Nivel", "Inscripción rápida para jugadores locales, visitantes y eventos corporativos."),
            ("Comunidad & Acceso Directo", "Pin verificado en Google Maps y comunicación directa sin intermediarios."),
        ),
        "faq": (
            ("¿Cómo reservo pista o pido pareja de juego?", "Envía un mensaje por WhatsApp indicando horario y nivel para asignarte disponibilidad al instante."),
            ("¿Organizan torneos y retas de temporada?", "Sí, publicamos convocatorias, cuadros y resultados directo para la comunidad del club."),
        ),
    },
    "Fitness & CrossFit": {
        "layout_mode": "split-stage",
        "direction": "Athletic Performance Dark Grid",
        "hero_asset": "niche_heroes/niche_fitness_gym.jpg",
        "bg": "#0A0C12",
        "surface": "#141824",
        "surface_alt": "#1C2132",
        "ink": "#F4F5F2",
        "muted": "#9EA5B5",
        "accent": "#C6FF00",
        "accent_ink": "#090B10",
        "border": "rgba(255, 255, 255, 0.13)",
        "font_display": "'Cinzel', serif",
        "eyebrow": "ENTRENAMIENTO & PASE DE PRUEBA",
        "hero_sub": "Horarios claros, coaches dedicados y clase muestra o pase diario reservable por WhatsApp.",
        "cta_primary": "Solicitar Pase de Prueba",
        "cta_secondary": "Ver Mapa y Horarios",
        "highlights": (
            ("Pase Diario & Visitas", "Ideal para miembros locales y viajeros que buscan entrenar sin trámites largos."),
            ("Programación & Coaching", "Acompañamiento técnico de fuerza, acondicionamiento y bienestar integral."),
            ("Ubicación & Comunidad Activa", "Llega directo por Google Maps con horarios precisos de apertura."),
        ),
        "faq": (
            ("¿Puedo agendar clase muestra o week pass?", "Sí, confirma tu horario favorito por WhatsApp para recibir bienvenida y accesos."),
            ("¿Qué horarios manejan entre semana y sábado?", "Publicamos horarios exactos en la ficha Google Maps y por atención directa en WhatsApp."),
        ),
    },
    "Baile & Danza Señoras": {
        "layout_mode": "split-stage",
        "direction": "Escenario & Movimiento Editorial",
        "hero_asset": "niche_heroes/niche_danza_studio.jpg",
        "bg": "#110E14",
        "surface": "#1B1620",
        "surface_alt": "#241E2B",
        "ink": "#F8F5F9",
        "muted": "#BFB6C9",
        "accent": "#E6C16E",
        "accent_ink": "#110E14",
        "border": "rgba(255, 255, 255, 0.14)",
        "font_display": "'Cormorant Garamond', Georgia, serif",
        "eyebrow": "ACADEMIA & CLASES ABIERTAS",
        "hero_sub": "Clases por nivel, comunidad cercana y reserva de sesión prueba en un clic por WhatsApp.",
        "cta_primary": "Reservar Clase Prueba",
        "cta_secondary": "Ubicación del Estudio",
        "highlights": (
            ("Grupos por Ritmo y Nivel", "Ambiente cómodo, guía clara y horarios matutinos o vespertinos."),
            ("Presentaciones & Comunidad", "Eventos de temporada, talleres y memorias visuales de alto nivel."),
            ("Acceso Verificado en Maps", "Llega sin contratiempos y consulta horarios reales en la ficha oficial."),
        ),
        "faq": (
            ("¿Necesito experiencia previa para inscribirme?", "No; te orientamos por WhatsApp hacia el grupo ideal según tu ritmo y horario."),
            ("¿Puedo tomar una clase prueba antes de mensualidad?", "Sí, apártala directo por WhatsApp desde esta página."),
        ),
    },
}


def _select_prototype_theme(profile: NicheProfile) -> dict[str, Any]:
    if profile.niche_key in _PROTOTYPE_THEME_MAP:
        return _PROTOTYPE_THEME_MAP[profile.niche_key]
    if profile.niche_key == "Deporte de Alto Rendimiento":
        return _PROTOTYPE_THEME_MAP["Pádel & Raqueta"]
    return {
        "layout_mode": "editorial-report",
        "direction": "Estudio Local Editorial",
        "hero_asset": "niche_heroes/niche_comercio_boutique.jpg",
        "bg": "#F8F6F1",
        "surface": "#ECE8DF",
        "surface_alt": "#FFFFFF",
        "ink": "#14161A",
        "muted": "#585E68",
        "accent": "#8E672E",
        "accent_ink": "#FFFFFF",
        "border": "rgba(20, 22, 26, 0.13)",
        "font_display": "'Cormorant Garamond', Georgia, serif",
        "eyebrow": "SERVICIO VERIFICADO & ATENCIÓN DIRECTA",
        "hero_sub": "Presencia clara en Google Maps, contacto directo por WhatsApp e imagen sólida para clientes locales y visitantes.",
        "cta_primary": "Escribir por WhatsApp",
        "cta_secondary": "Ver en Google Maps",
        "highlights": (
            ("Atención Directa & Clara", "Comunicación sin rodeos por WhatsApp para cotizar, agendar o resolver dudas."),
            ("Vitrina Visual Verificada", "Fotografía fiel del espacio, productos y equipo que transmite confianza inmediata."),
            ("Ubicación & Reseñas Locales", "Información precisa en Google Maps y horarios actualizados todo el año."),
        ),
        "faq": (
            ("¿Cómo solicito cotización o disponibilidad?", "Presiona el botón de WhatsApp para recibir atención directa con el equipo."),
            ("¿Dónde se ubican y en qué horario atienden?", "Revisa el bloque de ubicación abajo con dirección exacta y enlace directo a Google Maps."),
        ),
    }


def build_smb_landing_prototype_html(
    record: dict[str, Any],
    *,
    assets_prefix: str = "../../../assets",
    gbp_checklist: dict[str, Any] | None = None,
) -> str:
    """
    Build a bespoke, origin-clean, responsive Web Express landing page prototype +
    embedded Google Business Profile checklist & Captoora -35% offer sheet for any prospect.
    """
    checklist = gbp_checklist or build_gbp_optimization_checklist(record)
    name = str(record.get("nombre") or record.get("slug") or "Negocio Local").strip()
    category = str(record.get("categoria") or "Negocio Local").strip()
    niche = str(record.get("nicho") or "").strip()
    profile = resolve_niche_profile(niche, name=name, category=category)
    theme = _select_prototype_theme(profile)

    municipio = str(record.get("municipio") or "Puerto Vallarta").strip()
    zona = str(record.get("zona") or municipio).strip()
    subzona = str(record.get("subzona") or zona).strip()
    direccion = str(record.get("direccion") or f"{subzona}, {municipio}, México").strip()
    telefono = str(record.get("telefono") or "").strip()
    gmaps_url = str(record.get("gmaps_url") or "#ubicacion").strip()
    rating = record.get("rating")
    resenas = int(record.get("resenas") or 0)
    imgs_count = record.get("images_count")
    flags = [str(f) for f in (record.get("audit_flags") or [])]
    external_territory = _is_non_nl_territory(municipio)

    hero_rel = theme["hero_asset"]
    hero_abs = ROOT_DIR / "assets" / hero_rel
    if assets_prefix == "data_uri" and hero_abs.exists():
        hero_src = _file_data_uri(hero_abs)
    else:
        hero_src = f"{assets_prefix.rstrip('/')}/{hero_rel}"

    shot_rel = str(record.get("screenshot_path") or record.get("gmaps_screenshot") or "").strip()
    shot_abs = (ROOT_DIR / shot_rel) if shot_rel else None
    shot_src = ""
    if shot_abs is not None and shot_abs.exists():
        if assets_prefix == "data_uri":
            shot_src = _file_data_uri(shot_abs)
        elif assets_prefix.startswith("/"):
            shot_src = f"/{shot_rel.lstrip('/')}"
        else:
            root_up = assets_prefix.rstrip("/").rsplit("/assets", 1)[0]
            shot_src = f"{root_up}/{shot_rel.lstrip('/')}" if root_up else shot_rel

    biz_wa_digits = _clean_wa_phone_digits(telefono)
    biz_wa_msg = urllib.parse.quote(f"Hola equipo de {name}, vi su página desde Google Maps y me gustaría recibir información.")
    biz_wa_href = f"https://wa.me/{biz_wa_digits}?text={biz_wa_msg}" if biz_wa_digits else "#diagnostico-gbp"

    captoora_wa_msg = urllib.parse.quote(
        f"Hola Jesús Gutiérrez 👋 Vi la propuesta Web Express + actualización Google Maps para {name} ({subzona}, -35% temporada). Me interesa activarlo."
    )
    captoora_wa_href = f"https://wa.me/528140050088?text={captoora_wa_msg}"

    rating_badge = f"{rating} ★ · {resenas} reseñas verificadas" if rating is not None else f"{resenas} reseñas en Google Maps"
    photos_stat = f"{imgs_count} fotos" if imgs_count is not None else "Galería por verificar"

    tier1 = tuple(_neutralize_origin_text(p) for p in profile.tier1) if external_territory else profile.tier1
    tier2 = tuple(_neutralize_origin_text(p) for p in profile.tier2) if external_territory else profile.tier2
    tier3 = tuple(_neutralize_origin_text(p) for p in profile.tier3) if external_territory else profile.tier3

    highlights_html = "".join(
        f"""
        <article class="feature-card">
          <span class="feature-idx">0{i}</span>
          <h3>{_esc(title)}</h3>
          <p>{_esc(desc)}</p>
        </article>"""
        for i, (title, desc) in enumerate(theme["highlights"], start=1)
    )

    faq_html = "".join(
        f"""
        <details class="faq-item">
          <summary>{_esc(q)}</summary>
          <p>{_esc(a)}</p>
        </details>"""
        for q, a in theme["faq"]
    )

    flags_html = (
        "".join(f'<span class="audit-pill">{_esc(f)}</span>' for f in flags)
        if flags
        else '<span class="audit-pill ok">FICHA ACTIVA · LISTA PARA ELEVAR CONVERSIÓN</span>'
    )

    tasks_html = "".join(
        f"""
        <li class="task-row { 'is-crit' if t['status'] == 'critico' else 'is-opt' }">
          <div class="task-head">
            <span class="task-badge">{ 'PRIORIDAD ALTA' if t['status'] == 'critico' else 'MEJORA ESTRATÉGICA' }</span>
            <strong>{_esc(t['area'])}</strong>
          </div>
          <p>{_esc(t['action'])}</p>
          <span class="task-impact">Impacto: {_esc(t['impact'])}</span>
        </li>"""
        for t in checklist["tasks"]
    )

    tiers_html = "".join(
        f"""
        <div class="tier-card {'featured' if idx == 2 else ''}">
          <div class="tier-title">{_esc(t[0])}</div>
          <div class="tier-price"><span class="old">{_esc(t[1])}</span> <strong>{_esc(t[2])}</strong></div>
          <p class="tier-desc">{_esc(t[3])}</p>
        </div>"""
        for idx, t in enumerate((tier1, tier2, tier3), start=1)
    )

    shot_block = (
        f'<img class="maps-shot" src="{_esc(shot_src)}" alt="Estado actual de {_esc(name)} en Google Maps" loading="lazy" />'
        if shot_src
        else f'<div class="maps-shot-empty"><strong>{_esc(name)}</strong><span>Score de oportunidad visual: {checklist["audit_score"]}/100 · Abrir ficha directa en Google Maps para validar portada y galería.</span></div>'
    )

    is_dark = theme["bg"].startswith("#0") or theme["bg"].startswith("#1")
    studio_bg = "#0C0D12" if is_dark else "#11161C"
    studio_card = "#151822" if is_dark else "#1A212A"
    hero_badge_bg = "rgba(15, 20, 26, 0.72)"
    hero_overlay = "linear-gradient(125deg, rgba(10,14,18,0.68) 0%, rgba(10,14,18,0.22) 70%)"

    html_doc = f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_esc(name)} · {_esc(subzona)} — Propuesta Web Express &amp; Google Business Profile</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Cormorant+Garamond:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: {theme["bg"]};
      --surface: {theme["surface"]};
      --surface-alt: {theme["surface_alt"]};
      --ink: {theme["ink"]};
      --muted: {theme["muted"]};
      --accent: {theme["accent"]};
      --accent-ink: {theme["accent_ink"]};
      --border: {theme["border"]};
    }}
    html {{ scroll-behavior: smooth; max-width: 100%; overflow-x: hidden; }}
    body {{
      background: var(--bg);
      color: var(--ink);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      line-height: 1.55;
      max-width: 100%;
      overflow-x: hidden;
    }}
    img {{ max-width: 100%; }}
    .wrap {{ max-width: 1180px; width: 100%; margin: 0 auto; padding: 0 24px; }}
    .studio-ribbon {{
      position: sticky;
      top: 0;
      z-index: 40;
      background: rgba(12, 14, 20, 0.94);
      backdrop-filter: blur(10px);
      color: #F4F5F2;
      border-bottom: 1px solid rgba(212, 175, 55, 0.35);
      padding: 10px 0;
    }}
    .studio-ribbon-inner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      font-size: 0.78rem;
    }}
    .studio-tag {{
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 0.08em;
      color: #E8D5A8;
      text-transform: uppercase;
      overflow-wrap: break-word;
    }}
    .ribbon-links {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-weight: 700;
      font-size: 0.88rem;
      padding: 12px 20px;
      border-radius: 999px;
      text-decoration: none;
      border: 1px solid var(--border);
      transition: transform 0.16s ease, opacity 0.16s ease;
      cursor: pointer;
    }}
    .btn:hover {{ transform: translateY(-1px); }}
    .btn-sm {{ font-size: 0.75rem; padding: 7px 14px; }}
    .btn-accent {{
      background: var(--accent);
      color: var(--accent-ink);
      border-color: var(--accent);
    }}
    .btn-ghost {{
      background: transparent;
      color: var(--ink);
    }}
    .btn-gold {{
      background: #C6FF00;
      color: #090B10;
      border-color: #C6FF00;
    }}
    .btn-outline-light {{
      background: rgba(255,255,255,0.06);
      color: #F4F5F2;
      border-color: rgba(255,255,255,0.28);
    }}
    .brand-nav {{
      padding: 20px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
      border-bottom: 1px solid var(--border);
    }}
    .brand-name {{
      font-family: {theme["font_display"]};
      font-size: 1.45rem;
      font-weight: 700;
      letter-spacing: 0.01em;
    }}
    .brand-nav-links {{ display: flex; gap: 18px; align-items: center; flex-wrap: wrap; font-size: 0.88rem; color: var(--muted); }}
    .brand-nav-links a:not(.btn) {{ color: inherit; text-decoration: none; font-weight: 600; }}
    .brand-nav-links a.btn {{ text-decoration: none; }}
    .hero {{
      padding: 56px 0 64px;
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 40px;
      align-items: center;
    }}
    .hero > *, .info-grid > *, .audit-grid > * {{ min-width: 0; }}
    @media (max-width: 880px) {{ .hero {{ grid-template-columns: 1fr; padding: 36px 0 44px; }} }}
    @media (max-width: 640px) {{
      .wrap {{ padding: 0 16px; }}
      .hero {{ gap: 24px; padding: 28px 0 36px; }}
      .hero-media, .hero-media img {{ min-height: 250px; }}
      .hero-caption {{ flex-wrap: wrap; }}
    }}
    .eyebrow {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 12px;
      display: inline-block;
      overflow-wrap: break-word;
      max-width: 100%;
    }}
    h1 {{
      font-family: {theme["font_display"]};
      font-size: clamp(1.85rem, 4.4vw, 3.6rem);
      line-height: 1.08;
      letter-spacing: -0.02em;
      margin-bottom: 16px;
      overflow-wrap: break-word;
    }}
    .hero-sub {{
      font-size: 1.05rem;
      color: var(--muted);
      max-width: 56ch;
      margin-bottom: 24px;
    }}
    .hero-ctas {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }}
    .proof-strip {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      padding-top: 18px;
      border-top: 1px solid var(--border);
      font-size: 0.84rem;
      color: var(--muted);
    }}
    .proof-strip strong {{ color: var(--ink); }}
    .hero-media {{
      position: relative;
      border-radius: 22px;
      overflow: hidden;
      min-height: 400px;
      border: 1px solid var(--border);
      background: var(--surface);
      box-shadow: 0 24px 48px rgba(0,0,0,0.12);
    }}
    .hero-media img {{
      width: 100%;
      height: 100%;
      min-height: 400px;
      max-height: 520px;
      object-fit: cover;
      display: block;
    }}
    .hero-media::after {{
      content: "";
      position: absolute;
      inset: 0;
      background: {hero_overlay};
      pointer-events: none;
    }}
    .hero-caption {{
      position: absolute;
      left: 18px;
      right: 18px;
      bottom: 18px;
      z-index: 2;
      background: {hero_badge_bg};
      color: #F9F8F4;
      padding: 12px 16px;
      border-radius: 14px;
      backdrop-filter: blur(8px);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      font-size: 0.82rem;
    }}
    .section {{ padding: 64px 0; border-top: 1px solid var(--border); }}
    .section-head {{ max-width: 68ch; margin-bottom: 32px; }}
    .section-head h2 {{
      font-family: {theme["font_display"]};
      font-size: clamp(1.6rem, 2.8vw, 2.35rem);
      line-height: 1.14;
      margin-bottom: 10px;
    }}
    .section-head p {{ color: var(--muted); font-size: 0.96rem; }}
    .features-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}
    @media (max-width: 820px) {{ .features-grid {{ grid-template-columns: 1fr; }} }}
    .feature-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 24px;
    }}
    .feature-idx {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem;
      color: var(--accent);
      font-weight: 700;
      display: block;
      margin-bottom: 10px;
    }}
    .feature-card h3 {{ font-size: 1.1rem; margin-bottom: 8px; }}
    .feature-card p {{ font-size: 0.9rem; color: var(--muted); }}
    .info-grid {{
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 24px;
      align-items: start;
    }}
    @media (max-width: 820px) {{ .info-grid {{ grid-template-columns: 1fr; }} }}
    .loc-card {{
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 26px;
    }}
    .loc-row {{ padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 0.92rem; }}
    .loc-row:last-child {{ border-bottom: none; }}
    .loc-label {{ font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; text-transform: uppercase; color: var(--muted); display: block; }}
    .faq-list {{ display: flex; flex-direction: column; gap: 10px; }}
    .faq-item {{
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px 18px;
    }}
    .faq-item summary {{ font-weight: 700; cursor: pointer; font-size: 0.95rem; }}
    .faq-item p {{ margin-top: 10px; color: var(--muted); font-size: 0.88rem; }}

    /* Captoora Studio Backend GBP Audit & -35% Package Sheet */
    .studio-audit {{
      background: {studio_bg};
      color: #F4F5F2;
      padding: 72px 0;
      border-top: 3px solid #D4AF37;
    }}
    .audit-kicker {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
      letter-spacing: 0.16em;
      color: #C6FF00;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    .studio-audit h2 {{
      font-family: 'Cinzel', serif;
      font-size: clamp(1.55rem, 2.8vw, 2.3rem);
      color: #FFFFFF;
      margin-bottom: 10px;
    }}
    .audit-sub {{ color: #B4B6C2; max-width: 72ch; margin-bottom: 28px; font-size: 0.95rem; }}
    .audit-grid {{
      display: grid;
      grid-template-columns: 0.95fr 1.05fr;
      gap: 24px;
      align-items: start;
      margin-bottom: 32px;
    }}
    @media (max-width: 900px) {{ .audit-grid {{ grid-template-columns: 1fr; }} }}
    .audit-box {{
      background: {studio_card};
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 18px;
      padding: 22px;
    }}
    .maps-shot {{ width: 100%; border-radius: 12px; border: 1px solid rgba(255,255,255,0.14); display: block; margin: 12px 0; }}
    .maps-shot-empty {{
      background: rgba(255,255,255,0.04);
      border: 1px dashed rgba(255,255,255,0.22);
      border-radius: 12px;
      padding: 28px 18px;
      margin: 12px 0;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 0.86rem;
      color: #C4C6D0;
    }}
    .flags-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }}
    .audit-pill {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.69rem;
      padding: 4px 9px;
      border-radius: 6px;
      background: rgba(255, 107, 107, 0.14);
      border: 1px solid rgba(255, 107, 107, 0.4);
      color: #FFB6B6;
    }}
    .audit-pill.ok {{
      background: rgba(198,255,0,0.1);
      border-color: rgba(198,255,0,0.4);
      color: #C6FF00;
    }}
    .task-list {{ list-style: none; display: flex; flex-direction: column; gap: 10px; margin-top: 14px; }}
    .task-row {{
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.1);
      border-left: 3px solid #D4AF37;
      border-radius: 10px;
      padding: 12px 14px;
    }}
    .task-row.is-crit {{ border-left-color: #C6FF00; }}
    .task-head {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-bottom: 4px; font-size: 0.9rem; }}
    .task-badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      padding: 2px 7px;
      border-radius: 999px;
      background: rgba(212, 175, 55, 0.16);
      color: #E8D5A8;
    }}
    .task-row.is-crit .task-badge {{ background: rgba(198,255,0,0.16); color: #C6FF00; }}
    .task-row p {{ font-size: 0.84rem; color: #D7D8E0; }}
    .task-impact {{ display: block; margin-top: 4px; font-size: 0.76rem; color: #9C9FB0; }}
    .tiers-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin: 26px 0;
    }}
    @media (max-width: 880px) {{ .tiers-grid {{ grid-template-columns: 1fr; }} }}
    .tier-card {{
      background: {studio_card};
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 16px;
      padding: 20px;
    }}
    .tier-card.featured {{ border-color: #C6FF00; box-shadow: 0 0 0 1px rgba(198,255,0,0.25); }}
    .tier-title {{ font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #E8D5A8; margin-bottom: 8px; }}
    .tier-price {{ font-size: 1.5rem; margin-bottom: 8px; display: flex; align-items: baseline; gap: 10px; }}
    .tier-price .old {{ font-size: 0.9rem; text-decoration: line-through; color: #8A8D9E; }}
    .tier-price strong {{ color: #C6FF00; }}
    .tier-desc {{ font-size: 0.84rem; color: #C6C8D4; }}
    .studio-footer {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding-top: 22px;
      border-top: 1px solid rgba(255,255,255,0.12);
      font-size: 0.82rem;
      color: #A6A8B8;
    }}
  </style>
</head>
<body>
  <div class="studio-ribbon">
    <div class="wrap studio-ribbon-inner">
      <span class="studio-tag">PROTOTIPO WEB EXPRESS &amp; AUDITORÍA GOOGLE MAPS · {_esc(subzona.upper())} · {_esc(theme["direction"].upper())}</span>
      <div class="ribbon-links">
        <a class="btn btn-sm btn-outline-light" href="#diagnostico-gbp">Checklist Google Maps ({checklist["urgent_count"]} alertas)</a>
        <a class="btn btn-sm btn-gold" href="{_esc(captoora_wa_href)}" target="_blank">Activar Web + Maps (-35%) &rarr;</a>
      </div>
    </div>
  </div>

  <header class="wrap brand-nav">
    <div class="brand-name">{_esc(name)}</div>
    <nav class="brand-nav-links">
      <a href="#experiencia">Servicios</a>
      <a href="#ubicacion">Ubicación</a>
      <a href="#diagnostico-gbp">Diagnóstico Maps (-35%)</a>
      <a class="btn btn-sm btn-accent" href="{_esc(biz_wa_href)}" target="{ '_blank' if biz_wa_digits else '_self' }">{_esc(theme["cta_primary"])}</a>
    </nav>
  </header>

  <main>
    <section class="wrap hero">
      <div>
        <span class="eyebrow">{_esc(theme["eyebrow"])} · {_esc(subzona)}</span>
        <h1>{_esc(name)}</h1>
        <p class="hero-sub">{_esc(theme["hero_sub"])}</p>
        <div class="hero-ctas">
          <a class="btn btn-accent" href="{_esc(biz_wa_href)}" target="{ '_blank' if biz_wa_digits else '_self' }">{_esc(theme["cta_primary"])}</a>
          <a class="btn btn-ghost" href="{_esc(gmaps_url)}" target="_blank">{_esc(theme["cta_secondary"])} &rarr;</a>
        </div>
        <div class="proof-strip">
          <span><strong>{_esc(category)}</strong></span>
          <span>&bull; <strong>{_esc(rating_badge)}</strong></span>
          <span>&bull; {_esc(subzona)}, {_esc(municipio)}</span>
        </div>
      </div>
      <div class="hero-media">
        <img src="{_esc(hero_src)}" alt="{_esc(name)} — propuesta visual editorial en {_esc(subzona)}" />
        <div class="hero-caption">
          <span><strong>{_esc(subzona)}</strong> · {_esc(category)}</span>
          <span>{_esc(rating_badge)}</span>
        </div>
      </div>
    </section>

    <section id="experiencia" class="section">
      <div class="wrap">
        <div class="section-head">
          <span class="eyebrow">EXPERIENCIA DIRECTA SIN FRICCIÓN</span>
          <h2>Diseñada para convertir búsquedas en visitas y reservas reales</h2>
          <p>En lugar de depender únicamente de redes sociales o portales externos, {_esc(name)} proyecta identidad propia desde el primer clic en Google Maps.</p>
        </div>
        <div class="features-grid">
          {highlights_html}
        </div>
      </div>
    </section>

    <section id="ubicacion" class="section">
      <div class="wrap info-grid">
        <div class="loc-card">
          <span class="eyebrow">FICHA DE CONTACTO &amp; RUTA OFICIAL</span>
          <h2 style="font-family:{theme['font_display']}; font-size:1.85rem; margin-bottom:14px;">Visita o contacta a {_esc(name)}</h2>
          <div class="loc-row"><span class="loc-label">Dirección verificada</span>{_esc(direccion)}</div>
          <div class="loc-row"><span class="loc-label">Teléfono / WhatsApp comercial</span>{_esc(telefono or "Pendiente de verificación oficial en Google Business Profile")}</div>
          <div class="loc-row"><span class="loc-label">Zona &amp; Municipio</span>{_esc(subzona)} · {_esc(municipio)}</div>
          <div class="loc-row"><span class="loc-label">Reputación actual</span>{_esc(rating_badge)} · {_esc(photos_stat)}</div>
          <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:18px;">
            <a class="btn btn-accent" href="{_esc(gmaps_url)}" target="_blank">Abrir en Google Maps &rarr;</a>
            <a class="btn btn-ghost" href="{_esc(biz_wa_href)}" target="{ '_blank' if biz_wa_digits else '_self' }">Contacto Directo</a>
          </div>
        </div>
        <div>
          <span class="eyebrow">PREGUNTAS FRECUENTES DE CLIENTES</span>
          <div class="faq-list">
            {faq_html}
          </div>
        </div>
      </div>
    </section>
  </main>

  <section id="diagnostico-gbp" class="studio-audit">
    <div class="wrap">
      <div class="audit-kicker">RESPALDO CAPTOORA STUDIO · ACTUALIZACIÓN GOOGLE BUSINESS PROFILE + WEB EXPRESS</div>
      <h2>Hoja de Ruta Google Maps &amp; Lanzamiento para {_esc(name)}</h2>
      <p class="audit-sub">{_esc(checklist["headline_diagnosis"])} Prioridad detectada: <strong>{_esc(checklist["priority_level"])} ({checklist["audit_score"]}/100)</strong>.</p>

      <div class="audit-grid">
        <div class="audit-box">
          <strong style="font-size:0.98rem;">1. Estado actual detectado en Google Maps</strong>
          {shot_block}
          <div class="flags-row">{flags_html}</div>
          <p style="font-size:0.8rem; color:#B0B3C2; margin-top:12px;">{ _esc(checklist["sla_note"]) }</p>
        </div>
        <div class="audit-box">
          <strong style="font-size:0.98rem;">2. Checklist personalizado de actualización GBP ({checklist["total_actions"]} puntos)</strong>
          <ul class="task-list">
            {tasks_html}
          </ul>
        </div>
      </div>

      <div class="audit-kicker">ESQUEMAS DISPONIBLES CAPTOORA SMALL BUSINESS · -35% VIGENTE</div>
      <div class="tiers-grid">
        {tiers_html}
      </div>

      <div class="studio-footer">
        <div>
          <strong>Jesús Gutiérrez</strong> · Fotógrafo y Director · Captoora Studio<br>
          <span>Portafolio, técnica y resultados: <a href="https://captoora.studio/sports" style="color:#E8D5A8;">https://captoora.studio/sports</a> · chuy@captoora.studio · +52 81 4005 0088</span>
        </div>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
          <a class="btn btn-gold" href="{_esc(captoora_wa_href)}" target="_blank">Activar Página + Google Maps con Jesús Gutiérrez &rarr;</a>
        </div>
      </div>
    </div>
  </section>
</body>
</html>"""

    _assert_origin_and_copy_clean(_strip_data_uris(html_doc), external_territory=external_territory, context=f"Prototipo HTML ({name})")
    return html_doc


def build_self_test_plain_summary(spec: MockupSpec) -> str:
    """Create verified plain-text checklist body for email/WhatsApp self-tests (zero AI mentions)."""
    return (
        f"Hola equipo de {spec.club_name},\n\n"
        f"Preparamos su propuesta personalizada para {spec.tournament_name} · {spec.season_label} "
        f"con -35% Descuento de Temporada activo y tres esquemas a elegir (sin paquete único obligatorio):\n\n"
        f"1) Opción 1 · Solo Digital ($4,900 -> $3,185 MXN): Cobertura 1/2000s + galería mismo día ({spec.gallery_url}) para proyectar imagen profesional.\n"
        f"2) Opción 2 · Foto + Impresión / Marcos ($7,900 -> $5,135 MXN): Digital mismo día + impresiones Fine Art / marcos en 2do momento opcional.\n"
        f"3) Opción 3 · Suite Full + Ads & Acrílicos LED ($11,500 -> $7,475 MXN): Cobertura + Reels Meta Ads + 4 placas LED + 20 llaveros (pago físico en 2do momento).\n\n"
        f"Programa Piloto · Captoora Biogen (Beta · -35%): Seguimiento fotográfico escultórico de evolución física en estudio "
        f"(semanal, quincenal, mensual o bimestral · 3 a 60 meses, desde $1,950 -> $1,268 MXN/mes).\n\n"
        f"Nueva Línea · Captoora Small Business ('Arranca 2027 · -35%'):\n"
        f"• SMB Impulso Google Maps ($6,000 -> $3,900 MXN): Fotos pro + reclamo oficial + carga directa en ficha Maps.\n"
        f"• SMB Suite Total ($10,600 -> $6,890 MXN): Foto + Reels + Maps + Setup Meta Business Portfolio (FB+IG+WA sin bloqueos).\n"
        f"• SMB Posicionamiento + QR LED / Biogen ($16,000 -> $10,400 MXN): Placa LED en 2do momento opcional.\n\n"
        f"Portal 3D & Portafolio Sports: {spec.website_url}\n"
        f"Galerías en vivo: {spec.gallery_url}\n"
        f"Respaldo institucional: Coca-Cola FEMSA · Heineken / Tecate · Poder Judicial de Nuevo León\n\n"
        f"*Entrega digital el mismo día · Acrílicos LED y marcos en taller MTY/SPGG: 3 a 5 días hábiles.\n\n"
        f"— {spec.director_name} | {spec.director_role}\n"
        f"WhatsApp: {spec.whatsapp_display} · {spec.email_address} · {spec.instagram_handle}\n"
        f"{spec.address_line}"
    )


def build_complete_eml_bundle(
    spec: MockupSpec,
    *,
    html_body_path: Path,
    attachments: list[Path],
    to_email: str = "ponchogf88@me.com",
    output_path: Path,
) -> Path:
    """Build an RFC-2822 .eml email bundle with HTML body and PDF/PNG attachments."""
    validate_mockup_spec(spec)
    plain_text = build_self_test_plain_summary(spec)
    if validate_client_copy(plain_text):
        raise ValueError("Guardrail failed on plain summary")

    msg = EmailMessage()
    msg["Subject"] = (
        f"Captoora Studio 2026 (-35% Temporada) · 3 Opciones + Biogen Beta + Small Business 2027 ({spec.club_name})"
    )
    msg["From"] = f"{spec.director_name} <{to_email}>"
    msg["To"] = to_email
    msg.set_content(plain_text)
    msg.add_alternative(html_body_path.read_text(encoding="utf-8"), subtype="html")

    for att in attachments:
        if not att.exists():
            continue
        ctype, _ = mimetypes.guess_type(str(att))
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        msg.add_attachment(
            att.read_bytes(),
            maintype=maintype,
            subtype=subtype,
            filename=att.name,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(msg.as_bytes())
    return output_path


def render_mockup_png(
    spec: MockupSpec,
    variant: Literal["A", "B"],
    output_path: Path,
) -> Path:
    """Render Option A or Option B 1080x1350 PNG mockup via Chrome Headless."""
    validate_mockup_spec(spec)
    html_content = _build_option_a_html(spec) if variant == "A" else _build_option_b_html(spec)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_html = Path(tmp_dir) / f"mockup_{variant}.html"
        tmp_png = Path(tmp_dir) / f"mockup_{variant}.png"
        tmp_html.write_text(html_content, encoding="utf-8")
        _run_chrome(
            [
                "--window-size=1080,1350",
                "--force-device-scale-factor=1",
                f"--screenshot={tmp_png}",
                tmp_html.as_uri(),
            ]
        )
        shutil.move(str(tmp_png), str(output_path))
    return output_path


def render_dossier_pdf(
    spec: MockupSpec,
    mockup_a_path: Path,
    mockup_b_path: Path,
    output_path: Path,
) -> Path:
    """Render a strictly 1-page Letter executive dossier PDF with embedded mockups and live links."""
    validate_mockup_spec(spec)
    html_content = _build_dossier_pdf_html(spec, mockup_a_path, mockup_b_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_html = Path(tmp_dir) / "dossier.html"
        tmp_pdf = Path(tmp_dir) / "dossier.pdf"
        tmp_html.write_text(html_content, encoding="utf-8")
        _run_chrome(
            [
                "--no-pdf-header-footer",
                f"--print-to-pdf={tmp_pdf}",
                tmp_html.as_uri(),
            ]
        )
        shutil.move(str(tmp_pdf), str(output_path))
    return output_path


def render_email_templates(spec: MockupSpec, output_dir: Path) -> dict[str, Path]:
    """Write dark/light responsive HTML emails plus standalone horizontal signature matching Captoora Studio identity."""
    validate_mockup_spec(spec)
    output_dir.mkdir(parents=True, exist_ok=True)
    dark_path = output_dir / "Captoora_Email_Oscuro_Navidad2026.html"
    light_path = output_dir / "Captoora_Email_Claro_Navidad2026.html"
    sig_path = output_dir / "Captoora_Firma_Horizontal_2026.html"
    dark_path.write_text(_build_email_html(spec, theme="dark"), encoding="utf-8")
    light_path.write_text(_build_email_html(spec, theme="light"), encoding="utf-8")
    sig_path.write_text(_build_signature_html(spec), encoding="utf-8")
    return {
        "email_dark": dark_path,
        "email_light": light_path,
        "signature_html": sig_path,
    }


def generate_self_test_bundle(to_email: str = "ponchogf88@me.com") -> dict[str, Path]:
    """Generate Option A/B PNGs, Navidad -35% Dossier PDF, Small Business Antes/Después PNG+PDF, Emails, Signature, and .eml."""
    test_dir = MOCKUPS_DIR / "test"
    spec = MockupSpec(
        club_name="Cuatro Padel",
        tournament_name="Torneo del Pavo",
        season_label="NAVIDAD 2026 · -35% TEMPORADA",
        year="2026",
        category_label="CAMPEÓN · EDICIÓN 2026",
        sponsor_label="TU MARCA AQUÍ · 2026",
        city_label="MONTERREY · SAN PEDRO",
    )
    out_a = test_dir / "Mockup_Prueba_OpcA_Navidad2026.png"
    out_b = test_dir / "Mockup_Prueba_OpcB_AccionLED_2026.png"
    out_pdf = test_dir / "Captoora_Dossier_Prueba_Navidad2026.pdf"
    out_eml = test_dir / "Captoora_Autoprueba_Completa_2026.eml"

    # Find an actual captured Google Maps screenshot if present (e.g., Pádel del Norte or first available)
    audits_dir = ROOT_DIR / "assets" / "gmaps_audits"
    preferred_shots = [
        audits_dir / "padel_del_norte.png",
        audits_dir / "ejercicios_crossfit.png",
        audits_dir / "evilfit.png",
    ]
    sample_shot = next((p for p in preferred_shots if p.exists()), None)
    if sample_shot is None and audits_dir.exists():
        any_pngs = sorted(audits_dir.glob("*.png"))
        sample_shot = any_pngs[0] if any_pngs else None

    smb_spec = SmallBusinessSpec(
        business_name="Pádel del Norte",
        category_label="Club Deportivo · San Pedro Garza García",
        city_label="SAN PEDRO · MONTERREY",
        maps_screenshot_path=sample_shot,
        rating_label="Google Maps · Street View detectado",
        observations=(
            "Tu portada actual en Google Maps muestra la vista automática de Street View en lugar de tus canchas e instalaciones.",
            "La ficha aún muestra 'Agregar número de teléfono' y no cuenta con sitio web o catálogo comercial enlazado.",
            "Configuramos Meta Business Portfolio (FB + IG + WhatsApp Business) para vender sin riesgo de bloqueos en 2027.",
        ),
    )
    out_smb_ba = test_dir / "Captoora_SmallBusiness_AntesDespues_2027.png"
    out_smb_pdf = test_dir / "Captoora_SmallBusiness_Dossier_2027.pdf"

    render_mockup_png(spec, "A", out_a)
    render_mockup_png(spec, "B", out_b)
    render_dossier_pdf(spec, out_a, out_b, out_pdf)
    render_before_after_audit_png(smb_spec, out_smb_ba)
    render_small_business_dossier_pdf(smb_spec, out_smb_pdf, before_after_png_path=out_smb_ba)
    emails = render_email_templates(spec, test_dir)
    build_complete_eml_bundle(
        spec,
        html_body_path=emails["email_dark"],
        attachments=[out_pdf, out_smb_pdf, out_smb_ba, out_a, out_b, emails["signature_html"]],
        to_email=to_email,
        output_path=out_eml,
    )
    return {
        "option_a": out_a,
        "option_b": out_b,
        "dossier_pdf": out_pdf,
        "smb_before_after_png": out_smb_ba,
        "smb_dossier_pdf": out_smb_pdf,
        "eml_bundle": out_eml,
        **emails,
    }


def build_club_mockup_spec(record: dict[str, Any]) -> MockupSpec:
    """Build an individualized 2026 Navidad MockupSpec for a Pádel, Danza, School, or Sports club."""
    name = str(record.get("nombre") or record.get("club_name") or "Club Deportivo").strip()
    niche = str(record.get("nicho") or "").strip()
    category = str(record.get("categoria") or "").strip()
    profile = resolve_niche_profile(niche, name=name, category=category)
    logo_path = resolve_club_logo_path(name, record.get("logo"))
    municipio = str(record.get("municipio") or "Monterrey").strip()
    zona = str(record.get("zona") or "").strip()
    city_label = _format_city_label(zona, municipio)

    if profile.niche_key == "Baile & Danza Señoras":
        return MockupSpec(
            club_name=name,
            tournament_name="Gala Navideña de Danza",
            season_label="NAVIDAD 2026",
            year="2026",
            category_label="GALA OFICIAL · 2026",
            sponsor_label="MARCA ALIADA / RECEPCIÓN 2026",
            city_label=city_label,
            package_label="GALA WHITE-GLOVE + TROFEOS ACRÍLICO LED",
            hero_photo_path=profile.hero_path,
            acrylic_base_path=DANCE_ACRYLIC_BLANK_PATH,
            plate_style="dance",
            club_logo_path=logo_path,
            header_brand_title="CAPTOORA DANZA",
            hero_metrics=("ESCENARIO LUZ CÁLIDA", "REELS DE COREOGRAFÍA", "GALERÍA MISMO DÍA"),
            extra_card=(
                "OPCIÓN WHITE-GLOVE · FAMILIAS (-35%)",
                "$2,400",
                "$1,560 /cuadro",
                "Galería privada por alumna y marcos finos para papás liquidables en 2do momento.",
            ),
        )

    is_school = profile.niche_key in {"Colegios Privados Élite", "Colegios & Jardines de Niños"}
    tourney = (
        "Festival & Copa Invierno"
        if is_school
        else ("Torneo del Pavo & Posada" if profile.niche_key == "Pádel & Raqueta" else "Copa Navidad & Premiación")
    )
    extra_card = (
        (
            "COPA + ANUARIO PRIVADO (-35%)",
            "$11,500",
            "$7,475 MXN",
            "Galería escolar con contraseña para familias + reconocimientos LED en base de nogal.",
        )
        if is_school
        else (
            "ESQUEMA PATROCINADO · -35%",
            "$11,500",
            "$0 neto club*",
            "Integración de patrocinadores en placas acrílicas LED y galería para autofinanciar tu copa.",
        )
    )
    return MockupSpec(
        club_name=name,
        tournament_name=tourney,
        season_label="NAVIDAD 2026",
        year="2026",
        category_label="CAMPEÓN · EDICIÓN 2026",
        sponsor_label="TU PATROCINADOR AQUÍ · 2026",
        city_label=city_label,
        package_label="HALFTIME BLITZ + TROFEOS ACRÍLICO LED",
        hero_photo_path=profile.hero_path if profile.hero_path.exists() else PADEL_ACTION_PATH,
        acrylic_base_path=ACRYLIC_BLANK_PATH,
        plate_style="padel",
        club_logo_path=logo_path,
        header_brand_title="CAPTOORA SPORTS",
        hero_metrics=("RAW 1/2000s", "REELS VERTICALES", "CERO LOGÍSTICA EXTRA"),
        extra_card=extra_card,
    )


def _find_free_port() -> int:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


async def _batch_render_cdp_async(
    smb_records: list[dict[str, Any]],
    club_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Render every prospect SMB Before/After PNG + Letter PDF and club Navidad kits via 1 Chrome CDP session."""
    import asyncio
    import json
    import urllib.request
    import websockets

    if not CHROME_BIN.exists():
        raise FileNotFoundError(f"No se encontró Google Chrome en {CHROME_BIN}")

    smb_dir = MOCKUPS_DIR / "small_biz"
    clubs_dir = MOCKUPS_DIR / "clubs"
    smb_dir.mkdir(parents=True, exist_ok=True)
    clubs_dir.mkdir(parents=True, exist_ok=True)

    port = _find_free_port()
    user_data_dir = tempfile.mkdtemp(prefix="captoora_render_cdp_")
    tmp_html_dir = Path(tempfile.mkdtemp(prefix="captoora_html_cdp_"))
    tmp_html = tmp_html_dir / "stage.html"

    proc = subprocess.Popen(
        [
            str(CHROME_BIN),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            "--no-first-run",
            "--no-default-browser-check",
            f"--remote-debugging-port={port}",
            f"--user-data-dir={user_data_dir}",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    smb_rendered = 0
    clubs_rendered = 0
    errors: list[str] = []

    try:
        ws_url = ""
        for _ in range(45):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=1.5) as resp:
                    targets = json.loads(resp.read().decode("utf-8"))
                page_target = next((t for t in targets if t.get("type") == "page"), None)
                if page_target and page_target.get("webSocketDebuggerUrl"):
                    ws_url = page_target["webSocketDebuggerUrl"]
                    break
            except Exception:
                await asyncio.sleep(0.2)
        if not ws_url:
            raise RuntimeError("No se pudo conectar al WebSocket CDP de Chrome para lote de dossiers.")

        req_counter = 1
        doc_counter = 0
        current_vp: tuple[int, int] | None = None

        async def cdp_send(ws: Any, method: str, params: dict[str, Any] | None = None, *, wait_load: bool = False) -> dict[str, Any]:
            nonlocal req_counter
            cid = req_counter
            req_counter += 1
            await ws.send(json.dumps({"id": cid, "method": method, "params": params or {}}))
            result: dict[str, Any] = {}
            saw_reply = False
            saw_load = not wait_load
            while not (saw_reply and saw_load):
                raw = await asyncio.wait_for(ws.recv(), timeout=30.0)
                msg = json.loads(raw)
                if msg.get("id") == cid:
                    if "error" in msg:
                        raise RuntimeError(f"CDP {method} error: {msg['error']}")
                    result = msg.get("result", {})
                    saw_reply = True
                elif wait_load and msg.get("method") == "Page.loadEventFired":
                    saw_load = True
            return result

        async def load_html(ws: Any, html_str: str) -> Path:
            nonlocal doc_counter
            doc_counter += 1
            page_path = tmp_html_dir / f"doc_{doc_counter}.html"
            page_path.write_text(html_str, encoding="utf-8")
            await cdp_send(ws, "Page.navigate", {"url": page_path.as_uri()}, wait_load=True)
            await cdp_send(
                ws,
                "Runtime.evaluate",
                {
                    "expression": "(async () => { await document.fonts.ready; await Promise.all(Array.from(document.images).map(i => i.complete ? null : new Promise(r => { i.onload = r; i.onerror = r; }))); return true; })()",
                    "awaitPromise": True,
                },
            )
            return page_path

        async def render_png(ws: Any, html_str: str, out_path: Path, width: int, height: int) -> None:
            nonlocal current_vp
            if current_vp != (width, height):
                await cdp_send(
                    ws,
                    "Emulation.setDeviceMetricsOverride",
                    {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False},
                )
                current_vp = (width, height)
            page_path = await load_html(ws, html_str)
            try:
                shot = await cdp_send(ws, "Page.captureScreenshot", {"format": "png", "fromSurface": True})
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(base64.b64decode(shot["data"]))
            finally:
                page_path.unlink(missing_ok=True)

        async def render_pdf(ws: Any, html_str: str, out_path: Path) -> None:
            page_path = await load_html(ws, html_str)
            try:
                pdf = await cdp_send(
                    ws,
                    "Page.printToPDF",
                    {"printBackground": True, "preferCSSPageSize": True, "transferMode": "ReturnAsBase64"},
                )
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(base64.b64decode(pdf["data"]))
            finally:
                page_path.unlink(missing_ok=True)

        async with websockets.connect(ws_url, max_size=None) as ws:
            await cdp_send(ws, "Page.enable")
            await cdp_send(ws, "Runtime.enable")

            for rec in smb_records:
                slug = str(rec.get("slug") or slugify(str(rec.get("nombre") or "negocio")))
                try:
                    spec = build_small_business_spec_from_record(rec, hero_override="auto")
                    validate_smb_spec(spec)
                    ba_html = _build_before_after_audit_html(spec)
                    if validate_client_copy(_strip_data_uris(ba_html)):
                        raise ValueError("Guardrail bloqueó HTML Antes/Después")
                    ba_path = smb_dir / f"{slug}_AntesDespues_2027.png"
                    pdf_path = smb_dir / f"{slug}_Dossier_SMB_2027.pdf"
                    await render_png(ws, ba_html, ba_path, 1200, 1500)
                    pdf_html = _build_smb_dossier_pdf_html(spec, ba_path)
                    await render_pdf(ws, pdf_html, pdf_path)
                    rec["before_after_path"] = f"assets/mockups/small_biz/{slug}_AntesDespues_2027.png"
                    rec["dossier_pdf_path"] = f"assets/mockups/small_biz/{slug}_Dossier_SMB_2027.pdf"
                    smb_rendered += 1
                except Exception as exc:
                    errors.append(f"{slug}: {exc}")

            for crec in (club_records or []):
                slug = str(crec.get("slug") or slugify(str(crec.get("nombre") or "club")))
                try:
                    cspec = build_club_mockup_spec(crec)
                    validate_mockup_spec(cspec)
                    cdir = clubs_dir / slug
                    out_a = cdir / f"{slug}_OpcA_Navidad2026.png"
                    out_b = cdir / f"{slug}_OpcB_EditorialLED_2026.png"
                    out_pdf = cdir / f"{slug}_Dossier_Navidad2026.pdf"
                    await render_png(ws, _build_option_a_html(cspec), out_a, 1080, 1350)
                    await render_png(ws, _build_option_b_html(cspec), out_b, 1080, 1350)
                    await render_pdf(ws, _build_dossier_pdf_html(cspec, out_a, out_b), out_pdf)
                    clubs_rendered += 1
                except Exception as exc:
                    errors.append(f"club:{slug}: {exc}")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.rmtree(user_data_dir, ignore_errors=True)
        shutil.rmtree(tmp_html_dir, ignore_errors=True)

    return {
        "smb_rendered": smb_rendered,
        "clubs_rendered": clubs_rendered,
        "errors": errors,
    }


def batch_render_personalized_assets_cdp(
    smb_records: list[dict[str, Any]],
    club_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Synchronous entry point to batch-render personalized PNGs & PDFs across all prospects."""
    import asyncio

    return asyncio.run(_batch_render_cdp_async(smb_records, club_records))


def main() -> None:
    parser = argparse.ArgumentParser(description="Renderizador de mockups y dossiers Captoora.")
    parser.add_argument("--test", "--self-test", action="store_true", help="Genera el paquete de autoprueba completo (-35%%, 3 Opciones, Biogen Beta, Small Business).")
    args = parser.parse_args()
    if args.test:
        bundle = generate_self_test_bundle()
        for key, path in bundle.items():
            print(f"{key}: {path}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
