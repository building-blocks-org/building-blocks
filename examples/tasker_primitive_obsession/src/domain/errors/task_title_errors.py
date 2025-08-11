from building_blocks.abstractions.errors.core import ErrorMessage
from building_blocks.abstractions.errors.validation_error import ValidationError


class OutOfLimitsTaskTitleError(ValidationError):
    def __init__(self, min_length: int, max_length: int) -> None:
        message = ErrorMessage(
            f"Task title length must be between {min_length} and {max_length}"
            " characters."
        )
        super().__init__(message)
