---
layout: default
title: Software Templates
parent: Hybrid Mesh AI Workshop
nav_order: 3
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Software Templates


![Developer Hub software templates]({{ site.baseurl }}/assets/images/workshop/12-software-templates.png)
{: .mb-4 }

## Overview

Red Hat Developer Hub software templates encode golden paths: parameterized scaffolder actions create Git repos, register catalog entities, and trigger Argo CD Applications with guardrails (namespaces, quotas, network policies) already wired. Platform teams publish templates once; developers self-serve through the Create flow without opening infrastructure tickets.

This workshop ships templates for Industrial Edge, Camel Kaoto, API products, OpenShift AI workspaces, CNV VMs, and NeuroFace. If your `%USER_NAME%` scaffold fails due to quota or Gitea timing, switch to Plan B — Developer Hub System `hybrid-mesh-shared-demos` exposes pre-deployed Components with the same URLs and Topology entries.

Templates are the bridge between executive strategy (module 01) and spoke deployments (module 13). Inspect `docs/assets/backstage/software-templates/` and catalog ConfigMaps to see how OpenShift GitOps picks up generated repos automatically.

## Show and Tell

. Live Developer Hub Create flow for Industrial Edge template.
. Show catalog YAML source and generated Gitea repo URL pattern.
. Demonstrate Plan B fallback entity in `hybrid-mesh-shared-demos`.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Template catalog | `docs/assets/backstage/software-templates/` |
| Plan B demos | `components/workshop-demos/files/catalog/hybrid-mesh-shared-demos.yaml` |

Verify in the Showroom terminal:

```bash
oc get configmap developer-hub-catalog-demos -n developer-hub 2>/dev/null
```

## Your TODO

* [ ] Browse Developer Hub Create templates list
* [ ] Locate Plan B System `hybrid-mesh-shared-demos` as fallback
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get configmap developer-hub-catalog-demos -n developer-hub 2>/dev/null
```

