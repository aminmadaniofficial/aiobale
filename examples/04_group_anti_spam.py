"""
04. Group Anti-Spam & Admin Bot
مدیریت گروه، حذف لینک‌های تبلیغاتی و دستورات ادمین (/ban و /kick)
"""
import asyncio
import re
from aiobale import Client, Dispatcher, F, Command, CommandObject
from aiobale.enums import ChatType
from aiobale.types import Message

LINK_REGEX = re.compile(r"(https?://|ble\.ir/|t\.me/|eitaa\.com/|rubika\.ir/)")

dp = Dispatcher()
client = Client(dp, session_file="session.bale")

# ۱. دستور اخراج کاربر (ابتدا ثبت می‌شود تا بر سایر پیام‌ها اولویت داشته باشد)
@dp.message(Command("ban", "kick", prefix="/!"))
async def handle_ban(msg: Message, command: CommandObject):
    print(f"👮 [Command /ban] received from {msg.sender_id} with args: {command.args}")
    
    if not command.args_list:
        await msg.reply("⚠️ فرمت دستور:\n/ban <user_id> [دلیل]")
        return
    
    target_user_id = int(command.args_list[0])
    reason = " ".join(command.args_list[1:]) if len(command.args_list) > 1 else "تخلف از قوانین گروه"

    try:
        await client.kick_user(chat_id=msg.chat.id, user_id=target_user_id)
        await msg.reply(f"🚫 کاربر `{target_user_id}` به دلیل «{reason}» از گروه اخراج شد.")
    except Exception as e:
        await msg.reply(f"❌ خطا در اخراج کاربر: {e}")

# ۲. حذف خودکار پیام‌های حاوی لینک در گروه‌ها
@dp.message(F.chat.type.in_([ChatType.GROUP, ChatType.SUPER_GROUP]))
async def anti_link(msg: Message):
    if msg.text and LINK_REGEX.search(msg.text):
        print(f"🗑️ [Anti-Link] پیامی حاوی لینک از کاربر {msg.sender_id} در گروه {msg.chat.id} شناسایی شد.")
        try:
            await msg.delete()
            print("✅ پیام متخلف با موفقیت حذف شد.")
        except Exception as e:
            print(f"⚠️ امکان حذف پیام وجود نداشت (ربات باید دسترسی ادمین داشته باشد): {e}")

async def main():
    print("🚀 Group Admin & Anti-Spam Bot is running...")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
