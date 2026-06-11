---
layout: default
title: OpenShift GitOps
parent: Hybrid Mesh AI Workshop
nav_order: 7
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# OpenShift GitOps


![OpenShift GitOps and Argo CD]({{ site.baseurl }}/assets/images/workshop/16-openshift-gitops.png)
{: .mb-4 }

## Overview

OpenShift GitOps installs Argo CD as a managed operator and integrates with ACM ApplicationSets to propagate manifests hub-to-spoke. The **App-of-Apps** pattern in `templates/component-applications.yaml` is the single entry point: one Application per component, each with its own sync-wave, ignoreDifferences, and Helm valuesObject. Platform teams commit desired state to Git; controllers reconcile drift automatically.

*The App-of-Apps template* iterates `.Values.connectivityLink.apps` and generates one Application per component. Notice the key patterns:

[source,yaml]
----
# templates/component-applications.yaml (simplified)
{{- range .Values.connectivityLink.apps }}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ $.Release.Name }}-{{ .id }}
  namespace: openshift-gitops
  labels:
    app.kubernetes.io/part-of: platform-hub-spoke
  annotations:
    argocd.argoproj.io/sync-wave: {{ .syncWave | quote }}     # controls deployment order
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: {{ $.Values.gitops.repoUrl }}
    targetRevision: {{ $.Values.gitops.revision }}
    path: components/{{ .path }}                               # each component in its own dir
  destination:
    server: https://kubernetes.default.svc
    namespace: {{ .destinationNamespace }}
  syncPolicy:
    automated:
      prune: {{ .prune }}
      selfHeal: {{ .selfHeal }}         # drift is auto-corrected
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
      - RespectIgnoreDifferences=true   # prevents flip-flop on operator-managed fields
{{- end }}
----

*Why `ignoreDifferences` matters:* Operators and controllers mutate fields that would cause perpetual OutOfSync. The template includes a comprehensive list — here are the critical ones:

[source,yaml]
----
# templates/component-applications.yaml — ignoreDifferences (excerpt)
ignoreDifferences:
  - kind: Service
    jsonPointers: [/spec/clusterIP, /spec/clusterIPs]
  - group: route.openshift.io
    kind: Route
    jsonPointers: [/spec/host, /status]
  - kind: Secret
    jsonPointers: [/data]                   # never drift-check secret values
  - group: sailoperator.io
    kind: Istio
    jsonPointers: [/spec/profile, /status]  # sail operator rewrites profile
  - group: rhdh.redhat.com
    kind: Backstage
    jsonPointers:                            # RHDH operator shrinks spec after sync
      - /spec/application/appConfig/configMaps
      - /spec/application/extraFiles
  - group: cluster.open-cluster-management.io
    kind: "*"
    jsonPointers: [/metadata/annotations, /metadata/labels, /status]
----

*Helm valuesObject per component:* Instead of static `values.yaml`, the template injects cluster-specific values inline. For example, `acm-hub-spoke` receives spoke API URLs and tokens:

[source,yaml]
----
# templates/component-applications.yaml — valuesObject for acm-hub-spoke
    helm:
      valuesObject:
        clusterDomain: {{ $domain }}
        managedClusters:
          east:
            apiUrl: {{ $.Values.clusters.east.apiUrl }}
            domain: {{ $eastDomain }}
          west:
            apiUrl: {{ $.Values.clusters.west.apiUrl }}
            domain: {{ $westDomain }}
----

Verify GitOps health from the Showroom terminal:

[source,bash]
----
# List all hub Applications and their sync status
oc get applications -n openshift-gitops -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status

# Check ApplicationSet for spoke propagation
oc get applicationsets -n openshift-gitops

# See which components are deployed and their sync waves
oc get applications -n openshift-gitops -o jsonpath='{range .items[*]}{.metadata.name}{" wave="}{.metadata.annotations.argocd\.argoproj\.io/sync-wave}{"\n"}{end}'
----

See link:https://docs.redhat.com/en/documentation/red_hat_openshift_gitops[OpenShift GitOps documentation] for ApplicationSet patterns.

### Learn more

### Learn more

* [OpenShift GitOps documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops)
* [Argo CD documentation](https://argo-cd.readthedocs.io/)
* [ACM GitOps overview](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.14/html/gitops/gitops-overview)

## Features, benefits & cloud configuration

## Features, benefits & cloud configuration

### Key features

* **Argo CD** on hub deploys hub and spoke components via ApplicationSet + Placements.
* Sync waves order operators before workloads (see `templates/component-applications.yaml`).
* `%USER_NAME%` changes flow: Gitea PR → Argo sync → live cluster.

### Business benefits

* Auditable drift detection — every factory config in Git.
* ACM placement targets east/west without duplicate Application CRs per cluster.

### AWS — CodePipeline deploy to ROSA

```bash
aws codebuild create-project --name gitops-sync --source type=GITHUB,location=org/platform-hub-spoke-config
aws codepipeline create-pipeline --cli-input-json file://gitops-pipeline.json
# Lab: OpenShift GitOps pulls directly from Gitea/GitHub
```

### Azure — DevOps pipeline

```bash
az pipelines create --name gitops-sync --repository platform-hub-spoke-config   --repository-type tfsgit --branch main --yaml-path azure-pipelines.yml
```

## Show and Tell

. Argo CD UI: hub Application vs user spoke Application sources.
. Highlight ApplicationSet generator for east/west matrix.
. Show sync wave or health status for IE app.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Hub Applications | `templates/component-applications.yaml` |
| ApplicationSet IE | `components/acm-hub-spoke/templates/applicationset.yaml` |

Verify in the Showroom terminal:

```bash
oc get applications -n openshift-gitops 2>/dev/null | head -10
```

## Your TODO

* [ ] Find your IE Application in Argo CD and note sync status
* [ ] Identify Git repo source (user Gitea vs hub platform repo)
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
oc get applications -n openshift-gitops 2>/dev/null | head -10
```

