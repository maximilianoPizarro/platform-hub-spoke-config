---
layout: default
title: Hybrid Cloud Strategy
parent: Hybrid Mesh AI Workshop
nav_order: 1
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Hybrid Cloud Strategy


![Hybrid cloud strategy overview]({{ site.baseurl }}/assets/images/workshop/01-hybrid-strategy.png)
{: .mb-4 }

## Overview

Hybrid cloud strategy starts with workload placement: keep latency-sensitive factory systems at the edge, burst analytics and AI training to cloud regions, and govern everything from a central OpenShift hub. Red Hat OpenShift Container Platform delivers a single Kubernetes API and operator model whether clusters run on-prem, at edge sites, or as ROSA in AWS.

In this lab, ACM on the hub represents that governance layer — policies, observability federation, and GitOps placement target east and west spokes the same way a customer would target ROSA and on-prem clusters. You are not learning abstract slides; every Part B module reinforces a strategic pillar: automation, security, developer velocity, or AI readiness.

Executives should note that OpenShift avoids replatforming twice: microservices, VMs (CNV), and AI pipelines share the same RBAC, networking, and CI/CD patterns. When you register as `%USER_NAME%`, your hands-on path mirrors how platform teams onboard application squads in production.

### Learn more

### Learn more

* [Red Hat OpenShift cloud services overview](https://www.redhat.com/en/technologies/cloud-computing/openshift/cloud-services)
* [OpenShift Service on AWS (ROSA) documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws)
* [Red Hat Developer — learning paths](https://developers.redhat.com/learn)
* [ACM — multicluster management](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes)

## Show and Tell

. Frame the four strategic pillars: modernize, secure, automate, monetize AI on OpenShift.
. Map each pillar to a Part B module number on the agenda table.
. Ask attendees their current hybrid split (ROSA vs on-prem vs edge).

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| ACM fleet UI | `components/acm-hub-spoke/` |
| Hub app-of-apps | `templates/component-applications.yaml` |

Verify in the Showroom terminal:

```bash
oc get managedclusters 2>/dev/null | head -5
```

## Your TODO

* [ ] Map your organization's workloads to hub vs spoke vs ROSA placement
* [ ] Identify which Part B module addresses your top priority pillar
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get managedclusters 2>/dev/null | head -5
```

