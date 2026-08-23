from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ...enums import Services
from ..base import BaleMethod


class SignUp(BaleMethod):
    __service__ = Services.AUTH.value
    __method__ = "SignUp"

    __returning__ = None

    transaction_hash: str = Field(..., alias="1")
    """
    The unique hash representing the authentication transaction.
    """

    name: str = Field(..., alias="2")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            self, *, transaction_hash: str, name: str, **__pydantic_kwargs
        ) -> None:
            super().__init__(
                transaction_hash=transaction_hash, name=name, **__pydantic_kwargs
            )
