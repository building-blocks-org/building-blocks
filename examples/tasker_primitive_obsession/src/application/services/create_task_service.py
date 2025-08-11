from examples.tasker_primitive_obsession.src.application.ports import (
    CreateTaskRequest,
    CreateTaskResponse,
    CreateTaskUseCase,
)
from examples.tasker_primitive_obsession.src.domain.entities.task import DraftTask
from examples.tasker_primitive_obsession.src.domain.ports import (
    TaskRepository,
)


class CreateTaskService(CreateTaskUseCase):
    """
    Service implementation for creating tasks.

    This service handles the creation of tasks by interacting with the
    TaskRepository to persist the task data.
    """

    def __init__(self, task_repository: TaskRepository) -> None:
        """
        Initialize the service with a task repository.

        Args:
            task_repository: The repository to handle task persistence.
        """
        self._task_repository = task_repository

    async def execute(self, request: CreateTaskRequest) -> CreateTaskResponse:
        """
        Execute the use case to create a new task.

        Args:
            request (CreateTaskRequest): The request containing task details.

        Returns:
            CreateTaskResponse: The response containing the created task ID.
        """
        task_result = DraftTask.create(
            id=None,
            title=request.title,
            description=request.description,
            due_date=request.due_date,
            priority=request.priority,
            tags=request.tags,
            progress=request.progress,
            assignee_email=request.assignee_email,
        )

        if task_result.is_err:
            raise task_result.error

        task = task_result.value
        await self._task_repository.save(task)

        return CreateTaskResponse()
