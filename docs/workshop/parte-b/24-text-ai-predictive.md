> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# Generative & Predictive Text

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

Anomaly alerter; KServe optional; MaaS playground.

## Show and Tell

1. Facilitador cubre módulo **24** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| Anomaly alerter | components/ie-anomaly-alerter/ | Deployment |
| KServe optional | openshift-ai-hub | InferenceService |

```yaml
# ie-anomaly-alerter watches sensor metrics
```

```bash
oc get deploy -n industrial-edge-tst-all | grep anomaly
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
