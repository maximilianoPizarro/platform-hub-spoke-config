---
layout: default
title: Troubleshooting
nav_order: 13
---

# Troubleshooting

Production lessons from fleet GitOps, ambient mesh, and centralized observability. See also ebook Ch.15 matrix (adapted below).

## Symptom matrix

| Symptom | Likely cause | Fix |
| ------- | ------------ | --- |
| `upstream connect error` / 503 on mesh routes | HBONE port 15008 not configured (pod before ztunnel) | Restart pods in ambient namespaces; ensure ambient labels at sync-wave **2** after Istio/ZTunnel |
| ApplicationSet Degraded: *both name and server* | Stale `destination.server` from older template (SSA) | Delete/recreate ApplicationSet or set `server: ""` in template |
| ACM UI: *no Argo applications created* | ApplicationSet missing `cluster.open-cluster-management.io/placement` label | Label ApplicationSet + child Apps; verify with `oc get applications -n openshift-gitops \| grep spoke` |
| Kiali: `Unauthorized` on east/west | Stale **`kiali-multi-cluster-secret`** or expired spoke token | Delete aggregate secret; run token-sync job; restart Kiali pod |
| Kafka Console: `/api/kafkas` 404 | External route hits UI only; Next.js does not proxy `/api` | Enable `apiRoute` in `components/kafka-console`; verify HTTP 200 on `/api/kafkas` |
| Strimzi entity-operator CrashLoop | mTLS on 9091 conflicts with ztunnel | Exclude operator namespace from ambient or use documented Strimzi tuning |
| Skupper listener not Ready | Site or token not synced | Check `oc get site,listener -n service-interconnect` on hub and spoke |

---

## HBONE port 15008 not configured

**Symptom:** Routes return `upstream connect error` or 503; ztunnel logs show missing HBONE listener for pod IP.

**Cause:** Workloads started **before** ambient enrollment or before ztunnel programmed iptables.

**Fix:**

1. Ensure namespaces get `istio.io/dataplane-mode: ambient` **after** Istio + IstioCNI + ZTunnel (wave 2 in `servicemeshoperator3`, not wave 1 `namespaces`).
2. Restart affected Deployments after mesh is Ready.
3. `reconcileIptablesOnStartup: true` on IstioCNI helps new nodes but does not retrofix running pods.

```yaml
# components/servicemeshoperator3 — ambient labels (wave 2)
metadata:
  labels:
    istio.io/dataplane-mode: ambient
  annotations:
    argocd.argoproj.io/sync-wave: "2"
```

---

## ApplicationSet: both `name` and `server` defined

**Symptom:**

```text
application destination spec is invalid: application destination can't
have both name and server defined: west https://kubernetes.default.svc
```

**Cause:** Older ApplicationSet template set `server`; Server-Side Apply does not remove fields the new manifest omits.

**Fix:**

```yaml
# components/acm-hub-spoke/templates/applicationset.yaml
destination:
  name: '{{name}}'
  namespace: openshift-gitops
  server: ""   # explicit blank clears stale SSA
```

Then delete and let Argo CD recreate the ApplicationSet, or patch live spec to remove `server`.

---

## Kiali multi-cluster Unauthorized

**Symptom:** Hub Kiali logs: `Error fetching Namespaces for cluster [east]: Unauthorized`.

**Cause:**

1. Expired token in spoke `kiali-hub-export` ConfigMap.
2. Legacy **`kiali-multi-cluster-secret`** still labeled `kiali.io/multiCluster=true` alongside **`kiali-remote-*`** secrets.

**Fix:**

```bash
# Hub
oc delete secret kiali-multi-cluster-secret -n openshift-cluster-observability-operator --ignore-not-found
oc create job kiali-token-refresh --from=cronjob/kiali-multicluster-token-sync \
  -n openshift-cluster-observability-operator
oc delete pod -n openshift-cluster-observability-operator -l app=kiali
```

On spokes, confirm export ConfigMap exists:

```bash
oc get cm kiali-hub-export -n openshift-cluster-observability-operator -o jsonpath='{.data.updatedAt}'
```

---

## Kafka Console 404 on `/api/*`

**Symptom:** Browser or `curl` to `https://kafka-console.<hub-domain>/api/kafkas` returns Next.js HTML 404; in-pod `console-api` returns 200.

**Cause:** Operator Service targets UI port 3000 only; external route does not split `/api` to port 8080.

**Fix:** Deploy supplemental Route (GitOps: `components/kafka-console/templates/api-route.yaml`):

```yaml
spec:
  host: kafka-console.apps.hub.example.com
  path: /api
  to:
    kind: Service
    name: kafka-console-api-service
  port:
    targetPort: http   # 8080 on console-api container
```

Do **not** set `haproxy.router.openshift.io/rewrite-target` — the API expects the `/api` prefix.

### Blank UI / NextAuth 404 on `/api/auth/*`

**Symptom:** Kafka Console page loads partially or stays blank; browser network tab shows **404** on `/api/auth/providers`; `console-api` logs show `GET /api/auth/providers ... 404`.

**Cause:** The supplemental `/api` Route sends **all** `/api/*` traffic to Quarkus. NextAuth runs in the **UI** container (Next.js) on port **3000**, not in `console-api`.

**Fix:** Add a more specific Route **`/api/auth`** → `kafka-console-console-service` with `port.targetPort: **3000**` (not `80` — the Service’s EndpointSlice exposes pod port 3000). GitOps: `components/kafka-console/templates/api-route.yaml` (`kafka-console-ui-auth`).

```bash
curl -sk -o /dev/null -w '%{http_code}\n' \
  https://kafka-console.<hub-domain>/api/auth/providers
# Expect 200
```

### JSON `404` / code `4041` on cluster detail

**Symptom:** UI shows `{"errors":[{"title":"Resource not found","status":"404","code":"4041"}]}` when opening a Kafka cluster.

**Cause:** Valid API route, but the cluster id is unknown **or** the console-api cannot reach brokers (often west spoke offline → Skupper listener has no connector).

**Checks:**

```bash
# List works?
curl -sk https://kafka-console.<hub-domain>/api/kafkas

# Detail per cluster (replace id from list response)
curl -sk -o /dev/null -w '%{http_code}\n' https://kafka-console.<hub-domain>/api/kafkas/<id>

# West spoke up?
oc config use-context west
oc get applications spoke-interconnect-west -n openshift-gitops
oc get link -n service-interconnect
```

**Fix:** Restore west (or east) spoke apps and Skupper link; resync `field-content-kafka-console` for broker DNS EndpointSlices.

---

## industrial-edge-tst Degraded (Camel / KServe)

**Symptom:** Argo CD app `industrial-edge-tst-east` (or `-west`) is **Degraded** with:

- `Integration/mqtt-to-kafka`: `dependency camel:mqtt not found in Camel catalog`
- `InferenceService/anomaly-detection`: stuck **Progressing**; sync waits for healthy state

**Causes:**

1. **Camel K:** Routes use `paho:` URIs; the catalog dependency is **`camel:paho`**, not `camel:mqtt`.
2. **KServe:** Chart ships `InferenceService` only when `anomalyDetection.enabled: true`. Default is **`false`** because spokes need ODH **RawDeployment** (no Serverless Operator), a MinIO model at `s3://models/anomaly-detection/model`, and a Ready `DataScienceCluster`. Threshold alerts still work via `ie-anomaly-alerter` without KServe.

**Fix (GitOps):**

```yaml
# components/industrial-edge-tst/templates/camel-integrations.yaml
dependencies:
  - camel:paho
  - camel:kafka

# components/industrial-edge-data-science-cluster — edge RawDeployment
kserve:
  defaultDeploymentMode: RawDeployment
  serving:
    managementState: Removed
modelmeshserving:
  managementState: Removed
```

**Verify Camel integration:**

```bash
oc get integration mqtt-to-kafka -n industrial-edge-tst-all \
  -o jsonpath='{range .status.conditions[?(@.type=="Ready")]}{.status} {.message}{"\n"}{end}'
```

**Enable ML inference later:** upload model to MinIO, set `anomalyDetection.enabled: true` in spoke app values, sync `industrial-edge-data-science-cluster` then `industrial-edge-tst`.

**Camel K `401 Unauthorized` / `ImagePullBackOff` on internal registry:** The PostSync Job `camel-k-registry-bootstrap` creates `camel-k-registry-docker` from the `builder` SA token and patches `IntegrationPlatform` + `pull-secret` trait. If the integration kit is stuck in Error, delete the Integration and IntegrationKit, then re-sync the app.

---

## spoke-gateway Degraded (`modelmesh-serving` not found)

**Symptom:** Argo CD app `spoke-gateway-east` (on the **east** cluster) shows HTTPRoute `ie-anomaly-detection` Degraded.

**Cause:** Optional KServe/ModelMesh route points at a backend that is not Ready yet (or ML stack not installed).

**Fix (GitOps):** `components/spoke-gateway/values.yaml` sets `inferenceRoute.enabled: false` by default. Enable only after `InferenceService` is Ready and set backend namespace to `redhat-ods-applications` when using cluster-scoped ModelMesh.

---

## Argo CD: where applications live

| Cluster | Namespace | Examples |
| ------- | --------- | -------- |
| Hub | `openshift-gitops` | `field-content-*`, `east-spoke-components`, `west-spoke-components` |
| East spoke | `openshift-gitops` | `operators-east`, `spoke-gateway-east`, `spoke-interconnect-east` |
| West spoke | `openshift-gitops` | `operators-west`, `spoke-gateway-west`, `spoke-interconnect-west` |

Parent apps use `destination.server` = cluster-proxy URL. Child apps on spokes use `https://kubernetes.default.svc`.

---


**Symptom:** `entity-operator` CrashLoopBackOff after enabling ambient on Kafka namespaces.

**Cause:** Double encryption or ztunnel intercept on internal replication port 9091.

**Fix:** Keep Kafka control-plane namespaces off ambient where documented, or follow Strimzi + OSSM ambient guidance for your version.

---

## Related docs

- [Service Mesh sync waves](products/service-mesh.md#sync-wave-ordering-ambient)
- [Architecture sync-wave table](architecture.md#spoke-sync-wave-reference)
- [Getting Started](getting-started.md)
