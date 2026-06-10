#!/usr/bin/env python3
"""Generate Hybrid Mesh AI Workshop Showroom (.adoc) and GitHub Pages (.md) modules."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOWROOM = ROOT / "showroom-hybrid-mesh-ai"
DOCS = ROOT / "docs" / "workshop"

HYBRID_CALLOUT_ADOC = """
== Nube híbrida — ROSA/AWS vs este lab

[cols="1,1"]
|===
| En producción (ROSA + AWS) | En este lab (RHDP hub-spoke)

| Clúster ROSA gestionado en cuenta AWS (Multi-AZ) | Hub pre-provisionado; spokes east/west vía ACM
| ROSA MachineSets / autoscaling workers | Kairos SmartScalingPolicy + HPA + Kafka
| Security Groups + IAM + NP en VPC | OVN NetworkPolicy + ACS + Kuadrant
| Amazon Bedrock / SageMaker | OpenShift AI + MaaS + NeuroFace + Lightspeed
| AWS Cost Explorer + tags | Kubecost federated ETL
| Route 53 + ALB | Hub Gateway + Skupper + Connectivity Link
|===
"""

HYBRID_CALLOUT_MD = """
## Nube híbrida — ROSA/AWS vs este lab

| En producción (ROSA + AWS) | En este lab (RHDP hub-spoke) |
|----------------------------|------------------------------|
| Clúster ROSA en AWS (Multi-AZ) | Hub + spokes east/west importados vía ACM |
| ROSA MachineSets / autoscaling | Kairos + HPA + Kafka |
| Security Groups + IAM + NP | OVN NetworkPolicy + ACS + Kuadrant |
| Bedrock / SageMaker | OpenShift AI + MaaS + NeuroFace |
| AWS Cost Explorer | Kubecost federated ETL |
| Route 53 + ALB | Hub Gateway + Skupper |
"""

PROGRESS_HTML = """
++++
<div class="workshop-progress" data-module="{module_id}">
  <label><input type="checkbox" data-completed> Completé este módulo</label>
  <label><input type="checkbox" data-interest> Me interesa profundizar</label>
  <button type="button" onclick="saveWorkshopProgress('{module_id}')">Guardar progreso</button>
</div>
++++
"""

INDEX_AGENDA_ADOC = """
== Agenda dual

.Parte A — Ejecutiva (01–05)
[cols="1,3"]
|===
| 01 | Hybrid Cloud Strategy
| 02 | ROSA Architecture & Benefits
| 03 | Security & Scale in Hybrid
| 04 | AWS Services & AI Integration
| 05 | Real Cases & Roadmap
|===

.Parte B — Hands-on (10–28)
[cols="1,3"]
|===
| 10–14 | Foundation — ACM, mesh, templates, IE, Kairos
| 15–18 | Operations — observability, GitOps, mesh, scale
| 19–21 | Security & FinOps — NP, ACS/Kuadrant, Kubecost
| 22–26 | Hybrid Mesh AI — ODS, LLM, NeuroFace
| 27–28 | Verification & recording runbook
|===

== Registro y demos Plan B

* Registro: `https://workshop-registration.{hub_domain}` → redirect Showroom con `USER_NAME=userN`
* Console OpenShift: **Hybrid Mesh AI Workshop** (ApplicationMenu)
* Developer Hub → System `hybrid-mesh-shared-demos` (Plan B sin scaffolder)
* NeuroFace: `https://neuroface.{hub_domain}` (no LibreChat)
"""

# slug → (ui_table adoc rows, yaml excerpt, verify command)
YAML_BEHIND: dict[str, tuple[str, str, str]] = {
    "hybrid-cloud-strategy": (
        "| Estrategia ejecutiva | docs/workshop/parte-a/ | Narrative |\n| Fleet ACM | components/acm-hub-spoke/ | ManagedCluster |",
        "# Executive track — no CR required on cluster for Parte A\n# Reference: https://docs.redhat.com/en/documentation/rosa/",
        "oc get managedclusters 2>/dev/null | head -5",
    ),
    "rosa-architecture": (
        "| ROSA control plane AWS | docs.redhat.com ROSA | Managed service |\n| Lab hub-spoke | components/acm-hub-spoke/templates/managed-clusters.yaml | ManagedCluster |",
        """apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: east
  labels:
    region: east
    vendor: OpenShift
spec:
  hubAcceptsClient: true""",
        "oc get managedclusters",
    ),
    "security-scale-hybrid": (
        "| ACS Central | components/acs-operator/ | Central |\n| Mesh ambient | components/operators/templates/servicemeshoperator3.yaml | Subscription |",
        """# stackrox namespace must NOT use istio ambient
metadata:
  name: stackrox
  labels:
    # no istio.io/dataplane-mode: ambient""",
        "oc get central -n stackrox",
    ),
    "aws-ai-integration": (
        "| Bedrock/SageMaker (narrativa) | AWS docs | External |\n| MaaS lab | components/openshift-ai-hub/ | DataScienceCluster |",
        """stringData:
  OPENAI_API_BASE: "https://maas-rhdp.apps.maas.redhatworkshops.io/v1"
# Secret openshift-ai-maas-credentials in maas-workshop""",
        "oc get dsc -A",
    ),
    "cases-roadmap": (
        "| Industrial Edge | components/industrial-edge-tst/ | Kafka + dashboard |\n| Workshop | components/showroom/ | Showroom |",
        "# Transition to Parte B — register at workshop-registration",
        "curl -sk -o /dev/null -w '%{http_code}' https://workshop-registration.${HUB_DOMAIN}/api/health",
    ),
    "acm-multicluster": (
        "| ACM Clusters UI | components/acm-hub-spoke/templates/managed-clusters.yaml | ManagedCluster |\n| GitOpsCluster | components/acm-hub-spoke/templates/gitops-cluster.yaml | GitOpsCluster |",
        """apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: east
spec:
  hubAcceptsClient: true""",
        "oc get managedclusters",
    ),
    "hybrid-mesh-architecture": (
        "| Hub gateway | components/hub-gateway/templates/httproute.yaml | HTTPRoute |\n| Skupper | components/service-interconnect/ | Site/Connector |",
        """apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: industrial-edge-front
# routes hub ingress to spoke gateways via Skupper""",
        "oc get httproute -A | head",
    ),
    "software-templates": (
        "| Developer Hub Create | docs/assets/backstage/software-templates/ | SoftwareTemplate |\n| Plan B catalog | components/workshop-demos/files/catalog/ | System |",
        """metadata:
  name: hybrid-mesh-shared-demos
  title: Hybrid Mesh AI — Shared Demos (Plan B)""",
        "oc get configmap developer-hub-catalog-demos -n developer-hub",
    ),
    "deploy-industrial-edge": (
        "| Scaffold IE | software-templates/industrial-edge/template.yaml | SoftwareTemplate |\n| Spoke deploy | east/templates/component-applications.yaml | Application |",
        """# Argo CD Application on spoke after scaffold
spec:
  destination:
    namespace: industrial-edge-tst-all""",
        "oc get applications -n openshift-gitops | grep industrial",
    ),
    "kairos-scaling": (
        "| Kairos Console | components/kairos/templates/console-rbac.yaml | ClusterRole |\n| Sensor scan SSP | components/kairos/templates/sensor-scan-policies.yaml | SmartScalingPolicy |",
        """apiVersion: kairos.io/v1alpha1
kind: SmartScalingPolicy
metadata:
  name: scan-policy-machine-sensor
# approve scaling in Kairos Console""",
        "oc get smartscalingpolicy -A",
    ),
    "observability": (
        "| Grafana | components/grafana-dashboards/ | ConfigMap |\n| OTEL | components/opentelemetry/ | Instrumentation |",
        """# Grafana multicluster dashboards on hub
# Kafka Console: components/kafka-console/""",
        "oc get grafanadashboard -A | head",
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
        "| OSSM3 | components/operators/templates/servicemeshoperator3.yaml | Subscription |\n| Kiali | components/kiali/ | Kiali CR |",
        """spec:
  values:
    meshConfig:
      defaultConfig:
        tracing: {}""",
        "oc get servicemeshcontrolplane -n istio-system",
    ),
    "scalability": (
        "| Kafka | components/industrial-edge-tst/templates/kafka-cluster.yaml | Kafka |\n| HPA | workload manifests | HorizontalPodAutoscaler |",
        """apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: line-dashboard""",
        "oc get hpa -n industrial-edge-tst-all",
    ),
    "network-policies": (
        "| NP demo IE | components/workshop-demos/templates/network-policy-demo.yaml | NetworkPolicy |\n| OVN | OpenShift SDN/OVN | CNI |",
        """apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ie-workshop-allow-dashboard
  namespace: industrial-edge-tst-all""",
        "oc get networkpolicy -n industrial-edge-tst-all",
    ),
    "acs-kuadrant": (
        "| ACS init bundles | components/acs-init-bundle-sync/ | Job |\n| Kuadrant | components/hub-gateway/ | AuthPolicy |",
        """# Secret acs-init-credentials required in stackrox
# roxctl central init-bundles generate hub --output-secrets -""",
        "oc get securedcluster -n stackrox",
    ),
    "finops-kubecost": (
        "| Kubecost hub | components/kubecost/templates/all.yaml | Kubecost |\n| Federated ETL | MinIO bucket kubecost | Object storage |",
        """# Kubecost primary on hub, agents on spokes""",
        "oc get deploy -n kubecost",
    ),
    "openshift-ai": (
        "| DSC | components/openshift-ai-hub/templates/all.yaml | DataScienceCluster |\n| MaaS workshop | maas-workshop namespace | Secret |",
        """apiVersion: datasciencecluster.opendatahub.io/v1
kind: DataScienceCluster
metadata:
  name: default-dsc""",
        "oc get dsc",
    ),
    "llm-rag": (
        "| Lightspeed | components/developer-hub/templates/lightspeed.yaml | Deployment |\n| Kairos agents | components/kairos/ | Console |",
        """# MaaS endpoint shared with NeuroFace and Continue AI on spokes""",
        "oc get deploy -n developer-hub | grep lightspeed",
    ),
    "text-ai-predictive": (
        "| Anomaly alerter | components/ie-anomaly-alerter/ | Deployment |\n| KServe optional | openshift-ai-hub | InferenceService |",
        """# ie-anomaly-alerter watches sensor metrics""",
        "oc get deploy -n industrial-edge-tst-all | grep anomaly",
    ),
    "neuroface": (
        "| NeuroFace UI | components/neuroface/ | Helm wrapper |\n| MaaS chat | neuroface.chat.modelEndpoint | Config |\n| No LibreChat | — | Decision |",
        """chat:
  enabled: true
  modelEndpoint: "https://maas-rhdp.apps.maas.redhatworkshops.io/v1"
  modelName: "llama-scout-17b"
ovms:
  modelmesh:
    enabled: true
litellm:
  enabled: false""",
        "curl -sk https://neuroface.${HUB_DOMAIN}/api/health",
    ),
    "ai-end-user-apps": (
        "| line-dashboard | industrial-edge-tst-all | Deployment |\n| Camel | Camel K Integration | Integration |",
        """# End-user apps consume IE + AI stack on spoke""",
        "oc get deploy -n industrial-edge-tst-all line-dashboard",
    ),
    "full-verification": (
        "| Registration | components/workshop-registration/ | Deployment |\n| Showroom | components/showroom/ | Deployment |\n| Progress API | POST /api/progress | HTTP |",
        """# verification/progress-checklist.yaml — user1 east Parte B""",
        "bash scripts/verify-workshop-e2e.sh",
    ),
    "agent-browser-recording": (
        "| Agent Browser | verification/agent-browser/*.yaml | Scripts |\n| Recordings | NOT in Git | Local only |",
        """# recording-runbook.md — Win+G / OBS, no MP4 in repo
recordings/
*.mp4  # gitignored""",
        "test -f showroom-hybrid-mesh-ai/verification/recording-runbook.md",
    ),
}

MODULES = [
    ("00", "index", "Hybrid Mesh AI Workshop", "Taller Hybrid Mesh AI", "A", True,
     "Agenda Parte A (01–05) y Parte B (10–28). Registro: `https://workshop-registration.{hub_domain}`. Showroom live con terminal `oc`."),
    ("01", "hybrid-cloud-strategy", "Hybrid Cloud Strategy", "Estrategia nube híbrida", "A", False,
     "Modernizar apps, escalar híbrido, automatización/seguridad, time-to-market."),
    ("02", "rosa-architecture", "ROSA Architecture & Benefits", "ROSA arquitectura y beneficios", "A", False,
     "Control plane gestionado AWS; workers; SLA; mismo operador en on-prem y ROSA."),
    ("03", "security-scale-hybrid", "Security & Scale in Hybrid", "Seguridad y escala híbrida", "A", False,
     "ACM governance; mesh zero-trust; observabilidad multicluster; FinOps."),
    ("04", "aws-ai-integration", "AWS Services & AI Integration", "Integración AWS e IA", "A", False,
     "IAM/OIDC; Bedrock/SageMaker narrativa; patrón OpenShift AI + MaaS en lab."),
    ("05", "cases-roadmap", "Real Cases & Roadmap", "Casos reales y roadmap", "A", False,
     "Industrial Edge IoT; Hybrid Mesh AI roadmap; transición a Parte B hands-on."),
    ("10", "acm-multicluster", "Multicluster Fleet & ACM", "Flota multicluster y ACM", "B", False,
     "ACM Clusters; ManagedCluster; GitOpsCluster."),
    ("11", "hybrid-mesh-architecture", "Hybrid Mesh Architecture", "Arquitectura Hybrid Mesh", "B", False,
     "Hub gateway, Skupper, spoke gateways."),
    ("12", "software-templates", "Software Templates", "Plantillas software", "B", False,
     "Developer Hub Create; golden paths. Plan B: demos compartidos en catálogo."),
    ("13", "deploy-industrial-edge", "Deploy Industrial Edge Apps", "Deploy Industrial Edge", "B", False,
     "Scaffold IE east/west; Gitea `ws-{user_name}`; Argo CD Application on spoke."),
    ("14", "kairos-scaling", "Worker Scaling with Kairos", "Escalado con Kairos", "B", False,
     "SmartScalingPolicy sensor-scan; approve flow en Kairos Console."),
    ("15", "observability", "Metrics Logging Dashboards", "Métricas y logging", "B", False,
     "Grafana multicluster; OTEL; Kafka Console."),
    ("16", "openshift-gitops", "OpenShift GitOps", "OpenShift GitOps", "B", False,
     "Argo CD Applications hub + spoke; ApplicationSet."),
    ("17", "service-mesh", "OpenShift Service Mesh", "Service Mesh", "B", False,
     "OSSM3 ambient; Kiali; ztunnel metrics."),
    ("18", "scalability", "Scalability HPA Kafka", "Escalabilidad", "B", False,
     "HPA workloads; KafkaNodePool; Kairos policies."),
    ("19", "network-policies", "Network Policies", "Network Policies", "B", False,
     "NetworkPolicy demo en namespace IE."),
    ("20", "acs-kuadrant", "ACS & Connectivity Link", "ACS y Kuadrant", "B", False,
     "ACS Central; AuthPolicy; APIProduct demo."),
    ("21", "finops-kubecost", "FinOps with Kubecost", "FinOps Kubecost", "B", False,
     "Kubecost hub primary + spoke agents; allocations by namespace."),
    ("22", "openshift-ai", "OpenShift AI Workshop", "Taller OpenShift AI", "B", False,
     "DSC hub; maas-workshop; demo-ods-workspace."),
    ("23", "llm-rag", "LLMs & RAG", "LLMs y RAG", "B", False,
     "Developer Lightspeed; Kairos agents; Continue AI DevSpaces."),
    ("24", "text-ai-predictive", "Generative & Predictive Text", "Texto gen y predictivo", "B", False,
     "Anomaly alerter; KServe optional; MaaS playground."),
    ("25", "neuroface", "Face & Object AI + Chat", "NeuroFace", "B", False,
     "Webcam; YOLO + face detection; `/api/chat` → MaaS. URL: `https://neuroface.{hub_domain}`."),
    ("26", "ai-end-user-apps", "AI in End-User Apps", "IA en apps finales", "B", False,
     "line-dashboard; Camel alerts; NeuroFace + IE stack integration."),
    ("27", "full-verification", "Full Stack Verification", "Verificación completa", "B", False,
     "Checklist Parte A + B; Plan B demos; progress API summary."),
    ("28", "agent-browser-recording", "Agent Browser & Recording", "Agent Browser y grabación", "B", False,
     "Agent Browser YAML en `verification/agent-browser/`. Grabaciones **no** se commitean — ver runbook."),
]


def yaml_section(slug: str) -> str:
    if slug not in YAML_BEHIND:
        return ""
    table, yaml_block, verify = YAML_BEHIND[slug]
    return f"""
== YAML behind the scenes

[cols="2,3,1"]
|===
| UI action | Git source | Kind

{table}
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


def adoc_page(num: str, slug: str, title_en: str, summary: str, is_index: bool) -> str:
    mid = f"{num}-{slug}" if not is_index else "00-index"
    index_extra = INDEX_AGENDA_ADOC if is_index else ""
    live = "\n== Live lab\n* Showroom: terminal `oc` integrada\n" if not is_index and num.isdigit() and int(num) >= 10 else ""
    img = ""
    if slug in ("index", "hybrid-cloud-strategy", "rosa-architecture", "neuroface"):
        img_name = {"index": "00-index-hybrid-mesh", "hybrid-cloud-strategy": "01-hybrid-strategy",
                    "rosa-architecture": "02-rosa-architecture", "neuroface": "25-neuroface-dashboard"}[slug]
        img = f"\nimage::images/{img_name}.png[Workshop illustration,600]\n"

    return f"""= {title_en}
{img}
{HYBRID_CALLOUT_ADOC.strip()}
{index_extra}
== Contexto

{summary}

== Show and Tell

. Facilitador presenta objetivos del módulo **{num}**.
. Señalar analogía ROSA/AWS vs lab en la tabla anterior.
. {"Enlazar registro y demos Plan B." if is_index else "Demostrar en Developer Hub / consola / Showroom terminal."}

== Your TODO (user `{{user_name}}`)

* [ ] Leer callout nube híbrida
* [ ] {"Registrarse en workshop-registration" if is_index else "Completar pasos hands-on o usar demo compartido Plan B"}
* [ ] Marcar progreso al final del módulo
{live}{yaml_section(slug)}
== Verify

[cols="1,2,1"]
|===
| Check | Action | Expected

| Progress | Guardar checkbox al final | `POST /api/progress` OK
|===

{PROGRESS_HTML.format(module_id=mid)}

TIP: Plan B — Demo compartido en Developer Hub → System `hybrid-mesh-shared-demos` si el scaffolder falla.
"""


def md_yaml_section(slug: str) -> str:
    if slug not in YAML_BEHIND:
        return ""
    table, yaml_block, verify = YAML_BEHIND[slug]
    rows = []
    for line in table.strip().split("\n"):
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if len(cols) >= 3:
            rows.append(f"| {cols[0]} | {cols[1]} | {cols[2]} |")
    table_md = "\n".join(rows)
    return f"""
## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
{table_md}

```yaml
{yaml_block.strip()}
```

```bash
{verify}
```
"""


def md_page(num: str, slug: str, title_en: str, summary: str, is_index: bool, parte: str) -> str:
    if is_index:
        return f"""---
layout: default
title: Hybrid Mesh AI Workshop
nav_order: 11
has_children: true
---

> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` — registro: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Hybrid Mesh AI Workshop

{HYBRID_CALLOUT_MD.strip()}

## Agenda

### Parte A (01–05) — Executive
Strategy, ROSA, security/scale, AWS+AI, cases & roadmap.

### Parte B (10–28) — Hands-on
ACM, mesh, GitOps, IE, AI, NeuroFace, verification.

## Registro

OpenShift Console → **Hybrid Mesh AI Workshop** → email → `userN` → Showroom redirect.

{summary}

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
"""
    live = "> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)\n\n"
    return live + f"# {title_en}\n\n{HYBRID_CALLOUT_MD.strip()}\n\n## Contexto\n\n{summary}\n\n## Show and Tell\n\n1. Facilitador cubre módulo **{num}** ({parte}).\n2. Comparar ROSA/AWS vs lab RHDP.\n{md_yaml_section(slug)}\n## Your TODO\n\n- [ ] Completar lectura o lab\n- [ ] Marcar progreso en Showroom in-cluster\n\n## Verify\n\n- Progress API responde OK\n\n---\n\n*Las grabaciones de pantalla del evento no se publican en este repositorio.*\n"


def main() -> None:
    if not SHOWROOM.is_dir():
        SHOWROOM.mkdir(parents=True, exist_ok=True)
    for lang in ("en", "es"):
        pages = SHOWROOM / "content" / "modules" / lang / "ROOT" / "pages"
        pages.mkdir(parents=True, exist_ok=True)
    nav_en = ["* xref:00-index.adoc[Welcome]\n", "\n.Part A — Strategy\n"]
    nav_es = ["* xref:00-index.adoc[Bienvenida]\n", "\n.Parte A — Estrategia\n"]
    for num, slug, en, es, parte, is_idx, summary in MODULES:
        fname = "00-index.adoc" if is_idx else f"{num}-{slug}.adoc"
        en_body = adoc_page(num, slug, en, summary, is_idx)
        es_body = en_body.replace("Show and Tell", "Show and Tell").replace("Your TODO", "Tu TODO").replace(
            "Completé este módulo", "Completé este módulo"
        ).replace("Me interesa profundizar", "Me interesa profundizar").replace(
            "Guardar progreso", "Guardar progreso"
        )
        (SHOWROOM / "content/modules/en/ROOT/pages" / fname).write_text(en_body, encoding="utf-8")
        (SHOWROOM / "content/modules/es/ROOT/pages" / fname).write_text(es_body, encoding="utf-8")
        label = en if is_idx else f"{num}. {en}"
        entry = f"* xref:{fname}[{label}]\n"
        if parte == "A" and num != "00":
            nav_en.append(entry)
            nav_es.append(entry.replace(en, es))
        elif num == "10":
            nav_en.append("\n.Part B — Hands-on\n")
            nav_es.append("\n.Parte B — Hands-on\n")
            nav_en.append(entry)
            nav_es.append(entry.replace(en, es))
        elif parte == "B":
            nav_en.append(entry)
            nav_es.append(entry.replace(en, es))

    for lang, nav in (("en", nav_en), ("es", nav_es)):
        (SHOWROOM / "content/modules" / lang / "ROOT/nav.adoc").write_text("".join(nav), encoding="utf-8")

    (DOCS / "index.md").write_text(md_page("00", "index", "Hybrid Mesh AI Workshop", MODULES[0][6], True, "A"), encoding="utf-8")
    for num, slug, en, es, parte, is_idx, summary in MODULES:
        if is_idx:
            continue
        sub = "parte-a" if parte == "A" else "parte-b"
        (DOCS / sub / f"{num}-{slug}.md").write_text(md_page(num, slug, en, summary, False, parte), encoding="utf-8")

    extras = {
        "registration.md": """---
layout: default
title: Workshop Registration
parent: Hybrid Mesh AI Workshop
nav_order: 1
---

# Workshop Registration

Register via OpenShift Console **Hybrid Mesh AI Workshop** or directly at `https://workshop-registration.YOUR_HUB_DOMAIN/`.

After email registration you receive `userN` and are redirected to the Showroom with terminal `oc`.

Password (demo): `Welcome123!`
""",
        "shared-demos.md": """---
layout: default
title: Shared Demos (Plan B)
parent: Hybrid Mesh AI Workshop
nav_order: 2
---

# Shared Demos — Plan B

Pre-deployed examples in Developer Hub System **hybrid-mesh-shared-demos** — no scaffolder required.

| Template | Catalog entity | URL |
|----------|----------------|-----|
| Industrial Edge | demo-industrial-edge-east | line-dashboard on east |
| Camel Kaoto | demo-camel-kaoto-east | DevSpaces + Topology |
| Camel CDC | demo-camel-cdc-east | Integration status |
| API Product | demo-ie-api-product | Kuadrant APIProduct |
| OpenShift AI | demo-ods-workspace | ODS dashboard |
| CNV VM | demo-cnv-vm | workshop-cnv-demo |
| NeuroFace | demo-neuroface | https://neuroface.YOUR_HUB_DOMAIN |
""",
        "showroom-live.md": """---
layout: default
title: Showroom Live Lab
parent: Hybrid Mesh AI Workshop
nav_order: 3
---

# Showroom Live

- **Entry (registration → Showroom):** OpenShift Console → **Hybrid Mesh AI Workshop**
- **Registration:** `https://workshop-registration.YOUR_HUB_DOMAIN/`
- **Lab guide + terminal:** `https://showroom.YOUR_HUB_DOMAIN/`
- **Antora source:** [showroom-hybrid-mesh-ai](https://github.com/maximilianoPizarro/showroom-hybrid-mesh-ai)
- **GitHub Pages mirror:** this section (read-only)
""",
    }
    for name, content in extras.items():
        (DOCS / name).write_text(content, encoding="utf-8")

    print(f"Generated {len(MODULES)} modules × 2 langs + GitHub Pages workshop/")


if __name__ == "__main__":
    main()
