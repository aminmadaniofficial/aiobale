from aiobale import F, Client, Dispatcher
from aiobale.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

dp = Dispatcher()
# You can also use a proxy
client = Client(dp, proxy="http://host:port")


@dp.message(F.text == "bot")
async def image(msg: Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Google", url="https://google.com"),
                InlineKeyboardButton(
                    text="Copy google address", copy_text="https://google.com"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Callback (NO Response!!!)", callback_data="test"
                )
            ],
        ]
    )

    await msg.answer("Hi. I'm a user, but I can use buttons!!!!", reply_markup=markup)


client.run()
