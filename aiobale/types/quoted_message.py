from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ..exceptions import AiobaleError
from .peer import Peer
from .values import IntValue
from .base import BaleObject
from .message_content import MessageContent
from .chat import Chat

if TYPE_CHECKING:
    from .message import Message


class QuotedMessage(BaleObject):
    """
    Represents a quoted (replied-to) message within another message.

    This model is used when a message is replying to another message, 
    and contains enough metadata to reconstruct or display the original one.
    """

    message_id: IntValue = Field(..., alias="1")
    """The ID of the quoted message (wrapped in `IntValue` for internal consistency)."""

    sender_id: int = Field(..., alias="3")
    """The ID of the sender of the quoted message (usually a user ID)."""

    date: int = Field(..., alias="4")
    """Timestamp (in milliseconds) when the quoted message was originally sent."""

    content: MessageContent = Field(..., alias="5")
    """Content of the quoted message — includes text, media, or other types."""

    peer: Peer = Field(..., alias="6")
    """The peer (user, group, or channel) where the quoted message originally belongs."""

    chat: Optional[Chat] = Field(None, exclude=True)
    """Optional chat object, used for reconstructing full `Message` instance. Not serialized."""

    @property
    def message(self) -> Message:
        """
        Reconstructs the quoted message as a full `Message` object.

        Requires `self.chat` to be set. If it's not set, raises `AiobaleError`.

        Returns:
            Message: A reconstructed message instance, usable as a full object.
        """
        from .message import Message

        if self.chat is None:
            self.chat = Chat(id=self.peer.id, type=self.peer.type)

        return Message(
            message_id=self.message_id.value,
            chat=self.chat,
            sender_id=self.sender_id,
            date=self.date,
            content=self.content
        ).as_(self.client)

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            message_id: IntValue,
            sender_id: int,
            date: int,
            content: MessageContent,
            peer: Peer,
            chat: Optional[Chat] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                message_id=message_id,
                sender_id=sender_id,
                date=date,
                content=content,
                peer=peer,
                chat=chat,
                **__pydantic_kwargs
            )
