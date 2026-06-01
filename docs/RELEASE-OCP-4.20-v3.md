# Release: OCP 4.20 — v3 (`ocp-420-v3`)

Snapshot of the Hybrid Mesh hub-spoke platform validated on **OpenShift 4.20.4** (channel `stable-4.20`).

## Clusters

| Role | API / Apps domain |
|------|-------------------|
| Hub | `cluster-xqg4c` |
| East | `cluster-2847b` |
| West | `cluster-5zjkk` |

## Highlights (since `ocp-420-v2`)

- **Skupper VAN**: automated `AccessToken` sync (PostSync Job + CronJob on hub).
- **Kafka Console**: supplemental `/api` → Quarkus; `/api/auth` → UI (port 3000).
- **Kiali multicluster**: `kiali-remote-*` secrets + token-sync CronJob; legacy aggregate secret removed.
- **Industrial Edge**: Camel K `camel:paho`, Java RouteBuilder, internal-registry bootstrap Job, `mqtt-to-kafka` pull-secret.
- **KServe**: RawDeployment on spokes; `anomalyDetection.enabled: false` until MinIO model is uploaded.
- **Mesh / Kafka**: Strimzi PeerAuth scoped to brokers; entity-operator `dataplane-mode: none`; Helm `.helmignore` for Argo pack size.
- **Spoke routes**: Argo CD no longer ignores `Route.spec.host` so line-dashboard hosts match spoke domains.

## GitOps entry points

| Cluster | Parent app | Child examples |
|---------|------------|----------------|
| Hub | `field-content-*`, `east-spoke-components` (ApplicationSet) | `field-content-kafka-console`, `field-content-kiali` |
| East | `east` chart via ApplicationSet | `industrial-edge-tst-east`, `spoke-interconnect-east` |
| West | `west` chart via ApplicationSet | `industrial-edge-tst-west`, `spoke-interconnect-west` |

## Post-deploy checks

```bash
# Hub
curl -sk -o /dev/null -w '%{http_code}\n' \
  https://kafka-console.<hub-apps-domain>/api/auth/providers
curl -sk -o /dev/null -w '%{http_code}\n' \
  https://industrial-edge.<hub-apps-domain>/

# East spoke
curl -sk -o /dev/null -w '%{http_code}\n' \
  https://line-dashboard-industrial-edge-tst-all.<east-apps-domain>/

oc get integration mqtt-to-kafka -n industrial-edge-tst-all \
  -o jsonpath='{.status.phase}{" "}{.status.conditions[?(@.type=="Ready")].status}{"\n"}'

# Skupper
oc get site hub -n service-interconnect -o jsonpath='sites={.status.sitesInNetwork}{"\n"}'
```

## Pin this release

```bash
git checkout ocp-420-v3
# or set Argo CD targetRevision to tag ocp-420-v3
```

See [Troubleshooting](troubleshooting.md) for Kafka auth routes, Kiali tokens, Camel registry, and `industrial-edge-tst` Degraded states.
