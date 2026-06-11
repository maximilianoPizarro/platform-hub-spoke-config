---
layout: default
title: OpenShift Service Mesh
parent: Hybrid Mesh AI Workshop
nav_order: 8
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# OpenShift Service Mesh


![OpenShift Service Mesh ambient]({{ site.baseurl }}/assets/images/workshop/17-service-mesh.png)
{: .mb-4 }

## Overview

OpenShift Service Mesh 3 introduces ambient mode: a shared ztunnel layer handles mTLS and L4 telemetry without injecting sidecars into every workload pod by default. Kiali visualizes traffic graphs; mesh config enables distributed tracing for Industrial Edge microservices traversing east spoke namespaces. See link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/index[Service Mesh documentation] for ambient mode details.

In this workshop, OSSM3 is subscribed via `components/operators/templates/servicemeshoperator3.yaml` and configured for ambient dataplane mode on IE namespaces — excluding `stackrox` where ACS requires direct network visibility. Compare this to ROSA deployments using App Mesh or third-party meshes: OpenShift keeps mesh CRDs and policies native to the platform lifecycle.

Use Kiali from the OpenShift console to view live traffic for `%USER_NAME%` deployments and validate mTLS between line-dashboard and Kafka-facing services. Module 17 pairs with observability dashboards from module 15 for end-to-end latency analysis.

The configuration is declarative and minimal:

[source,yaml]
----
# components/servicemeshoperator3/templates/istio.yaml
apiVersion: sailoperator.io/v1alpha1
kind: Istio
metadata:
  name: default
  namespace: istio-system
spec:
  version: v1.24.3
  namespace: istio-system
  values:
    pilot:
      env:
        ENABLE_AMBIENT: "true"
----

### Learn more

### Learn more

* [OpenShift Service Mesh](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/index)
* [Istio documentation](https://istio.io/latest/docs/)
* [Ambient mesh overview](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/ambient-overview)
* [Kiali service mesh observability](https://kiali.io/docs/)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **OpenShift Service Mesh 3** ambient mode — no sidecar injection for many workloads.
* **Kiali** observability, **mTLS** between services, **waypoint** proxies where needed.
* `stackrox` namespace excluded from ambient to protect ACS sensors.

### Business benefits

* Zero-trust east-west without rewriting apps for sidecars.
* Consistent telemetry for IE microservices crossing namespaces.

### AWS — App Mesh contrast

```bash
aws appmesh create-mesh --mesh-name factory-mesh
aws appmesh create-virtual-node --mesh-name factory-mesh --virtual-node-name ie-backend   --spec file://virtual-node.json
# OpenShift Service Mesh preferred when already on ROSA/ARO
```

### Azure — Service Fabric mesh (legacy contrast)

```bash
# Prefer OpenShift Service Mesh on ARO for Kubernetes-native teams
az network application-gateway create --name mesh-ingress --resource-group rg-workshop --sku Standard_v2
```

## Show and Tell

. Open Kiali graph for IE namespace — point out ambient ztunnel edges.
. Note `stackrox` exclusion from ambient mesh.
. Optional: show mTLS lock icon on service edges.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| OSSM3 subscription | `components/servicemeshoperator3/` |
| Kiali | `components/kiali/` |

Verify in the Showroom terminal:

```bash
oc get istio -n istio-system 2>/dev/null; oc get kiali -A 2>/dev/null | head -3
```

## Your TODO

* [ ] Open Kiali and view traffic for your IE deployments
* [ ] Confirm ambient mesh enabled on IE namespace (not stackrox)
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get istio -n istio-system 2>/dev/null; oc get kiali -A 2>/dev/null | head -3
```

