from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaleObject
from .peer import Peer


class ChatData(BaleObject):
    """
    Represents chat-related data in the Bale application.

    This class encapsulates information about a chat, including its associated peer.
    """

    peer: Peer = Field(..., alias="1")
    """
    The peer associated with this chat.

    This field represents the entity (user, group, or channel) that the chat is linked to.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(peer=peer, **__pydantic_kwargs)
