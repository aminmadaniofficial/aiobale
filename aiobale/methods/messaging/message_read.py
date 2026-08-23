import time
from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types import Peer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class MessageRead(BaleMethod):
    """
    Marks a message as read in a specific chat or conversation.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.MESSAGING.value
    __method__ = "MessageRead"

    __returning__ = DefaultResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) where the message is being marked as read.
    """

    date: int = Field(default_factory=lambda: int(time.time() * 1000), alias="2")
    """
    The timestamp (in milliseconds) when the message was marked as read. Defaults to the current time.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, peer: Peer, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(peer=peer, **__pydantic_kwargs)
