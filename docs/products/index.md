---
layout: default
title: Red Hat Products
nav_order: 5
has_children: true
---

# Red Hat Products

This platform composes multiple Red Hat operators and patterns. Use the child pages for installation notes, CRDs, and documentation links.

## Overview

| Product | Role in platform | Git path |
| ------- | ----------------- | -------- |
| [Advanced Cluster Management](acm.md) | Fleet lifecycle, policy, placement, GitOps integration | `components/acm-hub-spoke/` |
| [Developer Hub](developer-hub.md) | Internal developer portal (Backstage) | `components/developer-hub/` |
| [Advanced Cluster Security](acs.md) | Vulnerability management, runtime risk | `components/acs-secured-cluster/` |
| [OpenShift GitOps](openshift-gitops.md) | Declarative continuous delivery (Argo CD) | `components/openshift-gitops/` |
| [OpenShift Service Mesh 3](service-mesh.md) | Ambient mesh, ztunnel, waypoints | `components/servicemeshoperator3/` |
| [Connectivity Link](connectivity-link.md) | Kuadrant + Gateway API policies | `components/connectivity-link/` |
| [Service Interconnect](../service-interconnect.md) | Skupper VAN for cross-cluster connectivity | `components/service-interconnect/` |
| [OpenShift AI](openshift-ai.md) | DataScienceCluster, model serving | `components/openshift-ai/` |
| [AMQ Streams](amq-streams.md) | Kafka for telemetry pipelines | `components/industrial-edge-*/` |
| [Apache Camel / Camel K](camel-k.md) | Integrations (MQTT, S3, Kafka) | `components/camel-k/` |
| [OpenShift Pipelines](pipelines.md) | Tekton CI/CD for Industrial Edge | `components/industrial-edge-pipelines/` |
