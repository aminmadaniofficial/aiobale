from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import BannedUsersResponse
from ...enums import Services
from ..base import BaleMethod


class GetBannedUsers(BaleMethod):
    """
    Retrieves the list of banned users from a specified group.

    Returns:
        aiobale.types.responses.BannedUsersResponse: The response containing banned users information.
    """

    __service__ = Services.GROUPS.value
    __method__ = "GetBannedUsers"

    __returning__ = BannedUsersResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group from which banned users are to be retrieved.
    Should be provided as a ShortPeer instance representing the target group.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, group: ShortPeer, **__pydantic_kwargs
        ) -> None:
            super().__init__(group=group, **__pydantic_kwargs)
