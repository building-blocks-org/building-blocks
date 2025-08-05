from typing import List

from building_blocks.abstractions.errors.core import ErrorMessage, FieldReference
from building_blocks.abstractions.errors.validation_error import (
    ValidationError,
    ValidationErrors,
)


class FakeValidationError(ValidationError):
    def __init__(self) -> None:
        super().__init__(ErrorMessage("This is a fake validation error."))

    def layer_name(self) -> str:
        return "FakeLayer"

    def field(self) -> FieldReference:
        return FieldReference("fake_field")

    def _get_title_prefix(self) -> str:
        return "Fake Validation Error"


class FakeValidationErrors(ValidationErrors):
    def _get_title_prefix(self) -> str:
        return "Fake Validation Errors"


class TestValidationError:
    def test__str__when_errors_are_empty(self):
        error = FakeValidationError()
        assert str(error) == "Validation Error: This is a fake validation error."

    def test__str__when_errors_are_defined(self):
        error = FakeValidationError()
        assert str(error) == "Validation Error: This is a fake validation error."


class TestValidationErrors:
    def test__str__when_errors_are_empty(self):
        field = FieldReference("test_field")
        errors: List[ValidationError] = []

        validation_errors = FakeValidationErrors(field=field, errors=errors)

        expected_validation_error_string = "Validation errors for field 'test_field':\n"
        assert str(validation_errors) == expected_validation_error_string

    def test__str__when_errors_are_defined(self):
        field = FieldReference("test_field")
        errors: List[ValidationError] = [
            ValidationError(ErrorMessage("Error 1")),
            ValidationError(ErrorMessage("Error 2")),
        ]

        validation_errors = FakeValidationErrors(field=field, errors=errors)

        expected = (
            "Validation errors for field 'test_field':\n"
            " - Validation Error: Error 1\n"
            " - Validation Error: Error 2"
        )
        assert str(validation_errors) == expected
