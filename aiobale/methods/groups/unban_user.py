from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class UnbanUser(BaleMethod):
    """
    Unbans a user from a group.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the unban operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "UnBanUser"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group from which the user is being unbanned.
    """

    user: ShortPeer = Field(..., alias="2")
    """
    The user who is being unbanned from the group.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            user: ShortPeer,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(group=group, user=user, **__pydantic_kwargs)
