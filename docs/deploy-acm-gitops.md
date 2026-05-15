---
layout: default
title: Deploy with ACM and GitOps
nav_order: 4
---

# Deploy with ACM and GitOps

This guide explains how Red Hat ACM primitives cooperate with OpenShift GitOps (Argo CD) to drive hub-spoke deployment from Git.

## ManagedClusterSet

A **ManagedClusterSet** groups clusters for RBAC and placement. Typical patterns:

- One set for all fleet clusters.
- Separate sets for production vs non-production.

Cluster membership in a set is what downstream objects reference—not individual cluster names embedded in static YAML.

## Placement

**Placement** selects clusters from a `ManagedClusterSet` using label selectors or predicates. ACM computes intent continuously as clusters join, leave, or change labels.

Example concerns:

- Select `region=east` for east-only workloads.
- Require feature labels such as `environment=prod`.

## PlacementDecision

ACM publishes **PlacementDecision** objects listing concrete cluster names that satisfied a `Placement` at a given time. GitOps integrations watch these decisions to know *where* to apply manifests without hardcoding kube-apiserver URLs in Git.

## GitOpsCluster

A **GitOpsCluster** resource associates Argo CD (`spec.argocd`) with clusters chosen by placement. It bridges ACM’s fleet selection with Argo CD’s cluster secrets and Application destinations.

Together, `Placement` → `PlacementDecision` → `GitOpsCluster` avoids brittle per-cluster Application YAML checked into Git.

## ApplicationSet matrix generator

An **ApplicationSet** **matrix** generator combines two lists (for example **cluster** × **component**) to emit many `Application` objects from one definition.

Common axes:

- Git directories or Helm charts per component.
- Cluster list from a generator that reads `PlacementDecision` or cluster labels.

This matches hub-spoke scaling: adding a spoke with correct labels yields new `Application` instances automatically.

## Step-by-step deployment

1. **Install OpenShift GitOps** on the hub (subscription stable channel) if not already present.
2. **Install ACM** hub components and verify `MultiClusterHub` is healthy.
3. **Create ManagedClusterSet** and bind hub + spokes.
4. **Label spokes** for placement (`region`, `environment`, etc.).
5. **Define Placement** and verify generated **PlacementDecision** objects show expected clusters.
6. **Create GitOpsCluster** referencing your Argo CD namespace (`openshift-gitops` by convention).
7. **Apply ApplicationSet** manifests (often shipped via this repo’s `acm-hub-spoke` chart path) so Applications appear under the Argo CD project.
8. **Observe sync waves** — lower waves (namespaces, operators) complete before application workloads.

## References

- [ACM Architecture — Welcome](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.16/html/about/welcome-to-red-hat-advanced-cluster-management-for-kubernetes)
- [Multicloud GitOps Validated Pattern](https://validatedpatterns.io/patterns/multicloud-gitops)
- [ApplicationSet Generators](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators/)
