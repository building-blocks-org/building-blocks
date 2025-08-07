from typing import Protocol


class Debuggable(Protocol):
    """
    Protocol for objects that can provide a debug string representation.
    This is used to ensure that any object that implements this protocol
    can be converted to a debug string format.
    """

    def as_debug_string(self) -> str:
        """
        Return a detailed, multi-line string describing this object for debugging.
        """
        raise NotImplementedError("Subclasses must implement this method.")
