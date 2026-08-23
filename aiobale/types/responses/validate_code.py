from typing import TYPE_CHECKING
from pydantic import Field

from ..base import BaleObject
from ..user import UserAuth
from ..values import StringValue


class ValidateCodeResponse(BaleObject):
    """
    Response returned after validating a code (e.g., authentication code).

    Attributes:
        user (UserAuth): Authenticated user details returned after successful validation.
        jwt (Value): JSON Web Token as a wrapped string value, used for subsequent authentication.
    """

    user: UserAuth = Field(..., alias="2")
    """Authenticated user information."""

    jwt: StringValue = Field(..., alias="4")
    """Authentication token wrapped in a Value object."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            user: UserAuth = ...,
            jwt: StringValue = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(user=user, jwt=jwt, **__pydantic_kwargs)
