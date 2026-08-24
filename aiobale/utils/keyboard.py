from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class InlineKeyboardButton(BaseModel):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = Field(default=None, alias="callback_data")


class ReplyKeyboardButton(BaseModel):
    text: str


class InlineKeyboardBuilder:
    """
    Fluid builder for constructing Inline Keyboards.
    
    Example:
        builder = InlineKeyboardBuilder()
        builder.button(text="وبسایت", url="https://aiobale.ir")
        builder.button(text="کلیک", callback_data="btn_click")
        builder.adjust(2)
        markup = builder.as_markup()
    """
    def __init__(self) -> None:
        self._buttons: List[InlineKeyboardButton] = []

    @property
    def buttons(self) -> List[InlineKeyboardButton]:
        return self._buttons

    def button(
        self,
        text: str,
        url: Optional[str] = None,
        callback_data: Optional[str] = None
    ) -> InlineKeyboardBuilder:
        self._buttons.append(InlineKeyboardButton(text=text, url=url, callback_data=callback_data))
        return self

    def add(self, *buttons: InlineKeyboardButton) -> InlineKeyboardBuilder:
        self._buttons.extend(buttons)
        return self

    def row(self, *buttons: InlineKeyboardButton) -> InlineKeyboardBuilder:
        self._buttons.extend(buttons)
        return self

    def attach(self, builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
        self._buttons.extend(builder._buttons)
        return self

    def adjust(self, *sizes: int) -> List[List[InlineKeyboardButton]]:
        if not sizes:
            sizes = (1,)
        result: List[List[InlineKeyboardButton]] = []
        buttons_copy = self._buttons.copy()
        size_idx = 0

        while buttons_copy:
            current_size = sizes[size_idx % len(sizes)]
            chunk = buttons_copy[:current_size]
            result.append(chunk)
            buttons_copy = buttons_copy[current_size:]
            size_idx += 1

        return result

    def as_markup(self, *sizes: int) -> List[List[Dict[str, Any]]]:
        grid = self.adjust(*sizes) if sizes else [[b] for b in self._buttons]
        return [[b.model_dump(exclude_none=True) for b in row] for row in grid]


class ReplyKeyboardBuilder:
    """
    Fluid builder for constructing Reply/Menu Keyboards.
    
    Example:
        builder = ReplyKeyboardBuilder()
        builder.button(text="ارسال موقعیت")
        builder.button(text="تماس با پشتیبانی")
        builder.adjust(2)
        markup = builder.as_markup()
    """
    def __init__(self) -> None:
        self._buttons: List[ReplyKeyboardButton] = []

    @property
    def buttons(self) -> List[ReplyKeyboardButton]:
        return self._buttons

    def button(self, text: str) -> ReplyKeyboardBuilder:
        self._buttons.append(ReplyKeyboardButton(text=text))
        return self

    def add(self, *buttons: ReplyKeyboardButton) -> ReplyKeyboardBuilder:
        self._buttons.extend(buttons)
        return self

    def row(self, *buttons: ReplyKeyboardButton) -> ReplyKeyboardBuilder:
        self._buttons.extend(buttons)
        return self

    def attach(self, builder: ReplyKeyboardBuilder) -> ReplyKeyboardBuilder:
        self._buttons.extend(builder._buttons)
        return self

    def adjust(self, *sizes: int) -> List[List[ReplyKeyboardButton]]:
        if not sizes:
            sizes = (1,)
        result: List[List[ReplyKeyboardButton]] = []
        buttons_copy = self._buttons.copy()
        size_idx = 0

        while buttons_copy:
            current_size = sizes[size_idx % len(sizes)]
            chunk = buttons_copy[:current_size]
            result.append(chunk)
            buttons_copy = buttons_copy[current_size:]
            size_idx += 1

        return result

    def as_markup(self, *sizes: int) -> List[List[Dict[str, Any]]]:
        grid = self.adjust(*sizes) if sizes else [[b] for b in self._buttons]
        return [[b.model_dump(exclude_none=True) for b in row] for row in grid]
