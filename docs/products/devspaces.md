---
layout: default
title: Dev Spaces
parent: Red Hat Products
nav_order: 13
---

# Dev Spaces

**Git path:** `components/devspaces/` (east and west spokes only)
{: .fs-3 .text-grey-dk-000 }

Red Hat **OpenShift Dev Spaces** (Eclipse Che) runs on **each spoke** — not on the hub. Workshop users open DevSpaces on the spoke that matches their scaffolded project's `targetCluster`.

## What ships

| Resource | Purpose |
| -------- | ------- |
| Dev Spaces operator | OLM subscription on east/west |
| Kubernetes Image Puller operator | Pre-pulls UDI images (`CheCluster.components.imagePuller`) |
| `CheCluster` `devspaces` | Controller in namespace `devspaces` |
| Per-user namespace | `{username}-devspaces` (e.g. `user1-devspaces`) |
| PostSync `devspaces-gitea-credentials` | Git credentials for Gitea on hub |
| PostSync `devspaces-continue-ai-sync` | Continue AI env secrets from `kairos-system/kairos-ai-credentials` |

OpenShift Console link (spokes only): **DevSpaces (Kaoto + Continue AI)** → `https://devspaces.<spoke-apps-domain>`.

## Software templates

Templates link to DevSpaces with the spoke apps domain:

```
https://devspaces.<spokeAppsDomain>/#https://gitea-gitea.<hub-domain>/ws-<user>/<repo>/raw/branch/main/devfile.yaml
```

| Template | DevSpaces use |
| -------- | --------------- |
| **Camel CDC (Kaoto + Continue AI)** | Standalone Camel route + Kaoto + Continue |
| **Industrial Edge Camel Kaoto** | IE MQTT/Kafka routes with Kaoto |

Continue AI reads `CONTINUE_API_KEY`, `CONTINUE_API_BASE`, and `CONTINUE_MODEL` from Secret `continue-ai-config` in the user's DevSpaces namespace (auto-mounted via devfile controller labels).

## Authentication (Keycloak OIDC via hub)

Like [test-drive-pe-oscg](https://github.com/maximilianoPizarro/test-drive-pe-oscg), DevSpaces authenticates users with the **same Keycloak `backstage` realm** as Developer Hub — not separate OpenShift htpasswd accounts on spokes:

```yaml
networking:
  auth:
    identityProviderURL: "https://sso.<hub-domain>/realms/backstage"
    oAuthClientName: devspaces
    oAuthSecret: devspaces-oidc-secret
```

The hub Keycloak realm includes a `devspaces` OIDC client with redirect URIs for **each spoke** (`https://devspaces.<east-domain>/*`, `https://devspaces.<west-domain>/*`). Users sign in with `user1` / `Welcome123!` (same as Developer Hub).

## Operator discovery

DevSpaces does not use Backstage annotations on the cluster. Catalog entities expose DevSpaces via **entity links** and devfile URLs. Kubernetes visibility uses:

```yaml
annotations:
  backstage.io/kubernetes-cluster: east   # or west
```

## Verify

```bash
# Switch to east or west context
oc get checluster -n devspaces
oc get ns | grep devspaces
oc get job devspaces-continue-ai-sync -n devspaces
oc get secret continue-ai-config -n user1-devspaces
```

## Troubleshooting

| Symptom | Fix |
| ------- | --- |
| DevSpaces link 404 on hub | Expected — DevSpaces is spoke-only; use east/west domain |
| Continue AI no API key | Ensure `kairos-system/kairos-ai-credentials` exists on spoke; re-run sync job |
| Gitea clone fails in workspace | Check `devspaces-gitea-credentials` job and `{user}-devspaces` secret |

## Documentation

- [Red Hat OpenShift Dev Spaces](https://docs.redhat.com/en/documentation/red_hat_openshift_dev_spaces/)

**Next:** [Scaffolding](../scaffolding.md) for template parameters including `targetCluster` and `spokeAppsDomain`.
