"""
Project-specific logging configuration.

This file intentionally shadows stdlib 'logging' to test the
resolve_shadow_imports resolver: bare 'import logging' in other modules
must resolve to stdlib (phantom), while qualified 'from tts.logging import ...'
resolves here (genuine).
"""

import logging as _stdlib_logging


def setup_logging(name: str) -> _stdlib_logging.Logger:
    """Configure and return a logger for the given module name."""
    logger = _stdlib_logging.getLogger(name)
    if not logger.handlers:
        handler = _stdlib_logging.StreamHandler()
        formatter = _stdlib_logging.Formatter(
            "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(_stdlib_logging.INFO)
    return logger
