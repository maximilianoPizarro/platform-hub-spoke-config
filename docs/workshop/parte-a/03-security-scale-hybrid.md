---
layout: default
title: Security & Scale in Hybrid
parent: Hybrid Mesh AI Workshop
nav_order: 3
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Security & Scale in Hybrid


![Hybrid cloud security and scale]({{ site.baseurl }}/assets/images/workshop/03-security-scale-hybrid.png)
{: .mb-4 }

## Overview

Security and scale in hybrid OpenShift environments require defense in depth: identity federation, network segmentation, runtime threat detection, and policy-driven compliance across every cluster in the fleet. Red Hat Advanced Cluster Security (ACS) centralizes vulnerability management and runtime policies while OpenShift Service Mesh adds zero-trust connectivity between microservices.

In this lab, ACS Central runs on the hub with SecuredCluster agents on spokes — note that the `stackrox` namespace deliberately avoids ambient mesh labels so ACS sensors are not disrupted. NetworkPolicy demos in module 19 use OVN on spokes, analogous to security groups plus Kubernetes NP on ROSA. Kuadrant AuthPolicy at the hub gateway shows how API traffic is authenticated and rate-limited before it reaches Industrial Edge backends.

Scaling hybrid fleets means automating placement and capacity: ACM policies, Kairos SmartScalingPolicy, Kafka buffering, and HPA together handle sensor spikes without manual ticket queues. As `%USER_NAME%`, you will observe these controls in modules 14 and 18 on workloads that simulate factory telemetry bursts.

### Learn more

### Learn more

* [Advanced Cluster Security (ACS) documentation](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_security_for_kubernetes)
* [OpenShift security and compliance](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/security_and_compliance/index)
* [ACM governance overview](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.14/html/governance/governance-overview)
* [Red Hat security blog](https://www.redhat.com/en/blog/tag/security)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* ACS Central for image/runtime policy across hub and spokes.
* OVN-Kubernetes NetworkPolicies on spokes; mesh ambient on app namespaces.
* Kuadrant rate limits at hub ingress before traffic reaches OT backends.

### Business benefits

* Detect supply-chain and runtime threats without agents blocking mesh dataplane.
* Scale sensor ingestion with Kafka + HPA while policy stays centralized in ACM.

### AWS — security services alignment

```bash
# GuardDuty + ROSA (runtime signals complement ACS)
aws guardduty create-detector --enable
# PrivateLink endpoint for ROSA API (factory networks)
aws ec2 create-vpc-endpoint --vpc-id vpc-xxx --service-name com.amazonaws.us-east-1.sts

# Security group rules for worker nodes (analog to NP module 19)
aws ec2 authorize-security-group-ingress --group-id sg-workers   --protocol tcp --port 443 --cidr 10.0.0.0/8
```

### Azure — Defender + AKS

```bash
az security pricing create --name VirtualMachines --tier Standard
az aks update --resource-group rg-workshop --name factory-east --enable-defender
az network nsg rule create --resource-group rg-workshop --nsg-name aks-nsg   --name allow-hub --priority 100 --destination-port-ranges 443 --access Allow
```

## Show and Tell

. Highlight ACS + mesh coexistence (`stackrox` without ambient labels).
. Preview NetworkPolicy (19) and Kuadrant (20) as defense layers.
. Discuss factory edge scale events and Kairos approval workflow.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| ACS operator | `components/acs-operator/` |
| ACS Central route | namespace `stackrox` |

Verify in the Showroom terminal:

```bash
oc get central -n stackrox; oc get ns stackrox --show-labels | head -3
```

## Your TODO

* [ ] List three security layers you will verify in Part B (ACS, NP, Kuadrant)
* [ ] Note why `stackrox` avoids ambient mesh in this lab
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get central -n stackrox; oc get ns stackrox --show-labels | head -3
```

