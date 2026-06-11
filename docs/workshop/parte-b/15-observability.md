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

