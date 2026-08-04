"""Base service definition.

UseTransitive fixture (b): the definition site for DI injection.
consumer_di.py receives a Service instance from factory.py without
importing base.py directly.
"""


class Service:
    """A service with a process method, injected via factory."""

    def process(self) -> str:
        return "processed"
