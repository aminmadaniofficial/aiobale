from aiobale.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def test_inline_keyboard_builder():
    builder = InlineKeyboardBuilder()
    builder.button(text="وبسایت", url="https://aiobale.ir")
    builder.button(text="کلیک ۱", callback_data="cb_1")
    builder.button(text="کلیک ۲", callback_data="cb_2")
    builder.button(text="کپی کد", copy_text="CODE123")

    # Test adjust method returning builder
    assert builder.adjust(2, 2) is builder
    markup = builder.as_markup()

    assert len(markup) == 2
    assert len(markup[0]) == 2
    assert len(markup[1]) == 2
    assert markup[0][0]["text"] == "وبسایت"
    assert markup[0][0]["url"] == "https://aiobale.ir"
    assert markup[0][1]["callback_data"] == "cb_1"
    assert markup[1][0]["callback_data"] == "cb_2"
    assert markup[1][1]["copy_text"] == "CODE123"


def test_reply_keyboard_builder():
    builder = ReplyKeyboardBuilder()
    builder.button(text="دکمه ۱")
    builder.button(text="دکمه ۲")
    builder.button(text="دکمه ۳")

    assert builder.adjust(2) is builder
    markup = builder.as_markup()

    assert len(markup) == 2
    assert len(markup[0]) == 2
    assert len(markup[1]) == 1
    assert markup[0][0]["text"] == "دکمه ۱"
    assert markup[1][0]["text"] == "دکمه ۳"
