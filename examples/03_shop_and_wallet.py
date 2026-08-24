"""
03. Shop & Wallet Example
کاتالوگ محصولات با صفحه‌بندی هوشمند، دکمه‌های تایپ‌شده و استعلام موجودی کیف‌پول
"""
import asyncio
from aiobale import Client, Dispatcher, F, Command, CallbackData
from aiobale.types import Message
from aiobale.utils import KeyboardPaginator

# تعریف داده‌های تایپ‌شده کال‌بک
class ProductCB(CallbackData, prefix="prod"):
    action: str
    product_id: int

PRODUCTS = [
    {"id": 101, "name": "کتاب پایتون پیشرفته", "price": 250000},
    {"id": 102, "name": "دوره آموزش FastAPI", "price": 450000},
    {"id": 103, "name": "کتاب طراحی سیستم", "price": 380000},
    {"id": 104, "name": "دوره Asyncio در پایتون", "price": 290000},
    {"id": 105, "name": "آموزش داکر و کوبرنتیز", "price": 500000},
]

dp = Dispatcher()
client = Client(dp, session_file="shop_bot.bale")

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
    # ساخت صفحه‌بندی کاتالوگ (۲ محصول در هر صفحه)
    paginator = KeyboardPaginator(
        items=PRODUCTS,
        page_size=2,
        item_button_factory=lambda item, idx: {
            "text": f"🛒 {item['name']} - {item['price']:,} ریال",
            "callback_data": ProductCB(action="buy", product_id=item["id"]).pack()
        },
        callback_prefix="shop_page"
    )
    markup = paginator.get_page(page=1)
    await msg.reply("📚 لیست محصولات فروشگاه آموزشی:", components=markup)

@dp.message(ProductCB.filter(F.action == "buy"))
async def buy_product(event, callback_data: ProductCB):
    product = next((p for p in PRODUCTS if p["id"] == callback_data.product_id), None)
    if product:
        print(f"خرید محصول: {product['name']}")

async def main():
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
