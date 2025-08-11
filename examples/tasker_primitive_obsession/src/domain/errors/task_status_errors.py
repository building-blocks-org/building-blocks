from building_blocks.abstractions.errors.core import (
    ErrorMessage,
)
from building_blocks.abstractions.errors.validation_error import ValidationError


class InvalidTaskStatusError(ValidationError):
    def __init__(self, valid_statuses: list[str]) -> None:
        message = ErrorMessage(
            "Invalid task status. Task status must be one of the following: "
            f"{valid_statuses}."
        )
        super().__init__(message)
