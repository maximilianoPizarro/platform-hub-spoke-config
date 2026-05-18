---
layout: default
title: Kubecost
parent: Community & Third-Party
nav_order: 1
---

# Kubecost

Red Hat certified **Kubecost** operator provides Kubernetes cost monitoring and optimization via Federated ETL for multicluster visibility.

**Git path:** `components/kubecost/`

![Kubecost – Cluster Details]({{ site.baseurl }}/assets/images/kubecost.png)
{: .mb-4 }
*Kubecost hub cluster overview — nodes, namespaces, cost and efficiency metrics.*
{: .fs-2 .text-grey-dk-000 }

![Kubecost – Allocations by namespace]({{ site.baseurl }}/assets/images/kubecost-2.png)
{: .mb-4 }
*Cost allocations by namespace — stackrox, open-cluster-management, openshift-gitops, and platform workloads.*
{: .fs-2 .text-grey-dk-000 }

## Role in this platform

Kubecost is deployed as a **hub primary** (aggregator) and **spoke agents**. Spokes push ETL data to shared object storage (MinIO), and the hub aggregates cost data across all clusters.

## Architecture

```mermaid
flowchart LR
  subgraph Hub["Hub Cluster"]
    KCA["Kubecost<br/>CostAnalyzer<br/>(primary)"]
    AGG["Kubecost<br/>Aggregator"]
    MINIO["MinIO<br/>(shared storage)"]
    KCA --> AGG
    AGG --> MINIO
  end
  subgraph East["East Spoke"]
    KCE["Kubecost Agent<br/>(agentOnly)"]
    KCE --> MINIO
  end
  subgraph West["West Spoke"]
    KCW["Kubecost Agent<br/>(agentOnly)"]
    KCW --> MINIO
  end
```

## Deployment notes

| Cluster | Role | CostAnalyzer config |
| ------- | ---- | ------------------- |
| Hub | primary | `agentOnly: false`, `kubecostAggregator.deployMethod: statefulset` |
| East/West | agent | `agentOnly: true`, no aggregator |

### OperatorGroup

The Kubecost operator does **NOT** support `AllNamespaces` install mode. Always configure:

```yaml
spec:
  targetNamespaces:
    - kubecost
```

### Security Context Constraints

Kubecost pods require **privileged** SCC (not just `anyuid`) because they run as UID 1001 with `fsGroup: 1001` and include `seccomp` annotations. Grant to these service accounts:

- `kubecost-cost-analyzer`
- `kubecost-grafana`
- `kubecost-prometheus-server`
- `kubecost-forecasting`
- `default` (used by `kubecost-forecasting` deployment which has no explicit `serviceAccountName`)

### Federated storage

All clusters share a MinIO bucket (`kubecost`) in namespace `industrial-edge-ml-workspace` on the hub. The secret `kubecost-federated-store` contains S3-compatible credentials:

```yaml
type: S3
config:
  bucket: kubecost
  endpoint: minio.industrial-edge-ml-workspace.svc.cluster.local:9000
  region: us-east-1
  insecure: true
```

## Troubleshooting

| Error | Cause | Fix |
| ----- | ----- | --- |
| `AllNamespaces InstallModeType not supported` | OperatorGroup missing `targetNamespaces` | Set `spec.targetNamespaces: [kubecost]` |
| `forbidden: unable to validate against any security context constraint` | Missing SCC binding | Grant `system:openshift:scc:privileged` to all Kubecost SAs |
| `kubecost-forecasting` pod fails SCC | Uses `default` SA (no `serviceAccountName` set) | Include `default` SA in privileged SCC binding |

## Links

- [Kubecost documentation](https://docs.kubecost.com/)
- [Red Hat Ecosystem Catalog — Kubecost Operator](https://catalog.redhat.com/en/software/containers/kubecost/operator/668b7eaee2edda86e70a09cf)
