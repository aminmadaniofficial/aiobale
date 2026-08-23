from typing import List, TYPE_CHECKING
from pydantic import Field

from ..base import BaleObject
from ..ext import ExtKeyValue


class ParametersResponse(BaleObject):
    """
    Response model representing a list of key-value parameters.

    Attributes:
        params (List[ExtKeyValue]): A list of key-value pairs representing
            parameters returned from the server. Always normalized as a list.
    """

    params: List[ExtKeyValue] = Field(default_factory=list, alias="1")
    """List of key-value parameter pairs."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            params: List[ExtKeyValue] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(params=params, **__pydantic_kwargs)
