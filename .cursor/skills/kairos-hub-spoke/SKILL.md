---
name: kairos-hub-spoke
description: Kairos Community operator, console image tags, hub mirror SmartScalingPolicy, and hub-only KairosConsole on ACM hub-spoke platform-hub-spoke-config.
---

# Kairos Hub-Spoke Skill

Apply when editing **`components/kairos/`**, hub `field-content-kairos` / spoke `kairos-east|west` apps, or **`docs/community/kairos.md`**.

## Deployment matrix

| `clusterRole` | Argo app (examples) | Console | Sensor scan SSP |
| ------------- | ------------------- | ------- | ----------------- |
| `hub` | `field-content-kairos` | `KairosConsole` + image tag in `values.yaml` | Mirrors only if `displayOnHub: true` |
| `spoke` | `kairos-east`, `kairos-west` | **No** console (hub URL only) | Active `scan-policy-machine-sensor-*` |

Hub overrides in `templates/component-applications.yaml`: `sensorScanPolicies.enabled: true`, `displayOnHub: true`.

## Console image and CI

- Pin: `console.image: quay.io/maximilianopizarro/kairos-console:v2.0.x` (not `:latest` in production GitOps).
- **v2.0.2+**: lists `SmartScalingPolicy` via in-cluster API (`policies_k8s.go`); requires `templates/console-rbac.yaml` ClusterRole.
- **v2.0.3**: in-cluster TLS uses service account CA; `kairos.io/display-cluster` annotation on mirror CRs.
- Upstream **Dockerfile**: build with `go build .` not `go build main.go` only (includes `policies_k8s.go`).
- Tag releases in [maximilianoPizarro/kairos](https://github.com/maximilianoPizarro/kairos); platform pins the console tag separately from OLM CSV version (e.g. CSV v2.0.1, console v2.0.3).

## Hub mirror policies (`hub-spoke-policy-display.yaml`)

Console reads SSP on the **local** cluster. Spoke policies are not federated. On hub:

- Four CRs: `{east,west}-scan-policy-machine-sensor-{1,2}`
- `spec.paused: true`, `kairos.io/display-only: "true"`, `kairos.io/display-cluster: east|west`
- Enforcement stays on spoke `sensor-scan-policies.yaml` (`paused: false`)

Disable mirrors: `sensorScanPolicies.displayOnHub: false` (hub Scaling Policies tab empty unless other SSP exist on hub).

## Operator / OLM pitfalls

- Single OperatorGroup `kairos-operator` with `targetNamespaces: [kairos-system]` — delete leftover `operator-sdk-og`.
- Argo: omit `ServerSideApply` on kairos apps if SSA + `force` conflicts (see parent helm skill).
- Secret `kairos-ai-credentials`: backup before reinstall; `ignoreDifferences` on hub.

## Console behavior (workshop)

| Feature | Hub | Spoke console (if leftover) |
| ------- | --- | --------------------------- |
| Scaling Policies | Lists hub CRs (mirrors + any local) | Lists spoke SSP only |
| Approve POST | Works on hub route | Often **404** — use hub |
| Approvals / History | Demo data in console `main.go` | Same |

ConsoleLink: `platform-kairos-console` → hub apps domain only.

## Verify

```bash
oc get smartscalingpolicy -n kairos-system -l kairos.io/policy-type=sensor-scan
oc get deployment -n kairos-system -l app=kairos-console -o jsonpath='{.items[0].spec.template.spec.containers[0].image}{"\n"}'
oc auth can-i list smartscalingpolicies --as=system:serviceaccount:kairos-system:$(oc get deploy -n kairos-system -l app=kairos-console -o jsonpath='{.items[0].spec.template.spec.serviceAccountName}')
```

## Related skills

- **developer-hub-scaffolder** — IE labels `kairos.io/managed`, environment agents
- **helm-app-of-apps** — `component-applications.yaml` hub valuesObject for kairos
- **github-pages-docs** — `docs/community/kairos.md`, logo `.page-brand-logo` 48px CSS
