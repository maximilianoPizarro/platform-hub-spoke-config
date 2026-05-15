---
layout: default
title: Developer Hub
parent: Red Hat Products
nav_order: 2
---

# Developer Hub

Red Hat **Developer Hub** is the enterprise distribution of [Backstage](https://backstage.io/), providing a software catalog, templates, and plugins for OpenShift-centric workflows.

## Plugins relevant to this platform

| Plugin area | Purpose |
| ----------- | ------- |
| **OpenShift Cluster Manager (OCM)** | Surface cluster metadata and links from the fleet perspective. |
| **Advanced Cluster Security** | Tie vulnerability findings and policies into developer workflows. |
| **Kubernetes** | Inspect workloads and resources within connected clusters. |

## Deployment notes

The `developer-hub` component chart provisions Backstage-style Custom Resources and supporting operators on the **hub**, keeping the portal close to ACM and GitOps entry points.

## Links

- [Red Hat Developer Hub product documentation](https://docs.redhat.com/en/documentation/red_hat_developer_hub/)
- [Backstage documentation](https://backstage.io/docs/)
