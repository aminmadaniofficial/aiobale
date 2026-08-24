"""
02. FSM Form & Registration Example
فرم چند مرحله‌ای استخدام / ثبت‌نام با ذخیره‌سازی دائمی در SQLite
"""
import asyncio
from aiobale import Client, Dispatcher, F, Command, SQLiteStorage
from aiobale.fsm import State, StatesGroup, FSMContext
from aiobale.types import Message
from aiobale.utils.keyboard import ReplyKeyboardBuilder

class RegisterForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_phone = State()

# استفاده از دیتابیس محلی برای ذخیره وضعیت‌ها حتی در صورت ری‌استارت
storage = SQLiteStorage("registration_fsm.db")
dp = Dispatcher(storage=storage)

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
    await state.clear()

    await msg.reply(
        "🎉 ثبت‌نام شما با موفقیت تکمیل شد!\n\n"
        f"👤 نام: {data.get('full_name')}\n"
        f"🎂 سن: {data.get('age')}\n"
        f"📞 شماره: {data.get('phone')}"
    )

async def main():
    client = Client(dp, session_file="session.bale")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
