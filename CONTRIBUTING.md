# Contributing to llm-stream-processor

Thank you for your interest in contributing! This guide outlines how to get started.

## Directory Structure

Root of the repository:
```
llm-stream-processor/        # project root
├── src/                     # source code
│   └── llm_stream_processor/  # Python package
│       ├── api/
│       └── engine/
├── examples/                # example usage scripts
│   └── example.py
├── tests/                   # unit and integration tests
├── README.md                # project overview and quickstart
├── ARCHITECTURE.md          # design and architecture details
├── CONTRIBUTING.md          # this document
├── CODE_OF_CONDUCT.md       # project CoC
├── pyproject.toml           # Poetry package config
├── .gitignore
```

## Development Setup

1. Install dependencies and the package in editable mode:
   ```bash
   poetry install            # installs dev and runtime dependencies
   pip install -e .          # installs the package in editable mode
   ```
2. Run tests:
   ```bash
   poetry run pytest
   ```
3. Lint and format:
   ```bash
   poetry run black .
   poetry run flake8 .
   ```

## How to Contribute

1. Fork the repository and create a feature branch.
2. Write tests for new features or bug fixes.
3. Follow existing code style and add docstrings where needed.
4. Update documentation (`README.md`, `ARCHITECTURE.md`, etc.) if your change affects usage or design.
5. Submit a pull request with a clear description of your changes.