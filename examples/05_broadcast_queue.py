"""
05. Broadcast Queue & Anti-Flood Example
ارسال امن پیام‌های همگانی به هزاران کاربر با کنترل نرخ و نوار پیشرفت زنده
"""
import asyncio
from aiobale import Client, Dispatcher, F, Command
from aiobale.enums import ChatType
from aiobale.types import Message
from aiobale.utils import MessageThrottler, create_progress_bar

dp = Dispatcher()
client = Client(dp, session_file="session.bale")

# صف هوشمند کنترل نرخ (حداکثر ۲۰ درخواست در ثانیه)
throttler = MessageThrottler(rate_limit=0.05, max_retries=3)

# لیست کاربران هدف (برای نمونه)
TARGET_USERS = [10000001, 10000002, 10000003, 10000004, 10000005]

@dp.message(Command("broadcast"))
async def start_broadcast(msg: Message):
    await msg.reply(f"📢 ارسال پیام همگانی به {len(TARGET_USERS)} کاربر آغاز شد...")

    # هوک نوار پیشرفت در کنسول
    progress_bar = create_progress_bar("ارسال پیام به کاربران")

    async def send_to_user(uid: int):
        await client.send_message(
            chat_id=uid,
            chat_type=ChatType.USER,
            text="سلام کاربر عزیز! این یک پیام اطلاع‌رسانی از ربات است 🚀"
        )

    # اجرای همگانی ایمن با مدیریت خطاهای احتمالی
    report = await throttler.broadcast(
        send_fn=send_to_user,
        chat_ids=TARGET_USERS,
        progress_callback=progress_bar
    )

    await msg.reply(
        "✅ عملیات ارسال همگانی به پایان رسید!\n\n"
        f"📊 کل کاربران: {report.total}\n"
        f"✔️ ارسال‌های موفق: {report.success_count}\n"
        f"❌ ناموفق: {report.failure_count}\n"
        f"⏱️ زمان کل: {report.duration_seconds:.2f} ثانیه"
    )

async def main():
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
