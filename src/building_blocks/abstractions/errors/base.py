from typing import Any, Collection, Dict, Generic, Iterator, Optional, Sequence, TypeVar

from building_blocks.abstractions.debuggable import Debuggable

from .core import ErrorMessage, ErrorMetadata, FieldReference


class Error(Exception):
    """Base class for all errors in the system, with message and metadata."""

    def __init__(self, message: ErrorMessage, metadata: Optional[ErrorMetadata] = None):
        self._message = message
        self._metadata = metadata or ErrorMetadata(context={})
        super().__init__(message.value)

    def __repr__(self):
        return (
            f"<{self._get_title_prefix()} message={self._message.value!r} "
            f"context={self._metadata.context!r}>"
        )

    def __str__(self):
        return (
            f"{self._get_title_prefix()}: {self._message.value}"
            f"{self._format_context()}"
        )

    @property
    def message(self) -> ErrorMessage:
        return self._message

    @property
    def context(self) -> Dict[str, Any]:
        return self._metadata.context

    @property
    def metadata(self) -> ErrorMetadata:
        return self._metadata

    def as_debug_string(self) -> str:
        """Return a detailed, multi-line string describing this error for debugging."""
        return (
            f"{self._get_title_prefix()}(\n"
            f"  message={repr(self._message)},\n"
            f"  metadata={repr(self._metadata)}\n"
            ")"
        )

    def _format_context(self) -> str:
        if self.metadata.context:
            return f" | Context: {self._metadata.context}"
        return ""

    def _get_title_prefix(self) -> str:
        return self.__class__.__name__


class FieldErrors:
    """
    Base class for errors associated with a specific field.
    """

    def __init__(self, field: FieldReference, errors: Collection[Error]):
        self._field: FieldReference = field
        self._errors: Sequence[Error] = tuple(
            errors,
        )

    def __repr__(self):
        return (
            f"<{self._get_title_prefix()} field={self._field.value!r} "
            f"errors={len(self._errors)}>"
        )

    def __str__(self):
        error_messages = "\n".join(f" - {str(error)}" for error in self._errors)
        return (
            f"{self._get_title_prefix()} for field '{self._field.value}':\n"
            f"{error_messages}"
        )

    @property
    def field(self) -> FieldReference:
        return self._field

    @property
    def errors(self) -> Sequence[Error]:
        return self._errors

    def as_debug_string(self) -> str:
        """
        Return detailed, multi-line string of this field error collection for debugging.
        """
        error_strings = [f"    {err.as_debug_string()}" for err in self._errors]
        return (
            f"{self._get_title_prefix()}(\n"
            f"  field={repr(self._field)},\n"
            f"  errors=[\n"
            + ("" if not error_strings else "\n".join(error_strings) + "\n")
            + "  ]\n"
            ")"
        )

    def __iter__(self) -> Iterator[Error]:
        return iter(self._errors)

    def __len__(self) -> int:
        return len(self._errors)

    def _get_title_prefix(self) -> str:
        return self.__class__.__name__


ErrorType = TypeVar("ErrorType", bound=Debuggable)


class CombinedErrors(Exception, Generic[ErrorType]):
    """
    Base class for handling multiple errors of the same type.
    This class aggregates errors and provides a unified interface for accessing them.
    """

    def __init__(self, errors: Collection[ErrorType], message: Optional[str] = None):
        self._errors: Sequence[ErrorType] = tuple(
            errors,
        )
        super().__init__(message or "Multiple errors occurred.")

    def __repr__(self):
        return f"<{self._get_title_prefix()} errors={len(self._errors)}>"

    def __str__(self):
        error_details = "\n".join(f"- {str(error)}" for error in self._errors)
        return f"{self._get_title_prefix()}:\n{error_details}"

    @property
    def errors(self) -> Sequence[ErrorType]:
        return self._errors

    def as_debug_string(self) -> str:
        """
        Return a detailed, multi-line string for debugging, showing all contained
        errors.
        """
        error_strings = [
            f"    {e.as_debug_string().replace(chr(10), chr(10)+'    ')}"
            for e in self._errors
        ]
        return (
            f"{self._get_title_prefix()}(\n"
            f"  errors=[\n"
            + ("" if not error_strings else "\n".join(error_strings) + "\n")
            + "  ]\n"
            ")"
        )

    def __iter__(self) -> Iterator[ErrorType]:
        return iter(self._errors)

    def __len__(self) -> int:
        return len(self._errors)

    def _get_title_prefix(self) -> str:
        return self.__class__.__name__
