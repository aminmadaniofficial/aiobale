from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer
from ...types.responses import JoinedGroupResponse
from ...enums import Services
from ..base import BaleMethod


class JoinPublicGroup(BaleMethod):
    """
    Joins a public group using the provided peer information.

    Returns:
        aiobale.types.responses.JoinedGroupResponse: The response containing details of the joined group.
    """

    __service__ = Services.GROUPS.value
    __method__ = "JoinPublicGroup"

    __returning__ = JoinedGroupResponse

    peer: Peer = Field(..., alias="1")
    """
    The peer (public group) to join.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(__pydantic__self__, *, peer: Peer, **__pydantic_kwargs) -> None:
            super().__init__(peer=peer, **__pydantic_kwargs)
