#!/bin/bash
# Tự cài công cụ edit video mỗi khi mở phiên Claude Code trên cloud.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

bash "$CLAUDE_PROJECT_DIR/tools/setup.sh"
