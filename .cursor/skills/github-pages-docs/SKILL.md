---
name: github-pages-docs
description: Jekyll + Just the Docs for platform-hub-spoke-config GitHub Pages under docs/.
---

# GitHub Pages Documentation (Just the Docs)

Use this skill when authoring or restructuring **`docs/`** static documentation published via GitHub Pages.

## Stack

- **Jekyll 4.x** builds the site.
- **`jekyll-remote-theme`** pulls **Just the Docs** without vendoring the theme (`remote_theme: just-the-docs/just-the-docs` in `_config.yml`).
- Ruby gems are declared in `docs/Gemfile`.

## `_config.yml` essentials

- **`title` / `description`**: branding and SEO.
- **`url` + `baseurl`**: must match GitHub Pages URL (`baseurl` includes repo leading slash).
- **`aux_links`**: top-right shortcuts (GitHub).
- **`mermaid.version`**: pins Mermaid for diagrams.

## Existing documentation structure

```
docs/
├── _config.yml                  # Jekyll configuration
├── _includes/
│   └── head_custom.html         # Custom CSS + favicon
├── assets/
│   └── css/custom.css           # Red Hat design overrides
├── Gemfile                      # Ruby gems
├── index.md                     # Home page (nav_order: 1)
├── architecture.md              # Platform architecture with Mermaid diagrams (nav_order: 2)
├── getting-started.md           # Prerequisites and deployment steps (nav_order: 3)
├── deploy-acm-gitops.md         # ACM + GitOps deployment guide (nav_order: 4)
├── branch-strategy.md           # Single-branch multi-cluster strategy (nav_order: 9)
├── hub-gateway.md               # Hub gateway as F5 analog (nav_order: 6)
├── industrial-edge.md           # Industrial Edge application details (nav_order: 8)
    ├── observability.md             # Grafana panels, Kafka metrics, Kiali, Kafka Console (nav_order: 7)
    ├── service-interconnect.md      # Skupper: metrics, gateways, Kafka (nav_order: 10)
└── products/
    ├── index.md                 # Red Hat Products overview (has_children: true, nav_order: 5)
    ├── acm.md                   # Advanced Cluster Management
    ├── acs.md                   # Advanced Cluster Security
    ├── amq-streams.md           # AMQ Streams (Kafka)
    ├── camel-k.md               # Camel K
    ├── connectivity-link.md     # Connectivity Link (Kuadrant)
    ├── developer-hub.md         # Developer Hub (Backstage)
    ├── mailpit.md               # Mailpit SMTP testing
    ├── openshift-ai.md          # OpenShift AI
    ├── openshift-gitops.md      # OpenShift GitOps (ArgoCD)
    ├── pipelines.md             # OpenShift Pipelines (Tekton)
    └── service-mesh.md          # OSSM3 3.2 GA ambient, IstioCNI profile, ztunnel troubleshooting
```

## Front matter conventions

Every page should set:

```yaml
---
layout: default
title: Page Title
nav_order: <integer>
---
```

**Child pages** under a section:

```yaml
---
layout: default
title: Child Page
parent: Exact Parent Title   # must match parent's title string
nav_order: 1                 # order among siblings
---
```

Section roots use **`has_children: true`** (see `docs/products/index.md`).

## Adding product pages

1. Create `docs/products/<slug>.md`.
2. Set `parent: Red Hat Products` (matches `docs/products/index.md` title).
3. Assign **`nav_order`** unique among siblings.
4. Link from `docs/products/index.md` overview table.

## Adding architecture/guide pages

1. Create `docs/<slug>.md` at the root level.
2. Set `nav_order` to position it in the sidebar navigation.
3. For topics that need sub-pages, add `has_children: true` and create child pages with `parent: <title>`.

## Mermaid diagrams

Use fenced blocks:

````markdown
```mermaid
flowchart LR
  A --> B
```
````

Ensure `_config.yml` includes the `mermaid` key; Just the Docs renders Mermaid client-side.

## Local preview

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Browse `http://localhost:4000/platform-hub-spoke-config/` (prepend `baseurl`).

## GitHub Pages deployment

Configure the repository **Pages** settings to publish from the **`/docs`** folder on `main` (or `gh-pages` if your org requires). The built HTML outputs to `_site` locally only; GitHub Actions may build remotely—native Pages builds Jekyll when compatible gems exist.

## Red Hat product page template

```markdown
---
layout: default
title: Product Display Name
parent: Red Hat Products
nav_order: N
---

# Product Display Name

## Role in this platform
...

## Deployment / Operator notes
...

## Documentation
- [Product docs](https://docs.redhat.com/...)
```

Keep links authoritative (`docs.redhat.com`, upstream operators). Prefer short actionable paragraphs over marketing copy.

## Content guidelines for this platform

When documenting platform-specific topics, include these sections where relevant:

- **What it does in this architecture** — one paragraph connecting the product to the hub-spoke pattern
- **How it's deployed** — GitOps-driven (ArgoCD Application), operator channel, namespace
- **Key resources created** — CRDs, ConfigMaps, Routes
- **Mermaid diagram** — architecture or flow diagrams using fenced `mermaid` blocks. Use `flowchart TB` or `flowchart LR` for architecture, `sequenceDiagram` for flows
- **Links to official docs** — always use `docs.redhat.com` URLs, not community/upstream
- **Troubleshooting notes** — known issues specific to this deployment (e.g. OOM, SCC, TLS)

**Topic routing for this repo:**
- Mesh install, ztunnel, `IstioCNI` ambient profile → `docs/products/service-mesh.md`
- Grafana dashboards, Kafka metrics queries, Kiali 401, Kafka Console DNS/metrics → `docs/observability.md`
- Skupper, broker `advertisedHost`, EndpointSlice → `docs/service-interconnect.md` + `docs/products/amq-streams.md`
- Kubecost multicluster, federated ETL, MinIO, SCC → `docs/products/kubecost.md` (new)
- Developer Hub OAuth, plugins, dynamic plugins → `docs/products/developer-hub.md`

### Diagram conventions

- Use `subgraph` blocks to group resources by cluster (Hub, East, West)
- Label nodes with role and port/namespace when relevant
- Use `-->` for data flow, `-.->` for claim/bootstrap, `===` for VAN/network links
- Keep diagrams focused — one concern per diagram (architecture, data flow, sync flow)

---

## Troubleshooting

### Styles missing on GitHub Pages

If the site deploys but has no CSS:
- Verify `baseurl` in `_config.yml` matches exactly `/<repo-name>` (case-sensitive).
- Ensure `remote_theme: just-the-docs/just-the-docs` is set (not a local theme path).
- Check that `jekyll-remote-theme` is listed in `plugins:` array in `_config.yml` and in the `Gemfile`.
- All internal links must use `{{ site.baseurl }}` prefix or relative paths — absolute paths break under the repo subdirectory.

### Broken internal links

Just the Docs links between pages using the navigation hierarchy. If a parent/child relationship breaks:
- Verify `parent:` in child front matter exactly matches the parent page's `title:`.
- Verify `has_children: true` is set on the parent page.
- Use `nav_order` to control ordering; gaps in numbering are fine.

### GitHub Actions build failures

If using GitHub Actions to build Jekyll:
- Ensure `Gemfile.lock` is committed (or add it to `.gitignore` and let the action generate it).
- Pin the Ruby version in the workflow to match the `Gemfile`.
- If the theme fails to load, check that `jekyll-remote-theme` gem version is compatible with the Jekyll version.
