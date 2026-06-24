"""These messages are meant to be sent in control group only."""

import os
from telegram import Update
from telegram.ext import CallbackContext

# This grabs your secret ID from Railway
# We use int() because Telegram IDs are numbers, but environment variables are text
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

def clear(update: Update, context: CallbackContext):
    # 1. Check who sent the message
    user_id = update.effective_user.id
    
    # 2. The Bouncer: If their ID doesn't match yours, kick them out
    if user_id != ADMIN_ID:
        update.message.reply_text("⛔ You are not authorized to use this command.")
        return # This instantly stops the code from running further
        
    # 3. If it IS you, run the actual command!
    update.message.reply_text("Authorization accepted. Clearing data...")
    # (The rest of your clear code goes here)

from config import CONTROL_GROUP, SUPPORT_GROUP


def clear(update: Update, context: CallbackContext):
    """Clear commands."""

    context.bot.delete_my_commands(BotCommandScopeChat(SUPPORT_GROUP))

    context.bot.set_my_commands(
        [
            ("clear", "Clears commands and temporary user data."),
            ("reset", "Resets commands. Use if after clearing."),
        ],
        scope=BotCommandScopeChat(CONTROL_GROUP),
    )

    update.message.reply_text("Command lists were cleared.")


def reset(update: Update, context: CallbackContext):
    """Reset commands."""

    admin_commands = [
        ("warn", "Warn a user"),
        ("unwarn", "Reduce the warnings for a user"),
        ("info", "Get information about a user")
    ]

    support_commands = [
        ("android16", "Official UI 7.0 / Android 16 roadmap 📲"),
        ("gcam", "Latest release and configurations 📷"),
        ("cleaners", "The recommended cleaning apps ♻️"),
        ("whatsapp", "Message the support directly 💬"),
        ("bug", "How to report a bug ⚠️"),
        ("stable", "Estimate the stable release date 📆"),
        ("push", "How an update is pushed 🅿️"),
        ("debloat", "Guide to remove unwanted apps 🚫"),
        ("battery", "Keep your battery healthy 🔋"),
        ("polls", "Take a look at our current polls 📊"),
        ("benchmark", "How to benchmark your device 💪🏼"),
        ("cool", "Cool and useful Apps 😎"),
        ("aod", "Why there is no Customization or AOD 🎨"),
        ("ram", "Virtual Ram performance 💾"),
        ("manual", "Manual updates may be worse 😟"),
        ("apk", "Why an Apk fails to install 🚫"),
        ("rules", "Show this group's rules 📜"),
        ("ask", "How to ask questions properly ❓"),
        ("help", "Show commands 🆘"),
        ("about", "Information about this Bot 🤖")
    ]

    context.bot.set_my_commands(support_commands, scope=BotCommandScopeChat(SUPPORT_GROUP))

    context.bot.set_my_commands(support_commands + [
        ("realistic", "If people expect to much"),
        ("fps", "Games are demanding"),
        ("banana", "Where update?"),
        ("rant", "Why updates don't have dates"),
        ("offtopic", "Move messages to Off-Topic ➡️")
    ] + admin_commands, scope=BotCommandScopeChatAdministrators(SUPPORT_GROUP))

    update.message.reply_text("Command list was updated.")
