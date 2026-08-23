from typing import Optional, TYPE_CHECKING
from pydantic import Field, model_validator

from ..enums import ChatType
from .base import BaleObject
from .message_data import MessageData
from .message import Message
from .other_message import OtherMessage
from .chat import Chat


class GroupMessagePinned(BaleObject):
    """
    Indicates that a message has been pinned in a group chat.

    This object wraps the raw message data and ensures that the `chat` context
    is properly set on the nested `MessageData` (and any replied message) so that
    downstream code can always rely on `.chat` being populated correctly.
    """

    group_id: int = Field(..., alias="1")
    """The unique identifier of the group where the pin event occurred."""

    message_data: MessageData = Field(..., alias="2")
    """
    The raw, unwrapped message payload.

    Contains all message fields (sender, content, timestamps in milliseconds, etc.)
    as received from the Bale API.
    """

    message: Optional[Message] = Field(None)
    """
    A fully constructed `Message` instance, linked to `message_data`.

    Set automatically in the post-validator to avoid reconstructing the message
    object manually. This lets you access methods or properties on `Message`
    directly (e.g., `message.sender`).
    """

    @model_validator(mode="after")
    def _attach_chat_context(self):
        chat = Chat(id=self.group_id, type=ChatType.GROUP)
        self.message_data.chat = chat

        if self.message_data.replied_to is not None:
            self.message_data.replied_to.chat = chat

        # Prevent infinite loop: bypass Pydantic
        object.__setattr__(self, "message", self.message_data.message)
        return self

    if TYPE_CHECKING:
        # This __init__ is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group_id: int,
            message_data: MessageData,
            message: Optional[Message] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                group_id=group_id,
                message_data=message_data,
                message=message,
                **__pydantic_kwargs
            )


class GroupPinRemoved(BaleObject):
    """
    Indicates that the pinned message has been removed in a group chat.

    Wraps the raw removal event, carrying only the group ID and the message
    info that was unpinned.
    """

    group_id: int = Field(..., alias="1")
    """The unique identifier of the group where the unpin event occurred."""

    message: Optional[OtherMessage] = Field(None, alias="2")
    """
    The message that was removed from the pinned position.

    Provided as `OtherMessage` because it may lack certain fields present in
    a full `Message` (e.g., metadata or attachment details).
    """

    if TYPE_CHECKING:
        # This __init__ is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group_id: int,
            message: Optional[OtherMessage] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(group_id=group_id, message=message, **__pydantic_kwargs)
