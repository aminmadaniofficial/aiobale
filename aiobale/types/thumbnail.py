from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Union

from .base import BaleObject


class Thumbnail(BaleObject):
    """
    Represents a thumbnail image with size and image data.

    This is typically used to provide a small preview version of a media file.
    The image data can either be:
    - A URL (if the image is hosted remotely)
    - Raw bytes (if embedded directly in the structure)
    """

    w: int = Field(..., alias="1")
    """Width of the thumbnail in pixels."""

    h: int = Field(..., alias="2")
    """Height of the thumbnail in pixels."""

    image: Union[str, bytes] = Field(..., alias="3")
    """Thumbnail image data. Can be either:
    
    - `str`: a URL pointing to the image
    - `bytes`: raw image bytes (e.g., in base64 or binary format)
    """

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            w: int,
            h: int,
            image: Union[str, bytes],
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(w=w, h=h, image=image, **__pydantic_kwargs)
