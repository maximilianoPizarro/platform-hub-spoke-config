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
