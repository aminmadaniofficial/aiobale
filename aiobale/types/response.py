from pydantic import Field
from typing import Any, Optional, TYPE_CHECKING

from .base import BaleObject
from .update import UpdateBody
from .values import IntValue


class BaleError(BaleObject):
    """
    Represents an error returned from the Bale API.

    Contains an error topic (code) and a human-readable message describing the error.
    """

    topic: int = Field(..., alias="1")
    """Numeric error code indicating the error category or type."""

    message: str = Field(..., alias="2")
    """Detailed error message explaining the cause or context."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            topic: int,
            message: str,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(topic=topic, message=message, **__pydantic_kwargs)


class ResponseBody(BaleObject):
    """
    Represents the body of a response from the Bale API.

    It can contain either an error, a result object, or both, along with a sequence number.
    """

    error: Optional[BaleError] = Field(None, alias="1")
    """Error details if the request failed."""

    result: Optional[Any] = Field(None, alias="2")
    """The successful result data of the request, type varies depending on the call."""

    number: int = Field(..., alias="3")
    """Sequence or request number for matching requests and responses."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            error: Optional[BaleError] = None,
            result: Optional[Any] = None,
            number: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(error=error, result=result, number=number, **__pydantic_kwargs)


class UpdateField(BaleObject):
    """
    Wrapper class for an update event body.

    Update events represent asynchronous server-pushed data, such as message updates.
    """

    body: UpdateBody = Field(..., alias="1")
    """The detailed body of the update event."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            body: UpdateBody,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(body=body, **__pydantic_kwargs)


class Response(BaleObject):
    """
    General response envelope from the Bale server.

    Contains either:
    - `response`: the result of a request,
    - `update`: pushed asynchronous update data,
    - `terminate_session`: signal to close the session,
    - `pong`: pong response for keep-alive,
    - `handshake`: handshake info for session establishment.
    """

    response: Optional[ResponseBody] = Field(None, alias="1")
    """The main response to a request, including results or errors."""

    update: Optional[UpdateField] = Field(None, alias="2")
    """Asynchronous update data pushed by the server."""

    terminate_session: Optional[Any] = Field(None, alias="3")
    """Signal to terminate the current session. Content is opaque."""

    pong: Optional[IntValue] = Field(None, alias="4")
    """Pong response to a ping, used for keep-alive."""

    handshake: Optional[Any] = Field(None, alias="5")
    """Handshake data used during session establishment."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            response: Optional[ResponseBody] = None,
            update: Optional[UpdateField] = None,
            terminate_session: Optional[Any] = None,
            pong: Optional[IntValue] = None,
            handshake: Optional[Any] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                response=response,
                update=update,
                terminate_session=terminate_session,
                pong=pong,
                handshake=handshake,
                **__pydantic_kwargs,
            )
