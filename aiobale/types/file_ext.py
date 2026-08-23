from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Optional

from .base import BaleObject


class PhotoExt(BaleObject):
    """
    Metadata extension for a photo file.

    Provides optional width and height of the image.
    """

    w: Optional[int] = Field(None, alias="1")
    """Photo width in pixels."""

    h: Optional[int] = Field(None, alias="2")
    """Photo height in pixels."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            w: Optional[int] = None,
            h: Optional[int] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(w=w, h=h, **__pydantic_kwargs)


class VideoExt(BaleObject):
    """
    Metadata extension for a video file.

    Includes optional width, height, and duration of the video.
    """

    w: Optional[int] = Field(None, alias="1")
    """Video width in pixels."""

    h: Optional[int] = Field(None, alias="2")
    """Video height in pixels."""

    duration: Optional[int] = Field(None, alias="3")
    """Video duration in seconds."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            w: Optional[int] = None,
            h: Optional[int] = None,
            duration: Optional[int] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(w=w, h=h, duration=duration, **__pydantic_kwargs)


class VoiceExt(BaleObject):
    """
    Metadata extension for a voice message.

    Contains only the optional duration field.
    """

    duration: Optional[int] = Field(None, alias="1")
    """Voice message duration in seconds."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            duration: Optional[int] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(duration=duration, **__pydantic_kwargs)


class AudioExt(BaleObject):
    """
    Metadata extension for an audio (music) file.

    Includes common music tags such as album, genre, and track name.
    """

    duration: Optional[int] = Field(None, alias="1")
    """Audio duration in seconds."""

    album: Optional[str] = Field(None, alias="2")
    """Album name from audio metadata."""

    genre: Optional[str] = Field(None, alias="3")
    """Genre of the audio."""

    track: Optional[str] = Field(None, alias="4")
    """Track title or name of the song."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            duration: Optional[int] = None,
            album: Optional[str] = None,
            genre: Optional[str] = None,
            track: Optional[str] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                duration=duration,
                album=album,
                genre=genre,
                track=track,
                **__pydantic_kwargs,
            )


class DocumentsExt(BaleObject):
    """
    Collection of optional metadata extensions for various document types.

    Depending on the file type (photo, video, voice, etc.), the corresponding
    extension field will be populated to describe its media attributes.

    - `gif` is treated similarly to a video, but semantically used for short loops.
    """

    photo: Optional[PhotoExt] = Field(None, alias="1")
    """Metadata for a photo file."""

    video: Optional[VideoExt] = Field(None, alias="2")
    """Metadata for a video file."""

    voice: Optional[VoiceExt] = Field(None, alias="3")
    """Metadata for a voice message."""

    gif: Optional[VideoExt] = Field(None, alias="4")
    """Metadata for a GIF file (handled as a video under the hood)."""

    audio: Optional[AudioExt] = Field(None, alias="5")
    """Metadata for an audio/music file."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            photo: Optional[PhotoExt] = None,
            video: Optional[VideoExt] = None,
            voice: Optional[VoiceExt] = None,
            gif: Optional[VideoExt] = None,
            audio: Optional[AudioExt] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                photo=photo,
                video=video,
                voice=voice,
                gif=gif,
                audio=audio,
                **__pydantic_kwargs,
            )
