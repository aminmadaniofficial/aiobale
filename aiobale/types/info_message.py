from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Optional, Union, Any

from .peer import Peer
from .base import BaleObject
from .values import IntValue
from .other_message import OtherMessage


class InfoMessage(BaleObject):
    """
    Represents metadata about a message, typically used in reply or reference contexts.

    This object encapsulates information about the message sender (peer),
    the unique message identifier, the timestamp of the message, 
    and optionally a reference to the previous message in a thread or conversation.
    """

    peer: Peer = Field(..., alias="1")
    """The sender or participant related to this message."""

    message_id: int = Field(..., alias="2")
    """Unique identifier of the message within the peer's message history."""

    date: Union[IntValue, int] = Field(..., alias="3")
    """
    Timestamp of the message.
    
    Can be either a plain integer UNIX timestamp or a wrapped `IntValue` 
    for extended or protobuf-compatible representations.
    """

    previous_message: Optional[OtherMessage] = Field(None, alias="4")
    """
    Reference to the previous message, if any.

    Useful in reply chains or threaded conversations to link to the message
    this one is replying to or following.
    """

    if TYPE_CHECKING:
        # This constructor is only for type checking and IDE autocompletion.
        # It won't affect runtime behavior.
        def __init__(
            self,
            *,
            peer: Peer,
            message_id: int,
            date: Union[IntValue, int],
            previous_message: Optional[OtherMessage] = None,
            **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(
                peer=peer,
                message_id=message_id,
                date=date,
                previous_message=previous_message,
                **__pydantic_kwargs
            )
