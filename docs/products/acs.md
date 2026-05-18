---
layout: default
title: Advanced Cluster Security
parent: Red Hat Products
nav_order: 3
---

# Advanced Cluster Security

Red Hat **Advanced Cluster Security for Kubernetes (ACS)** centralizes Kubernetes-native security: build-time image scanning, deployment-time policy, and runtime detection.

**Git path:** `components/acs-operator/` (hub), `components/acs-secured-cluster/` (hub + spokes)

![ACS Central – Cluster registration]({{ site.baseurl }}/assets/images/ACS.png)
{: .mb-4 }
*ACS Central — hub and spoke clusters registered (hub, east, west).*
{: .fs-2 .text-grey-dk-000 }

## Topology for hub-spoke

| Component | Location | Role |
| --------- | -------- | ---- |
| **Central** | Hub | Policy console, vulnerability DB integration, admission coordination |
| **SecuredCluster** | Hub + spokes | Sensor, collector, and admission control per cluster |

Hub and spokes register with Central using **init bundles** (TLS secrets in namespace `stackrox`). Generate once per cluster from Central:

```bash
roxctl -e central.stackrox:443 --password "$ROX_ADMIN_PASSWORD" --insecure-skip-tls-verify \
  central init-bundles generate <cluster-name> --output-secrets - | oc apply -n stackrox -f -
```

Cluster names: `hub`, `east`, `west`. The `rhacs-operator` subscription on spokes is deployed via `openshift-operators` (ApplicationSet `subscriptions` list).

## Capabilities used

- **CVE scanning** for images referenced by Industrial Edge and platform workloads.
- **Risk prioritization** across many namespaces and clusters.
- **Network and process baselines** optional hardening for regulated factories.

## Documentation

- [Red Hat Advanced Cluster Security for Kubernetes 4.10](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_security_for_kubernetes/4.10)

Chart paths: `components/acs-operator` (hub central install), `components/acs-secured-cluster` (spoke agents) when enabled.
