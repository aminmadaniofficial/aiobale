from __future__ import annotations

from typing import List, Any, Dict, TYPE_CHECKING
from pydantic import Field, model_validator

from ..base import BaleObject
from ..reaction import Reaction


class ReactionSentResponse(BaleObject):
    """
    Represents the response received after sending reactions.

    Attributes:
        reactions (List[Reaction]): A list of Reaction objects included in the response.
            This list is normalized to always be a list even if a single Reaction is returned.
    """

    reactions: List[Reaction] = Field(default_factory=list, alias="2")
    """List of reactions included in the response."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes the 'reactions' field (alias '2') in the input data.

        Ensures that if the server returns a single Reaction object instead of a list,
        it is wrapped into a list for consistency.
        """
        if "2" not in data:
            return data

        if not isinstance(data["2"], list):
            data["2"] = [data["2"]]

        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            reactions: List[Reaction] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(reactions=reactions, **__pydantic_kwargs)
