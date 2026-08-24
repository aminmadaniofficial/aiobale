"""
05. Broadcast Queue & Anti-Flood Example
ارسال امن پیام‌های همگانی با کنترل نرخ و نوار پیشرفت زنده
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

@dp.message(Command("broadcast"))
async def start_broadcast(msg: Message):
    # برای تست زنده، ۳ پیام به اکانت خودتان ارسال می‌کنیم تا ۱۰۰٪ موفق باشد
    target_users = [msg.sender_id, msg.sender_id, msg.sender_id]
    
    await msg.reply(f"📢 ارسال {len(target_users)} پیام اطلاع‌رسانی از طریق صف Throttler آغاز شد...")

    # هوک نوار پیشرفت در کنسول
    progress_bar = create_progress_bar("ارسال پیام به کاربران")

    async def send_to_user(uid: int):
        await client.send_message(
            chat_id=uid,
            chat_type=ChatType.USER,
            text="سلام! این یک پیام اطلاع‌رسانی تست از طریق صف ضد بلاکی Aiobale است 🚀"
        )

    # اجرای همگانی ایمن
    report = await throttler.broadcast(
        send_fn=send_to_user,
        chat_ids=target_users,
        progress_callback=progress_bar
    )

    error_details = ""
    if report.errors:
        error_details = "\n⚠️ خطاهای رخ داده:\n" + "\n".join([f"- کاربر {k}: {v}" for k, v in report.errors.items()])

    await msg.reply(
        "✅ عملیات ارسال همگانی به پایان رسید!\n\n"
        f"📊 کل درخواست‌ها: {report.total}\n"
        f"✔️ موفق: {report.success_count}\n"
        f"❌ ناموفق: {report.failure_count}\n"
        f"⏱️ زمان کل: {report.duration_seconds:.2f} ثانیه"
        f"{error_details}"
    )

async def main():
    print("🚀 Broadcast Bot is running...")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
