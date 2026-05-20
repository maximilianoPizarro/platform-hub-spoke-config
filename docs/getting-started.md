---
layout: default
title: Getting Started
nav_order: 3
---

# Getting Started

Follow these steps to bootstrap the hub-spoke GitOps platform from this repository.

## You'll have when finished

After a successful hub deploy and spoke registration, expect:

- [ ] **ACM** — `east` and `west` in `ManagedCluster` Ready state
- [ ] **Argo CD** — root Application synced; ApplicationSet pushing `east/` and `west/` charts
- [ ] **Industrial Edge** — sensors, MQTT, Kafka, line-dashboard on each spoke
- [ ] **Skupper** — hub `sitesInNetwork: 3`; listeners Ready in `service-interconnect`
- [ ] **Grafana** — hub dashboards with east/west Prometheus datasources
- [ ] **Developer Hub** — Industrial Edge catalog + three software templates under **Create**
- [ ] **Gitea** — route `gitea-gitea.<domain>`; orgs `ws-platformadmin`, `app-of-apps`
- [ ] **Quay** — route `quay-registry.<domain>` (optional image catalog)

Then continue with **[Scaffolding](scaffolding.md)** to deploy a new edge instance on east or west.

## Prerequisites

- **Red Hat OpenShift** 4.14 or newer on each cluster (hub + two spokes is the reference layout).
- **Three clusters**: one hub, one east-region spoke, one west-region spoke (labels determine placement).
- **Helm 3** installed locally or in a CI runner (`helm version`).
- **Git** client and a Git hosting account (GitHub is used in examples).
- Optional: `oc` CLI logged into the hub as a cluster-admin for ACM import flows.

## Repository layout

```
.              → hub cluster (path: .)
east/          → east spoke cluster (path: east)
west/          → west spoke cluster (path: west)
components/    → shared component charts referenced by all clusters
```

Each cluster path is a self-contained Helm chart with its own `Chart.yaml`, `values.yaml`, and `templates/`.

## Step 1: Fork the repository

Fork [`platform-hub-spoke-config`](https://github.com/maximilianoPizarro/platform-hub-spoke-config) (or clone into your org) so you can customize domains, secrets references, and configuration without coupling to upstream history.

Update `gitops.repoUrl` in `values.yaml`, `east/values.yaml`, and `west/values.yaml` to your fork URL.

## Step 2: Configure cluster domains

Set DNS names for each cluster:

**Hub** (`values.yaml`):
- **`deployer.domain`** — hub apps domain
- **`clusters.hub.domain`**, **`clusters.east.domain`**, **`clusters.west.domain`**

**East** (`east/values.yaml`):
- **`deployer.domain`** — east spoke apps domain
- **`clusters.hub.domain`** — hub domain for cross-cluster links

**West** (`west/values.yaml`):
- **`deployer.domain`** — west spoke apps domain
- **`clusters.hub.domain`** — hub domain for cross-cluster links

Validate rendering:

```bash
helm template test-hub . -f values.yaml --set deployer.domain=apps.hub.example.com
helm template test-east east/
helm template test-west west/
```

## Step 3: Install on the hub

The hub uses the repository root path (`.`):

**Helm (bootstrap)**

```bash
helm install platform-hub-spoke . -f values.yaml --set deployer.domain=apps.hub.example.com
```

**Argo CD Application**

Create an `Application` that points at this chart on branch `main`, matching `gitops.revision`, and supply value files via Helm parameters or a values ConfigMap pattern your org prefers.

## Step 4: Import managed clusters in ACM

From the hub, import east and west clusters using ACM's **Import cluster** flow or klusterlet automation.

Apply labels used by placement rules:

- `cluster.open-cluster-management.io/clusterset=global`
- Region labels: `region=east` and `region=west`

Ensure spoke kubeconfigs or credentials are stored per ACM requirements.

## Step 5: Register spokes as Argo CD cluster secrets

The ApplicationSet deploys spoke charts remotely. Register each spoke cluster:

```bash
helm upgrade field-content . \
  --set clusters.east.token=sha256~... \
  --set clusters.west.token=sha256~...
```

Or create cluster secrets directly with `oc apply` using label `argocd.argoproj.io/secret-type: cluster`.

## Step 6: Verify ApplicationSet generates spoke applications

On the hub, confirm the remote GitOps flow:

1. `Placement` selects labeled spokes (`region=east`, `region=west`).
2. `GitOpsCluster` binds clusters to Argo CD instances.
3. **ApplicationSet** pushes each spoke's chart (`east/`, `west/`) to the remote cluster.
4. Each spoke's Argo CD syncs child Applications locally.

Check from the hub:

```bash
oc get applications -n openshift-gitops
# Should show east-spoke-components, west-spoke-components
```

Check from each spoke:

```bash
oc get applications -n openshift-gitops
# Should show east-namespaces, east-operators, east-industrial-edge-tst, etc.
```

Healthy sync waves progress: namespaces → operators → platform → observability → Industrial Edge workloads.

## Step 7: Kiali multi-cluster (hub)

Hub Kiali can show mesh topology from east and west without Istio trust federation. Each spoke keeps its own Istio; the hub Kiali uses remote cluster secrets plus links to spoke Kiali UIs.

### 7a. Automated token sync (default — zero manual steps)

With `multiCluster.automateTokens: true` (hub) and `exportTokenForHub: true` (spokes), Argo CD **PostSync hook Jobs** run automatically on every sync:

1. **Spoke PostSync** (`kiali-hub-token-export-hook`): waits for `kiali-service-account` (created by Kiali operator), creates a token, and stores it in ConfigMap `kiali-hub-export`
2. **Hub PostSync** (`kiali-multicluster-token-sync-hook`): reads **apiUrl**/**caBundle** from each ACM `ManagedCluster`, fetches spoke tokens via **ManagedClusterView** (retries up to 10 min if spoke export hasn't completed), and creates/updates **`kiali-multi-cluster-secret`**

Both hooks have retry logic so the installation is fully automatic even if Kiali operator takes time to provision the ServiceAccount.

**Periodic refresh:** CronJobs (`kiali-hub-token-export` on spokes, `kiali-multicluster-token-sync` on hub) renew tokens every 6 hours.

To disable automation and use manual tokens instead, set `multiCluster.automateTokens: false` on the kiali chart.

### 7b. Manual tokens (optional)

If you disable `automateTokens`, create tokens on each spoke and pass them via Helm (never commit to Git):

```bash
oc create token kiali-service-account -n openshift-cluster-observability-operator --duration=8760h
```

```bash
helm upgrade field-content . \
  --set multiCluster.automateTokens=false \
  --set clusters.east.kialiToken=sha256~... \
  --set clusters.east.kialiCaData=LS0tLS1... \
  --set clusters.west.kialiToken=sha256~... \
  --set clusters.west.kialiCaData=LS0tLS1... \
  --reuse-values
```

### 7c. OpenShift login per cluster

With `auth.strategy: openshift`, users must use **Log in** in the Kiali UI for each remote cluster the first time they access it.

### 7d. Metrics note

Topology and configuration are visible across clusters. Request-rate metrics on the hub use the hub Thanos endpoint; full cross-cluster metrics require Prometheus federation (see [Observability]({% link observability.md %})).

## Step 8: Developer Hub (Keycloak OIDC)

Developer Hub uses the cluster **Keycloak** instance (`sso.<hub-domain>`) with realm `backstage`. GitHub OAuth is not used.

1. Set the same client secret on the realm and the hub Secret (do not commit real values to Git):

```bash
SECRET=$(openssl rand -base64 24)
helm upgrade field-content . \
  --set keycloakOidcClientSecret="$SECRET" \
  --reuse-values
```

Or patch after deploy:

```bash
oc create secret generic developer-hub-oidc-auth \
  --from-literal=OIDC_CLIENT_SECRET="$SECRET" \
  -n developer-hub --dry-run=client -o yaml | oc apply -f -
```

2. Log in at `https://developer-hub.<hub-domain>` with `platformadmin` / `Welcome123!` (platform-engineer) or `developer1` / `Welcome123!` (developer).

## Step 9: Continue AI (DevSpaces + Kaoto templates)

MaaS credentials are **not** stored in Git. After deploy, create the DevSpaces secret:

```bash
oc create secret generic continue-ai-config -n devspaces \
  --from-literal=CONTINUE_API_KEY='<your-maas-api-key>' \
  --from-literal=CONTINUE_API_BASE='https://litellm-prod.apps.maas.redhatworkshops.io/v1' \
  --from-literal=CONTINUE_MODEL='deepseek-r1-distill-qwen-14b' \
  --dry-run=client -o yaml | oc apply -f -
```

The **Industrial Edge** system and components are loaded from an in-cluster catalog ConfigMap (no GitHub API). Software templates are published as static assets on GitHub Pages:

`https://maximilianopizarro.github.io/platform-hub-spoke-config/assets/backstage/software-templates/`

After Argo CD syncs `developer-hub`, open **Catalog → Systems → industrial-edge** and **Create** for the templates. Ensure GitHub Pages is enabled for this repo (`docs/` on `main`).

### Developer Hub multi-cluster Topology

Spoke workloads appear in **Topology** / **Kubernetes** only when:

1. `ManagedServiceAccount` + token sync Job completed (`developer-hub-spoke-tokens` Secret exists)
2. Catalog entities have `backstage.io/kubernetes-cluster: east` or `west`

```bash
oc get secret developer-hub-spoke-tokens -n developer-hub
oc get job -n developer-hub -l job-name=developer-hub-spoke-token-sync-hook
```

Open a spoke component (e.g. **line-dashboard-east**) → Topology should list deployments in `industrial-edge-tst-all` on cluster **east**.

### Optional: Quay credentials (hub)

Never commit passwords to Git. To enable the optional `quay-push-credentials` Secret:

```bash
./scripts/generate-quay-dockerconfig.sh <quay-user> '<password>'   # output only — do not commit
helm upgrade field-content . --set quayDockerConfigJson='<json-one-line>' --reuse-values
```

Scaffolded pipelines push to the **internal OpenShift registry**; Quay is referenced in catalog via `quay.io/repository-slug`.

---

**Next →** [Scaffolding](scaffolding.md) — deploy a new Industrial Edge instance on east/west · [Architecture](architecture.md) · [Deploy with ACM and GitOps](deploy-acm-gitops.md)
