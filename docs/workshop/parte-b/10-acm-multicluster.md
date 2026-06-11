---
layout: default
title: Multicluster Fleet & ACM
parent: Hybrid Mesh AI Workshop
nav_order: 1
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Multicluster Fleet & ACM


![ACM multicluster fleet management]({{ site.baseurl }}/assets/images/workshop/10-acm-multicluster.png)
{: .mb-4 }

## Overview

Red Hat Advanced Cluster Management for Kubernetes turns OpenShift into a fleet control plane: import spokes, enforce policies, visualize health, and delegate GitOps to cluster admins with consistent RBAC. ManagedCluster and Klusterlet agents mirror how ROSA and on-prem clusters join a customer's governance hub without sharing kube-admin credentials broadly. See link:https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes[ACM documentation] for fleet lifecycle.

In this lab, open ACM Clusters on the hub and locate east and west — each spoke was bootstrapped from `components/acm-hub-spoke/` GitOps manifests. As `%USER_NAME%`, your workloads land on east by default; Topology in Developer Hub uses OCM APIs to show the same graph ACM displays.

This module establishes the mental model for every subsequent Part B exercise: the hub owns ingress, policy, FinOps aggregation, and AI control planes; spokes run Industrial Edge and user-scoped namespaces. Verify with `oc get managedclusters` from the Showroom terminal.

The configuration is declarative and minimal:

[source,yaml]
----
# components/acm-hub-spoke/templates/managed-clusters.yaml
apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: east
  labels:
    cloud: Amazon
    vendor: OpenShift
    cluster.open-cluster-management.io/clusterset: workshop
spec:
  hubAcceptsClient: true
  leaseDurationSeconds: 60
----

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

