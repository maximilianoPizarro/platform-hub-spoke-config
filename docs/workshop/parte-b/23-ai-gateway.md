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

The **AI Gateway** (`workshop-apis.%HUB_DOMAIN%`) fronts external MaaS with **Gateway API HTTPRoute**, Istio hub gateway, and **Kuadrant** (`AuthPolicy`, `TokenRateLimitPolicy`, API keys). GitOps: `components/workshop-kuadrant-apis/templates/routes.yaml` + `policies.yaml`.

**Overview-only (~5 min):** Catalog → **workshop-ai-gateway**; Kuadrant UI → show API key shape.

**Hands-on (~25 min):** Mint key for `%USER_NAME%`, `curl -H "Authorization: Bearer $KEY" https://workshop-apis.%HUB_DOMAIN%/llm/v1/chat/completions` with JSON body; compare to direct MaaS from notebook.

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

