from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaleObject
from .message_content import MessageContent
from .peer import Peer
from .chat import Chat
from .values import IntValue

if TYPE_CHECKING:
    from .message import Message


class UpdatedMessage(BaleObject):
    """
    Represents an event payload when a message is updated in Bale.

    This object contains the minimal updated information of a message,
    including its location (`peer`), unique ID, content, timestamp, and sender.

    The `message` property reconstructs the full `Message` object from this data,
    enabling further interactions or manipulations.
    """

    peer: Peer = Field(..., alias="1")
    """The peer (chat or user) where the updated message belongs."""

    message_id: int = Field(..., alias="2")
    """The unique identifier of the updated message."""

    content: MessageContent = Field(..., alias="3")
    """The updated content of the message, encapsulated in a MessageContent object."""

    date: IntValue = Field(..., alias="4")
    """
    The timestamp of the update, represented as an `IntValue`.  
    This is a millisecond UNIX timestamp indicating when the update occurred.
    """

    sender_id: IntValue = Field(..., alias="5")
    """
    The identifier of the sender as an `IntValue`.  
    Wraps the integer ID of the user who sent the updated message.
    """

    @property
    def message(self) -> Message:
        """
        Reconstructs a full `Message` instance from the updated data.

        Builds a minimal `Chat` object based on `peer` information, then
        returns a `Message` with all relevant fields filled in.

        The returned `Message` is linked with the current client context
        via `.as_(self.client)` for further operations.
        """
        from .message import Message

        chat = Chat(id=self.peer.id, type=self.peer.type)

        return Message(
            message_id=self.message_id,
            chat=chat,
            sender_id=self.sender_id.value,
            date=self.date.value,
            content=self.content,
        ).as_(self.client)

    @property
    def fixed(self) -> Message:
        """
        Alias for `message` property.

        Provided for convenience, offering an alternative name to
        access the reconstructed `Message` object.
        """
        return self.message

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_id: int,
            content: MessageContent,
            date: IntValue,
            sender_id: IntValue,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                peer=peer,
                message_id=message_id,
                content=content,
                date=date,
                sender_id=sender_id,
                **__pydantic_kwargs,
            )
