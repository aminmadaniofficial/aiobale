from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ...enums import Services
from ..base import BaleMethod


class ValidateCode(BaleMethod):
    """
    Validates the provided authentication code for a transaction.

    Returns:
        aiobale.types.ValidateCode: The result of the code validation process.
    """

    __service__ = Services.AUTH.value
    __method__ = "ValidateCode"

    __returning__ = None

    transaction_hash: str = Field(..., alias="1")
    """
    The unique hash representing the authentication transaction for which the code is being validated.
    """

    code: str = Field(..., alias="2")
    """
    The authentication code received by the user, typically via SMS or other means.
    """

    is_jwt: Optional[dict] = Field(default_factory=lambda: {"1": 1}, alias="3")
    """
    Optional dictionary indicating whether the response should include a JWT token.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            self, *, transaction_hash: str, code: str, **__pydantic_kwargs
        ) -> None:
            super().__init__(
                transaction_hash=transaction_hash, code=code, **__pydantic_kwargs
            )
