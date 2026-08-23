from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types import Peer
from ...types.responses import HistoryResponse
from ...enums import Services
from ..base import BaleMethod


class LoadPinnedMessages(BaleMethod):
    """
    Loads pinned messages from a specific peer (chat or user).
    
    Returns:
        aiobale.types.responses.HistoryResponse: The response containing the history of pinned messages.
    """

    __service__ = Services.MESSAGING.value
    __method__ = "LoadPinnedMessages"

    __returning__ = HistoryResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) from which the pinned messages are being loaded.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, peer: Peer, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(peer=peer, **__pydantic_kwargs)
