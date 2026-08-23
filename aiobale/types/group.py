from typing import List, Optional, TYPE_CHECKING
from pydantic import Field, model_validator

from ..enums import GroupType, Restriction
from .base import BaleObject
from .int_bool import IntBool
from .permissions import Permissions


class Group(BaleObject):
    """
    Represents a Bale group or channel with metadata, member information,
    permissions, and other configuration.

    This class is used for both regular groups and channels, with support for
    determining visibility, membership, permissions, and moderation options.
    """

    id: int = Field(..., alias="1")
    """Unique group ID."""

    access_hash: Optional[int] = Field(None, alias="2")
    """Access hash used for joining or accessing the group securely."""

    title: str = Field(..., alias="3")
    """Title (display name) of the group or channel."""

    is_member: IntBool = Field(False, alias="5")
    """Indicates if the current user is a member of this group."""

    is_hidden: IntBool = Field(False, alias="12")
    """Marks the group as hidden (not shown in standard lists)."""

    group_type: GroupType = Field(GroupType.GROUP, alias="15")
    """Type of group: regular group or channel."""

    can_send_message: IntBool = Field(False, alias="16")
    """Whether the current user can send messages to this group."""

    username: Optional[str] = Field(None, alias="17")
    """Public username (if set) that allows joining via @username."""

    is_orphaned: IntBool = Field(False, alias="18")
    """Indicates if the group is orphaned (original creator or context missing)."""

    members_count: int = Field(..., alias="20")
    """Current number of members in the group."""

    permissions: Optional[Permissions] = Field(None, alias="30")
    """Current permissions for regular members of the group."""

    default_permissions: Optional[Permissions] = Field(None, alias="31")
    """Default permissions applied to new members."""

    owner_id: Optional[int] = Field(None, alias="32")
    """User ID of the group owner, if available."""

    available_reactions: List[str] = Field(default_factory=list, alias="33")
    """List of allowed emoji reactions in the group."""

    is_suspend: IntBool = Field(False, alias="36")
    """Indicates if the group is currently suspended."""

    restriction: Restriction = Field(Restriction.PRIVATE, alias="40")
    """Restriction level of the group (e.g. public, private)."""

    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data):
        """
        Cleans incoming data by:
        - Unwrapping single-field dicts (e.g. {'1': value}) into raw values
        - Removing falsey values (None, empty strings, etc.)
        - Ensuring 'available_reactions' is always a list
        """
        from typing import Any, Dict  # moved inside to avoid unnecessary top-level import
        if not isinstance(data, dict):
            return data

        fixed = {}
        for key, value in data.items():
            if isinstance(value, dict) and set(value.keys()) == {"1"}:
                fixed[key] = value["1"]
            elif key == "33" and not isinstance(value, list):
                fixed[key] = [value]
            elif value:
                fixed[key] = value
        return fixed

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            access_hash: Optional[int] = None,
            title: str,
            is_member: IntBool = False,
            is_hidden: IntBool = False,
            group_type: GroupType = GroupType.GROUP,
            can_send_message: IntBool = False,
            username: Optional[str] = None,
            is_orphaned: IntBool = False,
            members_count: int,
            permissions: Optional[Permissions] = None,
            default_permissions: Optional[Permissions] = None,
            owner_id: Optional[int] = None,
            available_reactions: Optional[List[str]] = None,
            is_suspend: IntBool = False,
            restriction: Restriction = Restriction.PRIVATE,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                id=id,
                access_hash=access_hash,
                title=title,
                is_member=is_member,
                is_hidden=is_hidden,
                group_type=group_type,
                can_send_message=can_send_message,
                username=username,
                is_orphaned=is_orphaned,
                members_count=members_count,
                permissions=permissions,
                default_permissions=default_permissions,
                owner_id=owner_id,
                available_reactions=available_reactions or [],
                is_suspend=is_suspend,
                restriction=restriction,
                **__pydantic_kwargs
            )
