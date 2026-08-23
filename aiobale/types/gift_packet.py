from typing import TYPE_CHECKING, Optional
from pydantic import Field, model_validator

from ..enums import GivingType
from .base import BaleObject
from .values import StringValue, BoolValue


class GiftPacket(BaleObject):
    """
    Represents a packet of gifts that can be distributed among users.

    Used in scenarios like sending monetary gifts in a group or channel.  
    Includes information such as total amount, number of recipients, message, and distribution type.
    """

    count: int = Field(0, alias="1")
    """Number of recipients who can claim the gift."""

    total_amount: int = Field(0, alias="2")
    """Total amount of the gift to be distributed."""

    giving_type: GivingType = Field(GivingType.SAME, alias="3")
    """Defines how the gift is distributed (e.g., equally or randomly)."""

    token: Optional[StringValue] = Field(None, alias="4")
    """A unique identifier or token for the gift packet (optional)."""

    message: StringValue = Field(..., alias="5")
    """Custom message that accompanies the gift packet."""

    owner_id: int = Field(None, alias="6")
    """User ID of the gift sender or owner (optional)."""

    show_amounts: BoolValue = Field(default_factory=lambda: BoolValue(value=False), alias="7")
    """Indicates whether the individual received amounts should be shown to recipients."""
    
    @model_validator(mode="before")
    @classmethod
    def _remove_empty_show_amounts(cls, data: dict) -> dict:
        if isinstance(data, dict):
            field_7 = data.get("7")
            if isinstance(field_7, dict) and not field_7:
                data.pop("7")
        return data

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            count: int = 0,
            total_amount: int = 0,
            giving_type: GivingType = GivingType.SAME,
            token: Optional[StringValue] = None,
            message: StringValue,
            owner_id: Optional[int] = None,
            show_amounts: Optional[BoolValue] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                count=count,
                total_amount=total_amount,
                giving_type=giving_type,
                token=token,
                message=message,
                owner_id=owner_id,
                show_amounts=show_amounts or BoolValue(value=False),
                **__pydantic_kwargs
            )
