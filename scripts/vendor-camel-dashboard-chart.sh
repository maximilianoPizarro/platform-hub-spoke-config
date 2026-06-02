#!/usr/bin/env bash
# Re-vendor camel-dashboard-openshift-all into components/camel-dashboard-openshift/charts/
# Usage: ./scripts/vendor-camel-dashboard-chart.sh [version]   (default: 4.20.2)
set -euo pipefail

VERSION="${1:-4.20.2}"
CHART_DIR="$(cd "$(dirname "$0")/../components/camel-dashboard-openshift" && pwd)"

echo "==> Vendoring camel-dashboard-openshift-all ${VERSION} into ${CHART_DIR}"
helm repo add camel-dashboard https://camel-tooling.github.io/camel-dashboard/charts 2>/dev/null || true
helm repo update camel-dashboard

# Pin dependency version in Chart.yaml
sed -i.bak "s/^    version: .*/    version: ${VERSION}/" "${CHART_DIR}/Chart.yaml"
rm -f "${CHART_DIR}/Chart.yaml.bak"
sed -i.bak "s/^appVersion: .*/appVersion: \"${VERSION}\"/" "${CHART_DIR}/Chart.yaml"
rm -f "${CHART_DIR}/Chart.yaml.bak"

helm dependency update "${CHART_DIR}"

TGZ="${CHART_DIR}/charts/camel-dashboard-openshift-all-${VERSION}.tgz"
if [[ ! -f "${TGZ}" ]]; then
  echo "ERROR: expected ${TGZ} after helm dependency update" >&2
  exit 1
fi

# Remove stale tgz versions
find "${CHART_DIR}/charts" -name 'camel-dashboard-openshift-all-*.tgz' ! -name "$(basename "${TGZ}")" -delete 2>/dev/null || true

helm lint "${CHART_DIR}"
helm template test "${CHART_DIR}" --kube-version 1.33 --namespace camel-dashboard >/dev/null
echo "OK: ${TGZ} ($(du -h "${TGZ}" | cut -f1))"
echo "Commit Chart.lock, Chart.yaml, and charts/*.tgz, then refresh spoke Argo apps."
