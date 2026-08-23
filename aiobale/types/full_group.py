from typing import Any, Dict, List, Optional, TYPE_CHECKING
from pydantic import Field, model_validator

from ..enums import GroupType, PrivacyMode
from .base import BaleObject
from .int_bool import IntBool
from .full_user import ExInfo
from .member import Member
from .permissions import Permissions


class FullGroup(BaleObject):
    """
    Represents a complete group object in the Bale messaging platform.

    This model is returned when fetching full information about a group.
    It includes metadata such as title, owner, members, permissions,
    extended info (e.g. group type or verification), and visibility settings.
    """

    id: int = Field(..., alias="1")
    """Unique identifier of the group."""

    access_hash: Optional[int] = Field(None, alias="2")
    """Access hash used for accessing the group securely."""

    title: str = Field(..., alias="3")
    """Display name or title of the group."""

    owner_id: Optional[int] = Field(None, alias="5")
    """User ID of the group owner, if available."""

    created_at: Optional[int] = Field(None, alias="6")
    """Unix timestamp of when the group was created."""

    group_type: GroupType = Field(GroupType.GROUP, alias="7")
    """Type of the group (e.g., GROUP or CHANNEL)."""

    is_joined: IntBool = Field(False, alias="8")
    """Indicates whether the current user has joined the group."""

    members_count: int = Field(..., alias="10")
    """Total number of members in the group."""

    username: Optional[str] = Field(None, alias="11")
    """Public username (if the group has one)."""

    is_orphaned: IntBool = Field(False, alias="12")
    """True if the group has lost its owner or is in an orphaned state."""

    permissions: Optional[Permissions] = Field(None, alias="13")
    """Custom permissions configured for the group."""

    default_permissions: Optional[Permissions] = Field(None, alias="14")
    """Default permissions for new members in the group."""

    about: Optional[str] = Field(None, alias="16")
    """Group bio or description text."""

    members: Optional[List[Member]] = Field(None, alias="17")
    """Partial list of group members (may not be complete)."""

    ex_info: Optional[ExInfo] = Field(None, alias="18")
    """Extended info about the group, including:
    
    - `expeer_type`: Represents ChatType enum.
    - `identified`: Whether the group is verified (has blue badge).
    """

    available_reactions: List[str] = Field(default_factory=list, alias="24")
    """List of emoji/reactions that are allowed in the group."""

    is_suspend: IntBool = Field(False, alias="25")
    """True if the group is suspended by moderation."""

    privacy_mode: Optional[PrivacyMode] = Field(None, alias="28")
    """Defines who can see and join the group (e.g., public, private)."""

    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cleans up and normalizes incoming raw data before validation.

        - Fields with structure like {"1": value} are unwrapped to value.
        - Empty fields (None, empty dicts) are removed from the payload.
        - Field "4" is converted to a list if it's a single item.
        - Skips normalization for known structured fields: ex_info (18), permissions (13,14).
        """
        for key in list(data.keys()):
            value = data[key]

            if key in ["18", "13", "14"]:
                continue

            elif isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

            elif not value:
                data.pop(key)

            elif key == "4" and not isinstance(data[key], list):
                data[key] = [data[key]]

        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            access_hash: Optional[int] = None,
            title: str,
            owner_id: Optional[int] = None,
            created_at: Optional[int] = None,
            group_type: GroupType = GroupType.GROUP,
            is_joined: IntBool = False,
            members_count: int,
            username: Optional[str] = None,
            is_orphaned: IntBool = False,
            permissions: Optional[Permissions] = None,
            default_permissions: Optional[Permissions] = None,
            about: Optional[str] = None,
            members: Optional[List[Member]] = None,
            ex_info: Optional[ExInfo] = None,
            available_reactions: Optional[List[str]] = None,
            is_suspend: IntBool = False,
            privacy_mode: Optional[PrivacyMode] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                id=id,
                access_hash=access_hash,
                title=title,
                owner_id=owner_id,
                created_at=created_at,
                group_type=group_type,
                is_joined=is_joined,
                members_count=members_count,
                username=username,
                is_orphaned=is_orphaned,
                permissions=permissions,
                default_permissions=default_permissions,
                about=about,
                members=members,
                ex_info=ex_info,
                available_reactions=available_reactions or [],
                is_suspend=is_suspend,
                privacy_mode=privacy_mode,
                **__pydantic_kwargs
            )
