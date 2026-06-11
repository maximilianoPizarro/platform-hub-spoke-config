---
layout: default
title: Real Cases & Roadmap
parent: Hybrid Mesh AI Workshop
nav_order: 5
---
> **Showroom live:** `https://showroom-showroom.YOUR_HUB_DOMAIN/?USER_NAME=userN` — register: `https://workshop-registration.YOUR_HUB_DOMAIN/`

# Real Cases & Roadmap


![Customer cases and workshop roadmap]({{ site.baseurl }}/assets/images/workshop/05-cases-roadmap.png)
{: .mb-4 }

## Overview

**Industry case — precision manufacturing IoT:** A global automotive supplier deployed OpenShift at three factory edge sites plus a ROSA hub for analytics. Machine vibration sensors emit 12,000 events/minute per line; unplanned downtime cost $47,000/hour. After migrating to Industrial Edge on OpenShift with Kafka, Camel integrations, and ACS runtime policies, mean time to detect anomalies dropped from 18 minutes to 90 seconds, and Kairos-approved scaling reduced over-provisioned edge nodes by 34%.

That customer roadmap led to OpenShift AI for predictive maintenance models and Developer Hub templates so each plant could scaffold compliant pipelines without shadow IT. This workshop reproduces that journey at lab scale: modules 13–18 deploy IE on spoke east/west, modules 22–26 add MaaS and NeuroFace, module 21 adds Kubecost chargeback by namespace.

Your next step is Part B registration verification — ensure `%USER_NAME%` works in Showroom, then proceed to module 10 for ACM fleet visibility. Plan B shared demos remain available if your scaffold slot is unavailable.

### Learn more

### Learn more

* [Red Hat customer success stories](https://www.redhat.com/en/success-stories)
* [Developer Hub product page](https://developers.redhat.com/products/red-hat-developer-hub)
* [ACM product page](https://www.redhat.com/en/technologies/management/advanced-cluster-management)

## Show and Tell

. Present the automotive IoT case metrics (12k events/min, $47k/hr downtime, 34% node savings).
. Draw the customer roadmap timeline onto workshop module numbers.
. Transition room to Part B: verify `%USER_NAME%` login before module 10.

## Where this lab is defined

> Paths refer to the GitOps repo `platform-hub-spoke-config` deployed on **this** cluster. Do not copy-paste fragments as standalone manifests — use the console links above and verify with `oc`.

[cols="2,3"]
| UI / capability | Source in GitOps repo |

| Showroom | `components/showroom/` |
| Registration | `components/workshop-registration/` |

Verify in the Showroom terminal:

```bash
curl -sk -o /dev/null -w '%{http_code}' https://workshop-registration.%HUB_DOMAIN%/api/health
```

## Your TODO

* [ ] Write one metric from the manufacturing case relevant to your industry
* [ ] Confirm Showroom login as `%USER_NAME%` before module 10
* [ ] Save progress at the end of this module

## Verify

Run in the Showroom terminal:

```bash
curl -sk -o /dev/null -w '%{http_code}' https://workshop-registration.%HUB_DOMAIN%/api/health
```

