from typing import Any, Dict, List, Optional, cast
from uuid import UUID

from examples.tasker_primitive_obsession.src.domain.entities.user import User
from examples.tasker_primitive_obsession.src.domain.errors.user_email_errors import (
    UserEmailAlreadyExistsError,
)
from examples.tasker_primitive_obsession.src.domain.ports import UserRepository
from examples.tasker_primitive_obsession.src.infrastructure.persistence import (
    build_upsert_statement,
)
from examples.tasker_primitive_obsession.src.infrastructure.persistence.models import (
    UserModel,
)
from sqlalchemy import Table, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user: User) -> None:
        try:
            values = self._build_values(user)

            dialect_name = self._session.bind.dialect.name

            upsert_statement = build_upsert_statement(
                dialect_name, cast(Table, UserModel.__table__), values
            )

            await self._session.execute(upsert_statement)
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()

            if "email" in str(exc.orig):
                raise UserEmailAlreadyExistsError(user.email) from exc
            raise ValueError(f"Failed to save user: {exc.orig}") from exc

    async def find_all(self) -> List[User]:
        statement = select(UserModel)
        result = await self._session.execute(statement)
        models = result.scalars().all()

        return [model.to_entity() for model in models]

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        model = await self._session.get(UserModel, user_id)

        if model:
            return model.to_entity()
        return None

    async def delete_by_id(self, id: UUID) -> None:
        model = await self._session.get(UserModel, id)

        if model:
            await self._session.delete(model)
            await self._session.commit()

    async def find_by_email(self, email: str) -> Optional[User]:
        statement = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(statement)
        model = result.scalars().first()

        if model:
            return model.to_entity()
        return None

    def _build_values(self, user: User) -> Dict[str, Any]:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "role": user.role,
            "version": user.version.value,
        }
