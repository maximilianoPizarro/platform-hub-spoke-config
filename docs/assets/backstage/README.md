---
layout: default
title: Backstage Assets
parent: Getting Started
nav_exclude: true
---

# Backstage assets (GitHub Pages)

Static catalog entities and **software templates** for Red Hat Developer Hub. Runtime does **not** call the GitHub API — assets are served from GitHub Pages after `docs/` is published.

## URLs (after Pages deploy)

| Asset | URL |
| ----- | --- |
| Templates catalog | `https://maximilianopizarro.github.io/platform-hub-spoke-config/assets/backstage/software-templates/templates-catalog.yaml` |
| Industrial Edge template | `.../software-templates/industrial-edge/template.yaml` |
| Camel Kaoto template | `.../software-templates/industrial-edge-camel-kaoto/template.yaml` |
| Delete instance template | `.../software-templates/industrial-edge-delete/template.yaml` |

Hub RHDH loads the catalog via `catalog.locations` → `templates-catalog.yaml`.

## Software templates

### industrial-edge

Deploys an IoT edge stack on **east** or **west**:

- Namespace with `istio-injection: enabled` (sidecar, not ambient — for Prometheus `istio_*` metrics)
- Tekton Pipeline (git-clone → buildah → **internal registry**)
- Deployment + Service + ImageStream
- `catalog-info.yaml` with multi-cluster and Tekton annotations

### industrial-edge-camel-kaoto

Camel Quarkus routes with DevSpaces/Kaoto skeleton; same CI/CD and catalog pattern.

### industrial-edge-delete

Removes:

1. ArgoCD Application `gen-<owner>-<name>-<cluster>`
2. Gitea repo `ws-<owner>/<name>-<cluster>`
3. Sends in-app notification (catalog unregister may be manual)

## Skeleton annotations (required for Developer Hub tabs)

```yaml
metadata:
  annotations:
    backstage.io/kubernetes-id: ${{ values.uniqueName }}
    backstage.io/kubernetes-namespace: ${{ values.namespace }}
    backstage.io/kubernetes-cluster: ${{ values.targetCluster }}   # east | west
    janus-idp.io/tekton: ${{ values.namespace }}
    backstage.io/source-location: url:https://gitea-gitea.${{ values.clusterDomain }}/ws-...
    quay.io/repository-slug: maximilianopizarro/${{ values.uniqueName }}
  links:
    - title: Source Code (Gitea)
    - title: Documentation          # raw README on Gitea
    - title: Open in DevSpaces
```

## Scaffolder parameters

| Parameter | Notes |
| --------- | ----- |
| `clusterDomain` | Hub **apps** domain, e.g. `apps.cluster-xqg4c.dynamic2.redhatworkshops.io` |
| `targetCluster` | `east` or `west` — ArgoCD cluster name |
| `owner` | Keycloak username; Gitea org `ws-<owner>` |

## Images

| Stage | Registry |
| ----- | -------- |
| Pipeline push | `image-registry.openshift-image-registry.svc:5000/<namespace>/<uniqueName>:latest` |
| Catalog label | `quay.io/maximilianopizarro/<uniqueName>` (public) |

## Editing workflow

1. Change files under `docs/assets/backstage/`
2. Push to `main` → GitHub Pages rebuilds
3. Refresh Developer Hub catalog (or wait for poll)
4. For in-cluster IE system entities, edit `components/developer-hub/files/catalog/industrial-edge-system.yaml` and sync ArgoCD `developer-hub`

## Related docs

- [Developer Hub product page]({{ site.baseurl }}/products/developer-hub.html)
- [Annotations reference — Backstage catalog]({{ site.baseurl }}/annotations-reference.html#backstage-catalog-annotations)
