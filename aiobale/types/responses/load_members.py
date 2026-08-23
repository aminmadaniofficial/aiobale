from __future__ import annotations

from typing import List, Dict, Any, TYPE_CHECKING
from pydantic import Field, model_validator

from ..base import BaleObject
from ..member import Member


class MembersResponse(BaleObject):
    """
    Response model representing a list of members.

    Attributes:
        members (List[Member]): A list of members returned by the response.
            This field is always normalized to a list, even if the server
            returns a single member.
    """

    members: List[Member] = Field(default_factory=list, alias="1")
    """List of members included in the response."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates and normalizes the 'members' field (alias '1').

        Ensures that if the server returns a single Member object instead of a list,
        it will be wrapped into a list to maintain consistency.
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
            members: List[Member] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(members=members, **__pydantic_kwargs)
