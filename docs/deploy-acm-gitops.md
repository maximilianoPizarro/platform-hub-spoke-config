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

## Troubleshooting: `industrial-edge-spoke` shows no Applications

The OpenShift / ACM UI may report *no Argo applications* when any link in this chain is missing:

1. **Managed clusters** are **Imported / Available** (`oc get managedcluster`).
2. Each spoke used by this repo should be named **`east`** and **`west`** (Argo cluster secret name = `ManagedCluster` name), **or** add matching entries to the **merge list** in `components/acm-hub-spoke/templates/applicationset.yaml` (`name` + `clusterDomain`) for your real cluster names.
3. **`ManagedClusterSetBinding` `global`** exists in **`openshift-gitops`** and clusters carry **`cluster.open-cluster-management.io/clusterset: global`** (see chart templates).
4. **`Placement` `hub-spoke-placement`** selects your spokes (`region` in `east` | `west` by default).
5. **`PlacementDecision`** objects exist in **`openshift-gitops`** with decisions listing those cluster names:

   ```bash
   oc get placementdecisions.cluster.open-cluster-management.io -n openshift-gitops \
     -l cluster.open-cluster-management.io/placement=hub-spoke-placement -o yaml
   ```

6. **`GitOpsCluster` `hub-spoke-gitops`** is reconciled so Argo registers the same clusters (**Settings → Clusters** in Argo CD).
7. **RBAC**: Role **`applicationset-placementdecisions`** binds **`openshift-gitops-applicationset-controller`** so the **clusterDecisionResource** generator can **list** `placementdecisions`. If your GitOps version uses a different ServiceAccount name, run `oc get sa -n openshift-gitops` and update the RoleBinding subject.

The ApplicationSet uses **`clusterDecisionResource`** (PlacementDecision) **merged** with the static **`east` / `west`** list so Apps are only generated when a cluster is **both** placed **and** registered in Argo CD.

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
