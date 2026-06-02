# Developer Hub: plugins, catalog users, rollout

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish the `backstage-developer-hub` rollout on the hub, surface `user1`…`userN` and `platformadmin` in the catalog, and enable the maximum set of RHDH 1.9 dynamic plugins that actually exist in the image—without breaking `install-dynamic-plugins` init.

**Architecture:** Catalog users are static YAML from Helm (`developer-hub-catalog-users` → `/opt/app-root/src/catalog-data/users.yaml`). Sign-in is Keycloak OIDC (`preferredUsernameMatchingUserEntityName`). Plugins are installed at pod start from `dynamic-plugins-rhdh`; any `disabled: false` entry whose package is missing causes init **CrashLoop** (npm ENOENT). Spoke workload visibility depends on `ManagedServiceAccount` tokens in `developer-hub-spoke-tokens`, not on catalog users.

**Tech Stack:** RHDH operator (`Backstage` CR v1alpha5), Helm `components/developer-hub/`, Argo CD `field-content-developer-hub`, Keycloak realm `backstage`, ACM `ManagedServiceAccount` on east/west.

---

> **Note:** The Cursor command `/write-plan` is deprecated; use the **superpowers writing-plans** skill instead.

## Problem summary (from cluster + Git)

| Symptom | Likely cause |
| -------- | ------------- |
| Only ~2 corrupt `User` entities in UI | Old pod still **Running** with stale mount at `/opt/app-root/src` (pre-`catalog-data` fix) |
| Rollout never completes | New ReplicaSet pod stuck: init `install-dynamic-plugins` failed when `quay-backend-dynamic` / `security-insights` were enabled without packages in image; or readiness **503** during long plugin install |
| `userN` / `platformadmin` “missing” | Catalog file not loaded on **active** backend pod, or catalog filter / refresh not run after rollout |
| “More plugins” | Several entries in `all.yaml` are intentionally `disabled: true` (ENOENT in RHDH 1.9); must discover `dynamic-plugins/dist` before enabling |

Git already contains the mount fix and plugin guards (`832f0a5`+). Remaining work is **cluster apply + verification** and **image-aware plugin toggles**.

## File map

| File | Role |
| ------ | ------ |
| `components/developer-hub/templates/catalog-users.yaml` | Generates `user1`…`user{{ userCount }}`, `platformadmin`, groups |
| `components/developer-hub/templates/all.yaml` | `catalog.locations`, `dynamic-plugins-rhdh`, `Backstage` extraFiles, kubernetes CRs |
| `components/developer-hub/values.yaml` | `userCount`, `plugins.techdocs/quay/acsSecurityInsights/argocd` |
| `components/developer-hub/templates/keycloak-realm.yaml` | OIDC users matching `userN` / `platformadmin` |
| `components/developer-hub/templates/managed-service-accounts.yaml` | Spoke read RBAC for Topology/Kubernetes |
| `components/developer-hub/templates/spoke-token-sync.yaml` | CronJob → `developer-hub-spoke-tokens` |
| `.cursor/skills/developer-hub-scaffolder/SKILL.md` | **Out of date** on catalog mount path and techdocs (update in Task 8) |

---

### Task 1: Hub login and baseline health

**Files:** none (cluster only)

- [ ] **Step 1: Use hub context**

```bash
oc config use-context hub
oc whoami
```

Expected: logged-in user (not `Unauthorized`).

- [ ] **Step 2: Deployment and pods**

```bash
oc get deploy,rs,pods -n developer-hub -l app.kubernetes.io/name=backstage
oc get backstage developer-hub -n developer-hub -o jsonpath='{.status.stage}{"\n"}'
```

Expected: note **two** ReplicaSets if rollout is stuck (old + new).

- [ ] **Step 3: Argo CD app**

```bash
oc get application field-content-developer-hub -n openshift-gitops \
  -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status
```

Expected: may show `OutOfSync` + `Healthy` (secrets ignored)—not blocking if sync revision matches Git.

---

### Task 2: Fix dynamic-plugins ConfigMap (prevent init CrashLoop)

**Files:**
- Verify: `components/developer-hub/templates/all.yaml` (ConfigMap `dynamic-plugins-rhdh`)
- Verify: `components/developer-hub/values.yaml` (`plugins.acsSecurityInsights.enabled: false`)

- [ ] **Step 1: Inspect live ConfigMap**

```bash
oc get cm dynamic-plugins-rhdh -n developer-hub -o yaml | \
  grep -E 'package:|disabled:' | paste - -
```

**Required live state** (must match Git):

```yaml
      - package: ./dynamic-plugins/dist/backstage-community-plugin-quay-backend-dynamic
        disabled: true
      - package: ./dynamic-plugins/dist/backstage-plugin-security-insights
        disabled: true
      - package: ./dynamic-plugins/dist/backstage-community-plugin-kafka
        disabled: true
      - package: ./dynamic-plugins/dist/backstage-community-plugin-kafka-backend-dynamic
        disabled: true
```

- [ ] **Step 2: If mismatch, sync GitOps**

```bash
argocd app sync field-content-developer-hub -n openshift-gitops --grpc-web || \
  oc patch application field-content-developer-hub -n openshift-gitops \
    --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{}}}'
```

- [ ] **Step 3: Confirm init container logs on newest pod**

```bash
POD=$(oc get pods -n developer-hub -l app.kubernetes.io/name=backstage \
  --sort-by=.metadata.creationTimestamp -o name | tail -1)
oc logs -n developer-hub "$POD" -c install-dynamic-plugins --tail=80
```

Expected: no `ENOENT` / `npm pack` errors; ends with successful plugin install.

---

### Task 3: Complete rollout and retire stale pod

**Files:** none (cluster); optional Git if readiness timeout needs annotation (only if Step 4 fails repeatedly)

- [ ] **Step 1: Wait for rollout**

```bash
oc rollout status deployment/backstage-developer-hub -n developer-hub --timeout=20m
```

- [ ] **Step 2: If timeout, diagnose**

```bash
oc describe pod -n developer-hub -l app.kubernetes.io/name=backstage | tail -40
oc get events -n developer-hub --field-selector involvedObject.kind=Pod --sort-by='.lastTimestamp' | tail -20
```

Common fixes:
- Delete pod stuck in `Init:CrashLoopBackOff` **after** Task 2 fixes CM.
- If only old pod is `Ready` and new pod is `Running` but not ready: check `/healthcheck` 503 until plugins finish—wait or increase probe `failureThreshold` only as last resort.

- [ ] **Step 3: Ensure single ready backend**

```bash
oc get pods -n developer-hub -l app.kubernetes.io/name=backstage -o wide
```

Expected: **one** pod `2/2 Running` with annotation `developer-hub.redhat.com/catalog-users: "50"` (or current `userCount`).

- [ ] **Step 4: Scale down old ReplicaSet if needed**

```bash
oc get rs -n developer-hub -l app.kubernetes.io/name=backstage
# If old RS still has desired=1 while new RS not ready, fix plugins first; do not force-delete new pod.
```

---

### Task 4: Verify catalog users file on running pod

**Files:**
- Reference: `components/developer-hub/templates/catalog-users.yaml`
- Reference: `components/developer-hub/templates/all.yaml` (`catalog.locations` → `catalog-data/users.yaml`)

- [ ] **Step 1: Count User entities in mounted file**

```bash
oc exec -n developer-hub deploy/backstage-developer-hub -c backstage-backend -- \
  sh -c 'test -f /opt/app-root/src/catalog-data/users.yaml && grep -c "kind: User" /opt/app-root/src/catalog-data/users.yaml'
```

Expected: **`51`** (= `userCount` 50 + `platformadmin`; plus `maximilianoPizarro` → **52** if that entity is present).

- [ ] **Step 2: Confirm catalog location in app config**

```bash
oc exec -n developer-hub deploy/backstage-developer-hub -c backstage-backend -- \
  sh -c 'grep -A2 "catalog-data/users" /opt/app-root/src/app-config*.yaml 2>/dev/null || \
         grep -r "catalog-data/users" /opt/app-root/src/ 2>/dev/null | head -5'
```

Expected: `target: /opt/app-root/src/catalog-data/users.yaml` with `allow: [User, Group]`.

- [ ] **Step 3: Backend catalog refresh**

```bash
oc exec -n developer-hub deploy/backstage-developer-hub -c backstage-backend -- \
  curl -sS -o /dev/null -w "%{http_code}\n" \
  -X POST http://127.0.0.1:7007/api/catalog/refresh
```

Expected: `202` or `204`.

- [ ] **Step 4: UI verification**

1. Open `https://developer-hub.<clusterDomain>/catalog`
2. Filter: `kind=user`
3. Search `user1`, `user50`, `platformadmin`

**Sign-in test** (not htpasswd): OIDC → `user1` / `Welcome123!` and `platformadmin` / `Welcome123!`.

---

### Task 5: Discover plugins in RHDH image and enable safely

**Files:**
- Modify: `components/developer-hub/templates/all.yaml` (`dynamic-plugins-rhdh` section)
- Modify: `components/developer-hub/values.yaml` (`plugins.*` toggles)

- [ ] **Step 1: List packages in image**

```bash
oc exec -n developer-hub deploy/backstage-developer-hub -c backstage-backend -- \
  ls -1 /opt/app-root/src/dynamic-plugins/dist 2>/dev/null | sort
```

Save output as the allowlist for this cluster image.

- [ ] **Step 2: Enable frontend plugins present in dist**

For each package below, set `disabled: false` **only if** the directory exists in Step 1 output:

| Package dir (under `dist/`) | Helm change |
| --------------------------- | ----------- |
| `backstage-community-plugin-redhat-argocd` | `disabled: {{ not (.Values.plugins.argocd.enabled \| default true) }}` and set community `roadiehq` vs redhat per testing—**do not** enable both if only one exists |
| `backstage-community-plugin-acr` | optional `plugins.acr.enabled` in values |
| `backstage-plugin-techdocs` (+ backend + module) | already tied to `plugins.techdocs.enabled: true` |

Keep **hard-disabled** unless image upgrades:

- `backstage-community-plugin-kafka*`
- `kuadrant-backstage-plugin-*`
- `backstage-community-plugin-quay-backend-dynamic`
- `backstage-plugin-security-insights` (until `plugins.acsSecurityInsights.enabled` and package exists)

Example values addition:

```yaml
# components/developer-hub/values.yaml
plugins:
  techdocs:
    enabled: true
  quay:
    enabled: true
  argocd:
    enabled: true
  acr:
    enabled: false
  acsSecurityInsights:
    enabled: false
```

Example template toggle for Red Hat Argo CD (only if listed in `dist/`):

```yaml
      - package: ./dynamic-plugins/dist/backstage-community-plugin-redhat-argocd
        disabled: {{ not (.Values.plugins.argocd.enabled | default true) }}
```

- [ ] **Step 3: Render Helm locally**

```bash
helm template developer-hub components/developer-hub \
  --set clusterDomain=apps.example.com \
  --set keycloakOidcClientSecret=dummy \
  --set giteaToken=dummy \
  --set sessionSecret=dummy \
  | grep -A1 'package:.*redhat-argocd\|security-insights\|quay-backend'
```

- [ ] **Step 4: Commit**

```bash
git add components/developer-hub/values.yaml components/developer-hub/templates/all.yaml
git commit -m "fix(developer-hub): enable image-present plugins via values toggles"
```

- [ ] **Step 5: Sync and re-run Task 3**

Any new `disabled: false` entry **must** be validated against Step 1 list before merge.

---

### Task 6: Plugin access for userN and platformadmin

**Files:**
- Reference: `components/developer-hub/templates/all.yaml` (`permission.enabled: false`)
- Reference: `components/developer-hub/templates/all.yaml` (`auth` ConfigMap / sign-in resolvers)

With `permission.enabled: false`, all authenticated users see the same plugin surface; gaps are usually **sign-in** or **empty catalog entities**, not RBAC.

- [ ] **Step 1: Confirm OIDC resolver**

```bash
oc get cm app-config-auth-rhdh -n developer-hub -o yaml | grep -A5 signIn
```

Expected: `preferredUsernameMatchingUserEntityName` and `dangerouslyAllowSignInWithoutUserInCatalog: true`.

- [ ] **Step 2: Keycloak users exist**

```bash
oc exec -n rhbk deploy/keycloak -- \
  /opt/keycloak/bin/kcadm.sh get users -r backstage -q username=user1 --fields username 2>/dev/null | head
```

Repeat for `platformadmin`.

- [ ] **Step 3: Functional plugin smoke test as `user1`**

After Task 4 UI shows users:

| Area | Expected |
| ------ | -------- |
| Catalog → Templates | Industrial Edge templates load |
| Entity (east component) → Kubernetes / Topology | Resources from **east** cluster (needs `developer-hub-spoke-tokens`) |
| Entity → CI (Tekton) | Pipelines if `janus-idp.io/tekton` annotation set |
| Docs tab | TechDocs tab if `plugins.techdocs.enabled` and entity has `backstage.io/techdocs-ref` |
| Quay card | If quay frontend plugin enabled and annotations present |

- [ ] **Step 4: Spoke tokens (Topology prerequisite)**

```bash
oc get secret developer-hub-spoke-tokens -n developer-hub -o jsonpath='{range .data}{.}{"\n"}{end}' | wc -l
oc get cronjob developer-hub-spoke-token-sync -n developer-hub
```

If secret empty: sync `field-content-developer-hub` and wait for CronJob or manual job from `spoke-token-sync.yaml`.

---

### Task 7: Keycloak org provider vs file users (dedup)

**Files:**
- Reference: `components/developer-hub/templates/all.yaml` (`catalog.providers.keycloakOrg` + file location)
- Reference: `components/developer-hub/templates/keycloak-realm.yaml`

Both sources can emit `User` entities. File users use `userN@developer-hub.local`; Keycloak realm uses the same pattern in `keycloak-realm.yaml`.

- [ ] **Step 1: Check catalog conflicts in backend logs**

```bash
oc logs -n developer-hub deploy/backstage-developer-hub -c backstage-backend --tail=200 | \
  grep -iE 'user[0-9]+|platformadmin|conflict|duplicate'
```

- [ ] **Step 2: If duplicates block processing**

Option A (minimal): keep file location as source of truth; set Keycloak catalog module schedule less aggressive or disable provider temporarily in `app-config-rhdh` for debugging.

Option B: rely on Keycloak org provider only—remove file location (not recommended for workshop; file users are deterministic).

Default for this repo: **keep file location** + Keycloak org for group membership sync.

---

### Task 8: Update developer-hub skill documentation

**Files:**
- Modify: `.cursor/skills/developer-hub-scaffolder/SKILL.md`

- [ ] **Step 1: Fix catalog mount table**

Replace wrong paths with:

| ConfigMap key | mountPath | catalog `target` |
| ------------- | --------- | ---------------- |
| `users.yaml` | `/opt/app-root/src/catalog-data` | `/opt/app-root/src/catalog-data/users.yaml` |
| `industrial-edge-system.yaml` | `/opt/app-root/src/catalog-data/ie` | `/opt/app-root/src/catalog-data/ie/industrial-edge-system.yaml` |

- [ ] **Step 2: Update dynamic plugins table**

Mark techdocs **enabled** when `plugins.techdocs.enabled: true`; document `quay-backend-dynamic` and `security-insights` must stay disabled on RHDH 1.9 unless image includes them.

- [ ] **Step 3: Commit**

```bash
git add .cursor/skills/developer-hub-scaffolder/SKILL.md
git commit -m "docs(skill): align DevHub catalog mount and plugin matrix with RHDH 1.9"
```

---

### Task 9: End-to-end verification checklist

- [ ] `oc rollout status deployment/backstage-developer-hub -n developer-hub` → success
- [ ] `grep -c "kind: User"` on pod → 51–52
- [ ] Catalog UI lists `user1`, `user50`, `platformadmin`
- [ ] OIDC login works for `user1` and `platformadmin`
- [ ] Topology/Kubernetes show spoke resources for scaffolded entity with `backstage.io/kubernetes-cluster: east`
- [ ] `install-dynamic-plugins` logs clean on newest pod
- [ ] `field-content-developer-hub` synced to intended Git revision

---

## Self-review (spec coverage)

| Requirement | Task |
| ------------- | ------ |
| More plugins for workshop users | Task 5 (image discovery) + Task 6 (smoke test) |
| userN + platformadmin in catalog | Task 4 |
| Finish rollout | Task 2 + Task 3 |
| platformadmin / userN can use plugins | Task 6 (permission off + OIDC + tokens) |
| Docs tab | Task 5/6 (techdocs enabled in values) |
| No placeholder steps | All steps have concrete commands or YAML |

## Risks

1. **Enabling a missing plugin** → init CrashLoop; always run Task 5 Step 1 before flipping `disabled`.
2. **Two Ready pods** → users read from old mount; complete Task 3 before Task 4.
3. **Confusing htpasswd with DevHub** → spokes use `htpasswd_users`; DevHub uses Keycloak only (documented in Task 6 Step 3).

---

## Execution handoff

**Plan saved to:** `docs/superpowers/plans/2026-06-02-developer-hub-plugins-users-rollout.md`

**Two execution options:**

1. **Subagent-Driven (recommended)** — one subagent per task, review between tasks  
2. **Inline Execution** — run Tasks 1–9 in this session with cluster access restored (`oc login`)

Which approach do you want?
