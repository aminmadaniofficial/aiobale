from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer
from ...types.responses import MemberPermissionsResponse
from ...enums import Services
from ..base import BaleMethod


class GetMemberPermissions(BaleMethod):
    """
    Retrieves the permissions of a specific member in a group.

    Returns:
        aiobale.types.responses.MemberPermissionsResponse: The response containing the member's permissions data.
    """

    __service__ = Services.GROUPS.value
    __method__ = "GetMemberPermissions"

    __returning__ = MemberPermissionsResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group from which the member's permissions are being queried.
    """

    user: ShortPeer = Field(..., alias="2")
    """
    The user whose permissions in the group are being retrieved.
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
