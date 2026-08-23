<p align="center">
  <img src="https://i.postimg.cc/Ssg1Tfhr/banner.png" alt="Aiobale Banner">
</p>

<h1 align="center">Aiobale (Revived & Maintained)</h1>
<h3 align="center">Async Python Client for Bale Messenger — Simplified, Modern, Pythonic</h3>

<p align="center">
  <strong>Aiobale</strong> is an asynchronous Python library that unlocks Bale Messenger's internal API, making it effortless to build bots, automation, and tools without diving into gRPC or Protobuf complexity.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-brightgreen?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-blue?logo=open-source-initiative" alt="License">
  <img src="https://img.shields.io/badge/Status-Restored%20%26%20Maintained-orange" alt="Status">
</p>

---

### 📌 About This Repository

This repository is a preserved and actively maintained mirror of **Aiobale** (originally created by [Alireza Jahani](https://github.com/enalite)).

On **August 19, 2026**, the original repository was removed by the author and replaced on PyPI with an empty placeholder package. Since this was one of the cleanest reverse-engineered asynchronous clients for Bale Messenger's internal API, this repository has been restored and prepared with ready-to-use installation files so the community can continue using and developing it.

Further maintenance, bug fixes, protocol updates, and feature enhancements will be applied directly to this repository moving forward.

---

## 🚀 Why Aiobale?

Bale Messenger's API can be a maze of encrypted gRPC calls. **Aiobale** cuts through the noise:

- **Async-first, fully non-blocking**, built on `aiohttp` and `asyncio`.
- **Type-safe** Python classes for messages, users, groups, and more powered by `pydantic`.
- **Event-driven Dispatcher** for clean, modular bot code.
- **Handles connections**, reconnections, and multi-client setups effortlessly.
- **Reverse-engineered**, zero reliance on `.proto` files.

**In short:** Build bots, automation, or monitoring tools **without wrestling with low-level network details**.

---

## ✨ Features

- **Async & High Performance:** Responsive bots and automation pipelines.
- **Complete API Coverage:** Messaging, files, presence, bots, groups, channels.
- **Pythonic Interface:** Type hints, dataclasses, clean methods.
- **Smart Dispatcher:** Decorator-based event routing, multiple clients support.
- **Robust Connections:** Auto-reconnects, handles disconnects gracefully.
- **Extensible & Modular:** Easy to adapt and extend for custom workflows.

---

## ⚠️ Important Notes

- Bale’s API is sensitive to excessive POST gRPC calls, especially outside authentication. Overuse may trigger **rate limits** or temporary account bans.
- Use Aiobale responsibly — **no spamming, scraping, or TOS violations**.
- Aiobale is **unofficial** and provided **as-is** for educational and ethical purposes.

---

## 📦 Installation

#### Direct via Git
```bash
pip install git+https://github.com/aminmadaniofficial/aiobale-revived.git

```

#### Clone and Install Locally

```bash
git clone https://github.com/aminmadaniofficial/aiobale-revived.git
cd aiobale-revived
pip install .

```

#### Direct Wheel Package (Releases)

```bash
pip install https://github.com/aminmadaniofficial/aiobale-revived/releases/download/v0.1.5/aiobale-0.1.5-py3-none-any.whl

```

---

## 💡 Quick Start — Echo Bot

```python
from aiobale import Client, Dispatcher
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp)

@dp.message()
async def echo(msg: Message):
    if content := msg.document:
        await msg.answer_document(content, use_own_content=True)
    elif text := msg.text:
        await msg.answer(text)
    else:
        await msg.answer("Nothing to echo!")

client.run()

```

---

## 🧑‍💻 Contributing

We welcome contributions of all kinds:

* ⭐ Star the repo
* 🐞 Report bugs or request features via Issues
* 🧩 Submit pull requests (code, docs, tests)
* ✍️ Help document unknown methods or structures

Every contribution counts — even small fixes make a difference.

---

## 📄 License & Credits

* **Original Author:** Alireza Jahani ([@enalite](https://github.com/enalite))
* **Maintained by:** Mohammadamin Madani ([@aminmadaniofficial](https://github.com/aminmadaniofficial))
* **License:** [MIT License](https://github.com/aminmadaniofficial/aiobale-revived/blob/main/LICENSE)
