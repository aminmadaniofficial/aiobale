from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .base import Filter

if TYPE_CHECKING:
    from ..types.message import Message


class IsText(Filter):
    """
    Filter to check if the message contains text content.
    """

    async def __call__(self, event: Any) -> bool:
        return getattr(event, "text", None) is not None


class IsDocument(Filter):
    """
    Filter to check if the message contains a document.
    """

    async def __call__(self, event: Any) -> bool:
        return getattr(event, "document", None) is not None


class IsGift(Filter):
    """
    Filter to check if the message contains a gift packet.
    """

    async def __call__(self, event: Any) -> bool:
        return getattr(event, "gift", None) is not None


class IsMedia(Filter):
    """
    Filter to check if the message contains any media (photo, document, audio, video, voice, gif).
    """

    async def __call__(self, event: Any) -> bool:
        return getattr(event, "document", None) is not None
