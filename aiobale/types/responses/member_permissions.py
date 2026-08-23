from __future__ import annotations

from typing import TYPE_CHECKING
from pydantic import Field

from ..base import BaleObject
from ..permissions import Permissions


class MemberPermissionsResponse(BaleObject):
    """
    Response model representing the permissions assigned to a member.

    Attributes:
        permissions (Permissions): The permissions object detailing what
            actions the member is allowed to perform.
    """

    permissions: Permissions = Field(..., alias="1")
    """Permissions assigned to the member."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            permissions: Permissions,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(permissions=permissions, **__pydantic_kwargs)
