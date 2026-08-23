from pydantic import Field
from typing import TYPE_CHECKING, List

from ...types import Peer, OtherMessage
from ...types.responses import ViewsResponse
from ...enums import Services
from ..base import BaleMethod


class GetMessagesViews(BaleMethod):
    """
    Retrieves view counts for specified messages in a given peer (chat or user).

    Returns:
        aiobale.types.responses.ViewsResponse: The response containing view counts for the requested messages.
    """

    __service__ = Services.ABACUS.value
    __method__ = "GetMessagesViews"

    __returning__ = ViewsResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) from which the messages' view counts are being requested.
    """

    message_ids: List[OtherMessage] = Field(..., alias="2")
    """
    List of message identifiers for which view counts are requested.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_ids: List[OtherMessage],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(peer=peer, message_ids=message_ids, **__pydantic_kwargs)
