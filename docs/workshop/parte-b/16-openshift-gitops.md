---
layout: default
title: OpenShift GitOps
parent: Hybrid Mesh AI Workshop
nav_order: 7
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# OpenShift GitOps


![OpenShift GitOps and Argo CD]({{ site.baseurl }}/assets/images/workshop/16-openshift-gitops.png)
{: .mb-4 }

## Overview

OpenShift GitOps installs Argo CD as a managed operator and integrates with ACM ApplicationSets to propagate manifests hub-to-spoke with policy-safe destinations. Platform teams commit desired state to Git; controllers reconcile drift — the same GitOps discipline ROSA customers use when pairing ROSA clusters with ACM hub repositories.

In this lab, hub Applications under `templates/component-applications.yaml` deploy shared services while spoke Applications (for example Industrial Edge) sync from user Gitea repos created in module 13. ApplicationSet `industrial-edge-spoke` demonstrates matrix generators targeting east/west labels.

Inspect sync status in Argo CD UI as `%USER_NAME%` and identify which repo revision triggered your deployment. GitOps is the operational backbone: every product module (mesh, ACS, AI) ultimately resolves to tracked YAML in `platform-hub-spoke-config`.

### Learn more

### Learn more

* [OpenShift GitOps documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops)
* [Argo CD documentation](https://argo-cd.readthedocs.io/)
* [ACM GitOps overview](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.14/html/gitops/gitops-overview)

## Show and Tell

. Argo CD UI: hub Application vs user spoke Application sources.
. Highlight ApplicationSet generator for east/west matrix.
. Show sync wave or health status for IE app.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Hub Applications | `templates/component-applications.yaml` |
| ApplicationSet IE | `components/acm-hub-spoke/templates/applicationset.yaml` |

Verify in the Showroom terminal:

```bash
oc get applications -n openshift-gitops 2>/dev/null | head -10
```

## Your TODO

* [ ] Find your IE Application in Argo CD and note sync status
* [ ] Identify Git repo source (user Gitea vs hub platform repo)
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get applications -n openshift-gitops 2>/dev/null | head -10
```

