# ROADMAP.md – code‑forge

**Product:** *code‑forge* – A skill‑library platform that empowers AI coding agents to generate high‑quality, production‑ready code for real‑world software tasks.  
**Target launch:** Q4 2026 (MVP)  

---  

## 📌 MVP (Must‑Have for Launch) – Q4 2026  

| Milestone | Description | Success Criteria |
|-----------|-------------|-------------------|
| **Core Skill Library** | Curated collection of **≥150** reusable coding skills (e.g., “Create a REST endpoint”, “Generate Dockerfile”, “Write unit tests with pytest”). Each skill includes: <br>• Prompt template <br>• Input schema <br>• Expected output schema <br>• Validation tests | • All skills pass automated validation suite <br>• Average skill execution latency ≤ 800 ms (vLLM backend) |
| **AI Agent Runtime** | Integration with **vLLM** (production inference) and **SGLang** for structured generation. Provides a sandboxed execution environment for generated code. | • 99.9 % sandbox stability <br>• Secure execution (no network/file system escapes) |
| **Web UI (Beta)** | Simple React dashboard for: <br>• Browsing/searching skills <br>• Submitting a task (prompt + parameters) <br>• Viewing generated code and validation results | • 5‑minute onboarding flow <br>• NPS ≥ 7 from internal beta users |
| **Automated Validation** | End‑to‑end test harness that runs generated code against: <br>• Unit tests <br>• Linting (flake8/ESLint) <br>• Type checking (mypy/tsc) | • ≥ 90 % of generated snippets pass all checks on first run |
| **Telemetry & Analytics** | pgVector‑backed knowledge store logs: <br>• Prompt → skill mapping <br>• Execution latency <br>• Success/failure rates | • Real‑time dashboards for ops team <br>• Data ingestion ≤ 5 ms per request |
| **Security & Compliance** | License‑aware code generation (respect Apache‑2.0, MIT, etc.) and GDPR‑compatible logging. | • No license violations detected in 1 M generated snippets <br>• Security audit sign‑off |

> **MVP‑Critical** items are highlighted in **bold** above. All other features are optional for the beta launch.

---

## 🚀 Version 1 – “Enterprise Enablement” (2027 H1)

| Theme | Key Features | Timeline |
|-------|--------------|----------|
| **Skill Marketplace** | • User‑contributed skill publishing workflow <br>• Rating & review system <br>• Versioning of skills | Q1 2027 |
| **Team Collaboration** | • Shared workspaces <br>• Role‑based access control (admin, developer, reviewer) <br>• Comment threads on generated artifacts | Q1 2027 |
| **Advanced Prompt Engineering** | • Prompt chaining via SGLang <br>• Contextual memory (reuse prior generated snippets) | Q2 2027 |
| **CI/CD Integration** | • GitHub Actions & GitLab CI plugins to invoke code‑forge during pipelines <br>• Auto‑merge guard that rejects PRs failing validation | Q2 2027 |
| **Metrics & Billing** | • Usage‑based metering (tokens, generated lines) <br>• Tiered pricing & quota enforcement | Q3 2027 |
| **Extended Language Support** | • Add Go, Rust, and JavaScript/TypeScript skill sets (≈100 new skills) | Q3 2027 |
| **Compliance Audits** | • SPDX SBOM generation for every output <br>• Automated license conflict detection | Q4 2027 |

---

## 🚀 Version 2 – “AI‑First Development Platform” (2027 H2 – 2028)

| Theme | Key Features | Timeline |
|-------|--------------|----------|
| **Adaptive Skill Generation** | • Meta‑skill that creates new skills on‑the‑fly from user examples <br>• Reinforcement loop feeding back successful generations into the library | H2 2027 |
| **Multi‑Agent Orchestration** | • Coordinator service that routes sub‑tasks to specialized agents (e.g., DB schema, UI, infra) <br>• Visual DAG editor for complex workflows | H2 2027 |
| **Live Debugger & Explainability** | • Step‑through execution view <br>• LLM‑generated explanations of design decisions | H1 2028 |
| **Enterprise SSO & Auditing** | • SAML/OIDC integration <br>• Immutable audit log stored in append‑only vector store | H1 2028 |
| **Performance Optimizations** | • Model quantization & caching layers for sub‑second responses <br>• Distributed vLLM inference across GPU nodes | H2 2028 |
| **Marketplace Monetization** | • Revenue share for third‑party skill authors <br>• Marketplace API for external platforms | H2 2028 |
| **Open‑Source SDK** | • Python & TypeScript client libraries <br>• Plug‑and‑play Docker image for on‑prem deployments | H2 2028 |

---

## 📅 Quarterly Review Cadence

| Quarter | Review Focus | Owner |
|---------|--------------|-------|
| Q4 2026 | MVP readiness – functional, security, and performance gates | PM + QA Lead |
| Q1 2027 | Skill Marketplace UX & community onboarding | Community Manager |
| Q2 2027 | CI/CD plugins & enterprise billing integration | DevOps Lead |
| Q3 2027 | Language expansion & compliance tooling | Legal & Engineering |
| Q4 2027 | Full‑stack performance benchmark & SLA definition | Site Reliability Engineer |
| H1 2028 | Adaptive skill generation & multi‑agent orchestration prototypes | Research Lead |
| H2 2028 | Marketplace monetization & SDK release | Business Development |

---

## 📈 Success Metrics (post‑launch)

| Metric | Target (12 mo) |
|--------|----------------|
| **Active Teams** | ≥ 150 paying teams |
| **Generated Code Volume** | ≥ 2 B lines of code |
| **Skill Adoption Rate** | ≥ 80 % of skills used ≥ 5 times |
| **Mean Time to Resolution (bugs in generated code)** | ≤ 4 hours |
| **Revenue** | $3.2 M ARR |
| **Customer NPS** | ≥ 9 |

---  

*Prepared by the senior product/engineering lead, 2026‑06‑17.*
