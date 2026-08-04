"""Consumer via init-shim re-export (import-style, not from-import).

Uses `import shim` then accesses shim.Color.RED — this forces StackGraphs
to treat Color access as an attribute lookup through the shim module, rather
than resolving the from-import binding directly to defs.py.
"""
import shim

favorite = shim.Color.RED
print(f"Favorite color: {favorite.name}, value={favorite.value}")
