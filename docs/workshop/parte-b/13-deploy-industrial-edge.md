---
layout: default
title: Deploy Industrial Edge Apps
parent: Hybrid Mesh AI Workshop
nav_order: 4
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Deploy Industrial Edge Apps


![Industrial Edge deployment on spoke]({{ site.baseurl }}/assets/images/workshop/13-deploy-industrial-edge.png)
{: .mb-4 }

## Overview

Industrial Edge on OpenShift combines event streaming, integration, and visualization for factory and IoT scenarios. The entire stack is defined in `components/industrial-edge-tst/` and deployed via GitOps to spoke clusters.

*Kafka cluster (KRaft mode):* A single-node KRaft broker with ephemeral storage, plus `temperature` and `vibration` topics for sensor data. Notice the Strimzi annotations and the Prometheus JMX exporter for observability:

[source,yaml]
----
# components/industrial-edge-tst/templates/kafka-cluster.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaNodePool
metadata:
  name: broker
  namespace: industrial-edge-tst-all
  labels:
    strimzi.io/cluster: dev-cluster
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  replicas: 1
  roles: [controller, broker]        # KRaft combined mode — no ZooKeeper
  storage:
    type: ephemeral                   # workshop-scale; production uses persistent
---
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: dev-cluster
  namespace: industrial-edge-tst-all
  annotations:
    strimzi.io/kraft: enabled
    strimzi.io/node-pools: enabled
    argocd.argoproj.io/sync-wave: "3"
spec:
  kafka:
    version: 4.2.0
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
    metricsConfig:
      type: jmxPrometheusExporter     # feeds Grafana dashboards (module 15)
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics-config
          key: kafka-metrics-config.yml
  entityOperator:
    topicOperator: {}
    template:
      pod:
        metadata:
          labels:
            istio.io/dataplane-mode: none   # entity-operator bypasses ambient mesh
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: temperature
  namespace: industrial-edge-tst-all
  labels:
    strimzi.io/cluster: dev-cluster
  annotations:
    argocd.argoproj.io/sync-wave: "4"
spec:
  partitions: 1
  replicas: 1
----

*Sync-wave ordering:* Broker pool (wave 2) → Kafka cluster (wave 3) → Topics (wave 4) → Sensor deployments (wave 5). Argo CD respects this sequence so topics exist before producers start.

Run the Industrial Edge template as `%USER_NAME%` and confirm your Gitea organization `ws-%USER_NAME%` contains the generated repository. Argo CD on east syncs the Application into namespace `industrial-edge-tst-all`. Plan B demo `demo-industrial-edge-east` offers the same topology if scaffolding is skipped.

This module is the operational heart of Part B: later observability, scaling, network policy, anomaly detection, and AI modules all assume IE workloads are running on your spoke.

[source,bash]
----
# Verify Kafka cluster is ready
oc get kafka dev-cluster -n industrial-edge-tst-all -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'

# Check topics exist
oc get kafkatopics -n industrial-edge-tst-all

# Confirm line-dashboard is serving
oc get route -n industrial-edge-tst-all -l app=line-dashboard

# Check Argo CD sync status
oc get applications -n openshift-gitops | grep industrial-edge
----

### Learn more

### Learn more

* [Industrial Edge on OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift/industrial-edge)
* [AMQ Streams documentation](https://docs.redhat.com/en/documentation/red_hat_amq_streams)
* [Microservices learning hub](https://developers.redhat.com/topics/microservices)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **Industrial Edge** stack — line dashboard, Kafka, Camel, ML inference at the edge.
* Deployed on **east spoke** via ACM placement and GitOps.
* Plan B demo `demo-industrial-edge-east` if scaffolder unavailable.

### Business benefits

* Process sensor data locally; sync summaries to hub for AI and FinOps.
* Reduces cloud egress costs for high-frequency OT telemetry.

### AWS — IoT Greengrass / edge ROSA

```bash
aws greengrassv2 create-component-version --inline-recipe file://line-recipe.yaml
aws iot thing create --thing-name line-01-edge
# ROSA single-node compact cluster at edge (3-node minimum production)
rosa create cluster --cluster-name=line-01 --region=us-east-1 --compute-machine-type=m5.xlarge
```

### Azure — IoT Edge on AKS

```bash
az iot edge set-modules --device-id line-01 --hub-name plant-iot --content file://deployment.json
az aks nodepool add --resource-group rg-workshop --cluster-name factory-east --name edgepool --node-count 2
```

## Show and Tell

. Confirm Gitea org `ws-%USER_NAME%` and Argo CD sync on east.
. Open line-dashboard route and Kafka Console topics.
. Offer Plan B `demo-industrial-edge-east` if scaffold fails.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| IE on spoke | `components/industrial-edge-tst/` (east Application) |
| Line dashboard | namespace `industrial-edge-tst-all` |

Verify in the Showroom terminal:

```bash
oc get deploy -n industrial-edge-tst-all 2>/dev/null | head -8
```

## Your TODO

* [ ] Scaffold IE or open Plan B `demo-industrial-edge-east`
* [ ] Verify Gitea org `ws-%USER_NAME%` and Argo CD sync Healthy
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get deploy -n industrial-edge-tst-all 2>/dev/null | head -8
```

