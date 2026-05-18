---
layout: default
title: Connectivity Link
parent: Red Hat Products
nav_order: 6
---

# Connectivity Link

**Connectivity Link** brings multi-cluster ingress and policy using **Kubernetes Gateway API** with **Kuadrant**-family controllers for DNS, TLS, rate limiting, and auth patterns.

![Connectivity Link – Policy Topology]({{ site.baseurl }}/assets/images/connectivity-link-hub.png)
{: .mb-4 }
*Gateway API policy topology — hub-gateway, HTTPRoute, and route rules in OpenShift Console.*
{: .fs-2 .text-grey-dk-000 }

## In this platform

- Gateway API `Gateway` and `HTTPRoute` objects align with **hub gateway** style routing (including weighted splits similar to hardware ADC behavior).
- **Policies may be disabled initially** to reduce rollout friction; enable Kuadrant `AuthPolicy`, `RateLimitPolicy`, and DNS TLS strategies as you harden environments.

## Links

- [Connectivity Link documentation](https://docs.redhat.com/en/documentation/red_hat_connectivity_link/)
- [Kuadrant documentation](https://docs.kuadrant.io/)
- [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/)

Chart path: `components/rhcl-operator`.
