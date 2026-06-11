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

Kairos Community on OpenShift analyzes workload metrics and recommends resource adjustments through `SmartScalingPolicy` resources — bridging the gap between Kubernetes HPA (pod-level) and infrastructure provisioning (cluster-level). The policies live in `components/kairos/templates/sensor-scan-policies.yaml`.

*SmartScalingPolicy for sensor workloads:* Two policies monitor `machine-sensor-1` and `machine-sensor-2` deployments, each with CPU and memory rules that trigger resource increases with cooldown periods:

[source,yaml]
----
# components/kairos/templates/sensor-scan-policies.yaml
apiVersion: kairos.maximilianopizarro.github.io/v1alpha1
kind: SmartScalingPolicy
metadata:
  name: scan-policy-machine-sensor-1
  namespace: kairos-system
  labels:
    kairos.io/policy-type: sensor-scan
  annotations:
    argocd.argoproj.io/sync-wave: "6"
spec:
  scope: cluster
  target:
    apiVersion: apps/v1
    kind: Deployment
    name: machine-sensor-1
    namespace: industrial-edge-tst-all
  otelEndpoint: "..."                  # OpenTelemetry collector on spoke
  prometheusEndpoint: "..."            # Prometheus metrics for analysis
  rules:
    - name: sensor-cpu-hot
      when:
        metric: container_cpu_usage_seconds_total
        operator: GreaterThan
        threshold: "70"                # 70% CPU triggers action
        for: 2m                        # sustained for 2 minutes
      action:
        type: IncreaseResources
        increaseCPUPercent: 25         # bump CPU limit by 25%
        maxCPU: "1"                    # never exceed 1 core
        cooldown: 5m                   # wait 5 min before re-evaluating
    - name: sensor-memory-hot
      when:
        metric: container_memory_working_set_bytes
        operator: GreaterThan
        threshold: "80"
        for: 2m
      action:
        type: IncreaseResources
        increaseMemoryPercent: 20
        maxMemory: 1Gi
        cooldown: 5m
  ai:
    enabled: true                      # AI-assisted recommendations
  paused: false
----

*Kairos Console:* The console is deployed on the hub via `KairosConsole` CR — operators approve or reject recommendations through a web UI:

[source,yaml]
----
# components/kairos/templates/kairos-console.yaml
apiVersion: kairos.maximilianopizarro.github.io/v1alpha1
kind: KairosConsole
metadata:
  name: kairos-console
  namespace: kairos-system
  annotations:
    argocd.argoproj.io/sync-wave: "4"
spec:
  replicas: 1
  route:
    enabled: true
    host: "kairos-console-kairos-system.{{ .Values.clusterDomain }}"
    tlsEnabled: true
----

*Hub mirror:* The App-of-Apps template passes `sensorScanPolicies.displayOnHub: true` so the hub Kairos Console can visualize spoke policy status without requiring direct spoke access — matching how ROSA customers centralize capacity decisions.

Pair this module with module 18 (HPA + Kafka) to show two layers: pods scale horizontally while Kairos evaluates resource limits.

[source,bash]
----
# List all SmartScalingPolicies across clusters
oc get smartscalingpolicy -A

# Check Kairos Console route
oc get route -n kairos-system

# See policy recommendations
oc describe smartscalingpolicy scan-policy-machine-sensor-1 -n kairos-system
----

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

