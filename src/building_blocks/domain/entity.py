"""
Domain entities module.

This module provides the base entity classes for implementing domain entities,
following the principles of Domain-Driven Design (DDD).

- `TransientEntity`: For entities whose id may be None (not yet persisted).
- `Entity`: For entities whose id must always be present (never None).
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Hashable
from typing import Generic, Optional, TypeVar

TId = TypeVar("TId", bound=Hashable)  # Type variable for the entity's unique identifier


class TransientEntity(Generic[TId], ABC):
    """
    Base class for domain entities whose id may be None (not yet persisted).

    Use this for entities where the id is assigned by a persistence mechanism
    (e.g., database auto-increment), and so may be None until after persistence.

    Example:
        >>> class Task(TransientEntity[int]):
        ...     def __init__(self, id: Optional[int], title: str) -> None:
        ...         super().__init__(id)
        ...         self.title = title
    """

    def __init__(self, id: Optional[TId] = None) -> None:
        self._id = id

    @property
    def id(self) -> Optional[TId]:
        """Returns the (possibly None) unique identifier of the entity."""
        return self._id

    def is_persisted(self) -> bool:
        """Returns True if the entity has a non-None id (i.e., has been persisted)."""
        return self._id is not None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TransientEntity):
            return False
        return self.id is not None and other.id is not None and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self) -> str:
        return self.__str__()


class Entity(TransientEntity[TId], ABC):
    """
    Base class for domain entities whose id must always be set (never None).

    Use this for entities where the id is always present, such as those with UUIDs
    or any entity after it has been persisted.

    Example:
        >>> class User(Entity[str]):
        ...     def __init__(self, id: str, name: str):
        ...         super().__init__(id)
        ...         self.name = name
    """

    def __init__(self, id: TId) -> None:
        if id is None:
            raise ValueError("Entity ID cannot be None")
        super().__init__(id)

    @property
    def id(self) -> TId:
        """Returns the unique identifier of the entity (never None)."""
        return self._id  # type: ignore
