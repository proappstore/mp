from telegram import Update
from telegram.ext import ContextTypes
from constants.texts import HELP_TEXT

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(HELP_TEXT)