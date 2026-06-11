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

### Learn more

### Learn more

* [OpenShift nodes and scaling](https://docs.redhat.com/en/documentation/red_hat_openshift_container_platform/4.16/html/nodes/index)
* [ACM — capacity planning](https://www.redhat.com/en/technologies/management/advanced-cluster-management)
* [Cluster autoscaler documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/nodes/automatically-scaling-a-cluster)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **SmartScalingPolicy** CRs recommend node/workload sizing.
* **Kairos Console** agent answers scaling questions in natural language.
* Correlates with HPA (module 18) and Kubecost (module 21).

### Business benefits

* Human-in-the-loop approval before edge node changes — safe for OT environments.
* Data-driven rightsizing reduces cloud and hardware spend.

### AWS — Cluster Autoscaler on ROSA

```bash
# ROSA machine pools scale workers
rosa edit machinepool --cluster=workshop-hub --machinepool=worker --replicas=5
aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[?contains(Tags[?Key==`rosa`].Value, `workshop-hub`)]'
```

### Azure — AKS cluster autoscaler

```bash
az aks update --resource-group rg-workshop --name factory-east --enable-cluster-autoscaler   --min-count 2 --max-count 10
az aks nodepool update --resource-group rg-workshop --cluster-name factory-east   --name nodepool1 --enable-cluster-autoscaler --min-count 2 --max-count 8
```

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

