from pydantic import Field
from typing import TYPE_CHECKING, Any

from .base import BaleObject
from .user import UserAuth


class ClientData(BaleObject):
    """
    Represents the client data associated with a user in the Bale system.

    This class contains information about the user's authentication and 
    the application/service they are interacting with.
    """

    id: int = Field(..., alias="user_id")
    """The unique identifier for the user. This is aliased as 'user_id'."""

    user: UserAuth
    """The authentication details of the user."""

    app_id: int
    """The identifier for the application the user is interacting with."""

    auth_id: str
    """The unique authentication ID for the user session."""

    auth_sid: int
    """The session ID associated with the user's authentication."""

    service: str
    """The name of the service the user is interacting with."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            user: UserAuth,
            app_id: int,
            auth_id: str,
            auth_sid: int,
            service: str,
            **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(
                id=id,
                user=user,
                app_id=app_id,
                auth_id=auth_id,
                auth_sid=auth_sid,
                service=service,
                **__pydantic_kwargs
            )
