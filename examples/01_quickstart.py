"""
01. Quickstart Example
ساده‌ترین ربات بله برای پاسخ به دستورات و پیام‌های متنی
"""
import asyncio
from aiobale import Client, Dispatcher, F, Command, CommandObject
from aiobale.types import Message

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.reply(
        "سلام! به ربات Aiobale خوش آمدید 🚀\n"
        "دستور /help را برای مشاهده راهنما ارسال کنید."
    )

@dp.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.reply(
        "📚 راهنمای دستورات:\n"
        "/start - شروع ربات\n"
        "/help - راهنما\n"
        "/id - دریافت شناسه کاربری و چت"
    )

@dp.message(Command("id"))
async def cmd_id(msg: Message):
    await msg.reply(
        f"👤 شناسه شما: `{msg.sender_id}`\n"
        f"💬 شناسه چت: `{msg.chat.id}`"
    )

@dp.message(F.text)
async def echo_message(msg: Message):
    await msg.reply(f"پیام دریافت شد: {msg.text}")

async def main():
    # اگر شماره تلفن را پاس دهید، فقط کد پیامک شده در کنسول پرسیده می‌شود
    client = Client(dp, session_file="session.bale")
    print("🚀 Bot is running...")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
