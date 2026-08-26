import pytest
from aiobale.types import (
    Message,
    MessageContent,
    TextMessage,
    TemplateMessage,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def test_message_inline_keyboard_helpers():
    # 1. Message without inline keyboard
    plain_msg = Message.model_validate(
        {
            "1": {"1": 1, "2": 100},
            "2": 1,
            "3": 1700000000,
            "4": 1,
            "5": {"text": {"1": "Simple text"}},
        }
    )
    assert not plain_msg.has_inline_keyboard
    assert plain_msg.inline_keyboard is None
    assert plain_msg.buttons == []
    assert plain_msg.button_matrix == []
    assert plain_msg.button_texts == []
    assert plain_msg.find_button(text="Any") is None

    # 2. Message WITH bot template message and inline keyboard
    btn1 = InlineKeyboardButton(text="سایت", url="https://ble.ir")
    btn2 = InlineKeyboardButton(text="تایید", callback_data="confirm_order")
    btn3 = InlineKeyboardButton(text="کپی کد", copy_text="DISCOUNT2026")
    
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2], [btn3]])
    
    content = MessageContent(
        text=TextMessage(value="سفارش شما آماده است"),
        bot_message=TemplateMessage(
            message=MessageContent(text=TextMessage(value="سفارش شما آماده است")),
            inline_keyboard_markup=markup,
        )
    )

    bot_msg = Message.model_validate(
        {
            "1": {"1": 1, "2": 100},
            "2": 1,
            "3": 1700000000,
            "4": 2,
            "5": content.model_dump(by_alias=True, exclude_none=True),
        }
    )

    assert bot_msg.has_inline_keyboard
    assert bot_msg.inline_keyboard is not None
    assert len(bot_msg.buttons) == 3
    assert len(bot_msg.button_matrix) == 2
    assert bot_msg.button_texts == ["سایت", "تایید", "کپی کد"]
    assert bot_msg.button_urls == ["https://ble.ir"]
    assert bot_msg.button_callbacks == ["confirm_order"]

    # Button type checks
    all_btns = bot_msg.buttons
    assert all_btns[0].is_url
    assert not all_btns[0].is_callback
    assert all_btns[1].is_callback
    assert not all_btns[1].is_url
    assert all_btns[2].is_copy

    # Find button
    found_site = bot_msg.find_button(text="سایت")
    assert found_site is not None
    assert found_site.url == "https://ble.ir"

    found_callback = bot_msg.find_button(callback_data="confirm")
    assert found_callback is not None
    assert found_callback.text == "تایید"

    not_found = bot_msg.find_button(text="ناموجود")
    assert not_found is None

    # Find buttons (multiple)
    found_all = bot_msg.find_buttons()
    assert len(found_all) == 3
