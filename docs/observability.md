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
| Metrics | User Workload Monitoring / Prometheus | RED/USE signals, Kafka lag, mesh stats |
| Dashboards | Grafana | Fleet and factory KPI views (`components/grafana-dashboards`) |
| Mesh UI | Kiali | Traffic graphs for Service Mesh |
| Tracing | OpenTelemetry Collector & backends | Distributed traces across integrations |

## Kiali setup for Service Mesh 3

Kiali requires explicit configuration to access Prometheus and Grafana. Without this, the UI loads but all traffic graphs show empty:

1. **Grant Prometheus read access** to Kiali's service account:
   ```bash
   oc adm policy add-cluster-role-to-user cluster-monitoring-view \
     -z kiali-service-account -n openshift-cluster-observability-operator
   ```

2. **Configure auth** in the Kiali CR:
   ```bash
   oc patch kiali kiali -n openshift-cluster-observability-operator --type merge -p '{
     "spec": {
       "external_services": {
         "prometheus": { "auth": { "type": "bearer", "use_kiali_token": true } },
         "grafana": { "auth": { "type": "basic", "username": "admin", "password": "admin" } }
       }
     }
   }'
   ```

## Prometheus scraping for Istio metrics

OpenShift Prometheus does **not** scrape Istio metrics by default. You must create:

- **ServiceMonitor** for `istiod` (port `http-monitoring` / 15014, path `/metrics`)
- **PodMonitor** for waypoint/gateway proxies (port `metrics` / 15020, path `/stats/prometheus`)

Additionally, the User Workload Prometheus needs **RoleBindings** in each mesh namespace (`istio-system`, `hub-gateway-system`, `industrial-edge-tst-all`, etc.) to grant the `prometheus-k8s` ClusterRole to the `prometheus-user-workload` ServiceAccount.

Key metrics path differences:
- **istiod**: `/metrics` (standard Prometheus format)
- **Envoy proxies** (gateways, waypoints): `/stats/prometheus` (Envoy admin format)

## Multi-cluster patterns

- Federated **Grafana** data sources or remote Prometheus endpoints per spoke.
- Consistent **OpenTelemetry** exporter configuration in Camel and Java workloads.
- Hub Kiali visualizes traffic for hub-local mesh namespaces. Spoke clusters run their own Kiali instances for local visibility.

## Links

- [OpenShift Observability](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/monitoring/)
- [OpenTelemetry on OpenShift](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/red_hat_build_of_opentelemetry/)
- [Kiali Service Mesh observability](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/service_mesh/)

Charts: `components/observability`, `components/grafana-dashboards`, `components/kiali`, `components/opentelemetry`.
