> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# Deploy Industrial Edge Apps

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

Scaffold IE east/west; Gitea `ws-{user_name}`; Argo CD Application on spoke.

## Show and Tell

1. Facilitador cubre módulo **13** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| Scaffold IE | software-templates/industrial-edge/template.yaml | SoftwareTemplate |
| Spoke deploy | east/templates/component-applications.yaml | Application |

```yaml
# Argo CD Application on spoke after scaffold
spec:
  destination:
    namespace: industrial-edge-tst-all
```

```bash
oc get applications -n openshift-gitops | grep industrial
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
