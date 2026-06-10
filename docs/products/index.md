---
layout: default
title: Red Hat Products
nav_order: 11
has_children: true
---

# Red Hat Products

This platform composes multiple Red Hat operators and patterns. Each child page answers three questions for operators who arrived via **[Getting Started](../getting-started.md)**: what ships here, **what signals tell an operator it has reconciled**, and **how workloads join inventory** (CRDs vs annotations vs explicit registrations).

Keep **[Discover workloads consistently](../architecture.md#components-on-the-hub-vs-spokes)** in mind as context — namespaces rarely manage ACM fleets directly; charts declare APIs operators reconcile against Git.

## Overview

| Product | Role in platform | Git path |
| ------- | ----------------- | -------- |
| [Advanced Cluster Management](acm.md) | Fleet lifecycle, policy, placement, GitOps integration | `components/acm-hub-spoke/` |
| [Developer Hub](developer-hub.md) | Internal developer portal (Backstage) | `components/developer-hub/` |
| [Advanced Cluster Security](acs.md) | Vulnerability management, runtime risk | `components/acs-secured-cluster/` |
| [OpenShift GitOps](openshift-gitops.md) | Declarative continuous delivery (Argo CD) | `components/openshift-gitops/` |
| [OpenShift Service Mesh 3](service-mesh.md) | Ambient mesh, ztunnel, waypoints | `components/servicemeshoperator3/` |
| [Connectivity Link](connectivity-link.md) | RHCL / Gateway API (hub + spoke gateway screenshots) | `components/rhcl-operator/` |
| [Service Interconnect](../service-interconnect.md) | Skupper VAN for cross-cluster connectivity | `components/service-interconnect/` |
| [OpenShift AI](openshift-ai.md) | DataScienceCluster, model serving | `components/openshift-ai/` |
| [NeuroFace](neuroface.md) | Workshop face/object AI + MaaS chat | `components/neuroface/` |
| [AMQ Streams](amq-streams.md) | Kafka for telemetry pipelines | `components/industrial-edge-*/` |
| [Apache Camel / Camel K](camel-k.md) | Integrations (MQTT, S3, Kafka) | `components/camel-k/` |
| [OpenShift Pipelines](pipelines.md) | Tekton CI/CD for Industrial Edge | `components/industrial-edge-pipelines/` |
| [Quay Registry](quay.md) | Hub container registry, workshop org | `components/quay-registry/` |
| [Dev Spaces](devspaces.md) | Spoke IDEs (Kaoto + Continue AI) | `components/devspaces/` |
| [OpenShift Virtualization](cnv.md) | Workshop VM + CNV template | `components/cnv-example/` |
| [Gitea](gitea.md) | Hub Git for scaffolder repos | `components/gitea/` |
| [Kafka Console](kafka-console.md) | Hub UI for spoke Kafka clusters | `components/kafka-console/` |

## Operator discovery — annotations & registrations at a glance

Most visibility comes from **CRDs**, but namespaces carry mesh/policy hints when controllers reconcile selectively:

| Product | Where workloads surface | Typical annotation / label / CR binding |
| ------- | ------------------------- | ------------------------------------------ |
| [ACM](acm.md) | Fleet hub inventory | **`ManagedCluster`**, **`Placement`** — spokes inherit ACM labels during import (no Git annotation magic). |
| [Developer Hub](developer-hub.md) | Catalog / plugins / Topology | **`Backstage`** CR + `app-config-*`; OCM + **Kubernetes** (hub/east/west via MSA tokens); catalog annotation **`backstage.io/kubernetes-cluster`**. |
| [ACS](acs.md) | Central clusters UI | **`SecuredCluster`** in each cluster's **`stackrox`** namespace + TLS Secrets from **init bundles**. |
| [GitOps](openshift-gitops.md) | Argo CD Applications | **`Application`** / **`ApplicationSet`** — paths/branches define drift detection targets. |
| [Service Mesh](service-mesh.md) | Ambient dataplane | Namespace **`istio.io/dataplane-mode: ambient`** (see **`components/namespaces`**); exceptions **`stackrox`**, **`gitea`**, **`industrial-edge-data-lake`**, … stay **off mesh**. |
| [Connectivity Link](connectivity-link.md) | Gateway exposure | Gateway API **`Gateway`** / **`HTTPRoute`** CRDs Kuadrant/DNS controllers reconcile (explicit refs). |
| [OpenShift AI](openshift-ai.md) | DS pipelines / serving | **`DataScienceCluster`** operator provisioning — namespaces created/managed by operator CRs. |
| [AMQ Streams](amq-streams.md) | Kafka Console UI | This repo: **`Console`** CR (`kafkaClusters[].namespace` + bootstrap URL). Strimzi **`Kafka`** CRs live in those namespaces. |
| [Camel K](camel-k.md) | Integrations | **`IntegrationPlatform`** (per-operator scope) selects Camel runtime profile for that namespace set. |
| [Pipelines](pipelines.md) | Tekton controllers | **`TektonConfig`** cluster-wide / operator-managed — namespaces enabled by operator policy. |
| [Quay](quay.md) | Image registry (hub) | **`QuayRegistry`** CR + org setup Job — catalog uses **`quay.io/repository-slug`** annotation. |
| [Dev Spaces](devspaces.md) | Spoke dev environments | **`CheCluster`** on east/west — catalog entity **links** to devfile URL on spoke domain. |
| [CNV](cnv.md) | Virtual machines | **`VirtualMachine`** CRs — catalog **`backstage.io/kubernetes-*`** on hub. |
| [Gitea](gitea.md) | Source repos (hub) | PostSync org Job — scaffolder **`backstage.io/source-location`** URLs. |
| [Kafka Console](kafka-console.md) | Fleet Kafka UI | **`Console`** CR `spec.kafkaClusters[]` — explicit bootstrap list. |
| [Service Interconnect](../service-interconnect.md) | Cross-cluster Services | **`Site`**, **`Listener`**, **`Connector`** Skupper CRs — **not** workload Deployment annotations. |

Details and YAML snippets live on each product page under **Operator discovery**.

For the complete list of every Kubernetes label and annotation that activates a feature — namespace enrollment, monitoring selectors, gateway hints, ConfigMap syncing — see **[Annotations & Labels Reference](../annotations-reference.md)**.

---

**Next:** pick your deployment lane — mesh labels ([Service Mesh](service-mesh.md)), fleet placement ([ACM](acm.md)), or Kafka plumbing ([AMQ Streams](amq-streams.md)).
