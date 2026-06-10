> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# ROSA Architecture & Benefits

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

Control plane gestionado AWS; workers; SLA; mismo operador en on-prem y ROSA.

## Show and Tell

1. Facilitador cubre módulo **02** (A).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| ROSA control plane AWS | docs.redhat.com ROSA | Managed service |
| Lab hub-spoke | components/acm-hub-spoke/templates/managed-clusters.yaml | ManagedCluster |

```yaml
apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: east
  labels:
    region: east
    vendor: OpenShift
spec:
  hubAcceptsClient: true
```

```bash
oc get managedclusters
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
