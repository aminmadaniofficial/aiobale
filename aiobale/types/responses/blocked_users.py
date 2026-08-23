from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING

from pydantic import Field, model_validator

from ..base import BaleObject
from ..info_peer import InfoPeer


class BlockedUsersResponse(BaleObject):
    """
    Represents the response received when querying the list of blocked users.

    This response includes a list of `InfoPeer` objects, each representing a user
    who has been blocked by the current user. If the server sends a single object
    instead of a list, it will be normalized to a list automatically.
    """

    users: List[InfoPeer] = Field(default_factory=list, alias="1")
    """List of users that have been blocked, represented as `InfoPeer` objects."""

    @model_validator(mode="before")
    @classmethod
    def normalize_users_field(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures that the 'users' field (alias '1') is always a list, even if the raw data is a single object.
        This prevents deserialization errors when the backend returns a single item instead of a list.
        """
        if "1" not in data:
            return data

        if not isinstance(data["1"], list):
            data["1"] = [data["1"]]

        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            users: List[InfoPeer] = [],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(users=users, **__pydantic_kwargs)
