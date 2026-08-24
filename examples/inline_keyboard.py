"""
Detecting & Reading Bot Inline Keyboards
تشخیص دکمه‌های شیشه‌ای ارسال شده توسط بازوها و ربات‌های بله و استخراج دکمه‌ها
"""
import asyncio
from aiobale import Client, Dispatcher, F
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp, session_file="session.bale")


@dp.message(F.content.bot_message)
async def handle_bot_inline_keyboard(msg: Message):
    template = msg.content.bot_message
    if not template or not template.inline_keyboard_markup:
        return

    markup = template.inline_keyboard_markup
    print(f"🤖 [Bot Message] پیامی حاوی دکمه شیشه‌ای از شناسه {msg.sender_id} دریافت شد:")

    # پیمایش تمام ردیف‌ها و دکمه‌های شیشه‌ای بازوی بله
    for row_idx, row in enumerate(markup.inline_keyboard, start=1):
        for btn in row:
            btn_info = f"   - سطر {row_idx}: «{btn.text}»"
            if btn.url:
                btn_info += f" | لینک: {btn.url}"
            if btn.callback_data:
                btn_info += f" | دیتای کال‌بک: {btn.callback_data}"
            if btn.copy_text:
                btn_info += f" | متن کپی: {btn.copy_text}"
            print(btn_info)

    await msg.reply("✅ دکمه‌های شیشه‌ای این ربات با موفقیت توسط aiobale خوانده و در کنسول لاگ شدند.")


if __name__ == "__main__":
    print("🚀 Bot Inline Keyboard Detector is running...")
    client.run()
