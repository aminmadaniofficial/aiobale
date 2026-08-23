from typing import TYPE_CHECKING, Any, Dict, Optional
from pydantic import Field, model_validator

from .base import BaleObject
from .int_bool import IntBool


class Wallet(BaleObject):
    """
    Represents the user's wallet containing account information, balance, and metadata.

    This object holds essential wallet-related data such as PAN, account number, balance,
    and whether the user is a merchant.
    """

    is_merchant: IntBool = Field(False, alias="1")
    """Indicates whether the user is a merchant account."""

    app: str = Field(..., alias="2")
    """The app or platform this wallet is associated with."""

    balance: int = Field(0, alias="3")
    """Current wallet balance in Rials (or the platform’s unit)."""

    token: str = Field(..., alias="4")
    """Unique token representing the wallet session or identity."""

    level: int = Field(0, alias="5")
    """Level or tier of the wallet (e.g., normal user, verified, etc.)."""

    pan: Optional[str] = Field(None, alias="6")
    """Partial or full PAN (Primary Account Number) of the connected card, if available."""

    account: Optional[str] = Field(None, alias="7")
    """Bank account number associated with the wallet, if any."""

    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pre-processes incoming data to flatten nested field structures.

        Some fields may arrive wrapped inside dicts with a single key '1'.
        This validator simplifies such fields before model parsing.
        """
        for key in list(data.keys()):
            value = data[key]
            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]
        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            is_merchant: IntBool = False,
            app: str,
            balance: int = 0,
            token: str,
            level: int = 0,
            pan: Optional[str] = None,
            account: Optional[str] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                is_merchant=is_merchant,
                app=app,
                balance=balance,
                token=token,
                level=level,
                pan=pan,
                account=account,
                **__pydantic_kwargs,
            )
