from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING
from pydantic import Field, model_validator

from ..short_peer import ShortPeer
from ..group import Group
from ..base import BaleObject


class JoinedGroupResponse(BaleObject):
    """
    Represents the response received when joining a group.

    Attributes:
        group (Group): The group that was joined.
        random_id (int): A unique random identifier for this join event.
        users (List[ShortPeer]): List of users currently in the group.
            Always normalized to a list for consistency.
        inviter_id (int): The identifier of the user who invited the current user.
        group_seq (int): Sequence number representing the group's state or version.
    """

    group: Group = Field(default=None, alias="1")
    """The joined group object."""

    random_id: int = Field(..., alias="6")
    """Unique random ID associated with the join operation."""

    users: List[ShortPeer] = Field(default_factory=list, alias="7")
    """List of users in the group; normalized to a list."""

    inviter_id: int = Field(..., alias="8")
    """User ID of the person who invited the current user to the group."""

    group_seq: int = Field(..., alias="9")
    """Sequence number indicating the version or update state of the group."""

    @model_validator(mode="before")
    @classmethod
    def normalize_lists(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures that the 'users' field (alias '7') is always a list.

        Wraps single user entries into a list for consistent downstream processing.
        """
        value = data.get("7")
        if value is not None and not isinstance(value, list):
            data["7"] = [value]
        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: Group = None,
            random_id: int,
            users: List[ShortPeer] = ...,
            inviter_id: int,
            group_seq: int,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                group=group,
                random_id=random_id,
                users=users,
                inviter_id=inviter_id,
                group_seq=group_seq,
                **__pydantic_kwargs,
            )
