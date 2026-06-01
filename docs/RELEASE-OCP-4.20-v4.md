# Release: OCP 4.20 — v4 (`ocp-420-v4`)

Snapshot extending **v3** with **Camel Dashboard** on east and west spokes (OpenShift 4.20.4, channel `stable-4.20`).

## Clusters

| Role | API / Apps domain |
|------|-------------------|
| Hub | `cluster-xqg4c` |
| East | `cluster-2847b` |
| West | `cluster-5zjkk` |

## Highlights (since `ocp-420-v3`)

- **Camel Dashboard (spokes only):** GitOps via Argo CD app `camel-dashboard-openshift-all-{east,west}`; Helm chart `camel-dashboard-openshift-all` **4.20.2**; namespace `camel-dashboard`; Hawtio plugin disabled by default.
- **Spoke templates:** `east/` and `west/` charts support external Helm repos (same pattern as hub `skupper-network-observer`).
- **Console:** Enable the Camel Dashboard plugin under **Cluster settings → Console** after sync (see [Troubleshooting](troubleshooting.md#camel-dashboard-spoke-console-plugin)).
- **Industrial Edge:** unchanged Camel K `Integration` workloads; dashboard lists `CamelApp` CRs primarily.

## GitOps entry points

| Cluster | Parent app | Child examples |
|---------|------------|----------------|
| Hub | `field-content-*`, `east-spoke-components`, `west-spoke-components` | (no camel-dashboard on hub) |
| East | `east` chart via ApplicationSet | `camel-dashboard-openshift-all-east`, `industrial-edge-tst-east` |
| West | `west` chart via ApplicationSet | `camel-dashboard-openshift-all-west`, `industrial-edge-tst-west` |

## Post-deploy checks

```bash
# Camel Dashboard (east; repeat on west context)
oc get application camel-dashboard-openshift-all-east -n openshift-gitops \
  -o jsonpath='{.status.sync.status}{" "}{.status.health.status}{"\n"}'
oc get deployment -n camel-dashboard
oc get consoleplugin | grep -i camel

# Industrial Edge regression
oc get integration mqtt-to-kafka -n industrial-edge-tst-all \
  -o jsonpath='{.status.phase}{" "}{.status.conditions[?(@.type=="Ready")].status}{"\n"}'

curl -sk -o /dev/null -w '%{http_code}\n' \
  https://line-dashboard-industrial-edge-tst-all.<east-apps-domain>/
```

Refresh all clusters:

```bash
./scripts/argocd-refresh-all.sh
```

## Pin this release

```bash
git checkout ocp-420-v4
# or set Argo CD targetRevision to tag ocp-420-v4
```

See [Troubleshooting](troubleshooting.md) for Camel Dashboard, Kafka auth, Kiali, and IE Degraded states.
