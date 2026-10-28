#!/usr/bin/env python3
"""Valida el registro maestro y prepara la cola verificable de producción diaria."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
REGISTER = ROOT / "REGISTRO_MAESTRO_PIEZAS.csv"
REPORTS = ROOT / "reportes-diarios"
VALID_STATES = {"rechazado", "piloto_existente", "referencia", "planificado", "en_produccion", "revision", "listo", "publicado"}
VALID_DECISIONS = {"conservar", "mejorar", "actualizar", "desechar", "crear"}
ACTIONABLE = {"mejorar": 0, "actualizar": 1, "crear": 2}


def load_rows() -> list[dict[str, str]]:
    with REGISTER.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("El registro maestro está vacío.")
    ids = [row["id"].strip() for row in rows]
    duplicates = [key for key, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise SystemExit(f"IDs duplicados: {', '.join(duplicates)}")
    errors = []
    for row in rows:
        if row["estado"] not in VALID_STATES:
            errors.append(f'{row["id"]}: estado inválido {row["estado"]}')
        if row["decision_editorial"] not in VALID_DECISIONS:
            errors.append(f'{row["id"]}: decisión inválida {row["decision_editorial"]}')
        for required in ("titulo", "descripcion_actual", "accion_descripcion", "herramientas_reales", "siguiente_accion"):
            if not row[required].strip():
                errors.append(f'{row["id"]}: falta {required}')
    if errors:
        raise SystemExit("\n".join(errors))
    return rows


def select_queue(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    candidates = [row for row in rows if row["decision_editorial"] in ACTIONABLE and row["estado"] != "listo"]
    candidates.sort(key=lambda row: (ACTIONABLE[row["decision_editorial"]], row["id"]))
    return candidates[:limit]


def write_report(rows: list[dict[str, str]], queue: list[dict[str, str]], now: datetime) -> tuple[Path, Path]:
    REPORTS.mkdir(exist_ok=True)
    stamp = now.strftime("%Y-%m-%d")
    md_path = REPORTS / f"{stamp}_0800.md"
    json_path = REPORTS / f"{stamp}_0800.json"
    decisions = Counter(row["decision_editorial"] for row in rows)
    lines = [
        f"# Reporte de producción · {stamp} · 08:00",
        "",
        "## Control editorial",
        "",
        f"- Total registrado: {len(rows)}",
        f"- Conservar: {decisions['conservar']}",
        f"- Mejorar: {decisions['mejorar']}",
        f"- Actualizar: {decisions['actualizar']}",
        f"- Desechar: {decisions['desechar']}",
        f"- Crear: {decisions['crear']}",
        "",
        "## Piezas programadas para trabajar",
        "",
        "| ID | Pieza | Decisión | Descripción | Herramientas comprobadas | Siguiente acción |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in queue:
        lines.append(
            f"| {row['id']} | {row['titulo']} | {row['decision_editorial']} | "
            f"{row['descripcion_actual']} | {row['herramientas_reales']} | {row['siguiente_accion']} |"
        )
    lines += [
        "",
        "## Reglas de ejecución",
        "",
        "- Verificar saldo y cuenta en vivo antes de generar.",
        "- Empezar por una prueba pequeña y revisar el archivo, no solo el estado del proveedor.",
        "- Registrar herramienta, ID, archivo, costo y saldo antes/después.",
        "- No publicar automáticamente.",
        "- No llamar video a una fotografía con zoom.",
        "- No sustituir fuentes autorizadas disponibles con generación innecesaria.",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    payload = {
        "generated_at": now.isoformat(),
        "register": str(REGISTER),
        "counts": dict(decisions),
        "queue": queue,
        "report": str(md_path),
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md_path, json_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--now", help="ISO timestamp for deterministic tests")
    args = parser.parse_args()
    zone = ZoneInfo("America/Monterrey")
    now = datetime.fromisoformat(args.now).astimezone(zone) if args.now else datetime.now(zone)
    rows = load_rows()
    queue = select_queue(rows, args.limit)
    md_path, json_path = write_report(rows, queue, now)
    print(json.dumps({
        "ok": True,
        "registered": len(rows),
        "scheduled": len(queue),
        "ids": [row["id"] for row in queue],
        "markdown": str(md_path),
        "json": str(json_path),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
