from building_blocks.abstractions.errors.core import (
    ErrorMessage,
)
from building_blocks.abstractions.errors.validation_error import ValidationError


class InvalidTaskIdError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Invalid task ID. Task ID must be a positive integer.")
        super().__init__(message)
