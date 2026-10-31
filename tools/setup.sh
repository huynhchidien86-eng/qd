#!/bin/bash
# Cài công cụ edit video (chạy một lần mỗi phiên): bash tools/setup.sh
set -euo pipefail
cd "$(dirname "$0")/.."
missing=""
command -v ffmpeg >/dev/null || missing="$missing ffmpeg"
command -v espeak-ng >/dev/null || missing="$missing espeak-ng"
if [ -n "$missing" ]; then
  apt-get update -qq && apt-get install -y -qq $missing
fi
pip install -q -r requirements.txt
echo "Sẵn sàng edit video."
