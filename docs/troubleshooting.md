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

---

## Strimzi entity-operator and ambient mesh

**Symptom:** `entity-operator` CrashLoopBackOff after enabling ambient on Kafka namespaces.

**Cause:** Double encryption or ztunnel intercept on internal replication port 9091.

**Fix:** Keep Kafka control-plane namespaces off ambient where documented, or follow Strimzi + OSSM ambient guidance for your version.

---

## Related docs

- [Service Mesh sync waves](products/service-mesh.md#sync-wave-ordering-ambient)
- [Architecture sync-wave table](architecture.md#spoke-sync-wave-reference)
- [Getting Started](getting-started.md)
