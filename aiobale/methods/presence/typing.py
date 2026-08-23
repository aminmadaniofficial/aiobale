from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer
from ...types.responses import DefaultResponse
from ...enums import Services, TypingMode
from ..base import BaleMethod


class Typing(BaleMethod):
    """
    Indicates the typing status of a user in a chat.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the typing status update.
    """

    __service__ = Services.PRESENCE.value
    __method__ = "Typing"

    __returning__ = DefaultResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) where the typing status is being updated.
    """

    typing_type: TypingMode = Field(..., alias="3")
    """
    The type of typing status being indicated (e.g., typing, recording audio, etc.).
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            typing_type: TypingMode,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(peer=peer, typing_type=typing_type, **__pydantic_kwargs)
