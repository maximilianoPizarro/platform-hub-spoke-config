#!/usr/bin/env bash
# Refresh and sync key Argo CD apps on hub, east, and west (requires oc contexts: hub, east, west).
set -euo pipefail

refresh_apps() {
  local ctx="$1"
  shift
  echo "=== context: ${ctx} ==="
  oc config use-context "${ctx}" >/dev/null
  for app in "$@"; do
    oc annotate application "${app}" -n openshift-gitops \
      argocd.argoproj.io/refresh=hard --overwrite 2>/dev/null || true
  done
}

HUB_APPS=(
  field-content-acm-hub-spoke
  field-content-kafka-console
  field-content-kiali
  field-content-hub-gateway
  field-content-service-interconnect
  east-spoke-components
  west-spoke-components
)

EAST_APPS=(
  industrial-edge-tst-east
  spoke-interconnect-east
  spoke-gateway-east
  operators-east
  servicemeshoperator3-east
)

WEST_APPS=(
  industrial-edge-tst-west
  spoke-interconnect-west
  spoke-gateway-west
  operators-west
  servicemeshoperator3-west
)

refresh_apps hub "${HUB_APPS[@]}"
refresh_apps east "${EAST_APPS[@]}"
refresh_apps west "${WEST_APPS[@]}"

echo "Done. Check: oc get applications -n openshift-gitops (per context)"
