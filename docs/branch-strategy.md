---
layout: default
title: Branch Strategy
nav_order: 9
---

# Branch Strategy

This repository follows a **single-branch, multi-directory model**: all configuration lives on `main` and cluster-specific configuration is handled via **dedicated folders** per cluster.

## Repository layout

```
.              → Hub cluster (root Helm chart)
east/          → East spoke cluster (self-contained Helm chart)
west/          → West spoke cluster (self-contained Helm chart)
components/    → Shared component charts referenced by all clusters
```

Each directory (`east/`, `west/`) is an independent Helm chart with its own `Chart.yaml`, `values.yaml`, and `templates/`. The hub uses the repository root (`.`) as its chart.

## How it works

| Path / File | Purpose |
| ----------- | ------- |
| `values.yaml` | Hub cluster -- operators, observability, gateway, hub-only components |
| `east/values.yaml` | East spoke -- full component list, subscriptions, domain configuration |
| `west/values.yaml` | West spoke -- full component list, subscriptions, domain configuration |
| `values-lite.yaml` | Minimal hub profile -- fewer subscriptions, lighter footprint for demos |
| `components/` | Shared Helm charts used by hub and spoke Application CRs |

The **ACM ApplicationSet** (`components/acm-hub-spoke/templates/applicationset.yaml`) uses a `clusterDecisionResource` generator to deploy each spoke's folder to the remote cluster:

```yaml
source:
  path: '{{name}}'       # resolves to east/ or west/
destination:
  name: '{{name}}'       # deploys to remote spoke via cluster secret
```

Each spoke chart generates child Application CRs that the **spoke's own Argo CD** syncs locally.

## Adding a new cluster

1. **Provision** the OpenShift cluster and import it into ACM.
2. **Label** the `ManagedCluster` for placement selectors (`region=<name>`, `cluster.open-cluster-management.io/clusterset=global`).
3. **Create a folder** (e.g. `south/`) by copying `east/` and adjusting `clusterName`, `deployer.domain`, and `clusters.hub.domain` in `values.yaml`.
4. **Add the cluster domain** to hub `values.yaml` under `clusters.<name>.domain`.
5. **Register the spoke** as an Argo CD cluster secret on the hub.
6. **Run** `helm template` and CI (`helm lint`, `helm template south/`) to validate.

The Placement will automatically include the new cluster if it matches the label selectors, and the ApplicationSet will generate an Application pointing to the new folder.

## Minimal profiles

For constrained environments, use `values-lite.yaml` on the hub: fewer subscriptions and disabled heavy components while preserving GitOps bootstrap paths.

```bash
helm template test . -f values-lite.yaml
```
