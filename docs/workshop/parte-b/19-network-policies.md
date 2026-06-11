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

The configuration is declarative and minimal:

[source,yaml]
----
# components/workshop-demos/templates/network-policy-demo.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dashboard-ingress
  namespace: industrial-edge-tst-all
spec:
  podSelector:
    matchLabels: { app: line-dashboard }
  ingress:
    - from:
        - namespaceSelector:
            matchLabels: { network.openshift.io/policy-group: ingress }
      ports:
        - { protocol: TCP, port: 8080 }
  policyTypes: [Ingress]
----

### Learn more

### Learn more

* [OpenShift network policies](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/networking/network-policies)
* [Understanding network policies](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/networking/understanding-network-policies)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **NetworkPolicy** demo in `industrial-edge-tst-all` from GitOps.
* OVN-Kubernetes enforcement on spokes — default-deny with explicit allow lists.
* `%USER_NAME%` tests allowed vs denied curl paths from Showroom terminal.

### Business benefits

* Micro-segmentation for OT/IT convergence — contain lateral movement.
* Complements ACS runtime policies and mesh mTLS.

### AWS — Security groups + NP

```bash
aws ec2 authorize-security-group-ingress --group-id sg-ie --protocol tcp --port 8080 --cidr 10.128.0.0/14
aws ec2 revoke-security-group-ingress --group-id sg-ie --protocol tcp --port 8080 --cidr 0.0.0.0/0
oc get networkpolicy -n industrial-edge-tst-all
```

### Azure — NSG + NP

```bash
az network nsg rule create --resource-group rg-workshop --nsg-name ie-nsg   --name allow-dashboard --priority 200 --destination-port-ranges 8080 --access Allow   --source-address-prefixes VirtualNetwork
oc exec -it deploy/curlpod -- curl -s -o /dev/null -w '%{http_code}' http://line-dashboard:8080
```

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

