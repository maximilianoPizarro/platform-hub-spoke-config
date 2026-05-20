# Contributing Guide

Thanks for contributing to `platform-hub-spoke-config`.

This repository drives a multi-cluster platform, so changes can impact hub and spokes differently. Use this guide for safe, repeatable contributions, especially around Developer Hub, software templates, and Topology.

## Branch Model

- `main`: hub cluster configuration and shared platform services.
- `east`: east spoke profile.
- `west`: west spoke profile.

Unless you are intentionally changing a spoke-only profile, start from `main`.

## Contribution Workflow

1. Create a feature branch from the target branch.
2. Make focused changes (one concern per commit when possible).
3. Validate Helm rendering/linting before push.
4. Open PR with:
   - scope and impacted cluster(s),
   - test steps you ran,
   - rollback notes for risky changes.

## Required Validation

Run these before submitting:

```bash
helm lint .
helm template test . --set deployer.domain=apps.example.com
helm template test . -f values-east.yaml --set deployer.domain=apps.east.example.com
helm template test . -f values-west.yaml --set deployer.domain=apps.west.example.com
```

If you touched `components/developer-hub/` or templates in `docs/assets/backstage/software-templates/`, also run an end-to-end scaffold test in Developer Hub.

## Developer Hub / Scaffolder Checklist

When changing Backstage config or software templates, verify all of the following:

1. **Create flow**
   - `Fetch Skeleton` succeeds.
   - `Publish to Gitea` succeeds in `ws-<owner>` org.
   - `Register in Catalog` succeeds.

2. **Template URL and integration**
   - Catalog location uses GitHub `blob` URL for `templates-catalog.yaml`.
   - `integrations.github` includes `github.com` (plus Gitea host).
   - `backend.reading.allow` allows `github.com` and `raw.githubusercontent.com`.

3. **Catalog register path**
   - Use `catalogInfoPath: /catalog-info.yaml` (not `/main/catalog-info.yaml`).

4. **Entity tabs**
   - Both **Topology** and **Kubernetes** tabs are visible on IE entities.
   - Avoid custom topology mount overrides unless required by upstream plugin changes.

5. **Spoke visibility**
   - `backstage.io/kubernetes-cluster` annotation exists on spoke entities.
   - No 403 on spoke resources in Topology/Kubernetes views.

## Gitea Bootstrap Reliability

The `gitea-admin-setup` PostSync hook must remain recreatable on every sync:

- `argocd.argoproj.io/hook-delete-policy: BeforeHookCreation,HookSucceeded,HookFailed`

This prevents stale failed jobs from blocking org/user bootstrap (e.g. `ws-platformadmin`).

## Documentation and Skills

If behavior changes for operators/developers, update all relevant artifacts in the same PR:

- runtime docs under `docs/`,
- skills under `.cursor/skills/`,
- this `CONTRIBUTING.md` if process changed.

Keep troubleshooting notes aligned with real cluster behavior and known failure signatures.
