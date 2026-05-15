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

## Step 1: Fork the repository

Fork [`platform-hub-spoke-config`](https://github.com/maximilianoPizarro/platform-hub-spoke-config) (or clone into your org) so you can customize domains, secrets references, and branch strategy without coupling to upstream history.

Update `gitops.repoUrl` in `values.yaml`, `values-east.yaml`, and `values-west.yaml` to your fork URL.

## Step 2: Configure `values.yaml` with cluster domains

Set realistic DNS names for ingress and cluster APIs:

- **`deployer.domain`** — base apps domain used by Helm templates where hostnames are templated (override per environment as needed).
- **`clusters.hub.domain`**, **`clusters.east.domain`**, **`clusters.west.domain`** — align with your managed cluster URLs and TLS certificates.

Validate rendering early:

```bash
helm template test-release . -f values.yaml --set deployer.domain=apps.hub.example.com
```

## Step 3: Install on the hub

Choose one approach:

**Helm (bootstrap)**

```bash
helm install platform-hub-spoke . -f values.yaml --set deployer.domain=apps.hub.example.com
```

**Argo CD Application**

Create an `Application` that points at this chart on branch `main`, matching `gitops.revision`, and supply value files via Helm parameters or a values ConfigMap pattern your org prefers.

## Step 4: Import managed clusters in ACM

From the hub, import east and west clusters using ACM’s **Import cluster** flow or klusterlet automation.

Apply labels used by placement rules, for example:

- `cluster.open-cluster-management.io/clusterset=your-set`
- Region labels such as `region=east` and `region=west` if your `Placement` selectors expect them.

Ensure spoke kubeconfigs or credentials are stored per ACM requirements.

## Step 5: Create east/west branches with spoke values

Maintain branch-aligned values:

| Branch | Values file | Purpose |
| -------|-------------|---------|
| `main` | `values.yaml` | Hub-centric defaults |
| `east` | `values-east.yaml` | East spoke overlays (`gitops.revision: east`) |
| `west` | `values-west.yaml` | West spoke overlays (`gitops.revision: west`) |

Merge structural chart changes on `main`, then rebase or merge into `east`/`west` so spokes stay compatible.

## Step 6: Verify ApplicationSet generates spoke applications

On the hub, confirm ACM GitOps integration:

1. `Placement` selects labeled spokes.
2. `GitOpsCluster` binds clusters to Argo CD instances.
3. **ApplicationSet** generators (for example **matrix** of cluster × component) emit per-spoke `Application` objects.

Check Argo CD UI or CLI:

```bash
argocd app list
kubectl get applications -n openshift-gitops
```

Healthy sync waves should progress from namespaces → operators → platform → observability → workloads.

---

Next: [Deploy with ACM and GitOps]({% link deploy-acm-gitops.md %}) · [Architecture]({% link architecture.md %})
