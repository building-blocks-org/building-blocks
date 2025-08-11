from __future__ import annotations

import datetime
from typing import Optional

from examples.tasker_primitive_obsession.src.domain.entities.task import Task
from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from building_blocks.domain.aggregate_root import AggregateVersion

from .base import (
    OrmModel,
)


class TaskModel(OrmModel[Task, int]):
    """
    SQLAlchemy model for Task aggregate.

    This model maps the Task aggregate to a database table, providing
    methods to convert between the model and the domain entity.
    """

    __tablename__ = "tasks"

    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    status: Mapped[str]
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="normal")
    tags: Mapped[str] = mapped_column(String(255), nullable=True, default="")
    # Using a string for tags to keep it simple
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    assignee_email: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, default=None
    )

    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    def __init__(
        self,
        id: Optional[int],
        title: str,
        description: str,
        status: str,
        due_date: datetime.date,
        version: int = 0,
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.due_date = due_date
        self.version = version

    def to_entity(self) -> Task:
        return Task(
            id=self.id,  # type: ignore
            title=self.title,
            description=self.description,
            due_date=self.due_date,
            status=self.status,
            priority=self.priority,
            tags=self.tags.split(",") if self.tags else [],
            progress=self.progress,
            assignee_email=self.assignee_email,
            version=AggregateVersion(self.version),
        )

    @classmethod
    def from_entity(cls, entity: Task) -> TaskModel:
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            status=entity.status,
            due_date=entity.due_date,
            version=entity.version.value,
        )
