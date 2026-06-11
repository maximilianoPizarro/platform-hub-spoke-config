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

Hybrid mesh architecture connects application networks across clusters without flattening VPCs or exposing kube-apiserver endpoints publicly. The hub runs a single **Istio Gateway** that terminates all external traffic; Skupper tunnels carry requests to spoke services. The configuration lives in `components/hub-gateway/`.

*Hub Gateway — the single entry point:* One Istio-class Gateway with a ClusterIP service (no LoadBalancer — OpenShift Routes handle TLS termination upstream):

[source,yaml]
----
# components/hub-gateway/templates/gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: hub-gateway
  namespace: hub-gateway-system
  annotations:
    argocd.argoproj.io/sync-wave: "1"
    networking.istio.io/service-type: ClusterIP   # OCP Route handles external TLS
spec:
  gatewayClassName: istio
  listeners:
    - name: http
      port: 8080
      protocol: HTTP
      allowedRoutes:
        namespaces:
          from: Same             # only HTTPRoutes in hub-gateway-system can attach
----

*HTTPRoutes attach to the Gateway* for each backend — IE dashboard, workshop APIs, Kuadrant endpoints. The Kuadrant API routes (module 23) use Istio `Hostname` backendRefs to reach external MaaS without proxy containers:

[source,yaml]
----
# components/workshop-kuadrant-apis/templates/routes.yaml (pattern)
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: workshop-{{ $name }}
  namespace: hub-gateway-system
  labels:
    kuadrant.io/exposed: "true"
    workshop.kuadrant.io/external-host: {{ $api.host }}
spec:
  parentRefs:
    - name: hub-gateway
      namespace: hub-gateway-system
  hostnames: ["workshop-apis.{{ $hostname }}"]
  rules:
    - matches:
        - path: { type: PathPrefix, value: {{ $api.pathPrefix }} }
      filters:
        - type: URLRewrite
          urlRewrite:
            hostname: {{ $api.host }}     # TLS origination via ServiceEntry
      backendRefs:
        - group: networking.istio.io
          kind: Hostname
          name: {{ $api.host }}
          port: 443
----

*Skupper Sites and Connectors* in `components/service-interconnect/` bridge the hub-gateway-system to spoke namespaces, carrying traffic for IE frontends, Kafka Console, and cross-cluster observability — all encrypted over the Skupper tunnel without VPC peering.

Verify from the Showroom terminal:

[source,bash]
----
# List all HTTPRoutes attached to the hub gateway
oc get httproutes -n hub-gateway-system

# Check the Gateway status and attached routes
oc get gateway hub-gateway -n hub-gateway-system -o yaml | grep -A5 conditions

# Skupper status
oc get sites,connectors,listeners -n service-interconnect
----

Understanding this layer explains why Kuadrant policies (module 20/23) attach at the hub gateway and why Industrial Edge traffic (module 13) flows through Skupper.

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

