---
layout: default
title: Getting Started
nav_order: 3
---

# Getting Started (ACM-first)

This guide bootstraps the **hub** with one Helm install, registers **east** and **west** in ACM, and lets the **ApplicationSet** deploy spoke charts automatically. You do **not** run `helm install` on spokes.

## You'll have when finished

- [ ] **ACM** — `east` and `west` `ManagedCluster` Ready
- [ ] **Argo CD** — `east-spoke-components` / `west-spoke-components` from ApplicationSet
- [ ] **Industrial Edge** — sensors, MQTT, Kafka, line-dashboard on each spoke
- [ ] **Skupper** — hub `sitesInNetwork: 3`; listeners Ready in `service-interconnect`
- [ ] **Grafana / Kiali / Kafka Console** — hub fleet views
- [ ] **Developer Hub** — catalog + software templates

**Next:** [Scaffolding](scaffolding.md) for a new edge instance on east or west.

## Prerequisites

- OpenShift **4.14+** on hub + two spokes
- **Helm 3** and **`oc`** (cluster-admin on hub for ACM import)
- Fork of this repository; update `gitops.repoUrl` in `values.yaml`, `east/values.yaml`, `west/values.yaml`

## Repository layout

```
.              → hub (helm install here only)
east/          → east spoke chart (ApplicationSet path: east)
west/          → west spoke chart (ApplicationSet path: west)
components/    → shared component charts
```

---

## Phase 1: Prepare

1. Fork [`platform-hub-spoke-config`](https://github.com/maximilianoPizarro/platform-hub-spoke-config).
2. Set cluster domains in **`values.yaml`** (hub) and spoke **`deployer.domain`** / **`clusters.hub.domain`** in `east/values.yaml`, `west/values.yaml`.
3. Validate rendering:

```bash
helm template test-hub . -f values.yaml --set deployer.domain=apps.hub.example.com
helm template test-east east/
helm template test-west west/
```

---

## Phase 2: Bootstrap hub (one Helm install)

```bash
helm install platform-hub-spoke . \
  -f values.yaml \
  --set deployer.domain=apps.hub.example.com
```

This creates the root Argo CD Application, which syncs all hub `components/*` (ACM, GitOps, mesh, Kafka Console, Developer Hub, etc.).

Alternatively, create an Argo CD `Application` pointing at `.` on your fork with the same values.

---

## Phase 3: Register spokes (ACM + tokens)

1. Import **east** and **west** in ACM (UI or `ManagedCluster` + `auto-import-secret`).
2. Label clusters for placement:

```yaml
metadata:
  labels:
    cluster.open-cluster-management.io/clusterset: global
    region: east   # or west
```

3. Inject spoke API tokens on the hub (never commit):

```bash
helm upgrade platform-hub-spoke . \
  --set clusters.east.token=sha256~... \
  --set clusters.west.token=sha256~... \
  --reuse-values
```

4. **ApplicationSet** `industrial-edge-spoke` generates **`east-spoke-components`** and **`west-spoke-components`**. Each spoke's Argo CD syncs child Applications from `east/` or `west/` — **no Helm install on spokes**.

```bash
oc get applications -n openshift-gitops | grep spoke
```

---

## Phase 4: Verify fleet

| Check | Command / UI |
| ----- | -------------- |
| ACM clusters | Console → **Infrastructure → Clusters** |
| Spoke app tree | ACM **Applications** or hub Argo CD |
| Skupper | `oc get listeners,connectors -n service-interconnect` (hub: `sitesInNetwork: 3`) |
| Industrial Edge | Route `industrial-edge.apps.<spoke-domain>` |
| Sync order | Spoke apps: wave 1 namespaces → 2 operators → 3 mesh → 5 edge → 6 interconnect |

---

## Phase 5: Enable features

### Kiali multi-cluster (hub)

Default: `multiCluster.automateTokens: true` + spoke `exportTokenForHub: true`.

- Spoke PostSync writes **`kiali-hub-export`** ConfigMap.
- Hub CronJob writes **`kiali-remote-east`** / **`kiali-remote-west`**.
- If remote clusters show **Unauthorized**, delete legacy **`kiali-multi-cluster-secret`** and re-run token sync — see [Troubleshooting](troubleshooting.md).

### Kafka Console (hub)

Central UI for all Kafka clusters via Skupper bootstrap services. If `/api/kafkas` returns 404 on the external route, ensure **`apiRoute.enabled: true`** in `components/kafka-console` (supplemental `/api` Route to the API container).

### Developer Hub OIDC

Keycloak realm `backstage` on `sso.<hub-domain>`. Set `keycloakOidcClientSecret` via `helm upgrade` (do not commit). See existing Keycloak steps in [Developer Hub](products/developer-hub.md).

### Continue AI (DevSpaces)

Create `continue-ai-config` Secret with MaaS API key after deploy (not in Git).

---

## Phase 6: Day-two

- [Troubleshooting](troubleshooting.md) — ApplicationSet SSA, HBONE, Kiali tokens, Kafka Console API route
- [Architecture](architecture.md) — sync-wave reference
- [Deploy with ACM and GitOps](deploy-acm-gitops.md) — placement and GitOpsCluster detail
- **New spoke:** add `ManagedCluster`, label, copy `east/` pattern, extend ApplicationSet placement, `helm upgrade` token

---

## Quick reference: legacy nine-step map

| Old step | ACM-first phase |
| -------- | ----------------- |
| 1 Fork | Phase 1 |
| 2 Domains | Phase 1 |
| 3 Helm hub | Phase 2 |
| 4 ACM import | Phase 3 |
| 5 Argo cluster secrets | Phase 3 (tokens via `helm upgrade`) |
| 6 ApplicationSet | Phase 3–4 |
| 7 Kiali | Phase 5 |
| 8 Developer Hub | Phase 5 |
| 9 Continue AI | Phase 5 |

---

**Next →** [Scaffolding](scaffolding.md) · [Architecture](architecture.md) · [Troubleshooting](troubleshooting.md)
