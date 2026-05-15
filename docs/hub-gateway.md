---
layout: default
title: Hub Gateway
nav_order: 6
---

# Hub Gateway

The **hub gateway** pattern provides centralized HTTP ingress on the hub cluster with behaviors similar to an **F5 BIG-IP ADC**: VIP-style routing, TLS termination at the edge, and **weighted traffic splits** across backend services or spoke-derived routes.

## Gateway API theory

Kubernetes **Gateway API** separates concerns:

- **`Gateway`** — listens on addresses and ports; attaches TLS and listener policies.
- **`HTTPRoute`** — attaches to a `Gateway` and selects backend `Service` resources with matches, filters, and weighted backends.

Weighted rules enable **canary** or **active-active** distributions between service versions or regions when paired with mesh or multi-cluster DNS strategies.

## Relationship to Connectivity Link

Connectivity Link (Kuadrant) layers DNS automation, TLS policies, and advanced controls atop Gateway API. Start with plain HTTPRoutes if you need incremental adoption; enable Kuadrant policies when teams are ready.

## Operational notes

- Keep **hostnames aligned** with `deployer.domain` and corporate DNS wildcard records.
- Combine with **Service Mesh ambient** when east-west encryption between gateway hops and workloads matters.

## References

- [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/)
- [Connectivity Link documentation](https://docs.redhat.com/en/documentation/red_hat_connectivity_link/)

Implementation chart: `components/hub-gateway`.
