---
name: github-pages-docs
description: Jekyll + Just the Docs for platform-hub-spoke-config GitHub Pages under docs/.
---

# GitHub Pages Documentation (Just the Docs)

Use this skill when authoring or restructuring **`docs/`** static documentation published via GitHub Pages.

## Contribution policy linkage

Before finalizing docs changes, align with root `CONTRIBUTING.md`:

- run the required Helm validation commands,
- update related skills when behavior/process changes,
- include troubleshooting signatures for any new failure mode discovered during rollout.

## Stack

- **Jekyll 4.x** builds the site.
- **`jekyll-remote-theme`** pulls **Just the Docs** without vendoring the theme (`remote_theme: just-the-docs/just-the-docs` in `_config.yml`).
- Ruby gems are declared in `docs/Gemfile`.

## `_config.yml` essentials

- **`title` / `description`**: branding and SEO.
- **`url` + `baseurl`**: must match GitHub Pages URL (`baseurl` includes repo leading slash).
- **`aux_links`**: top-right shortcuts (GitHub).
- **`mermaid.version`**: pins Mermaid for diagrams.

## Just the Docs customization (this repo)

Just the Docs does **not** use `site_header_custom.html`. Valid override includes:

| File | Purpose |
| ---- | ------- |
| `_includes/title.html` | Sidebar logo — overrides theme `title.html` (renders `<img class="site-logo-img">` when `logo:` is set in `_config.yml`) |
| `_includes/nav_footer_custom.html` | Sidebar footer — author name and role only (**no** Red Hat logo) |
| `_includes/head_custom.html` | Loads `custom.css`, favicon, client-side “On this page” TOC (`site-nav-toc`) |

**Logo:** set in `_config.yml` as `logo: "/assets/images/rh-logo.svg"`. Size is controlled in CSS (`height: 32px`), not the HTML `width`/`height` attributes alone.

**Layout CSS variables** (`docs/assets/css/custom.css`):

- `--rh-sidebar-width: 264px`
- `--rh-main-padding-x: 2rem` — horizontal padding inside `.main`
- `--rh-toc-width: 11rem` — right “On this page” column

`.main` fills the area beside the sidebar (`margin-left: sidebar width`, no `max-width` on content). Content + TOC use CSS grid (`1fr` + TOC width) so there is **no** centered narrow column and no empty margin on the right. Do **not** use `align-items: center` on `.main`.

**Do not** add `site_header_custom.html` — it is ignored by Just the Docs and confuses maintainers.

`footer_content` in `_config.yml` is empty; attribution lives only in `nav_footer_custom.html`.

### Mobile / responsive rules (critical)

Sidebar layout overrides (`display: flex`, `height: 100vh`, flex-column pinning) **must** be wrapped in `@media (min-width: 50rem)`. Without this guard, the sidebar covers the full viewport on mobile and the `h1` stacks vertically into a 1000 px column.

Key mobile breakpoints:
- `< 50rem` (800px) — sidebar collapses into Just the Docs' native hamburger drawer; **do not** force `height: 100vh` or `display: flex` on `header.side-bar`
- `< 31.25rem` (500px) — true phone; sidebar footer hidden, attribution shown under content
- `≥ 66.5rem` (1064px) — desktop grid with fixed sidebar width + right-side TOC

Mobile header should have:
- `padding: 0.5rem 0.75rem` on `.site-header`
- Logo capped at `height: 24px`, `max-width: 110px`
- `header.side-bar { height: auto; overflow: visible }` below 50rem

## Existing documentation structure

```
docs/
├── _config.yml                  # url, baseurl, logo path, color_scheme: dark
├── _includes/
│   ├── title.html               # Sidebar Red Hat logo (img)
│   ├── nav_footer_custom.html   # Author footer (no logo)
│   └── head_custom.html         # custom.css + favicon + right-side TOC script
├── assets/
│   ├── css/custom.css           # Red Hat branding, layout, TOC
│   └── images/                  # Product screenshots (see table below)
├── Gemfile                      # Ruby gems
├── index.md                     # Home page (nav_order: 1)
├── architecture.md              # Platform architecture with Mermaid diagrams (nav_order: 2)
├── getting-started.md           # Prerequisites and deployment steps (nav_order: 3)
├── deploy-acm-gitops.md         # ACM + GitOps deployment guide (nav_order: 4)
├── annotations-reference.md     # Annotations & Labels Reference (nav_order: 10)
├── branch-strategy.md           # Single-branch multi-cluster strategy (nav_order: 9)
├── hub-gateway.md               # Hub gateway as F5 analog (nav_order: 6)
├── industrial-edge.md           # Industrial Edge application details (nav_order: 8)
├── observability.md             # Grafana panels, Kafka metrics, Kiali, Kafka Console (nav_order: 7)
├── service-interconnect.md      # Skupper VAN (parent: Red Hat Products, nav_order: 12)
├── products/
│   ├── index.md                 # Red Hat Products overview (has_children: true, nav_order: 5)
│   ├── acm.md                   # Advanced Cluster Management
│   ├── acs.md                   # Advanced Cluster Security
│   ├── amq-streams.md           # AMQ Streams (Kafka)
│   ├── camel-k.md               # Camel K
│   ├── connectivity-link.md     # Connectivity Link (Kuadrant)
│   ├── developer-hub.md         # Developer Hub (Backstage)
│   ├── openshift-ai.md          # OpenShift AI
│   ├── openshift-gitops.md      # OpenShift GitOps (ArgoCD)
│   ├── pipelines.md             # OpenShift Pipelines (Tekton)
│   ├── service-mesh.md          # OSSM3 3.2 GA; hero image = Kiali
└── community/
    ├── index.md                 # Community & Third-Party (has_children: true, nav_order: 6)
    ├── kubecost.md              # Kubecost cost monitoring (Red Hat certified)
    └── mailpit.md               # Mailpit SMTP testing
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

## Product screenshots (`docs/assets/images/`)

Always reference with `{{ site.baseurl }}` prefix:

```markdown
![Caption]({{ site.baseurl }}/assets/images/<file>.png)
{: .mb-4 }
*Italic caption under image.*
{: .fs-2 .text-grey-dk-000 }
```

**Click-to-zoom:** `_includes/head_custom.html` attaches a `<dialog>` lightbox to `.main-content img` (cursor `zoom-in`, keyboard activatable). Keep meaningful `alt` text — it feeds the modal.

| File | Used on |
| ---- | ------- |
| `product-kiali-service-mesh.png` | `products/service-mesh.md` (hero) |
| `product-grafana-observability.png` … `-4.png` | `observability.md` (Grafana gallery — avoid duplicating on `service-mesh.md`) |
| `connectivity-link-hub.png` | `products/connectivity-link.md` (intro) |
| `connectivity-link-hub-gateway.png` | `products/connectivity-link.md` (Hub gateway) |
| `connectivity-link-spoke.png` | `products/connectivity-link.md` (Spoke) |
| `connectivity-link-spoke-gateway.png` | `products/connectivity-link.md` (Spoke gateway) |
| `ACS.png`, `ACS-2.png` | `products/acs.md` |
| `product-kafka-console-amq-streams.png` (+ `-2`, `-3`) | `products/amq-streams.md` (Kafka Console — **not** `service-interconnect.md`; Skupper page links there) |
| `service-interconnect-console.png` | `service-interconnect.md` (Network Console — components view) |
| `service-interconnect-console-topology.png` | `service-interconnect.md` (sites topology) |
| `service-interconnect-console-topology-process.png` | `service-interconnect.md` (process topology) |
| `service-interconnect-console-process.png` | `service-interconnect.md` (process detail) |
| `service-interconnect-console-metrics.png` | `service-interconnect.md` (built-in metrics) |
| `kairos-community-logo.svg` | `community/kairos.md` (header logo — use `{: .page-brand-logo }` so `custom.css` caps at 48px; lightbox excludes this class in `head_custom.html`) |
| `kairos-ia-agents.png`, `kairos-observability.png`, `kairos-history.png`, `kairos-events.png`, `kairos-human-in-the-loop.png` | `community/kairos.md` (console gallery) |
| `ACM.png`, `product-argocd-openshift-gitops.png`, `product-developer-hub.png`, … | respective product pages |

**Operator discovery:** Each `docs/products/*.md` page includes an **Operator discovery** subsection; `products/index.md` has a summary table (annotations vs CRDs).

After adding images, verify HTTP 200 on GitHub Pages:  
`https://maximilianopizarro.github.io/platform-hub-spoke-config/assets/images/<file>.png`

## Content guidelines for this platform

When documenting platform-specific topics, include these sections where relevant:

- **What it does in this architecture** — one paragraph connecting the product to the hub-spoke pattern
- **Operator discovery** — how controllers find workloads (CRDs vs namespace labels vs explicit registrations); see `products/index.md` table for cross-links
- **How it's deployed** — GitOps-driven (ArgoCD Application), operator channel, namespace
- **Key resources created** — CRDs, ConfigMaps, Routes
- **Mermaid diagram** — architecture or flow diagrams using fenced `mermaid` blocks. Use `flowchart TB` or `flowchart LR` for architecture, `sequenceDiagram` for flows
- **Links to official docs** — always use `docs.redhat.com` URLs, not community/upstream
- **Troubleshooting notes** — known issues specific to this deployment (e.g. OOM, SCC, TLS)

**Topic routing for this repo:**
- Mesh install, ztunnel, `IstioCNI` ambient profile, **namespaces on/off ambient** → `docs/products/service-mesh.md`
- ACS Central, Helm init-bundle automation (`acs-init-bundle-sync`), manual `roxctl` fallback, **`stackrox` off mesh** → `docs/products/acs.md`
- RHDP field-content (hub + spoke orders, `clusters.hub.domain`) → `docs/rhdp-field-content.md`
- Connectivity Link screenshots and RHCL operator → `docs/products/connectivity-link.md`
- Grafana dashboards, Kafka metrics queries, Kiali 401, Kafka Console DNS/metrics → `docs/observability.md`
- Skupper, broker `advertisedHost`, EndpointSlice → `docs/service-interconnect.md` + `docs/products/amq-streams.md`
- Kubecost multicluster, federated ETL, MinIO, SCC → `docs/community/kubecost.md`
- Developer Hub OAuth, plugins, dynamic plugins → `docs/products/developer-hub.md`
- Mailpit SMTP testing → `docs/community/mailpit.md`
- Kairos labels, SmartScalingPolicy, hub mirror policies, console v2.0.3, agent tiers → `docs/community/kairos.md` (skill: **kairos-hub-spoke**)
- Developer Hub RBAC CSV, Lightspeed, OCM `/ocm`, TechDocs local builder → `docs/products/developer-hub.md`
- Quay org-setup, DevSpaces spoke-only, Gitea orgs, CNV workshop, Kafka Console → `docs/products/{quay,devspaces,gitea,cnv,kafka-console}.md`
- Namespace labels, pod selectors, annotations for feature activation → `docs/annotations-reference.md`

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

### Mobile: sidebar covers viewport / header too large

If the sidebar overlays the entire mobile screen or the page title stacks into a very tall column:
- Ensure all sidebar layout overrides (`display: flex`, `height: 100vh`, `overflow: hidden`, flex-column pinning) are inside `@media (min-width: 50rem)`.
- The only unconditional sidebar rule should be `border-top: 3px solid ...` (branding stripe).
- At `< 50rem`, set `header.side-bar { height: auto; overflow: visible }` to let Just the Docs handle the hamburger drawer.
- Logo: `height: 24px` on mobile vs `32px` on desktop.

### Layout: large empty margin on the right

- Ensure `custom.css` sets `.main { width: calc(100vw - var(--rh-sidebar-width)); align-items: center; }` and matching `body` background.
- Content max-width is intentional (`52rem` with TOC); do not use `position: fixed` TOC on the viewport edge.
- Hard-refresh after deploy (`Ctrl+Shift+R`) — GitHub Pages caches CSS.

### GitHub Actions build failures

If using GitHub Actions to build Jekyll:
- Ensure `Gemfile.lock` is committed (or add it to `.gitignore` and let the action generate it).
- Pin the Ruby version in the workflow to match the `Gemfile`.
- If the theme fails to load, check that `jekyll-remote-theme` gem version is compatible with the Jekyll version.
