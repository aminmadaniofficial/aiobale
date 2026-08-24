"""
03. Shop & Wallet Example
کاتالوگ محصولات، استعلام موجودی کیف‌پول و منوی تعاملی فروشگاه
"""
import asyncio
from aiobale import Client, Dispatcher, F, Command
from aiobale.types import Message
from aiobale.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

PRODUCTS = {
    "🛒 کتاب پایتون پیشرفته": 250000,
    "🛒 دوره آموزش FastAPI": 450000,
    "🛒 کتاب طراحی سیستم": 380000,
    "🛒 دوره Asyncio در پایتون": 290000,
    "🛒 آموزش داکر و کوبرنتیز": 500000,
}

dp = Dispatcher()
client = Client(dp, session_file="session.bale")

@dp.message(Command("wallet", "balance"))
async def check_wallet(msg: Message):
    resp = await client.get_wallet()
    wallet = resp.wallet
    await msg.reply(
        "💼 اطلاعات کیف‌پول بله شما:\n\n"
        f"💰 موجودی: {wallet.balance:,} ریال\n"
        f"💳 شماره کارت: {wallet.pan or 'ثبت نشده'}\n"
        f"🏦 شماره حساب: {wallet.account or 'ثبت نشده'}"
    )

@dp.message(Command("shop", "products"))
async def show_shop(msg: Message):
    # ساخت کیبورد منوی فروشگاه
    builder = ReplyKeyboardBuilder()
    for product_name in PRODUCTS.keys():
        builder.button(text=product_name)
    builder.button(text="💰 استعلام کیف‌پول")
    
    markup = builder.as_markup(2)  # چینش ۲ دکمه در هر سطر
    await msg.reply("📚 به فروشگاه آموزشی خوش آمدید! محصول مورد نظر را انتخاب کنید:", reply_markup=markup)

@dp.message(F.text == "💰 استعلام کیف‌پول")
async def btn_wallet(msg: Message):
    await check_wallet(msg)

@dp.message(F.text.startswith("🛒"))
async def handle_product_select(msg: Message):
    price = PRODUCTS.get(msg.text)
    if price:
        await msg.reply(
            f"✅ شما محصول «{msg.text}» را انتخاب کردید.\n"
            f"💵 قیمت: {price:,} ریال\n\n"
            f"جهت خرید می‌توانید از دستور /wallet موجودی خود را بررسی کنید."
        )

async def main():
    print("🚀 Shop & Wallet Bot is running...")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
