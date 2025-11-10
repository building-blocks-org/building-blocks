"""Outbound port for a message bus."""

from typing import Generic, Protocol, TypeVar

from forging_blocks.application.ports.inbound.message_handler import MessageHandler
from forging_blocks.domain.messages.message import Message

MessageBusResponse = TypeVar("MessageBusResponse", covariant=True)


class MessageBus(Protocol, Generic[MessageBusResponse]):
    """Asynchronous outbound port for a message bus."""

    async def dispatch(self, message: Message) -> MessageBusResponse:
        """Dispatch a message asynchronously."""
        ...

    async def register_handler(self, handler: MessageHandler) -> None:
        """Register a message handler asynchronously."""
        ...
