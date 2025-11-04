"""Domain entity base classes.

This module provides base classes for domain entities, including Entity and DraftEntity,
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Hashable
from typing import Any, Generic, TypeVar

from building_blocks.domain.errors.entity_id_errors import (
    DraftEntityIsNotHashableError,
    EntityIdCannotBeNoneError,
)

TId = TypeVar("TId", bound=Hashable)


class _BaseEntity(Generic[TId], ABC):
    """Base class for domain entities.

    Identity is immutable once set.
    """

    __slots__ = ("_id",)

    def __init__(self, entity_id: TId | None) -> None:
        self._id: TId | None = entity_id

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_id" and hasattr(self, "_id"):
            raise AttributeError("Cannot modify 'id' once it is set.")
        super().__setattr__(name, value)

    @property
    def id(self) -> TId | None:
        """The unique identifier of the entity (may be None for drafts)."""
        return self._id

    def is_persisted(self) -> bool:
        """Check if the entity has been persisted (i.e., has a non-null ID)."""
        return self.id is not None

    def __eq__(self, other: object) -> bool:
        """Entities are equal if they are of the same class and have the same ID."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Entities can only be hashed if they have a non-null ID."""
        if self.id is None:
            raise TypeError(f"Unhashable {self.__class__.__name__}: id is None")
        return hash(self.id)

    def __str__(self) -> str:
        """Return a string representation of the entity."""
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the entity."""
        return str(self)


class Entity(_BaseEntity[TId], ABC):
    """Base class for entities that must have an ID at creation."""

    def __init__(self, entity_id: TId) -> None:
        if entity_id is None:
            raise EntityIdCannotBeNoneError()
        super().__init__(entity_id)


class DraftEntity(_BaseEntity[TId], ABC):
    """Base class for entities that may start without an ID (drafts).

    Drafts:
    - Can have id as None initially.
    - Superclass to be used for non-persisted entities that when persisted
      will receive an ID.
    - Equality:
        - If both have non-null IDs: compare by ID.
        - If either has null ID: compare by object identity (is).
    - Hashing:
        - Draft entities are not hashable to avoid issues with mutable identity.
        - Raises DraftEntityIsNotHashableError on __hash__ calls.
    - Intended for use cases where entities are created and manipulated
      before being saved to a database or persistent store.

    Examples:
        >>> draft1 = DraftEntity()
        >>> draft2 = DraftEntity()
        >>> draft1 == draft2
        False
    """

    def __init__(self, entity_id: TId | None = None) -> None:
        super().__init__(entity_id)

    def __eq__(self, other: object) -> bool:
        """Draft entities equality logic."""
        if not isinstance(other, self.__class__):
            return False
        if self.id is None or other.id is None:
            return self is other
        return self.id == other.id

    def __hash__(self) -> int:
        """Draft entities are not hashable."""
        raise DraftEntityIsNotHashableError()


__all__ = ["Entity", "DraftEntity"]
