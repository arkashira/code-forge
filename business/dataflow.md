# dataflow.md  

## 1. Overview  

`code‑forge` is a **skill‑library platform** that ingests raw code artefacts, transforms them into reusable, searchable “skills” (code‑generation prompts + context), stores them securely, and serves them to AI‑coding agents via authenticated APIs/SDKs.

---

## 2. System Dataflow  

```
+-------------------+        +-------------------+        +-------------------+
|  External Data    |        |   Ingestion Layer |        |  Processing /    |
|  Sources          |        |   (Service)       |        |  Transform Layer |
|-------------------|        |-------------------|        |-------------------|
| • Public GitHub   |  --->  | • Fetcher Workers |  --->  | • Parser (AST)    |
| • GitLab, Bitbucket|       | • Webhook Listener|        | • Metadata Extract|
| • Package registries (npm, PyPI) | • Scheduler (Cron) |   | • Embedding Gen   |
| • Docs, READMEs   |        | • Queue (Kafka)   |        | • Skill Builder   |
| • StackOverflow   |        +-------------------+        | • Security Scan   |
| • Internal Datasets (auto, instr‑resp, …) |        +-------------------+
+-------------------+                                         |
                                                             |
+-------------------+        +-------------------+        +-------------------+
|   Storage Tier    | <----  |  Query / Serving  | <----  |   Egress to User  |
|-------------------|        |   Layer (API)     |        |   (Clients)       |
| • Object Store (S3) |      |-------------------|        |-------------------|
| • Relational DB (Postgres) | • API Gateway (Auth) |   | • Web UI (React) |
| • Vector DB (pgvector) |   | • Skill Catalog Service|   | • SDKs (Python/JS)|
| • Cache (Redis)        |   | • Embedding Search Service| | • CLI (Go)        |
| • Audit Log (Elastic)  |   | • Generation Service (LLM) | | • Webhook Callbacks|
+-------------------+        | • Rate‑Limiter / Quota |   +-------------------+
                             | • RBAC / ABAC Engine   |
                             +-------------------+

```

---

## 3. Tier‑by‑Tier Component Breakdown  

### 3.1 External Data Sources  
- **Public Code Repos** – GitHub, GitLab, Bitbucket (OAuth‑app tokens)  
- **Package Registries** – npm, PyPI, Maven Central (API keys)  
- **Documentation & READMEs** – Docs sites, Markdown files (public HTTP)  
- **Community Q&A** – StackOverflow data dump / API (access token)  
- **Internal Datasets** – `auto`, `instr‑resp`, `messages`, `system‑user‑assistant` (mounted volumes, internal network)  

*Auth boundary*: All external calls are made via **service‑scoped credentials** stored in Vault; no user credentials cross this boundary.

---

### 3.2 Ingestion Layer  
| Component | Responsibility | Tech / Protocol |
|-----------|----------------|-----------------|
| **Fetcher Workers** | Pull code archives / API responses, chunk into raw blobs | Python asyncio, `aiohttp`, Git clone |
| **Webhook Listener** | Receive push events from repos/registries | FastAPI, HTTPS, HMAC signature verification |
| **Scheduler (Cron)** | Periodic re‑crawls, back‑fill jobs | Airflow / Prefect |
| **Message Queue** | Decouple fetchers from processors, guarantee ordering | Apache Kafka (TLS) |
| **Ingress Auth Service** | Validate service tokens, enforce rate limits | mTLS + JWT, Vault‑backed secrets |

*Auth boundary*: Service‑to‑service auth (mTLS + signed JWT). No direct user traffic enters this tier.

---

### 3.3 Processing / Transform Layer  
| Component | Responsibility | Tech |
|-----------|----------------|------|
| **Parser (AST)** | Language‑specific parsing, generate ASTs | Tree‑Sitter, Babel |
| **Metadata Extractor** | Extract function signatures, docstrings, dependencies | Custom Python/Node scripts |
| **Embedding Generator** | Produce vector embeddings for code & docs | OpenAI/Claude embeddings, `sentence‑transformers` |
| **Skill Builder** | Assemble *skill* objects (prompt template + context) | Jinja2, YAML schema validator |
| **Security Scanner** | Static analysis, secret detection, license compliance | Bandit, TruffleHog, SPDX tools |
| **Transform Orchestrator** | DAG orchestration, retries, idempotency | Temporal.io or Airflow |
| **Processing Auth** | Service‑level JWT, role‑based policies | Vault‑issued JWT, OPA policies |

*Auth boundary*: Internal micro‑services communicate over **mutual TLS**; each request carries a short‑lived JWT with scopes (`parse`, `embed`, `scan`).

---

### 3.4 Storage Tier  
- **Object Store (S3‑compatible)** – Raw blobs, compiled skill packages, scanned artifacts.  
- **Relational DB (PostgreSQL)** – Skill metadata, versioning, user‑skill ownership.  
- **Vector DB (pgvector extension)** – Embedding index for semantic search.  
- **Cache (Redis)** – Hot skill look‑ups, rate‑limit counters.  
- **Audit Log (ElasticSearch)** – Immutable event trail for compliance.  

*Auth boundary*:  
- DBs enforce **role‑based DB users** (read‑only, write, admin).  
- S3 buckets use **IAM policies** scoped to service principals.  
- All storage traffic is encrypted in‑flight (TLS) and at rest (AES‑256).

---

### 3.5 Query / Serving Layer  
| Component | Responsibility | Tech |
|-----------|----------------|------|
| **API Gateway** | Entry point, TLS termination, request routing | Kong / Envoy |
| **Auth & RBAC Service** | Validate user JWT, map to roles/permissions | OIDC provider (Keycloak), OPA |
| **Skill Catalog Service** | CRUD on skill definitions, pagination, filters | FastAPI, PostgreSQL |
| **Embedding Search Service** | Approximate nearest‑neighbor queries | pgvector + Postgres, or Milvus |
| **Generation Service** | Invoke LLM with selected skill prompt | OpenAI/Claude API, LangChain |
| **Rate‑Limiter / Quota** | Enforce per‑user/tenant limits | Redis token bucket |
| **Observability** | Tracing, metrics, logs | OpenTelemetry, Prometheus, Grafana |

*Auth boundary*: **User‑facing** traffic terminates at the API Gateway; JWTs are validated and enriched with claims before reaching downstream services. Service‑to‑service calls inside this tier use **mTLS + internal JWT**.

---

### 3.6 Egress to User  
- **Web UI** – React SPA, interactive skill explorer, usage dashboards.  
- **SDKs** – Python (`code_forge`), JavaScript/TypeScript (`@codeforge/sdk`).  
- **CLI** – Go binary (`codeforge-cli`) for CI/CD integration.  
- **Webhook Callbacks** – User‑registered endpoints for async skill generation results.  

All egress channels require **Bearer JWT** obtained via OAuth2 Authorization Code flow (or client‑credentials for server‑to‑server).  

*Auth boundary*: Front‑end and SDKs send tokens to the API Gateway; webhook callbacks are signed with HMAC secret per‑tenant and verified on receipt.

---

## 4. Security & Compliance Highlights  

| Area | Controls |
|------|----------|
| **Ingress** | HMAC verification for webhooks, IP allow‑lists for fetchers |
| **Transit** | TLS 1.3 everywhere, mTLS for inter‑service calls |
| **At Rest** | SSE‑S3, PostgreSQL Transparent Data Encryption, encrypted Redis |
| **Identity** | Central OIDC provider, short‑lived JWTs (5 min), refresh tokens |
| **Authorization** | OPA policies enforce fine‑grained RBAC/ABAC per skill, tenant |
| **Auditing** | Immutable audit log in Elastic, retained 2 years |
| **Scanning** | Automated secret/license scanning on every ingest, block on violations |
| **Disaster Recovery** | Multi‑AZ S3 replication, PG logical replication, daily snapshots |

---

## 5. Dataflow Summary  

1. **External sources** → **Fetcher/Webhook** (service auth) → **Kafka**  
2. **Kafka** → **Processing Workers** (parse → embed → scan) → **Object Store + DB + Vector DB**  
3. **User request** (JWT) → **API Gateway** → **Auth Service** → **Catalog / Search / Generation** → **Response** (skill payload or generated code)  
4. **Optional async** → **Webhook** (HMAC‑signed) → **User endpoint**  

---  

*End of dataflow.md*