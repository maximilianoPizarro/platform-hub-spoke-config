#!/usr/bin/env python3
"""Generate workshop hero images (1200x630) via Google Gemini Imagen API.

Uses the same Google AI Studio API key as Gemini in Cursor (BYOK) or GEMINI_API_KEY.

  export GEMINI_API_KEY="..."   # https://aistudio.google.com/apikey
  python scripts/generate_workshop_images.py
  FORCE=1 python scripts/generate_workshop_images.py   # regenerate all

Fallback order: Gemini Imagen -> platform PNG assets -> styled PIL placeholders.
"""
from __future__ import annotations

import base64
import json
import os
import struct
import sys
import time
import urllib.error
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets" / "images"
SHOWROOM_EN = ROOT / "showroom-hybrid-mesh-ai/content/modules/en/modules/ROOT/images"
SHOWROOM_ES = ROOT / "showroom-hybrid-mesh-ai/content/modules/es/modules/ROOT/images"
DOCS_IMG = ROOT / "docs/assets/images/workshop"

IMAGEN_MODEL = os.environ.get("GEMINI_IMAGEN_MODEL", "imagen-4.0-fast-generate-001")
IMAGEN_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{IMAGEN_MODEL}:predict"
)

# filename, prompt, optional fallback asset basename under docs/assets/images/
IMAGE_SPECS: list[tuple[str, str, str]] = [
    (
        "00-index-hybrid-mesh.png",
        "Professional tech illustration, Red Hat hybrid cloud hub-spoke architecture, central OpenShift hub connected to east and west factory edge spokes, subtle AWS cloud icons, clean white background, red EE0000 accent bars, 16:9 widescreen, high quality, no text",
        "arch-hub-spoke-flow.png",
    ),
    (
        "01-hybrid-strategy.png",
        "Hybrid Mesh AI platform executive diagram, centralized hub edge cloud environments, AI security GitOps edge pillars, clean white background, Red Hat red accents, flat professional 16:9",
        "arch-overview.png",
    ),
    (
        "02-rosa-architecture.png",
        "Red Hat OpenShift hub-spoke topology diagram, ACM fleet hub with east west spokes, ApplicationSet GitOps sync, Skupper VAN, clean white background, red EE0000 accents, flat professional 16:9, labeled components",
        "arch-hub-spoke-flow.png",
    ),
    (
        "03-security-scale-hybrid.png",
        "Cybersecurity and autoscaling hybrid cloud diagram, shield lock HPA graph factory sensors, ACS and service mesh concept, Red Hat red accent, 16:9 illustration, no text",
        "",
    ),
    (
        "04-aws-ai-integration.png",
        "OpenShift AI inference architecture, DataScienceCluster KServe ModelMesh MaaS API OpenAI compatible, consumers NeuroFace DevSpaces Lightspeed, white background Red Hat red accents, 16:9",
        "22-openshift-ai.png",
    ),
    (
        "05-cases-roadmap.png",
        "Industrial Edge data flow diagram, factory sensors MQTT Kafka Camel CDC PostgreSQL dashboard, workshop customer journey, white background Red Hat red accents, 16:9",
        "arch-data-flow.png",
    ),
    (
        "10-acm-multicluster.png",
        "Red Hat ACM multicluster fleet management, hub controlling multiple OpenShift clusters on world map, 16:9 professional illustration, no text",
        "ACM.png",
    ),
    (
        "11-hybrid-mesh.png",
        "Skupper service interconnect hybrid mesh, Gateway API traffic hub to edge spokes encrypted links, network topology, red accents, 16:9, no text",
        "arch-skupper-topology.png",
    ),
    (
        "12-software-templates.png",
        "Developer Hub Backstage software template golden path, developer creating app from catalog, teal and red, 16:9, no text",
        "product-developer-hub.png",
    ),
    (
        "13-deploy-industrial-edge.png",
        "Industrial Edge factory OT dashboard Kafka sensors on OpenShift edge cluster, manufacturing digital twin, 16:9, no text",
        "industrial-edge.png",
    ),
    (
        "14-kairos-scaling.png",
        "Kubernetes autoscaling SmartScaling CPU memory graphs Kairos operator recommendations, cyan red, 16:9, no text",
        "kairos-observability.png",
    ),
    (
        "15-observability.png",
        "Observability Prometheus Grafana Jaeger tracing multicluster dashboards, SRE monitoring, 16:9, no text",
        "product-grafana-observability.png",
    ),
    (
        "16-openshift-gitops.png",
        "OpenShift GitOps Argo CD continuous delivery Git to multiple clusters sync waves, 16:9, no text",
        "product-argocd-openshift-gitops.png",
    ),
    (
        "17-service-mesh.png",
        "OpenShift Service Mesh ambient mode Kiali service graph mTLS microservices factory apps, 16:9, no text",
        "product-kiali-service-mesh.png",
    ),
    (
        "18-scalability.png",
        "Horizontal Pod Autoscaler HPA Kafka streaming scale sensor spike factory workload, 16:9, no text",
        "",
    ),
    (
        "19-network-policies.png",
        "Kubernetes network policy microsegmentation allowed denied traffic paths OVN factory namespace, 16:9, no text",
        "",
    ),
    (
        "20-acs-kuadrant.png",
        "Red Hat ACS security shield and Kuadrant API gateway keys rate limits, combined illustration, 16:9, no text",
        "ACS.png",
    ),
    (
        "21-finops-kubecost.png",
        "FinOps Kubecost Kubernetes cost allocation charts namespace spend, teal red, 16:9, no text",
        "kubecost.png",
    ),
    (
        "22-openshift-ai.png",
        "OpenShift AI DataScienceCluster Jupyter notebook ModelMesh inference pipeline, red hat AI, 16:9, no text",
        "openshift-ia.png",
    ),
    (
        "23-ai-gateway.png",
        "AI Gateway API management Kuadrant HTTPRoute LLM MaaS endpoint factory apps chat completions, 16:9, no text",
        "",
    ),
    (
        "24-mcp-gateway.png",
        "Model Context Protocol MCP gateway federated tools ArgoCD Kubernetes developer AI assistant, 16:9, no text",
        "",
    ),
    (
        "25-llm-rag.png",
        "LLM RAG retrieval augmented generation vector database factory runbooks OpenShift AI, 16:9, no text",
        "",
    ),
    (
        "27-neuroface.png",
        "NeuroFace AI webcam face detection dashboard chat MaaS factory operator UI, 16:9, no text",
        "",
    ),
    (
        "28-ai-end-user-apps.png",
        "End user factory operator dashboard mobile alerts line dashboard AI insights embedded manufacturing UX, 16:9, no text",
        "",
    ),
    (
        "29-full-verification.png",
        "Full stack verification checklist workshop graduation green checks OpenShift multicluster AI, 16:9, no text",
        "",
    ),
]

ACRONYMS = {
    "ai", "acs", "acm", "aws", "mcp", "maas", "rag", "llm", "ie", "rosa",
    "api", "hpa", "e2e", "ui", "ovms", "gitops",
}

THEMES: dict[str, tuple[str, str, str]] = {
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


def resolve_api_key() -> str:
    for name in (
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "CURSOR_GEMINI_API_KEY",
    ):
        val = os.environ.get(name, "").strip()
        if val:
            return val
    key_file = ROOT / ".gemini_api_key"
    if key_file.is_file():
        return key_file.read_text(encoding="utf-8").strip()
    return ""


def label_from_filename(fname: str) -> str:
    stem = Path(fname).stem
    words = stem.replace("-", " ").split()
    parts: list[str] = []
    for w in words:
        if w.isdigit():
            parts.append(w)
        elif w.lower() in ACRONYMS:
            parts.append(w.upper())
        else:
            parts.append(w.capitalize())
    return " ".join(parts)


def resize_to_hero(src: Path, dest: Path) -> None:
    try:
        from PIL import Image

        img = Image.open(src).convert("RGB")
        img = img.resize((1200, 630), Image.Resampling.LANCZOS)
        img.save(dest, format="PNG", optimize=True)
    except ImportError:
        dest.write_bytes(src.read_bytes())


def generate_gemini_imagen(api_key: str, prompt: str, dest: Path) -> bool:
    body = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9",
            "imageSize": "2K",
            "personGeneration": "dont_allow",
        },
    }
    req = urllib.request.Request(
        IMAGEN_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        print(f"  Gemini Imagen HTTP {exc.code}: {err_body[:300]}", file=sys.stderr)
        return False
    except urllib.error.URLError as exc:
        print(f"  Gemini Imagen network error: {exc}", file=sys.stderr)
        return False

    predictions = payload.get("predictions") or []
    if not predictions:
        print(f"  Gemini Imagen empty response: {payload}", file=sys.stderr)
        return False
    b64 = predictions[0].get("bytesBase64Encoded")
    if not b64:
        print(f"  Gemini Imagen no image bytes: {predictions[0]}", file=sys.stderr)
        return False

    tmp = dest.with_suffix(".tmp.png")
    tmp.write_bytes(base64.b64decode(b64))
    resize_to_hero(tmp, dest)
    tmp.unlink(missing_ok=True)
    return True


def generate_placeholder(fname: str, dest: Path) -> None:
    stem = Path(fname).stem
    label = label_from_filename(fname)
    theme_key = next((k for k in THEMES if k in stem), "index")
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
        img.save(dest, format="PNG", optimize=True)
        return
    except ImportError:
        pass

    raw = b"".join(b"\x00" + b"\xf5\xf5\xf5" * w for _ in range(h))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    dest.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def publish(dest: Path, fname: str) -> None:
    for folder in (DOCS_IMG, SHOWROOM_ES):
        folder.mkdir(parents=True, exist_ok=True)
        (folder / fname).write_bytes(dest.read_bytes())


def main() -> int:
    force = os.environ.get("FORCE", "0") == "1"
    api_key = resolve_api_key()
    use_gemini = bool(api_key)

    SHOWROOM_EN.mkdir(parents=True, exist_ok=True)
    DOCS_IMG.mkdir(parents=True, exist_ok=True)

    if use_gemini:
        print(f"Using Google Gemini Imagen ({IMAGEN_MODEL}) — same API family as Gemini in Cursor.")
    else:
        print(
            "GEMINI_API_KEY not set — using platform art + placeholders.\n"
            "Get a free key: https://aistudio.google.com/apikey\n"
            "  export GEMINI_API_KEY=... && FORCE=1 python scripts/generate_workshop_images.py"
        )

    gemini_ok = 0
    for fname, prompt, fallback in IMAGE_SPECS:
        out = SHOWROOM_EN / fname
        if out.is_file() and not force:
            publish(out, fname)
            continue

        generated = False
        if use_gemini:
            print(f"Gemini: {fname}...")
            if generate_gemini_imagen(api_key, prompt, out):
                generated = True
                gemini_ok += 1
                print(f"  -> {out}")
                time.sleep(2)
            else:
                print("  failed — trying fallback")

        if not generated:
            fb = ASSETS / fallback if fallback else None
            if fb and fb.is_file():
                resize_to_hero(fb, out)
                print(f"Copied {fallback} -> {out}")
            else:
                generate_placeholder(fname, out)
                print(f"Placeholder -> {out}")

        publish(out, fname)

    print(f"Done. {len(IMAGE_SPECS)} images; Gemini generated {gemini_ok}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
