---
layout: default
title: AMQ Streams
parent: Red Hat Products
nav_order: 8
---

# AMQ Streams

Red Hat **AMQ Streams** is the enterprise distribution of **Apache Kafka** on OpenShift, including operators for Kafka, KRaft mode, Kafka Connect, and **MirrorMaker 2** for geo replication.

## Industrial Edge usage

- **Sensor and MQTT-derived topics** land in Kafka via integrations (often Camel K).
- **KRaft mode** (Kafka 4.x) with `KafkaNodePool` — no ZooKeeper.
- East and west spokes each run **dev-cluster** (`industrial-edge-tst-all`) and **factory-cluster** (`industrial-edge-stormshift-messaging`).
- Topics partition workload between east and west factories while observability aggregates lag and throughput metrics.

Charts: `components/industrial-edge-tst`, `components/industrial-edge-stormshift`, `components/industrial-edge-data-lake`.

## Metrics (Grafana)

Kafka brokers expose JMX metrics via Strimzi's `jmxPrometheusExporter` ConfigMap. Scraping requires:

- **User Workload Monitoring** enabled on the cluster
- `PodMonitor` in `components/istio-monitoring` selecting `strimzi.io/name: <cluster>-kafka`

Dashboard queries use `_objectname` regex filters for Kafka 4.x KRaft JMX layout (for example `kafka_server_brokertopicmetrics_*` with `.*OneMinuteRate.*`).

## Kafka Console (hub)

The **Streams for Apache Kafka Console** (`amq-streams-console` operator) runs on the **hub** only (`components/kafka-console`). It lists four remote clusters:

| Console name | Skupper bootstrap (hub) |
| ------------ | ------------------------ |
| dev-cluster-east | `kafka-east-tst.service-interconnect.svc:9092` |
| dev-cluster-west | `kafka-west-tst.service-interconnect.svc:9092` |
| factory-cluster-east | `kafka-east-stormshift.service-interconnect.svc:9092` |
| factory-cluster-west | `kafka-west-stormshift.service-interconnect.svc:9092` |

OpenShift Console link: **Kafka Console (All Clusters)** → `https://kafka-console.<hub-domain>`.

### Broker advertised addresses

Brokers must advertise hostnames resolvable **on the hub** after metadata exchange. The platform uses:

- **Spoke** `advertisedHost`: `dev-cluster-broker-0-<east|west>.dev-cluster-kafka-brokers.industrial-edge-tst-all.svc.cluster.local`
- **Hub** `broker-dns.yaml`: **EndpointSlice** (not Endpoints — Argo CD excludes Endpoints) pointing each `advertisedHost` to the correct Skupper listener IP

Without this, the UI shows: `Timed out waiting for a node assignment` / `listNodes`.

## Documentation

- [Red Hat AMQ Streams documentation](https://docs.redhat.com/en/documentation/red_hat_amq_streams/)
- [Streams for Apache Kafka Console](https://docs.redhat.com/en/documentation/red_hat_streams_for_apache_kafka/)

Related: [Service Interconnect](../service-interconnect.md), [Observability](../observability.md).
