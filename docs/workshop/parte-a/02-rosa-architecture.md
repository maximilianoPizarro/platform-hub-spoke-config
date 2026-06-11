---
layout: default
title: ROSA Architecture & Benefits
parent: Hybrid Mesh AI Workshop
nav_order: 2
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# ROSA Architecture & Benefits


![ROSA and OpenShift hub-spoke architecture]({{ site.baseurl }}/assets/images/workshop/02-rosa-architecture.png)
{: .mb-4 }

## Overview

Red Hat OpenShift Service on AWS (ROSA) provides a fully managed control plane in your AWS account while Red Hat handles upgrades, security patches, and SRE operations. Worker nodes scale via MachineSets; ingress integrates with Route 53 and ALB; IAM and STS enable secure cloud service access — the reference architecture for hybrid customers who standardize on OpenShift everywhere.

This workshop's hub-spoke layout maps cleanly to ROSA concepts: the hub is your fleet management cluster (like an ACM hub on ROSA), spokes are regional or edge clusters importing via ManagedCluster resources. You will inspect `ManagedCluster` objects and GitOpsCluster links in module 10 — the same CRDs a ROSA customer uses when joining factory edge clusters to a central governance hub.

Understanding ROSA architecture helps you explain SLA boundaries: Red Hat manages the control plane; you own worker sizing, networking, and data. In the lab, Kairos and HPA on spokes simulate ROSA autoscaling decisions without AWS billing, preparing you for FinOps modules later.

## Show and Tell

. Whiteboard ROSA control plane vs worker responsibility split.
. Show ACM ManagedCluster list as the lab equivalent of joining ROSA to a fleet hub.
. Mention SLA and support boundaries Red Hat vs customer ops.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| ManagedCluster CRs | `components/acm-hub-spoke/templates/managed-clusters.yaml` |
| Spoke registration | ACM → Clusters UI on this hub |

Verify in the Showroom terminal:

```bash
oc get managedclusters -o wide
```

## Your TODO

* [ ] Sketch ROSA control plane vs worker responsibilities for your account
* [ ] Preview ACM ManagedCluster in module 10 reading list
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get managedclusters -o wide
```

