"""Curated YAML from platform-hub-spoke-config (simplified for the ebook)."""

# Hub values — GitOps entry point (values.yaml)
HUB_GITOPS = """# values.yaml (hub) — point Git at your fork
gitops:
  repoUrl: "https://github.com/YOUR-ORG/platform-hub-spoke-config"
  revision: "main"

clusters:
  hub:
    domain: "apps.hub.example.com"
  east:
    domain: "apps.east.example.com"
    # token: inject at deploy — never commit
  west:
    domain: "apps.west.example.com"

deployer:
  domain: "apps.hub.example.com"
"""

# Spoke app list — sync waves on east (east/values.yaml excerpt)
SPOKE_SYNC_WAVES = """# east/values.yaml — one list drives the whole spoke stack
clusterName: east

apps:
  - id: namespaces
    path: components/namespaces
    syncWave: "1"              # no ambient label here
  - id: operators
    path: components/operators
    syncWave: "2"
  - id: servicemeshoperator3
    path: components/servicemeshoperator3
    syncWave: "3"              # wave 2 inside chart adds ambient labels
  - id: industrial-edge-tst
    path: components/industrial-edge-tst
    destinationNamespace: industrial-edge-tst-all
    syncWave: "5"
  - id: spoke-interconnect
    path: components/spoke-interconnect
    syncWave: "6"
"""

# ACM Placement
PLACEMENT = """# components/acm-hub-spoke/templates/placement.yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Placement
metadata:
  name: hub-spoke-placement
  namespace: openshift-gitops
spec:
  clusterSets:
    - global
  predicates:
    - requiredClusterSelector:
        labelSelector:
          matchExpressions:
            - key: region
              operator: In
              values: [east, west]
"""

# ApplicationSet — fleet fan-out
APPLICATIONSET = """# components/acm-hub-spoke/templates/applicationset.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: industrial-edge-spoke
  namespace: openshift-gitops
spec:
  generators:
    - clusterDecisionResource:
        configMapRef: acm-placement
        labelSelector:
          matchLabels:
            cluster.open-cluster-management.io/placement: hub-spoke-placement
  template:
    metadata:
      name: "{{name}}-spoke-components"
    spec:
      source:
        repoURL: https://github.com/YOUR-ORG/platform-hub-spoke-config
        path: "{{name}}"          # east/ or west/
      destination:
        name: "{{name}}"
        namespace: openshift-gitops
        server: ""               # clears stale SSA server field
      syncPolicy:
        automated:
          selfHeal: true
          prune: true
"""

# OSSM3 ambient — the one field that enables ztunnel
ISTIO_CNI_AMBIENT = """# components/servicemeshoperator3 — IstioCNI (ambient)
apiVersion: sailoperator.io/v1
kind: IstioCNI
metadata:
  name: default
  namespace: istio-cni
spec:
  namespace: istio-cni
  profile: ambient                    # required for ztunnel + L4 metrics
  values:
    cni:
      ambient:
        reconcileIptablesOnStartup: true
"""

# Namespace off ambient (wave 1) — ambient labels applied in servicemeshoperator3 wave 2
NAMESPACE_OFF_MESH = """# components/namespaces — base namespaces without ambient enrollment
apiVersion: v1
kind: Namespace
metadata:
  name: stackrox
  labels:
    istio.io/dataplane-mode: none     # stay off mesh — ACS <-> PostgreSQL
---
apiVersion: v1
kind: Namespace
metadata:
  name: industrial-edge-tst-all
  # ambient label applied later by servicemeshoperator3 (sync-wave 2)
---
apiVersion: v1
kind: Namespace
metadata:
  name: industrial-edge-data-lake
  labels:
    istio.io/dataplane-mode: none     # MinIO double-TLS
"""

# Ambient enrollment after Istio + ZTunnel (servicemeshoperator3)
NAMESPACE_AMBIENT = """# components/servicemeshoperator3 — after mesh CRs are Ready
apiVersion: v1
kind: Namespace
metadata:
  name: industrial-edge-tst-all
  labels:
    istio.io/dataplane-mode: ambient
  annotations:
    argocd.argoproj.io/sync-wave: "2"
"""

# Skupper hub listener + spoke connector (pair)
SKUPPER_LISTENER = """# Hub — expose spoke gateway to the fleet (service-interconnect)
apiVersion: skupper.io/v2alpha1
kind: Listener
metadata:
  name: ie-gateway-east
  namespace: service-interconnect
spec:
  routingKey: ie-gateway-east
  host: ie-gateway-east
  port: 8080
"""

SKUPPER_CONNECTOR = """# Spoke east — announce local gateway to the VAN
apiVersion: skupper.io/v2alpha1
kind: Connector
metadata:
  name: ie-gateway-east
  namespace: service-interconnect
spec:
  routingKey: ie-gateway-east
  host: spoke-gateway-istio.spoke-gateway-system.svc.cluster.local
  port: 8080
"""

# Camel K — red thread stages 1-2
CAMEL_MQTT_TO_KAFKA = """# components/industrial-edge-tst — mqtt-to-kafka Integration
apiVersion: camel.apache.org/v1
kind: Integration
metadata:
  name: mqtt-to-kafka
  namespace: industrial-edge-tst-all
spec:
  flows:
    - route:
        id: mqtt-temperature
        from:
          uri: "paho:iot-sensor/sw/temperature?brokerUrl=tcp://messaging...:1883"
        steps:
          - to:
              uri: "kafka:temperature?brokers=dev-cluster-kafka-bootstrap...:9092"
"""

# Kafka topic + single-broker pool
KAFKA_TOPIC = """# Temperature topic — one CR, GitOps-managed
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: temperature
  namespace: industrial-edge-tst-all
  labels:
    strimzi.io/cluster: dev-cluster
spec:
  partitions: 1
  replicas: 1
"""

# Hub Gateway + weighted route
HUB_GATEWAY = """# components/hub-gateway — Gateway API on the hub
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: hub-gateway
  namespace: hub-gateway-system
spec:
  gatewayClassName: istio
  listeners:
    - name: http
      port: 8080
      protocol: HTTP
"""

HTTPROUTE_WEIGHTS = """# Weighted east/west — change weights with one helm upgrade
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: industrial-edge-lb
  namespace: hub-gateway-system
spec:
  parentRefs:
    - name: hub-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: industrial-edge-east-api
          port: 8080
          weight: 100
        - name: industrial-edge-west-api
          port: 8080
          weight: 0
    - backendRefs:
        - name: industrial-edge-east-front
          port: 8080
          weight: 50
        - name: industrial-edge-west-front
          port: 8080
          weight: 50
"""

DESTINATION_RULE_CB = """# Circuit breaking per spoke backend (hub-gateway-system)
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: cb-industrial-edge-east-front
  namespace: hub-gateway-system
spec:
  host: industrial-edge-east-front.hub-gateway-system.svc.cluster.local
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 3
      baseEjectionTime: 30s
      maxEjectionPercent: 100
"""

# Helm gateway weights — no YAML edit for maintenance
HELM_GATEWAY_WEIGHTS = """# Drain east during maintenance — values only
hub:
  gateway:
    weights:
      east: 0
      west: 100
    apiWeights:
      east: 0
      west: 100
"""

# UWM enable
UWM_CONFIG = """# Enable application metrics on every cluster
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-monitoring-config
  namespace: openshift-monitoring
data:
  config.yaml: |
    enableUserWorkload: true
"""

# ManagedCluster labels for new spoke
MANAGED_CLUSTER_LABELS = """# After ACM import — labels drive Placement + ApplicationSet
apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: south
  labels:
    region: south
    cluster.open-cluster-management.io/clusterset: global
"""
