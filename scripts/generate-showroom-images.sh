#!/usr/bin/env bash
# Generate workshop hero images (1200x630) via NanoBanana 2 API.
# Output: showroom-hybrid-mesh-ai/.../images/*.png + docs/assets/images/workshop/
#
# Requires: NANOBANANA_API_KEY — https://nanobananaapi.ai/api-key
# Without key: copies existing platform art or generates styled PIL placeholders.
#
# Usage:
#   NANOBANANA_API_KEY=... ./scripts/generate-showroom-images.sh
#   FORCE=1 NANOBANANA_API_KEY=... ./scripts/generate-showroom-images.sh   # regenerate all
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ASSETS="${ROOT}/docs/assets/images"
SHOWROOM_IMG="${ROOT}/showroom-hybrid-mesh-ai/content/modules/en/modules/ROOT/images"
SHOWROOM_IMG_ES="${ROOT}/showroom-hybrid-mesh-ai/content/modules/es/modules/ROOT/images"
DOCS_IMG="${ROOT}/docs/assets/images/workshop"
API_GEN="https://api.nanobananaapi.ai/api/v1/nanobanana/generate-2"
API_RECORD="https://api.nanobananaapi.ai/api/v1/nanobanana/record-info"

mkdir -p "$SHOWROOM_IMG" "$SHOWROOM_IMG_ES" "$DOCS_IMG"

# filename|NanoBanana prompt|optional fallback asset in docs/assets/images/
IMAGE_SPECS=(
  "00-index-hybrid-mesh.png|Professional tech illustration, Red Hat hybrid cloud hub-spoke architecture diagram, central OpenShift hub cluster connected to east and west factory edge spokes, AWS cloud icons subtle, clean white background, red #EE0000 accent bars, no text labels, 16:9|arch-hub-spoke-flow.png"
  "01-hybrid-strategy.png|Executive hybrid cloud strategy infographic, OpenShift on-prem edge and public cloud unified, modernization security automation AI pillars icons, Red Hat red accents, minimal flat design, no text|arch-overview.png"
  "02-rosa-architecture.png|AWS ROSA Red Hat OpenShift Service architecture diagram, managed control plane worker nodes VPC subnets Route53, professional isometric cloud illustration, red gray palette, no text|arch-hub-spoke-flow.png"
  "03-security-scale-hybrid.png|Cybersecurity and autoscaling hybrid cloud diagram, shield lock HPA graph factory sensors, ACS and mesh concept, Red Hat style red accent, clean illustration no text|"
  "04-aws-ai-integration.png|AWS Bedrock SageMaker vs OpenShift AI comparison illustration, Kubernetes AI pipeline MaaS endpoint, cloud and cluster icons, red black white, no text|"
  "05-cases-roadmap.png|Manufacturing IoT customer journey roadmap timeline, factory sensors to AI dashboard FinOps, automotive plant icons, professional infographic no text|"
  "10-acm-multicluster.png|Red Hat ACM multicluster fleet management dashboard concept, hub controlling multiple OpenShift clusters map pins, multicloud illustration no text|ACM.png"
  "11-hybrid-mesh.png|Skupper service interconnect hybrid mesh diagram, gateway API traffic hub to edge spokes encrypted links, network topology illustration red accents no text|arch-skupper-topology.png"
  "12-software-templates.png|Developer Hub Backstage software template golden path illustration, developer creating app from template catalog UI concept, teal red colors no text|product-developer-hub.png"
  "13-deploy-industrial-edge.png|Industrial Edge factory OT dashboard Kafka sensors on OpenShift edge cluster, manufacturing line digital twin illustration no text|industrial-edge.png"
  "14-kairos-scaling.png|Kubernetes node autoscaling recommendations dashboard SmartScaling CPU memory graphs, Kairos operator concept cyan red illustration no text|kairos-observability.png"
  "15-observability.png|Observability stack Prometheus Grafana Jaeger tracing dashboards multicluster metrics, SRE monitoring illustration no text|product-grafana-observability.png"
  "16-openshift-gitops.png|OpenShift GitOps Argo CD continuous delivery diagram Git repository to multiple clusters sync waves illustration no text|product-argocd-openshift-gitops.png"
  "17-service-mesh.png|OpenShift Service Mesh ambient mode Kiali service graph mTLS microservices illustration factory apps no text|product-kiali-service-mesh.png"
  "18-scalability.png|Horizontal Pod Autoscaler HPA Kafka streaming scale diagram sensor spike factory workload illustration no text|"
  "19-network-policies.png|Kubernetes network policy microsegmentation diagram allowed denied traffic paths OVN factory namespace illustration no text|"
  "20-acs-kuadrant.png|Red Hat ACS security shield plus Kuadrant API gateway keys rate limit tokens illustration combined no text|ACS.png"
  "21-finops-kubecost.png|FinOps Kubecost Kubernetes cost allocation charts namespace spend optimization illustration teal red no text|kubecost.png"
  "22-openshift-ai.png|OpenShift AI DataScienceCluster Jupyter notebook ModelMesh inference pipeline illustration red hat AI no text|openshift-ia.png"
  "23-ai-gateway.png|AI Gateway API management Kuadrant HTTPRoute LLM MaaS endpoint factory apps calling chat completions illustration no text|"
  "24-mcp-gateway.png|Model Context Protocol MCP gateway federated tools ArgoCD Kubernetes developer AI assistant illustration no text|"
  "25-llm-rag.png|LLM RAG retrieval augmented generation vector database documents factory runbooks OpenShift AI illustration no text|"
  "27-neuroface.png|NeuroFace AI webcam face detection dashboard chat MaaS factory operator UI concept illustration no text|"
  "28-ai-end-user-apps.png|End user factory operator dashboard mobile alerts line dashboard AI insights embedded manufacturing UX illustration no text|"
  "29-full-verification.png|Checklist full stack verification workshop graduation green checks OpenShift multicluster AI illustration no text|"
)

poll_task() {
  local task_id="$1"
  local attempt=0
  while (( attempt < 72 )); do
    sleep 5
    local resp flag url
    resp=$(curl -sS -G "${API_RECORD}" \
      -H "Authorization: Bearer ${NANOBANANA_API_KEY}" \
      --data-urlencode "taskId=${task_id}")
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

generate_nanobanana() {
  local out="$1"
  local prompt="$2"
  local tmp_png
  tmp_png=$(mktemp /tmp/workshop-img-XXXXXX.png)

  echo "  NanoBanana 2: $(basename "$out")..."
  local resp task_id
  resp=$(curl -sS -X POST "${API_GEN}" \
    -H "Authorization: Bearer ${NANOBANANA_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$(python3 -c "import json; print(json.dumps({'prompt': '''${prompt}''', 'imageUrls': [], 'aspectRatio': '16:9', 'resolution': '2K', 'outputFormat': 'png', 'googleSearch': True}))")")

  task_id=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('taskId',''))" 2>/dev/null || true)
  if [[ -z "$task_id" ]]; then
    echo "  API error: $resp" >&2
    rm -f "$tmp_png"
    return 1
  fi

  local img_url
  img_url=$(poll_task "$task_id") || { rm -f "$tmp_png"; return 1; }
  curl -fsSL "$img_url" -o "$tmp_png"
  python3 - "$tmp_png" "$out" <<'PY'
import sys
from pathlib import Path
try:
    from PIL import Image
    img = Image.open(sys.argv[1]).convert("RGB")
    img = img.resize((1200, 630), Image.Resampling.LANCZOS)
    img.save(sys.argv[2], format="PNG", optimize=True)
except ImportError:
    Path(sys.argv[2]).write_bytes(Path(sys.argv[1]).read_bytes())
PY
  rm -f "$tmp_png"
  echo "  -> $out"
}

generate_placeholder() {
  local out="$1"
  local name="$2"
  python3 - "$out" "$name" <<'PY'
import sys
from pathlib import Path

out = Path(sys.argv[1])
name = Path(sys.argv[2]).stem
ACRONYMS = {"ai", "acs", "acm", "aws", "mcp", "maas", "rag", "llm", "ie", "rosa", "api", "hpa", "e2e", "ui", "ovms", "gitops"}
THEMES = {
    "index": ("#151515", "#ee0000", "hub-spoke"),
    "strategy": ("#004080", "#ee0000", "strategy"),
    "rosa": ("#232F3E", "#ee0000", "AWS ROSA"),
    "security": ("#3d0000", "#ee0000", "security"),
    "aws": ("#232F3E", "#ff9900", "AWS AI"),
    "cases": ("#292929", "#73bcf7", "roadmap"),
    "acm": ("#ee0000", "#151515", "ACM fleet"),
    "mesh": ("#0066cc", "#ee0000", "hybrid mesh"),
    "templates": ("#0f766e", "#ee0000", "templates"),
    "industrial": ("#c46100", "#151515", "Industrial Edge"),
    "kairos": ("#008080", "#ee0000", "Kairos scale"),
    "observability": ("#f0ab00", "#151515", "observability"),
    "gitops": ("#ef7b4d", "#151515", "GitOps"),
    "service-mesh": ("#009596", "#151515", "service mesh"),
    "scalability": ("#3e8635", "#151515", "scale"),
    "network": ("#0066cc", "#151515", "network policy"),
    "acs": ("#ee0000", "#151515", "ACS Kuadrant"),
    "finops": ("#29B0C6", "#151515", "FinOps"),
    "openshift-ai": ("#ee0000", "#151515", "OpenShift AI"),
    "gateway": ("#6a6e73", "#ee0000", "AI Gateway"),
    "mcp": ("#151515", "#73bcf7", "MCP Gateway"),
    "llm": ("#4a154b", "#ee0000", "LLM RAG"),
    "neuroface": ("#151515", "#f0ab00", "NeuroFace"),
    "end-user": ("#0066cc", "#ee0000", "end-user apps"),
    "verification": ("#3e8635", "#151515", "verification"),
}
words = name.replace("-", " ").split()
label_parts = []
for w in words:
    if w.isdigit():
        label_parts.append(w)
    elif w.lower() in ACRONYMS:
        label_parts.append(w.upper())
    else:
        label_parts.append(w.capitalize())
label = " ".join(label_parts)
theme_key = next((k for k in THEMES if k in name), "index")
bg, accent, subtitle = THEMES[theme_key]
w, h = 1200, 630

try:
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (w, h), "#f5f5f5")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w, 8), fill="#ee0000")
    draw.rectangle((0, h - 8, w, h), fill="#ee0000")
    draw.rectangle((40, 80, w - 40, h - 80), fill=bg)
    draw.ellipse((w // 2 - 120, 120, w // 2 + 120, 360), outline=accent, width=6)
    draw.rectangle((w // 2 - 200, 380, w // 2 + 200, 420), fill=accent)
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        sub_font = ImageFont.truetype("arial.ttf", 26)
        cap_font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        title_font = sub_font = cap_font = ImageFont.load_default()
    draw.text((w // 2, 480), "Hybrid Mesh AI Workshop", fill="#ffffff", anchor="mm", font=title_font)
    draw.text((w // 2, 530), label, fill="#c7c7c7", anchor="mm", font=sub_font)
    draw.text((w // 2, 570), subtitle, fill=accent, anchor="mm", font=cap_font)
    img.save(out, format="PNG", optimize=True)
except ImportError:
    import struct, zlib
    raw = b"".join(b"\x00" + b"\xf5\xf5\xf5" * w for _ in range(h))
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    out.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
PY
  echo "  placeholder -> $out"
}

use_api=0
[[ -n "${NANOBANANA_API_KEY:-}" ]] && use_api=1

if [[ "$use_api" -eq 0 ]]; then
  echo "NANOBANANA_API_KEY not set — using platform art + styled placeholders."
  echo "Set NANOBANANA_API_KEY from https://nanobananaapi.ai/api-key for AI-generated heroes."
fi

for spec in "${IMAGE_SPECS[@]}"; do
  IFS='|' read -r fname prompt fallback <<< "$spec"
  out="${SHOWROOM_IMG}/${fname}"
  docs_out="${DOCS_IMG}/${fname}"

  if [[ -f "$out" && "${FORCE:-0}" != "1" && "$use_api" -eq 0 ]]; then
    cp "$out" "$docs_out" 2>/dev/null || true
    cp "$out" "${SHOWROOM_IMG_ES}/${fname}" 2>/dev/null || true
    continue
  fi

  generated=0
  if [[ "$use_api" -eq 1 ]]; then
    if generate_nanobanana "$out" "$prompt"; then
      generated=1
    else
      echo "  NanoBanana failed for ${fname}, trying fallback..."
    fi
  fi

  if [[ "$generated" -eq 0 ]]; then
    if [[ -n "$fallback" && -f "${ASSETS}/${fallback}" ]]; then
      cp "${ASSETS}/${fallback}" "$out"
      echo "Copied ${fallback} -> $out"
    else
      generate_placeholder "$out" "${fname%.png}"
    fi
  fi

  cp "$out" "$docs_out"
  cp "$out" "${SHOWROOM_IMG_ES}/${fname}"
done

echo "Done. ${#IMAGE_SPECS[@]} workshop images in ${SHOWROOM_IMG}"
