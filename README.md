# Hybrid Mesh Platform

Multi-cluster GitOps platform using Red Hat Advanced Cluster Management (ACM) with Industrial Edge, Connectivity Link, and centralized observability on OpenShift.

## Architecture

![Platform hub-spoke overview — Git, ACM, Skupper VAN, and Industrial Edge on east/west](https://maximilianopizarro.github.io/platform-hub-spoke-config/assets/images/arch-overview.png)

## Cluster Sizing

Sizing recommendations based on OpenShift 4.20 provisioning parameters (multinode, demo.redhat.com).

### Hub Cluster (main branch)

The hub runs ACM, ACS Central, Developer Hub, full observability stack, data lake Kafka (3 replicas), OpenShift AI, and the F5 hub gateway. This is the heaviest cluster.

| Parameter | Recommended | Minimum |
|---|---|---|
| **cluster_size** | multinode | multinode |
| **OpenShift Version** | 4.20 | 4.17+ |
| **Worker count** | 3 | 3 |
| **Worker memory** | **32Gi** | 16Gi |
| **Worker CPU** | **8** | 4 |
| **Total cluster capacity** | **24 vCPU / 96Gi RAM** | 12 vCPU / 48Gi RAM |

<details>
<summary>Hub workload breakdown</summary>

| Component | CPU request | Memory request | Notes |
|---|---|---|---|
| ACM (MultiClusterHub) | ~2 CPU | ~8Gi | Hub controller, search, console, observability-addon |
| ACS Central (StackRox) | ~2 CPU | ~4Gi | Central + Scanner (autoscale 1-3 replicas) |
| OpenShift GitOps (ArgoCD) | ~1 CPU | ~2Gi | Server + repo + applicationset controller |
| Developer Hub (Backstage) | ~0.5 CPU | ~1.5Gi | OCM, ACS, Kubernetes, ArgoCD, Kafka plugins |
| Service Mesh 3 (Istio ambient) | ~1 CPU | ~2Gi | istiod + ztunnel (DaemonSet) + CNI |
| Connectivity Link (Kuadrant) | ~0.5 CPU | ~512Mi | Authorino + Limitador (policies disabled) |
| Observability (Grafana + Kiali + OTel) | ~1 CPU | ~2Gi | Grafana, Kiali, OpenTelemetry collector |
| Industrial Edge Data Lake (Kafka 3r) | ~3 CPU | ~6Gi | Kafka 3 replicas + ZooKeeper 3 replicas |
| MinIO | ~0.25 CPU | ~512Mi | S3 storage for ML models |
| OpenShift AI (DSC) | ~1 CPU | ~2Gi | Dashboard, KServe, ModelMesh |
| Hub Gateway (Istio) | ~0.25 CPU | ~256Mi | Gateway + HTTPRoute only |
| **Total estimated** | **~12.5 CPU** | **~29Gi** | |

</details>

### East / West Spoke Clusters (east, west branches)

Spokes run Industrial Edge workloads, sensors, factory Kafka, MirrorMaker, ACS agent, and service mesh. Lighter than hub.

| Parameter | Recommended | Minimum (demo) |
|---|---|---|
| **cluster_size** | multinode | multinode |
| **OpenShift Version** | 4.20 | 4.17+ |
| **Worker count** | 3 | 3 |
| **Worker memory** | **16Gi** | **8Gi** |
| **Worker CPU** | **4** | 4 |
| **Total cluster capacity** | **12 vCPU / 48Gi RAM** | 12 vCPU / 24Gi RAM |

<details>
<summary>Spoke workload breakdown</summary>

| Component | CPU request | Memory request | Notes |
|---|---|---|---|
| Industrial Edge TST | ~0.5 CPU | ~1Gi | Line dashboard, anomaly detection, 2 sensors |
| AMQ Broker (messaging) | ~0.5 CPU | ~1Gi | MQTT + AMQP for sensors |
| Kafka (factory, 1 replica) | ~1 CPU | ~2Gi | Factory Kafka cluster + topics |
| KafkaMirrorMaker2 | ~0.5 CPU | ~1Gi | Replicates to hub data lake |
| Stormshift sensors | ~0.25 CPU | ~256Mi | Additional sensor streams |
| ACS SecuredCluster | ~1 CPU | ~2Gi | Collector (eBPF) + admission control |
| Service Mesh 3 (ambient) | ~1 CPU | ~2Gi | istiod + ztunnel DaemonSet |
| Tekton Pipelines | ~0.25 CPU | ~512Mi | CI/CD for sensor images |
| Operators (AMQ Broker, Camel K) | ~0.5 CPU | ~1Gi | OLM-managed |
| **Total estimated** | **~5.5 CPU** | **~11Gi** | |

</details>

### Sizing for demo.redhat.com

If provisioning on **demo.redhat.com** with limited resources:

```
Hub:          3 workers x 8 vCPU x 32Gi  (ideal)
              3 workers x 4 vCPU x 16Gi  (tight, disable OpenShift AI)

East spoke:   3 workers x 4 vCPU x 8Gi   (OK for demo)
West spoke:   3 workers x 4 vCPU x 8Gi   (OK for demo)
```

To run with **8Gi workers** on the hub, use `values-lite.yaml` which disables the heaviest components (OpenShift AI, ACS, Grafana dashboards, hub gateway).

## Quick Start

### Prerequisites

- 3 OpenShift 4.17+ clusters (hub + 2 spokes)
- `helm` v3.15+
- `git`
- Cluster admin access

### 1. Fork and configure

```bash
git clone https://github.com/maximilianoPizarro/platform-hub-spoke-config.git
cd platform-hub-spoke-config

# Set your cluster domains
# values.yaml -> deployer.domain: apps.hub.example.com
# values.yaml -> clusters.east.domain: apps.east.example.com
# values.yaml -> clusters.west.domain: apps.west.example.com
```

### 2. Deploy on hub (Option A: Helm)

```bash
helm install platform-hub . \
  --set deployer.domain=apps.hub.example.com \
  --set clusters.east.domain=apps.east.example.com \
  --set clusters.west.domain=apps.west.example.com \
  -n openshift-gitops
```

### 2. Deploy on hub (Option B: ArgoCD Application)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: platform-hub-spoke
  namespace: openshift-gitops
spec:
  project: default
  source:
    repoURL: https://github.com/maximilianoPizarro/platform-hub-spoke-config.git
    targetRevision: main
    path: .
    helm:
      valuesObject:
        deployer:
          domain: apps.hub.example.com
        clusters:
          east:
            domain: apps.east.example.com
          west:
            domain: apps.west.example.com
  destination:
    server: https://kubernetes.default.svc
    namespace: openshift-gitops
```

### 3. Import managed clusters

In ACM, import east and west clusters with labels:

```yaml
# East cluster
metadata:
  labels:
    region: east
    vendor: OpenShift

# West cluster
metadata:
  labels:
    region: west
    vendor: OpenShift
```

The `Placement` resource will detect them and the `ApplicationSet` will deploy Industrial Edge workloads to both.

### 4. Validate

```bash
# Lint
helm lint .

# Template hub profile
helm template test . --set deployer.domain=apps.hub.example.com

# Template spoke profiles
helm template test . -f values-east.yaml --set deployer.domain=apps.east.example.com
helm template test . -f values-west.yaml --set deployer.domain=apps.west.example.com
```

## Branch Strategy

| Branch | Cluster | What it deploys |
|--------|---------|-----------------|
| `main` | Hub | ACM, ACS Central, Developer Hub, observability, data lake, hub gateway, GitOps |
| `east` | East spoke | Industrial Edge workloads, SecuredCluster, factory Kafka, pipelines |
| `west` | West spoke | Industrial Edge workloads, SecuredCluster, factory Kafka, pipelines |

## Value Profiles

| File | Purpose |
|------|---------|
| `values.yaml` | Hub cluster - full stack |
| `values-east.yaml` | East spoke - Industrial Edge workloads |
| `values-west.yaml` | West spoke - Industrial Edge workloads |
| `values-lite.yaml` | Minimal profile (disable heavy components for small clusters) |

## Components

| Component | Type | Sync Wave | Description |
|-----------|------|-----------|-------------|
| `openshift-gitops` | Vendored | 0 | ArgoCD configuration with custom health checks |
| `namespaces` | Vendored | 1 | Ambient labels for app namespaces; `gitea` and `stackrox` excluded (DB/init) |
| `operators` | Vendored | 2 | OLM subscriptions (Service Mesh, Pipelines, AMQ, Camel K, RHODS, etc.) |
| `acm-operator` | New | 3 | ACM Subscription + MultiClusterHub |
| `acs-operator` | New | 3 | ACS Subscription + Central CR |
| `servicemeshoperator3` | Vendored | 3 | Istio ambient mode (ztunnel L4 + waypoint L7) |
| `developer-hub` | Vendored | 3 | Backstage with OCM, ACS, K8s, ArgoCD, Kafka, Kuadrant plugins |
| `acm-hub-spoke` | New | 4 | Placement, GitOpsCluster, ApplicationSet (matrix east/west) |
| `observability` | Vendored | 5 | Grafana + Prometheus datasource |
| `kiali` | Vendored | 6 | Service mesh visualization |
| `opentelemetry` | Vendored | 6 | Distributed tracing collector |
| `rhcl-operator` | Vendored | 6 | Connectivity Link / Kuadrant (policies disabled) |
| `industrial-edge-data-lake` | Vendored | 6 | Kafka 3-replica production cluster |
| `hub-gateway` | New | 7 | Istio Gateway (F5) with weighted HTTPRoutes east/west 50/50 |
| `grafana-dashboards` | New | 8 | East-west traffic, ambient mesh, Kafka metrics |
| `acs-secured-cluster` | New | -- | SecuredCluster CR (deployed to spokes via ApplicationSet) |
| `industrial-edge-tst` | Vendored | -- | Sensors, messaging, Kafka, ML inference, line dashboard |
| `industrial-edge-stormshift` | Vendored | -- | Factory Kafka + MirrorMaker2 to hub |
| `industrial-edge-pipelines` | Vendored | -- | Tekton CI/CD for sensor images |

## Red Hat Products

- **Advanced Cluster Management (ACM)** - Multi-cluster lifecycle management
- **Advanced Cluster Security (ACS)** - CVE scanning and policy enforcement
- **OpenShift GitOps** - Argo CD for declarative deployments
- **OpenShift Service Mesh 3** - Istio ambient mode (no sidecars)
- **Connectivity Link** - Kuadrant (Gateway API, Authorino, Limitador)
- **Developer Hub** - Internal developer portal (Backstage)
- **OpenShift AI** - ML model serving (anomaly detection)
- **AMQ Streams** - Apache Kafka (Strimzi)
- **OpenShift Pipelines** - Tekton CI/CD
- **Apache Camel** - Integration (MQTT-to-Kafka)

## Documentation

Full documentation available at: https://maximilianoPizarro.github.io/platform-hub-spoke-config

## Releases (OpenShift 4.20)

| Tag | Notes |
|-----|--------|
| [`ocp-420-v4`](docs/RELEASE-OCP-4.20-v4.md) | Current — Camel Dashboard on east/west spokes (Helm 4.20.2) |
| [`ocp-420-v3`](docs/RELEASE-OCP-4.20-v3.md) | Skupper token sync, Kafka/Kiali fixes, Camel K registry, IE route hosts |
| `ocp-420-v2` | RHDH Topology + Scaffolder |
| `ocp-420` | Initial OCP 4.20 baseline |

Pin GitOps: set `targetRevision: ocp-420-v4` on hub/spoke Argo CD Applications.

## Contributing

See `CONTRIBUTING.md` for branch strategy, validation requirements, and Developer Hub/scaffolder contribution checks.

## CI Pipeline

GitHub Actions runs on push/PR to `main`, `east`, `west`:
- `helm lint` on parent chart and all sub-charts
- `helm template` for hub, east, and west profiles
- YAML validation with `yamllint`
- ArgoCD preflight checks (hardcoded URLs, duplicate apps, sync-wave audit)

## License

Apache License 2.0
