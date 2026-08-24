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
ADMINS = [2091967932]  # شناسه ادمین‌های ربات

dp = Dispatcher()
client = Client(dp, session_file="admin_bot.bale")

# ۱. حذف خودکار لینک‌های تبلیغاتی در گروه‌ها
@dp.message(F.chat.type == ChatType.GROUP)
async def anti_link(msg: Message):
    if msg.text and LINK_REGEX.search(msg.text):
        # کاربر عادی لینک فرستاده -> حذف پیام
        if msg.sender_id not in ADMINS:
            await msg.delete()
            print(f"🗑️ لینک ارسالی کاربر {msg.sender_id} حذف شد.")

# ۲. دستور اخراج موقت یا دائم کاربر
@dp.message(Command("ban", "kick", prefix="/!"), F.sender_id.in_(ADMINS))
async def handle_ban(msg: Message, command: CommandObject):
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

async def main():
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
