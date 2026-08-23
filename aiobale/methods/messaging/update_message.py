from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer, MessageContent
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class UpdateMessage(BaleMethod):
    """
    Updates the content of a specific message in a chat.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the update operation.
    """

    __service__ = Services.MESSAGING.value
    __method__ = "UpdateMessage"

    __returning__ = DefaultResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) where the message to be updated is located.
    """

    message_id: int = Field(..., alias="2")
    """
    The unique identifier of the message to be updated.
    """

    updated_message: MessageContent = Field(..., alias="3")
    """
    The new content to replace the existing message content.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_id: int,
            updated_message: MessageContent,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                peer=peer,
                message_id=message_id,
                updated_message=updated_message,
                **__pydantic_kwargs
            )
