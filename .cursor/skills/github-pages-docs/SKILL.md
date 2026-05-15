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
