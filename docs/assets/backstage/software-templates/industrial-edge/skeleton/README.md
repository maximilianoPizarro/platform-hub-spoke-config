# Industrial Edge — ${{ values.name }} (${{ values.targetCluster }})

IoT edge instance scaffolded from Developer Hub.

## Cluster

- **Target spoke:** `${{ values.targetCluster }}`
- **Namespace:** `${{ values.namespace }}`
- **Image (deploy):** `image-registry.openshift-image-registry.svc:5000/${{ values.namespace }}/${{ values.uniqueName }}:latest`
- **Quay (public catalog):** `quay.io/maximilianopizarro/${{ values.uniqueName }}`

## Components

- Namespace with Istio sidecar injection (Prometheus `istio_*` metrics)
- Tekton pipeline (git-clone → buildah → Quay.io)
- Deployment + Service

## Links

- [Gitea repo](https://gitea-gitea.${{ values.clusterDomain }}/ws-${{ values.owner }}/${{ values.name }}-${{ values.targetCluster }})
- [Open in DevSpaces](https://devspaces.${{ values.clusterDomain }}/#https://gitea-gitea.${{ values.clusterDomain }}/ws-${{ values.owner }}/${{ values.name }}-${{ values.targetCluster }})
