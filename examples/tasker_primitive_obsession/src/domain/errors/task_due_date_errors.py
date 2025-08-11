from building_blocks.abstractions.errors.core import (
    ErrorMessage,
)
from building_blocks.abstractions.errors.validation_error import ValidationError


class DueDateCannotBeInPastError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Due date cannot be in the past.")
        super().__init__(message)


class DueDateCannotBeOneYearInFutureError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Due date cannot be more than one year in the future.")
        super().__init__(message)
