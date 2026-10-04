from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .base import Filter
from ..enums import ChatType

if TYPE_CHECKING:
    from ..types.message import Message


class IsGroupOrChannel(Filter):
    """
    Filter to check if the message is from a group or channel chat.

    This filter returns True if the incoming event is a Message and its chat type is
    GROUP, SUPER_GROUP, or CHANNEL.
    """

    async def __call__(self, event: Any) -> bool:
        chat = getattr(event, "chat", None)
        if not chat:
            return False

        return chat.type in (
            ChatType.GROUP,
            ChatType.SUPER_GROUP,
            ChatType.CHANNEL,
        )


class IsPrivate(Filter):
    """
    Filter to check if the message is from a private chat.

    This filter returns True if the incoming event is a Message and its chat type is
    PRIVATE or BOT.
    """

    async def __call__(self, event: Any) -> bool:
        chat = getattr(event, "chat", None)
        if not chat:
            return False

        return chat.type in (
            ChatType.PRIVATE,
            ChatType.BOT,
        )


class ChatTypeFilter(Filter):
    """
    Filter to match messages from a specific chat type.

    Args:
        chat_type (ChatType): The chat type to match (e.g., ChatType.GROUP).
    """

    def __init__(self, chat_type: ChatType):
        self.chat_type = chat_type

    async def __call__(self, event: Any) -> bool:
        chat = getattr(event, "chat", None)
        if not chat:
            return False

        return chat.type == self.chat_type
