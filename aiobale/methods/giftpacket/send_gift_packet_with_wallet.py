from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer, GiftPacket
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class SendGiftPacketWithWallet(BaleMethod):
    """
    Sends a gift packet using the sender's wallet balance.

    This method allows transferring a gift packet to a peer (user, group, or channel),
    including distribution details and a unique token from your wallet.

    The response is a simple confirmation via `DefaultResponse`.
    """

    __service__ = Services.GIFT_PACKET.value
    __method__ = "SendGiftPacketWithWallet"
    
    __returning__ = DefaultResponse

    peer: Peer = Field(..., alias="1")
    """The recipient peer (user, group, or channel) who will receive the gift."""

    random_id: int = Field(..., alias="2")
    """A unique random identifier to prevent duplicate requests (used for idempotency)."""

    gift: GiftPacket = Field(..., alias="3")
    """The gift packet containing amount, message, and distribution settings."""

    token: str = Field(..., alias="4")
    """A token used to authorize or identify the gift request."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            random_id: int,
            gift: GiftPacket,
            token: str,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                peer=peer,
                random_id=random_id,
                gift=gift,
                token=token,
                **__pydantic_kwargs,
            )
