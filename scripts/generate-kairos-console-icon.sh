#!/usr/bin/env bash
# Regenerate Kairos + all ConsoleLink icons. Prefer: ./scripts/generate-console-icons.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
"${ROOT}/scripts/generate-console-icons.sh"
if [[ -f "${ROOT}/components/console-links/files/icons/kairos.svg" ]]; then
  cp "${ROOT}/components/console-links/files/icons/kairos.svg" \
    "${ROOT}/components/console-links/files/kairos-community-icon.svg"
fi
