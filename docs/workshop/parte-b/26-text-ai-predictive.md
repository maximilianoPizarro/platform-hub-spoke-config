---
layout: default
title: Generative & Predictive Text
parent: Hybrid Mesh AI Workshop
nav_order: 17
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Generative & Predictive Text


## Overview

Generative AI assists operators with natural-language summaries of alarms; predictive AI forecasts failures before downtime. On OpenShift, the ie-anomaly-alerter deployment watches Prometheus metrics from Industrial Edge sensors and emits alerts when statistical thresholds breach — a lightweight predictive pattern without mandatory KServe for this workshop track.

Optional KServe InferenceService resources on the hub demonstrate full model serving for custom scikit-learn or ONNX models trained in DS workspaces. MaaS playground endpoints let `%USER_NAME%` test generative prompts for incident postmortems: "Summarize last hour Kafka lag and ACS violations for my namespace."

Connect predictive alerts to module 26 end-user apps: Camel routes can fan out anomaly events to line-dashboard overlays and NeuroFace notifications. This closes the loop from telemetry → ML/statistical detection → human + generative AI response on the same OpenShift footprint.

## Show and Tell

. Show ie-anomaly-alerter firing on threshold breach in metrics.
. MaaS prompt: generative summary of recent IE alerts.
. Mention optional KServe path for custom models.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| IE alerter | `components/ie-anomaly-alerter/` |
| Kafka topics | `industrial-edge-tst-all` |

Verify in the Showroom terminal:

```bash
oc get deploy -n industrial-edge-tst-all 2>/dev/null | grep -i anomaly
```

## Your TODO

* [ ] Confirm ie-anomaly-alerter deployment running on your spoke
* [ ] Generate one alarm summary prompt via MaaS playground
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get deploy -n industrial-edge-tst-all 2>/dev/null | grep -i anomaly
```

