> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# Real Cases & Roadmap

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

Industrial Edge IoT; Hybrid Mesh AI roadmap; transición a Parte B hands-on.

## Show and Tell

1. Facilitador cubre módulo **05** (A).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| Industrial Edge | components/industrial-edge-tst/ | Kafka + dashboard |
| Workshop | components/showroom/ | Showroom |

```yaml
# Transition to Parte B — register at workshop-registration
```

```bash
curl -sk -o /dev/null -w '%{http_code}' https://workshop-registration.${HUB_DOMAIN}/api/health
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
