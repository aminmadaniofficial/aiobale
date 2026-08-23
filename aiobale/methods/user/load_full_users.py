from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types import InfoPeer
from ...types.responses import FullUsersResponse
from ...enums import Services
from ..base import BaleMethod


class LoadFullUsers(BaleMethod):
    """
    Loads detailed information about specified users.

    Returns:
        aiobale.types.responses.FullUsersResponse: The response containing full user details.
    """

    __service__ = Services.USER.value
    __method__ = "LoadFullUsers"

    __returning__ = FullUsersResponse

    peers: List[InfoPeer] = Field(..., alias="1")
    """
    A list of peers (users or groups) for which detailed information is requested.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, peers: List[InfoPeer], **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(peers=peers, **__pydantic_kwargs)
