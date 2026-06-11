---
layout: default
title: LLMs & RAG
parent: Hybrid Mesh AI Workshop
nav_order: 16
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# LLMs & RAG


![LLM + RAG — factory runbooks via governed MaaS]({{ site.baseurl }}/assets/images/workshop/25-llm-rag.png)
{: .mb-4 }

## Overview

Large language models and retrieval-augmented generation (RAG) on OpenShift combine centralized inference with domain-specific context from factory docs, runbooks, and sensor logs — without exporting proprietary data to public SaaS. Red Hat Developer Hub Lightspeed assists developers in-catalog; Kairos Console agents answer scaling questions; Continue AI in DevSpaces suggests code inline using the same MaaS backend.

RAG architecture in hybrid manufacturing typically indexes PDFs and SOPs into a vector store (customer choice) while the LLM runs on link:https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed[OpenShift AI] ModelMesh or external MaaS. In this lab, you configure Lightspeed deployment in `components/developer-hub/templates/lightspeed.yaml` and test prompts against the shared MaaS endpoint — observe latency and token usage suitable for shop-floor Wi-Fi constraints.

As `%USER_NAME%`, open Developer Hub, trigger Lightspeed on a catalog Component, and compare responses with Continue AI in a DevSpaces workspace. Module 25 extends the same MaaS path to multimodal NeuroFace chat — proving one governance model serves dev, ops, and end-user AI surfaces.

### Learn more

### Learn more

* [OpenShift AI documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed)
* [Developer Hub Lightspeed plugin](https://docs.redhat.com/en/documentation/red_hat_developer_hub/html-single/plug-ins_for_red_hat_developer_hub/index#con-lightspeed-plugin)
* [AI workloads on OpenShift AI](https://developers.redhat.com/articles/2024/05/07/run-ai-workloads-openshift-ai)
* [What is RAG — Red Hat](https://www.redhat.com/en/topics/ai/what-is-retrieval-augmented-generation)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **Lightspeed** in Developer Hub for catalog-aware prompts.
* **RAG** pattern: vector store + OpenShift AI inference (lab uses MaaS endpoint).
* **Continue AI** in DevSpaces for inline code suggestions.

### Business benefits

* Factory runbooks and SOPs ground LLM answers — fewer hallucinations on the shop floor.
* Same MaaS backend as NeuroFace and AI Gateway — unified governance.

### AWS — Bedrock Knowledge Bases

```bash
aws bedrock-agent create-knowledge-base --name factory-sops   --role-arn arn:aws:iam::123456789012:role/BedrockKBRole   --knowledge-base-configuration file://kb-config.json
aws bedrock-agent ingest-knowledge-base-documents --knowledge-base-id KB123   --documents file://sops.pdf
```

### Azure — AI Search + OpenAI

```bash
az search service create --name factory-search --resource-group rg-workshop --sku basic
az cognitiveservices account deployment create --name hybrid-openai --resource-group rg-workshop   --deployment-name embeddings --model-name text-embedding-ada-002
```

## Show and Tell

. Trigger Developer Hub Lightspeed on a catalog Component live.
. Optional DevSpaces Continue AI inline suggestion using MaaS.
. Discuss RAG index placement (customer choice) vs LLM on OpenShift AI.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Developer Hub Lightspeed | `components/developer-hub/` |
| MaaS endpoint | hub `maas-workshop` |

Verify in the Showroom terminal:

```bash
oc get deploy -n developer-hub 2>/dev/null | head -5
```

## Your TODO

* [ ] Trigger Lightspeed in Developer Hub on a catalog entity
* [ ] Send one MaaS prompt and note latency/response quality
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get deploy -n developer-hub 2>/dev/null | head -5
```

