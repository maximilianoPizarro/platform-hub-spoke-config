---
name: hybrid-mesh-ai-workshop
description: Greenfield install and ops for Hybrid Mesh AI Workshop — Showroom, registration userN, Plan B demos, NeuroFace, ACS, content repos, verification scripts.
---

# Hybrid Mesh AI Workshop Skill

Apply when deploying, extending, or troubleshooting the **Hybrid Mesh AI Workshop** (Showroom userN + Parte A/B lab) on a fresh hub-spoke platform.

**Related skills:** `helm-app-of-apps`, `acm-hub-spoke`, `developer-hub-scaffolder`, `github-pages-docs`, `kairos-hub-spoke`.

## Two repositories

| Repo | Role |
|------|------|
| [platform-hub-spoke-config](https://github.com/maximilianoPizarro/platform-hub-spoke-config) | GitOps — `components/showroom`, `workshop-registration`, `workshop-demos`, `neuroface` |
| [showroom-hybrid-mesh-ai](https://github.com/maximilianoPizarro/showroom-hybrid-mesh-ai) | Antora lab guide (in-cluster git-cloner); **not** tracked in monorepo (`showroom-hybrid-mesh-ai/` gitignored) |

Regenerate Antora + Jekyll mirror from monorepo:

```bash
python3 scripts/generate-workshop-content.py   # writes showroom-hybrid-mesh-ai/ + docs/workshop/
bash scripts/generate-showroom-images.sh       # PNG → Antora + docs/assets/images/workshop/
# Push Antora repo separately
cd showroom-hybrid-mesh-ai && git push
```

## Greenfield install checklist (hub)

Complete **after** base platform phases in `acm-hub-spoke` / `helm-app-of-apps` (ACM, spokes, mesh, Developer Hub).

### 1. GitOps (automatic on hub sync)

Apps in `values.yaml` `connectivityLink.apps[]` (sync waves):

| Wave | App id | Namespace | Purpose |
|------|--------|-----------|---------|
| 4 | `workshop-registration` | `showroom` | Email→userN, progress API, redirect Showroom |
| 5 | `showroom` | `showroom` | Antora + terminal `oc` |
| 6 | `workshop-demos` | `developer-hub` (+ east resources) | Plan B catalog, CDC/API gaps, NP demo |
| 7 | `neuroface` | `neuroface` | Shared AI demo (MaaS chat; **no LibreChat**) |

Helm `valuesObject` wiring: `templates/component-applications.yaml`.

ConsoleLinks (hub only): **`platform-hybrid-mesh-workshop`** → registration (post-register redirect to Showroom); `platform-neuroface` for Plan B demo.

### 2. Runtime secrets (never commit to Git)

Create **after** dependent apps are Ready:

```bash
# ACS cluster registration (required before ACS UI shows hub/east/west)
oc create secret generic acs-init-credentials -n stackrox \
  --from-literal=ROX_ADMIN_PASSWORD='<central-admin-password>'
# Re-sync Argo app acs-init-bundle-sync or wait for CronJob (12h)

# Developer Hub (if not injected by RHDP helm upgrade)
# keycloakOidcClientSecret, giteaToken, sessionSecret via --set on field-content

# Optional: ACS Security Insights in Developer Hub (read-only fleet CVEs)
# --set developer-hub.rhacsApiToken=<acs-api-token>
# plugins.acsSecurityInsights.enabled: true  # only if package exists in RHDH image

# MaaS / NeuroFace / Kairos / Lightspeed — RHDP injects litemaas.apiKey, kairos.aiCredentials
```

### 3. RHDP / field-content values (required for workshop URLs)

Hub `helm upgrade` / RHDP overlay must inject:

| Value | Used by |
|-------|---------|
| `deployer.domain` | All hub routes |
| `clusters.east.domain`, `clusters.west.domain` | Registration redirect, Showroom userdata, demos catalog |
| `clusters.hub.domain` | Spoke ACS `centralEndpoint`, IE links |
| `clusters.east/west.apiUrl` + tokens | ACM, Developer Hub Topology |
| `litemaas.apiKey`, `litemaas.apiUrl` | NeuroFace chat, OpenShift AI, Lightspeed |
| `userCount` (default 50) | Registration max users, Gitea, Keycloak, htpasswd |

Spoke orders: **`clusters.hub.domain`** on east/west field-content (ACS spokes, Mailpit alerts).

### 4. Verify greenfield install

```bash
bash scripts/verify-workshop-e2e.sh

# Live URLs (replace HUB_DOMAIN)
curl -sk -o /dev/null -w '%{http_code}\n' https://workshop-registration.${HUB_DOMAIN}/api/health
curl -sk -o /dev/null -w '%{http_code}\n' https://showroom-showroom.${HUB_DOMAIN}/
curl -sk -o /dev/null -w '%{http_code}\n' https://neuroface.${HUB_DOMAIN}/api/health

oc get securedcluster -n stackrox
oc get secret -n stackrox | grep -E 'collector-tls|sensor-tls|admission-control-tls'
oc get configmap developer-hub-catalog-demos -n developer-hub
```

### 5. Facilitator smoke test (user1)

1. Open `https://workshop-registration.${HUB_DOMAIN}/` → register → redirect `showroom?USER_NAME=user1&EAST_DOMAIN=…#shared-demos`
2. Developer Hub → System **`hybrid-mesh-shared-demos`** (Plan B)
3. Showroom module **27** verification checklist
4. Password demo: `Welcome123!` (`userCount` pool `user1`…`userN`)

## Workshop userN model

| System | Auth | Notes |
|--------|------|-------|
| Registration | Email → assigns `userN` | PVC `workshop-registration-data`; admin `/admin` + `ADMIN_TOKEN` |
| Developer Hub | Keycloak OIDC | Group `developers`; RBAC CSV |
| Gitea | Same password | Org `ws-{userN}` on scaffold |
| DevSpaces | **Spoke htpasswd only** | Not Keycloak; see `developer-hub-scaffolder` |
| Showroom terminal | `%USER_NAME%` from query string | userdata ConfigMap |

Progress API: `POST /api/progress` on registration service; Showroom `progress-tracker.js`.

## CVE / vulnerability visibility for userN

| Path | Prerequisite |
|------|----------------|
| **Quay tab** (Developer Hub entity) | Image in org `workshop`; plugin enabled |
| **Security Insights** (optional) | ACS clusters registered + `RHACS_API_TOKEN` + plugin enabled |
| **ACS Central UI** | Facilitator/admin; init bundles applied |

See `docs/products/acs.md` § Developer Hub — CVE visibility for userN.

## Content delivery channels

| Channel | Audience |
|---------|----------|
| Showroom in-cluster | Hands-on lab, terminal `oc`, progress tracking |
| [docs/workshop/](https://maximilianoPizarro.github.io/platform-hub-spoke-config/workshop/) | GitHub Pages mirror (read-only) |
| [showroom-hybrid-mesh-ai](https://github.com/maximilianoPizarro/showroom-hybrid-mesh-ai) | Antora source for git-cloner |

**No video in Git:** `*.mp4`, `recordings/` excluded; runbook `showroom-hybrid-mesh-ai/verification/recording-runbook.md`.

## Troubleshooting (workshop-specific)

| Symptom | Fix |
|---------|-----|
| Showroom empty / old content | Confirm git URL in `components/showroom/values.yaml`; `oc rollout restart deploy -n showroom`; Antora repo on `main` |
| Registration redirect missing east/west | `EAST_DOMAIN`/`WEST_DOMAIN` env on registration Deployment; `clusters.east/west.domain` in valuesObject |
| Plan B catalog missing in DevHub | Sync `workshop-demos`; ConfigMap `developer-hub-catalog-demos`; catalog location in `developer-hub/all.yaml` |
| NeuroFace chat fails | `litemaas.apiKey` injected; route `neuroface.${HUB_DOMAIN}`; subchart vendored in `components/neuroface/charts/` |
| ACS UI empty clusters | Secret `acs-init-credentials`; sync `acs-init-bundle-sync` — **not** a workshop bug |
| Progress API 404 | App `workshop-registration` synced; path `/api/progress` in ConfigMap `workshop-registration-app` |

## Argo recovery (workshop apps)

```bash
for APP in field-content-workshop-registration field-content-showroom \
           field-content-workshop-demos field-content-neuroface; do
  oc annotate application $APP -n openshift-gitops argocd.argoproj.io/refresh=hard --overwrite
done
```

## Pinning releases for reproducible workshops

Pin `targetRevision` on hub/spoke Argo Applications to a platform tag (e.g. `ocp-420-v5`). Antora repo: tag or branch `main` in `components/showroom/values.yaml` `content.repoRef`.
