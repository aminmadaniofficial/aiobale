from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, Dict, List

from .base import BaleObject
from ..types import InfoMessage


class Upvote(BaleObject):
    """
    Represents an upvote action containing one or more messages
    and a limit for the upvote operation.
    """

    messages: List[InfoMessage] = Field(..., alias="1")
    """List of messages to be upvoted."""

    limit: int = Field(..., alias="2")
    """The maximum number of upvotes allowed."""

    if TYPE_CHECKING:
        # This __init__ is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            messages: List[InfoMessage],
            limit: int,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(messages=messages, limit=limit, **__pydantic_kwargs)

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes the 'data' field (alias '1') to always be a list.
        """
        if "1" in data and not isinstance(data["1"], list):
            data["1"] = [data["1"]]

        return data
