"""
Project-specific JSON serialization helpers.

Failure-mode fixture B5 (third-party / stdlib shadow): this file shadows
stdlib ``json``.  Python 3 absolute imports mean ``import json`` resolves to
stdlib, not here.  Only a qualified ``from tts.json import ...`` is genuine.

Same mechanism as tts/logging.py (P1), but tests that the shadow resolver
generalises beyond a single known name.
"""

import json as _stdlib_json
from typing import Any


def to_json(obj: Any, pretty: bool = False) -> str:
    """Serialize an object to a JSON string."""
    indent = 2 if pretty else None
    return _stdlib_json.dumps(obj, indent=indent, default=str)


def from_json(text: str) -> Any:
    """Deserialize a JSON string."""
    return _stdlib_json.loads(text)
