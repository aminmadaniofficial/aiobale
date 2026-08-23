from typing import TYPE_CHECKING, Optional
from pydantic import Field

from .base import BaleObject


class Winner(BaleObject):
    """
    Represents a user who received a portion of a gift packet.

    Contains information about the recipient's ID, the amount they received,
    and the timestamp when they claimed their share.
    """

    id: int = Field(..., alias="1")
    """Unique identifier of the recipient user."""

    amount: int = Field(0, alias="2")
    """The amount of the gift claimed by the user."""

    date: Optional[int] = Field(None, alias="3")
    """Unix timestamp (in milliseconds) indicating when the gift was received."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            amount: int = 0,
            date: Optional[int] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                id=id,
                amount=amount,
                date=date,
                **__pydantic_kwargs,
            )
