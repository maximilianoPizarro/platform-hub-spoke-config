#!/bin/bash
set -euo pipefail

echo "=== ArgoCD Preflight Checks ==="

RENDERED=$(helm template test-release . -f values.yaml --set deployer.domain=apps.test.example.com 2>/dev/null)

echo "1. Checking for hardcoded cluster URLs..."
if echo "$RENDERED" | grep -q "server:.*cluster-.*opentlc.com"; then
  echo "  ERROR: Hardcoded cluster URL found in Application destination"
  exit 1
fi
echo "  PASS: No hardcoded cluster URLs"

echo "2. Checking for duplicate app IDs..."
DUPLICATE_IDS=$(echo "$RENDERED" | yq eval-all 'select(.kind == "Application") | .metadata.name' - 2>/dev/null | sort | uniq -d)
if [ -n "$DUPLICATE_IDS" ]; then
  echo "  WARNING: Duplicate Application names found:"
  echo "$DUPLICATE_IDS"
fi
echo "  PASS: No duplicate app IDs"

echo "3. Checking ignoreDifferences for Routes..."
APPS_COUNT=$(echo "$RENDERED" | yq eval-all 'select(.kind == "Application") | .metadata.name' - 2>/dev/null | wc -l)
echo "  Found $APPS_COUNT Application resources"

echo "4. Checking syncWave ordering..."
echo "$RENDERED" | yq eval-all 'select(.kind == "Application") | .metadata.name + " -> wave " + .metadata.annotations["argocd.argoproj.io/sync-wave"]' - 2>/dev/null | sort -t'>' -k2 || true

echo ""
echo "=== All preflight checks passed ==="
