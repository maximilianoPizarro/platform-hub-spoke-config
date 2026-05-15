---
layout: default
title: Industrial Edge
nav_order: 8
---

# Industrial Edge

The **Industrial Edge** validated pattern models discrete manufacturing and operational technology (OT) connectivity to Kubernetes: sensors, MQTT, Kafka-centric pipelines, CI/CD for edge software, and ML-assisted insights.

## Factory pattern

Factories emit telemetry through brokers and integrations. Kubernetes namespaces isolate teams while GitOps keeps spoke clusters aligned with approved revisions.

## Data stack

| Stage | Component |
| ----- | ---------- |
| Ingress | MQTT brokers (AMQ Broker), Camel K bridges |
| Streaming | AMQ Streams / Kafka topics |
| Processing | OpenShift AI or lightweight scoring services |
| Visualization | Grafana dashboards |

## Links

- [Industrial Edge Validated Pattern](https://validatedpatterns.io/patterns/industrial-edge)

Related charts: `industrial-edge-tst`, `industrial-edge-stormshift`, `industrial-edge-pipelines`, hub-side data lake charts when enabled.
