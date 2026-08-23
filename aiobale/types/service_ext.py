from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Optional

from .base import BaleObject


class GiftOpened(BaleObject):
    user_id: int = Field(..., alias="1")
    others_count: Optional[int] = Field(None, alias="2")
    message_id: int = Field(..., alias="3")
    message_date: int = Field(..., alias="4")


class ServiceExt(BaleObject):
    gift_opened: Optional[GiftOpened] = Field(None, alias="18")
