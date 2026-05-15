---
layout: default
title: Observability
nav_order: 7
---

# Observability

Observability ties together **metrics**, **logs**, **traces**, and **mesh visualization** so operators can compare east and west Industrial Edge clusters from the hub.

## Components

| Layer | Technology | Role |
| ----- | ----------- | ---- |
| Metrics | User Workload Monitoring / Prometheus-compatible stacks | RED/USE signals, Kafka lag, mesh stats |
| Dashboards | Grafana | Fleet and factory KPI views (`components/grafana-dashboards`) |
| Mesh UI | Kiali | Traffic graphs for Service Mesh |
| Tracing | OpenTelemetry Collector & backends | Distributed traces across integrations |

## Multi-cluster patterns

- Federated **Grafana** data sources or remote Prometheus endpoints per spoke.
- Consistent **OpenTelemetry** exporter configuration in Camel and Java workloads.

## Links

- [OpenShift Observability](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/monitoring/)
- [OpenTelemetry on OpenShift](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/red_hat_build_of_opentelemetry/)
- [Kiali Service Mesh observability](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/service_mesh/)

Charts: `components/observability`, `components/grafana-dashboards`, `components/kiali`, `components/opentelemetry`.
