---
layout: default
title: Kairos Operator
parent: Community & Third-Party
nav_order: 3
---

# Kairos Community Operator

AI-assisted Kubernetes optimization from the **Community Operators** catalog (`kairos-operator` v2.0.1). The platform deploys it on **hub, east, and west** via GitOps (`components/kairos/`).

## Role in this platform

| Capability | CR / resource |
| ---------- | ------------- |
| Operator install | OLM `Subscription` in `kairos-system` |
| Multi-cluster UI | `KairosConsole` (hub only) |
| Workload analysis | `KairosAgent` per cluster + per environment (`-dev`, `-qa`, `-prod`) |
| Sensor / metrics scan | `SmartScalingPolicy` (scan policies on `machine-sensor-*`) |
| Events | `KairosEvent` (optional) |

Industrial Edge software templates create namespaces ending in `-dev`, `-qa`, or `-prod` so environment agents and Kairos scan tiers align with Developer Hub scaffolds.

## AI model credentials (do not lose on reinstall)

The Granite / OpenShift AI endpoint is configured in Git; **credentials stay in the cluster only**:

```text
Secret: kairos-system/kairos-ai-credentials
Key:    api-key   (see values.yaml — kairos.aiCredentials.secretKey)
```

Argo CD **ignoreDifferences** on that Secret prevents GitOps from overwriting your key. Before reinstall:

```bash
oc get secret kairos-ai-credentials -n kairos-system -o yaml > /tmp/kairos-ai-credentials.backup.yaml
# Remove metadata.resourceVersion, uid, etc. if restoring manually
```

After sync, agents reference the same Secret name via `spec.aiModel.apiKeySecret`.

Default model URL (hub OpenShift AI):

`https://isvc-granite-31-8b-fp8-predictor.sandbox-shared-models.svc.cluster.local:8443/v1/chat/completions`

## Reinstall from catalog (replace manual CRDs)

Previously CRDs were applied with `kubectl`; the catalog **ClusterServiceVersion** now owns them. Safe migration:

1. **Back up** `kairos-ai-credentials` (above).
2. **Commit and sync** `field-content-kairos` (hub) and `kairos-east` / `kairos-west` spoke apps.
3. **Remove duplicate manual installs** only if they conflict (same CRDs from CSV are fine):

   ```bash
   # Optional: delete old kubectl-applied CRs that duplicate Git names
   oc delete kairosagent hub-agent -n kairos-system --ignore-not-found
   # Git will recreate hub-agent, agent-dev-environments, etc.
   ```

4. **Do not delete** `kairos-ai-credentials` or the `Subscription` if the operator is already healthy.

Verify:

```bash
oc get subscription kairos-operator -n kairos-system
oc get csv -n kairos-system | grep kairos
oc get kairosagent,smartscalingpolicy -n kairos-system
```

Console route: `https://kairos-console-kairos-system.<hub-apps-domain>`

## Scan policies for machine sensors

On **spokes**, Git deploys `SmartScalingPolicy` resources:

- `scan-policy-machine-sensor-1`
- `scan-policy-machine-sensor-2`

Targets: `machine-sensor-1` / `machine-sensor-2` in `industrial-edge-tst-all` (platform baseline). AI-assisted rules use CPU/memory thresholds; OTel/Prometheus endpoints match the observability stack.

Scaffolded apps add **labeled** `machine-sensor-*` deployments in namespaces like `ie-factory-1-east-dev`. **KairosAgents** watch:

| Agent | Namespace suffix | Mode |
| ----- | ---------------- | ---- |
| `agent-dev-environments` | `-dev` | autopilot |
| `agent-qa-environments` | `-qa` | supervised |
| `agent-prod-environments` | `-prod` | supervised (dry-run corrections on hub cluster agent config) |

Label required: `kairos.io/managed=true`

## Developer Hub templates

When scaffolding Industrial Edge or Camel/Kaoto, choose **Environment** (`dev` / `qa` / `prod`). Artifact names include the suffix, for example:

- Repo: `edge-factory-1-east-dev`
- Namespace: `ie-edge-factory-1-east-dev`
- Catalog component: `user1-edge-factory-1-dev`

Use three scaffolds (same factory, different environments) to exercise all three Kairos agent tiers.

## Git paths

| Cluster | Argo Application | Chart |
| ------- | ------------------ | ----- |
| Hub | `field-content-kairos` | `components/kairos/` |
| East | `kairos-east` | `components/kairos/` |
| West | `kairos-west` | `components/kairos/` |

Upstream operator: [github.com/maximilianoPizarro/kairos](https://github.com/maximilianoPizarro/kairos)
