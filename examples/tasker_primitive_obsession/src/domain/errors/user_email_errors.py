from building_blocks.abstractions.errors.core import (
    ErrorMessage,
    ErrorMetadata,
)
from building_blocks.abstractions.errors.rule_violation_error import RuleViolationError
from building_blocks.abstractions.errors.validation_error import ValidationError

from .email_errors import InvalidEmailFormatError


class EmptyEmailError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Email cannot be empty.")
        super().__init__(message)


class InvalidUserEmailError(InvalidEmailFormatError):
    pass


class UserEmailAlreadyExistsError(RuleViolationError):
    def __init__(self, email: str):
        self.email = email
        error_message = ErrorMessage(f"User with email '{email}' already exists.")
        context = ErrorMetadata({"email": email})
        super().__init__(error_message, metadata=context)

    def __str__(self):
        return f"UserEmailAlreadyExistsError: {self.email}"
