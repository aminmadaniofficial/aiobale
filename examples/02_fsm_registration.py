"""
02. FSM Form & Registration Example
فرم چند مرحله‌ای استخدام / ثبت‌نام با نگهداری موقت حالت در FSM و ذخیره نهایی در SQLite
"""
import asyncio
import sqlite3
from aiobale import Client, Dispatcher, F, Command, SQLiteStorage
from aiobale.fsm import State, StatesGroup, FSMContext
from aiobale.types import Message

class RegisterForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_phone = State()

# ۱. استوریج FSM برای ذخیره مراحل کاربر
storage = SQLiteStorage("registration_fsm.db")
dp = Dispatcher(storage=storage)

# ۲. ایجاد جدول دائمی کاربران ثبت‌نام شده در دیتابیس SQLite
def init_users_table():
    with sqlite3.connect("registration_fsm.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS registered_users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                age INTEGER,
                phone TEXT
            )
        """)
        conn.commit()

init_users_table()

@dp.message(Command("cancel"))
async def cancel_form(msg: Message, state: FSMContext):
    await state.clear()
    await msg.reply("❌ عملیات ثبت‌نام لغو شد.")

@dp.message(Command("register"))
async def start_registration(msg: Message, state: FSMContext):
    await state.set_state(RegisterForm.waiting_for_name)
    await msg.reply("👋 به فرم ثبت‌نام خوش آمدید.\nلطفاً نام و نام خانوادگی خود را وارد کنید:")

@dp.message(RegisterForm.waiting_for_name)
async def process_name(msg: Message, state: FSMContext):
    await state.update_data(full_name=msg.text)
    await state.set_state(RegisterForm.waiting_for_age)
    await msg.reply("✅ نام شما ثبت شد. لطفاً سن خود را وارد کنید:")

@dp.message(RegisterForm.waiting_for_age)
async def process_age(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.reply("⚠️ لطفاً سن را فقط به صورت عدد وارد کنید:")
        return
    
    await state.update_data(age=int(msg.text))
    await state.set_state(RegisterForm.waiting_for_phone)
    await msg.reply("📱 لطفاً شماره تماس خود را وارد کنید:")

@dp.message(RegisterForm.waiting_for_phone)
async def process_phone(msg: Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    data = await state.get_data()
    
    # پاک کردن وضعیت موقت FSM (کاربر از حالت فرم خارج می‌شود)
    await state.clear()

    # ذخیره دائمی مشخصات در جدول دیتابیس SQLite
    with sqlite3.connect("registration_fsm.db") as conn:
        conn.execute(
            "INSERT OR REPLACE INTO registered_users (user_id, full_name, age, phone) VALUES (?, ?, ?, ?)",
            (msg.sender_id, data.get("full_name"), data.get("age"), data.get("phone"))
        )
        conn.commit()

    await msg.reply(
        "🎉 ثبت‌نام شما با موفقیت در دیتابیس ثبت شد!\n\n"
        f"👤 نام: {data.get('full_name')}\n"
        f"🎂 سن: {data.get('age')}\n"
        f"📞 شماره: {data.get('phone')}"
    )
    print(f"💾 کاربر {msg.sender_id} با موفقیت در registration_fsm.db ذخیره شد.")

async def main():
    client = Client(dp, session_file="session.bale")
    print("🚀 Registration Bot is running...")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
