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

### OSSM3 version: use GA stable-3.2, not Tech Preview

**Do not use** `channel: candidates` (`3.0.0-tp.2`). Tech Preview does **not** deploy **ztunnel** — ambient mode is configured at istiod but no L4 dataplane intercepts traffic, so `istio_requests_total` and Kiali traffic graphs stay empty except on ingress gateways.

Use **`channel: stable-3.2`** in `components/operators/templates/servicemeshoperator3.yaml` (OCP 4.18–4.21).

Required GitOps resources in `components/servicemeshoperator3/templates/all.yaml`:

1. **`Istio` CR** — `profile: ambient`, `PILOT_ENABLE_AMBIENT: "true"`, **`trustedZtunnelNamespace: ztunnel`**. Do **not** pin `version: v1.24.1`; let the operator choose the Istio version for 3.2.
2. **`IstioCNI` CR** — **`profile: ambient`** (required). Namespace-only is **not** enough: CNI starts with `AmbientEnabled: false`, never creates `/var/run/ztunnel/ztunnel.sock`, and ztunnel stays `0/N Ready` with `ZTunnelNotHealthy`.
3. **`ZTunnel` CR** + namespace `ztunnel` — deploys the per-node L4 proxy DaemonSet.
4. **`Telemetry` mesh-default** in `istio-system` — enables Prometheus metrics from the mesh.

**IstioCNI ambient example** (from Red Hat OSSM 3.2 docs):

```yaml
apiVersion: sailoperator.io/v1
kind: IstioCNI
metadata:
  name: default
spec:
  namespace: istio-cni
  profile: ambient
  values:
    cni:
      ambient:
        reconcileIptablesOnStartup: true
```

Verify after sync:

```bash
oc get ztunnel -n ztunnel
oc get ds -n ztunnel                    # READY must equal DESIRED
oc get istio -n istio-system -o jsonpath='{.items[0].status.state}{"\n"}'
oc logs -n istio-cni $(oc get pods -n istio-cni -o name | head -1) | grep AmbientEnabled
# Must show: AmbientEnabled: true
oc get csv -n openshift-operators | grep servicemesh
```

**ztunnel stuck / no `istio_tcp_*` metrics:** patch or sync `IstioCNI` with `profile: ambient`, wait for CNI rollout, then ztunnel pods become Ready without reinstalling OSSM.

### Ambient mesh practices

- Align identity/trust configuration across hubs and spokes before enabling strict mTLS defaults.
- Start with namespaces that already use Kafka clients and Camel integrations.
- Use **waypoints** only where L7 policy complexity justifies another hop.
- Add waypoint `Gateway` resources in the service mesh component, not in the namespace component — they require the mesh CRDs to exist first.
- Label namespaces with `istio.io/dataplane-mode: ambient` for ztunnel redirection (with GA, ztunnel must also be running).
- Scrape **ztunnel** via `PodMonitor` in namespace `ztunnel` (port `ztunnel-stats`, path `/stats/prometheus`) and grant UWM RoleBinding in `ztunnel`.

### Namespaces excluded from ambient (`components/namespaces`)

GitOps maintains two lists in `components/namespaces/templates/all.yaml`:

| List | Label / behavior |
| ---- | ---------------- |
| `$ambientNamespaces` | `istio.io/dataplane-mode: ambient` |
| `$noMeshNamespaces` | No mesh label — plain cluster networking |

**Keep off ambient (verified on hub):**

| Namespace | Symptom if ambient | Fix |
| --------- | ------------------ | --- |
| `stackrox` | ACS Central ↔ PostgreSQL TLS fails; route down or flaky | `$noMeshNamespaces` |
| `gitea` | `configure-gitea` init: `connection reset by peer` to PostgreSQL ClusterIP; pod `Init:Error` | `$noMeshNamespaces` |
| `industrial-edge-data-lake` | Data lake / MinIO patterns | `$noMeshNamespaces` |

**Currently ambient:** `industrial-edge-tst-all`, `industrial-edge-stormshift-messaging`, `industrial-edge-ml-workspace`, `industrial-edge-ci`, `ml-development`, `hub-gateway-system`, `redhat-ods-operator`, `openshift-cluster-observability-operator`, `developer-hub`, `devspaces`, `redhat-connectivity-link-operator`.

Kiali may show Gitea/ACS as outside the mesh — expected. Gitea remains reachable via Route and cluster DNS for Developer Hub / DevSpaces.

### ACS Central (hub)

- Operator + Central: `components/acs-operator` → namespace `stackrox`
- SecuredCluster hub + spokes: `components/acs-secured-cluster` (init bundles required per cluster: `hub`, `east`, `west`)
- ConsoleLink route: `central-stackrox.<hubClusterDomain>`
- Spoke operator: `rhacs-operator` subscription via ApplicationSet `openshift-operators` (not `targetNamespaces` OperatorGroup)

## Hub Gateway as F5 analog

- Implement **Gateway API** `Gateway` + routing with weighted backends for traffic shaping.
- **Use HTTP port 80 to remote OpenShift Routes**, not HTTPS/443 — Istio ambient gateway pods do not apply `DestinationRule` TLS settings, causing `CERTIFICATE_VERIFY_FAILED` errors.
- Add `insecureEdgeTerminationPolicy: Allow` to spoke Routes so they accept HTTP.
- A `ServiceEntry` for each external host is **mandatory** — without it Envoy has no cluster definition and returns 500.
- **Per-backend `RequestHeaderModifier`** is mandatory in the HTTPRoute — the remote OpenShift router routes by `Host` header and returns 503 if the header doesn't match.
- **Split `/api` into a separate HTTPRoute rule** pinned to a single backend — Socket.IO requires session affinity across polling and WebSocket requests. Without this, the `sid` token from one backend is invalid on another.
- Layer Connectivity Link policies after baseline routing works.

## Observability: Kiali + Prometheus for service mesh traffic

### Kiali auth to Prometheus (401 errors on OSSM Console plugin)

The **OSSMConsole** dynamic plugin proxies to Kiali, which queries **Thanos Querier** on port **9091**. Without RBAC, the plugin returns **401 Unauthorized** even when Kiali pods are healthy.

**GitOps fix** (preferred) in `components/kiali/templates/all.yaml`:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kiali-monitoring-rbac
roleRef:
  kind: ClusterRole
  name: cluster-monitoring-view
subjects:
- kind: ServiceAccount
  name: kiali-service-account
  namespace: openshift-cluster-observability-operator
---
# Kiali CR spec.external_services.prometheus:
prometheus:
  auth:
    type: bearer
    use_kiali_token: true
  thanos_proxy:
    enabled: true
  url: https://thanos-querier.openshift-monitoring.svc.cluster.local:9091
```

Manual equivalent:

```bash
oc adm policy add-cluster-role-to-user cluster-monitoring-view \
  -z kiali-service-account -n openshift-cluster-observability-operator
```

Deploy Kiali + `OSSMConsole` on **hub and spokes** (`values.yaml` hub component + ApplicationSet `kiali` entry). Hub shows local mesh traffic; spokes show local topology. Cross-cluster visibility uses Grafana multi-cluster dashboards + Skupper.

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
- **ztunnel** (ambient L4): port `ztunnel-stats`, path `/stats/prometheus` — namespace `ztunnel`
- **Envoy gateways/waypoints**: port `metrics` (15020), path `/stats/prometheus`
- **Envoy sidecars**: port `http-envoy-prom` (15090), path `/stats/prometheus`

**Dashboard metric expectations (OSSM3 GA + ztunnel):**
- **L4 (ztunnel)**: `istio_tcp_connections_opened_total`, `istio_tcp_sent_bytes_total`, `istio_tcp_received_bytes_total` — available once `IstioCNI` has `profile: ambient` and ztunnel DS is Ready; values stay **0** until real mesh traffic flows.
- **L7 HTTP**: `istio_requests_total` — requires traffic through **waypoints** or **ingress gateways**; hub `hub-gateway-istio` only shows rates when clients hit the gateway.
- Spoke dashboards (`spoke-dashboards`) should prefer L4 queries when L7 panels show "No data".

**Grafana dashboard panels (`grafana-dashboards`, `spoke-dashboards`):**
- Use **gauge** for Kafka `kafka_server_kafkaserver_brokerstate` (3 = Running) and under-replicated partitions.
- Use **piechart** (donut) for leader partition split (East vs West on hub).
- Use **bargauge** for `kafka_network_requestmetrics_requestspersec_total` and `kafka_server_replicamanager_partitioncount` — these JMX metrics are always scraped.
- **Do not** use `kafka_server_brokertopicmetrics_*` with `_objectname=~".*OneMinuteRate.*"` — that MBean naming is not present in Strimzi JMX export on this platform; panels stay empty.
- Hub `east-west-traffic` uses templated datasources `${ds_east}` / `${ds_west}`; spoke `local-metrics` uses default Prometheus only.

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

### Prometheus metrics export via Skupper (auth proxy pattern)

Thanos Querier on spoke clusters requires a bearer token for authentication. Connecting Skupper directly to Thanos returns 401. The solution is an **Nginx reverse proxy** on each spoke that injects the service account token:

```
spoke cluster:
  prometheus-auth-proxy (nginx:9091 HTTP)
    → injects SA bearer token
    → forwards to thanos-querier:9091 HTTPS
  Skupper Connector → prometheus-auth-proxy:9091
hub cluster:
  Skupper Listener → prometheus-east:9091 (HTTP, no auth needed)
  Grafana datasource → http://prometheus-east.service-interconnect.svc:9091
```

Key resources per spoke (in `spoke-interconnect` component):

1. **ServiceAccount** `prometheus-auth-proxy` with `cluster-monitoring-view` ClusterRoleBinding
2. **Secret** (type `kubernetes.io/service-account-token`) for the SA
3. **ConfigMap** with Nginx config that proxies to Thanos and injects `Authorization: Bearer <token>`
4. **Deployment** with init container that reads the SA token and injects it into the Nginx config via `sed`
5. **Service** exposing port 9091
6. **Skupper Connector** pointing to `prometheus-auth-proxy.service-interconnect.svc:9091` (NOT directly to Thanos)

**CRITICAL — nginx image selection**: Use `nginxinc/nginx-unprivileged:alpine` as the container image. Do NOT use `registry.access.redhat.com/ubi9/nginx-124:latest` — that is an S2I builder image that prints a help message and exits immediately with code 0, causing CrashLoopBackOff. The unprivileged image reads `/etc/nginx/nginx.conf` and starts nginx as expected.

Hub Grafana datasources use `http://` (no TLS, no bearer token needed — the proxy handles both):

```yaml
datasource:
  url: http://prometheus-east.service-interconnect.svc.cluster.local:9091
```

### Kafka bootstrap via Skupper (hub Kafka Console)

Expose spoke Kafka bootstrap services to the hub with Skupper **Connector** (spoke) + **Listener** (hub) on port **9092** (`kafka-east-tst`, `kafka-west-tst`, `kafka-east-stormshift`, `kafka-west-stormshift`).

**Metadata DNS problem:** After connecting to bootstrap, the Kafka client receives **broker advertised addresses** like `dev-cluster-broker-0.dev-cluster-kafka-brokers.industrial-edge-tst-all.svc:9092`. Those names do not resolve on the hub → `Timed out waiting for a node assignment` / `listNodes` 504.

**Fix (two parts):**

1. **Spokes** — per-broker `advertisedHost` in Strimzi listener `configuration.brokers` using `clusterName` suffix:
   - `dev-cluster-broker-0-{{ .Values.clusterName }}.dev-cluster-kafka-brokers.industrial-edge-tst-all.svc.cluster.local`
   - `factory-cluster-broker-0-{{ .Values.clusterName }}.factory-cluster-kafka-brokers.industrial-edge-stormshift-messaging.svc.cluster.local`

2. **Hub** — `components/kafka-console/templates/broker-dns.yaml`: headless `Service` + `Endpoints` in the Industrial Edge namespaces mapping each `hostname` to the Skupper listener ClusterIP. Uses Helm `lookup` at ArgoCD sync time — re-sync `kafka-console` after Skupper listeners exist.

Console CR (`components/kafka-console`) registers four clusters via bootstrap Skupper DNS; `amq-streams-console` operator subscription on hub.

### Kafka Console metrics configuration

The `Console` CR `metricsSources` type `openshift-monitoring` may NOT work in all operator versions (logs: `Prometheus URL is not configured`). Use **`type: standalone`** with explicit Thanos Querier URL instead:

```yaml
metricsSources:
  - name: thanos
    type: standalone
    url: https://thanos-querier.openshift-monitoring.svc.cluster.local:9091
    authentication:
      bearer:
        token:
          valueFrom:
            secretKeyRef:
              name: console-metrics-token
              key: token
    trustStore:
      type: PEM
      content:
        valueFrom:
          configMapKeyRef:
            name: openshift-service-ca.crt
            key: service-ca.crt
```

Required supporting resources:
1. **Secret** `console-metrics-token` (type `kubernetes.io/service-account-token`) for the SA `kafka-console-console-serviceaccount`
2. **ClusterRoleBinding** `kafka-console-monitoring-view` → `cluster-monitoring-view` for that SA
3. **Each `kafkaCluster` entry MUST include `namespace`** — without it logs show `namespace is required for metrics retrieval but none was provided`
4. Metrics only appear for clusters whose Kafka pods run **in the same cluster** as the Console (hub metrics visible, spoke metrics require remote-write or federation)
5. The `openshift-service-ca.crt` ConfigMap (auto-injected by OpenShift in every namespace) provides the CA for Thanos TLS
6. The hub `prod-cluster` (namespace `industrial-edge-data-lake`) has full metrics; spoke clusters connected via Skupper only show topics/nodes without metrics unless Prometheus federation is configured

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

## Grafana configuration (aligned with field-sourced-content-template)

### Grafana CR — let the operator manage the image

**NEVER** override the Grafana container image in `deployment.spec`. The grafana-operator manages its own version. Custom images (e.g. `docker.io/grafana/grafana:11.4.0`) cause persistent 401 errors because the operator's credential management expects its own image.

```yaml
apiVersion: grafana.integreatly.org/v1beta1
kind: Grafana
metadata:
  name: grafana
  labels:
    dashboards: grafana
spec:
  config:
    auth:
      disable_login_form: "false"
    auth.anonymous:
      enabled: "true"
      org_role: Viewer
    security:
      admin_user: admin
      admin_password: openshift
  route:
    spec:
      host: grafana.{{ .Values.clusterDomain }}
      tls:
        termination: edge
```

Key rules:
- **No `deployment.spec`** — no custom image, no `GF_SECURITY_*` env vars
- **`auth.anonymous`** enabled with Viewer role — allows dashboard access without login
- **Password `openshift`** — consistent with field-sourced-content-template convention
- **No `auth.basic`** section needed — anonymous auth covers read access
- **No `server.root_url`** or `log.mode` — keep config minimal

### Hub Grafana datasources

- **Local Prometheus**: points to `thanos-querier.openshift-monitoring.svc:9091` with SA bearer token via `valuesFrom` + `secretKeyRef`
- **Remote East/West**: point to `http://prometheus-east.service-interconnect.svc:9091` (HTTP, no auth — Skupper proxy handles it)

### Spoke Grafana

Spokes deploy the same `observability` component. The Grafana CR is identical. Spoke dashboards (`spoke-dashboards` component) only contain a `local-metrics` GrafanaDashboard CR, no additional datasources.

**Verify dashboards have data** (from hub or spoke):

```bash
TOKEN=$(oc create token grafana-thanos-reader -n openshift-cluster-observability-operator --duration=600s)
oc run promq --rm -i --restart=Never --image=curlimages/curl:latest --command -- sh -c \
  "curl -sk -H 'Authorization: Bearer $TOKEN' \
   'https://thanos-querier.openshift-monitoring.svc:9091/api/v1/query?query=count(kafka_server_kafkaserver_brokerstate==3)'"
# East via Skupper (hub only):
oc run promq --rm -i --restart=Never --image=curlimages/curl:latest --command -- \
  curl -sk 'http://prometheus-east.service-interconnect.svc:9091/api/v1/query?query=sum(kafka_network_requestmetrics_requestspersec_total)'
```

Route: `oc get route grafana-route -n openshift-cluster-observability-operator -o jsonpath='https://{.spec.host}{"\n"}'`

## ManagedClusterAction / ManagedClusterView limitations

### Subscription API group ambiguity

`ManagedClusterAction` with `resource: subscription` always resolves to `subscriptions.apps.open-cluster-management.io`, NOT `subscriptions.operators.coreos.com`. The `apiGroup` field is ignored for Delete actions. To delete OLM subscriptions on spoke clusters, you **must** use a Job:

```yaml
apiVersion: action.open-cluster-management.io/v1beta1
kind: ManagedClusterAction
metadata:
  name: delete-olm-subs
  namespace: <spoke>
spec:
  actionType: Create
  kube:
    resource: job
    namespace: openshift-operators
    template:
      apiVersion: batch/v1
      kind: Job
      metadata:
        name: delete-olm-subs
        namespace: openshift-operators
      spec:
        ttlSecondsAfterFinished: 120
        template:
          spec:
            serviceAccountName: <sa-with-cluster-admin>
            restartPolicy: Never
            containers:
              - name: fix
                image: registry.redhat.io/openshift4/ose-cli:latest
                command: ["/bin/bash", "-c"]
                args:
                  - oc delete subscription.operators.coreos.com <name> -n openshift-operators
```

For `ManagedClusterView`, the same ambiguity applies — use Jobs + ConfigMap output pattern to read OLM subscription details on spoke clusters.

### MCA Delete works for unambiguous resources

`ManagedClusterAction` Delete works correctly for resources with unique API groups:
- `ClusterServiceVersion` (`operators.coreos.com`) — works
- `ConfigMap`, `Secret`, `Job` — works
- `Subscription` — **broken** (API group conflict)

## OLM ResolutionFailed on spoke clusters

### Root cause: orphan CSVs

When a CSV exists in a namespace but is not referenced by any Subscription, OLM's dependency resolver fails for ALL subscriptions in that namespace. Error pattern:

```
constraints not satisfiable: clusterserviceversion <name> exists and is not
referenced by a subscription, subscription <name> exists, subscription <name>
requires at least one of ...
```

### Fix procedure

1. **Delete the orphan CSV** (via MCA Delete or Job):
   ```bash
   oc delete csv grafana-operator.v5.22.2 -n openshift-operators
   ```
2. **Delete the Subscription** (via Job — MCA Delete won't work):
   ```bash
   oc delete subscription.operators.coreos.com grafana-operator -n openshift-operators
   ```
3. **Restart the catalog-operator** to clear OLM's resolution cache:
   ```bash
   oc delete pod -n openshift-operator-lifecycle-manager -l app=catalog-operator
   ```
4. **Hard-refresh ArgoCD** to recreate the Subscription:
   ```bash
   oc annotate application operators-east -n openshift-gitops argocd.argoproj.io/refresh=hard --overwrite
   ```

The Service Account used by Jobs on spokes needs `cluster-admin`. Create a temporary ClusterRoleBinding via MCA:

```yaml
apiVersion: action.open-cluster-management.io/v1beta1
kind: ManagedClusterAction
spec:
  actionType: Create
  kube:
    resource: clusterrolebinding
    template:
      apiVersion: rbac.authorization.k8s.io/v1
      kind: ClusterRoleBinding
      metadata:
        name: <sa>-admin-temp
      roleRef:
        apiGroup: rbac.authorization.k8s.io
        kind: ClusterRole
        name: cluster-admin
      subjects:
        - kind: ServiceAccount
          name: <sa>
          namespace: <ns>
```

## OLM cleanup with direct cluster access

When you have direct `oc login` credentials to the spoke cluster (preferred over MCA+Job):

```bash
# 1. Identify orphan CSVs
oc get csv -n openshift-operators --no-headers | grep -v Succeeded

# 2. Delete orphan CSV
oc delete csv <orphan-csv-name> -n openshift-operators

# 3. Delete stuck subscriptions
oc delete subscription.operators.coreos.com grafana-operator kiali-ossm skupper-operator -n openshift-operators

# 4. Restart catalog-operator to clear cache
oc delete pod -n openshift-operator-lifecycle-manager -l app=catalog-operator

# 5. Wait ~15s, then verify subscriptions are recreated by ArgoCD
#    If selfHeal doesn't recreate them, manually apply:
oc apply -f - <<EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: grafana-operator
  namespace: openshift-operators
spec:
  channel: v5
  installPlanApproval: Automatic
  name: grafana-operator
  source: community-operators
  sourceNamespace: openshift-marketplace
EOF

# 6. Force ArgoCD refresh from hub
oc annotate application operators-west -n openshift-gitops argocd.argoproj.io/refresh=hard --overwrite
```

## Kubecost multicluster (Federated ETL)

Red Hat certified Kubecost operator deployed via `components/kubecost/` as hub primary + spoke agents:

### Hub (primary aggregator)
- `OperatorGroup` with `targetNamespaces: [kubecost]` (OwnNamespace mode — **AllNamespaces NOT supported**)
- `CostAnalyzer` CR with `federatedETL.federatedCluster: true`, `agentOnly: false`, `kubecostAggregator.deployMethod: statefulset`
- Route `kubecost.<clusterDomain>` on port 9090
- ConsoleLink in OpenShift console menu

### Spokes (agents)
- Same chart with `role: agent`, `clusterRole: spoke` → `agentOnly: true`, no aggregator
- Must include same `OperatorGroup` with `targetNamespaces: [kubecost]`
- Federated store secret pointing to hub MinIO (`minio.industrial-edge-ml-workspace.svc.cluster.local:9000`)

### SCC requirements (critical)
Kubecost pods run as UID 1001 with `fsGroup: 1001` and `seccomp` annotations. Grant **`privileged`** SCC (not just `anyuid`) to ALL service accounts:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kubecost-privileged-scc
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:openshift:scc:privileged
subjects:
  - kind: ServiceAccount
    name: kubecost-cost-analyzer
    namespace: kubecost
  - kind: ServiceAccount
    name: kubecost-grafana
    namespace: kubecost
  - kind: ServiceAccount
    name: kubecost-prometheus-server
    namespace: kubecost
  - kind: ServiceAccount
    name: kubecost-forecasting
    namespace: kubecost
  - kind: ServiceAccount
    name: default       # kubecost-forecasting uses default SA
    namespace: kubecost
```

**Common errors:**
- `AllNamespaces InstallModeType not supported` → OperatorGroup missing `targetNamespaces`
- `forbidden: unable to validate against any security context constraint` → missing privileged SCC binding
- `kubecost-forecasting` deployment does NOT set `serviceAccountName` → uses `default` SA

## Developer Hub (RHDH) GitHub OAuth

Catalog users (e.g. workshop GitHub accounts) can be provisioned via `components/developer-hub/templates/catalog-users.yaml` and mounted into the Backstage catalog. Set `dangerouslyAllowSignInWithoutUserInCatalog: true` under `auth.providers.github.production.signIn.resolvers` (not at the root of `app-config`).

Configure GitHub sign-in in `app-config.yaml`:

```yaml
auth:
  environment: production
  providers:
    github:
      production:
        clientId: ${GITHUB_CLIENT_ID}
        clientSecret: ${GITHUB_CLIENT_SECRET}
signInPage: github
```

- Mount credentials via `envFrom.secretRef` in the Backstage CR deployment patch
- Secret `developer-hub-github-auth` created **manually** (never in Git)
- GitHub OAuth App callback URL: `https://developer-hub.<domain>/api/auth/github/handler/frame`
- **NOT** `/api/oauth/callback` — that path is incorrect for Backstage

### RHDH dynamic plugins known issues (RHDH 1.9)
These plugins fail with `npm pack ENOENT` and must be `disabled: true`:
- `backstage-community-plugin-argocd`
- `backstage-community-plugin-kafka-backend-dynamic` / `backstage-community-plugin-kafka`
- `kuadrant-backstage-plugin-backend-dynamic` / `kuadrant-backstage-plugin-frontend`
- `roadiehq-backstage-plugin-argo-cd-backend-dynamic`
- `backstage-community-plugin-redhat-argocd`

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
# Grafana
oc get grafana,grafanadatasource -n openshift-cluster-observability-operator
# OLM health on spokes (via MCV)
oc get csv -n openshift-operators --no-headers | grep -iE "grafana|skupper|kiali"
# OSSM Console
oc get ossmconsole -A
```
