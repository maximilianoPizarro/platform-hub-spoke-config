---
layout: default
title: Security & Scale in Hybrid
parent: Hybrid Mesh AI Workshop
nav_order: 3
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Security & Scale in Hybrid


![Hybrid cloud security and scale]({{ site.baseurl }}/assets/images/workshop/03-security-scale-hybrid.png)
{: .mb-4 }

## Overview

Security and scale in hybrid OpenShift environments require defense in depth: identity federation, network segmentation, runtime threat detection, and policy-driven compliance across every cluster in the fleet. Red Hat Advanced Cluster Security (ACS) centralizes vulnerability management and runtime policies while OpenShift Service Mesh adds zero-trust connectivity between microservices.

In this lab, ACS Central runs on the hub with SecuredCluster agents on spokes — note that the `stackrox` namespace deliberately avoids ambient mesh labels so ACS sensors are not disrupted. NetworkPolicy demos in module 19 use OVN on spokes, analogous to security groups plus Kubernetes NP on ROSA. Kuadrant AuthPolicy at the hub gateway shows how API traffic is authenticated and rate-limited before it reaches Industrial Edge backends.

Scaling hybrid fleets means automating placement and capacity: ACM policies, Kairos SmartScalingPolicy, Kafka buffering, and HPA together handle sensor spikes without manual ticket queues. As `%USER_NAME%`, you will observe these controls in modules 14 and 18 on workloads that simulate factory telemetry bursts.

### Learn more

### Learn more

* [Advanced Cluster Security (ACS) documentation](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_security_for_kubernetes)
* [OpenShift security and compliance](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/security_and_compliance/index)
* [ACM governance overview](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.14/html/governance/governance-overview)
* [Red Hat security blog](https://www.redhat.com/en/blog/tag/security)

## Show and Tell

. Highlight ACS + mesh coexistence (`stackrox` without ambient labels).
. Preview NetworkPolicy (19) and Kuadrant (20) as defense layers.
. Discuss factory edge scale events and Kairos approval workflow.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| ACS operator | `components/acs-operator/` |
| ACS Central route | namespace `stackrox` |

Verify in the Showroom terminal:

```bash
oc get central -n stackrox; oc get ns stackrox --show-labels | head -3
```

## Your TODO

* [ ] List three security layers you will verify in Part B (ACS, NP, Kuadrant)
* [ ] Note why `stackrox` avoids ambient mesh in this lab
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get central -n stackrox; oc get ns stackrox --show-labels | head -3
```

