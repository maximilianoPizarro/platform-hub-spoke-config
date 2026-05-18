---
layout: default
title: Developer Hub
parent: Red Hat Products
nav_order: 2
---

# Developer Hub

Red Hat **Developer Hub** is the enterprise distribution of [Backstage](https://backstage.io/), providing a software catalog, templates, and plugins for OpenShift-centric workflows.

## Plugins relevant to this platform

| Plugin area | Status | Purpose |
| ----------- | ------ | ------- |
| **OpenShift Cluster Manager (OCM)** | Enabled | Surface cluster metadata and links from the fleet perspective. |
| **Kubernetes** | Enabled | Inspect workloads and resources within connected clusters. |
| **Tekton** | Enabled | View pipeline runs from entity CI tab. |
| **Topology** | Enabled | Visual topology of workloads. |
| **Azure DevOps** | Disabled (requires config) | Pull requests and pipelines from Azure DevOps. |
| **ArgoCD** | Disabled (ENOENT in RHDH 1.9) | ArgoCD integration. |
| **Kafka** | Disabled (ENOENT in RHDH 1.9) | Kafka topic browser. |

## Authentication

GitHub OAuth is configured as the sign-in provider:

```yaml
auth:
  environment: production
  providers:
    github:
      production:
        clientId: ${GITHUB_CLIENT_ID}
        clientSecret: ${GITHUB_CLIENT_SECRET}
signInPage: github
```

- Credentials stored in Secret `developer-hub-github-auth` (manually created, never in Git)
- OAuth callback URL: `https://developer-hub.<domain>/api/auth/github/handler/frame`
- Anonymous access is disabled when GitHub auth is active

## Known issues (RHDH 1.9)

Several dynamic plugins fail `npm pack` with ENOENT errors and must be `disabled: true`:
- `backstage-community-plugin-argocd`
- `backstage-community-plugin-kafka-backend-dynamic` / `backstage-community-plugin-kafka`
- `kuadrant-backstage-plugin-backend-dynamic` / `kuadrant-backstage-plugin-frontend`
- `roadiehq-backstage-plugin-argo-cd-backend-dynamic`
- `backstage-community-plugin-redhat-argocd`

## Deployment notes

The `developer-hub` component chart provisions:
- `Backstage` CR (`rhdh.redhat.com/v1alpha5`) on the **hub**
- `app-config-rhdh` ConfigMap with app-config.yaml
- `dynamic-plugins-rhdh` ConfigMap for plugin configuration
- ServiceAccount with OCM ClusterRole
- Route: `developer-hub.<clusterDomain>`

## Links

- [Red Hat Developer Hub product documentation](https://docs.redhat.com/en/documentation/red_hat_developer_hub/)
- [Backstage documentation](https://backstage.io/docs/)
- [RHDH dynamic plugins](https://docs.redhat.com/en/documentation/red_hat_developer_hub/1.4/html/configuring_plugins_in_red_hat_developer_hub/)
