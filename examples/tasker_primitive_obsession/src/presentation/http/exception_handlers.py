from typing import Any, Dict

from fastapi import Request
from fastapi.responses import JSONResponse

from building_blocks.abstractions.errors.base import Error
from building_blocks.abstractions.errors.rule_violation_error import (
    CombinedRuleViolationErrors,
)
from building_blocks.abstractions.errors.validation_error import (
    CombinedValidationErrors,
)

ERROR_STATUS_MAP = {
    CombinedRuleViolationErrors: 409,
    CombinedValidationErrors: 400,
}


def get_status_code(exc: Exception) -> int:
    """
    Get the HTTP status code for a given exception.
    """
    for error_type, status_code in ERROR_STATUS_MAP.items():
        if isinstance(exc, error_type):
            return status_code
    return 500


def generic_error_handler(_: Request, exc: Exception) -> JSONResponse:
    error_type = type(exc).__name__
    status_code = get_status_code(exc)
    content: Dict[str, Any] = {}

    if isinstance(exc, CombinedValidationErrors):
        content = create_validation_error_payload(exc)
    elif isinstance(exc, CombinedRuleViolationErrors):
        content = create_rule_violation_error_payload(exc)
    else:
        print(f"Handling generic error: {exc}")
        details = exc.as_debug_string() if isinstance(exc, Error) else str(exc)
        content = {"error": error_type, "message": str(exc), "details": details}

    return JSONResponse(status_code=status_code, content=content)


def create_validation_error_payload(exc: CombinedValidationErrors) -> Dict[str, Any]:
    """
    Handle validation errors by returning a structured JSON response.
    """
    content = {}

    for errors_collection in exc.errors:  # exc.errors returns a collection of Errors
        content[errors_collection.field.value] = []

        for error in errors_collection:
            content[errors_collection.field.value].append(error.message.value)

    return content


def create_rule_violation_error_payload(
    exc: CombinedRuleViolationErrors,
) -> Dict[str, Any]:
    """
    Handle rule violation errors by returning a structured JSON response.
    """
    content = {}

    for errors_collection in exc.errors:
        content["rule_violation_error"] = {
            "message": errors_collection.message.value,
            "context": errors_collection.context,
        }

    return content
