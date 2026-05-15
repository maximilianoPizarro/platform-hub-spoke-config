---
layout: default
title: Advanced Cluster Security
parent: Red Hat Products
nav_order: 3
---

# Advanced Cluster Security

Red Hat **Advanced Cluster Security for Kubernetes (ACS)** centralizes Kubernetes-native security: build-time image scanning, deployment-time policy, and runtime detection.

## Topology for hub-spoke

| Component | Location | Role |
| --------- | -------- | ---- |
| **Central** | Hub | Policy console, vulnerability DB integration, admission coordination |
| **SecuredCluster** | Spokes | Sensors collecting runtime and orchestrator events |

## Capabilities used

- **CVE scanning** for images referenced by Industrial Edge and platform workloads.
- **Risk prioritization** across many namespaces and clusters.
- **Network and process baselines** optional hardening for regulated factories.

## Documentation

- [Red Hat Advanced Cluster Security for Kubernetes 4.10](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_security_for_kubernetes/4.10)

Chart paths: `components/acs-operator` (hub central install), `components/acs-secured-cluster` (spoke agents) when enabled.
