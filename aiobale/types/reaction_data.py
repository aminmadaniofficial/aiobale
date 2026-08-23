from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaleObject


class ReactionData(BaleObject):
    """
    Represents a reaction made by a user on a message or an entity in Bale.

    Contains the user's ID, the emoji used for the reaction, and the timestamp
    of when the reaction was made. All timestamps are in milliseconds since Unix epoch.
    """

    user_id: int = Field(..., alias="1")
    """The unique identifier of the user who made the reaction."""

    emoji: str = Field(..., alias="2")
    """The emoji character or string representing the reaction."""

    date: int = Field(..., alias="3")
    """The reaction timestamp in milliseconds since Unix epoch."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            user_id: int,
            emoji: str,
            date: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(user_id=user_id, emoji=emoji, date=date, **__pydantic_kwargs)
