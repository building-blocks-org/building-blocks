from examples.tasker_primitive_obsession.src.application.ports import (
    CreateTaskRequest,
    CreateTaskResponse,
)
from examples.tasker_primitive_obsession.src.presentation.http.requests import (
    CreateTaskHttpRequest,
)
from examples.tasker_primitive_obsession.src.presentation.http.responses import (
    CreateTaskHttpResponse,
)


class CreateTaskDtoMapper:
    """
    Mapper class to convert a request object into a task creation dictionary.
    """

    @staticmethod
    def from_http_request(request: CreateTaskHttpRequest) -> CreateTaskRequest:
        """
        Maps the HTTP request object to a service request object.
        """

        return CreateTaskRequest(
            title=request.title,
            description=request.description,
            due_date=request.due_date,
        )

    @staticmethod
    def to_http_response(response: CreateTaskResponse) -> CreateTaskHttpResponse:
        """
        Maps the response object to a HTTP response object.
        """
        return CreateTaskHttpResponse()
