# Platform releases (OpenShift 4.20)

Release notes live in this directory only — they are **not** published on [GitHub Pages](https://maximilianopizarro.github.io/platform-hub-spoke-config/) (see `docs/` for the site).

| Tag | Document |
|-----|----------|
| `ocp-420-v4` | [OCP 4.20 — v4](OCP-4.20-v4.md) — current; Camel Dashboard on spokes |
| `ocp-420-v3` | [OCP 4.20 — v3](OCP-4.20-v3.md) — Skupper tokens, Kafka/Kiali, IE routes |
| `ocp-420-v2` | RHDH Topology + Scaffolder (tag only; no notes file) |
| `ocp-420` | Initial OCP 4.20 baseline (tag only) |

Pin GitOps: set `targetRevision` on hub/spoke Argo CD Applications to the tag (e.g. `ocp-420-v4`).
