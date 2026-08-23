from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...types import ShortPeer, StringValue
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class MakeUserAdmin(BaleMethod):
    """
    Assigns admin privileges to a user in a specified group.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "MakeUserAdmin"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group in which the user is being promoted to admin.
    """

    user: ShortPeer = Field(..., alias="2")
    """
    The user who is being assigned admin privileges.
    """

    admin_name: Optional[StringValue] = Field(None, alias="3")
    """
    The custom name to assign to the admin (optional).
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            user: ShortPeer,
            admin_name: Optional[str] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                group=group, user=user, admin_name=admin_name, **__pydantic_kwargs
            )
