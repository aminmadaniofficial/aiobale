from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer
from ...types.responses import ReactionSentResponse
from ...enums import Services
from ..base import BaleMethod


class MessageRemoveReaction(BaleMethod):
    """
    Removes a reaction from a specified message in a chat.

    Returns:
        aiobale.types.responses.ReactionSentResponse: The response indicating the result of the reaction removal.
    """

    __service__ = Services.ABACUS.value
    __method__ = "MessageRemoveReaction"

    __returning__ = ReactionSentResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) where the target message is located.
    """

    message_id: int = Field(..., alias="2")
    """
    The unique identifier of the message from which the reaction will be removed.
    """

    emojy: str = Field(..., alias="3")
    """
    The emoji representing the reaction to be removed from the message.
    """

    date: int = Field(..., alias="4")
    """
    The timestamp (Unix time) when the reaction removal is requested.
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
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                peer=peer,
                message_id=message_id,
                date=date,
                emojy=emojy,
                **__pydantic_kwargs
            )
