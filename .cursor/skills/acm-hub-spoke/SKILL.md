---
name: acm-hub-spoke
description: ACM hub-spoke GitOps patterns for OpenShift—placement, ApplicationSet, cluster registration, mesh ambient, gateway, observability.
---

# ACM Hub-Spoke Platform Skill

Apply this skill when designing or troubleshooting **fleet GitOps** that combines **Red Hat ACM** with **OpenShift GitOps** and regional Industrial Edge clusters.

## ACM operator installation

- Install from stable channels appropriate to your OpenShift version.
- Confirm **`MultiClusterHub`** reaches Running before registering spokes.
- Keep klusterlet versions compatible with hub; watch ACM upgrade docs during z-stream bumps.
- **ACM console is a plugin, not a separate route.** Since ACM 2.x on OpenShift 4.x, the UI is integrated into the OpenShift Console via `consoleplugin/acm`. Access it at `Infrastructure > Clusters` or navigate to `/multicloud/infrastructure/clusters`. There is no standalone `multicloud-console` route.

## Automated cluster registration via GitOps

Register managed clusters declaratively by templating `ManagedCluster` and `KlusterletAddonConfig` in Helm:

```yaml
{{- range $name, $cluster := .Values.managedClusters }}
{{- if $cluster.apiUrl }}
---
apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: {{ $name }}
  labels:
    name: {{ $name }}
    region: {{ $name }}
    cloud: auto-detect
    vendor: OpenShift
    cluster.open-cluster-management.io/clusterset: global
spec:
  hubAcceptsClient: true
  leaseDurationSeconds: 60
---
apiVersion: agent.open-cluster-management.io/v1
kind: KlusterletAddonConfig
metadata:
  name: {{ $name }}
  namespace: {{ $name }}
spec:
  clusterName: {{ $name }}
  clusterNamespace: {{ $name }}
  applicationManager: { enabled: true }
  certPolicyController: { enabled: true }
  policyController: { enabled: true }
  searchCollector: { enabled: true }
{{- end }}
{{- end }}
```

Pass `managedClusters.east.apiUrl` and `managedClusters.west.apiUrl` via values. After ArgoCD syncs these resources, manually create the `auto-import-secret` in each cluster namespace to complete the join:

```bash
oc create secret generic auto-import-secret \
  -n east \
  --from-literal=token=sha256~<spoke-token> \
  --from-literal=server=https://api.east-cluster:6443
oc label secret auto-import-secret -n east managedcluster-import=true
```

### ignoreDifferences for ACM resources

ACM controllers continuously update annotations, labels, and status on `ManagedCluster` and `KlusterletAddonConfig`. Add these to the Application's `ignoreDifferences` to prevent ArgoCD from reporting constant drift:

```yaml
ignoreDifferences:
  - group: cluster.open-cluster-management.io
    kind: "*"
    jsonPointers: [/metadata/annotations, /metadata/labels, /status]
  - group: agent.open-cluster-management.io
    kind: "*"
    jsonPointers: [/metadata/annotations, /status]
```

## Placement, GitOpsCluster, ApplicationSet

1. **ManagedClusterSet** groups clusters for RBAC boundaries.
2. **Placement** expresses label selectors (for example `region=east`).
3. **PlacementDecision** materializes matching cluster names for generators.
4. **GitOpsCluster** wires those clusters into Argo CD's managed cluster inventory.
5. **ApplicationSet** uses generators (matrix, cluster-decision, SCM) to stamp `Application` resources without per-cluster Git forks.

Prefer label-driven placement over embedding kube-apiserver URLs in Git.

## Single-branch multi-cluster strategy

Instead of separate git branches per cluster, use **subdirectories** on `main`:

```
.              → hub (path: .)
east/          → east cluster (path: east)
west/          → west cluster (path: west)
components/    → shared components referenced by all
```

Each subdirectory is an independent Helm chart with its own `Chart.yaml`, `values.yaml`, and `templates/`. The hub ArgoCD Application uses `path: .` and east/west use `path: east` and `path: west`. This avoids branch divergence, makes PRs simpler, and allows shared components.

## Cluster domain externalization

Store DNS in values (`deployer.domain`, `clusters.*.domain`). ACM import and Argo destinations should reference cluster secrets created by the GitOps integration—not literals committed to the repo.

For hub-specific links (Grafana, Kiali, ACM), always use `hubClusterDomain` so spoke ConsoleLinks point back to hub services.

## Service Mesh ambient mode (multi-cluster)

- Align identity/trust configuration across hubs and spokes before enabling strict mTLS defaults.
- Start with namespaces that already use Kafka clients and Camel integrations.
- Use **waypoints** only where L7 policy complexity justifies another hop.
- Add waypoint `Gateway` resources in the service mesh component, not in the namespace component — they require the mesh CRDs to exist first.
- Label namespaces with `istio.io/dataplane-mode: ambient` for ztunnel injection.

## Hub Gateway as F5 analog

- Implement **Gateway API** `Gateway` + routing with weighted backends for traffic shaping.
- **Use HTTP port 80 to remote OpenShift Routes**, not HTTPS/443 — Istio ambient gateway pods do not apply `DestinationRule` TLS settings, causing `CERTIFICATE_VERIFY_FAILED` errors.
- Add `insecureEdgeTerminationPolicy: Allow` to spoke Routes so they accept HTTP.
- A `ServiceEntry` for each external host is **mandatory** — without it Envoy has no cluster definition and returns 500.
- **Per-backend `RequestHeaderModifier`** is mandatory in the HTTPRoute — the remote OpenShift router routes by `Host` header and returns 503 if the header doesn't match.
- **Split `/api` into a separate HTTPRoute rule** pinned to a single backend — Socket.IO requires session affinity across polling and WebSocket requests. Without this, the `sid` token from one backend is invalid on another.
- Layer Connectivity Link policies after baseline routing works.

## Observability: Kiali + Prometheus for service mesh traffic

### Kiali auth to Prometheus (401 errors)

Kiali needs explicit credentials to reach Prometheus and Grafana. Without this, Kiali loads but shows no traffic graphs:

```bash
# Grant Prometheus read access to Kiali's service account
oc adm policy add-cluster-role-to-user cluster-monitoring-view \
  -z kiali-service-account -n openshift-cluster-observability-operator

# Configure Kiali to use its own token for Prometheus
oc patch kiali kiali -n openshift-cluster-observability-operator --type merge -p '{
  "spec": {
    "external_services": {
      "prometheus": { "auth": { "type": "bearer", "use_kiali_token": true } },
      "grafana": { "auth": { "type": "basic", "username": "admin", "password": "admin" } }
    }
  }
}'
```

### Prometheus scraping Istio metrics

By default, OpenShift Prometheus does **not** scrape Istio. Create ServiceMonitor/PodMonitor resources:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: istiod-monitor
  namespace: istio-system
spec:
  selector:
    matchLabels: { app: istiod }
  endpoints:
    - port: http-monitoring
      interval: 15s
      path: /metrics          # istiod uses /metrics, NOT /stats/prometheus
---
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: istio-proxies
  namespace: istio-system
spec:
  selector:
    matchExpressions:
      - { key: istio.io/gateway-name, operator: Exists }
  podMetricsEndpoints:
    - port: metrics           # port 15020
      interval: 15s
      path: /stats/prometheus  # Envoy proxies use /stats/prometheus
  namespaceSelector: { any: true }
```

**Critical**: The User Workload Prometheus needs RoleBindings in each mesh namespace to scrape pods:

```bash
for NS in istio-system hub-gateway-system industrial-edge-tst-all industrial-edge-data-lake; do
  oc create rolebinding prometheus-user-workload -n $NS \
    --clusterrole=prometheus-k8s \
    --serviceaccount=openshift-user-workload-monitoring:prometheus-user-workload
done
```

Without these RoleBindings, targets appear as 0 in Prometheus even though ServiceMonitors exist.

**Metrics path cheat-sheet:**
- **istiod**: port `http-monitoring` (15014), path `/metrics`
- **Envoy gateways/waypoints**: port `metrics` (15020), path `/stats/prometheus`
- **Envoy sidecars**: port `http-envoy-prom` (15090), path `/stats/prometheus`

## ConsoleLinks for multi-cluster navigation

Define ConsoleLinks in a dedicated component with role-based rendering (`hub`/`spoke`):

- **Common links** (all clusters): Industrial Edge, Grafana, Kiali → point to `hubClusterDomain`
- **Hub-only links**: ACM Clusters (→ `/multicloud/infrastructure/clusters`), ACS Central, Developer Hub, Gitea, MinIO
- **Spoke-only links**: usually none — operators (DevSpaces, ArgoCD) create their own ConsoleLinks automatically
- **Avoid duplicating** links that operators already create (ArgoCD, DevSpaces)

## Service Interconnect (Skupper) for cross-cluster exposure

Skupper v2alpha1 creates a Virtual Application Network (VAN) linking hub and spoke clusters. Key resources:

- **Hub**: `Site`, `AccessGrant`, `Listener` (per exposed service)
- **Spoke**: `Site`, `AccessToken` (from hub grant), `Connector` (per local service to expose)

### Spoke gateway aggregation pattern

Instead of exposing every Industrial Edge service individually via Skupper, deploy a **spoke-gateway** (Gateway API `Gateway` + `HTTPRoute`) that aggregates all services behind a single entry point. Skupper then exposes only this gateway.

```yaml
# spoke-interconnect: Connector pointing to the spoke-gateway
apiVersion: skupper.io/v2alpha1
kind: Connector
metadata:
  name: ie-gateway-{{ .Values.clusterName }}
  namespace: service-interconnect
spec:
  routingKey: ie-gateway-{{ .Values.clusterName }}
  host: spoke-gateway-istio.spoke-gateway-system.svc.cluster.local
  port: 8080
```

### AccessToken for link establishment

The `AccessToken` on spokes is created manually (via `ManagedClusterAction`) because it contains sensitive claim data (ca, code, url from the hub's `AccessGrant`). Do NOT store AccessTokens in Git.

```yaml
apiVersion: skupper.io/v2alpha1
kind: AccessToken
metadata:
  name: hub-token
  namespace: service-interconnect
spec:
  ca: "<hub-grant-ca>"
  code: "<hub-grant-code>"
  url: "<hub-grant-url>"
```

The AccessToken automatically creates a `Link` with correct TLS credentials and router endpoints. Do NOT manually create `Link` resources — the endpoints in the hub's `RouterAccess` change and the AccessToken handles this correctly.

### Prometheus metrics export via Skupper

Add a second `Connector` on each spoke to expose `thanos-querier`:

```yaml
apiVersion: skupper.io/v2alpha1
kind: Connector
metadata:
  name: prometheus-{{ .Values.clusterName }}
spec:
  routingKey: prometheus-{{ .Values.clusterName }}
  host: thanos-querier.openshift-monitoring.svc.cluster.local
  port: 9091
```

Hub Grafana datasources then point to `prometheus-east.service-interconnect.svc.cluster.local:9091` and `prometheus-west.service-interconnect.svc.cluster.local:9091`.

## Kiali + OSSM Console plugin

Deploy Kiali with the `OSSMConsole` CR on both hub and spokes to activate the dynamic console plugin:

```yaml
apiVersion: kiali.io/v1alpha1
kind: OSSMConsole
metadata:
  name: ossmconsole
  namespace: openshift-cluster-observability-operator
spec:
  version: default
  kiali:
    serviceName: kiali
    serviceNamespace: openshift-cluster-observability-operator
```

The `kiali-ossm` operator subscription must be deployed before the CR. Add it to the `subscriptions` list in the ApplicationSet `valuesObject` for the `operators` component.

## Grafana dashboards for east-west

- Hub Grafana has three datasources: Hub (local Thanos), Prometheus-East (via Skupper), Prometheus-West (via Skupper).
- Dashboard variables `ds_east` and `ds_west` select the remote datasources.
- Spoke Grafana instances have a single local Prometheus datasource with `local-metrics` dashboard.
- Configure `[auth.basic] enabled = true` as a separate INI section (NOT a nested value under `[auth]`) to avoid 401 errors on the Grafana API.

## Quick verification commands

```bash
oc get managedcluster
oc get placement -A
oc get placementdecision -A
oc get applications -n openshift-gitops
oc get consolelink | grep platform-
oc get consoleplugin
# Kiali/Prometheus
oc logs deploy/kiali -n openshift-cluster-observability-operator --tail=10 | grep 401
oc get servicemonitor,podmonitor -n istio-system
# Skupper
oc get site,accessgrant,listener -n service-interconnect
oc get grafanadatasource -n openshift-cluster-observability-operator
# OSSM Console
oc get ossmconsole -A
```
