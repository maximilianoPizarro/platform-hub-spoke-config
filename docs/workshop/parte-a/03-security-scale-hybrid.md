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

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| ACS Central | components/acs-operator/ | Central |
| Mesh ambient | components/operators/templates/servicemeshoperator3.yaml | Subscription |

```yaml
# stackrox namespace must NOT use istio ambient
metadata:
  name: stackrox
  labels:
    # no istio.io/dataplane-mode: ambient
```

```bash
oc get central -n stackrox
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
