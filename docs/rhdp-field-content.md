# RHDP Field Content — 3 cluster orders (hub / east / west)

Use **three separate catalog orders**, one per OpenShift cluster.

## How RHDP injects cluster domain (`existing_gitops: true`)

RHDP does **not** template `values.yaml` in Git. It creates an Argo CD `Application` with inline `spec.source.helm.values` containing:

- `deployer.domain` ← `openshift_cluster_ingress_domain`
- `deployer.apiUrl` ← `openshift_api_url`
- `litemaas.apiKey` / `litemaas.apiUrl` (when LiteLLM enabled)

**Never put `{{ openshift_cluster_ingress_domain }}` in Git-tracked YAML** — Helm interprees `{{ }}` as Helm template syntax and Argo CD fails with `invalid map key`.

Hub templates use `deployer.domain` with fallback `apps.cluster.example.com`; RHDP overrides via Argo CD values.

## Catalog parameters

| Parameter | Hub | East | West |
|-----------|-----|------|------|
| `ocp4_workload_field_content_gitops_repo_url` | `https://github.com/maximilianoPizarro/platform-hub-spoke-config` | same | same |
| `ocp4_workload_field_content_gitops_repo_revision` | `main` | `main` | `main` |
| `ocp4_workload_field_content_gitops_repo_path` | `.` | `east/` | `west/` |
| `existing_gitops` | `true` | `true` | `true` |

## Recommended order

1. **Hub** — path `.`
2. **East** / **West** — separate clusters, paths `east/` and `west/`
3. **Hub** — after ACM import, upgrade with spoke domains + tokens:

```bash
helm upgrade field-content . -f values.yaml \
  --set deployer.domain=apps.cluster-<hub>.dynamic2.redhatworkshops.io \
  --set deployer.apiUrl=https://api.cluster-<hub>.dynamic2.redhatworkshops.io:6443 \
  --set clusters.hub.domain=apps.cluster-<hub>.dynamic2.redhatworkshops.io \
  --set clusters.east.domain=apps.cluster-<east>.dynamic2.redhatworkshops.io \
  --set clusters.east.apiUrl=https://api.cluster-<east>.dynamic2.redhatworkshops.io:6443 \
  --set clusters.west.domain=apps.cluster-<west>.dynamic2.redhatworkshops.io \
  --set clusters.west.apiUrl=https://api.cluster-<west>.dynamic2.redhatworkshops.io:6443 \
  --set clusters.east.token=sha256~... \
  --set clusters.west.token=sha256~...
```

Or patch the Argo CD `Application` `field-content` `helm.values` with the same keys.

## Verify hub after provision

```bash
oc get application field-content -n openshift-gitops
oc get applications -n openshift-gitops -l app.kubernetes.io/part-of=platform-hub-spoke
```

Expect many `field-content-*` child apps after `field-content` syncs. If sync is `Unknown`, check:

```bash
oc get application field-content -n openshift-gitops -o jsonpath='{.status.conditions[*].message}{"\n"}'
```

## Local validation

```bash
helm template test-hub . -f values.yaml \
  --set deployer.domain=apps.hub.example.com \
  --set deployer.apiUrl=https://api.hub.example.com:6443 \
  --set clusters.hub.domain=apps.hub.example.com
```
