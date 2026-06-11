"""Extended module sections: features, benefits, AWS/Azure configuration procedures."""
from __future__ import annotations

# slug -> lang -> AsciiDoc body (subsections use === / ====)
MODULE_EXTENDED: dict[str, dict[str, str]] = {
    "index": {
        "en": """
=== Key capabilities in this lab

* Hub-spoke fleet managed by ACM with east/west spokes for Industrial Edge and user-scoped workloads.
* Ambient service mesh, Skupper interconnect, Gateway API ingress, and Kuadrant API governance on the hub.
* OpenShift AI + MaaS, AI Gateway, MCP Gateway, NeuroFace, and Developer Hub golden paths.
* GitOps-first delivery via OpenShift GitOps; observability via Prometheus, Grafana, and distributed tracing.

=== Business benefits

* One platform narrative for executives (Part A) and operators (Part B) — no slide-only vs lab-only split.
* Patterns portable to ROSA, on-prem, and Azure Red Hat OpenShift without rewriting applications.
* `%USER_NAME%`-scoped namespaces demonstrate multi-tenant factory onboarding at scale.

=== Hybrid cloud setup — reference procedures

==== AWS — ROSA hub + edge import

[source,bash]
----
# Install ROSA CLI and create fleet hub (replace with your account)
rosa create cluster --cluster-name=hybrid-hub --region=us-east-1 --compute-machine-type=m5.4xlarge
rosa create cluster --cluster-name=factory-east --region=us-east-1 --private-link

# Import spoke to ACM hub (after kubeconfig for hub)
oc login https://api.hybrid-hub.<domain>:6443
rosa download kubeconfig --cluster=factory-east -o east-kubeconfig
# ACM console: Infrastructure → Clusters → Import cluster → paste east kubeconfig

# OIDC for external secrets / S3 data lake analog
aws iam create-open-id-connect-provider \
  --url https://oidc.eks.us-east-1.amazonaws.com/id/EXAMPLE \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 9e99a48a9960b14926bb7f2b02d22dab16c8f9c9
aws s3 mb s3://hybrid-mesh-data-lake --region us-east-1
----

==== Azure — ARO hub + AKS edge

[source,bash]
----
az group create --name rg-hybrid-workshop --location eastus
az aro create --resource-group rg-hybrid-workshop --name hybrid-hub --version 4.16
az aks create --resource-group rg-hybrid-workshop --name factory-east --node-count 3 --network-plugin azure

# Import AKS to ACM (ManagedCluster CR or ACM import wizard)
az aks get-credentials --resource-group rg-hybrid-workshop --name factory-east
# On hub: create ManagedCluster + Klusterlet bootstrap per ACM docs
----
""",
        "es": """
=== Capacidades clave en este lab

* Flota hub-spoke con ACM y spokes east/west para Industrial Edge y cargas por usuario.
* Service mesh ambient, Skupper, Gateway API, gobernanza Kuadrant en el hub.
* OpenShift AI + MaaS, AI Gateway, MCP Gateway, NeuroFace y golden paths Developer Hub.

=== Beneficios de negocio

* Una narrativa para ejecutivos (Parte A) y operadores (Parte B).
* Patrones portables a ROSA, on-prem y Azure Red Hat OpenShift.

=== Configuración nube híbrida

==== AWS — ROSA hub + import edge

[source,bash]
----
rosa create cluster --cluster-name=hybrid-hub --region=us-east-1
rosa create cluster --cluster-name=factory-east --region=us-east-1
# Importar spoke en ACM desde consola hub
aws s3 mb s3://hybrid-mesh-data-lake --region us-east-1
----

==== Azure — ARO + AKS

[source,bash]
----
az aro create --resource-group rg-hybrid-workshop --name hybrid-hub --version 4.16
az aks create --resource-group rg-hybrid-workshop --name factory-east --node-count 3
----
""",
    },
    "hybrid-cloud-strategy": {
        "en": """
=== Key features

* Workload placement framework: edge for latency, cloud for burst, hub for governance.
* Unified OpenShift API across ROSA, bare metal, and edge — operators learn once.
* ACM policy engine for fleet-wide compliance without per-cluster kubectl scripts.

=== Business benefits

* Avoid double replatforming when AI or analytics moves from cloud to edge.
* Faster plant onboarding: `%USER_NAME%` mirrors how squads get isolated namespaces and catalog entries.
* Executive KPI alignment: security, automation, FinOps, and AI on one roadmap.

=== AWS configuration — ROSA fleet anchor

[source,bash]
----
# Tag ROSA clusters for FinOps chargeback (module 21)
aws ec2 create-tags --resources i-0123456789abcdef0 \
  --tags Key=kubernetes.io/cluster/factory-east,Value=owned Key=cost-center,Value=plant-01

# Cost and usage report bucket for Kubecost/AWS integration
aws s3 mb s3://rosa-cur-export
aws cur put-report-definition --report-definition file://cur-definition.json
----

=== Azure configuration — policy at scale

[source,bash]
----
az policy assignment create --name require-aro-tags \
  --policy SetDefinition --params '{"tagName":{"value":"cost-center"}}'
az monitor log-analytics workspace create --resource-group rg-hybrid-workshop --name hybrid-ops
----
""",
        "es": """
=== Características clave

* Marco de ubicación de cargas: edge por latencia, cloud por burst, hub por gobernanza.
* API OpenShift unificada en ROSA, bare metal y edge.

=== Beneficios

* Evita replatformear dos veces cuando la IA se mueve cloud → edge.
* Onboarding de plantas más rápido con namespaces `%USER_NAME%`.

=== AWS — ROSA

[source,bash]
----
aws ec2 create-tags --resources i-EXAMPLE --tags Key=cost-center,Value=plant-01
----

=== Azure

[source,bash]
----
az monitor log-analytics workspace create --resource-group rg-hybrid-workshop --name hybrid-ops
----
""",
    },
    "rosa-architecture": {
        "en": """
=== Key features

* Managed control plane (Red Hat SRE) with customer-owned worker MachineSets.
* STS/IAM integration for pod identity to AWS services without long-lived keys.
* PrivateLink and VPC isolation patterns for factory connectivity.

=== Business benefits

* Predictable upgrades and CVE response on control plane while you control worker sizing.
* Same ACM/GitOps/AI modules as on-prem — skills transfer directly to ROSA spokes.

=== AWS — ROSA cluster lifecycle

[source,bash]
----
rosa verify permissions
rosa create account-roles --mode auto
rosa create cluster --cluster-name=workshop-hub \
  --region=us-east-1 --multi-az --replicas=3 \
  --compute-machine-type=m5.4xlarge --version 4.16.12

rosa describe cluster --cluster=workshop-hub
rosa create idp --cluster=workshop-hub --type htpasswd --name workshop-users \
  --username admin --password 'ChangeMe123!'

# Worker autoscaling (analog to module 14 Kairos recommendations)
aws autoscaling put-scaling-policy --auto-scaling-group-name rosa-worker-asg \
  --policy-name scale-on-cpu --policy-type TargetTrackingScaling \
  --target-tracking-configuration file://cpu-target.json
----

=== Azure — compare with ARO

[source,bash]
----
az aro create --resource-group rg-workshop --name workshop-hub \
  --version 4.16 --worker-count 3 --master-vm-size Standard_D8s_v3
az aro list --output table
----
""",
        "es": """
=== Características ROSA

* Plano de control gestionado; workers bajo tu cuenta AWS.
* Integración STS/IAM para identidad de pods.

=== AWS — ciclo de vida ROSA

[source,bash]
----
rosa create cluster --cluster-name=workshop-hub --region=us-east-1 --multi-az
rosa create idp --cluster=workshop-hub --type htpasswd --name workshop-users
----
""",
    },
    "security-scale-hybrid": {
        "en": """
=== Key features

* ACS Central for image/runtime policy across hub and spokes.
* OVN-Kubernetes NetworkPolicies on spokes; mesh ambient on app namespaces.
* Kuadrant rate limits at hub ingress before traffic reaches OT backends.

=== Business benefits

* Detect supply-chain and runtime threats without agents blocking mesh dataplane.
* Scale sensor ingestion with Kafka + HPA while policy stays centralized in ACM.

=== AWS — security services alignment

[source,bash]
----
# GuardDuty + ROSA (runtime signals complement ACS)
aws guardduty create-detector --enable
# PrivateLink endpoint for ROSA API (factory networks)
aws ec2 create-vpc-endpoint --vpc-id vpc-xxx --service-name com.amazonaws.us-east-1.sts

# Security group rules for worker nodes (analog to NP module 19)
aws ec2 authorize-security-group-ingress --group-id sg-workers \
  --protocol tcp --port 443 --cidr 10.0.0.0/8
----

=== Azure — Defender + AKS

[source,bash]
----
az security pricing create --name VirtualMachines --tier Standard
az aks update --resource-group rg-workshop --name factory-east --enable-defender
az network nsg rule create --resource-group rg-workshop --nsg-name aks-nsg \
  --name allow-hub --priority 100 --destination-port-ranges 443 --access Allow
----
""",
        "es": """
=== Características

* ACS Central para política de imagen/runtime en hub y spokes.
* NetworkPolicies OVN en spokes; mesh ambient en apps.

=== AWS

[source,bash]
----
aws guardduty create-detector --enable
aws ec2 create-vpc-endpoint --vpc-id vpc-xxx --service-name com.amazonaws.us-east-1.sts
----
""",
    },
    "aws-ai-integration": {
        "en": """
=== Key features

* OpenShift AI DataScienceCluster with ModelMesh/KServe on hub.
* MaaS shared LLM endpoint — portable alternative to Bedrock/SageMaker lock-in.
* IAM OIDC patterns for optional AWS model service calls from OpenShift projects.

=== Business benefits

* Keep inference on-cluster for data residency; call Bedrock only when policy allows.
* One MaaS URL for Developer Hub Lightspeed, notebooks, and NeuroFace chat.

=== AWS — Bedrock + ROSA workload identity

[source,bash]
----
# Enable Bedrock model access (console or CLI)
aws bedrock put-model-invocation-logging-configuration \
  --logging-config cloudWatchConfig={logGroupName=/bedrock/invocations}

# IRSA-style trust for OpenShift service account (conceptual — use cluster OIDC issuer)
aws iam create-role --role-name rosa-ai-invoke-bedrock \
  --assume-role-policy-document file://trust-openshift-oidc.json
aws iam attach-role-policy --role-name rosa-ai-invoke-bedrock \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

# Invoke (compare with lab MaaS curl in module 23)
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-3-sonnet-20240229-v1:0 \
  --body file://prompt.json --cli-binary-format raw-in-base64-out out.json
----

=== Azure — OpenAI alternative

[source,bash]
----
az cognitiveservices account create --name hybrid-openai --resource-group rg-workshop \
  --kind OpenAI --sku S0 --location eastus
az cognitiveservices account deployment create --name hybrid-openai \
  --resource-group rg-workshop --deployment-name gpt-4o --model-name gpt-4o --model-version "2024-05-13"
# Lab uses OpenShift AI MaaS instead — same consumer app pattern
----
""",
        "es": """
=== Características

* OpenShift AI con ModelMesh/KServe en hub.
* MaaS como alternativa portable a Bedrock/SageMaker.

=== AWS — Bedrock

[source,bash]
----
aws bedrock-runtime invoke-model --model-id anthropic.claude-3-sonnet-20240229-v1:0 \
  --body file://prompt.json --cli-binary-format raw-in-base64-out out.json
----

=== Azure OpenAI

[source,bash]
----
az cognitiveservices account create --name hybrid-openai --resource-group rg-workshop --kind OpenAI --sku S0
----
""",
    },
    "ai-end-user-apps": {
        "en": """
=== Key features

* **line-dashboard** — live Kafka sensor visualization on east spoke for operators.
* **ie-anomaly-alerter** — statistical/predictive alerts surfaced in the plant UX.
* **Camel K** integrations (`demo-camel-kaoto-east`, `demo-camel-cdc-east`) — event-driven OT/IT bridges.
* **NeuroFace + MaaS** — contextual AI help embedded in end-user flows, not only notebooks.

=== Business benefits

* Operators act on AI insights in the same dashboard they use for line status — no context switching.
* Platform teams publish catalog dependencies once; each plant binds AI services via Developer Hub.
* `%USER_NAME%` capstone proves multi-tenant factory rollout without shadow IT pipelines.

=== AWS — stream plant events to cloud analytics

[source,bash]
----
# Mirror Kafka topics to Kinesis (optional hybrid analytics)
aws kinesis create-stream --stream-name plant-sensors --shard-count 2
# MSK cluster for ROSA-adjacent streaming
aws kafka create-cluster --cluster-name factory-msk \
  --broker-node-group-info file://broker-nodes.json \
  --kafka-version 3.5.1

# SNS mobile push for operator alerts (analog to anomaly → notification)
aws sns create-topic --name plant-anomaly-alerts
aws sns subscribe --topic-arn arn:aws:sns:us-east-1:123456789012:plant-anomaly-alerts \
  --protocol email --notification-endpoint ops@factory.example.com
----

=== Azure — Event Hubs + IoT

[source,bash]
----
az eventhubs namespace create --resource-group rg-workshop --name plant-events --sku Standard
az eventhubs eventhub create --resource-group rg-workshop --namespace-name plant-events --name sensors
az iot hub create --resource-group rg-workshop --name plant-iot --sku S1

# Route IE anomaly events (conceptual CDC pattern from Camel demo)
az eventhubs eventhub consumer-group create --resource-group rg-workshop \
  --namespace-name plant-events --eventhub-name sensors --name line-dashboard
----

=== Lab hands-on sequence

. Open link:https://industrial-edge.%HUB_DOMAIN%[Industrial Edge line-dashboard] — confirm live metrics.
. Developer Hub → catalog components for `%USER_NAME%` IE namespace and Grafana dashboards.
. Trigger anomaly threshold or review ie-anomaly-alerter logs: `oc logs -l app=ie-anomaly-alerter -n industrial-edge-tst-all --tail=20`.
. Optional: embed link:https://neuroface.%HUB_DOMAIN%[NeuroFace] for operator AI assist.
""",
        "es": """
=== Características

* **line-dashboard** — visualización Kafka en vivo en spoke east.
* **ie-anomaly-alerter** — alertas predictivas en UX de planta.
* **Camel K** — integraciones event-driven OT/IT.
* **NeuroFace + MaaS** — IA contextual en flujos finales.

=== Beneficios

* Operadores actúan sobre insights IA en el mismo dashboard de línea.
* Equipos de plataforma publican dependencias de catálogo una vez.

=== AWS

[source,bash]
----
aws kinesis create-stream --stream-name plant-sensors --shard-count 2
aws sns create-topic --name plant-anomaly-alerts
----

=== Azure

[source,bash]
----
az eventhubs namespace create --resource-group rg-workshop --name plant-events --sku Standard
az iot hub create --resource-group rg-workshop --name plant-iot --sku S1
----
""",
    },
    "openshift-ai": {
        "en": """
=== Key features

* **DataScienceCluster** (`default-dsc`) — ModelMesh, KServe, dashboard, notebooks.
* Per-user project **`ai-%USER_NAME%`** with `workshop-notebook` and InferenceService `workshop-sklearn`.
* MaaS playground in `maas-workshop` — shared LLM for all AI modules.

=== Business benefits

* Data scientists and developers share one governed inference layer.
* Notebooks and pipelines stay on-cluster — no export of factory data to public SaaS.

=== AWS — SageMaker vs OpenShift AI

[source,bash]
----
# SageMaker endpoint (cloud alternative — lab uses OpenShift AI instead)
aws sagemaker create-model --model-name sklearn-factory --primary-container \
  Image=246618743249.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3,ModelDataUrl=s3://models/sklearn.tar.gz
aws sagemaker create-endpoint-config --endpoint-config-name sklearn-cfg \
  --production-variants VariantName=AllTraffic,ModelName=sklearn-factory,InitialInstanceCount=1,InstanceType=ml.m5.large
aws sagemaker create-endpoint --endpoint-name sklearn-factory --endpoint-config-name sklearn-cfg
----

=== Azure — ML workspace

[source,bash]
----
az ml workspace create --resource-group rg-workshop --name factory-ml
az ml online-deployment create --name sklearn-deploy --model sklearn:1 --workspace-name factory-ml
----
""",
        "es": """
=== Características

* **DataScienceCluster** con ModelMesh, notebooks y MaaS.
* Proyecto **`ai-%USER_NAME%`** con notebook y modelos.

=== AWS SageMaker (alternativa cloud)

[source,bash]
----
aws sagemaker create-endpoint --endpoint-name sklearn-factory --endpoint-config-name sklearn-cfg
----
""",
    },
    "ai-gateway": {
        "en": """
=== Key features

* **Gateway API HTTPRoute** on hub with Istio ingress.
* **Kuadrant AuthPolicy** + **TokenRateLimitPolicy** — API keys per workshop user.
* Public hostname **`workshop-apis.%HUB_DOMAIN%`** routing `/llm` to MaaS backend.

=== Business benefits

* Factory apps get stable external API with auth — no shared cluster-internal URLs.
* Rate limits protect MaaS from runaway OT scripts or misconfigured loops.

=== AWS — API Gateway + ROSA analogy

[source,bash]
----
aws apigateway create-rest-api --name factory-llm-gateway
# Map to private integration (NLB → OpenShift route) — lab uses Kuadrant instead
aws apigateway create-deployment --rest-api-id abc123 --stage-name prod

# WAF rate limit (compare Kuadrant TokenRateLimitPolicy)
aws wafv2 create-web-acl --name llm-rate-limit --scope REGIONAL \
  --default-action Allow={} --rules file://rate-limit-rules.json
----

=== Azure — API Management

[source,bash]
----
az apim create --resource-group rg-workshop --name factory-apim --publisher-name Hybrid --publisher-email admin@example.com
az apim api create --resource-group rg-workshop --service-name factory-apim \
  --api-id maas-llm --path llm --display-name "MaaS LLM"
az apim product create --resource-group rg-workshop --service-name factory-apim \
  --product-id plant-tier --product-name "Plant API tier" --subscription-required true
----
""",
        "es": """
=== Características

* **HTTPRoute** Gateway API + Kuadrant en hub.
* API keys por usuario en **`workshop-apis.%HUB_DOMAIN%`**.

=== AWS API Gateway

[source,bash]
----
aws apigateway create-rest-api --name factory-llm-gateway
aws wafv2 create-web-acl --name llm-rate-limit --scope REGIONAL --default-action Allow={}
----
""",
    },
    "acm-multicluster": {
        "en": """
=== Key features

* **ManagedCluster** import for east/west spokes without sharing kube-admin broadly.
* **Placement** and **GitOpsCluster** — deploy apps to selected clusters from hub.
* OCM APIs power Developer Hub Topology multicluster view.

=== Business benefits

* Single pane for fleet health — critical for 10+ factory edge sites.
* Policy violations visible before they reach production OT networks.

=== AWS — ROSA spoke registration

[source,bash]
----
# On spoke ROSA cluster — bootstrap klusterlet (ACM auto-import flow)
# Hub: oc get managedclusters
rosa list clusters
aws eks update-cluster-config --name factory-east --resources-vpc-config endpointPublicAccess=false

# Hub credentials for import (use ACM console Import cluster wizard)
oc get secret -n open-cluster-management hub-kubeconfig-secret -o yaml
----

=== Azure — AKS attach

[source,bash]
----
az aks get-credentials --resource-group rg-workshop --name factory-east
# ACM: Clusters → Import → paste kubeconfig / auto import
az aks update --resource-group rg-workshop --name factory-east --enable-aad --aad-admin-group-object-ids <guid>
----
""",
        "es": """
=== Características

* Import **ManagedCluster** para spokes east/west.
* APIs OCM en Topology Developer Hub.

=== AWS

[source,bash]
----
rosa list clusters
oc get managedclusters
----
""",
    },
    "hybrid-mesh-architecture": {
        "en": """
=== Key features

* **Skupper** service interconnect — encrypted app networks without VPN mesh complexity.
* **Gateway API HTTPRoute** on hub terminates north-south traffic.
* Industrial Edge frontends on spokes reached through logical mesh.

=== Business benefits

* No flat VPC peering between every plant and cloud hub.
* Same OpenShift Routes and policies whether underlay is AWS, Azure, or MPLS.

=== AWS — ALB + PrivateLink to ROSA

[source,bash]
----
aws elbv2 create-load-balancer --name hybrid-ingress --type application --subnets subnet-a subnet-b
aws ec2 create-vpc-endpoint --vpc-id vpc-hub --service-name com.amazonaws.us-east-1.s3
# Skupper analog: private connectivity to spoke services without public kube API
----

=== Azure — Application Gateway

[source,bash]
----
az network application-gateway create --resource-group rg-workshop --name hybrid-appgw \
  --capacity 2 --sku Standard_v2 --public-ip-address hybrid-pip
----
""",
        "es": """
=== Características

* **Skupper** + **HTTPRoute** hub → spokes IE.

=== AWS ALB

[source,bash]
----
aws elbv2 create-load-balancer --name hybrid-ingress --type application --subnets subnet-a subnet-b
----
""",
    },
    "deploy-industrial-edge": {
        "en": """
=== Key features

* **Industrial Edge** stack — line dashboard, Kafka, Camel, ML inference at the edge.
* Deployed on **east spoke** via ACM placement and GitOps.
* Plan B demo `demo-industrial-edge-east` if scaffolder unavailable.

=== Business benefits

* Process sensor data locally; sync summaries to hub for AI and FinOps.
* Reduces cloud egress costs for high-frequency OT telemetry.

=== AWS — IoT Greengrass / edge ROSA

[source,bash]
----
aws greengrassv2 create-component-version --inline-recipe file://line-recipe.yaml
aws iot thing create --thing-name line-01-edge
# ROSA single-node compact cluster at edge (3-node minimum production)
rosa create cluster --cluster-name=line-01 --region=us-east-1 --compute-machine-type=m5.xlarge
----

=== Azure — IoT Edge on AKS

[source,bash]
----
az iot edge set-modules --device-id line-01 --hub-name plant-iot --content file://deployment.json
az aks nodepool add --resource-group rg-workshop --cluster-name factory-east --name edgepool --node-count 2
----
""",
        "es": """
=== Características

* Stack **Industrial Edge** en spoke east — dashboard, Kafka, Camel.

=== AWS IoT

[source,bash]
----
aws iot thing create --thing-name line-01-edge
----
""",
    },
    "acs-kuadrant": {
        "en": """
=== Key features

* **ACS Central** — vulnerability and runtime policy for containers across fleet.
* **Kuadrant** — API keys, AuthPolicy, rate limits on `workshop-apis` routes.
* Developer Hub Kuadrant plugin for self-service key minting.

=== Business benefits

* Security and API governance on one OpenShift footprint — no separate API gateway appliance.
* `%USER_NAME%` keys isolate usage for chargeback and audit.

=== AWS — WAF + Secrets Manager

[source,bash]
----
aws secretsmanager create-secret --name kuadrant-api-keys --secret-string '{"user1":"..."}'
aws wafv2 associate-web-acl --web-acl-arn arn:aws:wafv2:... --resource-arn arn:aws:elasticloadbalancing:...
----

=== Azure — Key Vault + Front Door

[source,bash]
----
az keyvault secret set --vault-name hybrid-kv --name kuadrant-user1 --value <api-key>
az network front-door waf-policy create --resource-group rg-workshop --name api-waf --sku Premium_AzureFrontDoor
----
""",
        "es": """
=== Características

* **ACS Central** + **Kuadrant** API keys en hub.

=== AWS

[source,bash]
----
aws secretsmanager create-secret --name kuadrant-api-keys --secret-string '{}'
----
""",
    },
    "finops-kubecost": {
        "en": """
=== Key features

* **Kubecost** primary on hub with agents on east/west spokes.
* Namespace-level allocation for `%USER_NAME%` and IE workloads.
* Correlates with Kairos right-sizing recommendations (module 14).

=== Business benefits

* CFO-ready chargeback without spreadsheet exports from each cluster.
* Identify idle capacity before buying more edge hardware.

=== AWS — Cost Explorer + ROSA tags

[source,bash]
----
aws ce get-cost-and-usage --time-period Start=2026-01-01,End=2026-02-01 \
  --granularity MONTHLY --metrics BlendedCost \
  --group-by Type=TAG,Key=kubernetes.io/cluster/factory-east
aws cur put-report-definition --report-definition file://rosa-cur.json
----

=== Azure — Cost Management

[source,bash]
----
az consumption usage list --start-date 2026-01-01 --end-date 2026-02-01
az costmanagement export create --scope subscriptions/<sub-id> --name kubecost-sync \
  --storage-account hybridcost --storage-container exports --timeframe MonthToDate
----
""",
        "es": """
=== Características

* **Kubecost** hub + agentes spokes; asignación por namespace.

=== AWS Cost Explorer

[source,bash]
----
aws ce get-cost-and-usage --time-period Start=2026-01-01,End=2026-02-01 --granularity MONTHLY --metrics BlendedCost
----
""",
    },
    "neuroface": {
        "en": """
=== Key features

* **OVMS** local vision inference for webcam latency-sensitive detection.
* **MaaS chat** at `/api/chat` for operator Q&A.
* Catalog entity **neuroface-workshop** links UI, routes, and OpenShift AI.

=== Business benefits

* Vision at edge; generative answers from governed hub MaaS — split latency/cost optimally.
* Demo of multimodal AI in factory safety and training scenarios.

=== AWS — Rekognition + Bedrock combo

[source,bash]
----
aws rekognition create-collection --collection-id factory-faces
aws rekognition index-faces --collection-id factory-faces --image '{"S3Object":{"Bucket":"photos","Name":"worker.jpg"}}'

aws bedrock-runtime invoke-model --model-id anthropic.claude-3-haiku-20240307-v1:0 \
  --body file://chat.json --cli-binary-format raw-in-base64-out chat-out.json
# Lab: OVMS + MaaS on OpenShift instead
----

=== Azure — Vision + OpenAI

[source,bash]
----
az cognitiveservices account create --name factory-vision --kind ComputerVision --resource-group rg-workshop --sku S1
az cognitiveservices account create --name factory-openai --kind OpenAI --resource-group rg-workshop --sku S0
----
""",
        "es": """
=== Características

* **OVMS** visión local + chat **MaaS** en NeuroFace.

=== AWS Rekognition + Bedrock

[source,bash]
----
aws rekognition create-collection --collection-id factory-faces
----
""",
    },
    "mcp-gateway": {
        "en": """
=== Key features

* **MCP Gateway** — Kuadrant CRDs, ArgoCD MCP, k8s MCP tools.
* **Developer Hub Lightspeed** invokes tools via `remote::mcp`.
* Public URL `https://mcp-gateway.%HUB_DOMAIN%/mcp`.

=== Business benefits

* Developers ask natural-language questions that trigger safe, scoped automation.
* Same MCP pattern for OpenShift AI assistant servers (module 22).

=== AWS — Lambda tools (contrast)

[source,bash]
----
aws lambda create-function --function-name list-argocd-apps \
  --runtime python3.12 --handler app.handler --role arn:aws:iam::123456789012:role/lambda-basic \
  --zip-file fileb://function.zip
# MCP Gateway on OpenShift replaces ad-hoc Lambda glue for K8s operations
----

=== Azure — Functions

[source,bash]
----
az functionapp create --resource-group rg-workshop --name hybrid-tools --storage-account hybridstore \
  --consumption-plan-location eastus --runtime python --functions-version 4
----
""",
        "es": """
=== Características

* **MCP Gateway** + Lightspeed en Developer Hub.

=== AWS Lambda (contraste)

[source,bash]
----
aws lambda create-function --function-name list-argocd-apps --runtime python3.12 --handler app.handler --role arn:aws:iam::123:role/lambda-basic --zip-file fileb://function.zip
----
""",
    },
    "llm-rag": {
        "en": """
=== Key features

* **Lightspeed** in Developer Hub for catalog-aware prompts.
* **RAG** pattern: vector store + OpenShift AI inference (lab uses MaaS endpoint).
* **Continue AI** in DevSpaces for inline code suggestions.

=== Business benefits

* Factory runbooks and SOPs ground LLM answers — fewer hallucinations on the shop floor.
* Same MaaS backend as NeuroFace and AI Gateway — unified governance.

=== AWS — Bedrock Knowledge Bases

[source,bash]
----
aws bedrock-agent create-knowledge-base --name factory-sops \
  --role-arn arn:aws:iam::123456789012:role/BedrockKBRole \
  --knowledge-base-configuration file://kb-config.json
aws bedrock-agent ingest-knowledge-base-documents --knowledge-base-id KB123 \
  --documents file://sops.pdf
----

=== Azure — AI Search + OpenAI

[source,bash]
----
az search service create --name factory-search --resource-group rg-workshop --sku basic
az cognitiveservices account deployment create --name hybrid-openai --resource-group rg-workshop \
  --deployment-name embeddings --model-name text-embedding-ada-002
----
""",
        "es": """
=== Características

* **Lightspeed** + RAG con MaaS en OpenShift AI.

=== AWS Bedrock Knowledge Bases

[source,bash]
----
aws bedrock-agent create-knowledge-base --name factory-sops --role-arn arn:aws:iam::123:role/BedrockKBRole --knowledge-base-configuration file://kb-config.json
----
""",
    },
    "cases-roadmap": {
        "en": """
=== Key features

* Customer journey map from edge IoT → hub analytics → OpenShift AI → FinOps.
* Plan B **hybrid-mesh-shared-demos** for rooms without scaffolder capacity.
* Module numbering ties executive story to hands-on checkpoints.

=== Business benefits

* Stakeholders see ROI metrics (downtime $, detection time, node savings) before deep technical labs.
* Roadmap reduces "pilot purgatory" — each module is a production milestone.

=== AWS — landing zone alignment

[source,bash]
----
# Organize ROSA accounts per plant (Control Tower / Organizations)
aws organizations create-account --email plant-01@example.com --account-name factory-east
aws servicecatalog provision-product --product-id prod-rosa-spoke --provisioned-product-name plant-01
----

=== Azure — enterprise scale

[source,bash]
----
az account create --enrollment-account-name hybrid --offer-type MS-AZR-0017P
az deployment sub create --location eastus --template-file landing-zone.json
----
""",
        "es": """
=== Características

* Mapa de viaje cliente IoT edge → hub → OpenShift AI → FinOps.
* Demos Plan B **hybrid-mesh-shared-demos**.

=== AWS Organizations

[source,bash]
----
aws organizations create-account --email plant-01@example.com --account-name factory-east
----
""",
    },
    "software-templates": {
        "en": """
=== Key features

* Backstage **Software Templates** in Developer Hub Create flow.
* Parameters: namespace, quota, Git repo, Argo CD Application, catalog registration.
* Templates under `docs/assets/backstage/software-templates/`.

=== Business benefits

* Cut onboarding from weeks to minutes with guardrails baked in.
* `%USER_NAME%` scaffold creates auditable GitOps path per developer.

=== AWS — CodeCommit + ROSA CI

[source,bash]
----
aws codecommit create-repository --repository-name ie-app-user1
aws codepipeline create-pipeline --cli-input-json file://pipeline.json
# Lab uses Gitea + OpenShift GitOps instead
----

=== Azure — DevOps + ARO

[source,bash]
----
az devops project create --name hybrid-platform --organization https://dev.azure.com/myorg
az repos create --name ie-app-user1 --project hybrid-platform
----
""",
        "es": """
=== Características

* **Software Templates** en Developer Hub con GitOps y catálogo.

=== AWS CodeCommit

[source,bash]
----
aws codecommit create-repository --repository-name ie-app-user1
----
""",
    },
    "kairos-scaling": {
        "en": """
=== Key features

* **SmartScalingPolicy** CRs recommend node/workload sizing.
* **Kairos Console** agent answers scaling questions in natural language.
* Correlates with HPA (module 18) and Kubecost (module 21).

=== Business benefits

* Human-in-the-loop approval before edge node changes — safe for OT environments.
* Data-driven rightsizing reduces cloud and hardware spend.

=== AWS — Cluster Autoscaler on ROSA

[source,bash]
----
# ROSA machine pools scale workers
rosa edit machinepool --cluster=workshop-hub --machinepool=worker --replicas=5
aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[?contains(Tags[?Key==`rosa`].Value, `workshop-hub`)]'
----

=== Azure — AKS cluster autoscaler

[source,bash]
----
az aks update --resource-group rg-workshop --name factory-east --enable-cluster-autoscaler \
  --min-count 2 --max-count 10
az aks nodepool update --resource-group rg-workshop --cluster-name factory-east \
  --name nodepool1 --enable-cluster-autoscaler --min-count 2 --max-count 8
----
""",
        "es": """
=== Características

* **SmartScalingPolicy** + consola Kairos para recomendaciones.

=== AWS ROSA machine pools

[source,bash]
----
rosa edit machinepool --cluster=workshop-hub --machinepool=worker --replicas=5
----
""",
    },
    "observability": {
        "en": """
=== Key features

* **Prometheus** federation hub ← spokes; **Grafana** dashboards for `%USER_NAME%`.
* **Tempo/Jaeger** distributed tracing across mesh and IE services.
* **Kiali** service graph for ambient mesh (module 17).

=== Business benefits

* Mean time to resolution drops when traces link IE Kafka lag to specific pods.
* Single Grafana entry for executives and SREs.

=== AWS — CloudWatch + ROSA

[source,bash]
----
aws logs create-log-group --log-group-name /rosa/workshop-hub/application
aws cloudwatch put-metric-alarm --alarm-name kafka-lag-high \
  --metric-name EstimatedLag --namespace AWS/Kafka --threshold 10000 \
  --comparison-operator GreaterThanThreshold --evaluation-periods 2 --period 300
----

=== Azure — Monitor + Container Insights

[source,bash]
----
az monitor diagnostic-settings create --name aks-logs --resource /subscriptions/.../factory-east \
  --workspace hybrid-ops --logs '[{"category":"kube-audit","enabled":true}]'
az monitor metrics alert create --name kafka-lag --resource-group rg-workshop \
  --scopes <resource-id> --condition "avg Percentage CPU > 80" --window-size 5m
----
""",
        "es": """
=== Características

* **Prometheus** + **Grafana** + tracing distribuido.

=== AWS CloudWatch

[source,bash]
----
aws logs create-log-group --log-group-name /rosa/workshop-hub/application
----
""",
    },
    "openshift-gitops": {
        "en": """
=== Key features

* **Argo CD** on hub deploys hub and spoke components via ApplicationSet + Placements.
* Sync waves order operators before workloads (see `templates/component-applications.yaml`).
* `%USER_NAME%` changes flow: Gitea PR → Argo sync → live cluster.

=== Business benefits

* Auditable drift detection — every factory config in Git.
* ACM placement targets east/west without duplicate Application CRs per cluster.

=== AWS — CodePipeline deploy to ROSA

[source,bash]
----
aws codebuild create-project --name gitops-sync --source type=GITHUB,location=org/platform-hub-spoke-config
aws codepipeline create-pipeline --cli-input-json file://gitops-pipeline.json
# Lab: OpenShift GitOps pulls directly from Gitea/GitHub
----

=== Azure — DevOps pipeline

[source,bash]
----
az pipelines create --name gitops-sync --repository platform-hub-spoke-config \
  --repository-type tfsgit --branch main --yaml-path azure-pipelines.yml
----
""",
        "es": """
=== Características

* **Argo CD** + ApplicationSet + Placements ACM.

=== AWS CodePipeline

[source,bash]
----
aws codebuild create-project --name gitops-sync --source type=GITHUB,location=org/platform-hub-spoke-config
----
""",
    },
    "service-mesh": {
        "en": """
=== Key features

* **OpenShift Service Mesh 3** ambient mode — no sidecar injection for many workloads.
* **Kiali** observability, **mTLS** between services, **waypoint** proxies where needed.
* `stackrox` namespace excluded from ambient to protect ACS sensors.

=== Business benefits

* Zero-trust east-west without rewriting apps for sidecars.
* Consistent telemetry for IE microservices crossing namespaces.

=== AWS — App Mesh contrast

[source,bash]
----
aws appmesh create-mesh --mesh-name factory-mesh
aws appmesh create-virtual-node --mesh-name factory-mesh --virtual-node-name ie-backend \
  --spec file://virtual-node.json
# OpenShift Service Mesh preferred when already on ROSA/ARO
----

=== Azure — Service Fabric mesh (legacy contrast)

[source,bash]
----
# Prefer OpenShift Service Mesh on ARO for Kubernetes-native teams
az network application-gateway create --name mesh-ingress --resource-group rg-workshop --sku Standard_v2
----
""",
        "es": """
=== Características

* **Service Mesh 3** ambient + Kiali.

=== AWS App Mesh

[source,bash]
----
aws appmesh create-mesh --mesh-name factory-mesh
----
""",
    },
    "scalability": {
        "en": """
=== Key features

* **HPA** on IE and demo deployments; **Kafka** buffering for sensor spikes.
* **Cluster Autoscaler** / machine pool growth on spokes under load tests.
* `%USER_NAME%` namespaces include quota limits — observe scaling boundaries.

=== Business benefits

* Handle shift-change telemetry bursts without manual node provisioning.
* HPA + Kafka decouple ingestion from processing.

=== AWS — MSK + HPA on ROSA

[source,bash]
----
aws kafka create-cluster --cluster-name ie-kafka --kafka-version 3.5.1 \
  --number-of-broker-nodes 3 --broker-node-group-info file://brokers.json
oc autoscale deployment line-dashboard --min=2 --max=10 --cpu-percent=70 -n industrial-edge-tst-all
----

=== Azure — Event Hubs Kafka head

[source,bash]
----
az eventhubs namespace create --name ie-kafka --resource-group rg-workshop --sku Standard \
  --enable-kafka true
oc autoscale deployment line-dashboard --min=2 --max=10 --cpu-percent=70
----
""",
        "es": """
=== Características

* **HPA** + **Kafka** para picos de sensores.

=== AWS MSK

[source,bash]
----
aws kafka create-cluster --cluster-name ie-kafka --kafka-version 3.5.1 --number-of-broker-nodes 3 --broker-node-group-info file://brokers.json
----
""",
    },
    "network-policies": {
        "en": """
=== Key features

* **NetworkPolicy** demo in `industrial-edge-tst-all` from GitOps.
* OVN-Kubernetes enforcement on spokes — default-deny with explicit allow lists.
* `%USER_NAME%` tests allowed vs denied curl paths from Showroom terminal.

=== Business benefits

* Micro-segmentation for OT/IT convergence — contain lateral movement.
* Complements ACS runtime policies and mesh mTLS.

=== AWS — Security groups + NP

[source,bash]
----
aws ec2 authorize-security-group-ingress --group-id sg-ie --protocol tcp --port 8080 --cidr 10.128.0.0/14
aws ec2 revoke-security-group-ingress --group-id sg-ie --protocol tcp --port 8080 --cidr 0.0.0.0/0
oc get networkpolicy -n industrial-edge-tst-all
----

=== Azure — NSG + NP

[source,bash]
----
az network nsg rule create --resource-group rg-workshop --nsg-name ie-nsg \
  --name allow-dashboard --priority 200 --destination-port-ranges 8080 --access Allow \
  --source-address-prefixes VirtualNetwork
oc exec -it deploy/curlpod -- curl -s -o /dev/null -w '%{http_code}' http://line-dashboard:8080
----
""",
        "es": """
=== Características

* **NetworkPolicy** demo OVN en spoke east.

=== AWS security groups

[source,bash]
----
aws ec2 authorize-security-group-ingress --group-id sg-ie --protocol tcp --port 8080 --cidr 10.128.0.0/14
----
""",
    },
    "text-ai-predictive": {
        "en": """
=== Key features

* **ie-anomaly-alerter** — Prometheus-driven statistical alerts from IE metrics.
* Optional **KServe InferenceService** for custom sklearn models on hub.
* MaaS generative prompts for incident summaries post-alert.

=== Business benefits

* Predictive maintenance signals before catastrophic line stops.
* Combine deterministic alerts with LLM postmortem drafts for shift handover.

=== AWS — Lookout for Equipment / SageMaker anomaly

[source,bash]
----
aws lookoutequipment create-dataset --dataset-name vibration-line-01 --dataset-schema file://schema.json
aws sagemaker create-model-bias-job-definition --job-definition-name ie-anomaly \
  --model-bias-baseline-config file://baseline.json
# Lab: ie-anomaly-alerter + OpenShift AI instead
----

=== Azure — Anomaly Detector

[source,bash]
----
az cognitiveservices account create --name factory-anomaly --kind AnomalyDetector \
  --resource-group rg-workshop --sku S0
az rest --method post --url "https://factory-anomaly.cognitiveservices.azure.com/anomalydetector/v1.0/timeseries/entire/detect"
----
""",
        "es": """
=== Características

* **ie-anomaly-alerter** + MaaS para resúmenes generativos.

=== AWS Lookout for Equipment

[source,bash]
----
aws lookoutequipment create-dataset --dataset-name vibration-line-01 --dataset-schema file://schema.json
----
""",
    },
}


def _default_extended(slug: str, lang: str) -> str:
    """Generic extended block for modules without bespoke content."""
    if lang == "es":
        return f"""
=== Características clave

* Patrón OpenShift híbrido alineado al módulo **{slug}** en la flota hub-spoke del lab.
* GitOps en `platform-hub-spoke-config` — sincronizado vía Argo CD.
* Usuario de lab **`%USER_NAME%`** con RBAC de solo lectura en namespaces workshop.

=== Beneficios

* Mismas prácticas en ROSA, on-prem o Azure Red Hat OpenShift.
* Reduce tickets de plataforma con autoservicio Developer Hub y políticas ACM.

=== AWS (referencia)

[source,bash]
----
oc get pods -A | head -20
aws sts get-caller-identity
----

=== Azure (referencia)

[source,bash]
----
az account show
oc get nodes
----
"""
    return f"""
=== Key features

* OpenShift hybrid pattern aligned to module **{slug}** on the lab hub-spoke fleet.
* GitOps definitions in `platform-hub-spoke-config` — synced via Argo CD.
* Lab user **`%USER_NAME%`** with view RBAC in workshop namespaces.

=== Business benefits

* Same practices on ROSA, on-prem, or Azure Red Hat OpenShift.
* Fewer platform tickets via Developer Hub self-service and ACM policies.

=== AWS reference

[source,bash]
----
oc get pods -A | head -20
aws sts get-caller-identity
----

=== Azure reference

[source,bash]
----
az account show
oc get nodes
----
"""


def extended_section_body(slug: str, lang: str) -> str:
    if slug in MODULE_EXTENDED:
        body = MODULE_EXTENDED[slug].get(lang) or MODULE_EXTENDED[slug].get("en", "")
        if body:
            return body.strip()
    return _default_extended(slug, lang).strip()
