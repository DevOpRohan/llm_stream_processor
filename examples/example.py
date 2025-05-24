"""Example usage of stream_processor."""
import os
import sys
# Allow running example directly without installing or setting PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stream_processor import KeywordRegistry, llm_stream_processor, replace, halt

# Create a registry and register callbacks
reg = KeywordRegistry()
# Register callbacks: use functions that accept context and return Decision
reg.register("secret", lambda ctx: replace("[REDACTED]"))
reg.register("halt", halt)

@llm_stream_processor(reg, yield_mode="token")
def gen_tokens():
    yield "This is a secret message. "
    yield "Now we will halt the stream here."
    yield "You should not see this."

if __name__ == "__main__":
    for out in gen_tokens():
        print(out, end="")