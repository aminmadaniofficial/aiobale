from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from pydantic import Field, model_serializer, model_validator

from .base import BaleObject


class InlineKeyboardButton(BaleObject):
    """
    Represents a button within an inline keyboard.
    """

    text: str = Field(..., alias="1")
    """Label text displayed on the button."""

    url: Optional[str] = Field(None, alias="2")
    """URL to be opened when the button is pressed."""

    callback_data: Optional[str] = Field(None, alias="3")
    """Data sent back to the bot when the button is pressed."""

    copy_text: Optional[str] = Field(None, alias="9")
    """Text to be copied to the clipboard when the button is pressed."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            text: str,
            url: Optional[str] = None,
            callback_data: Optional[str] = None,
            copy_text: Optional[str] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                text=text,
                url=url,
                callback_data=callback_data,
                copy_text=copy_text,
                **__pydantic_kwargs,
            )

    
    @property
    def is_url(self) -> bool:
        """Returns True if this button contains a web URL."""
        return bool(self.url)

    @property
    def is_callback(self) -> bool:
        """Returns True if this button contains callback data."""
        return bool(self.callback_data)

    @property
    def is_copy(self) -> bool:
        """Returns True if this button copies text to clipboard."""
        return bool(self.copy_text)

    def as_dict(self) -> Dict[str, Any]:
        """Returns button attributes as a clean dictionary."""
        return {
            "text": self.text,
            "url": self.url,
            "callback_data": self.callback_data,
            "copy_text": self.copy_text,
        }

    @model_validator(mode="before")
    @classmethod
    def validate_keyboard(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "1" in data and isinstance(data.get("1"), str):
                for i in ("2", "3", "9"):
                    if i in data and isinstance(data[i], dict) and "1" in data[i]:
                        data[i] = data[i]["1"]
        return data

    @model_serializer(mode="wrap")
    def ser(self, nxt, info):
        if not info.by_alias:
            return nxt(self)

        out = nxt(self)
        for i in ("2", "3", "9"):
            if i not in out:
                continue
            out[i] = {"1": out[i]}
        return out


class InlineKeyboardMarkup(BaleObject):
    """
    Represents the entire inline keyboard layout for a message.
    """

    inline_keyboard: List[List[InlineKeyboardButton]] = Field(
        default_factory=list, alias="1"
    )
    """Two-dimensional array of inline keyboard button rows."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            inline_keyboard: List[List[InlineKeyboardButton]],
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(inline_keyboard=inline_keyboard, **__pydantic_kwargs)

    @model_validator(mode="before")
    @classmethod
    def validate_keyboard(cls, data: Any) -> Any:
        def _parse_button(b: Any) -> InlineKeyboardButton:
            if isinstance(b, InlineKeyboardButton):
                return b
            if isinstance(b, dict):
                return InlineKeyboardButton.model_validate(b)
            return InlineKeyboardButton(text=str(b))

        def _parse_row(r: Any) -> List[InlineKeyboardButton]:
            if isinstance(r, list):
                return [_parse_button(b) for b in r]
            if isinstance(r, dict):
                if "1" in r and isinstance(r["1"], (list, dict)):
                    inner = r["1"]
                    if isinstance(inner, dict):
                        if all(isinstance(v, dict) for v in inner.values()):
                            return [_parse_button(b) for b in inner.values()]
                        return [_parse_button(inner)]
                    elif isinstance(inner, list):
                        return [_parse_button(b) for b in inner]
                return [_parse_button(r)]
            return [_parse_button(r)]

        if isinstance(data, dict):
            if "inline_keyboard" in data:
                data = data["inline_keyboard"]
            elif "1" in data:
                data = data["1"]

        if isinstance(data, dict):
            data = list(data.values())

        if isinstance(data, list):
            formatted_rows = [_parse_row(r) for r in data]
            return {"1": formatted_rows}

        return data

    @model_serializer(mode="wrap")
    def ser(self, nxt, info):
        if not info.by_alias:
            return nxt(self)

        out = []
        for row in self.inline_keyboard:
            buttons_serialized = [
                btn.model_dump(by_alias=True, exclude_none=True) for btn in row
            ]
            out.append({"1": buttons_serialized})
        return {"1": out}
