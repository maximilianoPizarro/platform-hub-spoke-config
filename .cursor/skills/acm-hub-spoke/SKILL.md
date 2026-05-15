---
name: acm-hub-spoke
description: ACM hub-spoke GitOps patterns for OpenShift—placement, ApplicationSet, branches, mesh ambient, gateway, Grafana.
---

# ACM Hub-Spoke Platform Skill

Apply this skill when designing or troubleshooting **fleet GitOps** that combines **Red Hat ACM** with **OpenShift GitOps** and regional Industrial Edge clusters.

## ACM operator installation

- Install from stable channels appropriate to your OpenShift version.
- Confirm **`MultiClusterHub`** reaches Running before registering spokes.
- Keep klusterlet versions compatible with hub; watch ACM upgrade docs during z-stream bumps.

## Placement, GitOpsCluster, ApplicationSet

1. **ManagedClusterSet** groups clusters for RBAC boundaries.
2. **Placement** expresses label selectors (for example `region=east`).
3. **PlacementDecision** materializes matching cluster names for generators.
4. **GitOpsCluster** wires those clusters into Argo CD’s managed cluster inventory.
5. **ApplicationSet** uses generators (matrix, cluster-decision, SCM) to stamp `Application` resources without per-cluster Git forks.

Prefer label-driven placement over embedding kube-apiserver URLs in Git.

## Branch-based spoke configuration

- **`main`**: hub-oriented `values.yaml`.
- **`east` / `west`**: branch pointers in `gitops.revision` with regional values files.
- Promote chart template changes through **main first**, then merge into regional branches to avoid skew.

## Cluster domain externalization

Store DNS in values (`deployer.domain`, `clusters.*.domain`). ACM import and Argo destinations should reference cluster secrets created by the GitOps integration—not literals committed to the repo.

## Service Mesh ambient mode (multi-cluster)

- Align identity/trust configuration across hubs and spokes before enabling strict mTLS defaults.
- Start with namespaces that already use Kafka clients and Camel integrations.
- Use **waypoints** only where L7 policy complexity justifies another hop.

## Hub Gateway as F5 analog

- Implement **Gateway API** `Gateway` + `HTTPRoute` with weighted backends for traffic shaping.
- Coordinate DNS wildcards and TLS certs with central PKI.
- Layer Connectivity Link policies after baseline routing works.

## Grafana dashboards for east-west

- Configure Prometheus-compatible data sources per region.
- Standardize dashboard UIDs and labels so hub Grafana can load both without duplication.
- Capture Kafka consumer lag and factory KPIs consistently across regions for apples-to-apples comparisons.

## Quick verification commands

```bash
kubectl get managedcluster
kubectl get placement -A
kubectl get placementdecision -A
kubectl get applications -n openshift-gitops
```
