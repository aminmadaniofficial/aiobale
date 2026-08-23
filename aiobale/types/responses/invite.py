from __future__ import annotations

from typing import List, Any, Dict, TYPE_CHECKING
from pydantic import Field, model_validator

from ..base import BaleObject
from ..peer import Peer


class InviteResponse(BaleObject):
    """
    Response model representing the result of an invitation request.

    Attributes:
        not_added_users (List[Peer]): List of users who could not be added
            via the invite. Normalized to always be a list for consistent handling.
    """

    not_added_users: List[Peer] = Field(default_factory=list, alias="1")
    """List of peers that were not added during the invite process."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates and normalizes the 'not_added_users' field (alias '1').

        Ensures that if the server returns a single Peer object instead of a list,
        it will be wrapped into a list for consistency.
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
            not_added_users: List[Peer] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(not_added_users=not_added_users, **__pydantic_kwargs)
