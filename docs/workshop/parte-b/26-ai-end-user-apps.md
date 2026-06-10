> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# AI in End-User Apps

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

line-dashboard; Camel alerts; NeuroFace + IE stack integration.

## Show and Tell

1. Facilitador cubre módulo **26** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| line-dashboard | industrial-edge-tst-all | Deployment |
| Camel | Camel K Integration | Integration |

```yaml
# End-user apps consume IE + AI stack on spoke
```

```bash
oc get deploy -n industrial-edge-tst-all line-dashboard
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
