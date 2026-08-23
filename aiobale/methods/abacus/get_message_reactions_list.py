from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer
from ...types.responses import ReactionListResponse
from ...enums import Services
from ..base import BaleMethod


class GetMessageReactionsList(BaleMethod):
    """
    Represents the BaleMethod for retrieving the list of reactions for a specific message.
    
    Returns: 
        aiobale.types.responses.ReactionListResponse: The response containing reactions data.
    """

    __service__ = Services.ABACUS.value
    __method__ = "GetMessageReactionsList"

    __returning__ = ReactionListResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) where the message is located.
    """

    message_id: int = Field(..., alias="2")
    """
    The unique identifier of the message for which reactions are requested.
    """

    date: int = Field(..., alias="3")
    """
    The timestamp of the message, used for filtering or pagination.
    """

    emojy: str = Field(..., alias="4")
    """
    The emoji string to filter reactions by a specific emoji.
    """

    page: int = Field(..., alias="5")
    """
    The page number for paginated results.
    """

    limit: int = Field(..., alias="6")
    """
    The maximum number of reactions to return per page.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_id: int,
            date: int,
            emojy: str,
            page: int,
            limit: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                peer=peer,
                message_id=message_id,
                date=date,
                emojy=emojy,
                page=page,
                limit=limit,
                **__pydantic_kwargs
            )
