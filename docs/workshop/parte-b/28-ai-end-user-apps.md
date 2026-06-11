---
layout: default
title: AI in End-User Apps
parent: Hybrid Mesh AI Workshop
nav_order: 19
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# AI in End-User Apps


![AI in end-user applications]({{ site.baseurl }}/assets/images/workshop/26-ai-end-user-apps.png)
{: .mb-4 }

## Overview

End-user applications — operator dashboards, mobile alerts, MES integrations — consume AI insights where work happens, not only in data science notebooks. line-dashboard on the east spoke visualizes Kafka sensor streams; Camel integrations route anomaly events; NeuroFace and MaaS summaries embed into the same UX `%USER_NAME%` sees in production rollouts.

This module integrates modules 13–25: verify line-dashboard displays live IE data, trigger ie-anomaly-alerter thresholds, and optionally embed a NeuroFace iframe or chat link for contextual AI help. Camel K Integrations from templates `demo-camel-kaoto-east` and `demo-camel-cdc-east` show event-driven patterns factory teams deploy on OpenShift alongside OT systems.

Platform teams win when AI is invisible infrastructure: OpenShift AI, MaaS, and NeuroFace become services catalog entries — app squads bind them through Developer Hub dependencies without rebuilding ML pipelines per plant.

### Learn more

### Learn more

* [Developer Hub — golden paths for apps](https://docs.redhat.com/en/documentation/red_hat_developer_hub)
* [OpenShift AI — production patterns](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed)
* [Industrial Edge on OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift/industrial-edge)

## Show and Tell

. line-dashboard live data + anomaly overlay or alert badge.
. Optional Camel integration status in Topology.
. Story: operator sees telemetry, prediction, and AI help in one UX.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Line dashboard | `industrial-edge-tst-all` |
| Developer Hub IE catalog | `components/developer-hub/files/catalog/industrial-edge-system.yaml` |

Verify in the Showroom terminal:

```bash
oc get deploy -n industrial-edge-tst-all line-dashboard 2>/dev/null
```

## Your TODO

* [ ] Verify line-dashboard shows live IE telemetry
* [ ] Connect one anomaly or AI insight to operator workflow
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get deploy -n industrial-edge-tst-all line-dashboard 2>/dev/null
```

