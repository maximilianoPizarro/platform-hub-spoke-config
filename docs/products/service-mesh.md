---
layout: default
title: Service Mesh 3
parent: Red Hat Products
nav_order: 5
---

# OpenShift Service Mesh 3

Red Hat **OpenShift Service Mesh 3** targets **ambient mesh** patterns that reduce mandatory sidecars while preserving security and observability building blocks.

## Ambient mode concepts

| Piece | Purpose |
| ----- | ------- |
| **ztunnel** | Handles transparent encryption and L4 policy on the node dataplane. |
| **Waypoint** | Optional L7 proxy for fine-grained HTTP policy where needed. |
| **Control plane** | Istio-based control plane integrated with OpenShift lifecycle. |

## Multi-cluster considerations

- Align **trust domains** and federation patterns with your ACM cluster naming.
- Start with namespaces that benefit from east-west identity (Industrial Edge services, Kafka clients).

## Documentation

- [OpenShift Service Mesh 3.0](https://docs.redhat.com/en/documentation/openshift_service_mesh/3.0)

Operator chart path: `components/servicemeshoperator3`.
