# Aiobale

<div align="center">

[![CI Test Suite](https://github.com/aminmadaniofficial/aiobale/actions/workflows/ci.yml/badge.svg)](https://github.com/aminmadaniofficial/aiobale/actions/workflows/ci.yml)
[![PyPI Version](https://img.shields.io/pypi/v/aiobale-py.svg?color=blue)](https://pypi.org/project/aiobale-py/)
[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-2563eb?style=flat&logo=github)](https://aminmadaniofficial.github.io/aiobale/)
[![Python](https://img.shields.io/badge/Python-3.8%20--%203.14-3776AB?style=flat&logo=python)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/aminmadaniofficial/aiobale/blob/main/LICENSE)

**Modern, fast, fully asynchronous Python framework for Bale Messenger.**

[📖 Interactive Documentation](https://aminmadaniofficial.github.io/aiobale/) • [📦 PyPI Package](https://pypi.org/project/aiobale-py/) • [🚀 Quickstart](#-quickstart) • [✨ Key Features](#-key-features) • [📁 Ready Examples](#-ready-to-run-examples)

</div>

---

## 🌟 Overview

**Aiobale** (`aiobale-py`) is a high-performance, asynchronous Python framework built on top of `asyncio`, WebSockets, and Protocol Buffers for the **Bale Messenger** platform. Designed with inspiration from modern bot frameworks like `aiogram`, it allows developers to build userbots, official bots, automated services, and group management systems with minimal resource usage and complete type safety.

---

## 💖 Special Thanks

Special thanks to **Mohammad Reza Taghdiri (محمدرضا تقدیری)** for his invaluable assistance in testing, discovering edge-case bugs, and contributing to the library's development and stability.

---

## ✨ Key Features

- **⚡ Fully Asynchronous:** Built natively on Python `asyncio` for non-blocking I/O and high concurrency.
- **💬 Interactive Conversations (`Conversation`):** Multi-step question & answer wizard flows with async context managers (`async with client.conversation(...) as conv:`).
- **📜 History Iterator (`iter_messages`):** Asynchronously iterate and paginate through chat message histories with automated deduplication and chunking.
- **🧠 Advanced FSM:** Multi-step conversational form management with `State`, `StatesGroup`, `MemoryStorage`, and persistent `SQLiteStorage`.
- **🛡️ Middlewares & Rate Limiter:** Intercept events and prevent spam using `BaseMiddleware` and the built-in `MessageThrottler`.
- **⌨️ Fluent Keyboards & Pagination:** Chainable `InlineKeyboardMarkup`, `ReplyKeyboardMarkup`, and `KeyboardPaginator` for multi-page menus.
- **🔮 Rich Magic Filter (`F`) & Text Filters:** Filter events effortlessly with `F`, `Command`, `IsMedia`, `TextEquals`, `TextContains`, and logical combinators (`and_f`, `or_f`, `invert_f`).
- **🔀 Modular Routing:** Structure large-scale codebases across multiple files using `Router` and sub-routers.
- **🌐 Webhook HTTP Server:** Built-in lightweight `AiohttpWebhookServer` with secret token security for serverless and production deployments.
- **📁 Smart Media & Downloads:** Direct file path (`str`), `Path`, raw `bytes`, and `io.BytesIO` support in all sending methods, plus 1-line `await message.download()`.
- **🛠️ Command-Line CLI:** Scaffolding tool (`aiobale startproject my_bot`) and interactive phone session login (`aiobale login`).
- **🛡️ Complete RPC Coverage (80+ Methods):** Full access to Messaging, Groups, Channels, Contacts, Presence, Reactions, and Wallet APIs.
- **🧩 100% Type-Safe:** Powered by Pydantic v2 for robust data validation and complete IDE autocompletion.

---

## 📦 Installation

```bash
# Install officially from PyPI
pip install aiobale-py

# Or install using the ultra-fast uv package manager
uv pip install aiobale-py

# Or install the latest development build directly from GitHub
pip install git+https://github.com/aminmadaniofficial/aiobale.git
```

> **Important:** The package name on PyPI is **`aiobale-py`**, while in your Python code you import it directly as **`aiobale`**:
> ```python
> from aiobale import Client, Dispatcher, F, Conversation
> ```

---

## 🚀 Quickstart

Create a functional bot in less than 5 minutes:

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

When you run this script for the first time in your terminal, it will interactively prompt for your phone number and SMS verification code, then persist the session in `my_bot.bale` for automatic reconnects.

---

## 🎯 Code Showcases

### 1. Interactive Linear Conversation (Wizard)

```python
from aiobale import Client, Dispatcher, F
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp, session_file="wizard_bot")

@dp.message(F.text == "/register")
async def register_flow(msg: Message, client: Client):
    async with client.conversation(msg.chat.id) as conv:
        await conv.send_message("Please enter your full name:")
        name_msg = await conv.get_response(timeout=60)

        await conv.send_message(f"Nice to meet you, {name_msg.text}! How old are you?")
        age_msg = await conv.get_response(timeout=60)

        await conv.send_message(f"Registration successful! ✅\nName: {name_msg.text}\nAge: {age_msg.text}")

if __name__ == "__main__":
    client.run()
```

### 2. Message History Pagination (`iter_messages`)

```python
from aiobale import Client

client = Client(session_file="my_account")

async def backup_chat_history(chat_id: int):
    print(f"Reading message history for chat {chat_id}...")
    async for message in client.iter_messages(chat_id=chat_id, limit=50):
        if message.text:
            print(f"[{message.date}] {message.sender_id}: {message.text}")
        elif message.document:
            print(f"[{message.date}] Media attachment: {message.document.name}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(backup_chat_history(123456789))
```

### 3. Persistent FSM with SQLite Storage

```python
from aiobale import Client, Dispatcher, F
from aiobale.fsm import State, StatesGroup, FSMContext, SQLiteStorage
from aiobale.types import Message

class OrderForm(StatesGroup):
    item = State()
    address = State()

storage = SQLiteStorage("bot_orders.db")
dp = Dispatcher(storage=storage)
client = Client(dp, session_file="shop_bot")

@dp.message(F.text == "/order")
async def start_order(msg: Message, state: FSMContext):
    await state.set_state(OrderForm.item)
    await msg.reply("What item would you like to purchase?")

@dp.message(OrderForm.item)
async def process_item(msg: Message, state: FSMContext):
    await state.update_data(item_name=msg.text)
    await state.set_state(OrderForm.address)
    await msg.reply("Please provide your delivery address:")

@dp.message(OrderForm.address)
async def process_address(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await msg.reply(f"Order confirmed! Item: {data.get('item_name')}, Address: {msg.text}")

if __name__ == "__main__":
    client.run()
```

---

## 📁 Ready-to-Run Examples

The [`examples/`](examples/) directory contains 6 complete, production-grade scripts demonstrating every core capability:

| Script | Description | Features Covered |
|---|---|---|
| [`01_auth_and_echo.py`](examples/01_auth_and_echo.py) | Basics, Echo bot, and authentication | CLI login, Message handlers, Replies |
| [`02_fsm_registration.py`](examples/02_fsm_registration.py) | User onboarding and state machines | `StatesGroup`, `FSMContext`, `SQLiteStorage` |
| [`03_shop_and_wallet.py`](examples/03_shop_and_wallet.py) | E-commerce catalog & Bale wallet transfers | `ReplyKeyboardMarkup`, `CallbackData`, Wallet RPC |
| [`04_webhook_and_server.py`](examples/04_webhook_and_server.py) | Webhook server deployment | `AiohttpWebhookServer`, Secret Token auth |
| [`05_rate_limiting_and_middleware.py`](examples/05_rate_limiting_and_middleware.py) | Spam prevention and middleware pipelines | `MessageThrottler`, `BaseMiddleware` |
| [`06_pagination_and_keyboards.py`](examples/06_pagination_and_keyboards.py) | Interactive multi-page keyboards | `KeyboardPaginator`, Grid builders |

---

## 📚 Comprehensive Documentation

The repository includes a modern, web-based interactive documentation website with zero emojis, custom Lucide icons, Dark/Light modes, live search (`Ctrl+K`), and reference guides for all 80+ methods:

👉 **[Read the Full Documentation](https://aminmadaniofficial.github.io/aiobale/)**

---

## 🏛️ Project Origin & Acknowledgements

- **Core Foundation:** Built upon the foundational work of the original `aiobale` library created by **Alireza Jahani** ([Enalite LD](https://github.com/Enalite)).
- **Testing & Bug Reports:** Special thanks to **Mohammad Reza Taghdiri (محمدرضا تقدیری)** for testing, discovering edge cases, and helping improve codebase stability.
- **Maintainer & Lead Developer:** Modernized, heavily refactored, debugged, and actively maintained by **[Amin Madani](https://github.com/aminmadaniofficial)**.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more details.
