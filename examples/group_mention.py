import asyncio
from aiobale import Client, Dispatcher
from aiobale.types import Message
from aiobale.enums import ChatType

dp = Dispatcher()
client = Client(dp)


@dp.message()
async def handler(msg: Message):
    if msg.chat.type != ChatType.GROUP:
        return

    all_members = []
    offset = 0
    # Using 100 makes it faster though.
    # Bale usually sticks to 20 — pushing it too much might get you banned.
    limit = 100
    while True:
        members = await client.load_members(
            msg.chat.id, limit=limit, next_offset=offset
        )
        
        all_members.extend(members)
        offset += limit
        
        if len(members) < limit:
            break
        
        await asyncio.sleep(0.5)
    
    text = "\n".join([f"ID: {member.id}" for member in all_members])
    print(text)


client.run()
