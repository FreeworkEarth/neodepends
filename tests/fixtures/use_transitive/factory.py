"""Factory module — creates Service instances.

UseTransitive fixture (b): the factory imports base.py and provides
create_service(). consumer_di.py imports the factory, not base.py.
"""
from base import Service


def create_service() -> Service:
    return Service()
