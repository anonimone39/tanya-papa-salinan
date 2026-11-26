#!/bin/bash
# Buat video dari folder video (berisi naskah.py, template.html, efek.py).
#   bash Skrip/buat_video.sh "02 Computer Things - Printer USB"          -> render MP4 ke Upload/
#   bash Skrip/buat_video.sh "02 ..." cek 3,12,30                        -> hanya frame uji (periksa label dan posisi)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VID="$ROOT/${1:?sebutkan folder video}"
MODE="${2:-render}"
PY="$ROOT/.venv/bin/python"
B="$VID/build"
mkdir -p "$B/tts" "$ROOT/Upload"
[ -x "$PY" ] || { echo "Belum terpasang. Jalankan dulu: bash setup.sh"; exit 1; }
NAMA="$("$PY" -c 'import runpy,sys; print(runpy.run_path(sys.argv[1])["NAMA_FILE"])' "$VID/naskah.py")"
echo "1/5 suara";   "$PY" "$ROOT/Skrip/suara.py" "$VID/naskah.py" "$B"
DUR="$("$PY" -c 'import json,sys; print(round(json.load(open(sys.argv[1]))["total"]+4.2,2))' "$B/timing.json")"
FADE="$("$PY" -c 'import sys; print(round(float(sys.argv[1])-1.3,2))' "$DUR")"
echo "2/5 halaman"; "$PY" "$ROOT/Skrip/halaman.py" "$VID" "$B/timing.json" "$B/index.html" mix.mp3
echo "3/5 efek";    "$PY" "$ROOT/Skrip/efek.py" "$VID/efek.py" "$B/timing.json" "$B/sfx.wav"
echo "4/5 campur";  ffmpeg -y -loglevel error -i "$B/suara.mp3" -i "$B/sfx.wav" -filter_complex "[0:a]apad=whole_dur=${DUR}[v];[1:a]volume=0.55[s];[v][s]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=${FADE}:d=1.3,loudnorm=I=-16:TP=-1.5:LRA=9" -ar 44100 -ac 1 -c:a libmp3lame -b:a 160k "$B/mix.mp3"
if [ "$MODE" = "cek" ]; then
  node "$ROOT/Skrip/render.mjs" test "$B/index.html" "$B/frame" "${3:-3,12,30}"
  echo "Frame uji ada di: $B"; exit 0
fi
echo "5/5 render (beberapa menit)"
node "$ROOT/Skrip/render.mjs" full "$B/index.html" "$ROOT/Upload/${NAMA}.mp4" "$B/mix.mp3" "$DUR"
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate -show_entries format=duration,size -of default=nw=1 "$ROOT/Upload/${NAMA}.mp4"
