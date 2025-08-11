from typing import List

from building_blocks.abstractions.errors.core import (
    ErrorMessage,
)
from building_blocks.abstractions.errors.validation_error import ValidationError


class InvalidTaskPriorityError(ValidationError):
    def __init__(self, valid_priorities: List[str]) -> None:
        message = ErrorMessage(
            "Invalid task priority. Task priority must be one of the following: "
            f"{valid_priorities}."
        )
        super().__init__(message)
