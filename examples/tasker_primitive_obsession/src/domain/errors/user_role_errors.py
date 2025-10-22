from typing import List

from building_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata
from building_blocks.foundation.errors.rule_violation_error import RuleViolationError
from building_blocks.foundation.errors.validation_error import ValidationError


class InvalidRoleError(ValidationError):
    def __init__(self, valid_roles: List[str]) -> None:
        message = ErrorMessage(f"Invalid role. Valid roles are: {valid_roles}.")
        self._valid_roles_str = valid_roles
        super().__init__(message)


class UserAlreadyHasRoleError(RuleViolationError):
    def __init__(self, new_role: str, current_role: str) -> None:
        message = ErrorMessage(
            f"User already has the role '{new_role}'. "
            f"Attempted to assign role '{current_role}'. "
            "This operation violates the system's rules."
        )
        metadata = ErrorMetadata(
            context={
                "new_role": new_role,
                "current_role": current_role,
            }
        )
        super().__init__(message, metadata)
