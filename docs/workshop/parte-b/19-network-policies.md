---
layout: default
title: Network Policies
parent: Hybrid Mesh AI Workshop
nav_order: 10
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Network Policies


![Network policies workshop demo]({{ site.baseurl }}/assets/images/workshop/19-network-policies.png)
{: .mb-4 }

## Overview

Kubernetes NetworkPolicy on OpenShift OVN enforces micro-segmentation: only labeled pods and namespaces you explicitly allow can communicate — essential for zero-trust factory networks where compromised sensors must not lateral-move to MES backends. Red Hat OpenShift ships OVN-Kubernetes as the default CNI with policy-aware routing.

This workshop applies a demo NetworkPolicy in `industrial-edge-tst-all` from `components/workshop-demos/templates/network-policy-demo.yaml`, allowing dashboard ingress while denying unexpected cross-namespace traffic. As `%USER_NAME%`, test allowed and denied paths using `oc exec` curl probes from the Showroom terminal.

Compare to ROSA security groups plus Kubernetes NP: defense in depth at cloud VPC and pod layers. Pair this module with ACS (module 20) for runtime anomaly detection when policies are misconfigured or bypassed.

## Show and Tell

. Apply or review demo NetworkPolicy in `industrial-edge-tst-all`.
. Run allowed vs denied curl from Showroom terminal pods.
. Relate to ROSA security groups + NP defense in depth.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| NP demo | `components/workshop-demos/templates/network-policy-demo.yaml` |
| IE namespace | `industrial-edge-tst-all` |

Verify in the Showroom terminal:

```bash
oc get networkpolicy -n industrial-edge-tst-all 2>/dev/null
```

## Your TODO

* [ ] Review NetworkPolicy in `industrial-edge-tst-all`
* [ ] Test one allowed and one denied pod-to-pod connection
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get networkpolicy -n industrial-edge-tst-all 2>/dev/null
```

