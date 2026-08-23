import time
from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types.responses import NickNameAvailable
from ...enums import Services
from ..base import BaleMethod


class CheckNickName(BaleMethod):
    """
    Checks the availability of a given nickname for a user.

    Returns:
        aiobale.types.responses.NickNameAvailable: The response indicating whether the nickname is available.
    """

    __service__ = Services.USER.value
    __method__ = "CheckNickName"

    __returning__ = NickNameAvailable

    nick_name: str = Field(..., alias="1")
    """
    The nickname to be checked for availability.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, nick_name: str, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(nick_name=nick_name, **__pydantic_kwargs)
