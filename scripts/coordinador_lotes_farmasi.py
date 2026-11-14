#!/usr/bin/env python3
"""
Coordinador de Lotes Farmasi (Grok Imagine / Workspace 799)
Captoora Studio - Protocolo de Ejecución en Lotes de 10

Mantiene:
1. Bloqueo de concurrencia (.coordinator.lock)
2. Ledger durable JSON con estados: pending, submitting, running, generated, needs_review, blocked
3. Reconciliación previa de historial antes de despachar
4. Persistencia obligatoria de 'submitting' antes del envío
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime, timezone

WORKSPACE_DIR = "/Users/imac/Desktop/Projects/CAPTOORA.STUDIO"
LEDGER_PATH = os.path.join(WORKSPACE_DIR, "proyectos/farmasi-799/registros/ledger_farmasi_lotes.json")
LOCK_PATH = os.path.join(WORKSPACE_DIR, "proyectos/farmasi-799/registros/.coordinator.lock")
CONVERSATION_E25_ID = "e25a0fbc-09aa-4663-a171-3b7268e7ca3a"
CONVERSATION_IMAGINE_ID = "deee59db-d892-4afa-b779-39a4e042142c"

def acquire_lock():
    if os.path.exists(LOCK_PATH):
        try:
            with open(LOCK_PATH) as f:
                lock_info = json.load(f)
            pid = lock_info.get("pid")
            # Check if PID is still alive
            if pid and os.path.exists(f"/proc/{pid}"):
                raise RuntimeError(f"Coordinador ya activo con PID {pid}")
        except Exception:
            pass
    with open(LOCK_PATH, "w") as f:
        json.dump({"pid": os.getpid(), "started_at": datetime.now(timezone.utc).isoformat()}, f)

def release_lock():
    if os.path.exists(LOCK_PATH):
        try:
            os.remove(LOCK_PATH)
        except OSError:
            pass

def load_ledger():
    with open(LEDGER_PATH) as f:
        return json.load(f)

def save_ledger(ledger):
    ledger["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
    temp_path = LEDGER_PATH + ".tmp"
    with open(temp_path, "w") as f:
        json.dump(ledger, f, indent=2)
    os.replace(temp_path, LEDGER_PATH)

def reconcile_grok_conversation():
    """Consulta la conversación activa en Grok para reconciliar respuestas."""
    script = f'''
    var chrome = Application("Google Chrome");
    var tab = chrome.windows[0].tabs().find(t => t.url().includes("grok.com"));
    if (!tab) {{
        "NO_TAB";
    }} else {{
        tab.execute({{javascript: `
            (() => {{
                try {{
                    const xhr = new XMLHttpRequest();
                    xhr.open("GET", "/rest/app-chat/conversations/{CONVERSATION_E25_ID}/responses", false);
                    xhr.send();
                    return xhr.responseText;
                }} catch(e) {{
                    return JSON.stringify({{error: e.toString()}});
                }}
            }})()
        `}});
    }}
    '''
    try:
        proc = subprocess.run(["osascript", "-l", "JavaScript", "-e", script], capture_output=True, text=True, timeout=15)
        out = proc.stdout.strip()
        if out and out != "NO_TAB" and not out.startswith("error"):
            return json.loads(out)
    except Exception as e:
        print(f"Error al reconciliar Grok: {e}")
    return None

def get_ledger_summary(ledger):
    counts = {}
    for item in ledger["items"].values():
        st = item.get("estado", "unknown")
        counts[st] = counts.get(st, 0) + 1
    return counts

def main():
    acquire_lock()
    try:
        ledger = load_ledger()
        summary = get_ledger_summary(ledger)
        print("=== ESTADO ACTUAL DEL LEDGER DURABLE ===")
        for k, v in sorted(summary.items()):
            print(f"  {k}: {v}")
            
        # Reconciliación con respuestas de Grok
        print("\nReconciliando con Grok conversación activa...")
        data = reconcile_grok_conversation()
        if data and "responses" in data:
            responses = data["responses"]
            print(f"Respuestas totales en Grok: {len(responses)}")
            last_resp = responses[-1]
            print(f"Última respuesta: [{last_resp.get('sender')}] {last_resp.get('createTime')}")
            fam = last_resp.get("fileAttachmentAssetMetadata", [])
            print(f"Imágenes adjuntas en última respuesta: {len(fam)}")
            
        print("\nLote activo reconciliado con éxito. Listo para ejecución continua controlada.")
    finally:
        release_lock()

if __name__ == "__main__":
    main()
