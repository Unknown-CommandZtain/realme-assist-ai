"""
This file serves as an entry point to the program.

Here all the stuff is initialized and updates being handled.
"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from telegram import Update, ParseMode
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater, Defaults,
)

import config
from constants import FORBIDDEN_TEXT
from messages.control import clear, reset
from messages.general import (
    banana,
    benchmark,
    cool,
    polls,
    private_not_available,
    realistic,
    rules, about, ban, warn, unwarn, resolve_model, info
)
from messages.offtopic import (
    move_to_support
)
from messages.support import (
    android16,
    aod,
    apk,
    ask,
    battery,
    bug,
    cleaners,
    commands,
    debloat,
    form,
    fps,
    gcam,
    manual,
    move_to_offtopic,
    push,
    ram,
    rant,
    stable,
    whatsapp, fooview, swap, charge, miss, eol, rumor
)
from postgres import PostgresPersistence
from utils import remove_message
from messages.general import chat_with_gemini

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start_session() -> scoped_session:
    """Start the database session."""
    engine = create_engine(config.DATABASE_URL)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


def error(update: Update, context: CallbackContext):
    """Log the error to control group."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    if update is Update:
        context.bot.send_message(
            config.CONTROL_GROUP,
            (
                "<b>🤖 Affected Bot</b>\n@{context.bot.username}\n\n"
                "<b>⚠️ Error</b>\n"
                "<code>{context.error}</code>\n\n"
                "<b>Caused by Update</b>\n"
                "<code>{update}</code>"
            )
        )


def start(update: Update, context: CallbackContext):
    """Handle the /start command."""
    update.message.reply_text(
        "Hello there! 🤖 Please check the command menu (usually at the bottom left of your screen) to explore all my available features."
    )


if __name__ == "__main__":
    session = start_session()

    updater = Updater(config.TOKEN, persistence=PostgresPersistence(session),
                      defaults=Defaults(parse_mode=ParseMode.HTML))
    dp = updater.dispatcher

    for i in FORBIDDEN_TEXT:
        dp.add_handler(MessageHandler(Filters.regex(r"(?i)" + i), remove_message))

    # General
    dp.add_handler(MessageHandler(Filters.regex(r"(?i)(?:(?!/)rmx\d{4})"), resolve_model))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cleaners", cleaners))
    dp.add_handler(CommandHandler("cool", cool))
    dp.add_handler(CommandHandler("gcam", gcam))
    dp.add_handler(CommandHandler("polls", polls))
    dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("warn", warn))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("unwarn", unwarn))
    dp.add_handler(CommandHandler("ban", ban))

    # Support (REMOVED GROUP FILTERS)
    dp.add_handler(CommandHandler("android16", android16))
    dp.add_handler(CommandHandler("aod", aod))
    dp.add_handler(CommandHandler("apk", apk))
    dp.add_handler(CommandHandler("ask", ask))
    dp.add_handler(CommandHandler("eol", eol))
    dp.add_handler(CommandHandler("rumor", rumor))

    dp.add_handler(CommandHandler("battery", battery))
    dp.add_handler(CommandHandler("benchmark", benchmark))
    dp.add_handler(CommandHandler("bug", bug))
    dp.add_handler(CommandHandler("debloat", debloat))
    dp.add_handler(CommandHandler("form", form))
    dp.add_handler(CommandHandler("help", commands))
    dp.add_handler(CommandHandler("manual", manual))
    dp.add_handler(CommandHandler("offtopic", move_to_offtopic))
    dp.add_handler(CommandHandler("push", push))
    dp.add_handler(CommandHandler("stable", stable))
    dp.add_handler(CommandHandler("fooview", fooview))
    dp.add_handler(CommandHandler("swap", swap))
    dp.add_handler(CommandHandler("charge", charge))
    dp.add_handler(CommandHandler("whatsapp", whatsapp))
    dp.add_handler(CommandHandler("miss", miss))

    # Personal opinion (REMOVED GROUP FILTERS)
    dp.add_handler(CommandHandler("fps", fps))
    dp.add_handler(CommandHandler("ram", ram))
    dp.add_handler(CommandHandler("rant", rant))

    # Offtopics (REMOVED GROUP FILTERS)
    dp.add_handler(CommandHandler("support", move_to_support))

    # Control (Kept Admin filters but removed chat group filter)
    dp.add_handler(CommandHandler("clear", clear, Filters.user(config.ADMINS)))
    dp.add_handler(CommandHandler("reset", reset, Filters.user(config.ADMINS)))

   # Crap
    dp.add_handler(CommandHandler("banana", banana))
    dp.add_handler(CommandHandler("realistic", realistic))

    # ====== SMART GEMINI FILTER ======
    from telegram.ext import MessageHandler, Filters

    # Trigger rule 1: It's a private chat
    private_filter = Filters.chat_type.private

    # Trigger rule 2: It's a group, AND the bot's username is explicitly mentioned/tagged
    group_mention_filter = (Filters.chat_type.groups | Filters.chat_type.supergroup) & Filters.entity("mention")

    # Combine them: Fire the AI if it's a normal text message in Private OR a Mention in Groups
    dp.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command & (private_filter | group_mention_filter), 
            chat_with_gemini
        )
    )

    # Commands have been set up, start polling
    updater.start_polling()
    updater.idle()
