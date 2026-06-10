> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# LLMs & RAG

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

Developer Lightspeed; Kairos agents; Continue AI DevSpaces.

## Show and Tell

1. Facilitador cubre módulo **23** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| Lightspeed | components/developer-hub/templates/lightspeed.yaml | Deployment |
| Kairos agents | components/kairos/ | Console |

```yaml
# MaaS endpoint shared with NeuroFace and Continue AI on spokes
```

```bash
oc get deploy -n developer-hub | grep lightspeed
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
