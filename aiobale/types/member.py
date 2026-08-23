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
    """Timestamp (ms) when the member joined."""

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
          (This often happens due to nested Protobuf encoding.)
        - Remove keys with empty or falsy values to avoid storing meaningless data.
        - Ensure 'permissions' ("7") is always a list, even if a single permission is provided.
        """

        # Iterate over a copy of keys to allow modification during iteration
        for key in list(data.keys()):
            value = data[key]

            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

            elif not value:
                data.pop(key)

        # Normalize permissions field to always be a list if it exists and is not already a list
        if "7" in data and not isinstance(data["7"], list):
            data["7"] = [data["7"]]

        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            inviter_id: Optional[int] = None,
            date: Optional[int] = None,
            is_admin: IntBool = False,
            promoted_by: Optional[int] = None,
            promoted_at: Optional[int] = None,
            permissions: Optional[List[Permissions]] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                id=id,
                inviter_id=inviter_id,
                date=date,
                is_admin=is_admin,
                promoted_by=promoted_by,
                promoted_at=promoted_at,
                permissions=permissions,
                **__pydantic_kwargs
            )
