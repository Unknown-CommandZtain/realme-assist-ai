"""
This file contains the actions that will happen once a command is called.
These are messages that can appear in both groups or in private.
"""

from telegram import Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from config import VERIFIED_USERS, CONTROL_GROUP, OFFTOPIC_GROUP, SUPPORT_GROUP, ADMINS

from utils import delay_group, delay_group_preview, delay_html, remove_message

def banana(update: Update, context: CallbackContext):
    # Using your exact local path (the 'r' prevents backslash errors)
    file_path = r"C:\Users\Unknown_CommandZtain\Documents\realme Assist\resources\where_update.png"
    
    with open(file_path, "rb") as photo_file:
        update.message.reply_photo(
            photo=photo_file,
            caption="Where update? 🍌"
        )

def realistic(update: Update, context: CallbackContext):
    delay_html(update, context, "realistic")

def rules(update: Update, context: CallbackContext):
    delay_html(update, context, "onrules")

def about(update: Update, context: CallbackContext):
    delay_html(update, context, "about")

def ban(update: Update, context: CallbackContext):
    update.message.reply_text("Ban hammer goes bonk! 🔨")

def warn(update: Update, context: CallbackContext):
    update.message.reply_text("Warning issued! ⚠️")

def unwarn(update: Update, context: CallbackContext):
    update.message.reply_text("Warning removed! ✅")

def info(update: Update, context: CallbackContext):
    update.message.reply_text("User information retrieved. ℹ️")

def resolve_model(update: Update, context: CallbackContext):
    update.message.reply_text("Model resolved! 📱")

def cool(update: Update, context: CallbackContext):
    delay_html(update, context, "cool")

def polls(update: Update, context: CallbackContext):
    update.message.reply_text("Current polls: None 📊")

def private_not_available(update: Update, context: CallbackContext):
    update.message.reply_text("This command is not available in private chat.")

def benchmark(update: Update, context: CallbackContext):
    """Handle for /benchmark."""
    text = open("strings/benchmark.html", encoding="utf-8").read()
    
    norm_text = """Hey {} 🤖\n{}"""
    veri_text = (
        "Hey {} 🤖\n"
        "Pretty cool that you got the latest Update!"
        "\nBefore you update to a newer version, please do "
        "some benchmarks first to be able to compare what "
        "\n{}"
    )
    if (
            update.message.reply_to_message
            and update.message.from_user.id in VERIFIED_USERS
    ):
        delay_group(
            update,
            context,
            veri_text.format(update.message.reply_to_message.from_user.name, text),
        )

    else:
        delay_group(
            update, context, norm_text.format(update.message.from_user.name, text)
        )