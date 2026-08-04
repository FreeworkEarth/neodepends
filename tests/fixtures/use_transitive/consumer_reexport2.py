"""Consumer via module-shim re-export (import-style).

Uses `import shim.enums` then accesses shim.enums.Color.GREEN.
Same as consumer_reexport.py but through a named module, not __init__.py.
"""
import shim.enums

second = shim.enums.Color.GREEN
print(f"Second color: {second.name}, value={second.value}")
