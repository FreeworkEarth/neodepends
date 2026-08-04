"""
Structural typing protocols for the TrainTicketSystem.

Failure-mode fixture B2 (protocol / structural typing): ``Displayable``
defines a structural contract — any class with a ``display_info()`` method
satisfies it, WITHOUT inheriting from it.

Static analysis cannot detect that Person, TrainStation, Ticket, etc. all
structurally implement Displayable.  There is no ``extends`` or ``implements``
keyword — the relationship is implicit.

NeoDepends will see the Import edge to this file from any file that references
``Displayable`` in a type hint, but will NOT detect the structural subtyping
relationship between Displayable and the implementing classes.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Displayable(Protocol):
    """Anything that can display its info."""

    def display_info(self) -> None: ...


@runtime_checkable
class Identifiable(Protocol):
    """Anything with a string ID."""

    @property
    def id(self) -> str: ...
