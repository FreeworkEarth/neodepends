"""Definition module — defines Color enum.

UseTransitive fixture (a): the definition site.
consumer_reexport.py and consumer_reexport2.py use Color without importing
this module directly — they import via shim/__init__.py or shim/enums.py.
"""
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
