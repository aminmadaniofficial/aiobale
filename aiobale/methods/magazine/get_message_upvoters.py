from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...types import InfoMessage, StringValue
from ...types.responses import UpvotersResponse
from ...enums import Services
from ..base import BaleMethod


class GetMessageUpvoters(BaleMethod):
    """
    Represents a request to retrieve the list of users who have upvoted a specific message.
    """

    __service__ = Services.MAGAZINE.value
    __method__ = "GetMessageUpvoters"

    __returning__ = UpvotersResponse

    load_more_state: Optional[StringValue] = Field(None, alias="1")
    """A token or state string for loading additional pages of upvoters."""

    message: InfoMessage = Field(..., alias="2")
    """The message for which upvoters should be retrieved."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            load_more_state: Optional[StringValue] = None,
            message: InfoMessage,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                message=message, load_more_state=load_more_state, **__pydantic_kwargs
            )
