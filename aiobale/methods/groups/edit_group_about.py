from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer, StringValue
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class EditGroupAbout(BaleMethod):
    """
    Edits the 'about' section of a group.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the result of the edit operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "EditGroupAbout"
    
    __returning__ = DefaultResponse
    
    group: ShortPeer = Field(..., alias="1")
    """
    The group whose 'about' section is to be edited.
    """

    random_id: int = Field(..., alias="2")
    """
    A unique random identifier to ensure idempotency of the request.
    """

    about: StringValue = Field(..., alias="3")
    """
    The new 'about' text to be set for the group.
    """
    
    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            random_id: int,
            about: StringValue,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                random_id=random_id,
                group=group,
                about=about,
                **__pydantic_kwargs
            )
