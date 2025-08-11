from abc import ABC, abstractmethod
from typing import List, Optional, Union

from examples.tasker_primitive_obsession.src.domain.entities.task import DraftTask, Task

from building_blocks.domain.ports.outbound.repository import AsyncRepository


class TaskRepository(AsyncRepository[Task, int], ABC):
    """
    Repository interface for Task aggregate.

    This interface defines the methods for managing Task aggregates in a
    persistent storage. It extends AsyncRepository to provide asynchronous
    operations for creating, updating, and retrieving tasks.
    """

    @abstractmethod
    async def find_by_id(self, id: int) -> Optional[Task]:
        """
        Find a Task aggregate by its ID.
        Args:
            id (int): The unique identifier of the task.
        Returns:
            Optional[Task]: The Task aggregate if found, otherwise None.
        """
        pass

    @abstractmethod
    async def save(self, task: Union[Task, DraftTask]) -> None:
        """
        Save a Task aggregate to the repository.
        Args:
            task (Union[Task, DraftTask]): The Task aggregate to save.
        """
        pass

    @abstractmethod
    async def delete_by_id(self, id: int) -> None:
        """
        Attempt to delete Task aggregate by its ID.

        Args:
            id (int): The unique identifier of the task to delete.

        """
        pass

    @abstractmethod
    async def find_all(self) -> List[Task]:
        """
        Find all Task aggregates in the repository.

        Returns:
            List[Task]: A list of all Task aggregates.
        """
        pass
