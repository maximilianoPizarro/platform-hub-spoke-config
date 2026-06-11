---
layout: default
title: Deploy Industrial Edge Apps
parent: Hybrid Mesh AI Workshop
nav_order: 4
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Deploy Industrial Edge Apps


![Industrial Edge deployment on spoke]({{ site.baseurl }}/assets/images/workshop/13-deploy-industrial-edge.png)
{: .mb-4 }

## Overview

Industrial Edge on OpenShift combines event streaming, integration, and visualization for factory and IoT scenarios. Apache Kafka buffers high-volume sensor topics; Camel K integrations transform and route events; line-dashboard provides operators a live view — all deployed via GitOps to spoke clusters after Developer Hub scaffolding.

Run the Industrial Edge template as `%USER_NAME%` and confirm your Gitea organization `ws-%USER_NAME%` contains the generated repository. Argo CD on east syncs the Application into namespace `industrial-edge-tst-all` (or your user-scoped equivalent). Plan B demo `demo-industrial-edge-east` offers the same topology if scaffolding is skipped.

This module is the operational heart of Part B: later observability, scaling, network policy, anomaly detection, and AI modules all assume IE workloads are running on your spoke. Verify the line-dashboard route and Kafka topics before proceeding to Kairos scaling.

### Learn more

### Learn more

* [Industrial Edge on OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift/industrial-edge)
* [AMQ Streams documentation](https://docs.redhat.com/en/documentation/red_hat_amq_streams)
* [Microservices learning hub](https://developers.redhat.com/topics/microservices)

## Show and Tell

. Confirm Gitea org `ws-%USER_NAME%` and Argo CD sync on east.
. Open line-dashboard route and Kafka Console topics.
. Offer Plan B `demo-industrial-edge-east` if scaffold fails.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| IE on spoke | `components/industrial-edge-tst/` (east Application) |
| Line dashboard | namespace `industrial-edge-tst-all` |

Verify in the Showroom terminal:

```bash
oc get deploy -n industrial-edge-tst-all 2>/dev/null | head -8
```

## Your TODO

* [ ] Scaffold IE or open Plan B `demo-industrial-edge-east`
* [ ] Verify Gitea org `ws-%USER_NAME%` and Argo CD sync Healthy
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get deploy -n industrial-edge-tst-all 2>/dev/null | head -8
```

