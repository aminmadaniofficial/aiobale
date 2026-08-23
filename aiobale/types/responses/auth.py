from pydantic import Field
from typing import Optional, TYPE_CHECKING

from ..int_bool import IntBool
from ..base import BaleObject
from ...enums import SendCodeType


class Value(BaleObject):
    """
    A simple wrapper for a single integer value.

    Used in Bale's API for encapsulating numeric values such as timestamps or durations.
    """

    value: int = Field(..., alias="1")
    """The integer value. Can represent different units depending on context (e.g., milliseconds or seconds)."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            value: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(value=value, **__pydantic_kwargs)


class PhoneAuthResponse(BaleObject):
    """
    Response object for phone authentication requests in Bale.

    This response includes transaction info, registration status, code delivery method,
    expiration timing, and resend strategy. Time-related values follow two conventions:
    - `code_expiration_date` is a timestamp in **milliseconds**
    - `code_timeout` is a duration in **seconds**
    """

    transaction_hash: str = Field(..., alias="1")
    """Unique identifier for this authentication attempt, used in follow-up requests."""

    is_registered: IntBool = Field(False, alias="2")
    """Whether the phone number is already registered on Bale"""

    sent_code_type: SendCodeType = Field(..., alias="5")
    """The method used to send the authentication code (e.g., SMS, FlashCall)."""

    code_expiration_date: Value = Field(..., alias="6")
    """The absolute expiration time of the code, represented as a Unix timestamp in **milliseconds**."""

    next_send_code_type: Optional[SendCodeType] = Field(None, alias="7")
    """The method that will be used for the next code send, if needed."""

    code_timeout: Value = Field(..., alias="8")
    """How long (in **seconds**) the client should wait before being allowed to request a new code."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            transaction_hash: str,
            is_registered: IntBool,
            sent_code_type: SendCodeType,
            code_expiration_date: Value,
            next_send_code_type: Optional[SendCodeType] = None,
            code_timeout: Value,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                transaction_hash=transaction_hash,
                is_registered=is_registered,
                sent_code_type=sent_code_type,
                code_expiration_date=code_expiration_date,
                next_send_code_type=next_send_code_type,
                code_timeout=code_timeout,
                **__pydantic_kwargs
            )
