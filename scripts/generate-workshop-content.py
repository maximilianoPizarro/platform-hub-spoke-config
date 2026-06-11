#!/usr/bin/env python3
"""Generate Hybrid Mesh AI Workshop Showroom (.adoc) and GitHub Pages (.md) modules."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from workshop_module_extended import extended_section_body  # noqa: E402
from workshop_content_data import (  # noqa: E402
    CRED_NOTE_EN,
    ESTIMATED_MIN,
    FACILITATOR_ONLY_SLUGS,
    HYBRID_INTEGRATION_EN,
    INDEX_INTRO_EN,
    INDEX_HUB_SPOKE_EN,
    INDEX_MESH_FLOW_EN,
    INDEX_AI_MAAS_EN,
    INDEX_KUADRANT_EN,
    INDEX_VERIFY_EN,
    LAB_ACCESS_EN,
    LEARN_MORE_EN,
    MODULE_CONTEXT,
    NARRATIVES,
    NEXT_PAGE,
    PREREQUISITES_EN,
    PRODUCT_CATALOG_EN,
    PROGRESS_UI_EN,
    REGISTRATION_CTA_EN,
    SHOW_TELL_EN,
    TODO_EN,
)

SHOWROOM = ROOT / "showroom-hybrid-mesh-ai"
DOCS = ROOT / "docs" / "workshop"

# slug → (GitOps source table rows, verify command) — no fabricated YAML snippets
GITOPS_REF: dict[str, tuple[str, str]] = {
    "hybrid-cloud-strategy": (
        "| ACM fleet UI | `components/acm-hub-spoke/` |\n| Hub app-of-apps | `templates/component-applications.yaml` |",
        "oc get managedclusters 2>/dev/null | head -5",
    ),
    "rosa-architecture": (
        "| ManagedCluster CRs | `components/acm-hub-spoke/templates/managed-clusters.yaml` |\n| Spoke registration | ACM → Clusters UI on this hub |",
        "oc get managedclusters -o wide",
    ),
    "security-scale-hybrid": (
        "| ACS operator | `components/acs-operator/` |\n| ACS Central route | namespace `stackrox` |",
        "oc get central -n stackrox; oc get ns stackrox --show-labels | head -3",
    ),
    "aws-ai-integration": (
        "| OpenShift AI hub | `components/openshift-ai-hub/` |\n| MaaS credentials | namespace `maas-workshop` |",
        "oc get dsc -A 2>/dev/null; oc get ns maas-workshop 2>/dev/null",
    ),
    "cases-roadmap": (
        "| Showroom | `components/showroom/` |\n| Registration | `components/workshop-registration/` |",
        "curl -sk -o /dev/null -w '%{http_code}' https://workshop-registration.%HUB_DOMAIN%/api/health",
    ),
    "acm-multicluster": (
        "| ManagedCluster | `components/acm-hub-spoke/templates/managed-clusters.yaml` |\n| GitOpsCluster | `components/acm-hub-spoke/templates/gitops-cluster.yaml` |",
        "oc get managedclusters; oc get gitopscluster -A 2>/dev/null | head -5",
    ),
    "hybrid-mesh-architecture": (
        "| Hub gateway | `components/hub-gateway/` |\n| Skupper | `components/service-interconnect/` |",
        "oc get httproute -n hub-gateway-system 2>/dev/null | head -5",
    ),
    "software-templates": (
        "| Template catalog | `docs/assets/backstage/software-templates/` |\n| Plan B demos | `components/workshop-demos/files/catalog/hybrid-mesh-shared-demos.yaml` |",
        "oc get configmap developer-hub-catalog-demos -n developer-hub 2>/dev/null",
    ),
    "deploy-industrial-edge": (
        "| IE on spoke | `components/industrial-edge-tst/` (east Application) |\n| Line dashboard | namespace `industrial-edge-tst-all` |",
        "oc get deploy -n industrial-edge-tst-all 2>/dev/null | head -8",
    ),
    "kairos-scaling": (
        "| Kairos policies | `components/kairos/templates/sensor-scan-policies.yaml` |\n| Kairos Console | `components/kairos/` |",
        "oc get smartscalingpolicy -A 2>/dev/null | head -5",
    ),
    "observability": (
        "| Grafana dashboards | `components/grafana-dashboards/` |\n| OTEL | `components/opentelemetry/` |",
        "oc get route -n openshift-cluster-observability-operator 2>/dev/null | head -3",
    ),
    "openshift-gitops": (
        "| Hub Applications | `templates/component-applications.yaml` |\n| ApplicationSet IE | `components/acm-hub-spoke/templates/applicationset.yaml` |",
        "oc get applications -n openshift-gitops 2>/dev/null | head -10",
    ),
    "service-mesh": (
        "| OSSM3 subscription | `components/servicemeshoperator3/` |\n| Kiali | `components/kiali/` |",
        "oc get istio -n istio-system 2>/dev/null; oc get kiali -A 2>/dev/null | head -3",
    ),
    "scalability": (
        "| IE workloads | `components/industrial-edge-tst/` |\n| HPA / Kafka | spoke namespace `industrial-edge-tst-all` |",
        "oc get hpa -n industrial-edge-tst-all 2>/dev/null",
    ),
    "network-policies": (
        "| NP demo | `components/workshop-demos/templates/network-policy-demo.yaml` |\n| IE namespace | `industrial-edge-tst-all` |",
        "oc get networkpolicy -n industrial-edge-tst-all 2>/dev/null",
    ),
    "acs-kuadrant": (
        "| Workshop APIs | `components/workshop-kuadrant-apis/` |\n| Hub gateway | `components/hub-gateway/` |",
        "oc get httproute,serviceentry -n hub-gateway-system 2>/dev/null | grep -i workshop | head -5",
    ),
    "finops-kubecost": (
        "| Kubecost | `components/kubecost/` |\n| MinIO data lake | `components/industrial-edge-minio/` |",
        "oc get deploy -n kubecost 2>/dev/null | head -3",
    ),
    "openshift-ai": (
        "| DSC + ModelMesh | `components/openshift-ai-hub/` |\n"
        "| Notebooks | `user-projects.yaml` → `workshop-notebook` |\n"
        "| ModelMesh ISVC | `workshop-sklearn` per `ai-userN` |\n"
        "| MCP + Playground | `ods-mcp-server.yaml`, `dashboard-config.yaml` |",
        "oc get dsc; oc get notebook,inferenceservice -n ai-%USER_NAME% 2>/dev/null",
    ),
    "ai-gateway": (
        "| HTTPRoute + policies | `components/workshop-kuadrant-apis/` |\n"
        "| Catalog | `catalog-ai-platform.yaml` → workshop-ai-gateway |",
        "oc get httproute -n hub-gateway-system 2>/dev/null | grep workshop",
    ),
    "mcp-gateway": (
        "| MCP CRDs + controller | `components/mcp-gateway/` |\n"
        "| Lightspeed MCP | `llama-stack-run.yaml` tool_groups |",
        "oc get mcpserverregistration -n mcp-system 2>/dev/null",
    ),
    "llm-rag": (
        "| Developer Hub Lightspeed | `components/developer-hub/` |\n| MaaS endpoint | hub `maas-workshop` |",
        "oc get deploy -n developer-hub 2>/dev/null | head -5",
    ),
    "text-ai-predictive": (
        "| IE alerter | `components/ie-anomaly-alerter/` |\n| Kafka topics | `industrial-edge-tst-all` |",
        "oc get deploy -n industrial-edge-tst-all 2>/dev/null | grep -i anomaly",
    ),
    "neuroface": (
        "| NeuroFace chart | `components/neuroface/` |\n| Route | `neuroface.%HUB_DOMAIN%` |",
        "curl -sk -o /dev/null -w '%{http_code}' https://neuroface.%HUB_DOMAIN%/",
    ),
    "ai-end-user-apps": (
        "| Line dashboard | `industrial-edge-tst-all` |\n| Developer Hub IE catalog | `components/developer-hub/files/catalog/industrial-edge-system.yaml` |",
        "oc get deploy -n industrial-edge-tst-all line-dashboard 2>/dev/null",
    ),
}

MODULES = [
    ("00", "index", "Hybrid Mesh AI Workshop", "A", True),
    ("01", "hybrid-cloud-strategy", "Hybrid Cloud Strategy", "A", False),
    ("02", "rosa-architecture", "ROSA Architecture & Benefits", "A", False),
    ("03", "security-scale-hybrid", "Security & Scale in Hybrid", "A", False),
    ("04", "aws-ai-integration", "AWS Services & AI Integration", "A", False),
    ("05", "cases-roadmap", "Real Cases & Roadmap", "A", False),
    ("10", "acm-multicluster", "Multicluster Fleet & ACM", "B", False),
    ("11", "hybrid-mesh-architecture", "Hybrid Mesh Architecture", "B", False),
    ("12", "software-templates", "Software Templates", "B", False),
    ("13", "deploy-industrial-edge", "Deploy Industrial Edge Apps", "B", False),
    ("14", "kairos-scaling", "Worker Scaling with Kairos", "B", False),
    ("15", "observability", "Metrics Logging Dashboards", "B", False),
    ("16", "openshift-gitops", "OpenShift GitOps", "B", False),
    ("17", "service-mesh", "OpenShift Service Mesh", "B", False),
    ("18", "scalability", "Scalability HPA Kafka", "B", False),
    ("19", "network-policies", "Network Policies", "B", False),
    ("20", "acs-kuadrant", "ACS & Connectivity Link", "B", False),
    ("21", "finops-kubecost", "FinOps with Kubecost", "B", False),
    ("22", "openshift-ai", "OpenShift AI Workshop", "B", False),
    ("23", "ai-gateway", "AI Gateway — MaaS + Kuadrant", "B", False),
    ("24", "mcp-gateway", "MCP Gateway + Lightspeed", "B", False),
    ("25", "llm-rag", "LLMs & RAG", "B", False),
    ("26", "text-ai-predictive", "Generative & Predictive Text", "B", False),
    ("27", "neuroface", "Face & Object AI + Chat", "B", False),
    ("28", "ai-end-user-apps", "AI in End-User Apps", "B", False),
    ("29", "full-verification", "Full Stack Verification (facilitator)", "F", False, True),
    ("30", "agent-browser-recording", "Agent Browser (facilitator)", "F", False, True),
]

IMAGE_BY_SLUG = {
    "index": ("00-index-hybrid-mesh.png", "Hybrid Mesh AI hub-spoke architecture diagram"),
    "hybrid-cloud-strategy": ("01-hybrid-strategy.png", "Hybrid cloud strategy overview"),
    "rosa-architecture": ("02-rosa-architecture.png", "ROSA and OpenShift hub-spoke architecture"),
    "security-scale-hybrid": ("03-security-scale-hybrid.png", "Hybrid cloud security and scale"),
    "aws-ai-integration": ("04-aws-ai-integration.png", "AWS and AI integration on OpenShift"),
    "cases-roadmap": ("05-cases-roadmap.png", "Customer cases and workshop roadmap"),
    "acm-multicluster": ("10-acm-multicluster.png", "ACM multicluster fleet management"),
    "hybrid-mesh-architecture": ("11-hybrid-mesh.png", "Hybrid mesh traffic flow hub to spokes"),
    "software-templates": ("12-software-templates.png", "Developer Hub software templates"),
    "deploy-industrial-edge": ("13-deploy-industrial-edge.png", "Industrial Edge deployment on spoke"),
    "kairos-scaling": ("14-kairos-scaling.png", "Kairos SmartScaling recommendations"),
    "observability": ("15-observability.png", "Observability dashboards and tracing"),
    "openshift-gitops": ("16-openshift-gitops.png", "OpenShift GitOps and Argo CD"),
    "service-mesh": ("17-service-mesh.png", "OpenShift Service Mesh ambient"),
    "scalability": ("18-scalability.png", "HPA and Kafka scalability"),
    "network-policies": ("19-network-policies.png", "Network policies workshop demo"),
    "acs-kuadrant": ("20-acs-kuadrant.png", "ACS and Kuadrant API security"),
    "finops-kubecost": ("21-finops-kubecost.png", "FinOps Kubecost cost allocation"),
    "openshift-ai": ("22-openshift-ai.png", "OpenShift AI DataScienceCluster"),
    "ai-gateway": ("23-ai-gateway.png", "AI Gateway Kuadrant MaaS"),
    "mcp-gateway": ("24-mcp-gateway.png", "MCP Gateway federated tools"),
    "llm-rag": ("25-llm-rag.png", "LLM and RAG with MaaS"),
    "neuroface": ("27-neuroface.png", "NeuroFace AI dashboard with webcam and chat"),
    "ai-end-user-apps": ("28-ai-end-user-apps.png", "AI in end-user applications"),
    "full-verification": ("29-full-verification.png", "Full stack workshop verification"),
}


def clickable_lab_access(text: str) -> str:
    """Convert backtick-wrapped https URLs in lab tables to AsciiDoc link: macros."""

    def linkify_line(line: str) -> str:
        m = re.search(r"`(https?://[^`]+)`", line)
        if not m:
            return line
        url = m.group(1)
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3 and parts[1]:
            label = parts[1]
            return line.replace(f"`{url}`", f"link:{url}[{label}]")
        return line.replace(f"`{url}`", f"link:{url}[Open]")

    return "\n".join(linkify_line(line) for line in text.split("\n"))


def gitops_section(slug: str) -> str:
    if slug in FACILITATOR_ONLY_SLUGS or slug not in GITOPS_REF:
        return ""
    table, verify = GITOPS_REF[slug]
    rows = "\n".join(
        "| " + " | ".join(cell.strip() for cell in line.split("|") if cell.strip()) + " |"
        for line in table.strip().split("\n")
        if line.strip()
    )
    return f"""
== Where this lab is defined

NOTE: Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
|===
| UI / capability | Source in GitOps repo

{rows}
|===

Verify in the Showroom terminal:

[source,bash]
----
{verify.strip()}
----
"""


def module_context_section(slug: str) -> str:
    if slug not in MODULE_CONTEXT:
        return ""
    banner = ""
    if slug in FACILITATOR_ONLY_SLUGS:
        banner = "IMPORTANT: **Facilitator / automation agent only** — this page is not part of the learner navigation.\n\n"
    return f"""
== What you will do

{banner}{(MODULE_CONTEXT[slug] if isinstance(MODULE_CONTEXT[slug], str) else MODULE_CONTEXT[slug]["en"]).strip()}
"""


def callout_ref() -> str:
    return "\nNOTE: For AWS/Azure integration snippets see xref:00-index.adoc#hybrid-integration[Module 00 — hybrid integration notes].\n"


def lab_access_section(slug: str) -> str:
    if slug not in LAB_ACCESS_EN:
        return ""
    note = ""
    if slug != "index":
        note = CRED_NOTE_EN.strip() + "\n\n"
    body = clickable_lab_access(LAB_ACCESS_EN[slug].strip())
    return f"\n== Lab access — URLs & credentials\n\n{note}{body}\n"


def next_nav(slug: str) -> str:
    nxt = NEXT_PAGE.get(slug)
    if not nxt:
        return ""
    stem = nxt.replace(".adoc", ".html")
    return f"""
++++
<div class="workshop-next-nav">
  <a href="{stem}">Next → {nxt.replace('.adoc', '').replace('-', ' ')}</a>
</div>
++++
"""


def time_badge(minutes: int) -> str:
    label = f"~{minutes} min"
    return f"""
++++
<span class="workshop-time-badge">{label}</span>
++++
"""


def extended_section(slug: str) -> str:
    if slug in FACILITATOR_ONLY_SLUGS:
        return ""
    body = extended_section_body(slug)
    if not body:
        return ""
    return f"""
== Features, benefits & cloud configuration

{body}
"""


def learn_more_section(slug: str) -> str:
    """Red Hat external docs — deep links after Overview."""
    if slug in FACILITATOR_ONLY_SLUGS:
        return ""
    body = LEARN_MORE_EN.get(slug, "")
    if not body:
        return ""
    return f"""
=== Learn more

{body.strip()}
"""


def track_pacing_section() -> str:
    return """
NOTE: **Workshop pacing (~4 hours hands-on)** — Each module includes **Overview-only** steps (demo/visualization, ~5–10 min) and **Hands-on** steps (full lab). Skip Hands-on blocks to run a ~90-minute executive tour.

"""


def adoc_page(num: str, slug: str, title: str, is_index: bool) -> str:
    mid = "00-index" if is_index else f"{num}-{slug}"
    minutes = ESTIMATED_MIN.get(slug, 15)
    time_label = time_badge(minutes)
    narrative = NARRATIVES[slug] if isinstance(NARRATIVES[slug], str) else NARRATIVES[slug]["en"]
    show_tell = SHOW_TELL_EN[slug]
    todos_raw = TODO_EN[slug]
    todos = "\n".join(todos_raw) if isinstance(todos_raw, list) else todos_raw
    progress = PROGRESS_UI_EN.format(module_id=mid)
    live = ""
    if not is_index and num.isdigit() and int(num) >= 10:
        live = "\n== Live lab\n\n* Showroom integrated `oc` terminal — use hub context unless module says east/west.\n"

    img = ""
    if slug in IMAGE_BY_SLUG:
        fname, alt = IMAGE_BY_SLUG[slug]
        img = f"\nimage::{fname}[{alt},960]\n"

    index_block = ""
    if is_index:
        lab_access = lab_access_section(slug)
        agenda = """
== Dual agenda

.Part A — Executive (01–05)
[cols="1,3"]
|===
| 01 | Hybrid Cloud Strategy
| 02 | ROSA Architecture & Benefits
| 03 | Security & Scale in Hybrid
| 04 | AWS Services & AI Integration
| 05 | Real Cases & Roadmap
|===

.Part B — Hands-on (10–28, ~4 hours)
[cols="1,3"]
|===
| 10–14 | Foundation — ACM, mesh, templates, IE, Kairos
| 15–18 | Operations — observability, GitOps, mesh, scale
| 19–21 | Security & FinOps — NP, ACS/Kuadrant, Kubecost
| 22–24 | OpenShift AI — projects, AI Gateway, MCP Gateway
| 25–28 | LLM, NeuroFace (OVMS), end-user apps
|===

NOTE: Modules 29–30 (verification & Agent Browser) are **facilitator/agent tasks** only — see `showroom-hybrid-mesh-ai/verification/`. Each Part B module supports **Overview-only** (~90 min) vs **Hands-on** (~4 h).

== Registration & Plan B demos

* Register: link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[workshop registration] → redirect with `USER_NAME=%USER_NAME%`
* OpenShift Console: **Hybrid Mesh AI Workshop** (ApplicationMenu)
* Developer Hub → System `hybrid-mesh-shared-demos` (Plan B without scaffolder)
* NeuroFace: link:https://neuroface.%HUB_DOMAIN%[NeuroFace]
* Kuadrant: link:https://developer-hub.%HUB_DOMAIN%/kuadrant[Kuadrant UI] + link:https://workshop-apis.%HUB_DOMAIN%[Workshop APIs]
"""
        index_parts = [
            "== Welcome",
            INDEX_INTRO_EN.strip(),
            REGISTRATION_CTA_EN.strip(),
            INDEX_HUB_SPOKE_EN.strip(),
            INDEX_MESH_FLOW_EN.strip(),
            INDEX_AI_MAAS_EN.strip(),
            INDEX_KUADRANT_EN.strip(),
            lab_access.strip(),
            PRODUCT_CATALOG_EN.strip(),
            PREREQUISITES_EN.strip(),
            agenda.strip(),
            HYBRID_INTEGRATION_EN.strip(),
        ]
        index_block = "\n\n".join(index_parts)
    else:
        index_block = callout_ref()

    overview_section = ""
    if not is_index and slug not in FACILITATOR_ONLY_SLUGS:
        overview_section = f"""
== Overview

{track_pacing_section() if (not is_index and num.isdigit() and int(num) >= 10) else ""}{narrative.strip()}
{learn_more_section(slug)}
{extended_section(slug)}
"""
    elif slug in FACILITATOR_ONLY_SLUGS:
        overview_section = module_context_section(slug)

    context_section = ""
    if not is_index and slug not in FACILITATOR_ONLY_SLUGS and slug in MODULE_CONTEXT:
        context_section = module_context_section(slug)

    body_lab_access = "" if is_index or slug in FACILITATOR_ONLY_SLUGS else lab_access_section(slug)

    show_block = ""
    todo_block = ""
    verify_block = ""
    if slug not in FACILITATOR_ONLY_SLUGS:
        show_block = f"""
== Show and Tell

{show_tell.strip()}
"""
        todo_block = f"""
== Your TODO (user %USER_NAME%)

{todos.strip()}
"""
        if is_index:
            verify_body = INDEX_VERIFY_EN.strip()
        else:
            verify_body = """[cols="1,2,1"]
|===
| Check | Action | Expected

| Progress | Save checkboxes below | `POST /api/progress` returns OK
|==="""
        verify_block = f"""
== Verify

{verify_body}
"""

    return f"""= {title}

{time_label.strip()}
{img}
{index_block.strip()}

{context_section.strip()}

{overview_section.strip()}

{body_lab_access}
{show_block.strip()}
{todo_block.strip()}
{live}{gitops_section(slug)}
{verify_block.strip()}

{progress if slug not in FACILITATOR_ONLY_SLUGS else ""}

{"TIP: Plan B — shared demo in Developer Hub → System `hybrid-mesh-shared-demos` if scaffolder fails." if slug not in FACILITATOR_ONLY_SLUGS else ""}

{next_nav(slug)}
"""


SHOWROOM_BANNER = (
    "> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — "
    "register: `https://workshop-registration.YOUR_HUB_DOMAIN/`"
)


def asciidoc_to_md(text: str) -> str:
    """Best-effort AsciiDoc → Markdown for GitHub Pages (English workshop mirror)."""
    out: list[str] = []
    in_source: str | None = None
    source_delim_seen = False
    skip_passthrough = False
    for line in text.splitlines():
        if line.strip() == "++++":
            skip_passthrough = not skip_passthrough
            continue
        if skip_passthrough:
            continue
        if line.startswith("[source,"):
            lang = line.split(",", 1)[1].rstrip("]").strip() or "text"
            in_source = lang
            source_delim_seen = False
            out.append(f"```{lang}")
            continue
        if line.strip() == "----":
            if in_source:
                if not source_delim_seen:
                    source_delim_seen = True
                    continue
                out.append("```")
                in_source = None
                source_delim_seen = False
            continue
        if in_source:
            out.append(line)
            continue
        if line.startswith("=== "):
            out.append(f"### {line[4:].strip()}")
            continue
        if line.startswith("== "):
            out.append(f"## {line[3:].strip()}")
            continue
        if line.startswith("image::"):
            m = re.match(r"image::([^[]+)\[([^,\]]+)", line)
            if m:
                fname, alt = m.group(1), m.group(2)
                out.append(
                    f"![{alt}]({{{{ site.baseurl }}}}/assets/images/workshop/{fname})"
                )
            continue
        line = re.sub(
            r"link:([^[]+)\[([^\]]+)\]",
            r"[\2](\1)",
            line,
        )
        if line.startswith("NOTE:"):
            out.append(f"> {line[5:].strip()}")
            continue
        if line.startswith("IMPORTANT:"):
            out.append(f"> **Important:** {line[12:].strip()}")
            continue
        if line.startswith("|==="):
            continue
        if line.startswith("|") and line.count("|") >= 2:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and not all(set(c) <= {"-", "="} for c in cells):
                out.append("| " + " | ".join(cells) + " |")
            continue
        out.append(line)
    return "\n".join(out).strip()


def md_front_matter(
    title: str, nav_order: int, parent: str | None = None, has_children: bool = False
) -> str:
    fm = [
        "---",
        "layout: default",
        f"title: {title}",
    ]
    if has_children:
        fm.append("has_children: true")
    if parent:
        fm.append(f"parent: {parent}")
    fm.extend([f"nav_order: {nav_order}", "---", ""])
    return "\n".join(fm)


def write_github_pages() -> None:
    """Mirror English workshop content to docs/workshop/ for Jekyll GitHub Pages."""
    parent = "Hybrid Mesh AI Workshop"
    index_body = "\n\n".join(
        [
            SHOWROOM_BANNER,
            "",
            "# Hybrid Mesh AI Workshop",
            "",
            asciidoc_to_md(INDEX_INTRO_EN),
            "",
            asciidoc_to_md(INDEX_HUB_SPOKE_EN),
            "",
            asciidoc_to_md(INDEX_MESH_FLOW_EN),
            "",
            asciidoc_to_md(INDEX_AI_MAAS_EN),
            "",
            asciidoc_to_md(INDEX_KUADRANT_EN),
            "",
            asciidoc_to_md(HYBRID_INTEGRATION_EN),
            "",
            "## Dual agenda",
            "",
            "**Part A (01–05)** — Executive strategy modules.",
            "",
            "**Part B (10–28)** — Hands-on labs on the live RHDP fleet (~4 h).",
            "",
            "Facilitator-only modules 29–30 stay in-cluster Showroom only.",
            "",
            "## Live vs this mirror",
            "",
            "| Surface | URL | Notes |",
            "|---------|-----|-------|",
            "| **Showroom (hands-on)** | `https://showroom-showroom.YOUR_HUB_DOMAIN/` | Antora + embedded `oc` terminal |",
            "| **Registration** | `https://workshop-registration.YOUR_HUB_DOMAIN/` | Assigns `userN` |",
            "| **GitHub Pages (read-only)** | [Workshop mirror]({{ site.baseurl }}/workshop/) | This section |",
            "| **Antora source** | [showroom-hybrid-mesh-ai](https://github.com/maximilianoPizarro/showroom-hybrid-mesh-ai) | Regenerate with `python scripts/generate-workshop-content.py` |",
            "",
            "*Screen recordings are not published in this repository.*",
        ]
    )
    (DOCS / "index.md").write_text(
        md_front_matter("Hybrid Mesh AI Workshop", 11, has_children=True) + index_body + "\n",
        encoding="utf-8",
    )

    (DOCS / "registration.md").write_text(
        md_front_matter("Workshop Registration", 1, parent)
        + f"""{SHOWROOM_BANNER}

# Workshop Registration

Register via OpenShift Console **Hybrid Mesh AI Workshop** or directly at `https://workshop-registration.YOUR_HUB_DOMAIN/?USER_NAME=userN`.

After email registration you receive `userN` and are redirected to the Showroom with an embedded `oc` terminal.

**Demo password:** `Welcome123!` (Developer Hub Keycloak + OpenShift htpasswd on hub/east/west).
""",
        encoding="utf-8",
    )

    (DOCS / "showroom-live.md").write_text(
        md_front_matter("Showroom Live Lab", 3, parent)
        + f"""{SHOWROOM_BANNER}

# Showroom Live

| Item | URL |
|------|-----|
| Registration | `https://workshop-registration.YOUR_HUB_DOMAIN/` |
| Showroom home | `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` |
| Developer Hub Plan B | `https://developer-hub.YOUR_HUB_DOMAIN/catalog/default/system/hybrid-mesh-shared-demos` |
| NeuroFace | `https://neuroface.YOUR_HUB_DOMAIN/` |

Replace `YOUR_HUB_DOMAIN` with your hub ingress domain (e.g. `apps.cluster-xxxx.dynamic2.redhatworkshops.io`).

**Antora source:** [showroom-hybrid-mesh-ai](https://github.com/maximilianoPizarro/showroom-hybrid-mesh-ai) — cloned at Showroom build time by the git-cloner init container.
""",
        encoding="utf-8",
    )

    shared = """| Demo | Catalog entity | Notes |
|------|----------------|-------|
| Industrial Edge | demo-industrial-edge-east | Line dashboard on east |
| Camel Kaoto | demo-camel-kaoto-east | DevSpaces + Topology |
| Camel CDC | demo-camel-cdc-east | Mailpit Templates inbox |
| API Product | demo-ie-api-product | Kuadrant workshop-apis |
| AI Gateway | demo-ai-gateway | MaaS via Kuadrant |
| MCP Gateway | demo-mcp-gateway | Lightspeed + ODS MCP |
| OpenShift AI | demo-ods-workspace | ODS dashboard |
| CNV VM | demo-cnv-vm | workshop-cnv-demo |
| NeuroFace | demo-neuroface | Webcam + MaaS chat |
| Mailpit Templates | demo-mailpit-templates | Scaffolder SMTP (separate from IE alerts) |
"""
    (DOCS / "shared-demos.md").write_text(
        md_front_matter("Shared Demos (Plan B)", 2, parent)
        + f"""{SHOWROOM_BANNER}

# Shared Demos — Plan B

Pre-deployed examples in Developer Hub System **`hybrid-mesh-shared-demos`** — no scaffolder required.

{shared}
""",
        encoding="utf-8",
    )

    parte_a_dir = DOCS / "parte-a"
    parte_b_dir = DOCS / "parte-b"
    parte_a_dir.mkdir(parents=True, exist_ok=True)
    parte_b_dir.mkdir(parents=True, exist_ok=True)
    for stale in list(parte_a_dir.glob("*.md")) + list(parte_b_dir.glob("*.md")):
        stale.unlink()

    nav_a = 1
    nav_b = 1
    for item in MODULES:
        num, slug, title, parte, is_idx = item[:5]
        facilitator_only = item[5] if len(item) > 5 else False
        if is_idx or facilitator_only:
            continue
        fname = f"{num}-{slug}.md"
        target_dir = parte_a_dir if parte == "A" else parte_b_dir
        nav_order = nav_a if parte == "A" else nav_b
        if parte == "A":
            nav_a += 1
        else:
            nav_b += 1

        img_md = ""
        if slug in IMAGE_BY_SLUG:
            fname_img, alt = IMAGE_BY_SLUG[slug]
            img_md = (
                f"\n![{alt}]({{{{ site.baseurl }}}}/assets/images/workshop/{fname_img})\n"
                "{: .mb-4 }\n"
            )

        narrative = (NARRATIVES[slug] if isinstance(NARRATIVES[slug], str) else NARRATIVES[slug]["en"]).strip()
        show_tell = SHOW_TELL_EN[slug].strip()
        todos = TODO_EN[slug]
        todo_lines = (
            "\n".join(todos) if isinstance(todos, list) else todos
        )
        todo_lines = re.sub(
            r"link:([^[]+)\[([^\]]+)\]",
            r"[\2](\1)",
            todo_lines,
        )

        gitops_md = asciidoc_to_md(gitops_section(slug)) if slug in GITOPS_REF else ""
        verify_cmd = GITOPS_REF[slug][1] if slug in GITOPS_REF else "Save progress in Showroom"

        learn_md = ""
        if slug in LEARN_MORE_EN:
            learn_md = "\n### Learn more\n\n" + asciidoc_to_md(
                learn_more_section(slug).strip()
            )
        ext_md = ""
        if slug not in FACILITATOR_ONLY_SLUGS:
            ext_md = "\n## Features, benefits & cloud configuration\n\n" + asciidoc_to_md(
                extended_section(slug).strip()
            )

        body = f"""{SHOWROOM_BANNER}

# {title}

{img_md}
## Overview

{narrative}
{learn_md}
{ext_md}

## Show and Tell

{show_tell}

{gitops_md}

## Your TODO

{todo_lines}

## Verify

Run in the Showroom terminal:

```bash
{verify_cmd.strip()}
```
"""
        (target_dir / fname).write_text(
            md_front_matter(title, nav_order, parent) + body + "\n",
            encoding="utf-8",
        )

    print(f"Generated GitHub Pages workshop mirror -> {DOCS}")


def write_antora_component(title: str) -> None:
    text = f"""name: en
title: {title}
version: ~
nav:
  - modules/ROOT/nav.adoc
"""
    (SHOWROOM / "content/modules/en/antora.yml").write_text(text, encoding="utf-8")


def main() -> None:
    if not SHOWROOM.is_dir():
        SHOWROOM.mkdir(parents=True, exist_ok=True)
    write_antora_component("Hybrid Mesh AI Workshop (English)")

    pages = SHOWROOM / "content/modules/en/modules/ROOT/pages"
    pages.mkdir(parents=True, exist_ok=True)

    nav_en = ["* xref:00-index.adoc[Welcome]\n", "\n.Part A — Strategy\n"]

    for item in MODULES:
        num, slug, title, parte, is_idx = item[:5]
        facilitator_only = item[5] if len(item) > 5 else False
        fname = "00-index.adoc" if is_idx else f"{num}-{slug}.adoc"
        (SHOWROOM / "content/modules/en/modules/ROOT/pages" / fname).write_text(
            adoc_page(num, slug, title, is_idx), encoding="utf-8"
        )
        if facilitator_only:
            continue
        label = title if is_idx else f"{num}. {title}"
        entry = f"* xref:{fname}[{label}]\n"
        if parte == "A" and num != "00":
            nav_en.append(entry)
        elif num == "10":
            nav_en.append("\n.Part B — Hands-on\n")
            nav_en.append(entry)
        elif parte == "B":
            nav_en.append(entry)

    (SHOWROOM / "content/modules/en/modules/ROOT/nav.adoc").write_text(
        "".join(nav_en), encoding="utf-8"
    )

    write_github_pages()
    print(f"Generated {len(MODULES)} modules (EN only) -> {SHOWROOM}")


if __name__ == "__main__":
    main()
