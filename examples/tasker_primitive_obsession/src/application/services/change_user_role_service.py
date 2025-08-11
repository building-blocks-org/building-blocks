from uuid import UUID

from examples.tasker_primitive_obsession.src.application.ports import (
    ChangeUserRoleFailedResponse,
    ChangeUserRoleRequest,
    ChangeUserRoleResponse,
    ChangeUserRoleSucceededResponse,
    ChangeUserRoleUseCase,
)
from examples.tasker_primitive_obsession.src.domain.ports import UserRepository


class ChangeUserRoleService(ChangeUserRoleUseCase):
    def __init__(self, user_repository: UserRepository) -> None:
        """
        Initialize the service with a user repository.

        Args:
            user_repository: The repository to interact with user data.
        """
        self._user_repository = user_repository

    async def execute(self, request: ChangeUserRoleRequest) -> ChangeUserRoleResponse:
        """
        Execute the use case to change a user's role.

        Args:
            request (ChangeUserRoleRequest): The request containing user ID and new
            role.

        Returns:
        ChangeUserRoleResponse: Contains a success flag and an optional error array of
        messages.
        """
        id = UUID(request.user_id)
        user = await self._user_repository.find_by_id(id)

        if not user:
            return ChangeUserRoleFailedResponse(
                reason="User not found", code="USER_NOT_FOUND"
            )

        previous_role = user.role

        user.change_role(request.new_role)

        await self._user_repository.save(user)

        return ChangeUserRoleSucceededResponse(
            user_id=str(user.id), previous_role=previous_role, new_role=user.role
        )
