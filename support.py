"""These messages are meant to be sent in support group (@realme_support) only."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext

from config import ADMINS, OFFTOPIC_GROUP
from utils import (
    delay_group,
    message_button_url,
    delete,
    delay_group_button_url,
    delay_group_preview, delay_html,
)


def ask(update: Update, context: CallbackContext):
    delay_html(update, context, "ask")

def commands(update: Update, context: CallbackContext):
    delay_html(update, context, "commands")

def gcam(update: Update, context: CallbackContext):
    delay_html(update, context, "gcam")

def cleaners(update: Update, context: CallbackContext):
    delay_html(update, context, "cleaners")

def aod(update: Update, context: CallbackContext):
    delay_html(update, context, "aod")

def manual(update: Update, context: CallbackContext):
    delay_html(update, context, "manual")

def apk(update: Update, context: CallbackContext):
    delay_html(update, context, "apk")

def form(update: Update, context: CallbackContext):
    # Added encoding safety wrapper here too!
    delay_group_button_url(update, context, open("strings/form.html", encoding="utf-8").read(), button_text="Access form 📝",
                           button_url="https://docs.google.com/forms/d/e/1FAIpQLSceGI9ZaNOIb4NN-3UdJ-mbzvbRwulAh2-VGJasy8VU_BLsFA/viewform")

def bug(update: Update, context: CallbackContext):
    delay_html(update, context, "bug")

def battery(update: Update, context: CallbackContext):
    delay_html(update, context, "battery")

def stable(update: Update, context: CallbackContext):
    delay_html(update, context, "stable")

def push(update: Update, context: CallbackContext):
    delay_html(update, context, "push")

def ram(update: Update, context: CallbackContext):
    delay_html(update, context, "ram")

def rant(update: Update, context: CallbackContext):
    delay_html(update, context, "rant")

def whatsapp(update: Update, context: CallbackContext):
    update.message.delete()
    text = (
        "You can contact the official support directly on WhatsApp:"
        "\n\n+919711012312 🆕"
    )
    button_text = "Message Support 💬"
    button_url = "https://wa.me/+919711012312"

    if update.message.reply_to_message:
        update.message.reply_to_message.reply_text(
            "Hey {} 🤖\n\n".format(update.message.reply_to_message.from_user.name)
            + text,
            ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(button_text, button_url)
            ),
        )
    else:
        reply_message = context.bot.send_message(
            update.message.chat_id,
            text,
            ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(button_text, button_url)
            ),
        )
        context.job_queue.run_once(
            delete, 600, reply_message.chat_id, str(reply_message.message_id)
        )

def move_to_offtopic(update: Update, context: CallbackContext):
    if (
            update.message.reply_to_message is not None
            and update.message.from_user.id in ADMINS
    ):
        update.message.delete()
        original_msg = update.message.reply_to_message.copy(
            OFFTOPIC_GROUP,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Original Message ➡️",
                            url=update.message.reply_to_message.link
                        )
                    ]
                ]
            ),
        )
        moved_link = "https://t.me/realme_offtopic/" + str(original_msg.message_id)
        message_button_url(
            update,
            context,
            "Hey {} 🤖"
            "\n\nThis is getting pretty off-topic now."
            "\n\nI moved the message to @realme_offtopic"
            "\n\nPlease continue the discussion there.".format(
                update.message.reply_to_message.from_user.name
            ),
            "Continue here 😉",
            moved_link
        )
    else:
        delay_group(
            update,
            context,
            "Hey guys 🤖"
            "\n\nFeel free to join @realme_offtopic to discuss topics "
            "not related to Realme or Android."
            "\n\nYou can also send Links and Stickers there 🥳"
        )

# FIXED: Added explicit UTF-8 decoding to read modern characters perfectly
def android16(update: Update, context: CallbackContext):
    """Handle for /android16."""
    delay_group_preview(update, context, open("strings/android16.html", encoding="utf-8").read())

def debloat(update: Update, context: CallbackContext):
    delay_html(update, context, "debloat")

def fps(update: Update, context: CallbackContext):
    delay_html(update, context, "fps")

def fooview(update: Update, context: CallbackContext):
    delay_html(update, context, "fooview")

def swap(update: Update, context: CallbackContext):
    delay_html(update, context, "swap")

def charge(update: Update, context: CallbackContext):
    delay_html(update, context, "charge")

def miss(update: Update, context: CallbackContext):
    delay_html(update, context, "miss")

def eol(update: Update, context: CallbackContext):
    delay_html(update, context, "eol")

def rumor(update: Update, context: CallbackContext):
    delay_html(update, context, "rumor")