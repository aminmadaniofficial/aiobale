"""
03. Shop & Wallet Example
کاتالوگ محصولات، مدیریت سفارشات با کامندهای متنی و استعلام موجودی کیف‌پول
(سازگار با تمام اکانت‌های کاربری و ربات بله)
"""
import asyncio
from aiobale import Client, Dispatcher, F, Command, CommandObject
from aiobale.types import Message

PRODUCTS = {
    101: {"name": "کتاب پایتون پیشرفته", "price": 250000},
    102: {"name": "دوره آموزش FastAPI", "price": 450000},
    103: {"name": "کتاب طراحی سیستم", "price": 380000},
    104: {"name": "دوره Asyncio در پایتون", "price": 290000},
    105: {"name": "آموزش داکر و کوبرنتیز", "price": 500000},
}

dp = Dispatcher()
client = Client(dp, session_file="session.bale")

# ۱. استعلام موجودی و اطلاعات حساب کیف‌پول بله
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

# ۲. نمایش کاتالوگ فروشگاه
@dp.message(Command("shop", "products"))
async def show_shop(msg: Message):
    catalog_lines = ["📚 کاتالوگ محصولات فروشگاه آموزشی:\n"]
    for pid, pinfo in PRODUCTS.items():
        catalog_lines.append(f"▫️ [{pid}] {pinfo['name']} — {pinfo['price']:,} ریال (خرید: /buy_{pid})")
    
    catalog_lines.append("\n💡 برای خرید، روی شناسه محصول بزنید یا بنویسید: /buy <شناسه>")
    catalog_lines.append("💼 برای استعلام موجودی: /wallet")
    
    await msg.reply("\n".join(catalog_lines))

# ۳. پردازش خرید محصول با دستور /buy <id> یا /buy_<id>
@dp.message(Command("buy"))
async def handle_buy(msg: Message, command: CommandObject):
    if not command.args:
        await msg.reply("⚠️ لطفاً شناسه محصول را وارد کنید. مثال: `/buy 101`")
        return

    try:
        pid = int(command.args.strip())
    except ValueError:
        await msg.reply("❌ شناسه محصول باید عددی باشد.")
        return

    product = PRODUCTS.get(pid)
    if not product:
        await msg.reply(f"❌ محصولی با شناسه {pid} یافت نشد.")
        return

    # دریافت موجودی کاربر
    wallet_info = await client.get_wallet()
    balance = wallet_info.wallet.balance if wallet_info.wallet else 0

    if balance < product["price"]:
        await msg.reply(
            f"❌ موجودی کیف‌پول شما کافی نیست!\n"
            f"💵 قیمت محصول: {product['price']:,} ریال\n"
            f"💰 موجودی شما: {balance:,} ریال\n\n"
            f"لطفاً ابتدا کیف‌پول خود را در بله شارژ نمایید."
        )
    else:
        await msg.reply(
            f"🎉 خرید شما با موفقیت انجام شد!\n\n"
            f"📦 محصول: {product['name']}\n"
            f"💵 مبلغ: {product['price']:,} ریال\n"
            f"✅ لینک دانلود اختصاصی برای شما ارسال خواهد شد."
        )

# ۴. پشتیبانی از دستورات کلیکی مثل /buy_101
@dp.message(F.text.regexp(r"^/buy_(\d+)$"))
async def handle_buy_regex(msg: Message):
    pid = int(msg.text.replace("/buy_", ""))
    product = PRODUCTS.get(pid)
    if not product:
        await msg.reply(f"❌ محصولی با شناسه {pid} یافت نشد.")
        return

    await msg.reply(
        f"🛒 محصول انتخابی: {product['name']}\n"
        f"💵 قیمت: {product['price']:,} ریال\n\n"
        f"برای تایید و تکمیل خرید دستور `/buy {pid}` را ارسال کنید."
    )

async def main():
    print("🚀 Shop & Wallet Bot is running...")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
