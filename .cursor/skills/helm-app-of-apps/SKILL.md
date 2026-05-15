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

### Operator deprecation: Kuadrant → Red Hat Connectivity Link

The community `kuadrant-operator` is deprecated. Use `rhcl-operator` from `redhat-operators` catalog in namespace `redhat-connectivity-link-operator`. Delete any leftover Kuadrant CRDs before installing RHCL to avoid conflicts.

### OperatorGroup scope for namespace-scoped operators

If an operator (e.g. AMQ Broker) needs CRDs available in specific namespaces, the `OperatorGroup` in that namespace must list those namespaces in `spec.targetNamespaces[]`. For cluster-wide operators, use `spec: {}` (AllNamespaces mode).

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
