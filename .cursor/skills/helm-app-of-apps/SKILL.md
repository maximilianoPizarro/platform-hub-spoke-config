---
name: helm-app-of-apps
description: Create and extend App-of-Apps Helm charts like platform-hub-spoke-config (components, values, sync waves, testing).
---

# Helm App-of-Apps (platform-hub-spoke-config)

Use this skill when editing the **parent Helm chart** that renders Argo CD `Application` objects for each component under `components/`.

## Pattern overview

1. **Parent chart** (`Chart.yaml` + `templates/`) loops `connectivityLink.apps[]` and emits one **Application** per enabled entry (`templates/component-applications.yaml`).
2. Each **child chart** lives in `components/<name>/` with its own `Chart.yaml` and manifests.
3. Git remains the source of truth; Argo CD syncs the child chart path referenced by each Application `spec.source.path`.

## Adding a new component

1. Scaffold `components/<component-id>/` with a valid Helm chart (`Chart.yaml`, `templates/`).
2. Append an entry to **`connectivityLink.apps[]`** in the appropriate values file (`values.yaml`, `values-east.yaml`, …):

   - **`id`**: stable identifier used in Argo CD Application name (`Release.Name-id`).
   - **`path`**: directory under `components/` (matches chart folder name unless customized).
   - **`destinationNamespace`**: target namespace on the spoke/hub.
   - **`syncWave`**: string annotation `argocd.argoproj.io/sync-wave` controlling ordering.
   - **`enabled`**: toggle rendering without deleting the list entry.

3. If the component needs operator subscriptions, extend **`connectivityLink.operators.subscriptions`** with OLM `Subscription` metadata (namespace, channel, catalog source).

## Connectivity Link apps array

`connectivityLink.apps[]` is the **single manifest** of which Applications exist. Keep IDs unique. Prefer disabling with `enabled: false` over deleting rows when temporarily turning off workloads—preserves history and diff clarity.

## ignoreDifferences best practices

The parent template ships defaults for OpenShift realities:

- **`Route`**: ignore `/spec/host`, `/spec/wildcardPolicy`, `/status` so Argo does not fight DNS/router-assigned hosts.
- **`Service` cluster IPs**: immutable fields assigned by the platform.
- **`Deployment`**: optional ignoring of injected annotations (operators, mesh).

When adding CRDs that reconcile status heavily (Service Mesh, Kafka), consider targeted `ignoreDifferences` on status-only noise—but **never** ignore fields that encode desired state you intend Git to own.

## syncWave ordering convention

Use waves consistently across the fleet:

| Wave | Purpose |
| ---- | -------- |
| **0** | GitOps bootstrap (`openshift-gitops`) |
| **1** | Namespaces and foundational RBAC |
| **2** | Shared operators subscriptions baseline |
| **3** | Platform operators (mesh, ACM, ACS central, Developer Hub) |
| **4** | ACM hub-spoke GitOps bindings |
| **5** | Observability operators / Industrial Edge foundations |
| **6** | Apps, integrations, Connectivity Link operator |
| **7** | Hub gateway and higher-layer routing |
| **8** | Grafana dashboards and presentation-layer resources |

Keep dependent workloads **strictly greater** than their prerequisites.

## Externalizing deployer.domain

Never hardcode cluster-specific URLs in templates. Pass **`deployer.domain`** (and `clusters.*.domain` when needed) via Helm values or `--set` flags so the same chart renders for hub, east, and west.

CI should run:

```bash
helm template test-release . -f values.yaml --set deployer.domain=apps.example.com
```

## Testing checklist

- `helm lint .` at repo root.
- `helm lint components/<chart>/` per changed component.
- `helm template` with **each** profile: `values.yaml`, `values-east.yaml`, `values-west.yaml`, optional `values-lite.yaml`.

## Profile management with values-lite.yaml

`values-lite.yaml` trims heavy subscriptions and disables optional Applications while preserving bootstrap (`openshift-gitops`, `namespaces`, `operators`, `servicemeshoperator3`) and **`industrial-edge-tst`**. Use it for labs, CI subsets, or constrained clusters—merge lessons back into full profiles when promoting features.
