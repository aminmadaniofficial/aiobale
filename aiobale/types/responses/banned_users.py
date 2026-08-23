from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING
from pydantic import Field, model_validator

from ..ban_data import BanData
from ..base import BaleObject


class BannedUsersResponse(BaleObject):
    """
    Represents the response for a banned users query.

    This structure is used to parse the response from Bale when requesting the list of banned users.
    Due to inconsistencies in the API, the `users` field may sometimes be returned as a single object
    instead of a list — this class handles that gracefully via a pre-validation step.
    """

    users: List[BanData] = Field(default_factory=list, alias="3")
    """A list of banned user records (may be a single object in raw API, handled via validator)."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures that the 'users' field is always a list, even if a single object is returned.

        Bale API sometimes returns a single `BanData` object instead of a list of them.
        This validator normalizes the data so `users` is always a list, which simplifies client-side logic.
        """
        if "3" not in data:
            return data

        if not isinstance(data["3"], list):
            data["3"] = [data["3"]]

        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            users: List[BanData],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(users=users, **__pydantic_kwargs)
