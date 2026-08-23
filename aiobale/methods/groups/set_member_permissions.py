from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer, Permissions
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class SetMemberPermissions(BaleMethod):
    """
    Sets permissions for a specific member in a group.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "SetMemberPermissions"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group where the member's permissions are being set.
    """

    user: ShortPeer = Field(..., alias="2")
    """
    The user whose permissions are being updated.
    """

    permissions: Permissions = Field(..., alias="3")
    """
    The new permissions to be assigned to the user.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            user: ShortPeer,
            permissions: Permissions,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                group=group, user=user, permissions=permissions, **__pydantic_kwargs
            )
