from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ...types import Peer, OtherMessage, IntBool
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class PinMessage(BaleMethod):
    """
    Pins a specific message in a chat or channel.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the pin operation.
    """

    __service__ = Services.MESSAGING.value
    __method__ = "PinMessage"

    __returning__ = DefaultResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) where the message should be pinned.
    """

    message: OtherMessage = Field(..., alias="2")
    """
    The message to be pinned.
    """

    just_me: Optional[IntBool] = Field(None, alias="3")
    """
    Whether the pin should only be visible to the current user (True) or to everyone (False).
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message: OtherMessage,
            just_me: bool,
            **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(
                peer=peer, message=message, just_me=just_me, **__pydantic_kwargs
            )
