"""
llm_stream_processor: A callback-driven, prefix-safe, lazy LLM stream sanitization library.
"""

from .engine.registry import KeywordRegistry
from .engine.processor import StreamProcessor
from .engine.exceptions import StreamHalted
from .engine.context import ActionContext
from .engine.types import ActionDecision, ActionType
from .engine.history import StreamHistory
from .api import (
    llm_stream_processor,
    drop,
    continuous_drop,
    continuous_pass,
    replace,
    passthrough,
    halt,
)

__all__ = [
    "KeywordRegistry",
    "StreamProcessor",
    "StreamHalted",
    "ActionContext",
    "ActionDecision",
    "ActionType",
    "StreamHistory",
    "llm_stream_processor",
    "drop",
    "continuous_drop",
    "continuous_pass",
    "replace",
    "passthrough",
    "halt",
]