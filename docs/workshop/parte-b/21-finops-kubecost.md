---
layout: default
title: FinOps with Kubecost
parent: Hybrid Mesh AI Workshop
nav_order: 12
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# FinOps with Kubecost


![FinOps Kubecost cost allocation]({{ site.baseurl }}/assets/images/workshop/21-finops-kubecost.png)
{: .mb-4 }

## Overview

Kubecost on OpenShift allocates Kubernetes spend by namespace, label, and cluster — federating data from hub primary and spoke agents into MinIO-backed ETL storage. Platform teams charge back factory edge tenants and compare ROSA node costs versus on-prem depreciation using consistent Kubernetes unit economics.

In this lab, Kubecost deploys from `components/kubecost/` with agents on east/west reporting to the hub primary. Filter allocations to namespaces owned by `%USER_NAME%` and correlate idle capacity with Kairos recommendations from module 14.

FinOps closes the executive loop from module 01: hybrid strategy without cost visibility fails in CFO review. Kubecost complements AWS Cost Explorer tags on ROSA by exposing pod-level waste inside the cluster boundary.

### Learn more

### Learn more

* [Kubecost documentation](https://docs.kubecost.com/)
* [OpenShift capacity and nodes](https://docs.redhat.com/en/documentation/red_hat_openshift_container_platform/4.16/html/nodes/index)
* [Red Hat FinOps blog tag](https://www.redhat.com/en/blog/tag/finops)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **Kubecost** primary on hub with agents on east/west spokes.
* Namespace-level allocation for `%USER_NAME%` and IE workloads.
* Correlates with Kairos right-sizing recommendations (module 14).

### Business benefits

* CFO-ready chargeback without spreadsheet exports from each cluster.
* Identify idle capacity before buying more edge hardware.

### AWS — Cost Explorer + ROSA tags

```bash
aws ce get-cost-and-usage --time-period Start=2026-01-01,End=2026-02-01   --granularity MONTHLY --metrics BlendedCost   --group-by Type=TAG,Key=kubernetes.io/cluster/factory-east
aws cur put-report-definition --report-definition file://rosa-cur.json
```

### Azure — Cost Management

```bash
az consumption usage list --start-date 2026-01-01 --end-date 2026-02-01
az costmanagement export create --scope subscriptions/<sub-id> --name kubecost-sync   --storage-account hybridcost --storage-container exports --timeframe MonthToDate
```

## Show and Tell

. Kubecost UI: allocation by namespace for `%USER_NAME%`.
. Show federated cluster dropdown (hub + spokes).
. Compare idle cost with Kairos over-provision narrative.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Kubecost | `components/kubecost/` |
| MinIO data lake | `components/industrial-edge-minio/` |

Verify in the Showroom terminal:

```bash
oc get deploy -n kubecost 2>/dev/null | head -3
```

## Your TODO

* [ ] Open Kubecost and filter allocations to your namespace
* [ ] Compare hub vs spoke cluster costs in federated view
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get deploy -n kubecost 2>/dev/null | head -3
```

