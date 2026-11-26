#!/bin/bash
# Periksa apakah semua alat sudah terpasang.
cd "$(dirname "$0")/.."
ok=0
cek() { if eval "$2" >/dev/null 2>&1; then echo "OK     $1"; else echo "KURANG $1"; ok=1; fi; }
cek "ffmpeg"              "ffmpeg -version"
cek "ffmpeg libx264"      "ffmpeg -hide_banner -encoders | grep -q libx264"
cek "Node.js"             "node --version"
cek "Python (.venv)"      ".venv/bin/python --version"
cek "edge-tts"            ".venv/bin/python -c 'import edge_tts'"
cek "numpy"               ".venv/bin/python -c 'import numpy'"
cek "Playwright"          "test -d node_modules/playwright"
cek "Chromium Playwright" "node -e \"const{chromium}=require('playwright');require('fs').accessSync(chromium.executablePath())\""
cek "Logo (Brand/)"       "test -f Brand/logo-tanya-papa.svg"
cek "GitHub CLI login"    "gh auth status"
[ $ok = 0 ] && echo "Semua siap." || echo "Ada yang kurang. Jalankan: bash setup.sh"
exit $ok
