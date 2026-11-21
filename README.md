<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,50:4338ca,100:06b6d4&height=220&section=header&text=ENTERPRISE%20AGENTIC%20AI&fontSize=36&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Cloud-Native%20AI%20Operations%20Platform&descAlignY=60&descSize=17" width="100%" alt="Enterprise Agentic AI"/>

### Intelligent Operations · Agentic Workflows · AWS Cloud

A serverless AI operations platform combining **Amazon Bedrock, Strands Agents, Retrieval-Augmented Generation, and n8n workflow automation**.

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

<br>

![Amazon Bedrock](https://img.shields.io/badge/AI-Amazon_Bedrock-8B5CF6)
![Strands Agents](https://img.shields.io/badge/Framework-Strands_Agents-6366F1)
![Deployment](https://img.shields.io/badge/Deployment-AWS_Lambda-16A34A)
![Security](https://img.shields.io/badge/Security-AWS_IAM-0284C7)

</div>

---

## Overview

**Enterprise Agentic AI Operations Platform** is a cloud-native backend system that connects large language models with operational tools, enterprise document retrieval, and business analytics.

Built with **Python and Strands Agents**, the platform uses Amazon Bedrock for model inference and AWS Lambda for serverless execution.

An IAM-protected API Gateway endpoint exposes the agent to external clients, including an n8n workflow that automates requests and processes agent responses.

The implementation covers agent orchestration, RAG, cloud integrations, containerized deployment, CI/CD, and operational monitoring.

---

## System Architecture

```mermaid
flowchart TD
    USER["User / n8n Workflow"]
    API["API Gateway - IAM Auth"]
    LAMBDA["AWS Lambda - Python / Docker"]
    AGENT["Strands AI Agent"]
    MODEL["Amazon Bedrock - Claude Haiku"]
    KB["Bedrock Knowledge Base"]
    S3["Amazon S3"]
    ROI["Business Metrics"]
    GH["GitHub Actions"]
    ECR["Amazon ECR"]
    CW["CloudWatch"]
    SNS["Amazon SNS"]

    USER --> API
    API --> LAMBDA
    LAMBDA --> AGENT
    AGENT <--> MODEL
    AGENT --> KB
    AGENT --> S3
    AGENT --> ROI

    GH --> ECR
    ECR --> LAMBDA
    LAMBDA --> CW
    API --> CW
    CW --> SNS

    classDef gateway fill:#172554,stroke:#38bdf8,color:#ffffff
    classDef intelligence fill:#312e81,stroke:#a78bfa,color:#ffffff
    classDef operations fill:#064e3b,stroke:#34d399,color:#ffffff

    class API,LAMBDA,ECR gateway
    class AGENT,MODEL,KB,ROI intelligence
    class GH,CW,SNS,S3 operations
```

### Request Lifecycle

1. A client or n8n workflow submits an authenticated request to API Gateway.
2. API Gateway invokes the containerized AWS Lambda backend.
3. The Strands agent interprets the request and selects the appropriate tool.
4. The selected tool performs document retrieval, S3 inspection, or business calculations.
5. The agent processes the tool output and returns a natural-language response.

---

## Core Capabilities

<table>
<tr>
<td width="50%" valign="top">

### 🧠 Agent Orchestration

Natural-language request processing through Strands Agents and Amazon Bedrock.

- LLM-driven tool calling
- Task classification and planning
- Structured tool execution
- Response generation

</td>
<td width="50%" valign="top">

### 📚 Retrieval-Augmented Generation

Document-grounded responses using an existing Amazon Bedrock Knowledge Base.

- Knowledge Base retrieval
- Relevant evidence extraction
- Document summarization
- Source-aware answers

</td>
</tr>
<tr>
<td valign="top">

### 📊 Business Analytics

Dedicated calculation tools for financial and operational analysis.

- ROI calculation
- Net return analysis
- Input validation
- Explainable calculations

</td>
<td valign="top">

### ☁️ AWS Integration

Serverless operations with AWS-managed services.

- Amazon S3 document listing
- IAM-scoped resource access
- Lambda-based execution
- CloudWatch monitoring

</td>
</tr>
<tr>
<td valign="top">

### 🔄 n8n Automation

Workflow integration between n8n and the deployed AWS agent.

- Webhook-triggered workflows
- AWS IAM-authenticated requests
- JSON request and response handling
- External agent invocation

</td>
<td valign="top">

### 🚀 DevOps

Containerized deployment with automated delivery.

- Docker packaging
- GitHub Actions CI/CD
- Amazon ECR
- AWS OIDC authentication

</td>
</tr>
</table>

---

## Technology Stack

| Layer | Technology |
|---|---|
| Programming | Python |
| Agent Framework | Strands Agents |
| LLM | Claude Haiku 4.5 via Amazon Bedrock |
| RAG | Amazon Bedrock Knowledge Bases |
| Backend | AWS Lambda |
| API | Amazon API Gateway |
| Storage | Amazon S3 |
| Automation | n8n |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Container Registry | Amazon ECR |
| Authentication | AWS IAM / SigV4 |
| Monitoring | Amazon CloudWatch |
| Notifications | Amazon SNS |
| Testing | pytest |

---

## Agent Tools

The agent uses specialized tools to perform operations beyond text generation.

| Tool | Responsibility |
|---|---|
| `search_knowledge_base` | Retrieve relevant enterprise document evidence |
| `list_s3_documents` | Discover documents stored in Amazon S3 |
| `calculate_business_metrics` | Calculate ROI and related financial metrics |

### Example: Business Metrics

**Request**

```json
{
  "prompt": "Calculate ROI for an investment of $13.3M and total returns of $20M."
}
```

**Calculation**

```text
Investment       $13,300,000
Total Returns    $20,000,000
Net Benefit       $6,700,000

ROI                    50.38%
```

---

## Workflow Automation with n8n

n8n acts as an external orchestration layer, connecting workflow triggers to the deployed AI backend.

```mermaid
flowchart LR
    A["Webhook Trigger"] --> B["n8n Workflow"]
    B --> C["AWS IAM Authentication"]
    C --> D["API Gateway"]
    D --> E["Lambda AI Agent"]
    E --> F["JSON Response"]

    classDef workflow fill:#312e81,stroke:#a78bfa,color:#ffffff
    class A,B,C,D,E,F workflow
```

The integration uses AWS Signature Version 4 authentication to invoke the API Gateway endpoint without exposing it as a publicly callable unauthenticated API.

---

## CI/CD Architecture

The deployment pipeline automates application testing, container builds, image publishing, and Lambda updates.

```mermaid
flowchart LR
    A["GitHub Push"] --> B["pytest"]
    B --> C["Docker Build"]
    C --> D["Amazon ECR"]
    D --> E["AWS Lambda"]

    classDef pipeline fill:#172554,stroke:#38bdf8,color:#ffffff
    class A,B,C,D,E pipeline
```

### Deployment Approach

- GitHub Actions runs the automated workflow.
- AWS OIDC provides temporary deployment credentials.
- Docker packages the application and dependencies.
- Amazon ECR stores the container image.
- AWS Lambda runs the updated image.

This approach avoids storing long-lived AWS access keys in the GitHub deployment workflow.

---

## Security and Observability

The platform uses AWS-native security and monitoring components.

**Security**

- IAM-authorized API Gateway endpoint
- Dedicated Lambda execution role
- Resource-scoped S3 and Knowledge Base access
- Dedicated IAM permissions for n8n API invocation
- GitHub Actions authentication through OIDC

**Observability**

- CloudWatch application logs
- Lambda error monitoring
- API Gateway 5xx monitoring
- CloudWatch alarms
- SNS email notifications

---

## Engineering Notes

### Bedrock Knowledge Base SDK Compatibility

During container deployment, the Knowledge Base retrieval integration encountered an AWS SDK parameter validation error.

The managed Knowledge Base required `managedSearchConfiguration`, but the installed botocore service model did not recognize that parameter.

The issue was resolved by updating the boto3 and botocore dependencies and adding a Docker build-time compatibility check.

This ensured the deployed Lambda container supported the required Bedrock Agent Runtime request structure.

---

## Repository

The project is maintained in GitHub with automated deployment through GitHub Actions.

**Repository:** [enterprise-agentic-ai-platform](https://github.com/GopikrishnaAshok/enterprise-agentic-ai-platform)

---

<div align="center">

## About the Developer

### GopiKrishna

**Senior Software Engineer**

Backend Engineering · AWS Cloud · DevOps · Generative AI · Agentic AI

[![GitHub](https://img.shields.io/badge/GitHub-GopikrishnaAshok-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GopikrishnaAshok)

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:06b6d4,50:4338ca,100:0f172a&height=110&section=footer" width="100%" alt="Footer"/>

</div>
