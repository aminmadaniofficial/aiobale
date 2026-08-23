from pydantic import Field
from typing import TYPE_CHECKING, List

from ...types import Peer, OtherMessage
from ...types.responses import ReactionsResponse
from ...enums import Services
from ..base import BaleMethod


class GetMessagesReactions(BaleMethod):
    """
    Retrieves reactions for specified messages and their origins.
    
    Returns:
        aiobale.types.responses.ReactionsResponse: The response containing reactions data.
    """

    __service__ = Services.ABACUS.value
    __method__ = "GetMessagesReactions"

    __returning__ = ReactionsResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) from which the messages are being queried.
    """

    message_ids: List[OtherMessage] = Field(..., alias="2")
    """
    List of message identifiers for which reactions are requested.
    """

    origin_peer: Peer = Field(..., alias="3")
    """
    The original peer (chat or user) where the referenced messages originated.
    """

    origin_message_ids: List[OtherMessage] = Field(..., alias="4")
    """
    List of original message identifiers in the origin peer for which reactions are requested.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_ids: List[OtherMessage],
            origin_peer: Peer,
            origin_message_ids: List[OtherMessage],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                peer=peer,
                message_ids=message_ids,
                origin_peer=origin_peer,
                origin_message_ids=origin_message_ids,
                **__pydantic_kwargs
            )
