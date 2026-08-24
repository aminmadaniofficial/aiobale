"""
06. Multi-Account Client Manager Example
اجرای همزمان چندین اکانت کاربری و ربات بله در یک برنامه واحد
"""
from aiobale import ClientManager, Dispatcher, F, Command
from aiobale.types import Message

# تعریف دیسپچر مشترک برای همه کلاینت‌ها (یا مجزا برای هر کدام)
dp = Dispatcher()

@dp.message(Command("start"))
async def handle_start(msg: Message):
    await msg.reply(f"درود! اکانت با شناسه شما: {msg.sender_id}")

@dp.message(F.text)
async def handle_text(msg: Message):
    print(f"[{msg.chat.id}] {msg.text}")

def main():
    manager = ClientManager(dp)

    # افزودن اکانت اول با سشن محلی و شماره
    manager.add_client(
        session_file="support_account.bale",
        phone_number="09121111111"
    )

    # افزودن اکانت دوم با توکن مستقیم
    manager.add_client(
        session_file="bot_account.bale",
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )

    print("🚀 Running all clients concurrently...")
    manager.run_all()

if __name__ == "__main__":
    main()
