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

OpenShift AI on the hub runs **ModelMesh + Serverless (Knative)** via `default-dsc`. Each user owns project **`ai-%USER_NAME%`** with pre-provisioned **Jupyter notebook** `workshop-notebook`, MaaS secret, and Developer Hub catalog entity. The configuration lives in `components/openshift-ai-hub/`.

*App-of-Apps valuesObject for OpenShift AI* configures model serving modes, user projects, MCP integration, and available MaaS models — all declarative:

[source,yaml]
----
# templates/component-applications.yaml — openshift-ai-hub valuesObject
helm:
  valuesObject:
    clusterDomain: {{ $domain }}
    userCount: {{ $.Values.userCount | default 50 }}
    userProjects:
      enabled: true               # creates ai-user1..ai-userN projects
      notebook:
        enabled: true             # pre-provisions workshop-notebook per user
    dashboardExtensions:
      enabled: true
    modelServing:
      modelMeshEnabled: true      # shared multi-model serving
      serverlessEnabled: true     # KServe for dedicated single-model
      defaultDeploymentMode: ModelMesh
    mcp:
      enabled: true
      deployServer: true          # deploys ods-maas-mcp-server in maas-workshop
    maas:
      endpoint: {{ $.Values.litemaas.apiUrl }}
      apiKey: {{ $.Values.litemaas.apiKey }}
      models:
        - id: llama-scout-17b
          displayName: Llama Scout 17B (workshop default)
        - id: deepseek-r1-distill-qwen-14b
          displayName: DeepSeek R1 Distill Qwen 14B
        - id: codellama-7b-instruct
          displayName: CodeLlama 7B Instruct
----

**Overview-only (~10 min):** Catalog → **OpenShift AI — %USER_NAME%** → open dashboard; show Playground in `maas-workshop` (do not run notebook).

**Hands-on (~30 min):** Launch **workshop-notebook**, run `maas-smoke-test.ipynb`, open **AI Assistants → MCP Servers** and add `ods-maas-mcp-server` URL from ConfigMap `ods-mcp-server-registration`. In **ai-%USER_NAME%** → **Models**, confirm **`workshop-sklearn`** InferenceService (ModelMesh) is Ready; test predict from dashboard or `curl` the internal predictor URL.

[source,bash]
----
# Confirm DataScienceCluster is Ready
oc get dsc default-dsc -o jsonpath='{.status.phase}'

# Check your user project and notebook
oc get notebook,inferenceservice -n ai-%USER_NAME%

# List available MaaS models
oc get configmap ods-mcp-server-registration -n maas-workshop -o yaml

# MCP server deployment
oc get pods -n maas-workshop -l app=ods-maas-mcp-server
----

See link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI documentation] for DSC and model serving guides.

### Learn more

### Learn more

* [OpenShift AI documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed)
* [Serving models — ModelMesh and KServe](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/serving_models/index)
* [Connected applications and notebooks](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/working_with_connected_applications/index)
* [Run AI workloads on OpenShift AI](https://developers.redhat.com/articles/2024/05/07/run-ai-workloads-openshift-ai)
* [Red Hat AI blog](https://www.redhat.com/en/blog/tag/artificial-intelligence)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **DataScienceCluster** (`default-dsc`) — ModelMesh, KServe, dashboard, notebooks.
* Per-user project **`ai-%USER_NAME%`** with `workshop-notebook` and InferenceService `workshop-sklearn`.
* MaaS playground in `maas-workshop` — shared LLM for all AI modules.

### Business benefits

* Data scientists and developers share one governed inference layer.
* Notebooks and pipelines stay on-cluster — no export of factory data to public SaaS.

### AWS — SageMaker vs OpenShift AI

```bash
# SageMaker endpoint (cloud alternative — lab uses OpenShift AI instead)
aws sagemaker create-model --model-name sklearn-factory --primary-container   Image=246618743249.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3,ModelDataUrl=s3://models/sklearn.tar.gz
aws sagemaker create-endpoint-config --endpoint-config-name sklearn-cfg   --production-variants VariantName=AllTraffic,ModelName=sklearn-factory,InitialInstanceCount=1,InstanceType=ml.m5.large
aws sagemaker create-endpoint --endpoint-name sklearn-factory --endpoint-config-name sklearn-cfg
```

### Azure — ML workspace

```bash
az ml workspace create --resource-group rg-workshop --name factory-ml
az ml online-deployment create --name sklearn-deploy --model sklearn:1 --workspace-name factory-ml
```

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

