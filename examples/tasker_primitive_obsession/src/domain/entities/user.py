from __future__ import annotations

import re
from typing import List, Optional
from uuid import UUID, uuid4

from examples.tasker_primitive_obsession.src.domain.errors.user_email_errors import (
    EmptyEmailError,
    InvalidEmailFormatError,
)
from examples.tasker_primitive_obsession.src.domain.errors.user_name_errors import (
    EmptyNameError,
    InvalidNameCharactersError,
    OutOfLimitsUserNameError,
)
from examples.tasker_primitive_obsession.src.domain.errors.user_password_errors import (
    DigitCharacterRequiredPasswordError,
    EmptyPasswordError,
    MixedCasePasswordError,
    PasswordMustNotContainWhitespaceError,
    PasswordTooShortError,
    SpecialCharacterRequiredPasswordError,
)
from examples.tasker_primitive_obsession.src.domain.errors.user_role_errors import (
    InvalidRoleError,
    UserAlreadyHasRoleError,
)

from building_blocks.abstractions.errors.base import CombinedErrors
from building_blocks.abstractions.errors.core import FieldReference
from building_blocks.abstractions.errors.rule_violation_error import (
    CombinedRuleViolationErrors,
)
from building_blocks.abstractions.errors.validation_error import (
    CombinedValidationErrors,
    ValidationFieldErrors,
)
from building_blocks.abstractions.result import Err, Ok, Result
from building_blocks.domain.aggregate_root import AggregateRoot, AggregateVersion


class User(AggregateRoot[UUID]):
    _VALID_ROLE = [
        "admin",
        "engineer",
        "designer",
        "manager",
    ]
    _NAME_LENGTHS = {
        "min": 3,
        "max": 50,
    }
    _min_name_length = 3
    _max_name_length = 50

    def __init__(
        self,
        user_id: UUID,
        name: str,
        email: str,
        password: str,
        role: str = "engineer",
        version: Optional[AggregateVersion] = None,
    ) -> None:
        super().__init__(user_id, version)
        self._name = name
        self._email = email
        self._password = password
        self._role = role

    def __str__(self) -> str:
        return (
            f"User(id={self.id}, "
            f"name={self.name}, "
            f"email={self.email}, "
            f"role={self.role}, "
            f"version={self.version})"
        )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, "
            f"name={self.name}, "
            f"email={self.email}, "
            f"role={self.role}, "
            f"version={self.version})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def create(
        cls,
        user_id: UUID,
        name: str,
        email: str,
        password: str,
        role: str = "engineer",
        version: Optional[AggregateVersion] = None,
    ) -> Result[User, CombinedErrors]:
        errors: List[ValidationFieldErrors] = []

        user_id_result = cls._validate_user_id(user_id)
        name_result = cls._validate_name(name)
        email_result = cls._validate_email(email)
        password_result = cls._validate_password(password)
        role_result = cls._validate_role(role)

        for result in [
            user_id_result,
            name_result,
            email_result,
            password_result,
            role_result,
        ]:
            if isinstance(result, Err):
                errors.append(result.error)

        if errors:
            return Err(CombinedValidationErrors(errors))

        user = cls(user_id, name, email, password, role, version)

        return Ok(user)

    @classmethod
    def register(
        cls,
        name: str,
        email: str,
        password: str,
        role: str = "engineer",
        version: Optional[AggregateVersion] = None,
    ) -> Result[User, CombinedErrors]:
        user_id = uuid4()

        return cls.create(user_id, name, email, password, role, version)

    @property
    def id(self) -> UUID:
        return self._id  # type: ignore[return-value]

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password

    def change_password(self, new_password: str) -> None:
        password_result = self._validate_password(new_password)

        if isinstance(password_result, Err):
            raise CombinedValidationErrors([password_result.error])
        self._password = new_password

    @property
    def role(self) -> str:
        return self._role

    def change_role(self, new_role: str) -> None:
        role_result = self._validate_role(new_role)

        if isinstance(role_result, Err):
            raise CombinedValidationErrors([role_result.error])

        if new_role == self._role:
            raise CombinedRuleViolationErrors(
                errors=[
                    UserAlreadyHasRoleError(new_role=new_role, current_role=self._role)
                ]
            )

        self._role = new_role

    @classmethod
    def _validate_user_id(cls, user_id: UUID) -> Result[UUID, ValidationFieldErrors]:
        errors = []

        if errors:
            return Err(
                ValidationFieldErrors(field=FieldReference("user_id"), errors=errors)
            )

        return Ok(user_id)

    @classmethod
    def _validate_name(cls, name: str) -> Result[str, ValidationFieldErrors]:
        min_length = cls._NAME_LENGTHS["min"]
        max_length = cls._NAME_LENGTHS["max"]
        errors = []

        if not name or not name.strip():
            errors.append(EmptyNameError())
        if len(name) < min_length or len(name) > max_length:
            errors.append(OutOfLimitsUserNameError(min_length, max_length))
        if not all(char.isalpha() or char.isspace() for char in name):
            errors.append(InvalidNameCharactersError())

        if errors:
            return Err(
                ValidationFieldErrors(field=FieldReference("name"), errors=errors)
            )

        return Ok(name)

    @classmethod
    def _validate_email(
        cls,
        email: str,
    ) -> Result[str, ValidationFieldErrors]:
        errors = []

        if not email or not email.strip():
            errors.append(EmptyEmailError())
        if "@" not in email or "." not in email.split("@")[-1]:
            errors.append(InvalidEmailFormatError())

        if errors:
            return Err(
                ValidationFieldErrors(field=FieldReference("email"), errors=errors)
            )

        return Ok(email)

    @classmethod
    def _validate_password(
        cls,
        password: str,
    ) -> Result[str, ValidationFieldErrors]:
        errors = []

        if not password or not password.strip():
            errors.append(EmptyPasswordError())
        if re.search(r"\s", password):
            errors.append(PasswordMustNotContainWhitespaceError())
        if len(password) < 8:
            errors.append(PasswordTooShortError())
        if not any(char.isdigit() for char in password):
            errors.append(DigitCharacterRequiredPasswordError())
        if not any(char.islower() for char in password) or not any(
            char.isupper() for char in password
        ):
            errors.append(MixedCasePasswordError())
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=~`[\]\\;/']", password):
            errors.append(SpecialCharacterRequiredPasswordError())

        if errors:
            field_reference = FieldReference("password")
            return Err(ValidationFieldErrors(field_reference, errors))

        return Ok(password)

    @classmethod
    def _validate_role(cls, role: str) -> Result[str, ValidationFieldErrors]:
        errors = []

        if role not in cls._VALID_ROLE:
            errors.append(InvalidRoleError(cls._VALID_ROLE))

        if errors:
            return Err(
                ValidationFieldErrors(field=FieldReference("role"), errors=errors)
            )
        return Ok(role)
