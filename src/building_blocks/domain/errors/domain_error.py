from typing import Literal

from building_blocks.abstractions.errors.layered_error import (
    LayeredError,
    LayeredErrors,
)


class DomainError(LayeredError[Literal["Domain"], Literal["DomainError"]]):
    """
    Base class for all domain-related exceptions.
    """

    @property
    def layer_name(self) -> Literal["Domain"]:
        return "Domain"

    @property
    def error_type(self) -> Literal["DomainError"]:
        return "DomainError"


class DomainErrors(LayeredErrors):
    """
    A collection of domain errors, typically for a single field or object.
    """

    @property
    def layer_name(self) -> str:
        return "Domain"

    def _get_title_prefix(self) -> str:
        return self.layer_name
