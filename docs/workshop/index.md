---
layout: default
title: Hybrid Mesh AI Workshop
nav_order: 11
has_children: true
---

> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` — registro: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Hybrid Mesh AI Workshop

## Nube híbrida — ROSA/AWS vs este lab

| En producción (ROSA + AWS) | En este lab (RHDP hub-spoke) |
|----------------------------|------------------------------|
| Clúster ROSA en AWS (Multi-AZ) | Hub + spokes east/west importados vía ACM |
| ROSA MachineSets / autoscaling | Kairos + HPA + Kafka |
| Security Groups + IAM + NP | OVN NetworkPolicy + ACS + Kuadrant |
| Bedrock / SageMaker | OpenShift AI + MaaS + NeuroFace |
| AWS Cost Explorer | Kubecost federated ETL |
| Route 53 + ALB | Hub Gateway + Skupper |

## Agenda

### Parte A (01–05) — Executive
Strategy, ROSA, security/scale, AWS+AI, cases & roadmap.

### Parte B (10–28) — Hands-on
ACM, mesh, GitOps, IE, AI, NeuroFace, verification.

## Registro

OpenShift Console → **Hybrid Mesh AI Workshop** → email → `userN` → Showroom redirect.

Agenda Parte A (01–05) y Parte B (10–28). Registro: `https://workshop-registration.{hub_domain}`. Showroom live con terminal `oc`.

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
