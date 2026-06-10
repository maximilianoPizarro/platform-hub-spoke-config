> **Showroom live:** `https://showroom.YOUR_HUB_DOMAIN/` (requiere registro)

# Agent Browser & Recording

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

Agent Browser YAML en `verification/agent-browser/`. Grabaciones **no** se commitean — ver runbook.

## Show and Tell

1. Facilitador cubre módulo **28** (B).
2. Comparar ROSA/AWS vs lab RHDP.

## YAML behind the scenes

| UI action | Git source | Kind |
|-----------|------------|------|
| Agent Browser | verification/agent-browser/*.yaml | Scripts |
| Recordings | NOT in Git | Local only |

```yaml
# recording-runbook.md — Win+G / OBS, no MP4 in repo
recordings/
*.mp4  # gitignored
```

```bash
test -f showroom-hybrid-mesh-ai/verification/recording-runbook.md
```

## Your TODO

- [ ] Completar lectura o lab
- [ ] Marcar progreso en Showroom in-cluster

## Verify

- Progress API responde OK

---

*Las grabaciones de pantalla del evento no se publican en este repositorio.*
