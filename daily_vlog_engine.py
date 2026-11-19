#!/usr/bin/env python3
"""
CAPTOORA STUDIO — Daily Vlog & Eufy S350 Set-Setup Engine (Multi-Host Compatible)
Usa scripts/captoora_paths.py para funcionar automáticamente tanto en el iMac 2015 (/Users/imac)
como en la MacBook Pro (/Users/user).
"""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
if (REPO_ROOT / "scripts" / "eufy_artemis_extractor.py").exists():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
elif (REPO_ROOT.parent.parent / "scripts" / "eufy_artemis_extractor.py").exists():
    sys.path.insert(0, str(REPO_ROOT.parent.parent / "scripts"))

import eufy_artemis_extractor as eufy

if __name__ == "__main__":
    eufy.run_pipeline(check_only=False)
