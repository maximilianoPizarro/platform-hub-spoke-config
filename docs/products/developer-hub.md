---
layout: default
title: Developer Hub
parent: Red Hat Products
nav_order: 2
---

# Developer Hub

**Git path:** `components/developer-hub/`
{: .fs-3 .text-grey-dk-000 }

Red Hat **Developer Hub** (RHDH) is the enterprise distribution of [Backstage](https://backstage.io/). On this platform it is the **single pane of glass** for Industrial Edge: catalog, scaffolding, multi-cluster topology, Tekton CI, and OCM fleet overview.

## Plugins enabled on this platform

| Plugin | Tab / area | Purpose |
| ------ | ---------- | ------- |
| **OCM** | Overview cards | Managed cluster health (east/west) |
| **Kubernetes** | Kubernetes | Pods, deployments, events per cluster |
| **Topology** | Topology | Workload graph (requires `kubernetes-cluster` annotation) |
| **Tekton** | CI | PipelineRuns (`janus-idp.io/tekton` annotation) |
| **Scaffolder** | Create | Software templates from GitHub Pages |
| **Notifications** | Bell icon | In-app alerts after scaffold/delete |
| **Keycloak catalog** | Users/Groups | Sync from Keycloak `backstage` realm |

Disabled in RHDH 1.9 (ENOENT in image): ArgoCD, Kafka, Kuadrant, TechDocs (no pre-built docs).

## Authentication (Keycloak OIDC)

Sign-in uses **Keycloak**, not GitHub:

- Realm: `backstage` at `https://sso.<hub-apps-domain>`
- Client: `developer-hub`
- Secret: `developer-hub-oidc-auth` (`OIDC_CLIENT_SECRET`, `GITEA_TOKEN`, `SESSION_SECRET`)
- Config split: `app-config-rhdh` + `app-config-auth-rhdh` (avoids YAML merge bugs on resolvers)

Platform users are defined in `components/developer-hub/templates/catalog-users.yaml` (mounted as `/opt/app-root/src/users.yaml`).

## Industrial Edge catalog

The **Industrial Edge** system is registered from ConfigMap `developer-hub-catalog-ie`:

- **System**, **Domains** (hub, spoke-east, spoke-west)
- **Components** per spoke (sensors, Kafka, Camel, line-dashboard, etc.)
- **APIs** (MQTT, Kafka topics, S3 data lake)

Each spoke component includes:

```yaml
annotations:
  backstage.io/kubernetes-namespace: industrial-edge-tst-all
  backstage.io/kubernetes-id: line-dashboard          # when applicable
  backstage.io/kubernetes-cluster: east               # or west — required for Topology
  janus-idp.io/tekton: industrial-edge-ci             # CI tab for pipeline components
```

## Multi-cluster workload visibility

The Kubernetes plugin is configured for **hub**, **east**, and **west**:

1. **ManagedServiceAccount** `developer-hub` on each spoke (ACM)
2. **ClusterPermission** read-only on spoke APIs
3. **CronJob** syncs tokens → Secret `developer-hub-spoke-tokens`
4. Backstage reads `EAST_API_URL`, `EAST_SA_TOKEN`, `WEST_*` from that Secret

Without `backstage.io/kubernetes-cluster` on a catalog entity, Topology only queries the hub and shows no spoke deployments.

Verify:

```bash
oc get secret developer-hub-spoke-tokens -n developer-hub
oc get job -n developer-hub | grep spoke-token
```

## Software templates

Templates are published as **GitHub Pages** static assets under `docs/assets/backstage/software-templates/`:

| Template | Description |
| -------- | ----------- |
| Industrial Edge | IoT instance on east/west → Gitea + ArgoCD + catalog |
| Camel Kaoto | Camel routes, DevSpaces, Continue AI |
| Industrial Edge Delete | Remove ArgoCD app + Gitea repo + notification |

Catalog location (in `app-config-rhdh`):

```text
https://maximilianopizarro.github.io/platform-hub-spoke-config/assets/backstage/software-templates/templates-catalog.yaml
```

Scaffolding flow (after template run):

1. `fetch:template` — skeleton from GitHub Pages
2. `publish:github` — push to Gitea org `ws-<owner>`
3. `catalog:register` — entity in Developer Hub
4. `http:backstage:request` — create ArgoCD Application on spoke
5. `http:backstage:request` — notify owner

Entity links include **Source Code**, **Documentation** (Gitea README), and **Open in DevSpaces**.

### clusterDomain in templates

Use the **hub apps domain** including the `apps.` prefix, e.g. `apps.cluster-xqg4c.dynamic2.redhatworkshops.io`. This is used for Gitea, DevSpaces, and Developer Hub URLs in generated repos.

## Quay and container images

| Use | Image reference |
| --- | ----------------- |
| Pipeline build (Tekton buildah) | Internal OCP registry: `image-registry.openshift-image-registry.svc:5000/<namespace>/<app>:latest` |
| Deployment | Same internal image |
| Public catalog label | `quay.io/maximilianopizarro/<uniqueName>` |

Quay push credentials are optional on the hub (`quayDockerConfigJson` via Helm `--set`, never committed). Helper: `scripts/generate-quay-dockerconfig.sh`.

## Proxies for scaffolder

| Proxy | Purpose |
| ----- | ------- |
| `/api/proxy/gitea` | Delete Gitea repositories |
| `/api/proxy/k8s-api` | Create/delete ArgoCD Applications |

## Deployment components

| Resource | Purpose |
| -------- | ------- |
| `Backstage` CR | RHDH operator workload |
| `app-config-rhdh` | Catalog, kubernetes, OCM, integrations, proxy |
| `app-config-auth-rhdh` | OIDC auth |
| `dynamic-plugins-rhdh` | Plugin enable/disable |
| `managed-service-accounts.yaml` | Spoke SA for K8s plugin |
| `spoke-token-sync.yaml` | Token refresh CronJob |
| `hub-sa-token-secret.yaml` | Hub SA token for k8s-api proxy |
| `continue-ai-secret.yaml` | Continue AI in `admin-devspaces` |

Route: `https://developer-hub.<hub-apps-domain>`

## Troubleshooting

| Symptom | Likely cause | Action |
| ------- | ------------- | ------ |
| No templates / empty catalog | Permissions or mount paths | `permission.enabled: false` for demo; fix `extraFiles` mountPath; sync ArgoCD |
| `No integration found` for github.io | Missing integration host | Add `maximilianopizarro.github.io` under `integrations.github` |
| Topology shows hub only | Missing cluster annotation | Set `backstage.io/kubernetes-cluster: east\|west` |
| K8s plugin TLS errors | Self-signed API certs | `skipTLSVerify` + `NODE_TLS_REJECT_UNAUTHORIZED=0` |
| CI tab empty | Wrong Tekton annotation | `janus-idp.io/tekton: <namespace>` not `"true"` |
| IoT dashboard 503 from hub | Mesh on IE namespaces | Keep `industrial-edge-tst-all` and `spoke-gateway-system` **off** ambient mesh |

See also [Backstage assets README]({{ site.baseurl }}/assets/backstage/README.html) and the **developer-hub-scaffolder** Cursor skill.

## Links

- [Red Hat Developer Hub documentation](https://docs.redhat.com/en/documentation/red_hat_developer_hub/)
- [Backstage documentation](https://backstage.io/docs/)
- [test-drive-pe-oscg](https://github.com/maximilianoPizarro/test-drive-pe-oscg) — reference scaffolding pattern
