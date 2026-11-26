#!/bin/bash
# Pasang semua alat untuk membuat video Tanya Papa (macOS). Aman dijalankan berulang.
set -euo pipefail
cd "$(dirname "$0")"
command -v brew >/dev/null || { echo "Homebrew belum ada. Pasang dulu dari https://brew.sh lalu jalankan lagi."; exit 1; }
for p in ffmpeg node python@3.12 gh; do brew list "$p" >/dev/null 2>&1 || brew install "$p"; done
"$(brew --prefix python@3.12)/bin/python3.12" -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
npm install
npx playwright install chromium
bash Skrip/cek.sh || true
