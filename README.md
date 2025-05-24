# stream_processor

A callback-driven, prefix-safe, lazy LLM stream sanitization library.

## Installation

```bash
pip install llm-stream-processor  # installs the `stream_processor` package
```

## Quickstart

```python
from stream_processor import KeywordRegistry, llm_stream_processor, replace

reg = KeywordRegistry()
reg.register("secret", replace("[REDACTED]"))

@llm_stream_processor(reg, yield_mode="token")
def gen():
    yield "The secret is out."

print(list(gen()))  # ['The [REDACTED] is out.']
```

## Usage

1. Create a `KeywordRegistry` and register patterns with callbacks.
2. Decorate your token generator with `@llm_stream_processor`.
3. Consume the filtered output.

See `examples/example.py` for more examples (importing from `stream_processor`).

To run the demo example directly:
```bash
python3 examples/example.py
```

## Documentation

- Architecture: see `ARCHITECTURE.md`

## Building & Publishing

Using Poetry:
```bash
poetry build           # create source and wheel archives
poetry publish --dry-run  # preview publish to PyPI
poetry publish         # upload to PyPI
```

Using pip/setuptools:
```bash
python3 setup.py sdist bdist_wheel
twine upload dist/*
```