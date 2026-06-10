> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# AWS Services & AI Integration

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

IAM/OIDC; Bedrock/SageMaker narrativa; patrón OpenShift AI + MaaS en lab.

## Show and Tell

1. Facilitador cubre módulo **04** (A).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| Bedrock/SageMaker (narrativa) | AWS docs | External |
| MaaS lab | components/openshift-ai-hub/ | DataScienceCluster |

```yaml
stringData:
  OPENAI_API_BASE: "https://maas-rhdp.apps.maas.redhatworkshops.io/v1"
# Secret openshift-ai-maas-credentials in maas-workshop
```

```bash
oc get dsc -A
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
