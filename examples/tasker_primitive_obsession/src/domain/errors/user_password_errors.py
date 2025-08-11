from building_blocks.abstractions.errors.core import ErrorMessage
from building_blocks.abstractions.errors.validation_error import ValidationError


class EmptyPasswordError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Password cannot be empty. ")
        super().__init__(message)


class PasswordMustNotContainWhitespaceError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Password must not contain whitespace.")
        super().__init__(message)


class PasswordTooShortError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Password must be at least 8 characters long.")
        super().__init__(message)


class DigitCharacterRequiredPasswordError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Password must contain at least one digit.")
        super().__init__(message)


class MixedCasePasswordError(ValidationError):
    def __init__(self) -> None:
        content = (
            "Password must contain at least one uppercase letter and one lowercase"
            " letter."
        )
        message = ErrorMessage(content)
        super().__init__(message)


class SpecialCharacterRequiredPasswordError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Password must contain at least one special character.")
        super().__init__(message)
