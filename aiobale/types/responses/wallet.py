from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING, Optional
from pydantic import Field, model_validator

from ..base import BaleObject
from ..wallet import Wallet


class WalletResponse(BaleObject):
    """
    Represents a response containing wallet information and optional user details.
    """

    wallet: Optional[Wallet] = Field(None, alias="1")
    """The user's wallet information, if available."""

    first_name: Optional[str] = Field(None, alias="2")
    """The first name of the wallet owner, if provided."""

    last_name: Optional[str] = Field(None, alias="3")
    """The last name of the wallet owner, if provided."""

    if TYPE_CHECKING:
        # This __init__ is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            wallet: Optional[Wallet] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                wallet=wallet,
                first_name=first_name,
                last_name=last_name,
                **__pydantic_kwargs
            )

    @model_validator(mode="before")
    @classmethod
    def _validate_wallets(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" in data and isinstance(data["1"], list):
            data["1"] = data["1"][0] if data["1"] else None

        for key in list(data.keys()):
            value = data[key]
            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

        return data
