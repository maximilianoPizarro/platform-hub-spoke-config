---
layout: default
title: AWS Services & AI Integration
parent: Hybrid Mesh AI Workshop
nav_order: 4
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# AWS Services & AI Integration


![AWS and AI integration on OpenShift]({{ site.baseurl }}/assets/images/workshop/04-aws-ai-integration.png)
{: .mb-4 }

## Overview

AWS customers often pair ROSA with native AI services — Amazon Bedrock for foundation models, SageMaker for training pipelines, and IAM OIDC for secure workload identity. Red Hat's hybrid approach keeps inference and data pipelines on OpenShift AI while still allowing optional AWS service integration via credentials and external endpoints where policy permits.

This workshop intentionally substitutes OpenShift AI plus Model-as-a-Service (MaaS) for Bedrock/SageMaker so you experience a portable pattern: a `DataScienceCluster` on the hub, shared LLM endpoint, and consumer apps (NeuroFace, Developer Hub Lightspeed) on spokes. The secret `openshift-ai-maas-credentials` and MaaS base URL mirror how production teams centralize model access instead of embedding API keys in every deployment.

Module 22 onward activates this stack hands-on. Executives should recognize that OpenShift AI on ROSA or on-prem avoids rewriting applications when cloud AI pricing or residency rules change — the Kubernetes-native serving layer moves with the cluster.

### Learn more

### Learn more

* [ROSA on AWS](https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws)
* [OpenShift AI — self-managed](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed)
* [Developer article — AI workloads on OpenShift AI](https://developers.redhat.com/articles/2024/05/07/run-ai-workloads-openshift-ai)
* [AWS — Red Hat OpenShift Service on AWS](https://aws.amazon.com/rosa/)

## Show and Tell

. Contrast Bedrock/SageMaker with OpenShift AI + MaaS in this lab.
. Show MaaS credential secret location conceptually (no secret values).
. Explain portable inference when AWS residency or pricing changes.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| OpenShift AI hub | `components/openshift-ai-hub/` |
| MaaS credentials | namespace `maas-workshop` |

Verify in the Showroom terminal:

```bash
oc get dsc -A 2>/dev/null; oc get ns maas-workshop 2>/dev/null
```

## Your TODO

* [ ] Compare your AWS AI services with OpenShift AI + MaaS lab pattern
* [ ] Locate module 22 for hands-on DSC and MaaS setup
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get dsc -A 2>/dev/null; oc get ns maas-workshop 2>/dev/null
```

