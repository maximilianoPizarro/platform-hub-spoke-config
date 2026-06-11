---
layout: default
title: Scalability HPA Kafka
parent: Hybrid Mesh AI Workshop
nav_order: 9
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Scalability HPA Kafka


![HPA and Kafka scalability]({{ site.baseurl }}/assets/images/workshop/18-scalability.png)
{: .mb-4 }

## Overview

Scalability on OpenShift spans horizontal pod autoscaling, Kafka partition scaling, and node-level recommendations from Kairos. HPA v2 watches CPU, memory, or custom metrics from Prometheus adapters; KafkaNodePool resources expand broker capacity when IE topics saturate consumer lag.

In this lab, line-dashboard and related IE deployments include HPAs defined in workload manifests under `components/industrial-edge-tst/`. Trigger load via workshop scripts or simulated sensor rates, then watch pods scale in the Topology view as `%USER_NAME%`. Kafka scaling complements HPA by absorbing event bursts before pods reject traffic.

This module completes the capacity story started in module 14: Kairos proposes nodes, HPA adds pods, Kafka buffers events — together they mirror how a ROSA customer scales factory edge during production peaks without manual cluster admin intervention.

## Show and Tell

. Watch HPA scale line-dashboard pods under simulated load.
. Show Kafka consumer lag recovering after buffer capacity.
. Tie pod-scale (HPA) vs node-scale (Kairos) layering.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| IE workloads | `components/industrial-edge-tst/` |
| HPA / Kafka | spoke namespace `industrial-edge-tst-all` |

Verify in the Showroom terminal:

```bash
oc get hpa -n industrial-edge-tst-all 2>/dev/null
```

## Your TODO

* [ ] Check HPA status for line-dashboard or related IE deployment
* [ ] Observe Kafka consumer lag under load or simulated traffic
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get hpa -n industrial-edge-tst-all 2>/dev/null
```

