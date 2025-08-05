from typing import Literal

from building_blocks.abstractions.errors.layered_error import LayeredError
from building_blocks.domain.errors.domain_error import DomainErrors


class DomainValidationError(
    LayeredError[Literal["Domain"], Literal["Validation Error"]]
):
    """
    Indicates a failure of a specific domain validation rule.
    """

    @property
    def layer_name(self) -> Literal["Domain"]:
        return "Domain"

    @property
    def error_type(self) -> Literal["Validation Error"]:
        return "Validation Error"


class DomainValidationErrors(DomainErrors):
    """
    A collection of domain validation errors.
    """

    def _get_title_prefix(self) -> str:
        return "Domain Validation Errors"
