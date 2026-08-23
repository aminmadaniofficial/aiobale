from pydantic import Field
from typing import TYPE_CHECKING

from ...types import InfoMessage
from ...types.responses import PacketResponse
from ...enums import Services
from ..base import BaleMethod


class OpenGiftPacket(BaleMethod):
    """
    Opens a received gift packet using the provided message and receiver token.

    This method is used when a user attempts to claim a gift packet. It validates the token,
    returns the result of the opening, and may include pagination and sorting options.

    Returns a `PacketResponse` containing detailed info about the gift opening.
    """

    __service__ = Services.GIFT_PACKET.value
    __method__ = "OpenGiftPacket"
    
    __returning__ = PacketResponse

    message: InfoMessage = Field(..., alias="1")
    """The message object containing gift packet metadata."""

    receiver_token: str = Field(..., alias="2")
    """A unique token representing the user's attempt to open the packet."""

    page_no: dict = Field(default_factory=dict, alias="3")
    """Pagination info if the result is spread over multiple pages."""

    order_type: int = Field(3, alias="4")
    """Ordering mode (e.g., 3 might represent default or time-based order)."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            message: InfoMessage,
            receiver_token: str,
            page_no: dict = {},
            order_type: int = 3,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                message=message,
                receiver_token=receiver_token,
                page_no=page_no,
                order_type=order_type,
                **__pydantic_kwargs,
            )
