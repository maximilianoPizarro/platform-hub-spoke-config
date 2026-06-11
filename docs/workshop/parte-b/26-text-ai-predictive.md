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

### Learn more

### Learn more

* [Model serving on OpenShift AI](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/serving_models/index)
* [Notebooks and connected apps](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/working_with_connected_applications/index)
* [Red Hat AI blog](https://www.redhat.com/en/blog/tag/artificial-intelligence)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **ie-anomaly-alerter** — Prometheus-driven statistical alerts from IE metrics.
* Optional **KServe InferenceService** for custom sklearn models on hub.
* MaaS generative prompts for incident summaries post-alert.

### Business benefits

* Predictive maintenance signals before catastrophic line stops.
* Combine deterministic alerts with LLM postmortem drafts for shift handover.

### AWS — Lookout for Equipment / SageMaker anomaly

```bash
aws lookoutequipment create-dataset --dataset-name vibration-line-01 --dataset-schema file://schema.json
aws sagemaker create-model-bias-job-definition --job-definition-name ie-anomaly   --model-bias-baseline-config file://baseline.json
# Lab: ie-anomaly-alerter + OpenShift AI instead
```

### Azure — Anomaly Detector

```bash
az cognitiveservices account create --name factory-anomaly --kind AnomalyDetector   --resource-group rg-workshop --sku S0
az rest --method post --url "https://factory-anomaly.cognitiveservices.azure.com/anomalydetector/v1.0/timeseries/entire/detect"
```

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

