import time
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, Update
from telegram.ext import CallbackContext
from config import ADMINS
from constants import WARNINGS, DEVICES


def delay_group(update, context, text):
    update.message.reply_text(text)


def delay_group_preview(update, context, text):
    update.message.reply_text(text)


def remove_message(update, context):
    pass


def message_button_url(update, context, text, url):
    keyboard = [[InlineKeyboardButton("Click Here", url=url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, reply_markup=reply_markup)


def delete(update, context):
    """
    Deletes the message that triggered the command.
    """
    try:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")


# --- THE FIXED FUNCTIONS ---

def delay_html(update: Update, context: CallbackContext, path: str):
    file_content = open(f"strings/{path}.html", encoding="utf-8").read()
    
    if update.message.reply_to_message is not None and update.message.reply_to_message.from_user.name != "Telegram":
        delay_group(update, context, f"Hey {update.message.reply_to_message.from_user.name} 🤖\n\n" + file_content)
        return
    
    # If it's a normal direct command, just send the text!
    delay_group(update, context, file_content)


def delay_group_button_url(update, context, text, button_text, button_url):
    # Now it dynamically uses the text and URL you passed from support.py!
    keyboard = [[InlineKeyboardButton(button_text, url=button_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Check if it's a reply first
    if update.message.reply_to_message:
        update.message.reply_to_message.reply_text(text, reply_markup=reply_markup)
    else:
        # If it's a direct command, reply normally
        update.message.reply_text(text, reply_markup=reply_markup)