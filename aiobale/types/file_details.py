from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel


class FileDetails(BaseModel):
    """
    Represents detailed information about a file in the Bale messenger system.

    This includes the file's name, size in bytes, MIME type to identify format,
    a unique file identifier, and an access hash used for authorization.
    """

    name: str
    """The name of the file including extension (e.g., 'photo.jpg')."""

    size: int
    """Size of the file in bytes."""

    mime_type: str
    """MIME type of the file (e.g., 'image/jpeg', 'application/pdf')."""

    file_id: int
    """Unique identifier assigned to the file."""

    access_hash: int
    """Access hash used for security and authorization related to the file."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            name: str,
            size: int,
            mime_type: str,
            file_id: int,
            access_hash: int,
            **__pydantic_kwargs,
        ) -> None:
            # This init is only used for type checking and IDE autocomplete.
            # It will not be included in runtime behavior.
            super().__init__(
                name=name,
                size=size,
                mime_type=mime_type,
                file_id=file_id,
                access_hash=access_hash,
                **__pydantic_kwargs,
            )
