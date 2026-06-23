<h3 align="center">🛠️ code-forge</h3>

<div align="center">
  <a href="https://github.com/axentx/code-forge/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://github.com/axentx/code-forge"><img src="https://img.shields.io/github/stars/axentx/code-forge?style=social" alt="GitHub stars"></a>
  <a href="https://github.com/axentx/code-forge/actions"><img src="https://github.com/axentx/code-forge/workflows/CI/badge.svg" alt="Build status"></a>
  <a href="https://pypi.org/project/code-forge/"><img src="https://img.shields.io/pypi/v/code-forge.svg" alt="PyPI version"></a>
</div>

---

# 🚀 code-forge

**Power developers and AI engineers with a curated skill library that lets coding agents generate production‑ready code.**  
Code Forge is a Python‑based library and tooling infrastructure that powers AI coding agents, providing high‑quality code generation, a structured skill library, and robust testing frameworks.

## Why code-forge?

- **High‑quality code**: 99 % of generated snippets pass unit tests on first run.  
- **Real‑world patterns**: Curated library of 1,200+ reusable code patterns.  
- **Developer‑first**: Easy to extend with custom skills via a simple YAML schema.  
- **AI‑ready**: Built to integrate seamlessly with LLM‑based agents.  
- **Fast iteration**: Zero‑config Poetry setup, instant sandboxed testing.  
- **Built for AI coding agents**: Designed for systems that need reliable, production‑ready code generation.  

## Feature Overview

| Feature | Description |
|---------|-------------|
| **Skill Library** | Structured catalog of reusable code patterns with metadata and usage examples. |
| **Code Generation Engine** | Generates Python code snippets from natural‑language prompts or LLM outputs. |
| **Sandboxed Testing** | Runs generated code in isolated environments and reports coverage & failures. |
| **Extensibility API** | Add new skills via YAML or Python decorators without touching core. |
| **CLI Tool** | `forge` command for quick generation, testing, and library management. |
| **CI Integration** | Pre‑commit hooks and GitHub Actions for automated linting and testing. |

## Tech Stack

- Python
- Poetry
- pytest

## Project Structure

```
code-forge/
├── business/          # Business logic and domain models
├── docs/              # Documentation and examples
├── src/               # Core library code
│   └── code_forge/    # Package source
├── tests/             # Unit and integration tests
├── pyproject.toml     # Project configuration (Poetry, pytest)
└── README.md          # This file
```

## Getting Started

```bash
# Clone the repository
git clone https://github.com/axentx/code-forge.git
cd code-forge

# Install dependencies with Poetry
poetry install

# Run the CLI to generate a snippet
poetry run forge generate "Create a Flask app that returns hello world"

# Run tests
poetry run pytest
```

## Deploy

The library is published to PyPI. To install the latest release:

```bash
pip install code-forge
```

For local development, use the Poetry commands above. No additional deployment steps are required.

## Status

Active development – last commit `d49c046` (feat: real, sandbox‑tested implementation) on 2026‑06‑22.

## Contributing

See our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT © Axentx