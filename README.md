<h3 align="center">🛠️ code-forge</h3>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Language: Python](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/)
[![Build: Poetry](https://img.shields.io/badge/build-Poetry-green.svg)](https://python-poetry.org/)
[![Stars: 0](https://img.shields.io/github/stars/axentx/code-forge.svg)](https://github.com/axentx/code-forge/stargazers)

</div>

---

# 🚀 code-forge

**Power developers and AI engineers with structured code generation and testing.**

## Why code-forge?

- **Structured Skill Library**: Leverage 1,200+ reusable code patterns to guide AI agents toward production-ready outputs.
- **Sandboxed Testing**: Validate generated code in isolated environments to ensure correctness and safety.
- **Developer-First Design**: Built with a clean API and extensible YAML/Python decorator support for easy customization.
- **LLM Integration Ready**: Designed for seamless integration into LLM-based code-generation workflows.
- **Production-Grade Tooling**: Powered by Python, Poetry, and pytest—ready for enterprise adoption.
- **Extensible Architecture**: Add new skills effortlessly through declarative configuration or Python decorators.
- **Real-World Validation**: Tested end-to-end with sandboxed execution ensuring reliability.

## Feature Overview

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Code Generation Engine   | Generate code snippets from natural language prompts using structured skills. |
| Skill Library            | Over 1,200 reusable code patterns curated for common development tasks.     |
| Sandboxed Execution      | Run generated code safely in isolated environments for validation.         |
| YAML/Decorator Support   | Extend the skill library using YAML definitions or Python decorators.       |
| Test Framework           | Integrated pytest-based testing for validating generated code behavior.     |
| Developer-Friendly API   | Clean interface for integrating into larger AI coding agent pipelines.      |

## Tech Stack

- **Python**
- **Poetry**
- **pytest**

## Project Structure

```
code-forge/
├── business/        # Business logic and domain models
├── docs/            # Documentation assets
├── src/             # Source code root
│   └── code_forge/  # Main package
├── tests/           # Unit and integration tests
├── pyproject.toml   # Project metadata and dependencies
└── README.md        # This file
```

## Getting Started

### Install Dependencies

```bash
poetry install
```

### Run Tests

```bash
poetry run pytest tests/
```

### Example Usage

```bash
poetry run python -m code_forge.generate --prompt "Create a Python function to sort a list of dictionaries by a key."
```

## Deploy

Deployments are managed via the standard Python packaging workflow:

```bash
poetry build
pip install dist/*.whl
```

Alternatively, publish to PyPI using:

```bash
poetry publish
```

## Status

✅ Early-stage prototype with sandboxed implementation  
Latest commit: `7529bf4 feat(code-forge): real, sandbox-tested implementation`

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.