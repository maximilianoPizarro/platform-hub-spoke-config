---
layout: default
title: "Security & Scale in Hybrid"
parent: Hybrid Mesh AI Workshop
nav_order: 3
---

> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# Security & Scale in Hybrid

## Nube híbrida — ROSA/AWS vs este lab

| En producción (ROSA + AWS) | En este lab (RHDP hub-spoke) |
|----------------------------|------------------------------|
| Clúster ROSA en AWS (Multi-AZ) | Hub + spokes east/west importados vía ACM |
| ROSA MachineSets / autoscaling | Kairos + HPA + Kafka |
| Security Groups + IAM + NP | OVN NetworkPolicy + ACS + Kuadrant |
| Bedrock / SageMaker | OpenShift AI + MaaS + NeuroFace |
| AWS Cost Explorer | Kubecost federated ETL |
| Route 53 + ALB | Hub Gateway + Skupper |

## Contexto

ACM governance; mesh zero-trust; observabilidad multicluster; FinOps.

## Show and Tell

1. Facilitador cubre módulo **03** (A).
2. Comparar ROSA/AWS vs lab RHDP.

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
