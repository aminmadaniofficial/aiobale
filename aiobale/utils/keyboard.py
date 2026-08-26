from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class InlineKeyboardButton(BaseModel):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None
    copy_text: Optional[str] = None


class ReplyKeyboardButton(BaseModel):
    text: str


class InlineKeyboardBuilder:
    """
    Fluid builder for constructing Inline Keyboards.

    Example:
        builder = InlineKeyboardBuilder()
        builder.button(text="وبسایت", url="https://aiobale.ir")
        builder.button(text="کلیک", callback_data="btn_click")
        builder.button(text="کپی کد", copy_text="CODE123")
        builder.adjust(2)
        markup = builder.as_markup()
    """

    def __init__(self) -> None:
        self._buttons: List[InlineKeyboardButton] = []
        self._sizes: List[int] = []

    @property
    def buttons(self) -> List[InlineKeyboardButton]:
        return self._buttons

    def button(
        self,
        text: str,
        url: Optional[str] = None,
        callback_data: Optional[str] = None,
        copy_text: Optional[str] = None,
        **kwargs: Any,
    ) -> InlineKeyboardBuilder:
        self._buttons.append(
            InlineKeyboardButton(
                text=text,
                url=url,
                callback_data=callback_data,
                copy_text=copy_text,
                **kwargs,
            )
        )
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

    def adjust(self, *sizes: int) -> InlineKeyboardBuilder:
        self._sizes = list(sizes) if sizes else [1]
        return self

    def export(self, *sizes: int) -> List[List[InlineKeyboardButton]]:
        layout_sizes = list(sizes) if sizes else (self._sizes if self._sizes else [1])
        result: List[List[InlineKeyboardButton]] = []
        buttons_copy = self._buttons.copy()
        size_idx = 0

        while buttons_copy:
            current_size = layout_sizes[size_idx % len(layout_sizes)]
            chunk = buttons_copy[:current_size]
            result.append(chunk)
            buttons_copy = buttons_copy[current_size:]
            size_idx += 1

        return result

    def as_markup(self, *sizes: int) -> List[List[Dict[str, Any]]]:
        grid = self.export(*sizes)
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
        self._sizes: List[int] = []

    @property
    def buttons(self) -> List[ReplyKeyboardButton]:
        return self._buttons

    def button(self, text: str, **kwargs: Any) -> ReplyKeyboardBuilder:
        self._buttons.append(ReplyKeyboardButton(text=text, **kwargs))
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

    def adjust(self, *sizes: int) -> ReplyKeyboardBuilder:
        self._sizes = list(sizes) if sizes else [1]
        return self

    def export(self, *sizes: int) -> List[List[ReplyKeyboardButton]]:
        layout_sizes = list(sizes) if sizes else (self._sizes if self._sizes else [1])
        result: List[List[ReplyKeyboardButton]] = []
        buttons_copy = self._buttons.copy()
        size_idx = 0

        while buttons_copy:
            current_size = layout_sizes[size_idx % len(layout_sizes)]
            chunk = buttons_copy[:current_size]
            result.append(chunk)
            buttons_copy = buttons_copy[current_size:]
            size_idx += 1

        return result

    def as_markup(self, *sizes: int) -> List[List[Dict[str, Any]]]:
        grid = self.export(*sizes)
        return [[b.model_dump(exclude_none=True) for b in row] for row in grid]
