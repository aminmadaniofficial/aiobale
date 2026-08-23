from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer
from ...types.responses import DefaultResponse
from ...enums import Services, TypingMode
from ..base import BaleMethod


class StopTyping(BaleMethod):
    """
    Stops the typing indicator for a specific peer and typing mode.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.PRESENCE.value
    __method__ = "StopTyping"

    __returning__ = DefaultResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (chat or user) for which the typing indicator should be stopped.
    """

    typing_type: TypingMode = Field(..., alias="2")
    """
    The type of typing activity (e.g., text, audio) to stop.
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
            super().__init__(
                peer=peer,
                typing_type=typing_type,
                **__pydantic_kwargs
            )
