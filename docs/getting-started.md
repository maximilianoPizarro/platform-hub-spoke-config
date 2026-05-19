---
layout: default
title: Getting Started
nav_order: 3
---

# Getting Started

Follow these steps to bootstrap the hub-spoke GitOps platform from this repository.

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

---

Next: [Deploy with ACM and GitOps]({% link deploy-acm-gitops.md %}) · [Architecture]({% link architecture.md %})
