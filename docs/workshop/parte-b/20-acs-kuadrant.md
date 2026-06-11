---
layout: default
title: ACS & Connectivity Link
parent: Hybrid Mesh AI Workshop
nav_order: 11
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# ACS & Connectivity Link


![ACS and Kuadrant API security]({{ site.baseurl }}/assets/images/workshop/20-acs-kuadrant.png)
{: .mb-4 }

## Overview

Red Hat Advanced Cluster Security provides vulnerability scanning, compliance benchmarks, and runtime threat detection across ACM-managed clusters. SecuredCluster agents on spokes report to ACS Central on the hub; init bundles sync via GitOps jobs in `components/acs-init-bundle-sync/`.

Connectivity Link and Kuadrant extend API management to the hub gateway: AuthPolicy validates tokens, RateLimitPolicy protects backends, and APIProduct publishes Industrial Edge APIs for external consumers. Demo `demo-ie-api-product` in Plan B catalog exposes the same Kuadrant resources without scaffolding.

As `%USER_NAME%`, verify ACS sees your spoke workloads and test APIProduct routes through the hub gateway. Remember ACS runs outside ambient mesh — this coexistence pattern is deliberate and matches production ROSA + ACS deployments.

### Learn more

### Learn more

* [ACS documentation](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_security_for_kubernetes)
* [Kuadrant documentation](https://www.kuadrant.io/docs/)
* [Developer Hub Kuadrant plugin](https://docs.redhat.com/en/documentation/red_hat_developer_hub/html-single/plug-ins_for_red_hat_developer_hub/index#con-kuadrant-plugin)
* [Developer article — API management with Kuadrant](https://developers.redhat.com/articles/2024/08/22/api-management-kubernetes-kuadrant)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **ACS Central** — vulnerability and runtime policy for containers across fleet.
* **Kuadrant** — API keys, AuthPolicy, rate limits on `workshop-apis` routes.
* Developer Hub Kuadrant plugin for self-service key minting.

### Business benefits

* Security and API governance on one OpenShift footprint — no separate API gateway appliance.
* `%USER_NAME%` keys isolate usage for chargeback and audit.

### AWS — WAF + Secrets Manager

```bash
aws secretsmanager create-secret --name kuadrant-api-keys --secret-string '{"user1":"..."}'
aws wafv2 associate-web-acl --web-acl-arn arn:aws:wafv2:... --resource-arn arn:aws:elasticloadbalancing:...
```

### Azure — Key Vault + Front Door

```bash
az keyvault secret set --vault-name hybrid-kv --name kuadrant-user1 --value <api-key>
az network front-door waf-policy create --resource-group rg-workshop --name api-waf --sku Premium_AzureFrontDoor
```

## Show and Tell

. ACS Central overview — violations and deployments on spokes.
. Demo APIProduct route via hub gateway with AuthPolicy.
. Remind ACS namespace stays outside ambient mesh.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Workshop APIs | `components/workshop-kuadrant-apis/` |
| Hub gateway | `components/hub-gateway/` |

Verify in the Showroom terminal:

```bash
oc get httproute,serviceentry -n hub-gateway-system 2>/dev/null | grep -i workshop | head -5
```

## Your TODO

* [ ] Verify ACS shows your spoke workloads in Central UI
* [ ] Test APIProduct route through hub gateway (or Plan B demo)
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get httproute,serviceentry -n hub-gateway-system 2>/dev/null | grep -i workshop | head -5
```

