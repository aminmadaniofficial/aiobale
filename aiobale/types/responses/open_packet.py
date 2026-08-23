from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING, List
from pydantic import Field, model_validator

from ..base import BaleObject
from ..winner import Winner
from ...enums import GiftOpenning


class PacketResponse(BaleObject):
    """
    Represents the response data when opening a gift packet, including
    the list of receivers, the opening status, and related statistics.
    """

    receivers: List[Winner] = Field(default_factory=list, alias="1")
    """List of users who received the gift."""

    status: GiftOpenning = Field(GiftOpenning.ALREADY_RECEIVED, alias="2")
    """The current status of the gift opening process."""

    openned_count: int = Field(..., alias="3")
    """The total number of times the gift has been opened."""

    win_amount: int = Field(..., alias="4")
    """The amount the current user won from the gift, if applicable."""

    rank: int = Field(..., alias="5")
    """The rank of the current user among all receivers."""

    if TYPE_CHECKING:
        # This __init__ is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            receivers: List[Winner] = [],
            status: GiftOpenning = GiftOpenning.ALREADY_RECEIVED,
            openned_count: int,
            win_amount: int,
            rank: int,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                receivers=receivers,
                status=status,
                openned_count=openned_count,
                win_amount=win_amount,
                rank=rank,
                **__pydantic_kwargs
            )

    @model_validator(mode="before")
    @classmethod
    def _validate_wallets(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" in data and not isinstance(data["1"], list):
            data["1"] = [data["1"]]

        if "4" in data:
            data["4"] = data["4"]["1"]
            
        if "5" in data:
            data["5"] = data["5"]["1"]

        return data
