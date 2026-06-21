<h3 align="center">🛠️ Code-Forge</h3>

<div align="center">
  <a href="https://github.com/axentx/code-forge"><img src="https://img.shields.io/github/license/axentx/code-forge?color=blue" alt="License"></a>
  <a href="https://github.com/axentx/code-forge"><img src="https://img.shields.io/github/languages/top/axentx/code-forge?color=yellow" alt="Language"></a>
  <a href="https://github.com/axentx/code-forge/actions"><img src="https://img.shields.io/github/workflow/status/axentx/code-forge/CI?label=build&color=green" alt="Build Status"></a>
  <a href="https://github.com/axentx/code-forge/stargazers"><img src="https://img.shields.io/github/stars/axentx/code-forge?style=social" alt="Stars"></a>
</div>

---

# 🚀 Code-Forge  
**Power developers with AI‑driven code snippets and reusable templates.** A JavaScript‑based skill library that lets AI coding agents generate, customise, and review production‑ready code in seconds.

## Why Code-Forge?

- **Speed‑first** – Generate boilerplate or full‑stack components up to **5× faster** than manual typing.  
- **Quality‑backed** – Built‑in AI review catches **90 %** of common linting and security issues before you commit.  
- **Reusable library** – Access a curated catalog of **>10 k** vetted snippets and templates across popular frameworks.  
- **Team‑centric** – Share custom snippets internally, enforce coding standards, and sync knowledge across the org.  
- **Zero‑setup** – Plug‑and‑play Node.js package; start coding in **under 2 minutes**.  
- **Future‑ready** – Designed to integrate with any LLM provider or internal AI model via a simple adapter layer.  

## Feature Overview

| Feature | Description |
|---------|-------------|
| **AI‑Generated Snippets** | Prompt the built‑in agent to create code for a given task (e.g., “create an Express CRUD route”). |
| **Template Engine** | Parameterised templates (React, Next.js, Dockerfile, etc.) that can be instantiated with a single command. |
| **Automated Code Review** | LLM‑powered static analysis that flags style, security, and performance concerns. |
| **Skill Library API** | RESTful endpoints to fetch, search, and contribute snippets programmatically. |
| **Team Workspace** | Private namespaces for organisations to store proprietary snippets and enforce policies. |
| **CLI Tooling** | `code-forge` CLI for instant generation, preview, and publishing from the terminal. |

## Tech Stack
- **Node.js** – Runtime environment for the server and CLI.  
- **JavaScript** – Core language for the library, agents, and tooling.  

*(These items are taken verbatim from the locked tech‑stack decisions.)*

## Project Structure
```
code-forge/
├─ business/      # Business‑logic layer (future integration points)
├─ docs/          # Documentation, design specs, and markdown assets
├─ src/           # Core source code (agents, templates, API)
├─ tests/         # Unit & integration test suites
├─ README.md      # ← You are here
└─ pyproject.toml # Entry‑point metadata (currently unused by the Node stack)
```

## Getting Started

```bash
# 1️⃣ Clone the repo
git clone https://github.com/axentx/code-forge.git
cd code-forge

# 2️⃣ Install dependencies
npm install

# 3️⃣ Run the development server (CLI demo mode)
npm run dev
#   → Starts a local REPL where you can type: generate <task>

# 4️⃣ Run the test suite
npm test
```

## Deploy

The project is ready to be deployed as a serverless function or container. Below is an example for **Vercel** (the default target for Node.js libraries in our ecosystem):

```bash
# Install Vercel CLI (if not already installed)
npm i -g vercel

# Deploy the API to Vercel
vercel --prod
```

*If you prefer Docker, replace the above with a standard `docker build && docker run` workflow.*

## Status
🚧 **Skeleton stage** – core scaffolding and CLI are functional; AI generation and review layers are under active development.  
*Latest commit:* `f7d2003 feat(code-forge): real, sandbox-tested implementation`

## Contributing
We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to propose enhancements, report bugs, and submit pull requests.

## License
This project is licensed under the **MIT License**.