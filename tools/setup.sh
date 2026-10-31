#!/bin/bash
# Cài công cụ edit video (chạy một lần mỗi phiên): bash tools/setup.sh
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null || { apt-get update -qq && apt-get install -y -qq ffmpeg; }
pip install -q -r requirements.txt
echo "Sẵn sàng edit video."
