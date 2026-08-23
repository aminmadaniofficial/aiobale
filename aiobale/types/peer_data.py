from typing import Any, Dict, Optional, TYPE_CHECKING
from pydantic import Field, model_validator

from .base import BaleObject
from .peer import Peer
from .message_content import MessageContent
from .message import Message
from .chat import Chat


class PeerData(BaleObject):
    """
    Represents a peer's latest message state and metadata in the dialog list.

    Used primarily for generating a summarized view of conversations (similar to a chat list),
    including information about unread counts, last message content, and timestamps.
    """

    peer: Peer = Field(..., alias="1")
    """The peer (user, group, or channel) that this data is associated with."""

    unread_count: int = Field(2, alias="2")
    """Number of unread messages in this conversation. Defaults to 2."""

    sort_date: int = Field(..., alias="3")
    """Timestamp (in milliseconds) used to sort the chat list."""

    sender_id: int = Field(..., alias="4")
    """ID of the user who sent the last message in this peer."""

    message_id: int = Field(..., alias="5")
    """ID of the last message in this peer."""

    date: int = Field(..., alias="6")
    """Timestamp (in milliseconds) of the last message sent in this peer."""

    content: MessageContent = Field(..., alias="7")
    """Content of the last message (e.g., text, image, etc.)."""

    first_unread_message: int = Field(..., alias="9")
    """Message ID of the first unread message (used for navigation in clients)."""

    unread_mentions: int = Field(..., alias="13")
    """Number of unread mentions in this peer (e.g., when you are @mentioned in a group)."""

    @model_validator(mode="before")
    @classmethod
    def normalize_nested_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts nested fields like 'first_unread_message' and 'unread_mentions' 
        from wrapped objects returned by the backend. The API returns these as 
        dicts with a "1" key, so we unwrap them here.
        """
        if "9" in data and isinstance(data["9"], dict):
            data["9"] = data["9"].get("1", 0)
        if "13" in data and isinstance(data["13"], dict):
            data["13"] = data["13"].get("1", 0)
        return data

    @property
    def message(self) -> Message:
        """
        Returns the full `Message` object constructed from this peer data.

        This is useful for reconstructing a message instance with correct context
        (chat and sender), based on the summary data in this structure.
        """
        chat = Chat(id=self.peer.id, type=self.peer.type)
        return Message(
            chat=chat,
            sender_id=self.sender_id,
            date=self.date,
            message_id=self.message_id,
            content=self.content
        ).as_(self.client)

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            unread_count: int = 2,
            sort_date: int,
            sender_id: int,
            message_id: int,
            date: int,
            content: MessageContent,
            first_unread_message: int,
            unread_mentions: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                peer=peer,
                unread_count=unread_count,
                sort_date=sort_date,
                sender_id=sender_id,
                message_id=message_id,
                date=date,
                content=content,
                first_unread_message=first_unread_message,
                unread_mentions=unread_mentions,
                **__pydantic_kwargs
            )
