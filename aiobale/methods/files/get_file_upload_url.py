from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...types import Chat, SendTypeModel, FileUploadInfo
from ...enums import Services
from ..base import BaleMethod


class GetFileUploadUrl(BaleMethod):
    """
    Requests a URL for uploading a file to the Bale server.

    Returns:
        aiobale.types.FileUploadInfo: The information required for file upload.
    """

    __service__ = Services.FILES.value
    __method__ = "GetNasimFileUploadUrl"

    __returning__ = FileUploadInfo

    expected_size: int = Field(..., alias="1")
    """
    The expected size of the file to be uploaded, in bytes.
    """

    user_id: int = Field(..., alias="3")
    """
    The unique identifier of the user requesting the upload URL.
    """

    name: str = Field(..., alias="4")
    """
    The name of the file to be uploaded.
    """

    mime_type: str = Field(..., alias="5")
    """
    The MIME type of the file (e.g., 'image/png', 'application/pdf').
    """

    chat: Optional[Chat] = Field(None, alias="6")
    """
    The chat context in which the file will be used, if applicable.
    """

    send_type: Optional[SendTypeModel] = Field(None, alias="7")
    """
    The type of sending operation for the file (e.g., as a message, as a media).
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            expected_size: int,
            user_id: int,
            name: int,
            mime_type: int,
            chat: Chat,
            send_type: Optional[SendTypeModel],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                expected_size=expected_size,
                user_id=user_id,
                name=name,
                mime_type=mime_type,
                chat=chat,
                send_type=send_type,
                **__pydantic_kwargs
            )
