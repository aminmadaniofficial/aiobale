from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ...types import Chat, Peer, MessageContent, InfoMessage
from ...types.responses import MessageResponse
from ...enums import Services
from ..base import BaleMethod


class SendMessage(BaleMethod):
    """
    Sends a message to a specified peer with the given content and optional reply.

    Returns:
        aiobale.types.responses.MessageResponse: The response containing the sent message details.
    """

    __service__ = Services.MESSAGING.value
    __method__ = "SendMessage"

    __returning__ = MessageResponse

    peer: Peer = Field(..., alias="1")
    """
    The recipient peer (chat or user) to whom the message is being sent.
    """

    message_id: int = Field(..., alias="2")
    """
    The unique identifier for the message being sent.
    """

    content: MessageContent = Field(..., alias="3")
    """
    The content of the message, which can include text, media, or other types.
    """

    reply_to: Optional[InfoMessage] = Field(None, alias="5")
    """
    The message to which this message is a reply, if applicable.
    """

    chat: Chat = Field(..., alias="6")
    """
    The chat context in which the message is being sent.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_id: int,
            content: MessageContent,
            reply_to: Optional[InfoMessage] = None,
            chat: Chat,
            **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(
                peer=peer,
                message_id=message_id,
                content=content,
                reply_to=reply_to,
                chat=chat,
                **__pydantic_kwargs
            )
