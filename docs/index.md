---
layout: default
title: Home
nav_order: 1
---

# Hybrid Mesh Platform

> **Your journey:** This platform deploys in one `helm upgrade`, connects three OpenShift clusters (hub + east + west), and shows IoT sensor data across Grafana and Developer Hub within about 30 minutes. The pages below follow one continuous story — concept, install, operate, scaffold — so you can read straight through or jump to any chapter.

**Multi-cluster GitOps platform using Red Hat products** — a hub-spoke topology that centralizes governance with Red Hat Advanced Cluster Management (ACM), delivers Industrial Edge workloads on regional spokes, uses OpenShift Service Mesh in ambient mode for east-west connectivity, layers Connectivity Link (Kuadrant) for API-aware ingress policy, exposes Grafana dashboards for cross-cluster visibility, and integrates Advanced Cluster Security (ACS) for vulnerability and runtime protection.

Read **concept → mechanics → operations**: start with [Architecture](architecture.md), install via [Getting Started](getting-started.md) or [Deploy with ACM and GitOps](deploy-acm-gitops.md), scaffold workloads via [Scaffolding](scaffolding.md), then use platform chapters (**Hub Gateway**, **Observability**, **Industrial Edge**) before drilling into individual **[Red Hat Products](products/)**.

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

![Platform hub-spoke overview — Git, ACM, Skupper VAN, and Industrial Edge on east/west]({{ site.baseurl }}/assets/images/arch-overview.png)
{: .mb-4 }
*Hub cluster aggregates observability and Developer Hub; east and west spokes run Industrial Edge workloads connected via Service Interconnect (Skupper). Click the image to zoom.*
{: .fs-2 .text-grey-dk-000 }

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
| Scaffolding | [Scaffolding](scaffolding.md) |
| Troubleshooting | [Troubleshooting](troubleshooting.md) |
| Service Interconnect | [Service Interconnect](service-interconnect.md) |
| Branch strategy | [Branch Strategy](branch-strategy.md) |

## Recommended reading order

1. [Architecture](architecture.md) — mental model of hub, spokes, GitOps, and observability  
2. [Getting Started](getting-started.md) or [Deploy with ACM and GitOps](deploy-acm-gitops.md) — bring clusters under GitOps  
3. [Scaffolding](scaffolding.md) — deploy Industrial Edge instances on east/west from Developer Hub  
4. [Hub Gateway](hub-gateway.md) — weighted ingress and circuit breaking across spokes  
5. [Observability](observability.md) — Grafana, Kiali, Kafka Console  
6. [Industrial Edge](industrial-edge.md) — factory data pipeline: sensors, Kafka, Camel, ML  
7. [Red Hat Products](products/index.md) — per-operator deep dives and discovery annotations

Screenshots and architecture diagrams support **click-to-zoom** in a full-screen modal — handy after deploying dashboards.

**Next →** [Architecture](architecture.md) — understand how Git, ACM, and Skupper wire the three clusters together.

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
- Red Hat OpenShift Dev Spaces (spoke IDEs — Kaoto, Continue AI)
- Red Hat OpenShift Virtualization (KubeVirt / CNV workshop)
- Red Hat Quay (container registry on hub)
- Gitea (in-cluster Git for scaffolder repos)
- Streams for Apache Kafka Console (hub fleet UI)
- Red Hat Service Interconnect (Skupper)
- Mailpit (SMTP testing for notifications)
- Observability stack (Prometheus-compatible metrics, Grafana, OpenTelemetry, Kiali)
