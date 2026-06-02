---
name: developer-hub-scaffolder
description: Red Hat Developer Hub (RHDH) scaffolder, multi-cluster Kubernetes/Topology, OCM, notifications, Gitea, Quay, and GitHub Pages templates for platform-hub-spoke-config.
---

# Developer Hub & Scaffolder Skill

Apply when editing **`components/developer-hub/`**, Backstage catalog entities, or **`docs/assets/backstage/software-templates/`**.

## Architecture (single pane of glass)

```
User → Developer Hub (hub)
  → Software Template (GitHub Pages static assets)
    → fetch:template → publish:github (Gitea) → catalog:register
    → http:backstage:request → ArgoCD Application (k8s-api proxy)
    → http:backstage:request → /api/notifications
  → ArgoCD (hub) deploys to spoke (east/west)
  → Entity pages: Topology, Kubernetes, Tekton CI, OCM cluster card
```

Reference pattern: [test-drive-pe-oscg](https://github.com/maximilianoPizarro/test-drive-pe-oscg) (Neuralbank scaffolding flow).

## Workshop users (`userCount`)

- Root [`values.yaml`](../../values.yaml): `userCount: 50` (up to 200) drives Gitea, DevSpaces, Keycloak, and [`components/platform-users`](../../components/platform-users/) htpasswd.
- Developer Hub login: Keycloak OIDC — `user1`…`userN` / `Welcome123!` (same as Gitea; not synced to spoke htpasswd).
- Spoke DevSpaces: cluster htpasswd on east/west (`platform-users` chart); template link uses `spokeAppsDomain`.
- Quay pushes: org `workshop`, secret `quay-workshop-push`; see [`docs/assets/backstage/onboarding/`](../../docs/assets/backstage/onboarding/).

## Authentication (Keycloak OIDC, not GitHub)

- **`signInPage: oidc`** with Keycloak realm `backstage` at `https://sso.<clusterDomain>`
- Auth in **separate** ConfigMap `app-config-auth-rhdh` (prevents YAML merge flattening `signIn.resolvers`)
- Secret `developer-hub-oidc-auth`: `OIDC_CLIENT_SECRET`, `GITEA_TOKEN`, `SESSION_SECRET`
- Resolver: `preferredUsernameMatchingUserEntityName` + `dangerouslyAllowSignInWithoutUserInCatalog: true`

## Catalog mounting (RHDH operator extraFiles)

The operator mounts `extraFiles` as **directories** when `mountPath` includes the filename. Use:

| ConfigMap key | mountPath | catalog `target` |
| ------------- | --------- | ---------------- |
| `users.yaml` | `/opt/app-root/src` | `/opt/app-root/src/users.yaml` |
| `industrial-edge-system.yaml` | `/opt/app-root/src/catalog-ie` | `/opt/app-root/src/catalog-ie/industrial-edge-system.yaml` |

**Wrong:** `mountPath: /opt/app-root/src/catalog-users.yaml` → `EISDIR` error.

## Software templates via GitHub (catalog + raw fetch)

Templates still live under `docs/assets/backstage/software-templates/`, but the catalog location must use a GitHub `blob` URL so relative `./skeleton` paths resolve reliably in scaffolder runs:

```yaml
catalog:
  locations:
    - type: url
      target: https://github.com/maximilianopizarro/platform-hub-spoke-config/blob/main/docs/assets/backstage/software-templates/templates-catalog.yaml
```

**Scaffolder integrations** should include:

```yaml
integrations:
  github:
    - host: github.com                       # fetch:template / catalog URLs
      apiBaseUrl: https://api.github.com
      rawBaseUrl: https://raw.githubusercontent.com
    - host: gitea-gitea.<clusterDomain>      # publish:github -> Gitea
      apiBaseUrl: https://gitea-gitea.<domain>/api/v1
      rawBaseUrl: https://gitea-gitea.<domain>/raw
      token: ${GITEA_TOKEN}
```

Do **not** force a separate `raw.githubusercontent.com` integration host unless strictly required; incorrect host routing can cause scaffolder URL reader mismatches.

**Reading allowlist:**

```yaml
backend:
  reading:
    allow:
      - host: "*.github.io"
      - host: github.com
      - host: raw.githubusercontent.com
```

## Proxy endpoints (scaffolder http:backstage:request)

| Path | Target | Auth | Used for |
| ---- | ------ | ---- | -------- |
| `/api/proxy/gitea/*` | Gitea API v1 | `token ${GITEA_TOKEN}` | Delete repo |
| `/api/proxy/k8s-api/*` | `kubernetes.default.svc` | `Bearer ${K8S_SA_TOKEN}` | Create/delete ArgoCD Application |

`K8S_SA_TOKEN` from Secret `developer-hub-sa-token` (type `kubernetes.io/service-account-token`, annotation `kubernetes.io/service-account.name: developer-hub`).

Hub ClusterRole must include `argoproj.io/applications` verbs: get, list, watch, create, update, patch, delete.

## Dynamic plugins (RHDH 1.9)

| Plugin | Status | Purpose |
| ------ | ------ | ------- |
| `backstage-community-plugin-ocm` | enabled | Cluster overview cards |
| `backstage-plugin-kubernetes` | enabled | Workloads tab |
| `backstage-community-plugin-topology` | enabled | Topology graph |
| `backstage-community-plugin-tekton` | enabled | CI tab (`entity.page.ci/content`) |
| `roadiehq-scaffolder-backend-module-http-request-dynamic` | enabled | `http:backstage:request` |
| `backstage-plugin-scaffolder-backend-module-github-dynamic` | enabled | `publish:github` → Gitea |
| `backstage-plugin-notifications` + backend | enabled | In-app notifications |
| `backstage-plugin-techdocs` | **disabled** | No pre-built docs (FetchUrlReader / empty UI) |
| kafka, argocd, kuadrant plugins | disabled | ENOENT in RHDH 1.9 image |

## Multi-cluster Kubernetes / Topology (CRITICAL)

### Problem

Default config only registers **hub**. Spoke deployments (east/west) are invisible in Topology/Kubernetes tabs.

### Solution

1. **`ManagedServiceAccount`** + **`ClusterPermission`** per spoke (`components/developer-hub/templates/managed-service-accounts.yaml`)
2. **Token sync Job/CronJob** → Secret `developer-hub-spoke-tokens` with `EAST_API_URL`, `EAST_SA_TOKEN`, `WEST_*` (`spoke-token-sync.yaml`)
3. **Kubernetes plugin config** — three clusters in `clusterLocatorMethods`:

```yaml
kubernetes:
  clusterLocatorMethods:
    - type: config
      clusters:
        - name: hub
          url: https://kubernetes.default.svc.cluster.local:443
          authProvider: serviceAccount
          skipTLSVerify: true
        - name: east
          url: ${EAST_API_URL}
          serviceAccountToken: ${EAST_SA_TOKEN}
          skipTLSVerify: true
        - name: west
          url: ${WEST_API_URL}
          serviceAccountToken: ${WEST_SA_TOKEN}
          skipTLSVerify: true
```

4. **Catalog annotation** on every spoke component:

```yaml
annotations:
  backstage.io/kubernetes-id: <selector label value>
  backstage.io/kubernetes-namespace: <namespace on spoke>
  backstage.io/kubernetes-cluster: east   # or west — REQUIRED
```

Without `kubernetes-cluster`, the plugin queries **hub only**.

5. **TLS**: `NODE_TLS_REJECT_UNAUTHORIZED=0` on backend + `skipTLSVerify: true` on clusters (OpenShift self-signed chains).

6. **`automountServiceAccountToken: true`** on Backstage pod + `backstage-kubernetes-plugin` ClusterRole (read pods, deployments, tekton, routes, etc.).

### OCM plugin

`catalog.providers.ocm` reads `ManagedCluster` from hub API. OCM overview cards show fleet health; **workload detail** still needs kubernetes-cluster annotation + spoke tokens.

### Verify multi-cluster

```bash
oc get secret developer-hub-spoke-tokens -n developer-hub -o jsonpath='{.data}' | head
oc get managedserviceaccount -n east
oc get managedserviceaccount -n west
# After RHDH rollout:
# Entity line-dashboard-east → Topology should show deployments in industrial-edge-tst-all on cluster east
```

## Software template scaffolding flow

### Templates shipped

| Template | Purpose |
| -------- | ------- |
| `industrial-edge` | IoT edge instance on east/west |
| `industrial-edge-camel-kaoto` | Camel routes + DevSpaces/Kaoto |
| `industrial-edge-delete` | Delete ArgoCD app + Gitea repo + notify |

### Skeleton catalog-info.yaml annotations

```yaml
annotations:
  backstage.io/kubernetes-id: ${{ values.uniqueName }}
  backstage.io/kubernetes-namespace: ${{ values.namespace }}
  backstage.io/kubernetes-cluster: ${{ values.targetCluster }}
  janus-idp.io/tekton: ${{ values.namespace }}
  backstage.io/source-location: url:https://gitea-gitea.${{ values.clusterDomain }}/ws-${{ values.owner }}/...
  quay.io/repository-slug: maximilianopizarro/${{ values.uniqueName }}
links:
  - title: Source Code (Gitea)
  - title: Documentation  # → Gitea raw README.md
  - title: Open in DevSpaces
```

### Template output links

Always include in `output.links`:

```yaml
- title: Open in DevSpaces
  icon: chat
  url: "https://devspaces.${{ parameters.clusterDomain }}/#https://gitea-gitea.${{ parameters.clusterDomain }}/ws-${{ parameters.owner }}/${{ parameters.name }}-${{ parameters.targetCluster }}"
```

### clusterDomain parameter

Use **hub apps domain** with `apps.` prefix:

```yaml
clusterDomain:
  default: apps.cluster-xqg4c.dynamic2.redhatworkshops.io
```

Repo URL pattern: `gitea-gitea.${{ parameters.clusterDomain }}` (not bare cluster API domain).

### catalog:register path (critical)

When using `repoContentsUrl` from `publish:github`, set:

```yaml
catalogInfoPath: /catalog-info.yaml
```

Do **not** use `/main/catalog-info.yaml`; it can produce `.../main/main/catalog-info.yaml` and fail with catalog HTTP 400.

## Pipelines: internal registry + Quay catalog

| Stage | Registry |
| ----- | -------- |
| **Pipeline push (buildah)** | `image-registry.openshift-image-registry.svc:5000/<namespace>/<app>:latest` |
| **Deployment pull** | Same internal image (no pull secret on OCP) |
| **Catalog / public** | `quay.io/maximilianopizarro/<uniqueName>` via `quay.io/repository-slug` annotation |

Quay credentials **never in Git**. Optional hub Secret:

```bash
JSON=$(./scripts/generate-quay-dockerconfig.sh <user> '<password>')
helm upgrade ... --set quayDockerConfigJson="$JSON"
```

Renders `quay-push-credentials` when `quayDockerConfigJson` is set (`components/developer-hub/templates/quay-push-secret.yaml`).

Tekton: use `tekton.dev/v1` Pipeline with `taskRef.kind: ClusterTask` (git-clone, buildah) — verify cluster has ClusterTasks installed.

## Notifications

```yaml
- id: notify
  action: http:backstage:request
  input:
    method: POST
    path: /api/notifications
    body:
      recipients:
        type: entity
        entityRef: "user:default/${{ parameters.owner }}"
      payload:
        title: "..."
        link: ${{ steps['register'].output.entityRef }}
        severity: normal
```

Requires notifications plugins enabled. No Mailpit/email processor in this platform — in-app only.

## Permission framework

For demos, `permission.enabled: false` in app-config avoids empty catalog for non-admin users. Re-enable for production RBAC.

## Mesh exclusions affecting Developer Hub views

| Namespace | Mesh | Reason |
| --------- | ---- | ------ |
| `industrial-edge-tst-all` | **no ambient** | ztunnel auth failures broke hub→spoke dashboard via gateway; direct TCP works |
| `spoke-gateway-system` | **no ambient** | Same — WebSocket `/api` to line-dashboard |
| `developer-hub` | ambient | OK on hub |
| `gitea` | no mesh | PostgreSQL init breaks under ztunnel |

IoT dashboard fix: remove ambient from `industrial-edge-tst-all` + `spoke-gateway-system`; use cross-namespace HTTPRoute + ReferenceGrant (not ExternalName for Gateway API).

## Hub gateway → spoke routing

- `Service` ports need **`name: http`** (required for Istio/Gateway API)
- HTTPRoute: split `/api` rule for Socket.IO session affinity
- `ReferenceGrant` in target namespace for cross-namespace `backendRefs`

## Common errors

| Error | Fix |
| ----- | --- |
| `InputError: No integration found` for GitHub template URLs | Ensure `integrations.github` has `host: github.com` with `apiBaseUrl` + `rawBaseUrl` |
| `NotFoundError` on `/repos/.../main/docs/.../skeleton` | Use GitHub `blob` catalog URL (not raw URL) for `templates-catalog.yaml` |
| `catalog:register` HTTP 400 with `/main/main/catalog-info.yaml` | Set `catalogInfoPath: /catalog-info.yaml` |
| `EISDIR` on catalog-users.yaml | Fix extraFiles mountPath (directory not file) |
| `NotAllowedError` fetching templates | Add `github.com` and `raw.githubusercontent.com` to `backend.reading.allow` |
| Empty catalog / templates | `permission.enabled: false`; verify catalog locations; rollout RHDH |
| Topology empty on spoke entities | Add `backstage.io/kubernetes-cluster: east\|west`; verify `developer-hub-spoke-tokens` |
| Topology/Kubernetes tabs disappear after plugin edits | Remove custom topology mount override; keep default dynamic plugin wiring |
| `ENOENT` SA token | `automountServiceAccountToken: true` |
| Self-signed cert in K8s plugin | `NODE_TLS_REJECT_UNAUTHORIZED=0` + skipTLSVerify |
| TechDocs `FetchUrlReader does not implement readTree` | Disable techdocs plugins or use local builder with pre-generated docs |
| Scaffolder 503 on industrial-edge URL | Spoke gateway / mesh — see mesh exclusions above |
| `publish:github` fails: `user redirect does not exist [name: ws-<owner>]` | Ensure Gitea bootstrap created org/user; hook job must be recreatable (`BeforeHookCreation,HookSucceeded,HookFailed`) |

## Files map

| File | Purpose |
| ---- | ------- |
| `components/developer-hub/templates/all.yaml` | Namespace, RBAC, app-config, plugins, Backstage CR |
| `managed-service-accounts.yaml` | MSA + ClusterPermission east/west |
| `spoke-token-sync.yaml` | CronJob → developer-hub-spoke-tokens |
| `hub-sa-token-secret.yaml` | K8S_SA_TOKEN for scaffolder |
| `quay-push-secret.yaml` | Optional Quay dockerconfig |
| `files/catalog/industrial-edge-system.yaml` | Static IE system catalog |
| `docs/assets/backstage/software-templates/` | Templates for GitHub Pages |

## Tag / release

Platform snapshot tag: **`ocp-420`** — scaffolder enhancement + multi-cluster topology baseline.
