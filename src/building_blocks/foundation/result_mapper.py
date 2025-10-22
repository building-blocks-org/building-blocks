# pragma: no cover
from typing import Generic, Protocol, TypeVar

from building_blocks.foundation.mapper import Mapper
from building_blocks.foundation.result import Result

SuccessIn = TypeVar("SuccessIn", contravariant=True)
ErrorIn = TypeVar("ErrorIn", contravariant=True)
SuccessOut = TypeVar("SuccessOut", covariant=True)
ErrorOut = TypeVar("ErrorOut", covariant=True)


class ResultMapper(
    Mapper[
        Result[SuccessIn, ErrorIn],
        Result[SuccessOut, ErrorOut],
    ],
    Protocol,
    Generic[SuccessIn, ErrorIn, SuccessOut, ErrorOut],
):
    """
    Maps a Result[SuccessIn, ErrorIn] from one layer or representation
    to another Result[SuccessOut, ErrorOut].

    Example:
        ApplicationResult = Result[CreateTaskResponse, CombinedValidationErrors]
        HttpResult = Result[JSONResponse, ErrorResponse]

        class CreateTaskHttpResultMapper(
            ResultMapper[
                CreateTaskResponse,
                CombinedValidationErrors,
                JSONResponse,
                ErrorResponse
            ]
        ):
            def __init__(self, success_mapper: Mapper, error_mapper: Mapper):
                self.success_mapper = success_mapper
                self.error_mapper = error_mapper

            def map(self, result: ApplicationResult) -> HttpResult:
                if result.is_ok():
                    data = self.success_mapper.map(result.unwrap())
                    return Result.ok(data)
                else:
                    error = self.error_mapper.map(result.unwrap_err())
                    return Result.err(error)
    """

    def map(
        self, result: Result[SuccessIn, ErrorIn]
    ) -> Result[SuccessOut, ErrorOut]: ...
