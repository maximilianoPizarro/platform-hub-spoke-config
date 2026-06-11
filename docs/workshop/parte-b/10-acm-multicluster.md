---
layout: default
title: Multicluster Fleet & ACM
parent: Hybrid Mesh AI Workshop
nav_order: 1
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Multicluster Fleet & ACM


![ACM multicluster fleet — hub governing east and west OpenShift spokes]({{ site.baseurl }}/assets/images/workshop/10-acm-multicluster.png)
{: .mb-4 }

## Overview

Red Hat Advanced Cluster Management for Kubernetes turns OpenShift into a fleet control plane: import spokes, enforce policies, visualize health, and delegate GitOps to cluster admins with consistent RBAC. The actual CRDs live in `components/acm-hub-spoke/` — three resources wire the entire fleet:

*Step 1: Register spokes as ManagedClusters.* The Helm template iterates `.Values.managedClusters` and creates one `ManagedCluster` + `KlusterletAddonConfig` per spoke:

[source,yaml]
----
# components/acm-hub-spoke/templates/managed-clusters.yaml
{{- range $name, $cluster := .Values.managedClusters }}
apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: {{ $name }}               # east, west
  labels:
    name: {{ $name }}
    region: {{ $name }}
    cloud: auto-detect
    vendor: OpenShift
    cluster.open-cluster-management.io/clusterset: global
  annotations:
    argocd.argoproj.io/sync-wave: "1"
spec:
  hubAcceptsClient: true
  leaseDurationSeconds: 60
---
apiVersion: agent.open-cluster-management.io/v1
kind: KlusterletAddonConfig
metadata:
  name: {{ $name }}
  namespace: {{ $name }}
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  clusterName: {{ $name }}
  applicationManager:  { enabled: true }
  certPolicyController: { enabled: true }
  policyController:    { enabled: true }
  searchCollector:     { enabled: true }
{{- end }}
----

*Step 2: Placement selects which clusters receive workloads.* Only spokes matching `region: east|west` are selected:

[source,yaml]
----
# components/acm-hub-spoke/templates/placement.yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Placement
metadata:
  name: hub-spoke-placement
  namespace: openshift-gitops
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  clusterSets: [global]
  predicates:
    - requiredClusterSelector:
        labelSelector:
          matchExpressions:
            - key: region
              operator: In
              values: [east, west]
----

*Step 3: GitOpsCluster bridges ACM placement to Argo CD.* This lets hub Argo CD deploy Applications to spoke clusters without manual kubeconfig:

[source,yaml]
----
# components/acm-hub-spoke/templates/gitops-cluster.yaml
apiVersion: apps.open-cluster-management.io/v1beta1
kind: GitOpsCluster
metadata:
  name: hub-spoke-gitops
  namespace: openshift-gitops
  annotations:
    argocd.argoproj.io/sync-wave: "3"
spec:
  argoServer:
    cluster: local-cluster
    argoNamespace: openshift-gitops
  placementRef:
    kind: Placement
    name: hub-spoke-placement
    apiVersion: cluster.open-cluster-management.io/v1beta1
----

*Step 4: ApplicationSet generates spoke Applications automatically.* The `clusterDecisionResource` generator reads ACM placement decisions — when a new spoke joins, its Application appears without editing Git:

[source,yaml]
----
# components/acm-hub-spoke/templates/applicationset.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: industrial-edge-spoke
  namespace: openshift-gitops
  annotations:
    argocd.argoproj.io/sync-wave: "4"
spec:
  generators:
    - clusterDecisionResource:
        configMapRef: acm-placement
        labelSelector:
          matchLabels:
            cluster.open-cluster-management.io/placement: hub-spoke-placement
        requeueAfterSeconds: 180
  template:
    spec:
      source:
        repoURL: {{ .Values.gitops.repoUrl }}
        path: '{{name}}'           # east/ or west/ directory
      destination:
        name: '{{name}}'           # deploys to that spoke
      syncPolicy:
        automated: { selfHeal: true, prune: true }
----

Verify from the Showroom terminal:

[source,bash]
----
# Confirm both spokes are joined and available
oc get managedclusters
# NAME   HUB ACCEPTED   MANAGED CLUSTER URLS   JOINED   AVAILABLE
# east   true           ...                    True     True
# west   true           ...                    True     True

# Check the GitOpsCluster bridge
oc get gitopsclusters -n openshift-gitops

# See ApplicationSet-generated spoke Applications
oc get applicationsets -n openshift-gitops
----

See link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes[ACM documentation] for fleet lifecycle.

### Learn more

### Learn more

* [ACM documentation](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes)
* [ACM — cluster lifecycle](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.14/html/clusters/index)
* [OpenShift GitOps — fleet patterns](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops)
* [Red Hat Interactive Labs](https://access.redhat.com/labs/)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **ManagedCluster** import for east/west spokes without sharing kube-admin broadly.
* **Placement** and **GitOpsCluster** — deploy apps to selected clusters from hub.
* OCM APIs power Developer Hub Topology multicluster view.

### Business benefits

* Single pane for fleet health — critical for 10+ factory edge sites.
* Policy violations visible before they reach production OT networks.

### AWS — ROSA spoke registration

```bash
# On spoke ROSA cluster — bootstrap klusterlet (ACM auto-import flow)
# Hub: oc get managedclusters
rosa list clusters
aws eks update-cluster-config --name factory-east --resources-vpc-config endpointPublicAccess=false

# Hub credentials for import (use ACM console Import cluster wizard)
oc get secret -n open-cluster-management hub-kubeconfig-secret -o yaml
```

### Azure — AKS attach

```bash
az aks get-credentials --resource-group rg-workshop --name factory-east
# ACM: Clusters → Import → paste kubeconfig / auto import
az aks update --resource-group rg-workshop --name factory-east --enable-aad --aad-admin-group-object-ids <guid>
```

## Show and Tell

. Open ACM Clusters UI — identify east and west spokes.
. Run `oc get managedclusters` in Showroom terminal live.
. Show Developer Hub Topology mirroring OCM graph.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| ManagedCluster | `components/acm-hub-spoke/templates/managed-clusters.yaml` |
| GitOpsCluster | `components/acm-hub-spoke/templates/gitops-cluster.yaml` |

Verify in the Showroom terminal:

```bash
oc get managedclusters; oc get gitopscluster -A 2>/dev/null | head -5
```

## Your TODO

* [ ] Run `oc get managedclusters` and identify east/west
* [ ] Open ACM Clusters UI and Developer Hub Topology for the same fleet
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get managedclusters; oc get gitopscluster -A 2>/dev/null | head -5
```

