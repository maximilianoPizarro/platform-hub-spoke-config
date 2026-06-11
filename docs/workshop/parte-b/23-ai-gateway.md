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

The **AI Gateway** pattern centralizes how factory, edge, and partner applications consume large language models on OpenShift. Instead of every team embedding cluster-internal URLs and shared credentials, traffic enters through **`workshop-apis.%HUB_DOMAIN%`**, backed by **link:https://gateway-api.sigs.k8s.io/[Gateway API]** `HTTPRoute` resources on the hub, the Istio ingress gateway, and **Red Hat Connectivity Link (RHCL)** Kuadrant policies for authentication, authorization, plan tiers, and token-based rate limiting.

Three Kuadrant CRDs in `components/workshop-kuadrant-apis/templates/policies.yaml` govern the MaaS LLM endpoint — all attached to the same `HTTPRoute`:

*1. AuthPolicy — API key authentication + OPA authorization:*

[source,yaml]
----
# components/workshop-kuadrant-apis/templates/policies.yaml
apiVersion: kuadrant.io/v1
kind: AuthPolicy
metadata:
  name: workshop-maas-auth
  namespace: hub-gateway-system
  annotations:
    argocd.argoproj.io/sync-wave: "3"
spec:
  targetRef:
    group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: workshop-maas
  rules:
    authentication:
      api-key-users:
        apiKey:
          allNamespaces: true      # keys can live in any namespace
          selector:
            matchLabels:
              app: workshop-maas
        credentials:
          authorizationHeader:
            prefix: APIKEY
    response:
      success:
        filters:
          identity:
            json:
              properties:
                userid:            # extract user ID for per-user rate limiting
                  selector: auth.identity.metadata.annotations.secret\.kuadrant\.io/user-id
    authorization:
      allow-groups:
        opa:
          rego: |
            # Only "free" or "gold" plan users are authorized
            plan := object.get(input.auth.identity.metadata.annotations,
                               "secret.kuadrant.io/plan-id", "")
            allow { plan == "free" }
            allow { plan == "gold" }
----

*2. PlanPolicy — tier-based request limits via CEL predicates:*

[source,yaml]
----
apiVersion: extensions.kuadrant.io/v1alpha1
kind: PlanPolicy
metadata:
  name: workshop-maas-plans
  namespace: hub-gateway-system
spec:
  targetRef:
    group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: workshop-maas
  plans:
    - tier: free
      predicate: |
        has(auth.identity) && auth.identity.metadata.annotations["secret.kuadrant.io/plan-id"] == "free"
      limits:
        custom:
          - limit: 100
            window: 1h
    - tier: gold
      predicate: |
        has(auth.identity) && auth.identity.metadata.annotations["secret.kuadrant.io/plan-id"] == "gold"
      limits:
        custom:
          - limit: 500
            window: 1h
----

*3. TokenRateLimitPolicy — per-user token counters with CEL:*

[source,yaml]
----
apiVersion: kuadrant.io/v1alpha1
kind: TokenRateLimitPolicy
metadata:
  name: workshop-maas-token-limits
  namespace: hub-gateway-system
spec:
  targetRef:
    group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: workshop-maas
  limits:
    free:
      rates:
        - limit: {{ .Values.tokenRateLimit.free.limit }}
          window: {{ .Values.tokenRateLimit.free.window }}
      when:
        - predicate: request.path == "/llm/v1/chat/completions"
        - predicate: |
            auth.identity.metadata.annotations["secret.kuadrant.io/plan-id"] == "free" ||
            auth.identity.groups.split(",").exists(g, g == "free")
      counters:
        - expression: auth.identity.userid     # per-user counter, not global
    gold:
      rates:
        - limit: {{ .Values.tokenRateLimit.gold.limit }}
          window: {{ .Values.tokenRateLimit.gold.window }}
      when:
        - predicate: request.path == "/llm/v1/chat/completions"
        - predicate: |
            auth.identity.metadata.annotations["secret.kuadrant.io/plan-id"] == "gold"
      counters:
        - expression: auth.identity.userid
----

*The HTTPRoute + external backend pattern:* Routes use Istio `Hostname` backendRefs to reach external MaaS without in-cluster proxy images:

[source,yaml]
----
# components/workshop-kuadrant-apis/templates/routes.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: workshop-maas
  namespace: hub-gateway-system
  labels:
    kuadrant.io/exposed: "true"
spec:
  parentRefs:
    - name: hub-gateway
      namespace: hub-gateway-system
  hostnames: ["workshop-apis.{{ .Values.clusterDomain }}"]
  rules:
    - matches:
        - path: { type: PathPrefix, value: /llm }
      filters:
        - type: URLRewrite
          urlRewrite:
            hostname: {{ .Values.apis.maas.host }}
      backendRefs:
        - group: networking.istio.io
          kind: Hostname
          name: {{ .Values.apis.maas.host }}
          port: 443
----

**Hands-on (~25 min):** Mint key for `%USER_NAME%` in Developer Hub Kuadrant UI, then:

[source,bash]
----
export KEY="<your-kuadrant-api-key>"
curl -sk "https://workshop-apis.%HUB_DOMAIN%/llm/v1/chat/completions" \
  -H "Authorization: APIKEY $KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"llama-scout-17b","messages":[{"role":"user","content":"Summarize hybrid mesh in one sentence."}],"max_tokens":50}'
----

Compare response time and HTTP 429 behavior (when token limits are exceeded) to a direct call from the **workshop-notebook** in project `ai-%USER_NAME%`.

[source,bash]
----
# Verify Kuadrant policies are applied
oc get authpolicy,planpolicy,tokenratelimitpolicy -n hub-gateway-system

# Check APIProduct catalog
oc get apiproducts -n hub-gateway-system
----

See link:https://www.kuadrant.io/docs/[Kuadrant docs] and link:https://gateway-api.sigs.k8s.io/[Gateway API specification].

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

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **Gateway API HTTPRoute** on hub with Istio ingress.
* **Kuadrant AuthPolicy** + **TokenRateLimitPolicy** — API keys per workshop user.
* Public hostname **`workshop-apis.%HUB_DOMAIN%`** routing `/llm` to MaaS backend.

### Business benefits

* Factory apps get stable external API with auth — no shared cluster-internal URLs.
* Rate limits protect MaaS from runaway OT scripts or misconfigured loops.

### AWS — API Gateway + ROSA analogy

```bash
aws apigateway create-rest-api --name factory-llm-gateway
# Map to private integration (NLB → OpenShift route) — lab uses Kuadrant instead
aws apigateway create-deployment --rest-api-id abc123 --stage-name prod

# WAF rate limit (compare Kuadrant TokenRateLimitPolicy)
aws wafv2 create-web-acl --name llm-rate-limit --scope REGIONAL   --default-action Allow={} --rules file://rate-limit-rules.json
```

### Azure — API Management

```bash
az apim create --resource-group rg-workshop --name factory-apim --publisher-name Hybrid --publisher-email admin@example.com
az apim api create --resource-group rg-workshop --service-name factory-apim   --api-id maas-llm --path llm --display-name "MaaS LLM"
az apim product create --resource-group rg-workshop --service-name factory-apim   --product-id plant-tier --product-name "Plant API tier" --subscription-required true
```

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

