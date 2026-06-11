---
layout: default
title: Hybrid Mesh Architecture
parent: Hybrid Mesh AI Workshop
nav_order: 2
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Hybrid Mesh Architecture


![Hybrid mesh traffic flow hub to spokes]({{ site.baseurl }}/assets/images/workshop/11-hybrid-mesh.png)
{: .mb-4 }

## Overview

Hybrid mesh architecture connects application networks across clusters without flattening VPCs or exposing kube-apiserver endpoints publicly. Red Hat Service Interconnect (Skupper) paired with Gateway API HTTPRoutes on the hub creates a logical application network: frontends on the hub route to spoke services through encrypted links.

In this workshop, the hub gateway terminates external traffic and forwards to Industrial Edge frontends on east/west via Skupper Sites and Connectors defined under `components/service-interconnect/` and `components/hub-gateway/`. This is the lab analogue to ROSA ALB plus private connectivity into factory networks — same OpenShift routes and policies, different underlay.

Observe `HTTPRoute` resources and Skupper status in the console; module 13 deploys IE apps that become reachable through this mesh. Understanding this layer explains why Kuadrant policies attach at the hub gateway in module 20.

### Learn more

### Learn more

* [OpenShift Service Mesh documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/index)
* [Skupper — service interconnect](https://skupper.io/)
* [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/)
* [Gateway API for OpenShift Service Mesh](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/gateway-api-for-service-mesh)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **Skupper** service interconnect — encrypted app networks without VPN mesh complexity.
* **Gateway API HTTPRoute** on hub terminates north-south traffic.
* Industrial Edge frontends on spokes reached through logical mesh.

### Business benefits

* No flat VPC peering between every plant and cloud hub.
* Same OpenShift Routes and policies whether underlay is AWS, Azure, or MPLS.

### AWS — ALB + PrivateLink to ROSA

```bash
aws elbv2 create-load-balancer --name hybrid-ingress --type application --subnets subnet-a subnet-b
aws ec2 create-vpc-endpoint --vpc-id vpc-hub --service-name com.amazonaws.us-east-1.s3
# Skupper analog: private connectivity to spoke services without public kube API
```

### Azure — Application Gateway

```bash
az network application-gateway create --resource-group rg-workshop --name hybrid-appgw   --capacity 2 --sku Standard_v2 --public-ip-address hybrid-pip
```

## Show and Tell

. Trace external URL → hub HTTPRoute → Skupper → spoke IE frontend.
. Display Skupper site/connector status in console.
. Relate to ROSA ALB + private link narrative from Part A.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Hub gateway | `components/hub-gateway/` |
| Skupper | `components/service-interconnect/` |

Verify in the Showroom terminal:

```bash
oc get httproute -n hub-gateway-system 2>/dev/null | head -5
```

## Your TODO

* [ ] Inspect hub HTTPRoute and Skupper resources in console
* [ ] Trace how external traffic reaches IE frontends on spokes
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get httproute -n hub-gateway-system 2>/dev/null | head -5
```

