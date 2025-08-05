from typing import Literal

from building_blocks.abstractions.errors.layered_error import LayeredError
from building_blocks.domain.errors.domain_error import DomainErrors


class DomainRuleViolationError(
    LayeredError[Literal["Domain"], Literal["Rule Violation"]]
):
    """
    Indicates that a business rule has been violated.
    """

    @property
    def layer_name(self) -> Literal["Domain"]:
        return "Domain"

    @property
    def error_type(self) -> Literal["Rule Violation"]:
        return "Rule Violation"


class DomainRuleViolationErrors(DomainErrors):
    """
    A collection of domain rule violation errors.
    """

    @property
    def layer_name(self) -> str:
        return "Domain"

    def _get_title_prefix(self) -> str:
        return "Domain Rule Violations"
