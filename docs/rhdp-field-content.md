# RHDP Field Content — 3 cluster orders (hub / east / west)

Use **three separate catalog orders**, one per OpenShift cluster. Each order points at this repo with a different Helm path and merges `values-rhdp.yaml` (Ansible/Jinja overlays).

## Catalog parameters (all three orders)

| Parameter | Hub | East | West |
|-----------|-----|------|------|
| `ocp4_workload_field_content_gitops_repo_url` | `https://github.com/maximilianoPizarro/platform-hub-spoke-config` | same | same |
| `ocp4_workload_field_content_gitops_repo_revision` | `main` | `main` | `main` |
| `ocp4_workload_field_content_gitops_repo_path` | `.` | `east/` | `west/` |
| `existing_gitops` | `true` | `true` | `true` |

RHDP must merge **two values files** (base + overlay):

| Cluster | Base | RHDP overlay (Jinja) |
|---------|------|----------------------|
| Hub | `values.yaml` | `values-rhdp.yaml` |
| East | `east/values.yaml` | `east/values-rhdp.yaml` |
| West | `west/values.yaml` | `west/values-rhdp.yaml` |

If your catalog item supports `ocp4_workload_field_content_gitops_extra_values` or an extra-values file path, point it at the overlay file for that path.

## Variables injected automatically (per cluster)

| RHDP variable | Helm value | Hub | East | West |
|---------------|------------|-----|------|------|
| `openshift_cluster_ingress_domain` | `deployer.domain` | this hub | this east spoke | this west spoke |
| `openshift_api_server_url` | `deployer.apiUrl` | this hub | this east spoke | this west spoke |
| `openshift_cluster_ingress_domain` | `clusters.hub.domain` | same as hub | — | — |
| `openshift_cluster_hub_ingress_domain` | `clusters.hub.domain` | — | **required** | **required** |
| `litellm_virtual_key` | `litemaas.apiKey` | hub only | — | — |
| `litellm_api_base_url` | `litemaas.apiUrl` | hub only | — | — |

### Hub-only optional (after east/west exist)

Set on a **second hub helm upgrade** or via catalog custom vars:

- `openshift_cluster_east_ingress_domain` → `clusters.east.domain`
- `openshift_cluster_east_api_url` → `clusters.east.apiUrl`
- `openshift_cluster_west_ingress_domain` → `clusters.west.domain`
- `openshift_cluster_west_api_url` → `clusters.west.apiUrl`

## Recommended order

1. **Hub** — path `.`, merge `values.yaml` + `values-rhdp.yaml`
2. **East** — path `east/`, set `openshift_cluster_hub_ingress_domain` to the hub's `openshift_cluster_ingress_domain`
3. **West** — path `west/`, same hub domain parameter
4. **Hub again** — import east/west in ACM; `helm upgrade` with spoke domains + tokens:

```bash
helm upgrade field-content . -f values.yaml -f values-rhdp.yaml \
  --set clusters.east.domain=apps.cluster-<east-id>.dynamic2.redhatworkshops.io \
  --set clusters.east.apiUrl=https://api.cluster-<east-id>.dynamic2.redhatworkshops.io:6443 \
  --set clusters.west.domain=apps.cluster-<west-id>.dynamic2.redhatworkshops.io \
  --set clusters.west.apiUrl=https://api.cluster-<west-id>.dynamic2.redhatworkshops.io:6443 \
  --set clusters.east.token=sha256~... \
  --set clusters.west.token=sha256~...
```

## Local validation (without Jinja)

```bash
helm template test-hub . -f values.yaml \
  --set deployer.domain=apps.hub.example.com \
  --set deployer.apiUrl=https://api.hub.example.com:6443 \
  --set clusters.hub.domain=apps.hub.example.com

helm template test-east east/ -f east/values.yaml \
  --set deployer.domain=apps.east.example.com \
  --set deployer.apiUrl=https://api.east.example.com:6443 \
  --set clusters.hub.domain=apps.hub.example.com

helm template test-west west/ -f west/values.yaml \
  --set deployer.domain=apps.west.example.com \
  --set deployer.apiUrl=https://api.west.example.com:6443 \
  --set clusters.hub.domain=apps.hub.example.com
```

## East / west spoke on hub

After hub `field-content-acm-hub-spoke` syncs, ACM ApplicationSet `industrial-edge-spoke` creates `east-spoke-components` and `west-spoke-components` using `east/values.yaml` and `west/values.yaml` from Git. Update those files (or hub `clusters.east/west`) once spoke domains are known so Developer Hub, Kiali, and hub-gateway multicluster URLs are correct.
