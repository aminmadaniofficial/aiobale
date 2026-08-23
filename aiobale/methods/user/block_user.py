from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types import InfoPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class BlockUser(BaleMethod):
    """
    Blocks a user by specifying their peer information.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the block operation.
    """

    __service__ = Services.USER.value
    __method__ = "BlockUser"

    __returning__ = DefaultResponse

    peer: InfoPeer = Field(..., alias="1")
    """
    The peer (user or chat) to be blocked.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, peer: InfoPeer, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(peer=peer, **__pydantic_kwargs)
