#!/usr/bin/env bash
# Offline verification for Hybrid Mesh AI Workshop platform wiring (no cluster required).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOMAIN=apps.test.example.com
EAST=apps.east.example.com
WEST=apps.west.example.com

echo "== helm template root (workshop apps) =="
helm template test "$ROOT" \
  --set deployer.domain="$DOMAIN" \
  --set clusters.east.domain="$EAST" \
  --set clusters.west.domain="$WEST" \
  | rg -q "test-showroom"
helm template test "$ROOT" \
  --set deployer.domain="$DOMAIN" \
  --set clusters.east.domain="$EAST" \
  --set clusters.west.domain="$WEST" \
  | rg -q "test-neuroface"
helm template test "$ROOT" \
  --set deployer.domain="$DOMAIN" \
  --set clusters.east.domain="$EAST" \
  --set clusters.west.domain="$WEST" \
  | rg -q "test-workshop-registration"
helm template cl "$ROOT/components/console-links" \
  --set clusterDomain="$DOMAIN" \
  --set hubClusterDomain="$DOMAIN" \
  --set clusterRole=hub \
  | rg -q "platform-showroom"

echo "== component charts =="
helm template sr "$ROOT/components/showroom" --set deployer.domain="$DOMAIN" >/dev/null
helm template reg "$ROOT/components/workshop-registration" --set deployer.domain="$DOMAIN" >/dev/null
helm template wd "$ROOT/components/workshop-demos" --set clusterDomain="$DOMAIN" --set hubClusterDomain="$DOMAIN" --set eastClusterDomain="$EAST" >/dev/null
helm template nf "$ROOT/components/neuroface" --set clusterDomain="$DOMAIN" --set neuroface.route.host=neuroface."$DOMAIN" >/dev/null

echo "== showroom content =="
if [ -f "$ROOT/showroom-hybrid-mesh-ai/site.yml" ]; then
  test -f "$ROOT/showroom-hybrid-mesh-ai/verification/recording-runbook.md"
  python3 "$ROOT/scripts/generate-workshop-content.py" >/dev/null
else
  echo "showroom-hybrid-mesh-ai/ not cloned (content: https://github.com/maximilianoPizarro/showroom-hybrid-mesh-ai)"
fi

echo "OK — workshop platform templates and content verified locally."
