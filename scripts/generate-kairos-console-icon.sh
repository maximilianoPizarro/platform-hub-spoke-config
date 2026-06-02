#!/usr/bin/env bash
# Regenerate components/console-links/files/kairos-community-icon.svg via NanoBanana 2 API.
# Requires: NANOBANANA_API_KEY (https://docs.nanobananaapi.ai/)
# Fallback: repo ships the official Kairos OLM operator icon (maximilianoPizarro/kairos).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${ROOT}/components/console-links/files/kairos-community-icon.svg"
PROMPT="Minimal flat app icon for Kairos Kubernetes operator: cyan-to-navy gradient diamond on dark circle, 48x48, clean lines, no text, transparent-friendly, same style as OpenShift console menu icons"

if [[ -z "${NANOBANANA_API_KEY:-}" ]]; then
  echo "NANOBANANA_API_KEY not set — keeping bundled SVG from OLM operator icon."
  echo "Set key and re-run to generate via NanoBanana 2."
  exit 0
fi

echo "Generating icon with NanoBanana 2..."
RESP=$(curl -sS -X POST "https://api.nanobananaapi.ai/api/v1/generate-2" \
  -H "Authorization: Bearer ${NANOBANANA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"${PROMPT}\",\"aspectRatio\":\"1:1\",\"resolution\":\"1K\",\"outputFormat\":\"png\"}")

TASK_ID=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('taskId',''))" 2>/dev/null || true)
if [[ -z "$TASK_ID" ]]; then
  echo "API error: $RESP"
  exit 1
fi

echo "Task $TASK_ID — poll task endpoint per NanoBanana docs, then convert PNG to SVG and save to $OUT"
