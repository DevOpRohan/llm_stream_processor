# Contributing to llm-stream-processor

Thank you for your interest in contributing! This document covers our Code of Conduct, project background, architecture overview, development setup, and contribution process.

## Repository Layout

```text
.                              # project root
├── docs/                     # design docs: problem statement and architecture
│   ├── PROBLEM.md            # problem statement and motivations
│   └── ARCHITECTURE.md       # detailed architecture and design
├── stream_processor/         # core Python package (import as `stream_processor`)
│   ├── api/
│   └── engine/
├── examples/                 # example usage scripts
│   └── example.py
├── tests/                    # unit and integration tests
├── CONTRIBUTING.md           # this document
├── README.md                 # project overview and quickstart
└── setup.cfg                 # setuptools configuration
```

## Code of Conduct

**Our Pledge**
We pledge to make participation in our community a harassment-free experience for everyone.

**Our Standards**
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community

**Enforcement**
Instances of abusive behavior may be reported by contacting the project maintainers.

## Project Background

llm-stream-processor provides prefix-safe, lazy sanitization of streaming LLM outputs. It allows real-time redaction, replacement, and abort based on user-defined patterns, with minimal latency and optional history tracking.

## Quick Architecture Overview

1. Decorate a sync/async generator with `@llm_stream_processor` to intercept each token.
2. Tokens are split into characters and processed by an Aho–Corasick automaton.
3. On pattern match, user callbacks decide to PASS, DROP, REPLACE(text), HALT, or CONTINUE_DROP/PASS.
4. A lazy buffer up to the longest keyword length ensures no partial leaks.
5. Flushed output is reassembled per the requested `yield_mode` (char/token/chunk).

For detailed usage, see `README.md`.

## Development Setup

1. Install in editable mode:
   ```bash
   pip install -e .
   ```
2. Run tests:
   ```bash
   pytest      # or: python -m unittest discover -v tests
   ```
3. Lint and format:
   ```bash
   black .
   flake8 .
   ```

## How to Contribute

1. Fork the repository and create a feature branch.
2. Write tests for new features or bug fixes.
3. Follow existing code style and add docstrings where needed.
4. Update `README.md` or this document if your change affects usage or design.
5. Submit a pull request with a clear description of your changes.