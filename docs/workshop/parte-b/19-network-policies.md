> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# Network Policies

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

NetworkPolicy demo en namespace IE.

## Show and Tell

1. Facilitador cubre módulo **19** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| NP demo IE | components/workshop-demos/templates/network-policy-demo.yaml | NetworkPolicy |
| OVN | OpenShift SDN/OVN | CNI |

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ie-workshop-allow-dashboard
  namespace: industrial-edge-tst-all
```

```bash
oc get networkpolicy -n industrial-edge-tst-all
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
