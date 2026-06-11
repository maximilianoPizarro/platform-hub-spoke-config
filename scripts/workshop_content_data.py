"""Data structures for Hybrid Mesh AI Workshop content generator."""
from __future__ import annotations

# slug -> estimated minutes
ESTIMATED_MIN: dict[str, int] = {
    "index": 10,
    "hybrid-cloud-strategy": 10,
    "rosa-architecture": 12,
    "security-scale-hybrid": 12,
    "aws-ai-integration": 10,
    "cases-roadmap": 12,
    "acm-multicluster": 15,
    "hybrid-mesh-architecture": 15,
    "software-templates": 18,
    "deploy-industrial-edge": 25,
    "kairos-scaling": 20,
    "observability": 18,
    "openshift-gitops": 15,
    "service-mesh": 18,
    "scalability": 15,
    "network-policies": 12,
    "acs-kuadrant": 18,
    "finops-kubecost": 15,
    "openshift-ai": 30,
    "ai-gateway": 25,
    "mcp-gateway": 30,
    "llm-rag": 20,
    "text-ai-predictive": 18,
    "neuroface": 30,
    "ai-end-user-apps": 15,
    "full-verification": 15,
    "agent-browser-recording": 12,
}

# slug -> next adoc filename (None for last module)
NEXT_PAGE: dict[str, str | None] = {
    "index": "01-hybrid-cloud-strategy.adoc",
    "hybrid-cloud-strategy": "02-rosa-architecture.adoc",
    "rosa-architecture": "03-security-scale-hybrid.adoc",
    "security-scale-hybrid": "04-aws-ai-integration.adoc",
    "aws-ai-integration": "05-cases-roadmap.adoc",
    "cases-roadmap": "10-acm-multicluster.adoc",
    "acm-multicluster": "11-hybrid-mesh-architecture.adoc",
    "hybrid-mesh-architecture": "12-software-templates.adoc",
    "software-templates": "13-deploy-industrial-edge.adoc",
    "deploy-industrial-edge": "14-kairos-scaling.adoc",
    "kairos-scaling": "15-observability.adoc",
    "observability": "16-openshift-gitops.adoc",
    "openshift-gitops": "17-service-mesh.adoc",
    "service-mesh": "18-scalability.adoc",
    "scalability": "19-network-policies.adoc",
    "network-policies": "20-acs-kuadrant.adoc",
    "acs-kuadrant": "21-finops-kubecost.adoc",
    "finops-kubecost": "22-openshift-ai.adoc",
    "openshift-ai": "23-ai-gateway.adoc",
    "ai-gateway": "24-mcp-gateway.adoc",
    "mcp-gateway": "25-llm-rag.adoc",
    "llm-rag": "26-text-ai-predictive.adoc",
    "text-ai-predictive": "27-neuroface.adoc",
    "neuroface": "28-ai-end-user-apps.adoc",
    "ai-end-user-apps": None,
    "full-verification": None,
    "agent-browser-recording": None,
}

# Not shown in learner nav — used by facilitators / CI agents only
FACILITATOR_ONLY_SLUGS: frozenset[str] = frozenset({"full-verification", "agent-browser-recording"})

# Practical learner context (what to do in the lab — not marketing copy)
MODULE_CONTEXT: dict[str, dict[str, str]] = {
    "acm-multicluster": {
        "en": """In this module you open the **ACM Clusters** view on the hub and confirm `east` and `west` spokes are `Available`. Use the Showroom terminal: `oc get managedclusters`. Every later Part B exercise assumes you know which cluster hosts your workloads (usually `east`).""",
        "es": """En este módulo abres **ACM Clusters** en el hub y confirmas que los spokes `east` y `west` están `Available`. Usa la terminal Showroom: `oc get managedclusters`. Cada ejercicio posterior asume que sabes en qué cluster corren tus cargas (normalmente `east`).""",
    },
    "hybrid-mesh-architecture": {
        "en": """You will trace how external traffic reaches Industrial Edge on a spoke: hub Gateway API `HTTPRoute`, Skupper interconnect, and the IE route. Open the Skupper observer and IE UI from the lab access table — no separate ACM or ROSA documentation site is required.""",
        "es": """Rastrearás cómo el tráfico externo llega a Industrial Edge en un spoke: `HTTPRoute` Gateway API en hub, interconnect Skupper y ruta IE. Abre el observer Skupper y la UI IE desde la tabla de acceso — no necesitas sitios externos de ACM o ROSA.""",
    },
    "software-templates": {
        "en": """You will create (or browse) a workload from **Developer Hub → Create**. If your `%USER_NAME%` scaffold fails, open **Plan B** system `hybrid-mesh-shared-demos` — same URLs, pre-deployed. Check Gitea only if you successfully scaffolded.""",
        "es": """Crearás (o explorarás) una carga desde **Developer Hub → Create**. Si falla el scaffold de `%USER_NAME%`, abre el system **Plan B** `hybrid-mesh-shared-demos`. Revisa Gitea solo si el scaffold tuvo éxito.""",
    },
    "deploy-industrial-edge": {
        "en": """Goal: confirm Industrial Edge workloads are reachable — line dashboard, Kafka topics, and (optional) your user-scoped namespace. Use Plan B demo `demo-industrial-edge-east` if you did not scaffold.""",
        "es": """Objetivo: confirmar que las cargas Industrial Edge responden — line dashboard, topics Kafka y (opcional) tu namespace. Usa demo Plan B `demo-industrial-edge-east` si no hiciste scaffold.""",
    },
    "acs-kuadrant": {
        "en": """You will use **ACS Central** on this cluster (`central-stackrox` route) for runtime security context and **Developer Hub → Kuadrant** to request an API key for `workshop-apis`. Test with `curl` and your key — not a generic Red Hat marketing URL.""",
        "es": """Usarás **ACS Central** en este cluster (ruta `central-stackrox`) y **Developer Hub → Kuadrant** para solicitar API key de `workshop-apis`. Prueba con `curl` y tu key — no URLs genéricas de marketing.""",
    },
    "ai-gateway": {
        "en": """Open **Developer Hub → Catalog → workshop-ai-gateway** and trace GitOps in `components/workshop-kuadrant-apis/`. Create a Kuadrant API key and call the MaaS LLM route at `workshop-apis.%HUB_DOMAIN%/llm`.""",
        "es": """Abre **Developer Hub → Catálogo → workshop-ai-gateway** y sigue GitOps en `components/workshop-kuadrant-apis/`. Crea API key Kuadrant y llama la ruta MaaS LLM.""",
    },
    "mcp-gateway": {
        "en": """Verify MCP Gateway in `mcp-system`, then use **Developer Hub → Lightspeed** with prompts that invoke ArgoCD/k8s MCP tools. Register OpenShift AI MCP server in dashboard (maas-workshop).""",
        "es": """Verifica MCP Gateway en `mcp-system`, usa **Developer Hub → Lightspeed** con tools MCP, y registra MCP server OpenShift AI en el dashboard.""",
    },
    "openshift-ai": {
        "en": """Open the **OpenShift AI dashboard** → project **ai-%USER_NAME%** → **Workbenches → workshop-notebook** and run the MaaS smoke-test notebook. Catalog entity **OpenShift AI — %USER_NAME%** links Topology and dashboard.""",
        "es": """Abre **dashboard OpenShift AI** → proyecto **ai-%USER_NAME%** → **Workbenches → workshop-notebook** y ejecuta el notebook MaaS. La entidad **OpenShift AI — %USER_NAME%** enlaza Topology y dashboard.""",
    },
    "neuroface": {
        "en": """Open link:https://neuroface.%HUB_DOMAIN%[NeuroFace] and **Developer Hub → Catalog → neuroface-workshop** for Topology. OVMS is enabled for local vision; chat uses MaaS. Allow webcam and test detection + `/api/chat`.""",
        "es": """Abre link:https://neuroface.%HUB_DOMAIN%[NeuroFace] y **Developer Hub → Catálogo → neuroface-workshop**. OVMS habilitado para visión local; chat usa MaaS.""",
    },
    "ai-end-user-apps": {
        "en": """Capstone: tie together IE dashboard, Developer Hub catalog entries, and Grafana for `%USER_NAME%`. This is the **last learner module (28)** — facilitators run automated verification separately.""",
        "es": """Cierre: conecta dashboard IE, entradas Developer Hub y Grafana para `%USER_NAME%`. Este es el **último módulo del participante (28)**.""",
    },
    "full-verification": {
        "en": """**Facilitator / agent only.** Run `scripts/verify-workshop-e2e.sh` and `showroom-hybrid-mesh-ai/verification/progress-checklist.yaml` — not shown to learners in the workshop nav.""",
        "es": """**Solo facilitador / agente.** Ejecuta `scripts/verify-workshop-e2e.sh` y `showroom-hybrid-mesh-ai/verification/progress-checklist.yaml` — no aparece en la navegación del participante.""",
    },
    "agent-browser-recording": {
        "en": """**Facilitator / agent only.** Agent Browser YAML under `verification/agent-browser/` replays UI flows for CI. Recordings stay local (`*.mp4` gitignored).""",
        "es": """**Solo facilitador / agente.** YAML Agent Browser bajo `verification/agent-browser/` reproduce flujos UI para CI. Grabaciones locales (`*.mp4` gitignored).""",
    },
}

HYBRID_INTEGRATION_EN = """
[[#hybrid-integration]]
== Hybrid cloud integration notes

Workshop patterns apply to OpenShift on-premises, at the edge, or on public cloud. This lab uses a pre-provisioned RHDP hub-spoke fleet — use the snippets below when you need to provision or attach similar services in AWS or Azure.

=== AWS — attach clusters and integrate services

[source,bash]
----
# Example: create ROSA cluster (or use existing EKS/ROSA) and import to ACM hub
rosa create cluster --cluster-name=factory-edge --region=us-east-1
# ACM: cluster import / ManagedCluster — see module 10
aws iam create-open-id-connect-provider ...   # OIDC for cloud integrations
aws s3 mb s3://my-data-lake                   # analog to MinIO data lake on hub
----

=== Azure — attach AKS and optional AI endpoints

[source,bash]
----
az aks create --resource-group rg-workshop --name aks-edge --node-count 3
# Import to ACM hub (ManagedCluster) — same GitOps placement as east/west spokes
# Azure OpenAI can replace MaaS for inference; lab uses OpenShift AI + MaaS (module 22)
----

Hands-on equivalents: ACM fleet (module 10), Kuadrant API gateway (module 20), OpenShift AI + MaaS (modules 22–25).
"""

HYBRID_INTEGRATION_ES = """
[[#hybrid-integration]]
== Notas de integración nube híbrida

Los patrones del taller aplican a OpenShift on-prem, edge o cloud público. Este lab usa flota RHDP hub-spoke pre-provisionada — usa los snippets siguientes para provisionar o adjuntar servicios similares en AWS o Azure.

=== AWS — adjuntar clusters e integrar servicios

[source,bash]
----
rosa create cluster --cluster-name=factory-edge --region=us-east-1
aws iam create-open-id-connect-provider ...
aws s3 mb s3://my-data-lake
----

=== Azure — adjuntar AKS e IA opcional

[source,bash]
----
az aks create --resource-group rg-workshop --name aks-edge --node-count 3
----

Equivalentes hands-on: flota ACM (módulo 10), Kuadrant (20), OpenShift AI + MaaS (22–25).
"""

HYBRID_CALLOUT_EN = HYBRID_INTEGRATION_EN
HYBRID_CALLOUT_ES = HYBRID_INTEGRATION_ES

REGISTRATION_CTA_EN = """
++++
<p class="workshop-register-cta">
  <a id="workshop-register-cta-main" class="workshop-register-btn"
     href="https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%"
     target="_blank" rel="noopener noreferrer">Register for lab access →</a>
  <span class="workshop-register-hint">Already registered? Open this page with <code>USER_NAME=userN</code> in the URL.</span>
</p>
++++
"""

REGISTRATION_CTA_ES = """
++++
<p class="workshop-register-cta">
  <a id="workshop-register-cta-main" class="workshop-register-btn"
     href="https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%"
     target="_blank" rel="noopener noreferrer">Registrarse para acceso al lab →</a>
  <span class="workshop-register-hint">¿Ya registrado? Abre esta página con <code>USER_NAME=userN</code> en la URL.</span>
</p>
++++
"""

INDEX_LAB_ACCESS_NOTE_EN = """NOTE: *Workshop login* — %USER_NAME% / `Welcome123!` (Keycloak Developer Hub; htpasswd OpenShift hub/east/west; DevSpaces east). OAuth products use the same OpenShift identity.

"""

INDEX_LAB_ACCESS_NOTE_ES = """NOTE: *Login del taller* — %USER_NAME% / `Welcome123!` (Keycloak Developer Hub; htpasswd consola hub/east/west; DevSpaces east). Productos OAuth usan la misma identidad OpenShift.

"""

INDEX_INTRO_EN = """
Welcome to the *Hybrid Mesh AI Workshop* — a dual-track experience that mirrors how Red Hat customers run hybrid cloud on OpenShift.

*Part A (modules 01–05)* is executive-oriented: it covers hybrid cloud strategy, ROSA architecture, security at scale, AWS AI integration, and real customer cases. No hands-on required — facilitators can demo while the audience follows along.

*Part B (modules 10–28)* is fully hands-on on a live RHDP hub-spoke fleet provisioned for this workshop. Each module targets a specific product area and includes a `verify` step to confirm your work.

The lab simulates a production hybrid mesh: a hub cluster (OpenShift on AWS) managing two spoke clusters (east and west) via ACM, with ambient service mesh, GitOps, and an AI inference layer backed by OpenShift AI + MaaS.

Register at `https://workshop-registration.%HUB_DOMAIN%` to receive your lab identity (`userN`). The Showroom at `https://showroom-showroom.%HUB_DOMAIN%` embeds an authenticated `oc` terminal — no local kubeconfig required. If scaffolding fails, use *Plan B* shared demos in Developer Hub → System `hybrid-mesh-shared-demos`.
"""

INDEX_HUB_SPOKE_EN = """
== Hub-spoke architecture

The workshop fleet is a three-cluster hub-spoke topology managed by ACM:

[source,yaml]
----
# ACM ManagedCluster — hub registers spoke clusters automatically
apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: east
  labels:
    cloud: Amazon
    region: us-east-1
    env: workshop
spec:
  hubAcceptsClient: true
----

[source,yaml]
----
# GitOpsCluster — lets Argo CD on the hub deploy to spokes
apiVersion: apps.open-cluster-management.io/v1beta1
kind: GitOpsCluster
metadata:
  name: workshop-gitops
  namespace: openshift-gitops
spec:
  argoServer:
    cluster: local-cluster
    argoNamespace: openshift-gitops
  placementRef:
    kind: Placement
    apiGroup: cluster.open-cluster-management.io
    name: all-workshop-clusters
----

The hub runs: ACM, OpenShift GitOps (Argo CD), Developer Hub, OpenShift AI, Service Mesh control plane, Skupper, Kuadrant, ACS Central, Grafana, and Kubecost. +
The east spoke runs: Industrial Edge workloads, DevSpaces, Kairos, and spoke-local Argo CD agents. +
The west spoke runs: additional workload replicas and demonstrates cross-cluster traffic via Skupper.
"""

INDEX_MESH_FLOW_EN = """
== Service mesh & traffic flow

The workshop uses OpenShift Service Mesh 3 in *ambient mode* (no sidecars). Traffic between hub and spokes crosses a Skupper tunnel exposed via Gateway API:

[source,yaml]
----
# HTTPRoute — routes /api/inference from hub gateway to MaaS on east spoke via Skupper
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: maas-inference-route
  namespace: hybrid-mesh-gateway
spec:
  parentRefs:
    - name: hub-gateway
      namespace: hybrid-mesh-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api/inference
      backendRefs:
        - name: skupper-maas-backend   # Skupper connector bridging to east spoke
          port: 8080
----

[source,yaml]
----
# AuthorizationPolicy — zero-trust: only gateway SA can reach MaaS
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: maas-allow-gateway
  namespace: maas-workshop
spec:
  selector:
    matchLabels:
      app: maas-api
  rules:
    - from:
        - source:
            principals:
              - cluster.local/ns/hybrid-mesh-gateway/sa/hub-gateway
----
"""

INDEX_AI_MAAS_EN = """
== OpenShift AI — Model as a Service

The AI layer is a shared LLM endpoint (MaaS) deployed on the hub via the OpenShift AI operator. All AI modules (22–26) consume this endpoint.

[source,yaml]
----
# DataScienceCluster — installs all RHOAI components on the hub
apiVersion: datasciencecluster.opendatahub.io/v1
kind: DataScienceCluster
metadata:
  name: default-dsc
spec:
  components:
    dashboard: {managementState: Managed}
    workbenches: {managementState: Managed}
    modelmeshserving: {managementState: Managed}
    datasciencepipelines: {managementState: Managed}
    kserve: {managementState: Managed}
----

[source,yaml]
----
# Secret — OpenAI-compatible base URL pointing to the in-cluster MaaS
apiVersion: v1
kind: Secret
metadata:
  name: maas-api-key
  namespace: maas-workshop
stringData:
  OPENAI_API_BASE: "http://maas-api.maas-workshop.svc.cluster.local:8080/v1"
  OPENAI_API_KEY: "workshop-key-%USER_NAME%"
----

Any application that speaks the OpenAI REST API can consume MaaS without code changes — just point `OPENAI_API_BASE` to the in-cluster service.
"""

INDEX_KUADRANT_EN = """
== Kuadrant API gateway

Kuadrant manages API rate limiting and auth policies across the hub gateway. Each workshop user gets their own API key scoped to a plan:

[source,yaml]
----
# APIProduct — exposes the workshop AI endpoints under a single managed product
apiVersion: kuadrant.io/v1alpha1
kind: APIProduct
metadata:
  name: workshop-ai-api
  namespace: kuadrant-system
spec:
  hosts:
    - workshop-apis.%HUB_DOMAIN%
  APIs:
    - name: maas-inference-route
      namespace: hybrid-mesh-gateway
----

[source,yaml]
----
# TokenRateLimitPolicy — limits per API key to 100 req/min for workshop users
apiVersion: kuadrant.io/v1alpha1
kind: TokenRateLimitPolicy
metadata:
  name: workshop-rate-limit
  namespace: kuadrant-system
spec:
  targetRef:
    group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: maas-inference-route
  limits:
    per-user:
      rates:
        - limit: 100
          duration: 1
          unit: minute
      counters:
        - auth.identity.username
----
"""

INDEX_VERIFY_EN = """
Run these checks from the embedded Showroom terminal to confirm the lab environment is ready:

[source,bash]
----
# 1. Hub cluster is reachable and you are logged in
oc whoami
# Expected: user1 (or your assigned userN)

# 2. Both spoke clusters are registered and available
oc get managedclusters
# Expected: NAME    HUB ACCEPTED   MANAGED CLUSTER URLS   JOINED   AVAILABLE
#           east    true           ...                    True     True
#           west    true           ...                    True     True

# 3. OpenShift AI operator is running
oc get dsc default-dsc -o jsonpath='{.status.phase}'
# Expected: Ready

# 4. MaaS endpoint is responding
curl -s http://maas-api.maas-workshop.svc.cluster.local:8080/v1/models | jq '.data[].id'
# Expected: one or more model IDs (e.g. "mistral-7b")
----

[cols="2,3,3", options="header"]
|===
| Check | Command | Expected result
| Login | `oc whoami` | `user1`
| Spoke clusters | `oc get managedclusters` | east + west, AVAILABLE=True
| OpenShift AI | `oc get dsc default-dsc` | phase: Ready
| MaaS health | curl to maas-api | model IDs returned
| Developer Hub | open URL in browser | catalog loads
|===
"""

INDEX_INTRO_ES = """
Bienvenido al **Taller Hybrid Mesh AI** — experiencia dual en flota hub-spoke RHDP. Parte A (01–05) es narrativa ejecutiva; Parte B (10–28) es hands-on en este Showroom y la consola OpenShift.

Regístrate en link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[registro del taller] para obtener **%USER_NAME%**. Abre link:https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[Showroom] para la terminal `oc` integrada. Si falla el scaffolder, usa demos **Plan B** en link:https://developer-hub.%HUB_DOMAIN%/catalog/default/system/hybrid-mesh-shared-demos[Developer Hub — hybrid-mesh-shared-demos].

NOTE: La verificación E2E y runbooks de grabación en `showroom-hybrid-mesh-ai/verification/` son solo para **facilitadores y agentes de automatización** — no forman parte del recorrido del participante.
"""

PROGRESS_UI_EN = """
++++
<div class="workshop-progress" data-module="{module_id}">
  <label><input type="checkbox" data-completed> I completed this module</label>
  <label><input type="checkbox" data-interest> I want to learn more</label>
  <button type="button" onclick="saveWorkshopProgress('{module_id}')">Save progress</button>
</div>
++++
"""

PROGRESS_UI_ES = """
++++
<div class="workshop-progress" data-module="{module_id}">
  <label><input type="checkbox" data-completed> Completé este módulo</label>
  <label><input type="checkbox" data-interest> Me interesa profundizar</label>
  <button type="button" onclick="saveWorkshopProgress('{module_id}')">Guardar progreso</button>
</div>
++++
"""

PRODUCT_CATALOG_EN = """
== Red Hat product catalog in this workshop

=== OpenShift Container Platform
* **Advanced Cluster Management (ACM)** — fleet governance, policies, and GitOps-driven placement across hub and spokes.
* **Red Hat Advanced Cluster Security (ACS)** — runtime threat detection and compliance (`stackrox`; outside ambient mesh).
* **Quay** — container registry referenced by GitOps and template outputs.
* **OpenShift GitOps** — Argo CD Applications and ApplicationSets sync workshop components from Git.
* **Red Hat OpenShift Dev Spaces** — cloud IDE on the east spoke for Kaoto, Continue AI, and templates.
* **OpenShift Pipelines** — Tekton pipelines in Industrial Edge and template workflows.
* **OpenShift distributed tracing / cluster observability** — metrics, logging, and traces (Grafana, Kiali, OTEL).
* **OpenShift Service Mesh 3** — ambient mesh with ztunnel and L7 policy for Industrial Edge apps.

=== Red Hat Application Foundation
* **Apache Camel on Kubernetes** — integrations and CDC pipelines in the Industrial Edge demo.
* **Connectivity Link** — Gateway API ingress/egress patterns at the hub gateway (Skupper, HTTPRoute, external backends).
* **Kuadrant** — APIProduct catalog, AuthPolicy, PlanPolicy, and TokenRateLimitPolicy (separate from Connectivity Link).

=== Red Hat Advanced Developer Suite
* **Developer Hub (Backstage)** — software catalog, scaffolder templates, and Topology for multicluster views.
* **Software Templates** — golden paths for Industrial Edge, Camel, CNV, and OpenShift AI workspaces.

=== OpenShift AI
* **DataScienceCluster (DSC)** — unified operator for notebooks, serving, and model mesh on the hub.
* **Model-as-a-Service (MaaS)** — shared LLM endpoint consumed by NeuroFace, Lightspeed, and DevSpaces.
* **NeuroFace** — webcam object/face detection plus chat backed by MaaS.

=== OpenShift Virtualization
* **Container-native virtualization (CNV)** — VM workloads alongside containers via the workshop CNV demo template.

=== Community & third-party
* **Kairos Community** — SmartScalingPolicy recommendations for Industrial Edge sensor workloads (community operator).
* **Gitea** — per-user org `ws-%USER_NAME%` stores scaffolded Git repos for Argo CD.
* **MinIO** — object storage for model artifacts and data lake patterns.
* **Kubecost** — FinOps allocations on the hub cluster.
"""

PRODUCT_CATALOG_ES = """
== Catálogo de productos Red Hat en este taller

=== OpenShift Container Platform
* **Advanced Cluster Management (ACM)** — gobernanza de flota, políticas y placement GitOps entre hub y spokes.
* **Red Hat Advanced Cluster Security (ACS)** — detección runtime y cumplimiento (`stackrox`; fuera del mesh ambient).
* **Quay** — registro de contenedores referenciado por GitOps y plantillas.
* **OpenShift GitOps** — Applications y ApplicationSets de Argo CD sincronizan componentes desde Git.
* **Red Hat OpenShift Dev Spaces** — IDE en la nube en spoke east (Kaoto, Continue AI, plantillas).
* **OpenShift Pipelines** — pipelines Tekton en Industrial Edge y flujos de plantillas.
* **Trazas distribuidas / observabilidad del cluster** — métricas, logging y trazas (Grafana, Kiali, OTEL).
* **OpenShift Service Mesh 3** — mesh ambient con ztunnel y políticas L7 para apps Industrial Edge.

=== Red Hat Application Foundation
* **Apache Camel on Kubernetes** — integraciones y pipelines CDC en el demo Industrial Edge.
* **Connectivity Link** — patrones Gateway API ingress/egress en hub gateway (Skupper, HTTPRoute, APIs externas).
* **Kuadrant** — catálogo APIProduct, AuthPolicy, PlanPolicy y TokenRateLimitPolicy (separado de Connectivity Link).

=== Red Hat Advanced Developer Suite
* **Developer Hub (Backstage)** — catálogo, plantillas scaffolder y Topology multicluster.
* **Software Templates** — golden paths para Industrial Edge, Camel, CNV y workspaces OpenShift AI.

=== OpenShift AI
* **DataScienceCluster (DSC)** — operador unificado para notebooks, serving y model mesh en el hub.
* **Model-as-a-Service (MaaS)** — endpoint LLM compartido por NeuroFace, Lightspeed y DevSpaces.
* **NeuroFace** — detección objeto/rostro por webcam más chat vía MaaS.

=== OpenShift Virtualization
* **Virtualización nativa de contenedores (CNV)** — cargas VM junto a contenedores vía plantilla demo CNV.

=== Comunidad y terceros
* **Kairos Community** — SmartScalingPolicy para cargas de sensores IE (operador community).
* **Gitea** — org por usuario `ws-%USER_NAME%` para repos Git generados por Argo CD.
* **MinIO** — almacenamiento objeto para artefactos y data lake.
* **Kubecost** — asignaciones FinOps en el hub.
"""

PREREQUISITES_EN = """
== Prerequisites

* Modern web browser (Chrome or Firefox recommended) with webcam access for NeuroFace modules.
* Access to the OpenShift console on the workshop hub — launch **Hybrid Mesh AI Workshop** from the Application menu.
* Workshop registration at link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[workshop registration] to obtain `%USER_NAME%` and Showroom redirect.
* Optional: use the embedded Showroom terminal for `oc` commands; no local kubeconfig required for Part B.
"""

PREREQUISITES_ES = """
== Prerrequisitos

* Navegador moderno (Chrome o Firefox recomendado) con acceso a webcam para módulos NeuroFace.
* Acceso a la consola OpenShift del hub — iniciar **Hybrid Mesh AI Workshop** desde el menú Application.
* Registro en link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[registro del taller] para obtener `%USER_NAME%` y redirect al Showroom.
* Opcional: terminal Showroom integrada para comandos `oc`; no se requiere kubeconfig local para la Parte B.
"""

NARRATIVES: dict[str, dict[str, str]] = {
    "index": {
        "en": """This workshop demonstrates how Red Hat customers unify strategy and operations across hybrid cloud using OpenShift as the common platform. You will apply the same patterns on a live RHDP hub-spoke lab with east and west spokes managed by ACM.

Part A frames the business case: modernization, security, FinOps, and AI. Part B (modules 10–28) lets you use Industrial Edge, multicluster observability, Kuadrant API security, and OpenShift AI — as `%USER_NAME%` in this lab environment.

Register at link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[workshop registration] before hands-on modules.""",
        "es": """Este taller demuestra cómo unificar estrategia y operaciones en nube híbrida con OpenShift. Aplicarás los mismos patrones en un lab hub-spoke RHDP con spokes east y west gestionados por ACM.

La Parte A enmarca el caso de negocio; la Parte B (módulos 10–28) usa Industrial Edge, observabilidad multicluster, Kuadrant y OpenShift AI — como `%USER_NAME%` en este entorno.

Regístrate en link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[registro] antes de los módulos hands-on.""",
    },
    "hybrid-cloud-strategy": {
        "en": """Hybrid cloud strategy starts with workload placement: keep latency-sensitive factory systems at the edge, burst analytics and AI training to cloud regions, and govern everything from a central OpenShift hub. Red Hat OpenShift Container Platform delivers a single Kubernetes API and operator model whether clusters run on-prem, at edge sites, or as ROSA in AWS.

In this lab, ACM on the hub represents that governance layer — policies, observability federation, and GitOps placement target east and west spokes the same way a customer would target ROSA and on-prem clusters. You are not learning abstract slides; every Part B module reinforces a strategic pillar: automation, security, developer velocity, or AI readiness.

Executives should note that OpenShift avoids replatforming twice: microservices, VMs (CNV), and AI pipelines share the same RBAC, networking, and CI/CD patterns. When you register as `%USER_NAME%`, your hands-on path mirrors how platform teams onboard application squads in production.""",
        "es": """La estrategia de nube híbrida comienza con la ubicación de cargas: sistemas de fábrica sensibles a latencia en el edge, analytics e IA en regiones cloud, y gobernanza central desde un hub OpenShift. Red Hat OpenShift Container Platform ofrece una API Kubernetes y modelo de operadores únicos on-prem, edge o ROSA en AWS.

En este lab, ACM en el hub representa esa capa de gobernanza — políticas, federación de observabilidad y placement GitOps hacia spokes east y west como un cliente hacia clusters ROSA y on-prem. No aprendes diapositivas abstractas; cada módulo de la Parte B refuerza un pilar estratégico: automatización, seguridad, velocidad de desarrollo o preparación para IA.

Los ejecutivos deben notar que OpenShift evita replatformear dos veces: microservicios, VMs (CNV) e pipelines de IA comparten RBAC, red y CI/CD. Al registrarte como `%USER_NAME%`, tu ruta hands-on refleja cómo los equipos de plataforma incorporan squads en producción.""",
    },
    "rosa-architecture": {
        "en": """Red Hat OpenShift Service on AWS (ROSA) provides a fully managed control plane in your AWS account while Red Hat handles upgrades, security patches, and SRE operations. Worker nodes scale via MachineSets; ingress integrates with Route 53 and ALB; IAM and STS enable secure cloud service access — the reference architecture for hybrid customers who standardize on OpenShift everywhere.

This workshop's hub-spoke layout maps cleanly to ROSA concepts: the hub is your fleet management cluster (like an ACM hub on ROSA), spokes are regional or edge clusters importing via ManagedCluster resources. You will inspect `ManagedCluster` objects and GitOpsCluster links in module 10 — the same CRDs a ROSA customer uses when joining factory edge clusters to a central governance hub.

Understanding ROSA architecture helps you explain SLA boundaries: Red Hat manages the control plane; you own worker sizing, networking, and data. In the lab, Kairos and HPA on spokes simulate ROSA autoscaling decisions without AWS billing, preparing you for FinOps modules later.""",
        "es": """Red Hat OpenShift Service on AWS (ROSA) ofrece un plano de control totalmente gestionado en tu cuenta AWS mientras Red Hat maneja upgrades, parches de seguridad y operaciones SRE. Los workers escalan vía MachineSets; el ingress integra Route 53 y ALB; IAM y STS habilitan acceso seguro a servicios cloud — la arquitectura de referencia para clientes híbridos que estandarizan OpenShift.

El layout hub-spoke de este taller mapea a conceptos ROSA: el hub es tu cluster de gestión de flota (como un hub ACM en ROSA), los spokes son clusters regionales o edge que importan vía ManagedCluster. Inspeccionarás objetos `ManagedCluster` y enlaces GitOpsCluster en el módulo 10 — los mismos CRDs que un cliente ROSA usa al unir clusters edge de fábrica a un hub de gobernanza.

Entender la arquitectura ROSA ayuda a explicar límites de SLA: Red Hat gestiona el plano de control; tú el sizing de workers, red y datos. En el lab, Kairos y HPA en spokes simulan decisiones de autoscaling ROSA sin facturación AWS, preparándote para módulos FinOps posteriores.""",
    },
    "security-scale-hybrid": {
        "en": """Security and scale in hybrid OpenShift environments require defense in depth: identity federation, network segmentation, runtime threat detection, and policy-driven compliance across every cluster in the fleet. Red Hat Advanced Cluster Security (ACS) centralizes vulnerability management and runtime policies while OpenShift Service Mesh adds zero-trust connectivity between microservices.

In this lab, ACS Central runs on the hub with SecuredCluster agents on spokes — note that the `stackrox` namespace deliberately avoids ambient mesh labels so ACS sensors are not disrupted. NetworkPolicy demos in module 19 use OVN on spokes, analogous to security groups plus Kubernetes NP on ROSA. Kuadrant AuthPolicy at the hub gateway shows how API traffic is authenticated and rate-limited before it reaches Industrial Edge backends.

Scaling hybrid fleets means automating placement and capacity: ACM policies, Kairos SmartScalingPolicy, Kafka buffering, and HPA together handle sensor spikes without manual ticket queues. As `%USER_NAME%`, you will observe these controls in modules 14 and 18 on workloads that simulate factory telemetry bursts.""",
        "es": """Seguridad y escala en entornos OpenShift híbridos requieren defensa en profundidad: federación de identidad, segmentación de red, detección de amenazas en runtime y cumplimiento basado en políticas en toda la flota. Red Hat Advanced Cluster Security (ACS) centraliza gestión de vulnerabilidades y políticas runtime mientras OpenShift Service Mesh añade conectividad zero-trust entre microservicios.

En este lab, ACS Central corre en el hub con agentes SecuredCluster en spokes — el namespace `stackrox` evita deliberadamente labels de mesh ambient para no interferir con sensores ACS. Los demos NetworkPolicy del módulo 19 usan OVN en spokes, análogos a security groups más NP Kubernetes en ROSA. AuthPolicy Kuadrant en el gateway del hub muestra autenticación y rate limiting antes de backends Industrial Edge.

Escalar flotas híbridas implica automatizar placement y capacidad: políticas ACM, Kairos SmartScalingPolicy, buffering Kafka y HPA manejan picos de sensores sin colas manuales. Como `%USER_NAME%`, observarás estos controles en los módulos 14 y 18 en cargas que simulan ráfagas de telemetría de fábrica.""",
    },
    "aws-ai-integration": {
        "en": """AWS customers often pair ROSA with native AI services — Amazon Bedrock for foundation models, SageMaker for training pipelines, and IAM OIDC for secure workload identity. Red Hat's hybrid approach keeps inference and data pipelines on OpenShift AI while still allowing optional AWS service integration via credentials and external endpoints where policy permits.

This workshop intentionally substitutes OpenShift AI plus Model-as-a-Service (MaaS) for Bedrock/SageMaker so you experience a portable pattern: a `DataScienceCluster` on the hub, shared LLM endpoint, and consumer apps (NeuroFace, Developer Hub Lightspeed) on spokes. The secret `openshift-ai-maas-credentials` and MaaS base URL mirror how production teams centralize model access instead of embedding API keys in every deployment.

Module 22 onward activates this stack hands-on. Executives should recognize that OpenShift AI on ROSA or on-prem avoids rewriting applications when cloud AI pricing or residency rules change — the Kubernetes-native serving layer moves with the cluster.""",
        "es": """Los clientes AWS suelen combinar ROSA con servicios nativos de IA — Amazon Bedrock para modelos foundation, SageMaker para pipelines de entrenamiento e IAM OIDC para identidad segura de cargas. El enfoque híbrido de Red Hat mantiene inferencia y pipelines de datos en OpenShift AI permitiendo integración opcional con servicios AWS vía credenciales y endpoints externos donde la política lo permita.

Este taller sustituye intencionalmente OpenShift AI más Model-as-a-Service (MaaS) por Bedrock/SageMaker para que experimentes un patrón portable: `DataScienceCluster` en el hub, endpoint LLM compartido y apps consumidoras (NeuroFace, Developer Hub Lightspeed) en spokes. El secret `openshift-ai-maas-credentials` y la URL base MaaS reflejan cómo los equipos centralizan acceso a modelos en lugar de incrustar API keys en cada despliegue.

Desde el módulo 22 se activa este stack hands-on. Los ejecutivos deben reconocer que OpenShift AI en ROSA u on-prem evita reescribir aplicaciones cuando cambian precios o reglas de residencia — la capa de serving nativa Kubernetes se mueve con el cluster.""",
    },
    "cases-roadmap": {
        "en": """**Industry case — precision manufacturing IoT:** A global automotive supplier deployed OpenShift at three factory edge sites plus a ROSA hub for analytics. Machine vibration sensors emit 12,000 events/minute per line; unplanned downtime cost $47,000/hour. After migrating to Industrial Edge on OpenShift with Kafka, Camel integrations, and ACS runtime policies, mean time to detect anomalies dropped from 18 minutes to 90 seconds, and Kairos-approved scaling reduced over-provisioned edge nodes by 34%.

That customer roadmap led to OpenShift AI for predictive maintenance models and Developer Hub templates so each plant could scaffold compliant pipelines without shadow IT. This workshop reproduces that journey at lab scale: modules 13–18 deploy IE on spoke east/west, modules 22–26 add MaaS and NeuroFace, module 21 adds Kubecost chargeback by namespace.

Your next step is Part B registration verification — ensure `%USER_NAME%` works in Showroom, then proceed to module 10 for ACM fleet visibility. Plan B shared demos remain available if your scaffold slot is unavailable.""",
        "es": """**Caso industrial — IoT de manufactura de precisión:** Un proveedor automotriz global desplegó OpenShift en tres sitios edge de fábrica más un hub ROSA para analytics. Sensores de vibración emiten 12.000 eventos/minuto por línea; el downtime no planificado costaba 47.000 USD/hora. Tras migrar a Industrial Edge en OpenShift con Kafka, integraciones Camel y políticas runtime ACS, el tiempo medio de detección de anomalías bajó de 18 minutos a 90 segundos, y el escalado aprobado por Kairos redujo nodos edge sobreaprovisionados un 34%.

El roadmap de ese cliente llevó a OpenShift AI para modelos de mantenimiento predictivo y plantillas Developer Hub para que cada planta scaffoldeara pipelines conformes sin shadow IT. Este taller reproduce ese recorrido a escala lab: módulos 13–18 despliegan IE en spokes east/west, módulos 22–26 añaden MaaS y NeuroFace, módulo 21 añade chargeback Kubecost por namespace.

Tu siguiente paso es verificar registro Parte B — confirma que `%USER_NAME%` funciona en Showroom, luego continúa al módulo 10 para visibilidad de flota ACM. Los demos compartidos Plan B siguen disponibles si tu slot de scaffold no está libre.""",
    },
    "acm-multicluster": {
        "en": """Red Hat Advanced Cluster Management for Kubernetes turns OpenShift into a fleet control plane: import spokes, enforce policies, visualize health, and delegate GitOps to cluster admins with consistent RBAC. ManagedCluster and Klusterlet agents mirror how ROSA and on-prem clusters join a customer's governance hub without sharing kube-admin credentials broadly.

In this lab, open ACM Clusters on the hub and locate east and west — each spoke was bootstrapped from `components/acm-hub-spoke/` GitOps manifests. As `%USER_NAME%`, your workloads land on east by default; Topology in Developer Hub uses OCM APIs to show the same graph ACM displays.

This module establishes the mental model for every subsequent Part B exercise: the hub owns ingress, policy, FinOps aggregation, and AI control planes; spokes run Industrial Edge and user-scoped namespaces. Verify with `oc get managedclusters` from the Showroom terminal.""",
        "es": """Red Hat Advanced Cluster Management for Kubernetes convierte OpenShift en plano de control de flota: importar spokes, aplicar políticas, visualizar salud y delegar GitOps con RBAC consistente. ManagedCluster y agentes Klusterlet reflejan cómo clusters ROSA y on-prem se unen al hub de gobernanza sin compartir kube-admin ampliamente.

En este lab, abre ACM Clusters en el hub y localiza east y west — cada spoke se bootstrapeó desde manifiestos GitOps de `components/acm-hub-spoke/`. Como `%USER_NAME%`, tus cargas aterrizan en east por defecto; Topology en Developer Hub usa APIs OCM para mostrar el mismo grafo que ACM.

Este módulo establece el modelo mental para cada ejercicio Parte B: el hub posee ingress, política, agregación FinOps y planos de control IA; los spokes ejecutan Industrial Edge y namespaces con alcance de usuario. Verifica con `oc get managedclusters` desde la terminal Showroom.""",
    },
    "hybrid-mesh-architecture": {
        "en": """Hybrid mesh architecture connects application networks across clusters without flattening VPCs or exposing kube-apiserver endpoints publicly. Red Hat Service Interconnect (Skupper) paired with Gateway API HTTPRoutes on the hub creates a logical application network: frontends on the hub route to spoke services through encrypted links.

In this workshop, the hub gateway terminates external traffic and forwards to Industrial Edge frontends on east/west via Skupper Sites and Connectors defined under `components/service-interconnect/` and `components/hub-gateway/`. This is the lab analogue to ROSA ALB plus private connectivity into factory networks — same OpenShift routes and policies, different underlay.

Observe `HTTPRoute` resources and Skupper status in the console; module 13 deploys IE apps that become reachable through this mesh. Understanding this layer explains why Kuadrant policies attach at the hub gateway in module 20.""",
        "es": """La arquitectura hybrid mesh conecta redes de aplicación entre clusters sin aplanar VPCs ni exponer endpoints kube-apiserver públicamente. Red Hat Service Interconnect (Skupper) con HTTPRoutes Gateway API en el hub crea una red lógica de aplicación: frontends en el hub enrutan a servicios spoke por enlaces cifrados.

En este taller, el gateway del hub termina tráfico externo y reenvía a frontends Industrial Edge en east/west vía Sites y Connectors Skupper en `components/service-interconnect/` y `components/hub-gateway/`. Es el análogo lab a ALB ROSA más conectividad privada a redes de fábrica — mismas rutas y políticas OpenShift, distinto underlay.

Observa recursos `HTTPRoute` y estado Skupper en la consola; el módulo 13 despliega apps IE alcanzables por esta malla. Entender esta capa explica por qué las políticas Kuadrant se adjuntan en el gateway del hub en el módulo 20.""",
    },
    "software-templates": {
        "en": """Red Hat Developer Hub software templates encode golden paths: parameterized scaffolder actions create Git repos, register catalog entities, and trigger Argo CD Applications with guardrails (namespaces, quotas, network policies) already wired. Platform teams publish templates once; developers self-serve through the Create flow without opening infrastructure tickets.

This workshop ships templates for Industrial Edge, Camel Kaoto, API products, OpenShift AI workspaces, CNV VMs, and NeuroFace. If your `%USER_NAME%` scaffold fails due to quota or Gitea timing, switch to Plan B — Developer Hub System `hybrid-mesh-shared-demos` exposes pre-deployed Components with the same URLs and Topology entries.

Templates are the bridge between executive strategy (module 01) and spoke deployments (module 13). Inspect `docs/assets/backstage/software-templates/` and catalog ConfigMaps to see how OpenShift GitOps picks up generated repos automatically.""",
        "es": """Las plantillas software de Red Hat Developer Hub codifican golden paths: acciones scaffolder parametrizadas crean repos Git, registran entidades de catálogo y disparan Applications Argo CD con guardrails (namespaces, quotas, network policies) ya cableados. Los equipos de plataforma publican plantillas una vez; los desarrolladores se autoatienden vía Create sin tickets de infraestructura.

Este taller incluye plantillas para Industrial Edge, Camel Kaoto, API products, workspaces OpenShift AI, VMs CNV y NeuroFace. Si el scaffold de `%USER_NAME%` falla por quota o timing de Gitea, cambia a Plan B — Developer Hub System `hybrid-mesh-shared-demos` expone Components pre-desplegados con las mismas URLs y entradas Topology.

Las plantillas son el puente entre estrategia ejecutiva (módulo 01) y despliegues spoke (módulo 13). Inspecciona `docs/assets/backstage/software-templates/` y ConfigMaps de catálogo para ver cómo OpenShift GitOps recoge repos generados automáticamente.""",
    },
    "deploy-industrial-edge": {
        "en": """Industrial Edge on OpenShift combines event streaming, integration, and visualization for factory and IoT scenarios. Apache Kafka buffers high-volume sensor topics; Camel K integrations transform and route events; line-dashboard provides operators a live view — all deployed via GitOps to spoke clusters after Developer Hub scaffolding.

Run the Industrial Edge template as `%USER_NAME%` and confirm your Gitea organization `ws-%USER_NAME%` contains the generated repository. Argo CD on east syncs the Application into namespace `industrial-edge-tst-all` (or your user-scoped equivalent). Plan B demo `demo-industrial-edge-east` offers the same topology if scaffolding is skipped.

This module is the operational heart of Part B: later observability, scaling, network policy, anomaly detection, and AI modules all assume IE workloads are running on your spoke. Verify the line-dashboard route and Kafka topics before proceeding to Kairos scaling.""",
        "es": """Industrial Edge en OpenShift combina streaming de eventos, integración y visualización para escenarios de fábrica e IoT. Apache Kafka bufferiza topics de sensores de alto volumen; integraciones Camel K transforman y enrutan eventos; line-dashboard ofrece vista en vivo a operadores — todo desplegado vía GitOps a spokes tras scaffolding Developer Hub.

Ejecuta la plantilla Industrial Edge como `%USER_NAME%` y confirma que tu organización Gitea `ws-%USER_NAME%` contiene el repositorio generado. Argo CD en east sincroniza la Application al namespace `industrial-edge-tst-all` (o equivalente con alcance de usuario). El demo Plan B `demo-industrial-edge-east` ofrece la misma topología si se omite scaffolding.

Este módulo es el corazón operativo de la Parte B: observabilidad, escalado, network policy, detección de anomalías e IA posteriores asumen cargas IE en tu spoke. Verifica la ruta line-dashboard y topics Kafka antes de continuar a escalado Kairos.""",
    },
    "kairos-scaling": {
        "en": """Kairos Community on OpenShift analyzes workload metrics and recommends node or machine set adjustments through SmartScalingPolicy resources — bridging the gap between Kubernetes HPA (pod-level) and infrastructure provisioning (cluster-level). Operators approve recommendations in Kairos Console, preserving human oversight for factory edge sites where sudden scale-down is risky.

In this lab, the sensor-scan policy watches Industrial Edge metrics and proposes scaling when scan rates spike — analogous to ROSA MachineSet autoscaling triggered by custom CloudWatch metrics. Pair this module with module 18 (HPA + Kafka) to show two layers: pods scale horizontally while Kairos evaluates node capacity.

Open Kairos Console from the OpenShift menu, locate pending recommendations tied to `%USER_NAME%` namespaces, and approve or discuss trade-offs with the facilitator. Run `oc get smartscalingpolicy -A` to correlate CRDs with UI actions.""",
        "es": """Kairos Community en OpenShift analiza métricas de cargas y recomienda ajustes de nodos o machine sets vía SmartScalingPolicy — cerrando la brecha entre HPA Kubernetes (nivel pod) y aprovisionamiento de infraestructura (nivel cluster). Los operadores aprueban recomendaciones en Kairos Console, preservando supervisión humana en edge de fábrica donde un scale-down brusco es riesgoso.

En este lab, la política sensor-scan observa métricas Industrial Edge y propone escalado cuando las tasas de scan disparan — análogo a autoscaling MachineSet ROSA por métricas CloudWatch custom. Combina este módulo con el 18 (HPA + Kafka) para mostrar dos capas: pods escalan horizontalmente mientras Kairos evalúa capacidad de nodos.

Abre Kairos Console desde el menú OpenShift, localiza recomendaciones pendientes en namespaces de `%USER_NAME%` y aprueba o debate trade-offs con el facilitador. Ejecuta `oc get smartscalingpolicy -A` para correlacionar CRDs con acciones UI.""",
    },
    "observability": {
        "en": """OpenShift observability spans cluster metrics, logs, traces, and custom dashboards federated across ACM-managed clusters. Red Hat builds on Prometheus, Loki or Elasticsearch patterns, Grafana, and OpenTelemetry Instrumentation CRs so application teams inherit platform-wide collectors without sidecar sprawl on every pod.

This workshop deploys multicluster Grafana dashboards on the hub, OpenTelemetry collectors via `components/opentelemetry/`, and Kafka Console for IE topic inspection. As `%USER_NAME%`, filter dashboards to your namespace and correlate latency spikes with mesh traces in module 17.

Executives should connect this module to module 21 (Kubecost): metrics prove SLO compliance while cost metrics prove efficiency — both required for hybrid FinOps. Use Showroom `oc` to list `GrafanaDashboard` CRs and confirm IE workloads emit scrape targets.""",
        "es": """La observabilidad OpenShift abarca métricas de cluster, logs, trazas y dashboards custom federados en clusters gestionados por ACM. Red Hat se apoya en Prometheus, patrones Loki o Elasticsearch, Grafana e Instrumentation CRs OpenTelemetry para que equipos de aplicación hereden collectors de plataforma sin sidecar sprawl en cada pod.

Este taller despliega dashboards Grafana multicluster en el hub, collectors OpenTelemetry vía `components/opentelemetry/` y Kafka Console para inspección de topics IE. Como `%USER_NAME%`, filtra dashboards a tu namespace y correlaciona picos de latencia con trazas mesh en el módulo 17.

Los ejecutivos deben conectar este módulo con el 21 (Kubecost): métricas demuestran cumplimiento SLO mientras métricas de costo demuestran eficiencia — ambos requeridos para FinOps híbrido. Usa `oc` en Showroom para listar CRs `GrafanaDashboard` y confirmar que cargas IE emiten targets de scrape.""",
    },
    "openshift-gitops": {
        "en": """OpenShift GitOps installs Argo CD as a managed operator and integrates with ACM ApplicationSets to propagate manifests hub-to-spoke with policy-safe destinations. Platform teams commit desired state to Git; controllers reconcile drift — the same GitOps discipline ROSA customers use when pairing ROSA clusters with ACM hub repositories.

In this lab, hub Applications under `templates/component-applications.yaml` deploy shared services while spoke Applications (for example Industrial Edge) sync from user Gitea repos created in module 13. ApplicationSet `industrial-edge-spoke` demonstrates matrix generators targeting east/west labels.

Inspect sync status in Argo CD UI as `%USER_NAME%` and identify which repo revision triggered your deployment. GitOps is the operational backbone: every product module (mesh, ACS, AI) ultimately resolves to tracked YAML in `platform-hub-spoke-config`.""",
        "es": """OpenShift GitOps instala Argo CD como operador gestionado e integra con ApplicationSets ACM para propagar manifiestos hub-to-spoke con destinos seguros por política. Los equipos de plataforma commitean estado deseado a Git; controladores reconcilian drift — la misma disciplina GitOps que clientes ROSA usan al combinar clusters ROSA con repos hub ACM.

En este lab, Applications hub bajo `templates/component-applications.yaml` despliegan servicios compartidos mientras Applications spoke (por ejemplo Industrial Edge) sincronizan desde repos Gitea de usuario creados en el módulo 13. ApplicationSet `industrial-edge-spoke` demuestra generadores matrix apuntando a labels east/west.

Inspecciona estado de sync en UI Argo CD como `%USER_NAME%` e identifica qué revisión de repo disparó tu despliegue. GitOps es la columna operativa: cada módulo de producto (mesh, ACS, IA) resuelve en YAML rastreado en `platform-hub-spoke-config`.""",
    },
    "service-mesh": {
        "en": """OpenShift Service Mesh 3 introduces ambient mode: a shared ztunnel layer handles mTLS and L4 telemetry without injecting sidecars into every workload pod by default. Kiali visualizes traffic graphs; mesh config enables distributed tracing for Industrial Edge microservices traversing east spoke namespaces.

In this workshop, OSSM3 is subscribed via `components/operators/templates/servicemeshoperator3.yaml` and configured for ambient dataplane mode on IE namespaces — excluding `stackrox` where ACS requires direct network visibility. Compare this to ROSA deployments using App Mesh or third-party meshes: OpenShift keeps mesh CRDs and policies native to the platform lifecycle.

Use Kiali from the OpenShift console to view live traffic for `%USER_NAME%` deployments and validate mTLS between line-dashboard and Kafka-facing services. Module 17 pairs with observability dashboards from module 15 for end-to-end latency analysis.""",
        "es": """OpenShift Service Mesh 3 introduce modo ambient: una capa ztunnel compartida maneja mTLS y telemetría L4 sin inyectar sidecars en cada pod por defecto. Kiali visualiza grafos de tráfico; la config mesh habilita trazas distribuidas para microservicios Industrial Edge en namespaces spoke east.

En este taller, OSSM3 se suscribe vía `components/operators/templates/servicemeshoperator3.yaml` y se configura en modo dataplane ambient en namespaces IE — excluyendo `stackrox` donde ACS requiere visibilidad de red directa. Compara con despliegues ROSA usando App Mesh o meshes de terceros: OpenShift mantiene CRDs y políticas mesh nativas al ciclo de vida de plataforma.

Usa Kiali desde la consola OpenShift para ver tráfico en vivo de despliegues de `%USER_NAME%` y validar mTLS entre line-dashboard y servicios orientados a Kafka. El módulo 17 combina con dashboards de observabilidad del módulo 15 para análisis de latencia end-to-end.""",
    },
    "scalability": {
        "en": """Scalability on OpenShift spans horizontal pod autoscaling, Kafka partition scaling, and node-level recommendations from Kairos. HPA v2 watches CPU, memory, or custom metrics from Prometheus adapters; KafkaNodePool resources expand broker capacity when IE topics saturate consumer lag.

In this lab, line-dashboard and related IE deployments include HPAs defined in workload manifests under `components/industrial-edge-tst/`. Trigger load via workshop scripts or simulated sensor rates, then watch pods scale in the Topology view as `%USER_NAME%`. Kafka scaling complements HPA by absorbing event bursts before pods reject traffic.

This module completes the capacity story started in module 14: Kairos proposes nodes, HPA adds pods, Kafka buffers events — together they mirror how a ROSA customer scales factory edge during production peaks without manual cluster admin intervention.""",
        "es": """La escalabilidad en OpenShift abarca autoscaling horizontal de pods, escalado de particiones Kafka y recomendaciones a nivel nodo de Kairos. HPA v2 observa CPU, memoria o métricas custom de adaptadores Prometheus; KafkaNodePool expande capacidad de brokers cuando topics IE saturan lag de consumidores.

En este lab, line-dashboard y despliegues IE relacionados incluyen HPAs en manifiestos bajo `components/industrial-edge-tst/`. Dispara carga vía scripts del taller o tasas simuladas de sensores, luego observa pods escalar en Topology como `%USER_NAME%`. El escalado Kafka complementa HPA absorbiendo ráfagas de eventos antes de que pods rechacen tráfico.

Este módulo completa la historia de capacidad iniciada en el módulo 14: Kairos propone nodos, HPA añade pods, Kafka bufferiza eventos — juntos reflejan cómo un cliente ROSA escala edge de fábrica en picos de producción sin intervención manual del admin de cluster.""",
    },
    "network-policies": {
        "en": """Kubernetes NetworkPolicy on OpenShift OVN enforces micro-segmentation: only labeled pods and namespaces you explicitly allow can communicate — essential for zero-trust factory networks where compromised sensors must not lateral-move to MES backends. Red Hat OpenShift ships OVN-Kubernetes as the default CNI with policy-aware routing.

This workshop applies a demo NetworkPolicy in `industrial-edge-tst-all` from `components/workshop-demos/templates/network-policy-demo.yaml`, allowing dashboard ingress while denying unexpected cross-namespace traffic. As `%USER_NAME%`, test allowed and denied paths using `oc exec` curl probes from the Showroom terminal.

Compare to ROSA security groups plus Kubernetes NP: defense in depth at cloud VPC and pod layers. Pair this module with ACS (module 20) for runtime anomaly detection when policies are misconfigured or bypassed.""",
        "es": """NetworkPolicy Kubernetes en OpenShift OVN aplica micro-segmentación: solo pods y namespaces etiquetados que permitas explícitamente pueden comunicarse — esencial en redes zero-trust de fábrica donde sensores comprometidos no deben moverse lateralmente a backends MES. Red Hat OpenShift incluye OVN-Kubernetes como CNI por defecto con enrutamiento consciente de políticas.

Este taller aplica una NetworkPolicy demo en `industrial-edge-tst-all` desde `components/workshop-demos/templates/network-policy-demo.yaml`, permitiendo ingress al dashboard mientras niega tráfico cross-namespace inesperado. Como `%USER_NAME%`, prueba rutas permitidas y denegadas con probes curl `oc exec` desde la terminal Showroom.

Compara con security groups ROSA más NP Kubernetes: defensa en profundidad en VPC cloud y capas pod. Combina este módulo con ACS (módulo 20) para detección runtime de anomalías cuando políticas están mal configuradas o bypassed.""",
    },
    "acs-kuadrant": {
        "en": """Red Hat Advanced Cluster Security provides vulnerability scanning, compliance benchmarks, and runtime threat detection across ACM-managed clusters. SecuredCluster agents on spokes report to ACS Central on the hub; init bundles sync via GitOps jobs in `components/acs-init-bundle-sync/`.

Connectivity Link and Kuadrant extend API management to the hub gateway: AuthPolicy validates tokens, RateLimitPolicy protects backends, and APIProduct publishes Industrial Edge APIs for external consumers. Demo `demo-ie-api-product` in Plan B catalog exposes the same Kuadrant resources without scaffolding.

As `%USER_NAME%`, verify ACS sees your spoke workloads and test APIProduct routes through the hub gateway. Remember ACS runs outside ambient mesh — this coexistence pattern is deliberate and matches production ROSA + ACS deployments.""",
        "es": """Red Hat Advanced Cluster Security ofrece escaneo de vulnerabilidades, benchmarks de cumplimiento y detección de amenazas runtime en clusters gestionados por ACM. Agentes SecuredCluster en spokes reportan a ACS Central en el hub; init bundles sincronizan vía jobs GitOps en `components/acs-init-bundle-sync/`.

Connectivity Link y Kuadrant extienden gestión de APIs al gateway del hub: AuthPolicy valida tokens, RateLimitPolicy protege backends y APIProduct publica APIs Industrial Edge para consumidores externos. El demo `demo-ie-api-product` en catálogo Plan B expone los mismos recursos Kuadrant sin scaffolding.

Como `%USER_NAME%`, verifica que ACS ve tus cargas spoke y prueba rutas APIProduct vía gateway del hub. Recuerda que ACS corre fuera del mesh ambient — este patrón de coexistencia es deliberado y coincide con despliegues ROSA + ACS en producción.""",
    },
    "finops-kubecost": {
        "en": """Kubecost on OpenShift allocates Kubernetes spend by namespace, label, and cluster — federating data from hub primary and spoke agents into MinIO-backed ETL storage. Platform teams charge back factory edge tenants and compare ROSA node costs versus on-prem depreciation using consistent Kubernetes unit economics.

In this lab, Kubecost deploys from `components/kubecost/` with agents on east/west reporting to the hub primary. Filter allocations to namespaces owned by `%USER_NAME%` and correlate idle capacity with Kairos recommendations from module 14.

FinOps closes the executive loop from module 01: hybrid strategy without cost visibility fails in CFO review. Kubecost complements AWS Cost Explorer tags on ROSA by exposing pod-level waste inside the cluster boundary.""",
        "es": """Kubecost en OpenShift asigna gasto Kubernetes por namespace, label y cluster — federando datos del primario hub y agentes spoke en almacenamiento ETL respaldado por MinIO. Los equipos de plataforma cargan back tenants edge de fábrica y comparan costos de nodos ROSA versus depreciación on-prem con economía unitaria Kubernetes consistente.

En este lab, Kubecost se despliega desde `components/kubecost/` con agentes en east/west reportando al primario hub. Filtra asignaciones a namespaces de `%USER_NAME%` y correlaciona capacidad ociosa con recomendaciones Kairos del módulo 14.

FinOps cierra el loop ejecutivo del módulo 01: estrategia híbrida sin visibilidad de costo falla en revisión CFO. Kubecost complementa tags AWS Cost Explorer en ROSA exponiendo desperdicio a nivel pod dentro del límite del cluster.""",
    },
    "openshift-ai": {
        "en": """OpenShift AI on the hub runs **ModelMesh + Serverless (Knative)** via `default-dsc`. Each user owns project **`ai-%USER_NAME%`** with pre-provisioned **Jupyter notebook** `workshop-notebook`, MaaS secret, and Developer Hub catalog entity.

**Overview-only (~10 min):** Catalog → **OpenShift AI — %USER_NAME%** → open dashboard; show Playground in `maas-workshop` (do not run notebook).

**Hands-on (~30 min):** Launch **workshop-notebook**, run `maas-smoke-test.ipynb`, open **AI Assistants → MCP Servers** and add `ods-maas-mcp-server` URL from ConfigMap `ods-mcp-server-registration`. In **ai-%USER_NAME%** → **Models**, confirm **`workshop-sklearn`** InferenceService (ModelMesh) is Ready; test predict from dashboard or `curl` the internal predictor URL.

GitOps: `components/openshift-ai-hub/` (`user-projects.yaml`, `dashboard-config.yaml`, `ods-mcp-server.yaml`). Verify: `oc get notebook,inferenceservice -n ai-%USER_NAME%`.""",
        "es": """OpenShift AI en el hub ejecuta **ModelMesh + Serverless (Knative)** vía `default-dsc`. Cada usuario tiene **`ai-%USER_NAME%`** con **notebook Jupyter** `workshop-notebook`, secret MaaS y entidad en Developer Hub.

**Solo visualización (~10 min):** Catálogo → **OpenShift AI — %USER_NAME%**; mostrar Playground en `maas-workshop`.

**Hands-on (~30 min):** Abrir **workshop-notebook**, ejecutar `maas-smoke-test.ipynb`, registrar **MCP Server** `ods-maas-mcp-server` en extensiones OpenShift AI. En **ai-%USER_NAME%** → **Models**, confirmar **`workshop-sklearn`** (ModelMesh) Ready y probar inferencia.

GitOps: `components/openshift-ai-hub/`. Verificar: `oc get notebook,inferenceservice -n ai-%USER_NAME%`.""",
    },
    "ai-gateway": {
        "en": """The **AI Gateway** (`workshop-apis.%HUB_DOMAIN%`) fronts external MaaS with **Gateway API HTTPRoute**, Istio hub gateway, and **Kuadrant** (`AuthPolicy`, `TokenRateLimitPolicy`, API keys). GitOps: `components/workshop-kuadrant-apis/templates/routes.yaml` + `policies.yaml`.

**Overview-only (~5 min):** Catalog → **workshop-ai-gateway**; Kuadrant UI → show API key shape.

**Hands-on (~25 min):** Mint key for `%USER_NAME%`, `curl -H "Authorization: Bearer $KEY" https://workshop-apis.%HUB_DOMAIN%/llm/v1/chat/completions` with JSON body; compare to direct MaaS from notebook.""",
        "es": """El **AI Gateway** (`workshop-apis.%HUB_DOMAIN%`) expone MaaS externo con **Gateway API**, Istio y **Kuadrant**. GitOps: `components/workshop-kuadrant-apis/`.

**Solo visualización (~5 min):** Catálogo → **workshop-ai-gateway**; UI Kuadrant.

**Hands-on (~25 min):** Crear API key, `curl` a `/llm/v1/chat/completions`, comparar con MaaS directo.""",
    },
    "mcp-gateway": {
        "en": """**MCP Gateway** deploys Kuadrant community CRDs (`MCPGatewayExtension`, `MCPServerRegistration`), `mcp-controller`, Gateway API `Gateway`, **ArgoCD MCP**, and **k8s MCP** — pattern from test-drive-pe-oscg. Public URL: `https://mcp-gateway.%HUB_DOMAIN%/mcp`.

**Overview-only (~8 min):** Catalog → **workshop-mcp-gateway**; `oc get mcpserverregistration -n mcp-system`; Lightspeed demo prompt.

**Hands-on (~30 min):** Developer Hub **/lightspeed** — activity: "List Argo CD apps in OutOfSync state and suggest sync." Llama-stack uses `remote::mcp` to gateway (`components/developer-hub/files/lightspeed/llama-stack-run.yaml`).""",
        "es": """**MCP Gateway** despliega CRDs Kuadrant, controlador, Gateway API, **ArgoCD MCP** y **k8s MCP** — patrón test-drive-pe-oscg. URL: `https://mcp-gateway.%HUB_DOMAIN%/mcp`.

**Solo visualización (~8 min):** Catálogo → **workshop-mcp-gateway**; demo Lightspeed.

**Hands-on (~30 min):** **/lightspeed** — actividad: listar apps Argo CD OutOfSync y proponer sync.""",
    },
    "llm-rag": {
        "en": """Large language models and retrieval-augmented generation (RAG) on OpenShift combine centralized inference with domain-specific context from factory docs, runbooks, and sensor logs — without exporting proprietary data to public SaaS. Red Hat Developer Hub Lightspeed assists developers in-catalog; Kairos Console agents answer scaling questions; Continue AI in DevSpaces suggests code inline using the same MaaS backend.

RAG architecture in hybrid manufacturing typically indexes PDFs and SOPs into a vector store (customer choice) while the LLM runs on OpenShift AI ModelMesh or external MaaS. In this lab, you configure Lightspeed deployment in `components/developer-hub/templates/lightspeed.yaml` and test prompts against the shared MaaS endpoint — observe latency and token usage suitable for shop-floor Wi-Fi constraints.

As `%USER_NAME%`, open Developer Hub, trigger Lightspeed on a catalog Component, and compare responses with Continue AI in a DevSpaces workspace. Module 25 extends the same MaaS path to multimodal NeuroFace chat — proving one governance model serves dev, ops, and end-user AI surfaces.""",
        "es": """Los modelos de lenguaje grande y RAG (retrieval-augmented generation) en OpenShift combinan inferencia centralizada con contexto de dominio desde docs de fábrica, runbooks y logs de sensores — sin exportar datos propietarios a SaaS público. Red Hat Developer Hub Lightspeed asiste desarrolladores en catálogo; agentes Kairos Console responden preguntas de escalado; Continue AI en DevSpaces sugiere código inline usando el mismo backend MaaS.

La arquitectura RAG en manufactura híbrida típicamente indexa PDFs y SOPs en un vector store (elección del cliente) mientras el LLM corre en OpenShift AI ModelMesh o MaaS externo. En este lab, configuras el despliegue Lightspeed en `components/developer-hub/templates/lightspeed.yaml` y pruebas prompts contra el endpoint MaaS compartido — observa latencia y uso de tokens adecuados para restricciones Wi-Fi de planta.

Como `%USER_NAME%`, abre Developer Hub, dispara Lightspeed en un Component de catálogo y compara respuestas con Continue AI en un workspace DevSpaces. El módulo 25 extiende la misma ruta MaaS a chat multimodal NeuroFace — demostrando un modelo de gobernanza para superficies IA de dev, ops y usuario final.""",
    },
    "text-ai-predictive": {
        "en": """Generative AI assists operators with natural-language summaries of alarms; predictive AI forecasts failures before downtime. On OpenShift, the ie-anomaly-alerter deployment watches Prometheus metrics from Industrial Edge sensors and emits alerts when statistical thresholds breach — a lightweight predictive pattern without mandatory KServe for this workshop track.

Optional KServe InferenceService resources on the hub demonstrate full model serving for custom scikit-learn or ONNX models trained in DS workspaces. MaaS playground endpoints let `%USER_NAME%` test generative prompts for incident postmortems: "Summarize last hour Kafka lag and ACS violations for my namespace."

Connect predictive alerts to module 26 end-user apps: Camel routes can fan out anomaly events to line-dashboard overlays and NeuroFace notifications. This closes the loop from telemetry → ML/statistical detection → human + generative AI response on the same OpenShift footprint.""",
        "es": """La IA generativa asiste operadores con resúmenes en lenguaje natural de alarmas; la IA predictiva pronostica fallos antes del downtime. En OpenShift, el despliegue ie-anomaly-alerter observa métricas Prometheus de sensores Industrial Edge y emite alertas cuando umbrales estadísticos se violan — un patrón predictivo ligero sin KServe obligatorio en esta pista del taller.

Recursos opcionales KServe InferenceService en el hub demuestran model serving completo para modelos scikit-learn u ONNX entrenados en workspaces DS. Endpoints playground MaaS permiten a `%USER_NAME%` probar prompts generativos para postmortems de incidentes: "Resume lag Kafka y violaciones ACS de la última hora para mi namespace."

Conecta alertas predictivas al módulo 26 de apps finales: rutas Camel pueden distribuir eventos de anomalía a overlays line-dashboard y notificaciones NeuroFace. Esto cierra el loop telemetría → detección ML/estadística → respuesta humana + IA generativa en el mismo footprint OpenShift.""",
    },
    "neuroface": {
        "en": """NeuroFace combines **OVMS local vision** (face/object detection via `components/neuroface/` with `ovms.enabled: true`) and **MaaS chat** at `/api/chat`. Hub **ModelMesh** serves platform models; NeuroFace OVMS handles low-latency webcam inference on the app namespace.

**Overview-only (~10 min):** Developer Hub → **neuroface-workshop** → Topology; open UI without webcam.

**Hands-on (~30 min):** Register as `%USER_NAME%`, test webcam + chat, inspect OVMS Service/route in namespace `neuroface`.

Catalog: System `hybrid-mesh-ai-platform` → Component **neuroface-workshop** (links UI + OpenShift AI dashboard).""",
        "es": """NeuroFace combina **visión OVMS local** (`ovms.enabled: true`) y **chat MaaS** en `/api/chat`. **ModelMesh** en el hub sirve modelos de plataforma; OVMS NeuroFace maneja inferencia webcam de baja latencia.

**Solo visualización (~10 min):** Developer Hub → **neuroface-workshop** → Topology.

**Hands-on (~30 min):** Probar webcam + chat; inspeccionar Service OVMS en namespace `neuroface`.""",
    },
    "ai-end-user-apps": {
        "en": """End-user applications — operator dashboards, mobile alerts, MES integrations — consume AI insights where work happens, not only in data science notebooks. line-dashboard on the east spoke visualizes Kafka sensor streams; Camel integrations route anomaly events; NeuroFace and MaaS summaries embed into the same UX `%USER_NAME%` sees in production rollouts.

This module integrates modules 13–25: verify line-dashboard displays live IE data, trigger ie-anomaly-alerter thresholds, and optionally embed a NeuroFace iframe or chat link for contextual AI help. Camel K Integrations from templates `demo-camel-kaoto-east` and `demo-camel-cdc-east` show event-driven patterns factory teams deploy on OpenShift alongside OT systems.

Platform teams win when AI is invisible infrastructure: OpenShift AI, MaaS, and NeuroFace become services catalog entries — app squads bind them through Developer Hub dependencies without rebuilding ML pipelines per plant.""",
        "es": """Las aplicaciones finales — dashboards de operador, alertas móviles, integraciones MES — consumen insights de IA donde ocurre el trabajo, no solo en notebooks de data science. line-dashboard en spoke east visualiza streams Kafka de sensores; integraciones Camel enrutan eventos de anomalía; NeuroFace y resúmenes MaaS se embeben en la misma UX que `%USER_NAME%` ve en rollouts de producción.

Este módulo integra módulos 13–25: verifica que line-dashboard muestra datos IE en vivo, dispara umbrales ie-anomaly-alerter y opcionalmente embebe iframe NeuroFace o enlace chat para ayuda IA contextual. Integraciones Camel K de plantillas `demo-camel-kaoto-east` y `demo-camel-cdc-east` muestran patrones event-driven que equipos de fábrica despliegan en OpenShift junto a sistemas OT.

Los equipos de plataforma ganan cuando la IA es infraestructura invisible: OpenShift AI, MaaS y NeuroFace son entradas de catálogo — squads de app los vinculan vía dependencias Developer Hub sin reconstruir pipelines ML por planta.""",
    },
    "full-verification": {
        "en": """Full stack verification confirms Part A narrative comprehension and Part B hands-on outcomes for `%USER_NAME%`: registration redirect, Showroom terminal `oc`, ACM spoke visibility, IE sync, Kubecost allocations, DSC Ready, NeuroFace health, and progress API persistence.

Run `bash scripts/verify-workshop-e2e.sh` from the repo or follow the checklist in `verification/progress-checklist.yaml`. The workshop registration service at `https://workshop-registration.%HUB_DOMAIN%` and Showroom progress endpoint (`POST /api/progress`) must accept your module completions — facilitators use aggregate progress to pace the room.

Treat this module as your graduation gate: if any check fails, revisit the linked module or switch to Plan B shared demos documented in Developer Hub System `hybrid-mesh-shared-demos`.""",
        "es": """La verificación full stack confirma comprensión narrativa Parte A y resultados hands-on Parte B para `%USER_NAME%`: redirect de registro, terminal Showroom `oc`, visibilidad spoke ACM, sync IE, asignaciones Kubecost, DSC Ready, salud NeuroFace y persistencia API de progreso.

Ejecuta `bash scripts/verify-workshop-e2e.sh` desde el repo o sigue el checklist en `verification/progress-checklist.yaml`. El servicio de registro en `https://workshop-registration.%HUB_DOMAIN%` y el endpoint de progreso Showroom (`POST /api/progress`) deben aceptar tus completados de módulo — facilitadores usan progreso agregado para marcar ritmo de sala.

Trata este módulo como puerta de graduación: si algún check falla, revisita el módulo enlazado o cambia a demos compartidos Plan B documentados en Developer Hub System `hybrid-mesh-shared-demos`.""",
    },
    "agent-browser-recording": {
        "en": """Agent Browser automations in `verification/agent-browser/` replay workshop flows for CI-style smoke testing — navigating Developer Hub, ACM, and NeuroFace without manual clicks. Recordings support facilitator dry-runs and post-event highlights but are intentionally gitignored (`*.mp4`) per `verification/recording-runbook.md`.

Use Win+G or OBS locally to capture demos; never commit MP4 assets to `platform-hub-spoke-config`. Agent Browser YAML scripts document expected selectors and URLs with `%HUB_DOMAIN%` placeholders for forked environments.

As `%USER_NAME%`, optionally execute a read-only Agent Browser script against your assigned namespaces to validate UI regressions before executive sessions. This module closes the workshop loop: human learners, automated verification, and reproducible demo capture on OpenShift.""",
        "es": """Las automatizaciones Agent Browser en `verification/agent-browser/` reproducen flujos del taller para smoke testing estilo CI — navegando Developer Hub, ACM y NeuroFace sin clicks manuales. Las grabaciones apoyan dry-runs de facilitadores y highlights post-evento pero están intencionalmente en gitignore (`*.mp4`) según `verification/recording-runbook.md`.

Usa Win+G u OBS localmente para capturar demos; nunca commitees assets MP4 a `platform-hub-spoke-config`. Scripts YAML Agent Browser documentan selectores y URLs esperados con placeholders `%HUB_DOMAIN%` para entornos forked.

Como `%USER_NAME%`, opcionalmente ejecuta un script Agent Browser read-only contra tus namespaces asignados para validar regresiones UI antes de sesiones ejecutivas. Este módulo cierra el loop del taller: aprendices humanos, verificación automatizada y captura de demo reproducible en OpenShift.""",
    },
}

SHOW_TELL_EN: dict[str, str] = {
    "index": """. Walk the dual agenda: Part A strategy (01–05) then Part B hands-on (10–28).
. Demo registration flow at `https://workshop-registration.%HUB_DOMAIN%` and Showroom redirect.
. Point to Plan B shared demos in Developer Hub System `hybrid-mesh-shared-demos`.""",
    "hybrid-cloud-strategy": """. Frame the four strategic pillars: modernize, secure, automate, monetize AI on OpenShift.
. Map each pillar to a Part B module number on the agenda table.
. Ask attendees their current hybrid split (ROSA vs on-prem vs edge).""",
    "rosa-architecture": """. Whiteboard ROSA control plane vs worker responsibility split.
. Show ACM ManagedCluster list as the lab equivalent of joining ROSA to a fleet hub.
. Mention SLA and support boundaries Red Hat vs customer ops.""",
    "security-scale-hybrid": """. Highlight ACS + mesh coexistence (`stackrox` without ambient labels).
. Preview NetworkPolicy (19) and Kuadrant (20) as defense layers.
. Discuss factory edge scale events and Kairos approval workflow.""",
    "aws-ai-integration": """. Contrast Bedrock/SageMaker with OpenShift AI + MaaS in this lab.
. Show MaaS credential secret location conceptually (no secret values).
. Explain portable inference when AWS residency or pricing changes.""",
    "cases-roadmap": """. Present the automotive IoT case metrics (12k events/min, $47k/hr downtime, 34% node savings).
. Draw the customer roadmap timeline onto workshop module numbers.
. Transition room to Part B: verify `%USER_NAME%` login before module 10.""",
    "acm-multicluster": """. Open ACM Clusters UI — identify east and west spokes.
. Run `oc get managedclusters` in Showroom terminal live.
. Show Developer Hub Topology mirroring OCM graph.""",
    "hybrid-mesh-architecture": """. Trace external URL → hub HTTPRoute → Skupper → spoke IE frontend.
. Display Skupper site/connector status in console.
. Relate to ROSA ALB + private link narrative from Part A.""",
    "software-templates": """. Live Developer Hub Create flow for Industrial Edge template.
. Show catalog YAML source and generated Gitea repo URL pattern.
. Demonstrate Plan B fallback entity in `hybrid-mesh-shared-demos`.""",
    "deploy-industrial-edge": """. Confirm Gitea org `ws-%USER_NAME%` and Argo CD sync on east.
. Open line-dashboard route and Kafka Console topics.
. Offer Plan B `demo-industrial-edge-east` if scaffold fails.""",
    "kairos-scaling": """. Open Kairos Console and walk through a pending SmartScalingPolicy recommendation.
. Correlate UI action with `oc get smartscalingpolicy -A`.
. Discuss human-in-the-loop approval for factory edge.""",
    "observability": """. Open multicluster Grafana dashboard filtered to IE namespace.
. Show Kafka Console and a sample OTEL trace (or metrics gap if trace pending).
. Link metrics SLO story to upcoming Kubecost module.""",
    "openshift-gitops": """. Argo CD UI: hub Application vs user spoke Application sources.
. Highlight ApplicationSet generator for east/west matrix.
. Show sync wave or health status for IE app.""",
    "service-mesh": """. Open Kiali graph for IE namespace — point out ambient ztunnel edges.
. Note `stackrox` exclusion from ambient mesh.
. Optional: show mTLS lock icon on service edges.""",
    "scalability": """. Watch HPA scale line-dashboard pods under simulated load.
. Show Kafka consumer lag recovering after buffer capacity.
. Tie pod-scale (HPA) vs node-scale (Kairos) layering.""",
    "network-policies": """. Apply or review demo NetworkPolicy in `industrial-edge-tst-all`.
. Run allowed vs denied curl from Showroom terminal pods.
. Relate to ROSA security groups + NP defense in depth.""",
    "acs-kuadrant": """. ACS Central overview — violations and deployments on spokes.
. Demo APIProduct route via hub gateway with AuthPolicy.
. Remind ACS namespace stays outside ambient mesh.""",
    "finops-kubecost": """. Kubecost UI: allocation by namespace for `%USER_NAME%`.
. Show federated cluster dropdown (hub + spokes).
. Compare idle cost with Kairos over-provision narrative.""",
    "ai-gateway": """. Catalog → **workshop-ai-gateway** → inspect HTTPRoute in Topology.
. Kuadrant UI: create API key; curl `/llm/v1/chat/completions` with Bearer token.
. Show AuthPolicy + TokenRateLimitPolicy YAML paths in GitOps.""",
    "mcp-gateway": """. `oc get mcpgatewayextension,mcpserverregistration -n mcp-system`.
. Developer Hub `/lightspeed` — prompt: list Argo CD applications.
. OpenShift AI dashboard → register MCP server URL from maas-workshop ConfigMap.""",
    "openshift-ai": """. `oc get dsc` — confirm Ready; open **workshop-notebook** in ai-%USER_NAME%.
. Developer Hub → **OpenShift AI — %USER_NAME%** + **Playground** in maas-workshop.
. Show MCP server deployment `ods-maas-mcp-server` in maas-workshop.""",
    "llm-rag": """. Trigger Developer Hub Lightspeed on a catalog Component live.
. Optional DevSpaces Continue AI inline suggestion using MaaS.
. Discuss RAG index placement (customer choice) vs LLM on OpenShift AI.""",
    "text-ai-predictive": """. Show ie-anomaly-alerter firing on threshold breach in metrics.
. MaaS prompt: generative summary of recent IE alerts.
. Mention optional KServe path for custom models.""",
    "neuroface": """. Open `https://neuroface.%HUB_DOMAIN%` — webcam object detection live.
. Send chat question about detected object; show MaaS backend (not LibreChat).
. Highlight OVMS local vision + centralized chat governance.""",
    "ai-end-user-apps": """. line-dashboard live data + anomaly overlay or alert badge.
. Optional Camel integration status in Topology.
. Story: operator sees telemetry, prediction, and AI help in one UX.""",
    "full-verification": """. Walk checklist items and run verify script excerpt live.
. Confirm progress API save from Showroom checkbox UI.
. Celebrate completion; share Plan B paths for any failed checks.""",
    "agent-browser-recording": """. Show Agent Browser YAML in `verification/agent-browser/` (read-only).
. Review recording-runbook.md — no MP4 in Git policy.
. Optional: run one smoke script headlessly if environment allows.""",
}

SHOW_TELL_ES: dict[str, str] = {
    "index": """. Recorrer agenda dual: Parte A estrategia (01–05) luego Parte B hands-on (10–28).
. Demo flujo de registro en `https://workshop-registration.%HUB_DOMAIN%` y redirect Showroom.
. Señalar demos compartidos Plan B en Developer Hub System `hybrid-mesh-shared-demos`.""",
    "hybrid-cloud-strategy": """. Enmarcar cuatro pilares estratégicos: modernizar, asegurar, automatizar, monetizar IA en OpenShift.
. Mapear cada pilar a un número de módulo Parte B en la tabla agenda.
. Preguntar split híbrido actual de asistentes (ROSA vs on-prem vs edge).""",
    "rosa-architecture": """. Pizarra split plano de control ROSA vs responsabilidad workers.
. Mostrar lista ManagedCluster ACM como equivalente lab de unir ROSA a hub de flota.
. Mencionar límites SLA y soporte Red Hat vs ops cliente.""",
    "security-scale-hybrid": """. Destacar coexistencia ACS + mesh (`stackrox` sin labels ambient).
. Preview NetworkPolicy (19) y Kuadrant (20) como capas de defensa.
. Discutir eventos de escala edge fábrica y workflow aprobación Kairos.""",
    "aws-ai-integration": """. Contrastar Bedrock/SageMaker con OpenShift AI + MaaS en este lab.
. Mostrar ubicación conceptual del secret MaaS (sin valores de secret).
. Explicar inferencia portable cuando cambian residencia o precios AWS.""",
    "cases-roadmap": """. Presentar métricas caso IoT automotriz (12k eventos/min, 47k USD/hr downtime, 34% ahorro nodos).
. Dibujar timeline roadmap cliente sobre números de módulo del taller.
. Transicionar sala a Parte B: verificar login `%USER_NAME%` antes del módulo 10.""",
    "acm-multicluster": """. Abrir UI ACM Clusters — identificar spokes east y west.
. Ejecutar `oc get managedclusters` en terminal Showroom en vivo.
. Mostrar Topology Developer Hub reflejando grafo OCM.""",
    "hybrid-mesh-architecture": """. Trazar URL externa → HTTPRoute hub → Skupper → frontend IE spoke.
. Mostrar estado site/connector Skupper en consola.
. Relacionar con narrativa ALB ROSA + private link de Parte A.""",
    "software-templates": """. Flujo Create Developer Hub en vivo para plantilla Industrial Edge.
. Mostrar fuente YAML catálogo y patrón URL repo Gitea generado.
. Demostrar entidad fallback Plan B en `hybrid-mesh-shared-demos`.""",
    "deploy-industrial-edge": """. Confirmar org Gitea `ws-%USER_NAME%` y sync Argo CD en east.
. Abrir ruta line-dashboard y topics Kafka Console.
. Ofrecer Plan B `demo-industrial-edge-east` si falla scaffold.""",
    "kairos-scaling": """. Abrir Kairos Console y recorrer recomendación SmartScalingPolicy pendiente.
. Correlacionar acción UI con `oc get smartscalingpolicy -A`.
. Discutir aprobación human-in-the-loop para edge de fábrica.""",
    "observability": """. Abrir dashboard Grafana multicluster filtrado a namespace IE.
. Mostrar Kafka Console y traza OTEL de ejemplo (o gap métricas si trace pendiente).
. Enlazar historia SLO métricas al próximo módulo Kubecost.""",
    "openshift-gitops": """. UI Argo CD: Application hub vs fuentes Application spoke usuario.
. Destacar generador ApplicationSet matrix east/west.
. Mostrar sync wave o estado health para app IE.""",
    "service-mesh": """. Abrir grafo Kiali para namespace IE — señalar aristas ztunnel ambient.
. Notar exclusión `stackrox` del mesh ambient.
. Opcional: mostrar icono candado mTLS en aristas de servicio.""",
    "scalability": """. Observar HPA escalar pods line-dashboard bajo carga simulada.
. Mostrar consumer lag Kafka recuperándose tras capacidad buffer.
. Conectar capas pod-scale (HPA) vs node-scale (Kairos).""",
    "network-policies": """. Aplicar o revisar NetworkPolicy demo en `industrial-edge-tst-all`.
. Ejecutar curl permitido vs denegado desde pods terminal Showroom.
. Relacionar con security groups ROSA + NP defensa en profundidad.""",
    "acs-kuadrant": """. Overview ACS Central — violaciones y despliegues en spokes.
. Demo ruta APIProduct vía gateway hub con AuthPolicy.
. Recordar namespace ACS fuera del mesh ambient.""",
    "finops-kubecost": """. UI Kubecost: asignación por namespace para `%USER_NAME%`.
. Mostrar dropdown cluster federado (hub + spokes).
. Comparar costo ocioso con narrativa sobreaprovisión Kairos.""",
    "ai-gateway": """. Catálogo → **workshop-ai-gateway** → HTTPRoute en Topology.
. UI Kuadrant: crear API key; curl `/llm/v1/chat/completions`.
. Mostrar rutas GitOps AuthPolicy + TokenRateLimitPolicy.""",
    "mcp-gateway": """. `oc get mcpgatewayextension,mcpserverregistration -n mcp-system`.
. Developer Hub `/lightspeed` — prompt: listar apps Argo CD.
. Dashboard OpenShift AI → registrar MCP server maas-workshop.""",
    "openshift-ai": """. `oc get dsc` — confirmar Ready; abrir **workshop-notebook** en ai-%USER_NAME%.
. Developer Hub → **OpenShift AI — %USER_NAME%** + **Playground** maas-workshop.
. Mostrar deployment MCP `ods-maas-mcp-server`.""",
    "llm-rag": """. Disparar Developer Hub Lightspeed en Component catálogo en vivo.
. Opcional sugerencia inline Continue AI DevSpaces usando MaaS.
. Discutir ubicación índice RAG (elección cliente) vs LLM en OpenShift AI.""",
    "text-ai-predictive": """. Mostrar ie-anomaly-alerter disparando en violación umbral en métricas.
. Prompt MaaS: resumen generativo de alertas IE recientes.
. Mencionar ruta KServe opcional para modelos custom.""",
    "neuroface": """. Abrir `https://neuroface.%HUB_DOMAIN%` — detección objetos webcam en vivo.
. Enviar pregunta chat sobre objeto detectado; mostrar backend MaaS (no LibreChat).
. Destacar visión local OVMS + gobernanza chat centralizada.""",
    "ai-end-user-apps": """. Datos en vivo line-dashboard + overlay anomalía o badge alerta.
. Opcional estado integración Camel en Topology.
. Historia: operador ve telemetría, predicción y ayuda IA en una UX.""",
    "full-verification": """. Recorrer ítems checklist y ejecutar extracto script verify en vivo.
. Confirmar guardado API progreso desde UI checkbox Showroom.
. Celebrar completado; compartir rutas Plan B para checks fallidos.""",
    "agent-browser-recording": """. Mostrar YAML Agent Browser en `verification/agent-browser/` (read-only).
. Revisar recording-runbook.md — política sin MP4 en Git.
. Opcional: ejecutar un script smoke headless si el entorno lo permite.""",
}

TODO_EN: dict[str, list[str]] = {
    "index": [
        "* [ ] Skim hybrid cloud integration notes (AWS/Azure snippets)",
        "* [ ] Register at link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[workshop registration] and open Showroom",
        "* [ ] Save progress at the end of this module",
    ],
    "hybrid-cloud-strategy": [
        "* [ ] Map your organization's workloads to hub vs spoke vs ROSA placement",
        "* [ ] Identify which Part B module addresses your top priority pillar",
        "* [ ] Save progress at the end of this module",
    ],
    "rosa-architecture": [
        "* [ ] Sketch ROSA control plane vs worker responsibilities for your account",
        "* [ ] Preview ACM ManagedCluster in module 10 reading list",
        "* [ ] Save progress at the end of this module",
    ],
    "security-scale-hybrid": [
        "* [ ] List three security layers you will verify in Part B (ACS, NP, Kuadrant)",
        "* [ ] Note why `stackrox` avoids ambient mesh in this lab",
        "* [ ] Save progress at the end of this module",
    ],
    "aws-ai-integration": [
        "* [ ] Compare your AWS AI services with OpenShift AI + MaaS lab pattern",
        "* [ ] Locate module 22 for hands-on DSC and MaaS setup",
        "* [ ] Save progress at the end of this module",
    ],
    "cases-roadmap": [
        "* [ ] Write one metric from the manufacturing case relevant to your industry",
        "* [ ] Confirm Showroom login as `%USER_NAME%` before module 10",
        "* [ ] Save progress at the end of this module",
    ],
    "acm-multicluster": [
        "* [ ] Run `oc get managedclusters` and identify east/west",
        "* [ ] Open ACM Clusters UI and Developer Hub Topology for the same fleet",
        "* [ ] Save progress at the end of this module",
    ],
    "hybrid-mesh-architecture": [
        "* [ ] Inspect hub HTTPRoute and Skupper resources in console",
        "* [ ] Trace how external traffic reaches IE frontends on spokes",
        "* [ ] Save progress at the end of this module",
    ],
    "software-templates": [
        "* [ ] Browse Developer Hub Create templates list",
        "* [ ] Locate Plan B System `hybrid-mesh-shared-demos` as fallback",
        "* [ ] Save progress at the end of this module",
    ],
    "deploy-industrial-edge": [
        "* [ ] Scaffold IE or open Plan B `demo-industrial-edge-east`",
        "* [ ] Verify Gitea org `ws-%USER_NAME%` and Argo CD sync Healthy",
        "* [ ] Save progress at the end of this module",
    ],
    "kairos-scaling": [
        "* [ ] Open Kairos Console and review one SmartScalingPolicy",
        "* [ ] Run `oc get smartscalingpolicy -A` from Showroom terminal",
        "* [ ] Save progress at the end of this module",
    ],
    "observability": [
        "* [ ] Open a multicluster Grafana dashboard for your IE namespace",
        "* [ ] Inspect Kafka Console topics for sensor data",
        "* [ ] Save progress at the end of this module",
    ],
    "openshift-gitops": [
        "* [ ] Find your IE Application in Argo CD and note sync status",
        "* [ ] Identify Git repo source (user Gitea vs hub platform repo)",
        "* [ ] Save progress at the end of this module",
    ],
    "service-mesh": [
        "* [ ] Open Kiali and view traffic for your IE deployments",
        "* [ ] Confirm ambient mesh enabled on IE namespace (not stackrox)",
        "* [ ] Save progress at the end of this module",
    ],
    "scalability": [
        "* [ ] Check HPA status for line-dashboard or related IE deployment",
        "* [ ] Observe Kafka consumer lag under load or simulated traffic",
        "* [ ] Save progress at the end of this module",
    ],
    "network-policies": [
        "* [ ] Review NetworkPolicy in `industrial-edge-tst-all`",
        "* [ ] Test one allowed and one denied pod-to-pod connection",
        "* [ ] Save progress at the end of this module",
    ],
    "acs-kuadrant": [
        "* [ ] Verify ACS shows your spoke workloads in Central UI",
        "* [ ] Test APIProduct route through hub gateway (or Plan B demo)",
        "* [ ] Save progress at the end of this module",
    ],
    "finops-kubecost": [
        "* [ ] Open Kubecost and filter allocations to your namespace",
        "* [ ] Compare hub vs spoke cluster costs in federated view",
        "* [ ] Save progress at the end of this module",
    ],
    "openshift-ai": [
        "* [ ] Run `oc get dsc` and confirm DataScienceCluster Ready",
        "* [ ] Launch **workshop-notebook** in project `ai-%USER_NAME%` and run MaaS smoke test",
        "* [ ] Open Developer Hub catalog Component **ai-%USER_NAME%**",
        "* [ ] Enable OpenShift AI **Playground** / **MCP Server** extension (maas-workshop)",
        "* [ ] Save progress at the end of this module",
    ],
    "ai-gateway": [
        "* [ ] Open catalog **workshop-ai-gateway** and Kuadrant UI",
        "* [ ] Create API key and call `https://workshop-apis.%HUB_DOMAIN%/llm/v1/chat/completions`",
        "* [ ] Save progress at the end of this module",
    ],
    "mcp-gateway": [
        "* [ ] Verify MCP CRDs and `MCPServerRegistration` in `mcp-system`",
        "* [ ] Lightspeed: list Argo CD apps via MCP gateway tools",
        "* [ ] Register OpenShift AI MCP server in dashboard",
        "* [ ] Save progress at the end of this module",
    ],
    "llm-rag": [
        "* [ ] Trigger Lightspeed in Developer Hub on a catalog entity",
        "* [ ] Send one MaaS prompt and note latency/response quality",
        "* [ ] Save progress at the end of this module",
    ],
    "text-ai-predictive": [
        "* [ ] Confirm ie-anomaly-alerter deployment running on your spoke",
        "* [ ] Generate one alarm summary prompt via MaaS playground",
        "* [ ] Save progress at the end of this module",
    ],
    "neuroface": [
        "* [ ] Open `https://neuroface.%HUB_DOMAIN%` and test webcam detection",
        "* [ ] Ask `/api/chat` one question about a detected object",
        "* [ ] Save progress at the end of this module",
    ],
    "ai-end-user-apps": [
        "* [ ] Verify line-dashboard shows live IE telemetry",
        "* [ ] Connect one anomaly or AI insight to operator workflow",
        "* [ ] Save progress at the end of this module",
    ],
    "full-verification": [
        "* [ ] Complete checklist in `verification/progress-checklist.yaml`",
        "* [ ] Run or review output of `scripts/verify-workshop-e2e.sh`",
        "* [ ] Save progress at the end of this module",
    ],
    "agent-browser-recording": [
        "* [ ] Read `verification/recording-runbook.md` (no MP4 in Git)",
        "* [ ] Browse one Agent Browser YAML under `verification/agent-browser/`",
        "* [ ] Save progress at the end of this module",
    ],
}

TODO_ES: dict[str, list[str]] = {
    "index": [
        "* [ ] Revisar notas de integración nube híbrida (snippets AWS/Azure)",
        "* [ ] Registrarse en link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[registro] y abrir Showroom",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "hybrid-cloud-strategy": [
        "* [ ] Mapear cargas de tu organización a placement hub vs spoke vs ROSA",
        "* [ ] Identificar qué módulo Parte B aborda tu pilar prioritario",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "rosa-architecture": [
        "* [ ] Esbozar responsabilidades plano control ROSA vs workers para tu cuenta",
        "* [ ] Preview ManagedCluster ACM en lectura previa módulo 10",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "security-scale-hybrid": [
        "* [ ] Listar tres capas de seguridad que verificarás en Parte B (ACS, NP, Kuadrant)",
        "* [ ] Anotar por qué `stackrox` evita mesh ambient en este lab",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "aws-ai-integration": [
        "* [ ] Comparar tus servicios IA AWS con patrón lab OpenShift AI + MaaS",
        "* [ ] Localizar módulo 22 para setup hands-on DSC y MaaS",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "cases-roadmap": [
        "* [ ] Escribir una métrica del caso manufactura relevante para tu industria",
        "* [ ] Confirmar login Showroom como `%USER_NAME%` antes del módulo 10",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "acm-multicluster": [
        "* [ ] Ejecutar `oc get managedclusters` e identificar east/west",
        "* [ ] Abrir UI ACM Clusters y Topology Developer Hub para la misma flota",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "hybrid-mesh-architecture": [
        "* [ ] Inspeccionar HTTPRoute hub y recursos Skupper en consola",
        "* [ ] Trazar cómo tráfico externo alcanza frontends IE en spokes",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "software-templates": [
        "* [ ] Explorar lista plantillas Create en Developer Hub",
        "* [ ] Localizar System Plan B `hybrid-mesh-shared-demos` como fallback",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "deploy-industrial-edge": [
        "* [ ] Scaffoldear IE o abrir Plan B `demo-industrial-edge-east`",
        "* [ ] Verificar org Gitea `ws-%USER_NAME%` y sync Argo CD Healthy",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "kairos-scaling": [
        "* [ ] Abrir Kairos Console y revisar una SmartScalingPolicy",
        "* [ ] Ejecutar `oc get smartscalingpolicy -A` desde terminal Showroom",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "observability": [
        "* [ ] Abrir dashboard Grafana multicluster para tu namespace IE",
        "* [ ] Inspeccionar topics Kafka Console para datos de sensores",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "openshift-gitops": [
        "* [ ] Encontrar tu Application IE en Argo CD y anotar estado sync",
        "* [ ] Identificar fuente repo Git (Gitea usuario vs repo plataforma hub)",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "service-mesh": [
        "* [ ] Abrir Kiali y ver tráfico de tus despliegues IE",
        "* [ ] Confirmar mesh ambient habilitado en namespace IE (no stackrox)",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "scalability": [
        "* [ ] Revisar estado HPA para line-dashboard u otro despliegue IE",
        "* [ ] Observar consumer lag Kafka bajo carga o tráfico simulado",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "network-policies": [
        "* [ ] Revisar NetworkPolicy en `industrial-edge-tst-all`",
        "* [ ] Probar una conexión pod-a-pod permitida y una denegada",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "acs-kuadrant": [
        "* [ ] Verificar que ACS muestra tus cargas spoke en UI Central",
        "* [ ] Probar ruta APIProduct vía gateway hub (o demo Plan B)",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "finops-kubecost": [
        "* [ ] Abrir Kubecost y filtrar asignaciones a tu namespace",
        "* [ ] Comparar costos cluster hub vs spoke en vista federada",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "openshift-ai": [
        "* [ ] Ejecutar `oc get dsc` y confirmar DataScienceCluster Ready",
        "* [ ] Abrir **workshop-notebook** en `ai-%USER_NAME%` y ejecutar prueba MaaS",
        "* [ ] Encontrar Component **ai-%USER_NAME%** en Developer Hub",
        "* [ ] Habilitar extensión **Playground** / **MCP Server** OpenShift AI",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "ai-gateway": [
        "* [ ] Abrir catálogo **workshop-ai-gateway** y UI Kuadrant",
        "* [ ] Crear API key y llamar `/llm/v1/chat/completions`",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "mcp-gateway": [
        "* [ ] Verificar CRDs MCP y `MCPServerRegistration` en `mcp-system`",
        "* [ ] Lightspeed: listar apps Argo CD vía MCP gateway",
        "* [ ] Registrar MCP server OpenShift AI en dashboard",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "llm-rag": [
        "* [ ] Disparar Lightspeed en Developer Hub sobre entidad catálogo",
        "* [ ] Enviar un prompt MaaS y anotar latencia/calidad de respuesta",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "text-ai-predictive": [
        "* [ ] Confirmar despliegue ie-anomaly-alerter corriendo en tu spoke",
        "* [ ] Generar un prompt resumen de alarma vía playground MaaS",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "neuroface": [
        "* [ ] Abrir `https://neuroface.%HUB_DOMAIN%` y probar detección webcam",
        "* [ ] Preguntar a `/api/chat` sobre un objeto detectado",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "ai-end-user-apps": [
        "* [ ] Verificar que line-dashboard muestra telemetría IE en vivo",
        "* [ ] Conectar un insight de anomalía o IA al flujo del operador",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "full-verification": [
        "* [ ] Completar checklist en `verification/progress-checklist.yaml`",
        "* [ ] Ejecutar o revisar salida de `scripts/verify-workshop-e2e.sh`",
        "* [ ] Guardar progreso al final de este módulo",
    ],
    "agent-browser-recording": [
        "* [ ] Leer `verification/recording-runbook.md` (sin MP4 en Git)",
        "* [ ] Explorar un YAML Agent Browser bajo `verification/agent-browser/`",
        "* [ ] Guardar progreso al final de este módulo",
    ],
}

# Shared credential snippets (AsciiDoc)
_WORKSHOP_USER_EN = """*Username:* %USER_NAME% (e.g. `user1` after registration) +
*Password:* `Welcome123!` +
*Used for:* Developer Hub (Keycloak), OpenShift Console htpasswd (hub / east / west), DevSpaces (east spoke)"""

_WORKSHOP_USER_ES = """*Usuario:* %USER_NAME% (p. ej. `user1` tras registro) +
*Contraseña:* `Welcome123!` +
*Válido en:* Developer Hub (Keycloak), consola OpenShift htpasswd (hub / east / west), DevSpaces (spoke east)"""

_FACILITATOR_GITEA_EN = """*Gitea admin (facilitator):* `gitea_admin` / `openshift`"""

_FACILITATOR_GITEA_ES = """*Admin Gitea (facilitador):* `gitea_admin` / `openshift`"""

# Short labels for per-module tables (full detail on index + NOTE in generator)
_WU_EN = "Workshop user"
_WU_ES = "Usuario taller"
_OAUTH_EN = "OpenShift OAuth"
_OAUTH_ES = "OAuth OpenShift"
_PUBLIC_EN = "Public (no login)"
_PUBLIC_ES = "Pública (sin login)"
_APIKEY_EN = "Kuadrant API key (module 20)"
_APIKEY_ES = "API key Kuadrant (módulo 20)"

CRED_NOTE_EN = """NOTE: *Workshop login* — %USER_NAME% / `Welcome123!` (Keycloak for Developer Hub; htpasswd for OpenShift Console on hub, east, and west; DevSpaces on east spoke). OAuth products use the same OpenShift identity."""

CRED_NOTE_ES = """NOTE: *Login del taller* — %USER_NAME% / `Welcome123!` (Keycloak en Developer Hub; htpasswd en consola OpenShift hub/east/west; DevSpaces en spoke east). Productos OAuth usan la misma identidad OpenShift."""
LAB_ACCESS_EN: dict[str, str] = {
    "index": f"""
{INDEX_LAB_ACCESS_NOTE_EN}
.Workshop entry points
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Registration | link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[Register for lab access] | Email → assigns %USER_NAME%
| Showroom (this site) | link:https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[Showroom home] | After registration redirect
| OpenShift Console (hub) | link:https://console-openshift-console.%HUB_DOMAIN%[OpenShift Console] | {_WU_EN}
| Developer Hub | link:https://developer-hub.%HUB_DOMAIN%[Developer Hub] | {_WU_EN}
| Mailpit (IE alerts) | link:https://mailpit.%HUB_DOMAIN%[Mailpit IE] | {_PUBLIC_EN}
| Mailpit (Templates) | link:https://mailpit-templates.%HUB_DOMAIN%[Mailpit Templates] | {_PUBLIC_EN}
|===

.Product catalog — quick links
[cols="2,3,2"]
|===
| Product | URL | Credentials

| ACM fleet | link:https://console-openshift-console.%HUB_DOMAIN%/multicloud/infrastructure/clusters[ACM fleet] | {_WU_EN}
| Industrial Edge | link:https://industrial-edge.%HUB_DOMAIN%[Industrial Edge UI] | {_PUBLIC_EN}
| Gitea | link:https://gitea-gitea.%HUB_DOMAIN%[Gitea] | {_WU_EN} or facilitator
| Grafana | link:https://grafana.%HUB_DOMAIN%[Grafana] | {_OAUTH_EN}
| Kiali | link:https://kiali-openshift-cluster-observability-operator.%HUB_DOMAIN%[Kiali] | {_OAUTH_EN}
| Kairos Console | link:https://kairos-console-kairos-system.%HUB_DOMAIN%[Kairos] | {_OAUTH_EN}
| ACS Central | link:https://central-stackrox.%HUB_DOMAIN%[ACS Central] | {_OAUTH_EN}
| Kuadrant API keys | link:https://developer-hub.%HUB_DOMAIN%/kuadrant[Kuadrant UI] | {_WU_EN}
| Workshop APIs | link:https://workshop-apis.%HUB_DOMAIN%[Workshop APIs] | {_APIKEY_EN}
| Kafka Console | link:https://kafka-console.%HUB_DOMAIN%[Kafka Console] | {_OAUTH_EN}
| Kubecost | link:https://kubecost.%HUB_DOMAIN%[Kubecost] | {_OAUTH_EN}
| Quay | link:https://quay-registry.%HUB_DOMAIN%[Quay] | {_OAUTH_EN}
| DevSpaces (east) | link:https://devspaces.%EAST_DOMAIN%[DevSpaces east] | {_WU_EN}
| OpenShift AI dashboard | link:https://rhods-dashboard-redhat-ods-applications.%HUB_DOMAIN%[ODS Dashboard] | {_OAUTH_EN}
| Skupper observer | link:https://field-content-skupper-network-observer-service-interconnect.%HUB_DOMAIN%[Skupper] | {_OAUTH_EN}
| NeuroFace | link:https://neuroface.%HUB_DOMAIN%[NeuroFace] | {_PUBLIC_EN}
|===
""",
    "hybrid-cloud-strategy": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Showroom | `https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%` | After registration
| OpenShift Console (hub) | `https://console-openshift-console.%HUB_DOMAIN%` | {_WU_EN}
| ACM fleet overview | `https://console-openshift-console.%HUB_DOMAIN%/multicloud/infrastructure/clusters` | {_WU_EN}
|===
""",
    "rosa-architecture": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| ACM — ManagedClusters | `https://console-openshift-console.%HUB_DOMAIN%/multicloud/infrastructure/clusters` | {_WU_EN}
| Hub cluster console | `https://console-openshift-console.%HUB_DOMAIN%` | {_WU_EN}
| East spoke (switch cluster in ACM) | Same ACM UI → cluster `east` | {_WU_EN}
| West spoke | ACM UI → cluster `west` | {_WU_EN}
|===
""",
    "security-scale-hybrid": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| ACS Central | link:https://central-stackrox.%HUB_DOMAIN%[ACS Central] | {_OAUTH_EN}
| OpenShift Console (hub) | link:https://console-openshift-console.%HUB_DOMAIN%[OpenShift Console] | {_WU_EN}
| Kiali (mesh policies) | link:https://kiali-openshift-cluster-observability-operator.%HUB_DOMAIN%[Kiali] | {_OAUTH_EN}
|===
""",
    "aws-ai-integration": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| OpenShift AI dashboard | `https://rhods-dashboard-redhat-ods-applications.%HUB_DOMAIN%` | {_OAUTH_EN}
| Developer Hub (Lightspeed / catalog) | `https://developer-hub.%HUB_DOMAIN%` | {_WU_EN}
| MaaS endpoint (lab) | `https://maas-rhdp.apps.maas.redhatworkshops.io/v1` | Facilitator token
|===
""",
    "cases-roadmap": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Registration (start Part B) | `https://workshop-registration.%HUB_DOMAIN%/` | Email → %USER_NAME%
| Showroom | `https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%` | After redirect
| Developer Hub — Plan B demos | `https://developer-hub.%HUB_DOMAIN%/catalog/default/system/hybrid-mesh-shared-demos` | {_WU_EN}
| Industrial Edge demo | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_EN}
| NeuroFace preview | `https://neuroface.%HUB_DOMAIN%` | {_PUBLIC_EN}
|===
""",
    "acm-multicluster": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| ACM Clusters | `https://console-openshift-console.%HUB_DOMAIN%/multicloud/infrastructure/clusters` | {_WU_EN}
| ACM GitOps (Policies) | `https://console-openshift-console.%HUB_DOMAIN%/multicloud/policies` | {_WU_EN}
| Hub console | `https://console-openshift-console.%HUB_DOMAIN%` | {_WU_EN}
|===
""",
    "hybrid-mesh-architecture": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Industrial Edge (via hub gateway) | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_EN}
| Skupper network observer | `https://field-content-skupper-network-observer-service-interconnect.%HUB_DOMAIN%` | {_OAUTH_EN}
| Hub Gateway routes | `https://console-openshift-console.%HUB_DOMAIN%/k8s/ns/hub-gateway-system/gateway.networking.k8s.io~v1~HTTPRoute` | {_WU_EN}
| Kiali | `https://kiali-openshift-cluster-observability-operator.%HUB_DOMAIN%` | {_OAUTH_EN}
|===
""",
    "software-templates": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Developer Hub — Create | `https://developer-hub.%HUB_DOMAIN%/create` | {_WU_EN}
| Developer Hub — Catalog | `https://developer-hub.%HUB_DOMAIN%/catalog` | {_WU_EN}
| Plan B shared demos | `https://developer-hub.%HUB_DOMAIN%/catalog/default/system/hybrid-mesh-shared-demos` | {_WU_EN}
| Gitea (repos created by scaffold) | `https://gitea-gitea.%HUB_DOMAIN%` | {_WU_EN}
|===
""",
    "deploy-industrial-edge": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Developer Hub — scaffold IE | `https://developer-hub.%HUB_DOMAIN%/create` | {_WU_EN}
| Gitea — your IE repos | `https://gitea-gitea.%HUB_DOMAIN%` | {_WU_EN}
| Industrial Edge UI | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_EN}
| OpenShift GitOps (east) | ACM → cluster `east` → GitOps applications | {_WU_EN}
| Kafka Console | `https://kafka-console.%HUB_DOMAIN%` | {_OAUTH_EN}
|===
""",
    "kairos-scaling": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Kairos Console | `https://kairos-console-kairos-system.%HUB_DOMAIN%` | {_OAUTH_EN}
| Grafana (sensor metrics) | `https://grafana.%HUB_DOMAIN%` | {_OAUTH_EN}
| OpenShift Console — HPA | ACM → `east` → Workloads → HPA | {_WU_EN}
|===
""",
    "observability": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Grafana | `https://grafana.%HUB_DOMAIN%` | {_OAUTH_EN}
| Kiali | `https://kiali-openshift-cluster-observability-operator.%HUB_DOMAIN%` | {_OAUTH_EN}
| OpenShift Console — Observe | `https://console-openshift-console.%HUB_DOMAIN%/observe/metrics` | {_WU_EN}
|===
""",
    "openshift-gitops": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Gitea | `https://gitea-gitea.%HUB_DOMAIN%` | {_WU_EN} ({_FACILITATOR_GITEA_EN})
| Argo CD (hub) | `https://console-openshift-console.%HUB_DOMAIN%/k8s/ns/openshift-gitops/applications.argoproj.io~v1alpha1~Application` | {_WU_EN}
| ACM GitOps cluster | ACM → Infrastructure → Clusters → GitOps | {_WU_EN}
|===
""",
    "service-mesh": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Kiali | `https://kiali-openshift-cluster-observability-operator.%HUB_DOMAIN%` | {_OAUTH_EN}
| Industrial Edge (meshed apps) | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_EN}
| OpenShift Console — mesh | ACM → `east` → Operators → Service Mesh | {_WU_EN}
|===
""",
    "scalability": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Kairos Console | `https://kairos-console-kairos-system.%HUB_DOMAIN%` | {_OAUTH_EN}
| Kafka Console | `https://kafka-console.%HUB_DOMAIN%` | {_OAUTH_EN}
| Grafana (Kafka lag) | `https://grafana.%HUB_DOMAIN%` | {_OAUTH_EN}
|===
""",
    "network-policies": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Industrial Edge | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_EN}
| OpenShift Console — east | ACM → cluster `east` → Networking → NetworkPolicies | {_WU_EN}
| NeuroFace (NP demo target) | `https://neuroface.%HUB_DOMAIN%` | {_PUBLIC_EN}
|===
""",
    "acs-kuadrant": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| ACS Central | `https://central-stackrox.%HUB_DOMAIN%` | {_OAUTH_EN}
| Kuadrant — API keys | `https://developer-hub.%HUB_DOMAIN%/kuadrant` | {_WU_EN} → key for %USER_NAME%
| Workshop APIs (httpbin, REST, LLM) | `https://workshop-apis.%HUB_DOMAIN%` | `Authorization: Bearer <API_KEY>`
| Developer Hub — API catalog | `https://developer-hub.%HUB_DOMAIN%/catalog` | {_WU_EN}
|===
""",
    "finops-kubecost": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Kubecost | `https://kubecost.%HUB_DOMAIN%` | {_OAUTH_EN}
| OpenShift Console — quotas | ACM → your namespace on `east` | {_WU_EN}
|===
""",
    "ai-gateway": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| AI Gateway (MaaS LLM) | `https://workshop-apis.%HUB_DOMAIN%/llm/v1/chat/completions` | Kuadrant API key
| Kuadrant UI | `https://developer-hub.%HUB_DOMAIN%/kuadrant` | {_WU_EN}
| Catalog entity | `https://developer-hub.%HUB_DOMAIN%/catalog/default/component/workshop-ai-gateway` | {_WU_EN}
|===
""",
    "mcp-gateway": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| MCP Gateway | `https://mcp-gateway.%HUB_DOMAIN%/mcp` | {_WU_EN}
| Lightspeed | `https://developer-hub.%HUB_DOMAIN%/lightspeed` | {_WU_EN}
| OpenShift AI MCP (in-cluster) | `ods-maas-mcp-server.maas-workshop.svc:8080/mcp` | {_OAUTH_EN}
| Catalog entity | `https://developer-hub.%HUB_DOMAIN%/catalog/default/component/workshop-mcp-gateway` | {_WU_EN}
|===
""",
    "openshift-ai": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| OpenShift AI dashboard | `https://rhods-dashboard-redhat-ods-applications.%HUB_DOMAIN%` | {_OAUTH_EN}
| Your DS project | OpenShift AI → Projects → **ai-%USER_NAME%** | {_WU_EN} (project admin)
| Developer Hub — your AI entity | `https://developer-hub.%HUB_DOMAIN%/catalog/default/component/ai-%USER_NAME%` | {_WU_EN}
| Shared MaaS playground | OpenShift AI → **maas-workshop** (Plan B) | {_OAUTH_EN}
|===
""",
    "llm-rag": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Developer Hub — Lightspeed | `https://developer-hub.%HUB_DOMAIN%` (catalog → Ask) | {_WU_EN}
| Workshop APIs — LLM route | `https://workshop-apis.%HUB_DOMAIN%/llm` | {_APIKEY_EN}
| MaaS (optional) | `https://maas-rhdp.apps.maas.redhatworkshops.io/v1` | Facilitator token
|===
""",
    "text-ai-predictive": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| MaaS playground | `https://maas-rhdp.apps.maas.redhatworkshops.io/v1` | Facilitator token
| OpenShift AI dashboard | `https://rhods-dashboard-redhat-ods-applications.%HUB_DOMAIN%` | {_OAUTH_EN}
| Anomaly alerter (east spoke) | ACM → `east` → `industrial-edge-tst-%USER_NAME%` | {_WU_EN}
|===
""",
    "neuroface": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| NeuroFace app | `https://neuroface.%HUB_DOMAIN%` | {_PUBLIC_EN}
| API chat | `https://neuroface.%HUB_DOMAIN%/api/chat` | {_PUBLIC_EN}
| OpenShift Console — deploy | ACM → `hub` → namespace `neuroface` | {_WU_EN}
|===
""",
    "ai-end-user-apps": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Industrial Edge line dashboard | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_EN}
| Developer Hub — IE components | `https://developer-hub.%HUB_DOMAIN%/catalog` | {_WU_EN}
| Grafana (telemetry) | `https://grafana.%HUB_DOMAIN%` | {_OAUTH_EN}
|===
""",
    "full-verification": f"""
.Re-run registration if needed
* `https://workshop-registration.%HUB_DOMAIN%/` → %USER_NAME%

.Checklist URLs (all products)
[cols="2,3,2"]
|===
| Product | URL | Credentials

| Showroom | `https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%` | Registered user
| Developer Hub | `https://developer-hub.%HUB_DOMAIN%` | {_WU_EN}
| Industrial Edge | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_EN}
| Kuadrant + APIs | `https://developer-hub.%HUB_DOMAIN%/kuadrant` + `https://workshop-apis.%HUB_DOMAIN%` | API key
| NeuroFace | `https://neuroface.%HUB_DOMAIN%` | {_PUBLIC_EN}
| Kubecost | `https://kubecost.%HUB_DOMAIN%` | {_OAUTH_EN}
|===
""",
    "agent-browser-recording": f"""
[cols="2,3,2"]
|===
| Service | URL | Credentials

| Showroom (record here) | `https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%` | {_WU_EN}
| Developer Hub (catalog targets) | `https://developer-hub.%HUB_DOMAIN%` | {_WU_EN}
| OpenShift Console | `https://console-openshift-console.%HUB_DOMAIN%` | {_WU_EN}
|===
""",
}

LAB_ACCESS_ES: dict[str, str] = {
    "index": f"""
{INDEX_LAB_ACCESS_NOTE_ES}
.Puntos de entrada del taller
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Registro | link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[Registrarse] | Email → asigna %USER_NAME%
| Showroom (este sitio) | link:https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[Showroom] | Tras redirect de registro
| Consola OpenShift (hub) | link:https://console-openshift-console.%HUB_DOMAIN%[Consola OpenShift] | {_WU_ES}
| Developer Hub | link:https://developer-hub.%HUB_DOMAIN%[Developer Hub] | {_WU_ES}
| Mailpit (alertas IE) | link:https://mailpit.%HUB_DOMAIN%[Mailpit IE] | {_PUBLIC_ES}
| Mailpit (Templates) | link:https://mailpit-templates.%HUB_DOMAIN%[Mailpit Templates] | {_PUBLIC_ES}
|===

.Catálogo de productos — enlaces rápidos
[cols="2,3,2"]
|===
| Producto | URL | Credenciales

| Flota ACM | link:https://console-openshift-console.%HUB_DOMAIN%/multicloud/infrastructure/clusters[Flota ACM] | {_WU_ES}
| Industrial Edge | link:https://industrial-edge.%HUB_DOMAIN%[Industrial Edge] | {_PUBLIC_ES}
| Gitea | link:https://gitea-gitea.%HUB_DOMAIN%[Gitea] | {_WU_ES} o facilitador
| Grafana | link:https://grafana.%HUB_DOMAIN%[Grafana] | {_OAUTH_ES}
| Kiali | link:https://kiali-openshift-cluster-observability-operator.%HUB_DOMAIN%[Kiali] | {_OAUTH_ES}
| Kairos Console | link:https://kairos-console-kairos-system.%HUB_DOMAIN%[Kairos] | {_OAUTH_ES}
| ACS Central | link:https://central-stackrox.%HUB_DOMAIN%[ACS Central] | {_OAUTH_ES}
| API keys Kuadrant | link:https://developer-hub.%HUB_DOMAIN%/kuadrant[Kuadrant UI] | {_WU_ES}
| Workshop APIs | link:https://workshop-apis.%HUB_DOMAIN%[Workshop APIs] | {_APIKEY_ES}
| Kafka Console | link:https://kafka-console.%HUB_DOMAIN%[Kafka Console] | {_OAUTH_ES}
| Kubecost | link:https://kubecost.%HUB_DOMAIN%[Kubecost] | {_OAUTH_ES}
| Quay | link:https://quay-registry.%HUB_DOMAIN%[Quay] | {_OAUTH_ES}
| DevSpaces (east) | link:https://devspaces.%EAST_DOMAIN%[DevSpaces east] | {_WU_ES}
| Dashboard OpenShift AI | link:https://rhods-dashboard-redhat-ods-applications.%HUB_DOMAIN%[ODS Dashboard] | {_OAUTH_ES}
| Skupper observer | link:https://field-content-skupper-network-observer-service-interconnect.%HUB_DOMAIN%[Skupper] | {_OAUTH_ES}
| NeuroFace | link:https://neuroface.%HUB_DOMAIN%[NeuroFace] | {_PUBLIC_ES}
|===
""",
    "hybrid-cloud-strategy": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Showroom | `https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%` | Tras registro
| Consola OpenShift (hub) | `https://console-openshift-console.%HUB_DOMAIN%` | {_WU_ES}
| Vista flota ACM | `https://console-openshift-console.%HUB_DOMAIN%/multicloud/infrastructure/clusters` | {_WU_ES}
|===
""",
    "rosa-architecture": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| ACM — ManagedClusters | `https://console-openshift-console.%HUB_DOMAIN%/multicloud/infrastructure/clusters` | {_WU_ES}
| Consola hub | `https://console-openshift-console.%HUB_DOMAIN%` | {_WU_ES}
| Spoke east (cambiar cluster en ACM) | Misma UI ACM → cluster `east` | {_WU_ES}
| Spoke west | UI ACM → cluster `west` | {_WU_ES}
|===
""",
    "security-scale-hybrid": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| ACS Central | `https://central-stackrox.%HUB_DOMAIN%` | {_OAUTH_ES}
| Consola OpenShift — Security | `https://console-openshift-console.%HUB_DOMAIN%/security` | {_WU_ES}
| Kiali (políticas mesh) | `https://kiali-openshift-cluster-observability-operator.%HUB_DOMAIN%` | {_OAUTH_ES}
|===
""",
    "aws-ai-integration": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Dashboard OpenShift AI | `https://rhods-dashboard-redhat-ods-applications.%HUB_DOMAIN%` | {_OAUTH_ES}
| Developer Hub (Lightspeed / catálogo) | `https://developer-hub.%HUB_DOMAIN%` | {_WU_ES}
| Endpoint MaaS (lab) | `https://maas-rhdp.apps.maas.redhatworkshops.io/v1` | Token facilitador
|===
""",
    "cases-roadmap": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Registro (inicio Parte B) | `https://workshop-registration.%HUB_DOMAIN%/` | Email → %USER_NAME%
| Showroom | `https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%` | Tras redirect
| Developer Hub — demos Plan B | `https://developer-hub.%HUB_DOMAIN%/catalog/default/system/hybrid-mesh-shared-demos` | {_WU_ES}
| Demo Industrial Edge | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_ES}
| Vista previa NeuroFace | `https://neuroface.%HUB_DOMAIN%` | {_PUBLIC_ES}
|===
""",
    "acm-multicluster": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| ACM Clusters | `https://console-openshift-console.%HUB_DOMAIN%/multicloud/infrastructure/clusters` | {_WU_ES}
| ACM GitOps (Policies) | `https://console-openshift-console.%HUB_DOMAIN%/multicloud/policies` | {_WU_ES}
| Consola hub | `https://console-openshift-console.%HUB_DOMAIN%` | {_WU_ES}
|===
""",
    "hybrid-mesh-architecture": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Industrial Edge (vía hub gateway) | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_ES}
| Skupper network observer | `https://field-content-skupper-network-observer-service-interconnect.%HUB_DOMAIN%` | {_OAUTH_ES}
| Rutas Hub Gateway | `https://console-openshift-console.%HUB_DOMAIN%/k8s/ns/hub-gateway-system/gateway.networking.k8s.io~v1~HTTPRoute` | {_WU_ES}
| Kiali | `https://kiali-openshift-cluster-observability-operator.%HUB_DOMAIN%` | {_OAUTH_ES}
|===
""",
    "software-templates": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Developer Hub — Create | `https://developer-hub.%HUB_DOMAIN%/create` | {_WU_ES}
| Developer Hub — Catálogo | `https://developer-hub.%HUB_DOMAIN%/catalog` | {_WU_ES}
| Demos compartidas Plan B | `https://developer-hub.%HUB_DOMAIN%/catalog/default/system/hybrid-mesh-shared-demos` | {_WU_ES}
| Gitea (repos del scaffold) | `https://gitea-gitea.%HUB_DOMAIN%` | {_WU_ES}
|===
""",
    "deploy-industrial-edge": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Developer Hub — scaffold IE | `https://developer-hub.%HUB_DOMAIN%/create` | {_WU_ES}
| Gitea — repos IE | `https://gitea-gitea.%HUB_DOMAIN%` | {_WU_ES}
| UI Industrial Edge | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_ES}
| OpenShift GitOps (east) | ACM → cluster `east` → aplicaciones GitOps | {_WU_ES}
| Kafka Console | `https://kafka-console.%HUB_DOMAIN%` | {_OAUTH_ES}
|===
""",
    "kairos-scaling": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Kairos Console | `https://kairos-console-kairos-system.%HUB_DOMAIN%` | {_OAUTH_ES}
| Grafana (métricas sensores) | `https://grafana.%HUB_DOMAIN%` | {_OAUTH_ES}
| Consola OpenShift — HPA | ACM → `east` → Workloads → HPA | {_WU_ES}
|===
""",
    "observability": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Grafana | `https://grafana.%HUB_DOMAIN%` | {_OAUTH_ES}
| Kiali | `https://kiali-openshift-cluster-observability-operator.%HUB_DOMAIN%` | {_OAUTH_ES}
| Consola OpenShift — Observe | `https://console-openshift-console.%HUB_DOMAIN%/observe/metrics` | {_WU_ES}
|===
""",
    "openshift-gitops": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Gitea | `https://gitea-gitea.%HUB_DOMAIN%` | {_WU_ES} ({_FACILITATOR_GITEA_ES})
| Argo CD (hub) | `https://console-openshift-console.%HUB_DOMAIN%/k8s/ns/openshift-gitops/applications.argoproj.io~v1alpha1~Application` | {_WU_ES}
| ACM GitOps cluster | ACM → Infrastructure → Clusters → GitOps | {_WU_ES}
|===
""",
    "service-mesh": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Kiali | `https://kiali-openshift-cluster-observability-operator.%HUB_DOMAIN%` | {_OAUTH_ES}
| Industrial Edge (apps en mesh) | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_ES}
| Consola OpenShift — mesh | ACM → `east` → Operators → Service Mesh | {_WU_ES}
|===
""",
    "scalability": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Kairos Console | `https://kairos-console-kairos-system.%HUB_DOMAIN%` | {_OAUTH_ES}
| Kafka Console | `https://kafka-console.%HUB_DOMAIN%` | {_OAUTH_ES}
| Grafana (lag Kafka) | `https://grafana.%HUB_DOMAIN%` | {_OAUTH_ES}
|===
""",
    "network-policies": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Industrial Edge | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_ES}
| Consola OpenShift — east | ACM → cluster `east` → Networking → NetworkPolicies | {_WU_ES}
| NeuroFace (objetivo demo NP) | `https://neuroface.%HUB_DOMAIN%` | {_PUBLIC_ES}
|===
""",
    "acs-kuadrant": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| ACS Central | `https://central-stackrox.%HUB_DOMAIN%` | {_OAUTH_ES}
| Kuadrant — API keys | `https://developer-hub.%HUB_DOMAIN%/kuadrant` | {_WU_ES} → key para %USER_NAME%
| Workshop APIs (httpbin, REST, LLM) | `https://workshop-apis.%HUB_DOMAIN%` | `Authorization: Bearer <API_KEY>`
| Developer Hub — catálogo API | `https://developer-hub.%HUB_DOMAIN%/catalog` | {_WU_ES}
|===
""",
    "finops-kubecost": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Kubecost | `https://kubecost.%HUB_DOMAIN%` | {_OAUTH_ES}
| Consola OpenShift — quotas | ACM → tu namespace en `east` | {_WU_ES}
|===
""",
    "ai-gateway": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| AI Gateway (MaaS LLM) | `https://workshop-apis.%HUB_DOMAIN%/llm/v1/chat/completions` | API key Kuadrant
| UI Kuadrant | `https://developer-hub.%HUB_DOMAIN%/kuadrant` | {_WU_ES}
| Entidad catálogo | `https://developer-hub.%HUB_DOMAIN%/catalog/default/component/workshop-ai-gateway` | {_WU_ES}
|===
""",
    "mcp-gateway": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| MCP Gateway | `https://mcp-gateway.%HUB_DOMAIN%/mcp` | {_WU_ES}
| Lightspeed | `https://developer-hub.%HUB_DOMAIN%/lightspeed` | {_WU_ES}
| MCP OpenShift AI (in-cluster) | `ods-maas-mcp-server.maas-workshop.svc:8080/mcp` | {_OAUTH_ES}
| Entidad catálogo | `https://developer-hub.%HUB_DOMAIN%/catalog/default/component/workshop-mcp-gateway` | {_WU_ES}
|===
""",
    "openshift-ai": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Dashboard OpenShift AI | `https://rhods-dashboard-redhat-ods-applications.%HUB_DOMAIN%` | {_OAUTH_ES}
| Tu proyecto DS | OpenShift AI → Projects → **ai-%USER_NAME%** | {_WU_ES} (admin proyecto)
| Developer Hub — entidad IA | `https://developer-hub.%HUB_DOMAIN%/catalog/default/component/ai-%USER_NAME%` | {_WU_ES}
| Playground MaaS compartido | OpenShift AI → **maas-workshop** (Plan B) | {_OAUTH_ES}
|===
""",
    "llm-rag": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Developer Hub — Lightspeed | `https://developer-hub.%HUB_DOMAIN%` (catálogo → Ask) | {_WU_ES}
| Workshop APIs — ruta LLM | `https://workshop-apis.%HUB_DOMAIN%/llm` | {_APIKEY_ES}
| MaaS (opcional) | `https://maas-rhdp.apps.maas.redhatworkshops.io/v1` | Token facilitador
|===
""",
    "text-ai-predictive": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Playground MaaS | `https://maas-rhdp.apps.maas.redhatworkshops.io/v1` | Token facilitador
| Dashboard OpenShift AI | `https://rhods-dashboard-redhat-ods-applications.%HUB_DOMAIN%` | {_OAUTH_ES}
| Anomaly alerter (spoke east) | ACM → `east` → `industrial-edge-tst-%USER_NAME%` | {_WU_ES}
|===
""",
    "neuroface": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| App NeuroFace | `https://neuroface.%HUB_DOMAIN%` | {_PUBLIC_ES}
| API chat | `https://neuroface.%HUB_DOMAIN%/api/chat` | {_PUBLIC_ES}
| Consola OpenShift — deploy | ACM → `hub` → namespace `neuroface` | {_WU_ES}
|===
""",
    "ai-end-user-apps": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Dashboard línea IE | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_ES}
| Developer Hub — componentes IE | `https://developer-hub.%HUB_DOMAIN%/catalog` | {_WU_ES}
| Grafana (telemetría) | `https://grafana.%HUB_DOMAIN%` | {_OAUTH_ES}
|===
""",
    "full-verification": f"""
.Re-registro si hace falta
* `https://workshop-registration.%HUB_DOMAIN%/` → %USER_NAME%

.Checklist URLs (todos los productos)
[cols="2,3,2"]
|===
| Producto | URL | Credenciales

| Showroom | `https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%` | Usuario registrado
| Developer Hub | `https://developer-hub.%HUB_DOMAIN%` | {_WU_ES}
| Industrial Edge | `https://industrial-edge.%HUB_DOMAIN%` | {_PUBLIC_ES}
| Kuadrant + APIs | `https://developer-hub.%HUB_DOMAIN%/kuadrant` + `https://workshop-apis.%HUB_DOMAIN%` | API key
| NeuroFace | `https://neuroface.%HUB_DOMAIN%` | {_PUBLIC_ES}
| Kubecost | `https://kubecost.%HUB_DOMAIN%` | {_OAUTH_ES}
|===
""",
    "agent-browser-recording": f"""
[cols="2,3,2"]
|===
| Servicio | URL | Credenciales

| Showroom (grabar aquí) | `https://showroom-showroom.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%` | {_WU_ES}
| Developer Hub (objetivos catálogo) | `https://developer-hub.%HUB_DOMAIN%` | {_WU_ES}
| Consola OpenShift | `https://console-openshift-console.%HUB_DOMAIN%` | {_WU_ES}
|===
""",
}
