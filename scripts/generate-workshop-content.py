#!/usr/bin/env python3
"""Generate Hybrid Mesh AI Workshop Showroom (.adoc) and GitHub Pages (.md) modules."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from workshop_content_data import (  # noqa: E402
    CRED_NOTE_EN,
    CRED_NOTE_ES,
    ESTIMATED_MIN,
    HYBRID_INTEGRATION_EN,
    HYBRID_INTEGRATION_ES,
    INDEX_INTRO_EN,
    INDEX_INTRO_ES,
    LAB_ACCESS_EN,
    LAB_ACCESS_ES,
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

# slug → (ui_table adoc rows, yaml excerpt, verify command)
YAML_BEHIND: dict[str, tuple[str, str, str]] = {
    "hybrid-cloud-strategy": (
        "| Executive narrative | docs/workshop/parte-a/ | Narrative |\n| Fleet ACM | components/acm-hub-spoke/ | ManagedCluster |",
        "# Executive track — reference ROSA docs\n# https://docs.redhat.com/en/documentation/rosa/",
        "oc get managedclusters 2>/dev/null | head -5",
    ),
    "rosa-architecture": (
        "| ROSA control plane | docs.redhat.com ROSA | Managed service |\n| Lab hub-spoke | components/acm-hub-spoke/templates/managed-clusters.yaml | ManagedCluster |\n| West spoke | same chart | ManagedCluster west |",
        """apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: east
  labels:
    region: east
spec:
  hubAcceptsClient: true
---
apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: west
  labels:
    region: west
spec:
  hubAcceptsClient: true""",
        "oc get managedclusters",
    ),
    "security-scale-hybrid": (
        "| ACS Central | components/acs-operator/ | Central |\n| Mesh ambient | components/servicemeshoperator3/ | Subscription |",
        """# stackrox namespace must NOT use istio ambient label
metadata:
  name: stackrox""",
        "oc get central -n stackrox",
    ),
    "aws-ai-integration": (
        "| Bedrock/SageMaker (narrative) | AWS docs | External |\n| MaaS lab | components/openshift-ai-hub/ | DataScienceCluster |",
        """stringData:
  OPENAI_API_BASE: "https://maas-rhdp.apps.maas.redhatworkshops.io/v1"
# Secret openshift-ai-maas-credentials in maas-workshop""",
        "oc get dsc -A",
    ),
    "cases-roadmap": (
        "| Industrial Edge | components/industrial-edge-tst/ | Deployments |\n| Showroom | components/showroom/ | Deployment |\n| Registration | components/workshop-registration/ | Deployment |",
        "# Transition to Parte B after registration",
        "curl -sk -o /dev/null -w '%{http_code}' https://workshop-registration.{hub_domain}/api/health",
    ),
    "acm-multicluster": (
        "| ACM Clusters UI | components/acm-hub-spoke/ | ManagedCluster |\n| GitOpsCluster | components/acm-hub-spoke/templates/gitops-cluster.yaml | GitOpsCluster |",
        """apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: east
spec:
  hubAcceptsClient: true""",
        "oc get managedclusters && oc get gitopscluster -A",
    ),
    "hybrid-mesh-architecture": (
        "| Hub gateway | components/hub-gateway/templates/httproute.yaml | HTTPRoute |\n| Skupper | components/service-interconnect/ | Site/Connector |",
        """apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: industrial-edge-lb
# hub ingress → spoke gateways via Skupper""",
        "oc get httproute -n hub-gateway-system",
    ),
    "software-templates": (
        "| Developer Hub Create | docs/assets/backstage/software-templates/ | SoftwareTemplate |\n| Plan B catalog | components/workshop-demos/files/catalog/ | System |",
        """metadata:
  name: hybrid-mesh-shared-demos
  title: Hybrid Mesh AI — Shared Demos (Plan B)""",
        "oc get configmap developer-hub-catalog-demos -n developer-hub 2>/dev/null || oc get application -n openshift-gitops | grep workshop",
    ),
    "deploy-industrial-edge": (
        "| Scaffold IE | software-templates/industrial-edge/template.yaml | SoftwareTemplate |\n| Spoke deploy | east/templates/component-applications.yaml | Application |",
        """spec:
  destination:
    namespace: industrial-edge-tst-all""",
        "oc get applications -n openshift-gitops | grep -E 'industrial|east-spoke'",
    ),
    "kairos-scaling": (
        "| Kairos Console | components/kairos/templates/console-rbac.yaml | ClusterRole |\n| SmartScalingPolicy | components/kairos/templates/sensor-scan-policies.yaml | SmartScalingPolicy |",
        """apiVersion: kairos.io/v1alpha1
kind: SmartScalingPolicy
metadata:
  name: scan-policy-machine-sensor""",
        "oc get smartscalingpolicy -A",
    ),
    "observability": (
        "| Grafana dashboards | components/grafana-dashboards/ | ConfigMap |\n| OTEL | components/opentelemetry/ | Instrumentation |\n| Kafka Console | components/kafka-console/ | Deployment |",
        "# Open Grafana from ConsoleLink; filter by cluster label",
        "oc get grafanadashboard -A 2>/dev/null | head -5; oc get route -n openshift-cluster-observability-operator 2>/dev/null | head -3",
    ),
    "openshift-gitops": (
        "| ApplicationSet | components/acm-hub-spoke/templates/applicationset.yaml | ApplicationSet |\n| Hub apps | templates/component-applications.yaml | Application |",
        """apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: industrial-edge-spoke""",
        "oc get applicationset -n openshift-gitops",
    ),
    "service-mesh": (
        "| OSSM3 | components/servicemeshoperator3/ | Subscription |\n| Kiali | components/kiali/ | Kiali CR |",
        """metadata:
  labels:
    istio.io/dataplane-mode: ambient""",
        "oc get istio -n istio-system; oc get kiali -A",
    ),
    "scalability": (
        "| Kafka | components/industrial-edge-tst/ | KafkaNodePool |\n| HPA | industrial-edge manifests | HorizontalPodAutoscaler |",
        """apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: line-dashboard""",
        "oc get hpa -n industrial-edge-tst-all",
    ),
    "network-policies": (
        "| NP demo | components/workshop-demos/templates/network-policy-demo.yaml | NetworkPolicy |\n| OVN CNI | OpenShift networking | Cluster default |",
        """apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ie-workshop-allow-dashboard
  namespace: industrial-edge-tst-all""",
        "oc get networkpolicy -n industrial-edge-tst-all",
    ),
    "acs-kuadrant": (
        "| ACS init | components/acs-init-bundle-sync/ | Job |\n| External APIs | components/workshop-kuadrant-apis/templates/external-backends.yaml | ServiceEntry |\n| Kuadrant policies | components/workshop-kuadrant-apis/templates/policies.yaml | TokenRateLimitPolicy |\n| Hub gateway | components/hub-gateway/ | HTTPRoute |",
        """# External public APIs — no in-cluster Docker images
# ServiceEntry + DestinationRule + HTTPRoute (Hostname backendRef)
# curl -H 'Authorization: APIKEY $KEY' https://workshop-apis.{hub_domain}/httpbin/get""",
        "oc get serviceentry,httproute -n hub-gateway-system | grep workshop",
    ),
    "finops-kubecost": (
        "| Kubecost | components/kubecost/ | CostAnalyzer |\n| MinIO ETL | components/industrial-edge-minio/ | Bucket |",
        "# Free tier: single-cluster Kubecost on hub",
        "oc get deploy -n kubecost kubecost-cost-analyzer",
    ),
    "openshift-ai": (
        "| DSC | components/openshift-ai-hub/ | DataScienceCluster |\n| MaaS | maas-workshop namespace | Secret |",
        """apiVersion: datasciencecluster.opendatahub.io/v1
kind: DataScienceCluster
metadata:
  name: default-dsc""",
        "oc get dsc; oc get ns maas-workshop demo-ods-workspace 2>/dev/null",
    ),
    "llm-rag": (
        "| Lightspeed | components/developer-hub/ | Plugin |\n| MaaS | openshift-ai-hub | Credentials |",
        """# Developer Hub → Lightspeed uses MaaS llama-scout-17b""",
        "oc get deploy -n developer-hub 2>/dev/null | grep -i lightspeed || echo 'Lightspeed via RHDH plugin'",
    ),
    "text-ai-predictive": (
        "| Anomaly alerter | components/ie-anomaly-alerter/ | Deployment |\n| Kafka metrics | industrial-edge-tst-all | Topic |",
        "# ie-anomaly-alerter correlates sensor anomalies",
        "oc get deploy -n industrial-edge-tst-all | grep -i anomaly",
    ),
    "neuroface": (
        "| NeuroFace | components/neuroface/ | Helm chart |\n| MaaS chat | neuroface.chat | Config |",
        """chat:
  enabled: true
  modelEndpoint: "https://maas-rhdp.apps.maas.redhatworkshops.io/v1"
litellm:
  enabled: false""",
        "curl -sk -o /dev/null -w '%{http_code}' https://neuroface.{hub_domain}/api/health",
    ),
    "ai-end-user-apps": (
        "| line-dashboard | industrial-edge-tst-all | Deployment |\n| Camel K | industrial-edge-pipelines | Integration |",
        "# End-user apps on spoke consume IE + AI stack",
        "oc get deploy -n industrial-edge-tst-all line-dashboard",
    ),
    "full-verification": (
        "| Progress API | workshop-registration | POST /api/progress |\n| E2E script | scripts/verify-workshop-e2e.sh | Shell |\n| Checklist | verification/progress-checklist.yaml | YAML |",
        """# Checks: registration, showroom, ACM clusters, IE deploy, NeuroFace route""",
        "bash scripts/verify-workshop-e2e.sh 2>/dev/null || oc get managedclusters",
    ),
    "agent-browser-recording": (
        "| Agent Browser | verification/agent-browser/*.yaml | YAML flows |\n| Runbook | verification/recording-runbook.md | Doc |",
        """# Recordings stay local — *.mp4 gitignored
# Naming: YYYY-MM-DD-userN-module-slug.mp4""",
        "test -f verification/recording-runbook.md && test -d verification/agent-browser",
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
    ("23", "llm-rag", "LLMs & RAG", "LLMs y RAG", "B", False),
    ("24", "text-ai-predictive", "Generative & Predictive Text", "Texto gen y predictivo", "B", False),
    ("25", "neuroface", "Face & Object AI + Chat", "NeuroFace", "B", False),
    ("26", "ai-end-user-apps", "AI in End-User Apps", "IA en apps finales", "B", False),
    ("27", "full-verification", "Full Stack Verification", "Verificación completa", "B", False),
    ("28", "agent-browser-recording", "Agent Browser & Recording", "Agent Browser y grabación", "B", False),
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
    "openshift-gitops": ("16-openshift-gitops.png", "OpenShift GitOps and Argo CD"),
    "service-mesh": ("17-service-mesh.png", "OpenShift Service Mesh ambient"),
    "acs-kuadrant": ("20-acs-kuadrant.png", "ACS and Kuadrant API security"),
    "openshift-ai": ("22-openshift-ai.png", "OpenShift AI DataScienceCluster"),
    "llm-rag": ("23-llm-rag.png", "LLM and RAG with MaaS"),
    "neuroface": ("25-neuroface-dashboard.png", "NeuroFace AI dashboard with webcam and chat"),
    "ai-end-user-apps": ("26-ai-end-user-apps.png", "AI in end-user applications"),
    "full-verification": ("27-full-verification.png", "Full stack workshop verification"),
}


def yaml_section(slug: str) -> str:
    if slug not in YAML_BEHIND:
        return ""
    table, yaml_block, verify = YAML_BEHIND[slug]
    rows = "\n".join(
        "| " + " | ".join(cell.strip() for cell in line.split("|") if cell.strip()) + " |"
        for line in table.strip().split("\n")
        if line.strip()
    )
    return f"""
== YAML behind the scenes

[cols="2,3,1"]
|===
| UI action | Git source | Kind

{rows}
|===

[source,yaml]
----
{yaml_block.strip()}
----

Verify:

[source,bash]
----
{verify}
----
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
    return f"\n== {title}\n\n{note}{access_map[slug].strip()}\n"


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
        img = f"\nimage::images/{fname}[{alt},600]\n"

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

.Part B — Hands-on (10–28)
[cols="1,3"]
|===
| 10–14 | Foundation — ACM, mesh, templates, IE, Kairos
| 15–18 | Operations — observability, GitOps, mesh, scale
| 19–21 | Security & FinOps — NP, ACS/Kuadrant, Kubecost
| 22–26 | Hybrid Mesh AI — ODS, LLM, NeuroFace
| 27–28 | Verification & recording runbook
|===

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

.Parte B — Hands-on (10–28)
[cols="1,3"]
|===
| 10–14 | Foundation — ACM, mesh, templates, IE, Kairos
| 15–18 | Operations — observabilidad, GitOps, mesh, escala
| 19–21 | Security & FinOps — NP, ACS/Kuadrant, Kubecost
| 22–26 | Hybrid Mesh AI — ODS, LLM, NeuroFace
| 27–28 | Verificación y runbook de grabación
|===

== Registro y demos Plan B

* Registro: link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[registro taller] → redirect con `USER_NAME=%USER_NAME%`
* Consola OpenShift: **Hybrid Mesh AI Workshop** (ApplicationMenu)
* Developer Hub → System `hybrid-mesh-shared-demos` (Plan B sin scaffolder)
* NeuroFace: link:https://neuroface.%HUB_DOMAIN%[NeuroFace]
* Kuadrant: link:https://developer-hub.%HUB_DOMAIN%/kuadrant[Kuadrant UI] + link:https://workshop-apis.%HUB_DOMAIN%[Workshop APIs]
"""
        agenda = agenda_en if lang == "en" else agenda_es
        index_block = "\n\n".join(
            [
                f"== {welcome}",
                intro.strip(),
                reg_cta.strip(),
                lab_access.strip(),
                catalog.strip(),
                prereq.strip(),
                agenda.strip(),
                integration.strip(),
            ]
        )
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
    if not is_index:
        overview_section = f"""
== {overview}

{narrative.strip()}
"""

    body_lab_access = "" if is_index else lab_access_section(slug, lang)

    return f"""= {title}

{time_label.strip()}
{img}
{index_block.strip()}
{overview_section.strip()}
{body_lab_access}
== {show_label}

{show_tell.strip()}

== {todo_label}

{todos.strip()}
{live}{yaml_section(slug)}
== {verify_label}

[cols="1,2,1"]
|===
| Check | Action | Expected

| Progress | Save checkboxes below | `POST /api/progress` returns OK
|===

{progress}

{tip}

{next_nav(slug, lang)}
"""


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

    for num, slug, en_title, es_title, parte, is_idx in MODULES:
        fname = "00-index.adoc" if is_idx else f"{num}-{slug}.adoc"
        (SHOWROOM / "content/modules/en/modules/ROOT/pages" / fname).write_text(
            adoc_page(num, slug, en_title, "en", is_idx), encoding="utf-8"
        )
        (SHOWROOM / "content/modules/es/modules/ROOT/pages" / fname).write_text(
            adoc_page(num, slug, es_title, "es", is_idx), encoding="utf-8"
        )
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

    print(f"Generated {len(MODULES)} modules x 2 langs -> {SHOWROOM}")


if __name__ == "__main__":
    main()
