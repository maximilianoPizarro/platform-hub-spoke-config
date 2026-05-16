---
layout: default
title: Home
nav_order: 1
---

# Platform Hub-Spoke Config

**Multi-cluster GitOps platform using Red Hat products** -- a hub-spoke topology that centralizes governance with Red Hat Advanced Cluster Management (ACM), delivers Industrial Edge workloads on regional spokes, uses OpenShift Service Mesh in ambient mode for east-west connectivity, layers Connectivity Link (Kuadrant) for API-aware ingress policy, exposes Grafana dashboards for cross-cluster visibility, and integrates Advanced Cluster Security (ACS) for vulnerability and runtime protection.

## Overview

This repository models a **GitOps-first platform** where:

- **Hub cluster** runs ACM, OpenShift GitOps (Argo CD), observability aggregation, Developer Hub, ACS Central, Mailpit for notifications, and gateway-style HTTP routing with **circuit breaking** for shared services.
- **Spoke clusters** (east/west regions) host **Industrial Edge** patterns: sensor and MQTT-style ingestion, Kafka pipelines, optional ML scoring, and dashboards fed by Prometheus-compatible metrics.
- **Service Mesh 3 ambient** reduces sidecar overhead while retaining ztunnel-based L4 and waypoint-based L7 policy where needed.
- **Hub Gateway** splits traffic into **front** and **API** services per spoke, with per-service **circuit breaking** via `DestinationRule`.
- **Service Interconnect (Skupper)** bridges spoke services and metrics to the hub via a Virtual Application Network, without VPN or firewall changes.
- **Spoke Gateways** aggregate Industrial Edge services per spoke for simplified cross-cluster exposure.
- **Kiali + OSSM Console** provides service mesh topology visualization on every cluster via the OpenShift Console plugin.
- **Grafana dashboards** roll up cluster and application signals from all clusters.
- **ACS** provides centralized policy, CVE visibility, and SecuredCluster agents on spokes.

```mermaid
flowchart TB
  subgraph Hub["Hub Cluster"]
    ARGO["ArgoCD / GitOps"]
    ACM["ACM"]
    GW["Hub Gateway<br/>(Gateway API)"]
    SKUPPER_H["Skupper<br/>(Listeners)"]
    OBS["Grafana<br/>(multi-cluster)"]
    KIALI_H["Kiali"]
    ACS_C["ACS Central"]
  end

  subgraph East["East Spoke"]
    IE_E["Industrial Edge<br/>(sensors → MQTT → Kafka → ML)"]
    SGW_E["Spoke Gateway"]
    SKUPPER_E["Skupper<br/>(Connectors)"]
    GRAFANA_E["Grafana (local)"]
    KIALI_E["Kiali"]
  end

  subgraph West["West Spoke"]
    IE_W["Industrial Edge<br/>(sensors → MQTT → Kafka → ML)"]
    SGW_W["Spoke Gateway"]
    SKUPPER_W["Skupper<br/>(Connectors)"]
    GRAFANA_W["Grafana (local)"]
    KIALI_W["Kiali"]
  end

  Git[(Git repo)] --> ARGO
  ARGO --> ACM
  ACM -->|"ApplicationSet"| East
  ACM -->|"ApplicationSet"| West
  GW -->|"front/api + circuit breaking"| East
  GW -->|"front/api + circuit breaking"| West
  SKUPPER_E <-->|"VAN"| SKUPPER_H
  SKUPPER_W <-->|"VAN"| SKUPPER_H
  SKUPPER_H -->|"metrics"| OBS
  SGW_E --> SKUPPER_E
  SGW_W --> SKUPPER_W
```

## Quick links

| Topic | Page |
| ------ | ------ |
| Architecture deep dive | [Architecture](architecture.md) |
| Install flow | [Getting Started](getting-started.md) |
| ACM + GitOps | [Deploy with ACM and GitOps](deploy-acm-gitops.md) |
| Red Hat products | [Red Hat Products](products/) |
| Hub Gateway | [Hub Gateway](hub-gateway.md) |
| Observability | [Observability](observability.md) |
| Industrial Edge | [Industrial Edge](industrial-edge.md) |
| Service Interconnect | [Service Interconnect](service-interconnect.md) |
| Branch strategy | [Branch Strategy](branch-strategy.md) |

## Red Hat products used

- Red Hat OpenShift Container Platform
- Red Hat Advanced Cluster Management for Kubernetes
- Red Hat OpenShift GitOps (Argo CD)
- Red Hat Advanced Cluster Security for Kubernetes
- Red Hat OpenShift Service Mesh
- Red Hat Connectivity Link (Kuadrant, Gateway API)
- Red Hat OpenShift AI
- Red Hat AMQ Streams (Apache Kafka)
- Red Hat build of Apache Camel / Camel K
- Red Hat OpenShift Pipelines (Tekton)
- Red Hat Developer Hub (Backstage)
- Red Hat Service Interconnect (Skupper)
- Mailpit (SMTP testing for notifications)
- Observability stack (Prometheus-compatible metrics, Grafana, OpenTelemetry, Kiali)
