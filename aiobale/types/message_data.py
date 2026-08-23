from __future__ import annotations

from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, Dict, Optional

from ..exceptions import AiobaleError
from .other_message import OtherMessage
from .base import BaleObject
from .message_content import MessageContent
from .quoted_message import QuotedMessage
from .chat import Chat

if TYPE_CHECKING:
    from .message import Message


class MessageData(BaleObject):
    """
    Represents the core data of a message in the Bale messaging system.

    All timestamps are represented as Unix timestamps in **milliseconds**.

    This model holds references to the message sender, message content, replies,
    and the chat context. It also tracks editing history and message threading
    via previous and next message links.
    """

    sender_id: int = Field(..., alias="1")
    """The unique identifier of the sender (user or bot) who created the message."""

    message_id: int = Field(..., alias="2")
    """The unique identifier of this message within the chat."""

    date: int = Field(..., alias="3")
    """Timestamp when the message was originally sent, in milliseconds since epoch."""

    content: MessageContent = Field(..., alias="4")
    """The main content of the message, such as text, media, or service info."""

    replied_to: Optional[QuotedMessage] = Field(None, alias="8")
    """If this message is a reply, the quoted message object it replies to."""

    previous_message: Optional[OtherMessage] = Field(None, alias="10")
    """Reference to the message immediately before this one in the chat thread."""

    next_message: Optional[OtherMessage] = Field(None, alias="11")
    """Reference to the message immediately after this one in the chat thread."""

    edited_at: Optional[int] = Field(None, alias="12")
    """
    Timestamp of the last edit to this message, in milliseconds since epoch.

    The raw data for this field may be nested, so it is normalized during validation.
    """

    chat: Optional[Chat] = Field(None, exclude=True)
    """
    The chat object this message belongs to.

    This is excluded from serialization and must be set manually when constructing 
    a MessageData instance during runtime.
    """

    @model_validator(mode="before")
    @classmethod
    def normalize_edited_at_field(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocesses incoming raw data before model initialization.

        Specifically normalizes the 'edited_at' field ('12') which can be nested
        inside another dict with key '1'.

        Args:
            data (Dict[str, Any]): Raw input data from the Bale API.

        Returns:
            Dict[str, Any]: The normalized data dict with 'edited_at' as int or None.
        """
        if "12" in data and isinstance(data["12"], dict) and "1" in data["12"]:
            data["12"] = data["12"]["1"]
        return data

    @property
    def message(self) -> Message:
        """
        Creates and returns a fully initialized `Message` object from this data.

        Raises:
            AiobaleError: If the `chat` property is not set, which is required to
                          correctly construct the `Message` instance.

        Returns:
            Message: The high-level message object linked to this data.
        """
        from .message import Message

        if self.chat is None:
            raise AiobaleError("Need the current chat to process")

        return Message(
            message_id=self.message_id,
            chat=self.chat,
            sender_id=self.sender_id,
            date=self.date,
            content=self.content,
            previous_message=self.previous_message,
            quoted_replied_to=self.replied_to,
            replied_to=self.replied_to.message if self.replied_to is not None else None,
        ).as_(self.client)

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            sender_id: int,
            message_id: int,
            date: int,
            content: MessageContent,
            replied_to: Optional[QuotedMessage] = None,
            previous_message: Optional[OtherMessage] = None,
            next_message: Optional[OtherMessage] = None,
            edited_at: Optional[int] = None,
            chat: Optional[Chat] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                sender_id=sender_id,
                message_id=message_id,
                date=date,
                content=content,
                replied_to=replied_to,
                previous_message=previous_message,
                next_message=next_message,
                edited_at=edited_at,
                chat=chat,
                **__pydantic_kwargs,
            )
