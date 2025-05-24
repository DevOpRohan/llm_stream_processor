"""Example usage of stream_processor."""
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
        # wait 1 second to simulate streaming
        import time
        time.sleep(1)