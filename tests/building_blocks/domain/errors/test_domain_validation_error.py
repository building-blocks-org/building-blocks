import pytest

from building_blocks.abstractions.errors.core import ErrorMessage
from building_blocks.domain.errors import DomainValidationError


class TestDomainValidationError:
    @pytest.fixture
    def error(self) -> DomainValidationError:
        error_message = ErrorMessage("Invalid domain state detected.")
        return DomainValidationError(error_message)

    def test_str_representation(self, error: DomainValidationError) -> None:
        expected_str = "Domain Validation Error: Invalid domain state detected."
        assert str(error) == expected_str

    def test_error_type_property(self, error: DomainValidationError) -> None:
        expected_type = "Validation Error"
        assert error.error_type == expected_type
