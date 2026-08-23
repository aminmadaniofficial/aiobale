from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...enums import Services
from ..base import BaleMethod


class ValidatePassword(BaleMethod):
    """
    Validates a user's password for authentication purposes.

    Returns:
        aiobale.types.ValidatePassword: The result of password validation.
    """

    __service__ = Services.AUTH.value
    __method__ = "ValidatePassword"
    
    __returning__ = None

    transaction_hash: str = Field(..., alias="1")
    """
    The transaction hash associated with the authentication request.
    Used to uniquely identify the password validation transaction.
    """

    password: str = Field(..., alias="2")
    """
    The password provided by the user for validation.
    This should be the plain or hashed password depending on the authentication flow.
    """

    is_jwt: Optional[dict] = Field(default_factory=lambda: {"1": 1}, alias="3")
    """
    Indicates whether the authentication response should be in JWT format.
    If set, the response will include a JWT token.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            self,
            *,
            transaction_hash: str,
            password: str,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                transaction_hash=transaction_hash,
                password=password,
                **__pydantic_kwargs
            )
