from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_db
from constants.texts import WALLET_TEXT

async def wallet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = str(query.from_user.id)
    db = load_db()
    user = db["users"].get(uid)
    if not user:
        await query.edit_message_text("User not found. Send /start")
        return
    text = WALLET_TEXT.format(balance=user.get("wallet", 0))
    await query.edit_message_text(text)