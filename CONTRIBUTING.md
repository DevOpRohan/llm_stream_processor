# Contributing to LLM Stream Processor

Thank you for your interest in contributing! This guide will help you get started.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Project Architecture](#project-architecture)

---

## 📜 Code of Conduct

**Our Pledge**: We are committed to making participation in our community a harassment-free experience for everyone.

**Our Standards**:
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community

**Enforcement**: Instances of abusive behavior may be reported by contacting the project maintainers.

---

## 🚀 Getting Started

### First-Time Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/llm_stream_processor.git
   cd llm_stream_processor
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/DevOpRohan/llm_stream_processor.git
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Repository Layout

```
.
├── docs/                    # Design documentation
│   ├── PROBLEM.md           # Problem statement and motivations
│   └── ARCHITECTURE.md      # Detailed architecture and design
├── stream_processor/        # Core Python package
│   ├── api/                 # Public API (decorator, actions)
│   └── engine/              # Core engine (processor, registry, types)
├── examples/                # Usage examples
├── tests/                   # Unit and integration tests
├── CONTRIBUTING.md          # This document
├── README.md                # Project overview
├── pyproject.toml           # Package configuration
└── setup.cfg                # Setuptools configuration
```

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.7+ (tested on 3.10, 3.11)
- Git

### Installation

```bash
# Clone and install in editable mode
git clone https://github.com/DevOpRohan/llm_stream_processor.git
cd llm_stream_processor
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

### Verify Installation

```bash
# Run the example
python -m examples.example

# Run tests
python -m pytest tests/ -v
```

---

## 🎨 Code Style

We follow these conventions to maintain code consistency:

### Python Style

- **Formatter**: [Black](https://black.readthedocs.io/) (line length: 88)
- **Linter**: [Flake8](https://flake8.pycqa.org/)
- **Type Hints**: Use type annotations for all public functions

### Before Committing

```bash
# Format code
black .

# Check for linting issues
flake8 stream_processor/ tests/

# Type checking (optional but recommended)
mypy stream_processor/
```

### Docstring Style

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of function.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When input is invalid.
    """
    pass
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_stream_processor.py -v

# Run with coverage (install pytest-cov first)
pip install pytest-cov
python -m pytest tests/ --cov=stream_processor --cov-report=term-missing
```

### Writing Tests

- Place test files in `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test method names: `test_<feature>_<scenario>_<expected>`
- Include tests for both sync and async code paths
- Test edge cases: empty inputs, boundary conditions, error handling

### Test Categories

| Category | Description |
|----------|-------------|
| `TestActions` | Verify action helper functions |
| `TestHistory` | Test history tracking |
| `TestRegistry` | Test keyword registration and trie compilation |
| `TestProcessor` | Test core stream processing logic |
| `TestDecorator` | Test sync/async decorator behavior |

---

## 🔄 Pull Request Process

### Before Submitting

- [ ] Create a focused PR addressing a single concern
- [ ] Write/update tests for new features or bug fixes
- [ ] Run `black .` and `flake8 .` to ensure code quality
- [ ] Run full test suite: `python -m pytest tests/ -v`
- [ ] Update documentation if your change affects usage

### PR Checklist

1. **Title**: Use a clear, descriptive title (e.g., "Add regex pattern support")
2. **Description**: Explain what and why, not just what changed
3. **Link Issues**: Reference related issues with "Fixes #123" or "Relates to #456"
4. **Keep it Small**: PRs under 400 lines are easier to review

### Review Process

1. Maintainers will review your PR within a few days
2. Address feedback and push additional commits
3. Once approved, your PR will be merged

---

## 🐛 Reporting Issues

### Bug Reports

Please include:
- Python version and OS
- Minimal reproducible example
- Expected vs actual behavior
- Full error traceback (if applicable)

### Feature Requests

- Describe the use case
- Explain why existing features don't suffice
- Suggest an implementation approach (optional)

---

## 🏗️ Project Architecture

### Quick Overview

1. **Decorator** (`api/decorator.py`) wraps sync/async generators
2. **StreamProcessor** (`engine/processor.py`) handles character-level processing
3. **KeywordRegistry** (`engine/registry.py`) manages patterns and compiles Aho-Corasick trie
4. **Actions** (`api/actions.py`) provide helper functions for common callback decisions

### Key Design Decisions

- **Aho-Corasick Automaton**: Efficient O(n) multi-pattern matching
- **Lazy Buffering**: Buffer up to max keyword length for prefix safety
- **Callback-Driven**: Users define behavior via callback functions

For detailed architecture, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 📬 Questions?

Open an issue or discussion on GitHub. We're happy to help!