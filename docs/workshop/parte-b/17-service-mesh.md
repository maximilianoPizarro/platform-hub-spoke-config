---
layout: default
title: "OpenShift Service Mesh"
parent: Hybrid Mesh AI Workshop
nav_order: 17
---

> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# OpenShift Service Mesh

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

OSSM3 ambient; Kiali; ztunnel metrics.

## Show and Tell

1. Facilitador cubre módulo **17** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
