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

OpenShift Service Mesh 3 uses ambient mode: a shared ztunnel layer handles mTLS and L4 telemetry without injecting sidecars. The entire mesh stack is defined in `components/servicemeshoperator3/templates/all.yaml` — three CRDs deploy the control plane, CNI, and ztunnel:

*Istio control plane (ambient profile):*

[source,yaml]
----
# components/servicemeshoperator3/templates/all.yaml
apiVersion: sailoperator.io/v1
kind: Istio
metadata:
  name: default
  namespace: istio-system
  annotations:
    argocd.argoproj.io/sync-wave: "1"
spec:
  namespace: istio-system
  profile: ambient                        # no sidecars — ztunnel handles mTLS
  values:
    pilot:
      env:
        PILOT_ENABLE_AMBIENT: "true"
      trustedZtunnelNamespace: ztunnel
    global:
      platform: openshift
    meshConfig:
      extensionProviders:
        - name: otel-tracing              # feeds distributed tracing (module 15)
          opentelemetry:
            service: cluster-collector-collector.openshift-opentelemetry.svc.cluster.local
            port: 4317
----

*IstioCNI + ZTunnel:* CNI configures iptables interception; ZTunnel runs as a DaemonSet handling L4 mTLS:

[source,yaml]
----
apiVersion: sailoperator.io/v1
kind: IstioCNI
metadata:
  name: default
  namespace: istio-cni
spec:
  profile: ambient
  values:
    cni:
      ambient:
        reconcileIptablesOnStartup: true   # ensures clean iptables on node restart
---
apiVersion: sailoperator.io/v1
kind: ZTunnel
metadata:
  name: default
  namespace: ztunnel
  annotations:
    argocd.argoproj.io/sync-wave: "1"
spec:
  namespace: ztunnel
----

*Namespace enrollment:* Namespaces are labeled `istio.io/dataplane-mode: ambient` at sync-wave 2 — **after** the control plane is ready (wave 1). This prevents pods from starting before ztunnel can configure HBONE (port 15008):

[source,yaml]
----
# Applied to: hub-gateway-system, developer-hub, industrial-edge-tst-all (spokes), etc.
apiVersion: v1
kind: Namespace
metadata:
  name: hub-gateway-system
  labels:
    istio.io/dataplane-mode: ambient      # automatic mTLS — zero app changes
  annotations:
    argocd.argoproj.io/sync-wave: "2"
----

*Waypoint proxies* add L7 policy where needed (AuthorizationPolicy, traffic splitting):

[source,yaml]
----
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: hub-gateway-system-waypoint
  namespace: hub-gateway-system
  labels:
    istio.io/waypoint-for: service
spec:
  gatewayClassName: istio-waypoint
  listeners:
    - name: mesh
      port: 15008
      protocol: HBONE
----

*Kafka PeerAuthentication bypass:* Strimzi brokers need permissive mTLS on inter-broker port 9092 so Kafka replication works alongside ambient mesh:

[source,yaml]
----
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: kafka-strimzi-bypass
  namespace: industrial-edge-tst-all
spec:
  selector:
    matchLabels:
      strimzi.io/cluster: dev-cluster
  mtls:
    mode: STRICT
  portLevelMtls:
    9091: { mode: DISABLE }         # Strimzi admin port
    9092: { mode: PERMISSIVE }      # Kafka broker plain listener
----

Verify from the Showroom terminal:

[source,bash]
----
# Istio control plane status
oc get istio -n istio-system

# ZTunnel DaemonSet running on all nodes
oc get ztunnel -n ztunnel

# Which namespaces are meshed
oc get ns -l istio.io/dataplane-mode=ambient

# Waypoint proxies
oc get gateways -A -l istio.io/waypoint-for=service
----

Use Kiali from the OpenShift console to view live traffic for `%USER_NAME%` deployments and validate mTLS between line-dashboard and Kafka-facing services. See link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/service_mesh/index[Service Mesh documentation] for ambient mode details.

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

