---
layout: default
title: AMQ Streams
parent: Red Hat Products
nav_order: 8
---

# AMQ Streams

Red Hat **AMQ Streams** is the enterprise distribution of **Apache Kafka** on OpenShift, including operators for Kafka, ZooKeeper (where applicable), Kafka Connect, and **MirrorMaker 2** for geo replication.

## Industrial Edge usage

- **Sensor and MQTT-derived topics** land in Kafka via integrations (often Camel K).
- **MirrorMaker 2** can replicate topics toward a hub data lake when architectural boundaries require it.
- Topics partition workload between east and west factories while observability aggregates lag and throughput metrics.

## Documentation

- [Red Hat AMQ Streams documentation](https://docs.redhat.com/en/documentation/red_hat_amq_streams/)

Topics and brokers are provisioned through Industrial Edge component charts (for example `industrial-edge-tst`, `industrial-edge-stormshift`, data lake charts).
