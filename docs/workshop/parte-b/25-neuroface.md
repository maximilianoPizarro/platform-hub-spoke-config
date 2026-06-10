> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# Face & Object AI + Chat

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

Webcam; YOLO + face detection; `/api/chat` → MaaS. URL: `https://neuroface.{hub_domain}`.

## Show and Tell

1. Facilitador cubre módulo **25** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| NeuroFace UI | components/neuroface/ | Helm wrapper |
| MaaS chat | neuroface.chat.modelEndpoint | Config |
| No LibreChat | — | Decision |

```yaml
chat:
  enabled: true
  modelEndpoint: "https://maas-rhdp.apps.maas.redhatworkshops.io/v1"
  modelName: "llama-scout-17b"
ovms:
  modelmesh:
    enabled: true
litellm:
  enabled: false
```

```bash
curl -sk https://neuroface.${HUB_DOMAIN}/api/health
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
