---
layout: default
title: Branch Strategy
nav_order: 9
---

# Branch Strategy

This repository follows a **single-branch model**: all configuration lives on `main` and spoke-specific overrides are handled via separate **values files** and the **ACM ApplicationSet**.

## How it works

| Values file | Purpose |
| ----------- | ------- |
| `values.yaml` | Hub cluster bootstrap — operators, observability, gateway, hub-only components |
| `values-east.yaml` | East spoke overlay — subscriptions and app list for the east region |
| `values-west.yaml` | West spoke overlay — subscriptions and app list for the west region |
| `values-lite.yaml` | Minimal profile — fewer subscriptions, lighter footprint for demos |

The **ACM ApplicationSet** (`components/acm-hub-spoke/templates/applicationset.yaml`) generates one ArgoCD Application per component per spoke cluster. All applications point to `targetRevision: main` and receive cluster-specific values (`clusterDomain`, `clusterName`, `clusterRole`, `hubClusterDomain`) via the `valuesObject`.

```yaml
# Simplified view of the ApplicationSet matrix generator
generators:
  - matrix:
      generators:
        - list:
            elements:
              - clusterName: east
                clusterDomain: apps.east.example.com
              - clusterName: west
                clusterDomain: apps.west.example.com
        - list:
            elements:
              - id: operators
                path: components/operators
              - id: observability
                path: components/observability
              # ... all spoke components
```

## Adding a new cluster

1. **Provision** the OpenShift cluster and import it into ACM.
2. **Label** the `ManagedCluster` for placement selectors (`region`, `site`, etc.).
3. **Add the cluster** to the ApplicationSet generator list in `components/acm-hub-spoke/templates/applicationset.yaml`.
4. **Add domains** to `values.yaml` under `clusters.<name>.domain`.
5. **Create a values file** (optional) — copy `values-east.yaml` and adjust domains and subscriptions.
6. **Run** `helm template` and CI (`helm lint`, `yamllint`) to validate.

## Minimal profiles

For constrained environments, use `values-lite.yaml`: fewer subscriptions and disabled heavy components while preserving GitOps bootstrap paths.

```bash
helm template test . -f values-lite.yaml
```
