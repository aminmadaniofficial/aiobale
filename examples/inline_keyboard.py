"""
Bot Message & Inline Keyboard Inspector
ثبت و لاگ تمامی پیام‌های دریافتی از بازوها و بات‌ها برای بررسی دکمه‌ها و محتوا
"""
import asyncio
from aiobale import Client, Dispatcher, F
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp, session_file="session.bale")


@dp.message()
async def on_any_message(msg: Message):
    print("\n" + "=" * 60)
    print("📩 [New Message Received]")
    print(f"   - Chat ID: {msg.chat.id} (Type: {msg.chat.type})")
    print(f"   - Sender ID: {msg.sender_id}")
    print(f"   - Text: {msg.text}")
    print(f"   - Raw Content Dict: {msg.content.model_dump(by_alias=True, exclude_none=True)}")
    
    if msg.content.bot_message:
        template = msg.content.bot_message
        print("🤖 [Bot Message Structure Detected]")
        if template.inline_keyboard_markup:
            for row_idx, row in enumerate(template.inline_keyboard_markup.inline_keyboard, start=1):
                for btn in row:
                    print(f"   👉 دکمه سطر {row_idx}: «{btn.text}» | دیتا: {btn.callback_data} | لینک: {btn.url}")
    print("=" * 60 + "\n")


@dp.message_edited()
async def on_edited_message(event):
    print("\n" + "=" * 60)
    print(f"✏️ [Message Edited Event Received]: {event}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    print("🚀 Bot Message & Keyboard Inspector is running...")
    client.run()
