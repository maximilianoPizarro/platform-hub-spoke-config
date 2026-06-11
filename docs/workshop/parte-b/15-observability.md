---
layout: default
title: Metrics Logging Dashboards
parent: Hybrid Mesh AI Workshop
nav_order: 6
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Metrics Logging Dashboards


![Observability dashboards and tracing]({{ site.baseurl }}/assets/images/workshop/15-observability.png)
{: .mb-4 }

## Overview

OpenShift observability spans cluster metrics, logs, traces, and custom dashboards federated across ACM-managed clusters. Red Hat builds on Prometheus, Loki or Elasticsearch patterns, Grafana, and OpenTelemetry Instrumentation CRs so application teams inherit platform-wide collectors without sidecar sprawl on every pod.

This workshop deploys multicluster Grafana dashboards on the hub, OpenTelemetry collectors via `components/opentelemetry/`, and Kafka Console for IE topic inspection. As `%USER_NAME%`, filter dashboards to your namespace and correlate latency spikes with mesh traces in module 17.

Executives should connect this module to module 21 (Kubecost): metrics prove SLO compliance while cost metrics prove efficiency — both required for hybrid FinOps. Use Showroom `oc` to list `GrafanaDashboard` CRs and confirm IE workloads emit scrape targets.

### Learn more

### Learn more

* [OpenShift monitoring](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/monitoring/index)
* [Distributed tracing](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/distributed_tracing/distributed-tracing-overview)
* [Grafana documentation](https://grafana.com/docs/)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **Prometheus** federation hub ← spokes; **Grafana** dashboards for `%USER_NAME%`.
* **Tempo/Jaeger** distributed tracing across mesh and IE services.
* **Kiali** service graph for ambient mesh (module 17).

### Business benefits

* Mean time to resolution drops when traces link IE Kafka lag to specific pods.
* Single Grafana entry for executives and SREs.

### AWS — CloudWatch + ROSA

```bash
aws logs create-log-group --log-group-name /rosa/workshop-hub/application
aws cloudwatch put-metric-alarm --alarm-name kafka-lag-high   --metric-name EstimatedLag --namespace AWS/Kafka --threshold 10000   --comparison-operator GreaterThanThreshold --evaluation-periods 2 --period 300
```

### Azure — Monitor + Container Insights

```bash
az monitor diagnostic-settings create --name aks-logs --resource /subscriptions/.../factory-east   --workspace hybrid-ops --logs '[{"category":"kube-audit","enabled":true}]'
az monitor metrics alert create --name kafka-lag --resource-group rg-workshop   --scopes <resource-id> --condition "avg Percentage CPU > 80" --window-size 5m
```

## Show and Tell

. Open multicluster Grafana dashboard filtered to IE namespace.
. Show Kafka Console and a sample OTEL trace (or metrics gap if trace pending).
. Link metrics SLO story to upcoming Kubecost module.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Grafana dashboards | `components/grafana-dashboards/` |
| OTEL | `components/opentelemetry/` |

Verify in the Showroom terminal:

```bash
oc get route -n openshift-cluster-observability-operator 2>/dev/null | head -3
```

## Your TODO

* [ ] Open a multicluster Grafana dashboard for your IE namespace
* [ ] Inspect Kafka Console topics for sensor data
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get route -n openshift-cluster-observability-operator 2>/dev/null | head -3
```

