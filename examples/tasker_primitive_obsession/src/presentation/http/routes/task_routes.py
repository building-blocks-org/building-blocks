from examples.tasker_primitive_obsession.src.application.ports import (
    CreateTaskUseCase,
)
from examples.tasker_primitive_obsession.src.presentation.http.dependencies import (
    get_create_task_use_case,
)
from examples.tasker_primitive_obsession.src.presentation.http.mappers import (
    CreateTaskDtoMapper,
)
from examples.tasker_primitive_obsession.src.presentation.http.requests import (
    CreateTaskHttpRequest,
)
from fastapi import APIRouter, Depends, Response, status

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def create_task(
    request: CreateTaskHttpRequest,
    use_case: CreateTaskUseCase = Depends(get_create_task_use_case),
) -> Response:
    service_request = CreateTaskDtoMapper.from_http_request(request)
    await use_case.execute(service_request)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
