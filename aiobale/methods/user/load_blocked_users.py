from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types.responses import BlockedUsersResponse
from ...enums import Services
from ..base import BaleMethod


class LoadBlockedUsers(BaleMethod):
    """
    Loads the list of users blocked by the current user.

    Returns:
        aiobale.types.responses.BlockedUsersResponse: The response containing the list of blocked users.
    """

    __service__ = Services.USER.value
    __method__ = "LoadBlockedUsers"

    __returning__ = BlockedUsersResponse
