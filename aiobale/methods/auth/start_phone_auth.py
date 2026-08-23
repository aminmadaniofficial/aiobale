from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...types.responses import PhoneAuthResponse
from ...enums import Services, SendCodeType
from ..base import BaleMethod


class StartPhoneAuth(BaleMethod):
    """
    Initiates the phone authentication process for a user.

    Returns:
        aiobale.types.responses.PhoneAuthResponse: The response containing authentication details and status.
    """

    __service__ = Services.AUTH.value
    __method__ = "StartPhoneAuth"
    
    __returning__ = PhoneAuthResponse

    phone_number: int = Field(..., alias="1")
    """
    The user's phone number to be authenticated.
    """

    app_id: int = Field(..., alias="2")
    """
    The application identifier used for authentication.
    """

    app_key: str = Field(..., alias="3")
    """
    The application key associated with the app_id for secure authentication.
    """

    device_hash: str = Field(..., alias="4")
    """
    Unique hash representing the user's device for identification.
    """

    device_title: str = Field(..., alias="5")
    """
    Human-readable title or name of the user's device.
    """

    send_code_type: SendCodeType = Field(..., alias="9")
    """
    The method or type used to send the authentication code (e.g., SMS, call).
    """

    options: Optional[dict] = Field(default_factory=lambda: {"0": 1}, alias="10")
    """
    Additional options for the authentication process, such as configuration flags.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            phone_number: int,
            app_id: int,
            app_key: str,
            device_hash: str,
            device_title: str,
            send_code_type: SendCodeType = SendCodeType.DEFAULT,
            options: Optional[dict] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                phone_number=phone_number,
                app_id=app_id,
                app_key=app_key,
                device_hash=device_hash,
                device_title=device_title,
                send_code_type=send_code_type,
                options=options,
                **__pydantic_kwargs
            )
