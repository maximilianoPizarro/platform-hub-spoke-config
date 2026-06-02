#!/usr/bin/env bash
# Generate OpenShift ConsoleLink menu icons (48x48) via NanoBanana 2 API.
# Output: components/console-links/files/icons/<name>.svg (PNG wrapped in SVG for data-URI use)
#
# Requires: NANOBANANA_API_KEY — https://nanobananaapi.ai/api-key
# Without key: downloads official/community logos from simple-icons / Kairos OLM icon.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ICON_DIR="${ROOT}/components/console-links/files/icons"
API_GEN="https://api.nanobananaapi.ai/api/v1/nanobanana/generate-2"
API_RECORD="https://api.nanobananaapi.ai/api/v1/nanobanana/record-info"
KAIROS_OLM_ICON="https://raw.githubusercontent.com/maximilianoPizarro/kairos/main/config/manifests/bases/kairos-operator.clusterserviceversion.yaml"

mkdir -p "$ICON_DIR"

# name|prompt for NanoBanana 2|simple-icons slug (fallback, empty to skip)
COMPONENTS=(
  "industrial-edge|Flat app icon for Red Hat Industrial Edge / factory OT platform on OpenShift, orange and dark gray, 48x48, no text|redhatopenshift"
  "grafana|Official Grafana logo style, orange spiral G mark, flat 48x48 app icon, no text|grafana"
  "kiali|Kiali service mesh observability logo style, green and white, 48x48, no text|istio"
  "kairos|Kairos Kubernetes community operator logo, cyan diamond on dark circle, 48x48, no text|"
  "acm|Red Hat Advanced Cluster Management multicluster logo style, red hat mark, 48x48, no text|redhatopenshift"
  "acs|Red Hat Advanced Cluster Security / StackRox shield logo style, red and white, 48x48, no text|redhat"
  "developer-hub|Red Hat Developer Hub Backstage logo style, teal backstage mark, 48x48, no text|backstage"
  "gitea|Gitea git forge logo, green tea cup mark, 48x48, no text|gitea"
  "minio|MinIO object storage logo, red bird on dark, 48x48, no text|minio"
  "mailpit|Mailpit email testing tool logo, blue envelope, 48x48, no text|"
  "kafka-console|Apache Kafka streaming logo, black K mark, 48x48, no text|apachekafka"
  "kubecost|Kubecost cost monitoring for Kubernetes, teal bar chart, 48x48, no text|"
  "quay|Red Hat Quay container registry logo, red Q, 48x48, no text|redhat"
  "skupper|Skupper network interconnect logo, coral circles linked, 48x48, no text|"
)

poll_task() {
  local task_id="$1"
  local attempt=0
  while (( attempt < 60 )); do
    sleep 5
    local resp
    resp=$(curl -sS -G "${API_RECORD}" \
      -H "Authorization: Bearer ${NANOBANANA_API_KEY}" \
      --data-urlencode "taskId=${task_id}")
    local flag url
    flag=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin).get('data',{}); print(d.get('successFlag',-1))" 2>/dev/null || echo "-1")
    if [[ "$flag" == "1" ]]; then
      url=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin).get('data',{}).get('response',{}); print(d.get('resultImageUrl',''))" 2>/dev/null || true)
      echo "$url"
      return 0
    fi
    if [[ "$flag" == "2" || "$flag" == "3" ]]; then
      echo "Task failed: $resp" >&2
      return 1
    fi
    (( attempt++ )) || true
  done
  echo "Task timed out: $task_id" >&2
  return 1
}

png_to_svg_wrapper() {
  local png="$1"
  local out_svg="$2"
  local b64
  b64=$(base64 -w0 "$png" 2>/dev/null || base64 < "$png" | tr -d '\n')
  cat > "$out_svg" <<EOF
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 48 48" role="img">
  <image width="48" height="48" xlink:href="data:image/png;base64,${b64}"/>
</svg>
EOF
}

generate_nanobanana() {
  local name="$1"
  local prompt="$2"
  local out_svg="${ICON_DIR}/${name}.svg"
  local tmp_png
  tmp_png=$(mktemp /tmp/console-icon-XXXXXX.png)

  echo "NanoBanana 2: ${name}..."
  local resp task_id
  resp=$(curl -sS -X POST "${API_GEN}" \
    -H "Authorization: Bearer ${NANOBANANA_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$(python3 -c "import json; print(json.dumps({'prompt': '''${prompt}''', 'imageUrls': [], 'aspectRatio': '1:1', 'resolution': '1K', 'outputFormat': 'png', 'googleSearch': True}))")")

  task_id=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('taskId',''))" 2>/dev/null || true)
  if [[ -z "$task_id" ]]; then
    echo "  API error: $resp" >&2
    rm -f "$tmp_png"
    return 1
  fi

  local img_url
  img_url=$(poll_task "$task_id") || { rm -f "$tmp_png"; return 1; }
  curl -fsSL "$img_url" -o "$tmp_png"
  png_to_svg_wrapper "$tmp_png" "$out_svg"
  rm -f "$tmp_png"
  echo "  -> ${out_svg}"
}

fetch_simple_icon() {
  local slug="$1"
  local out_svg="$2"
  curl -fsSL "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/${slug}.svg" -o "$out_svg"
}

fetch_kairos_icon() {
  local out_svg="$1"
  if [[ -f "${ROOT}/components/console-links/files/kairos-community-icon.svg" ]]; then
    cp "${ROOT}/components/console-links/files/kairos-community-icon.svg" "$out_svg"
    return 0
  fi
  echo "  (no bundled kairos SVG; run generate-kairos-console-icon.sh first)" >&2
  return 1
}

main() {
  local use_api=0
  [[ -n "${NANOBANANA_API_KEY:-}" ]] && use_api=1

  if [[ "$use_api" -eq 0 ]]; then
    echo "NANOBANANA_API_KEY not set — fetching community/brand SVG fallbacks (simple-icons)."
  fi

  while IFS='|' read -r name prompt slug; do
    local out="${ICON_DIR}/${name}.svg"
    if [[ "$use_api" -eq 1 ]]; then
      generate_nanobanana "$name" "$prompt" || {
        echo "  fallback for ${name}..."
        if [[ "$name" == "kairos" ]]; then fetch_kairos_icon "$out"
        elif [[ -n "$slug" ]]; then fetch_simple_icon "$slug" "$out"
        else echo "  skip ${name}" >&2
        fi
      }
    else
      if [[ "$name" == "kairos" ]]; then
        fetch_kairos_icon "$out" || cp "${ICON_DIR}/kairos.svg" "$out" 2>/dev/null || true
      elif [[ -n "$slug" ]]; then
        fetch_simple_icon "$slug" "$out" && echo "ok ${name} (${slug})"
      elif [[ "$name" == "mailpit" ]]; then
        cat > "$out" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img"><path fill="#49A6E9" d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5L4 8V6l8 5 8-5v2z"/></svg>
SVG
        echo "ok ${name} (inline)"
      elif [[ "$name" == "kubecost" ]]; then
        cat > "$out" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img"><path fill="#29B0C6" d="M3 20h18v2H3v-2zm2-3h3v3H5v-3zm4-3h3v6H9v-6zm4-4h3v10h-3V10zm4-6h3v16h-3V4z"/></svg>
SVG
        echo "ok ${name} (inline)"
      elif [[ "$name" == "skupper" ]]; then
        cat > "$out" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img"><circle cx="6" cy="12" r="3" fill="#E9654B"/><circle cx="18" cy="12" r="3" fill="#E9654B"/><path stroke="#E9654B" stroke-width="2" d="M9 12h6"/></svg>
SVG
        echo "ok ${name} (inline)"
      else
        echo "skip ${name} (no fallback slug)" >&2
      fi
    fi
  done < <(printf '%s\n' "${COMPONENTS[@]}")

  cp "${ICON_DIR}/kafka.svg" "${ICON_DIR}/kafka-console.svg" 2>/dev/null || true
  echo "Done. Icons in ${ICON_DIR}"
}

main "$@"
