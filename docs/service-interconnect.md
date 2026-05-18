---
layout: default
title: Service Interconnect
nav_order: 10
---

# Service Interconnect (Skupper)

**Red Hat Service Interconnect** creates a Virtual Application Network (VAN) that connects services across clusters without requiring VPN tunnels, direct network routes, or firewall changes. In this platform, Skupper bridges spoke Industrial Edge services and Prometheus metrics to the hub for centralized observability.

## Architecture

```mermaid
flowchart TB
  subgraph Hub["Hub Cluster"]
    direction TB
    SITE_H["Skupper Site (hub)<br/>namespace: service-interconnect"]
    AG["AccessGrant<br/>(spoke-link)"]
    L_GW_E["Listener: ie-gateway-east<br/>port 8080"]
    L_GW_W["Listener: ie-gateway-west<br/>port 8080"]
    L_PM_E["Listener: prometheus-east<br/>port 9091"]
    L_PM_W["Listener: prometheus-west<br/>port 9091"]
    L_K_E["Listener: kafka-east-tst<br/>port 9092"]
    L_K_W["Listener: kafka-west-tst<br/>port 9092"]
    GRAFANA["Grafana Datasources"]
    KAFKA_C["Kafka Console"]
    L_PM_E -->|"svc.cluster.local"| GRAFANA
    L_PM_W -->|"svc.cluster.local"| GRAFANA
  end

  subgraph East["East Spoke"]
    SITE_E["Skupper Site (east)"]
    TOKEN_E["AccessToken<br/>(hub-token)"]
    CONN_GW_E["Connector:<br/>ie-gateway-east"]
    CONN_PM_E["Connector:<br/>prometheus-east"]
    CONN_K_E["Connector:<br/>kafka-east-tst"]
    SGW_E["Spoke Gateway<br/>:8080"]
    TQ_E["Thanos Querier<br/>:9091"]
    KAFKA_E["Kafka bootstrap<br/>:9092"]
    SGW_E --> CONN_GW_E
    TQ_E --> CONN_PM_E
    KAFKA_E --> CONN_K_E
  end

  subgraph West["West Spoke"]
    SITE_W["Skupper Site (west)"]
    TOKEN_W["AccessToken<br/>(hub-token)"]
    CONN_GW_W["Connector:<br/>ie-gateway-west"]
    CONN_PM_W["Connector:<br/>prometheus-west"]
    CONN_K_W["Connector:<br/>kafka-west-tst"]
    SGW_W["Spoke Gateway<br/>:8080"]
    TQ_W["Thanos Querier<br/>:9091"]
    KAFKA_W["Kafka bootstrap<br/>:9092"]
    SGW_W --> CONN_GW_W
    TQ_W --> CONN_PM_W
    KAFKA_W --> CONN_K_W
  end

  AG -.->|"redeem"| TOKEN_E
  AG -.->|"redeem"| TOKEN_W
  TOKEN_E -->|"TLS link"| SITE_H
  TOKEN_W -->|"TLS link"| SITE_H
  CONN_GW_E ===|"VAN"| L_GW_E
  CONN_PM_E ===|"VAN"| L_PM_E
  CONN_GW_W ===|"VAN"| L_GW_W
  CONN_PM_W ===|"VAN"| L_PM_W
  CONN_K_E ===|"VAN"| L_K_E
  CONN_K_W ===|"VAN"| L_K_W
  L_K_E --> KAFKA_C
  L_K_W --> KAFKA_C
```

## Link establishment flow

The Skupper link between spoke and hub requires an **AccessToken** that is created from the hub's **AccessGrant**:

```mermaid
sequenceDiagram
  participant Hub as Hub (AccessGrant)
  participant GrantSrv as Grant Server (HTTPS)
  participant Spoke as Spoke (AccessToken)
  participant Router as Skupper Router

  Hub->>GrantSrv: Create AccessGrant → generates URL + code
  Note over Hub: AccessGrant status.url + status.code + status.ca
  Spoke->>GrantSrv: Redeem token (ca + code + url)
  GrantSrv-->>Spoke: TLS credentials
  Spoke->>Spoke: Create Link with TLS credentials
  Spoke->>Router: Establish inter-router connection
  Router-->>Hub: VAN link active
  Note over Hub,Spoke: Connectors ↔ Listeners now bridged
```

## Components

### Hub (`components/service-interconnect`)

| Resource | Purpose |
| -------- | ------- |
| `Site/hub` | Declares the hub as a Skupper site |
| `AccessGrant/spoke-link` | Generates claim tokens for spoke connections |
| `Listener/ie-gateway-east` | Receives spoke-gateway traffic from east |
| `Listener/ie-gateway-west` | Receives spoke-gateway traffic from west |
| `Listener/prometheus-east` | Receives Prometheus metrics from east |
| `Listener/prometheus-west` | Receives Prometheus metrics from west |
| `Listener/kafka-east-tst` | Kafka bootstrap (dev-cluster) from east |
| `Listener/kafka-west-tst` | Kafka bootstrap (dev-cluster) from west |
| `Listener/kafka-east-stormshift` | Kafka bootstrap (factory-cluster) from east |
| `Listener/kafka-west-stormshift` | Kafka bootstrap (factory-cluster) from west |

### Spoke (`components/spoke-interconnect`)

| Resource | Purpose |
| -------- | ------- |
| `Namespace/service-interconnect` | Skupper workspace |
| `Site/<clusterName>` | Declares the spoke as a Skupper site |
| `Connector/ie-gateway-<cluster>` | Exposes local spoke-gateway to hub |
| `Connector/prometheus-<cluster>` | Exposes auth proxy → Thanos Querier to hub |
| `Connector/kafka-<cluster>-tst` | Exposes `dev-cluster-kafka-bootstrap` to hub |
| `Connector/kafka-<cluster>-stormshift` | Exposes `factory-cluster-kafka-bootstrap` to hub |

The `AccessToken` is created manually via `ManagedClusterAction` since it contains sensitive claim data that should not be stored in Git.

## Kafka Console and broker DNS

Skupper forwards **TCP** to Kafka bootstrap (`:9092`) correctly. The Kafka client then receives **broker metadata** with spoke-internal hostnames (for example `dev-cluster-broker-0.dev-cluster-kafka-brokers.industrial-edge-tst-all.svc`), which do not resolve on the hub.

**Resolution pattern:**

1. **Spokes** — set per-broker `advertisedHost` in Strimzi with a unique suffix per cluster (`dev-cluster-broker-0-east`, `dev-cluster-broker-0-west`, …).
2. **Hub** — `components/kafka-console/templates/broker-dns.yaml` creates headless Services and **`EndpointSlice`** resources mapping those hostnames to Skupper listener ClusterIPs (Helm `lookup` per broker IP — avoid nested lookups in slice `addresses`).

Argo CD excludes **`Endpoints`** from sync; EndpointSlice is the supported GitOps pattern for broker DNS on the hub.

After deploying Skupper listeners, sync the `kafka-console` application so EndpointSlices are populated. See [Observability](observability.md#kafka-console-hub).

## Spoke gateway aggregation

Rather than exposing each Industrial Edge service individually, each spoke runs a **Gateway API gateway** (`components/spoke-gateway`) that aggregates all services behind a single entry point. Skupper exposes only this gateway to the hub.

```mermaid
flowchart LR
  subgraph Spoke["Spoke Cluster"]
    GW["spoke-gateway<br/>(Istio Gateway)"]
    FE["line-dashboard"]
    AD["anomaly-detection"]
    MSG["messaging"]
    KB["kafka-bootstrap"]
    GW --> FE
    GW --> AD
    GW --> MSG
    GW --> KB
  end

  CONN["Skupper Connector"] --> GW
  CONN -->|"VAN"| LIST["Hub Listener<br/>ie-gateway-*"]
```

## Operator deployment

The `skupper-operator` subscription is deployed to spokes via the `operators` component in the ApplicationSet `valuesObject`. This ensures the CRDs are available before Skupper CRs are applied.

## References

- [Red Hat Service Interconnect 2.1](https://docs.redhat.com/en/documentation/red_hat_service_interconnect/2.1)
- [Skupper v2 API](https://skupper.io/docs/)

Charts: `components/service-interconnect` (hub), `components/spoke-interconnect` (spokes), `components/spoke-gateway` (spokes).
