"""
Bot Message & Inline Keyboard Inspector & Extractor
دریافت، استخراج و پردازش دکمه‌های شیشه‌ای و محتوای ارسالی از بازوها و بات‌ها در یوزربات
"""
import asyncio
from aiobale import Client, Dispatcher, F
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp, session_file="session.bale")


@dp.message()
async def on_bot_message(msg: Message):
    # بررسی آیا پیام حاوی اینلاین کیبورد بات است یا خیر
    if msg.has_inline_keyboard:
        print("\n" + "=" * 60)
        print("🤖 [پیام بات حاوی دکمه‌های شیشه‌ای (Inline Keyboard) دریافت شد]")
        print(f"   - شناسه چت: {msg.chat.id}")
        print(f"   - فرستنده: {msg.sender_id}")
        print(f"   - متن پیام: {msg.text}")
        print(f"   - تعداد سطرها: {len(msg.button_matrix)}")
        print(f"   - تعداد کل دکمه‌ها: {len(msg.buttons)}")
        print(f"   - عناوین دکمه‌ها: {msg.button_texts}")
        print(f"   - لینک‌های موجود: {msg.button_urls}")
        print(f"   - دیتای دکمه‌ها (Callbacks): {msg.button_callbacks}")
        print("-" * 60)

        # پیمایش دقیق سطرها و دکمه‌ها
        for row_idx, row in enumerate(msg.button_matrix, start=1):
            for btn_idx, btn in enumerate(row, start=1):
                btn_type = "🔗 لینک" if btn.is_url else ("🔘 کال‌بک" if btn.is_callback else "📋 کپی")
                detail = btn.url or btn.callback_data or btn.copy_text or "بدون دیتا"
                print(f"   👉 [سطر {row_idx}, دکمه {btn_idx}] «{btn.text}» | نوع: {btn_type} | مقدار: {detail}")

        # جستجوی یک دکمه خاص با تابع find_button
        target_btn = msg.find_button(text="ورود")
        if target_btn:
            print(f"\n🎯 دکمه ورود پیدا شد: لینک={target_btn.url}")

        print("=" * 60 + "\n")


if __name__ == "__main__":
    print("🚀 Bot Message & Keyboard Inspector is running...")
    client.run()
