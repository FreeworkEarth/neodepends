"""Provider package.

Re-exports ProviderError for convenience, matching the pattern found in
production codebases (e.g. a providers/__init__.py with re-exports).
"""
from tts.providers.protocol import ProviderError

__all__ = ["ProviderError"]
