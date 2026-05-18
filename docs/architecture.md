---
layout: default
title: Architecture
nav_order: 2
---

# Architecture

## Hub-spoke theory in multi-cluster Kubernetes

In multi-cluster Kubernetes, a **hub-spoke** model designates one administrative cluster (the **hub**) and one or more workload clusters (**spokes**). The hub owns fleet APIs: cluster inventory, policy placement, credentials for spoke registration, and often centralized GitOps controllers that fan out desired state.

Spokes remain the execution venues for application namespaces, data-plane components (Kafka, MQTT bridges, mesh dataplane), and regional isolation for latency, data residency, or blast-radius control.

## Why hub-spoke?

| Benefit | Description |
| --------|------------- |
| **Centralized management** | One control plane for membership, RBAC patterns, and bulk upgrades. |
| **Policy enforcement** | Kubernetes policies, compliance checks, and security baselines propagate from the hub. |
| **Observability** | Aggregated metrics, logging, and tracing strategies start at the hub and uniform dashboards span spokes. |
| **GitOps consistency** | A single Git revision strategy (with branch or overlay variants) drives spoke drift correction. |

## Platform architecture overview

```mermaid
flowchart TB
  subgraph Git["Git Repository (main branch)"]
    REPO["platform-hub-spoke-config"]
  end

  subgraph Hub["Hub Cluster"]
    direction TB
    ARGO["OpenShift GitOps<br/>(ArgoCD)"]
    ACM["Advanced Cluster<br/>Management"]
    APPSET["ApplicationSet<br/>(matrix generator)"]
    GW["Hub Gateway<br/>(Gateway API + Istio)"]
    GRAFANA["Grafana<br/>(multi-cluster dashboards)"]
    KAFKA_C["Kafka Console"]
    KIALI_H["Kiali + OSSM Console"]
    ACS_C["ACS Central"]
    DEVHUB["Developer Hub"]
    SKUPPER_H["Skupper Hub Site<br/>(Listeners)"]
    RHCL["Connectivity Link"]
  end

  subgraph East["East Spoke"]
    direction TB
    IE_E["Industrial Edge<br/>(sensors, MQTT, Kafka, ML)"]
    SGW_E["Spoke Gateway"]
    SKUPPER_E["Skupper Spoke Site<br/>(Connectors)"]
    GRAFANA_E["Grafana (local)"]
    KIALI_E["Kiali + OSSM Console"]
    MESH_E["OSSM3 Ambient<br/>(ztunnel)"]
  end

  subgraph West["West Spoke"]
    direction TB
    IE_W["Industrial Edge<br/>(sensors, MQTT, Kafka, ML)"]
    SGW_W["Spoke Gateway"]
    SKUPPER_W["Skupper Spoke Site<br/>(Connectors)"]
    GRAFANA_W["Grafana (local)"]
    KIALI_W["Kiali + OSSM Console"]
    MESH_W["OSSM3 Ambient<br/>(ztunnel)"]
  end

  REPO --> ARGO
  ARGO --> ACM
  ARGO --> APPSET
  APPSET -->|"spoke apps"| East
  APPSET -->|"spoke apps"| West
  ACM ---|"fleet mgmt"| East
  ACM ---|"fleet mgmt"| West
  GW -->|"front/api traffic"| East
  GW -->|"front/api traffic"| West
  SKUPPER_E <-->|"VAN link"| SKUPPER_H
  SKUPPER_W <-->|"VAN link"| SKUPPER_H
  SKUPPER_H -->|"metrics"| GRAFANA
  SGW_E --> SKUPPER_E
  SGW_W --> SKUPPER_W
```

## Components on the hub vs spokes

| Area | Hub | Spokes |
| -----|-----|--------|
| ACM hub operator & APIs | yes | |
| ArgoCD / App-of-Apps root | yes | |
| ApplicationSet (spoke apps) | yes | |
| ACS Central | yes | |
| ACS Secured Cluster | | yes |
| Developer Hub | yes | |
| Hub Gateway (Gateway API) | yes | |
| Spoke Gateway (Gateway API) | | yes |
| Industrial Edge workloads | | yes |
| Kafka brokers (regional) | optional | yes |
| Service Mesh ambient / ztunnel | yes | yes |
| Istio CNI (`profile: ambient`) | yes | yes |
| Skupper Site (hub listeners) | yes | |
| Skupper Site (spoke connectors) | | yes |
| Grafana (multi-cluster dashboards) | yes | |
| Grafana (local metrics) | | yes |
| Kiali + OSSM Console plugin | yes | yes |
| Connectivity Link (RHCL) | yes | yes |

## GitOps application delivery flow

```mermaid
sequenceDiagram
  participant Git as Git Repository
  participant Argo as ArgoCD (Hub)
  participant Hub as Hub Cluster
  participant AppSet as ApplicationSet
  participant East as East Spoke
  participant West as West Spoke

  Git->>Argo: Webhook / poll (main branch)
  Argo->>Hub: Sync hub components<br/>(operators, gateway, observability)
  Argo->>AppSet: Render matrix (cluster x component)
  AppSet->>East: Create spoke Applications<br/>(namespaces, operators, IE, kiali...)
  AppSet->>West: Create spoke Applications<br/>(namespaces, operators, IE, kiali...)
  East-->>Argo: Health + sync status
  West-->>Argo: Health + sync status
```

## Sync wave ordering

Components deploy in strict order via ArgoCD sync waves:

```mermaid
flowchart LR
  W0["Wave 0<br/>GitOps bootstrap"] --> W1["Wave 1<br/>Namespaces, RBAC"]
  W1 --> W2["Wave 2<br/>Operators (OLM)"]
  W2 --> W3["Wave 3<br/>Platform<br/>(Mesh, ACM, ACS)"]
  W3 --> W4["Wave 4<br/>ACM hub-spoke<br/>bindings"]
  W4 --> W5["Wave 5<br/>Observability,<br/>Industrial Edge"]
  W5 --> W6["Wave 6<br/>Apps,<br/>Connectivity Link"]
  W6 --> W7["Wave 7<br/>Hub Gateway,<br/>routing"]
  W7 --> W8["Wave 8<br/>Dashboards,<br/>presentation"]
```

## Service Interconnect (Skupper) topology

Red Hat Service Interconnect creates a Virtual Application Network (VAN) that bridges services across clusters without VPN or direct network connectivity.

```mermaid
flowchart LR
  subgraph Hub["Hub Cluster"]
    SITE_H["Skupper Site<br/>(hub)"]
    L1["Listener<br/>ie-gateway-east:8080"]
    L2["Listener<br/>ie-gateway-west:8080"]
    L3["Listener<br/>prometheus-east:9091"]
    L4["Listener<br/>prometheus-west:9091"]
    AG["AccessGrant<br/>(spoke-link)"]
  end

  subgraph East["East Spoke"]
    SITE_E["Skupper Site<br/>(east)"]
    AT_E["AccessToken<br/>(hub-token)"]
    C1_E["Connector<br/>ie-gateway-east"]
    C2_E["Connector<br/>prometheus-east"]
    SGW_E["Spoke Gateway<br/>:8080"]
    TQ_E["Thanos Querier<br/>:9091"]
  end

  subgraph West["West Spoke"]
    SITE_W["Skupper Site<br/>(west)"]
    AT_W["AccessToken<br/>(hub-token)"]
    C1_W["Connector<br/>ie-gateway-west"]
    C2_W["Connector<br/>prometheus-west"]
    SGW_W["Spoke Gateway<br/>:8080"]
    TQ_W["Thanos Querier<br/>:9091"]
  end

  AG -.->|"claim"| AT_E
  AG -.->|"claim"| AT_W
  AT_E -->|"TLS link"| SITE_H
  AT_W -->|"TLS link"| SITE_H
  C1_E -->|"routingKey"| L1
  C2_E -->|"routingKey"| L3
  C1_W -->|"routingKey"| L2
  C2_W -->|"routingKey"| L4
  SGW_E --> C1_E
  TQ_E --> C2_E
  SGW_W --> C1_W
  TQ_W --> C2_W
```

## Spoke gateway aggregation

Each spoke runs a **Gateway API gateway** that fronts all Industrial Edge services, providing a single entry point for Skupper to expose to the hub.

```mermaid
flowchart LR
  subgraph Spoke["Spoke Cluster"]
    GW["spoke-gateway<br/>(Gateway API)"]
    FE["line-dashboard<br/>(frontend)"]
    AD["anomaly-detection<br/>(ML inference)"]
    MSG["messaging<br/>(MQTT/AMQP)"]
    KAFKA["kafka-bootstrap"]
  end

  GW -->|"/frontend"| FE
  GW -->|"/anomaly"| AD
  GW -->|"/messaging"| MSG
  GW -->|"/kafka"| KAFKA

  SKUPPER["Skupper Connector"] --> GW
```

## Multi-cluster observability pipeline

```mermaid
flowchart TB
  subgraph East["East Spoke"]
    PROM_E["Prometheus /<br/>Thanos Querier"]
    ISTIO_E["Istio metrics"]
    KAFKA_E["Kafka metrics"]
    ISTIO_E --> PROM_E
    KAFKA_E --> PROM_E
  end

  subgraph West["West Spoke"]
    PROM_W["Prometheus /<br/>Thanos Querier"]
    ISTIO_W["Istio metrics"]
    KAFKA_W["Kafka metrics"]
    ISTIO_W --> PROM_W
    KAFKA_W --> PROM_W
  end

  subgraph Hub["Hub Cluster"]
    PROM_H["Prometheus /<br/>Thanos Querier"]
    GRAFANA["Grafana"]
    DS_H["Datasource: Hub"]
    DS_E["Datasource: East<br/>(via Skupper)"]
    DS_W["Datasource: West<br/>(via Skupper)"]
    GRAFANA --> DS_H --> PROM_H
    GRAFANA --> DS_E
    GRAFANA --> DS_W
  end

  PROM_E -->|"Skupper VAN<br/>prometheus-east:9091"| DS_E
  PROM_W -->|"Skupper VAN<br/>prometheus-west:9091"| DS_W
```

## Data flow (sensors to dashboard)

```mermaid
flowchart LR
  S["Sensors / OPC-UA / PLC"] --> M["MQTT broker<br/>(AMQ)"]
  M --> C["Camel K<br/>integration"]
  C --> K["Kafka<br/>(AMQ Streams)"]
  K --> ML["OpenShift AI<br/>scoring"]
  ML --> DB["Grafana<br/>dashboards"]
  K --> DB
  K -->|"MirrorMaker"| DL["Data Lake<br/>(S3 / MinIO)"]
```

## Comparison with Red Hat Validated Patterns

The **[Multicloud GitOps](https://validatedpatterns.io/patterns/multicloud-gitops)** validated pattern demonstrates fleet GitOps with OpenShift GitOps and ACM patterns that resemble this repository's hub-push model: a declarative root Application, cluster grouping, and progressive rollout.

This platform extends that idea with **Industrial Edge** workloads, **Service Mesh ambient**, **Connectivity Link**, optional **OpenShift AI**, **ACS** depth, and **Service Interconnect** for cross-cluster service exposure -- tuned for factory-style telemetry and east-west observability rather than only infrastructure provisioning.

## Official documentation

- [ACM Architecture](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.16/html/about/welcome-to-red-hat-advanced-cluster-management-for-kubernetes)
- [Multicloud GitOps Pattern](https://validatedpatterns.io/patterns/multicloud-gitops)
- [Red Hat Service Interconnect](https://docs.redhat.com/en/documentation/red_hat_service_interconnect/2.1)
- [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/)
- [Argo CD ApplicationSet Generators](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators/)
