---
layout: default
title: OpenShift AI
parent: Red Hat Products
nav_order: 7
---

# OpenShift AI

Red Hat **OpenShift AI** operationalizes data science workloads on OpenShift: notebooks, model training pipelines, and **model serving** with scalable inference routes.

![OpenShift AI – Data Science Projects]({{ site.baseurl }}/assets/images/openshift-ia.png)
{: .mb-4 }
*OpenShift AI home — data science projects and model training workflows.*
{: .fs-2 .text-grey-dk-000 }

## Platform integration

| Concern | Notes |
| ------- | ----- |
| **DataScienceCluster** | Top-level operator CR provisioning OpenShift AI services. |
| **Model serving** | Serves scoring endpoints consumed by Industrial Edge dashboards or Kafka processors. |
| **Anomaly detection** | Example ML use case over sensor-derived features flowing through Kafka. |

Industrial Edge charts such as `industrial-edge-data-science-cluster` and `industrial-edge-data-science-project` wrap operator-managed namespaces and projects.

## Documentation

- [Red Hat OpenShift AI documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_ai/)
