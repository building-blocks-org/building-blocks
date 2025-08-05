from abc import abstractmethod
from typing import Generic, TypeVar

from building_blocks.abstractions.errors.base import Error, Errors

LayerName = TypeVar("LayerName", bound=str)
ErrorType = TypeVar("ErrorType", bound=str)


class LayeredError(Error, Generic[LayerName, ErrorType]):
    """
    An abstract base class for all layered errors.
    It provides a common structure for errors that belong to a specific
    application layer.
    """

    @property
    @abstractmethod
    def layer_name(self) -> LayerName:
        """The name of the application layer this error belongs to."""
        raise NotImplementedError

    @property
    @abstractmethod
    def error_type(self) -> ErrorType:
        """A specific type or title for the error within its layer."""
        raise NotImplementedError

    def __str__(self) -> str:
        return (
            f"{self.layer_name} {self.error_type}: {self.message.value}"
            f"{self._format_context()}"
        )


class LayeredErrors(Errors):
    """
    A collection of layered errors, typically for a single field or object.
    This class can be used to group multiple layered errors together.
    """

    @property
    def layer_name(self) -> str:
        """The name of the application layer these errors belong to."""
        return "Layered"

    def _get_title_prefix(self) -> str:
        return self.layer_name
