from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer
from ...types.responses import ReactionSentResponse
from ...enums import Services
from ..base import BaleMethod


class MessageSetReaction(BaleMethod):
    """
    Sets a reaction (emoji) on a specific message in a chat.

    Returns:
        aiobale.types.responses.ReactionSentResponse: The response indicating the result of setting the reaction.
    """

    __service__ = Services.ABACUS.value
    __method__ = "MessageSetReaction"

    __returning__ = ReactionSentResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) where the target message is located.
    """

    message_id: int = Field(..., alias="2")
    """
    The unique identifier of the message to which the reaction will be added.
    """

    emojy: str = Field(..., alias="3")
    """
    The emoji string representing the reaction to be set on the message.
    """

    date: int = Field(..., alias="4")
    """
    The timestamp (in seconds) when the reaction is set.
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
