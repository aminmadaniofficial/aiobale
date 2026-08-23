from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class RemoveUserAdmin(BaleMethod):
    """
    Removes a user from the admin list of a group.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "RemoveUserAdmin"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group from which the user is being removed as an admin.
    """

    user: ShortPeer = Field(..., alias="2")
    """
    The user who is being removed from the admin list.
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
