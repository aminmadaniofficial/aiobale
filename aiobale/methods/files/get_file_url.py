from pydantic import Field
from typing import TYPE_CHECKING

from ...types import FileInfo
from ...types.responses import FileURLResponse
from ...enums import Services
from ..base import BaleMethod


class GetFileUrl(BaleMethod):
    """
    Retrieves the download URL for a specified file.

    Returns:
        aiobale.types.responses.FileURLResponse: The response containing the file URL.
    """

    __service__ = Services.FILES.value
    __method__ = "GetNasimFileUrl"

    __returning__ = FileURLResponse

    file: FileInfo = Field(..., alias="1")
    """
    Information about the file for which the download URL is requested.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, file: FileInfo, **__pydantic_kwargs
        ) -> None:
            super().__init__(file=file, **__pydantic_kwargs)
