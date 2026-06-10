> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# ACS & Connectivity Link

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

ACS Central; AuthPolicy; APIProduct demo.

## Show and Tell

1. Facilitador cubre módulo **20** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| ACS init bundles | components/acs-init-bundle-sync/ | Job |
| Kuadrant | components/hub-gateway/ | AuthPolicy |

```yaml
# Secret acs-init-credentials required in stackrox
# roxctl central init-bundles generate hub --output-secrets -
```

```bash
oc get securedcluster -n stackrox
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
