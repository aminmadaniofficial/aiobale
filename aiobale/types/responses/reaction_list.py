from __future__ import annotations

from typing import List, Any, Dict, TYPE_CHECKING
from pydantic import Field, model_validator

from ..base import BaleObject
from ..reaction_data import ReactionData


class ReactionListResponse(BaleObject):
    """
    Response model containing a list of reaction data items.

    Attributes:
        data (List[ReactionData]): List of reactions returned by the server.
            Normalized to always be a list even if a single item is returned.
    """

    data: List[ReactionData] = Field(default_factory=list, alias="1")
    """List of reaction data items."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates and normalizes the 'data' field (alias '1').

        If the server returns a single ReactionData item instead of a list,
        it wraps it into a list to maintain consistency.
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
            data: List[ReactionData] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(data=data, **__pydantic_kwargs)
