# TECH_SPEC.md
## Code‑Forge – Technical Specification

**Product**: Code‑Forge – a skill‑library platform enabling AI coding agents to generate high‑quality, production‑ready code for real‑world software tasks.  
**Repository**: `arkashira/code-forge` (main branch)  
**Owner**: AxentX AI‑Workforce  
**Last Updated**: 2026‑06‑17  

---  

### 1. Overview  

Code‑Forge is a modular SaaS that stores, curates, and serves *skills* (self‑contained code generation prompts + execution environments) for autonomous AI agents.  
An AI agent queries the **Skill Service** with a task description; the service selects the best matching skill, runs the associated **Executor** (containerized LLM‑driven code generator), validates the output via **Static Analyzer** and **Test Harness**, and returns the final artifact to the caller.

Key goals:

| Goal | Metric |
|------|--------|
| **Quality** | ≥ 90 % of generated snippets pass static analysis + unit tests |
| **Latency** | 95 th‑percentile response ≤ 2 s (skill lookup) + ≤ 8 s (generation) |
| **Scalability** | 10 k concurrent skill invocations, auto‑scaled via Kubernetes |
| **Extensibility** | New skills added via declarative YAML; no code changes required |
| **Security** | Execution sandboxed; no network egress; resource limits enforced |

---  

### 2. Architecture Diagram  

```
+-------------------+       +-------------------+       +-------------------+
|   API Gateway     | <---> |   Auth Service    | <---> |   Identity DB     |
+-------------------+       +-------------------+       +-------------------+
          |                         |
          v                         v
+-------------------+       +-------------------+
|   Skill Service   | <---> |   Skill Store (DB)|
+-------------------+       +-------------------+
          |
          v
+-------------------+       +-------------------+       +-------------------+
|   Executor Pool   | <---> |   vLLM Inference  | <---> |   Model Artifacts |
| (K8s Jobs)        |       +-------------------+       +-------------------+
+-------------------+                |
          |                         v
          |               +-------------------+
          |               | Static Analyzer   |
          |               +-------------------+
          |                         |
          v                         v
+-------------------+       +-------------------+
|   Test Harness    | <---> |   Test Repo (Git) |
+-------------------+       +-------------------+
          |
          v
+-------------------+
|   Result Store    |
+-------------------+
```

---  

### 3. Core Components  

| Component | Responsibility | Tech Stack | Key Interfaces |
|-----------|----------------|-----------|----------------|
| **API Gateway** | HTTP/HTTPS entry point, request routing, rate limiting | **Envoy** (L7 proxy) + **Istio** for service mesh | `POST /v1/skill/invoke` |
| **Auth Service** | JWT validation, API‑key management, RBAC | **Keycloak** (OpenID Connect) | `Authorization: Bearer <token>` |
| **Skill Service** | Skill lookup, versioning, metadata management | **FastAPI** (Python 3.11) + **SQLModel** | `GET /v1/skill/{id}`; `POST /v1/skill/invoke` |
| **Skill Store** | Persistent storage of skill definitions (YAML) | **PostgreSQL 15** (pgvector extension for embeddings) | SQLAlchemy ORM |
| **Executor Pool** | Runs isolated generation jobs | **Kubernetes Jobs** (PodSecurityPolicy, seccomp) + **Docker** (distroless) | Job spec via K8s API |
| **vLLM Inference** | High‑throughput LLM serving (e.g., Llama‑3‑8B) | **vLLM** (GitHub `vllm-project/vllm`) | gRPC `GenerateCode(request)` |
| **Static Analyzer** | Linting, type‑checking, security scans | **Pyright**, **ESLint**, **Bandit**, **Clang‑Tidy** (via `pre-commit`) | CLI `analyze <path>` |
| **Test Harness** | Executes unit/integration tests supplied with the skill | **pytest**, **JUnit**, **Go test** (containerized runners) | CLI `run-tests <artifact>` |
| **Result Store** | Stores generated artifacts, logs, and validation reports | **MinIO** (S3‑compatible) + **PostgreSQL** metadata | `GET /v1/result/{run_id}` |
| **Monitoring** | Metrics, tracing, alerts | **Prometheus**, **Grafana**, **OpenTelemetry** | Exporters on each service |

---  

### 4. Data Model  

#### 4.1 Skill Definition (YAML)

```yaml
id: string            # UUID v4
name: string
description: string
version: semver
owner: string         # team / user id
model: string         # e.g., "llama3-8b"
prompt_template: |
  {{#system}}
  You are a senior software engineer...
  {{/system}}
  {{#user}}
  {{task_description}}
  {{/user}}
runtime:
  language: python|go|js|cpp
  dependencies:
    - name: numpy
      version: ">=1.24"
    - name: requests
      version: ">=2.28"
tests:
  - path: tests/test_example.py
    framework: pytest
  - path: go/tests/example_test.go
    framework: gotest
```

#### 4.2 Database Schemas (PostgreSQL)

```sql
CREATE TABLE skills (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    version TEXT NOT NULL,
    owner_id UUID REFERENCES users(id),
    model TEXT NOT NULL,
    prompt_template TEXT NOT NULL,
    runtime JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    embedding VECTOR(1536)   -- pgvector, for semantic search
);

CREATE TABLE skill_runs (
    run_id UUID PRIMARY KEY,
    skill_id UUID REFERENCES skills(id),
    requester_id UUID REFERENCES users(id),
    status TEXT CHECK (status IN ('queued','running','failed','succeeded')),
    start_ts TIMESTAMP WITH TIME ZONE,
    end_ts TIMESTAMP WITH TIME ZONE,
    artifact_url TEXT,
    analysis_report JSONB,
    test_report JSONB
);
```

---  

### 5. API Specification  

All endpoints are versioned under `/v1/`. JSON payloads; `application/json` content type.

#### 5.1 `POST /v1/skill/invoke`

| Field | Type | Description |
|-------|------|-------------|
| `skill_id` | UUID | Target skill (optional – if omitted, semantic search is performed) |
| `task_description` | string | Natural‑language description of the coding task |
| `inputs` | object | Optional key/value pairs passed to the prompt template |
| `timeout_seconds` | int | Max allowed runtime (default 30) |

**Response (202 Accepted)**  

```json
{
  "run_id": "c1a2b3d4-...",
  "status_url": "/v1/skill/run/c1a2b3d4-..."
}
```

#### 5.2 `GET /v1/skill/run/{run_id}`

Returns current status and, when finished, links to the artifact and reports.

```json
{
  "run_id": "...",
  "status": "succeeded",
  "artifact_url": "s3://code-forge-results/...",
  "analysis_report": { ... },
  "test_report": { ... }
}
```

#### 5.3 `GET /v1/skill/search?q=...&limit=10`

Semantic search over skill embeddings (pgvector + cosine similarity). Returns ranked list of skill IDs.

---  

### 6. Technology Stack  

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | Python 3.11 (core services) | FastAPI, rich ecosystem, easy integration with vLLM |
| **LLM Inference** | vLLM (GPU‑accelerated, tensor‑parallel) | Proven low‑latency, supports quantized models |
| **Container Runtime** | Docker (distroless) + Kubernetes 1.28 | Autoscaling, isolation, pod‑security |
| **Database** | PostgreSQL 15 + pgvector | Relational integrity + vector search |
| **Object Store** | MinIO (S3‑compatible) | Simple self‑hosted storage, works with CI |
| **Auth** | Keycloak (OIDC) | Enterprise‑grade, supports API‑key flow |
| **Observability** | OpenTelemetry (auto‑instrumented), Prometheus, Grafana | End‑to‑end tracing from API to executor |
| **CI/CD** | GitHub Actions + Argo CD (GitOps) | Automated testing, canary deployments |
| **Static Analysis** | Pre‑commit framework with language‑specific linters | Guarantees code hygiene before returning results |
| **Testing** | Pytest, JUnit, Go test (containerized) | Language‑agnostic test harness |

---  

### 7. Dependencies  

| Dependency | Version | License |
|------------|---------|---------|
| fastapi | 0.112.0 | MIT |
| uvicorn | 0.30.1 | BSD‑3 |
| sqlmodel | 0.0.16 | MIT |
| psycopg2‑binary | 2.9.9 | LGPL‑3 |
| pgvector | 0.5.0 | PostgreSQL |
| vllm | 0.5.2 | Apache‑2.0 |
| torch | 2.3.0 | BSD |
| pre‑commit | 3.7.1 | MIT |
| pytest | 8.2.2 | MIT |
| keycloak‑admin | 0.13.0 | Apache‑2.0 |
| prometheus‑client | 0.20.0 | Apache‑2.0 |
| opentelemetry‑sdk | 1.26.0 | Apache‑2.0 |

All third‑party libraries are vetted for permissive licenses compatible with AxentX commercial distribution.

---  

### 8. Deployment Architecture  

1. **Infrastructure** – Managed Kubernetes (EKS/GKE) across three AZs for HA.  
2. **Ingress** – Envoy + Istio gateway exposing `/v1/*` over TLS (Let’s Encrypt).  
3. **Stateful Services** – PostgreSQL (RDS/Aurora) with read replicas; MinIO in distributed mode (3‑node).  
4. **Executor Nodes** – GPU‑enabled node pool (NVIDIA A100) for vLLM; separate CPU‑only pool for static analysis & test harness.  
5. **Autoscaling** –  
   * Horizontal Pod Autoscaler (HPA) on executor jobs (target CPU ≤ 60 %).  
   * Cluster Autoscaler for node scaling.  
6. **Security** –  
   * PodSecurityPolicy: `runAsNonRoot`, `readOnlyRootFilesystem`.  
   * NetworkPolicy: executor pods isolated, only allowed to reach model artifact bucket and internal services.  
   * Resource quotas per job (CPU ≤ 4, Memory ≤ 16 Gi, GPU ≤ 1).  

**CI/CD Flow**  

```
push -> GitHub Actions
   -> lint + unit tests
   -> build Docker images (multi‑arch)
   -> push to ECR
   -> Argo CD sync (staging)
   -> integration tests (skill end‑to‑end)
   -> canary rollout to prod
```

---  

### 9. Operational Concerns  

| Concern | Mitigation |
|---------|------------|
| **Model Drift** | Periodic re‑training pipeline (leverages AxentX “instr‑resp” dataset). Model artifacts versioned; `skill.model` points to a specific tag. |
| **Skill Poisoning** | Skills are signed with GPG by owners; only verified signatures accepted. |
| **Cost Control** | GPU usage metered; per‑run cost caps enforced in the API gateway. |
| **Data Privacy** | No user code leaves the sandbox; logs are redacted before storage. |
| **Disaster Recovery** | Daily snapshots of PostgreSQL and MinIO; cross‑region replication. |

---  

### 10. Future Enhancements  

| Feature | Description | Target Release |
|---------|-------------|----------------|
| **Multi‑model orchestration** | Dynamically select best‑fit model per skill (e.g., CodeLlama vs. Gemini). | v0.3 |
| **Skill Marketplace** | Public marketplace with revenue sharing for external contributors. | v0.4 |
| **Fine‑grained Usage Billing** | Per‑run token/compute accounting integrated with AxentX billing engine. | v0.5 |
| **Explainability UI** | Visual diff of generated code vs. template, with LLM rationale. | v0.6 |

---  

### 11. Glossary  

- **Skill** – A declarative package containing prompt template, runtime metadata, dependencies, and validation tests.  
- **Executor** – A Kubernetes Job that runs the vLLM inference, static analysis, and test harness for a single skill invocation.  
- **Run ID** – UUID that uniquely identifies an invocation instance.  
- **Embedding** – Vector representation of skill metadata used for semantic search (pgvector).  

---  

*Prepared by:* Senior Product/Engineering Lead – Code‑Forge  
*Document ID:* CF‑TECH‑2026‑06‑17  
*Status:* Draft → Review → Approved → Version 1.0  

---
