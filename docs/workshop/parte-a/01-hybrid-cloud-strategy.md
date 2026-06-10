> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# Hybrid Cloud Strategy

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

Modernizar apps, escalar híbrido, automatización/seguridad, time-to-market.

## Show and Tell

1. Facilitador cubre módulo **01** (A).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| Estrategia ejecutiva | docs/workshop/parte-a/ | Narrative |
| Fleet ACM | components/acm-hub-spoke/ | ManagedCluster |

```yaml
# Executive track — no CR required on cluster for Parte A
# Reference: https://docs.redhat.com/en/documentation/rosa/
```

```bash
oc get managedclusters 2>/dev/null | head -5
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
