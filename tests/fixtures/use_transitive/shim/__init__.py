"""Init-shim re-export — re-exports Color from defs.

UseTransitive fixture (a-init): consumer_reexport.py imports Color from here.
StackGraphs resolves the symbol to its definition in defs.py, creating a Use
edge from consumer_reexport.py to defs.py despite no direct import line.
"""
from defs import Color
