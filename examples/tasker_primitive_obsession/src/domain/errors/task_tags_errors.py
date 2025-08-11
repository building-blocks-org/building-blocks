from building_blocks.abstractions.errors.core import (
    ErrorMessage,
)
from building_blocks.abstractions.errors.validation_error import ValidationError


class InvalidTaskTagError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage(
            "Invalid task tag. Task tag must be a non-empty string without special"
            " characters."
        )
        super().__init__(message)
