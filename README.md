# 📱 realme Assist Bot

A 24/7 Telegram bot built with Python to manage, support, and entertain the community. 

## ✨ What It Does Now
* **Community Support:** Manages user queries and routes support features.
* **Admin Controls:** Secure control commands for group administrators.
* **Always Online:** Hosted 24/7 in the cloud with an active database connection.

## 🛠️ Tech Stack
* **Language:** Python 3.10
* **Framework:** `python-telegram-bot`
* **Database:** PostgreSQL
* **Hosting:** Railway.app

## 📁 Project Structure
* `main.py` — The core script that initializes the bot and connects to the database.
* `/messages/` — Contains all the modular command logic (`general.py`, `support.py`, `offtopic.py`, `control.py`).
* `/resources/` — Stores images and media used by the bot.

## 🚀 How to Run Locally
If you are cloning this project to test on your own Windows machine:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
