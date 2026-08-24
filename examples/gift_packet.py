"""
Gift Packet Example
دریافت و باز کردن پاکت هدیه / عیدی و ارسال پاسخ تشکر
"""
import asyncio
from aiobale import Client, Dispatcher
from aiobale.filters import IsGift, IsPrivate
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp, session_file="session.bale")


@dp.message(IsGift(), IsPrivate())
async def handle_gift(msg: Message):
    # باز کردن بسته هدیه و دریافت وجه به کیف‌پول
    open_resp = await client.open_gift(msg)
    print(f"🎁 بسته هدیه باز شد: {open_resp}")

    await asyncio.sleep(1)
    await msg.answer("خیلی ممنون از بسته هدیه و عیدی شما! 🎁❤️")


if __name__ == "__main__":
    client.run()
