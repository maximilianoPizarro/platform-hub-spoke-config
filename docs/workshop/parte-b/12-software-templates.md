> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# Software Templates

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

Developer Hub Create; golden paths. Plan B: demos compartidos en catálogo.

## Show and Tell

1. Facilitador cubre módulo **12** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| Developer Hub Create | docs/assets/backstage/software-templates/ | SoftwareTemplate |
| Plan B catalog | components/workshop-demos/files/catalog/ | System |

```yaml
metadata:
  name: hybrid-mesh-shared-demos
  title: Hybrid Mesh AI — Shared Demos (Plan B)
```

```bash
oc get configmap developer-hub-catalog-demos -n developer-hub
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
