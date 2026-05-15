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

## Grafana + Thanos (dashboards with data)

Grafana **11** often ships with **HTTP basic auth to the Grafana API disabled**. The Grafana Operator must authenticate to Grafana to install datasources; if that fails, the **Prometheus** datasource never syncs and dashboards show **No data** even when metrics exist in Prometheus.

This repository configures:

1. **`[auth.basic] enabled`** on the `Grafana` CR via `spec.config.auth.basic` as a **string** (INI snippet), because the Grafana Operator CRD expects `auth.basic` to be a string, not a nested object.
2. A **ServiceAccount** (`grafana-thanos-reader`) bound to **`cluster-monitoring-view`**, plus a **`kubernetes.io/service-account-token`** Secret.
3. **`GrafanaDatasource.valuesFrom`** so the Thanos `Authorization: Bearer …` header is built from that token (instead of the non-functional `${GRAFANA_SA_TOKEN}` placeholder).

After syncing, confirm the datasource in the Grafana UI (**Connections → Data sources → Prometheus → Save & test**) and use **Explore** with `up` or `istio_requests_total`.

## Multi-cluster patterns

- **Hub Kiali** only shows workloads running **on the hub cluster**. HTTP you see toward `industrial-edge-east` / `industrial-edge-west` is traffic from the hub gateway to **external** OpenShift routes; it is not the same as rendering east/west pod graphs inside hub Kiali unless you add **multi-cluster Kiali** (remote kubeconfigs / ACM integration) or **federated metrics**.
- **Red Hat Service Interconnect** (`components/service-interconnect`, operator `skupper-operator`): create linked **Site** resources on hub and spokes and **expose** the spoke `Service` into the hub VAN so the hub mesh sees concrete `Service` backends (then Kiali/Grafana on the hub can observe that traffic). Linking uses access tokens generated per site; see [Using Service Interconnect](https://docs.redhat.com/en/documentation/red_hat_service_interconnect/2.1/html-single/using_service_interconnect/).
- Federated **Grafana** data sources or **remote Prometheus** endpoints per spoke.
- Consistent **OpenTelemetry** exporter configuration in Camel and Java workloads.
- Spoke clusters can run their own **Kiali** instances for full local mesh graphs.


- [OpenShift Observability](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/monitoring/)
- [OpenTelemetry on OpenShift](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/red_hat_build_of_opentelemetry/)
- [Kiali Service Mesh observability](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/service_mesh/)

Charts: `components/observability`, `components/grafana-dashboards`, `components/kiali`, `components/opentelemetry`, `components/istio-monitoring`, `components/service-interconnect`.
