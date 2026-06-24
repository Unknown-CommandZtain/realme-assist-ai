import time
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, Update
from telegram.ext import CallbackContext
from config import ADMINS

def delete_job(context: CallbackContext):
    """Background worker that actually deletes the messages."""
    job = context.job
    chat_id = job.context['chat_id']
    message_id = job.context['message_id']
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass # Ignores errors if the message was already deleted by an admin

def schedule_delete(context: CallbackContext, chat_id, message_id, delay=600):
    """Helper to queue messages for deletion after 10 minutes (600s)."""
    context.job_queue.run_once(delete_job, delay, context={'chat_id': chat_id, 'message_id': message_id})

def delay_group(update: Update, context: CallbackContext, text: str):
    msg = update.message.reply_text(text, parse_mode=ParseMode.HTML)
    # Schedule deletion for BOTH the bot's response and the user's command
    schedule_delete(context, msg.chat_id, msg.message_id)
    schedule_delete(context, update.message.chat_id, update.message.message_id)

def delay_group_preview(update: Update, context: CallbackContext, text: str):
    msg = update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=False)
    schedule_delete(context, msg.chat_id, msg.message_id)
    schedule_delete(context, update.message.chat_id, update.message.message_id)

def remove_message(update: Update, context: CallbackContext):
    """Immediately deletes forbidden text triggered by the regex filter."""
    try:
        update.message.delete()
    except Exception:
        pass

def message_button_url(update: Update, context: CallbackContext, text: str, url: str):
    keyboard = [[InlineKeyboardButton("Click Here", url=url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    schedule_delete(context, msg.chat_id, msg.message_id)
    schedule_delete(context, update.message.chat_id, update.message.message_id)

def delete(update: Update, context: CallbackContext):
    """Immediate manual deletion."""
    try:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")

def delay_html(update: Update, context: CallbackContext, path: str):
    file_content = open(f"strings/{path}.html", encoding="utf-8").read()
    
    if update.message.reply_to_message is not None and update.message.reply_to_message.from_user.name != "Telegram":
        msg = update.message.reply_text(f"Hey {update.message.reply_to_message.from_user.name} 🤖\n\n" + file_content, parse_mode=ParseMode.HTML)
        schedule_delete(context, msg.chat_id, msg.message_id)
        schedule_delete(context, update.message.chat_id, update.message.message_id)
        return
    
    delay_group(update, context, file_content)

def delay_group_button_url(update: Update, context: CallbackContext, text: str, button_text: str, button_url: str):
    keyboard = [[InlineKeyboardButton(button_text, url=button_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message.reply_to_message:
        msg = update.message.reply_to_message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        msg = update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    schedule_delete(context, msg.chat_id, msg.message_id)
    schedule_delete(context, update.message.chat_id, update.message.message_id)
