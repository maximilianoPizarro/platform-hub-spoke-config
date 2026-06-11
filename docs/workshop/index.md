---
layout: default
title: Hybrid Mesh AI Workshop
has_children: true
nav_order: 11
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`



# Hybrid Mesh AI Workshop



Welcome to the *Hybrid Mesh AI Workshop* — a dual-track experience that mirrors how Red Hat customers run hybrid cloud on OpenShift.

*Part A (modules 01–05)* is executive-oriented: it covers hybrid cloud strategy, ROSA architecture, security at scale, AWS AI integration, and real customer cases. No hands-on required — facilitators can demo while the audience follows along.

*Part B (modules 10–28)* is fully hands-on on a live RHDP hub-spoke fleet provisioned for this workshop. Each module targets a specific product area and includes a `verify` step to confirm your work.

The lab simulates a production hybrid mesh: a hub cluster (OpenShift on AWS) managing two spoke clusters (east and west) via ACM, with ambient service mesh, GitOps, and an AI inference layer backed by OpenShift AI + MaaS.

Register at `https://workshop-registration.%HUB_DOMAIN%` to receive your lab identity (`userN`). The Showroom at `https://showroom-showroom.%HUB_DOMAIN%` embeds an authenticated `oc` terminal — no local kubeconfig required. If scaffolding fails, use *Plan B* shared demos in Developer Hub → System `hybrid-mesh-shared-demos`.



## Hub-spoke architecture

The workshop fleet is a three-cluster hub-spoke topology managed by ACM:

```yaml
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
```

```yaml
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
```

The hub runs: ACM, OpenShift GitOps (Argo CD), Developer Hub, OpenShift AI, Service Mesh control plane, Skupper, Kuadrant, ACS Central, Grafana, and Kubecost. +
The east spoke runs: Industrial Edge workloads, DevSpaces, Kairos, and spoke-local Argo CD agents. +
The west spoke runs: additional workload replicas and demonstrates cross-cluster traffic via Skupper.



## Service mesh & traffic flow

The workshop uses OpenShift Service Mesh 3 in *ambient mode* (no sidecars). Traffic between hub and spokes crosses a Skupper tunnel exposed via Gateway API:

```yaml
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
```

```yaml
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
```



## OpenShift AI — Model as a Service

The AI layer is a shared LLM endpoint (MaaS) deployed on the hub via the OpenShift AI operator. All AI modules (22–26) consume this endpoint.

```yaml
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
```

```yaml
# Secret — OpenAI-compatible base URL pointing to the in-cluster MaaS
apiVersion: v1
kind: Secret
metadata:
  name: maas-api-key
  namespace: maas-workshop
stringData:
  OPENAI_API_BASE: "http://maas-api.maas-workshop.svc.cluster.local:8080/v1"
  OPENAI_API_KEY: "workshop-key-%USER_NAME%"
```

Any application that speaks the OpenAI REST API can consume MaaS without code changes — just point `OPENAI_API_BASE` to the in-cluster service.



## Kuadrant API gateway

Kuadrant manages API rate limiting and auth policies across the hub gateway. Each workshop user gets their own API key scoped to a plan:

```yaml
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
```

```yaml
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
```



[[#hybrid-integration]]
## Hybrid cloud integration notes

Workshop patterns apply to OpenShift on-premises, at the edge, or on public cloud. This lab uses a pre-provisioned RHDP hub-spoke fleet — use the snippets below when you need to provision or attach similar services in AWS or Azure.

### AWS — attach clusters and integrate services

```bash
# Example: create ROSA cluster (or use existing EKS/ROSA) and import to ACM hub
rosa create cluster --cluster-name=factory-edge --region=us-east-1
# ACM: cluster import / ManagedCluster — see module 10
aws iam create-open-id-connect-provider ...   # OIDC for cloud integrations
aws s3 mb s3://my-data-lake                   # analog to MinIO data lake on hub
```

### Azure — attach AKS and optional AI endpoints

```bash
az aks create --resource-group rg-workshop --name aks-edge --node-count 3
# Import to ACM hub (ManagedCluster) — same GitOps placement as east/west spokes
# Azure OpenAI can replace MaaS for inference; lab uses OpenShift AI + MaaS (module 22)
```

Hands-on equivalents: ACM fleet (module 10), Kuadrant API gateway (module 20), OpenShift AI + MaaS (modules 22–25).



## Dual agenda



**Part A (01–05)** — Executive strategy modules.



**Part B (10–28)** — Hands-on labs on the live RHDP fleet (~4 h).



Facilitator-only modules 29–30 stay in-cluster Showroom only.



## Live vs this mirror



| Surface | URL | Notes |

|---------|-----|-------|

| **Showroom (hands-on)** | `https://showroom-showroom.YOUR_HUB_DOMAIN/` | Antora + embedded `oc` terminal |

| **Registration** | `https://workshop-registration.YOUR_HUB_DOMAIN/` | Assigns `userN` |

| **GitHub Pages (read-only)** | [Workshop mirror]({{ site.baseurl }}/workshop/) | This section |

| **Antora source** | [showroom-hybrid-mesh-ai](https://github.com/maximilianoPizarro/showroom-hybrid-mesh-ai) | Regenerate with `python scripts/generate-workshop-content.py` |



*Screen recordings are not published in this repository.*
