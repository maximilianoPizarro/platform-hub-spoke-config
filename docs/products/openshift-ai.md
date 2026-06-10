---
layout: default
title: OpenShift AI
parent: Red Hat Products
nav_order: 7
---

# OpenShift AI

Red Hat **OpenShift AI** on the **hub** provides dashboard, workbenches, KServe (RawDeployment), and MaaS-backed external models for the workshop.

## Hub component

| Path | Purpose |
|------|---------|
| `components/openshift-ai-hub/` | `DataScienceCluster`, `maas-workshop` project, MaaS proxies, playground config |
| `components/industrial-edge-data-science-cluster/` | Spoke-only DSC (east/west ML) |

## MaaS models (external)

Models are proxied from `https://maas-rhdp.apps.maas.redhatworkshops.io/v1` — API keys via RHDP `litemaas.apiKey` or Secret `openshift-ai-maas-credentials` (never Git).

| Model | Use case |
|-------|----------|
| `llama-scout-17b` | Default workshop / Lightspeed / userN |
| `deepseek-r1-distill-qwen-14b` | Admin reasoning / GitOps reconciliation |
| `codellama-7b-instruct` | Code / scaffolder / templates |

## Console

- **ConsoleLink:** Platform Hub-Spoke → OpenShift AI
- URL: `https://rhods-dashboard-redhat-ods-applications.<hub-apps-domain>`

## Developer Hub

- Software template: **OpenShift AI: Data Science Workspace**
- MCP: Developer Hub MCP tools + OpenShift AI playground config in `maas-workshop`

## Documentation

- [Red Hat OpenShift AI documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_ai/)
