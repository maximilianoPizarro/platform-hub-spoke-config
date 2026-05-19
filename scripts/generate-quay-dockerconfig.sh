#!/usr/bin/env bash
# Generate quayDockerConfigJson for helm --set (never commit output to git).
# Usage: ./scripts/generate-quay-dockerconfig.sh <username> <password>
set -euo pipefail
USER="${1:?username}"
PASS="${2:?password}"
AUTH="$(printf '%s:%s' "$USER" "$PASS" | base64 -w0 2>/dev/null || printf '%s:%s' "$USER" "$PASS" | base64)"
cat <<EOF
{"auths":{"quay.io":{"auth":"${AUTH}"}}}
EOF
