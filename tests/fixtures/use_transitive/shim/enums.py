"""Module-shim re-export — re-exports Color from defs via a named module.

UseTransitive fixture (a-module): consumer_reexport2.py imports Color from
here. Same mechanism as __init__.py but through a named module, proving the
mechanism is independent of __init__.py granularity artifacts.
"""
from defs import Color
