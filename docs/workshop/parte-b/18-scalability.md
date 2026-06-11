---
layout: default
title: Scalability HPA Kafka
parent: Hybrid Mesh AI Workshop
nav_order: 9
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Scalability HPA Kafka


![Three-tier scaling — Kairos nodes, HPA pods, Kafka buffering]({{ site.baseurl }}/assets/images/workshop/18-scalability.png)
{: .mb-4 }

## Overview

Scalability on OpenShift spans horizontal pod autoscaling, Kafka partition scaling, and node-level recommendations from Kairos. HPA v2 watches CPU, memory, or custom metrics from Prometheus adapters; KafkaNodePool resources expand broker capacity when IE topics saturate consumer lag.

In this lab, line-dashboard and related IE deployments include HPAs defined in workload manifests under `components/industrial-edge-tst/`. Trigger load via workshop scripts or simulated sensor rates, then watch pods scale in the Topology view as `%USER_NAME%`. Kafka scaling complements HPA by absorbing event bursts before pods reject traffic.

This module completes the capacity story started in module 14: Kairos proposes nodes, HPA adds pods, Kafka buffers events — together they mirror how a ROSA customer scales factory edge during production peaks without manual cluster admin intervention. Verify with: `oc get hpa -n industrial-edge-tst-all`.

### Learn more

### Learn more

* [Horizontal Pod Autoscaler](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/nodes/automatically-scaling-a-deployment)
* [AMQ Streams — Kafka on OpenShift](https://docs.redhat.com/en/documentation/red_hat_amq_streams)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **HPA** on IE and demo deployments; **Kafka** buffering for sensor spikes.
* **Cluster Autoscaler** / machine pool growth on spokes under load tests.
* `%USER_NAME%` namespaces include quota limits — observe scaling boundaries.

### Business benefits

* Handle shift-change telemetry bursts without manual node provisioning.
* HPA + Kafka decouple ingestion from processing.

### AWS — MSK + HPA on ROSA

```bash
aws kafka create-cluster --cluster-name ie-kafka --kafka-version 3.5.1   --number-of-broker-nodes 3 --broker-node-group-info file://brokers.json
oc autoscale deployment line-dashboard --min=2 --max=10 --cpu-percent=70 -n industrial-edge-tst-all
```

### Azure — Event Hubs Kafka head

```bash
az eventhubs namespace create --name ie-kafka --resource-group rg-workshop --sku Standard   --enable-kafka true
oc autoscale deployment line-dashboard --min=2 --max=10 --cpu-percent=70
```

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

