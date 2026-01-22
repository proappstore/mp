from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from utils.storage import ensure_user, save_db, load_db
import constants.buttons as buttons
import constants.texts as texts
import json

def build_menu():
    kb = [
        [InlineKeyboardButton("Help", callback_data="menu:help")],
        [InlineKeyboardButton("Buy Orders", callback_data="menu:buy")],
        [InlineKeyboardButton("Orders History", callback_data="menu:history")],
        [InlineKeyboardButton("Wallet", callback_data="menu:wallet")],
        [InlineKeyboardButton("UPI ID Setup", callback_data="menu:upi")],
    ]
    return InlineKeyboardMarkup(kb)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user is None:
        return
    ensure_user(str(user.id), user.full_name)
    await update.message.reply_text(texts.WELCOME.format(name=user.full_name), reply_markup=build_menu())

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # If user clicked menu, re-show the same menu
    await query.edit_message_text("Choose an option:", reply_markup=build_menu())
