import datetime
from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from building_blocks.application.ports.inbound.use_case import AsyncUseCase as UseCase


@dataclass(frozen=True)
class CreateTaskRequest:
    title: str
    description: str
    due_date: datetime.date
    priority: str = "medium"
    tags: Optional[List[str]] = None
    progress: int = 0
    duration_minutes: int = 0
    assignee_email: Optional[str] = None


@dataclass(frozen=True)
class CreateTaskResponse:
    pass


class CreateTaskUseCase(UseCase[CreateTaskRequest, CreateTaskResponse]):
    @abstractmethod
    async def execute(self, request: CreateTaskRequest) -> CreateTaskResponse:
        """
        Execute the use case to create a new task.

        Args:
            request (CreateTaskRequest): The request containing task details.

        Returns:
            CreateTaskResponse: The response containing the created task ID.
        """
        pass
