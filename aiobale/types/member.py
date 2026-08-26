from __future__ import annotations
from pydantic import Field, model_validator
from typing import Dict, List, Optional, Any, TYPE_CHECKING

from .base import BaleObject
from .int_bool import IntBool
from .permissions import Permissions


class Member(BaleObject):
    """
    Represents a member of a Bale channel or group, including 
    information about their role, invitation, promotion, and permissions.

    All date fields represent timestamps in milliseconds since the Unix epoch.
    """

    id: int = Field(..., alias="1")
    """Unique identifier of the member (user ID)."""

    inviter_id: Optional[int] = Field(None, alias="2")
    """ID of the user who invited this member, if available."""

    date: Optional[int] = Field(None, alias="3")
    """Timestamp (ms) when the member joined (if numeric)."""

    title: Optional[str] = None
    """Display title or channel name if returned in field 3 by Bale."""

    name: Optional[str] = None
    """Alias for display title/name."""

    is_admin: IntBool = Field(False, alias="4")
    """Flag indicating whether the member is an admin (1 for True, 0 for False)."""

    promoted_by: Optional[int] = Field(None, alias="5")
    """ID of the user who promoted this member to admin, if applicable."""

    promoted_at: Optional[int] = Field(None, alias="6")
    """Timestamp (ms) when the member was promoted to admin."""

    permissions: Optional[List[Permissions]] = Field(None, alias="7")
    """List of permissions granted to the member.  
    Even if only one permission exists, it is normalized as a list.
    """

    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess incoming data to normalize field formats:

        - If a field is a dict with a single key "1", replace it with that value.
        - If field "3" is a text string rather than an integer timestamp,
          assign it to 'title'/'name' and avoid int parsing failures for 'date'.
        - Ensure integer fields are cleanly parsed or coerced.
        - Ensure 'permissions' ("7") is always a list, even if a single permission is provided.
        """
        if not isinstance(data, dict):
            return data

        fixed = {}
        for key, value in list(data.items()):
            # Unwrap nested dict like {"1": val}
            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                value = value["1"]

            if not value and value != 0 and value is not False:
                continue

            # Field "3" can be either integer timestamp (date) or string (title/name)
            if key == "3" or key == "date":
                if isinstance(value, int):
                    fixed["3"] = value
                elif isinstance(value, str):
                    if value.isdigit():
                        fixed["3"] = int(value)
                    else:
                        fixed["title"] = value
                        fixed["name"] = value
                continue

            # Field "7" (permissions) normalization to list
            if key == "7" or key == "permissions":
                if not isinstance(value, list):
                    fixed["7"] = [value]
                else:
                    fixed["7"] = value
                continue

            # Field "4" (is_admin) IntBool coercion
            if key == "4" or key == "is_admin":
                fixed["4"] = value
                continue

            # Numeric fields (1, 2, 5, 6)
            if key in ["1", "2", "5", "6", "id", "inviter_id", "promoted_by", "promoted_at"]:
                if isinstance(value, str) and value.isdigit():
                    fixed[key] = int(value)
                else:
                    fixed[key] = value
                continue

            fixed[key] = value

        return fixed

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            inviter_id: Optional[int] = None,
            date: Optional[int] = None,
            title: Optional[str] = None,
            name: Optional[str] = None,
            is_admin: IntBool = False,
            promoted_by: Optional[int] = None,
            promoted_at: Optional[int] = None,
            permissions: Optional[List[Permissions]] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                id=id,
                inviter_id=inviter_id,
                date=date,
                title=title,
                name=name,
                is_admin=is_admin,
                promoted_by=promoted_by,
                promoted_at=promoted_at,
                permissions=permissions,
                **__pydantic_kwargs,
            )
