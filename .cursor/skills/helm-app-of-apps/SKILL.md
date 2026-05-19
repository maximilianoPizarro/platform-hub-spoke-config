---
name: helm-app-of-apps
description: Create and extend App-of-Apps Helm charts like platform-hub-spoke-config (components, values, sync waves, testing).
---

# Helm App-of-Apps (platform-hub-spoke-config)

Use this skill when editing the **parent Helm chart** that renders Argo CD `Application` objects for each component under `components/`.

## Pattern overview

1. **Parent chart** (`Chart.yaml` + `templates/`) loops `connectivityLink.apps[]` and emits one **Application** per enabled entry (`templates/component-applications.yaml`).
2. Each **child chart** lives in `components/<name>/` with its own `Chart.yaml` and manifests.
3. Git remains the source of truth; Argo CD syncs the child chart path referenced by each Application `spec.source.path`.

## Adding a new component

1. Scaffold `components/<component-id>/` with a valid Helm chart (`Chart.yaml`, `templates/`).
2. Append an entry to **`connectivityLink.apps[]`** in the appropriate values file (`values.yaml`, `values-east.yaml`, …):

   - **`id`**: stable identifier used in Argo CD Application name (`Release.Name-id`).
   - **`path`**: directory under `components/` (matches chart folder name unless customized).
   - **`destinationNamespace`**: target namespace on the spoke/hub.
   - **`syncWave`**: string annotation `argocd.argoproj.io/sync-wave` controlling ordering.
   - **`enabled`**: toggle rendering without deleting the list entry.

3. If the component needs operator subscriptions, extend **`connectivityLink.operators.subscriptions`** with OLM `Subscription` metadata (namespace, channel, catalog source).

### External Helm charts (non-Git sources)

For third-party charts (e.g. Gitea from `dl.gitea.com/charts`), use extra fields in `connectivityLink.apps[]`:

```yaml
- id: gitea-chart
  enabled: true
  path: ""            # empty — not a local component
  repoURL: "https://dl.gitea.com/charts/"
  chart: gitea
  targetRevision: "12.5.0"
  destinationNamespace: gitea
  syncWave: "3"
```

The parent template conditionally switches between `repoURL`/`chart`/`targetRevision` (external) and `gitops.repoUrl`/`gitops.revision`/`path` (internal). Add a matching `{{- if eq .id "<id>" }}` block in `component-applications.yaml` to pass `helm.valuesObject` for the external chart.

## Connectivity Link apps array

`connectivityLink.apps[]` is the **single manifest** of which Applications exist. Keep IDs unique. Prefer disabling with `enabled: false` over deleting rows when temporarily turning off workloads—preserves history and diff clarity.

## ignoreDifferences best practices

The parent template ships defaults for OpenShift realities:

- **`Route`**: ignore `/spec/host`, `/spec/wildcardPolicy`, `/status` so Argo does not fight DNS/router-assigned hosts.
- **`Service` cluster IPs**: immutable fields assigned by the platform.
- **`Deployment`**: optional ignoring of injected annotations (operators, mesh).
- **ACM resources** (`cluster.open-cluster-management.io`, `agent.open-cluster-management.io`): ignore `/metadata/annotations`, `/metadata/labels`, `/status` — ACM controllers continuously reconcile these fields.

When adding CRDs that reconcile status heavily (Service Mesh, Kafka), consider targeted `ignoreDifferences` on status-only noise—but **never** ignore fields that encode desired state you intend Git to own.

## syncWave ordering convention

Use waves consistently across the fleet:

| Wave | Purpose |
| ---- | -------- |
| **0** | GitOps bootstrap (`openshift-gitops`) |
| **1** | Namespaces and foundational RBAC |
| **2** | Shared operators subscriptions baseline |
| **3** | Platform operators (mesh, ACM, ACS central, Developer Hub) |
| **4** | ACM hub-spoke GitOps bindings |
| **5** | Observability operators / Industrial Edge foundations |
| **6** | Apps, integrations, Connectivity Link operator |
| **7** | Hub gateway and higher-layer routing |
| **8** | Grafana dashboards and presentation-layer resources |

Keep dependent workloads **strictly greater** than their prerequisites.

## Spoke components via ApplicationSet (remote model)

Each spoke cluster has its own Helm chart in a dedicated folder (`east/`, `west/`) at the repository root. The `acm-hub-spoke` chart generates an **ApplicationSet** (`industrial-edge-spoke`) that uses a **`clusterDecisionResource`** generator from ACM `PlacementDecision` to deploy each spoke's chart **remotely** to the spoke cluster.

### Deployment flow

1. Hub Argo CD evaluates the ApplicationSet.
2. For each cluster in the PlacementDecision (e.g. `east`, `west`), it creates an Application:
   - **source.path**: `{{name}}` (resolves to `east/` or `west/`)
   - **destination.name**: `{{name}}` (deploys to the remote spoke via cluster secret)
3. The spoke chart (`east/` or `west/`) generates child Application CRs in the spoke's `openshift-gitops` namespace.
4. The spoke's own Argo CD picks up those Application CRs and syncs them locally (`server: https://kubernetes.default.svc`).

```
Hub Argo CD
  └── ApplicationSet (industrial-edge-spoke)
        ├── east-spoke-components (deployed to east cluster)
        │     └── east/ chart generates child Apps
        │           └── east's Argo CD syncs locally
        └── west-spoke-components (deployed to west cluster)
              └── west/ chart generates child Apps
                    └── west's Argo CD syncs locally
```

### Per-cluster chart structure

```
east/                          west/
├── Chart.yaml                 ├── Chart.yaml
├── values.yaml                ├── values.yaml
└── templates/                 └── templates/
    └── component-applications.yaml
```

Each chart is **self-contained**: its `values.yaml` defines `clusterName`, `deployer.domain`, `clusters.hub.domain`, `operators.subscriptions[]`, and the full `apps[]` list. No values are passed from the ApplicationSet — the charts carry all configuration.

### Adding a component to spokes

1. Create the component chart in `components/<id>/`.
2. Add the entry to **both** `east/values.yaml` and `west/values.yaml` under `apps[]`:

```yaml
apps:
  - id: <component-id>
    path: components/<component-id>
    destinationNamespace: <target-ns>
    syncWave: "<wave>"
```

3. If the component needs an operator, add the subscription to `operators.subscriptions[]` in **both** `east/values.yaml` and `west/values.yaml`.

### Adding operator subscriptions to spokes

Add new operator subscriptions to `operators.subscriptions[]` in **each spoke's `values.yaml`** (`east/values.yaml`, `west/values.yaml`). The `operators` component iterates `{{ range .Values.subscriptions }}` to render OLM Subscription CRs. **Critical**: `amq-streams` and `amq-broker-rhel8` must be in this list or Industrial Edge components will fail (missing Kafka/ActiveMQArtemis CRDs).

Current spoke components: `namespaces`, `operators`, `servicemeshoperator3`, `observability`, `acs-secured-cluster`, `spoke-dashboards`, `istio-monitoring`, `rhcl-operator`, `kiali`, `industrial-edge-tst`, `industrial-edge-stormshift`, `industrial-edge-pipelines`, `industrial-edge-minio`, `industrial-edge-data-science-cluster`, `industrial-edge-data-lake`, `industrial-edge-data-science-project`, `ie-anomaly-alerter`, `spoke-gateway`, `spoke-interconnect`, `devspaces`, `console-links`, `kubecost`.

Hub-only components (NOT in spoke charts): `kafka-console`, `grafana-dashboards`, `hub-gateway`, `service-interconnect`, `acm-hub-spoke`, `acm-operator`, `acs-operator`, `developer-hub`, `gitea`, `gitea-chart`, `mailpit`.

### Spoke cluster registration in Argo CD

Spokes must be registered as Argo CD cluster secrets before the ApplicationSet can deploy to them. The `acm-hub-spoke` chart includes `argocd-cluster-secrets.yaml` which generates secrets when `managedClusters.<name>.token` is set:

```bash
# Pass tokens at deploy time — NEVER commit tokens to Git
helm upgrade field-content . \
  --set clusters.east.token=sha256~... \
  --set clusters.west.token=sha256~...
```

Or create them directly via `oc apply` with label `argocd.argoproj.io/secret-type: cluster`.

### Hub-only resources (clusterRole guard)

Some CRDs only exist on the hub (e.g. `InferenceService` from OpenShift AI). Guard these with `{{- if ne .Values.clusterRole "spoke" }}` in the component template. Example: `components/industrial-edge-tst/templates/anomaly-detection.yaml`.

## Externalizing deployer.domain

Never hardcode cluster-specific URLs in templates. Pass **`deployer.domain`** (and `clusters.*.domain` when needed) via Helm values or `--set` flags so the same chart renders for hub, east, and west.

CI should run:

```bash
helm template test-release . -f values.yaml --set deployer.domain=apps.example.com
```

## Testing checklist

- `helm lint .` at repo root.
- `helm lint components/<chart>/` per changed component.
- `helm template` with **each** profile: `values.yaml`, `values-east.yaml`, `values-west.yaml`, optional `values-lite.yaml`.

## Profile management with values-lite.yaml

`values-lite.yaml` trims heavy subscriptions and disables optional Applications while preserving bootstrap (`openshift-gitops`, `namespaces`, `operators`, `servicemeshoperator3`) and **`industrial-edge-tst`**. Use it for labs, CI subsets, or constrained clusters—merge lessons back into full profiles when promoting features.

---

## Production lessons / troubleshooting

These issues **always happen** — plan for them upfront rather than debugging live.

### ArgoCD application-controller OOM (critical, recurring)

The default `application-controller` memory limit (2 Gi) is **not enough** when managing 15+ Applications with large CRDs (Kafka, ACM, Service Mesh). The controller gets OOMKilled, stops syncing, and all apps appear degraded.

**Fix — apply immediately after GitOps operator installation:**

```bash
oc patch argocd openshift-gitops -n openshift-gitops --type merge -p '{
  "spec": {
    "controller": {
      "resources": {
        "limits": {"memory": "4Gi"},
        "requests": {"memory": "2Gi"}
      }
    }
  }
}'
```

Consider adding this as a Helm-rendered resource at sync-wave 0 so it is always in Git.

### Java workloads OOM (machine-sensor, Camel, etc.)

Java apps with default 128 Mi memory limits will OOMKill because the JVM, Jolokia agent, and app heap together exceed 128 Mi. Set:

```yaml
resources:
  requests: { cpu: 50m, memory: 256Mi }
  limits:   { cpu: 500m, memory: 512Mi }
env:
  - name: JAVA_MAX_MEM_RATIO
    value: "50"
```

### Gitea namespace — not ambient mesh

`gitea` is in `$noMeshNamespaces` in `components/namespaces/templates/all.yaml`. **Do not** label it `istio.io/dataplane-mode: ambient`.

With ambient enabled, the Gitea chart init container `configure-gitea` fails migrating against PostgreSQL:

```text
read tcp …-><postgresql-clusterIP>:5432: read: connection reset by peer
```

PostgreSQL pod is healthy; ztunnel interception of pod→Service traffic breaks the init handshake. Same class of issue as ACS Central in `stackrox`.

Gitea chart: `connectivityLink.apps[]` entry `gitea-chart` (Helm repo `https://dl.gitea.com/charts/`, chart `gitea`). Wrapper routes/SCC: `components/gitea/`. Requires `anyuid` SCC (see below).

### ACS `stackrox` namespace — not ambient mesh

Keep `stackrox` in `$noMeshNamespaces`. Ambient breaks Central ↔ `central-db` PostgreSQL. Documented in `docs/products/acs.md`.

### OpenShift SCC for third-party images

Third-party containers (Gitea, MinIO) often run as non-root UID (e.g. 1000). OpenShift's default `restricted` SCC blocks this. Grant `anyuid`:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: <app>-anyuid
subjects:
  - kind: ServiceAccount
    name: <sa-name>
    namespace: <ns>
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:openshift:scc:anyuid
```

### Kafka 4.x requires KRaft + KafkaNodePool

Strimzi / AMQ Streams ≥ 4.x dropped ZooKeeper. Every `Kafka` CR **must** include:
- `metadata.annotations["strimzi.io/kraft": "enabled"]`
- `metadata.annotations["strimzi.io/node-pools": "enabled"]`
- A companion `KafkaNodePool` resource defining `replicas`, `roles: [broker, controller]`, and `storage`

Omitting any of these causes the operator to reject the CR silently.

### PVC WaitForFirstConsumer deadlock

Demo clusters often use `WaitForFirstConsumer` storage classes. MinIO and other stateful services get stuck waiting for a consumer pod that is itself waiting for the PVC. **Use `emptyDir` for demo/ephemeral workloads** — it avoids the deadlock and eliminates PV provisioning issues.

### Cross-cluster gateway routing (Istio ambient + OpenShift Routes)

When routing from a hub Istio Gateway to spoke cluster OpenShift Routes:

1. **Never use HTTPS/TLS origination to spoke routes** — Istio ambient mode gateway does not apply `DestinationRule` TLS settings to gateway pods. The `CERTIFICATE_VERIFY_FAILED` error is unsolvable without CA distribution.
2. **Use HTTP port 80** instead. Add `insecureEdgeTerminationPolicy: Allow` to spoke Routes so they accept plain HTTP.
3. **ServiceEntry is mandatory** — without a `ServiceEntry` for the external hostname on port 80, Envoy has no cluster definition and returns 500.
4. **Host header rewrite is mandatory** — the remote OpenShift router routes by `Host` header. Use per-backend `RequestHeaderModifier` in `HTTPRoute`:

```yaml
backendRefs:
  - name: industrial-edge-east-front
    port: 80
    weight: 50
    filters:
      - type: RequestHeaderModifier
        requestHeaderModifier:
          set:
            - name: Host
              value: line-dashboard.apps.east-cluster.example.com
```

Without this, the router returns 503 because it doesn't recognize the gateway's hostname.

5. **Socket.IO requires session affinity** — when load-balancing across multiple backends, Socket.IO's polling transport creates a `sid` on one backend that is unknown on others. Split the HTTPRoute into two rules: `/api` prefix pinned to a single backend, everything else load-balanced. Without this, every other polling request returns an error and WebSocket upgrade fails.

```yaml
rules:
  - matches:
      - path: { type: PathPrefix, value: /api }
    backendRefs:
      - name: industrial-edge-east-api
        port: 80
        weight: 100
  - backendRefs:
      - name: industrial-edge-east-front
        port: 80
        weight: 50
      - name: industrial-edge-west-front
        port: 80
        weight: 50
```

### IoT dashboard requires iot-consumer sidecar

The `iot-frontend` image is a static Apache app. It connects to a backend `iot-consumer` (Node.js + Socket.IO) that bridges MQTT sensor data to WebSocket. Without `iot-consumer` as a sidecar or separate deployment, the dashboard loads but sensors never appear.

Deploy `iot-consumer` alongside `line-dashboard` with:
- `MQTT_BROKER=mqtt://messaging:1883`
- `SOCKET_PATH=/api/service-web/socket`
- A path-based Route (`/api`) pointing to port 3000
- A ConfigMap overriding `conf/config.json` with **`websocketHost: ""`** (empty string = same origin). Never use `localhost:3000` (the image default) or an absolute cross-origin URL — Socket.IO connects to the current page's origin, and the path-based route proxies `/api` to port 3000.

### Grafana CR — operator-managed image only

**NEVER** override the Grafana container image via `deployment.spec.template.spec.containers`. The grafana-operator manages its own image version. Using a custom image (e.g. `docker.io/grafana/grafana:11.4.0`) causes persistent 401 errors because the operator's credential management and the custom image's auth expectations diverge.

```yaml
# CORRECT — let the operator manage everything
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

# WRONG — causes 401 loops, PVC password mismatch
spec:
  deployment:
    spec:
      template:
        spec:
          containers:
            - name: grafana
              image: docker.io/grafana/grafana:11.4.0
```

This pattern matches `field-sourced-content-template`. Use `auth.anonymous` with Viewer role for read-only dashboard access. Password `openshift` is the convention.

### Grafana INI section rendering

The Grafana CR `spec.config` maps to `grafana.ini` sections. Dotted section names like `auth.basic` or `auth.anonymous` must be **separate top-level keys** in the config map — NOT nested values:

```yaml
# CORRECT
config:
  auth:
    disable_login_form: "false"
  auth.anonymous:
    enabled: "true"
    org_role: Viewer

# WRONG — renders incorrectly in grafana.ini
config:
  auth:
    anonymous:
      enabled: "true"
```

### Tekton Pipeline taskRef: use cluster resolver (not ClusterTask)

Modern Tekton (v1) deprecated `ClusterTask`. Use the `resolver: cluster` pattern:

```yaml
# CORRECT (Tekton v1)
taskRef:
  resolver: cluster
  params:
    - name: kind
      value: task
    - name: name
      value: git-clone
    - name: namespace
      value: openshift-pipelines

# WRONG (deprecated, fails validation webhook)
taskRef:
  name: git-clone
  kind: ClusterTask
```

The validation webhook rejects `ClusterTask` references without `apiVersion` on newer OpenShift Pipelines versions.

### OLM ResolutionFailed — orphan CSV pattern

When OLM shows `ResolutionFailed` for multiple subscriptions with message `clusterserviceversion X exists and is not referenced by a subscription`, the fix is:

1. Delete the orphan CSV: `oc delete csv <name> -n openshift-operators`
2. Delete the affected subscription: `oc delete subscription.operators.coreos.com <name> -n openshift-operators`
3. Restart catalog-operator: `oc delete pod -n openshift-operator-lifecycle-manager -l app=catalog-operator`
4. Let ArgoCD recreate the subscription via selfHeal

This typically happens when subscriptions are deleted and recreated while the CSV from the previous install persists. The orphan CSV blocks OLM's dependency resolver for ALL subscriptions in the namespace.

### OSSM3 operator channel

`servicemeshoperator3` Subscription uses **`channel: stable-3.2`** (GA with ztunnel). Avoid `candidates` (TP2) — no ztunnel DaemonSet, broken ambient metrics and Kiali traffic graphs.

The `servicemeshoperator3` component chart deploys `Istio`, `IstioCNI`, `ZTunnel`, waypoint `Gateway`s, and `Telemetry` mesh-default — not the OLM Subscription (that lives in `components/operators`).

**`IstioCNI` must use `profile: ambient`** — same as `ZTunnel`. Without it, `istio-cni-node` logs `AmbientEnabled: false`, ztunnel cannot connect to `ztunnel.sock`, and `istio_tcp_*` never appear in Prometheus. Set `values.cni.ambient.reconcileIptablesOnStartup: true` per Red Hat OSSM 3.2 ambient install guide.

**OLM upgrade blocker** (`risk of data loss updating istiocnis.sailoperator.io`): delete `Istio` + `IstioCNI` CRs, delete sailoperator `Istio`/`IstioCNI` CRDs if stuck, reinstall subscription on `stable-3.2`, re-apply mesh manifests from Git.

### Grafana dashboards (hub + spoke)

| Chart | Dashboards | Datasources |
| ----- | ------------ | ----------- |
| `grafana-dashboards` (hub) | `east-west-traffic`, `multi-cluster-istio` | Hub Thanos + `Prometheus-East` / `Prometheus-West` via Skupper |
| `spoke-dashboards` | `local-metrics` | Local Thanos only |

Panel conventions: **gauge** for broker state, **piechart** for leader split, **bargauge** for `kafka_network_requestmetrics_requestspersec_total` and partition counts. Avoid `kafka_server_brokertopicmetrics_*` + `_objectname` filters — not exported by Strimzi JMX scrape on this platform.

Sync-wave **8** for dashboard CRs; instanceSelector `dashboards: grafana` must match Grafana CR labels in `components/observability`.

### Kiali monitoring RBAC in Git

Include `ClusterRoleBinding` `kiali-monitoring-rbac` → `cluster-monitoring-view` in `components/kiali/templates/all.yaml` **before** the Kiali CR. Set `external_services.prometheus.auth` + `thanos_proxy.enabled: true`. Without this, OSSM Console plugin returns 401 on spokes.

### Kafka Console (hub)

Component `components/kafka-console`:
- `Console` CR with five clusters (hub prod-cluster + east/west × tst/stormshift) via Skupper bootstrap URLs
- `broker-dns.yaml` — creates IE namespaces on hub as DNS shims (`industrial-edge-tst-all`, `industrial-edge-stormshift-messaging`, `industrial-edge-data-lake`) + headless Services + **`EndpointSlice`** (not `Endpoints`) mapping `advertisedHost` names to Skupper listener IPs via Helm `lookup`
- **Argo CD excludes `Endpoints`** from sync — plain Endpoints in Git are never applied; use `discovery.k8s.io/v1` EndpointSlice instead
- Store Skupper ClusterIPs in separate template variables per broker (avoid nested `lookup` in `addresses[]` — renders empty endpoints)
- Requires spoke Kafka `advertisedHost` per `clusterName` suffix in `industrial-edge-tst` / `industrial-edge-stormshift` (`dev-cluster-broker-0-east`, etc.)
- Hub subscription: `amq-streams-console` in `values.yaml` `connectivityLink.operators.subscriptions`
- Verify: Console UI `listNodes` / `listTopics` return 200 (not 504)

**Console CR simplified model** — let the operator manage its own ServiceAccount:
- Do NOT define `ServiceAccount`, `Secret`, or `ClusterRoleBinding` in Git for the Console — the operator creates `kafka-console-console-serviceaccount` automatically
- Including these in Argo CD's `ServerSideApply` causes 409 Conflicts with the operator and OpenShift SA token controller
- `kafkaClusters` entries should NOT include `namespace` or `listener` fields when connecting via Skupper bootstrap — those fields cause the operator to look up Kafka CRs locally which don't exist on the hub
- Use only `properties.values[].bootstrap.servers` for connection via Skupper listener DNS

**Hub IE namespaces are DNS shims, not workloads** — the namespaces `industrial-edge-tst-all`, `industrial-edge-stormshift-messaging`, `industrial-edge-data-lake` created by `broker-dns.yaml` on the hub exist ONLY for headless Service DNS resolution of Kafka broker advertised hostnames. They contain no Industrial Edge workloads.

### KafkaTopic finalizer cleanup (stuck Terminating namespaces)

When IE namespaces are stuck in `Terminating` state on spokes (blocking Argo CD sync), the root cause is `KafkaTopic` resources with `strimzi.io/topic-operator` finalizers. The topic operator pod is already gone so the finalizer never clears.

Fix via ManagedClusterAction Job:

```bash
oc get kafkatopic -n industrial-edge-tst-all -o name | xargs -I{} oc patch {} -n industrial-edge-tst-all --type merge -p '{"metadata":{"finalizers":[]}}'
```

### Spoke Prometheus auth — Nginx reverse proxy

Spoke Thanos Querier requires bearer token auth. Direct Skupper Connectors to Thanos return 401. Deploy an Nginx reverse proxy (`prometheus-auth-proxy`) in `service-interconnect` that:
- Reads the SA token from the mounted service account
- Injects `Authorization: Bearer <token>` header
- Proxies HTTP→HTTPS to Thanos Querier on port 9091

The Skupper Connector points to this proxy, and hub Grafana datasources use `http://` URLs (no auth needed from the hub side).

### Operator deprecation: Kuadrant → Red Hat Connectivity Link

The community `kuadrant-operator` is deprecated. Use `rhcl-operator` from `redhat-operators` catalog in namespace `redhat-connectivity-link-operator`. Delete any leftover Kuadrant CRDs before installing RHCL to avoid conflicts.

### OperatorGroup scope for namespace-scoped operators

If an operator (e.g. AMQ Broker) needs CRDs available in specific namespaces, the `OperatorGroup` in that namespace must list those namespaces in `spec.targetNamespaces[]`. For cluster-wide operators, use `spec: {}` (AllNamespaces mode).

**Kubecost operator**: requires `OwnNamespace` mode — `AllNamespaces` NOT supported. Always set:
```yaml
spec:
  targetNamespaces:
    - kubecost
```

### Kubecost SCC requirements (privileged, not anyuid)

Kubecost pods run as UID 1001 with `fsGroup: 1001` and include `seccomp` annotations incompatible with `anyuid`. Must grant **`system:openshift:scc:privileged`** to:
- `kubecost-cost-analyzer`
- `kubecost-grafana`
- `kubecost-prometheus-server`
- `kubecost-forecasting`
- `default` (used by kubecost-forecasting deployment which has no explicit `serviceAccountName`)

### Kubecost multicluster spoke deployment

Add kubecost to spoke `apps` list with path `components/kubecost` and override values:
```yaml
# In east/west templates/component-applications.yaml
{{- else if eq .id "kubecost" }}
helm:
  valuesObject:
    clusterDomain: {{ $domain }}
    clusterName: {{ $.Values.clusterName }}
    role: agent
    clusterRole: spoke
    federatedStore:
      bucket: kubecost
      endpoint: minio.industrial-edge-ml-workspace.svc.cluster.local:9000
      region: us-east-1
      accessKey: minio
      secretKey: minio123
```

### Developer Hub GitHub OAuth (non-secret in Git)

The `app-config.yaml` ConfigMap references env vars `${GITHUB_CLIENT_ID}` and `${GITHUB_CLIENT_SECRET}`. The actual credentials are in a manually-created Secret `developer-hub-github-auth` mounted via `envFrom.secretRef` in the Backstage CR deployment patch. Never commit OAuth secrets to Git.

GitHub OAuth callback URL for RHDH: `https://developer-hub.<domain>/api/auth/github/handler/frame`

### ArgoCD sync stuck or not applying changes

ArgoCD caches aggressively. When changes don't appear after push:

```bash
# Force cache invalidation
oc annotate application <app> -n openshift-gitops argocd.argoproj.io/refresh=hard --overwrite
# Clear stuck operation
oc patch application <app> -n openshift-gitops --type json -p '[{"op":"remove","path":"/operation"}]'
# Then trigger sync
oc patch application <app> -n openshift-gitops --type merge -p '{
  "operation":{"initiatedBy":{"username":"admin"},"sync":{
    "prune":true,
    "syncOptions":["CreateNamespace=true","ServerSideApply=true","SkipDryRunOnMissingResource=true"]
  }}
}'
```

Always use `ServerSideApply=true` and `SkipDryRunOnMissingResource=true` — CRDs from operators may not exist yet during dry-run, causing spurious failures.

### ConfigMap volume mounts require pod restart

When updating a ConfigMap that is mounted as a `subPath` volume (e.g. `config.json`), Kubernetes does **not** hot-reload the file. You must delete the pod (`oc delete pod -l app=<label>`) to pick up the new content. Plan for this in deployment workflows.

### clusterDecisionResource generator does NOT resolve metadata.labels

The `clusterDecisionResource` generator provides `{{name}}` and `{{server}}` from `PlacementDecision`. It does **NOT** resolve `{{metadata.labels.*}}` — those render as literal strings (e.g. `{{metadata.labels.domain}}` in Route hosts causes invalid hostnames).

To pass cluster-specific data like domains, either:
1. Use self-contained spoke charts (`east/`, `west/`) with hardcoded values (current model)
2. Use a merge generator combining `clusterDecisionResource` with a static `list` generator

### ServerSideApply conflicts with operator-managed resources

When Argo CD uses `ServerSideApply=true`, it becomes the field manager for all fields it defines. If an operator also manages the same resource (e.g. `ServiceAccount`, `Secret`), the two field managers conflict and produce 409 errors.

**Pattern**: Do NOT define resources in Git that an operator creates and manages. Let the operator be the sole owner. Examples:
- Kafka Console `ServiceAccount` → operator creates it
- `kubernetes.io/service-account-token` Secrets → OpenShift token controller manages them
- Operator-generated `ConfigMap`s and `Secret`s

If you previously defined these in Git and need to remove them, delete the live resources first (Argo CD's SSA won't remove fields it no longer defines), then let the operator recreate them.

### Hub waypoint Gateways conditional on clusterRole

The `servicemeshoperator3` component creates Istio waypoint `Gateway` resources for Industrial Edge namespaces. On the hub, these namespaces don't have workloads, so waypoints must be skipped:

```yaml
{{- if ne .Values.clusterRole "hub" }}
{{- $waypointNamespaces = append $waypointNamespaces "industrial-edge-tst-all" }}
{{- end }}
```

Pass `clusterRole: hub` from the hub's `component-applications.yaml` to `servicemeshoperator3`. Spoke charts pass `clusterRole: spoke` via their catch-all valuesObject.
