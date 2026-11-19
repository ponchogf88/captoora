#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/Users/imac/Documents/antigravity/epic-bohr"
PLIST_PATH="$HOME/Library/LaunchAgents/com.captoora.server247.plist"
LOG_DIR="$HOME/Library/Logs/Captoora"
mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR"

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.captoora.server247</string>
  <key>ProgramArguments</key>
  <array>
    <string>$REPO_DIR/.venv/bin/python</string>
    <string>-m</string>
    <string>captoora_agents.server</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$REPO_DIR</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$LOG_DIR/server_stdout.log</string>
  <key>StandardErrorPath</key>
  <string>$LOG_DIR/server_stderr.log</string>
</dict>
</plist>
EOF

launchctl unload "$PLIST_PATH" >/dev/null 2>&1 || true
launchctl load "$PLIST_PATH"
echo "Captoora 24/7 LaunchAgent instalado y activo en: $PLIST_PATH"
echo "Logs: $LOG_DIR/server_stdout.log"
