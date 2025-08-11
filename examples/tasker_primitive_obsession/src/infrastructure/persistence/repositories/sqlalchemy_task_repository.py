from __future__ import annotations

from typing import List, Optional, Union, cast

from examples.tasker_primitive_obsession.src.domain.entities.task import DraftTask, Task
from examples.tasker_primitive_obsession.src.domain.ports import (
    TaskRepository,
)
from examples.tasker_primitive_obsession.src.infrastructure.persistence import (
    build_upsert_statement,
)
from examples.tasker_primitive_obsession.src.infrastructure.persistence.models import (
    TaskModel,
)
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyTaskRepository(TaskRepository):
    """
    SQLAlchemy implementation of the TaskRepository interface.

    This class provides methods to interact with the database for Task aggregates,
    including finding, saving, and deleting tasks.

    Note: This is a placeholder for the actual implementation.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the repository with a database session.

        Args:
            session: SQLAlchemy session for database operations.
        """
        self._session = session

    async def save(self, task: Union[Task, DraftTask]) -> None:
        values = self._build_values(task)

        if values.get("id") is None:
            values.pop("id")

        dialect_name = self._session.bind.dialect.name

        upsert_statement = build_upsert_statement(
            dialect_name, cast(Table, TaskModel.__table__), values
        )

        await self._session.execute(upsert_statement)
        await self._session.commit()

    async def find_all(self) -> List[Task]:
        statement = select(TaskModel)
        result = await self._session.execute(statement)
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def find_by_id(self, id: int) -> Optional[Task]:
        model = await self._session.get(TaskModel, id)

        if model:
            return model.to_entity()
        return None

    async def delete_by_id(self, id: int) -> None:
        model = await self._session.get(TaskModel, id)

        if model:
            await self._session.delete(model)
            await self._session.commit()

    def _build_values(self, task: Union[Task, DraftTask]) -> dict:
        version = 0

        if isinstance(task, Task):
            version = task.version.value if task.version else 0

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "due_date": task.due_date,
            "version": version,
        }
