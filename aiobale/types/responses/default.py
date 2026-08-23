from typing import Optional, TYPE_CHECKING
from pydantic import Field

from ..base import BaleObject


class DefaultResponse(BaleObject):
    """
    Base class for standard responses in the Bale messaging protocol.

    Most response objects inherit from this class, which provides:
    - `seq`: a sequence number for tracking message or request order.
    - `date`: a millisecond-based timestamp representing the server time 
      when the response was generated.

    These fields are typically included in nearly all API responses from Bale.
    """

    seq: Optional[int] = Field(None, alias="1")
    """Sequence number for ordering and synchronization of responses."""

    date: Optional[int] = Field(None, alias="2")
    """Server timestamp (in milliseconds) when this response was created."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            seq: Optional[int] = None,
            date: Optional[int] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(seq=seq, date=date, **__pydantic_kwargs)
