from pydantic import Field
from typing import TYPE_CHECKING

from ...types.responses import JoinedGroupResponse
from ...enums import Services
from ..base import BaleMethod


class JoinGroup(BaleMethod):
    """
    Joins a group using the provided token.

    Returns:
        aiobale.types.responses.JoinedGroupResponse: The response containing details of the joined group.
    """

    __service__ = Services.GROUPS.value
    __method__ = "JoinGroup"

    __returning__ = JoinedGroupResponse

    token: str = Field(..., alias="1")
    """
    The token used to join the group.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            token: str,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                token=token,
                **__pydantic_kwargs
            )
