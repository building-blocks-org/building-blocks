from building_blocks.abstractions.errors.core import ErrorMessage, FieldReference
from building_blocks.domain.errors import DomainRuleViolationError
from building_blocks.domain.errors.domain_rule_violation_error import (
    DomainRuleViolationErrors,
)


class TestDomainRuleViolationError:
    def test_layer_name_property(self) -> None:
        error = DomainRuleViolationError(ErrorMessage("Test error."))
        assert error.layer_name == "Domain"

    def test_error_type_property(self) -> None:
        error = DomainRuleViolationError(ErrorMessage("Test error."))
        assert error.error_type == "Rule Violation"

    def test__str__representation(self) -> None:
        error = DomainRuleViolationError(ErrorMessage("A business rule was violated."))
        assert str(error) == "Domain Rule Violation: A business rule was violated."


class TestDomainRuleViolationErrors:
    def test_get_title_prefix(self) -> None:
        errors = DomainRuleViolationErrors(
            field=FieldReference("order_number"), errors=[]
        )
        assert errors._get_title_prefix() == "Domain Rule Violations"

    def test__str__representation(self) -> None:
        field = FieldReference("order_number")
        error = DomainRuleViolationError(
            ErrorMessage("Order must be placed by an authenticated user.")
        )

        errors = DomainRuleViolationErrors(field, errors=[error])

        expected_str = (
            "Domain Rule Violations for field 'order_number':\n - "
            "Domain Rule Violation: Order must be placed by an authenticated user."
        )
        assert str(errors) == expected_str
