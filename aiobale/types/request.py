from pydantic import Field
from typing import Any, List, Optional, TYPE_CHECKING

from .ext import ExtData
from .base import BaleObject
from .auth import AuthBody
from .values import IntValue


class MetaList(BaleObject):
    """
    Container for a list of extended metadata entries.

    This class wraps multiple `ExtData` objects into a single structure,
    facilitating passing and handling metadata collections.
    """

    meta_list: List[ExtData] = Field(..., alias="1")
    """List of extended metadata items, each describing a key-value pair with typed values."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            meta_list: List[ExtData],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(meta_list=meta_list, **__pydantic_kwargs)


class RequestBody(BaleObject):
    """
    Represents the body of a request sent to the Bale service.

    Attributes like `service` and `method` specify the target endpoint,
    while `payload` contains the optional data sent with the request.
    `metadata` holds extended information such as authentication tokens, 
    timestamps (in milliseconds), or other contextual data.
    `request_id` uniquely identifies this request for matching responses.
    """

    service: str = Field(..., alias="1")
    """The name of the Bale service being requested (e.g., 'bale.messaging.v2.Messaging', 'user')."""

    method: str = Field(..., alias="2")
    """The method or action name within the service (e.g., 'SendMessage')."""

    payload: Optional[Any] = Field(None, alias="3")
    """Optional data payload associated with the request.  
    Can be any serializable structure depending on the method."""

    metadata: MetaList = Field(..., alias="4")
    """Extended metadata for the request, such as auth data and timestamps (all dates as millisecond timestamps)."""

    request_id: int = Field(..., alias="5")
    """Unique identifier for this request, useful for matching responses and debugging."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            service: str,
            method: str,
            payload: Optional[Any] = None,
            metadata: MetaList,
            request_id: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                service=service,
                method=method,
                payload=payload,
                metadata=metadata,
                request_id=request_id,
                **__pydantic_kwargs,
            )


class Request(BaleObject):
    """
    Represents a general Bale request envelope.

    This can contain either:
    - `body`: the main request body with detailed data,
    - `ping`: an optional field often used for keep-alive or heartbeat (opaque),
    - `handshake`: authentication-related data for initial connection setup.

    Only one of these is expected to be non-null at a time.
    """

    body: Optional[RequestBody] = Field(None, alias="1")
    """The main request body, containing the service call and payload."""

    ping: Optional[IntValue] = Field(None, alias="2")
    """Optional ping or heartbeat data, using for keep-alive."""

    handshake: Optional[AuthBody] = Field(None, alias="3")
    """Authentication handshake data used when establishing a session."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            body: Optional[RequestBody] = None,
            ping: Optional[IntValue] = None,
            handshake: Optional[AuthBody] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                body=body,
                ping=ping,
                handshake=handshake,
                **__pydantic_kwargs,
            )
