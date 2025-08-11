from building_blocks.abstractions.errors.core import (
    ErrorMessage,
)
from building_blocks.abstractions.errors.validation_error import ValidationError


class InvalidEmailFormatError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Email format is invalid.")
        super().__init__(message)
