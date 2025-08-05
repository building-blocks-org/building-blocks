from typing import Optional

from building_blocks.abstractions.errors.core import ErrorMessage, ErrorMetadata
from building_blocks.abstractions.errors.layered_error import LayeredError


class FakeLayeredError(LayeredError):
    """
    A fake implementation of LayeredError for testing purposes.
    This class is used to test the string representation of LayeredError.
    """

    def __init__(
        self, message: ErrorMessage, metadata: Optional[ErrorMetadata] = None
    ) -> None:
        super().__init__(message, metadata)

    @property
    def layer_name(self) -> str:
        return "LayerName"

    @property
    def error_type(s) -> str:
        return "FakeLayeredError"


class TestLayeredError:
    def test__str__when_message_is_empty(self) -> None:
        error_message = ErrorMessage("")
        error = FakeLayeredError(error_message)

        actual = str(error)

        expected = "LayerName FakeLayeredError: "
        assert actual == expected

    def test__str__when_message_is_defined(self) -> None:
        error_message = ErrorMessage("This is a layered error.")
        error = FakeLayeredError(error_message)

        actual = str(error)

        expected = "LayerName FakeLayeredError: This is a layered error."
        assert actual == expected

    def test__str__when_message_and_metadata_defined(self) -> None:
        metadata = ErrorMetadata({"context": "some context"})
        error_message = ErrorMessage("This is a layered error.")
        error = FakeLayeredError(error_message, metadata)

        actual = str(error)

        layer = error.layer_name
        error_type = error.error_type
        # Using a multi-line f-string for readability.
        expected = (
            f"{layer} {error_type}: {error_message.value}"
            f" | Context: {metadata.context}"
        )
        assert actual == expected
