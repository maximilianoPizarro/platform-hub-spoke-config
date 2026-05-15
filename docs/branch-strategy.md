---
layout: default
title: Branch Strategy
nav_order: 9
---

# Branch Strategy

This repository uses **Git branches** to align GitOps revisions with **hub vs regional spokes**.

## Branch layout

| Branch | Typical consumers | Values file |
| ------ | ----------------- | ----------- |
| `main` | Hub cluster bootstrap | `values.yaml` (`gitops.revision: main`) |
| `east` | East-region spoke | `values-east.yaml` (`gitops.revision: east`) |
| `west` | West-region spoke | `values-west.yaml` (`gitops.revision: west`) |

Argo CD Applications reference `spec.source.targetRevision` matching these branches so each fleet slice tracks appropriate overlays without duplicating repositories.

## Adding a new cluster

1. **Provision** the OpenShift cluster and import it into ACM.
2. **Label** the `ManagedCluster` for placement selectors (`region`, `site`, etc.).
3. **Decide branch model**: extend existing regional branches or add `site-foo` with a new values file.
4. **Copy** an existing spoke values file (for example `values-east.yaml`) and adjust `gitops.revision`, domains, and enabled `connectivityLink.apps[]` entries.
5. **Extend** `Placement` / **ApplicationSet** generators if you introduced new label keys.
6. **Run** `helm template` and CI (`helm lint`, `yamllint`) against the new profile before merging.

## Minimal profiles

For constrained environments, test `values-lite.yaml`: fewer subscriptions and disabled heavy components while preserving GitOps bootstrap paths.
