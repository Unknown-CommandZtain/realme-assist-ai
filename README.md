# 🤖 Realme Assist AI Bot

A 24/7 multimodal AI Telegram bot built with Python to manage, support, and troubleshoot for the community. 

Originally a standard command-based bot, Realme Assist has been upgraded with **Google's Gemini 3.1 Flash-Lite**. It now acts as a super-intelligent tech support gatekeeper capable of reading screenshots, managing its own API traffic, and preventing off-topic spam.

## ✨ Core Features
* **🧠 Super-Intelligent IT Assistant:** Tuned strictly for tech support. The bot automatically detects and politely rejects off-topic queries (like recipes or sports), saving API limits for actual IT problems.
* **👁️ Multimodal Vision:** Users can send screenshots of Android battery drains, error popups, or broken code. The bot downloads the image, analyzes it alongside the user's text, and diagnoses the problem instantly.
* **🚦 Auto-Healing Traffic Management:** Built with a custom Regex-powered Retry Loop. If the bot hits a global server overload or a rate limit during massive group spam, it intercepts Google's exact timeout request, puts the message to sleep, and successfully delivers it seconds later without crashing.
* **🛡️ Markdown Crash Protection:** Features a "Smart Fallback" that instantly intercepts Telegram parse errors and resends the message as raw text, guaranteeing zero failed deliveries.
* **🤫 Smart Group Privacy:** In private 1-on-1 chats, the bot is fully conversational. In massive group chats, it stays completely silent until explicitly tagged (e.g., `@YourBotName`), preventing API exhaustion.
* **👑 Admin & Legacy Controls:** Fully retains standard Telegram command structures (like `/bug`, `/debloat`) for instant, hard-coded template responses and secure group administrator tools.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** `python-telegram-bot` (v13)
* **AI Engine:** Google GenAI SDK (`gemini-3.1-flash-lite`)
* **Database:** PostgreSQL (with APScheduler)
* **Hosting:** Optimized for 24/7 containerized deployment on [Railway.app](https://railway.app/)

## 📁 Project Structure
* `main.py` — The core script that initializes the bot, database, and smart AI routing filters.
* `/messages/` — Contains all the modular logic:
  * `general.py` / `ai.py` — Houses the Gemini AI engine, vision processing, and smart retry loops.
  * `support.py` — Static support logic and routing.
  * `offtopic.py` — Standard text handling.
  * `control.py` — Admin and moderation tools.
* `/resources/` — Stores static images and media used by the bot.
