#!/usr/bin/env bash
# Generate placeholder workshop images for Showroom (NanoBanana 2 integration point).
# PNG output is committed; never commit MP4 from this script.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ASSETS="${ROOT}/docs/assets/images"
SHOWROOM_IMG="${ROOT}/showroom-hybrid-mesh-ai/content/modules/en/modules/ROOT/images"
SHOWROOM_IMG_ES="${ROOT}/showroom-hybrid-mesh-ai/content/modules/es/modules/ROOT/images"
DOCS_IMG="${ROOT}/docs/assets/images/workshop"
mkdir -p "$SHOWROOM_IMG" "$SHOWROOM_IMG_ES" "$DOCS_IMG"

MODULES=(
  "00-index-hybrid-mesh"
  "01-hybrid-strategy"
  "02-rosa-architecture"
  "03-security-scale-hybrid"
  "04-aws-ai-integration"
  "05-cases-roadmap"
  "10-acm-multicluster"
  "11-hybrid-mesh"
  "12-software-templates"
  "13-deploy-industrial-edge"
  "14-kairos-scaling"
  "15-observability"
  "16-openshift-gitops"
  "17-service-mesh"
  "18-scalability"
  "19-network-policies"
  "20-acs-kuadrant"
  "21-finops-kubecost"
  "22-openshift-ai"
  "23-ai-gateway"
  "23-llm-rag"
  "24-mcp-gateway"
  "25-neuroface-dashboard"
  "26-ai-end-user-apps"
  "27-full-verification"
)

# Prefer existing platform art when available (readable, not flat black placeholders).
declare -A SOURCE_IMAGES=(
  ["00-index-hybrid-mesh"]="arch-hub-spoke-flow.png"
  ["01-hybrid-strategy"]="arch-overview.png"
  ["02-rosa-architecture"]="arch-hub-spoke-flow.png"
  ["10-acm-multicluster"]="ACM.png"
  ["11-hybrid-mesh"]="arch-skupper-topology.png"
  ["12-software-templates"]="product-developer-hub.png"
  ["13-deploy-industrial-edge"]="industrial-edge.png"
  ["14-kairos-scaling"]="kairos-observability.png"
  ["15-observability"]="product-grafana-observability.png"
  ["16-openshift-gitops"]="product-argocd-openshift-gitops.png"
  ["17-service-mesh"]="product-kiali-service-mesh.png"
  ["20-acs-kuadrant"]="ACS.png"
  ["21-finops-kubecost"]="kubecost.png"
  ["22-openshift-ai"]="openshift-ia.png"
)

generate_placeholder() {
  local out="$1"
  local name="$2"
  python3 - "$out" "$name" <<'PY'
import sys
from pathlib import Path

out = Path(sys.argv[1])
name = sys.argv[2]
ACRONYMS = {"ai", "acs", "acm", "aws", "mcp", "maas", "rag", "llm", "ie", "rosa", "api", "hpa", "e2e", "ui", "ovms"}
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
w, h = 1200, 630

try:
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (w, h), "#f5f5f5")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w, 8), fill="#ee0000")
    draw.rectangle((0, h - 8, w, h), fill="#ee0000")
    try:
        title_font = ImageFont.truetype("arial.ttf", 44)
        sub_font = ImageFont.truetype("arial.ttf", 28)
    except OSError:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
    draw.text((w // 2, h // 2 - 30), "Hybrid Mesh AI Workshop", fill="#151515", anchor="mm", font=title_font)
    draw.text((w // 2, h // 2 + 30), label, fill="#6a6e73", anchor="mm", font=sub_font)
    img.save(out, format="PNG", optimize=True)
except ImportError:
    import struct, zlib
    raw = b"".join(b"\x00" + b"\xf5\xf5\xf5" * w for _ in range(h))
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    out.write_bytes(png)
PY
}

for name in "${MODULES[@]}"; do
  out="${SHOWROOM_IMG}/${name}.png"
  docs_out="${DOCS_IMG}/${name}.png"
  source_file="${SOURCE_IMAGES[$name]:-}"
  if [[ -n "$source_file" && -f "${ASSETS}/${source_file}" ]]; then
    cp "${ASSETS}/${source_file}" "$out"
    echo "Copied ${source_file} -> $out"
  elif command -v python3 >/dev/null 2>&1; then
    generate_placeholder "$out" "$name"
    echo "Generated placeholder -> $out"
  elif command -v magick >/dev/null 2>&1; then
    magick -size 1200x630 xc:'#f5f5f5' -fill '#151515' -gravity center -pointsize 36 \
      -annotate 0 "Hybrid Mesh AI Workshop\n${name}" "$out"
    echo "Generated placeholder (magick) -> $out"
  else
    echo "Install python3 or ImageMagick to generate ${name}.png" >&2
    exit 1
  fi
  cp "$out" "$docs_out"
  cp "$out" "${SHOWROOM_IMG_ES}/${name}.png"
done

echo "Done. Replace placeholders with NanoBanana 2 renders when API key is available."
