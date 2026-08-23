from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING
from pydantic import Field, model_validator

from ..short_peer import ShortPeer
from ..group import Group
from .default import DefaultResponse


class GroupCreatedResponse(DefaultResponse):
    """
    Response returned after successfully creating a group.

    Contains information about the created group, invited users, users 
    who couldn't be added, and an invite link to share. Some fields are 
    normalized to lists for consistent downstream handling.
    """

    group: Group = Field(default=None, alias="3")
    """The newly created group object."""

    users: List[ShortPeer] = Field(default_factory=list, alias="5")
    """List of users who were successfully added to the group."""

    not_added_users: List[ShortPeer] = Field(default_factory=list, alias="6")
    """List of users who could not be added to the group (e.g., blocked or privacy settings)."""

    invite_link: str = Field(..., alias="7")
    """Invite link to share access to the created group."""

    @model_validator(mode="before")
    @classmethod
    def normalize_lists(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures that the 'users' and 'not_added_users' fields (aliases '5' and '6')
        are always lists. If the server returns a single item, it's wrapped in a list.
        """
        for key in ("5", "6"):
            value = data.get(key)
            if value is not None and not isinstance(value, list):
                data[key] = [value]
        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: Group = None,
            users: List[ShortPeer] = ...,
            not_added_users: List[ShortPeer] = ...,
            invite_link: str,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                group=group,
                users=users,
                not_added_users=not_added_users,
                invite_link=invite_link,
                **__pydantic_kwargs,
            )
