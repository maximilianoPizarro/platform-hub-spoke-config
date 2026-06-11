#!/usr/bin/env bash
# Workshop hero images — delegates to Python (Gemini Imagen / fallbacks).
# Requires: GEMINI_API_KEY from https://aistudio.google.com/apikey (same as Gemini in Cursor BYOK)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "${ROOT}/scripts/generate_workshop_images.py" "$@"
