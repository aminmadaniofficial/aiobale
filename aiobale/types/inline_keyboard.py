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
        if isinstance(data, list):
            # 2D list of button dicts or InlineKeyboardButton instances
            formatted_rows = []
            for row in data:
                if isinstance(row, list):
                    btn_row = []
                    for b in row:
                        if isinstance(b, InlineKeyboardButton):
                            btn_row.append(b)
                        elif isinstance(b, dict):
                            btn_row.append(InlineKeyboardButton.model_validate(b))
                        else:
                            btn_row.append(InlineKeyboardButton(text=str(b)))
                    formatted_rows.append(btn_row)
                elif isinstance(row, (dict, InlineKeyboardButton)):
                    b = row if isinstance(row, InlineKeyboardButton) else InlineKeyboardButton.model_validate(row)
                    formatted_rows.append([b])
            return {"1": formatted_rows}

        if isinstance(data, dict):
            if "inline_keyboard" in data:
                return cls.validate_keyboard(data["inline_keyboard"])
            if "1" in data and isinstance(data["1"], list):
                raw_buttons = data["1"]
                keyboard_rows = []
                for row in raw_buttons:
                    if isinstance(row, dict) and "1" in row:
                        buttons_data = row["1"]
                        if isinstance(buttons_data, list):
                            btns = [
                                InlineKeyboardButton.model_validate(b) if isinstance(b, dict) else b
                                for b in buttons_data
                            ]
                            keyboard_rows.append(btns)
                        elif isinstance(buttons_data, dict):
                            btn = InlineKeyboardButton.model_validate(buttons_data)
                            keyboard_rows.append([btn])
                    elif isinstance(row, list):
                        btns = [
                            InlineKeyboardButton.model_validate(b) if isinstance(b, dict) else b
                            for b in row
                        ]
                        keyboard_rows.append(btns)
                return {"1": keyboard_rows}

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
