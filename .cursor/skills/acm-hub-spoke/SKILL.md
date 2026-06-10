---
name: acm-hub-spoke
description: ACM hub-spoke GitOps patterns for OpenShift—placement, ApplicationSet, cluster registration, mesh ambient, gateway, observability.
---

# ACM Hub-Spoke Platform Skill

Apply this skill when designing or troubleshooting **fleet GitOps** that combines **Red Hat ACM** with **OpenShift GitOps** and regional Industrial Edge clusters.

## Deploy Flow (ACM-first)

1. **`helm install` on hub** — creates the root App-of-Apps (`values.yaml` at repo root); all hub `components/*` Applications sync from Git.
2. **ACM imports spokes** — `ManagedCluster` + labels (`region=east|west`, `clusterset=global`).
3. **Tokens injected** — `helm upgrade --set clusters.east.token=... --set clusters.west.token=...` (never commit tokens).
4. **ApplicationSet fans out** — `industrial-edge-spoke` (persistent manifest in `components/acm-hub-spoke/templates/applicationset.yaml`, sync-wave 4) generates `east-spoke-components` / `west-spoke-components`; each spoke's Argo CD syncs `east/` or `west/` locally. See `docs/gitops-deployment-chain.md` for YAML chain.
5. **No `helm install` on spokes** — spoke charts are pushed by the hub ApplicationSet via ACM Placement + GitOpsCluster.
6. **Adding a spoke** — label + `east/` or `west/` folder + one `helm upgrade` line for domain/token.

### ApplicationSet destination (SSA pitfall)

Template must use **`destination.name` only** (cluster secret name). If an older revision left `server: https://kubernetes.default.svc`, Server-Side Apply will **not** remove it — Argo CD errors with *both name and server defined*. Fix: delete/recreate the ApplicationSet or set `server: ""` explicitly in the template.

### HBONE / sync-wave lesson

Pods created **before** ztunnel starts may lack HBONE port **15008** → `upstream connect error` on routes. **Fix:** apply `istio.io/dataplane-mode: ambient` on namespaces **after** Istio + IstioCNI + ZTunnel CRs (wave 2 in `servicemeshoperator3`, not in `namespaces` wave 1). `reconcileIptablesOnStartup: true` alone is insufficient for pods already running — restart workloads if needed.

### Kiali multi-cluster tokens

With `automateTokens: true`, the hub CronJob writes **`kiali-remote-east`** / **`kiali-remote-west`** (label `kiali.io/multiCluster=true`). Delete stale **`kiali-multi-cluster-secret`** if present — it uses the same label and causes **Unauthorized** on remote clusters.

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

### Argo CD cluster secrets (fast-path without full ACM import)

If spokes are not fully imported in ACM yet (workshop environments), register them directly as Argo CD cluster secrets. The `acm-hub-spoke` chart includes `argocd-cluster-secrets.yaml` — it renders a Secret with label `argocd.argoproj.io/secret-type: cluster` when both `apiUrl` and `token` are set:

```yaml
# components/acm-hub-spoke/templates/argocd-cluster-secrets.yaml
{{- range $name, $cluster := .Values.managedClusters }}
{{- if and $cluster.apiUrl $cluster.token }}
apiVersion: v1
kind: Secret
metadata:
  name: {{ $name }}-cluster-secret
  namespace: openshift-gitops
  labels:
    argocd.argoproj.io/secret-type: cluster
stringData:
  name: {{ $name }}
  server: {{ $cluster.apiUrl }}
  config: |
    { "bearerToken": "{{ $cluster.token }}", "tlsClientConfig": { "insecure": true } }
{{- end }}
{{- end }}
```

**NEVER commit tokens to Git.** Pass them at deploy time:

```bash
helm upgrade field-content . \
  --set clusters.east.token=sha256~... \
  --set clusters.west.token=sha256~...
```

Or create the secrets directly with `oc apply` on the hub.

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

## Single-branch multi-cluster strategy (remote GitOps model)

Instead of separate git branches per cluster, use **subdirectories** on `main`:

```
.              → hub (path: .)
east/          → east cluster (path: east)
west/          → west cluster (path: west)
components/    → shared components referenced by all
```

Each subdirectory is an independent Helm chart with its own `Chart.yaml`, `values.yaml`, and `templates/`. This avoids branch divergence, makes PRs simpler, and allows shared components.

### Remote deployment model

Each cluster has its own Argo CD instance. The hub's ApplicationSet pushes the per-cluster chart to each spoke's `openshift-gitops` namespace via remote cluster secrets. The spoke's own Argo CD then manages the child Applications locally.

**Flow:**

1. Hub Argo CD root Application: `path: .` deploys hub-only components (ACM, ACS Central, Kafka Console, Hub Gateway, etc.)
2. Hub ApplicationSet (`industrial-edge-spoke`) uses `clusterDecisionResource` generator from ACM `PlacementDecision`
3. For each spoke, the ApplicationSet creates an Application with `source.path: {{name}}` and `destination.name: {{name}}`
4. This deploys the spoke chart (`east/` or `west/`) to the remote cluster
5. The spoke chart generates child Application CRs in `openshift-gitops`
6. The spoke's own Argo CD syncs each child Application locally (`server: https://kubernetes.default.svc`)

**Key principle:** Industrial Edge components exist ONLY in spoke charts (`east/`, `west/`). The hub chart (root `.`) never includes Industrial Edge applications. Hub-only components (kafka-console, grafana-dashboards, hub-gateway, service-interconnect, acm-operator, developer-hub) are NOT in spoke charts.

### Self-contained spoke charts

Each spoke chart (`east/values.yaml`, `west/values.yaml`) carries all configuration:
- `clusterName`, `deployer.domain`, `clusters.hub.domain`
- `operators.subscriptions[]` — full list of OLM subscriptions for this spoke
- `apps[]` — full list of components to deploy

No values are passed from the ApplicationSet to the spoke charts. This makes each spoke independently deployable — a spoke's Argo CD can bootstrap directly from its folder without the hub.

## Cluster domain externalization

Store DNS in values (`deployer.domain`, `clusters.*.domain`). ACM import and Argo destinations should reference cluster secrets created by the GitOps integration—not literals committed to the repo.

For hub-specific links (Grafana, Kiali, ACS Central, Mailpit, Quay), always use `hubClusterDomain` so spoke ConsoleLinks and cross-cluster URLs point back to hub services.

**RHDP spokes:** `deployer.domain` is the **local** spoke apps domain. **`clusters.hub.domain`** must also be injected on east/west `field-content` orders — without it:
- `ie-anomaly-alerter` → `MAILPIT_URL` becomes `https://mailpit./api/v1/send`
- `acs-secured-cluster` → `central-stackrox.<hub-domain>:443` is wrong

See `docs/rhdp-field-content.md` § Spoke orders — `clusters.hub.domain`.

## Service Mesh ambient mode (multi-cluster)

### OSSM3 version: use GA stable-3.2, not Tech Preview

**Do not use** `channel: candidates` (`3.0.0-tp.2`). Tech Preview does **not** deploy **ztunnel** — ambient mode is configured at istiod but no L4 dataplane intercepts traffic, so `istio_requests_total` and Kiali traffic graphs stay empty except on ingress gateways.

Use **`channel: stable-3.2`** in `components/operators/templates/servicemeshoperator3.yaml` (OCP 4.18–4.21).

Required GitOps resources in `components/servicemeshoperator3/templates/all.yaml`:

1. **`Istio` CR** — `profile: ambient`, `PILOT_ENABLE_AMBIENT: "true"`, **`trustedZtunnelNamespace: ztunnel`**. Do **not** pin `version: v1.24.1`; let the operator choose the Istio version for 3.2. Set `values.global.multiCluster.clusterName` to the cluster identity (e.g. `east`, `west`).
2. **`IstioCNI` CR** — **`profile: ambient`** (required). Namespace-only is **not** enough: CNI starts with `AmbientEnabled: false`, never creates `/var/run/ztunnel/ztunnel.sock`, and ztunnel stays `0/N Ready` with `ZTunnelNotHealthy`.
3. **`ZTunnel` CR** + namespace `ztunnel` — deploys the per-node L4 proxy DaemonSet. **CRITICAL: set `spec.values.ztunnel.multiCluster.clusterName`** — see section below.
4. **`Telemetry` mesh-default** in `istio-system` — enables Prometheus metrics from the mesh.

### ZTunnel `multiCluster.clusterName` — CRITICAL for multi-cluster

The Sail operator does **NOT** propagate the Istio CR's `global.multiCluster.clusterName` to the ztunnel DaemonSet. By default, ztunnel gets `ISTIO_META_CLUSTER_ID=Kubernetes`, while istiod expects the configured cluster name (e.g. `east`). This causes **all ztunnel pods to stay `0/1 Running`** with:

```
XDS client connection error: status: Unauthenticated, message: "authentication failure"
```

istiod logs show:

```
Failed to authenticate client: KubeJWTAuthenticator: client claims to be in cluster "Kubernetes",
but we only know about local cluster "east" and remote clusters []
```

**Fix**: Set `clusterName` explicitly in the `ZTunnel` CR:

```yaml
apiVersion: sailoperator.io/v1
kind: ZTunnel
metadata:
  name: default
  namespace: ztunnel
spec:
  namespace: ztunnel
  values:
    ztunnel:
      multiCluster:
        clusterName: {{ .Values.clusterName }}  # east, west, etc.
```

This is already implemented in `components/servicemeshoperator3/templates/all.yaml`. The `oc set env daemonset/ztunnel` approach does NOT work because the Sail operator reconciles the DaemonSet and reverts env var changes — always patch via the `ZTunnel` CR.

**Emergency fix** (if ztunnel is broken and can't wait for ArgoCD sync):

```bash
oc patch ztunnel default -n ztunnel --type merge \
  -p '{"spec":{"values":{"ztunnel":{"multiCluster":{"clusterName":"east"}}}}}'
```

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
| `redhat-connectivity-link-operator` | `dns-operator-controller-manager` CrashLoopBackOff under ambient | `$noMeshNamespaces` |

**Currently ambient:** `industrial-edge-tst-all`, `industrial-edge-stormshift-messaging`, `industrial-edge-ml-workspace`, `industrial-edge-ci`, `ml-development`, `hub-gateway-system`, `redhat-ods-operator`, `openshift-cluster-observability-operator`, `developer-hub`, `devspaces`.

**Explicitly NOT ambient (verified):** `spoke-gateway-system` — stays off mesh. `industrial-edge-data-lake` — data lake / MinIO patterns.

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

### ReferenceGrant — required for cross-namespace HTTPRoute (install + restart)

`components/spoke-gateway/templates/all.yaml` deploys `HTTPRoute/ie-frontend` in `spoke-gateway-system` with `backendRefs` to `line-dashboard` in `industrial-edge-tst-all` (and stormshift messaging). Gateway API **requires** `ReferenceGrant` in the **target** namespace **before** the route resolves.

| Resource | Namespace | sync-wave |
| -------- | --------- | --------- |
| `ReferenceGrant/allow-spoke-gateway` | `industrial-edge-tst-all` | **2** |
| `ReferenceGrant/allow-spoke-gateway-messaging` | `industrial-edge-stormshift-messaging` | **2** |
| `HTTPRoute/ie-frontend` | `spoke-gateway-system` | **3** |

**Symptom after restart:** `https://industrial-edge.<hub-apps>/` returns **500** (empty body, `istio-envoy`) while direct spoke URL may work. On the spoke:

```bash
oc get httproute ie-frontend -n spoke-gateway-system -o jsonpath='{.status.parents[0].conditions[?(@.type=="ResolvedRefs")].message}{"\n"}'
# → backendRef line-dashboard/... not accessible (missing a ReferenceGrant?)
```

**Prevention:** Ensure `spoke-gateway` Argo app on **each spoke** (`spoke-gateway-east`, `spoke-gateway-west`) syncs **before** or **with** `industrial-edge-tst-*` and that ReferenceGrants are not pruned. Do **not** rely on manual `helm apply` in production GitOps — fix Argo sync instead.

**Verify after cold start:**

```bash
oc get referencegrant -n industrial-edge-tst-all allow-spoke-gateway
oc get httproute ie-frontend -n spoke-gateway-system -o jsonpath='ResolvedRefs={.status.parents[0].conditions[?(@.type=="ResolvedRefs")].status}{"\n"}'
curl -sk -o /dev/null -w '%{http_code}\n' https://industrial-edge.<hub-apps-domain>/
```

Hub path: `HTTPRoute/industrial-edge-lb` → `ExternalName` `industrial-edge-*-front` → Skupper `ie-gateway-east|west` → spoke `spoke-gateway-istio` → `ie-frontend` → `line-dashboard`.

### AccessToken for link establishment

Sensitive grant data (**code**, **url**, **ca**) must **not** be committed to Git. The hub chart deploys **`accesstoken-sync`** (PostSync Job + CronJob) that:

1. Reads `AccessGrant/spoke-link` **status** on the hub.
2. For each cluster in `accessTokenSync.clusters` (default `east,west`), creates `AccessToken/hub-link` on the spoke via **ManagedClusterAction**.
3. Skips spokes whose `Link/hub-link` is already **Ready** (checked via **ManagedClusterView**).

Chart: `components/service-interconnect/templates/accesstoken-sync.yaml`. CronJob schedule: **`*/30 * * * *`** (every 30 minutes; was 6h). Disable with `accessTokenSync.enabled: false` and apply tokens manually.

**Force sync** when a spoke joins late:

```bash
oc create job skupper-accesstoken-sync-manual \
  --from=cronjob/skupper-accesstoken-sync -n service-interconnect
```

**Manual fallback** (same shape as runtime apply — do not commit files like `.tmp/accesstoken-*.yaml`):

```yaml
apiVersion: skupper.io/v2alpha1
kind: AccessToken
metadata:
  name: hub-link
  namespace: service-interconnect   # same namespace as Site
spec:
  ca: "<from AccessGrant.status.ca>"
  code: "<from AccessGrant.status.code>"
  url: "<from AccessGrant.status.url>"
```

The AccessToken automatically creates a `Link` with correct TLS credentials and router endpoints. Do NOT manually create `Link` resources — the endpoints in the hub's `RouterAccess` change and the AccessToken handles this correctly.

**CRITICAL — CA certificate for AccessToken**: The Skupper grant server uses **passthrough TLS termination** on its OpenShift Route. This means it presents a self-signed certificate from its own CA (`SkupperGrantServerCA`), **NOT** the OpenShift Ingress CA.

The correct CA is found in the `skupper-grant-server-ca` secret in the Skupper namespace (typically `openshift-operators`) on the **hub** cluster:

```bash
oc get secret skupper-grant-server-ca -n openshift-operators -o jsonpath='{.data.ca\.crt}' | base64 -d
```

Using the wrong CA (e.g. OpenShift Ingress CA from `router-ca` secret) causes:

```
x509: certificate signed by unknown authority
```

The AccessToken `spec.ca` must contain the **SkupperGrantServerCA** PEM certificate, `spec.code` comes from the hub's `AccessGrant` status, and `spec.url` is the grant server Route URL.

**Verification after AccessToken creation:**

```bash
# On hub: check site count (should be 3 for hub+east+west)
oc get site -n openshift-operators -o jsonpath='{.items[0].status.sitesInNetwork}{"\n"}'
# On hub: check listeners are Ready
oc get listener -n service-interconnect
# On spoke: check link status
oc get link -n openshift-operators
```

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

### Kafka Console simplified model (no SA/Secret in Git)

The Console operator manages its own `ServiceAccount` (`kafka-console-console-serviceaccount`). Do NOT define SA, Secret (`console-metrics-token`), or ClusterRoleBinding in Git — this causes ServerSideApply 409 Conflicts between Argo CD and the operator/OpenShift SA token controller.

**Console CR `kafkaClusters`** for spoke clusters via Skupper:
- Do NOT include `namespace` or `listener` fields — these cause the operator to look up Kafka CRs locally on the hub, which don't exist
- Use only `properties.values[].bootstrap.servers` pointing to Skupper listener DNS

```yaml
kafkaClusters:
  - name: dev-cluster-east
    metricsSource: prometheus-east
    properties:
      values:
        - name: bootstrap.servers
          value: kafka-east-tst.service-interconnect.svc.cluster.local:9092
```

**Hub IE namespaces for broker DNS**: `broker-dns.yaml` creates `industrial-edge-tst-all`, `industrial-edge-stormshift-messaging`, `industrial-edge-data-lake` namespaces on the hub at sync-wave "0" — these are DNS shim namespaces for headless Service resolution of Kafka broker advertised hostnames, NOT workload namespaces.

**Spoke Prometheus metrics via Skupper**: Configure `metricsSources` entries for each spoke pointing to Skupper listeners:

```yaml
metricsSources:
  - name: prometheus-east
    type: standalone
    url: http://prometheus-east.service-interconnect.svc.cluster.local:9091
  - name: prometheus-west
    type: standalone
    url: http://prometheus-west.service-interconnect.svc.cluster.local:9091
```

### Skupper Network Observer (Network Console GUI)

Deploy the official Skupper Network Observer Helm chart (OCI) for a web GUI showing the service interconnect topology. Uses `oci://quay.io/skupper/helm/network-observer`.

**CRITICAL — TLS configuration for OpenShift Route**:

The network-observer binary binds to `127.0.0.1:8080` (localhost only) by design. An nginx reverse proxy in the same pod listens on `0.0.0.0:8443` with TLS and forwards to localhost. The OpenShift Route uses `reencrypt` termination, so the router verifies the backend certificate against the service CA.

**You MUST set `tls.openshiftIssued: true` and `tls.skupperIssued: false`** in the Helm values. Without this, the chart creates a Skupper `Certificate` CR that provisions a cert signed by the Skupper internal CA — the OpenShift router does NOT trust this CA and returns **503 Service Unavailable**.

```yaml
# In component-applications.yaml valuesObject for skupper-network-observer:
auth:
  strategy: none
route:
  enabled: true
tls:
  openshiftIssued: true
  skupperIssued: false
```

**If already deployed with the wrong TLS cert**, fix manually:

```bash
# 1. Delete the Skupper Certificate CR (prevents Skupper from recreating its cert)
oc delete certificate.skupper.io <release>-network-observer-tls -n service-interconnect

# 2. Delete the Skupper-issued secret
oc delete secret <release>-network-observer-tls -n service-interconnect

# 3. Clear stale error annotations on the service
oc annotate svc <release>-network-observer -n service-interconnect \
  service.alpha.openshift.io/serving-cert-generation-error- \
  service.alpha.openshift.io/serving-cert-generation-error-num- \
  service.alpha.openshift.io/serving-cert-signed-by- \
  service.beta.openshift.io/serving-cert-generation-error- \
  service.beta.openshift.io/serving-cert-generation-error-num- \
  service.beta.openshift.io/serving-cert-signed-by-

# 4. OpenShift service-ca will regenerate the secret with proper SANs
# 5. Restart the deployment
oc rollout restart deploy -n service-interconnect -l app.kubernetes.io/name=network-observer
```

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

### Kiali multi-cluster (hub observes east/west)

**Architecture**: Hub Kiali connects to spoke clusters using SA tokens stored in a Kubernetes Secret labeled `kiali.io/multiCluster=true`. The token sync is automated via PostSync hooks and CronJobs.

**Auth strategy — CRITICAL for multi-cluster**:

- `auth.strategy: openshift` (default) requires each user to authenticate INDIVIDUALLY to every remote cluster via the Kiali UI profile dropdown. Until a user logs into east/west, graph requests panic with `K8s Client [east/west] is not found or is not accessible for Kiali`.
- `auth.strategy: anonymous` uses Kiali's own SA tokens from secrets for ALL cluster access. No per-user auth required. **Use this for dev/demo environments.**
- For production with `openshift` strategy: deploy Kiali Operator on spokes with `remote_cluster_resources_only: true`, configure OAuthClients with redirect URIs, and users must log into each cluster from Kiali's profile dropdown.

**Prometheus TLS with anonymous strategy**: When switching to `anonymous`, Kiali loses the OpenShift service CA trust. Add `insecure_skip_verify: true` to Prometheus auth config:

```yaml
spec:
  auth:
    strategy: anonymous
  external_services:
    prometheus:
      auth:
        insecure_skip_verify: true
        type: bearer
        use_kiali_token: true
```

**Secret format (Kiali 2.22.3)**: Use a SINGLE multi-key secret where each key is the cluster name and the value is a kubeconfig YAML. Do NOT use separate secrets per cluster — Kiali 2.22.3 does not reliably detect them.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: kiali-multi-cluster-secret
  namespace: openshift-cluster-observability-operator
  labels:
    kiali.io/multiCluster: "true"
type: Opaque
stringData:
  east: |
    apiVersion: v1
    kind: Config
    contexts: [{name: east, context: {cluster: east, user: east}}]
    current-context: east
    clusters: [{name: east, cluster: {server: https://api.east:6443, certificate-authority-data: <base64-ca>}}]
    users: [{name: east, user: {token: <sa-token>}}]
  west: |
    # same structure for west
```

**Kiali CR multi-cluster config (hub)**:

```yaml
spec:
  kubernetes_config:
    cluster_name: Kubernetes    # must match Istio's multiCluster.clusterName on hub
  clustering:
    autodetect_secrets:
      enabled: true
      label: "kiali.io/multiCluster=true"
```

**Istio cluster name alignment**: Each Istio CR must report its correct cluster ID. Configure `values.global.multiCluster.clusterName` in the Sail operator Istio CR:
- Hub: `Kubernetes`
- East: `east`
- West: `west`

Without this, Kiali logs: `The controlplane cluster name ['Kubernetes'] does not match the cluster ['east']`

**Automated token sync (PostSync hooks + CronJobs)**:

1. **Spoke side** (`spoke-token-export.yaml`): PostSync Job creates a token for `kiali-service-account` and writes it to ConfigMap `kiali-hub-export`. CronJob refreshes daily.
2. **Hub side** (`multicluster-token-sync-cronjob.yaml`): PostSync Job reads spoke ConfigMaps via ACM `ManagedClusterView`, builds kubeconfig YAMLs, and upserts the multi-cluster secret. CronJob refreshes daily.

**ignoreDifferences required** (Argo CD would otherwise overwrite job-managed data):
- Spoke apps: `/data` on ConfigMap `kiali-hub-export`
- Hub app: `/data` and `/stringData` on `kiali-multi-cluster-secret`

**Traffic Graph shows "No inbound traffic"**: This means namespaces are NOT in the mesh or there's no actual traffic. Verify:
1. Namespaces labeled: `oc label ns <ns> istio.io/dataplane-mode=ambient`
2. Prometheus has `istio_requests_total` metrics: traffic flows through gateways/waypoints (L7) or ztunnel (L4 = `istio_tcp_*`)
3. Time range is wide enough in Kiali UI (try "Last 1h" or "Last 6h")

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

## Developer Hub (RHDH) — multi-cluster + scaffolder

**Full skill:** `.cursor/skills/developer-hub-scaffolder/SKILL.md`

### Auth & catalog

- **Keycloak OIDC** (`signInPage: oidc`), Secret `developer-hub-oidc-auth` — not GitHub OAuth
- Users: `catalog-users.yaml` → mountPath `/opt/app-root/src` (directory, not file — avoids `EISDIR`)
- IE catalog: `catalog-ie/industrial-edge-system.yaml` with `backstage.io/kubernetes-cluster: east|west|hub` per component
- Templates: GitHub Pages + `integrations.github` host `maximilianopizarro.github.io`

### Multi-cluster Topology

`ManagedServiceAccount` + `ClusterPermission` (east/west) → `developer-hub-spoke-token-sync` → Secret `developer-hub-spoke-tokens`. Kubernetes plugin lists hub/east/west. **Required annotation:** `backstage.io/kubernetes-cluster`.

### Scaffolder flow (test-drive-pe-oscg)

`fetch:template` → `publish:github` (Gitea) → `catalog:register` → ArgoCD app (`/api/proxy/k8s-api`) → `/api/notifications`. Proxies: gitea, k8s-api. Pipelines push to **internal registry**; Quay slug for catalog only.

### Plugins (RHDH 1.9)

Enabled via `plugins.*.enabled` flags: OCM (`/ocm` + `/clusters` alias), Kubernetes, Topology, Tekton, TechDocs, Quay, notifications (+ Mailpit email), ArgoCD CD tab, Kuadrant (`/kuadrant`), MCP. Disabled: kafka (ENOENT), kiali/grafana (no OCI). Hub `component-applications.yaml` sets `lightspeed.enabled: false` by default.

See `.cursor/skills/developer-hub-scaffolder/SKILL.md` for RBAC CSV, plugin-readiness PostSync, and scaffolder templates.

### ACS cluster registration (init bundles)

Charts: `acs-operator` (hub Central), `acs-secured-cluster` (hub + spokes), **`acs-init-bundle-sync`** (hub automation).

1. `SecuredCluster` CR alone is insufficient — needs TLS secrets from `roxctl central init-bundles generate`.
2. PostSync Job `acs-init-bundle-sync-hook` + CronJob (12h) reads `ROX_ADMIN_PASSWORD` from Secret `acs-init-credentials` in `stackrox` (runtime only).
3. Hub: apply bundle locally; spokes: **ManagedClusterAction** Job on each cluster (`hub`, `east`, `west`).
4. Manual fallback: `docs/products/acs.md` § Helm chart registration.

```bash
oc create secret generic acs-init-credentials -n stackrox \
  --from-literal=ROX_ADMIN_PASSWORD='<central-admin-password>'
```

Keep `stackrox` off Istio ambient — breaks Central ↔ PostgreSQL TLS.

### Quay + MinIO (hub)

Quay uses MinIO bucket `quay` at `minio.industrial-edge-ml-workspace.svc`. PostSync Job `minio-bucket-init` creates `quay` and `kubecost` buckets before `QuayRegistry` (sync wave 4). PostSync `quay-readiness` polls `/api/v1/discovery`. If Quay route returns 503, check MinIO bucket + Quay pod logs in `quay-registry`.

## ArgoCD resourceCustomizations → resourceHealthChecks migration

ArgoCD 2.13+ deprecated `resourceCustomizations` in the ArgoCD CR. Use `resourceHealthChecks` instead:

```yaml
# OLD (causes CRD schema errors)
spec:
  resourceCustomizations: |
    sailoperator.io/Istio:
      health.lua: |
        ...

# NEW
spec:
  resourceHealthChecks:
    - group: sailoperator.io
      kind: Istio
      check: |
        hs = {}
        hs.status = "Healthy"
        return hs
```

If the ArgoCD CR sync fails with schema validation errors on `resourceCustomizations`, migrate all custom health checks to `resourceHealthChecks` format.

## Post-restart recovery checklist

After a cluster restart (hub or spokes), verify and fix in this order:

### 1. ztunnel health (most common failure)

```bash
# Check ztunnel pods — must be 1/1 Running on every node
oc get pods -n ztunnel
oc get ztunnel -A  # STATUS must be Ready, not DaemonSetNotReady

# If 0/1 Running, check istiod for auth errors
oc logs deploy/istiod -n istio-system --tail=10 | grep "Failed to authenticate"
# If "client claims to be in cluster Kubernetes" → fix clusterName:
oc patch ztunnel default -n ztunnel --type merge \
  -p '{"spec":{"values":{"ztunnel":{"multiCluster":{"clusterName":"<east|west>"}}}}}'
```

### 2. MQTT sensors (Industrial Edge)

```bash
# Check sensor pods and broker
oc get pods -n industrial-edge-tst-all | grep -E "sensor|messaging"
# Check sensor MQTT connectivity
oc logs deploy/machine-sensor-1 -n industrial-edge-tst-all --tail=10
# If "Client is not connected" or "UnknownHostException: messaging":
oc rollout restart deploy/machine-sensor-1 deploy/machine-sensor-2 -n industrial-edge-tst-all
# If broker itself is unresponsive:
oc delete pod messaging-ss-0 -n industrial-edge-tst-all  # StatefulSet recreates it
```

Intermittent "Connection lost!" messages after successful publishes are normal MQTT Paho client behavior — the client auto-reconnects. Verify data flows by checking the `iot-consumer`:

```bash
oc logs deploy/line-dashboard -c iot-consumer -n industrial-edge-tst-all --tail=5
# Should show: handleTemperature data pump-1,...  / handleVibration data pump-1,...
```

### 3. Skupper links

```bash
# Hub: check site count (should be 3 for hub+east+west)
oc get site -n openshift-operators -o jsonpath='{.items[0].status.sitesInNetwork}{"\n"}'
# If < 3, check spoke links
oc get link -n openshift-operators  # run on spoke
```

### 4. Grafana datasources (hub)

```bash
# Verify Skupper listeners exist
oc get svc -n service-interconnect | grep -E "prometheus|ie-gateway"
# Test east/west Prometheus via Skupper
oc run prom-test --rm -i --restart=Never --image=curlimages/curl -n service-interconnect \
  -- -s 'http://prometheus-east:9091/api/v1/query?query=up' | head -c 100
```

### 5. Istio metrics flowing

```bash
# After ztunnel is healthy AND namespaces labeled with ambient:
oc run prom-test --rm -i --restart=Never --image=curlimages/curl -n service-interconnect \
  -- -s 'http://prometheus-east:9091/api/v1/query?query=istio_tcp_connections_opened_total' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('istio_tcp series:', len(d['data']['result']))"
# Should be > 0 if ambient-labeled namespaces have active connections
```

## Quick verification commands

```bash
# ACM
oc get managedcluster
oc get placement -A
oc get placementdecision -A
# ArgoCD (hub)
oc get applications -n openshift-gitops
# ArgoCD (spoke — check child apps)
# oc get applications -n openshift-gitops  (run on spoke cluster)
oc get consolelink | grep platform-
oc get consoleplugin
# Kiali/Prometheus
oc logs deploy/kiali -n openshift-cluster-observability-operator --tail=10 | grep 401
oc get servicemonitor,podmonitor -n istio-system
# Skupper (hub)
oc get site -n openshift-operators -o jsonpath='{.items[0].status.sitesInNetwork}{"\n"}'
oc get accessgrant -n openshift-operators
oc get listener -n service-interconnect
# Skupper (spoke)
# oc get link -n openshift-operators  (run on spoke cluster)
# Grafana
oc get grafana,grafanadatasource -n openshift-cluster-observability-operator
# OLM health on spokes (via MCV)
oc get csv -n openshift-operators --no-headers | grep -iE "grafana|skupper|kiali"
# OSSM Console
oc get ossmconsole -A
```
