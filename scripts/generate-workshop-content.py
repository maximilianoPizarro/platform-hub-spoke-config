#!/usr/bin/env python3
"""Generate Hybrid Mesh AI Workshop Showroom (.adoc) and GitHub Pages (.md) modules."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from workshop_content_data import (  # noqa: E402
    CRED_NOTE_EN,
    CRED_NOTE_ES,
    ESTIMATED_MIN,
    FACILITATOR_ONLY_SLUGS,
    HYBRID_INTEGRATION_EN,
    HYBRID_INTEGRATION_ES,
    INDEX_INTRO_EN,
    INDEX_INTRO_ES,
    INDEX_HUB_SPOKE_EN,
    INDEX_MESH_FLOW_EN,
    INDEX_AI_MAAS_EN,
    INDEX_KUADRANT_EN,
    INDEX_VERIFY_EN,
    LAB_ACCESS_EN,
    LAB_ACCESS_ES,
    LEARN_MORE_EN,
    LEARN_MORE_ES,
    MODULE_CONTEXT,
    NARRATIVES,
    NEXT_PAGE,
    PREREQUISITES_EN,
    PREREQUISITES_ES,
    PRODUCT_CATALOG_EN,
    PRODUCT_CATALOG_ES,
    PROGRESS_UI_EN,
    PROGRESS_UI_ES,
    REGISTRATION_CTA_EN,
    REGISTRATION_CTA_ES,
    SHOW_TELL_EN,
    SHOW_TELL_ES,
    TODO_EN,
    TODO_ES,
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
    ("00", "index", "Hybrid Mesh AI Workshop", "Taller Hybrid Mesh AI", "A", True),
    ("01", "hybrid-cloud-strategy", "Hybrid Cloud Strategy", "Estrategia nube híbrida", "A", False),
    ("02", "rosa-architecture", "ROSA Architecture & Benefits", "ROSA arquitectura y beneficios", "A", False),
    ("03", "security-scale-hybrid", "Security & Scale in Hybrid", "Seguridad y escala híbrida", "A", False),
    ("04", "aws-ai-integration", "AWS Services & AI Integration", "Integración AWS e IA", "A", False),
    ("05", "cases-roadmap", "Real Cases & Roadmap", "Casos reales y roadmap", "A", False),
    ("10", "acm-multicluster", "Multicluster Fleet & ACM", "Flota multicluster y ACM", "B", False),
    ("11", "hybrid-mesh-architecture", "Hybrid Mesh Architecture", "Arquitectura Hybrid Mesh", "B", False),
    ("12", "software-templates", "Software Templates", "Plantillas software", "B", False),
    ("13", "deploy-industrial-edge", "Deploy Industrial Edge Apps", "Deploy Industrial Edge", "B", False),
    ("14", "kairos-scaling", "Worker Scaling with Kairos", "Escalado con Kairos", "B", False),
    ("15", "observability", "Metrics Logging Dashboards", "Métricas y logging", "B", False),
    ("16", "openshift-gitops", "OpenShift GitOps", "OpenShift GitOps", "B", False),
    ("17", "service-mesh", "OpenShift Service Mesh", "Service Mesh", "B", False),
    ("18", "scalability", "Scalability HPA Kafka", "Escalabilidad", "B", False),
    ("19", "network-policies", "Network Policies", "Network Policies", "B", False),
    ("20", "acs-kuadrant", "ACS & Connectivity Link", "ACS y Kuadrant", "B", False),
    ("21", "finops-kubecost", "FinOps with Kubecost", "FinOps Kubecost", "B", False),
    ("22", "openshift-ai", "OpenShift AI Workshop", "Taller OpenShift AI", "B", False),
    ("23", "ai-gateway", "AI Gateway — MaaS + Kuadrant", "AI Gateway — MaaS + Kuadrant", "B", False),
    ("24", "mcp-gateway", "MCP Gateway + Lightspeed", "MCP Gateway + Lightspeed", "B", False),
    ("25", "llm-rag", "LLMs & RAG", "LLMs y RAG", "B", False),
    ("26", "text-ai-predictive", "Generative & Predictive Text", "Texto gen y predictivo", "B", False),
    ("27", "neuroface", "Face & Object AI + Chat", "NeuroFace", "B", False),
    ("28", "ai-end-user-apps", "AI in End-User Apps", "IA en apps finales", "B", False, False),
    ("29", "full-verification", "Full Stack Verification (facilitator)", "Verificación E2E (facilitador)", "F", False, True),
    ("30", "agent-browser-recording", "Agent Browser (facilitator)", "Agent Browser (facilitador)", "F", False, True),
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
    "llm-rag": ("23-llm-rag.png", "LLM and RAG with MaaS"),
    "neuroface": ("25-neuroface-dashboard.png", "NeuroFace AI dashboard with webcam and chat"),
    "ai-end-user-apps": ("26-ai-end-user-apps.png", "AI in end-user applications"),
    "full-verification": ("27-full-verification.png", "Full stack workshop verification"),
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


def gitops_section(slug: str, lang: str) -> str:
    if slug in FACILITATOR_ONLY_SLUGS or slug not in GITOPS_REF:
        return ""
    table, verify = GITOPS_REF[slug]
    rows = "\n".join(
        "| " + " | ".join(cell.strip() for cell in line.split("|") if cell.strip()) + " |"
        for line in table.strip().split("\n")
        if line.strip()
    )
    title = "Where this lab is defined" if lang == "en" else "Dónde está definido este lab"
    note = (
        "NOTE: Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. "
        "Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`."
        if lang == "en"
        else "NOTE: Las rutas referencian el repo GitOps `platform-hub-spoke-config` desplegado en **este** cluster. "
        "No copies fragmentos como manifiestos independientes — usa los enlaces de consola y verifica con `oc`."
    )
    verify_label = "Verify in the Showroom terminal" if lang == "en" else "Verificar en la terminal Showroom"
    return f"""
== {title}

{note}

[cols="2,3"]
|===
| UI / capability | Source in GitOps repo

{rows}
|===

{verify_label}:

[source,bash]
----
{verify.strip()}
----
"""


def module_context_section(slug: str, lang: str) -> str:
    if slug not in MODULE_CONTEXT:
        return ""
    label = "What you will do" if lang == "en" else "Qué harás"
    banner = ""
    if slug in FACILITATOR_ONLY_SLUGS:
        banner = (
            "IMPORTANT: **Facilitator / automation agent only** — this page is not part of the learner navigation.\n\n"
            if lang == "en"
            else "IMPORTANT: **Solo facilitador / agente de automatización** — esta página no forma parte de la navegación del participante.\n\n"
        )
    return f"""
== {label}

{banner}{MODULE_CONTEXT[slug][lang].strip()}
"""


def callout_ref(lang: str) -> str:
    if lang == "en":
        return "\nNOTE: For AWS/Azure integration snippets see xref:00-index.adoc#hybrid-integration[Module 00 — hybrid integration notes].\n"
    return "\nNOTE: Para snippets AWS/Azure ver xref:00-index.adoc#hybrid-integration[Módulo 00 — integración híbrida].\n"


def lab_access_section(slug: str, lang: str) -> str:
    access_map = LAB_ACCESS_EN if lang == "en" else LAB_ACCESS_ES
    if slug not in access_map:
        return ""
    title = (
        "Lab access — URLs & credentials"
        if lang == "en"
        else "Acceso al producto — URLs y credenciales"
    )
    note = ""
    if slug != "index":
        note = (CRED_NOTE_EN if lang == "en" else CRED_NOTE_ES).strip() + "\n\n"
    body = clickable_lab_access(access_map[slug].strip())
    return f"\n== {title}\n\n{note}{body}\n"


def next_nav(slug: str, lang: str) -> str:
    nxt = NEXT_PAGE.get(slug)
    if not nxt:
        return ""
    label = "Next →" if lang == "en" else "Siguiente →"
    stem = nxt.replace(".adoc", ".html")
    return f"""
++++
<div class="workshop-next-nav">
  <a href="{stem}">{label} {nxt.replace('.adoc', '').replace('-', ' ')}</a>
</div>
++++
"""


def time_badge(minutes: int, lang: str) -> str:
    label = f"~{minutes} min"
    return f"""
++++
<span class="workshop-time-badge">{label}</span>
++++
"""


def learn_more_section(slug: str, lang: str) -> str:
    """Red Hat external docs — deep links after Overview."""
    if slug in FACILITATOR_ONLY_SLUGS:
        return ""
    learn_map = LEARN_MORE_EN if lang == "en" else LEARN_MORE_ES
    body = learn_map.get(slug, "")
    if not body and lang != "en":
        body = LEARN_MORE_EN.get(slug, "")
    if not body:
        return ""
    label = "Learn more" if lang == "en" else "Profundizar"
    return f"""
=== {label}

{body.strip()}
"""


def track_pacing_section(lang: str) -> str:
    if lang == "en":
        return """
NOTE: **Workshop pacing (~4 hours hands-on)** — Each module includes **Overview-only** steps (demo/visualization, ~5–10 min) and **Hands-on** steps (full lab). Skip Hands-on blocks to run a ~90-minute executive tour.

"""
    return """
NOTE: **Ritmo del taller (~4 h hands-on)** — Cada módulo incluye pasos **Solo visualización** (~5–10 min) y **Hands-on** (lab completo). Omite Hands-on para un tour ejecutivo ~90 min.

"""


def adoc_page(num: str, slug: str, title: str, lang: str, is_index: bool) -> str:
    mid = "00-index" if is_index else f"{num}-{slug}"
    minutes = ESTIMATED_MIN.get(slug, 15)
    time_label = time_badge(minutes, lang)
    narrative = NARRATIVES[slug][lang]
    show_tell = SHOW_TELL_EN[slug] if lang == "en" else SHOW_TELL_ES[slug]
    todos_raw = TODO_EN[slug] if lang == "en" else TODO_ES[slug]
    todos = "\n".join(todos_raw) if isinstance(todos_raw, list) else todos_raw
    progress = (PROGRESS_UI_EN if lang == "en" else PROGRESS_UI_ES).format(module_id=mid)
    live = ""
    if not is_index and num.isdigit() and int(num) >= 10:
        live = "\n== Live lab\n\n* Showroom integrated `oc` terminal — use hub context unless module says east/west.\n" if lang == "en" else "\n== Lab en vivo\n\n* Terminal `oc` integrada en Showroom — usa contexto hub salvo que el módulo indique east/west.\n"

    img = ""
    if slug in IMAGE_BY_SLUG:
        fname, alt = IMAGE_BY_SLUG[slug]
        img = f"\nimage::{fname}[{alt},960]\n"

    index_block = ""
    if is_index:
        intro = INDEX_INTRO_EN if lang == "en" else INDEX_INTRO_ES
        reg_cta = REGISTRATION_CTA_EN if lang == "en" else REGISTRATION_CTA_ES
        catalog = PRODUCT_CATALOG_EN if lang == "en" else PRODUCT_CATALOG_ES
        prereq = PREREQUISITES_EN if lang == "en" else PREREQUISITES_ES
        integration = HYBRID_INTEGRATION_EN if lang == "en" else HYBRID_INTEGRATION_ES
        welcome = "Welcome" if lang == "en" else "Bienvenida"
        lab_access = lab_access_section(slug, lang)
        agenda_en = """
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
        agenda_es = """
== Agenda dual

.Parte A — Ejecutiva (01–05)
[cols="1,3"]
|===
| 01 | Estrategia nube híbrida
| 02 | Arquitectura y beneficios ROSA
| 03 | Seguridad y escala híbrida
| 04 | Integración AWS e IA
| 05 | Casos reales y roadmap
|===

.Parte B — Hands-on (10–28, ~4 h)
[cols="1,3"]
|===
| 10–14 | Foundation — ACM, mesh, plantillas, IE, Kairos
| 15–18 | Operaciones — observabilidad, GitOps, mesh, escala
| 19–21 | Seguridad y FinOps — NP, ACS/Kuadrant, Kubecost
| 22–24 | OpenShift AI — proyectos, AI Gateway, MCP Gateway
| 25–28 | LLM, NeuroFace (OVMS), apps finales
|===

NOTE: Los módulos 29–30 (verificación y Agent Browser) son **tareas de facilitador/agente**. Cada módulo Parte B admite **Solo visualización** (~90 min) o **Hands-on** (~4 h).

== Registro y demos Plan B

* Registro: link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[registro taller] → redirect con `USER_NAME=%USER_NAME%`
* Consola OpenShift: **Hybrid Mesh AI Workshop** (ApplicationMenu)
* Developer Hub → System `hybrid-mesh-shared-demos` (Plan B sin scaffolder)
* NeuroFace: link:https://neuroface.%HUB_DOMAIN%[NeuroFace]
* Kuadrant: link:https://developer-hub.%HUB_DOMAIN%/kuadrant[Kuadrant UI] + link:https://workshop-apis.%HUB_DOMAIN%[Workshop APIs]
"""
        agenda = agenda_en if lang == "en" else agenda_es
        index_parts = [
            f"== {welcome}",
            intro.strip(),
            reg_cta.strip(),
        ]
        if lang == "en":
            index_parts.extend(
                [
                    INDEX_HUB_SPOKE_EN.strip(),
                    INDEX_MESH_FLOW_EN.strip(),
                    INDEX_AI_MAAS_EN.strip(),
                    INDEX_KUADRANT_EN.strip(),
                ]
            )
        index_parts.extend(
            [
                lab_access.strip(),
                catalog.strip(),
                prereq.strip(),
                agenda.strip(),
                integration.strip(),
            ]
        )
        index_block = "\n\n".join(index_parts)
    else:
        index_block = callout_ref(lang)

    overview = "Overview" if lang == "en" else "Panorama"
    show_label = "Show and Tell" if lang == "en" else "Demostración"
    todo_label = (
        "Your TODO (user %USER_NAME%)" if lang == "en" else "Tu TODO (usuario %USER_NAME%)"
    )
    verify_label = "Verify" if lang == "en" else "Verificar"
    tip = (
        "TIP: Plan B — shared demo in Developer Hub → System `hybrid-mesh-shared-demos` if scaffolder fails."
        if lang == "en"
        else "TIP: Plan B — demo compartido en Developer Hub → System `hybrid-mesh-shared-demos` si falla el scaffolder."
    )

    overview_section = ""
    if not is_index and slug not in FACILITATOR_ONLY_SLUGS:
        overview_section = f"""
== {overview}

{track_pacing_section(lang) if (not is_index and num.isdigit() and int(num) >= 10) else ""}{narrative.strip()}
{learn_more_section(slug, lang)}
"""
    elif slug in FACILITATOR_ONLY_SLUGS:
        overview_section = module_context_section(slug, lang)

    context_section = ""
    if not is_index and slug not in FACILITATOR_ONLY_SLUGS and slug in MODULE_CONTEXT:
        context_section = module_context_section(slug, lang)

    body_lab_access = "" if is_index or slug in FACILITATOR_ONLY_SLUGS else lab_access_section(slug, lang)

    show_block = ""
    todo_block = ""
    verify_block = ""
    if slug not in FACILITATOR_ONLY_SLUGS:
        show_block = f"""
== {show_label}

{show_tell.strip()}
"""
        todo_block = f"""
== {todo_label}

{todos.strip()}
"""
        if is_index and lang == "en":
            verify_body = INDEX_VERIFY_EN.strip()
        else:
            verify_body = """[cols="1,2,1"]
|===
| Check | Action | Expected

| Progress | Save checkboxes below | `POST /api/progress` returns OK
|==="""
        verify_block = f"""
== {verify_label}

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
{live}{gitops_section(slug, lang)}
{verify_block.strip()}

{progress if slug not in FACILITATOR_ONLY_SLUGS else ""}

{tip if slug not in FACILITATOR_ONLY_SLUGS else ""}

{next_nav(slug, lang)}
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
        if line.startswith("=== "):
            out.append(f"### {line[4:].strip()}")
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
        num, slug, en_title, _es_title, parte, is_idx = item[:6]
        facilitator_only = item[6] if len(item) > 6 else False
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

        narrative = NARRATIVES[slug]["en"].strip()
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

        gitops_md = asciidoc_to_md(gitops_section(slug, "en")) if slug in GITOPS_REF else ""
        verify_cmd = GITOPS_REF[slug][1] if slug in GITOPS_REF else "Save progress in Showroom"

        learn_md = ""
        if slug in LEARN_MORE_EN:
            learn_md = "\n### Learn more\n\n" + asciidoc_to_md(
                learn_more_section(slug, "en").strip()
            )

        body = f"""{SHOWROOM_BANNER}

# {en_title}

{img_md}
## Overview

{narrative}
{learn_md}

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
            md_front_matter(en_title, nav_order, parent) + body + "\n",
            encoding="utf-8",
        )

    print(f"Generated GitHub Pages workshop mirror -> {DOCS}")


def write_antora_component(lang: str, title: str) -> None:
    text = f"""name: {lang}
title: {title}
version: ~
nav:
  - modules/ROOT/nav.adoc
"""
    text = text.format(lang=lang, title=title)
    (SHOWROOM / "content/modules" / lang / "antora.yml").write_text(text, encoding="utf-8")


def main() -> None:
    if not SHOWROOM.is_dir():
        SHOWROOM.mkdir(parents=True, exist_ok=True)
    write_antora_component("en", "Hybrid Mesh AI Workshop (English)")
    write_antora_component("es", "Hybrid Mesh AI Workshop (Español)")
    for lang in ("en", "es"):
        pages = SHOWROOM / "content/modules" / lang / "modules" / "ROOT" / "pages"
        pages.mkdir(parents=True, exist_ok=True)

    nav_en = ["* xref:00-index.adoc[Welcome]\n", "\n.Part A — Strategy\n"]
    nav_es = ["* xref:00-index.adoc[Bienvenida]\n", "\n.Parte A — Estrategia\n"]

    for item in MODULES:
        num, slug, en_title, es_title, parte, is_idx = item[:6]
        facilitator_only = item[6] if len(item) > 6 else False
        fname = "00-index.adoc" if is_idx else f"{num}-{slug}.adoc"
        (SHOWROOM / "content/modules/en/modules/ROOT/pages" / fname).write_text(
            adoc_page(num, slug, en_title, "en", is_idx), encoding="utf-8"
        )
        (SHOWROOM / "content/modules/es/modules/ROOT/pages" / fname).write_text(
            adoc_page(num, slug, es_title, "es", is_idx), encoding="utf-8"
        )
        if facilitator_only:
            continue
        label_en = en_title if is_idx else f"{num}. {en_title}"
        label_es = es_title if is_idx else f"{num}. {es_title}"
        entry_en = f"* xref:{fname}[{label_en}]\n"
        entry_es = f"* xref:{fname}[{label_es}]\n"
        if parte == "A" and num != "00":
            nav_en.append(entry_en)
            nav_es.append(entry_es)
        elif num == "10":
            nav_en.append("\n.Part B — Hands-on\n")
            nav_es.append("\n.Parte B — Hands-on\n")
            nav_en.append(entry_en)
            nav_es.append(entry_es)
        elif parte == "B":
            nav_en.append(entry_en)
            nav_es.append(entry_es)

    for lang, nav in (("en", nav_en), ("es", nav_es)):
        (SHOWROOM / "content/modules" / lang / "modules" / "ROOT" / "nav.adoc").write_text(
            "".join(nav), encoding="utf-8"
        )

    en_img = SHOWROOM / "content/modules/en/modules/ROOT/images"
    es_img = SHOWROOM / "content/modules/es/modules/ROOT/images"
    es_img.mkdir(parents=True, exist_ok=True)
    if en_img.is_dir():
        import shutil

        for png in en_img.glob("*.png"):
            shutil.copy2(png, es_img / png.name)

    write_github_pages()
    print(f"Generated {len(MODULES)} modules x 2 langs -> {SHOWROOM}")


if __name__ == "__main__":
    main()
