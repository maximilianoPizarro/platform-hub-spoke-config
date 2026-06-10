#!/usr/bin/env python3
"""Generate Hybrid Mesh AI Workshop Showroom (.adoc) and GitHub Pages (.md) modules."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Antora repo (separate Git): https://github.com/maximilianoPizarro/showroom-hybrid-mesh-ai
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

MODULES = [
    ("00", "index", "Hybrid Mesh AI Workshop", "Taller Hybrid Mesh AI", "A", True,
     "Agenda Parte A (01–05) y Parte B (10–27). Registro: `https://workshop-registration.{hub_domain}`. Showroom live con terminal `oc`."),
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
     "ACM Clusters; ManagedCluster; GitOpsCluster. YAML: `components/acm-hub-spoke/templates/managed-clusters.yaml`."),
    ("11", "hybrid-mesh-architecture", "Hybrid Mesh Architecture", "Arquitectura Hybrid Mesh", "B", False,
     "Hub gateway, Skupper, spoke gateways. YAML: hub-gateway + service-interconnect."),
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
     "NetworkPolicy demo en namespace IE; verify `oc get networkpolicy`."),
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


def adoc_page(num: str, slug: str, title_en: str, summary: str, is_index: bool) -> str:
    mid = f"{num}-{slug}" if not is_index else "00-index"
    body = f"""= {title_en}

{HYBRID_CALLOUT_ADOC.strip()}

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

{"== Live lab" if not is_index and num.startswith(("1", "2")) and num != "01" else ""}
{"* Showroom: terminal `oc` integrada" if not is_index and int(num) >= 10 else ""}

== Verify

[cols="1,2,1"]
|===
| Check | Action | Expected

| Progress | Guardar checkbox al final | `POST /api/progress` OK
|===

{PROGRESS_HTML.format(module_id=mid)}

TIP: Plan B — Demo compartido en Developer Hub → System `hybrid-mesh-shared-demos` si el scaffolder falla.
"""
    return body


def md_page(num: str, slug: str, title_en: str, summary: str, is_index: bool, parte: str) -> str:
    parent = "Hybrid Mesh AI Workshop"
    nav = 0 if is_index else int(num)
    fm = f"""---
layout: default
title: "{title_en}"
parent: {parent}
nav_order: {nav}
---

"""
    if is_index:
        fm = f"""---
layout: default
title: Hybrid Mesh AI Workshop
nav_order: 11
has_children: true
---

"""
    live = "> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)\n\n"
    return fm + live + f"# {title_en}\n\n{HYBRID_CALLOUT_MD.strip()}\n\n## Contexto\n\n{summary}\n\n## Show and Tell\n\n1. Facilitador cubre módulo **{num}** ({parte}).\n2. Comparar ROSA/AWS vs lab RHDP.\n\n## Your TODO\n\n- [ ] Completar lectura o lab\n- [ ] Marcar progreso en Showroom in-cluster\n\n## Verify\n\n- Progress API responde OK\n\n---\n\n*Las grabaciones de pantalla del evento no se publican en este repositorio.*\n"


def main() -> None:
    for lang in ("en", "es"):
        pages = SHOWROOM / "content" / "modules" / lang / "ROOT" / "pages"
        pages.mkdir(parents=True, exist_ok=True)
    nav_en = ["* xref:00-index.adoc[Welcome]\n", "\n.Part A — Strategy\n"]
    nav_es = ["* xref:00-index.adoc[Bienvenida]\n", "\n.Parte A — Estrategia\n"]
    for num, slug, en, es, parte, is_idx, summary in MODULES:
        fname = "00-index.adoc" if is_idx else f"{num}-{slug}.adoc"
        title = en if True else en
        (SHOWROOM / "content/modules/en/ROOT/pages" / fname).write_text(
            adoc_page(num, slug, en, summary, is_idx), encoding="utf-8"
        )
        (SHOWROOM / "content/modules/es/ROOT/pages" / fname).write_text(
            adoc_page(num, slug, es, summary, is_idx).replace("Show and Tell", "Show and Tell").replace(
                "Your TODO", "Tu TODO"
            ),
            encoding="utf-8",
        )
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

    # GitHub Pages
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

Register with your email at `https://workshop-registration.YOUR_HUB_DOMAIN/` to receive `userN` and access the in-cluster Showroom.

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

- **Lab guide + terminal:** `https://showroom.YOUR_HUB_DOMAIN/`
- **Registration:** `https://workshop-registration.YOUR_HUB_DOMAIN/`
- **GitHub Pages mirror:** this section (read-only)
""",
    }
    for name, content in extras.items():
        (DOCS / name).write_text(content, encoding="utf-8")

    print(f"Generated {len(MODULES)} modules × 2 langs + GitHub Pages workshop/")


if __name__ == "__main__":
    main()
