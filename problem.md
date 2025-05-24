# 📑 Problem Statement: LLM Stream Processing & Sanitization

## 1. Background & Motivation
Modern applications integrate large language models (LLMs) for real-time, streaming responses (e.g., chatbots, live assistants, video captions). As tokens arrive, compliance, UX, and safety requirements mandate:
- **Redaction & Replacement**: Hide or replace sensitive content (e.g., PII, secrets, banned terms) in-flight without delaying the user.
- **Dynamic Side-Effects**: Trigger analytics, webhooks, or metrics counters on keyword detection.
- **Segment-Based Control**: Drop or isolate segments (e.g., internal “thought” vs. public “response”).
- **Immediate Abort**: Halt streaming on critical policy violations (e.g., violence, self-harm content).

## 2. Challenges & Constraints
1. **Prefix Safety**: No partial sensitive pattern should be leaked before full match confirmation. LLM tokens may split sensitive words across token boundaries.
2. **Low Latency**: Target < 5 µs per token processing overhead to not degrade interactive experiences.
3. **High Throughput**: Stream millions of characters per second; must handle thousands of patterns.
4. **Memory Efficiency**: Optional history tracking without unbounded memory growth.
5. **Sync & Async Support**: Integrate seamlessly with both synchronous and asynchronous LLM SDKs.
6. **Dynamic Rule Updates**: Allow runtime registration/deregistration of patterns without restarting streams.

## 3. Objectives
- Provide a Python library that wraps any token generator (sync/async) with a one-line decorator.
- Expose a low-level API for per-character processing and manual control.
- Support these actions on pattern match:
  - PASS: leave text unchanged
  - DROP: remove the matched pattern
  - REPLACE(text): substitute the pattern with custom text
  - HALT: abort the stream immediately
  - CONTINUE_DROP / CONTINUE_PASS: enter/exit drop segments across multiple tokens
- Offer output modes: `char`, `token`, and `chunk:N`.

## 4. Success Criteria
- **Correctness**: No partial matches, all patterns detected, and actions applied consistently.
- **Performance**: ≤ 5 µs median per character on modern hardware (e.g., Apple M1).
- **Coverage**: 100% unit test coverage for sync, async, edge cases, and performance flags.
 