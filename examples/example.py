"""
Example usage of llm-stream-processor.

This module demonstrates various patterns for streaming LLM output sanitization:
1. Basic keyword redaction
2. Stream halting on critical patterns
3. Async streaming support
4. Segment dropping (e.g., internal "thinking" blocks)
5. Simulated streaming with real-time output

Run this example:
    python -m examples.example
"""
import asyncio
import time
from stream_processor import (
    KeywordRegistry,
    llm_stream_processor,
    replace,
    halt,
    drop,
    continuous_drop,
    continuous_pass,
)


def demo_basic_redaction():
    """Demo 1: Basic keyword redaction."""
    print("\n" + "=" * 60)
    print("DEMO 1: Basic Keyword Redaction")
    print("=" * 60)
    
    reg = KeywordRegistry()
    reg.register("secret", lambda ctx: replace("[REDACTED]"))
    reg.register("password", lambda ctx: replace("[HIDDEN]"))
    
    @llm_stream_processor(reg, yield_mode="token")
    def generate():
        yield "The secret is that the password for the vault "
        yield "is hidden in the secret compartment."
    
    print("Input:  The secret is that the password for the vault is hidden in the secret compartment.")
    print("Output:", end=" ")
    for token in generate():
        print(token, end="")
    print()


def demo_stream_halt():
    """Demo 2: Halting stream on critical patterns."""
    print("\n" + "=" * 60)
    print("DEMO 2: Stream Halting")
    print("=" * 60)
    
    reg = KeywordRegistry()
    reg.register("EMERGENCY_STOP", halt)
    
    @llm_stream_processor(reg, yield_mode="token")
    def generate():
        yield "Processing data... "
        yield "All systems normal... "
        yield "EMERGENCY_STOP detected! "
        yield "This should not appear."
    
    print("Input:  Processing data... All systems normal... EMERGENCY_STOP detected! This should not appear.")
    print("Output:", end=" ")
    result = list(generate())
    print("".join(result))


def demo_segment_dropping():
    """Demo 3: Drop internal 'thinking' segments."""
    print("\n" + "=" * 60)
    print("DEMO 3: Segment Dropping (Internal Thoughts)")
    print("=" * 60)
    
    reg = KeywordRegistry()
    reg.register("<think>", continuous_drop)
    reg.register("</think>", continuous_pass)
    
    @llm_stream_processor(reg, yield_mode="token")
    def generate():
        yield "Hello! "
        yield "<think>Let me reason about this internally...</think>"
        yield "Here is my final answer."
    
    print("Input:  Hello! <think>Let me reason about this internally...</think>Here is my final answer.")
    print("Output:", end=" ")
    for token in generate():
        print(token, end="")
    print()


def demo_streaming_effect():
    """Demo 4: Real-time streaming output with delays."""
    print("\n" + "=" * 60)
    print("DEMO 4: Real-Time Streaming (with delays)")
    print("=" * 60)
    
    reg = KeywordRegistry()
    reg.register("API_KEY", lambda ctx: replace("[KEY_HIDDEN]"))
    
    @llm_stream_processor(reg, yield_mode="token")
    def generate():
        yield "Your "
        yield "API_KEY "
        yield "is: "
        yield "sk-12345... "
        yield "Keep it safe!"
    
    print("Output:", end=" ", flush=True)
    for token in generate():
        print(token, end="", flush=True)
        time.sleep(0.2)  # Simulate streaming delay
    print()


async def demo_async_streaming():
    """Demo 5: Async streaming support."""
    print("\n" + "=" * 60)
    print("DEMO 5: Async Streaming")
    print("=" * 60)
    
    reg = KeywordRegistry()
    reg.register("confidential", lambda ctx: replace("[CLASSIFIED]"))
    
    @llm_stream_processor(reg, yield_mode="token")
    async def generate():
        chunks = [
            "This document is ",
            "confidential and ",
            "should not be shared."
        ]
        for chunk in chunks:
            yield chunk
            await asyncio.sleep(0.1)
    
    print("Input:  This document is confidential and should not be shared.")
    print("Output:", end=" ", flush=True)
    async for token in generate():
        print(token, end="", flush=True)
    print()


def demo_pii_redaction():
    """Demo 6: PII pattern redaction."""
    print("\n" + "=" * 60)
    print("DEMO 6: PII Redaction")
    print("=" * 60)
    
    reg = KeywordRegistry()
    
    # Redact common email domains
    for domain in ["@gmail.com", "@yahoo.com", "@outlook.com"]:
        reg.register(domain, lambda ctx: replace("@[EMAIL_REDACTED]"))
    
    # Redact phone number prefix
    reg.register("+1-", lambda ctx: replace("[PHONE:"))
    
    @llm_stream_processor(reg, yield_mode="token")
    def generate():
        yield "Contact: john.doe@gmail.com "
        yield "or call +1-555-1234"
    
    print("Input:  Contact: john.doe@gmail.com or call +1-555-1234")
    print("Output:", end=" ")
    for token in generate():
        print(token, end="")
    print()


def main():
    """Run all demos."""
    print("\n🌊 LLM Stream Processor - Examples")
    print("=" * 60)
    
    # Sync demos
    demo_basic_redaction()
    demo_stream_halt()
    demo_segment_dropping()
    demo_streaming_effect()
    demo_pii_redaction()
    
    # Async demo
    asyncio.run(demo_async_streaming())
    
    print("\n" + "=" * 60)
    print("✅ All demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()