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
    → http:backstage:request → Gitea webhook (optional, continueOnError)
    → http:backstage:request → /api/notifications (in-app + Mailpit email when enabled)
  → ArgoCD (hub) deploys to spoke (east/west)
  → Entity pages: Topology, Kubernetes, Tekton CI, ArgoCD CD, Quay, OCM cluster card, Kuadrant API Products
```

Reference patterns:
- [test-drive-pe-oscg](https://github.com/maximilianoPizarro/test-drive-pe-oscg) (Neuralbank scaffolding flow)
- [from-3scale-to-connectivity-link](https://github.com/maximilianoPizarro/from-3scale-to-connectivity-link) (Kuadrant, ArgoCD CD tab, Mailpit email, `publish:gitea`)
- [field-sourced-content-template](https://github.com/maximilianoPizarro/field-sourced-content-template) (RHDP field-content, template catalog import, Gitea webhooks)

## Workshop users (`userCount`)

- Root [`values.yaml`](../../values.yaml): `userCount: 50` (up to 200) drives Gitea, Keycloak, and [`components/platform-users`](../../components/platform-users/) htpasswd.
- **DevSpaces is spoke-only** — `components/devspaces` in `east/values.yaml` and `west/values.yaml`, **not** hub root `values.yaml`.
- **DevSpaces operators on each spoke** (see [test-drive-pe-oscg](https://github.com/maximilianoPizarro/test-drive-pe-oscg)): `devspaces` + `kubernetes-imagepuller-operator` (for `CheCluster.components.imagePuller`); `devworkspace-operator` is bundled in Dev Spaces 3.x (no separate sub).
- DevSpaces auth: **OpenShift htpasswd on each spoke** (`platform-users` chart — `userN`, `admin`, `platformadmin` / `Welcome123!`). **Not** Keycloak OIDC. Developer Hub stays Keycloak on the hub only.
- Developer Hub login: Keycloak OIDC — `user1`…`userN` / `Welcome123!` (same as Gitea; not synced to spoke htpasswd).
- Spoke DevSpaces: cluster htpasswd on east/west (`platform-users` chart); template link uses `spokeAppsDomain`.
- Continue AI on spokes: PostSync `devspaces-continue-ai-sync` copies `kairos-system/kairos-ai-credentials` → Secret `continue-ai-config` in `{user}-devspaces` (devfile controller labels).
- Quay pushes: org `workshop`, secret `quay-workshop-push`; see [`docs/assets/backstage/onboarding/`](../../docs/assets/backstage/onboarding/).

## Hybrid Mesh AI Workshop (Showroom userN)

- **Registration:** `components/workshop-registration/` → `https://workshop-registration.<hub-domain>` assigns `userN`, redirects to Showroom with `USER_NAME`, `EAST_DOMAIN`, `WEST_DOMAIN`.
- **Showroom:** `components/showroom/` + Antora repo `showroom-hybrid-mesh-ai/` (content generated via `scripts/generate-workshop-content.py`).
- **Plan B shared demos:** `components/workshop-demos/` ConfigMap `developer-hub-catalog-demos` → System `hybrid-mesh-shared-demos` (browse without scaffolding).
- **NeuroFace:** `components/neuroface/` — shared AI demo; **no LibreChat**.
- **Progress API:** `POST /api/progress` on registration service; Showroom `progress-tracker.js` posts module completion.
- **GitHub Pages mirror:** `docs/workshop/` — static read-only; hands-on uses in-cluster Showroom terminal `oc`.

## Authentication (Keycloak OIDC, not GitHub)

- **`signInPage: oidc`** with Keycloak realm `backstage` at `https://sso.<clusterDomain>`
- Auth in **separate** ConfigMap `app-config-auth-rhdh` (prevents YAML merge flattening `signIn.resolvers`)
- Secret `developer-hub-oidc-auth`: `OIDC_CLIENT_SECRET`, `GITEA_TOKEN`, `SESSION_SECRET`
- Resolver: `preferredUsernameMatchingUserEntityName` + `dangerouslyAllowSignInWithoutUserInCatalog: true`

## Catalog mounting (RHDH operator extraFiles)

The operator mounts `extraFiles` as **directories** when `mountPath` includes the filename. Use:

| ConfigMap key | mountPath | catalog `target` |
| ------------- | --------- | ---------------- |
| `users.yaml` | `/opt/app-root/src/catalog-data` | `/opt/app-root/src/catalog-data/users.yaml` |
| `industrial-edge-system.yaml` | `/opt/app-root/src/catalog-data/ie` | `/opt/app-root/src/catalog-data/ie/industrial-edge-system.yaml` |

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
| `backstage-community-plugin-ocm` | enabled | Cluster overview cards, `/ocm` sidebar |
| `backstage-plugin-kubernetes` | enabled | Workloads tab |
| `backstage-community-plugin-topology` | enabled | Topology graph |
| `backstage-community-plugin-tekton` | enabled | CI tab (`entity.page.ci/content`) |
| `backstage-community-plugin-tech-radar` | enabled (`plugins.techRadar.enabled`) | Tech Radar page `/tech-radar` |
| `backstage-plugin-mcp-actions-backend` | enabled (`plugins.mcp.enabled`) | MCP tools (catalog + techdocs) via OCI |
| `roadiehq-scaffolder-backend-module-http-request-dynamic` | enabled | `http:backstage:request` |
| `backstage-plugin-scaffolder-backend-module-github-dynamic` | enabled | `publish:github` → Gitea |
| `backstage-plugin-notifications` + backend | enabled | In-app notifications |
| `backstage-plugin-techdocs` | enabled (`plugins.techdocs.enabled`) | Docs tab (local builder/publisher) |
| `@kuadrant/kuadrant-backstage-plugin-*` | enabled (`plugins.kuadrant.enabled`) | Kuadrant page `/kuadrant` — external npm; needs `ephemeral-storage` 2Gi/5Gi on backend |
| `roadiehq-backstage-plugin-argo-cd-backend` + `redhat-argocd` frontend | enabled (`plugins.argocd.enabled`) | Argo CD entity tab `entity.page.cd/content` |
| `backstage-plugin-notifications-backend-module-email-dynamic` | enabled (`plugins.notificationsEmail.enabled`) | SMTP → `mailpit.mailpit.svc:1025` |
| `backstage-community-plugin-kafka` | **disabled** (`plugins.kafka.enabled: false`) | Not in RHDH 1.9 image; no ghcr.io OCI |
| `backstage-community-plugin-quay` | enabled (`plugins.quay.enabled`) | Quay entity tab; proxy `/quay` → `quay-registry.<domain>` |
| kiali, grafana, tech-insights | disabled | Not in RHDH 1.9 image or ghcr.io overlays |
| `quay-backend-dynamic`, `security-insights` | disabled | ENOENT in RHDH 1.9 image |

**Flag wiring:** `plugins.*.enabled` in `values.yaml` must drive `disabled: {{ not .Values.plugins.*.enabled }}` in `templates/all.yaml` — never hardcode `disabled: true` for argocd/kuadrant/email when values say enabled.

**Dynamic plugins PVC:** default chart size **2Gi** is too small for ArgoCD + Kuadrant + email + MCP OCI. Set `dynamicPluginsStorage: 10Gi` in hub `component-applications.yaml` and patch `dynamic-plugins-root` with `$patch: replace` in `deployment.patch`.

**Kuadrant K8s config:** hub cluster in `clusterLocatorMethods` needs `serviceAccountToken: ${K8S_SA_TOKEN}` (Kuadrant catalog provider requires token on clusters[0]). **ClusterRole `backstage-kubernetes-plugin`** must include `devportal.kuadrant.io` resources (`apiproducts`, `apikeys`) — CRD group is **not** `kuadrant.io`. API Product scaffold template uses `apiVersion: devportal.kuadrant.io/v1`.

**PostSync:** `developer-hub-plugin-readiness` Job (wave 10) checks `/healthcheck`, RBAC CSV mount, and basic plugin readiness.

**YAML trap:** `catalog.providers` (ocm, keycloakOrg) must be indented under `catalog:`, not under `quay:`.

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
          serviceAccountToken: ${K8S_SA_TOKEN}
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

## Public API catalog (Try It Out)

Bundled at `files/catalog/public-apis.yaml` → ConfigMap `developer-hub-catalog-public-apis` → `/opt/app-root/src/catalog-data/public-apis/public-apis.yaml`.

Includes Petstore, httpbin, REST Countries, JSONPlaceholder, Cat Facts. External specs use `$text:`; inline specs must include `servers:` for Swagger UI Try It Out (otherwise requests go to Developer Hub host).

Add hosts to `backend.reading.allow`: `petstore3.swagger.io`, `httpbin.org`, `restcountries.com`, `jsonplaceholder.typicode.com`, `catfact.ninja`.

## Software template scaffolding flow

### Templates shipped

| Template | Purpose |
| -------- | ------- |
| `industrial-edge` | IoT edge instance on east/west (+ Gitea webhook step) |
| `industrial-edge-camel-kaoto` | Camel routes + DevSpaces/Kaoto (+ mkdocs for TechDocs) |
| `camel-kaoto-cdc` | Standalone CDC route; DevSpaces on target spoke |
| `industrial-edge-api-product` | Kuadrant APIProduct (`devportal.kuadrant.io/v1`) + OpenAPI catalog entity |
| `industrial-edge-delete` | Delete ArgoCD app + Gitea repo + notify |

Template `owner` parameter: use `ui:field: OwnerPicker` (not `${{ user.entity.metadata.name }}` default — breaks form when user entity missing). Catalog locations: GitHub blob (scaffolder skeleton) + raw GitHub fallback for template ingestion.

### Skeleton catalog-info.yaml annotations

```yaml
annotations:
  backstage.io/kubernetes-id: ${{ values.uniqueName }}
  backstage.io/kubernetes-namespace: ${{ values.namespace }}
  backstage.io/kubernetes-cluster: ${{ values.targetCluster }}
  janus-idp.io/tekton: ${{ values.namespace }}
  backstage.io/source-location: url:https://gitea-gitea.${{ values.clusterDomain }}/ws-${{ values.owner }}/...
  quay.io/repository-slug: workshop/${{ values.uniqueName }}
  kuadrant.io/api-product: ${{ values.uniqueName }}
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
  default: apps.cluster.example.com   # RHDP injects real hub domain at provision time
spokeAppsDomain:
  default: apps.cluster-east.example.com   # or west — per targetCluster oneOf
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

Requires notifications plugins enabled. With `plugins.notificationsEmail.enabled: true`, the email processor sends via Mailpit SMTP (`mailpit.mailpit.svc:1025`). In-app notifications always work via `/api/notifications`.

## Permission framework (workshop default: RBAC on)

`plugins.rbac.enabled: true` in `values.yaml` sets `permission.enabled: true` and mounts **`files/lightspeed/rbac-policy.csv`** via `templates/rbac-policy.yaml`. The CSV is **decoupled from Lightspeed** — do not gate the ConfigMap on `lightspeedEnabled`.

**Install-time requirement (post-restart lesson):** `Backstage` CR `extraFiles` alone does **not** reliably mount `rbac-policy.csv` on `backstage-backend`. Also add an explicit **volume + volumeMount** in `templates/all.yaml` `deployment.patch` when `plugins.rbac.enabled` (ConfigMap `rhdh-rbac-policy`, `subPath: rbac-policy.csv`). Without it, readiness stays **503** with `ENOENT ... rbac-policy.csv` and the permission plugin never starts.

Grant `role:default/authenticated` at minimum:

| Area | Permission names |
| ---- | ------------------ |
| Catalog / scaffolder | `catalog-entity`, `catalog.location`, `scaffolder-*` |
| Kubernetes / Topology | `kubernetes.clusters.read`, `kubernetes.resources.read`, `kubernetes.proxy` |
| OCM | `ocm.entity.read`, `ocm.cluster.read` — required for `/ocm` and **Clusters** menu |
| Argo CD | `argocd.view.read` |
| Adoption Insights | `adoption-insights.events.read`, `adoption-insights.nav.read`, `adoption-insights.entity.read` |
| TechDocs | `techdocs.entity.read` |
| Kuadrant | `kuadrant.apiproduct.list`, `kuadrant.apiproduct.read.all`, `kuadrant.apikey.*`, `kuadrant.planpolicy.*` — **not** `kuadrant.api-product.read` |
| Notifications | `notification.entity.read` |
| Lightspeed | `lightspeed.chat.*` |

`pluginsWithPermission` in app-config must list: `catalog`, `scaffolder`, `permission`, `kubernetes`, `ocm`, `techdocs`, `argocd`, `kuadrant`, `notifications`, `adoption-insights`, and `lightspeed` when enabled.

**Group bindings** in `rbac-policy.csv`:
- `g, group:default/developers, role:default/authenticated` — **workshop userN** (`catalog-users.yaml` + Keycloak group `developers`)
- `g, group:default/backstage-users, role:default/authenticated` (optional alias if Keycloak sync adds it)
- `g, user:default/platformadmin, role:default/authenticated` (explicit OIDC admin)
- `g, user:default/platformadmin, role:default/admin`

**Trap:** binding only `backstage-users` leaves **userN without any role** — Clusters, public APIs, Adoption, Kuadrant all denied. Do **not** use `g, role:default/admin, role:default/authenticated` (rbac-backend rejects role inheritance).

`platformadmin` gets full Kuadrant + policy admin via `role:default/admin`.

For labs only, set `plugins.rbac.enabled: false` to restore deny-by-default off (empty catalog risk remains if partial CSV).

## Lightspeed (MaaS OpenAI-compatible)

- Enable: `plugins.lightspeed.enabled: true` in hub `component-applications.yaml`, OCI tag `bs_1.45.3__1.2.3`
- Sidecars: `llama-stack`, `lightspeed-core`, optional `rag-content`
- **Default model (workshop userN):** `llama-scout-17b` via `litemaas.apiUrl` → `https://maas-rhdp.apps.maas.redhatworkshops.io/v1`
- **API keys never in Git** — RHDP injects `litemaas.apiKey` and/or `kairos-system/kairos-ai-credentials`; PostSync `developer-hub-lightspeed-ai-sync` copies key into `llama-stack-secrets`
- Other MaaS models: `deepseek-r1-distill-qwen-14b` (admin/reasoning), `codellama-7b-instruct` (code/templates)
- Routes: `/lightspeed` page + FAB; secrets `lightspeed-secrets`, ConfigMaps `lightspeed-stack`, `lightspeed-app-config`

**Lightspeed kairos Role trap:** In `templates/lightspeed.yaml`, `Role` `developer-hub-lightspeed-ai-sync-kairos-read` must use `resourceNames: ["{{ $credName }}"]` where `$credName` defaults to `kairos-ai-credentials`. Using `$ai.credentialsSecretName` directly renders **empty** `resourceNames: [""]` when `aiModel` is unset → Job gets `Forbidden` on `kairos-system/kairos-ai-credentials` and **blocks** `field-content-developer-hub` sync on the PostSync hook.

## TechDocs (in-pod, not GitHub Pages)

- `plugins.techdocs.enabled: true` with **`techdocs.builder: local`** in app-config (builds from Gitea repo on Docs tab view)
- Scaffold skeletons: `mkdocs.yml`, `docs/index.md`, `backstage.io/techdocs-ref: dir:.` in `catalog-info.yaml`
- `templates/catalog-onboarding.yaml` + `files/onboarding/` (mkdocs, `techdocs-ref: dir:.`)
- Do **not** rely on `FetchUrlReader` to github.io for workshop onboarding — that caused `readTree` errors

## OCM plugin routes

Dynamic plugin config registers **`/ocm`** and sidebar **Clusters** (`OcmPage`). Alias route **`/clusters`** → same `OcmPage` (bookmarks/old links). Backend needs `catalog.providers.ocm` under `catalog:` (YAML indent trap) and ClusterRole `backstage-ocm-plugin` for `ManagedCluster`.

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
| TechDocs `FetchUrlReader does not implement readTree` | Use in-pod mkdocs (`catalog-onboarding.yaml`, `dir:.`) not remote github.io tree |
| `/ocm` or `/clusters` 404 | OCM dynamic plugin failed to load (check `install-dynamic-plugins` logs); or navigate to `/ocm` not a stale `/clusters` bookmark before alias was added |
| `/ocm` permission denied | RBAC on without `ocm.*` in CSV; sync `rhdh-rbac-policy`; verify `group:default/developers` binding for userN |
| Adoption Insights empty for userN | Add `adoption-insights` to `pluginsWithPermission`; CSV `adoption-insights.nav.read` + `developers` group |
| `install-dynamic-plugins` ENOSPC | Increase `dynamicPluginsStorage` to 10Gi; patch `dynamic-plugins-root` volume |
| Kuadrant backend startup fail | Add `serviceAccountToken: ${K8S_SA_TOKEN}` on hub cluster in kubernetes config |
| Docs tab empty (`workshop-onboarding`) | Missing `backstage.io/techdocs-ref: dir:.` on in-pod `files/onboarding/catalog-info.yaml` |
| Topology "Missing Permission" | User not in `authenticated` role; verify Keycloak username matches CSV; ensure `kubernetes.clusters.read` in CSV |
| Kuadrant permission denied | Use `kuadrant.apiproduct.list` not `kuadrant.api-product.read`; add `kuadrant` to `pluginsWithPermission` |
| Empty scaffolder form / Review only | Stale catalog entity or `${{ user.entity... }}` owner default — use OwnerPicker; refresh catalog |
| Lightspeed works but catalog empty | CSV only had `lightspeed.*`; expand full workshop CSV |
| Scaffolder 503 on industrial-edge URL | Spoke gateway / mesh — see mesh exclusions above |
| `publish:github` fails: `user redirect does not exist [name: ws-<owner>]` | Ensure Gitea bootstrap created org/user; hook job must be recreatable (`BeforeHookCreation,HookSucceeded,HookFailed`) |
| Readiness **503**, `ENOENT rbac-policy.csv` | Add deployment.patch volumeMount (not only `extraFiles`); sync `field-content-developer-hub`; delete backstage pod |
| Argo stuck on `developer-hub-lightspeed-ai-sync` | Fix kairos Role `resourceNames`; delete Job; clear `/operation`; resync with `SkipHooks=true` if hook already ran |
| Keycloak catalog `HTTP 403` after restart | Keycloak still starting — non-fatal; catalog users.yaml still works |

## Cold start / post-restart (hub DevHub)

After hub reboot or first install, verify in order:

1. `field-content-developer-hub` — not blocked on PostSync hook; `rhdh-rbac-policy` ConfigMap exists.
2. `backstage-developer-hub` deployment has volume `rhdh-rbac-policy` on `backstage-backend`.
3. Readiness: `curl -sk -o /dev/null -w '%{http_code}' https://developer-hub.<hub-apps>/.backstage/health/v1/readiness` → **200**.
4. `developer-hub-spoke-tokens` Secret populated (CronJob or PostSync hook).
5. PostSync `developer-hub-plugin-readiness` Job completed.

Recovery when sync is wedged:

```bash
oc patch application field-content-developer-hub -n openshift-gitops --type json \
  -p '[{"op":"remove","path":"/operation"}]'
oc delete job developer-hub-lightspeed-ai-sync -n developer-hub --ignore-not-found
# sync with SkipHooks if PostSync already succeeded once
```

## Files map

| File | Purpose |
| ---- | ------- |
| `components/developer-hub/templates/all.yaml` | Namespace, RBAC, app-config, plugins, Backstage CR, **deployment.patch** (RBAC CSV mount) |
| `components/developer-hub/templates/lightspeed.yaml` | LCS sidecars config, PostSync kairos API key Job, kairos-system Role |
| `components/developer-hub/templates/rbac-policy.yaml` | ConfigMap `rhdh-rbac-policy` |
| `managed-service-accounts.yaml` | MSA + ClusterPermission east/west |
| `spoke-token-sync.yaml` | CronJob → developer-hub-spoke-tokens |
| `plugin-readiness.yaml` | PostSync health + RBAC CSV check |
| `hub-sa-token-secret.yaml` | K8S_SA_TOKEN for scaffolder |
| `quay-push-secret.yaml` | Optional Quay dockerconfig |
| `files/catalog/industrial-edge-system.yaml` | Static IE system catalog |
| `docs/assets/backstage/software-templates/` | Templates for GitHub Pages |

## Tag / release

Platform snapshot tags: **`ocp-420-v4`** (Camel Dashboard spokes), **`ocp-420-v5`** (RHDP hub-spoke, RHDH plugins 10Gi PVC, userN RBAC `developers` group, MaaS Lightspeed, Quay/Mailpit/Skupper/ACS). Pin Argo `targetRevision` to the tag for reproducible workshops.
