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

## Cross-cluster routing architecture

The hub gateway routes traffic to spoke cluster OpenShift Routes via `ExternalName` services:

```
Browser → Hub OpenShift Router (HTTPS) → Istio Gateway (port 8080) → ExternalName Service → Spoke OpenShift Router (HTTP port 80) → Backend Pod
```

### Key requirements

1. **HTTP port 80, not HTTPS** — Istio ambient mode gateways do not apply `DestinationRule` TLS settings. Using HTTPS causes `CERTIFICATE_VERIFY_FAILED` errors. Spoke Routes must set `insecureEdgeTerminationPolicy: Allow`.

2. **ServiceEntry for each external host** — without a `ServiceEntry`, Envoy has no cluster definition for the external hostname and returns HTTP 500.

3. **Per-backend Host header rewrite** — the spoke OpenShift router routes by `Host` header. Use `RequestHeaderModifier` filters on each `backendRef` in the HTTPRoute.

4. **Session affinity for Socket.IO** — when load-balancing across multiple backends, Socket.IO polling and WebSocket upgrade must reach the same backend. Split the HTTPRoute into:
   - `/api` prefix → pinned to single backend (session affinity)
   - Everything else → weighted across east/west (load-balanced static content)

## Relationship to Connectivity Link

Connectivity Link (Kuadrant) layers DNS automation, TLS policies, and advanced controls atop Gateway API. Start with plain HTTPRoutes if you need incremental adoption; enable Kuadrant policies when teams are ready.

## IoT Dashboard integration

The Industrial Edge `line-dashboard` (iot-frontend) requires an `iot-consumer` sidecar to display sensor data:

- **iot-consumer** bridges MQTT → WebSocket via Socket.IO
- Mount a ConfigMap `config.json` with `websocketHost: ""` (empty = same origin)
- Path-based Route `/api` → port 3000 (iot-consumer)
- The hub gateway proxies `/api` requests to the correct spoke backend where iot-consumer handles the Socket.IO connection

## Operational notes

- Keep **hostnames aligned** with `deployer.domain` and corporate DNS wildcard records.
- Combine with **Service Mesh ambient** when east-west encryption between gateway hops and workloads matters.
- Monitor the gateway Envoy proxy metrics at port 15020 `/stats/prometheus`.

## References

- [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/)
- [Connectivity Link documentation](https://docs.redhat.com/en/documentation/red_hat_connectivity_link/)

Implementation chart: `components/hub-gateway`.
