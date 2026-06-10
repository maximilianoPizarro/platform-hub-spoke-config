> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# Worker Scaling with Kairos

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

SmartScalingPolicy sensor-scan; approve flow en Kairos Console.

## Show and Tell

1. Facilitador cubre módulo **14** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| Kairos Console | components/kairos/templates/console-rbac.yaml | ClusterRole |
| Sensor scan SSP | components/kairos/templates/sensor-scan-policies.yaml | SmartScalingPolicy |

```yaml
apiVersion: kairos.io/v1alpha1
kind: SmartScalingPolicy
metadata:
  name: scan-policy-machine-sensor
# approve scaling in Kairos Console
```

```bash
oc get smartscalingpolicy -A
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
