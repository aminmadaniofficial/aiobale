from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types import InfoPeer
from ...types.responses import UsersResponse
from ...enums import Services
from ..base import BaleMethod


class LoadUsers(BaleMethod):
    """
    Loads user information for the specified peers.

    Returns:
        aiobale.types.responses.UsersResponse: The response containing user information.
    """

    __service__ = Services.USER.value
    __method__ = "LoadUsers"

    __returning__ = UsersResponse

    peers: List[InfoPeer] = Field(..., alias="1")
    """
    List of peers (users or groups) whose information is being requested.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, peers: List[InfoPeer], **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(peers=peers, **__pydantic_kwargs)
