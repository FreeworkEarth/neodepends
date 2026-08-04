"""Consumer via DI injection.

Imports create_service from factory.py, receives a Service instance,
and calls svc.process(). StackGraphs resolves .process() to
Service.process in base.py, but there is no import line from this
file to base.py — the edge should be labeled UseTransitive.
"""
from factory import create_service

svc = create_service()
result = svc.process()
print(f"Result: {result}")
