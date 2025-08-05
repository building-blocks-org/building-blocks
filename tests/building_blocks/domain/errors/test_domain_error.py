from typing import Optional

from building_blocks.abstractions.errors.core import (
    ErrorMessage,
    ErrorMetadata,
    FieldReference,
)
from building_blocks.domain.errors.domain_error import DomainError, DomainErrors


class FakeDomainError(DomainError):
    def __init__(
        self,
        message: ErrorMessage = ErrorMessage("This is a fake domain error."),
        metadata: Optional[ErrorMetadata] = None,
    ) -> None:
        super().__init__(message, metadata)


class TestDomainError:
    def test_layer_name_property(self) -> None:
        error = FakeDomainError()
        assert error.layer_name == "Domain"

    def test_error_type_property(self) -> None:
        error = FakeDomainError()
        assert error.error_type == "DomainError"

    def test__str__when_message_is_defined(self) -> None:
        error = FakeDomainError(ErrorMessage("This is a fake domain error."))
        actual = str(error)
        expected = "Domain DomainError: This is a fake domain error."
        assert actual == expected

    def test__str__when_message_and_metadata_defined(self) -> None:
        metadata = ErrorMetadata({"context": "some context"})
        error = FakeDomainError(ErrorMessage("This is a fake domain error."), metadata)
        actual = str(error)
        expected = (
            "Domain DomainError: This is a fake domain error. | Context: "
            "{'context': 'some context'}"
        )
        assert actual == expected


class TestDomainErrors:
    def test_layer_name_property(self) -> None:
        field = FieldReference("fake_domain_field")
        errors_collection = DomainErrors(field, errors=[])
        assert errors_collection.layer_name == "Domain"

    def test__str__when_errors_defined(self) -> None:
        field = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = FakeDomainError(error_message)
        errors = DomainErrors(errors=[error], field=field)

        actual_str = str(errors)

        expected_str = (
            f"Domain for field '{field.value}':\n - Domain DomainError: An error "
            "occurred"
        )
        assert actual_str == expected_str
