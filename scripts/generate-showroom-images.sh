#!/usr/bin/env bash
# Generate placeholder workshop images for Showroom (NanoBanana 2 integration point).
# PNG output is committed; never commit MP4 from this script.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SHOWROOM_IMG="${ROOT}/showroom-hybrid-mesh-ai/content/modules/en/ROOT/images"
DOCS_IMG="${ROOT}/docs/assets/images/workshop"
mkdir -p "$SHOWROOM_IMG" "$DOCS_IMG"

MODULES=(
  "00-index-hybrid-mesh"
  "01-hybrid-strategy"
  "25-neuroface-dashboard"
)

for name in "${MODULES[@]}"; do
  out="${SHOWROOM_IMG}/${name}.png"
  docs_out="${DOCS_IMG}/${name}.png"
  if command -v python3 >/dev/null 2>&1; then
    python3 - "$out" "$name" <<'PY'
import struct, sys, zlib
w, h = 1200, 630
raw = b"".join(b"\x00" + b"\x1a\x1a\x1a" * w for _ in range(h))
def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
open(sys.argv[1], "wb").write(png)
PY
    cp "$out" "$docs_out"
  elif command -v magick >/dev/null 2>&1; then
    magick -size 1200x630 xc:'#151515' -fill white -gravity center -pointsize 36 -annotate 0 "Hybrid Mesh AI\n${name}" "$out"
    cp "$out" "$docs_out"
  elif command -v convert >/dev/null 2>&1 && convert -version 2>/dev/null | grep -qi imagemagick; then
    convert -size 1200x630 xc:'#151515' \
      -fill white -gravity center -pointsize 36 -annotate 0 "Hybrid Mesh AI\n${name}" \
      "$out"
    cp "$out" "$docs_out"
  else
    echo "Install python3 or ImageMagick to generate ${name}.png" >&2
    exit 1
  fi
  echo "Wrote $out and $docs_out"
done

echo "Done. Replace placeholders with NanoBanana 2 renders when API key is available."
