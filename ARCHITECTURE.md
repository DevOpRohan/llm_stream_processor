# Architecture & Design

## Table of Contents
1. [Problem Overview](#problem-overview)
2. [Goals & Requirements](#goals--requirements)
3. [High-Level Design](#high-level-design)
   - [Component Diagram](#component-diagram)
   - [Data Flow](#data-flow)
4. [Low-Level Design](#low-level-design)
   - [Aho–Corasick Automaton](#aho–corasick-automaton)
   - [Lazy Buffering Mechanism](#lazy-buffering-mechanism)
   - [Callback Decision Engine](#callback-decision-engine)
5. [Data Structures](#data-structures)
6. [Public API & Usage](#public-api--usage)
7. [Extensibility & Runtime Updates](#extensibility--runtime-updates)
8. [Performance Considerations](#performance-considerations)
9. [Edge Cases & Error Handling](#edge-cases--error-handling)
10. [Testing & Validation](#testing--validation)

---

## Problem Overview

Refer to [problem.md](./problem.md) for a detailed problem statement, motivations, and challenges in streaming LLM output safely in real time.

## Goals & Requirements
1. Prefix-safe multi-pattern detection over a character stream.
2. Streaming sanitization with <5 µs overhead per token.
3. Support PASS, DROP, REPLACE(text), HALT, CONTINUE_DROP/PASS callbacks.
4. Sync and async generator integration via a decorator.
5. Optional history tracking with minimal overhead.
6. Dynamic rule registration/deregistration at runtime.

## High-Level Design

### Component Diagram
```
Client Token Generator (sync/async)
            │
            ▼
    @llm_stream_processor   ← Public API decorator
            │
            ▼
  StreamProcessor Core      ← Character-level engine
     ┌───────────────┐
     │  Aho–Corasick │
     │   Automaton   │
     └───────────────┘
            │
            ▼
  Lazy Buffer + Callbacks  ← apply user decisions
            │
            ▼
      Re-packer (char/token/chunk)
            │
            ▼
           Consumer
```

### Data Flow
1. Decorator wraps the token generator, intercepting each yielded token.
2. Token split into individual characters to maintain prefix safety.
3. Each character fed to `StreamProcessor.process()`:
   - Advance the Aho–Corasick state, following failure links.
   - On match, invoke callbacks in registration order.
   - Apply decisions (PASS/DROP/REPLACE/HALT/CONTINUE_DROP/PASS) to the buffer.
4. Lazy flush: once the buffer exceeds the longest keyword length, emit or drop the oldest character.
5. `@llm_stream_processor` repacks flushed characters into the requested output mode.

## Low-Level Design

### Aho–Corasick Automaton
- **Trie Construction**: Insert each keyword, storing callback lists at terminal nodes.
- **Failure Links**: BFS to point each node to the next longest suffix node.
- **Output Merge**: Each node accumulates outputs from its failure link for multi-pattern support.

### Lazy Buffering Mechanism
- Buffer incoming chars in a deque up to `max_keyword_length`.
- Ensures that partial matches are not prematurely emitted.

### Callback Decision Engine
On detecting the longest match at a node:
1. Build `ActionContext` (keyword, buffer snapshot, position, history).
2. Iterate callbacks:
   - **PASS**: no change.
   - **DROP**: pop the keyword length from the buffer.
   - **REPLACE(text)**: remove keyword and append replacement chars.
   - **HALT**: remove keyword, mark halted, raise `StreamHalted`.
   - **CONTINUE_DROP / PASS**: toggle drop mode, flush buffered content accordingly.
3. Reset automaton state to root to detect overlapping patterns.

## Data Structures
- **_Node**: children dict, failure link, output list of (keyword, callbacks).
- **deque(buffer)**: O(1) append/popleft for lazy flushing.
- **StreamHistory / NullHistory**: track or stub input/output/action logs.
- **ActionContext**: immutable snapshot for callbacks.
- **ActionDecision**: encapsulates callback return instructions.

## Public API & Usage
1. **KeywordRegistry**: register/deregister keywords & callbacks, compile automaton.
2. **@llm_stream_processor**: decorator for sync/async generators.
3. **Helper Actions**: `drop()`, `replace()`, `halt()`, `continuous_drop()`, etc.

```python
from llm_stream_processor import KeywordRegistry, llm_stream_processor, replace, halt
reg = KeywordRegistry()
reg.register('secret', replace('[REDACTED]'))
reg.register('stop', halt)

@llm_stream_processor(reg, yield_mode='token')
def chat():
    yield 'The secret is out.'
    yield 'Please stop here.'
    yield 'No more.'

print(list(chat()))  # ['The [REDACTED] is out.', 'Please ']  
```

## Extensibility & Runtime Updates
- Dynamic `register()` / `deregister()` calls on `KeywordRegistry` followed by `compile()` rebuild.
- Toggle `record_history` to optimize memory vs. introspection.

## Performance Considerations
- Pre-compute `max_keyword_length` to bound buffer size.
- Minimize per-char allocations; use local variables.
- Defer `.join()` calls to flush points, not in hot loops.

## Edge Cases & Error Handling
- Non-matching streams: flush buffer at end.
- Invalid `yield_mode` or decorator misuse → clear exceptions.
- Callback exceptions bubble up to abort processing.

## Testing & Validation
- 31 unit tests cover registry, processor, decorator, actions, history.
- Sync & async flows, overlapping patterns, edge cases, HALT segments.
- Run with `python -m unittest discover tests`.