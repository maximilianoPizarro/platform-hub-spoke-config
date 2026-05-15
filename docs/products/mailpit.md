---
layout: default
title: Mailpit
parent: Red Hat Products
nav_order: 11
---

# Mailpit

## Role in this platform

Mailpit provides a lightweight **SMTP testing server** with a web UI for inspecting captured emails. It replaces real mail delivery during demos and workshops, letting operators verify that notification pipelines (Developer Hub scaffolder, CDC alerts, anomaly detection) produce correct emails without configuring external SMTP.

## How it's deployed

- **GitOps-driven**: ArgoCD Application `field-content-mailpit`, sync wave 5.
- **Namespace**: `mailpit`.
- **Image**: `docker.io/axllent/mailpit:v1.21`.
- **Ports**: SMTP on 1025, web UI on 8025.
- **Route**: `https://mailpit.<clusterDomain>` with edge TLS termination.

## Key resources created

| Resource | Name | Purpose |
| -------- | ---- | ------- |
| Deployment | `mailpit` | Single-replica Mailpit server |
| Service | `mailpit` | ClusterIP with SMTP (1025) and HTTP (8025) ports |
| Route | `mailpit` | Public HTTPS access to the web UI |

## Using Mailpit with Developer Hub notifications

Configure the RHDH notifications backend to send via SMTP to `mailpit.mailpit.svc.cluster.local:1025`. Emails appear instantly in the Mailpit web UI without requiring external mail infrastructure.

## Documentation

- [Mailpit GitHub](https://github.com/axllent/mailpit)
- [Mailpit API docs](https://mailpit.axllent.org/docs/api-v1/)

Implementation chart: `components/mailpit`.
