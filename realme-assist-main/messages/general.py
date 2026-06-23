import os
import re
import requests
from bs4 import BeautifulSoup
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from serpapi import GoogleSearch
# Added SERPAPI_KEY to your config imports
from config import VERIFIED_USERS, CONTROL_GROUP, OFFTOPIC_GROUP, SUPPORT_GROUP, ADMINS, SERPAPI_KEY

from utils import delay_group, delay_group_preview, delay_html, remove_message, schedule_delete

def search_realme_model(rmx_code):
    """Dynamically searches Google via SerpApi to find the phone name for an RMX code."""
    params = {
        "engine": "google",
        "q": f"Realme {rmx_code} gsmarena",
        "api_key": SERPAPI_KEY
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        
        if organic_results:
            title = organic_results[0].get("title", "")
            
            # 1. Chop off website names (like "- GSMArena")
            clean_title = title.split('|')[0].split('-')[0]
            
            # 2. Remove the RMX code and its parentheses
            clean_title = re.sub(rf'\(?{rmx_code}\)?', '', clean_title, flags=re.IGNORECASE)
            
            # 3. Strip out expanded junk words
            junk_words = [
                r"specs?", r"review", r"price", r"release date", r"gsmarena", 
                r"kimovil", r"unboxing", r"technical", r"specifications", r"full", r"phone"
            ]
            for word in junk_words:
                clean_title = re.sub(rf'(?i)\b{word}\b', '', clean_title)
            
            # 4. Clean up any leftover double spaces and return!
            return re.sub(r'\s+', ' ', clean_title).strip()
                
    except Exception as e:
        print(f"SerpApi search failed for {rmx_code}: {e}")
        
    return "Unknown Realme Device"

def banana(update: Update, context: CallbackContext):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "resources", "where_update.png")
    
    with open(file_path, "rb") as photo_file:
        msg = update.message.reply_photo(photo=photo_file, caption="Where update? 🍌")
        schedule_delete(context, msg.chat_id, msg.message_id)
        schedule_delete(context, update.message.chat_id, update.message.message_id)

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
    """Scans the message for RMX codes and searches them online."""
    text = update.effective_message.text.upper()
    
    # Strictly hunts for Realme (RMX) models only
    matches = set(re.findall(r'(?:RMX\d{4})', text))
    
    if matches:
        # Send a typing indicator while the bot browses the web
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        
        response = "📱 <b>Realme Devices Detected:</b>\n\n"
        for match in matches:
            device_name = search_realme_model(match)
            response += f"• <b>{match}</b> : {device_name}\n"
            
        msg = update.message.reply_text(response, parse_mode=ParseMode.HTML)
        schedule_delete(context, msg.chat_id, msg.message_id)

def cool(update: Update, context: CallbackContext):
    delay_html(update, context, "cool")

def polls(update: Update, context: CallbackContext):
    update.message.reply_text("Current polls: None 📊")

def private_not_available(update: Update, context: CallbackContext):
    update.message.reply_text("This command is not available in private chat.")

def benchmark(update: Update, context: CallbackContext):
    text = open("strings/benchmark.html", encoding="utf-8").read()
    
    norm_text = """Hey {} 🤖\n{}"""
    veri_text = (
        "Hey {} 🤖\n"
        "Pretty cool that you got the latest Update!"
        "\nBefore you update to a newer version, please do "
        "some benchmarks first to be able to compare what "
        "\n{}"
    )
    if update.message.reply_to_message and update.message.from_user.id in VERIFIED_USERS:
        delay_group(update, context, veri_text.format(update.message.reply_to_message.from_user.name, text))
    else:
        delay_group(update, context, norm_text.format(update.message.from_user.name, text))

import time
import config
from google import genai
from google.genai import types

GEMINI_API_KEY = getattr(config, "GEMINI_API_KEY", None)
ai_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def chat_with_gemini(update: Update, context: CallbackContext):
    if not update.message or not update.message.text:
        return
    if not ai_client:
        print("AI initialization skipped: GEMINI_API_KEY is missing from config.")
        return

    bot_username = f"@{context.bot.username}"
    user_text = update.message.text.replace(bot_username, "").strip()

    # Tell the user the bot is typing
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # === SMART RETRY LOOP ===
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_text,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are Realme Assist, a super-intelligent, witty AI assistant. "
                        "CRITICAL RULE: You are ONLY allowed to answer questions and discuss topics "
                        "related to Information Technology (IT), tech, smartphones, software, programming, "
                        "and Android/Realme UI. If a user asks about anything outside of IT, politely decline "
                        "and tell them to look it up on a search engine instead. Keep your response brief."
                    )
                )
            )
            # If successful, send message and break out of the loop
            update.message.reply_text(response.text, parse_mode=ParseMode.MARKDOWN)
            break 
            
        except Exception as e:
            error_message = str(e)
            print(f"Attempt {attempt + 1} failed: {error_message}")
            
            # If it's a 503 overload, wait 2 seconds and try again
            if "503" in error_message and attempt < max_retries - 1:
                time.sleep(2)
                continue
                
            # If it's a different error OR we ran out of retries, let the user know gently
            if attempt == max_retries - 1:
                update.message.reply_text("My brain servers are experiencing a massive traffic jam right now! 🚦 Give me a few minutes and try again.")
            break
