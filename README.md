# Aiobale

<div align="center">

[![CI Test Suite](https://github.com/aminmadaniofficial/aiobale/actions/workflows/ci.yml/badge.svg)](https://github.com/aminmadaniofficial/aiobale/actions/workflows/ci.yml)
[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-2563eb?style=flat&logo=github)](https://aminmadaniofficial.github.io/aiobale/)
[![Python](https://img.shields.io/badge/Python-3.8%20--%203.14-3776AB?style=flat&logo=python)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/aminmadaniofficial/aiobale/blob/main/LICENSE)

**Modern, fast, fully asynchronous Python framework for Bale Messenger.**

[📖 Interactive Documentation](https://aminmadaniofficial.github.io/aiobale/) • [📦 PyPI Package](https://pypi.org/project/aiobale/) • [🚀 Quickstart](#-quickstart) • [✨ Features](#-key-features)

</div>

---

## 🌟 Overview

**Aiobale** is a high-performance, asynchronous Python library built on top of `asyncio`, WebSockets, and Protocol Buffers for the **Bale Messenger** platform. Designed with inspiration from modern bot frameworks like `aiogram`, it allows developers to build userbots, official bots, automation tools, and group management services with minimal resource usage and complete type safety.

---

## ✨ Key Features

- **⚡ Fully Asynchronous:** Built natively on Python `asyncio` for non-blocking I/O and high concurrency.
- **🔮 Magic Filter (`F`):** Powerful expression-based event filtering (e.g. `F.text.startswith("/start")`, `F.chat.type == ChatType.GROUP`).
- **🔀 Modular Routing:** Organize complex bots across multiple files using `Router` and sub-routers.
- **🛡️ Full RPC Coverage (79+ Methods):** Complete access to Messaging, Groups, Channels, Contacts, Presence, Reactions, and File APIs.
- **📁 Fast Media Upload & Download:** Automated chunked file streaming with binary support.
- **🔐 Flexible Authentication:** Interactive CLI phone login, persistent session files (`.bale`), direct JWT token support, and headless Docker readiness.
- **🧩 100% Type Annotated:** Powered by Pydantic v2 for data validation and complete IDE autocompletion.
- **🧪 Battle-Tested:** Automated CI pipeline verifying compatibility from Python 3.8 to 3.14.

---

## 📦 Installation

```bash
# Install from PyPI
pip install aiobale

# Or install the latest development version directly from GitHub
pip install git+https://github.com/aminmadaniofficial/aiobale.git
```

---

## 🚀 Quickstart

Create your first bot in less than 5 minutes:

```python
import asyncio
from aiobale import Client, Dispatcher, F
from aiobale.types import Message
from aiobale.filters import IsText

dp = Dispatcher()
client = Client(dp, session_file="my_bot")

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.reply("Hello! Welcome to Aiobale 🚀")

@dp.message(IsText())
async def echo_handler(message: Message):
    await message.reply(f"You said: {message.text}")

async def main():
    print("Connecting to Bale Messenger...")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
```

When you run this script for the first time in your terminal, it will interactively prompt for your phone number and SMS verification code, then store the session in `my_bot.bale` for automatic reconnects.

---

## 🎯 Code Examples

### 1. Group Moderation & Anti-Link Bot

```python
import re
from aiobale import Client, Dispatcher, F
from aiobale.types import Message
from aiobale.enums import ChatType

dp = Dispatcher()
client = Client(dp, session_file="mod_bot")

LINK_REGEX = re.compile(r"(https?://|ble\.ir/|t\.me/|eitaa\.com/)")

@dp.message(F.chat.type == ChatType.GROUP)
async def delete_links(msg: Message):
    if msg.text and LINK_REGEX.search(msg.text):
        await msg.delete()

@dp.message(F.text == "/ban", F.chat.type == ChatType.GROUP)
async def ban_user(msg: Message, client: Client):
    if msg.replied_to:
        await client.kick_user(msg.chat.id, msg.replied_to.sender_id)
        await msg.answer("User kicked from group.")

if __name__ == "__main__":
    client.run()
```

### 2. Media Downloader Bot

```python
from aiobale import Client, Dispatcher, F
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp, session_file="media_bot")

@dp.message(F.content.document)
async def handle_document(msg: Message, client: Client):
    doc = msg.content.document
    await msg.reply(f"Downloading {doc.name}...")
    
    file_bytes = await client.download_file(
        file_id=doc.file_id,
        access_hash=doc.access_hash
    )
    
    await msg.reply(f"File downloaded successfully ({len(file_bytes)} bytes)!")

if __name__ == "__main__":
    client.run()
```

---

## 📚 Comprehensive Documentation

The repository includes a modern, web-based interactive documentation website with zero emojis, custom Lucide icons, Dark/Light modes, live search (`Ctrl+K`), and reference guides for all 79+ methods:

👉 **[Read the Full Documentation](https://aminmadaniofficial.github.io/aiobale/)**

---

## 🏛️ Project Origin & Acknowledgements

This project is built upon the foundational work of the original `aiobale` library created by **Alireza Jahani** ([Enalite LD](https://github.com/Enalite)). 

It has been modernized, heavily refactored, debugged, and is now actively maintained with automated CI/CD and comprehensive docs by **[Amin Madani](https://github.com/aminmadaniofficial)**.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more details.
