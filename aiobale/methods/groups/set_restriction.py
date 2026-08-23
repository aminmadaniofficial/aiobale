from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer, StringValue
from ...types.responses import DefaultResponse
from ...enums import Services, Restriction
from ..base import BaleMethod


class SetRestriction(BaleMethod):
    """
    Sets a restriction for a user in a group.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "SetRestriction"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group in which the restriction is being applied.
    """

    restriction: Restriction = Field(..., alias="2")
    """
    The type of restriction to be applied to the user.
    """

    username: Optional[StringValue] = Field(None, alias="3")
    """
    The username of the user to whom the restriction is being applied. This field is optional.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            restriction: Restriction,
            username: Optional[StringValue] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                group=group,
                restriction=restriction,
                username=username,
                **__pydantic_kwargs
            )
