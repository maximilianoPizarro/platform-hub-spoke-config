---
layout: default
title: AI Gateway — MaaS + Kuadrant
parent: Hybrid Mesh AI Workshop
nav_order: 14
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# AI Gateway — MaaS + Kuadrant


![AI Gateway Kuadrant MaaS]({{ site.baseurl }}/assets/images/workshop/23-ai-gateway.png)
{: .mb-4 }

## Overview

The **AI Gateway** pattern centralizes how factory, edge, and partner applications consume large language models on OpenShift. Instead of every team embedding cluster-internal URLs and shared credentials, traffic enters through **`workshop-apis.%HUB_DOMAIN%`**, backed by **Gateway API** `HTTPRoute` resources on the hub, the Istio ingress gateway, and **Kuadrant** policies for authentication (`AuthPolicy`) and token-based rate limiting (`TokenRateLimitPolicy`).

**Why Kuadrant on OpenShift AI workloads:** Kuadrant extends Gateway API with first-class API management — API keys, usage limits, and policy attachment to routes that front inference services. This matches how platform teams govern REST and gRPC APIs while still allowing data science teams to iterate in OpenShift AI projects. See the Kuadrant documentation for policy CRDs and the Developer Hub Kuadrant plugin for self-service key minting.

**Architecture in this lab:** GitOps repo path `components/workshop-kuadrant-apis/` defines the public hostname, routes `/llm` to the MaaS backend in `maas-workshop`, and attaches Kuadrant policies scoped per workshop user. Developer Hub catalog entity **workshop-ai-gateway** documents the flow for `%USER_NAME%` and links Topology to the live `HTTPRoute`.

**Overview-only (~5 min):** Catalog → **workshop-ai-gateway** → Topology; Kuadrant UI → show API key shape and rate-limit policy names (do not run full curl).

**Hands-on (~25 min):** Mint key for `%USER_NAME%`, then:

[source,bash]
----
export KEY="<your-kuadrant-api-key>"
curl -sk "https://workshop-apis.%HUB_DOMAIN%/llm/v1/chat/completions" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"granite-3-8b-instruct","messages":[{"role":"user","content":"Summarize hybrid mesh in one sentence."}]}'
----

Compare response time and HTTP 429 behavior (if you exceed limits) to a direct call from the **workshop-notebook** in project `ai-%USER_NAME%`. Record which headers prove the request passed through the gateway (auth, rate-limit counters).

**Operations angle:** The same gateway hostname can front additional model routes (embeddings, vision) without changing client apps — add `HTTPRoute` rules and Kuadrant policies in GitOps, sync with Argo CD, validate in module **29 Full verification**.

### Learn more

### Learn more

* [Kuadrant — API management for Kubernetes](https://www.kuadrant.io/docs/)
* [Authorino — authentication and authorization](https://www.kuadrant.io/docs/3.2/authorino/overview/)
* [OpenShift AI — model serving](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.16/html-single/serving_models/index)
* [Gateway API on OpenShift Service Mesh](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/gateway-api-for-service-mesh)
* [Kubernetes Gateway API specification](https://gateway-api.sigs.k8s.io/)
* [Developer Hub Kuadrant plugin — API keys](https://docs.redhat.com/en/documentation/red_hat_developer_hub/html-single/plug-ins_for_red_hat_developer_hub/index#con-kuadrant-plugin)
* [API management on Kubernetes with Kuadrant](https://developers.redhat.com/articles/2024/08/22/api-management-kubernetes-kuadrant)
* [Building a trusted AI platform on OpenShift](https://www.redhat.com/en/blog/building-trusted-ai-platform-openshift)

## Show and Tell

. Catalog → **workshop-ai-gateway** → inspect HTTPRoute in Topology.
. Kuadrant UI: create API key; curl `/llm/v1/chat/completions` with Bearer token.
. Show AuthPolicy + TokenRateLimitPolicy YAML paths in GitOps.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| HTTPRoute + policies | `components/workshop-kuadrant-apis/` |
| Catalog | `catalog-ai-platform.yaml` → workshop-ai-gateway |

Verify in the Showroom terminal:

```bash
oc get httproute -n hub-gateway-system 2>/dev/null | grep workshop
```

## Your TODO

* [ ] Open catalog **workshop-ai-gateway** and Kuadrant UI
* [ ] Create API key and call `https://workshop-apis.%HUB_DOMAIN%/llm/v1/chat/completions`
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get httproute -n hub-gateway-system 2>/dev/null | grep workshop
```

