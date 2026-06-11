---
layout: default
title: Worker Scaling with Kairos
parent: Hybrid Mesh AI Workshop
nav_order: 5
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Worker Scaling with Kairos


![Kairos SmartScaling recommendations]({{ site.baseurl }}/assets/images/workshop/14-kairos-scaling.png)
{: .mb-4 }

## Overview

Kairos Community on OpenShift analyzes workload metrics and recommends node or machine set adjustments through SmartScalingPolicy resources — bridging the gap between Kubernetes HPA (pod-level) and infrastructure provisioning (cluster-level). Operators approve recommendations in Kairos Console, preserving human oversight for factory edge sites where sudden scale-down is risky.

In this lab, the sensor-scan policy watches Industrial Edge metrics and proposes scaling when scan rates spike — analogous to ROSA MachineSet autoscaling triggered by custom CloudWatch metrics. Pair this module with module 18 (HPA + Kafka) to show two layers: pods scale horizontally while Kairos evaluates node capacity.

Open Kairos Console from the OpenShift menu, locate pending recommendations tied to `%USER_NAME%` namespaces, and approve or discuss trade-offs with the facilitator. Run `oc get smartscalingpolicy -A` to correlate CRDs with UI actions.

## Show and Tell

. Open Kairos Console and walk through a pending SmartScalingPolicy recommendation.
. Correlate UI action with `oc get smartscalingpolicy -A`.
. Discuss human-in-the-loop approval for factory edge.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Kairos policies | `components/kairos/templates/sensor-scan-policies.yaml` |
| Kairos Console | `components/kairos/` |

Verify in the Showroom terminal:

```bash
oc get smartscalingpolicy -A 2>/dev/null | head -5
```

## Your TODO

* [ ] Open Kairos Console and review one SmartScalingPolicy
* [ ] Run `oc get smartscalingpolicy -A` from Showroom terminal
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get smartscalingpolicy -A 2>/dev/null | head -5
```

