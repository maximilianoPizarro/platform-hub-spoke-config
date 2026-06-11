---
layout: default
title: Face & Object AI + Chat
parent: Hybrid Mesh AI Workshop
nav_order: 18
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Face & Object AI + Chat


![NeuroFace AI dashboard with webcam and chat]({{ site.baseurl }}/assets/images/workshop/25-neuroface-dashboard.png)
{: .mb-4 }

## Overview

NeuroFace combines **OVMS local vision** (face/object detection via `components/neuroface/` with `ovms.enabled: true`) and **MaaS chat** at `/api/chat`. Hub **ModelMesh** serves platform models; NeuroFace OVMS handles low-latency webcam inference on the app namespace.

**Overview-only (~10 min):** Developer Hub → **neuroface-workshop** → Topology; open UI without webcam.

**Hands-on (~30 min):** Register as `%USER_NAME%`, test webcam + chat, inspect OVMS Service/route in namespace `neuroface`.

Catalog: System `hybrid-mesh-ai-platform` → Component **neuroface-workshop** (links UI + OpenShift AI dashboard).

### Learn more

### Learn more

* [OpenShift AI model serving](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/serving_models/index)
* [OpenShift AI overview](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed)
* [Run AI workloads on OpenShift AI](https://developers.redhat.com/articles/2024/05/07/run-ai-workloads-openshift-ai)

## Show and Tell

. Open `https://neuroface.%HUB_DOMAIN%` — webcam object detection live.
. Send chat question about detected object; show MaaS backend (not LibreChat).
. Highlight OVMS local vision + centralized chat governance.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| NeuroFace chart | `components/neuroface/` |
| Route | `neuroface.%HUB_DOMAIN%` |

Verify in the Showroom terminal:

```bash
curl -sk -o /dev/null -w '%{http_code}' https://neuroface.%HUB_DOMAIN%/
```

## Your TODO

* [ ] Open `https://neuroface.%HUB_DOMAIN%` and test webcam detection
* [ ] Ask `/api/chat` one question about a detected object
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
curl -sk -o /dev/null -w '%{http_code}' https://neuroface.%HUB_DOMAIN%/
```

