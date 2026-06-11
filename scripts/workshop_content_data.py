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
MODULE_CONTEXT: dict[str, str] = {
    "acm-multicluster": """In this module you open the **ACM Clusters** view on the hub and confirm `east` and `west` spokes are `Available`. Use the Showroom terminal: `oc get managedclusters`. Every later Part B exercise assumes you know which cluster hosts your workloads (usually `east`).""",
    "hybrid-mesh-architecture": """You will trace how external traffic reaches Industrial Edge on a spoke: hub Gateway API `HTTPRoute`, Skupper interconnect, and the IE route. Open the Skupper observer and IE UI from the lab access table — no separate ACM or ROSA documentation site is required.""",
    "software-templates": """You will create (or browse) a workload from **Developer Hub → Create**. If your `%USER_NAME%` scaffold fails, open **Plan B** system `hybrid-mesh-shared-demos` — same URLs, pre-deployed. Check Gitea only if you successfully scaffolded.""",
    "deploy-industrial-edge": """Goal: confirm Industrial Edge workloads are reachable — line dashboard, Kafka topics, and (optional) your user-scoped namespace. Use Plan B demo `demo-industrial-edge-east` if you did not scaffold.""",
    "acs-kuadrant": """You will use **ACS Central** on this cluster (`central-stackrox` route) for runtime security context and **Developer Hub → Kuadrant** to request an API key for `workshop-apis`. Test with `curl` and your key — not a generic Red Hat marketing URL.""",
    "ai-gateway": """In this module you expose **Model-as-a-Service (MaaS)** LLM inference through a governed **AI Gateway** — not by sharing raw OpenShift AI routes. You will:

. Open **Developer Hub → Catalog → workshop-ai-gateway** and follow links to Topology, TechDocs, and the Kuadrant API portal.
. Trace GitOps in `components/workshop-kuadrant-apis/` — `HTTPRoute` on the hub Gateway API, Istio `Gateway`, and Kuadrant `AuthPolicy` + `TokenRateLimitPolicy`.
. Mint an API key for `%USER_NAME%` in the Kuadrant UI and call `https://workshop-apis.%HUB_DOMAIN%/llm/v1/chat/completions` with a Bearer token.
. Compare latency, headers, and error responses against direct MaaS from the OpenShift AI notebook (module 22) — the gateway adds auth, rate limits, and a stable external hostname for factory apps.

*Prerequisite:* module **22 OpenShift AI** — you need a running `maas-workshop` playground and familiarity with chat-completions JSON.""",
    "mcp-gateway": """Verify MCP Gateway in `mcp-system`, then use **Developer Hub → Lightspeed** with prompts that invoke ArgoCD/k8s MCP tools. Register OpenShift AI MCP server in dashboard (maas-workshop).""",
    "openshift-ai": """Open the **OpenShift AI dashboard** → project **ai-%USER_NAME%** → **Workbenches → workshop-notebook** and run the MaaS smoke-test notebook. Catalog entity **OpenShift AI — %USER_NAME%** links Topology and dashboard.""",
    "neuroface": """Open link:https://neuroface.%HUB_DOMAIN%[NeuroFace] and **Developer Hub → Catalog → neuroface-workshop** for Topology. OVMS is enabled for local vision; chat uses MaaS. Allow webcam and test detection + `/api/chat`.""",
    "ai-end-user-apps": """Capstone module **28 — AI in End-User Apps**. You will connect everything operators touch on the factory floor:

. Open link:https://industrial-edge.%HUB_DOMAIN%[Industrial Edge line-dashboard] — confirm live Kafka sensor metrics for east spoke workloads.
. Developer Hub → **Catalog** — locate `%USER_NAME%` IE components, Grafana dashboards, and AI catalog dependencies.
. Review **ie-anomaly-alerter** alerts: `oc logs -l app=ie-anomaly-alerter -n industrial-edge-tst-all --tail=30` in the Showroom **Terminal**.
. Optional: open link:https://neuroface.%HUB_DOMAIN%[NeuroFace] for operator AI assist; compare with MaaS summaries from module 23.
. Trace Camel K demos `demo-camel-kaoto-east` / `demo-camel-cdc-east` in catalog Topology for event-driven OT/IT integration.

*Success criteria:* line-dashboard shows data, at least one catalog entity links IE → AI, and you can explain how AWS Kinesis or Azure Event Hubs would mirror the same event path in production.""",
    "full-verification": """**Facilitator / agent only.** Run `scripts/verify-workshop-e2e.sh` and `showroom-hybrid-mesh-ai/verification/progress-checklist.yaml` — not shown to learners in the workshop nav.""",
    "agent-browser-recording": """**Facilitator / agent only.** Agent Browser YAML under `verification/agent-browser/` replays UI flows for CI. Recordings stay local (`*.mp4` gitignored).""",
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

HYBRID_CALLOUT_EN = HYBRID_INTEGRATION_EN
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

INDEX_LAB_ACCESS_NOTE_EN = """NOTE: *Workshop login* — %USER_NAME% / `Welcome123!` (Keycloak Developer Hub; htpasswd OpenShift hub/east/west; DevSpaces east). OAuth products use the same OpenShift identity.

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

PROGRESS_UI_EN = """
++++
<div class="workshop-progress" data-module="{module_id}">
  <label><input type="checkbox" data-completed> I completed this module</label>
  <label><input type="checkbox" data-interest> I want to learn more</label>
  <button type="button" onclick="saveWorkshopProgress('{module_id}')">Save progress</button>
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

PREREQUISITES_EN = """
== Prerequisites

* Modern web browser (Chrome or Firefox recommended) with webcam access for NeuroFace modules.
* Access to the OpenShift console on the workshop hub — launch **Hybrid Mesh AI Workshop** from the Application menu.
* Workshop registration at link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[workshop registration] to obtain `%USER_NAME%` and Showroom redirect.
* Optional: use the embedded Showroom terminal for `oc` commands; no local kubeconfig required for Part B.
"""

NARRATIVES: dict[str, str] = {
    "index": """This workshop demonstrates how Red Hat customers unify strategy and operations across hybrid cloud using OpenShift as the common platform. You will apply the same patterns on a live RHDP hub-spoke lab with east and west spokes managed by ACM.

Part A frames the business case: modernization, security, FinOps, and AI. Part B (modules 10–28) lets you use Industrial Edge, multicluster observability, Kuadrant API security, and OpenShift AI — as `%USER_NAME%` in this lab environment.

Register at link:https://workshop-registration.%HUB_DOMAIN%/?USER_NAME=%USER_NAME%[workshop registration] before hands-on modules.""",
    "hybrid-cloud-strategy": """Hybrid cloud strategy starts with workload placement: keep latency-sensitive factory systems at the edge, burst analytics and AI training to cloud regions, and govern everything from a central OpenShift hub. Red Hat OpenShift Container Platform delivers a single Kubernetes API and operator model whether clusters run on-prem, at edge sites, or as ROSA in AWS.

In this lab, ACM on the hub represents that governance layer — policies, observability federation, and GitOps placement target east and west spokes the same way a customer would target ROSA and on-prem clusters. You are not learning abstract slides; every Part B module reinforces a strategic pillar: automation, security, developer velocity, or AI readiness.

Executives should note that OpenShift avoids replatforming twice: microservices, VMs (CNV), and AI pipelines share the same RBAC, networking, and CI/CD patterns. When you register as `%USER_NAME%`, your hands-on path mirrors how platform teams onboard application squads in production.""",
    "rosa-architecture": """Red Hat OpenShift Service on AWS (ROSA) provides a fully managed control plane in your AWS account while Red Hat handles upgrades, security patches, and SRE operations. Worker nodes scale via MachineSets; ingress integrates with Route 53 and ALB; IAM and STS enable secure cloud service access — the reference architecture for hybrid customers who standardize on OpenShift everywhere.

This workshop's hub-spoke layout maps cleanly to ROSA concepts: the hub is your fleet management cluster (like an ACM hub on ROSA), spokes are regional or edge clusters importing via ManagedCluster resources. You will inspect `ManagedCluster` objects and GitOpsCluster links in module 10 — the same CRDs a ROSA customer uses when joining factory edge clusters to a central governance hub.

Understanding ROSA architecture helps you explain SLA boundaries: Red Hat manages the control plane; you own worker sizing, networking, and data. In the lab, Kairos and HPA on spokes simulate ROSA autoscaling decisions without AWS billing, preparing you for FinOps modules later. See link:https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws[ROSA documentation] for architecture and planning guides.""",
    "security-scale-hybrid": """Defense in depth in this lab spans four layers — each controlled by a single YAML manifest in Git:

*Layer 1: Kuadrant AuthPolicy at the hub gateway* — every API request is authenticated before reaching backend services. The annotation `secret.kuadrant.io/plan-id` on the API key Secret determines the user's rate limit tier:

[source,yaml]
----
# components/workshop-kuadrant-apis/templates/policies.yaml
apiVersion: kuadrant.io/v1
kind: AuthPolicy
metadata:
  name: workshop-maas-auth
  namespace: hub-gateway-system
  annotations:
    argocd.argoproj.io/sync-wave: "3"
    argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true
spec:
  targetRef:
    group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: workshop-maas
  rules:
    authentication:
      api-key-users:
        apiKey:
          allNamespaces: true          # keys can live in any namespace
          selector:
            matchLabels:
              app: workshop-maas
        credentials:
          authorizationHeader:
            prefix: APIKEY
----

*Layer 2: Ambient mesh mTLS (zero config)* — namespaces get automatic encryption when labeled `istio.io/dataplane-mode: ambient`. But notice certain namespaces are deliberately excluded:

[source,yaml]
----
# components/namespaces/templates/all.yaml — noMeshNamespaces
# These namespaces NEVER get istio.io/dataplane-mode=ambient:
#   - stackrox        (ACS sensors would be disrupted by ztunnel interception)
#   - gitea           (internal git traffic — no mesh overhead needed)
#   - redhat-connectivity-link-operator (CrashLoopBackOff on spokes when meshed)
----

*Layer 3: ACS Central + SecuredCluster* — hub runs Central with auto-scaling image scanner; spokes report via eBPF collector without sidecars:

[source,yaml]
----
# components/acs-operator/templates/central.yaml
apiVersion: platform.stackrox.io/v1alpha1
kind: Central
metadata:
  name: stackrox-central-services
  namespace: stackrox
  annotations:
    argocd.argoproj.io/sync-wave: "5"
spec:
  central:
    exposure:
      loadBalancer:
        enabled: false
      route:
        enabled: true             # OCP route for console access
    persistence:
      persistentVolumeClaim:
        claimName: stackrox-db
  scanner:
    analyzer:
      scaling:
        autoScaling: Enabled
        maxReplicas: 3
        minReplicas: 1
    scannerComponent: Enabled
----

[source,yaml]
----
# components/acs-secured-cluster/templates/secured-cluster.yaml
apiVersion: platform.stackrox.io/v1alpha1
kind: SecuredCluster
metadata:
  name: stackrox-secured-cluster-services
  namespace: stackrox
  annotations:
    argocd.argoproj.io/sync-wave: "6"
spec:
  clusterName: {{ .Values.clusterName }}          # each spoke gets its own identity
  centralEndpoint: central-stackrox.apps.hub-domain:443
  admissionControl:
    listenOnCreates: true
    listenOnUpdates: true
    listenOnEvents: true
  perNode:
    collector:
      collection: EBPF   # kernel-level visibility without sidecars
      imageFlavor: Regular
    taintToleration: TolerateTaints
----

*Layer 4: OVN NetworkPolicy* — micro-segmentation at the pod level. Only the ingress controller and sensor pods can reach the dashboard:

[source,yaml]
----
# components/workshop-demos/templates/network-policy-demo.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ie-workshop-allow-dashboard
  namespace: industrial-edge-tst-all
  annotations:
    argocd.argoproj.io/sync-wave: "3"
    workshop.demo/maximilianopizarro: network-policy-module-19
spec:
  podSelector:
    matchLabels:
      app: line-dashboard
  policyTypes: [Ingress]
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: openshift-ingress
      ports: [{protocol: TCP, port: 8080}]
    - from:
        - podSelector:
            matchLabels:
              app: machine-sensor
      ports: [{protocol: TCP, port: 8080}]
----

Each layer is a **single CR in Git**. Argo CD applies them in sync-wave order (3→5→6). No imperative scripts, no manual firewall rules. Verify in the Showroom terminal:

[source,bash]
----
# ACS Central pods on hub
oc get pods -n stackrox -l app=central

# SecuredCluster on spoke
oc get securedclusters -n stackrox

# NetworkPolicy demo on east
oc get networkpolicy -n industrial-edge-tst-all
----

See link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_security_for_kubernetes[ACS docs] and link:https://www.kuadrant.io/docs/[Kuadrant docs].""",
    "aws-ai-integration": """AWS customers often pair ROSA with native AI services — Amazon Bedrock for foundation models, SageMaker for training pipelines, and IAM OIDC for secure workload identity. Red Hat's hybrid approach keeps inference and data pipelines on OpenShift AI while still allowing optional AWS service integration via credentials and external endpoints where policy permits.

This workshop intentionally substitutes OpenShift AI plus Model-as-a-Service (MaaS) for Bedrock/SageMaker so you experience a portable pattern: a `DataScienceCluster` on the hub, shared LLM endpoint, and consumer apps (NeuroFace, Developer Hub Lightspeed) on spokes. The secret `openshift-ai-maas-credentials` and MaaS base URL mirror how production teams centralize model access instead of embedding API keys in every deployment.

Module 22 onward activates this stack hands-on. Executives should recognize that OpenShift AI on ROSA or on-prem avoids rewriting applications when cloud AI pricing or residency rules change — the Kubernetes-native serving layer moves with the cluster.""",
    "cases-roadmap": """**Industry case — precision manufacturing IoT:** A global automotive supplier deployed OpenShift at three factory edge sites plus a ROSA hub for analytics. Machine vibration sensors emit 12,000 events/minute per line; unplanned downtime cost $47,000/hour. After migrating to Industrial Edge on OpenShift with Kafka, Camel integrations, and ACS runtime policies, mean time to detect anomalies dropped from 18 minutes to 90 seconds, and Kairos-approved scaling reduced over-provisioned edge nodes by 34%.

That customer roadmap led to OpenShift AI for predictive maintenance models and Developer Hub templates so each plant could scaffold compliant pipelines without shadow IT. This workshop reproduces that journey at lab scale: modules 13–18 deploy IE on spoke east/west, modules 22–26 add MaaS and NeuroFace, module 21 adds Kubecost chargeback by namespace.

Your next step is Part B registration verification — ensure `%USER_NAME%` works in Showroom, then proceed to module 10 for ACM fleet visibility. Plan B shared demos remain available if your scaffold slot is unavailable.""",
    "acm-multicluster": """Red Hat Advanced Cluster Management for Kubernetes turns OpenShift into a fleet control plane: import spokes, enforce policies, visualize health, and delegate GitOps to cluster admins with consistent RBAC. The actual CRDs live in `components/acm-hub-spoke/` — three resources wire the entire fleet:

*Step 1: Register spokes as ManagedClusters.* The Helm template iterates `.Values.managedClusters` and creates one `ManagedCluster` + `KlusterletAddonConfig` per spoke:

[source,yaml]
----
# components/acm-hub-spoke/templates/managed-clusters.yaml
{{- range $name, $cluster := .Values.managedClusters }}
apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: {{ $name }}               # east, west
  labels:
    name: {{ $name }}
    region: {{ $name }}
    cloud: auto-detect
    vendor: OpenShift
    cluster.open-cluster-management.io/clusterset: global
  annotations:
    argocd.argoproj.io/sync-wave: "1"
spec:
  hubAcceptsClient: true
  leaseDurationSeconds: 60
---
apiVersion: agent.open-cluster-management.io/v1
kind: KlusterletAddonConfig
metadata:
  name: {{ $name }}
  namespace: {{ $name }}
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  clusterName: {{ $name }}
  applicationManager:  { enabled: true }
  certPolicyController: { enabled: true }
  policyController:    { enabled: true }
  searchCollector:     { enabled: true }
{{- end }}
----

*Step 2: Placement selects which clusters receive workloads.* Only spokes matching `region: east|west` are selected:

[source,yaml]
----
# components/acm-hub-spoke/templates/placement.yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Placement
metadata:
  name: hub-spoke-placement
  namespace: openshift-gitops
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  clusterSets: [global]
  predicates:
    - requiredClusterSelector:
        labelSelector:
          matchExpressions:
            - key: region
              operator: In
              values: [east, west]
----

*Step 3: GitOpsCluster bridges ACM placement to Argo CD.* This lets hub Argo CD deploy Applications to spoke clusters without manual kubeconfig:

[source,yaml]
----
# components/acm-hub-spoke/templates/gitops-cluster.yaml
apiVersion: apps.open-cluster-management.io/v1beta1
kind: GitOpsCluster
metadata:
  name: hub-spoke-gitops
  namespace: openshift-gitops
  annotations:
    argocd.argoproj.io/sync-wave: "3"
spec:
  argoServer:
    cluster: local-cluster
    argoNamespace: openshift-gitops
  placementRef:
    kind: Placement
    name: hub-spoke-placement
    apiVersion: cluster.open-cluster-management.io/v1beta1
----

*Step 4: ApplicationSet generates spoke Applications automatically.* The `clusterDecisionResource` generator reads ACM placement decisions — when a new spoke joins, its Application appears without editing Git:

[source,yaml]
----
# components/acm-hub-spoke/templates/applicationset.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: industrial-edge-spoke
  namespace: openshift-gitops
  annotations:
    argocd.argoproj.io/sync-wave: "4"
spec:
  generators:
    - clusterDecisionResource:
        configMapRef: acm-placement
        labelSelector:
          matchLabels:
            cluster.open-cluster-management.io/placement: hub-spoke-placement
        requeueAfterSeconds: 180
  template:
    spec:
      source:
        repoURL: {{ .Values.gitops.repoUrl }}
        path: '{{name}}'           # east/ or west/ directory
      destination:
        name: '{{name}}'           # deploys to that spoke
      syncPolicy:
        automated: { selfHeal: true, prune: true }
----

Verify from the Showroom terminal:

[source,bash]
----
# Confirm both spokes are joined and available
oc get managedclusters
# NAME   HUB ACCEPTED   MANAGED CLUSTER URLS   JOINED   AVAILABLE
# east   true           ...                    True     True
# west   true           ...                    True     True

# Check the GitOpsCluster bridge
oc get gitopsclusters -n openshift-gitops

# See ApplicationSet-generated spoke Applications
oc get applicationsets -n openshift-gitops
----

See link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes[ACM documentation] for fleet lifecycle.""",
    "hybrid-mesh-architecture": """Hybrid mesh architecture connects application networks across clusters without flattening VPCs or exposing kube-apiserver endpoints publicly. The hub runs a single **Istio Gateway** that terminates all external traffic; Skupper tunnels carry requests to spoke services. The configuration lives in `components/hub-gateway/`.

*Hub Gateway — the single entry point:* One Istio-class Gateway with a ClusterIP service (no LoadBalancer — OpenShift Routes handle TLS termination upstream):

[source,yaml]
----
# components/hub-gateway/templates/gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: hub-gateway
  namespace: hub-gateway-system
  annotations:
    argocd.argoproj.io/sync-wave: "1"
    networking.istio.io/service-type: ClusterIP   # OCP Route handles external TLS
spec:
  gatewayClassName: istio
  listeners:
    - name: http
      port: 8080
      protocol: HTTP
      allowedRoutes:
        namespaces:
          from: Same             # only HTTPRoutes in hub-gateway-system can attach
----

*HTTPRoutes attach to the Gateway* for each backend — IE dashboard, workshop APIs, Kuadrant endpoints. The Kuadrant API routes (module 23) use Istio `Hostname` backendRefs to reach external MaaS without proxy containers:

[source,yaml]
----
# components/workshop-kuadrant-apis/templates/routes.yaml (pattern)
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: workshop-{{ $name }}
  namespace: hub-gateway-system
  labels:
    kuadrant.io/exposed: "true"
    workshop.kuadrant.io/external-host: {{ $api.host }}
spec:
  parentRefs:
    - name: hub-gateway
      namespace: hub-gateway-system
  hostnames: ["workshop-apis.{{ $hostname }}"]
  rules:
    - matches:
        - path: { type: PathPrefix, value: {{ $api.pathPrefix }} }
      filters:
        - type: URLRewrite
          urlRewrite:
            hostname: {{ $api.host }}     # TLS origination via ServiceEntry
      backendRefs:
        - group: networking.istio.io
          kind: Hostname
          name: {{ $api.host }}
          port: 443
----

*Skupper Sites and Connectors* in `components/service-interconnect/` bridge the hub-gateway-system to spoke namespaces, carrying traffic for IE frontends, Kafka Console, and cross-cluster observability — all encrypted over the Skupper tunnel without VPC peering.

Verify from the Showroom terminal:

[source,bash]
----
# List all HTTPRoutes attached to the hub gateway
oc get httproutes -n hub-gateway-system

# Check the Gateway status and attached routes
oc get gateway hub-gateway -n hub-gateway-system -o yaml | grep -A5 conditions

# Skupper status
oc get sites,connectors,listeners -n service-interconnect
----

Understanding this layer explains why Kuadrant policies (module 20/23) attach at the hub gateway and why Industrial Edge traffic (module 13) flows through Skupper.""",
    "software-templates": """Red Hat Developer Hub software templates encode golden paths: parameterized scaffolder actions create Git repos, register catalog entities, and trigger Argo CD Applications with guardrails already wired. The Developer Hub deployment is configured via `components/developer-hub/` with the App-of-Apps template injecting extensive plugin configuration.

*Developer Hub valuesObject in the App-of-Apps* shows how the platform team configures every plugin declaratively — RBAC, Lightspeed AI, Kuadrant, TechDocs, notifications, and multicluster Kubernetes Topology:

[source,yaml]
----
# templates/component-applications.yaml — developer-hub valuesObject (excerpt)
helm:
  valuesObject:
    clusterDomain: {{ $domain }}
    userCount: {{ $.Values.userCount | default 50 }}
    plugins:
      rbac: { enabled: true, policyAdminUser: platformadmin }
      lightspeed:
        enabled: true
        aiModel:
          apiURL: {{ $.Values.litemaas.apiUrl }}
          model: {{ $.Values.litemaas.model | default "llama-scout-17b" }}
      techdocs: { enabled: true }
      kuadrant: { enabled: true }          # API key self-service (module 23)
      argocd:   { enabled: true }
      notificationsEmail: { enabled: true }
      mcp:      { enabled: true }          # MCP Gateway integration (module 24)
    kubernetesSpokes:
      enabled: true
      east:
        apiUrl: {{ $.Values.clusters.east.apiUrl }}
      west:
        apiUrl: {{ $.Values.clusters.west.apiUrl }}
----

This workshop ships templates for Industrial Edge, Camel Kaoto, API products, OpenShift AI workspaces, CNV VMs, and NeuroFace. If your `%USER_NAME%` scaffold fails, switch to Plan B — Developer Hub System `hybrid-mesh-shared-demos` exposes pre-deployed Components with the same URLs and Topology entries.

Templates are the bridge between executive strategy (module 01) and spoke deployments (module 13). Inspect `docs/assets/backstage/software-templates/` and catalog ConfigMaps to see how OpenShift GitOps picks up generated repos automatically.

[source,bash]
----
# List available templates in Developer Hub
oc get configmaps -n developer-hub -l backstage.io/kind=Template

# Check catalog entities registered by scaffolding
oc get configmaps -n developer-hub -l backstage.io/kind=Component
----

See link:https://docs.redhat.com/en/documentation/red_hat_developer_hub[Developer Hub documentation] for template authoring.""",
    "deploy-industrial-edge": """Industrial Edge on OpenShift combines event streaming, integration, and visualization for factory and IoT scenarios. The entire stack is defined in `components/industrial-edge-tst/` and deployed via GitOps to spoke clusters.

*Kafka cluster (KRaft mode):* A single-node KRaft broker with ephemeral storage, plus `temperature` and `vibration` topics for sensor data. Notice the Strimzi annotations and the Prometheus JMX exporter for observability:

[source,yaml]
----
# components/industrial-edge-tst/templates/kafka-cluster.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaNodePool
metadata:
  name: broker
  namespace: industrial-edge-tst-all
  labels:
    strimzi.io/cluster: dev-cluster
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  replicas: 1
  roles: [controller, broker]        # KRaft combined mode — no ZooKeeper
  storage:
    type: ephemeral                   # workshop-scale; production uses persistent
---
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: dev-cluster
  namespace: industrial-edge-tst-all
  annotations:
    strimzi.io/kraft: enabled
    strimzi.io/node-pools: enabled
    argocd.argoproj.io/sync-wave: "3"
spec:
  kafka:
    version: 4.2.0
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
    metricsConfig:
      type: jmxPrometheusExporter     # feeds Grafana dashboards (module 15)
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics-config
          key: kafka-metrics-config.yml
  entityOperator:
    topicOperator: {}
    template:
      pod:
        metadata:
          labels:
            istio.io/dataplane-mode: none   # entity-operator bypasses ambient mesh
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: temperature
  namespace: industrial-edge-tst-all
  labels:
    strimzi.io/cluster: dev-cluster
  annotations:
    argocd.argoproj.io/sync-wave: "4"
spec:
  partitions: 1
  replicas: 1
----

*Sync-wave ordering:* Broker pool (wave 2) → Kafka cluster (wave 3) → Topics (wave 4) → Sensor deployments (wave 5). Argo CD respects this sequence so topics exist before producers start.

Run the Industrial Edge template as `%USER_NAME%` and confirm your Gitea organization `ws-%USER_NAME%` contains the generated repository. Argo CD on east syncs the Application into namespace `industrial-edge-tst-all`. Plan B demo `demo-industrial-edge-east` offers the same topology if scaffolding is skipped.

This module is the operational heart of Part B: later observability, scaling, network policy, anomaly detection, and AI modules all assume IE workloads are running on your spoke.

[source,bash]
----
# Verify Kafka cluster is ready
oc get kafka dev-cluster -n industrial-edge-tst-all -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'

# Check topics exist
oc get kafkatopics -n industrial-edge-tst-all

# Confirm line-dashboard is serving
oc get route -n industrial-edge-tst-all -l app=line-dashboard

# Check Argo CD sync status
oc get applications -n openshift-gitops | grep industrial-edge
----""",
    "kairos-scaling": """Kairos Community on OpenShift analyzes workload metrics and recommends resource adjustments through `SmartScalingPolicy` resources — bridging the gap between Kubernetes HPA (pod-level) and infrastructure provisioning (cluster-level). The policies live in `components/kairos/templates/sensor-scan-policies.yaml`.

*SmartScalingPolicy for sensor workloads:* Two policies monitor `machine-sensor-1` and `machine-sensor-2` deployments, each with CPU and memory rules that trigger resource increases with cooldown periods:

[source,yaml]
----
# components/kairos/templates/sensor-scan-policies.yaml
apiVersion: kairos.maximilianopizarro.github.io/v1alpha1
kind: SmartScalingPolicy
metadata:
  name: scan-policy-machine-sensor-1
  namespace: kairos-system
  labels:
    kairos.io/policy-type: sensor-scan
  annotations:
    argocd.argoproj.io/sync-wave: "6"
spec:
  scope: cluster
  target:
    apiVersion: apps/v1
    kind: Deployment
    name: machine-sensor-1
    namespace: industrial-edge-tst-all
  otelEndpoint: "..."                  # OpenTelemetry collector on spoke
  prometheusEndpoint: "..."            # Prometheus metrics for analysis
  rules:
    - name: sensor-cpu-hot
      when:
        metric: container_cpu_usage_seconds_total
        operator: GreaterThan
        threshold: "70"                # 70% CPU triggers action
        for: 2m                        # sustained for 2 minutes
      action:
        type: IncreaseResources
        increaseCPUPercent: 25         # bump CPU limit by 25%
        maxCPU: "1"                    # never exceed 1 core
        cooldown: 5m                   # wait 5 min before re-evaluating
    - name: sensor-memory-hot
      when:
        metric: container_memory_working_set_bytes
        operator: GreaterThan
        threshold: "80"
        for: 2m
      action:
        type: IncreaseResources
        increaseMemoryPercent: 20
        maxMemory: 1Gi
        cooldown: 5m
  ai:
    enabled: true                      # AI-assisted recommendations
  paused: false
----

*Kairos Console:* The console is deployed on the hub via `KairosConsole` CR — operators approve or reject recommendations through a web UI:

[source,yaml]
----
# components/kairos/templates/kairos-console.yaml
apiVersion: kairos.maximilianopizarro.github.io/v1alpha1
kind: KairosConsole
metadata:
  name: kairos-console
  namespace: kairos-system
  annotations:
    argocd.argoproj.io/sync-wave: "4"
spec:
  replicas: 1
  route:
    enabled: true
    host: "kairos-console-kairos-system.{{ .Values.clusterDomain }}"
    tlsEnabled: true
----

*Hub mirror:* The App-of-Apps template passes `sensorScanPolicies.displayOnHub: true` so the hub Kairos Console can visualize spoke policy status without requiring direct spoke access — matching how ROSA customers centralize capacity decisions.

Pair this module with module 18 (HPA + Kafka) to show two layers: pods scale horizontally while Kairos evaluates resource limits.

[source,bash]
----
# List all SmartScalingPolicies across clusters
oc get smartscalingpolicy -A

# Check Kairos Console route
oc get route -n kairos-system

# See policy recommendations
oc describe smartscalingpolicy scan-policy-machine-sensor-1 -n kairos-system
----""",
    "observability": """OpenShift observability spans cluster metrics, logs, traces, and custom dashboards federated across ACM-managed clusters. Red Hat builds on Prometheus, Loki or Elasticsearch patterns, Grafana, and OpenTelemetry Instrumentation CRs so application teams inherit platform-wide collectors without sidecar sprawl on every pod.

This workshop deploys multicluster Grafana dashboards on the hub, OpenTelemetry collectors via `components/opentelemetry/`, and Kafka Console for IE topic inspection. As `%USER_NAME%`, filter dashboards to your namespace and correlate latency spikes with mesh traces in module 17.

Executives should connect this module to module 21 (Kubecost): metrics prove SLO compliance while cost metrics prove efficiency — both required for hybrid FinOps. Use Showroom `oc` to list `GrafanaDashboard` CRs and confirm IE workloads emit scrape targets. Verify with: `oc get grafanadashboard -A`.""",
    "openshift-gitops": """OpenShift GitOps installs Argo CD as a managed operator and integrates with ACM ApplicationSets to propagate manifests hub-to-spoke. The **App-of-Apps** pattern in `templates/component-applications.yaml` is the single entry point: one Application per component, each with its own sync-wave, ignoreDifferences, and Helm valuesObject. Platform teams commit desired state to Git; controllers reconcile drift automatically.

*The App-of-Apps template* iterates `.Values.connectivityLink.apps` and generates one Application per component. Notice the key patterns:

[source,yaml]
----
# templates/component-applications.yaml (simplified)
{{- range .Values.connectivityLink.apps }}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ $.Release.Name }}-{{ .id }}
  namespace: openshift-gitops
  labels:
    app.kubernetes.io/part-of: platform-hub-spoke
  annotations:
    argocd.argoproj.io/sync-wave: {{ .syncWave | quote }}     # controls deployment order
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: {{ $.Values.gitops.repoUrl }}
    targetRevision: {{ $.Values.gitops.revision }}
    path: components/{{ .path }}                               # each component in its own dir
  destination:
    server: https://kubernetes.default.svc
    namespace: {{ .destinationNamespace }}
  syncPolicy:
    automated:
      prune: {{ .prune }}
      selfHeal: {{ .selfHeal }}         # drift is auto-corrected
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
      - RespectIgnoreDifferences=true   # prevents flip-flop on operator-managed fields
{{- end }}
----

*Why `ignoreDifferences` matters:* Operators and controllers mutate fields that would cause perpetual OutOfSync. The template includes a comprehensive list — here are the critical ones:

[source,yaml]
----
# templates/component-applications.yaml — ignoreDifferences (excerpt)
ignoreDifferences:
  - kind: Service
    jsonPointers: [/spec/clusterIP, /spec/clusterIPs]
  - group: route.openshift.io
    kind: Route
    jsonPointers: [/spec/host, /status]
  - kind: Secret
    jsonPointers: [/data]                   # never drift-check secret values
  - group: sailoperator.io
    kind: Istio
    jsonPointers: [/spec/profile, /status]  # sail operator rewrites profile
  - group: rhdh.redhat.com
    kind: Backstage
    jsonPointers:                            # RHDH operator shrinks spec after sync
      - /spec/application/appConfig/configMaps
      - /spec/application/extraFiles
  - group: cluster.open-cluster-management.io
    kind: "*"
    jsonPointers: [/metadata/annotations, /metadata/labels, /status]
----

*Helm valuesObject per component:* Instead of static `values.yaml`, the template injects cluster-specific values inline. For example, `acm-hub-spoke` receives spoke API URLs and tokens:

[source,yaml]
----
# templates/component-applications.yaml — valuesObject for acm-hub-spoke
    helm:
      valuesObject:
        clusterDomain: {{ $domain }}
        managedClusters:
          east:
            apiUrl: {{ $.Values.clusters.east.apiUrl }}
            domain: {{ $eastDomain }}
          west:
            apiUrl: {{ $.Values.clusters.west.apiUrl }}
            domain: {{ $westDomain }}
----

Verify GitOps health from the Showroom terminal:

[source,bash]
----
# List all hub Applications and their sync status
oc get applications -n openshift-gitops -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status

# Check ApplicationSet for spoke propagation
oc get applicationsets -n openshift-gitops

# See which components are deployed and their sync waves
oc get applications -n openshift-gitops -o jsonpath='{range .items[*]}{.metadata.name}{" wave="}{.metadata.annotations.argocd\\.argoproj\\.io/sync-wave}{"\\n"}{end}'
----

See link:https://docs.redhat.com/en/documentation/red_hat_openshift_gitops[OpenShift GitOps documentation] for ApplicationSet patterns.""",
    "service-mesh": """OpenShift Service Mesh 3 uses ambient mode: a shared ztunnel layer handles mTLS and L4 telemetry without injecting sidecars. The entire mesh stack is defined in `components/servicemeshoperator3/templates/all.yaml` — three CRDs deploy the control plane, CNI, and ztunnel:

*Istio control plane (ambient profile):*

[source,yaml]
----
# components/servicemeshoperator3/templates/all.yaml
apiVersion: sailoperator.io/v1
kind: Istio
metadata:
  name: default
  namespace: istio-system
  annotations:
    argocd.argoproj.io/sync-wave: "1"
spec:
  namespace: istio-system
  profile: ambient                        # no sidecars — ztunnel handles mTLS
  values:
    pilot:
      env:
        PILOT_ENABLE_AMBIENT: "true"
      trustedZtunnelNamespace: ztunnel
    global:
      platform: openshift
    meshConfig:
      extensionProviders:
        - name: otel-tracing              # feeds distributed tracing (module 15)
          opentelemetry:
            service: cluster-collector-collector.openshift-opentelemetry.svc.cluster.local
            port: 4317
----

*IstioCNI + ZTunnel:* CNI configures iptables interception; ZTunnel runs as a DaemonSet handling L4 mTLS:

[source,yaml]
----
apiVersion: sailoperator.io/v1
kind: IstioCNI
metadata:
  name: default
  namespace: istio-cni
spec:
  profile: ambient
  values:
    cni:
      ambient:
        reconcileIptablesOnStartup: true   # ensures clean iptables on node restart
---
apiVersion: sailoperator.io/v1
kind: ZTunnel
metadata:
  name: default
  namespace: ztunnel
  annotations:
    argocd.argoproj.io/sync-wave: "1"
spec:
  namespace: ztunnel
----

*Namespace enrollment:* Namespaces are labeled `istio.io/dataplane-mode: ambient` at sync-wave 2 — **after** the control plane is ready (wave 1). This prevents pods from starting before ztunnel can configure HBONE (port 15008):

[source,yaml]
----
# Applied to: hub-gateway-system, developer-hub, industrial-edge-tst-all (spokes), etc.
apiVersion: v1
kind: Namespace
metadata:
  name: hub-gateway-system
  labels:
    istio.io/dataplane-mode: ambient      # automatic mTLS — zero app changes
  annotations:
    argocd.argoproj.io/sync-wave: "2"
----

*Waypoint proxies* add L7 policy where needed (AuthorizationPolicy, traffic splitting):

[source,yaml]
----
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: hub-gateway-system-waypoint
  namespace: hub-gateway-system
  labels:
    istio.io/waypoint-for: service
spec:
  gatewayClassName: istio-waypoint
  listeners:
    - name: mesh
      port: 15008
      protocol: HBONE
----

*Kafka PeerAuthentication bypass:* Strimzi brokers need permissive mTLS on inter-broker port 9092 so Kafka replication works alongside ambient mesh:

[source,yaml]
----
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: kafka-strimzi-bypass
  namespace: industrial-edge-tst-all
spec:
  selector:
    matchLabels:
      strimzi.io/cluster: dev-cluster
  mtls:
    mode: STRICT
  portLevelMtls:
    9091: { mode: DISABLE }         # Strimzi admin port
    9092: { mode: PERMISSIVE }      # Kafka broker plain listener
----

Verify from the Showroom terminal:

[source,bash]
----
# Istio control plane status
oc get istio -n istio-system

# ZTunnel DaemonSet running on all nodes
oc get ztunnel -n ztunnel

# Which namespaces are meshed
oc get ns -l istio.io/dataplane-mode=ambient

# Waypoint proxies
oc get gateways -A -l istio.io/waypoint-for=service
----

Use Kiali from the OpenShift console to view live traffic for `%USER_NAME%` deployments and validate mTLS between line-dashboard and Kafka-facing services. See link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/index[Service Mesh documentation] for ambient mode details.""",
    "scalability": """Scalability on OpenShift spans horizontal pod autoscaling, Kafka partition scaling, and node-level recommendations from Kairos. HPA v2 watches CPU, memory, or custom metrics from Prometheus adapters; KafkaNodePool resources expand broker capacity when IE topics saturate consumer lag.

In this lab, line-dashboard and related IE deployments include HPAs defined in workload manifests under `components/industrial-edge-tst/`. Trigger load via workshop scripts or simulated sensor rates, then watch pods scale in the Topology view as `%USER_NAME%`. Kafka scaling complements HPA by absorbing event bursts before pods reject traffic.

This module completes the capacity story started in module 14: Kairos proposes nodes, HPA adds pods, Kafka buffers events — together they mirror how a ROSA customer scales factory edge during production peaks without manual cluster admin intervention. Verify with: `oc get hpa -n industrial-edge-tst-all`.""",
    "network-policies": """Kubernetes NetworkPolicy on OpenShift OVN enforces micro-segmentation: only labeled pods and namespaces you explicitly allow can communicate — essential for zero-trust factory networks where compromised sensors must not lateral-move to MES backends. Red Hat OpenShift ships OVN-Kubernetes as the default CNI with policy-aware routing.

This workshop applies a demo NetworkPolicy in `industrial-edge-tst-all` from `components/workshop-demos/templates/network-policy-demo.yaml`, allowing dashboard ingress while denying unexpected cross-namespace traffic. As `%USER_NAME%`, test allowed and denied paths using `oc exec` curl probes from the Showroom terminal.

Compare to ROSA security groups plus Kubernetes NP: defense in depth at cloud VPC and pod layers. Pair this module with ACS (module 20) for runtime anomaly detection when policies are misconfigured or bypassed.

The configuration is declarative and minimal:

[source,yaml]
----
# components/workshop-demos/templates/network-policy-demo.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dashboard-ingress
  namespace: industrial-edge-tst-all
spec:
  podSelector:
    matchLabels: { app: line-dashboard }
  ingress:
    - from:
        - namespaceSelector:
            matchLabels: { network.openshift.io/policy-group: ingress }
      ports:
        - { protocol: TCP, port: 8080 }
  policyTypes: [Ingress]
----""",
    "acs-kuadrant": """Red Hat Advanced Cluster Security provides vulnerability scanning, compliance benchmarks, and runtime threat detection across ACM-managed clusters. SecuredCluster agents on spokes report to ACS Central on the hub; init bundles sync via GitOps jobs in `components/acs-init-bundle-sync/`. See link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_security_for_kubernetes[ACS documentation] for runtime policies and link:https://www.kuadrant.io/docs/[Kuadrant documentation] for API management CRDs.

Connectivity Link and Kuadrant extend API management to the hub gateway: AuthPolicy validates tokens, RateLimitPolicy protects backends, and APIProduct publishes Industrial Edge APIs for external consumers. Demo `demo-ie-api-product` in Plan B catalog exposes the same Kuadrant resources without scaffolding.

As `%USER_NAME%`, verify ACS sees your spoke workloads and test APIProduct routes through the hub gateway. Remember ACS runs outside ambient mesh — this coexistence pattern is deliberate and matches production ROSA + ACS deployments.""",
    "finops-kubecost": """Kubecost on OpenShift allocates Kubernetes spend by namespace, label, and cluster — federating data from hub primary and spoke agents into MinIO-backed ETL storage. Platform teams charge back factory edge tenants and compare ROSA node costs versus on-prem depreciation using consistent Kubernetes unit economics.

In this lab, Kubecost deploys from `components/kubecost/` with agents on east/west reporting to the hub primary. Filter allocations to namespaces owned by `%USER_NAME%` and correlate idle capacity with Kairos recommendations from module 14.

FinOps closes the executive loop from module 01: hybrid strategy without cost visibility fails in CFO review. Kubecost complements AWS Cost Explorer tags on ROSA by exposing pod-level waste inside the cluster boundary. Verify with: `oc get pods -n kubecost -l app=cost-analyzer`.""",
    "openshift-ai": """OpenShift AI on the hub runs **ModelMesh + Serverless (Knative)** via `default-dsc`. Each user owns project **`ai-%USER_NAME%`** with pre-provisioned **Jupyter notebook** `workshop-notebook`, MaaS secret, and Developer Hub catalog entity. The configuration lives in `components/openshift-ai-hub/`.

*App-of-Apps valuesObject for OpenShift AI* configures model serving modes, user projects, MCP integration, and available MaaS models — all declarative:

[source,yaml]
----
# templates/component-applications.yaml — openshift-ai-hub valuesObject
helm:
  valuesObject:
    clusterDomain: {{ $domain }}
    userCount: {{ $.Values.userCount | default 50 }}
    userProjects:
      enabled: true               # creates ai-user1..ai-userN projects
      notebook:
        enabled: true             # pre-provisions workshop-notebook per user
    dashboardExtensions:
      enabled: true
    modelServing:
      modelMeshEnabled: true      # shared multi-model serving
      serverlessEnabled: true     # KServe for dedicated single-model
      defaultDeploymentMode: ModelMesh
    mcp:
      enabled: true
      deployServer: true          # deploys ods-maas-mcp-server in maas-workshop
    maas:
      endpoint: {{ $.Values.litemaas.apiUrl }}
      apiKey: {{ $.Values.litemaas.apiKey }}
      models:
        - id: llama-scout-17b
          displayName: Llama Scout 17B (workshop default)
        - id: deepseek-r1-distill-qwen-14b
          displayName: DeepSeek R1 Distill Qwen 14B
        - id: codellama-7b-instruct
          displayName: CodeLlama 7B Instruct
----

**Overview-only (~10 min):** Catalog → **OpenShift AI — %USER_NAME%** → open dashboard; show Playground in `maas-workshop` (do not run notebook).

**Hands-on (~30 min):** Launch **workshop-notebook**, run `maas-smoke-test.ipynb`, open **AI Assistants → MCP Servers** and add `ods-maas-mcp-server` URL from ConfigMap `ods-mcp-server-registration`. In **ai-%USER_NAME%** → **Models**, confirm **`workshop-sklearn`** InferenceService (ModelMesh) is Ready; test predict from dashboard or `curl` the internal predictor URL.

[source,bash]
----
# Confirm DataScienceCluster is Ready
oc get dsc default-dsc -o jsonpath='{.status.phase}'

# Check your user project and notebook
oc get notebook,inferenceservice -n ai-%USER_NAME%

# List available MaaS models
oc get configmap ods-mcp-server-registration -n maas-workshop -o yaml

# MCP server deployment
oc get pods -n maas-workshop -l app=ods-maas-mcp-server
----

See link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI documentation] for DSC and model serving guides.""",
    "ai-gateway": """The **AI Gateway** pattern centralizes how factory, edge, and partner applications consume large language models on OpenShift. Instead of every team embedding cluster-internal URLs and shared credentials, traffic enters through **`workshop-apis.%HUB_DOMAIN%`**, backed by **link:https://gateway-api.sigs.k8s.io/[Gateway API]** `HTTPRoute` resources on the hub, the Istio ingress gateway, and **link:https://www.kuadrant.io/docs/[Kuadrant]** policies for authentication, authorization, plan tiers, and token-based rate limiting.

Three Kuadrant CRDs in `components/workshop-kuadrant-apis/templates/policies.yaml` govern the MaaS LLM endpoint — all attached to the same `HTTPRoute`:

*1. AuthPolicy — API key authentication + OPA authorization:*

[source,yaml]
----
# components/workshop-kuadrant-apis/templates/policies.yaml
apiVersion: kuadrant.io/v1
kind: AuthPolicy
metadata:
  name: workshop-maas-auth
  namespace: hub-gateway-system
  annotations:
    argocd.argoproj.io/sync-wave: "3"
spec:
  targetRef:
    group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: workshop-maas
  rules:
    authentication:
      api-key-users:
        apiKey:
          allNamespaces: true      # keys can live in any namespace
          selector:
            matchLabels:
              app: workshop-maas
        credentials:
          authorizationHeader:
            prefix: APIKEY
    response:
      success:
        filters:
          identity:
            json:
              properties:
                userid:            # extract user ID for per-user rate limiting
                  selector: auth.identity.metadata.annotations.secret\.kuadrant\.io/user-id
    authorization:
      allow-groups:
        opa:
          rego: |
            # Only "free" or "gold" plan users are authorized
            plan := object.get(input.auth.identity.metadata.annotations,
                               "secret.kuadrant.io/plan-id", "")
            allow { plan == "free" }
            allow { plan == "gold" }
----

*2. PlanPolicy — tier-based request limits via CEL predicates:*

[source,yaml]
----
apiVersion: extensions.kuadrant.io/v1alpha1
kind: PlanPolicy
metadata:
  name: workshop-maas-plans
  namespace: hub-gateway-system
spec:
  targetRef:
    group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: workshop-maas
  plans:
    - tier: free
      predicate: |
        has(auth.identity) && auth.identity.metadata.annotations["secret.kuadrant.io/plan-id"] == "free"
      limits:
        custom:
          - limit: 100
            window: 1h
    - tier: gold
      predicate: |
        has(auth.identity) && auth.identity.metadata.annotations["secret.kuadrant.io/plan-id"] == "gold"
      limits:
        custom:
          - limit: 500
            window: 1h
----

*3. TokenRateLimitPolicy — per-user token counters with CEL:*

[source,yaml]
----
apiVersion: kuadrant.io/v1alpha1
kind: TokenRateLimitPolicy
metadata:
  name: workshop-maas-token-limits
  namespace: hub-gateway-system
spec:
  targetRef:
    group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: workshop-maas
  limits:
    free:
      rates:
        - limit: {{ .Values.tokenRateLimit.free.limit }}
          window: {{ .Values.tokenRateLimit.free.window }}
      when:
        - predicate: request.path == "/llm/v1/chat/completions"
        - predicate: |
            auth.identity.metadata.annotations["secret.kuadrant.io/plan-id"] == "free" ||
            auth.identity.groups.split(",").exists(g, g == "free")
      counters:
        - expression: auth.identity.userid     # per-user counter, not global
    gold:
      rates:
        - limit: {{ .Values.tokenRateLimit.gold.limit }}
          window: {{ .Values.tokenRateLimit.gold.window }}
      when:
        - predicate: request.path == "/llm/v1/chat/completions"
        - predicate: |
            auth.identity.metadata.annotations["secret.kuadrant.io/plan-id"] == "gold"
      counters:
        - expression: auth.identity.userid
----

*The HTTPRoute + external backend pattern:* Routes use Istio `Hostname` backendRefs to reach external MaaS without in-cluster proxy images:

[source,yaml]
----
# components/workshop-kuadrant-apis/templates/routes.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: workshop-maas
  namespace: hub-gateway-system
  labels:
    kuadrant.io/exposed: "true"
spec:
  parentRefs:
    - name: hub-gateway
      namespace: hub-gateway-system
  hostnames: ["workshop-apis.{{ .Values.clusterDomain }}"]
  rules:
    - matches:
        - path: { type: PathPrefix, value: /llm }
      filters:
        - type: URLRewrite
          urlRewrite:
            hostname: {{ .Values.apis.maas.host }}
      backendRefs:
        - group: networking.istio.io
          kind: Hostname
          name: {{ .Values.apis.maas.host }}
          port: 443
----

**Hands-on (~25 min):** Mint key for `%USER_NAME%` in Developer Hub Kuadrant UI, then:

[source,bash]
----
export KEY="<your-kuadrant-api-key>"
curl -sk "https://workshop-apis.%HUB_DOMAIN%/llm/v1/chat/completions" \\
  -H "Authorization: APIKEY $KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"model":"llama-scout-17b","messages":[{"role":"user","content":"Summarize hybrid mesh in one sentence."}],"max_tokens":50}'
----

Compare response time and HTTP 429 behavior (when token limits are exceeded) to a direct call from the **workshop-notebook** in project `ai-%USER_NAME%`.

[source,bash]
----
# Verify Kuadrant policies are applied
oc get authpolicy,planpolicy,tokenratelimitpolicy -n hub-gateway-system

# Check APIProduct catalog
oc get apiproducts -n hub-gateway-system
----

See link:https://www.kuadrant.io/docs/[Kuadrant docs] and link:https://gateway-api.sigs.k8s.io/[Gateway API specification].""",
    "mcp-gateway": """**MCP Gateway** deploys Kuadrant community CRDs (`MCPGatewayExtension`, `MCPServerRegistration`), `mcp-controller`, Gateway API `Gateway`, **ArgoCD MCP**, and **k8s MCP** — pattern from test-drive-pe-oscg. Public URL: `https://mcp-gateway.%HUB_DOMAIN%/mcp`.

**Overview-only (~8 min):** Catalog → **workshop-mcp-gateway**; `oc get mcpserverregistration -n mcp-system`; Lightspeed demo prompt.

**Hands-on (~30 min):** Developer Hub **/lightspeed** — activity: "List Argo CD apps in OutOfSync state and suggest sync." Llama-stack uses `remote::mcp` to gateway (`components/developer-hub/files/lightspeed/llama-stack-run.yaml`).

The configuration is declarative and minimal:

[source,yaml]
----
# components/mcp-gateway/templates/mcp-server-registration.yaml
apiVersion: kuadrant.io/v1alpha1
kind: MCPServerRegistration
metadata:
  name: argocd-mcp
  namespace: mcp-system
spec:
  url: "http://argocd-mcp-server.mcp-system.svc:8080"
  description: "Argo CD fleet operations via MCP"
  tools:
    - name: list-applications
    - name: sync-application
    - name: get-application-health
----""",
    "llm-rag": """Large language models and retrieval-augmented generation (RAG) on OpenShift combine centralized inference with domain-specific context from factory docs, runbooks, and sensor logs — without exporting proprietary data to public SaaS. Red Hat Developer Hub Lightspeed assists developers in-catalog; Kairos Console agents answer scaling questions; Continue AI in DevSpaces suggests code inline using the same MaaS backend.

RAG architecture in hybrid manufacturing typically indexes PDFs and SOPs into a vector store (customer choice) while the LLM runs on link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI] ModelMesh or external MaaS. In this lab, you configure Lightspeed deployment in `components/developer-hub/templates/lightspeed.yaml` and test prompts against the shared MaaS endpoint — observe latency and token usage suitable for shop-floor Wi-Fi constraints.

As `%USER_NAME%`, open Developer Hub, trigger Lightspeed on a catalog Component, and compare responses with Continue AI in a DevSpaces workspace. Module 25 extends the same MaaS path to multimodal NeuroFace chat — proving one governance model serves dev, ops, and end-user AI surfaces.""",
    "text-ai-predictive": """Generative AI assists operators with natural-language summaries of alarms; predictive AI forecasts failures before downtime. On OpenShift, the ie-anomaly-alerter deployment watches Prometheus metrics from Industrial Edge sensors and emits alerts when statistical thresholds breach — a lightweight predictive pattern without mandatory KServe for this workshop track.

Optional KServe InferenceService resources on the hub demonstrate full model serving for custom scikit-learn or ONNX models trained in DS workspaces. MaaS playground endpoints let `%USER_NAME%` test generative prompts for incident postmortems: "Summarize last hour Kafka lag and ACS violations for my namespace."

Connect predictive alerts to module 26 end-user apps: Camel routes can fan out anomaly events to line-dashboard overlays and NeuroFace notifications. This closes the loop from telemetry → ML/statistical detection → human + generative AI response on the same OpenShift footprint. Verify with: `oc logs -l app=ie-anomaly-alerter -n industrial-edge-tst-all --tail=10`.""",
    "neuroface": """NeuroFace combines **OVMS local vision** (face/object detection via `components/neuroface/` with `ovms.enabled: true`) and **MaaS chat** at `/api/chat`. Hub **ModelMesh** serves platform models; NeuroFace OVMS handles low-latency webcam inference on the app namespace. See link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI documentation] for model serving patterns.

**Overview-only (~10 min):** Developer Hub → **neuroface-workshop** → Topology; open UI without webcam.

**Hands-on (~30 min):** Register as `%USER_NAME%`, test webcam + chat, inspect OVMS Service/route in namespace `neuroface`.

Catalog: System `hybrid-mesh-ai-platform` → Component **neuroface-workshop** (links UI + OpenShift AI dashboard).""",
    "ai-end-user-apps": """End-user applications — operator dashboards, mobile alerts, MES integrations — consume AI insights where work happens, not only in data science notebooks. line-dashboard on the east spoke visualizes Kafka sensor streams; Camel integrations route anomaly events; NeuroFace and MaaS summaries embed into the same UX `%USER_NAME%` sees in production rollouts.

This module integrates modules 13–25: verify line-dashboard displays live IE data, trigger ie-anomaly-alerter thresholds, and optionally embed a NeuroFace iframe or chat link for contextual AI help. Camel K Integrations from templates `demo-camel-kaoto-east` and `demo-camel-cdc-east` show event-driven patterns factory teams deploy on OpenShift alongside OT systems.

Platform teams win when AI is invisible infrastructure: OpenShift AI, MaaS, and NeuroFace become services catalog entries — app squads bind them through link:https://docs.redhat.com/en/documentation/red_hat_developer_hub[Developer Hub] dependencies without rebuilding ML pipelines per plant.""",
    "full-verification": """Full stack verification confirms Part A narrative comprehension and Part B hands-on outcomes for `%USER_NAME%`: registration redirect, Showroom terminal `oc`, ACM spoke visibility, IE sync, Kubecost allocations, DSC Ready, NeuroFace health, and progress API persistence.

Run `bash scripts/verify-workshop-e2e.sh` from the repo or follow the checklist in `verification/progress-checklist.yaml`. The workshop registration service at `https://workshop-registration.%HUB_DOMAIN%` and Showroom progress endpoint (`POST /api/progress`) must accept your module completions — facilitators use aggregate progress to pace the room.

Treat this module as your graduation gate: if any check fails, revisit the linked module or switch to Plan B shared demos documented in Developer Hub System `hybrid-mesh-shared-demos`.""",
    "agent-browser-recording": """Agent Browser automations in `verification/agent-browser/` replay workshop flows for CI-style smoke testing — navigating Developer Hub, ACM, and NeuroFace without manual clicks. Recordings support facilitator dry-runs and post-event highlights but are intentionally gitignored (`*.mp4`) per `verification/recording-runbook.md`.

Use Win+G or OBS locally to capture demos; never commit MP4 assets to `platform-hub-spoke-config`. Agent Browser YAML scripts document expected selectors and URLs with `%HUB_DOMAIN%` placeholders for forked environments.

As `%USER_NAME%`, optionally execute a read-only Agent Browser script against your assigned namespaces to validate UI regressions before executive sessions. This module closes the workshop loop: human learners, automated verification, and reproducible demo capture on OpenShift.""",
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


# Shared credential snippets (AsciiDoc)
_WORKSHOP_USER_EN = """*Username:* %USER_NAME% (e.g. `user1` after registration) +
*Password:* `Welcome123!` +
*Used for:* Developer Hub (Keycloak), OpenShift Console htpasswd (hub / east / west), DevSpaces (east spoke)"""

_FACILITATOR_GITEA_EN = """*Gitea admin (facilitator):* `gitea_admin` / `openshift`"""

# Short labels for per-module tables (full detail on index + NOTE in generator)
_WU_EN = "Workshop user"
_OAUTH_EN = "OpenShift OAuth"
_PUBLIC_EN = "Public (no login)"
_APIKEY_EN = "Kuadrant API key (module 20)"
CRED_NOTE_EN = """NOTE: *Workshop login* — %USER_NAME% / `Welcome123!` (Keycloak for Developer Hub; htpasswd for OpenShift Console on hub, east, and west; DevSpaces on east spoke). OAuth products use the same OpenShift identity."""

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


# External Red Hat / product documentation — appended after Overview in Showroom modules
LEARN_MORE_EN: dict[str, str] = {
    "index": """
* link:https://developers.redhat.com/products[Red Hat Developer — product portfolio]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_container_platform[OpenShift Container Platform documentation]
* link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes[Advanced Cluster Management (ACM) documentation]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI documentation]
* link:https://docs.redhat.com/en/documentation/red_hat_developer_hub[Red Hat Developer Hub documentation]
""",
    "hybrid-cloud-strategy": """
* link:https://www.redhat.com/en/technologies/cloud-computing/openshift/cloud-services[Red Hat OpenShift cloud services overview]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws[OpenShift Service on AWS (ROSA) documentation]
* link:https://developers.redhat.com/learn[Red Hat Developer — learning paths]
* link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes[ACM — multicluster management]
""",
    "rosa-architecture": """
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws[ROSA product documentation]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws/html-single/planning_your_environment/index[ROSA — planning your environment]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_container_platform/4.16/html/architecture/architecture-overview[OpenShift architecture overview]
* link:https://developers.redhat.com/blog/tag/openshift[Red Hat Developer blog — OpenShift]
""",
    "security-scale-hybrid": """
* link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_security_for_kubernetes[Advanced Cluster Security (ACS) documentation]
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/security_and_compliance/index[OpenShift security and compliance]
* link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.14/html/governance/governance-overview[ACM governance overview]
* link:https://www.redhat.com/en/blog/tag/security[Red Hat security blog]
""",
    "aws-ai-integration": """
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws[ROSA on AWS]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI — self-managed]
* link:https://developers.redhat.com/articles/2024/05/07/run-ai-workloads-openshift-ai[Developer article — AI workloads on OpenShift AI]
* link:https://aws.amazon.com/rosa/[AWS — Red Hat OpenShift Service on AWS]
""",
    "cases-roadmap": """
* link:https://www.redhat.com/en/success-stories[Red Hat customer success stories]
* link:https://developers.redhat.com/products/red-hat-developer-hub[Developer Hub product page]
* link:https://www.redhat.com/en/technologies/management/advanced-cluster-management[ACM product page]
""",
    "acm-multicluster": """
* link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes[ACM documentation]
* link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.14/html/clusters/index[ACM — cluster lifecycle]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_gitops[OpenShift GitOps — fleet patterns]
* link:https://access.redhat.com/labs/[Red Hat Interactive Labs]
""",
    "hybrid-mesh-architecture": """
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/index[OpenShift Service Mesh documentation]
* link:https://skupper.io/[Skupper — service interconnect]
* link:https://gateway-api.sigs.k8s.io/[Kubernetes Gateway API]
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/gateway-api-for-service-mesh[Gateway API for OpenShift Service Mesh]
""",
    "software-templates": """
* link:https://docs.redhat.com/en/documentation/red_hat_developer_hub[Developer Hub documentation]
* link:https://backstage.io/docs/features/software-templates/[Backstage Software Templates]
* link:https://developers.redhat.com/products/red-hat-developer-hub/getting-started[Developer Hub getting started]
* link:https://docs.redhat.com/en/documentation/red_hat_developer_hub/html-single/plug-ins_for_red_hat_developer_hub/index[Developer Hub plugins]
""",
    "deploy-industrial-edge": """
* link:https://www.redhat.com/en/technologies/cloud-computing/openshift/industrial-edge[Industrial Edge on OpenShift]
* link:https://docs.redhat.com/en/documentation/red_hat_amq_streams[AMQ Streams documentation]
* link:https://developers.redhat.com/topics/microservices[Microservices learning hub]
""",
    "kairos-scaling": """
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_container_platform/4.16/html/nodes/index[OpenShift nodes and scaling]
* link:https://www.redhat.com/en/technologies/management/advanced-cluster-management[ACM — capacity planning]
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/nodes/automatically-scaling-a-cluster[Cluster autoscaler documentation]
""",
    "observability": """
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/monitoring/index[OpenShift monitoring]
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/distributed_tracing/distributed-tracing-overview[Distributed tracing]
* link:https://grafana.com/docs/[Grafana documentation]
""",
    "openshift-gitops": """
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_gitops[OpenShift GitOps documentation]
* link:https://argo-cd.readthedocs.io/[Argo CD documentation]
* link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.14/html/gitops/gitops-overview[ACM GitOps overview]
""",
    "service-mesh": """
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/index[OpenShift Service Mesh]
* link:https://istio.io/latest/docs/[Istio documentation]
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/ambient-overview[Ambient mesh overview]
* link:https://kiali.io/docs/[Kiali service mesh observability]
""",
    "scalability": """
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/nodes/automatically-scaling-a-deployment[Horizontal Pod Autoscaler]
* link:https://docs.redhat.com/en/documentation/red_hat_amq_streams[AMQ Streams — Kafka on OpenShift]
""",
    "network-policies": """
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/networking/network-policies[OpenShift network policies]
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/networking/understanding-network-policies[Understanding network policies]
""",
    "acs-kuadrant": """
* link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_security_for_kubernetes[ACS documentation]
* link:https://www.kuadrant.io/docs/[Kuadrant documentation]
* link:https://docs.redhat.com/en/documentation/red_hat_developer_hub/html-single/plug-ins_for_red_hat_developer_hub/index#con-kuadrant-plugin[Developer Hub Kuadrant plugin]
* link:https://developers.redhat.com/articles/2024/08/22/api-management-kubernetes-kuadrant[Developer article — API management with Kuadrant]
""",
    "finops-kubecost": """
* link:https://docs.kubecost.com/[Kubecost documentation]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_container_platform/4.16/html/nodes/index[OpenShift capacity and nodes]
* link:https://www.redhat.com/en/blog/tag/finops[Red Hat FinOps blog tag]
""",
    "openshift-ai": """
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI documentation]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/serving_models/index[Serving models — ModelMesh and KServe]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/working_with_connected_applications/index[Connected applications and notebooks]
* link:https://developers.redhat.com/articles/2024/05/07/run-ai-workloads-openshift-ai[Run AI workloads on OpenShift AI]
* link:https://www.redhat.com/en/blog/tag/artificial-intelligence[Red Hat AI blog]
""",
    "ai-gateway": """
* link:https://www.kuadrant.io/docs/[Kuadrant — API management for Kubernetes]
* link:https://www.kuadrant.io/docs/3.2/authorino/overview/[Authorino — authentication and authorization]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/serving_models/index[OpenShift AI — model serving]
* link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/gateway-api-for-service-mesh[Gateway API on OpenShift Service Mesh]
* link:https://gateway-api.sigs.k8s.io/[Kubernetes Gateway API specification]
* link:https://docs.redhat.com/en/documentation/red_hat_developer_hub/html-single/plug-ins_for_red_hat_developer_hub/index#con-kuadrant-plugin[Developer Hub Kuadrant plugin — API keys]
* link:https://developers.redhat.com/articles/2024/08/22/api-management-kubernetes-kuadrant[API management on Kubernetes with Kuadrant]
* link:https://www.redhat.com/en/blog/building-trusted-ai-platform-openshift[Building a trusted AI platform on OpenShift]
""",
    "mcp-gateway": """
* link:https://modelcontextprotocol.io/[Model Context Protocol (MCP) specification]
* link:https://www.kuadrant.io/docs/[Kuadrant MCP Gateway extensions]
* link:https://docs.redhat.com/en/documentation/red_hat_developer_hub[Developer Hub — Lightspeed and plugins]
* link:https://developers.redhat.com/products/red-hat-developer-hub[Developer Hub product overview]
""",
    "llm-rag": """
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI documentation]
* link:https://docs.redhat.com/en/documentation/red_hat_developer_hub/html-single/plug-ins_for_red_hat_developer_hub/index#con-lightspeed-plugin[Developer Hub Lightspeed plugin]
* link:https://developers.redhat.com/articles/2024/05/07/run-ai-workloads-openshift-ai[AI workloads on OpenShift AI]
* link:https://www.redhat.com/en/topics/ai/what-is-retrieval-augmented-generation[What is RAG — Red Hat]
""",
    "text-ai-predictive": """
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/serving_models/index[Model serving on OpenShift AI]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/working_with_connected_applications/index[Notebooks and connected apps]
* link:https://www.redhat.com/en/blog/tag/artificial-intelligence[Red Hat AI blog]
""",
    "neuroface": """
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/serving_models/index[OpenShift AI model serving]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI overview]
* link:https://developers.redhat.com/articles/2024/05/07/run-ai-workloads-openshift-ai[Run AI workloads on OpenShift AI]
""",
    "ai-end-user-apps": """
* link:https://docs.redhat.com/en/documentation/red_hat_developer_hub[Developer Hub — golden paths for apps]
* link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI — production patterns]
* link:https://www.redhat.com/en/technologies/cloud-computing/openshift/industrial-edge[Industrial Edge on OpenShift]
""",
}

