from aiobale import F, Client, Dispatcher
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp)

added = set()


@dp.message(F.content.empty, F.replied_to)  # Means the message is forwarded
async def handler(msg: Message):
    message_id = msg.replied_to.message_id
    if message_id in added:
        await client.revoke_upvote(msg.replied_to)
        added.remove(message_id)
        await msg.answer("Revoked!")

    else:
        await client.upvote_post(msg.replied_to)
        await msg.answer("Added!")
        added.add(message_id)


@dp.message()
async def handler(msg: Message):
    await msg.answer("Forward a message!!!")


client.run()
