from building_blocks.abstractions.errors.core import (
    ErrorMessage,
)
from building_blocks.abstractions.errors.validation_error import ValidationError


class EmptyNameError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Name cannot be empty.")
        super().__init__(message)


class OutOfLimitsUserNameError(ValidationError):
    def __init__(self, min_length: int, max_length: int) -> None:
        message = ErrorMessage(
            f"Name length must be between {min_length} and {max_length}."
        )
        super().__init__(message)


class InvalidNameCharactersError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Name must be alphabetic. Spaces are allowed.")
        super().__init__(message)
