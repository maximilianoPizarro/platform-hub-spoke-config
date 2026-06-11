---
layout: default
title: OpenShift AI Workshop
parent: Hybrid Mesh AI Workshop
nav_order: 13
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# OpenShift AI Workshop


![OpenShift AI DataScienceCluster]({{ site.baseurl }}/assets/images/workshop/22-openshift-ai.png)
{: .mb-4 }

## Overview

OpenShift AI on the hub runs **ModelMesh + Serverless (Knative)** via `default-dsc`. Each user owns project **`ai-%USER_NAME%`** with pre-provisioned **Jupyter notebook** `workshop-notebook`, MaaS secret, and Developer Hub catalog entity.

**Overview-only (~10 min):** Catalog → **OpenShift AI — %USER_NAME%** → open dashboard; show Playground in `maas-workshop` (do not run notebook).

**Hands-on (~30 min):** Launch **workshop-notebook**, run `maas-smoke-test.ipynb`, open **AI Assistants → MCP Servers** and add `ods-maas-mcp-server` URL from ConfigMap `ods-mcp-server-registration`. In **ai-%USER_NAME%** → **Models**, confirm **`workshop-sklearn`** InferenceService (ModelMesh) is Ready; test predict from dashboard or `curl` the internal predictor URL.

GitOps: `components/openshift-ai-hub/` (`user-projects.yaml`, `dashboard-config.yaml`, `ods-mcp-server.yaml`). Verify: `oc get notebook,inferenceservice -n ai-%USER_NAME%`.

### Learn more

### Learn more

* [OpenShift AI documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed)
* [Serving models — ModelMesh and KServe](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/serving_models/index)
* [Connected applications and notebooks](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/working_with_connected_applications/index)
* [Run AI workloads on OpenShift AI](https://developers.redhat.com/articles/2024/05/07/run-ai-workloads-openshift-ai)
* [Red Hat AI blog](https://www.redhat.com/en/blog/tag/artificial-intelligence)

## Show and Tell

. `oc get dsc` — confirm Ready; open **workshop-notebook** in ai-%USER_NAME%.
. Developer Hub → **OpenShift AI — %USER_NAME%** + **Playground** in maas-workshop.
. Show MCP server deployment `ods-maas-mcp-server` in maas-workshop.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| DSC + ModelMesh | `components/openshift-ai-hub/` |
| Notebooks | `user-projects.yaml` → `workshop-notebook` |
| ModelMesh ISVC | `workshop-sklearn` per `ai-userN` |
| MCP + Playground | `ods-mcp-server.yaml`, `dashboard-config.yaml` |

Verify in the Showroom terminal:

```bash
oc get dsc; oc get notebook,inferenceservice -n ai-%USER_NAME% 2>/dev/null
```

## Your TODO

* [ ] Run `oc get dsc` and confirm DataScienceCluster Ready
* [ ] Launch **workshop-notebook** in project `ai-%USER_NAME%` and run MaaS smoke test
* [ ] Open Developer Hub catalog Component **ai-%USER_NAME%**
* [ ] Enable OpenShift AI **Playground** / **MCP Server** extension (maas-workshop)
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get dsc; oc get notebook,inferenceservice -n ai-%USER_NAME% 2>/dev/null
```

