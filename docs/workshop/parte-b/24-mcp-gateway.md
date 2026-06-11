---
layout: default
title: MCP Gateway + Lightspeed
parent: Hybrid Mesh AI Workshop
nav_order: 15
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# MCP Gateway + Lightspeed


![MCP Gateway federated tools]({{ site.baseurl }}/assets/images/workshop/24-mcp-gateway.png)
{: .mb-4 }

## Overview

**MCP Gateway** deploys Kuadrant community CRDs (`MCPGatewayExtension`, `MCPServerRegistration`), `mcp-controller`, Gateway API `Gateway`, **ArgoCD MCP**, and **k8s MCP** — pattern from test-drive-pe-oscg. Public URL: `https://mcp-gateway.%HUB_DOMAIN%/mcp`.

**Overview-only (~8 min):** Catalog → **workshop-mcp-gateway**; `oc get mcpserverregistration -n mcp-system`; Lightspeed demo prompt.

**Hands-on (~30 min):** Developer Hub **/lightspeed** — activity: "List Argo CD apps in OutOfSync state and suggest sync." Llama-stack uses `remote::mcp` to gateway (`components/developer-hub/files/lightspeed/llama-stack-run.yaml`).

The configuration is declarative and minimal:

[source,yaml]
----
# components/mcp-gateway/templates/mcp-server-registration.yaml
apiVersion: kuadrant.io/v1alpha1
kind: MCPServerRegistration
metadata:
  name: argocd-mcp
  namespace: mcp-system
spec:
  url: "http://argocd-mcp-server.mcp-system.svc:8080"
  description: "Argo CD fleet operations via MCP"
  tools:
    - name: list-applications
    - name: sync-application
    - name: get-application-health
----

### Learn more

### Learn more

* [Model Context Protocol (MCP) specification](https://modelcontextprotocol.io/)
* [Kuadrant MCP Gateway extensions](https://www.kuadrant.io/docs/)
* [Developer Hub — Lightspeed and plugins](https://docs.redhat.com/en/documentation/red_hat_developer_hub)
* [Developer Hub product overview](https://developers.redhat.com/products/red-hat-developer-hub)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **MCP Gateway** — Kuadrant CRDs, ArgoCD MCP, k8s MCP tools.
* **Developer Hub Lightspeed** invokes tools via `remote::mcp`.
* Public URL `https://mcp-gateway.%HUB_DOMAIN%/mcp`.

### Business benefits

* Developers ask natural-language questions that trigger safe, scoped automation.
* Same MCP pattern for OpenShift AI assistant servers (module 22).

### AWS — Lambda tools (contrast)

```bash
aws lambda create-function --function-name list-argocd-apps   --runtime python3.12 --handler app.handler --role arn:aws:iam::123456789012:role/lambda-basic   --zip-file fileb://function.zip
# MCP Gateway on OpenShift replaces ad-hoc Lambda glue for K8s operations
```

### Azure — Functions

```bash
az functionapp create --resource-group rg-workshop --name hybrid-tools --storage-account hybridstore   --consumption-plan-location eastus --runtime python --functions-version 4
```

## Show and Tell

. `oc get mcpgatewayextension,mcpserverregistration -n mcp-system`.
. Developer Hub `/lightspeed` — prompt: list Argo CD applications.
. OpenShift AI dashboard → register MCP server URL from maas-workshop ConfigMap.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| MCP CRDs + controller | `components/mcp-gateway/` |
| Lightspeed MCP | `llama-stack-run.yaml` tool_groups |

Verify in the Showroom terminal:

```bash
oc get mcpserverregistration -n mcp-system 2>/dev/null
```

## Your TODO

* [ ] Verify MCP CRDs and `MCPServerRegistration` in `mcp-system`
* [ ] Lightspeed: list Argo CD apps via MCP gateway tools
* [ ] Register OpenShift AI MCP server in dashboard
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get mcpserverregistration -n mcp-system 2>/dev/null
```

